# Retrieval Quality

## The Problem You're Solving

Your RAG system retrieves documents but the answers are still wrong — either the right documents aren't in the top-K (recall problem), or too many irrelevant documents dilute the context (precision problem). Retrieval quality is the single biggest lever for RAG answer quality. Bad retrieval → bad answers, no matter how good your LLM is.

## Options Available

| Technique | What It Does | When to Use | Complexity |
|-----------|-------------|-------------|------------|
| Top-K tuning | Adjust number of returned results | Always (starting point) | Low |
| Metadata filtering | Pre-filter by category/date/version | Multi-category corpus | Low |
| Hybrid search (BM25 + vector) | Combine keyword + semantic matching | Keyword-heavy queries fail vector-only | Medium |
| Re-ranking | Score & reorder results with a cross-encoder | Top-K has right docs but wrong order | Medium |
| MMR (Maximal Marginal Relevance) | Diversify results (reduce redundancy) | Top-K returns duplicate info | Low |
| Query expansion | Rephrase/expand query before retrieval | Short or ambiguous queries | Medium |
| HyDE (Hypothetical Document Embeddings) | Generate hypothetical answer, embed that | Queries phrased differently than docs | Medium |
| Multi-query retrieval | Generate multiple query variants, union results | Complex questions needing multiple angles | Medium |
| Contextual compression | Summarize/extract relevant parts of chunks | Large chunks with low signal density | High |

## Recommended Approach

**Start with: Vector search + metadata filter + top-K=5. Then add: Re-ranking (cross-encoder) when precision matters. Then add: Hybrid search (BM25) when keyword queries fail.**

Why: Each addition is incremental. Start simple, measure, add complexity only when metrics justify it. Re-ranking gives the biggest quality lift for the complexity cost.

## Step-by-Step Implementation

### 1. Baseline: Vector Search + Metadata Filter

```python
from langchain_chroma import Chroma

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5,
        "filter": {"doc_type": "api_doc"},
    },
)

docs = retriever.invoke("How do I authenticate with OAuth?")
```

### 2. MMR for Diversity (Quick Win)

```python
# Maximal Marginal Relevance — reduces redundancy in results
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,              # final number of results
        "fetch_k": 20,       # initial candidates to consider
        "lambda_mult": 0.7,  # 0=max diversity, 1=max relevance (0.5-0.7 is sweet spot)
    },
)
```

### 3. Re-Ranking with Cross-Encoder

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# Cross-encoder scores query-document PAIRS (more accurate than bi-encoder similarity)
cross_encoder = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
reranker = CrossEncoderReranker(model=cross_encoder, top_n=3)

# Chain: retrieve 20 candidates → rerank → return top 3
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
reranking_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever,
)

docs = reranking_retriever.invoke("What's the rate limit for API calls?")
```

### 4. Hybrid Search (BM25 + Vector)

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# BM25 (keyword-based, TF-IDF style)
bm25_retriever = BM25Retriever.from_documents(documents, k=10)

# Vector (semantic)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Combine with Reciprocal Rank Fusion
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7],  # weight semantic higher for most use cases
)
```

### 5. Query Expansion (Multi-Query)

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    llm=llm,
    # Generates 3 query variants, retrieves for each, deduplicates
)

# Example: "OAuth auth" → also searches "How to implement OAuth 2.0", "authentication flow setup"
docs = multi_query_retriever.invoke("OAuth auth")
```

### 6. HyDE (Hypothetical Document Embeddings)

```python
from langchain.chains import HypotheticalDocumentEmbedder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Generate a hypothetical answer, embed THAT instead of the raw query
hyde_embeddings = HypotheticalDocumentEmbedder.from_llm(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    base_embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
    prompt_key="web_search",  # or custom prompt
)

# Now use hyde_embeddings as the embedding function in your vector store
vectorstore_hyde = Chroma(
    collection_name="docs",
    embedding_function=hyde_embeddings,
    persist_directory="./chroma_db",
)
```

### 7. Full Retrieval Pipeline (Combining Techniques)

```python
from langchain.retrievers import ContextualCompressionRetriever, EnsembleRetriever

# Step 1: Hybrid search (BM25 + vector)
hybrid = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7],
)

