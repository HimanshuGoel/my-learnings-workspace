# Multimodal RAG

## What This Enables

Standard RAG only handles clean text. But real documents have tables, charts, diagrams, code screenshots, and mixed layouts. Multimodal RAG extends your pipeline to handle PDFs, presentations, and scanned documents — extracting information from BOTH text and visual elements, then retrieving the right pieces for answering questions.

## Architecture Overview

### Three Approaches to Multimodal RAG

```
Approach 1: Extract-then-embed (convert everything to text)
  PDF → Extract text + OCR images + describe charts with VLM → Embed text → Standard RAG
  Pros: Simplest, works with existing text-only RAG pipeline
  Cons: Loses visual structure, VLM descriptions may miss details

Approach 2: Multi-modal embeddings (embed images directly)
  PDF → Extract text chunks + image chunks separately
  → Embed text with text model, embed images with CLIP/multi-modal model
  → Store both in same vector space → Retrieve text OR image chunks
  Pros: Preserves visual information, retrieves actual images
  Cons: More complex, multi-modal embedding quality varies

Approach 3: Late fusion (retrieve text, send images to VLM at generation time)
  PDF → Extract text chunks + save images with metadata
  → Retrieve relevant text chunks → Also attach related images
  → Send text chunks + images to VLM for answer generation
  Pros: Best quality (VLM sees actual images), flexible
  Cons: Most expensive (VLM token cost), higher latency
```

### Recommended Architecture

```
                    ┌─── Text chunks ──→ Text Embeddings ──→ Vector Store
PDF/Doc ──→ Parse ──┤
                    └─── Images/Tables ──→ VLM Description ──→ Text Embeddings ──→ Vector Store
                              │                                        ↑
                              └── Store original image (for late fusion) ─┘

At query time:
  Query → Retrieve top-K (includes image descriptions) → Attach original images → VLM generates answer
```

## Key Patterns & When to Use Each

| Pattern | When to Use | Quality | Cost | Complexity |
|---------|-------------|---------|------|-----------|
| Text-only extraction (OCR + layout) | Simple docs, mostly text | Medium | Low | Low |
| VLM description + text RAG | Charts, diagrams that need interpretation | High | Medium | Medium |
| Multi-modal embeddings (CLIP) | Image-heavy content, visual search | Medium | Low | High |
| Late fusion (images sent to VLM) | Maximum quality needed | Highest | High | Medium |
| Hybrid (text retrieval + image attachment) | Real-world documents (mix of everything) | High | Medium | Medium |

## Implementation with LangChain

### Step 1: Document Parsing (Unstructured / docling)

```python
from unstructured.partition.pdf import partition_pdf

# Parse PDF with element detection (text, tables, images)
elements = partition_pdf(
    filename="document.pdf",
    strategy="hi_res",                # Use layout detection model
    extract_images_in_pdf=True,       # Extract embedded images
    infer_table_structure=True,       # Detect and structure tables
    include_page_breaks=True,
)

# Elements are typed: NarrativeText, Table, Image, Title, ListItem, etc.
text_elements = [e for e in elements if e.category in ("NarrativeText", "Title", "ListItem")]
table_elements = [e for e in elements if e.category == "Table"]
image_elements = [e for e in elements if e.category == "Image"]
```

### Step 2: Process Tables and Images with VLM

```python
import base64
from openai import OpenAI

client = OpenAI()

def describe_image_for_rag(image_path: str, context: str = "") -> str:
    """Use VLM to create a text description of an image for embedding."""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cheaper model for descriptions
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": f"""Describe this image in detail for a search index.
Include: all text visible, data values, relationships shown, key takeaways.
Document context: {context}
Be specific and factual — this description will be used for retrieval."""},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            ],
        }],
        max_tokens=500,
    )
    return response.choices[0].message.content


def process_table_element(table_html: str) -> str:
    """Convert table to searchable text representation."""
    # Option 1: Keep as markdown table (good for embedding)
    # Option 2: Describe with LLM for better semantic search
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Summarize this table's key information in 2-3 sentences, "
                       f"including notable values and trends:\n\n{table_html}",
        }],
    )
    return response.choices[0].message.content
```

### Step 3: Build the Multimodal Index

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

documents = []

# Text chunks (standard)
for elem in text_elements:
    documents.append(Document(
        page_content=elem.text,
        metadata={"type": "text", "page": elem.metadata.page_number, "source": "doc.pdf"},
    ))

# Table descriptions (with original HTML in metadata)
for elem in table_elements:
    description = process_table_element(elem.metadata.text_as_html)
    documents.append(Document(
        page_content=description,
        metadata={
            "type": "table",
            "page": elem.metadata.page_number,
            "original_html": elem.metadata.text_as_html,  # Keep original for generation
            "source": "doc.pdf",
        },
    ))

