# Chunking Strategies

## The Problem You're Solving

Your RAG system retrieves wrong or partially-relevant passages because documents were split at arbitrary boundaries — mid-sentence, mid-paragraph, or at sizes that either lose context (too small) or dilute signal with noise (too big). Chunking strategy directly determines retrieval quality.

## Options Available

| Strategy | When to Use | Pros | Cons |
|----------|-------------|------|------|
| Fixed-size (token count) | Default starting point, unstructured text | Simple, predictable, fast | Cuts mid-sentence, ignores semantics |
| Fixed-size + overlap | Slightly better boundaries | Preserves context at edges | Duplicates content, more storage |
| Recursive character splitting | Documents with natural delimiters | Respects paragraphs/sections | Still arbitrary at leaf level |
| Sentence-based | Short-form content, FAQs | Clean semantic units | Often too small for context |
| Semantic chunking | Dense technical docs | Groups semantically similar text | Slower, embedding cost at index time |
| Document-structure-based | HTML, Markdown, code files | Preserves heading/function hierarchy | Requires parsing, format-specific |
| Agentic/LLM-based chunking | High-value, complex docs | Best boundary quality | Expensive, slow, non-deterministic |
| Parent-child (hierarchical) | Need both precision and context | Retrieve child, return parent for context | Complex indexing, more storage |

## Recommended Approach

**Start with Recursive Character Splitting (512 tokens, 50-token overlap) for general text. Switch to semantic or structure-based for specialized content.**

Why: Recursive splitting is the best default — it tries paragraph boundaries first, then sentence boundaries, then character boundaries. It's fast, deterministic, and works with LangChain out of the box. Optimize later based on retrieval quality metrics.

## Step-by-Step Implementation

### 1. Baseline: Recursive Character Splitting

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,          # tokens (approximate via characters: 512 * 4 ≈ 2048 chars)
    chunk_overlap=50,        # overlap to preserve boundary context
    separators=["\n\n", "\n", ". ", " ", ""],  # try these in order
    length_function=len,     # character-based; use tiktoken for exact token count
)

chunks = splitter.split_documents(documents)
```

### 2. Token-Exact Splitting (When Token Budget Matters)

```python
from langchain.text_splitter import TokenTextSplitter
import tiktoken

splitter = TokenTextSplitter(
    encoding_name="cl100k_base",  # GPT-4 tokenizer
    chunk_size=512,
    chunk_overlap=50,
)
```

### 3. Semantic Chunking (When Retrieval Quality Is Critical)

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",  # or "standard_deviation", "interquartile"
    breakpoint_threshold_amount=95,          # split when similarity drops below 95th percentile
)

chunks = splitter.split_documents(documents)
```

### 4. Markdown/HTML Structure-Based Splitting

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = splitter.split_text(markdown_content)
# Each chunk retains header metadata for filtering
```

### 5. Code-Specific Splitting

```python
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter

# Python-aware splitting (respects class/function boundaries)
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=1000,      # code needs more context per chunk
    chunk_overlap=100,
)
```

### 6. Parent-Child (Hierarchical) Strategy

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Small chunks for precise retrieval
child_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=30)

# Large chunks for context-rich answers
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)

# Store both; retrieve on child embeddings, return parent text to LLM
parent_chunks = parent_splitter.split_documents(documents)
for parent in parent_chunks:
    children = child_splitter.split_documents([parent])
    for child in children:
        child.metadata["parent_id"] = parent.metadata["id"]
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Chunk size | 512 tokens (general), 256 (precise retrieval), 1024 (code) | Balances retrieval precision vs context completeness |
| Overlap | 10-15% of chunk size (50-75 tokens) | Prevents losing context at boundaries |
| Separators priority | `\n\n` → `\n` → `. ` → ` ` → `""` | Respects natural document structure |
| Min chunk size | 100 tokens | Avoid trivially small chunks (headers alone) |
| Metadata to preserve | source, page, section heading, chunk_index | Essential for filtering and attribution |
| Encoding | cl100k_base (GPT-4) or model-specific | Exact token count prevents context window overflow |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Retrieved chunks lack sufficient context | Chunk size too small | Increase to 512-1024, or use parent-child |
| Retrieval returns irrelevant but high-similarity chunks | Chunk too large (noisy) | Decrease size, try semantic chunking |
| Answer misses info that's clearly in the document | Info split across chunk boundary | Increase overlap or use semantic chunking |
| Duplicate/near-duplicate chunks retrieved | Too much overlap | Reduce overlap, add dedup at retrieval |
| Code examples broken mid-function | Using general splitter on code | Switch to language-aware splitter |
| Tables split into meaningless rows | Row-level splitting | Custom table-aware parser, keep tables whole |
| Metadata lost after splitting | Splitter not preserving metadata | Ensure `split_documents()` (not `split_text()`) |

## Production Considerations

### Storage
- Each chunk stores: text + embedding vector + metadata
- 1000 pages ≈ 5000-10000 chunks at 512 tokens
- Storage cost is usually negligible vs compute

### Indexing Time
- Fixed/recursive: milliseconds per document
- Semantic: seconds per document (requires embedding computation)
- LLM-based: seconds to minutes per document

### Re-indexing
- When you change chunk strategy, you must re-embed everything
- Design for re-indexing from day one (keep source documents, automate pipeline)
- Version your chunking config alongside your code

### Monitoring
- Track: average chunk size distribution, chunks per document
- Alert on: chunks < 50 tokens (likely garbage), chunks > 2x target size (splitting failed)

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| Retrieval recall | % of relevant chunks in top-K | > 80% |
| Chunk coherence | Human eval: is chunk self-contained? | > 90% rated "makes sense alone" |
| Boundary quality | % of chunks cut mid-sentence | < 5% |
| Answer quality (downstream) | RAGAS faithfulness after changing chunking | Improvement over baseline |
| Duplicate rate | % near-duplicate chunks in corpus | < 3% |

## Ready to Ship? — Checklist

- [ ] Chunk size justified for your content type (tested, not just default)
- [ ] Overlap configured (not zero, not excessive)
- [ ] Metadata preserved through splitting (source, section, page)
- [ ] Min-chunk filter applied (no trivially small chunks)
- [ ] Tested on representative sample of your actual documents
- [ ] Retrieval quality measured before and after strategy change
- [ ] Re-indexing pipeline automated (one command to re-chunk + re-embed)
- [ ] Edge cases handled: tables, code blocks, headers-only sections
