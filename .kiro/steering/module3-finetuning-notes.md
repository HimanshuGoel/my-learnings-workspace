---
inclusion: fileMatch
fileMatchPattern: "**/module3-fine-tuning-alignment/**"
---

# Module 3 — Fine-Tuning & Alignment (Practitioner's Decision Guide)

## Context

Module 3 of the IIT KGP GenAI program (Sep 12 – Oct 31, 2026). Unlike Module 2 (assemble components, configure, wire), Module 3 is about understanding WHEN and HOW to modify model behavior at a deeper level. Fewer decisions, but each one is bigger and more expensive.

## Audience

- 14 years software dev (Java/.NET/Angular/Node.js)
- Completed: Mathematics, Python Libraries, GenAI Fundamentals, Module 2 (RAG engineering)
- Understands RAG, prompting, embeddings, vector stores, evaluation
- Now needs: When is RAG/prompting not enough? How do I customize model behavior? What are the trade-offs of fine-tuning?

## Key Difference from Module 2

| Module 2 (RAG) | Module 3 (Fine-Tuning) |
|----------------|------------------------|
| Assemble components | Modify model internals |
| Many small decisions | Fewer big decisions |
| Config-driven | Experiment-driven |
| Cheap to iterate (API calls) | Expensive to iterate (GPU hours) |
| "Which tool?" | "Should I even do this?" |
| Minutes to test | Hours/days to train |
| Implementation-heavy | Concept + decision-heavy |

## File Structure

```
module3-fine-tuning-alignment/
├── roadmap.md
├── when-to-fine-tune.md           ← Decision framework (most important topic)
├── when-to-fine-tune_PRINTABLE.html
├── full-fine-tuning.md            ← Traditional approach, SFT
├── full-fine-tuning_PRINTABLE.html
├── peft-lora.md                   ← LoRA, QLoRA, adapters
├── peft-lora_PRINTABLE.html
├── dataset-preparation.md         ← The make-or-break step
├── dataset-preparation_PRINTABLE.html
├── training-infrastructure.md     ← GPUs, cost, cloud options
├── training-infrastructure_PRINTABLE.html
├── rlhf.md                        ← Reward models, PPO
├── rlhf_PRINTABLE.html
├── dpo.md                         ← Simpler alignment alternative
├── dpo_PRINTABLE.html
├── evaluation-fine-tuned.md       ← Did it actually help?
├── evaluation-fine-tuned_PRINTABLE.html
├── merging-and-serving.md         ← Ship the fine-tuned model
├── merging-and-serving_PRINTABLE.html
└── alignment-safety.md            ← Guardrails, red-teaming
    alignment-safety_PRINTABLE.html
```

## Topic .md — Decision Guide Structure

Each topic follows this structure (adapted from Module 2's playbook):

1. **The Problem This Solves** (1-2 sentences)
2. **How It Works** (conceptual intuition — more depth than Module 2, because you can't debug what you don't understand)
3. **When to Use vs Alternatives** (decision framework — the key question)
4. **Implementation Walkthrough** (practical steps with HuggingFace/OpenAI)
5. **Dataset Requirements** (what data you need, how much, what format)
6. **Configuration & Hyperparameters** (what to set, ranges, defaults)
7. **What Can Go Wrong** (failure modes + debugging — more experimental than Module 2)
8. **Cost & Resource Planning** (GPU hours, cloud costs, time investment)
9. **Evaluation** (how to know it worked — benchmarks, comparison to baseline)
10. **Decision Checkpoint** ("Given what you now know, should you actually do this?")

## Topic _PRINTABLE.html — Visual Decision Guide

Same CSS as Module 2 printables. SVG diagrams focus on:

- Decision flowcharts ("RAG vs fine-tune vs prompt engineer")
- Architecture diagrams (LoRA adapter structure, RLHF pipeline)
- Before/after comparisons (base model vs fine-tuned behavior)
- Cost/benefit trade-off tables
- Training progression visuals
- At least 2-3 diagrams per topic

## Code Reference Stack

- Hugging Face transformers + PEFT + TRL (primary)
- OpenAI fine-tuning API (for comparison/simpler path)
- Weights & Biases (experiment tracking)
- bitsandbytes (quantization)
- datasets library (data loading)
- torch (training loops when needed)

## Tone

- More reflective than Module 2 — "here's the trade-off, here's what I'd recommend for YOUR context"
- Acknowledge that most fine-tuning is unnecessary for solo devs / learning projects
- Opinionated about when NOT to fine-tune (biggest value add of this module)
- Practical cost awareness throughout (GPU hours are real money)

## What NOT to Include

- Full training loop code for every variant (point to HuggingFace tutorials)
- Mathematical derivations (reference the math notes, give intuition instead)
- Exhaustive hyperparameter search results (give good defaults + ranges)
- Enterprise-scale distributed training details (beyond the scope for one person)