# Image descriptions (with path to original image)
for elem in image_elements:
    description = describe_image_for_rag(elem.metadata.image_path)
    documents.append(Document(
        page_content=description,
        metadata={
            "type": "image",
            "page": elem.metadata.page_number,
            "image_path": elem.metadata.image_path,  # Keep for late fusion
            "source": "doc.pdf",
        },
    ))

# Index everything
vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="./multimodal_db")
```

### Step 4: Multimodal Retrieval + Generation

```python
def multimodal_rag_query(question: str, vectorstore, k: int = 5) -> str:
    """Retrieve multimodal context and generate answer with VLM."""
    # Retrieve relevant chunks (text, table descriptions, image descriptions)
    docs = vectorstore.similarity_search(question, k=k)
    
    # Build context: text + tables + attach actual images
    text_context = []
    images_to_send = []
    
    for doc in docs:
        if doc.metadata["type"] == "text":
            text_context.append(doc.page_content)
        elif doc.metadata["type"] == "table":
            text_context.append(f"[Table from page {doc.metadata['page']}]:\n{doc.metadata['original_html']}")
        elif doc.metadata["type"] == "image":
            text_context.append(f"[Image from page {doc.metadata['page']}]: {doc.page_content}")
            images_to_send.append(doc.metadata["image_path"])
    
    # Generate answer with VLM (text + images)
    content = [{"type": "text", "text": f"Context:\n{'---'.join(text_context)}\n\nQuestion: {question}"}]
    
    # Attach up to 3 relevant images (cost control)
    for img_path in images_to_send[:3]:
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}})
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Answer based on the provided context and images. Cite sources."},
            {"role": "user", "content": content},
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content
```

## State Management & Memory

- Image descriptions are cached (don't re-describe the same image)
- Original images stored on disk with metadata references in vector store
- For multi-turn: send image descriptions (text) in conversation, not raw images (saves tokens)
- Document version tracking: re-parse + re-describe only changed pages

## Error Handling & Guardrails

| Failure Mode | Symptom | Fix |
|-------------|---------|-----|
| PDF parsing misses tables | Tables appear as garbled text | Use `strategy="hi_res"` with layout model |
| Images not extracted | Empty image elements | Check PDF has embedded images (not just vector graphics) |
| VLM description too vague | "This is a chart" (unhelpful for retrieval) | Better prompt: "include all data values, axis labels, trends" |
| Wrong image retrieved | Image description matches query but image doesn't answer it | Add page context to description, improve embedding |
| Token budget blown | Multiple images + long text exceeds context | Limit to 2-3 images, summarize text context |
| OCR errors | Garbled text from scanned documents | Use dedicated OCR (Tesseract) + VLM verification |

## Testing & Debugging

```python
# Multimodal RAG test set needs: query + expected answer + source element type
multimodal_test_set = [
    {
        "query": "What was Q3 revenue according to the chart on page 5?",
        "expected_source_type": "image",  # Should retrieve the chart
        "expected_answer_contains": "$4.2M",
    },
    {
        "query": "What are the system requirements?",
        "expected_source_type": "table",  # Should retrieve the requirements table
        "expected_answer_contains": "16 GB RAM",
    },
]

# Debug strategy: Check which elements were retrieved
# If wrong type → embedding/description quality issue
# If right type but wrong answer → generation/context assembly issue
```

## Production Considerations

### Cost
- VLM description generation: ~$0.01-0.05 per image (one-time, at index time)
- Late fusion at query time: ~$0.01-0.05 per query with images
- Total per document (50-page PDF with 20 images): ~$0.50-1.00 to index
- Query cost: ~$0.005 (text only) to $0.05 (with image attachment)

### Latency
- Document parsing: 10-60s per PDF (depends on complexity)
- Image description: 2-5s per image (at index time, not query time)
- Query with image attachment: 3-8s (VLM processing images)
- Query text-only: 1-3s (same as standard RAG)

### Scaling
- Pre-process documents asynchronously (background job)
- Cache image descriptions (never re-describe unchanged images)
- Use cheaper models for description (gpt-4o-mini), better models for generation (gpt-4o)
- For high-volume: batch image description with rate limiting

## Integration Points

- **Module 2 (RAG):** This IS RAG, extended for multimodal. Same retrieval/reranking patterns apply.
- **Module 4 (Agents):** Agent can use multimodal RAG as a tool ("search documents including figures")
- **Capstone:** Document understanding pipeline is a natural capstone project

## Architecture Decision Record

**Decision:** Use "VLM description + text RAG + late fusion for top results" (hybrid approach).

**Why:** Pure text extraction loses too much from charts/diagrams. Pure multi-modal embeddings aren't reliable enough yet. The hybrid gives good retrieval (via text descriptions) PLUS high-quality answers (via sending actual images to VLM at generation time).

**Trade-off accepted:** Higher indexing cost ($0.01-0.05 per image for descriptions), higher query cost when images are involved. Worth it for document QA quality.

**When to reconsider:** If multi-modal embedding models (like newer CLIP variants) reach text-embedding-3-small quality for cross-modal retrieval, can simplify to pure embedding approach.
