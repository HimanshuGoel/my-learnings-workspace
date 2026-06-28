"""
ChromaDB Exercises — 10 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. All exercises are AI-relevant.

SETUP: pip install chromadb sentence-transformers
(No API keys needed — all runs locally)

Run: python exercises.py
"""

import chromadb

# =============================================================================
# EASY (1-4)
# =============================================================================

# Exercise 1: Create Collection & Add Documents
# a) Create an in-memory ChromaDB client
# b) Create a collection called "test_collection"
# c) Add 5 documents with IDs, text, and metadata
# d) Print collection count
# e) Peek at the first 3 documents
# Expected: collection with 5 documents

def exercise_1():
    documents = [
        "Python is a programming language",
        "Machine learning uses algorithms to learn from data",
        "Neural networks are inspired by the human brain",
        "ChromaDB stores vector embeddings",
        "RAG combines retrieval with generation",
    ]
    metadatas = [
        {"topic": "programming", "level": "beginner"},
        {"topic": "ml", "level": "intermediate"},
        {"topic": "dl", "level": "advanced"},
        {"topic": "databases", "level": "intermediate"},
        {"topic": "ai", "level": "advanced"},
    ]
    # Your code here
    pass


# Exercise 2: Basic Query
# Using the collection from Exercise 1:
# a) Query with "How do computers learn?" (n_results=3)
# b) Print the matched documents with their distances
# c) Query with "database storage" (n_results=2)
# d) Compare results — verify semantic similarity works
# Expected: relevant docs returned even without exact keyword match

def exercise_2():
    # Your code here (recreate collection or continue from ex1)
    pass


# Exercise 3: Metadata Filtering
# a) Add 10 documents with metadata (topic, difficulty, year)
# b) Query with filter: only "ml" topic
# c) Query with filter: difficulty > 3
# d) Query with combined filter: topic="ml" AND year >= 2024
# Expected: filtered results based on metadata

def exercise_3():
    client = chromadb.Client()
    collection = client.create_collection("filtered_docs")
    
    documents = [
        "Linear regression for prediction",
        "Decision trees for classification", 
        "Convolutional neural networks for images",
        "Transformer attention mechanism",
        "Random forest ensemble method",
        "Gradient boosting for tabular data",
        "BERT for language understanding",
        "GPT for text generation",
        "K-means clustering algorithm",
        "Support vector machines",
    ]
    metadatas = [
        {"topic": "ml", "difficulty": 2, "year": 2020},
        {"topic": "ml", "difficulty": 3, "year": 2021},
        {"topic": "dl", "difficulty": 4, "year": 2022},
        {"topic": "dl", "difficulty": 5, "year": 2023},
        {"topic": "ml", "difficulty": 3, "year": 2022},
        {"topic": "ml", "difficulty": 3, "year": 2024},
        {"topic": "nlp", "difficulty": 4, "year": 2024},
        {"topic": "nlp", "difficulty": 5, "year": 2025},
        {"topic": "ml", "difficulty": 2, "year": 2020},
        {"topic": "ml", "difficulty": 3, "year": 2021},
    ]
    # Your code here: add docs, query with different filters
    pass


# Exercise 4: Update and Delete
# a) Create a collection with 5 documents
# b) Update document 3 (change text and metadata)
# c) Verify the update by getting doc 3
# d) Delete documents 1 and 2
# e) Verify count decreased
# Expected: collection reflects updates and deletions

def exercise_4():
    # Your code here
    pass


# =============================================================================
# MEDIUM (5-7)
# =============================================================================

# Exercise 5: RAG Ingestion Pipeline
# Build a document ingestion pipeline:
# a) Take a long text and split it into chunks (manually, ~100 chars each)
# b) Generate unique IDs using content hash
# c) Add all chunks to ChromaDB with metadata (source, chunk_index)
# d) Query and verify retrieval works across chunks
# This is the "store" step of Load→Split→Embed→Store→Retrieve→Generate
# Expected: relevant chunk retrieved from a larger document

def exercise_5():
    import hashlib

    long_text = """
    Machine learning is a subset of artificial intelligence that focuses on 
    building systems that learn from data. Unlike traditional programming where 
    you write explicit rules, ML algorithms discover patterns automatically.
    
    There are three main types: supervised learning uses labeled examples,
    unsupervised learning finds hidden patterns without labels, and 
    reinforcement learning learns through trial and error with rewards.
    
    Common supervised algorithms include linear regression for continuous 
    predictions, logistic regression for classification, decision trees for
    interpretable models, and neural networks for complex patterns.
    
    Deep learning is a subset of ML using neural networks with many layers.
    It excels at tasks like image recognition, natural language processing,
    and speech recognition. Training deep models requires large datasets
    and significant computational resources, often using GPUs.
    """
    # Your code here: split into chunks, hash for IDs, add to collection, query
    pass


# Exercise 6: Custom Embedding Function
# a) Create a collection with a specific embedding function (SentenceTransformer)
# b) Add documents
# c) Query and verify results
# d) Compare results using default vs explicit embedding function
# embedding function = the model that converts text to vectors
# Expected: understand how different models affect retrieval quality

