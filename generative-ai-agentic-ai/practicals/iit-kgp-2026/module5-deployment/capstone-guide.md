# Capstone Guide

## What You're Deploying

Your capstone project — a complete AI system that demonstrates mastery of Modules 1-5. This guide covers how to SCOPE (not too big, not too small), PLAN (architecture before code), BUILD (iteratively with checkpoints), and PRESENT (to evaluators on Feb 6). The project-ideas.md file has specific project options; this guide covers the PROCESS regardless of which project you choose.

## Prerequisites & Dependencies

- Modules 1-4 concepts understood
- Module 5 topics 1-9 for deployment patterns
- Project idea selected (from project-ideas.md or your own)
- 5 weeks available (Jan 2 – Feb 6)
- Feedback session: Jan 30 (project must be 90% by then)

## Step-by-Step Procedure

### Phase 1: Scope & Architecture (Week 1 — Jan 2-8)

```
Day 1-2: Define the problem clearly
  - What SPECIFIC task does this system solve?
  - Who is the user? What do they input? What do they get back?
  - What makes this MORE than just "send to LLM and get answer"?

Day 3-4: Architecture design
  - Draw the component diagram (what talks to what)
  - Identify: which Module 2-4 patterns you're using
  - Write the Architecture Decision Records (why this approach)

Day 5-7: Validate scope
  - Can I build this in 4 weeks? (If unsure → reduce scope)
  - Do I have access to needed data/APIs?
  - What's the MVP vs nice-to-have?
```

### Scope Calibration

| Scope | Description | Recommendation |
|-------|-------------|---------------|
| Too small | Just a prompt + API call | Add RAG, tools, or multi-step workflow |
| Just right | RAG pipeline OR agent with tools OR fine-tuned model + deployment | This is your target |
| Ambitious | RAG + agent + fine-tuning + multi-modal + deployment | Achievable if you reuse Module 2-4 work |
| Too big | Novel research, new model architecture, distributed system | Scale down — you have 4 weeks, not 4 months |

### Phase 2: Core Implementation (Week 2 — Jan 9-15)

```
Priority order:
1. Get the AI pipeline working end-to-end (even ugly/slow)
2. Ensure core quality (retrieval works, agent completes tasks)
3. Don't optimize yet — verify the APPROACH works first

Milestones:
  □ Data/documents loaded and chunked (if RAG)
  □ Core pipeline produces correct output for 5 test queries
  □ Agent completes its primary task (if agentic)
  □ End-to-end works locally (notebook or script)
```

### Phase 3: API + Deployment (Week 3 — Jan 16-22)

```
Apply Module 5 patterns:
  □ FastAPI service with /query or /chat endpoint
  □ Streaming response (SSE)
  □ Docker container (Dockerfile + docker-compose)
  □ Health/ready endpoints
  □ Basic auth (API key at minimum)
  □ .env for configuration (no hardcoded secrets)

Don't over-engineer:
  - Docker compose is enough (no Kubernetes)
  - Single container is fine (no microservices)
  - SQLite/file persistence is fine (no Postgres required)
```

### Phase 4: Quality + Polish (Week 4 — Jan 23-29)

```
  □ Evaluation: Run RAGAS or agent eval on test set
  □ Error handling: What happens on bad input? Empty retrieval? Timeout?
  □ Cost estimate: How much does one query cost? 1000 queries?
  □ Documentation: README with setup instructions, architecture diagram
  □ Demo preparation: 3-5 compelling test queries that showcase capabilities
  
Quality bar:
  - Works reliably for demo (not just once in a notebook)
  - Handles at least 2 error cases gracefully
  - Has measurable quality metric (faithfulness > X, task completion > Y%)
```

### Phase 5: Feedback + Final Polish (Jan 30 – Feb 6)

```
Jan 30: Feedback session
  - Present current state
  - Note all feedback points
  - Prioritize: what can I realistically fix in 1 week?

Feb 1-5: Final polish
  - Address critical feedback
  - Fix any demo-breaking bugs
  - Finalize documentation
  - Practice presentation (5-10 min)

Feb 6: Capstone Evaluation
  - Demo the system live
  - Explain architecture decisions
  - Show evaluation metrics
  - Answer questions about trade-offs
```

