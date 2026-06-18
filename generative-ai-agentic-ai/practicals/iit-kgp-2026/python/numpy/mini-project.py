"""
=============================================================================
MINI PROJECT: Document Similarity Search Engine (NumPy Only)
=============================================================================

PROBLEM STATEMENT:
Build a simple document search engine that finds the most relevant documents
for a given query using vector similarity — the same core technique used in
RAG (Retrieval-Augmented Generation) systems.

WHAT YOU'LL BUILD:
- A function to create fake "embeddings" (numerical representations of text)
- A similarity search function using cosine similarity
- A ranking system that returns top-K most relevant documents
- Basic evaluation metrics (precision-like measure)

WHY THIS MATTERS:
This is exactly what happens inside ChromaDB, FAISS, and Pinecone (vector
databases you'll use in Module 2). They store document embeddings and retrieve
the most similar ones when you ask a question. You're building the math layer.

ESTIMATED TIME: 30-45 minutes

SKILLS PRACTICED:
- Array creation and manipulation
- Broadcasting
- Linear algebra (dot product, norms)
- Sorting and indexing
- Vectorized operations (no Python loops for computation)

RULES:
- Use ONLY NumPy (no sklearn, no scipy)
- No Python for-loops for the math — use vectorized operations
- Follow the TODOs in order
=============================================================================
"""

import numpy as np


# =============================================================================
# SETUP: Document corpus (simulated)
# =============================================================================

# In a real system, these would be actual text documents.
# Here we simulate 20 "documents" with titles for readability.
DOCUMENTS = [
    "Introduction to machine learning algorithms",
    "Deep learning with neural networks",
    "Natural language processing fundamentals",
    "Computer vision and image recognition",
    "Reinforcement learning for game playing",
    "Transfer learning and fine-tuning models",
    "Generative adversarial networks explained",
    "Transformer architecture and attention mechanism",
    "BERT and language model pre-training",
    "GPT models and text generation",
    "Retrieval augmented generation (RAG)",
    "Vector databases and similarity search",
    "Prompt engineering best practices",
    "LangChain for building AI applications",
    "Supervised learning classification techniques",
    "Unsupervised learning and clustering",
    "Feature engineering for tabular data",
    "Model evaluation metrics and validation",
    "Gradient descent optimization explained",
    "Convolutional neural networks for images",
]

# Simulate queries
QUERIES = [
    "How do transformers work?",
    "Building search with vectors",
    "Training image classifiers",
]

# Expected: Query 0 should match docs about transformers/attention (index 7, 8, 9)
# Expected: Query 1 should match docs about vector search/RAG (index 10, 11, 13)
# Expected: Query 2 should match docs about images/CNN/classification (index 3, 14, 19)


# =============================================================================
# TODO 1: Generate fake embeddings
# =============================================================================
# In production, you'd use a model like sentence-transformers to create these.
# Here, we'll generate deterministic fake embeddings using a seeded RNG.
# This simulates what an embedding model would output for each document.
#
# Create:
#   - doc_embeddings: shape (20, 64) — 20 documents, 64-dimensional embeddings
#   - query_embeddings: shape (3, 64) — 3 queries, 64-dimensional embeddings
#
# Use np.random.default_rng(seed=42) for reproducibility.
# Generate from standard normal distribution.

def generate_embeddings(n_docs=20, n_queries=3, dim=64, seed=42):
    """Generate fake document and query embeddings."""
    # TODO: Create a random number generator with the given seed
    # TODO: Generate doc_embeddings of shape (n_docs, dim)
    # TODO: Generate query_embeddings of shape (n_queries, dim)
    # TODO: Return both arrays
    pass


# =============================================================================
# TODO 2: Normalize embeddings
# =============================================================================
# Cosine similarity requires normalized vectors (unit vectors with length = 1).
# Normalize each embedding by dividing by its L2 norm.
# After normalization, cosine similarity = simple dot product.
#
# Input: matrix of shape (N, D)
# Output: matrix of shape (N, D) where each row has L2 norm = 1
#
# Hint: compute norm per row (axis=1), keep dims for broadcasting.

def normalize(embeddings):
    """Normalize each row to unit length (L2 norm = 1)."""
    # TODO: Compute L2 norm of each row
    # TODO: Divide each row by its norm (use broadcasting)
    # TODO: Return normalized embeddings
    pass


