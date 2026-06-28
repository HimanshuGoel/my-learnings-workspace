---
inclusion: fileMatch
fileMatchPattern: "**/module2-advanced-prompting-rag/**"
---

# Module 2 — Advanced Prompting & RAG (Practitioner's Playbook)

## Context

Module 2 of the IIT KGP GenAI program (Jul 25 – Sep 5, 2026). Unlike Module 1 (conceptual fundamentals), Module 2 is an ENGINEERING module. Every topic is a practitioner's playbook — focused on decisions, implementation, debugging, and shipping.

## Audience

- 14 years software dev (Java/.NET/Angular/Node.js)
- Completed: Mathematics (8 topics), Python Libraries (13 libraries), GenAI Fundamentals (12 conceptual topics)
- Understands CONCEPTS (what is RAG, what is prompting, what are agents)
- Now needs ENGINEERING JUDGMENT — which approach, what settings, how to debug, when to ship

## File Structure

```
module2-advanced-prompting-rag/
├── roadmap.md                         ← topics, timeline, dependencies
├── advanced-prompting.md              ← CoT, few-shot, templates, eval
├── advanced-prompting_PRINTABLE.html
├── chunking-strategies.md             ← size, overlap, semantic, code
├── chunking-strategies_PRINTABLE.html
├── embedding-selection.md             ← which model, dims, trade-offs
├── embedding-selection_PRINTABLE.html
├── vector-store-design.md             ← collection, metadata, indexing
├── vector-store-design_PRINTABLE.html
├── retrieval-quality.md               ← top-k, re-ranking, hybrid, filters
├── retrieval-quality_PRINTABLE.html
├── rag-pipeline-architecture.md       ← end-to-end, component choices
├── rag-pipeline-architecture_PRINTABLE.html
├── rag-evaluation.md                  ← RAGAS, faithfulness, A/B testing
├── rag-evaluation_PRINTABLE.html
├── production-rag.md                  ← caching, streaming, monitoring, cost
├── production-rag_PRINTABLE.html
├── structured-output.md               ← JSON, Pydantic, function calling
├── structured-output_PRINTABLE.html
└── agentic-rag.md                     ← multi-step retrieval, routing
    agentic-rag_PRINTABLE.html
```

## Topic .md — Playbook Structure

Each topic follows this practitioner's playbook format:

1. **The Problem You're Solving** (1-2 sentences — what goes wrong without this)
2. **Options Available** (comparison table with trade-offs: approach / when to use / pros / cons)
3. **Recommended Approach** (with justification for our context — solo dev, learning, not enterprise-scale)
4. **Step-by-Step Implementation** (practical code snippets using Python libraries from our stack)
5. **Configuration Checklist** (what to set / recommended value / why)
6. **Failure Modes & Debugging** (if X happens → check Y → fix with Z)
7. **Production Considerations** (latency, cost, scale, monitoring)
8. **Evaluation Criteria** (how to know it's working — metrics, thresholds)
9. **Ready to Ship? — Checklist** (binary yes/no before moving on)

## Topic _PRINTABLE.html — Visual Playbook

Same CSS as module1-genai-fundamentals printables (7.5pt body, A4, same color scheme).

### SVG Diagram Focus (DECISIONS, not concepts)

- Decision flowcharts ("if X → use A, else → use B")
- Architecture diagrams (component wiring, data flow)
- Before/after comparisons (naive vs optimized)
- Configuration reference tables
- Failure mode → fix lookup tables
- At least 2-3 diagrams per topic

### Required Sections

1. Title + Problem Statement
2. Decision Flowchart (SVG — which approach to pick)
3. Architecture / Implementation Diagram (SVG)
4. Configuration Reference Table
5. Failure Mode → Fix Lookup Table
6. Production Checklist
7. Evaluation Quick-Reference

## Key Differences from Module 1

| Module 1 (Fundamentals) | Module 2 (Playbook) |
|--------------------------|---------------------|
| "What is RAG?" | "How do I build RAG that works?" |
| Conceptual understanding | Engineering decisions |
| Mental models & analogies | Code snippets & configs |
| Why it exists | When to use which option |
| Theory-first | Problem-first |
| Self-test questions | Ship-readiness checklists |

## Code Reference Stack

When referencing implementations, use these libraries (already covered in Python notes):
- LangChain / LlamaIndex for orchestration
- ChromaDB / FAISS for vector storage
- sentence-transformers for embeddings
- OpenAI / Anthropic APIs for LLM generation
- Pydantic for structured output
- FastAPI for serving
- RAGAS for evaluation

## Tone

- Direct, practical, opinionated (recommend a default, explain why)
- "Here's what I'd ship first, here's when to reconsider"
- No hedging — if there's a clear best practice, state it
- Acknowledge uncertainty only when genuinely trade-off-dependent
