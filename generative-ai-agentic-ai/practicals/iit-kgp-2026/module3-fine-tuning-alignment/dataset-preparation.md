# Dataset Preparation

## The Problem This Solves

Fine-tuning is only as good as the data you train on. "Garbage in, garbage out" applies more here than anywhere else in ML — the model will confidently replicate every error, inconsistency, and bad pattern in your training data. Dataset preparation is the make-or-break step that determines whether your fine-tuning investment produces a useful model or an expensive failure.

## How It Works — Conceptual Model

The model learns by adjusting weights to predict your outputs given your inputs. Every training example is a signal about "what behavior looks like." This means:

- **High-quality examples** = clear signal → model learns the right pattern quickly
- **Noisy/inconsistent examples** = conflicting signals → model learns averaged noise
- **Too few examples** = insufficient signal → model overfits to memorized patterns
- **Too many mediocre examples** = diluted signal → model learns the average, not the best

**Software analogy:** Think of it like training a junior developer. If you give them 100 perfectly-written code reviews, they learn good patterns fast. If you give them 1000 reviews where half are sloppy, they learn sloppy as "acceptable." Quality of examples > quantity.

## When to Use Different Dataset Strategies

| Scenario | Strategy | Data Source |
|----------|----------|-------------|
| Format/structure task | Curate from production logs | Existing API calls with correct outputs |
| Style/tone change | Rewrite base model outputs in target style | Take model output → manually edit to target |
| Domain specialization | Expert-annotated examples | Domain experts write ideal responses |
| Instruction following | Diverse instruction datasets | Combine existing datasets + custom |
| Cold start (no data) | Synthetic generation | Use GPT-4o to generate training examples |

## Implementation Walkthrough

### Step 1: Define Your Data Format

```python
# OpenAI format (standard for chat fine-tuning)
{
    "messages": [
        {"role": "system", "content": "You are a customer support classifier."},
        {"role": "user", "content": "My payment was charged twice last week."},
        {"role": "assistant", "content": "Category: billing\nSeverity: high\nSummary: Double charge on payment\nAction: escalate to billing team"}
    ]
}

# Hugging Face format (instruction tuning)
{
    "instruction": "Classify this customer ticket.",
    "input": "My payment was charged twice last week.",
    "output": "Category: billing\nSeverity: high\nSummary: Double charge on payment"
}
```

### Step 2: Collect and Curate Data

```python
import json
from pathlib import Path

class DatasetBuilder:
    def __init__(self):
        self.examples = []
    
    def add_from_production_logs(self, logs: list[dict]):
        """Extract successful interactions from production."""
        for log in logs:
            if log["user_rating"] >= 4:  # Only high-quality interactions
                self.examples.append({
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": log["query"]},
                        {"role": "assistant", "content": log["response"]},
                    ]
                })
    
    def add_synthetic(self, generator_llm, n: int = 100):
        """Generate synthetic training examples using a stronger model."""
        for _ in range(n):
            # Use GPT-4o to generate diverse examples
            example = generator_llm.invoke(
                "Generate a realistic customer ticket and its ideal classification..."
            )
            self.examples.append(self._format_example(example))
    
    def add_manual(self, input_text: str, ideal_output: str):
        """Manually add curated examples."""
        self.examples.append({
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_text},
                {"role": "assistant", "content": ideal_output},
            ]
        })
    
    def export_jsonl(self, path: str):
        """Export in JSONL format for training."""
        with open(path, "w") as f:
            for ex in self.examples:
                f.write(json.dumps(ex) + "\n")
```

### Step 3: Quality Filtering

```python
def filter_dataset(examples: list[dict]) -> list[dict]:
    """Apply quality filters to training data."""
    filtered = []
    
    for ex in examples:
        assistant_msg = ex["messages"][-1]["content"]
        user_msg = ex["messages"][-2]["content"]
        
        # Filter: too short (likely incomplete)
        if len(assistant_msg) < 20:
            continue
        
        # Filter: too long (likely verbose/off-topic)
        if len(assistant_msg) > 2000:
            continue
        
        # Filter: doesn't follow expected format
        if not has_expected_structure(assistant_msg):
            continue
        
        # Filter: duplicates or near-duplicates
        if is_duplicate(user_msg, seen_inputs):
            continue
        
        # Filter: contradicts other examples
        if contradicts_existing(ex, filtered):
            continue
        
        filtered.append(ex)
    
    return filtered
```

### Step 4: Dataset Splitting

```python
from sklearn.model_selection import train_test_split

def split_dataset(examples: list[dict], test_size=0.1, val_size=0.1):
    """Split into train/val/test with stratification if possible."""
    # First split: separate test set
    train_val, test = train_test_split(examples, test_size=test_size, random_state=42)
    
    # Second split: separate validation from training
    val_ratio = val_size / (1 - test_size)
    train, val = train_test_split(train_val, test_size=val_ratio, random_state=42)
    
    return {
        "train": train,       # ~80% — model trains on this
        "validation": val,    # ~10% — monitor during training (early stopping)
        "test": test,         # ~10% — final evaluation (never seen during training)
    }
```

### Step 5: Synthetic Data Generation

