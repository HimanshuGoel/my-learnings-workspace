# LlamaIndex — Notes

## What Problem Does This Library Solve?

LlamaIndex provides a data framework for LLM applications — it handles ingesting, structuring, indexing, and querying your private data so LLMs can answer questions about it. It's purpose-built for the "connect LLMs to your data" problem.

## Mental Model

Think of LlamaIndex as **the database access layer for LLMs** — like an ORM (Entity Framework, Hibernate) but for unstructured data. Just as an ORM abstracts away SQL and gives you objects, LlamaIndex abstracts away chunking, embedding, indexing, and retrieval and gives you a simple `query_engine.query("question")` interface.

If LangChain is **Spring Framework** (general-purpose, flexible, many components), LlamaIndex is **Spring Data** — focused specifically on the data access problem. It's more opinionated about RAG and does it better out of the box.

## Where It Fits

```
Your Private Data (docs, PDFs, APIs, databases)
        │
        ▼
┌───────────────────────────────────────┐
│           LlamaIndex                   │  ← (you are here)
│                                        │
│  ┌──────────┐   ┌─────────┐          │
│  │  Readers  │ → │  Nodes   │          │  Load + Parse + Chunk
│  └──────────┘   └────┬────┘          │
│                       │               │
│                  ┌────▼────┐          │
│                  │  Index   │          │  Embed + Store + Structure
│                  └────┬────┘          │
│                       │               │
│            ┌──────────▼──────────┐    │
│            │    Query Engine      │    │  Retrieve + Synthesize
│            └─────────────────────┘    │
└───────────────────────────────────────┘
        │
        ▼
  Natural language answers grounded in YOUR data
```

- **Before LlamaIndex:** Raw documents (PDFs, docs, web pages, databases)
- **After LlamaIndex:** A query engine that answers questions about your data
- **Talks to:** OpenAI/HuggingFace (LLMs + embeddings), ChromaDB/FAISS (vector storage), LangChain (can interoperate), Pydantic (structured output)

## Core Concepts

### 1. Documents and Nodes — The Data Model

```python
from llama_index.core import Document

# Document = a unit of raw input (a file, a web page, a database row)
doc = Document(
    text="LlamaIndex is a data framework for LLM applications.",
    metadata={"source": "docs.md", "page": 1}
)

# Nodes = chunks of documents (what actually gets embedded and indexed)
# LlamaIndex handles splitting Documents → Nodes automatically
# But you can control it:
from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = parser.get_nodes_from_documents([doc])
```

**Key distinction:** Documents are your raw inputs. Nodes are the processed chunks that get embedded and indexed. LlamaIndex manages this pipeline for you.

### 2. Readers (Data Connectors) — Load Anything

```python
from llama_index.core import SimpleDirectoryReader

# Load all files from a directory (auto-detects: PDF, txt, docx, etc.)
documents = SimpleDirectoryReader("./my_data/").load_data()

# Load specific file types
from llama_index.readers.web import SimpleWebPageReader
from llama_index.readers.file import PDFReader

# Web pages
web_docs = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://example.com/docs"]
)

# There are 100+ readers on LlamaHub for: Notion, Slack, GitHub, 
# databases, Google Drive, Wikipedia, YouTube transcripts, etc.
```

### 3. Index — The Core Abstraction

```python
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Configure global settings
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Create index from documents (embeds + stores automatically)
index = VectorStoreIndex.from_documents(documents)

# The index handles:
# 1. Splitting documents into nodes
# 2. Embedding each node
# 3. Storing in a vector store
# All in ONE line.
```

**Index types:**
- `VectorStoreIndex` — similarity search (default, best for most RAG)
- `SummaryIndex` — summarizes all documents (for "tell me about everything")
- `TreeIndex` — hierarchical summarization (for long documents)
- `KeywordTableIndex` — keyword-based retrieval (for precise matching)

### 4. Query Engine — Ask Questions

