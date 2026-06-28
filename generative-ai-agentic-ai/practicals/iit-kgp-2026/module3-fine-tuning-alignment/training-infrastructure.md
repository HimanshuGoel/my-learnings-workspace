# Training Infrastructure

## The Problem This Solves

You have your dataset and chosen LoRA/SFT — but where do you actually train? GPU options are confusing (T4 vs A100 vs H100), cloud providers charge differently, and miscalculating memory requirements means either OOM crashes or paying for unused capacity. You need a clear mental model for hardware selection, cost estimation, and practical cloud GPU workflows.

## How It Works — Conceptual Model

### GPU Memory Budget

Training requires storing three things in GPU RAM simultaneously:

```
Total GPU Memory = Model Weights + Gradients + Optimizer States + Activations

Full SFT (float32):    4B per param + 4B grad + 8B optimizer = 16B per parameter
Full SFT (bf16):       2B per param + 2B grad + 8B optimizer = 12B per parameter
LoRA (bf16 base):      2B per param (frozen) + tiny adapter overhead
QLoRA (4-bit base):    0.5B per param (frozen) + adapter overhead
```

**Rule of thumb:**
- Full SFT bf16: ~12 bytes × param count (7B model → ~84 GB)
- LoRA bf16: ~2.5 bytes × param count (7B model → ~18 GB)
- QLoRA 4-bit: ~0.7 bytes × param count (7B model → ~5 GB + overhead ≈ 8 GB)

### GPU Selection Guide

| GPU | VRAM | Best For | Cloud Cost/hr |
|-----|------|----------|---------------|
| T4 | 16 GB | QLoRA on ≤ 8B models, inference | $0.50-1.00 |
| A10G | 24 GB | LoRA on 8B, QLoRA on 13B | $1.00-1.50 |
| L4 | 24 GB | Similar to A10G, newer | $0.80-1.20 |
| A100 40GB | 40 GB | LoRA on 13B, QLoRA on 70B | $2.00-3.50 |
| A100 80GB | 80 GB | Full SFT 8B, LoRA on 70B | $3.00-5.00 |
| H100 80GB | 80 GB | Fastest training, large models | $4.00-8.00 |

### What Fits Where?

| Model Size | Full SFT | LoRA (bf16) | QLoRA (4-bit) |
|-----------|----------|-------------|---------------|
| 3B | 1× A100 40GB | 1× T4 16GB | 1× T4 16GB |
| 7-8B | 2× A100 80GB | 1× A100 40GB | 1× T4 16GB |
| 13B | 4× A100 80GB | 1× A100 80GB | 1× A100 40GB |
| 70B | 8× A100 80GB | 4× A100 80GB | 1× A100 80GB |

## When to Use Which Provider

| Provider | Best For | Pricing Model | GPU Access |
|----------|----------|---------------|------------|
| Google Colab (free/Pro) | Learning, small experiments | Free / $10-50/mo | T4 (free), A100 (Pro) |
| Lambda Labs | Dedicated GPU instances | $1.10/hr (A100) | On-demand, reserved |
| RunPod | Short training runs, flexible | $0.74/hr (A100 40GB) | Spot + on-demand |
| Vast.ai | Cheapest spot instances | $0.50-1.00/hr (A100) | Spot (may preempt) |
| AWS SageMaker | Enterprise, managed training | $3-5/hr (ml.p4d) | On-demand, spot |
| Modal | Serverless GPU, pay per second | $2.78/hr (A100 80GB) | Auto-scale |
| Hugging Face Spaces | Quick experiments (limited) | Free (T4) or $5-9/hr (A100) | Managed |

## Implementation Walkthrough

### Option 1: Google Colab (Learning/Prototyping)

```python
# Free tier: T4 16GB — enough for QLoRA on 8B models
# Pro tier ($10/mo): A100 40GB — LoRA on 8B, QLoRA on 13B

# Check available GPU
!nvidia-smi
# Install dependencies
!pip install transformers peft trl datasets bitsandbytes accelerate

# Training code runs exactly the same as local
# Limitation: session timeout (disconnect after idle/12hr max)
# Strategy: save checkpoints frequently to Google Drive
```

### Option 2: RunPod/Lambda Labs (Recommended for Serious Training)

```bash
# 1. Launch instance (RunPod example)
# Select: A100 80GB, PyTorch template, $3.50/hr

# 2. SSH in and set up environment
pip install transformers peft trl datasets bitsandbytes accelerate wandb

# 3. Upload data
rsync -avz ./training_data.jsonl runpod:/workspace/data/

# 4. Run training (use screen/tmux to persist)
screen -S training
python train.py --config config.yaml

# 5. Download results
rsync -avz runpod:/workspace/output/ ./results/

# 6. STOP THE INSTANCE (critical — billing continues otherwise!)
```

### Option 3: Modal (Serverless — Pay Per Second)

```python
import modal

app = modal.App("fine-tune")

image = modal.Image.debian_slim().pip_install(
    "transformers", "peft", "trl", "datasets", "bitsandbytes", "accelerate"
)

@app.function(gpu="A100", timeout=3600, image=image)
def train(config: dict):
    """Serverless training — pays only while running."""
    from trl import SFTTrainer, SFTConfig
    from peft import LoraConfig
    
    # Training code here...
    trainer.train()
    trainer.save_model("/results/adapter")
    
    return "/results/adapter"

# Run from local machine:
# modal run train.py
# Auto-provisions GPU, runs training, shuts down when done
```

