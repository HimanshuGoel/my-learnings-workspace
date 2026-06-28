# FastAPI Serving

## What You're Deploying

Your AI system from Modules 2-4 — a RAG pipeline, fine-tuned model, or LangGraph agent — exposed as a production HTTP API. FastAPI is the standard choice for Python AI services: async-native, auto-docs, type-safe, and integrates with all ML libraries. You already know FastAPI patterns — this topic focuses on AI-SPECIFIC serving concerns.

## Prerequisites & Dependencies

- Working AI system (RAG pipeline, agent, or model) tested locally
- Python 3.11+, FastAPI, uvicorn, pydantic
- LangServe (optional — auto-serves LangChain/LangGraph runnables)
- API key management (env vars or secrets manager)

## Step-by-Step Procedure

### 1. Project Structure

```
my-ai-service/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app + routes
│   ├── config.py         # Settings (pydantic-settings)
│   ├── models.py         # Request/Response schemas
│   ├── dependencies.py   # Shared state (LLM clients, vector stores)
│   ├── routers/
│   │   ├── chat.py       # /chat endpoint (streaming)
│   │   ├── rag.py        # /query endpoint (RAG)
│   │   └── health.py     # /health, /ready
│   ├── services/
│   │   ├── rag_pipeline.py
│   │   ├── agent.py
│   │   └── cache.py
│   └── middleware/
│       ├── auth.py
│       ├── rate_limit.py
│       └── logging.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── tests/
```

### 2. Core Application Setup

```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import chat, rag, health
from app.dependencies import init_resources, shutdown_resources

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize expensive resources once at startup."""
    await init_resources()  # Load models, connect to vector store, warm cache
    yield
    await shutdown_resources()  # Cleanup connections

app = FastAPI(
    title="AI Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router, tags=["health"])
app.include_router(chat.router, prefix="/v1", tags=["chat"])
app.include_router(rag.router, prefix="/v1", tags=["rag"])
```

### 3. Request/Response Models

```python
# app/models.py
from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    thread_id: str = Field(default="default")
    stream: bool = Field(default=True)
    max_steps: int = Field(default=10, ge=1, le=20)

class ChatResponse(BaseModel):
    response: str
    sources: list[str] = []
    tokens_used: int = 0
    latency_ms: float = 0
    cached: bool = False

class StreamEvent(BaseModel):
    type: str  # "token", "tool_call", "sources", "done", "error"
    content: str = ""
    metadata: dict = {}
```

### 4. Streaming Endpoint (SSE)

```python
# app/routers/chat.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.models import ChatRequest, StreamEvent
from app.services.agent import AgentService
import json, time

router = APIRouter()

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest, agent: AgentService = Depends()):
    async def event_generator():
        start = time.time()
        try:
            async for event in agent.stream(request):
                yield f"data: {event.model_dump_json()}\n\n"
            
            yield f"data: {StreamEvent(type='done', metadata={'ms': int((time.time()-start)*1000)}).model_dump_json()}\n\n"
        except Exception as e:
            yield f"data: {StreamEvent(type='error', content=str(e)).model_dump_json()}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/chat", response_model=ChatResponse)
async def chat_sync(request: ChatRequest, agent: AgentService = Depends()):
    """Non-streaming endpoint for simple integrations."""
    start = time.time()
    result = await agent.invoke(request)
    return ChatResponse(
        response=result.content,
        sources=result.sources,
        tokens_used=result.token_count,
        latency_ms=(time.time() - start) * 1000,
    )
```

### 5. Health & Readiness Probes

```python
# app/routers/health.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.dependencies import get_vectorstore, get_llm_client

router = APIRouter()

@router.get("/health")
async def liveness():
    """Is the process alive? (k8s liveness probe)"""
    return {"status": "ok"}

@router.get("/ready")
async def readiness():
    """Can we handle requests? (k8s readiness probe)"""
    checks = {}
    
    try:
        vs = get_vectorstore()
        vs.similarity_search("test", k=1)
        checks["vectorstore"] = "ok"
    except Exception as e:
        checks["vectorstore"] = f"error: {e}"
    
    try:
        llm = get_llm_client()
        # Lightweight ping — don't do full inference
        checks["llm_api"] = "ok"
    except Exception as e:
        checks["llm_api"] = f"error: {e}"
    
    all_ok = all(v == "ok" for v in checks.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={"ready": all_ok, "checks": checks},
    )
```

