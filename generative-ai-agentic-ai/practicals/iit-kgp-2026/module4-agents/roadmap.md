# Module 4 — Multimodal & Agentic AI: Roadmap

## Module Overview

**Timeline:** Nov 14 – Dec 26, 2026 (6 weeks, ~6 sessions)
**Proctored Test 2:** December 26, 2026 (covers Module 3 + Module 4)
**Prerequisite:** Module 3 completed — you understand fine-tuning, alignment, and when to use what

## The Big Question This Module Answers

"How do I build AI systems that can SEE (multimodal), PLAN (reasoning), ACT (tools), and COORDINATE (multi-agent) — and how do I architect them to be reliable, observable, and deployable?"

## Topic Sequence & Timeline

| # | Topic | Target Week | Session Date | Dependencies | Priority |
|---|-------|-------------|--------------|--------------|----------|
| 1 | VLM Fundamentals | Week 1 | Nov 14 | Module 1: transformers | HIGH |
| 2 | Multimodal RAG | Week 1-2 | Nov 14-21 | Topic 1, Module 2: RAG | HIGH |
| 3 | Agent Architectures | Week 2 | Nov 21 | Module 1: agents.md | CRITICAL |
| 4 | LangGraph Fundamentals | Week 2-3 | Nov 21-28 | Topic 3 | CRITICAL |
| 5 | Tool Use Design | Week 3 | Nov 28 | Topic 4 | HIGH |
| 6 | Multi-Agent Systems | Week 4 | Dec 5 | Topics 3-5 | HIGH |
| 7 | Planning & Reasoning | Week 4 | Dec 5 | Topics 3, 4 | HIGH |
| 8 | Agent Memory | Week 5 | Dec 12 | Topics 4-7 | MEDIUM |
| 9 | Agent Evaluation | Week 5 | Dec 12 | Topics 3-8 | HIGH |
| 10 | Production Agents | Week 6 | Dec 19 | All above | HIGH |

**Note:** Only 1 week between last session (Dec 19) and Test 2 (Dec 26) — start revision early!

## Learning Flow

```text
VLM Fundamentals ──→ Multimodal RAG
                              │
Agent Architectures ──→ LangGraph Fundamentals ──→ Tool Use Design
         │                     │                        │
         │                     ▼                        ▼
         └────────────→ Planning & Reasoning ──→ Multi-Agent Systems
                              │                        │
                              ▼                        ▼
                        Agent Memory ──────→ Agent Evaluation
                                                      │
                                                      ▼
                                              Production Agents
```

## Two Halves of Module 4

### Part A: Multimodal (Weeks 1-2)
- How models see and understand images/documents
- Building RAG systems that handle PDFs with figures, tables, charts
- Multi-modal embeddings and retrieval

### Part B: Agentic AI (Weeks 3-6)
- Designing agents that plan, reason, and use tools
- State machines with LangGraph (the core framework)
- Multi-agent coordination patterns
- Memory, evaluation, and production deployment

## Key Architecture Questions Per Topic

| Topic | Core Question |
|-------|--------------|
| VLM Fundamentals | "How do models understand images alongside text?" |
| Multimodal RAG | "How do I build RAG that handles PDFs with figures and tables?" |
| Agent Architectures | "Which agent pattern fits my use case?" |
| LangGraph Fundamentals | "How do I build a stateful agent as a graph?" |
| Tool Use Design | "How do I design reliable tool interfaces for agents?" |
| Multi-Agent Systems | "When do I need multiple agents, and how do they coordinate?" |
| Planning & Reasoning | "How do I make agents decompose and solve complex tasks?" |
| Agent Memory | "How does an agent maintain context across conversations and sessions?" |
| Agent Evaluation | "How do I test something that behaves differently each time?" |
| Production Agents | "How do I deploy agents that are reliable, observable, and cost-effective?" |

## Success Criteria for Module 4

- [ ] Can explain how VLMs process images (CLIP, patch embeddings, cross-attention)
- [ ] Can build a multimodal RAG pipeline (PDF → chunks with figures → retrieval)
- [ ] Can choose the right agent architecture for a given problem
- [ ] Can implement a stateful agent with LangGraph (nodes, edges, state, checkpoints)
- [ ] Can design tool interfaces that agents use reliably
- [ ] Can articulate when multi-agent is needed vs single agent with multiple tools
- [ ] Can evaluate agent behavior (trajectory testing, not just output testing)
- [ ] Can deploy an agent with human-in-the-loop and observability
- [ ] Ready for Proctored Test 2 (Dec 26, with Module 3)

## Connection to Other Modules

- **Module 2 (RAG):** Multimodal RAG builds directly on Module 2's RAG pipeline
- **Module 3 (Fine-Tuning):** Fine-tuned models as specialized agent components
- **Module 5 (Deployment):** Production agents feeds directly into FastAPI/MCP deployment
- **Capstone:** Will almost certainly involve an agent system (RAG + tools + orchestration)

## Key Scheduling Notes

- 2-week gap between Module 3 end (Oct 31) and Module 4 start (Nov 14) — use for capstone ideation
- Only 1 week between last Module 4 session (Dec 19) and Test 2 (Dec 26) — START REVISION BY DEC 12
- Capstone feedback session is Jan 30 — agent system should be near-complete by then
- Module 4 is the most "build heavy" module — plan hands-on time for LangGraph experimentation
