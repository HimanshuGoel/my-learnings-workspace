# Vector Store Design

## The Problem You're Solving

You have embeddings — now where do you put them? A naive "dump everything in one collection" approach breaks down fast: no metadata filtering, no multi-tenancy, slow queries at scale, and no way to update documents without re-indexing everything. Vector store design is the database schema design of RAG systems.

## Options Available

| Vector Store | Type | Best For | Scaling | Cost |
|-------------|------|----------|---------|------|
| ChromaDB | Embedded/Client-Server | Prototyping, < 1M docs | Single node | Free |
| FAISS | In-memory library | Speed-critical, batch processing | Single node (manual sharding) | Free |
| Pinecone | Managed cloud | Production SaaS, zero-ops | Fully managed auto-scale | $70+/mo |
| Weaviate | Self-hosted/cloud | Hybrid search, GraphQL API | Horizontal | Free (self) / Paid (cloud) |
| Qdrant | Self-hosted/cloud | Performance, filtering | Horizontal | Free (self) / Paid (cloud) |
| pgvector | PostgreSQL extension | Already using Postgres, < 5M docs | Postgres scaling | Free |
| Milvus | Distributed | Enterprise, > 10M docs | Horizontal, distributed | Free (self) / Paid (Zilliz) |

## Recommended Approach

**ChromaDB for development and learning projects. Qdrant or pgvector for production.**

Why:
- ChromaDB: Zero config, Python-native, LangChain integration, perfect for learning and prototyping
- pgvector: If you already run Postgres — one fewer moving part, familiar SQL, good enough to 5M docs
- Qdrant: Best performance/feature ratio for dedicated vector search (filtering, payload, hybrid)

## Step-by-Step Implementation

### 1. ChromaDB — Development Setup

```python
import chromadb
from chromadb.config import Settings

# Persistent storage (survives restarts)
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection with distance metric
collection = client.get_or_create_collection(
    name="documentation",
    metadata={
        "hnsw:space": "cosine",       # distance metric
        "hnsw:M": 16,                  # connections per node (higher = better recall, more memory)
        "hnsw:construction_ef": 200,   # build-time accuracy (higher = better index, slower build)
        "hnsw:search_ef": 100,         # query-time accuracy (higher = better recall, slower query)
    }
)
```

### 2. Collection Design — Multi-Collection Strategy

```python
# Strategy: One collection per document type (not one giant collection)
collections = {
    "api_docs": client.get_or_create_collection("api_docs"),
    "tutorials": client.get_or_create_collection("tutorials"),
    "changelogs": client.get_or_create_collection("changelogs"),
    "internal_wiki": client.get_or_create_collection("internal_wiki"),
}

# Why: Different content types have different retrieval needs
# - API docs: precise, keyword-heavy
# - Tutorials: longer context, semantic
# - Changelogs: time-filtered, version-specific
```

### 3. Metadata Schema Design

```python
# Define consistent metadata schema for all chunks
def create_chunk_metadata(
    source_file: str,
    page_number: int,
    section_heading: str,
    document_type: str,    # "api_doc", "tutorial", "changelog"
    version: str,          # software version this doc covers
    last_updated: str,     # ISO date string
    language: str = "en",
    chunk_index: int = 0,
    total_chunks: int = 1,
) -> dict:
    return {
        "source": source_file,
        "page": page_number,
        "section": section_heading,
        "doc_type": document_type,
        "version": version,
        "updated_at": last_updated,
        "language": language,
        "chunk_index": chunk_index,
        "total_chunks": total_chunks,
    }

# Add documents with metadata
collection.add(
    ids=["doc_001_chunk_0", "doc_001_chunk_1"],
    documents=["chunk text 1...", "chunk text 2..."],
    metadatas=[
        create_chunk_metadata("api/auth.md", 1, "Authentication", "api_doc", "2.1.0", "2026-07-15"),
        create_chunk_metadata("api/auth.md", 1, "OAuth Flow", "api_doc", "2.1.0", "2026-07-15"),
    ],
    embeddings=[embedding_1, embedding_2],  # pre-computed embeddings
)
```

### 4. Querying with Metadata Filters

```python
# Semantic search + metadata filter
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={
        "$and": [
            {"doc_type": {"$eq": "api_doc"}},
            {"version": {"$eq": "2.1.0"}},
        ]
    },
    where_document={"$contains": "authentication"},  # keyword filter on text
)

# Results include: documents, metadatas, distances, ids
for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"[{dist:.3f}] {meta['section']} — {doc[:100]}")
```

### 5. Update Strategy (Incremental, Not Full Re-index)

