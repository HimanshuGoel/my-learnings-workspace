---
inclusion: fileMatch
fileMatchPattern: '**/mathematics/*.md,**/extracted-notes/*.md'
---

# Notes Structure — Markdown Learning Notes Guidelines

When the user asks to rearrange, restructure, or clean up a learning notes file, follow these guidelines to produce well-organized, scannable, and revision-friendly content.

## Golden Rules

1. **Restructure for clarity — never drop content.** All concepts, formulas, mental models, AI connections, examples, and tables from the original must be preserved. The goal is: same knowledge, better organization, easier to scan and recall.

2. **Enhance readability and explainability.** Don't just reorganize — actively improve the content by:
   - Adding brief explanatory context where a concept feels too terse or abrupt
   - Including a short "why this matters" sentence when jumping into a formula or definition
   - Adding simple worked examples where only abstract definitions exist
   - Expanding bullet points into short sentences when they read like disconnected keywords
   - Adding transition phrases between concept groups so the reader understands the flow
   - Including "In plain English" rewrites for dense mathematical statements
   - Adding real-world analogies beyond what the original provides if they aid understanding
   - Noting common mistakes or misconceptions where relevant

## File Structure Template

Every notes file should follow this top-level structure:

```markdown
# Stage N — Topic Name

## One-Line Summary

> Single sentence capturing the essence of the topic.

---

## Why This Matters for AI

- 3-5 bullet points explaining relevance to GenAI/ML/Deep Learning
- Keep it concise and motivating

---

## Core Concepts

## Section Group Name

Brief 1-2 sentence introduction explaining what this group covers and why.

### 1. Concept Name

- **Meaning** — 1-2 sentence plain English definition
- **Why It Exists** — what problem this solves (1 sentence)
- **Formula** — mathematical notation with variables explained
- **Example** — simple worked numeric example
- **Mental Model** — analogy, visual, or memory trick
- **AI Connection** — how this maps to ML/AI/LLMs with a specific use case
- **Common Mistake** — (optional) frequent misconception

### 2. Next Concept Name

(same pattern)

---

## Quick Reference Tables

### Table 1 — [Descriptive Name]

| Column A | Column B | Column C |
| -------- | -------- | -------- |

---

## Memory Map

Visual flow diagram showing how concepts connect (use fenced code block with `text` language tag).

---

## Interview / Revision Summary

| Concept | Remember This |
| ------- | ------------- |

### If Someone Asks: "What is [Topic]?"

> Ready-made 5-7 sentence answer for interviews.
```

## Section Rules

### Title Section
- Use `#` for the document title only — format: `# Stage N — Topic Name`
- Follow immediately with a one-line summary in blockquote format
- The summary should be memorizable — one sentence that captures the entire topic

### Why This Matters for AI
- Brief motivational section (3-5 bullets max)
- Connects the abstract math to practical AI/ML use
- Helps the reader understand "why should I care?"

### Core Concepts
- Each concept gets a numbered `###` heading (e.g., `### 1. Derivative`)
- Every concept must have these sub-parts (skip Formula if not applicable):
  - **Meaning** — what it is in plain English (1-2 sentences, not just a phrase)
  - **Why It Exists** — brief context on what problem this concept solves or why we need it (1 sentence)
  - **Formula** — mathematical notation with variable meanings explained
  - **Example** — a simple worked example showing the formula/concept in action
  - **Mental Model** — analogy or visual metaphor for recall
  - **AI Connection** — practical relevance to ML/AI/LLMs with a specific use case
  - **Common Mistake** — optional; include when there's a frequent misconception
- Use `---` horizontal rules between major concept groups (not between every concept)
- Group related concepts under a `## Section Name` when they form a logical cluster (e.g., "## Derivative Rules", "## Optimization")
- Add a brief 1-2 sentence introduction at the start of each concept group explaining what the group covers and why it matters as a unit

### Quick Reference Tables
- All summary and reference tables go in this dedicated section at the bottom
- Tables are for quick scanning during revision — keep them dense
- Name each table descriptively (e.g., "Table 1 — Derivative Rules", "Table 2 — AI Mapping")
- Tables should NOT duplicate the explanations above — they condense them
- Include these standard tables when applicable:
  - **Concepts Overview** — one row per concept with columns: #, Concept, Core Question, Key Idea, AI Connection
  - **Formula Cheat Sheet** — all formulas in one place
  - **AI Translation Table** — math concept → AI/ML equivalent
  - **Visual Mental Models** — concept → analogy mapping
  - **Most Important Takeaways** — ranked list of key insights

