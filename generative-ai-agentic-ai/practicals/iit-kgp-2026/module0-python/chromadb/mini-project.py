"""
=============================================================================
MINI PROJECT: Personal Knowledge Base with Semantic Search
=============================================================================

PROBLEM STATEMENT:
Build a personal knowledge base that stores your notes/learnings as embeddings
and lets you semantically search across all your knowledge — like a personal
AI-powered search engine for everything you've learned.

WHAT YOU'LL BUILD:
- Document ingestion (add notes by topic)
- Smart chunking with metadata tracking
- Semantic search with confidence scoring
- Topic-based filtering
- "Related notes" discovery (find connections)
- Export relevant context for LLM prompting

WHY THIS MATTERS:
This is a personal RAG system. The same architecture powers:
- Notion AI (search your workspace semantically)
- GitHub Copilot Chat (search codebase)
- Any "chat with your docs" product

ESTIMATED TIME: 30-45 minutes

SETUP: pip install chromadb sentence-transformers

RULES:
- Use ChromaDB native API (no LangChain)
- All runs locally, no API keys
- Follow the TODOs in order
=============================================================================
"""

import chromadb
from chromadb.utils import embedding_functions
import hashlib
from datetime import datetime


# =============================================================================
# SETUP: Sample knowledge base entries
# =============================================================================

SAMPLE_NOTES = [
    {
        "topic": "machine-learning",
        "title": "Supervised vs Unsupervised Learning",
        "content": "Supervised learning uses labeled data to learn a mapping from inputs to outputs. "
                   "Examples: classification (spam detection), regression (price prediction). "
                   "Unsupervised learning finds patterns without labels. "
                   "Examples: clustering (customer segmentation), dimensionality reduction (PCA)."
    },
    {
        "topic": "machine-learning",
        "title": "Overfitting and Underfitting",
        "content": "Overfitting: model memorizes training data but fails on new data. Signs: high train "
                   "accuracy, low test accuracy. Fixes: more data, regularization, dropout, early stopping. "
                   "Underfitting: model too simple to capture patterns. Signs: low accuracy on both train "
                   "and test. Fixes: more complex model, more features, train longer."
    },
    {
        "topic": "deep-learning",
        "title": "Neural Network Basics",
        "content": "Neural networks consist of layers of neurons. Each neuron computes: output = "
                   "activation(weights * inputs + bias). Training uses backpropagation to compute gradients "
                   "and gradient descent to update weights. Key hyperparameters: learning rate, batch size, "
                   "number of layers, neurons per layer."
    },
    {
        "topic": "deep-learning",
        "title": "Transformer Architecture",
        "content": "Transformers process sequences in parallel using self-attention. Key components: "
                   "token embeddings, positional encoding, multi-head attention, feed-forward layers, "
                   "layer normalization. Attention computes: softmax(QK^T / sqrt(d)) * V. "
                   "This allows each token to attend to all other tokens simultaneously."
    },
    {
        "topic": "nlp",
        "title": "Tokenization Strategies",
        "content": "Tokenization converts text to token IDs. Types: word-level (simple but huge vocab), "
                   "character-level (tiny vocab but loses meaning), subword (BPE, WordPiece — best balance). "
                   "BERT uses WordPiece. GPT uses BPE. Always use the tokenizer paired with your model."
    },
    {
        "topic": "nlp",
        "title": "Embeddings and Semantic Similarity",
        "content": "Text embeddings are dense vectors representing meaning. Similar texts have similar "
                   "vectors. Measured by cosine similarity (dot product of normalized vectors). "
                   "Models: sentence-transformers (all-MiniLM-L6-v2 = fast, all-mpnet-base-v2 = accurate). "
                   "Used in: semantic search, RAG retrieval, clustering, recommendations."
    },
    {
        "topic": "rag",
        "title": "RAG Pipeline Steps",
        "content": "Retrieval-Augmented Generation: 1) Load documents 2) Split into chunks (500 chars, "
                   "50 overlap) 3) Embed chunks with sentence-transformer 4) Store in vector DB (ChromaDB) "
                   "5) At query time: embed query, find top-K similar chunks 6) Feed chunks as context to LLM "
                   "7) LLM generates answer grounded in the retrieved context."
    },
    {
        "topic": "rag",
        "title": "Chunking Strategies",
        "content": "Good chunking is critical for RAG quality. Recursive text splitter tries paragraph, "
                   "then sentence, then word boundaries. Chunk size 500-1000 chars works for most cases. "
                   "Overlap (50-100 chars) preserves context at boundaries. Semantic chunking groups by "
                   "meaning (more complex but better). Always include metadata: source, page, section."
    },
    {
        "topic": "python",
        "title": "NumPy Core Concepts",
        "content": "NumPy provides fast array operations via vectorization. Key: ndarray (fixed-type, "
                   "contiguous memory), broadcasting (auto-expand shapes), axes (axis=0 down, axis=1 across). "
                   "Common: reshape, slicing, boolean indexing, dot product, linalg.norm. "
                   "Everything in ML converts to/from NumPy arrays."
    },
    {
        "topic": "python",
        "title": "Pandas for Data Preparation",
        "content": "Pandas handles tabular data: load (read_csv), inspect (head, info, describe), "
                   "clean (dropna, fillna, drop_duplicates), transform (apply, get_dummies), "
                   "analyze (groupby, pivot_table), export (to_csv, to_numpy). 80% of data science "
                   "is data preparation — Pandas is where you spend most of your time."
    },
]


