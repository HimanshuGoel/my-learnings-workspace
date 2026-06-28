---
inclusion: fileMatch
fileMatchPattern: "**/module5-deployment/**"
---

# Module 5 — Deployment & Capstone (Deployment Runbook)

## Context

Module 5 of the IIT KGP GenAI program (Jan 2 – Feb 6, 2027). This is where everything converges — you take your RAG pipelines, fine-tuned models, and agent systems from Modules 2-4 and SHIP them. It's also the capstone preparation period. Unlike previous modules (build AI systems), Module 5 is about OPERATING AI systems — making them reliable, secure, observable, and cost-effective for real users.

## Audience

- 14 years software dev (Java/.NET/Angular/Node.js) — already knows Docker, APIs, CI/CD, monitoring
- Completed: All Modules 1-4 (fundamentals, RAG, fine-tuning, agents)
- What's NEW: AI-specific deployment concerns (model serving, token costs, streaming LLM responses, MCP protocol, responsible AI compliance, non-deterministic testing)
- What's FAMILIAR: FastAPI, Docker, monitoring patterns, security, CI/CD

## How All Modules Feed Into Module 5

| Module | Contribution to Deployment |
|--------|---------------------------|
| Module 1 (Fundamentals) | Debugging foundation — tokenization (cost), decoding (behavior), context windows (limits) |
| Module 2 (RAG) | Primary system to deploy — pipeline behind FastAPI with caching + streaming |
| Module 3 (Fine-Tuning) | Model to serve — vLLM, quantization, model versioning |
| Module 4 (Agents) | Most complex system — HITL, step budgets, fallbacks, streaming intermediate steps |

## Key Difference from Previous Modules

| Module 2-4 (Build) | Module 5 (Ship) |
|--------------------|-----------------|
| "Does it work?" | "Does it work at 3am with 1000 users?" |
| Notebooks | Docker containers |
| API keys in code | Secret management |
| Print statements | Structured logging + dashboards |
| "Try it again" | Automated recovery |
| Your machine | Cloud infrastructure |
| Free during dev | Real money in production |

## File Structure

```
module5-deployment/
├── roadmap.md
├── fastapi-serving.md              ← Primary deployment framework
├── fastapi-serving_PRINTABLE.html
├── mcp-protocol.md                 ← Model Context Protocol (tool integration standard)
├── mcp-protocol_PRINTABLE.html
├── containerization.md             ← Docker for AI services
├── containerization_PRINTABLE.html
├── streaming-and-ux.md             ← SSE, intermediate steps, loading states
├── streaming-and-ux_PRINTABLE.html
├── authentication-and-security.md  ← API keys, rate limiting, prompt injection
├── authentication-and-security_PRINTABLE.html
├── cost-monitoring.md              ← Token tracking, budgets, optimization
├── cost-monitoring_PRINTABLE.html
├── responsible-ai.md               ← Bias, filtering, transparency, compliance
├── responsible-ai_PRINTABLE.html
├── ci-cd-for-ai.md                 ← Testing non-deterministic, eval gates
├── ci-cd-for-ai_PRINTABLE.html
├── observability.md                ← LangSmith, tracing, dashboards
├── observability_PRINTABLE.html
└── capstone-guide.md               ← Scope, plan, build, present
    capstone-guide_PRINTABLE.html
```

## Topic .md — Deployment Runbook Structure

Each topic follows this procedure-oriented structure:

1. **What You're Deploying** (context from Modules 1-4 — what system/component)
2. **Prerequisites & Dependencies** (what you need before starting)
3. **Step-by-Step Procedure** (numbered, copy-pasteable, production-ready)
4. **Configuration Reference** (env vars, secrets, endpoints, values)
5. **Verification & Smoke Tests** (how to confirm it's working)
6. **Monitoring & Alerting** (what to watch, thresholds, dashboards)
7. **Troubleshooting Guide** (symptom → cause → fix, including Module 1 fundamentals for debugging)
8. **Security & Compliance** (auth, data handling, responsible AI aspects)
9. **Cost Management** (ongoing costs, optimization levers)
10. **Maintenance & Updates** (how to update models, data, configs without downtime)

## Topic _PRINTABLE.html — Deployment Visuals

Same CSS as Module 2-4 printables. SVG diagrams focus on:

- Infrastructure diagrams (boxes showing services, arrows showing traffic flow)
- Deployment pipeline flowcharts (build → test → deploy → monitor)
- Configuration reference tables (env vars, what they do, defaults)
- Troubleshooting decision trees (symptom → check this → try that)
- Checklists (pre-deploy, post-deploy, maintenance)
- At least 2-3 diagrams per topic — focused on PROCEDURE not concepts

## Code Reference Stack

- FastAPI (primary web framework)
- Docker + docker-compose (containerization)
- vLLM / HuggingFace TGI (model serving)
- LangServe (LangChain deployment)
- LangSmith (observability)
- Prometheus + Grafana (metrics)
- MCP SDK (Model Context Protocol)
- GitHub Actions (CI/CD)
- Pydantic (request/response validation)

## Tone

- Procedural — "do this, then this, then verify with this command"
- Ops-oriented — "here's what to monitor, here's when to alert"
- Security-conscious — "never put this in code, always use env vars"
- Cost-aware — "this costs $X/month, here's how to reduce it"
- Pragmatic — leverage your existing DevOps knowledge, focus on AI-SPECIFIC novelty
- Reference Module 1 concepts in troubleshooting ("if hallucinating, check temperature/decoding settings")

## What NOT to Include

- Basic Docker/FastAPI tutorials (you already know this — focus on AI-specific patterns)
- Cloud provider-specific setup (keep generic, mention options)
- Kubernetes details (beyond scope for capstone — keep to Docker/docker-compose)
- Enterprise security frameworks (keep to practical, implementable patterns)
- Full capstone implementation (guide the process, not do it for you)
