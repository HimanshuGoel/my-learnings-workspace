---
inclusion: fileMatch
fileMatchPattern: '*_PRINTABLE.html'
---

# Printable Notes — HTML Generation from Markdown

When the user asks to create a printable/compact/readable HTML version of a markdown file, follow these guidelines to produce a high-quality print-ready document.

## Golden Rule

**Never lose valuable information from the source markdown.** The printable file should contain ALL the explanatory content from the markdown — every "Why It Exists," every "Mental Model," every worked example, every "In Plain English" rewrite, every "Common Mistake," and every "AI Connection." These ARE the content, not decoration to be trimmed.

Rephrasing and tightening sentences is encouraged — remove filler words, merge genuinely redundant points. But **keep the full explanatory depth.** If a concept has 6 bullet points in the markdown (Meaning, Why It Exists, Formula, Example, Mental Model, AI Connection), all 6 should appear in the printable. The printable should feel like reading the markdown with better formatting, not like a stripped-down summary.

The compactness comes from CSS styling (small fonts, tight spacing, multi-column layouts) — NOT from removing explanatory text.

## Output Format

- Generate a single self-contained HTML file (no external CSS/JS dependencies)
- Place it alongside the source markdown file with suffix `_PRINTABLE.html`
- The file should open in any browser and print cleanly via Ctrl+P → Save as PDF

## Page Layout

- A4 page size with 0.5cm margins (`@page { margin: 0.5cm; }`)
- Body padding: 0.3cm
- No forced page breaks — let content flow naturally
- Use `break-inside: avoid` on code blocks, prompts, and tip boxes
- Use `break-after: avoid` on h2 and h3 to prevent orphaned headers

## Typography

- Body font: 'Segoe UI', Arial, sans-serif at **7.5pt**
- Line height: **1.2** (tight)
- Code/prompts: 'Consolas', monospace at **6.5pt**, line-height 1.15
- Headings: h1 = 11pt, h2 = 8.5pt, h3 = 7.5pt

## Visual Hierarchy

