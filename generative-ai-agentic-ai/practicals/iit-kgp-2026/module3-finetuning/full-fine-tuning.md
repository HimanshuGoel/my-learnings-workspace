# Full Fine-Tuning (Supervised Fine-Tuning / SFT)

## The Problem This Solves

You've decided fine-tuning is justified (passed the decision checkpoint). Now you need to understand what happens when you train a model on your data — how Supervised Fine-Tuning (SFT) modifies model weights, what the training loop looks like, and why this is the foundation that all other techniques (LoRA, RLHF, DPO) build upon.

## How It Works — Conceptual Model

### The Core Idea

SFT is conceptually simple: you show the model thousands of (input, correct_output) pairs and adjust its weights so it's more likely to produce those correct outputs. It's the same process used to train the model originally (pre-training), but focused on your specific task.

**Software analogy:** Think of the base model as a large Java class with millions of configuration parameters. Pre-training set those parameters for "general English text." Fine-tuning is like running a specialized optimizer that adjusts those parameters for "your specific task format and behavior."

### What Happens During Training

1. **Forward pass:** Input goes through the model, it predicts the next token
2. **Loss calculation:** Compare prediction to your correct output (cross-entropy loss)
3. **Backward pass:** Calculate how each weight contributed to the error (gradients)
4. **Weight update:** Nudge each weight slightly to reduce the error (optimizer step)
5. **Repeat:** Thousands of times across your dataset, multiple epochs

### What Changes vs What Doesn't

| Changes | Doesn't Change |
|---------|---------------|
| All model weights (billions of parameters) | Model architecture |
| Default output behavior | Maximum capability ceiling |
| Token prediction probabilities | Context window size |
| How confidently it follows your patterns | Tokenizer |

### Why Full Fine-Tuning Is Expensive

- **Memory:** Need to store all model weights + gradients + optimizer states in GPU RAM
- A 7B parameter model needs ~28 GB just for weights (float32)
- Add gradients + optimizer = ~3-4× the weight size = ~84-112 GB
- This is why you need multiple large GPUs (A100 80GB) for anything > 7B

## When to Use vs Alternatives

| Method | What It Does | Memory Needed | Quality | When to Choose |
|--------|-------------|---------------|---------|----------------|
| Full SFT | Updates ALL weights | 3-4× model size | Best (reference) | You have budget + need maximum quality |
| LoRA | Updates small adapter matrices | ~1.1× model size | 90-98% of full | Default choice (cost-effective) |
| QLoRA | LoRA on quantized base | ~0.5× model size | 85-95% of full | Limited GPU budget |
| OpenAI API | Managed full SFT | None (cloud) | Good for GPT models | Quick iteration, format fixes |

**Recommendation:** Use full SFT as your *mental model* for understanding fine-tuning, but use LoRA for *actual practice* (next topic). Full SFT is only justified when LoRA demonstrably underperforms.

## Implementation Walkthrough

### With OpenAI API (Simplest Path)

```python
from openai import OpenAI
client = OpenAI()

# Step 1: Prepare data in JSONL format
# training_data.jsonl:
# {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}

# Step 2: Upload training file
file = client.files.create(file=open("training_data.jsonl", "rb"), purpose="fine-tune")

# Step 3: Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "learning_rate_multiplier": 1.8,
        "batch_size": 4,
    },
)

# Step 4: Monitor progress
events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job.id)

# Step 5: Use fine-tuned model
response = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:org:custom-name:id",
    messages=[{"role": "user", "content": "..."}],
)
```

### With Hugging Face (Full Control)

```python
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    TrainingArguments, Trainer,
)
from datasets import load_dataset

# Load model and tokenizer
model_name = "meta-llama/Llama-3-8B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load and format dataset
dataset = load_dataset("json", data_files="training_data.jsonl")

def format_example(example):
    """Format as chat template."""
    messages = example["messages"]
    text = tokenizer.apply_chat_template(messages, tokenize=False)
    return tokenizer(text, truncation=True, max_length=2048)

tokenized = dataset.map(format_example, remove_columns=dataset["train"].column_names)

# Training arguments
training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,   # effective batch size = 4 * 4 = 16
    learning_rate=2e-5,
    warmup_ratio=0.1,
    weight_decay=0.01,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=50,
    save_strategy="steps",
    save_steps=100,
    bf16=True,                       # mixed precision (saves memory)
    gradient_checkpointing=True,     # trade compute for memory
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
)
trainer.train()
trainer.save_model("./fine-tuned-model")
```

