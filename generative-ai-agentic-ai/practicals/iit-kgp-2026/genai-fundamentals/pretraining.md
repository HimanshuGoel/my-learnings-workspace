# Pre-training

## What Is This?

Pre-training is the process of training a Transformer on massive text data (billions of pages) using a self-supervised objective (usually: predict the next token) — producing a general-purpose language model before any task-specific customization.

## Why Does It Exist?

**The Problem:** Training a model from scratch for each task (sentiment analysis, translation, QA) requires enormous labeled datasets per task. Most tasks don't have enough labeled data.

**The Solution:** Pre-train ONCE on unlabeled internet text (which is essentially infinite), then adapt to specific tasks cheaply. The model learns general language understanding during pre-training, and task-specific skills during fine-tuning.

This is the **transfer learning** paradigm: expensive general training (done once by a lab) → cheap task adaptation (done by you).

## Mental Model

Think of pre-training as **a university education**. A general degree (pre-training) gives broad knowledge. Then you specialize for a job (fine-tuning). You don't re-learn reading for every new project — you already know how language works.

Or: like **pre-compiling a shared library**. The expensive computation is done once. Every application that uses it gets the benefit without recompiling from scratch.

## How It Works

### Training Objectives

| Objective | Used By | How It Works |
|-----------|---------|-------------|
| Causal LM (next-token prediction) | GPT, LLaMA, Claude | "The cat sat on the ___" → predict "mat" |
| Masked LM (fill in blanks) | BERT | "The [MASK] sat on the mat" → predict "cat" |
| Seq2Seq (denoise) | T5 | Corrupt text → reconstruct original |

**Causal LM is dominant** — all modern generative models (GPT-4, Claude, LLaMA) use it.

### The Training Process

1. **Collect data** — trillions of tokens from: books, Wikipedia, web pages, code, forums, papers
2. **Tokenize** — convert all text to token IDs using the model's tokenizer
3. **Batch and feed** — process in batches of sequences (each ~2048-8192 tokens)
4. **Forward pass** — model predicts next token at each position
5. **Compute loss** — cross-entropy between predicted probability and actual next token
6. **Backprop** — compute gradients
7. **Update weights** — adjust billions of parameters slightly
8. **Repeat** — for months on thousands of GPUs

### What the Model Learns

By predicting the next word trillions of times, the model implicitly learns:
- Grammar and syntax (what's grammatically valid)
- Facts and knowledge (what's factually common in training data)
- Reasoning patterns (how conclusions follow from premises)
- Code patterns (how functions, loops, and APIs work)
- Style and format (how emails differ from code comments)
- Multi-language capability (from seeing multiple languages in data)

### Scale of Pre-training

| Model | Parameters | Training Tokens | GPUs | Time | Estimated Cost |
|-------|-----------|-----------------|------|------|---------------|
| GPT-2 | 1.5B | ~40B | 256 | weeks | ~$50K |
| LLaMA-2 7B | 7B | 2T | 2048 A100s | weeks | ~$2M |
| GPT-4 | ~1.8T | ~13T | tens of thousands | months | ~$100M+ |

**Key insight:** You don't pre-train. Labs do (OpenAI, Meta, Google). You use or fine-tune the result.

## Where You'll Use This

| Module | How Pre-training Applies |
|--------|--------------------------|
| Module 1 | Understanding what the model "knows" from training (and its limits) |
| Module 3 | Fine-tuning STARTS from a pre-trained checkpoint — you're adding, not starting over |
| Module 2 | RAG exists because pre-training has a knowledge cutoff — model doesn't know your docs |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "Pre-training = fine-tuning" | Pre-training = general learning (months, $millions). Fine-tuning = task adaptation (hours, $10s). |
| "The model memorizes text" | It learns patterns/distributions, not exact copies (though some memorization occurs) |
| "More data = always better" | Data QUALITY matters enormously. Junk data degrades performance. |
| "Pre-trained = ready to use" | Usually needs instruction tuning (RLHF/DPO) to follow instructions well. Raw pre-trained models just complete text. |
| "I should pre-train my own model" | Almost never. Use existing models + fine-tune. Pre-training from scratch is for labs with $10M+ budgets. |

## Connection to Other Topics

- **Builds on:** Transformer Architecture (what gets trained), Tokenization (how data is prepared)
- **Enables:** Prompting (using the pre-trained model), Fine-tuning (adapting it to your task)
- **Key insight:** Pre-training + instruction tuning + RLHF = the full recipe for a useful LLM (like ChatGPT)

## Ready to Move On?

- ☐ I understand that pre-training = predicting next tokens on internet-scale data
- ☐ I know the difference between pre-training (general, expensive) and fine-tuning (specific, cheap)
- ☐ I understand that raw pre-trained models just complete text — they need instruction tuning to be useful
- ☐ I know why I shouldn't pre-train from scratch (cost, data, compute) — use existing models

Next → **Prompting** (how to instruct the pre-trained model to do tasks)