```python
# Create query engine from index
query_engine = index.as_query_engine()

# Ask questions — returns synthesized answer
response = query_engine.query("What is LlamaIndex?")
print(response.response)           # the answer text
print(response.source_nodes)       # which chunks were used
print(response.source_nodes[0].metadata)  # source attribution

# Configure retrieval
query_engine = index.as_query_engine(
    similarity_top_k=5,            # retrieve top 5 chunks
    response_mode="compact",       # how to synthesize answer
)
```

**Response modes:**
- `"compact"` — stuff all context into one prompt (default, fastest)
- `"refine"` — iterate over chunks, refining answer (better for long contexts)
- `"tree_summarize"` — summarize in a tree structure (best for many chunks)
- `"no_text"` — return retrieved nodes only (no generation)

### 5. Chat Engine — Conversational Interface

```python
# Chat engine = query engine + memory (conversation history)
chat_engine = index.as_chat_engine(chat_mode="condense_question")

# Multi-turn conversation
response1 = chat_engine.chat("What is RAG?")
response2 = chat_engine.chat("How does it use embeddings?")  # understands "it" = RAG
response3 = chat_engine.chat("What are the limitations?")    # still in context

# Reset conversation
chat_engine.reset()
```

**Chat modes:**
- `"condense_question"` — rewrites follow-up questions to be self-contained
- `"context"` — always retrieves context for every message
- `"simple"` — direct chat without retrieval (just conversation)

### 6. Persistence — Save and Load

```python
# Save index to disk
index.storage_context.persist(persist_dir="./storage")

# Load later (no re-embedding needed!)
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="./storage")
loaded_index = load_index_from_storage(storage_context)
query_engine = loaded_index.as_query_engine()
```

### 7. Custom Vector Store (ChromaDB Integration)

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

# Use ChromaDB as the backend
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("my_docs")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create index backed by ChromaDB
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### 8. Structured Output with Pydantic

```python
from pydantic import BaseModel, Field
from llama_index.core.output_parsers import PydanticOutputParser

class MovieReview(BaseModel):
    title: str = Field(description="movie title")
    sentiment: str = Field(description="positive or negative")
    rating: int = Field(description="rating 1-10")

# Query with structured output
query_engine = index.as_query_engine(
    output_cls=MovieReview  # forces response to match this schema
)
response = query_engine.query("Review the latest movie mentioned")
# response is a MovieReview object
```

### 9. Sub-Question Query Engine — Complex Queries

```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata

# Create tools from different indexes (e.g., different document sets)
tools = [
    QueryEngineTool(
        query_engine=finance_engine,
        metadata=ToolMetadata(name="finance", description="Financial reports")
    ),
    QueryEngineTool(
        query_engine=product_engine,
        metadata=ToolMetadata(name="product", description="Product documentation")
    ),
]

# Sub-question engine breaks complex queries into parts
engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=tools)
response = engine.query("Compare Q3 revenue with product launch dates")
# Automatically queries both indexes and synthesizes
```

### 10. LlamaIndex vs LangChain — When to Use Which

| Aspect | LlamaIndex | LangChain |
|--------|-----------|-----------|
| **Primary focus** | Data indexing & retrieval (RAG) | General LLM orchestration |
| **RAG quality** | Better out-of-the-box (purpose-built) | Requires more configuration |
| **Agents** | Basic agent support | Comprehensive agent framework |
| **Tool ecosystem** | 100+ data readers (LlamaHub) | 100+ tool integrations |
| **Complexity** | Simpler for RAG tasks | More flexible but more code |
| **Best for** | "Chat with my docs" apps | Multi-step agents, tool orchestration |
| **Use together?** | Yes — LlamaIndex for retrieval, LangChain for orchestration |

## Key Functions/Methods

### Data Loading

| Function | Purpose |
|----------|---------|
| `SimpleDirectoryReader(path).load_data()` | Load all files from directory |
| `Document(text, metadata)` | Create document manually |
| LlamaHub readers | 100+ connectors (Notion, Slack, DBs) |

### Indexing

| Function | Purpose |
|----------|---------|
| `VectorStoreIndex.from_documents(docs)` | Create index (embed + store) |
| `SummaryIndex.from_documents(docs)` | Summary-based index |
| `index.as_query_engine()` | Create query engine from index |
| `index.as_chat_engine()` | Create conversational engine |

