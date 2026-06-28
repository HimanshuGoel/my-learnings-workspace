# FastAPI — Cheatsheet

## Install & Run

```bash
pip install fastapi uvicorn[standard]
uvicorn main:app --reload --port 8000
# Docs: http://localhost:8000/docs
```

## Import

```python
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from contextlib import asynccontextmanager
```

---

## App & Routes

```python
app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "hello"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: Optional[str] = None):
    return {"id": item_id, "q": q}

@app.post("/create", status_code=201)
def create(data: MyModel):
    return data
```

---

## Request Body (Pydantic)

```python
class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)
    source: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    # request is auto-validated!
    return QueryResponse(answer="...", confidence=0.9, sources=["doc1"])
```

---

## Path & Query Parameters

```python
# Path: /users/42
@app.get("/users/{user_id}")
def get_user(user_id: int): ...

# Query: /search?q=hello&limit=5
@app.get("/search")
def search(q: str, limit: int = 10, offset: int = 0): ...

# Optional query
@app.get("/items")
def items(category: Optional[str] = None): ...
```

---

## Lifespan (Load Model at Startup)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.model = load_model()
    app.state.index = build_index()
    yield
    # Shutdown (cleanup)

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def predict():
    model = app.state.model  # pre-loaded!
```

---

## Async vs Sync

```python
# Async — for I/O (API calls, DB, file reads)
@app.post("/generate")
async def generate(req: Request):
    result = await llm_client.generate(req.prompt)
    return result

# Sync — for CPU work (model inference, computation)
@app.post("/predict")
def predict(req: Request):
    return model.predict(req.features)
```

---

## Dependency Injection

```python
def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

def get_settings():
    return Settings()

@app.get("/users")
def users(db = Depends(get_db), settings = Depends(get_settings)):
    return db.query("SELECT * FROM users")
```

---

## Error Handling

```python
@app.get("/items/{id}")
def get_item(id: int):
    item = db.find(id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item

# Custom handler
@app.exception_handler(ValueError)
async def handle_value_error(request, exc):
    return JSONResponse(status_code=400, content={"error": str(exc)})
```

---

## Streaming (LLM Output)

```python
from fastapi.responses import StreamingResponse

@app.post("/stream")
async def stream(request: QueryRequest):
    async def generate():
        async for chunk in chain.astream(request.question):
            yield f"data: {chunk}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

## File Upload

```python
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
```

---

## CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Background Tasks

```python
from fastapi import BackgroundTasks

def process_document(doc_id: str):
    # Long-running task (indexing, embedding)
    ...

@app.post("/ingest")
def ingest(doc_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_document, doc_id)
    return {"status": "processing"}
```

---

## Testing

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}

def test_query():
    response = client.post("/query", json={"question": "What is AI?", "top_k": 3})
    assert response.status_code == 200
    assert "answer" in response.json()
```

---

## Quick Reference Links

- Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- Deployment: https://fastapi.tiangolo.com/deployment/
