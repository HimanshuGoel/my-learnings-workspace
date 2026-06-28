# Embeddings

## What Is This?

Embeddings are dense numerical vectors that represent the meaning of tokens, words, sentences, or documents in a high-dimensional space — where similar meanings live close together and different meanings live far apart.

## Why Does It Exist?

**The Problem:** After tokenization, you have token IDs like [348, 14372]. But these are just arbitrary integers — "348" isn't inherently closer to "349" in meaning. The model needs a representation where semantic relationships are captured numerically.

**What doesn't work:**
- One-hot encoding: [0,0,0,...,1,...,0] with 50,000 dimensions. Extremely sparse. No relationship between any two words — "cat" and "kitten" are as far apart as "cat" and "telescope."
- Raw integer IDs: "348" and "349" being numerically close means nothing semantically.

**The Solution:** Learn a dense vector (e.g., 768 floats) for each token where:
- Similar words → similar vectors (close in space)
- Relationships are preserved ("king" - "man" + "woman" ≈ "queen")
- Distance/angle between vectors = semantic similarity

## Mental Model

Think of embeddings as **GPS coordinates for meaning**. Just as GPS coordinates put physical locations in a space where "nearby = close" (New Delhi and Agra are closer than New Delhi and New York), embeddings put meanings in a space where "nearby = similar meaning."

Or: like a **feature vector in Angular's state management**. Instead of storing a component's state as a string label, you store it as a structured object with multiple numeric properties. Embeddings do the same for words — each dimension captures some aspect of meaning.

## How It Works

### The Embedding Layer

```
Token ID: 7592 ("hello")
    ↓
Lookup Table (learned matrix, shape: vocab_size × embedding_dim)
    ↓
Vector: [0.23, -0.14, 0.87, 0.02, ..., -0.56]  (768 numbers)
```

The embedding matrix is just a giant lookup table. Each row = one token's learned vector. During training, these vectors get adjusted so that semantically related tokens end up with similar vectors.

### What Each Dimension Captures

No single dimension means "happy" or "noun." Instead, it's distributed:
- Some directions in the space capture formality
- Some capture tense (past/present)
- Some capture topic (science/sports)
- Some capture sentiment
- Most are uninterpretable (but useful for the model)

### Types of Embeddings

| Type | What It Embeds | Dimension | Use Case |
|------|---------------|-----------|----------|
| Token embedding | Single token | 768-4096 | First layer of every LLM |
| Word embedding (Word2Vec, GloVe) | Single word | 100-300 | Legacy, static (same vector regardless of context) |
| Contextual embedding (BERT, GPT) | Token in context | 768-4096 | "bank" gets different vector in "river bank" vs "bank account" |
| Sentence embedding | Entire sentence | 384-768 | Semantic search, RAG retrieval |
| Document embedding | Entire document | 384-768 | Document clustering, recommendation |

### Static vs Contextual

- **Static** (Word2Vec): "bank" always has the same vector regardless of sentence. Outdated.
- **Contextual** (BERT, GPT): "bank" gets a different vector depending on surrounding words. This is the modern standard — the same word has different embeddings in different contexts.

## Concrete Example

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode sentences → vectors
emb1 = model.encode("The cat sat on the mat")     # shape: (384,)
emb2 = model.encode("A kitten rested on the rug")  # shape: (384,)
emb3 = model.encode("Python programming is fun")   # shape: (384,)

# Cosine similarity (dot product of normalized vectors)
sim_12 = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
sim_13 = np.dot(emb1, emb3) / (np.linalg.norm(emb1) * np.linalg.norm(emb3))

print(sim_12)  # ~0.75 (high — both about cats on surfaces)
print(sim_13)  # ~0.15 (low — unrelated topics)
```

**This is the foundation of semantic search and RAG.**

## Where You'll Use This

| Module | How Embeddings Apply |
|--------|---------------------|
| Module 1 | Understanding how models represent meaning internally |
| Module 2 | RAG = embed documents + embed query + find similar. This IS Module 2. |
| Module 3 | Fine-tuning adjusts embeddings so they better represent your domain |
| Module 4 | Agent memory uses embeddings for context retrieval |
| Module 5 | Choosing embedding models (size vs quality trade-off) for production |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "Each dimension has a clear meaning" | Dimensions are distributed — meaning is spread across all 768 values |
| "Embeddings are fixed once trained" | Contextual embeddings (BERT/GPT) change with surrounding context |
| "Bigger embedding = always better" | 384-dim (MiniLM) is often good enough. 768 or 1536 adds cost with diminishing returns. |
| "Embeddings capture truth" | They capture statistical patterns from training data — including biases |
| "You need to train your own embeddings" | Pre-trained sentence-transformers work great for most use cases |

## Connection to Other Topics

- **Builds on:** Tokenization (token IDs are the input to the embedding layer)
- **Math foundation:** Vectors (embeddings ARE vectors), cosine similarity, dot products
- **Enables:** Attention (operates on embedded token vectors), RAG (similarity search over embeddings)
- **Code:** NumPy (array ops), sentence-transformers (encoding), ChromaDB (storing)

## Ready to Move On?

- ☐ I can explain why one-hot encoding doesn't work (sparse, no similarity)
- ☐ I understand that embeddings place meaning in geometric space (similar = close)
- ☐ I know the difference between static (Word2Vec) and contextual (BERT) embeddings
- ☐ I can describe how embeddings enable semantic search (embed query → find similar docs)

Next → **Attention** (how the model focuses on relevant parts of the input)