### Option 4: Hugging Face AutoTrain (Zero-Code)

```python
# For those who want UI-based fine-tuning
# https://huggingface.co/autotrain
# Upload dataset → Select model → Configure → Train
# Handles infrastructure automatically
# Cost: $5-50 per run depending on model/data size
```

### Distributed Training (Multi-GPU)

```python
# For models too large for single GPU (full SFT on 13B+)
from accelerate import Accelerator

accelerator = Accelerator()  # Auto-detects multi-GPU

# In training script, wrap model and optimizer:
model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

# Launch with:
# accelerate launch --num_processes 4 train.py
# Automatically distributes across 4 GPUs
```

## Configuration & Hyperparameters

| Setting | Recommendation | Why |
|---------|---------------|-----|
| GPU type for LoRA 8B | A100 40GB or T4 (QLoRA) | Fits comfortably with room for batching |
| Spot vs on-demand | Spot for training (save 50-70%) | Training can checkpoint/resume |
| Checkpoint frequency | Every 100 steps | Can resume if instance preempted |
| Experiment tracking | Weights & Biases (free tier) | Track loss curves, compare runs |
| Training time estimate | (dataset_tokens × epochs) / (batch_size × tokens_per_second) | Plan before launching |
| Auto-shutdown | ALWAYS set up | Forgetting = $50-200 overnight bill |

### Estimating Training Time

```python
def estimate_training_time(
    num_examples: int,
    avg_tokens_per_example: int,
    epochs: int,
    batch_size: int,
    tokens_per_second: int = 5000,  # Rough: A100 with LoRA 8B
) -> dict:
    total_tokens = num_examples * avg_tokens_per_example * epochs
    total_seconds = total_tokens / (batch_size * tokens_per_second)
    total_hours = total_seconds / 3600
    
    return {
        "total_tokens": total_tokens,
        "estimated_hours": round(total_hours, 1),
        "estimated_cost_a100": round(total_hours * 3.50, 2),
        "estimated_cost_t4": round(total_hours * 0.75, 2),
    }

# Example:
estimate_training_time(1000, 500, 3, 4)
# → {"total_tokens": 1.5M, "estimated_hours": 0.8, "cost_a100": $2.80}
```

## What Can Go Wrong

| Problem | Symptom | Fix |
|---------|---------|-----|
| OOM (Out of Memory) | CUDA OOM error immediately or mid-training | Reduce batch size, enable gradient checkpointing, use QLoRA |
| Instance preempted (spot) | Training stops mid-run | Save checkpoints every 100 steps, resume from last |
| Forgot to stop instance | $50-200 unexpected bill | Set up auto-shutdown after training completes |
| Slow training (unexpectedly) | Hours when expected minutes | Check: bf16 enabled? Batch size too small? DataLoader bottleneck? |
| Data loading bottleneck | GPU utilization < 50% | Pre-tokenize dataset, use streaming, more DataLoader workers |
| Driver/CUDA mismatch | Errors on GPU operations | Use provider's pre-built PyTorch images |

## Cost & Resource Planning

### Budget Templates

| Project | Setup | Training Time | Total Cost |
|---------|-------|--------------|------------|
| Learning experiment | T4 (Colab free) | 2-4 hrs | $0 |
| Serious LoRA 8B | A100 40GB (RunPod) | 3-6 hrs | $10-20 |
| Production LoRA 8B | A100 80GB × 3 runs | 3-6 hrs × 3 | $30-60 |
| LoRA 70B | A100 80GB | 8-24 hrs | $30-85 |
| Full SFT 8B | 2× A100 80GB | 8-24 hrs | $50-170 |

### Cost Optimization Tips

1. **Use spot instances** — 50-70% cheaper, training can resume from checkpoints
2. **Start small** — Train for 100 steps first to validate setup before full run
3. **Use QLoRA** — Fits on cheaper GPUs with minimal quality loss
4. **Pre-tokenize data** — Don't waste GPU time on tokenization
5. **Set auto-shutdown** — Script that stops instance when training completes

```bash
# Auto-shutdown after training (add to end of train script)
python train.py && sudo shutdown -h now
```

## Evaluation

| Check | How | Pass |
|-------|-----|------|
| GPU utilization | nvidia-smi during training | > 80% (not bottlenecked) |
| Memory usage | nvidia-smi | < 90% of VRAM (room for spikes) |
| Training speed | tokens/second or samples/second | Matches estimate (±20%) |
| Checkpoint saves | Files appearing on disk | Every N steps as configured |
| Cost tracking | Provider dashboard | Within budget estimate |

## Decision Checkpoint

- [ ] I know what GPU I need for my model + method (LoRA vs full) combination
- [ ] I have an account on a cloud GPU provider (Colab Pro / RunPod / Lambda)
- [ ] I've estimated training time and cost before launching
- [ ] I have auto-shutdown or billing alerts configured
- [ ] I'm using spot instances for training (with checkpointing)
- [ ] I've verified my code works on a small subset (100 steps) before full training
- [ ] I have experiment tracking set up (W&B or similar)
