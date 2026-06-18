---
inclusion: fileMatch
fileMatchPattern: '**/python/**'
---

# Python Library Notes — Structure & Guidelines

When creating notes for Python libraries (NumPy, Pandas, PyTorch, etc.), follow this structure consistently.

## File Structure Per Library

```
python/
├── <library>/
│   ├── notes.md              ← Concepts, mental models, when to use, AI connection
│   ├── cheatsheet.md         ← Quick reference: functions, syntax, copy-paste patterns (on-screen lookup)
│   ├── exercises.py          ← 10-15 graded problems (easy → medium → hard)
│   ├── mini-project.py       ← One realistic project using the library
│   └── cheatsheet_PRINTABLE.html  ← Rich printable learning notes (NOT just a terse cheatsheet)
```

## notes.md — Structure

1. **What problem does this library solve?** (1-2 sentences, real-world framing)
2. **Mental model** (analogy from software dev world the user already knows)
3. **Where it fits** — a simple diagram or list showing: what comes BEFORE this library in the AI pipeline, what comes AFTER, and what it talks to. Helps see the big picture.
4. **Core concepts** (the 20% that gives 80% value, with code snippets)
5. **Key functions/methods** (grouped by task, with one-line descriptions)
6. **Common patterns** (idiomatic usage that shows up everywhere)
7. **AI/ML connection** — This section should be detailed and concrete, not just "used in AI." Structure it as:
   - **Where in the AI pipeline:** preprocessing? training? inference? evaluation?
   - **Concrete example:** "When you build a RAG system, you use NumPy to compute cosine similarity between embedding vectors"
   - **Which IIT KGP module uses this:** map to Module 1/2/3/4/5 so the user sees relevance
   - **What breaks without it:** "Without Pandas, cleaning a 10k-row dataset for model training takes 10x longer"
   - Keep to 5-8 bullet points. Each bullet = one real scenario, not abstract theory.
8. **Common mistakes** (what trips people up)
9. **When NOT to use** (alternatives and their trade-offs)
10. **Ready to move on?** — 3-5 checkboxes the user can self-test against. Example: "☐ I can create, reshape, and slice arrays without looking up docs." If all checked → move to next library.

## cheatsheet.md — Structure

- Terse, reference-style — meant for quick on-screen lookup, not deep reading
- Group by task (e.g., "Creating arrays", "Filtering", "Aggregation")
- Each entry: function signature + one-line explanation + minimal example
- No long explanations — that's what notes.md is for
- Should fit on 1-2 printed pages equivalent in content density

## cheatsheet_PRINTABLE.html — Structure

This is a **rich printable learning document** (like the mathematics printable notes), NOT just a terse code reference. It should be a standalone learning companion for paper reading.

### Format & Styling

- Use the same CSS styling as `mathematics/*_PRINTABLE.html` files (compact A4, 7.5pt body, styled h1/h2/h3, .tip, .prompt, .diagram classes)
- Use `@page { margin: 0.5cm; size: A4; }` for print optimization
- Use `.two-col` or `.three-col` CSS class for dense sections
- Code blocks use `.prompt` class (monospace, light background, border-left)
- Tips use `.tip` class (yellow background, orange left border)
- Diagrams use `.diagram` class with inline SVG

### Required Sections (in order)

1. **Title + Summary** — one sentence explaining what the library does
2. **Why It Exists** — problem, solution, mental model, AI connection (bullet list)
3. **Where It Fits** — SVG pipeline diagram showing before/after in the AI stack
4. **Core Concepts** — each concept with: meaning, why, formula/syntax, example, mental model, AI connection. Include SVG diagrams for visual concepts (broadcasting, axes, reshaping, etc.)
5. **Common AI Patterns** — normalization, cosine similarity, softmax, one-hot, etc. with code in `.prompt` blocks and SVG diagrams where helpful
6. **AI/ML Connection Table** — pipeline stage → NumPy operation → concrete example
7. **IIT KGP Module Mapping Table** — which module uses what from this library
8. **Common Mistakes Table** — mistake → fix
9. **When NOT to Use Table** — scenario → alternative → why
10. **Quick Reference** — grouped code blocks (`.prompt`) in `.two-col` layout for dense function reference
11. **AI Translation Table** — library concept → AI interpretation → specific example
12. **Mental Models Summary** — bullet list of all analogies used in the document
13. **Memory Map** — hierarchical concept flow in `.prompt` block (ASCII tree showing how concepts connect)
14. **Top Takeaways (Ranked)** — 10-12 key insights in a numbered table
15. **Ready to Move On?** — self-test checklist in a `.tip` block

### SVG Diagram Guidelines

- Use inline SVG (not external files) — keeps HTML self-contained for printing
- Keep viewBox compact (width 200-400, height 60-140)
- Use consistent colors: primary=#4F46E5, accent=#f59e0b, success=#059669, error=#ef4444
- Use arrow markers for flow/direction
- Add `.diagram-caption` below each SVG
- Use `.diagram-row` (flexbox) to place 2-3 small diagrams side-by-side
- Diagrams should explain ONE concept visually — not be decorative

### Content Source

- Draw content from `notes.md` in the same library folder — the printable should be consistent with and expand upon the notes, not contradict them
- Add visual explanations (diagrams) for concepts that are hard to grasp from text alone
- The printable should be self-sufficient — someone reading only the printable should understand the library without needing notes.md open

## exercises.py — Structure

- 10-15 exercises with increasing difficulty
- Each exercise as a comment block explaining the task, followed by empty function or space to solve
- Group into: Easy (5), Medium (5), Hard (3-5)
- Include expected output as comments
- Focus on library-specific skills, not general Python
- Each exercise should teach ONE concept (not combine 5 things)
- **At least 3-4 exercises should mirror real AI tasks** (e.g., "normalize features for a model", "compute cosine similarity between two vectors", "reshape data for a neural network input")
- When AI jargon appears in an exercise, add a brief inline comment explaining it (e.g., "# tensor = a multi-dimensional array, like a matrix but can be 3D, 4D, etc.")

## mini-project.py — Structure

- One realistic, self-contained project (30-60 min to complete)
- Clear problem statement at the top as a docstring
- Skeleton code with TODOs for the user to fill
- Uses a real or realistic dataset (can be generated inline)
- Connects to an AI/ML use case where possible
- Solution can be in a separate `mini-project-solution.py` if user asks

## Audience Assumptions

- 14 years software development experience (Java, .NET, Angular, Node.js)
- Knows OOP, design patterns, architecture — skip "what is a variable" content
- New to Python's data science ecosystem and AI libraries
- Learns best through analogies to familiar frameworks (Angular, Spring Boot, etc.)
- Needs to build muscle memory through practice, not just reading

## Tone & Style

- Concise, direct — no fluff
- Use familiar analogies: "like Array.map() in JS", "similar to Spring's @Service"
- Always explain WHY before HOW
- Code examples should be runnable as-is (not pseudocode)
- Comments in code should explain the "why", not the "what"
- **Define AI jargon inline on first use.** Don't assume the user knows terms like tensor, epoch, batch, embedding, loss, gradient. A short parenthetical is enough: "epoch (one full pass through all training data)"

## What NOT to Include

- Basic Python syntax (loops, if/else, classes) — user already knows this
- History of the library or who created it
- Exhaustive API documentation — link to official docs instead
- Anything that requires a GPU or cloud setup (keep exercises local-runnable)