### Using TRL (Simplified API)

```python
from trl import SFTTrainer, SFTConfig

config = SFTConfig(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-5,
    max_seq_length=2048,
    dataset_text_field="text",
)

trainer = SFTTrainer(
    model=model_name,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    args=config,
)
trainer.train()
```

## Dataset Requirements

| Aspect | Requirement | Why |
|--------|-------------|-----|
| Format | JSONL with messages array (chat format) | Standard for instruction-tuned models |
| Size | 100-5000 examples (task-dependent) | Less = overfit, more = diminishing returns |
| Quality | Every example must be correct | Model learns FROM your data — garbage in = garbage out |
| Diversity | Cover edge cases, not just happy path | Prevents narrow overfitting |
| Split | 80% train / 10% validation / 10% test | Validation for early stopping, test for final eval |

## Configuration & Hyperparameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| Learning rate | 2e-5 | 1e-5 to 5e-5 | Too high = instability, too low = no learning |
| Epochs | 3 | 1-5 | More = better fit BUT risk of overfitting |
| Batch size | 4-16 | 2-32 | Larger = more stable gradients, more memory |
| Warmup | 10% of steps | 5-15% | Prevents early instability |
| Weight decay | 0.01 | 0-0.1 | Regularization against overfitting |
| Max seq length | 2048 | 512-4096 | Must cover your longest example |
| bf16/fp16 | bf16 preferred | — | Halves memory with minimal quality loss |
| Gradient checkpointing | On | — | Trades ~30% speed for ~60% memory savings |

## What Can Go Wrong

| Problem | Symptom | How to Detect | Fix |
|---------|---------|---------------|-----|
| Overfitting | Train loss ↓ but eval loss ↑ after epoch 2 | Plot train vs eval loss | Reduce epochs, add dropout, more data |
| Catastrophic forgetting | Model can't do general tasks anymore | Test on general benchmarks | Mix in general instruction data (10-20%) |
| Learning rate too high | Loss spikes, NaN values, garbage output | Monitor loss curve | Reduce LR by 2-5×, add warmup |
| Learning rate too low | Loss barely decreases over epochs | Loss curve is flat | Increase LR by 2-5× |
| Data contamination | Model memorizes, doesn't generalize | Test on truly unseen examples | Ensure train/test split has no leakage |
| OOM (Out of Memory) | CUDA OOM error | Crashes during training | Reduce batch size, enable gradient checkpointing, use bf16 |

## Cost & Resource Planning

| Model Size | GPU Needed | Training Time (1000 examples) | Approx Cost |
|-----------|-----------|-------------------------------|-------------|
| 3B | 1× A100 40GB | 1-3 hours | $5-15 |
| 7-8B | 1× A100 80GB or 2× A100 40GB | 3-8 hours | $15-40 |
| 13B | 2× A100 80GB | 6-16 hours | $30-80 |
| 70B | 8× A100 80GB | 24-72 hours | $200-600 |

## Evaluation

| What to Measure | How | Target |
|----------------|-----|--------|
| Training loss curve | Should decrease smoothly, plateau | No spikes, converges |
| Eval loss | Should decrease, then flatten (not increase) | Lowest point = best checkpoint |
| Task-specific metrics | Run your test set through fine-tuned model | > baseline (best prompt) |
| General capability | Run MMLU/HellaSwag subset | No regression > 2% |
| Human evaluation | Blind A/B test: base vs fine-tuned | > 60% prefer fine-tuned |

## Decision Checkpoint

After understanding full SFT, ask yourself:

- [ ] Do I actually need to update ALL model weights? (probably not → use LoRA)
- [ ] Can I afford the GPU memory for full fine-tuning? (7B+ needs expensive GPUs)
- [ ] Is the quality gap between LoRA and full SFT worth the 3-10× cost? (usually no)
- [ ] Am I fine-tuning for learning/understanding, or for production? (learning = LoRA is fine)

**Most practitioners should proceed to LoRA/PEFT** — full SFT is the reference implementation, LoRA is what you'll actually use.
