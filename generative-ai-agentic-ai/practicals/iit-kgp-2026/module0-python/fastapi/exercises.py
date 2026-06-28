"""
FastAPI Exercises — 10 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. AI-relevant exercises are marked with [AI].

SETUP: pip install fastapi uvicorn[standard] httpx
TEST: Each exercise creates a mini app. Test with:
  uvicorn exercises:app --reload  (for manual testing via /docs)
  OR use the TestClient in the test section at the bottom.

Run tests: python exercises.py
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing import Optional, List

# =============================================================================
# EASY (1-4)
# =============================================================================

# Exercise 1: Hello World API
# Create an app with:
#   GET /           → {"message": "Hello World"}
#   GET /health     → {"status": "healthy"}
#   GET /info       → {"version": "1.0.0", "name": "My API"}
# Test all three endpoints.
# Expected: all return correct JSON

def exercise_1():
    app = FastAPI()
    # Your code here: define 3 GET endpoints
    # Test:
    # client = TestClient(app)
    # assert client.get("/").json() == {"message": "Hello World"}
    pass


# Exercise 2: Path and Query Parameters
# Create endpoints:
#   GET /users/{user_id}          → returns user_id (int validated)
#   GET /search?q=hello&limit=5   → returns query params
#   GET /items?category=books     → optional category filter
# Test: /users/abc should return 422 (validation error).
# Expected: type validation works automatically

def exercise_2():
    app = FastAPI()
    # Your code here
    pass


# Exercise 3: POST with Pydantic Request Body
# Create:
#   POST /create-user with body: {name: str, email: str, age: int}
#   Validate: name min 1 char, age >= 18
#   Return: same user data + generated id
# Test: invalid data should return 422.
# Expected: Pydantic validates request body automatically

def exercise_3():
    app = FastAPI()
    # Your code here: define request model, response model, endpoint
    pass


# Exercise 4: Response Model (Filter Output)
# Create:
#   A User model with: id, name, email, password_hash (internal)
#   A UserResponse model with: id, name, email (no password!)
#   GET /users/{id} → returns UserResponse (password filtered out)
# response_model ensures internal fields never leak to clients.
# Expected: password_hash NOT in response

def exercise_4():
    app = FastAPI()
    # Your code here
    pass


# =============================================================================
# MEDIUM (5-7)
# =============================================================================

# Exercise 5: ML Model Prediction Endpoint [AI]
# Simulate serving a trained model:
#   POST /predict with body: {features: List[float]}
#   Validate: features must have exactly 4 values (iris dataset)
#   Return: {prediction: int, class_name: str, confidence: float}
# Use a mock model (no sklearn needed).
# This is the standard ML serving pattern.
# Expected: validated input → prediction response

def exercise_5():
    app = FastAPI()
    # Simulated model
    class_names = ["setosa", "versicolor", "virginica"]
    
    # Your code here: define models, endpoint, mock prediction logic
    pass


# Exercise 6: RAG Query Endpoint [AI]
# Build a RAG API endpoint:
#   POST /ask with body: {question: str, top_k: int=3, source_filter: Optional[str]}
#   Response: {answer: str, sources: List[Source], confidence: float}
#   Source: {document: str, page: int, score: float}
# Use mock data (no real RAG needed).
# This is your Module 5 capstone API pattern.
# Expected: structured RAG response with sources

def exercise_6():
    app = FastAPI()
    # Your code here
    pass


# Exercise 7: Error Handling
# Create an endpoint that:
#   GET /items/{id} → returns item if exists, 404 if not
#   POST /divide → {a: float, b: float} → returns {result: a/b}
#     If b==0, return 400 with error message
# Test: verify correct status codes for error cases.
# Expected: proper HTTP error codes with messages

def exercise_7():
    app = FastAPI()
    # Mock database
    items_db = {1: "Widget", 2: "Gadget", 3: "Doohickey"}
    # Your code here
    pass


# =============================================================================
# HARD (8-10)
# =============================================================================

# Exercise 8: Dependency Injection (Shared State) [AI]
# Use dependency injection to share a "model" across endpoints:
#   - Create a get_model() dependency that returns a mock model
#   - GET /model-info → returns model metadata (using injected model)
#   - POST /predict → uses injected model for prediction
# This pattern avoids loading the model in every request.
# Expected: model injected consistently across endpoints

def exercise_8():
    app = FastAPI()
    # Your code here: define dependency, inject into multiple endpoints
    pass


# Exercise 9: Streaming Response (LLM Style) [AI]
# Create a streaming endpoint that simulates LLM token-by-token output:
#   POST /stream → streams response word by word (SSE format)
#   Use Server-Sent Events: "data: {word}\n\n"
# Simulate with time.sleep between words.
# This is how ChatGPT-like streaming works in production.
# Expected: response arrives incrementally, not all at once

def exercise_9():
    app = FastAPI()
    # Your code here
    pass


# Exercise 10: Complete AI API (Multi-Endpoint) [AI]
# Build a complete API with:
#   GET  /health → health check
#   POST /embed → {texts: List[str]} → {embeddings: List[List[float]]}
#   POST /search → {query: str, k: int} → {results: List[SearchResult]}
#   POST /ask → {question: str} → {answer: str, sources: List[str]}
#   POST /upload → file upload → {status: "indexed", chunks: int}
# Use mock implementations. This is a production RAG API skeleton.
# Expected: all endpoints work with proper validation

def exercise_10():
    app = FastAPI(title="RAG API", version="1.0.0")
    # Your code here: define all models and endpoints
    pass


# =============================================================================
# Run tests
# =============================================================================

if __name__ == "__main__":
    print("FastAPI exercises are best tested with:")
    print("  1. uvicorn exercises:app --reload  (interactive at /docs)")
    print("  2. TestClient (programmatic)")
    print("\nRunning basic sanity checks...\n")

    # Quick test of exercise 1 pattern
    test_app = FastAPI()

    @test_app.get("/")
    def root():
        return {"message": "Hello World"}

    @test_app.get("/health")
    def health():
        return {"status": "healthy"}

    client = TestClient(test_app)
    assert client.get("/").json() == {"message": "Hello World"}
    assert client.get("/health").json()["status"] == "healthy"
    print("✓ Basic FastAPI pattern works!")
    print("\nFill in each exercise, then test with TestClient or /docs UI.")
