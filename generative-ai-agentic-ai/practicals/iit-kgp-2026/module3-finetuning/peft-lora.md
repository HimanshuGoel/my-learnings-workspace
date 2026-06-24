# PEFT & LoRA

## The Problem This Solves

Full fine-tuning updates billions of parameters, requiring massive GPU memory and creating a full copy of the model for each task. LoRA (Low-Rank Adaptation) achieves 90-98% of full fine-tuning quality while training only 0.1-1% of parameters — making fine-tuning accessible on consumer GPUs and enabling multiple task-specific adapters that share a single base model.

## How It Works — Conceptual Model

### The Key Insight

During fine-tuning, the weight changes (ΔW) are typically low-rank — meaning they can be well-approximated by the product of two much smaller matrices. Instead of updating a 4096×4096 weight matrix (16M parameters), LoRA trains two small matrices: 4096×16 and 16×4096 (131K parameters total). That's 99.2% fewer parameters.

**Software analogy:** Imagine you have a massive configuration file (the base model weights) that mostly stays the same. Instead of copying the entire file for each customer, you store just the DIFF (the changes). LoRA is that diff — small, composable, and doesn't require duplicating the whole system.

### How LoRA Matrices Work

```
Original weight matrix: W (4096 × 4096) = 16M parameters — FROZEN
LoRA adapter:           A (4096 × r) × B (r × 4096) where r = 8-64
Total LoRA params:      4096 × r × 2 = ~65K-524K parameters

During inference: output = W·x + A·B·x (base output + adapter adjustment)
During training: only A and B are updated (W stays frozen)
```

### The "Rank" in Low-Rank

- Rank (r) = how many dimensions the adapter uses to represent changes
- r=8: Very small adapter, cheap, good for simple format changes
- r=16-32: Sweet spot for most tasks
- r=64-128: Larger adapter, approaches full fine-tuning quality
- Higher rank = more parameters = more memory = potentially better quality

### Variants

| Variant | What It Adds | When to Use |
|---------|-------------|-------------|
| LoRA | Low-rank adapters on attention layers | Default choice |
| QLoRA | LoRA on 4-bit quantized base model | Limited GPU budget (fit 70B on single GPU) |
| LoRA+ | Different learning rates for A and B matrices | Slightly better convergence |
| DoRA | Weight decomposition + LoRA | Closer to full fine-tuning quality |
| AdaLoRA | Adaptive rank allocation per layer | Automatic rank tuning |

## When to Use vs Alternatives

| Situation | Recommendation |
|-----------|---------------|
| First fine-tuning attempt | LoRA (always start here) |
| Limited GPU (16-24 GB) | QLoRA (4-bit base + LoRA) |
| Need maximum quality, have budget | Full SFT (but try LoRA first) |
| Multiple tasks on same base model | LoRA (swap adapters per task) |
| Production serving multiple fine-tunes | LoRA (one base + many adapters) |
| Very limited data (< 100 examples) | LoRA with low rank (r=8) |
| Complex behavior change | LoRA with higher rank (r=32-64) |

## Implementation Walkthrough

### Basic LoRA with PEFT

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Configure LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # rank — start here
    lora_alpha=32,                 # scaling factor (usually 2× rank)
    lora_dropout=0.05,             # regularization
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj",  # attention
                    "gate_proj", "up_proj", "down_proj"],      # MLP
    bias="none",
)

# Wrap model with LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# → trainable params: 6.5M || all params: 8B || trainable%: 0.08%
```

### QLoRA (4-bit Quantization + LoRA)

```python
from transformers import BitsAndBytesConfig
import torch

# Quantize base model to 4-bit (reduces memory ~4×)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # normalized float 4-bit
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,       # quantize the quantization constants
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B-Instruct",
    quantization_config=bnb_config,
    device_map="auto",
)

# Then apply LoRA exactly as before
model = get_peft_model(model, lora_config)
# Now 8B model fits on a single 16GB GPU!
```

### Training with TRL (Recommended)

```python
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig

lora_config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
                         target_modules="all-linear")

config = SFTConfig(
    output_dir="./lora-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,              # Higher LR for LoRA (vs 2e-5 for full)
    max_seq_length=2048,
    bf16=True,
)

trainer = SFTTrainer(
    model=model_name,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    peft_config=lora_config,
    args=config,
)
trainer.train()
trainer.save_model("./lora-adapter")  # Saves only the adapter (few MB)
```

### Loading and Using the Adapter

```python
from peft import PeftModel

