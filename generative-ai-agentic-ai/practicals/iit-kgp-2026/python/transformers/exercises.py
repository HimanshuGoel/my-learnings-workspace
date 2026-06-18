"""
HuggingFace Transformers Exercises — 13 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. AI-relevant exercises are marked with [AI].

SETUP: pip install transformers torch sentence-transformers datasets
(All exercises use small models that run on CPU without GPU)

Run: python exercises.py
"""

# Note: Some exercises require downloading models (~100-500MB on first run)
# After first download, they're cached locally.

# =============================================================================
# EASY (1-5)
# =============================================================================

# Exercise 1: pipeline() — Sentiment Analysis [AI]
# Use pipeline() to classify sentiment of 5 product reviews.
# Print each review with its label and confidence score.
# Expected output:
#   "Great product!" → POSITIVE (0.99)
#   "Terrible quality" → NEGATIVE (0.98)

def exercise_1():
    from transformers import pipeline
    reviews = [
        "This is the best purchase I've ever made!",
        "Completely waste of money, broke after one day",
        "Decent quality for the price",
        "Absolutely horrible customer service",
        "Would definitely recommend to friends",
    ]
    # Your code here: create pipeline, classify each, print results
    pass


# Exercise 2: pipeline() — Zero-Shot Classification [AI]
# Classify support tickets into categories WITHOUT any training data.
# Categories: ["billing", "technical", "account", "shipping"]
# zero-shot = the model classifies into categories it was never explicitly trained on
# Expected: each ticket matched to most relevant category

def exercise_2():
    from transformers import pipeline
    tickets = [
        "I can't log into my account, password reset isn't working",
        "I was charged twice for my last order",
        "The app keeps crashing on my phone",
        "My package hasn't arrived after 2 weeks",
        "I want to upgrade my subscription plan",
    ]
    categories = ["billing", "technical", "account", "shipping"]
    # Your code here: zero-shot classification
    pass


# Exercise 3: Tokenizer Basics [AI]
# Explore how a tokenizer converts text to numbers:
# a) Tokenize "Artificial Intelligence is transforming the world"
# b) Print: tokens (subwords), token IDs, attention mask
# c) Decode back to original text
# d) Print vocabulary size
# tokenizer = converts text to numbers (token IDs) that the model can process
# Expected: show the full tokenization → ID → decode round-trip

def exercise_3():
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    text = "Artificial Intelligence is transforming the world"
    # Your code here
    pass


# Exercise 4: Batch Tokenization [AI]
# Tokenize a batch of sentences with different lengths:
# a) Tokenize with padding=True, truncation=True, max_length=32
# b) Print shapes of input_ids and attention_mask
# c) Show how padding fills shorter sequences with 0s
# d) Show how attention_mask marks real tokens (1) vs padding (0)
# Expected: understand padding and attention mask behavior

def exercise_4():
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    texts = [
        "Hello",
        "This is a medium length sentence",
        "This sentence is quite a bit longer and contains more words for testing purposes"
    ]
    # Your code here: batch tokenize, print shapes, show padding
    pass


# Exercise 5: pipeline() — Text Generation [AI]
# Generate text continuations using GPT-2:
# a) Generate 3 different continuations for "The future of artificial intelligence"
# b) Use temperature=0.7, max_new_tokens=30
# c) Print all 3 variations
# temperature = controls randomness (low=deterministic, high=creative)
# Expected: 3 different but coherent continuations

def exercise_5():
    from transformers import pipeline
    # Your code here: text-generation pipeline with gpt2
    pass


# =============================================================================
# MEDIUM (6-10)
# =============================================================================

# Exercise 6: Get Embeddings from a Model [AI]
# Load a model and extract embeddings (vector representations):
# a) Load "sentence-transformers/all-MiniLM-L6-v2"
# b) Get embeddings for 3 sentences
# c) Print embedding shape (should be 384-dimensional)
# d) Compute cosine similarity between all pairs
# e) Verify: similar sentences have higher similarity
# embedding = dense vector capturing semantic meaning of text
# Expected: "cat" sentences more similar to each other than to "programming"

