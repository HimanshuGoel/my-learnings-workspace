---
inclusion: fileMatch
fileMatchPattern: "**/module4-multimodal-agentic-ai/**"
---

# Module 4 — Multimodal & Agentic AI (System Architect's Guide)

## Context

Module 4 of the IIT KGP GenAI program (Nov 14 – Dec 26, 2026). This module has two halves: Multimodal (VLMs, multi-modal RAG) and Agentic AI (LangGraph, multi-agent systems, orchestration). Unlike Module 2 (pipeline assembly) or Module 3 (model modification), Module 4 is about DESIGNING AUTONOMOUS SYSTEMS — agents that plan, route, use tools, and handle complex state.

## Audience

- 14 years software dev (Java/.NET/Angular/Node.js)
- Completed: Math, Python, GenAI Fundamentals, Module 2 (RAG), Module 3 (Fine-Tuning)
- Strong foundation in: RAG pipelines, prompting, evaluation, LoRA/DPO, production patterns
- Now needs: How to build systems that reason autonomously, handle multiple modalities, and orchestrate complex multi-step workflows

## Key Difference from Previous Modules

| Module 2 (RAG) | Module 3 (Fine-Tuning) | Module 4 (Agents) |
|----------------|------------------------|-------------------|
| Assemble components | Modify models | Design autonomous systems |
| Linear pipeline | Single experiment | Graphs + loops + branching |
| Config & quality | Cost & evaluation | Architecture & orchestration |
| Like a REST API | Like customizing a library | Like designing microservices |
| Bad retrieval | Wasted GPU hours | Infinite loops, wrong routing |

## File Structure

```
module4-multimodal-agentic-ai/
├── roadmap.md
├── vlm-fundamentals.md             ← Vision-Language Models
├── vlm-fundamentals_PRINTABLE.html
├── multimodal-rag.md               ← RAG with images, PDFs, tables
├── multimodal-rag_PRINTABLE.html
├── agent-architectures.md          ← ReAct, Plan-and-Execute, patterns
├── agent-architectures_PRINTABLE.html
├── langgraph-fundamentals.md       ← State machines for agents
├── langgraph-fundamentals_PRINTABLE.html
├── tool-use-design.md              ← Function calling, tool interfaces
├── tool-use-design_PRINTABLE.html
├── multi-agent-systems.md          ← Supervisor, crew, swarm patterns
├── multi-agent-systems_PRINTABLE.html
├── planning-and-reasoning.md       ← Task decomposition, reflection
├── planning-and-reasoning_PRINTABLE.html
├── agent-memory.md                 ← Short-term, long-term, episodic
├── agent-memory_PRINTABLE.html
├── agent-evaluation.md             ← Testing agents, trajectory eval
├── agent-evaluation_PRINTABLE.html
└── production-agents.md            ← Deploy, HITL, observability
    production-agents_PRINTABLE.html
```

## Topic .md — System Architect's Guide Structure

Each topic follows this structure:

1. **What This Enables** (1-2 sentences — the capability this unlocks)
2. **Architecture Overview** (how the system is structured — diagrams and components)
3. **Key Patterns & When to Use Each** (pattern catalog with trade-offs)
4. **Implementation with LangGraph/LangChain** (practical code)
5. **State Management & Memory** (how the system maintains context across steps)
6. **Error Handling & Guardrails** (what happens when things go wrong — loops, hallucinated actions)
7. **Testing & Debugging** (how to verify complex async/graph-based systems)
8. **Production Considerations** (latency, cost, observability at scale)
9. **Integration Points** (how this connects to RAG, fine-tuning, deployment)
10. **Architecture Decision Record** (ADR-style: "we chose X because Y, accepting trade-off Z")

## Topic _PRINTABLE.html — Architecture Visuals

Same CSS as Module 2/3 printables. SVG diagrams focus on:

- System component diagrams (boxes + arrows showing data flow)
- State machine diagrams (nodes, edges, conditional routing)
- Communication patterns (agent ↔ agent, agent ↔ tool)
- Sequence diagrams (multi-step agent reasoning)
- Architecture comparison diagrams (pattern A vs pattern B)
- At least 2-3 diagrams per topic — focused on STRUCTURE not concepts

## Code Reference Stack

- LangGraph (primary orchestration framework)
- LangChain (tools, prompts, LLM wrappers)
- OpenAI GPT-4V / Claude Vision (multimodal)
- LLaVA / open-source VLMs (local multimodal)
- Unstructured / docling (document parsing)
- CLIP / multi-modal embeddings
- CrewAI (multi-agent reference)
- FastAPI (serving agents)

## Tone

- Systems thinking — "here's the architecture, here's why each component exists"
- Pattern-oriented — "use this pattern when X, switch to that pattern when Y"
- Failure-aware — agents fail in novel ways (loops, hallucinated tools, wrong routing)
- Pragmatic — most real apps need a simple ReAct agent, not a 10-agent swarm
- Build up complexity gradually — start with single agent, add multi-agent only when justified

## What NOT to Include

- Exhaustive LangChain API documentation (point to official docs)
- Every possible agent framework comparison (focus on LangGraph as primary)
- Academic multi-agent research papers (give practical patterns instead)
- Complex distributed systems (beyond single-machine deployment for now)
- Detailed VLM training (covered conceptually, not hands-on training)
