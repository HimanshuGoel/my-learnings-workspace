# ChromaDB — Notes

## What Problem Does This Library Solve?

ChromaDB stores, indexes, and retrieves vector embeddings — enabling fast similarity search over documents, images, or any data represented as numerical vectors. It's the "database layer" for RAG systems.

## Mental Model

Think of ChromaDB as **SQLite for embeddings**. Just as SQLite gives you a zero-config local database for structured data, ChromaDB gives you a zero-config local vector store for embeddings. No server setup, no Docker, no cloud account — just `pip install` and go. It stores vectors + metadata + documents together, and finds the most similar ones to a query instantly.

Alternatively: if a SQL database answers "find rows WHERE condition matches," a vector database answers "find documents WHERE meaning is similar."

## Where It Fits

```
Documents (text, PDFs, web pages)
        │
        ▼
┌────────────────────┐
│  Embedding Model    │  ← convert text to vectors
│  (sentence-transformers, OpenAI)
└────────┬───────────┘
         │ vectors (arrays of floats)
         ▼
┌────────────────────┐
│     ChromaDB        │  ← store + index + search vectors (you are here)
└────────┬───────────┘
         │ top-K similar documents
         ▼
┌────────────────────┐
│    LLM (via         │  ← generate answer using retrieved context
│    LangChain)       │
└────────────────────┘
```

- **Before ChromaDB:** Embeddings from sentence-transformers or OpenAI
- **After ChromaDB:** Top-K most relevant documents for a query → fed to LLM
- **Talks to:** LangChain (as retriever), sentence-transformers (embeddings), OpenAI (embeddings), FAISS (alternative)

## Core Concepts

### 1. Collections — Like Tables in SQL

```python
import chromadb

# Create a client (in-memory or persistent)
client = chromadb.Client()                    # in-memory (for testing)
client = chromadb.PersistentClient(path="./chroma_db")  # saves to disk

# Create or get a collection
collection = client.get_or_create_collection(
    name="my_documents",
    metadata={"description": "Product documentation"}
)

# Delete collection
client.delete_collection("my_documents")

# List all collections
client.list_collections()
```

A **collection** = a named group of embeddings + documents + metadata. Like a table in SQL, but for vectors.

### 2. Adding Documents

```python
# Add documents (ChromaDB can auto-embed if configured)
collection.add(
    ids=["doc1", "doc2", "doc3"],              # unique IDs (required)
    documents=["First document text",          # raw text (optional)
               "Second document text",
               "Third document text"],
    metadatas=[                                 # metadata per doc (optional)
        {"source": "manual.pdf", "page": 1},
        {"source": "manual.pdf", "page": 2},
        {"source": "faq.md", "page": 1}
    ],
    embeddings=[[0.1, 0.2, ...],              # pre-computed embeddings (optional)
                [0.3, 0.4, ...],
                [0.5, 0.6, ...]]
)

# If you don't provide embeddings, ChromaDB uses its default embedding function
# (all-MiniLM-L6-v2 by default)
collection.add(
    ids=["doc4"],
    documents=["ChromaDB will embed this automatically"]
)
```

### 3. Querying — Find Similar Documents

```python
# Query by text (auto-embedded)
results = collection.query(
    query_texts=["How do I reset my password?"],
    n_results=3     # return top 3 most similar
)

# Results structure:
# results["ids"]        → [["doc2", "doc1", "doc3"]]
# results["documents"]  → [["text2", "text1", "text3"]]
# results["metadatas"]  → [[{meta2}, {meta1}, {meta3}]]
# results["distances"]  → [[0.12, 0.34, 0.56]]  (lower = more similar)

# Query by embedding (pre-computed)
results = collection.query(
    query_embeddings=[[0.2, 0.3, ...]],
    n_results=5
)

# Multiple queries at once
results = collection.query(
    query_texts=["question 1", "question 2"],
    n_results=3
)
```

### 4. Metadata Filtering — Precise Retrieval

