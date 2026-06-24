# Transformer Architecture

## What Is This?

The Transformer is a neural network architecture that stacks attention layers, feed-forward networks, and normalization into a repeating block — forming the backbone of every modern LLM (GPT, BERT, LLaMA, Claude).

## Why Does It Exist?

**The Problem:** Attention alone is powerful but insufficient. You need:
- A way to add non-linearity (attention is just weighted averaging — linear)
- Stability during training (deep networks collapse without normalization)
- A standard structure that scales from 100M to 1T parameters

**The Solution:** A repeating block: [Attention → Add & Norm → Feed-Forward → Add & Norm]. Stack N of these blocks. The simplicity of this pattern is what made scaling possible.

## Mental Model

Think of the Transformer as a **layered middleware pipeline** (like Express.js middleware). Each layer:
1. Processes the input (attention = understand context)
2. Transforms it (feed-forward = compute new features)
3. Passes it to the next layer (residual connection = don't lose the original)

Or: like an **Angular component tree**. Each layer is a component that receives input, processes it, and outputs a transformed version. Stacking 32 layers = 32 levels of increasingly abstract understanding.

## How It Works

### The Transformer Block (One Layer)

```
Input embeddings (seq_len × d_model)
    │
    ├──→ Multi-Head Attention
    │         │
    │    ←────┘ (residual connection: add input back)
    │
    ├──→ Layer Normalization
    │
    ├──→ Feed-Forward Network (2 linear layers + ReLU)
    │         │
    │    ←────┘ (residual connection: add input back)
    │
    ├──→ Layer Normalization
    │
    ▼
Output (same shape: seq_len × d_model)
```

Stack this block N times (N=12 for small models, N=96 for GPT-4 scale).

### Components Explained

| Component | What It Does | Why It's Needed |
|-----------|-------------|-----------------|
| Multi-Head Attention | Each token gathers context from all others | Core relationship computation |
| Feed-Forward (FFN) | Two linear layers with activation in between | Adds non-linearity, stores "knowledge" |
| Layer Normalization | Normalizes activations to stable range | Prevents training instability |
| Residual Connection | Adds input directly to output (skip connection) | Prevents gradient vanishing in deep networks |
| Positional Encoding | Adds position information to embeddings | Attention is position-agnostic — needs order |

### Encoder vs Decoder

| Variant | Used By | Key Difference |
|---------|---------|---------------|
| Encoder-only | BERT | Sees all tokens (bidirectional). For classification, embeddings. |
| Decoder-only | GPT, LLaMA, Claude | Sees only previous tokens (causal mask). For text generation. |
| Encoder-Decoder | T5, BART | Encoder reads input fully, decoder generates output. For translation, summarization. |

**Most modern LLMs (GPT-4, Claude, LLaMA) are decoder-only.**

### Positional Encoding

Attention doesn't know word order — "cat sat mat" and "mat sat cat" would produce the same attention scores without position information.

Solution: Add position vectors to embeddings before the first layer.
- Original paper: sinusoidal functions (fixed math formula)
- Modern: Rotary Position Embeddings (RoPE) — learned, better for long contexts

## Where You'll Use This

| Module | How This Applies |
|--------|-----------------|
| Module 1 | Understanding model internals when things go wrong |
| Module 3 | Fine-tuning targets specific layers (LoRA adds adapters to attention layers) |
| Module 4 | Architectural decisions: which model variant for which task |
| Module 5 | Model size/layer count affects serving speed and memory requirements |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "The Transformer is one thing" | It's encoder, decoder, or both — GPT and BERT are very different architectures |
| "More layers = smarter" | Diminishing returns. More layers = more memory and slower inference |
| "FFN is unimportant (attention does everything)" | FFN stores most of the model's "knowledge" — it has most of the parameters |
| "Position doesn't matter" | Without positional encoding, "I love you" = "you love I" to the model |
| "All modern LLMs use the same architecture" | Subtle differences: LLaMA uses RMSNorm, GPT uses LayerNorm pre/post, etc. |

## Connection to Other Topics

- **Builds on:** Attention (the core layer), Embeddings (the input), Matrices (all operations are matrix multiplies)
- **Enables:** Pre-training (the architecture that gets trained), Fine-tuning (which layers to adapt)
- **Contains:** Attention + FFN + LayerNorm + Residual + Positional Encoding

## Ready to Move On?

- ☐ I can describe the Transformer block: attention → add & norm → FFN → add & norm
- ☐ I understand encoder-only (BERT) vs decoder-only (GPT) vs encoder-decoder (T5)
- ☐ I know what residual connections are and why they matter (prevent gradient vanishing)
- ☐ I understand why positional encoding is needed (attention is order-agnostic)

Next → **Pre-training** (how this architecture learns from internet-scale data)