# =============================================================================
# TODO 3: Compute similarity matrix
# =============================================================================
# Compute cosine similarity between all queries and all documents.
# Since vectors are normalized, cosine similarity = dot product.
#
# Input:
#   - query_emb: shape (Q, D) — normalized query embeddings
#   - doc_emb: shape (N, D) — normalized document embeddings
# Output:
#   - similarity matrix: shape (Q, N) — sim[i][j] = similarity of query i to doc j
#
# This should be ONE matrix operation, no loops.

def compute_similarity(query_emb, doc_emb):
    """Compute cosine similarity matrix between queries and documents."""
    # TODO: Use matrix multiplication to compute all similarities at once
    # Hint: (Q, D) @ (D, N) = (Q, N) — you need to transpose doc_emb
    pass


# =============================================================================
# TODO 4: Retrieve top-K documents
# =============================================================================
# For each query, find the K most similar documents.
#
# Input:
#   - similarity_matrix: shape (Q, N)
#   - k: number of results to return
# Output:
#   - List of arrays, each containing the indices of top-K docs for that query
#     (sorted by similarity, highest first)
#
# Hint: np.argsort sorts ascending — you want descending. Use negative trick or [::-1].

def retrieve_top_k(similarity_matrix, k=5):
    """Return indices of top-K most similar documents for each query."""
    # TODO: For each query (row), find indices of K highest similarities
    # TODO: Return as a list of arrays
    pass


# =============================================================================
# TODO 5: Display results
# =============================================================================
# For each query, print:
#   - The query text
#   - Top-K document titles with their similarity scores
#   - Format: "  [rank] (score: 0.XX) Document title"

def display_results(queries, documents, similarity_matrix, top_k_indices):
    """Pretty-print search results."""
    # TODO: Loop through queries and their top-K results
    # TODO: Print query, then each result with rank, score, and title
    pass


# =============================================================================
# TODO 6: Evaluate search quality
# =============================================================================
# Simple evaluation: for each query, check how many of the expected relevant
# documents appear in the top-K results.
#
# Precision@K = (number of relevant docs in top-K) / K
#
# Input:
#   - top_k_indices: list of arrays with retrieved doc indices
#   - relevant_docs: list of sets with truly relevant doc indices per query
# Output:
#   - Average precision@K across all queries

def evaluate(top_k_indices, relevant_docs, k=5):
    """Compute average precision@K."""
    # TODO: For each query, count how many of top_k_indices are in relevant_docs
    # TODO: Compute precision = count / k
    # TODO: Return average precision across all queries
    pass


# =============================================================================
# MAIN: Bring it all together
# =============================================================================

def main():
    print("=" * 60)
    print("DOCUMENT SIMILARITY SEARCH ENGINE")
    print("=" * 60)

    # Step 1: Generate embeddings
    doc_emb, query_emb = generate_embeddings()
    print(f"\nDoc embeddings shape: {doc_emb.shape}")
    print(f"Query embeddings shape: {query_emb.shape}")

    # Step 2: Normalize
    doc_emb_norm = normalize(doc_emb)
    query_emb_norm = normalize(query_emb)

    # Verify normalization: each row should have norm ≈ 1.0
    norms = np.linalg.norm(doc_emb_norm, axis=1)
    print(f"\nNorm check (should all be 1.0): min={norms.min():.4f}, max={norms.max():.4f}")

    # Step 3: Compute similarity
    sim_matrix = compute_similarity(query_emb_norm, doc_emb_norm)
    print(f"\nSimilarity matrix shape: {sim_matrix.shape}")
    print(f"Similarity range: [{sim_matrix.min():.3f}, {sim_matrix.max():.3f}]")

    # Step 4: Retrieve top-5
    top_5 = retrieve_top_k(sim_matrix, k=5)

    # Step 5: Display
    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)
    display_results(QUERIES, DOCUMENTS, sim_matrix, top_5)

    # Step 6: Evaluate
    # These are "ground truth" relevant docs (which docs SHOULD match each query)
    relevant = [
        {7, 8, 9},      # Query 0: transformer-related docs
        {10, 11, 13},   # Query 1: vector search/RAG docs
        {3, 14, 19},    # Query 2: image classification docs
    ]
    avg_precision = evaluate(top_5, relevant, k=5)
    print(f"\nAverage Precision@5: {avg_precision:.2f}")
    print("(Note: with random embeddings, precision will be low — that's expected!)")
    print("(With real embeddings from a model like sentence-transformers, precision would be ~0.8+)")


if __name__ == "__main__":
    main()
