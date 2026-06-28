# Embedding Selection

## The Problem You're Solving

You need to convert text into vectors for similarity search, but there are dozens of embedding models with wildly different dimensions, performance, cost, and speed. The wrong choice means either poor retrieval quality (cheap/fast model) or unnecessary cost/latency (overkill model for simple use case).

## Options Available

| Model | Dimensions | MTEB Score | Speed | Cost | Best For |
|-------|-----------|------------|-------|------|----------|
| all-MiniLM-L6-v2 | 384 | ~63 | Very Fast | Free (local) | Prototyping, low-resource |
| all-mpnet-base-v2 | 768 | ~65 | Fast | Free (local) | Good local baseline |
| BGE-base-en-v1.5 | 768 | ~68 | Fast | Free (local) | Production local model |
| BGE-large-en-v1.5 | 1024 | ~70 | Medium | Free (local) | Higher quality, more compute |
| text-embedding-3-small | 1536 | ~68 | Fast | $0.02/1M tokens | Cost-effective API option |
| text-embedding-3-large | 3072 | ~72 | Medium | $0.13/1M tokens | Best OpenAI quality |
| voyage-3 | 1024 | ~72 | Fast | $0.06/1M tokens | Strong retrieval focus |
| Cohere embed-v3 | 1024 | ~71 | Fast | $0.10/1M tokens | Multi-language support |
| Jina-embeddings-v3 | 1024 | ~72 | Medium | Free/API | Long-context (8K tokens) |

*MTEB = Massive Text Embedding Benchmark (higher is better, scale ~40-75)*

## Recommended Approach

**Start with `all-MiniLM-L6-v2` for development/prototyping. Move to `text-embedding-3-small` or `BGE-base-en-v1.5` for production.**

Why:
- MiniLM is fast, free, runs locally, and good enough to validate your pipeline
- For production: OpenAI's text-embedding-3-small gives strong quality at very low cost
- If you need full control (no API dependency): BGE-base gives near-API quality locally
- Only go to large/3072-dim models if you've proven retrieval quality is your bottleneck

## Step-by-Step Implementation

### 1. Local Development Setup (sentence-transformers)

```python
from sentence_transformers import SentenceTransformer

# Fast and free — good for development
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed documents
doc_embeddings = model.encode(
    ["document 1 text", "document 2 text"],
    batch_size=64,
    show_progress_bar=True,
    normalize_embeddings=True,  # cosine similarity = dot product when normalized
)

# Embed query
query_embedding = model.encode(
    "what is the batch size limit?",
    normalize_embeddings=True,
)
```

### 2. Production with OpenAI

```python
from openai import OpenAI

client = OpenAI()

def get_embeddings(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    """Batch embed texts using OpenAI API."""
    response = client.embeddings.create(
        input=texts,
        model=model,
        # Optionally reduce dimensions (saves storage, small quality loss)
        # dimensions=512,  # only text-embedding-3-* supports this
    )
    return [item.embedding for item in response.data]
```

### 3. Production with Local BGE Model

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# BGE models need instruction prefix for queries (not for documents)
queries = ["Represent this sentence for searching relevant passages: " + q for q in raw_queries]
query_embeddings = model.encode(queries, normalize_embeddings=True)

# Documents get embedded without prefix
doc_embeddings = model.encode(documents, normalize_embeddings=True)
```

### 4. Dimensionality Reduction (When Storage/Speed Matters)

```python
# Option A: Use OpenAI's native dimension reduction
embeddings = client.embeddings.create(
    input=texts,
    model="text-embedding-3-large",
    dimensions=1024,  # reduce from 3072 to 1024
)

# Option B: PCA reduction for local models
from sklearn.decomposition import PCA
import numpy as np

full_embeddings = model.encode(documents)  # (N, 768)
pca = PCA(n_components=256)
reduced = pca.fit_transform(full_embeddings)  # (N, 256)
# Normalize after reduction
reduced = reduced / np.linalg.norm(reduced, axis=1, keepdims=True)
```

### 5. Embedding with LangChain (Integration Layer)

```python
# Local
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# OpenAI
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Use with vector store
from langchain_chroma import Chroma
vectorstore = Chroma.from_documents(documents, embeddings)
```

### 6. Benchmarking Your Choice

```python
from sentence_transformers import SentenceTransformer, util
import time

