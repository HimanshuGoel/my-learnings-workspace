# When to Fine-Tune

## The Problem This Solves

You've built a RAG pipeline with carefully crafted prompts, but the model still doesn't behave the way you need — wrong tone, inconsistent format, domain-specific errors, or it can't follow complex instructions reliably. Before spending GPU hours and money on fine-tuning, you need a rigorous framework to determine if fine-tuning is actually the right intervention or if you're solving the wrong problem.

## How It Works — Conceptual Model

Fine-tuning modifies the model's weights (parameters) by training it on task-specific examples. Think of it like this:

- **Base model** = a generalist that knows many things but follows your specific instructions inconsistently
- **Prompting** = giving the generalist better instructions (no weight changes)
- **RAG** = giving the generalist reference materials to consult (no weight changes)
- **Fine-tuning** = retraining the generalist as a specialist for your specific task (weights change)

The key insight: fine-tuning changes the model's *default behavior*. After fine-tuning, it does things your way without being told — the format, tone, reasoning pattern, and domain knowledge become baked in.

### What Fine-Tuning Can Fix

- **Format consistency** — model always outputs your exact JSON schema without examples
- **Tone/style** — model writes in your brand voice by default
- **Domain terminology** — model uses field-specific terms correctly
- **Complex instruction following** — multi-constraint tasks the model can't handle via prompting alone
- **Latency reduction** — baked-in behavior means shorter prompts (fewer tokens, faster)
- **Cost reduction** — no few-shot examples needed = smaller prompts = cheaper per call

### What Fine-Tuning CANNOT Fix

- **Knowledge gaps** — model doesn't know your private data → use RAG instead
- **Factual accuracy** — fine-tuning doesn't make models more truthful, just more fluent
- **Reasoning ability** — can't make a 7B model reason like a 70B model
- **Real-time information** — model's knowledge is still frozen at training time

## When to Use vs Alternatives

### The Decision Ladder (Try in This Order)

| Step | Try First | Cost | Time to Implement | When It's Enough |
|------|-----------|------|-------------------|------------------|
| 1 | Better prompting (system prompt, few-shot) | Free | Hours | 70% of cases |
| 2 | RAG (retrieve domain knowledge) | $5-50/mo | Days | 20% of cases |
| 3 | Prompt + RAG combined | $10-100/mo | Days | 5% of cases |
| 4 | Fine-tuning | $50-500+ | Weeks | 5% of remaining |
| 5 | Train from scratch | $10K-1M+ | Months | Almost never |

### Fine-Tune When ALL of These Are True

1. **Prompting fails** — you've tried 5+ prompt iterations with few-shot examples and it's still inconsistent
2. **The pattern is learnable** — you have 100+ examples of correct input→output
3. **The gap is behavioral** — it's about HOW the model responds, not WHAT it knows
4. **The cost math works** — savings from shorter prompts or quality improvement justifies training cost
5. **You'll use it enough** — the fine-tuned model will serve 1000+ queries (amortize training cost)

### DON'T Fine-Tune When