```python
# Filter by metadata (like SQL WHERE)
results = collection.query(
    query_texts=["deployment guide"],
    n_results=5,
    where={"source": "manual.pdf"}           # exact match
)

# Complex filters
results = collection.query(
    query_texts=["error handling"],
    n_results=5,
    where={
        "$and": [
            {"source": "api-docs.md"},
            {"page": {"$gte": 5}}            # page >= 5
        ]
    }
)

# Filter operators: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin, $and, $or

# Filter on document content
results = collection.query(
    query_texts=["authentication"],
    n_results=5,
    where_document={"$contains": "API key"}  # document must contain this
)
```

### 5. Updating and Deleting

```python
# Update documents
collection.update(
    ids=["doc1"],
    documents=["Updated text content"],
    metadatas=[{"source": "manual.pdf", "page": 1, "updated": True}]
)

# Upsert (insert or update)
collection.upsert(
    ids=["doc1", "doc_new"],
    documents=["Updated doc1", "Brand new doc"],
    metadatas=[{"v": 2}, {"v": 1}]
)

# Delete by ID
collection.delete(ids=["doc1", "doc2"])

# Delete by filter
collection.delete(where={"source": "old_docs.txt"})
```

### 6. Custom Embedding Functions

```python
from chromadb.utils import embedding_functions

# Use sentence-transformers (default)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Use OpenAI
ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-key",
    model_name="text-embedding-3-small"
)

# Use HuggingFace Inference API
ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="your-key",
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Attach to collection
collection = client.get_or_create_collection(
    name="my_docs",
    embedding_function=ef
)
```

### 7. Persistence — Save to Disk

```python
# Persistent client saves automatically
client = chromadb.PersistentClient(path="./my_vector_db")

# All add/update/delete operations are auto-saved
collection = client.get_or_create_collection("docs")
collection.add(ids=["1"], documents=["Hello world"])

# Next time you open the same path, data is still there
client2 = chromadb.PersistentClient(path="./my_vector_db")
collection2 = client2.get_collection("docs")
print(collection2.count())  # 1
```

### 8. Integration with LangChain

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Create from LangChain documents
docs = [Document(page_content="text", metadata={"source": "file.pdf"})]
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create vector store
vectorstore = Chroma.from_documents(
    docs, embeddings,
    persist_directory="./chroma_db",
    collection_name="my_docs"
)

# Use as retriever in RAG chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
relevant_docs = retriever.invoke("my question")
```

## Key Functions/Methods

### Client Operations

| Method | Purpose |
|--------|---------|
| `chromadb.Client()` | In-memory client (testing) |
| `chromadb.PersistentClient(path)` | Persistent client (saves to disk) |
| `client.get_or_create_collection(name)` | Get or create collection |
| `client.get_collection(name)` | Get existing collection |
| `client.delete_collection(name)` | Delete collection |
| `client.list_collections()` | List all collections |

### Collection Operations

| Method | Purpose |
|--------|---------|
| `collection.add(ids, documents, metadatas, embeddings)` | Add new documents |
| `collection.query(query_texts, n_results, where)` | Find similar |
| `collection.get(ids, where)` | Get by ID or filter |
| `collection.update(ids, documents, metadatas)` | Update existing |
| `collection.upsert(ids, documents, metadatas)` | Insert or update |
| `collection.delete(ids, where)` | Remove documents |
| `collection.count()` | Total document count |
| `collection.peek(n)` | Preview first n documents |

### Query Filters

| Operator | Meaning | Example |
|----------|---------|---------|
| `$eq` | Equals | `{"status": "active"}` |
| `$ne` | Not equals | `{"status": {"$ne": "deleted"}}` |
| `$gt/$gte` | Greater than | `{"page": {"$gte": 5}}` |
| `$lt/$lte` | Less than | `{"score": {"$lt": 0.5}}` |
| `$in` | In list | `{"source": {"$in": ["a.pdf", "b.pdf"]}}` |
| `$and/$or` | Combine | `{"$and": [{...}, {...}]}` |

## Common Patterns

### RAG Ingestion Pipeline

```python
import chromadb
from chromadb.utils import embedding_functions

