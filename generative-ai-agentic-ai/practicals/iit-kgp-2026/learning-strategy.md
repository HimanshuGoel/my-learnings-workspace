# Learning Strategy

## Approach — Hybrid

Best for an experienced Software Architect learning AI as a second specialization. Start from problems, not syntax.

```text
Real World Problem → Why This Tool Exists → Mental Model → Architecture → Code → AI Use Cases → Production Patterns
```

---

## Key Insight

> The bottleneck is not theory. It is converting abstract AI concepts into intuitive mental models and practical implementation skills.

---

## Tool Roles

| Tool    | When to Use          | Strengths                                          |
| ------- | -------------------- | -------------------------------------------------- |
| ChatGPT | Learning & Revision  | Teaching, analogies, simplification, Q&A, concepts |
| Kiro    | Building & Shipping  | Spec → Design → Tasks → Implementation            |

- ChatGPT excels at nonlinear learning (Why? What if? Explain again. Compare.)
- Kiro excels at structured execution (spec-driven projects, not learning)

---

## Learning Sequence Per Topic

```text
Learn Concept → Learn Library → Build Mini Project → Build Real Project → Move Forward
```

Example:

```text
Learn RAG → Learn LangChain → Build PDF Chatbot → Build Multi-document Assistant → Move to Agents
```

---

## Python Prerequisites

Learn enough to read AI code comfortably:

| Category        | Topics                                  |
| --------------- | --------------------------------------- |
| Data Structures | list, tuple, dict, set                  |
| Functions       | functions, lambda, comprehensions       |
| OOP             | classes, dataclasses                    |
| Advanced        | typing, generators, decorators, context managers |

---

## Combined Workflow

| Phase    | Tool    | Purpose                        |
| -------- | ------- | ------------------------------ |
| Learning | ChatGPT | Teach concepts, analogies, Q&A |
| Revision | ChatGPT | Compact notes, comparisons     |
| Building | Kiro    | Spec → Design → Tasks → Code  |
| Review   | ChatGPT | Test understanding, find gaps  |

---

## Retaining Deep Knowledge in the AI-Assisted Era

### The Problem

AI tools accelerate output but bypass the **generation effect** — the cognitive principle that information you actively produce (write, struggle through, solve) is retained far better than information you passively review. When AI writes code or content, you skip the effortful encoding phase that builds deep mental models.

The result: you ship faster but retain less. Your mental map of the system becomes sparse and fragile, reducing confidence in your own work.

### When AI-First is Fine

- Routine/boilerplate tasks (CRUD, config, glue code)
- Exploring unfamiliar territory quickly to decide if it is worth deeper investment
- Working under time pressure on well-understood problems
- AI handles the "how" while you own the "what" and "why"

### When It is Not Okay

- You cannot explain or debug what was generated
- You are building on foundations you do not understand
- Your confidence drops because you could not reproduce the work
- You stop growing as a practitioner

### Practical Tactics

| Tactic | Description |
| ------ | ----------- |
| AI as draft, not delivery | Let AI generate, then rewrite parts yourself. Rewriting even 30% builds significantly more retention than reviewing alone. |
| Explain-back practice | After accepting AI output, explain it as if teaching someone. If you cannot, dig deeper before moving on. |
| Selective depth | Decide upfront: "grow-through task or get-through task?" For grow-through tasks, slow down and write more yourself. |
| 70/30 rule | For mastery domains: write 70%, AI handles 30%. For get-things-done domains: flip the ratio. |
| Active review | Instead of reading generated code top-to-bottom, predict what the next section does before reading it, or find one thing to change. |
| From-scratch practice | Periodically build something small without AI. Keeps foundational skills sharp and confidence grounded. |
| Document decisions | Write a one-line note about *why* you chose an approach. Decision-making compounds; typing speed does not. |
| Visual notepad alongside AI | Keep a physical notepad while working with AI. Sketch mental models, relationships, and flows. Leverages dual coding theory (verbal + visual = two retrieval paths). Focus on connections, not details. Keep it messy and fast — it is for your brain, not others. Skip it for get-through tasks; use it for grow-through tasks. See [Visual Note-Taking Guide](./visual-note-taking-guide.md) for techniques. |

### The Bigger Picture

The skill shift is upward — automation handles the lower layers, freeing cognitive energy for architecture, trade-off analysis, debugging novel problems, and system thinking. Speed without understanding is debt. Build in small, intentional friction where growth matters.