def exercise_6():
    from chromadb.utils import embedding_functions
    # Your code here
    pass


# Exercise 7: Multi-Query Search with Scoring
# Build a search system that:
# a) Stores 15 FAQ entries in ChromaDB
# b) Takes multiple queries
# c) For each query, returns top-3 results with similarity scores
# d) Filters out results below a similarity threshold (distance > 1.0)
# e) Formats output as a ranked list
# This mimics production search behavior.
# Expected: ranked results with confidence filtering

def exercise_7():
    faqs = [
        "How do I reset my password?",
        "What payment methods do you accept?",
        "How long does shipping take?",
        "What is your return policy?",
        "How do I cancel my subscription?",
        "Do you offer student discounts?",
        "How do I contact support?",
        "Is my data secure?",
        "Can I use multiple devices?",
        "What happens if I exceed limits?",
        "How do I export my data?",
        "What are the system requirements?",
        "How do I upgrade my plan?",
        "Can I transfer my account?",
        "What languages do you support?",
    ]
    queries = [
        "change my password",
        "refund and returns",
        "student pricing",
        "what is quantum computing",  # should have no good matches
    ]
    # Your code here
    pass


# =============================================================================
# HARD (8-10)
# =============================================================================

# Exercise 8: Persistent Vector Store
# a) Create a PersistentClient that saves to "./test_chroma_db"
# b) Add 10 documents
# c) Close the client (del or let garbage collect)
# d) Re-open with a NEW PersistentClient at same path
# e) Verify all documents are still there
# f) Clean up (delete the directory)
# Expected: data survives client restart

def exercise_8():
    import shutil
    import os
    db_path = "./test_chroma_db_exercise"
    # Your code here
    # Remember to clean up: shutil.rmtree(db_path)
    pass


# Exercise 9: Hybrid Search (Semantic + Keyword)
# Combine ChromaDB semantic search with keyword filtering:
# a) Store documents with full text in documents field
# b) Query semantically (similarity)
# c) Additionally filter with where_document (must contain keyword)
# d) Compare results: semantic only vs semantic + keyword
# Hybrid = combining vector similarity with traditional filters
# Expected: more precise results with both filters applied

def exercise_9():
    documents = [
        "Python is great for machine learning and data science applications",
        "JavaScript is the language of the web and frontend development",
        "Python's NumPy library enables fast numerical computation",
        "React is a JavaScript framework for building user interfaces",
        "Python's scikit-learn makes machine learning accessible",
        "Node.js allows JavaScript to run on the server side",
        "TensorFlow and PyTorch are Python deep learning frameworks",
        "TypeScript adds type safety to JavaScript projects",
        "Python's pandas library excels at data manipulation",
        "Vue.js is an alternative JavaScript frontend framework",
    ]
    # Your code here: add all, query with and without where_document
    pass


# Exercise 10: Build Complete RAG Retriever (No LangChain)
# Build a RAG retrieval component from scratch using only ChromaDB:
# a) Ingest a knowledge base (20 chunks about AI topics)
# b) Implement a retrieve(query, k, threshold) function
# c) Function returns relevant chunks + metadata + scores
# d) Implement a format_context(results) that formats for LLM prompt
# e) Test with 3 different queries, print formatted context
# This is what LangChain's retriever does internally.
# Expected: clean retrieval function ready to plug into an LLM call

def exercise_10():
    knowledge_base = [
        "Transformers use self-attention to process sequences in parallel",
        "BERT is bidirectional and excels at understanding tasks",
        "GPT generates text left-to-right using causal attention",
        "Fine-tuning adapts a pre-trained model to a specific task",
        "LoRA reduces fine-tuning cost by training low-rank matrices",
        "RAG retrieves relevant documents before generating answers",
        "Vector databases store embeddings for fast similarity search",
        "Embeddings represent text as dense numerical vectors",
        "Cosine similarity measures directional alignment of vectors",
        "Tokenizers split text into subword units for model input",
        "Attention mechanism weighs the importance of different tokens",
        "Transfer learning reuses knowledge from pre-trained models",
        "Prompt engineering optimizes instructions for better outputs",
        "Few-shot learning provides examples in the prompt",
        "Zero-shot means the model handles tasks without examples",
        "Chain-of-thought prompting encourages step-by-step reasoning",
        "Agents use tools and reasoning to solve complex tasks",
        "Memory allows AI systems to maintain conversation context",
        "Hallucination occurs when models generate false information",
        "Grounding with retrieval reduces hallucination in responses",
    ]
    # Your code here: implement retrieve() and format_context()
    pass


# =============================================================================
# Run all exercises
# =============================================================================

if __name__ == "__main__":
    exercises = [exercise_1, exercise_2, exercise_3, exercise_4, exercise_5,
                 exercise_6, exercise_7, exercise_8, exercise_9, exercise_10]

    for i, ex in enumerate(exercises, 1):
        print(f"\n{'='*60}")
        print(f"Exercise {i}")
        print('='*60)
        try:
            ex()
        except Exception as e:
            print(f"  [Error: {type(e).__name__}: {e}]")
