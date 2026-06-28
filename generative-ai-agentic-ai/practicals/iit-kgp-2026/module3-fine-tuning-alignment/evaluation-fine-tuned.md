# Evaluation of Fine-Tuned Models

## The Problem This Solves

You've trained a model — training loss went down, it looks good on a few examples. But is it actually better? Fine-tuning can produce models that memorize training data (overfit), lose general capabilities (catastrophic forgetting), or improve on your metrics while degrading on everything else. You need rigorous evaluation that answers: "Did this investment pay off, and is it safe to deploy?"

## How It Works — Conceptual Model

Fine-tuning evaluation has THREE separate concerns:

1. **Task performance:** Is it better at your specific task than the baseline?
2. **Generalization:** Does it work on examples it hasn't seen (not just memorized)?
3. **Regression:** Did it lose capabilities it had before (general knowledge, reasoning)?

**Software analogy:** Like deploying a code change — you need (1) the feature works, (2) it handles edge cases, and (3) existing tests still pass. Ship without all three and you'll break production.

### The Evaluation Hierarchy

```
Level 1: Training metrics (loss curves)          — "Did training work mechanically?"
Level 2: Held-out test set (automatic metrics)   — "Does it generalize?"
Level 3: General benchmarks (regression check)   — "Did it break anything?"
Level 4: Human evaluation (qualitative)          — "Is it actually better to use?"
Level 5: A/B test in production (real-world)     — "Do users prefer it?"
```

## When to Use Which Evaluation

| Stage | Method | Cost | When |
|-------|--------|------|------|
| During training | Loss curves (train + eval) | Free | Every training run |
| After training | Held-out test set + benchmarks | Free (compute) | Every training run |
| Before deployment | Human evaluation (blind comparison) | Time | Every model you plan to ship |
| After deployment | A/B test, user feedback | Infra cost | Production models |

## Implementation Walkthrough

### Level 1: Training Metrics (Monitor During Training)

```python
import wandb

# What to watch in the loss curve:
# ✓ Train loss decreasing smoothly
# ✓ Eval loss decreasing (not increasing!)
# ✗ Eval loss increasing while train loss decreases = OVERFITTING
# ✗ Train loss not decreasing = LR too low or data issues
# ✗ Loss spikes = LR too high or data quality issues

# With Weights & Biases:
wandb.init(project="fine-tuning-eval")

# Key metrics to log during training:
# - train/loss (should decrease)
# - eval/loss (should decrease, then flatten — NOT increase)
# - learning_rate (track schedule)
# - grad_norm (should be stable, not exploding)
```

### Level 2: Task-Specific Evaluation

```python
def evaluate_task_performance(model, tokenizer, test_set: list[dict]) -> dict:
    """Evaluate on YOUR specific task metrics."""
    results = {"correct": 0, "format_valid": 0, "total": len(test_set)}
    
    for example in test_set:
        # Generate response
        output = generate(model, tokenizer, example["input"])
        
        # Check format compliance
        if is_valid_format(output, expected_schema):
            results["format_valid"] += 1
        
        # Check correctness (task-specific)
        if matches_expected(output, example["expected_output"]):
            results["correct"] += 1
    
    results["accuracy"] = results["correct"] / results["total"]
    results["format_rate"] = results["format_valid"] / results["total"]
    return results


def compare_to_baseline(fine_tuned_results: dict, baseline_results: dict) -> dict:
    """Compare fine-tuned model against baseline (best prompting result)."""
    comparison = {}
    for metric in fine_tuned_results:
        if isinstance(fine_tuned_results[metric], (int, float)):
            improvement = fine_tuned_results[metric] - baseline_results.get(metric, 0)
            comparison[metric] = {
                "fine_tuned": fine_tuned_results[metric],
                "baseline": baseline_results.get(metric, 0),
                "improvement": improvement,
                "significant": abs(improvement) > 0.05,  # 5% threshold
            }
    return comparison
```

### Level 3: General Capability Regression Check

```python
# Use standard benchmarks to check the model hasn't "forgotten" things

# Option 1: LM Evaluation Harness (comprehensive)
# pip install lm-eval
# lm_eval --model hf --model_args pretrained=./fine-tuned-model --tasks mmlu,hellaswag,arc

# Option 2: Quick sanity checks (manual)
REGRESSION_PROMPTS = [
    {"task": "math", "prompt": "What is 15% of 240?", "expected_contains": "36"},
    {"task": "reasoning", "prompt": "If all cats are animals and some animals are dogs, are all cats dogs?", "expected_contains": "no"},
    {"task": "code", "prompt": "Write a Python function to reverse a string", "expected_contains": "def"},
    {"task": "general", "prompt": "What is the capital of France?", "expected_contains": "Paris"},
    {"task": "instruction", "prompt": "Summarize this in one sentence: The quick brown fox jumps over the lazy dog. It is a pangram.", "check": "contains_one_sentence"},
]

def check_regression(model, tokenizer, prompts=REGRESSION_PROMPTS) -> dict:
    """Quick sanity check for capability regression."""
    passed = 0
    for test in prompts:
        output = generate(model, tokenizer, test["prompt"])
        if test.get("expected_contains") and test["expected_contains"].lower() in output.lower():
            passed += 1
        elif test.get("check") == "contains_one_sentence" and output.count(".") <= 2:
            passed += 1
    
    return {
        "regression_score": passed / len(prompts),
        "passed": passed,
        "total": len(prompts),
        "acceptable": passed / len(prompts) > 0.9,  # Allow 10% degradation max
    }
```

