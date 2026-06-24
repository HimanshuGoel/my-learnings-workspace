# Fine-Tuning

## What Is This?

Fine-tuning adapts a pre-trained model to a specific task or domain by training it further on a smaller, task-specific dataset — adjusting its weights so it becomes an expert at your particular use case while retaining its general capabilities.

## Why Does It Exist?

**The Problem:** Pre-trained models are generalists. They can do many things okay, but:
- They don't know your company's products, policies, or jargon
- They don't follow your specific output format consistently
- They may not perform well enough on niche domains (medical, legal, finance)
- Prompting has limits — can't fit enough examples/context in every prompt

**The Solution:** Continue training the model on YOUR data (hundreds to thousands of examples) so it learns YOUR patterns. Much cheaper than pre-training from scratch.

## Mental Model

Think of fine-tuning as **on-the-job training for an experienced hire**. You hired a senior developer (pre-trained model) who knows Java/Python/everything broadly. But they need to learn YOUR codebase, YOUR conventions, YOUR domain. A few weeks of onboarding (fine-tuning) makes them productive without re-learning programming from scratch.

## How It Works

### Types of Fine-Tuning

| Method | What Changes | Cost | When to Use |
|--------|-------------|------|-------------|
| Full fine-tuning | ALL parameters | $$$ (needs full model in memory) | Maximum quality, unlimited budget |
| LoRA | Only small adapter matrices (~0.1% params) | $ (fits on single GPU) | Most practical choice |
| QLoRA | LoRA + 4-bit quantization | ¢ (fits on consumer GPU) | Budget-constrained |
| Prefix tuning | Learned "virtual tokens" prepended | $ | Lighter than LoRA |
| RLHF/DPO | Align with human preferences | $$ | Making model helpful/safe |

### LoRA — The Standard Method (Module 3)

```
Original model:      output = W × input        (W is huge, frozen)
LoRA adds:           output = W × input + (A × B) × input
                                           ↑
                              small matrices (rank 8-64), THESE get trained
```

Instead of training 7 billion parameters, train ~3 million (0.04%). Nearly same quality, fraction of cost.

### Training Data Format

```json
{"instruction": "Classify this support ticket", "input": "I can't log in to my account", "output": "account_access"}
{"instruction": "Classify this support ticket", "input": "I was charged twice", "output": "billing"}
{"instruction": "Classify this support ticket", "input": "App crashes on startup", "output": "technical"}
```

Typically need: 100-10,000 examples depending on task complexity.

### The Training Pipeline

1. **Choose base model** (LLaMA-2-7B, Mistral-7B, etc.)
2. **Prepare dataset** (instruction/input/output format)
3. **Configure LoRA** (rank, alpha, target layers)
4. **Train** (1-5 epochs, few hours on single GPU)
5. **Evaluate** (compare to base model on held-out test set)
6. **Merge or deploy** (merge LoRA weights into base, or serve separately)

### RLHF / DPO — Alignment

After supervised fine-tuning, an additional step aligns the model with human preferences:
- **RLHF** (Reinforcement Learning from Human Feedback): train a reward model on human preferences, then optimize the LLM to maximize that reward
- **DPO** (Direct Preference Optimization): simpler alternative — directly optimize on preference pairs without a separate reward model

This is what makes ChatGPT "helpful and harmless" rather than just "predicts next token."

## When Fine-Tuning vs Prompting

| Factor | Use Prompting | Use Fine-Tuning |
|--------|--------------|----------------|
| Data available | < 50 examples | 100-10,000 examples |
| Budget | Minimal | Some GPU budget |
| Consistency needed | Moderate | High (same format every time) |
| Latency sensitive | Adding context = more tokens = slower | Fine-tuned model responds directly |
| Domain specificity | General domain | Niche domain (medical, legal) |
| Iteration speed | Instant (change prompt) | Hours per experiment |

## Where You'll Use This

| Module | How Fine-Tuning Applies |
|--------|-------------------------|
| Module 3 | THE entire module — LoRA, PEFT, dataset prep, evaluation |
| Module 1 | Understanding that models behind APIs were fine-tuned (GPT-4 = pre-train + SFT + RLHF) |
| Module 5 | Deciding whether to prompt, RAG, or fine-tune for your capstone |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "Fine-tuning = training from scratch" | Fine-tuning starts from pre-trained weights. Much cheaper. |
| "Need millions of examples" | 100-1000 quality examples often sufficient for LoRA |
| "Fine-tuning always beats prompting" | For simple tasks, a good prompt is often enough. Fine-tune when prompting fails. |
| "Fine-tuned model knows everything from base + your data" | It can FORGET base capabilities (catastrophic forgetting). Balance matters. |
| "LoRA is inferior to full fine-tuning" | In practice, LoRA with r=16-64 matches full fine-tuning for most tasks |

## Connection to Other Topics

- **Builds on:** Pre-training (provides the starting point), Transformer Architecture (which layers to target)
- **Relates to:** Prompting (fine-tuning as an alternative when prompting isn't enough)
- **Enables:** Better domain-specific models, aligned models (RLHF), specialized agents
- **Python connection:** HuggingFace Trainer + PEFT library (from your python/transformers notes)

## Ready to Move On?

- ☐ I understand the difference between pre-training (general, expensive) and fine-tuning (specific, affordable)
- ☐ I can explain LoRA at a high level (small adapter matrices, freeze original weights)
- ☐ I know when to fine-tune vs when to prompt (data availability, consistency needs)
- ☐ I understand RLHF/DPO conceptually (align model with human preferences)

Next → **RAG** (ground the model in your private data without fine-tuning)