def benchmark_model(model_name: str, queries: list, docs: list, relevant_pairs: list):
    """Measure retrieval quality and speed."""
    model = SentenceTransformer(model_name)
    
    # Speed
    start = time.time()
    doc_embs = model.encode(docs, normalize_embeddings=True)
    index_time = time.time() - start
    
    start = time.time()
    query_embs = model.encode(queries, normalize_embeddings=True)
    query_time = time.time() - start
    
    # Quality (recall@k)
    hits = 0
    for i, q_emb in enumerate(query_embs):
        scores = util.cos_sim(q_emb, doc_embs)[0]
        top_k = scores.argsort(descending=True)[:5]
        if relevant_pairs[i] in top_k:
            hits += 1
    recall_at_5 = hits / len(queries)
    
    return {
        "model": model_name,
        "recall@5": recall_at_5,
        "index_time_per_doc_ms": (index_time / len(docs)) * 1000,
        "query_time_ms": (query_time / len(queries)) * 1000,
    }
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Model | MiniLM (dev), BGE-base or text-embedding-3-small (prod) | Balance quality vs cost vs control |
| Normalize | Always True | Enables cosine similarity via dot product (faster) |
| Batch size | 64-256 (local), 100-2000 (API) | Maximize throughput without OOM |
| Max sequence length | 512 tokens (default), check model limit | Longer text gets truncated silently |
| Query prefix | Required for BGE models ("Represent this...") | Architecture-specific, missing it hurts quality |
| Dimension reduction | Only if storage/speed is proven bottleneck | Quality loss is small but measurable |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Retrieval quality suddenly drops | Model mismatch: query embedded with different model than docs | Ensure same model for indexing and querying |
| Symmetric queries work, asymmetric don't | Model needs query prefix (BGE, E5) | Add instruction prefix for queries |
| Long documents get bad embeddings | Text exceeds model's max sequence length (truncated) | Chunk documents properly before embedding |
| API cost unexpectedly high | Re-embedding unchanged documents | Cache embeddings, only re-embed changed content |
| Local model too slow | Running on CPU, large model | Use GPU, or switch to MiniLM for dev |
| Multilingual content retrieves poorly | Model trained on English only | Use multilingual model (Cohere v3, multilingual-MiniLM) |

## Production Considerations

### Cost Planning
- 1M tokens ≈ 750K words ≈ 1500 documents (500 words each)
- text-embedding-3-small: $0.02 per 1M tokens → $0.02 for 1500 docs
- Re-embedding is the hidden cost — design for incremental updates

### Latency
- Local (MiniLM, GPU): ~1ms per document
- Local (BGE-large, CPU): ~50ms per document
- API (OpenAI): ~100-300ms per batch (network-bound)
- Query-time latency matters more than index-time

### Model Versioning
- Pin your model version (don't use "latest")
- If model changes → all embeddings must be re-computed (vectors not compatible)
- Store model name + version in metadata alongside embeddings

### Scaling
- For > 1M documents: consider approximate nearest neighbor (HNSW) over brute-force
- For > 10M documents: consider dedicated vector DB (Pinecone, Weaviate) over local ChromaDB
- Batch embedding with queue for large ingestion jobs

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| Recall@5 | % of queries where correct doc is in top 5 | > 85% |
| Recall@10 | % of queries where correct doc is in top 10 | > 92% |
| MRR (Mean Reciprocal Rank) | Average 1/rank of first relevant doc | > 0.7 |
| Embedding latency | ms per query embedding | < 50ms (local), < 300ms (API) |
| Index throughput | docs per second during bulk indexing | > 100/s (local GPU) |
| Cost per 1K queries | Embedding API cost per 1000 queries | Track trending |

## Ready to Ship? — Checklist

- [ ] Model chosen with benchmarked retrieval quality (not just vibes)
- [ ] Same model used for indexing and querying (verified)
- [ ] Query prefix added if required by model architecture
- [ ] Normalization enabled (cosine similarity via dot product)
- [ ] Max sequence length known and chunking respects it
- [ ] Model version pinned in config (not "latest")
- [ ] Cost estimated for corpus size and query volume
- [ ] Fallback plan if API model becomes unavailable
- [ ] Benchmark script ready for evaluating alternatives
