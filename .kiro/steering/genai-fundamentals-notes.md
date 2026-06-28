---
inclusion: fileMatch
fileMatchPattern: '**/module1-genai-fundamentals/**'
---

# GenAI & LLM Fundamentals — Structure & Guidelines

When creating notes for GenAI concepts (Transformers, Attention, Tokenization, etc.), follow this structure consistently.

## File Structure Per Topic

```
module1-genai-fundamentals/
├── roadmap.md                    ← topics, order, priority, module mapping
├── <topic>.md                    ← detailed concept notes
├── <topic>_PRINTABLE.html        ← rich printable with SVG diagrams
└── diagrams/                     ← excalidraw big-picture diagrams
```

## Topic Notes (.md) — Structure

1. **What is this?** (1-2 sentences, non-technical framing)
2. **Why does it exist?** (the problem it solves — what broke before this existed)
3. **Mental model** (analogy from software dev the user already knows)
4. **How it works** (step-by-step intuition, NOT math-heavy — use the math notes for formulas)
5. **Visual explanation** (ASCII diagram or description that gets rendered as SVG in printable)
6. **Concrete example** (walk through one real scenario end-to-end)
7. **Where you'll use this** (map to IIT KGP modules: 1/2/3/4/5)
8. **Common misconceptions** (what people get wrong)
9. **Connection to other topics** (what prerequisite this builds on, what it enables next)
10. **Ready to move on?** — 3-4 self-test questions

## Printable HTML (_PRINTABLE.html) — Structure

Follow the same styling as `mathematics/*_PRINTABLE.html`:

### Format & Styling

- CSS: @page A4, 7.5pt body, h1/h2/h3, .tip, .prompt, .diagram classes
- Same color scheme: primary=#4F46E5, accent=#f59e0b, success=#059669, error=#ef4444
- Use inline SVG diagrams for visual concepts
- Use .tip for important callouts
- Use .prompt for code/pseudo-code blocks
- Use tables for comparisons and mappings

### Required Sections (in order)

1. **Title + Summary** — one sentence
2. **Why It Exists** — problem/solution/mental model
3. **How It Works** — step-by-step with SVG diagrams at each key step
4. **Concrete Example** — walk-through with diagram
5. **AI Pipeline Connection** — where in the stack this concept operates
6. **IIT KGP Module Mapping** — which module uses this
7. **Common Misconceptions** — table of wrong idea → correct understanding
8. **Connection Map** — what comes before, what comes after
9. **Key Terminology Table** — term → plain-English definition
10. **Top Takeaways** — 5-8 ranked insights
11. **Ready to Move On?** — self-test in .tip block

### SVG Diagram Guidelines

- Use inline SVG (self-contained for printing)
- Keep viewBox compact (200-400 width, 60-140 height)
- Colors: primary=#4F46E5, accent=#f59e0b, success=#059669, error=#ef4444
- Arrow markers for flow/direction
- .diagram-caption below each SVG
- Diagrams should explain process/flow/architecture — not be decorative
- At least 2-3 diagrams per topic (visual learning approach)

## Audience Assumptions

- 14 years software dev experience (Java, .NET, Angular, Node.js)
- Completed mathematics notes (vectors, matrices, probability, calculus)
- Completed Python library notes (NumPy through Streamlit)
- New to AI/ML theory — understands the CODE but not the CONCEPTS behind it
- Learns best through analogies, visuals, and "why does this exist?" framing

## Tone & Style

- Concise, direct — no academic fluff
- Always WHY before HOW
- Use familiar analogies: "like dependency injection", "like event-driven architecture"
- Define jargon inline on first use: "attention (mechanism that lets the model focus on relevant input parts)"
- No unnecessary math — reference the mathematics notes when formulas matter
- Focus on intuition and mental models, not derivations

## What NOT to Include

- Detailed mathematical derivations (point to mathematics/ folder instead)
- Code implementations (point to python/ folder instead)
- History/who invented what (unless it aids understanding)
- Exhaustive paper references (one key paper link per topic is enough)

## Topics to Cover (in order)

1. why-llms-exist.md — The problem: why not just use rules/sklearn? What LLMs do differently.
2. tokenization.md — Text → token IDs. BPE, WordPiece, SentencePiece. Vocabulary.
3. embeddings.md — Token IDs → dense meaning vectors. Semantic space. Similarity.
4. attention.md — Self-attention: how the model focuses on relevant parts. Q/K/V.
5. transformer-architecture.md — Full picture: encoder, decoder, layers, norms, FF.
6. pretraining.md — How models learn from internet-scale data. Next-token prediction.
7. prompting.md — Zero-shot, few-shot, CoT, system prompts, structured output.
8. decoding.md — Temperature, top-p, top-k, beam search, sampling strategies.
9. fine-tuning.md — Full fine-tuning, LoRA, PEFT, RLHF, DPO. Module 3 preview.
10. rag.md — Retrieval-augmented generation: architecture, chunking, retrieval, synthesis.
11. agents.md — Tool use, reasoning loops, ReAct, planning, multi-step.
12. evaluation.md — Metrics, hallucination, faithfulness, safety, alignment.
