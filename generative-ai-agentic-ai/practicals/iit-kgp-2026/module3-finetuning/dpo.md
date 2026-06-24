# DPO (Direct Preference Optimization)

## The Problem This Solves

RLHF works but is complex — you need to train a separate reward model, run PPO with unstable training dynamics, and manage three models simultaneously. DPO achieves the same goal (align model with human preferences) by reformulating the problem as a simple supervised loss. No reward model, no RL loop, just a modified training objective on preference pairs. Same results, 10× simpler.

## How It Works — Conceptual Model

### The Key Insight

The RLHF reward function can be expressed implicitly through the model's own probabilities. Instead of:
1. Train reward model → 2. Run PPO to maximize reward

DPO does:
1. Directly train the model to make preferred responses more probable and rejected responses less probable

**Software analogy:** RLHF is like hiring a separate quality reviewer (reward model) and then having the agent practice until the reviewer is happy (PPO loop). DPO skips the reviewer — instead, you directly show the agent pairs of "good response vs bad response" and train it to produce the good one. Same learning outcome, fewer moving parts.

### The DPO Loss Function (Intuition)

```
For each training example:
- Prompt: "Explain machine learning"
- Chosen (preferred): "Machine learning is a subset of AI where..."
- Rejected (dispreferred): "ML is basically when computers learn stuff..."

DPO loss pushes the model to:
- INCREASE probability of generating the chosen response
- DECREASE probability of generating the rejected response
- CONSTRAINED by: don't change too much from the reference model (β parameter)

Loss = -log(σ(β × (log_prob_chosen - log_prob_rejected)))

Where β controls how much the model can deviate from its starting point
(same role as KL penalty in RLHF, but built into the loss function)
```

### DPO vs RLHF — Side by Side

| Aspect | RLHF | DPO |
|--------|------|-----|
| Components needed | SFT model + Reward model + PPO trainer | SFT model only |
| Training stages | 3 (SFT → RM → PPO) | 2 (SFT → DPO) |
| Stability | Unstable (RL training dynamics) | Stable (supervised learning) |
| Memory | 2-3 models in memory simultaneously | 2 models (policy + reference) |
| Hyperparameter sensitivity | Very sensitive (KL coef, PPO epochs, etc.) | Few hyperparams (β, LR) |
| Data needed | 10K+ preference pairs + prompts for PPO | 1K+ preference pairs |
| Quality | Gold standard (proven at scale) | Comparable (sometimes better) |
| Cost | $5K-20K+ (human labels + compute) | $50-500 (compute only) |
| Practical for solo dev? | No | Yes |

## When to Use vs Alternatives

