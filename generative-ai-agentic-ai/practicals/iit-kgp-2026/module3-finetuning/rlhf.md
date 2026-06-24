# RLHF (Reinforcement Learning from Human Feedback)

## The Problem This Solves

SFT teaches a model to imitate your examples, but imitation has limits — the model doesn't learn WHY one response is better than another. RLHF goes beyond "copy this output" to "learn what humans prefer" — making the model optimize for helpfulness, safety, and quality as judged by human preference signals. This is how ChatGPT went from a competent text predictor to an assistant that feels genuinely helpful.

## How It Works — Conceptual Model

### The Three-Stage Pipeline

```
Stage 1: Supervised Fine-Tuning (SFT)
    Base model → trained on (prompt, ideal response) pairs → SFT model
    Purpose: Teach the model the general task format and quality bar

Stage 2: Reward Model Training
    Collect: For each prompt, get 2+ model responses ranked by humans
    Train: A separate model that predicts "how good is this response?" (scalar score)
    Purpose: Encode human preferences into a numerical signal

Stage 3: RL Optimization (PPO)
    The SFT model generates responses
    The reward model scores them
    PPO updates the SFT model to maximize reward scores
    KL penalty prevents drifting too far from the SFT model (avoids "reward hacking")
```

### Software Analogy

Think of it like training a customer support agent:
- **SFT** = giving them a manual with example responses (they can copy the format)
- **Reward model** = hiring a quality reviewer who rates responses 1-10
- **PPO** = letting the agent practice freely while the reviewer gives continuous feedback

The agent eventually internalizes what "good" means, not just what specific responses to give.

### Why RLHF Works Better Than SFT Alone

| Aspect | SFT Only | SFT + RLHF |
|--------|----------|-------------|
| Learns from | Correct examples only | Preferences (this > that) |
| Quality ceiling | Average of your examples | Can exceed your examples |
| Safety | Can produce unsafe text if in training | Trained to avoid unsafe outputs |
| Helpfulness | Follows instructions | Actively tries to be maximally helpful |
| Failure mode | Copies style but may miss intent | Optimizes for user satisfaction |

### The Reward Model — How Preferences Become Scores

```
Human comparison data:
    Prompt: "Explain quantum computing"
    Response A: [long technical explanation]
    Response B: [concise analogy-based explanation]
    Human preference: B > A (for this context)

Reward model learns:
    Score(prompt, response_B) > Score(prompt, response_A)
    
After training thousands of such comparisons:
    The reward model can score ANY new response for quality
```

### PPO (Proximal Policy Optimization) — The RL Part

PPO is the algorithm that updates the model to generate higher-scoring responses:

```
For each training step:
1. Model generates a response to a prompt
2. Reward model scores the response (e.g., 7.2 / 10)
3. PPO calculates: "how should I adjust weights to get higher scores?"
4. BUT also: "don't change too much from the SFT model" (KL penalty)
5. Update model weights slightly toward higher-reward responses

The KL penalty is critical — without it, the model finds "reward hacks"
(outputs that score high on the reward model but are actually bad)
```

## When to Use vs Alternatives

| Method | When to Use | Complexity | Data Needed |
|--------|-------------|------------|-------------|
| SFT only | Format/style tasks, you have gold examples | Low | 100-1000 examples |
| RLHF | General helpfulness, safety alignment | Very High | 10K+ comparisons |
| DPO | Same goals as RLHF, simpler pipeline | Medium | 1K+ preference pairs |
| RLAIF (AI feedback) | Can't collect human feedback at scale | High | Auto-generated |
| Constitutional AI | Safety alignment without human labelers | High | Rules + AI evaluation |

