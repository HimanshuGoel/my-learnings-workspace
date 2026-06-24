# Decoding Strategies

## What Is This?

Decoding is how a language model selects which token to output next from its predicted probability distribution — controlling the trade-off between creativity (randomness) and precision (determinism).

## Why Does It Exist?

**The Problem:** After a forward pass, the model outputs a probability distribution over all 50,000+ tokens in its vocabulary. "The cat sat on the ___" → {mat: 0.25, floor: 0.15, table: 0.10, ...}. How do you choose ONE token?

**The Options:**
- Always pick the highest probability (greedy) → boring, repetitive, safe
- Sample randomly from the distribution → creative but potentially incoherent
- Something in between → this is what temperature and top-p control

## Mental Model

Think of decoding as a **volume knob for creativity**:
- Turn it down (temperature=0) → deterministic, focused, repetitive (like a carefully reviewed legal document)
- Turn it up (temperature=1+) → creative, diverse, potentially wild (like brainstorming)

Or: like **randomness in game procedural generation**. A seed + randomness parameters control whether you get the "safe expected" world or a "surprising creative" one.

## How It Works

### Step 1: Model Outputs Logits

```
Input: "The cat sat on the"
Model output (logits): [2.5, 1.8, 1.2, 0.5, 0.1, ...] (50,000 values)
After softmax: [0.25, 0.15, 0.10, 0.05, 0.02, ...] (probabilities)
```

### Step 2: Apply Decoding Strategy

| Strategy | How | Effect |
|----------|-----|--------|
| Greedy | Always pick highest probability token | Deterministic, often repetitive |
| Temperature | Divide logits by T before softmax | T<1: sharper (more deterministic). T>1: flatter (more random) |
| Top-K | Only consider top K tokens, zero out rest | Limits choices to K most likely |
| Top-P (Nucleus) | Keep tokens until cumulative probability reaches P | Adaptive — considers more tokens when distribution is flat |
| Beam Search | Track N best sequences simultaneously | Better for translation/summarization, slower |

### Temperature Explained

```
Logits: [2.5, 1.8, 1.2, 0.5]

Temperature = 0.3 (divide by 0.3):
  → [8.3, 6.0, 4.0, 1.7] → softmax → [0.89, 0.08, 0.02, 0.00]
  → Almost certainly picks token 1 (very focused)

Temperature = 1.0 (no change):
  → [2.5, 1.8, 1.2, 0.5] → softmax → [0.44, 0.22, 0.12, 0.06]
  → Mostly token 1, but others possible (balanced)

Temperature = 2.0 (divide by 2):
  → [1.25, 0.9, 0.6, 0.25] → softmax → [0.32, 0.23, 0.17, 0.12]
  → Much more random (creative but risky)
```

### Top-P (Nucleus Sampling)

"Keep adding tokens (from most to least probable) until their combined probability reaches P."

```
Probabilities: [0.40, 0.25, 0.15, 0.08, 0.05, 0.03, 0.02, ...]

Top-P = 0.9:
  0.40 + 0.25 + 0.15 + 0.08 = 0.88 (not enough)
  0.40 + 0.25 + 0.15 + 0.08 + 0.05 = 0.93 ≥ 0.9 → keep top 5 tokens
  Sample from these 5 (renormalized)
```

### Practical Settings

| Use Case | Temperature | Top-P | Why |
|----------|------------|-------|-----|
| Code generation | 0.0-0.2 | 1.0 | Precision matters, creativity dangerous |
| Factual QA | 0.0-0.3 | 0.9 | Want accurate, consistent answers |
| Creative writing | 0.7-1.0 | 0.9 | Want diversity and surprise |
| Brainstorming | 1.0-1.5 | 0.95 | Maximum creativity |
| Classification | 0.0 | 1.0 | Deterministic — same input = same output |

## Where You'll Use This

| Module | How Decoding Applies |
|--------|---------------------|
| Module 1 | Understanding model output behavior and controlling it |
| Module 2 | RAG answers should be factual → low temperature |
| Module 4 | Agent reasoning → low temperature. Agent creativity → higher. |
| Module 5 | Production config: choosing the right params per endpoint |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "Temperature=0 means no randomness" | Technically it makes the distribution infinitely peaked → greedy. Same effect. |
| "Higher temperature = smarter" | Higher temperature = more random. Can be better OR worse depending on task. |
| "Top-P and Top-K are the same" | Top-K = fixed count. Top-P = adaptive (includes more tokens when uncertain). |
| "Just use default settings" | Defaults (T=1, no top-p) are rarely optimal. Always tune for your task. |
| "Beam search is always better" | Beam search is slower and can be bland. Sampling often produces more natural text. |

## Connection to Other Topics

- **Builds on:** Pre-training (model produces logits), Probability (softmax, sampling)
- **Relates to:** Prompting (prompt determines WHAT logits look like, decoding determines HOW to select from them)
- **Practical:** Every API call (OpenAI, Anthropic) lets you set temperature + top_p

## Ready to Move On?

- ☐ I understand what temperature controls (creativity vs determinism)
- ☐ I can explain the difference between greedy, top-k, and top-p decoding
- ☐ I know when to use low temperature (factual/code) vs high (creative)
- ☐ I understand that decoding doesn't change the model — it changes how we sample from its output

Next → **Fine-tuning** (adapting the model to your specific task)