# Step 2: Re-rank the hybrid results
final_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=hybrid,
)

# This gives: keyword coverage + semantic understanding + precision re-ranking
docs = final_retriever.invoke("How do I handle token refresh in OAuth?")
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Top-K (initial retrieval) | 10-20 (before reranking), 3-5 (final) | Over-retrieve then filter is better than under-retrieve |
| Re-ranker model | cross-encoder/ms-marco-MiniLM-L-6-v2 | Best speed/quality ratio for re-ranking |
| Re-ranker top_n | 3-5 (feed to LLM) | Enough context without noise |
| Hybrid weights | 0.3 BM25 / 0.7 vector | Semantic dominates, BM25 catches keyword matches |
| MMR lambda_mult | 0.5-0.7 | Balance relevance vs diversity |
| Multi-query variants | 3 | Diminishing returns after 3 |
| Similarity threshold | 0.7-0.8 (cosine) | Filter out clearly irrelevant results |
| HyDE temperature | 0.0 | Deterministic hypothetical doc for consistent retrieval |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Correct doc exists but not in top-K | Embedding mismatch (query phrased differently than doc) | Try HyDE, multi-query, or hybrid search |
| Top-K has right docs but LLM still gets wrong answer | Too many irrelevant docs diluting context | Add re-ranking, reduce final top_n |
| Keyword-specific queries fail | Vector search bad at exact matches ("error code 403") | Add BM25/hybrid search |
| Results are redundant (same info repeated) | Multiple overlapping chunks from same section | Use MMR, or deduplicate by source document |
| Re-ranker makes results worse | Re-ranker not trained on your domain | Try different cross-encoder, or fine-tune |
| Query expansion generates irrelevant variants | LLM misunderstands the query intent | Constrain expansion prompt, add domain context |
| Metadata filter returns empty results | Filter too restrictive or metadata values incorrect | Log filter + result count, verify metadata |

## Production Considerations

### Latency Budget

| Step | Typical Latency | Notes |
|------|----------------|-------|
| Embedding query | 5-50ms (local), 100-300ms (API) | Usually cached for repeated queries |
| Vector search (HNSW) | 5-50ms | Near-constant for well-tuned HNSW |
| BM25 search | 10-100ms | Depends on corpus size |
| Re-ranking (cross-encoder) | 50-200ms for 20 candidates | Main latency cost — limit candidates |
| Total retrieval | 100-500ms | Before LLM generation even starts |

### Cost
- Multi-query: 1 LLM call per retrieval (cheap with gpt-4o-mini)
- HyDE: 1 LLM call + 1 extra embedding call per retrieval
- Re-ranking: free (local cross-encoder) or API-priced (Cohere rerank)
- Trade-off: More retrieval steps = better quality but higher latency + cost

### Monitoring
- Track: retrieval latency, result count (should never be 0), re-ranker score distribution
- Alert on: zero results returned, latency > 2x baseline, score distribution shift
- Log: queries that produce poor downstream answers → improve retrieval for those patterns

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| Recall@5 | % of queries where relevant doc in top 5 | > 85% |
| Recall@10 | % of queries where relevant doc in top 10 | > 95% |
| Precision@5 | % of top-5 results that are actually relevant | > 60% |
| MRR | Mean reciprocal rank of first relevant result | > 0.7 |
| NDCG@10 | Quality of ranking (not just presence) | > 0.75 |
| Downstream faithfulness | Does better retrieval → better answers? | Correlation > 0.8 |
| Retrieval latency | End-to-end retrieval time | < 500ms p95 |

## Ready to Ship? — Checklist

- [ ] Baseline retrieval metrics measured (recall, MRR)
- [ ] Top-K value justified (not just default 4)
- [ ] Metadata filters working for known categories
- [ ] Re-ranking tested and metrics improved over baseline
- [ ] Hybrid search evaluated (does BM25 help for your queries?)
- [ ] Zero-result queries handled gracefully (fallback or user message)
- [ ] Retrieval latency within budget (< 500ms)
- [ ] Monitoring in place (latency, result counts, score distributions)
- [ ] Test set of 50+ query-relevance pairs for regression testing
