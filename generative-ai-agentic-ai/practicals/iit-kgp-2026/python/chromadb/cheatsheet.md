# ChromaDB — Cheatsheet

## Install

```bash
pip install chromadb
```

## Import

```python
import chromadb
from chromadb.utils import embedding_functions
```

---

## Client

```python
# In-memory (testing, ephemeral)
client = chromadb.Client()

# Persistent (saves to disk)
client = chromadb.PersistentClient(path="./chroma_db")
```

---

## Collections

```python
# Create or get
collection = client.get_or_create_collection("my_docs")

# Get existing (raises if not found)
collection = client.get_collection("my_docs")

# With custom embedding function
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection("my_docs", embedding_function=ef)

# Delete
client.delete_collection("my_docs")

# List all
client.list_collections()

# Count docs
collection.count()
```

---

## Adding Documents

```python
# Auto-embed (uses default embedding function)
collection.add(
    ids=["id1", "id2", "id3"],
    documents=["text 1", "text 2", "text 3"],
    metadatas=[{"source": "a"}, {"source": "b"}, {"source": "c"}]
)

# Pre-computed embeddings
collection.add(
    ids=["id1"],
    embeddings=[[0.1, 0.2, 0.3, ...]],
    documents=["original text"],
    metadatas=[{"source": "file.pdf"}]
)

# Upsert (insert or update)
collection.upsert(ids=["id1"], documents=["updated text"])
```

---

## Querying

```python
# By text (auto-embedded)
results = collection.query(
    query_texts=["my question"],
    n_results=5
)

# By embedding
results = collection.query(
    query_embeddings=[[0.1, 0.2, ...]],
    n_results=5
)

# Multiple queries
results = collection.query(
    query_texts=["q1", "q2"],
    n_results=3
)

# Access results
results["ids"]          # [[id1, id2, ...]]
results["documents"]    # [[text1, text2, ...]]
results["metadatas"]    # [[{meta1}, {meta2}, ...]]
results["distances"]    # [[0.12, 0.34, ...]] (lower = more similar)
```

---

## Metadata Filters

```python
# Exact match
where={"source": "manual.pdf"}

# Comparison operators
where={"page": {"$gt": 5}}       # greater than
where={"page": {"$gte": 5}}      # greater or equal
where={"page": {"$lt": 10}}      # less than
where={"score": {"$ne": 0}}      # not equal

# List membership
where={"source": {"$in": ["a.pdf", "b.pdf"]}}
where={"type": {"$nin": ["draft", "archived"]}}

# Combine with $and / $or
where={"$and": [
    {"source": "docs.pdf"},
    {"page": {"$gte": 5}}
]}

# Filter on document text
where_document={"$contains": "authentication"}
```

---

## Get (by ID or filter)

```python
# By IDs
docs = collection.get(ids=["id1", "id2"])

# By filter
docs = collection.get(where={"source": "manual.pdf"})

# Include specific fields
docs = collection.get(ids=["id1"], include=["documents", "metadatas", "embeddings"])
```

---

## Update & Delete

```python
# Update
collection.update(
    ids=["id1"],
    documents=["new text"],
    metadatas=[{"updated": True}]
)

# Delete by ID
collection.delete(ids=["id1", "id2"])

# Delete by filter
collection.delete(where={"source": "old.pdf"})
```

---

## Embedding Functions

```python
from chromadb.utils import embedding_functions

# Sentence Transformers (default, local, free)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# OpenAI
ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="sk-...", model_name="text-embedding-3-small"
)

# Default (all-MiniLM-L6-v2 — used when none specified)
# Just don't pass embedding_function to get_or_create_collection
```

---

## LangChain Integration

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create from documents
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="my_collection"
)

# As retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke("my query")

# With metadata filter
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5, "filter": {"source": "manual.pdf"}}
)
```

---

## Distance Metrics

```python
# Default: L2 (Euclidean distance)
collection = client.get_or_create_collection("docs",
    metadata={"hnsw:space": "l2"})        # default

# Cosine distance (most common for text)
collection = client.get_or_create_collection("docs",
    metadata={"hnsw:space": "cosine"})

# Inner product
collection = client.get_or_create_collection("docs",
    metadata={"hnsw:space": "ip"})
```

---

## Quick Reference Links

- Docs: https://docs.trychroma.com/
- Python API: https://docs.trychroma.com/reference/py-client
- LangChain integration: https://python.langchain.com/docs/integrations/vectorstores/chroma