def exercise_6():
    from sentence_transformers import SentenceTransformer
    import numpy as np
    sentences = [
        "The cat sat on the mat",
        "A kitten was resting on the rug",
        "Python programming is fun",
    ]
    # Your code here: encode, compute pairwise cosine similarity
    pass


# Exercise 7: Semantic Search [AI]
# Build a simple semantic search system:
# a) Encode a corpus of 10 documents
# b) Encode a query
# c) Find top-3 most similar documents using cosine similarity
# d) Print results with scores
# This is the core of RAG retrieval (Module 2).
# Expected: relevant documents ranked at top

def exercise_7():
    from sentence_transformers import SentenceTransformer
    import numpy as np

    corpus = [
        "Machine learning algorithms learn patterns from data",
        "Python is a popular programming language",
        "Neural networks are inspired by biological brains",
        "The weather forecast predicts rain tomorrow",
        "Deep learning uses multiple layers of neurons",
        "Cats are independent and curious animals",
        "Transfer learning reuses knowledge from pre-trained models",
        "Cooking pasta requires boiling water first",
        "GPT models generate human-like text",
        "Regular exercise improves mental health",
    ]
    query = "How do AI models learn from examples?"
    # Your code here: encode all, compute similarities, rank
    pass


# Exercise 8: Classification with AutoModel [AI]
# Use AutoModelForSequenceClassification for inference:
# a) Load a pre-trained sentiment model (distilbert-base-uncased-finetuned-sst-2-english)
# b) Tokenize input texts manually (not using pipeline)
# c) Run forward pass
# d) Convert logits to probabilities (softmax)
# e) Get predicted labels
# This shows what pipeline() does under the hood.
# Expected: same results as pipeline but with full control

def exercise_8():
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch

    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    texts = ["I absolutely love this!", "This is the worst.", "It's okay I guess."]
    # Your code here: load tokenizer+model, tokenize, forward, softmax, argmax
    pass


# Exercise 9: Explore Model Architecture [AI]
# Load a model and inspect its structure:
# a) Load "distilbert-base-uncased"
# b) Print model architecture (layers, dimensions)
# c) Count total parameters and trainable parameters
# d) Print the names of all layers
# This helps you understand what "768-dimensional hidden states" means concretely.
# Expected: see the actual nn.Module structure of a Transformer

def exercise_9():
    from transformers import AutoModel
    model = AutoModel.from_pretrained("distilbert-base-uncased")
    # Your code here: print model, count params, list layer names
    pass


# Exercise 10: Summarization [AI]
# Summarize a long text using a pre-trained model:
# a) Use pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
# b) Summarize the text below
# c) Try different max_length and min_length
# d) Print original length vs summary length
# Expected: coherent summary much shorter than original

def exercise_10():
    from transformers import pipeline
    long_text = """
    Artificial intelligence has transformed numerous industries in recent years.
    From healthcare to finance, AI systems are now capable of performing tasks
    that were once thought to be exclusively human domains. Machine learning
    algorithms can analyze vast amounts of data to identify patterns and make
    predictions. Natural language processing enables computers to understand
    and generate human language. Computer vision allows machines to interpret
    visual information from the world around them. Despite these advances,
    there remain significant challenges in AI safety, bias, and interpretability.
    Researchers continue to work on making AI systems more reliable, fair, and
    transparent. The future of AI will likely involve closer collaboration between
    humans and machines, with AI augmenting human capabilities rather than
    replacing them entirely.
    """
    # Your code here
    pass


# =============================================================================
# HARD (11-13)
# =============================================================================

# Exercise 11: Build a RAG-Style Retrieval System [AI]
# Combine embeddings + similarity search to answer questions:
# a) Create a knowledge base (10 facts as strings)
# b) Encode all facts into embeddings
# c) Given a question, find the 2 most relevant facts
# d) Format a prompt: "Based on: {facts}\n\nQuestion: {q}\nAnswer:"
# e) Use this prompt with a text-generation model
# This is a simplified RAG pipeline (Module 2).
# Expected: answer grounded in the retrieved facts

