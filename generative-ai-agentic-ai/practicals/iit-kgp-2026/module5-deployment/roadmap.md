# Module 5 — Deployment & Capstone: Roadmap

## Module Overview

**Timeline:** Jan 2 – Feb 6, 2027 (5 weeks, ~5 sessions)
**Capstone Feedback Session:** January 30, 2027
**Capstone Evaluation:** February 6, 2027
**Prerequisite:** Modules 1-4 completed — you have systems to deploy

## The Big Question This Module Answers

"How do I take my RAG pipeline, fine-tuned model, or agent system and ship it — reliably, securely, affordably — to real users?"

## Topic Sequence & Timeline

| # | Topic | Target Week | Session Date | Dependencies | Priority |
|---|-------|-------------|--------------|--------------|----------|
| 1 | FastAPI Serving | Week 1 | Jan 2 | Module 2-4 (systems to serve) | CRITICAL |
| 2 | MCP Protocol | Week 1 | Jan 2 | Topic 1 | HIGH |
| 3 | Containerization | Week 2 | Jan 9 | Topic 1 | HIGH |
| 4 | Streaming & UX | Week 2 | Jan 9 | Topics 1, 3 | HIGH |
| 5 | Authentication & Security | Week 3 | Jan 16 | Topics 1-3 | CRITICAL |
| 6 | Cost Monitoring | Week 3 | Jan 16 | Topics 1-4 | HIGH |
| 7 | Responsible AI | Week 3-4 | Jan 16-23 | All modules | HIGH |
| 8 | CI/CD for AI | Week 4 | Jan 23 | Topics 1-6 | MEDIUM |
| 9 | Observability | Week 4 | Jan 23 | Topics 1-6 | HIGH |
| 10 | Capstone Guide | Week 1-5 | Ongoing | All modules | CRITICAL |

## Learning Flow

```text
FastAPI Serving ──→ Containerization ──→ CI/CD for AI
       │                   │
       ├──→ MCP Protocol   ├──→ Authentication & Security
       │                   │
       └──→ Streaming & UX └──→ Cost Monitoring ──→ Observability
                                       │
                                       └──→ Responsible AI

Capstone Guide (parallel throughout — start Week 1, present Week 5)
```

## Key Deployment Questions Per Topic

| Topic | Core Question |
|-------|--------------|
| FastAPI Serving | "How do I expose my AI system as a production API?" |
| MCP Protocol | "How do I make my AI system interoperable with assistants/tools?" |
| Containerization | "How do I package AI services with model files and GPU support?" |
| Streaming & UX | "How do I make the UX feel fast despite 3-10s LLM processing?" |
| Auth & Security | "How do I prevent abuse, prompt injection, and data leaks?" |
| Cost Monitoring | "How do I track and control token spend in production?" |
| Responsible AI | "How do I ensure my system is fair, transparent, and safe?" |
| CI/CD for AI | "How do I test and deploy non-deterministic AI systems?" |
| Observability | "How do I know what's happening inside my AI system at runtime?" |
| Capstone Guide | "How do I scope, build, and present a complete AI project?" |

## What's FAMILIAR vs What's NEW

| Familiar (Your 14y Experience) | New (AI-Specific) |
|-------------------------------|-------------------|
| FastAPI routing, middleware | Streaming LLM tokens via SSE |
| Docker multi-stage builds | GPU passthrough, large model files |
| JWT auth, rate limiting | Prompt injection defense |
| Prometheus metrics | Token cost tracking per request |
| CI/CD pipelines | Testing non-deterministic outputs |
| Structured logging | LangSmith traces, agent trajectories |
| REST API design | MCP protocol for AI tool interop |
| Input validation | Content safety filtering |

## Success Criteria for Module 5

- [ ] Can deploy a RAG or agent system behind FastAPI with Docker
- [ ] Can implement streaming responses (SSE) with intermediate steps
- [ ] Understand MCP protocol and can expose tools via MCP server
- [ ] Have auth + rate limiting + prompt injection defense in place
- [ ] Can track and alert on token costs per user/endpoint
- [ ] Have CI/CD with eval-based quality gates for AI systems
- [ ] Have observability (tracing, dashboards) for production debugging
- [ ] Responsible AI: content filtering + bias testing + audit trail
- [ ] Capstone project scoped, built, and ready for presentation

## Capstone Timeline

| Week | Milestone |
|------|-----------|
| Week 1 (Jan 2) | Finalize capstone scope + architecture |
| Week 2 (Jan 9) | Core implementation (RAG/agent/fine-tuned model) |
| Week 3 (Jan 16) | API + deployment + security |
| Week 4 (Jan 23) | Testing + monitoring + documentation |
| Jan 30 | **Capstone Feedback Session** (near-complete) |
| Feb 6 | **Capstone Evaluation** (final) |

## Connection to Previous Modules

- **Module 1 (Fundamentals):** Debugging production issues requires understanding tokenization, decoding, context windows
- **Module 2 (RAG):** Most likely capstone component — deploy the pipeline you designed
- **Module 3 (Fine-Tuning):** Serve fine-tuned model via vLLM, handle model versioning
- **Module 4 (Agents):** Deploy agent with HITL, streaming steps, cost controls — the hardest deployment challenge

## Key Scheduling Notes

- Capstone feedback on Jan 30 — project must be 90% complete by then
- Only 1 week between feedback (Jan 30) and final evaluation (Feb 6) — use for polish only
- Start capstone implementation in Week 1, not Week 4 (common mistake)
- Module 5 topics are meant to be applied TO your capstone as you build it
