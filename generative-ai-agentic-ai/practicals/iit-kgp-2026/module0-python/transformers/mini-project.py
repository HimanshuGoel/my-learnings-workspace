"""
=============================================================================
MINI PROJECT: Build a Semantic FAQ Bot (Embeddings + Retrieval + Generation)
=============================================================================

PROBLEM STATEMENT:
Build an FAQ bot that answers user questions by:
1. Finding the most relevant FAQ entries using semantic similarity
2. Using the matched FAQ as context to generate a natural answer

This is a simplified RAG (Retrieval-Augmented Generation) system — exactly
what you'll build in Module 2, but distilled to its core mechanics.

WHAT YOU'LL BUILD:
- FAQ knowledge base with embeddings
- Semantic search (query → most similar FAQ)
- Answer generation using retrieved context
- Confidence scoring (how sure are we?)
- Fallback handling (when no FAQ matches)

WHY THIS MATTERS:
RAG is THE architecture for building AI assistants that can answer questions
about your own data (documents, FAQs, manuals). This project teaches the
core pattern: embed → retrieve → generate. Every enterprise AI chatbot
(customer support, internal docs, code assistants) uses this pattern.

ESTIMATED TIME: 30-45 minutes

SKILLS PRACTICED:
- SentenceTransformer for embeddings
- Cosine similarity for retrieval
- pipeline() for generation
- Combining multiple HuggingFace components

SETUP: pip install transformers sentence-transformers torch

RULES:
- Use sentence-transformers for embeddings
- Use transformers pipeline for generation (or just return the FAQ answer)
- No external APIs (everything runs locally)
- Follow the TODOs in order
=============================================================================
"""

import numpy as np
from typing import List, Tuple


# =============================================================================
# SETUP: FAQ Knowledge Base
# =============================================================================

FAQ_DATA = [
    {
        "question": "How do I reset my password?",
        "answer": "Go to Settings > Account > Reset Password. Click the reset link sent to your email. The link expires in 24 hours."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept Visa, Mastercard, American Express, PayPal, and bank transfers. All payments are encrypted and secure."
    },
    {
        "question": "How long does shipping take?",
        "answer": "Standard shipping takes 5-7 business days. Express shipping takes 1-2 business days. International orders take 10-14 days."
    },
    {
        "question": "What is your return policy?",
        "answer": "You can return items within 30 days of delivery for a full refund. Items must be in original packaging and unused condition."
    },
    {
        "question": "How do I cancel my subscription?",
        "answer": "Go to Settings > Subscription > Cancel. Your access continues until the end of the billing cycle. No partial refunds for cancellations."
    },
    {
        "question": "Do you offer student discounts?",
        "answer": "Yes! Students get 20% off with a valid .edu email address. Verify your student status at checkout to apply the discount."
    },
    {
        "question": "How do I contact customer support?",
        "answer": "Email us at support@company.com or use the live chat on our website. Phone support is available Mon-Fri 9am-5pm EST at 1-800-SUPPORT."
    },
    {
        "question": "Is my data secure?",
        "answer": "We use AES-256 encryption for all stored data and TLS 1.3 for data in transit. We're SOC 2 Type II certified and GDPR compliant."
    },
    {
        "question": "Can I use the service on multiple devices?",
        "answer": "Yes, you can use your account on up to 5 devices simultaneously. Your data syncs automatically across all devices."
    },
    {
        "question": "What happens if I exceed my plan limits?",
        "answer": "You'll receive a notification at 80% and 100% usage. After 100%, service continues but at reduced speeds until the next billing cycle or upgrade."
    },
]


# =============================================================================
# TODO 1: Initialize Embedding Model
# =============================================================================
# Load the sentence-transformer model for computing embeddings.
# Use "all-MiniLM-L6-v2" (small, fast, 384-dimensional).
# Return the loaded model.

def load_embedding_model():
    """Load the sentence-transformer model."""
    # TODO: from sentence_transformers import SentenceTransformer
    # TODO: Load "all-MiniLM-L6-v2"
    # TODO: Return model
    pass


# =============================================================================
# TODO 2: Build FAQ Index
# =============================================================================
# Encode all FAQ questions into embeddings (pre-compute for fast search).
# Return:
#   - embeddings: numpy array of shape (num_faqs, 384)
#   - faq_data: the original FAQ list (for retrieval)