# =============================================================================
# TODO 1: Initialize Knowledge Base
# =============================================================================
# Create a ChromaDB persistent client and collection for the knowledge base.
# Use the cosine distance metric (best for text similarity).
# Use SentenceTransformer embedding function.

def init_knowledge_base(db_path="./knowledge_base_db"):
    """Initialize the ChromaDB knowledge base."""
    # TODO: Create PersistentClient
    # TODO: Create embedding function (SentenceTransformer)
    # TODO: Create collection with cosine distance metric
    # TODO: Return client, collection
    pass


# =============================================================================
# TODO 2: Add Notes to Knowledge Base
# =============================================================================
# Add notes with proper chunking and metadata:
#   - Generate ID from content hash (prevents duplicates)
#   - Store metadata: topic, title, added_date
#   - Handle the case where content is too long (split into chunks)
#   - Use upsert to handle re-adding same content

def add_note(collection, topic, title, content):
    """Add a note to the knowledge base."""
    # TODO: Generate unique ID (hash of content)
    # TODO: Create metadata dict
    # TODO: Upsert into collection
    # TODO: Print confirmation
    pass


# =============================================================================
# TODO 3: Search Knowledge Base
# =============================================================================
# Implement semantic search with:
#   - Top-K results
#   - Optional topic filter
#   - Confidence threshold (skip low-similarity results)
#   - Return structured results with score, title, content

def search(collection, query, k=3, topic=None, min_similarity=0.3):
    """Search the knowledge base semantically."""
    # TODO: Build where filter if topic specified
    # TODO: Query collection
    # TODO: Filter by similarity threshold
    # TODO: Format and return results
    pass


# =============================================================================
# TODO 4: Find Related Notes
# =============================================================================
# Given a note ID, find other notes that are similar to it.
# This discovers connections between topics you might not have noticed.

def find_related(collection, note_id, k=3):
    """Find notes related to a given note."""
    # TODO: Get the note by ID
    # TODO: Use its text as a query
    # TODO: Exclude itself from results
    # TODO: Return related notes
    pass


# =============================================================================
# TODO 5: Knowledge Base Stats
# =============================================================================
# Print statistics about the knowledge base:
#   - Total notes
#   - Notes per topic
#   - Average content length

def print_stats(collection):
    """Print knowledge base statistics."""
    # TODO: Get all documents with metadata
    # TODO: Count per topic
    # TODO: Compute avg content length
    # TODO: Print formatted stats
    pass


# =============================================================================
# TODO 6: Export Context for LLM
# =============================================================================
# Given a question, retrieve relevant notes and format them as context
# ready to insert into an LLM prompt.
# Format: "## {title}\n{content}\n\n" for each retrieved note

def get_context_for_llm(collection, question, k=3):
    """Retrieve and format context for LLM prompting."""
    # TODO: Search for relevant notes
    # TODO: Format as readable context block
    # TODO: Return formatted string
    pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    import shutil
    import os

    db_path = "./knowledge_base_db"
    
    print("=" * 60)
    print("PERSONAL KNOWLEDGE BASE")
    print("=" * 60)

    # Step 1: Initialize
    print("\n--- STEP 1: INITIALIZE ---")
    client, collection = init_knowledge_base(db_path)

    # Step 2: Ingest notes
    print("\n--- STEP 2: INGEST NOTES ---")
    for note in SAMPLE_NOTES:
        add_note(collection, note["topic"], note["title"], note["content"])

    # Step 3: Stats
    print("\n--- STEP 3: KNOWLEDGE BASE STATS ---")
    print_stats(collection)

    # Step 4: Search
    print("\n--- STEP 4: SEMANTIC SEARCH ---")
    queries = [
        ("How does attention work in transformers?", None),
        ("data cleaning steps", "python"),
        ("how to avoid overfitting", "machine-learning"),
        ("vector similarity search", None),
    ]
    for query, topic in queries:
        print(f"\nQ: {query}" + (f" [topic: {topic}]" if topic else ""))
        results = search(collection, query, k=2, topic=topic)
        if results:
            for r in results:
                print(f"  [{r.get('score', 0):.3f}] {r.get('title', 'N/A')}")

    # Step 5: Related notes
    print("\n--- STEP 5: FIND RELATED NOTES ---")
    # Find notes related to the first one
    all_docs = collection.get()
    if all_docs and all_docs["ids"]:
        related = find_related(collection, all_docs["ids"][0])
        if related:
            print(f"Notes related to '{all_docs['metadatas'][0].get('title', 'N/A')}':")
            for r in related:
                print(f"  - {r.get('title', 'N/A')}")

    # Step 6: Export for LLM
    print("\n--- STEP 6: EXPORT CONTEXT FOR LLM ---")
    context = get_context_for_llm(collection, "How to build a RAG system?")
    if context:
        print("Context for LLM prompt:")
        print(context[:500] + "..." if len(context) > 500 else context)

    # Cleanup
    print("\n--- CLEANUP ---")
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
        print(f"Removed {db_path}")

    print("\n" + "=" * 60)
    print("Done! You've built a personal knowledge base with semantic search.")
    print("=" * 60)


if __name__ == "__main__":
    main()