```python
def upsert_document(collection, doc_id: str, chunks: list[str], metadatas: list[dict], embeddings):
    """Update a document's chunks without re-indexing everything."""
    
    # Delete old chunks for this document
    existing = collection.get(where={"source": doc_id})
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
    
    # Insert new chunks
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
        embeddings=embeddings,
    )
```

### 6. LangChain Integration

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma(
    collection_name="documentation",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_directory="./chroma_db",
)

# Add with metadata
vectorstore.add_documents(documents)  # LangChain Document objects

# Retrieve with filter
retriever = vectorstore.as_retriever(
    search_type="similarity",          # or "mmr" for diversity
    search_kwargs={
        "k": 5,
        "filter": {"doc_type": "api_doc"},
    },
)
```

### 7. HNSW Index Tuning

```python
# HNSW parameters control the speed/accuracy trade-off

# M (max connections per node)
# - Higher = better recall, more memory, slower build
# - Default: 16. Range: 8-64
# - Rule of thumb: 16 for < 1M docs, 32 for > 1M

# ef_construction (build-time beam width)
# - Higher = better index quality, slower indexing
# - Default: 200. Range: 100-500
# - Set once during build, doesn't affect query time

# ef_search (query-time beam width)
# - Higher = better recall, slower queries
# - Default: 100. Range: 50-500
# - This is your main query-time tuning knob
# - Start at 100, increase if recall@10 < 95%
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Distance metric | cosine | Standard for normalized embeddings; invariant to magnitude |
| HNSW M | 16 (< 1M docs), 32 (> 1M) | More connections = better recall, more memory |
| HNSW ef_construction | 200 | Good index quality without excessive build time |
| HNSW ef_search | 100-200 | Start at 100, increase if recall drops |
| Collection strategy | Per document type | Enables type-specific filters and configs |
| ID scheme | `{doc_id}_chunk_{index}` | Enables incremental updates per document |
| Metadata fields | source, section, version, updated_at, doc_type | Minimum viable schema for filtering and attribution |
| Persistence | Always on (not in-memory) | Survive restarts without re-indexing |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Queries return irrelevant results despite good embeddings | Wrong distance metric (L2 instead of cosine on normalized vectors) | Switch to cosine, or normalize vectors + use inner product |
| Query latency spikes at scale | ef_search too high, or index not built properly | Reduce ef_search, rebuild index with proper ef_construction |
| Metadata filter returns nothing | Filter field name mismatch or wrong type | Verify metadata keys/values with `collection.get()` |
| Updates don't reflect in queries | Stale cache or not persisted | Call `client.persist()` (if applicable), verify with `.get()` |
| Out of memory at index time | Too many dimensions, too many docs for RAM | Reduce dimensions, use disk-backed store, or switch to Qdrant/Milvus |
| Duplicate results from same document | Overlapping chunks without dedup | Add MMR retrieval or filter by source, return unique sources |

## Production Considerations

### Storage Planning
- Per vector: dimensions × 4 bytes (float32) + metadata overhead
- 1M docs × 768 dims = ~3 GB embeddings + ~1-2 GB metadata + ~2 GB HNSW index ≈ 7 GB
- ChromaDB works up to ~1M docs on a single machine with 16 GB RAM

### Backup & Recovery
- ChromaDB: backup the `persist_directory` folder
- Always keep source documents — you can re-index from scratch if needed
- Version your collection schema (metadata fields) in code

### Multi-Tenancy
- Option A: Separate collections per tenant (simpler isolation, more resources)
- Option B: Single collection + tenant_id in metadata filter (simpler management)
- For learning/personal projects: single collection is fine

### Monitoring
- Track: query latency p50/p95, index size, collection count
- Alert on: latency > 500ms, failed inserts, collection size > 80% capacity

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| Query latency | Time from query submit to results returned | < 100ms for < 100K docs |
| Recall@K | Does the correct chunk appear in top-K results? | > 90% |
| Filter accuracy | Does metadata filter return correct subset? | 100% (deterministic) |
| Index build time | Time to index full corpus | < 10 min for < 100K docs |
| Storage efficiency | GB used vs docs stored | Reasonable for hardware |

## Ready to Ship? — Checklist

- [ ] Distance metric matches embedding normalization (cosine for normalized vectors)
- [ ] Collection strategy decided (per-type vs single with filters)
- [ ] Metadata schema documented and enforced
- [ ] ID scheme enables incremental updates (not random UUIDs)
- [ ] HNSW parameters tuned (not just defaults)
- [ ] Persistence configured (not in-memory-only)
- [ ] Backup strategy in place
- [ ] Query latency measured and acceptable
- [ ] Filter queries tested with actual metadata values
- [ ] Scaling plan documented (what happens at 10x current size?)
