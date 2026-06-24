# GenAI & LLM Fundamentals — Roadmap

## Purpose

Conceptual understanding of how LLMs work — from tokenization to deployment. This is the theory behind the Python libraries you've already practiced.

## Topics (Learning Order)

| # | Topic | File | Key Question | Priority | Module |
|---|-------|------|-------------|----------|--------|
| 1 | Why LLMs Exist | why-llms-exist.md | Why can't sklearn/rules solve NLP? | Highest | M1 |
| 2 | Tokenization | tokenization.md | How does text become numbers? | Highest | M1 |
| 3 | Embeddings | embeddings.md | How do numbers carry meaning? | Highest | M1, M2 |
| 4 | Attention | attention.md | How does the model focus? | Highest | M1 |
| 5 | Transformer Architecture | transformer-architecture.md | How do all pieces fit together? | Highest | M1 |
| 6 | Pre-training | pretraining.md | How does the model learn initially? | High | M1, M3 |
| 7 | Prompting | prompting.md | How do we instruct the model? | Highest | M1, M2 |
| 8 | Decoding | decoding.md | How does the model choose words? | High | M1 |
| 9 | Fine-tuning | fine-tuning.md | How do we adapt it to our task? | Highest | M3 |
| 10 | RAG | rag.md | How do we ground it in our data? | Highest | M2 |
| 11 | Agents | agents.md | How does it use tools and reason? | High | M4 |
| 12 | Evaluation | evaluation.md | How do we measure quality? | High | M2, M5 |

---

## How This Connects to What You've Done

```
Mathematics (foundation)
    ↓ vectors, matrices, probability, calculus
Python Libraries (tools)
    ↓ NumPy, PyTorch, Transformers, LangChain...
GenAI Fundamentals (theory) ← YOU ARE HERE
    ↓ understanding WHY those tools do what they do
IIT KGP Modules (application)
    ↓ assignments, projects, capstone
```

---

## Prerequisite Chain

```
why-llms-exist
    ↓
tokenization → embeddings → attention → transformer-architecture
                                              ↓
                              pretraining → fine-tuning
                                              ↓
                    prompting → decoding → rag → agents → evaluation
```

---

## Aligned to IIT KGP Program

| Module | Topics You Need |
|--------|----------------|
| Module 1: GenAI Foundations | Topics 1-8 (all fundamentals) |
| Module 2: RAG & Prompting | Topics 7, 10, 12 |
| Module 3: Fine-tuning | Topics 6, 9 |
| Module 4: Agents | Topic 11 |
| Module 5: Deployment | Topics 10, 12 (evaluation for capstone) |

---

## Format Per Topic

Each topic gets:
- `<topic>.md` — detailed concept notes (reading material)
- `<topic>_PRINTABLE.html` — rich printable with SVG diagrams (for paper study)

No code files here — code is in the `python/` folder. This is purely conceptual understanding.

---

## Time Estimate

| Depth | Time per Topic | Total |
|-------|---------------|-------|
| Read notes | 15-20 min | ~4 hours |
| Read + printable study | 30-40 min | ~7 hours |
| Deep understanding (+ revisit math/code) | 60 min | ~12 hours |

Recommended: one topic per day, with the printable for paper reading in the evening.