- h1: bottom border (1.5px solid), used only once for document title
- h2: light gray background (#eee) with left border (2.5px solid #4F46E5), acts as section dividers
- h3: colored text (#4F46E5), bold, no background, for subsections
- Use bullet points — paragraphs waste vertical space
- Bold key terms at the start of list items for scannability

## Special Blocks

- Prompts/code examples: class `prompt` — gray background (#f5f5f5), 1px border (#ddd), monospace, `white-space: pre-wrap`
- Tips/callouts: class `tip` — yellow background (#fffbe6) with amber left border (2px solid #f59e0b)
- Multi-column layouts: class `two-col` (column-count: 2) or `three-col` (column-count: 3) with 10px gap — use for short bullet lists to save vertical space

## Content Rules

### CRITICAL: Do NOT over-summarize

The biggest mistake when generating printable files is aggressively trimming content for "compactness." DO NOT reduce rich explanatory bullet points into single-line summaries. The printable should feel like reading the source markdown with better visual formatting — not like a stripped-down cheat sheet.

**What to KEEP in full (never abbreviate):**
- "Why It Exists" explanations — these provide motivation and context
- "Mental Model" analogies — these are the primary recall triggers
- Worked examples with numbers — these make abstract concepts concrete
- "AI Connection" with specific use cases — these answer "why should I care?"
- "Common Mistake" warnings — these prevent real confusion
- "In Plain English" rewrites — render these as `.tip` callout boxes
- Section intro paragraphs — render as `<p class="section-intro">` in italic
- Interpretation lists (e.g., "Positive → similar, Zero → independent, Negative → opposite")

**What you MAY tighten:**
- Remove filler words ("basically", "essentially", "it's important to note that")
- Merge genuinely duplicate sentences that say the exact same thing twice
- Convert long paragraphs into bullet points (same content, better scannability)

**Where compactness comes from (CSS, NOT content removal):**
- Small font size (7.5pt body, 6.5pt code/tables)
- Tight line-height (1.2)
- Tight spacing (margins 0-2px on most elements)
- Multi-column layouts for short lists (`.two-col`, `.three-col`)
- Tables for dense reference data
- These CSS techniques alone can fit a 400-line markdown into 3-4 printed A4 pages without losing a single explanation

### Other content rules

- Keep all code snippets, prompts, and examples intact (these are reference material)
- Use multi-column CSS layout to save space where appropriate (e.g., short bullet lists, mental model summaries)
- Each concept in the source with sub-bullets (Meaning, Why, Formula, Example, Mental Model, AI Connection) should appear as a `<h3>` heading followed by a `<ul>` with ALL those sub-bullets preserved
- "In Plain English" blocks → render as `<div class="tip">` with yellow background
- Section introductions → render as `<p class="section-intro">` in italic

## Spacing (Compact)

- ul: margin 0 0 2px 12px
- li: margin-bottom 0.5px
- h2: margin-top 5px, margin-bottom 2px
- h3: margin-top 4px, margin-bottom 1px
- .prompt: margin 2px 0, padding 2px 5px
- .tip: margin 3px 0, padding 2px 5px

## Print Optimization

- No forced page breaks
- `@media print { body { margin: 0; padding: 0.2cm; } }`
- Headers should not appear alone at bottom of a page — `break-after: avoid`
- Code blocks should not split across pages — `break-inside: avoid`

## Styling Constraints

- Maximum 3 colors: primary (#4F46E5 indigo), warning (#f59e0b amber), text (#1a1a1a near-black)
- No shadows, no rounded corners, no gradients — printer-friendly
- Minimal ink: avoid large filled backgrounds

## Structure Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>[Document Title] — Printable Notes</title>
<style>
  @page { margin: 0.5cm; size: A4; }
  body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 7.5pt; line-height: 1.2; color: #1a1a1a; margin: 0; padding: 0.3cm; }
  h1 { font-size: 11pt; border-bottom: 1.5px solid #333; padding-bottom: 2px; margin-bottom: 4px; margin-top: 0; }
  h2 { font-size: 8.5pt; background: #eee; padding: 1.5px 5px; margin-top: 5px; margin-bottom: 2px; border-left: 2.5px solid #4F46E5; break-after: avoid; }
  h3 { font-size: 7.5pt; margin-top: 4px; margin-bottom: 1px; color: #4F46E5; break-after: avoid; font-weight: bold; }
  ul { margin: 0 0 2px 12px; padding: 0; }
  li { margin-bottom: 0.5px; }
  .tip { background: #fffbe6; border-left: 2px solid #f59e0b; padding: 2px 5px; margin: 3px 0; font-size: 7pt; break-inside: avoid; }
  .prompt { background: #f5f5f5; border: 1px solid #ddd; padding: 2px 5px; margin: 2px 0; font-family: 'Consolas', monospace; font-size: 6.5pt; white-space: pre-wrap; break-inside: avoid; line-height: 1.15; }
  .two-col { column-count: 2; column-gap: 10px; }
  .three-col { column-count: 3; column-gap: 10px; }
  code { background: #e5e7eb; padding: 0 2px; font-size: 6.5pt; }
  @media print { body { margin: 0; padding: 0.2cm; } }
</style>
</head>
<body>
<!-- Content here — preserve all source text exactly -->
</body>
</html>
```

## Visual Diagrams (SVG)

When generating printable HTML for mathematics or technical concept notes, include inline SVG diagrams to visually explain key concepts. These diagrams significantly improve understanding and recall.

### When to Add Diagrams

- **Vector operations** — show arrows for addition (tip-to-tail), subtraction (difference arrow), scalar multiplication (stretching/shrinking)
- **Coordinate spaces** — show labeled axes with example points/vectors plotted
- **Dot product / similarity** — show projection/shadow of one vector onto another
- **Orthogonality** — show two perpendicular arrows with a small square at the angle
- **Norms** — show unit circles/balls for L1 (diamond), L2 (circle), L∞ (square)
- **Span / basis** — show how two vectors span a plane vs one vector spanning a line
- **Matrices** — show transformation effects (rotation, scaling, shearing) on a grid or shape
- **Calculus** — show tangent lines, gradient descent steps on a curve, area under curve
- **Probability** — show Venn diagrams for joint/conditional/marginal probability
- **Any concept** where a picture would clarify what words struggle to explain

### SVG Styling Rules

- Use inline `<svg>` elements (no external files)
- Keep diagrams compact: max width 250px, max height 180px (they share space with text)
- Use the same color palette as the document: primary (#4F46E5), text (#1a1a1a), light gray (#ccc for grid lines), warning (#f59e0b for highlights)
- Use `stroke-width: 1.5` for main elements, `stroke-width: 0.5` for grid/axis lines
- Add arrowheads using `<marker>` definitions for vector arrows
- Label key points and vectors with small text (`font-size: 7pt`)
- Add `break-inside: avoid` to diagram containers
- Wrap each diagram in a `<div class="diagram">` with caption text below

### SVG CSS Addition

Add this to the style block:

```css
.diagram { text-align: center; margin: 4px 0; break-inside: avoid; }
.diagram svg { max-width: 100%; }
.diagram-caption { font-size: 6.5pt; color: #666; margin-top: 1px; font-style: italic; }
.diagram-row { display: flex; justify-content: space-around; flex-wrap: wrap; gap: 8px; margin: 4px 0; break-inside: avoid; }
.diagram-row .diagram { flex: 1; min-width: 120px; max-width: 250px; }
```

### Placement Rules

- Place diagrams immediately after the concept they illustrate (not grouped at the end)
- Use `.diagram-row` to place 2-3 related diagrams side-by-side when comparing (e.g., L1 vs L2 vs L∞ unit balls)
- Don't add a diagram for every concept — only where visual explanation adds clear value over text
- Aim for 4-8 diagrams per printable file for mathematics notes

### Example SVG Pattern

```html
<div class="diagram">
  <svg width="200" height="150" viewBox="0 0 200 150">
    <defs>
      <marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
        <path d="M0,0 L8,3 L0,6 Z" fill="#4F46E5"/>
      </marker>
    </defs>
    <!-- Grid lines -->
    <line x1="20" y1="130" x2="180" y2="130" stroke="#ccc" stroke-width="0.5"/>
    <line x1="20" y1="130" x2="20" y2="10" stroke="#ccc" stroke-width="0.5"/>
    <!-- Vector arrow -->
    <line x1="20" y1="130" x2="140" y2="40" stroke="#4F46E5" stroke-width="1.5" marker-end="url(#arrow)"/>
    <!-- Label -->
    <text x="85" y="75" font-size="7pt" fill="#1a1a1a">v = (3, 4)</text>
  </svg>
  <div class="diagram-caption">Vector (3,4) plotted from origin</div>
</div>
```

---

## Naming Convention

- Source: `BEST_PRACTICES.md` → Output: `BEST_PRACTICES_PRINTABLE.html`
- Source: `generative-ai-agentic-ai.md` → Output: `generative-ai-agentic-ai_PRINTABLE.html`