```python
from openai import OpenAI

def generate_synthetic_examples(
    task_description: str,
    output_format: str,
    n_examples: int = 200,
    diversity_seed: list[str] = None,
) -> list[dict]:
    """Use GPT-4o to generate training examples for fine-tuning a smaller model."""
    
    client = OpenAI()
    examples = []
    
    prompt = f"""Generate a training example for this task:

Task: {task_description}
Expected output format: {output_format}

Requirements:
- Make the input realistic and diverse
- The output should be perfect (this is training data)
- Cover edge cases and varying difficulty
- Each example should be unique

Generate ONE example as JSON:
{{"input": "...", "output": "..."}}"""
    
    for i in range(n_examples):
        seed = diversity_seed[i % len(diversity_seed)] if diversity_seed else ""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Context for diversity: {seed}"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.9,  # High temp for diversity
        )
        example = json.loads(response.choices[0].message.content)
        examples.append(example)
    
    return examples
```

### Step 6: Validation Before Training

```python
def validate_dataset(path: str) -> dict:
    """Run pre-training validation checks."""
    issues = []
    examples = [json.loads(line) for line in open(path)]
    
    # Check: minimum size
    if len(examples) < 50:
        issues.append(f"Too few examples: {len(examples)} (need 50+)")
    
    # Check: format consistency
    for i, ex in enumerate(examples):
        if "messages" not in ex:
            issues.append(f"Example {i}: missing 'messages' field")
        if len(ex.get("messages", [])) < 2:
            issues.append(f"Example {i}: need at least user + assistant messages")
    
    # Check: token length distribution
    lengths = [count_tokens(ex) for ex in examples]
    if max(lengths) > 4096:
        issues.append(f"Examples exceed max token length: {max(lengths)}")
    
    # Check: diversity (unique inputs)
    inputs = [ex["messages"][-2]["content"] for ex in examples]
    unique_ratio = len(set(inputs)) / len(inputs)
    if unique_ratio < 0.9:
        issues.append(f"Low diversity: {unique_ratio:.0%} unique inputs")
    
    return {
        "total_examples": len(examples),
        "avg_tokens": sum(lengths) / len(lengths),
        "max_tokens": max(lengths),
        "unique_ratio": unique_ratio,
        "issues": issues,
        "valid": len(issues) == 0,
    }
```

## Configuration & Requirements

| Aspect | Minimum | Recommended | Notes |
|--------|---------|-------------|-------|
| Dataset size | 50 examples | 200-1000 | More for complex tasks |
| Quality bar | All correct | Expert-verified | One bad example teaches bad behavior |
| Diversity | 90% unique inputs | 95%+ | Prevents memorization |
| Format | Consistent across all examples | Template-enforced | Inconsistency confuses the model |
| Max token length | Fit in model context | < 2048 tokens per example | Longer = more memory, slower training |
| Train/val/test split | 80/10/10 | 80/10/10 | Always hold out test set |
| System prompt | Same across all examples | Consistent | Becomes the model's default behavior |

## What Can Go Wrong

| Problem | Symptom | Fix |
|---------|---------|-----|
| Contradictory examples | Model gives random answers, oscillates | Audit data for conflicting input→output pairs |
| Format inconsistency | Model sometimes follows format, sometimes doesn't | Standardize ALL outputs to exact format before training |
| Too few examples | Overfits — perfect on training data, bad on new | Add synthetic examples, collect more, or reduce model/rank |
| Too many low-quality examples | Model learns average behavior (mediocre) | Filter to top 20% quality, re-train |
| Data leakage (test in train) | Eval scores are misleadingly high | Strict split by time or content, verify no overlap |
| Biased dataset | Model inherits biases in training data | Audit for representation, add diverse examples |
| Synthetic data too uniform | Model can't handle real-world variation | Add diversity seeds, include real examples (even 10%) |

## Cost & Resource Planning

| Activity | Cost | Time |
|----------|------|------|
| Manual curation (100 examples) | Free (your time) | 4-8 hours |
| Synthetic generation (GPT-4o, 500 examples) | ~$5-15 | 1-2 hours |
| Expert annotation (500 examples) | $500-2000 (contractor) | 1-2 weeks |
| Quality filtering + validation | Free (scripted) | 30 minutes |
| Iteration (fix issues, regenerate) | Variable | 1-3 cycles typical |

## Evaluation

| Check | How | Pass Criteria |
|-------|-----|---------------|
| Format compliance | All outputs match expected structure | 100% (fix before training) |
| No contradictions | Automated + manual review | Zero conflicting pairs |
| Diversity score | Unique inputs / total inputs | > 90% |
| Token distribution | Histogram of example lengths | No extreme outliers |
| Domain coverage | Examples cover all expected categories | Each category has 10+ examples |
| Quality audit | Sample 20 random examples, rate 1-5 | Average > 4.5 |

## Decision Checkpoint

- [ ] Dataset format matches target model's expected input (messages array or instruction format)
- [ ] Every example is correct — I'd be happy if the model produced this exact output
- [ ] Dataset is diverse enough to generalize (90%+ unique inputs)
- [ ] No contradictions between examples (same input → different outputs)
- [ ] Proper train/val/test split (no leakage)
- [ ] Validation script passes with no issues
- [ ] Dataset size is appropriate for task complexity (see table above)
- [ ] I have a plan to iterate if first training run shows data issues