**Recommendation for most practitioners:** Skip RLHF, use DPO (next topic). RLHF requires massive infrastructure and data. DPO achieves similar results with much less complexity. Understand RLHF conceptually (it's what the big labs do), but implement DPO in practice.

## Implementation Walkthrough

### Stage 1: SFT (Already Covered — Topic 2/3)

```python
# Use your SFT model from Topics 2-3 as the starting point
sft_model_path = "./sft-model"
```

### Stage 2: Reward Model Training

```python
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load a model to be your reward model (often same architecture, smaller)
reward_model = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3-8B-Instruct",
    num_labels=1,  # Single scalar output (reward score)
)

# Prepare preference dataset
# Format: {"prompt": "...", "chosen": "better response", "rejected": "worse response"}
# Each example is a pair where chosen > rejected according to human annotators

reward_config = RewardConfig(
    output_dir="./reward-model",
    num_train_epochs=1,
    per_device_train_batch_size=4,
    learning_rate=1e-5,
)

reward_trainer = RewardTrainer(
    model=reward_model,
    args=reward_config,
    train_dataset=preference_dataset["train"],
    eval_dataset=preference_dataset["validation"],
)
reward_trainer.train()
```

### Stage 3: PPO Training

```python
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

# Load SFT model with value head (for PPO)
model = AutoModelForCausalLMWithValueHead.from_pretrained(sft_model_path)

# PPO config
ppo_config = PPOConfig(
    learning_rate=1e-5,
    batch_size=16,
    mini_batch_size=4,
    gradient_accumulation_steps=4,
    ppo_epochs=4,
    kl_penalty="kl",          # KL divergence penalty
    init_kl_coef=0.2,         # How much to penalize divergence from SFT
    target_kl=6.0,            # Target KL divergence
)

ppo_trainer = PPOTrainer(
    model=model,
    config=ppo_config,
    tokenizer=tokenizer,
    dataset=prompt_dataset,
)

# Training loop
for batch in ppo_trainer.dataloader:
    # 1. Generate responses
    responses = ppo_trainer.generate(batch["input_ids"])
    
    # 2. Score with reward model
    rewards = reward_model(batch["input_ids"], responses)
    
    # 3. PPO update
    stats = ppo_trainer.step(batch["input_ids"], responses, rewards)
    
    # Monitor: reward should increase, KL should stay bounded
    print(f"Reward: {stats['ppo/mean_scores']:.2f}, KL: {stats['objective/kl']:.2f}")
```

## Dataset Requirements

| Stage | Data Type | Volume | Source |
|-------|-----------|--------|--------|
| SFT | (prompt, ideal response) | 1K-10K | Curated examples |
| Reward model | (prompt, chosen, rejected) | 10K-100K | Human annotators comparing pairs |
| PPO | Prompts only (model generates responses) | 10K-50K | Diverse prompts from your domain |

### Collecting Preference Data

```python
# Option 1: Human annotation (gold standard, expensive)
# Show annotators 2 responses, ask which is better

# Option 2: AI-assisted (use GPT-4o as judge)
def generate_preference_pair(prompt, model, judge_llm):
    response_a = model.generate(prompt, temperature=0.7)
    response_b = model.generate(prompt, temperature=0.9)
    
    judgment = judge_llm.invoke(
        f"Which response is better for this prompt?\n"
        f"Prompt: {prompt}\nA: {response_a}\nB: {response_b}\n"
        f"Reply with 'A' or 'B' and explain why."
    )
    
    if "A" in judgment:
        return {"prompt": prompt, "chosen": response_a, "rejected": response_b}
    else:
        return {"prompt": prompt, "chosen": response_b, "rejected": response_a}
```

## Configuration & Hyperparameters

| Parameter | Typical Value | Effect |
|-----------|--------------|--------|
| KL coefficient | 0.1-0.3 | Higher = less change from SFT (more conservative) |
| Target KL | 3-10 | Adaptive KL penalty target |
| PPO epochs | 2-4 | Number of PPO updates per batch |
| Reward model size | Same or smaller than policy | Larger reward model = better signal |
| Training steps | 1000-10000 | More = more aligned BUT risk of reward hacking |
| Batch size | 16-64 | Larger = more stable updates |
| Temperature (generation) | 0.7-1.0 | Diverse responses during training |

## What Can Go Wrong

| Problem | Symptom | Fix |
|---------|---------|-----|
| Reward hacking | Model finds exploits (repeats phrases that score high) | Increase KL penalty, improve reward model |
| Mode collapse | Model generates same response regardless of prompt | Reduce learning rate, increase KL penalty |
| Reward model inaccurate | PPO optimizes for wrong thing | More/better preference data, retrain reward model |
| Training instability | Reward oscillates wildly, doesn't converge | Reduce learning rate, smaller PPO epochs |
| Catastrophic forgetting | Model loses capabilities | Higher KL penalty, mix in SFT data |
| Too expensive | Can't afford 3 models + PPO loop | Use DPO instead (next topic) |

## Cost & Resource Planning

| Component | Resource | Cost |
|-----------|----------|------|
| SFT model training | 1× A100 for 4-8 hrs | $15-30 |
| Reward model training | 1× A100 for 2-4 hrs | $7-15 |
| PPO training | 2× A100 (policy + reward) for 12-48 hrs | $85-340 |
| Human annotations (10K pairs) | Contractors or Scale AI | $5,000-20,000 |
| **Total realistic RLHF project** | — | **$5,000-20,000+** |

**This is why most practitioners skip RLHF and use DPO.** The cost is justified only for production models serving millions of users.

## Evaluation

| What to Check | How | Target |
|---------------|-----|--------|
| Reward score improvement | Compare mean reward before/after PPO | Increasing over training |
| KL divergence | Monitor during training | Stays within target (not too high) |
| Win rate vs SFT | Human eval: RLHF output vs SFT output | > 60% prefer RLHF |
| Safety improvements | Red-team testing | Fewer harmful outputs |
| General capability | Benchmark scores (MMLU, etc.) | No significant regression |
| Reward hacking | Manual inspection of high-reward outputs | Outputs are genuinely good (not gamed) |

## Decision Checkpoint

- [ ] I understand the 3-stage pipeline (SFT → Reward Model → PPO)
- [ ] I understand WHY RLHF exists (preferences > imitation for alignment)
- [ ] I understand the KL penalty (prevents model from drifting too far from SFT)
- [ ] I understand reward hacking (and why it's the main failure mode)
- [ ] I recognize RLHF is overkill for my current needs (solo dev, learning)
- [ ] I'm ready to learn DPO as the practical alternative

**For most practitioners: understand RLHF conceptually, implement DPO practically.**
