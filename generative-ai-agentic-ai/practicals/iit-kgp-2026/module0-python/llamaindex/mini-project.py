"""
=============================================================================
MINI PROJECT: Multi-Document Research Assistant
=============================================================================

PROBLEM STATEMENT:
Build a research assistant that answers questions across multiple document
collections (e.g., technical papers, course notes, project docs) — routing
to the right source automatically and synthesizing cross-source answers.

WHAT YOU'LL BUILD:
- Multiple document indexes (one per topic/source)
- Automatic query routing (picks correct source)
- Cross-source synthesis (combines info from multiple sources)
- Chat mode (multi-turn with follow-ups)
- Source attribution (which documents answered)

WHY THIS MATTERS:
Real-world RAG isn't "one folder of docs." It's multiple knowledge bases:
product docs, API specs, HR policies, research papers. This project teaches
you to handle that complexity — directly applicable to Module 4 (multi-agent)
and Module 5 (capstone).

ESTIMATED TIME: 45-60 minutes

SETUP: pip install llama-index llama-index-llms-openai llama-index-embeddings-openai

RULES:
- Use LlamaIndex for indexing and querying
- Create at least 3 separate indexes
- Implement routing between them
- Follow the TODOs in order
=============================================================================
"""

from llama_index.core import Document


# =============================================================================
# SETUP: Simulated multi-source knowledge base
# =============================================================================

ML_DOCS = [
    Document(text="Supervised learning uses labeled data to train models. The model learns a mapping "
                  "from inputs to outputs. Common algorithms: linear regression, random forests, SVMs. "
                  "Evaluation uses train/test split and cross-validation.",
             metadata={"source": "ml_fundamentals.md", "topic": "supervised"}),
    Document(text="Neural networks consist of layers of interconnected neurons. Each neuron applies "
                  "weights, bias, and an activation function. Backpropagation updates weights using "
                  "gradient descent. Deep networks have many hidden layers.",
             metadata={"source": "ml_fundamentals.md", "topic": "neural_nets"}),
    Document(text="Overfitting occurs when a model memorizes training data but fails on new data. "
                  "Solutions: regularization (L1/L2), dropout, early stopping, more training data, "
                  "data augmentation, simpler model architecture.",
             metadata={"source": "ml_fundamentals.md", "topic": "overfitting"}),
    Document(text="Feature engineering creates new input features from raw data. Techniques: "
                  "normalization, one-hot encoding, polynomial features, interaction terms, "
                  "binning continuous variables, text vectorization (TF-IDF, embeddings).",
             metadata={"source": "ml_fundamentals.md", "topic": "features"}),
]

RAG_DOCS = [
    Document(text="RAG (Retrieval-Augmented Generation) combines retrieval with generation. "
                  "Steps: 1) chunk documents 2) embed chunks 3) store in vector DB "
                  "4) retrieve relevant chunks for query 5) generate answer with context.",
             metadata={"source": "rag_guide.md", "topic": "overview"}),
    Document(text="Chunking strategies affect RAG quality. Recursive text splitter respects "
                  "paragraph and sentence boundaries. Optimal chunk size: 256-512 tokens. "
                  "Overlap of 50-100 tokens preserves context at boundaries.",
             metadata={"source": "rag_guide.md", "topic": "chunking"}),
    Document(text="Embedding models convert text to dense vectors. Popular choices: "
                  "all-MiniLM-L6-v2 (fast, 384d), all-mpnet-base-v2 (accurate, 768d), "
                  "text-embedding-3-small (OpenAI, good balance). Match model at store and query time.",
             metadata={"source": "rag_guide.md", "topic": "embeddings"}),
    Document(text="Evaluation metrics for RAG: faithfulness (is answer supported by context?), "
                  "relevancy (are retrieved docs relevant?), answer correctness, "
                  "context precision/recall. Use RAGAS framework for automated evaluation.",
             metadata={"source": "rag_guide.md", "topic": "evaluation"}),
]

PYTHON_DOCS = [
    Document(text="NumPy provides fast array operations via vectorization. Core object: ndarray. "
                  "Key operations: reshape, broadcasting, dot product, slicing. "
                  "All ML libraries use NumPy arrays internally.",
             metadata={"source": "python_libs.md", "topic": "numpy"}),
    Document(text="Pandas handles tabular data: DataFrames and Series. Key operations: "
                  "read_csv, groupby, merge, fillna, get_dummies. 80% of data science "
                  "is data preparation — Pandas is where you spend most time.",
             metadata={"source": "python_libs.md", "topic": "pandas"}),
    Document(text="PyTorch builds neural networks with autograd. Core pattern: "
                  "define nn.Module, write training loop (forward, loss, backward, step). "
                  "Tensors = NumPy arrays with GPU + gradient tracking.",
             metadata={"source": "python_libs.md", "topic": "pytorch"}),
    Document(text="Scikit-learn provides consistent fit/predict/score API for ML. "
                  "Pipeline chains preprocessing + model. Cross-validation for robust eval. "
                  "GridSearchCV for hyperparameter tuning. Best for tabular data < 1M rows.",
             metadata={"source": "python_libs.md", "topic": "sklearn"}),
]