### Querying

| Parameter | Purpose |
|-----------|---------|
| `similarity_top_k=5` | Number of chunks to retrieve |
| `response_mode="compact"` | How to synthesize answer |
| `output_cls=PydanticModel` | Force structured output |
| `streaming=True` | Stream response tokens |

### Persistence

| Function | Purpose |
|----------|---------|
| `index.storage_context.persist(path)` | Save to disk |
| `load_index_from_storage(context)` | Load from disk |

## Common Patterns

### Minimal RAG (5 Lines)

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("./docs").load_data()
index = VectorStoreIndex.from_documents(documents)
engine = index.as_query_engine()
response = engine.query("What is the return policy?")
print(response)
```

### RAG with Custom Chunking

```python
from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter(chunk_size=256, chunk_overlap=30)
index = VectorStoreIndex.from_documents(documents, transformations=[parser])
```

### Multi-Document Query

```python
# Different indexes for different document sets
finance_index = VectorStoreIndex.from_documents(finance_docs)
product_index = VectorStoreIndex.from_documents(product_docs)

# Query across both
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[finance_tool, product_tool],
)
```

## AI/ML Connection

- **Where in the AI pipeline:** LlamaIndex handles the complete data→answer pipeline for RAG. It's more focused than LangChain — specifically optimized for connecting LLMs to private data.

- **Concrete example — RAG (Module 2):** Load your company docs, create an index, get a query engine. Five lines to a working RAG system. Then customize chunking, retrieval, and synthesis for quality.

- **Concrete example — Multi-source QA (Module 4):** Different document sets (HR policies, product docs, financial reports) indexed separately, queried through a router that picks the right source.

- **Concrete example — Capstone (Module 5):** Build a "chat with your codebase" or "chat with your research papers" app. LlamaIndex makes this a weekend project instead of a month-long build.

- **Which IIT KGP modules use this:** Module 2 (RAG), Module 4 (multi-agent data access), Module 5 (capstone RAG applications).

- **What breaks without it:** You'd manually handle document parsing, chunking strategies, embedding pipeline, retrieval logic, and response synthesis. LlamaIndex packages all of this into `from_documents()` → `query()`.

- **LlamaIndex + LangChain:** They complement each other. Use LlamaIndex for the RAG/retrieval part, LangChain for agent orchestration and tool-calling. Many production apps use both.

## Common Mistakes

1. **Chunk size too large** — default 1024 tokens might be too much for precise retrieval. Try 256-512 for better precision.

2. **Not persisting the index** — re-embedding every time is expensive. Always persist after building: `index.storage_context.persist()`.

3. **Ignoring response modes** — default "compact" fails with many retrieved chunks (context overflow). Switch to "refine" or "tree_summarize" for large retrievals.

4. **Not setting similarity_top_k appropriately** — too few chunks = missing info, too many = noise and slow. Start with 3-5.

5. **Using wrong LLM for the task** — gpt-4o-mini is fine for simple QA but may struggle with complex synthesis across many documents. Use gpt-4o for complex reasoning.

6. **Not checking source_nodes** — always verify which chunks were used. If irrelevant chunks are being retrieved, the index needs better chunking or metadata.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| General agent orchestration with tools | LangChain |
| Simple single LLM call (no retrieval) | Direct OpenAI SDK |
| Keyword search (exact matching) | Elasticsearch |
| Structured data (SQL tables) | Direct SQL queries |
| Real-time streaming data | Custom pipeline |
| Model training/fine-tuning | HuggingFace Transformers |

## Ready to Move On?

- ☐ I can load documents and create a VectorStoreIndex in 5 lines
- ☐ I understand the Documents → Nodes → Index → Query Engine pipeline
- ☐ I can configure chunk size, top_k, and response mode
- ☐ I know how to persist and reload an index
- ☐ I understand when to use LlamaIndex vs LangChain vs both

Once all checked → move to **Pydantic**.