### 6. Shared Dependencies (Singleton Pattern)

```python
# app/dependencies.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from app.config import settings

_vectorstore = None
_llm = None

async def init_resources():
    """Called once at startup — load expensive resources."""
    global _vectorstore, _llm
    _vectorstore = Chroma(
        persist_directory=settings.chroma_path,
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
    )
    _llm = ChatOpenAI(model=settings.llm_model, temperature=0)

def get_vectorstore() -> Chroma:
    return _vectorstore

def get_llm_client() -> ChatOpenAI:
    return _llm
```

### 7. Configuration (Pydantic Settings)

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM
    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0
    
    # Vector Store
    chroma_path: str = "./chroma_db"
    embedding_model: str = "text-embedding-3-small"
    
    # Limits
    max_tokens_per_request: int = 4000
    max_requests_per_minute: int = 60
    request_timeout_seconds: int = 30
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 8. Running the Server

```bash
# Development
uvicorn app.main:app --reload --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
# OR with gunicorn for process management:
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Configuration Reference

| Env Var | Default | Purpose |
|---------|---------|---------|
| OPENAI_API_KEY | — (required) | LLM + embedding API key |
| LLM_MODEL | gpt-4o-mini | Which model to use |
| CHROMA_PATH | ./chroma_db | Vector store persistence |
| MAX_REQUESTS_PER_MINUTE | 60 | Rate limit per client |
| REQUEST_TIMEOUT_SECONDS | 30 | Per-request timeout |
| WORKERS | 4 | Uvicorn worker processes |
| LOG_LEVEL | info | Logging verbosity |

## Verification & Smoke Tests

```bash
# 1. Health check
curl http://localhost:8000/health
# → {"status": "ok"}

# 2. Readiness check
curl http://localhost:8000/ready
# → {"ready": true, "checks": {"vectorstore": "ok", "llm_api": "ok"}}

# 3. Sync query
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2+2?", "stream": false}'

# 4. Streaming query (SSE)
curl -N -X POST http://localhost:8000/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain RAG in 3 sentences"}'
```

## Monitoring & Alerting

| Metric | Alert Threshold | Tool |
|--------|----------------|------|
| Response latency p95 | > 5s | Prometheus histogram |
| Error rate (5xx) | > 1% | Prometheus counter |
| Request rate | > capacity | Prometheus gauge |
| Token usage/day | > daily budget | Custom counter |
| Memory usage | > 80% RSS | System metrics |

## Troubleshooting Guide

| Symptom | Likely Cause | Fix | Module 1 Connection |
|---------|--------------|-----|---------------------|
| Timeout on first request | Model/vectorstore loading on demand | Use lifespan (load at startup) | — |
| Inconsistent outputs | Temperature > 0 in production | Set temperature=0.0 | Decoding (Module 1) |
| Context window exceeded | Too many retrieved chunks in prompt | Reduce top-k, summarize, check token count | Tokenization (Module 1) |
| High latency (>5s) | No streaming, waiting for full response | Enable SSE streaming | — |
| Memory growing | Message history accumulating | Implement conversation window/summary | Context windows (Module 1) |
| Cost spike | No rate limiting or token caps | Add per-user rate limit + token budget | — |

## Security & Compliance

- Never put API keys in code — use env vars or secrets manager
- Validate all inputs with Pydantic (max length, allowed characters)
- Add CORS middleware (restrict origins in production)
- Log request metadata but NEVER log full user messages (privacy)
- Rate limit per API key / user ID

## Cost Management

| Traffic | Estimated Monthly Cost |
|---------|----------------------|
| 100 queries/day | ~$5 (API) + $30 (infra) |
| 1K queries/day | ~$20 (API) + $50 (infra) |
| 10K queries/day | ~$180 (API) + $200 (infra) |

## Maintenance & Updates

- Model update: Change LLM_MODEL env var → restart (zero code change)
- Vector store update: Re-index endpoint or background job
- Code update: CI/CD pipeline (Topic 8)
- Zero-downtime: Rolling restart with multiple workers or blue-green deploy
