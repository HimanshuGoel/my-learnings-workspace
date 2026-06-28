"""
LlamaIndex Exercises — 10 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. All exercises are AI-relevant.

SETUP: pip install llama-index llama-index-llms-openai llama-index-embeddings-openai
       export OPENAI_API_KEY=your-key
       (Or use HuggingFace embeddings for free local exercises)

Run: python exercises.py
"""

# =============================================================================
# EASY (1-4)
# =============================================================================

# Exercise 1: Document Creation & Node Parsing
# a) Create 5 Document objects manually with text and metadata
# b) Use SentenceSplitter to parse them into nodes (chunk_size=100)
# c) Print: number of documents vs number of nodes
# d) Inspect one node: text, metadata, relationships
# Document = raw input, Node = processed chunk (what gets embedded)
# Expected: more nodes than documents due to splitting

def exercise_1():
    from llama_index.core import Document
    from llama_index.core.node_parser import SentenceSplitter

    documents = [
        Document(text="Machine learning is a subset of AI that learns from data. "
                      "It uses algorithms to find patterns without explicit programming. "
                      "Common types include supervised, unsupervised, and reinforcement learning.",
                 metadata={"source": "ml_intro.txt", "topic": "ml"}),
        Document(text="Deep learning uses neural networks with multiple layers. "
                      "Each layer extracts increasingly abstract features from the input. "
                      "It excels at image recognition, NLP, and speech processing.",
                 metadata={"source": "dl_intro.txt", "topic": "dl"}),
        Document(text="Natural language processing enables computers to understand human language. "
                      "Modern NLP uses transformer architectures like BERT and GPT. "
                      "Applications include translation, summarization, and question answering.",
                 metadata={"source": "nlp_intro.txt", "topic": "nlp"}),
        Document(text="Retrieval Augmented Generation combines search with text generation. "
                      "First retrieve relevant documents, then generate answers using that context. "
                      "This reduces hallucination and grounds responses in factual data.",
                 metadata={"source": "rag_intro.txt", "topic": "rag"}),
        Document(text="Vector databases store numerical representations of text called embeddings. "
                      "They enable fast similarity search across millions of documents. "
                      "Popular options include ChromaDB, FAISS, Pinecone, and Weaviate.",
                 metadata={"source": "vectordb.txt", "topic": "infra"}),
    ]
    # Your code here: parse into nodes, print stats
    pass


# Exercise 2: Create VectorStoreIndex (Minimal RAG)
# Build a complete RAG system in 5 lines:
# a) Create documents (use the ones from Exercise 1 or load from strings)
# b) Create a VectorStoreIndex from documents
# c) Create a query engine
# d) Ask a question
# e) Print the response and source nodes
# This is the "hello world" of LlamaIndex.
# Expected: relevant answer grounded in your documents

def exercise_2():
    from llama_index.core import VectorStoreIndex, Document, Settings
    # Set up (use mock or real LLM)
    # If no OpenAI key, you can use:
    # from llama_index.llms.huggingface import HuggingFaceLLM
    # Settings.llm = HuggingFaceLLM(model_name="gpt2")
    # Your code here
    pass


# Exercise 3: Explore Query Response Object
# After querying, explore what the response object contains:
# a) response.response — the answer text
# b) response.source_nodes — list of retrieved nodes
# c) For each source node: node.text, node.metadata, node.score
# d) Print a formatted table of sources with scores
# Understanding the response object is key for debugging RAG quality.
# Expected: clear view of what was retrieved and how confident

def exercise_3():
    # Your code here (build on exercise 2)
    pass


# Exercise 4: Configure Chunk Size and Top-K
# Test how different settings affect retrieval:
# a) Create index with chunk_size=100 (small chunks)
# b) Create index with chunk_size=500 (large chunks)
# c) Query both with the same question
# d) Compare: which retrieves more precisely?
# e) Try similarity_top_k=1 vs top_k=5
# Expected: understand trade-offs of chunk size

def exercise_4():
    from llama_index.core import VectorStoreIndex, Document, Settings
    from llama_index.core.node_parser import SentenceSplitter
    # Your code here: compare different configurations
    pass


# =============================================================================
# MEDIUM (5-7)
# =============================================================================

# Exercise 5: Persistence — Save and Load Index
# a) Create an index from documents
# b) Persist to disk (./test_storage)
# c) Delete the index object from memory
# d) Load the index back from disk
# e) Query the loaded index — verify it still works
# f) Clean up the storage directory
# Expected: index survives save/load cycle

def exercise_5():
    from llama_index.core import (
        VectorStoreIndex, Document, StorageContext, load_index_from_storage
    )
    import shutil, os
    # Your code here
    pass


# Exercise 6: Chat Engine (Multi-Turn Conversation)
# Build a conversational RAG system:
# a) Create index from documents
# b) Create chat engine (mode="condense_question")
# c) Ask an initial question
# d) Ask a follow-up that uses pronouns ("it", "they", "that")
# e) Verify the follow-up correctly resolves the reference
# f) Reset and ask a new unrelated question
# chat engine = query engine + conversation memory
# Expected: follow-up questions work without re-stating context

def exercise_6():
    # Your code here
    pass


# Exercise 7: Response Modes Comparison
# Compare different response modes:
# a) Query with response_mode="compact" (stuff all in one prompt)
# b) Query with response_mode="refine" (iterate over chunks)
# c) Query with response_mode="tree_summarize" (hierarchical)
# d) Query with response_mode="no_text" (retrieval only, no generation)
# e) Compare answer quality and note differences
# Expected: understand when to use each mode

def exercise_7():
    # Your code here
    pass


# =============================================================================
# HARD (8-10)
# =============================================================================

# Exercise 8: Multi-Index Router Query Engine
# Build a system that routes queries to the correct index:
# a) Create index 1: "Technical docs" (ML/AI content)
# b) Create index 2: "HR policies" (company policies)
# c) Create a Router that picks the right index per query
# d) Test with technical question → should use index 1
# e) Test with HR question → should use index 2
# This is how real enterprise systems handle multiple doc collections.
# Expected: queries automatically routed to correct knowledge base

def exercise_8():
    from llama_index.core.query_engine import RouterQueryEngine
    from llama_index.core.tools import QueryEngineTool, ToolMetadata
    # Your code here
    pass


# Exercise 9: Structured Output with Pydantic
# Force the query engine to return structured data:
# a) Define a Pydantic model for the expected output
# b) Configure query engine with output_cls=YourModel
# c) Query and get a typed object instead of raw text
# d) Access fields programmatically (response.title, response.summary)
# This is critical for production apps that need machine-readable output.
# Expected: response is a Pydantic object with typed fields

def exercise_9():
    from pydantic import BaseModel, Field
    # Your code here
    pass


# Exercise 10: Complete RAG Pipeline with ChromaDB Backend
# Build production-grade RAG:
# a) Create ChromaDB persistent collection
# b) Use it as LlamaIndex vector store backend
# c) Ingest 10+ documents
# d) Create query engine with custom settings
# e) Query with metadata filtering
# f) Print sources and scores
# g) Persist and verify reload works
# This combines LlamaIndex + ChromaDB for a production-ready setup.
# Expected: persistent, filterable, production-quality RAG

def exercise_10():
    import chromadb
    # from llama_index.vector_stores.chroma import ChromaVectorStore
    # Your code here
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
