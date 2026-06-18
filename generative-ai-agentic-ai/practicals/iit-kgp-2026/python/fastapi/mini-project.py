"""
=============================================================================
MINI PROJECT: RAG-as-a-Service API
=============================================================================

PROBLEM STATEMENT:
Build a complete REST API that exposes a RAG system as a service. This is
the deployment architecture for your Module 5 capstone.

WHAT YOU'LL BUILD:
- /health → health check
- /ingest → upload and index documents
- /ask → query the knowledge base
- /stream → streaming answer (token by token)
- /sources → list indexed documents
- /clear → reset the knowledge base

WHY THIS MATTERS:
Every AI product needs an API layer. Your capstone will be evaluated as
a deployed application, not a Jupyter notebook. This project teaches the
standard production pattern: FastAPI + Pydantic + RAG backend.

ESTIMATED TIME: 45-60 minutes

SETUP: pip install fastapi uvicorn[standard] pydantic

RULES:
- Use Pydantic for ALL request/response models
- Use lifespan for initializing the "RAG backend" (mocked)
- Include proper error handling (404, 400, 500)
- Follow the TODOs in order

TO RUN: uvicorn mini-project:app --reload --port 8000
TO TEST: http://localhost:8000/docs (Swagger UI)
=============================================================================
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from contextlib import asynccontextmanager
import time


# =============================================================================
# Models (Request/Response Schemas)
# =============================================================================

# TODO 1: Define all Pydantic models

class HealthResponse(BaseModel):
    status: str
    indexed_documents: int
    total_chunks: int

class IngestRequest(BaseModel):
    """Request to ingest a document."""
    # TODO: title (str), content (str, min 10 chars), source (optional str)
    pass

class IngestResponse(BaseModel):
    """Response after ingestion."""
    # TODO: status, document_id, chunks_created
    pass

class AskRequest(BaseModel):
    """Question to the RAG system."""
    # TODO: question (str, min 1 char), top_k (int, 1-10, default 3),
    #       source_filter (optional), include_sources (bool, default True)
    pass

class Source(BaseModel):
    """A source document reference."""
    # TODO: document_title, chunk_text (first 100 chars), relevance_score
    pass

class AskResponse(BaseModel):
    """RAG answer with sources."""
    # TODO: answer, confidence (0-1), sources (List[Source]),
    #       processing_time_ms (float)
    pass

class DocumentInfo(BaseModel):
    """Info about an indexed document."""
    # TODO: id, title, source, chunks_count, indexed_at
    pass


# =============================================================================
# Mock RAG Backend (simulates real RAG behavior)
# =============================================================================

class MockRAGBackend:
    """Simulates a RAG system for the API layer."""

    def __init__(self):
        self.documents = []
        self.chunks = []

    def ingest(self, title: str, content: str, source: str = "upload") -> dict:
        """Ingest a document (mock: just stores it)."""
        doc_id = f"doc_{len(self.documents) + 1}"
        # Simulate chunking (split by sentences)
        chunks = [s.strip() for s in content.split(".") if s.strip()]
        self.documents.append({
            "id": doc_id, "title": title, "source": source,
            "chunks_count": len(chunks), "indexed_at": "2026-06-18T10:00:00"
        })
        self.chunks.extend([{"doc_id": doc_id, "text": c, "title": title} for c in chunks])
        return {"document_id": doc_id, "chunks_created": len(chunks)}

    def query(self, question: str, top_k: int = 3, source_filter: str = None) -> dict:
        """Query the knowledge base (mock: returns fake relevant results)."""
        # Simulate retrieval (in reality: embed query → vector search)
        relevant = self.chunks[:top_k] if self.chunks else []
        if source_filter:
            relevant = [c for c in self.chunks if source_filter in c.get("title", "")][:top_k]

        if not relevant:
            return {
                "answer": "I don't have information about that in my knowledge base.",
                "confidence": 0.0,
                "sources": []
            }

        # Simulate answer generation
        context = " ".join([c["text"] for c in relevant])
        return {
            "answer": f"Based on the available documents: {context[:200]}...",
            "confidence": 0.85,
            "sources": [
                {"document_title": c["title"], "chunk_text": c["text"][:100], "relevance_score": 0.9 - i*0.1}
                for i, c in enumerate(relevant)
            ]
        }

    def stream_query(self, question: str):
        """Stream answer word by word (simulates LLM streaming)."""
        result = self.query(question)
        words = result["answer"].split()
        for word in words:
            yield word + " "
            time.sleep(0.05)  # simulate LLM generation delay

    def get_documents(self) -> List[dict]:
        """List all indexed documents."""
        return self.documents

    def clear(self):
        """Clear all indexed data."""
        self.documents = []
        self.chunks = []


# =============================================================================
# TODO 2: App Lifespan (Initialize Backend)
# =============================================================================
# Load the RAG backend at startup and store in app.state.

# TODO: Define lifespan context manager
# TODO: Initialize MockRAGBackend and store in app.state.rag


# =============================================================================
# TODO 3: Create FastAPI App with CORS
# =============================================================================

# TODO: Create app with title, version, description, lifespan
# TODO: Add CORS middleware (allow all origins for development)

app = FastAPI(title="RAG-as-a-Service", version="1.0.0")


# =============================================================================
# TODO 4: Health Check Endpoint
# =============================================================================
# GET /health → HealthResponse

@app.get("/health")
def health():
    # TODO: Return health status with document/chunk counts
    pass


# =============================================================================
# TODO 5: Ingest Document Endpoint
# =============================================================================
# POST /ingest → IngestResponse
# Accept document content and index it.

@app.post("/ingest")
def ingest_document(request: IngestRequest):
    # TODO: Call backend.ingest(), return response
    pass


# =============================================================================
# TODO 6: Ask Question Endpoint
# =============================================================================
# POST /ask → AskResponse
# Query the knowledge base and return grounded answer.

@app.post("/ask")
def ask_question(request: AskRequest):
    # TODO: Call backend.query(), measure time, return structured response
    pass


# =============================================================================
# TODO 7: Streaming Endpoint
# =============================================================================
# POST /stream → StreamingResponse (Server-Sent Events)
# Stream the answer token by token.

@app.post("/stream")
def stream_answer(request: AskRequest):
    # TODO: Use StreamingResponse with backend.stream_query()
    pass


# =============================================================================
# TODO 8: List Documents Endpoint
# =============================================================================
# GET /sources → List[DocumentInfo]

@app.get("/sources")
def list_sources():
    # TODO: Return list of indexed documents
    pass


# =============================================================================
# TODO 9: Clear Knowledge Base
# =============================================================================
# DELETE /clear → confirmation message
# Include safety: require a confirmation query parameter.

@app.delete("/clear")
def clear_knowledge_base(confirm: bool = False):
    # TODO: If not confirmed, return 400. If confirmed, clear and return status.
    pass


# =============================================================================
# TODO 10: File Upload Endpoint
# =============================================================================
# POST /upload → IngestResponse
# Accept a text file, read content, ingest it.

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # TODO: Read file content, call backend.ingest(), return response
    pass


# =============================================================================
# Run with: uvicorn mini_project:app --reload
# Test at: http://localhost:8000/docs
# =============================================================================