### Level 4: Human Evaluation (Blind Comparison)

```python
def prepare_blind_comparison(
    prompts: list[str],
    model_a,  # baseline (best prompting)
    model_b,  # fine-tuned
    n_samples: int = 20,
) -> list[dict]:
    """Prepare blind A/B comparison for human evaluation."""
    comparisons = []
    
    for prompt in random.sample(prompts, n_samples):
        response_a = generate(model_a, prompt)
        response_b = generate(model_b, prompt)
        
        # Randomly assign to position (avoid position bias)
        if random.random() > 0.5:
            comparisons.append({
                "prompt": prompt,
                "response_1": response_a, "model_1": "baseline",
                "response_2": response_b, "model_2": "fine_tuned",
            })
        else:
            comparisons.append({
                "prompt": prompt,
                "response_1": response_b, "model_1": "fine_tuned",
                "response_2": response_a, "model_2": "baseline",
            })
    
    return comparisons

# Human evaluator sees: prompt + response_1 + response_2
# Rates: "Which is better? 1, 2, or tie?"
# After collecting ratings, calculate win rate for fine-tuned model
```

### Level 5: LLM-as-Judge (Scalable Alternative to Human Eval)

```python
def llm_judge_comparison(prompt, response_a, response_b, judge_model="gpt-4o"):
    """Use GPT-4o to judge which response is better."""
    judgment = client.chat.completions.create(
        model=judge_model,
        messages=[{
            "role": "user",
            "content": f"""Compare these two responses. Which is better?

Prompt: {prompt}

Response A: {response_a}

Response B: {response_b}

Consider: accuracy, helpfulness, format compliance, conciseness.
Reply: {{"winner": "A" or "B" or "tie", "score_a": 1-5, "score_b": 1-5, "reason": "..."}}"""
        }],
        temperature=0,
    )
    return json.loads(judgment.choices[0].message.content)
```

## Configuration & What to Measure

| Level | Metric | Target | When It Fails |
|-------|--------|--------|--------------|
| Training | Eval loss trend | Decreasing → plateau | Increasing = overfitting |
| Task | Accuracy vs baseline | > 5% improvement | No improvement = wrong approach |
| Task | Format compliance | > 95% (ideally 99%) | Low = insufficient training data |
| Regression | General benchmarks | < 2% degradation | Large drop = catastrophic forgetting |
| Human | Win rate vs baseline | > 55% (ideally > 65%) | < 50% = fine-tuning made it worse |
| Production | User satisfaction | Improvement over baseline | No change = not worth the cost |

## What Can Go Wrong

| Problem | Symptom | Fix |
|---------|---------|-----|
| Overfitting (masked by test set) | Great test metrics, bad in production | Use truly diverse test set, not from same distribution as train |
| Evaluation metric doesn't capture quality | Metrics improve but output feels worse | Add human eval, LLM-as-judge |
| Data leakage between train and test | Unrealistically high test accuracy | Verify strict separation, ideally split by time |
| Benchmark gaming | Model scores well on benchmarks but not on real tasks | Add domain-specific test cases |
| Small test set (< 50 examples) | Results are noisy, not statistically significant | Larger test set, or run multiple times and average |
| Comparing unfairly | Fine-tuned model gets shorter prompt = fewer tokens = seems better | Compare with and without fine-tuning advantages |

## The Evaluation Report Template

```markdown
# Fine-Tuning Evaluation Report

## Model: [model name + training run ID]
## Date: [date]
## Training: [method] on [dataset size] examples, [epochs] epochs

### Task Performance (vs best prompting baseline)
| Metric | Baseline | Fine-tuned | Δ | Significant? |
|--------|----------|------------|---|--------------|
| Accuracy | X% | Y% | +Z% | Yes/No |
| Format compliance | X% | Y% | +Z% | Yes/No |

### Regression Check
| Benchmark | Base model | Fine-tuned | Δ | Acceptable? |
|-----------|-----------|------------|---|-------------|
| MMLU subset | X% | Y% | -Z% | Yes/No |

### Human/LLM-Judge Evaluation (N=20)
- Win rate: X% | Tie: Y% | Loss: Z%
- Average quality score: X/5 (baseline: Y/5)

### Recommendation: [Deploy / Iterate / Abandon]
### Justification: [Why]
```

## Cost & Resource Planning

| Activity | Cost | Time |
|----------|------|------|
| Automated task eval (test set) | Free (your GPU time) | 10-30 min |
| Benchmark evaluation (lm-eval) | Free (compute) | 1-4 hours |
| LLM-as-judge (GPT-4o, 50 examples) | $1-5 | 15 min |
| Human evaluation (20 comparisons) | Free (your time) | 1-2 hours |
| Full evaluation cycle | $1-5 + time | Half day |

## Decision Checkpoint

- [ ] I have a held-out test set (never seen during training)
- [ ] I'm comparing against a MEANINGFUL baseline (best prompting, not zero-shot)
- [ ] I've checked for regression on general capabilities
- [ ] I've done at least LLM-as-judge comparison (or human eval)
- [ ] I have a clear threshold for "good enough to deploy"
- [ ] I've documented results in an evaluation report
- [ ] If results are marginal (< 5% improvement), I'm questioning whether fine-tuning was worth it