## Configuration Reference — What Evaluators Look For

| Criteria | Weight | What Demonstrates It |
|----------|--------|---------------------|
| Real-world value | 30% | Solves an actual problem, not a toy demo |
| Agentic AI usage | 20% | LangGraph, tool use, multi-step reasoning |
| RAG usage | 20% | Document retrieval, chunking, evaluation |
| Architecture quality | 15% | Clean design, justified decisions, modularity |
| Technical depth | 15% | Evaluation metrics, error handling, deployment |

## Verification & Smoke Tests

### Pre-Submission Checklist

```
ARCHITECTURE:
  □ Component diagram exists (shows what connects to what)
  □ At least 2 Architecture Decision Records (why you chose X over Y)
  □ Technology stack documented with justifications

FUNCTIONALITY:
  □ Core use case works end-to-end (demo-able)
  □ 5+ test queries produce good results
  □ At least one error case handled gracefully
  □ Streaming works (if applicable)

QUALITY:
  □ Evaluation metric measured (RAGAS, task completion, or human eval)
  □ Quality above stated threshold
  □ Can explain WHY quality is at this level (what's the bottleneck)

DEPLOYMENT:
  □ Runs in Docker (docker-compose up → working)
  □ API documented (at least endpoint + example request/response)
  □ Configuration via env vars (no hardcoded keys)
  □ Health endpoint returns 200

DOCUMENTATION:
  □ README: what it does, how to run, architecture
  □ Cost estimate per query
  □ Known limitations documented
  □ Future improvements listed (shows self-awareness)
```

## Monitoring & Alerting

For the capstone, you don't need full production monitoring. But you SHOULD have:

- Token cost tracking (how much does each query cost?)
- Basic logging (what happened during each request?)
- Error counting (how often does it fail?)
- At least one quality metric tracked over your test set

## Troubleshooting Guide

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| "It works sometimes" | Non-deterministic LLM + no error handling | Set temperature=0, add retries, handle edge cases |
| Demo breaks during presentation | Untested on fresh environment | Test: clone repo → docker-compose up → run demo |
| Evaluator asks "why not simpler?" | Over-engineered for the problem | Have a clear answer: "I tried simpler first, it failed because..." |
| Retrieval quality is poor | Bad chunking or wrong embedding model | Run RAGAS, identify bottleneck, fix the weakest link |
| Agent loops during demo | No step budget | Add max_steps=10, timeout, fallback response |
| "What's the evaluation?" | No metrics | Run RAGAS, even on 20 examples. Show the numbers. |

## Security & Compliance

- Remove any real user data from demo (use synthetic)
- Don't expose API keys in demo (use env vars)
- If using proprietary data: get permission or anonymize
- Document any limitations of your system honestly (evaluators respect this)

## Cost Management

| Capstone Phase | Estimated Cost | Notes |
|----------------|---------------|-------|
| Development (4 weeks) | $20-50 (API calls) | Mostly testing queries |
| Evaluation runs | $5-15 | RAGAS + test queries |
| Demo day (live) | $1-5 | Few live queries |
| Total capstone budget | ~$30-70 | Very manageable |

If using fine-tuned model: add $10-50 for training runs.

## Maintenance & Updates

Post-capstone, your project can become:
- **Portfolio piece:** Clean up, open-source on GitHub
- **Learning reference:** Template for future AI projects
- **Interview demo:** "Here's a system I built end-to-end"

Document what you'd do differently with more time (shows growth mindset).

## Presentation Tips

```
Structure (5-10 minutes):
1. Problem statement (30s) — what does this solve?
2. Architecture diagram (60s) — how is it built?
3. Live demo (3-4 min) — show it working with 3-5 queries
4. Evaluation metrics (60s) — show the numbers
5. Trade-offs & decisions (60s) — what you chose and why
6. Future improvements (30s) — what you'd do with more time

Tips:
- Start with the demo (hook them with the working system)
- Have pre-typed queries ready (don't type during demo)
- Have a backup recording if live demo might fail
- Acknowledge limitations before they ask (shows maturity)
- "I chose X because Y, accepting trade-off Z" → this is what evaluators want to hear
```
