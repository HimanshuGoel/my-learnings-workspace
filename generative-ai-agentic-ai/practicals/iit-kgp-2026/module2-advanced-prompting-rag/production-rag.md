# Production RAG

## The Problem You're Solving

Your RAG pipeline works in a notebook but fails in production — cold starts are slow, costs spiral with traffic, errors cascade silently, and there's no way to know when quality degrades. Production RAG needs caching, error handling, streaming, monitoring, and cost controls that notebooks never need.

## Options Available

| Concern | Options | Trade-off |
|---------|---------|-----------|
| Caching | Semantic cache / Exact match cache / None | Quality vs speed vs cost |
| Streaming | Token-by-token / Chunk-based / Wait for full | Perceived latency vs complexity |
| Error handling | Fallback chain / Graceful degradation / Hard fail | Reliability vs accuracy guarantee |
| Rate limiting | Token bucket / Sliding window / Queue-based | Throughput vs fairness |
| Monitoring | Full trace / Sampled / Metrics-only | Observability vs storage cost |
| Deployment | Serverless / Container / VM | Scale flexibility vs cold start |

## Recommended Approach

**FastAPI + streaming + semantic caching + structured error handling + Prometheus metrics. Deploy in containers (Docker) with horizontal scaling.**


Why: FastAPI is what you'll deploy in Module 5. Streaming is table-stakes for UX. Semantic caching reduces cost by 30-60% for repeated similar queries. Container deployment is the standard for Python ML services.

## Step-by-Step Implementation

### 1. FastAPI Service Skeleton

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

app = FastAPI(title="RAG Service", version="1.0.0")

