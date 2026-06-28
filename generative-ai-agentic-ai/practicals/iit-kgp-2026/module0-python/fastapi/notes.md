# FastAPI — Notes

## What Problem Does This Library Solve?

FastAPI lets you build production-ready REST APIs in Python with automatic request validation, OpenAPI documentation, and async support — turning your ML models and RAG pipelines into HTTP endpoints that other applications can consume.

## Mental Model

Think of FastAPI as **Spring Boot for AI Engineers**. It gives you:
- **Decorators for routes** = like `@RestController` + `@GetMapping`
- **Pydantic models for validation** = like Spring's `@Valid` + DTOs
- **Automatic OpenAPI/Swagger** = built-in, no config needed
- **Async support** = like Node.js event loop but in Python
- **Dependency injection** = like Spring's `@Autowired`

It's the standard way to serve ML models and RAG systems as APIs. Your capstone (Module 5) will almost certainly use FastAPI.

## Where It Fits

```
Trained Model / RAG Pipeline / Agent
        │
        ▼
┌────────────────┐
│    FastAPI       │  ← wrap as HTTP endpoints (you are here)
└───────┬────────┘
        │ HTTP requests/responses
        ▼
┌────────────────────────────────┐
│  Consumers                      │
│  • Frontend (React, mobile app) │
│  • Other microservices          │
│  • Streamlit demo UI            │
│  • External clients             │
└────────────────────────────────┘
```

- **Before FastAPI:** Trained model, RAG chain, or agent logic (Python functions)
- **After FastAPI:** HTTP API that anyone/anything can call over the network
- **Talks to:** Pydantic (validation), LangChain/LlamaIndex (AI logic), uvicorn (server), Streamlit (demo UI)

## Core Concepts

### 1. Hello World — Minimal API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Run: uvicorn main:app --reload
# Visit: http://localhost:8000
# Docs: http://localhost:8000/docs (auto-generated Swagger UI!)
```

### 2. Path & Query Parameters

```python
# Path parameter (part of the URL)
@app.get("/users/{user_id}")
def get_user(user_id: int):  # auto-validates: must be int
    return {"user_id": user_id}

# Query parameters (after ? in URL)
@app.get("/search")
def search(query: str, limit: int = 10, offset: int = 0):
    # GET /search?query=hello&limit=5
    return {"query": query, "limit": limit, "offset": offset}

# Optional parameters
from typing import Optional

@app.get("/items")
def list_items(category: Optional[str] = None, min_price: float = 0):
    return {"category": category, "min_price": min_price}
```

### 3. Request Body (POST with Pydantic)

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(min_length=1, description="The user's question")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of results")
    filter_source: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float = Field(ge=0, le=1)

@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    # request is automatically validated by Pydantic!
    # If invalid → 422 Unprocessable Entity with error details
    answer = rag_chain.invoke(request.question)
    return QueryResponse(
        answer=answer,
        sources=["doc1.pdf", "doc2.pdf"],
        confidence=0.92
    )
```

**Key insight:** FastAPI + Pydantic = automatic request validation + response serialization + OpenAPI docs. All from the type hints.

### 4. Async Endpoints (for I/O-bound tasks)

```python
import httpx

# Async endpoint (non-blocking — handles many requests concurrently)
@app.post("/generate")
async def generate(request: QueryRequest):
    # async is ideal for: LLM API calls, database queries, file I/O
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.openai.com/v1/chat/completions", ...)
    return {"result": response.json()}

# Sync endpoint (blocking — fine for CPU-bound or quick tasks)
@app.get("/predict")
def predict(text: str):
    # sync is fine for: model inference, computation
    result = model.predict(text)
    return {"prediction": result}
```

**When to use async:** LLM API calls, database queries, external HTTP calls (anything that waits for I/O). When to use sync: local model inference, CPU computation.

### 5. Dependency Injection

```python
from fastapi import Depends

# Define dependencies (like Spring @Bean)
def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

def get_rag_chain():
    # Initialize once, reuse across requests
    return create_rag_chain()

# Inject into endpoints
@app.post("/query")
def query(request: QueryRequest, chain = Depends(get_rag_chain)):
    return chain.invoke(request.question)

@app.get("/users")
def get_users(db = Depends(get_db)):
    return db.query("SELECT * FROM users")
```

### 6. Startup/Shutdown (Load Model Once)

```python
from contextlib import asynccontextmanager

# Load expensive resources at startup, clean up at shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model, build index, connect DB
    app.state.model = load_model()
    app.state.index = build_rag_index()
    print("Model loaded!")
    yield
    # Shutdown: cleanup
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def predict(text: str):
    model = app.state.model  # access pre-loaded model
    return {"result": model.predict(text)}
```

### 7. Error Handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Custom exception handler
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"error": str(exc)})
```

### 8. Streaming Responses (for LLM output)

```python
from fastapi.responses import StreamingResponse

