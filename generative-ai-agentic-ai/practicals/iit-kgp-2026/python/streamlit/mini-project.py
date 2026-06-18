"""
=============================================================================
MINI PROJECT: RAG Chatbot Demo (Capstone Frontend Template)
=============================================================================

PROBLEM STATEMENT:
Build the frontend for your Module 5 capstone RAG application. This is a
complete Streamlit app that provides a ChatGPT-like interface over your own
documents — with file upload, chat, source display, and settings.

WHAT YOU'LL BUILD:
- Sidebar: model settings, file upload, document list
- Main area: chat interface with streaming
- Source display: show which documents answered the question
- Metrics: response time, confidence, token count
- Session management: persistent chat history

WHY THIS MATTERS:
This is the demo UI evaluators will interact with for your capstone.
A polished Streamlit frontend makes your project look professional
with minimal effort. Copy this template and connect to your real RAG backend.

ESTIMATED TIME: 30-40 minutes

SETUP: pip install streamlit

RUN: streamlit run mini-project.py

RULES:
- Use session_state for all persistent data
- Cache expensive operations (@st.cache_resource)
- Use st.spinner for loading states
- Follow the TODOs in order
=============================================================================
"""

import streamlit as st
import time
import random


# =============================================================================
# TODO 1: Page Configuration
# =============================================================================
# Configure the page: title, icon, layout (wide), sidebar state

# TODO: st.set_page_config(...)


# =============================================================================
# TODO 2: Session State Initialization
# =============================================================================
# Initialize all session state variables:
#   - messages: list of {"role": "user"/"assistant", "content": str}
#   - documents: list of uploaded document names
#   - settings: dict with model, temperature, top_k

def init_session_state():
    """Initialize session state variables."""
    # TODO: Initialize messages, documents, settings
    pass


# =============================================================================
# TODO 3: Simulated RAG Backend
# =============================================================================
# Mock RAG functions (replace with real backend when ready):
#   - ingest_document(name, content) → success message
#   - query(question, top_k) → {answer, sources, confidence, time_ms}
#   - stream_query(question) → yields words one by one

def mock_ingest(name, content):
    """Simulate document ingestion."""
    # TODO: Add to session_state.documents
    # TODO: Return success status
    pass

def mock_query(question, top_k=3):
    """Simulate RAG query."""
    # TODO: Return fake answer, sources, confidence
    time.sleep(0.5)  # simulate processing
    sources = [
        {"doc": "manual.pdf", "page": 3, "score": 0.92},
        {"doc": "faq.md", "page": 1, "score": 0.85},
    ]
    return {
        "answer": f"Based on the documents, here's what I found about '{question}': "
                  f"This is a simulated response that would normally come from your RAG pipeline. "
                  f"Connect this to your LangChain/LlamaIndex backend for real answers.",
        "sources": sources[:top_k],
        "confidence": random.uniform(0.75, 0.98),
        "time_ms": random.uniform(200, 800),
    }

def mock_stream(question):
    """Simulate streaming response."""
    response = mock_query(question)
    words = response["answer"].split()
    for word in words:
        yield word + " "
        time.sleep(0.03)


# =============================================================================
# TODO 4: Sidebar (Settings & Document Management)
# =============================================================================
# Build the sidebar with:
#   - App title/logo
#   - Model selection (selectbox)
#   - Temperature slider (0-2)
#   - Top-K slider (1-10)
#   - File uploader (PDF, TXT)
#   - List of uploaded documents
#   - Clear chat button

def render_sidebar():
    """Render the sidebar with settings and document management."""
    with st.sidebar:
        # TODO: Title
        # TODO: Model selectbox
        # TODO: Temperature slider
        # TODO: Top-K slider
        # TODO: File uploader
        # TODO: Show uploaded documents list
        # TODO: Clear chat button
        pass


# =============================================================================
# TODO 5: Chat Interface
# =============================================================================
# Build the main chat area:
#   - Display chat history from session_state
#   - Chat input at bottom
#   - On submit: add user message, generate response, add assistant message
#   - Use st.chat_message for role-based styling
#   - Use st.spinner during processing

def render_chat():
    """Render the chat interface."""
    # TODO: Display existing messages
    # TODO: Chat input
    # TODO: On new message: display user msg, generate response, display assistant msg
    pass


# =============================================================================
# TODO 6: Source Display
# =============================================================================
# After each response, show sources in an expander:
#   - Document name, page, relevance score
#   - Formatted as a mini table or bullet list

def render_sources(sources):
    """Display source documents used for the answer."""
    # TODO: Expander with source details
    pass


# =============================================================================
# TODO 7: Metrics Bar
# =============================================================================
# Show response metrics after each answer:
#   - Response time (ms)
#   - Confidence score
#   - Sources used (count)
# Use st.columns + st.metric

def render_metrics(result):
    """Display response metrics."""
    # TODO: 3 columns with metrics
    pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    init_session_state()
    render_sidebar()

    st.title("📚 Document QA Assistant")
    st.caption("Ask questions about your uploaded documents")

    render_chat()


if __name__ == "__main__":
    main()