# Load base model + adapter
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B-Instruct")
model = PeftModel.from_pretrained(base_model, "./lora-adapter")

# For inference: merge adapter into base (optional, slightly faster inference)
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged-model")
```

### Swapping Adapters at Runtime

```python
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B-Instruct")

# Load multiple adapters
model = PeftModel.from_pretrained(base, "./adapter-customer-support")
model.load_adapter("./adapter-code-review", adapter_name="code_review")

# Switch between tasks
model.set_adapter("default")        # customer support mode
model.set_adapter("code_review")    # code review mode
# Same base model, different behaviors!
```

## Configuration & Hyperparameters

| Parameter | Default | Range | Guidance |
|-----------|---------|-------|----------|
| Rank (r) | 16 | 4-128 | Higher = better quality, more params. Start at 16. |
| Alpha | 2 × rank | rank to 4×rank | Scaling factor. Alpha/rank = effective LR multiplier. |
| Dropout | 0.05 | 0-0.1 | Regularization. 0.05 is safe default. |
| Target modules | All attention + MLP | Varies by arch | More modules = better quality, more params |
| Learning rate | 2e-4 | 1e-4 to 5e-4 | 10× higher than full fine-tuning! |
| Epochs | 3 | 1-5 | Monitor eval loss for overfitting |
| Batch size | 4 × 4 grad accum | 2-8 per device | Effective batch 16-32 works well |

### Which Layers to Target?

```python
# Minimal (cheapest, often enough for format changes):
target_modules = ["q_proj", "v_proj"]

# Recommended (good balance):
target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]

# Maximum (best quality, most parameters):
target_modules = "all-linear"  # All linear layers including MLP
```

## What Can Go Wrong

| Problem | Symptom | Fix |
|---------|---------|-----|
| Rank too low | Model can't learn the pattern (underfitting) | Increase r from 8 → 16 → 32 |
| Rank too high | Overfitting, no benefit over full SFT | Reduce rank, you're wasting memory |
| Wrong target modules | Model doesn't change behavior | Add MLP layers (gate_proj, up_proj, down_proj) |
| LR too high for LoRA | Loss spikes, unstable training | Reduce from 2e-4 to 1e-4 |
| QLoRA quality loss | Noticeable quality gap vs LoRA | Try LoRA without quantization, or increase rank |
| Adapter doesn't load | Model architecture mismatch | Verify same base model version |
| Merged model quality differs | Merge process introduced errors | Use model directly without merging |

## Cost & Resource Planning

| Setup | GPU Memory Needed | Cost/Hour | Training Time (1K examples) |
|-------|-------------------|-----------|----------------------------|
| LoRA on 8B (bf16) | ~20 GB (1× A100 40GB) | $1-2/hr | 2-4 hours |
| QLoRA on 8B (4-bit) | ~8 GB (1× T4 16GB) | $0.50-1/hr | 3-6 hours |
| LoRA on 13B (bf16) | ~30 GB (1× A100 40GB) | $1-2/hr | 4-8 hours |
| QLoRA on 70B (4-bit) | ~40 GB (1× A100 80GB) | $2-4/hr | 8-24 hours |
| LoRA on 70B (bf16) | ~160 GB (4× A100) | $8-16/hr | 6-16 hours |

**Key savings vs full SFT:** LoRA uses 2-5× less memory, enabling larger models on smaller GPUs. Adapter files are typically 10-100 MB (vs 16-140 GB for full model).

## Evaluation

| Question | How to Check |
|----------|-------------|
| Is LoRA quality close enough to full SFT? | Run same eval on both → expect < 3% gap |
| Is the adapter generalizing (not just memorizing)? | Test on held-out examples the model hasn't seen |
| Does higher rank help? | Train r=8, r=16, r=32, compare on eval set |
| Are general capabilities preserved? | Run base model benchmarks on LoRA model → no regression |
| Can I merge safely? | Compare merged vs unmerged on test set → identical results |

## Decision Checkpoint

- [ ] LoRA at rank=16 is my starting point (not full SFT)
- [ ] I know which layers to target for my architecture (check model docs)
- [ ] I understand that LR for LoRA is ~10× higher than full SFT
- [ ] I can fit my model with LoRA/QLoRA on available hardware
- [ ] I understand the adapter file is separate from base model (composable)
- [ ] I know I can swap adapters at runtime for multi-task serving