@app.post("/stream")
async def stream_response(request: QueryRequest):
    async def generate():
        async for chunk in rag_chain.astream(request.question):
            yield f"data: {chunk}\n\n"  # Server-Sent Events format
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 9. CORS (Cross-Origin Resource Sharing)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 10. File Upload

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    # Process: chunk → embed → store in vector DB
    return {"filename": file.filename, "size": len(content)}
```

## Key Functions/Methods

### Route Decorators

| Decorator | HTTP Method | Use Case |
|-----------|-------------|----------|
| `@app.get("/path")` | GET | Read data, search |
| `@app.post("/path")` | POST | Create, query (send body) |
| `@app.put("/path")` | PUT | Full update |
| `@app.patch("/path")` | PATCH | Partial update |
| `@app.delete("/path")` | DELETE | Remove |

### Response Options

| Parameter | Purpose |
|-----------|---------|
| `response_model=Model` | Validate & filter response |
| `status_code=201` | Custom status code |
| `tags=["users"]` | Group in docs |
| `summary="..."` | Endpoint description |

### Common Imports

| Import | Purpose |
|--------|---------|
| `FastAPI` | The app |
| `Depends` | Dependency injection |
| `HTTPException` | Error responses |
| `UploadFile, File` | File uploads |
| `BackgroundTasks` | Async background work |
| `StreamingResponse` | Streaming output |

## Common Patterns

### ML Model Serving

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("model.joblib")
    yield

app = FastAPI(lifespan=lifespan)

class PredictRequest(BaseModel):
    features: List[float]

class PredictResponse(BaseModel):
    prediction: int
    probability: float

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    proba = app.state.model.predict_proba([request.features])[0]
    return PredictResponse(
        prediction=int(proba.argmax()),
        probability=float(proba.max())
    )
```

### RAG API Endpoint

```python
class RAGRequest(BaseModel):
    question: str
    top_k: int = 3
    source_filter: Optional[str] = None

class RAGResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: float

@app.post("/ask", response_model=RAGResponse)
async def ask(request: RAGRequest):
    result = await rag_chain.ainvoke(request.question)
    return RAGResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )
```

### Health Check + Metadata

```python
@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": app.state.model is not None}

@app.get("/info")
def info():
    return {
        "version": "1.0.0",
        "model": "gpt-4o-mini",
        "index_size": app.state.index.count(),
    }
```

## AI/ML Connection

- **Where in the AI pipeline:** FastAPI is the deployment layer — it wraps your trained model/RAG pipeline/agent as HTTP endpoints that clients (frontends, other services) can call.

- **Concrete example — Capstone (Module 5):** Build a RAG chatbot → wrap with FastAPI → add Streamlit frontend → deploy. This is the standard Module 5 architecture.

- **Concrete example — Model Serving:** Load sklearn/PyTorch model at startup → expose `/predict` endpoint → return predictions as JSON. Production ML serving in 20 lines.

- **Concrete example — Streaming LLM Output:** User asks a question → FastAPI streams the LLM response token by token via Server-Sent Events → frontend displays incrementally (like ChatGPT).

- **Which IIT KGP modules use this:** Module 5 (deployment, serving, capstone API layer). Also useful in Module 2/4 for building demo APIs.

- **What breaks without it:** Your model/RAG system only works as a Python script. FastAPI makes it accessible to any client over HTTP — frontends, mobile apps, other microservices.

- **FastAPI vs Flask:** FastAPI is faster (async), has built-in validation (Pydantic), auto-generates docs (Swagger), and has better type safety. Flask is simpler but lacks these features. For AI/ML serving, FastAPI is the modern standard.

## Common Mistakes

1. **Not using `lifespan` for model loading** — loading a model inside an endpoint means it loads on every request (slow!). Use lifespan to load once at startup.

2. **Blocking async endpoints with sync code** — if you use `async def` but call synchronous functions (like sklearn predict), it blocks the event loop. Use plain `def` for sync work, or run sync code in a thread pool.

3. **Forgetting CORS middleware** — frontend apps on different ports/domains get blocked. Add CORSMiddleware for development.

4. **Not using `response_model`** — without it, you might accidentally leak internal data. response_model filters the output to only declared fields.

5. **Hardcoding config** — use environment variables (via Pydantic Settings) for API keys, model paths, and ports.

6. **Not handling errors gracefully** — unhandled exceptions return 500 with stack traces. Use HTTPException for expected errors and exception handlers for unexpected ones.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Quick demo/prototype UI | Streamlit (one-file interactive app) |
| Simple script (no HTTP needed) | Just run the Python script |
| Very high throughput inference | vLLM, TorchServe, Triton |
| GraphQL API | Strawberry, Ariadne |
| Background job processing | Celery, Redis Queue |
| Static file serving | nginx, S3 |

## Ready to Move On?

- ☐ I can create a FastAPI app with GET and POST endpoints
- ☐ I can use Pydantic models for request validation and response schemas
- ☐ I can load a model at startup using lifespan
- ☐ I understand when to use async vs sync endpoints
- ☐ I can access auto-generated docs at /docs

Once all checked → move to **MLflow**.