# =============================================================================
# TODO 1: Create Individual Indexes
# =============================================================================
# Create 3 separate VectorStoreIndexes:
#   - ml_index (from ML_DOCS)
#   - rag_index (from RAG_DOCS)
#   - python_index (from PYTHON_DOCS)
# Each with appropriate chunk settings.
# Return all three indexes.

def create_indexes():
    """Create separate indexes for each document collection."""
    from llama_index.core import VectorStoreIndex, Settings
    from llama_index.core.node_parser import SentenceSplitter
    # TODO: Configure settings (LLM, embeddings, chunk size)
    # TODO: Create 3 indexes
    # TODO: Return them
    pass


# =============================================================================
# TODO 2: Create Query Engine Tools
# =============================================================================
# Wrap each index as a QueryEngineTool with descriptive metadata.
# The description helps the router decide which index to query.
# Return the list of tools.

def create_tools(ml_index, rag_index, python_index):
    """Create query engine tools for routing."""
    from llama_index.core.tools import QueryEngineTool, ToolMetadata
    # TODO: Create query engines from each index
    # TODO: Wrap in QueryEngineTool with clear descriptions
    # TODO: Return list of tools
    pass


# =============================================================================
# TODO 3: Create Router Query Engine
# =============================================================================
# Build a router that automatically picks the right index based on the query.
# Use LLMSingleSelector (LLM decides which tool fits best).
# Return the router engine.

def create_router(tools):
    """Create a router that directs queries to the right index."""
    from llama_index.core.query_engine import RouterQueryEngine
    from llama_index.core.selectors import LLMSingleSelector
    # TODO: Create RouterQueryEngine
    # TODO: Return it
    pass


# =============================================================================
# TODO 4: Create Chat Engine
# =============================================================================
# Build a chat engine for multi-turn conversation over one index.
# Use "condense_question" mode for follow-up handling.
# Return the chat engine.

def create_chat(index):
    """Create a conversational engine with memory."""
    # TODO: Create chat engine from index
    # TODO: Return it
    pass


# =============================================================================
# TODO 5: Query with Source Attribution
# =============================================================================
# Query the router and format results with:
#   - The answer text
#   - Source documents used (file, topic)
#   - Relevance scores

def query_with_attribution(router_engine, question):
    """Query and return formatted result with sources."""
    # TODO: Query router
    # TODO: Extract source_nodes
    # TODO: Format output
    # TODO: Return structured dict
    pass


# =============================================================================
# TODO 6: Multi-Turn Conversation
# =============================================================================
# Demonstrate multi-turn capability:
# a) Ask initial question about a topic
# b) Ask follow-up using pronouns
# c) Ask another follow-up that builds on both
# d) Verify context is maintained

def demo_conversation(chat_engine):
    """Demonstrate multi-turn conversation."""
    conversation = [
        "What is overfitting in machine learning?",
        "What are the main solutions for it?",          # "it" = overfitting
        "Which of those works best for neural networks?", # context from prev answers
    ]
    # TODO: Chat through each question, print responses
    pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("MULTI-DOCUMENT RESEARCH ASSISTANT")
    print("=" * 60)

    # Step 1: Create indexes
    print("\n--- STEP 1: CREATE INDEXES ---")
    ml_index, rag_index, python_index = create_indexes()
    print("Created 3 indexes: ML, RAG, Python")

    # Step 2: Create tools
    print("\n--- STEP 2: CREATE TOOLS ---")
    tools = create_tools(ml_index, rag_index, python_index)
    print(f"Created {len(tools)} query tools")

    # Step 3: Create router
    print("\n--- STEP 3: CREATE ROUTER ---")
    router = create_router(tools)
    print("Router ready — auto-routes queries to correct source")

    # Step 4: Test routing
    print("\n--- STEP 4: TEST ROUTING ---")
    test_queries = [
        "How does backpropagation work?",           # → ML index
        "What chunk size should I use for RAG?",    # → RAG index
        "How do I use Pandas groupby?",             # → Python index
        "How to evaluate a RAG pipeline?",          # → RAG index
    ]
    for q in test_queries:
        print(f"\nQ: {q}")
        result = query_with_attribution(router, q)
        if result:
            print(f"A: {result.get('answer', 'N/A')[:150]}...")
            print(f"Source: {result.get('sources', 'unknown')}")

    # Step 5: Multi-turn conversation
    print("\n--- STEP 5: CONVERSATION ---")
    chat = create_chat(ml_index)
    demo_conversation(chat)

    print("\n" + "=" * 60)
    print("Done! Multi-document research assistant complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