# Setup
client = chromadb.PersistentClient(path="./rag_db")
ef = embedding_functions.SentenceTransformerEmbeddingFunction()
collection = client.get_or_create_collection("docs", embedding_function=ef)

# Ingest documents (e.g., from chunks)
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk.page_content],
        metadatas=[chunk.metadata]
    )
```

### Semantic Search with Metadata Filter

```python
results = collection.query(
    query_texts=["deployment process"],
    n_results=5,
    where={"source": {"$in": ["deploy-guide.md", "ops-runbook.md"]}}
)
for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"[{dist:.3f}] {meta['source']}: {doc[:80]}...")
```

### Incremental Updates (Add New Docs Without Duplicates)

```python
import hashlib

def doc_id(text):
    return hashlib.md5(text.encode()).hexdigest()

# Upsert ensures no duplicates
collection.upsert(
    ids=[doc_id(chunk) for chunk in new_chunks],
    documents=[chunk for chunk in new_chunks],
    metadatas=[{"ingested_at": "2026-06-18"} for _ in new_chunks]
)
```

## AI/ML Connection

- **Where in the AI pipeline:** ChromaDB is the storage and retrieval layer between embedding creation and LLM generation. It's the "database" in RAG.

- **Concrete example — RAG (Module 2):** Embed 10,000 document chunks → store in ChromaDB → when user asks a question, embed the query → ChromaDB finds top-5 similar chunks → feed those to the LLM as context → LLM generates grounded answer.

- **Concrete example — Semantic Search:** Build a documentation search that understands meaning, not just keywords. "How to fix auth errors" matches docs about "authentication failures" even without exact keyword overlap.

- **Concrete example — Capstone (Module 5):** Your RAG application needs persistent vector storage that survives restarts. ChromaDB's PersistentClient handles this locally.

- **Which IIT KGP modules use this:** Module 2 (RAG retrieval), Module 4 (agent memory/knowledge base), Module 5 (capstone vector storage).

- **What breaks without it:** You'd recompute embeddings on every query (expensive and slow) or store them in flat files (no indexing, O(n) search). ChromaDB gives O(log n) approximate nearest neighbor search.

- **ChromaDB vs FAISS:** ChromaDB = easier API, built-in persistence, metadata filtering. FAISS = faster at scale (millions of vectors), but lower-level, no built-in metadata. For your coursework, ChromaDB is the right choice.

## Common Mistakes

1. **Forgetting unique IDs** — IDs must be unique strings. Duplicates silently overwrite. Use content hashes or UUIDs.

2. **Not persisting data** — `chromadb.Client()` is in-memory only (lost on restart). Use `PersistentClient(path)` for real applications.

3. **Mismatched embedding dimensions** — if you store 384-dim vectors, you must query with 384-dim vectors (same model). Mixing models = garbage results.

4. **Not using metadata filtering** — querying all documents when you know the source/category is wasteful. Filter first, then similarity search.

5. **Storing very long texts without chunking** — embeddings work best on focused content (100-500 words). Long documents should be split first.

6. **Ignoring distance scores** — low distance = high similarity. Use a threshold (e.g., > 0.7 similarity) to filter irrelevant results.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Millions of vectors, maximum speed | FAISS (Meta's library, optimized for scale) |
| Production distributed deployment | Pinecone, Weaviate, Qdrant (managed cloud vector DBs) |
| Structured data queries (SQL) | PostgreSQL, SQLite |
| Full-text keyword search | Elasticsearch |
| Simple in-memory similarity (< 1000 docs) | NumPy cosine similarity directly |
| Graph-based relationships | Neo4j |

## Ready to Move On?

- ☐ I can create a collection, add documents, and query for similar ones
- ☐ I understand the role of embedding functions (text → vectors)
- ☐ I can use metadata filters to narrow search results
- ☐ I can integrate ChromaDB with LangChain as a retriever
- ☐ I know when to use ChromaDB vs FAISS vs managed solutions

Once all checked → move to **Pydantic** or **FastAPI**.