def build_faq_index(model, faq_data):
    """Pre-compute embeddings for all FAQ questions."""
    # TODO: Extract all questions from faq_data
    # TODO: Encode using model.encode()
    # TODO: Return embeddings array and faq_data
    pass


# =============================================================================
# TODO 3: Semantic Search
# =============================================================================
# Given a user query, find the top-K most similar FAQ entries:
#   a) Encode the query
#   b) Compute cosine similarity with all FAQ embeddings
#   c) Return top-K results with scores
#
# Return: list of (faq_entry, similarity_score) tuples, sorted by score desc

def search_faq(query: str, model, faq_embeddings, faq_data, top_k: int = 3) -> List[Tuple[dict, float]]:
    """Find most similar FAQs for a user query."""
    # TODO: Encode query
    # TODO: Compute cosine similarity with all FAQ embeddings
    # TODO: Get top-k indices
    # TODO: Return [(faq_entry, score), ...] sorted by score
    pass


# =============================================================================
# TODO 4: Confidence Check
# =============================================================================
# Determine if the top result is confident enough to answer:
#   - If top score > 0.6 → confident (answer directly)
#   - If 0.4 < top score <= 0.6 → low confidence (answer with caveat)
#   - If top score <= 0.4 → no match (fallback message)
#
# Return: (confidence_level, message)

def check_confidence(top_score: float) -> Tuple[str, str]:
    """Determine confidence level based on similarity score."""
    # TODO: Implement threshold logic
    pass


# =============================================================================
# TODO 5: Generate Answer
# =============================================================================
# Compose a natural answer based on the retrieved FAQ:
#   - If confident: return the FAQ answer directly
#   - If low confidence: "I'm not entirely sure, but here's what I found: {answer}"
#   - If no match: "I don't have information about that. Please contact support."
#
# Optionally: use a text generation model to rephrase the answer.

def generate_answer(query: str, search_results: List[Tuple[dict, float]]) -> str:
    """Generate a user-friendly answer based on search results."""
    # TODO: Check confidence of top result
    # TODO: Compose appropriate answer based on confidence
    pass


# =============================================================================
# TODO 6: Full FAQ Bot
# =============================================================================
# Combine everything into a single function:
#   query → search → confidence check → answer

class FAQBot:
    def __init__(self):
        """Initialize the FAQ bot with model and index."""
        # TODO: Load model
        # TODO: Build FAQ index
        pass

    def answer(self, query: str) -> dict:
        """Answer a user query. Returns dict with answer, confidence, sources."""
        # TODO: Search FAQs
        # TODO: Check confidence
        # TODO: Generate answer
        # TODO: Return structured response
        pass


# =============================================================================
# MAIN: Interactive Demo
# =============================================================================

def main():
    print("=" * 60)
    print("SEMANTIC FAQ BOT (RAG Pattern)")
    print("=" * 60)

    # Initialize
    print("\nLoading model and building index...")
    bot = FAQBot()
    print("Ready!\n")

    # Test queries
    test_queries = [
        "How can I change my password?",           # Clear match
        "Do you ship internationally?",            # Related to shipping FAQ
        "Can students get a discount?",            # Clear match
        "What's the meaning of life?",             # No match (fallback)
        "Is my credit card information safe?",     # Related to security FAQ
        "I want to cancel, will I get money back?",  # Combines cancel + return
    ]

    for query in test_queries:
        print(f"{'─'*50}")
        print(f"Q: {query}")
        result = bot.answer(query)
        if result:
            print(f"A: {result.get('answer', 'No answer')}")
            print(f"   Confidence: {result.get('confidence', 'unknown')}")
            print(f"   Source: {result.get('source_question', 'N/A')}")
            print(f"   Score: {result.get('score', 0):.3f}")
        print()

    # Interactive mode (optional)
    print(f"\n{'='*60}")
    print("Interactive mode (type 'quit' to exit):")
    print("=" * 60)
    while True:
        query = input("\nYour question: ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if not query:
            continue
        result = bot.answer(query)
        if result:
            print(f"Answer: {result.get('answer', 'No answer')}")
            print(f"(Confidence: {result.get('confidence')}, Score: {result.get('score', 0):.3f})")


if __name__ == "__main__":
    main()
