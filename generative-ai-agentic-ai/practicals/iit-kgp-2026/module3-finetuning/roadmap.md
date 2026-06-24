# Module 3 — Fine-Tuning & Alignment: Roadmap

## Module Overview

**Timeline:** Sep 12 – Oct 31, 2026 (7 weeks, ~8 sessions)
**Proctored Test 2:** December 26, 2026 (covers Module 3 + Module 4)
**Prerequisite:** Module 2 completed — you can build, evaluate, and ship a RAG pipeline

## The Big Question This Module Answers

"When is prompting + RAG not enough, and how do I customize model behavior at a deeper level — without wasting GPU hours on unnecessary fine-tuning?"

## Topic Sequence & Timeline

| # | Topic | Target Week | Session Date | Dependencies | Priority |
|---|-------|-------------|--------------|--------------|----------|
| 1 | When to Fine-Tune | Week 1 | Sep 12 | Module 2 complete | CRITICAL |
| 2 | Full Fine-Tuning (SFT) | Week 1-2 | Sep 12-19 | Topic 1 | HIGH |
| 3 | PEFT & LoRA | Week 2 | Sep 19 | Topic 2 | HIGH |
| 4 | Dataset Preparation | Week 2-3 | Sep 19-26 | Topics 1-3 | CRITICAL |
| 5 | Training Infrastructure | Week 3 | Sep 26 | Topic 3 | MEDIUM |
| 6 | RLHF | Week 4 | Oct 3 | Topics 2, 4 | HIGH |
| 7 | DPO | Week 4-5 | Oct 3-10 | Topic 6 | HIGH |
| 8 | Evaluation of Fine-Tuned Models | Week 5 | Oct 10 | Topics 2-7 | HIGH |
| 9 | Merging & Serving | Week 6 | Oct 17 | Topics 3, 8 | MEDIUM |
| 10 | Alignment & Safety | Week 7 | Oct 24-31 | Topics 6-8 | HIGH |

## Learning Flow

```text
When to Fine-Tune (decision framework — gates everything else)
        │
        ├──→ Full Fine-Tuning (SFT) ──→ PEFT & LoRA ──→ Training Infrastructure
        │                                      │
        │                                      ▼
        └──→ Dataset Preparation ────────→ RLHF ──→ DPO
                                              │
                                              ▼
                                    Evaluation ──→ Merging & Serving
                                              │
                                              ▼
                                    Alignment & Safety
```

## Key Decision Questions Per Topic

| Topic | Core Question |
|-------|--------------|
| When to Fine-Tune | "Is fine-tuning the right tool, or am I over-engineering?" |
| Full Fine-Tuning | "How does supervised fine-tuning actually modify the model?" |
| PEFT & LoRA | "How do I get 90% of full fine-tuning at 10% of the cost?" |
| Dataset Preparation | "What data do I need, how much, and how do I prepare it?" |
| Training Infrastructure | "What hardware, how long, and what will it cost me?" |
| RLHF | "How do I align a model with human preferences at scale?" |
| DPO | "Can I skip the reward model and still get alignment?" |
| Evaluation | "How do I know my fine-tuned model is actually better?" |
| Merging & Serving | "How do I deploy the fine-tuned model efficiently?" |
| Alignment & Safety | "How do I prevent my fine-tuned model from being harmful?" |

## Module 3 vs Module 2 Approach

| Aspect | Module 2 (RAG) | Module 3 (Fine-Tuning) |
|--------|----------------|------------------------|
| Iteration speed | Minutes (API calls) | Hours/days (training runs) |
| Cost per experiment | $0.01-0.10 | $1-100+ (GPU hours) |
| Primary skill | Configuration & wiring | Experimentation & evaluation |
| Success metric | Retrieval + faithfulness | Task performance vs baseline |
| Most common mistake | Over-engineering retrieval | Fine-tuning when prompting suffices |
| Key artifact | Pipeline code | Trained model weights + eval report |

## Success Criteria for Module 3

- [ ] Can articulate WHEN to fine-tune vs use RAG/prompting (with confidence)
- [ ] Understand LoRA intuitively (what it does, why it's efficient, when it fails)
- [ ] Can prepare a fine-tuning dataset from raw data (format, filter, validate)
- [ ] Understand RLHF pipeline conceptually (reward model → policy optimization)
- [ ] Can explain DPO as a simpler alternative to RLHF (trade-offs)
- [ ] Can evaluate whether fine-tuning improved things (not just train loss)
- [ ] Can estimate cost and time for a fine-tuning project
- [ ] Ready for Proctored Test 2 (Dec 26, with Module 4)

## Connection to Other Modules

- **Module 2 (RAG):** "When RAG alone isn't enough" — fine-tuning for format/style/domain
- **Module 4 (Agentic AI):** Fine-tuned models as specialized agent components
- **Module 5 (Deployment):** Serving fine-tuned models via FastAPI, quantization for efficiency
- **Capstone:** May involve fine-tuning a domain-specific model for your project

## Key Scheduling Notes

- 2-week gap between Module 3 end (Oct 31) and Module 4 start (Nov 14) — use for capstone ideation
- Proctored Test 2 covers BOTH Module 3 + 4 on Dec 26 — start revision early
- Oct 24-31 is the last week — use for alignment/safety + consolidation