- You haven't tried prompt engineering seriously (most common mistake)
- The problem is knowledge, not behavior (use RAG)
- You have < 100 quality examples (won't generalize)
- The base model literally can't do the task (need a bigger model, not fine-tuning)
- You need real-time information (fine-tuning doesn't help)
- You're trying to make a small model match a large model's reasoning (won't work)

## Implementation Walkthrough — Decision Process

### Step 1: Document the Gap

```python
# Before fine-tuning, create a clear test set showing the problem
test_cases = [
    {
        "input": "Summarize this customer ticket: ...",
        "expected_output": "Category: billing\nSeverity: medium\nSummary: ...",
        "base_model_output": "The customer seems to have an issue with...",
        "gap": "Wrong format — prose instead of structured fields",
    },
    # ... 20+ examples showing the gap consistently
]
```

### Step 2: Try Prompt Engineering First

```python
# Attempt 1: Zero-shot with instructions
# Attempt 2: Add output format specification
# Attempt 3: Add 2-3 few-shot examples
# Attempt 4: Add chain-of-thought for reasoning
# Attempt 5: Adjust temperature, add constraints

# Document results for each attempt
prompt_experiments = {
    "v1_zero_shot": {"format_compliance": 0.45, "accuracy": 0.72},
    "v2_few_shot": {"format_compliance": 0.78, "accuracy": 0.80},
    "v3_cot": {"format_compliance": 0.82, "accuracy": 0.85},
    "v4_strict": {"format_compliance": 0.88, "accuracy": 0.84},
    "v5_max_effort": {"format_compliance": 0.91, "accuracy": 0.86},
}
# If v5 is still not good enough → fine-tuning is justified
```

### Step 3: Check Data Availability

```python
# Minimum viable dataset sizes
DATASET_REQUIREMENTS = {
    "format_learning": 50-100,      # Model learns output structure
    "style_adaptation": 100-500,    # Model learns tone/voice
    "domain_specialization": 500-2000,  # Model learns domain patterns
    "complex_reasoning": 1000-5000, # Model learns reasoning chains
}

# Quality > Quantity — 100 perfect examples > 1000 mediocre ones
```

### Step 4: Cost-Benefit Analysis

```python
def should_fine_tune(
    current_accuracy: float,
    target_accuracy: float,
    queries_per_month: int,
    prompt_tokens_saved_per_query: int,
    training_cost: float,
    quality_value_per_query: float,  # $ value of improved quality
):
    # Cost savings from shorter prompts (no few-shot needed post-fine-tune)
    monthly_token_savings = queries_per_month * prompt_tokens_saved_per_query * 0.15 / 1_000_000
    
    # Value of quality improvement
    accuracy_improvement = target_accuracy - current_accuracy
    monthly_quality_value = queries_per_month * accuracy_improvement * quality_value_per_query
    
    # Payback period
    monthly_benefit = monthly_token_savings + monthly_quality_value
    payback_months = training_cost / monthly_benefit if monthly_benefit > 0 else float('inf')
    
    return {
        "monthly_savings": monthly_token_savings,
        "monthly_quality_value": monthly_quality_value,
        "payback_months": payback_months,
        "recommendation": "fine-tune" if payback_months < 3 else "keep prompting",
    }
```

### Step 5: Define Success Criteria BEFORE Training

```python
# Don't start training without knowing what "success" looks like
success_criteria = {
    "format_compliance": "> 98% (vs 91% with best prompt)",
    "accuracy": "> 90% (vs 86% with best prompt)", 
    "latency_reduction": "20%+ (fewer prompt tokens)",
    "cost_reduction": "$X/month savings",
    "no_regression": "General capabilities don't degrade",
}
```

## The OpenAI Fine-Tuning Shortcut

For most practitioners, the fastest path is OpenAI's fine-tuning API:

```python
# When to use OpenAI fine-tuning vs open-source:
OPENAI_FINE_TUNING = {
    "best_for": [
        "Format/style consistency",
        "Quick iteration (hours not days)",
        "Don't want to manage GPUs",
        "gpt-4o-mini is close but not quite right",
    ],
    "limitations": [
        "No control over training process",
        "Vendor lock-in (can't export weights)",
        "Limited model choices (gpt-4o-mini, gpt-4o)",
        "Data sent to OpenAI (privacy concern)",
    ],
    "cost": "~$3-25 per training run (depends on data size)",
    "time": "15 minutes to 2 hours",
}

OPEN_SOURCE_FINE_TUNING = {
    "best_for": [
        "Full control over process",
        "Privacy (data stays local)",
        "Custom architectures (LoRA, DPO)",
        "Cost optimization at scale",
        "Academic understanding",
    ],
    "limitations": [
        "Need GPU access ($1-5/hr)",
        "More complex setup",
        "More things can go wrong",
        "Slower iteration cycle",
    ],
    "cost": "$10-200 per training run (GPU hours)",
    "time": "2-48 hours (depending on model size + data)",
}
```

## Configuration & Hyperparameters

| Decision | Recommended Default | Notes |
|----------|-------------------|-------|
| Try prompting first? | YES (always) | Don't skip this step |
| Minimum dataset size | 100 examples | Less = overfitting risk |
| Model to fine-tune | gpt-4o-mini (OpenAI) or Llama-3-8B (local) | Start small |
| Fine-tuning method | LoRA (not full) for open-source | 10x cheaper, nearly same quality |
| Epochs | 2-4 | More = overfitting; monitor eval loss |
| Learning rate | 1e-5 (full) or 2e-4 (LoRA) | Lower for larger models |
| Eval split | 10-20% of dataset | Must hold out for honest evaluation |

## What Can Go Wrong

| Problem | Symptom | Fix |
|---------|---------|-----|
| Overfitting | Perfect on training data, bad on new inputs | More diverse data, fewer epochs, regularization |
| Catastrophic forgetting | Fine-tuned model loses general abilities | Use LoRA (preserves base), add general data |
| Wrong problem diagnosis | Fine-tuning doesn't improve the issue | Revisit: is it really behavioral, or knowledge/reasoning? |
| Data quality issues | Model learns wrong patterns | Audit training data, remove contradictions |
| Cost overrun | Training takes longer/costs more than expected | Start with small experiments, estimate before scaling |
| No improvement | Metrics unchanged after fine-tuning | Dataset may not contain the signal, or too small |

## Cost & Resource Planning

| Approach | Cost Per Run | Time | Best For |
|----------|-------------|------|----------|
| OpenAI fine-tuning (gpt-4o-mini) | $3-25 | 15 min - 2 hr | Format/style, quick iteration |
| OpenAI fine-tuning (gpt-4o) | $25-200 | 1-8 hr | Complex behavior |
| LoRA on Llama-3-8B (cloud GPU) | $5-20 | 2-8 hr | Full control, privacy |
| LoRA on Llama-3-70B (cloud GPU) | $50-200 | 6-24 hr | High-quality open-source |
| Full fine-tuning (any model) | $100-1000+ | 12-72 hr | Rarely needed |

## Evaluation — How to Know If It Worked

| Metric | Compare Against | Threshold |
|--------|-----------------|-----------|
| Task accuracy | Best prompt engineering result | > 5% improvement |
| Format compliance | Best prompt result | > 95% (ideally 99%+) |
| General capability | Base model on benchmarks | No regression > 2% |
| Latency | Base model with full prompt | Should be faster (shorter prompt) |
| Cost per query | Base model with full prompt | Should be cheaper (fewer tokens) |
| Human preference | Side-by-side comparison | > 60% prefer fine-tuned |

## Decision Checkpoint

Before proceeding to the rest of Module 3, ask yourself:

- [ ] I've tried at least 5 prompt engineering iterations
- [ ] I can clearly articulate what the model does wrong (format? style? domain? reasoning?)
- [ ] I have 100+ examples of correct behavior
- [ ] The cost math makes sense (training cost < 3 months of quality improvement value)
- [ ] I've defined success criteria with measurable thresholds
- [ ] I accept that fine-tuning is an experiment (may not work first try)

If YES to all → proceed to choosing a fine-tuning method (Full SFT vs LoRA vs DPO)
If NO to any → go back and address the gap. Most likely: better prompting or RAG will solve it.