### Memory Map
- A single ASCII/text flow diagram showing how concepts in the file connect
- This is the "can I explain this without notes?" self-test
- Keep it to one diagram per file (two at most if the topic has distinct branches)

### Interview / Revision Summary
- Final table: one row per concept, one memorable sentence per row
- Acts as the 30-second recall sheet
- Optionally include a "If someone asks you about [Topic], answer:" block at the very end with a ready-made 5-7 sentence interview answer

## Readability & Explainability Enhancements

When restructuring, actively look for opportunities to improve understanding:

### Add Context Before Jumping In
- Before a formula, add one sentence explaining what problem it solves
- Before a new concept group, add a transition sentence connecting it to the previous group
- Example: "Now that we know how to measure individual vectors, the natural next question is: how do we compare two vectors?"

### Expand Terse Content
- If the original has a bare keyword like `"Predictable"`, expand to: "When variance is small, the data is predictable — values cluster tightly around the mean"
- If a formula appears without context, add: "This formula answers the question: ..."

### Add Simple Examples
- Every formula should have at least one worked numeric example
- Keep examples simple (2D vectors, small numbers) so the concept is clear
- Format: show the input, show the computation, show the result

### Add "In Plain English" Rewrites
- For mathematical definitions, add a plain English restatement
- Format: `**In plain English:** [rewrite]`
- Use this sparingly — only when the mathematical statement is genuinely hard to parse

### Add "Why This Matters" Micro-Motivations
- Before diving into a concept, briefly state what problem it solves
- One sentence is enough: "Without unit vectors, we couldn't compare directions independent of magnitude."

### Use Progressive Disclosure
- Start each concept with the simplest explanation
- Then layer on formula, then example, then AI connection
- Reader should understand the gist from the first line alone

## Content Cleanup Rules

### Remove
- Conversational artifacts ("Perfect. Let me now...", "Excellent idea.", "Just like we did for Stage 3...")
- Teaching prompts directed at the reader ("If someone asks you...", "This is the sheet I would personally keep if...")
- Duplicate paragraphs (same content appearing twice)
- Filler phrases that add no information
- Bare floating text that lacks any heading or context

### Preserve
- Every concept, formula, and example
- All mental models and analogies
- All AI/ML connections
- All tables (restructure but don't drop rows)
- Cross-stage references (convert to brief notes like "→ See calculus.md § Chain Rule")
- Any unique insight or "aha moment" phrasing — these are valuable for recall

### Convert
- Floating unstructured text → proper headed sections
- Code blocks used for plain emphasis → regular bold or bullet points
- Repeated "Mental Model: X" patterns → consistent `**Mental Model**` format
- Bare keyword lists → full sentences with context
- Disconnected bullet points → flowing explanations with transitions

### Enhance (add new content where it improves understanding)
- Add worked examples where only abstract formulas exist
- Add "In plain English" rewrites for dense definitions
- Add transition sentences between concept groups
- Add brief "why this matters" motivations before jumping into formulas
- Add common mistakes/misconceptions where relevant
- Add real-world analogies that aid intuition (mark these clearly so they're distinguishable from original content)

## Formatting Rules

### Headings
- `#` — document title (one per file)
- `##` — major sections (Why AI, Core Concepts, Quick Reference Tables, Memory Map, Interview Summary)
- `###` — individual concepts or table names
- Never skip heading levels (no `#` followed by `###`)

### Formulas
- Use consistent notation throughout a file
- Prefer inline format for short formulas: `f'(x) = 0`
- Use fenced code blocks only for multi-line formula flows or diagrams
- Do not use code blocks for single-word emphasis

### Lists
- Use `-` for bullet points (not `*`)
- Use numbered lists (`1.`, `2.`) only for sequential/ordered content
- Bold the key term at start of list items for scannability: `- **Gradient** — direction of steepest increase`

### Tables
- Always include header row and separator row
- Keep cell content concise — no full sentences in table cells
- Align columns for readability

### Horizontal Rules
- Use `---` to separate major topic groups within Core Concepts
- Use `---` before each `##` section for visual breathing room
- Do not overuse — one between every concept is too many

### Code Blocks
- Use ` ```text ` for ASCII diagrams and flow charts
- Use ` ```javascript `, ` ```python `, etc. for actual code examples
- Do not use code blocks to emphasize plain English words or phrases

## Cross-Reference Convention

When a concept connects to another file in the same folder:
- Use format: `→ See [filename.md] § [Section Name]`
- Example: `→ See calculus.md § Chain Rule`
- Keep cross-references inline within the relevant concept's AI Connection

## File Naming

- Files in the mathematics folder follow: `topic-name.md` (lowercase kebab-case)
- The `roadmap.md` file is the index/overview — do not restructure it using this template