| Situation | Recommendation |
|-----------|---------------|
| Want alignment without reward model complexity | DPO (this topic) |
| Have limited preference data (< 5K pairs) | DPO (works with less data) |
| Need absolute best alignment at scale | RLHF (more proven for large models) |
| Want a model to prefer certain response styles | DPO (natural fit) |
| Safety alignment | DPO or Constitutional AI |
| Only have gold examples (no preference pairs) | SFT only (can't do DPO without pairs) |
| Budget < $500 for alignment | DPO (only feasible option) |

## Implementation Walkthrough

### Step 1: Prepare Preference Dataset

```python
# DPO needs: (prompt, chosen_response, rejected_response) triplets
# Source options:
# 1. Human annotators compare model outputs
# 2. Use GPT-4o to judge which response is better  
# 3. Use existing preference datasets (UltraFeedback, HH-RLHF)

# Dataset format:
preference_data = {
    "prompt": "How do I handle errors in Python?",
    "chosen": "Use try/except blocks to catch specific exceptions. For example:\n```python\ntry:\n    result = int(input())\nexcept ValueError:\n    print('Please enter a number')\n```\nAlways catch specific exceptions rather than bare `except:`.",
    "rejected": "You can use try except. Just put your code in try and catch errors in except. It's pretty easy actually, just google it for more details.",
}

# Why "chosen" is better: specific, has code example, gives best practice advice
# Why "rejected" is worse: vague, dismissive, no concrete help
```

### Step 2: Generate Preference Pairs (If You Don't Have Them)

```python
from openai import OpenAI

client = OpenAI()

def generate_preference_pair(prompt: str, sft_model) -> dict:
    """Generate two responses and use GPT-4o to judge which is better."""
    
    # Generate two diverse responses from your SFT model
    response_a = sft_model.generate(prompt, temperature=0.7)
    response_b = sft_model.generate(prompt, temperature=0.9)
    
    # Use GPT-4o as judge
    judgment = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"""Compare these two responses to the prompt.
            
Prompt: {prompt}

Response A: {response_a}

Response B: {response_b}

Which is better? Consider: accuracy, helpfulness, clarity, safety.
Reply with JSON: {{"winner": "A" or "B", "reason": "..."}}"""
        }],
        temperature=0,
    )
    
    result = json.loads(judgment.choices[0].message.content)
    
    if result["winner"] == "A":
        return {"prompt": prompt, "chosen": response_a, "rejected": response_b}
    else:
        return {"prompt": prompt, "chosen": response_b, "rejected": response_a}
```

### Step 3: DPO Training with TRL

```python
from trl import DPOTrainer, DPOConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig
from datasets import load_dataset

# Load SFT model (your starting point)
model = AutoModelForCausalLM.from_pretrained(
    "./sft-model",  # or "meta-llama/Llama-3-8B-Instruct"
    torch_dtype=torch.bfloat16,
)
tokenizer = AutoTokenizer.from_pretrained("./sft-model")

# Reference model (frozen copy of the SFT model — DPO needs this)
ref_model = AutoModelForCausalLM.from_pretrained(
    "./sft-model",
    torch_dtype=torch.bfloat16,
)

# Optional: Use LoRA for memory efficiency
peft_config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules="all-linear",
)

# DPO training config
dpo_config = DPOConfig(
    output_dir="./dpo-output",
    num_train_epochs=1,              # DPO typically needs only 1-2 epochs
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=5e-7,              # Very low LR for DPO
    beta=0.1,                        # KL constraint strength
    max_length=1024,
    max_prompt_length=512,
    bf16=True,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=50,
)

# Load preference dataset
dataset = load_dataset("json", data_files="preferences.jsonl")

# Train
trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=dpo_config,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    tokenizer=tokenizer,
    peft_config=peft_config,  # Optional: LoRA for efficiency
)
trainer.train()
trainer.save_model("./dpo-adapter")
```

### Step 4: DPO Without Reference Model (Memory Efficient)

```python
# If you can't fit two models in memory, use implicit reference:
dpo_config = DPOConfig(
    ...
    ref_model=None,  # DPO will use the model's initial weights as reference
    # This works because LoRA keeps the base frozen (it IS the reference)
)

# With LoRA, the base model IS the reference model
# Only the LoRA weights change → natural KL constraint
# This is the recommended approach for most practitioners
```

## Dataset Requirements

| Aspect | Minimum | Recommended | Notes |
|--------|---------|-------------|-------|
| Preference pairs | 500 | 2000-5000 | More diversity = better generalization |
| Quality of judgments | Consistent annotators | Expert or GPT-4o judged | Noisy labels = noisy alignment |
| Prompt diversity | Cover all use cases | 80%+ unique prompts | Prevents overfitting to prompt styles |
| Chosen/rejected gap | Clear difference | Obviously better response | Subtle differences are hard to learn |
| Format | {"prompt", "chosen", "rejected"} | Consistent | Standard for TRL DPOTrainer |

### Existing Preference Datasets (For Learning/Baseline)

| Dataset | Size | Source | Use For |
|---------|------|--------|---------|
| HH-RLHF (Anthropic) | 170K pairs | Human annotators | General helpfulness + harmlessness |
| UltraFeedback | 64K pairs | GPT-4 judged | Instruction following quality |
| Nectar | 182K pairs | Multi-model ranked | Diverse preference signal |
| Orca DPO Pairs | 12K pairs | GPT-4 judged | Reasoning quality |

## Configuration & Hyperparameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| Beta (β) | 0.1 | 0.05-0.5 | Constraint strength. Lower = more change, higher = conservative |
| Learning rate | 5e-7 | 1e-7 to 5e-6 | Much lower than SFT! DPO is sensitive to LR |
| Epochs | 1 | 1-3 | DPO converges fast. More epochs = overfitting risk |
| Max length | 1024 | 512-2048 | Must fit chosen + rejected + prompt |
| Batch size | 2-4 per device | 2-8 | Small batches + grad accumulation |
| LoRA rank | 16 | 8-64 | Same guidance as SFT LoRA |
| Loss type | "sigmoid" | "sigmoid", "hinge", "ipo" | Sigmoid is standard DPO |

### Critical: β (Beta) Tuning

```
β = 0.05: Model changes a lot from reference (aggressive alignment)
β = 0.1:  Standard — good default for most cases
β = 0.2:  Conservative — small changes from reference
β = 0.5:  Very conservative — barely changes

If model degrades general capabilities → increase β
If alignment is too weak → decrease β
```

## What Can Go Wrong

| Problem | Symptom | Fix |
|---------|---------|-----|
| LR too high | Loss spikes, model degrades catastrophically | Reduce LR by 5-10× (DPO needs very low LR) |
| β too low | Model forgets general capabilities | Increase β (more conservative) |
| β too high | No visible alignment improvement | Decrease β (allow more change) |
| Noisy preference labels | Model learns inconsistent preferences | Clean data, use stronger judge (GPT-4o) |
| Chosen/rejected too similar | Model can't distinguish preference signal | Use examples with clear quality gaps |
| Overfitting (>1 epoch) | Perfect on train, bad on new prompts | Stop at 1 epoch, more diverse data |
| Length bias | Model learns to prefer longer (or shorter) responses | Ensure chosen/rejected are similar length |

## Cost & Resource Planning

| Setup | Resource | Cost | Time |
|-------|----------|------|------|
| DPO with LoRA on 8B | 1× A100 40GB | $7-20 | 2-6 hrs |
| DPO with LoRA on 70B | 1× A100 80GB (QLoRA) | $20-60 | 6-18 hrs |
| Preference data generation (GPT-4o, 2K pairs) | API calls | $20-50 | 2-4 hrs |
| **Total DPO project** | — | **$30-100** | **1-2 days** |

**Compare to RLHF: $5K-20K+ → DPO is 50-200× cheaper for similar results.**

## Evaluation

| What to Check | How | Target |
|---------------|-----|--------|
| Chosen vs rejected accuracy | DPO model rates chosen higher than rejected on held-out set | > 70% |
| Win rate vs SFT | Blind comparison: DPO output vs SFT output | > 55% (DPO should win) |
| General capability | Benchmark scores (MMLU, etc.) | No regression > 2% |
| Specific alignment goals | Test for the specific behavior you wanted | Measurable improvement |
| Safety (if relevant) | Red-team prompts | Fewer harmful outputs than SFT |
| Human preference | Side-by-side evaluation (10-20 examples) | Prefer DPO output |

## Decision Checkpoint

- [ ] I have 500+ preference pairs (or can generate them with GPT-4o)
- [ ] My preference pairs have clear quality differences (not subtle)
- [ ] I understand β controls how much the model can change
- [ ] I know DPO learning rate should be very low (5e-7 range)
- [ ] I'm using LoRA + DPO for memory efficiency (reference model is base)
- [ ] I have a clear evaluation plan before training
- [ ] I'll start with 1 epoch and check if it's enough before adding more