class QueryRequest(BaseModel):
    question: str
    collection: str = "default"
    stream: bool = True
    user_id: str | None = None

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    latency_ms: float
    cached: bool = False

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main RAG query endpoint."""
    import time
    start = time.time()
    
    # Check cache first
    cached = await cache.get(request.question)
    if cached:
        return QueryResponse(**cached, cached=True, latency_ms=0)
    
    # Run pipeline
    result = await pipeline.arun(request.question)
    latency = (time.time() - start) * 1000
    
    response = QueryResponse(
        answer=result.answer,
        sources=result.sources,
        latency_ms=latency,
    )
    
    # Cache the result
    await cache.set(request.question, response.dict())
    return response
```

### 2. Streaming Response

```python
from fastapi.responses import StreamingResponse
import json

@app.post("/query/stream")
async def query_stream(request: QueryRequest):
    """Stream RAG response token-by-token."""
    
    async def generate():
        # Retrieve context (non-streaming part)
        docs = await retriever.ainvoke(request.question)
        sources = [doc.metadata["source"] for doc in docs]
        
        # Send sources metadata first
        yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"
        
        # Stream LLM generation
        messages = build_prompt(request.question, docs)
        async for chunk in llm.astream(messages):
            if chunk.content:
                yield f"data: {json.dumps({'type': 'token', 'data': chunk.content})}\n\n"
        
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 3. Semantic Caching

```python
import hashlib
import numpy as np
from datetime import datetime, timedelta

class SemanticCache:
    """Cache RAG responses by query similarity, not exact match."""
    
    def __init__(self, vectorstore, threshold: float = 0.95, ttl_hours: int = 24):
        self.vectorstore = vectorstore
        self.threshold = threshold
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_store = {}  # In production: Redis
    
    async def get(self, query: str) -> dict | None:
        """Check if a similar query was recently answered."""
        results = self.vectorstore.similarity_search_with_score(query, k=1)
        
        if not results:
            return None
        
        doc, score = results[0]
        if score >= self.threshold:
            cache_key = doc.metadata["cache_key"]
            cached = self.cache_store.get(cache_key)
            
            if cached and datetime.now() - cached["timestamp"] < self.ttl:
                return cached["response"]
        
        return None
    
    async def set(self, query: str, response: dict):
        """Store query-response pair for future cache hits."""
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        # Store embedding for similarity lookup
        self.vectorstore.add_texts(
            texts=[query],
            metadatas=[{"cache_key": cache_key}],
        )
        
        # Store response
        self.cache_store[cache_key] = {
            "response": response,
            "timestamp": datetime.now(),
        }
```


### 4. Error Handling & Fallback Chain

```python
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class FallbackLevel(str, Enum):
    FULL = "full"          # Full pipeline
    NO_RERANK = "no_rerank"  # Skip reranking
    DIRECT_LLM = "direct_llm"  # No retrieval, just LLM
    APOLOGIZE = "apologize"  # "I can't answer right now"

class ResilientPipeline:
    """RAG pipeline with cascading fallbacks."""
    
    async def run(self, query: str) -> dict:
        # Try full pipeline
        try:
            return await self._full_pipeline(query)
        except RetrievalError as e:
            logger.warning(f"Retrieval failed: {e}, trying without rerank")
        
        # Fallback 1: Skip reranking
        try:
            return await self._no_rerank_pipeline(query)
        except Exception as e:
            logger.warning(f"Retrieval still failed: {e}, using direct LLM")
        
        # Fallback 2: Direct LLM (no retrieval)
        try:
            return await self._direct_llm(query)
        except Exception as e:
            logger.error(f"LLM failed: {e}")
        
        # Fallback 3: Apologize
        return {
            "answer": "I'm experiencing technical difficulties. Please try again in a moment.",
            "sources": [],
            "fallback_level": FallbackLevel.APOLOGIZE,
        }
    
    async def _full_pipeline(self, query: str):
        """Full pipeline with timeout."""
        return await asyncio.wait_for(
            self.pipeline.arun(query), timeout=10.0
        )
```

### 5. Rate Limiting & Cost Control

```python
from collections import defaultdict
import time

class TokenBudget:
    """Track and limit token spend per user/day."""
    
    def __init__(self, daily_limit: int = 100_000):
        self.daily_limit = daily_limit
        self.usage = defaultdict(lambda: {"tokens": 0, "reset_at": 0})
    
    def check_budget(self, user_id: str, estimated_tokens: int) -> bool:
        """Check if user has budget remaining."""
        user = self.usage[user_id]
        now = time.time()
        
        # Reset daily
        if now > user["reset_at"]:
            user["tokens"] = 0
            user["reset_at"] = now + 86400
        
        return (user["tokens"] + estimated_tokens) <= self.daily_limit
    
    def record_usage(self, user_id: str, actual_tokens: int):
        """Record actual token usage after generation."""
        self.usage[user_id]["tokens"] += actual_tokens


class CostTracker:
    """Track real-time cost across all API calls."""
    
    PRICING = {
        "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
        "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000},
        "text-embedding-3-small": {"input": 0.02 / 1_000_000},
    }
    
    def __init__(self):
        self.total_cost = 0.0
        self.daily_cost = 0.0
        self.daily_budget = 50.0  # $50/day max
    
    def record(self, model: str, input_tokens: int, output_tokens: int = 0):
        pricing = self.PRICING.get(model, {})
        cost = (
            input_tokens * pricing.get("input", 0) +
            output_tokens * pricing.get("output", 0)
        )
        self.total_cost += cost
        self.daily_cost += cost
        
        if self.daily_cost > self.daily_budget:
            raise BudgetExceeded(f"Daily budget ${self.daily_budget} exceeded")
```

### 6. Monitoring & Observability

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import structlog

# Prometheus metrics
query_counter = Counter("rag_queries_total", "Total queries", ["status", "cached"])
query_latency = Histogram("rag_query_duration_seconds", "Query latency", 
                          buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0])
active_queries = Gauge("rag_active_queries", "Currently processing queries")
retrieval_empty = Counter("rag_retrieval_empty_total", "Queries with zero retrieval results")
cost_total = Counter("rag_cost_dollars_total", "Total API cost in dollars")

# Structured logging
logger = structlog.get_logger()

async def monitored_query(request: QueryRequest):
    """Query with full observability."""
    active_queries.inc()
    
    with query_latency.time():
        try:
            result = await pipeline.arun(request.question)
            query_counter.labels(status="success", cached="false").inc()
            
            logger.info("query_completed",
                question=request.question[:100],
                sources=len(result.sources),
                answer_length=len(result.answer),
            )
            return result
            
        except Exception as e:
            query_counter.labels(status="error", cached="false").inc()
            logger.error("query_failed", error=str(e), question=request.question[:100])
            raise
        finally:
            active_queries.dec()
```

### 7. Health Check & Readiness

```python
@app.get("/health")
async def health_check():
    """Liveness probe — is the service running?"""
    return {"status": "ok"}

@app.get("/ready")
async def readiness_check():
    """Readiness probe — can the service handle queries?"""
    checks = {}
    
    # Check vector store connectivity
    try:
        vectorstore.similarity_search("test", k=1)
        checks["vectorstore"] = "ok"
    except Exception as e:
        checks["vectorstore"] = f"error: {e}"
    
    # Check LLM API connectivity
    try:
        await llm.ainvoke("test")
        checks["llm_api"] = "ok"
    except Exception as e:
        checks["llm_api"] = f"error: {e}"
    
    all_ok = all(v == "ok" for v in checks.values())
    status_code = 200 if all_ok else 503
    
    return JSONResponse(
        status_code=status_code,
        content={"ready": all_ok, "checks": checks}
    )
```


### 8. Document Ingestion Pipeline

```python
from pathlib import Path
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DocumentIngestionPipeline:
    """Watch for new/changed documents and index them."""
    
    def __init__(self, vectorstore, chunker, embedder):
        self.vectorstore = vectorstore
        self.chunker = chunker
        self.embedder = embedder
    
    async def ingest_file(self, file_path: Path):
        """Process a single file: load → chunk → embed → store."""
        logger.info("ingesting_file", path=str(file_path))
        
        # Load
        text = file_path.read_text(encoding="utf-8")
        
        # Chunk
        chunks = self.chunker.split_text(text)
        
        # Create metadata
        metadatas = [
            {
                "source": file_path.name,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "ingested_at": datetime.now().isoformat(),
            }
            for i in range(len(chunks))
        ]
        
        # Delete old chunks for this file
        self.vectorstore.delete(where={"source": file_path.name})
        
        # Embed and store
        self.vectorstore.add_texts(
            texts=chunks,
            metadatas=metadatas,
        )
        
        logger.info("file_ingested", path=str(file_path), chunks=len(chunks))
    
    async def ingest_directory(self, dir_path: Path):
        """Batch ingest all files in a directory."""
        files = list(dir_path.glob("**/*.md")) + list(dir_path.glob("**/*.txt"))
        
        for file in files:
            await self.ingest_file(file)
        
        logger.info("directory_ingested", path=str(dir_path), files=len(files))
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Streaming | Always on for user-facing | Perceived latency drops from 3s to <500ms |
| Cache TTL | 24 hours | Balance freshness vs cost savings |
| Cache similarity threshold | 0.95 | High enough to avoid wrong cache hits |
| Request timeout | 10s total, 5s per LLM call | Prevent hanging requests |
| Rate limit | 100 req/min per user | Prevent abuse, control cost |
| Daily budget | Set based on expected traffic | Hard stop prevents surprise bills |
| Max concurrent requests | 50-100 | Prevent resource exhaustion |
| Health check interval | 10s (liveness), 30s (readiness) | Fast failure detection |
| Log retention | 30 days detailed, 90 days metrics | Debug recent issues, trend long-term |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Cold start latency > 30s | Loading embedding model on first request | Pre-warm models at startup, use readiness probe |
| Cost spike | Cache miss rate increased (new query patterns) | Expand cache, add more general cache entries |
| Timeouts at scale | Too many concurrent LLM calls | Add request queue, limit concurrency |
| Memory growing unbounded | In-memory BM25 index or cache not evicting | Use external stores (Redis cache, ES for BM25) |
| Answers suddenly wrong | Corpus was updated, embeddings stale | Re-ingest changed documents, add ingestion pipeline |
| 5xx errors from LLM API | Rate limited or API outage | Implement retry with backoff, add fallback model |
| Streaming breaks mid-response | Client disconnect or timeout | Handle cancellation gracefully, clean up resources |

## Production Considerations

### Deployment Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│   Load       │────▶│  RAG Service │ (2-4 replicas)
│  (Browser)  │     │  Balancer    │     │  (FastAPI)   │
└─────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
                    ┌────────────────────────────┬┴──────────────────┐
                    │                            │                    │
              ┌─────▼──────┐          ┌─────────▼───┐      ┌───────▼──────┐
              │  Vector DB  │          │   LLM API   │      │    Redis     │
              │  (Qdrant)   │          │  (OpenAI)   │      │   (Cache)    │
              └─────────────┘          └─────────────┘      └──────────────┘
```

### Scaling Strategy
- **0-100 queries/day:** Single container, ChromaDB, in-memory cache
- **100-10K queries/day:** 2-4 containers, Qdrant, Redis cache
- **10K+ queries/day:** Auto-scaling, managed vector DB, CDN for static, queue for ingestion

### Cost at Scale
| Traffic | Estimated Monthly Cost |
|---------|----------------------|
| 1K queries/day | ~$20 (API) + $50 (infra) |
| 10K queries/day | ~$180 (API) + $200 (infra) |
| 100K queries/day | ~$1500 (API) + $500 (infra) |

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| Availability | Uptime percentage | > 99.5% |
| Latency (time to first token) | p95 from request to first streamed token | < 1.5s |
| Latency (total) | p95 end-to-end | < 5s |
| Error rate | 5xx responses / total requests | < 1% |
| Cache hit rate | Cached responses / total queries | > 30% |
| Cost per query | Total API spend / query count | < $0.002 |
| Throughput | Max queries/second sustained | > 10 qps |

## Ready to Ship? — Checklist

- [ ] FastAPI service running with streaming endpoint
- [ ] Semantic cache implemented and tested (verify cache hits)
- [ ] Error handling: graceful fallbacks, no unhandled exceptions
- [ ] Rate limiting in place (per user, per endpoint)
- [ ] Cost tracking active with daily budget alert
- [ ] Health and readiness endpoints passing
- [ ] Monitoring: latency, error rate, cache hit rate, cost dashboards
- [ ] Logging: structured logs with request tracing
- [ ] Deployment: containerized, scalable, with proper env config
- [ ] Load tested: confirmed behavior at 2-5x expected traffic
- [ ] Document ingestion pipeline automated (new docs auto-indexed)
- [ ] Runbook documented: what to do when each alert fires
