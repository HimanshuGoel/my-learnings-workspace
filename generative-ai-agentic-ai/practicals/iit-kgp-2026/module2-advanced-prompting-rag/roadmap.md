# Module 2 — Advanced Prompting & RAG: Roadmap

## Module Overview

**Timeline:** Jul 25 – Sep 5, 2026 (6 weeks, ~7 sessions)
**Proctored Test 1:** September 5, 2026
**Prerequisite:** GenAI Fundamentals (Module 1) completed — conceptual understanding of RAG, prompting, agents, embeddings

## Topic Sequence & Timeline

| # | Topic | Target Week | Session Date | Dependencies | Priority |
|---|-------|-------------|--------------|--------------|----------|
| 1 | Advanced Prompting | Week 1 | Jul 25 | Module 1: prompting.md | HIGH |
| 2 | Chunking Strategies | Week 1-2 | Jul 25-Aug 1 | Module 1: rag.md | HIGH |
| 3 | Embedding Selection | Week 2 | Aug 1 | Module 1: embeddings.md | HIGH |
| 4 | Vector Store Design | Week 2-3 | Aug 1-Aug 8 | Topic 3 (embeddings) | HIGH |
| 5 | Retrieval Quality | Week 3 | Aug 8 | Topics 2, 3, 4 | HIGH |
| 6 | RAG Pipeline Architecture | Week 3-4 | Aug 8-Aug 15 | Topics 1-5 | HIGH |
| 7 | RAG Evaluation | Week 4 | Aug 15* | Topic 6 (pipeline) | HIGH |
| 8 | Production RAG | Week 5 | Aug 22 | Topics 6, 7 | MEDIUM |
| 9 | Structured Output | Week 5 | Aug 22 | Topic 1 (prompting) | MEDIUM |
| 10 | Agentic RAG | Week 6 | Aug 29 | Topics 5, 6, 9 | HIGH |

*Aug 15 session (Dense Retrieval) may be rescheduled — Indian Independence Day.

## Revision Week

**Aug 29 – Sep 5:** Dedicated revision for Proctored Test 1
- Review all 10 playbooks (focus on decision tables and failure modes)
- Run through "Ready to Ship?" checklists
- Practice hands-on: build a mini RAG pipeline end-to-end
- Review configuration checklist tables for quick recall

## Learning Flow

```
Advanced Prompting ──┐
                     │
Chunking ────────────┤
                     ├──→ Retrieval Quality ──→ RAG Pipeline ──→ RAG Evaluation ──→ Production RAG
Embedding Selection ─┤                                              │
                     │                                              │
Vector Store Design ─┘                                              ▼
                                                               Agentic RAG
Advanced Prompting ──────────────────────────────→ Structured Output ─┘
```

## Key Engineering Questions Per Topic

| Topic | Core Question |
|-------|--------------|
| Advanced Prompting | "How do I systematically design prompts that work reliably?" |
| Chunking Strategies | "How should I split my documents for optimal retrieval?" |
| Embedding Selection | "Which embedding model should I use and why?" |
| Vector Store Design | "How do I structure my vector DB for my use case?" |
| Retrieval Quality | "How do I ensure the right documents come back?" |
| RAG Pipeline Architecture | "How do all the pieces fit together end-to-end?" |
| RAG Evaluation | "How do I know my RAG system is actually working?" |
| Production RAG | "What breaks when I go from notebook to production?" |
| Structured Output | "How do I get reliable, parseable output from LLMs?" |
| Agentic RAG | "When do I need multi-step retrieval and routing?" |

## Success Criteria for Module 2

- [ ] Can design a RAG pipeline from scratch with justified component choices
- [ ] Can diagnose common RAG failures (bad retrieval, hallucination, latency)
- [ ] Can evaluate RAG quality using RAGAS and custom metrics
- [ ] Can make informed trade-offs (cost vs quality vs latency)
- [ ] Can articulate when simple RAG is enough vs when agentic RAG is needed
- [ ] Ready for Proctored Test 1 (Sep 5)

## Connection to Later Modules

- **Module 3 (Fine-Tuning):** When RAG alone isn't enough — fine-tune for format/style
- **Module 4 (Agentic AI):** Build on agentic-rag topic — full agent architectures
- **Module 5 (Deployment):** Production RAG topic feeds directly into FastAPI deployment
- **Capstone:** Will likely combine RAG + agents + deployment