def exercise_11():
    from sentence_transformers import SentenceTransformer
    from transformers import pipeline
    import numpy as np

    knowledge_base = [
        "Python was created by Guido van Rossum and released in 1991.",
        "PyTorch was developed by Meta's AI Research lab.",
        "The Transformer architecture was introduced in 2017 in the paper 'Attention Is All You Need'.",
        "BERT stands for Bidirectional Encoder Representations from Transformers.",
        "GPT stands for Generative Pre-trained Transformer.",
        "Fine-tuning adapts a pre-trained model to a specific task with task-specific data.",
        "LoRA reduces fine-tuning cost by training low-rank adapter matrices.",
        "RAG combines retrieval of relevant documents with text generation.",
        "Embeddings are dense vector representations of text in high-dimensional space.",
        "Attention mechanism allows models to focus on relevant parts of the input.",
    ]
    question = "What is LoRA and what does it do?"
    # Your code here: encode KB, retrieve top-2, build prompt, generate answer
    pass


# Exercise 12: Compare Embedding Models [AI]
# Compare two embedding models on the same task:
# a) Use "all-MiniLM-L6-v2" (384-dim, fast)
# b) Use "all-mpnet-base-v2" (768-dim, more accurate)
# c) Encode same queries and documents with both
# d) Compare retrieval rankings — do they agree?
# e) Compare speed (time both)
# This teaches you trade-offs in model selection for RAG.
# Expected: both give similar rankings, MiniLM is faster

def exercise_12():
    from sentence_transformers import SentenceTransformer
    import numpy as np
    import time

    queries = ["How does attention work?", "What is transfer learning?"]
    documents = [
        "Attention allows models to focus on relevant input tokens",
        "Transfer learning reuses pre-trained model knowledge",
        "Cooking requires fresh ingredients",
        "Self-attention computes relationships between all positions",
        "Fine-tuning adapts existing models to new tasks",
    ]
    # Your code here: encode with both models, compare rankings and speed
    pass


# Exercise 13: Prepare Fine-Tuning Dataset [AI]
# Prepare a dataset in the format needed for Trainer:
# a) Create a small dataset (20 examples) with text and labels
# b) Tokenize using a tokenizer
# c) Create a HuggingFace Dataset object
# d) Verify it has the right columns (input_ids, attention_mask, labels)
# e) Split into train (16) and test (4)
# This is the data prep step before trainer.train() (Module 3).
# Expected: dataset ready for Trainer

def exercise_13():
    from transformers import AutoTokenizer
    from datasets import Dataset

    # Simulated classification data
    texts = [
        "Great product, highly recommend!", "Terrible quality, waste of money",
        "Love it, works perfectly", "Broke after one day, disappointed",
        "Best purchase ever", "Completely useless, returning it",
        "Exceeded my expectations", "Worst experience, avoid",
        "Amazing quality and fast shipping", "Defective item, poor packaging",
        "Very satisfied with this", "Regret buying this",
        "Outstanding performance", "Failed immediately",
        "Perfect for my needs", "Not as described, misleading",
        "Incredible value", "Overpriced garbage",
        "Would buy again", "Never ordering from here again",
    ]
    labels = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
    # Your code here: create Dataset, tokenize, split
    pass


# =============================================================================
# Run all exercises
# =============================================================================

if __name__ == "__main__":
    exercises = [exercise_1, exercise_2, exercise_3, exercise_4, exercise_5,
                 exercise_6, exercise_7, exercise_8, exercise_9, exercise_10,
                 exercise_11, exercise_12, exercise_13]

    for i, ex in enumerate(exercises, 1):
        print(f"\n{'='*60}")
        print(f"Exercise {i}")
        print('='*60)
        try:
            ex()
        except Exception as e:
            print(f"  [Skipped — {type(e).__name__}: {e}]")
            print("  (May need: pip install transformers sentence-transformers datasets)")
