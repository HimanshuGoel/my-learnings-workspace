# Attention Mechanism

## What Is This?

Attention is a mechanism that allows each token in a sequence to look at every other token and decide how much to "pay attention" to it — computing relevance scores between all token pairs to build context-aware representations.

## Why Does It Exist?

**The Problem:** Before attention, models processed sequences one token at a time (RNNs/LSTMs). This meant:
- Long-range dependencies were lost ("The cat that sat on the mat near the window was ___" — by the time the model reaches "was", it's forgotten "cat")
- Processing was sequential (slow — can't parallelize)
- Information bottleneck (entire sentence squeezed into one fixed-size vector)

**The Solution:** Let every token directly look at every other token in the sequence simultaneously. "was" can directly look at "cat" regardless of distance. All pairs computed in parallel (GPU-friendly).

## Mental Model

Think of attention as **a smart search engine running inside the model**. For every token being processed, the model asks: "Which other tokens in this sentence are relevant to me right now?" and gets back a weighted combination of all tokens, ranked by relevance.

Or: like **event listeners in JavaScript**. Each token "listens" to all other tokens, but only "responds" strongly to the relevant ones. The attention weights are like filter functions determining which events matter.

Or: in database terms, attention is like a **soft JOIN** — instead of matching exact keys, it computes similarity between every pair and returns a weighted average.

## How It Works

### The Core Idea: Query, Key, Value (Q, K, V)

For each token, create three vectors:
- **Query (Q):** "What am I looking for?"
- **Key (K):** "What do I contain/represent?"
- **Value (V):** "What information do I provide if selected?"

Then: attention = softmax(Q × K^T / √d) × V

### Step-by-Step

1. **Each token generates Q, K, V** by multiplying its embedding with learned weight matrices
2. **Compute attention scores:** Q of token A dot-product with K of every other token → how relevant is each token to A?
3. **Scale and softmax:** divide by √d (prevents explosion), apply softmax (get probabilities that sum to 1)
4. **Weighted sum:** multiply scores by V vectors → output = weighted combination of all tokens' values

### Example: "The cat sat on the mat"

When processing "sat":
- Q("sat") asks: "what's the subject doing the sitting?"
- K("cat") responds: "I'm an entity (animal)" → high score
- K("mat") responds: "I'm a location" → medium score
- K("the") responds: "I'm just an article" → low score

Result: "sat" attends mostly to "cat" and somewhat to "mat."

### Multi-Head Attention

Instead of one attention computation, run multiple "heads" in parallel (e.g., 12 heads):
- Head 1 might learn to focus on syntactic relationships
- Head 2 might focus on semantic similarity
- Head 3 might focus on positional proximity
- Each head has its own Q, K, V weight matrices

Results are concatenated and projected back to the original dimension.

## The Math (Intuition, Not Derivation)

```
Attention(Q, K, V) = softmax(Q × K^T / √d_k) × V

Where:
- Q × K^T = dot product between all query-key pairs (similarity matrix)
- √d_k = scaling factor (keeps numbers stable)
- softmax = converts scores to probabilities (0-1, sum to 1)
- × V = weighted combination of values
```

**Matrix dimensions:**
- Q, K, V: (seq_len, d_model) — one row per token
- Q × K^T: (seq_len, seq_len) — attention score for every pair
- Output: (seq_len, d_model) — updated representation per token

## Where You'll Use This

| Module | How Attention Applies |
|--------|----------------------|
| Module 1 | Understanding how Transformers process text (core mechanism) |
| Module 2 | Attention visualizations help debug retrieval quality |
| Module 3 | Fine-tuning often targets attention layers (LoRA on Q, V matrices) |
| Module 4 | Agents use attention over tool descriptions to pick the right tool |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "Attention = the model understands" | It's a mathematical operation (weighted average). No "understanding" is guaranteed. |
| "Each head has a specific meaning" | Heads learn different patterns but aren't designed for specific roles. |
| "More attention heads = better" | Diminishing returns. 12-32 heads is standard. More adds compute without proportional gain. |
| "Attention weights show what the model 'thinks'" | Weights are intermediate computations. Interpreting them directly is often misleading. |
| "Self-attention is O(n)" | It's O(n²) — every token attends to every other. This is why long contexts are expensive. |

## Connection to Other Topics

- **Builds on:** Embeddings (attention operates on embedded vectors), Linear Algebra (dot products, matrix multiplication)
- **Enables:** Transformer Architecture (attention is the core layer), Pre-training (training objective shapes what attention learns)
- **Math connection:** Dot product = similarity score, Softmax = probability from calculus notes, Matrix multiplication from matrices.md

## Ready to Move On?

- ☐ I can explain Q, K, V and what each represents (what am I looking for, what do I have, what do I give)
- ☐ I understand that attention computes pairwise relevance between all tokens
- ☐ I know why attention replaced RNNs (parallel, no distance limitation, no bottleneck)
- ☐ I can explain multi-head attention (multiple perspectives computed simultaneously)

Next → **Transformer Architecture** (how attention + other layers form the complete model)
