# Visual Note-Taking Guide

A practical reference for taking visual/learning notes on paper while working with AI or studying new concepts.

---

## Core Elements (Building Blocks)

| Element         | How to Draw                   | When to Use                                          |
| --------------- | ----------------------------- | ---------------------------------------------------- |
| Box / Rectangle | Simple bordered rectangle     | Represent a concept, component, class, or system     |
| Rounded box     | Rectangle with curved corners | Represent a process, action, or step                 |
| Circle / Oval   | Ellipse shape                 | Represent a starting/ending point, or a central idea |
| Diamond         | Rotated square                | Represent a decision or condition                    |
| Cylinder        | 3D rectangle with curved top  | Represent a database or storage                      |
| Cloud shape     | Wavy irregular blob           | Represent external systems, APIs, or the internet    |
| Stick figure    | Circle + lines                | Represent a user or actor                            |
| Document icon   | Rectangle with wavy bottom    | Represent a file or document                         |

---

## Connectors (Relationships)

| Connector        | How to Draw                  | Meaning                                |
| ---------------- | ---------------------------- | -------------------------------------- |
| Solid arrow →    | Straight line with arrowhead | "Flows to", "calls", "sends data to"   |
| Dashed arrow -→  | Dashed line with arrowhead   | "Depends on", "references", "optional" |
| Double arrow ↔   | Arrows on both ends          | "Bidirectional", "communicates with"   |
| Line (no arrow)  | Plain line                   | "Is associated with", "belongs to"     |
| Thick arrow ⇒    | Bold/thick arrow             | "Transforms into", "results in"        |
| Dotted line .... | Series of dots               | "Weak relationship", "might interact"  |

---

## Annotations and Emphasis

| Technique        | How                              | Purpose                                                                  |
| ---------------- | -------------------------------- | ------------------------------------------------------------------------ |
| Labels on arrows | Write text above/below the line  | Clarify what flows between elements                                      |
| Numbering        | Write 1, 2, 3 on arrows or steps | Show sequence/order                                                      |
| Color coding     | Use 2-3 pen colors               | Distinguish layers (e.g., blue = data, red = errors, green = happy path) |
| Highlighting     | Circle or underline              | Mark key insights or surprises                                           |
| Question marks   | Write "?" next to unclear parts  | Flag items to revisit                                                    |
| Stars ★          | Draw a star                      | Mark important takeaways                                                 |
| Exclamation !    | Write "!"                        | Mark gotchas or warnings                                                 |
| Brackets { }     | Group related items              | Show scope or boundary                                                   |

---

## Highlighting Printed Notes

When reviewing printed `_PRINTABLE.html` pages, keep it minimal — just 2 tools:

| Tool | Use For |
| ---- | ------- |
| **Yellow highlighter** | Formulas + AI Connections (the "what to remember") |
| **Pen (any color)** | Star ⭐ in the margin for "must know for exam" (max 3 per page) |

**Rules:**
- First read: don't highlight anything — just read and absorb
- Second read: highlight selectively (formulas, key AI use cases)
- Star only the critical items — if everything is starred, nothing is
- Skip highlighting "Why It Exists" and section intros — they're context, not recall material
- Tables at the bottom: star 3-4 most important rows, don't highlight entire tables

**The Blank Paper Test (after reading a section):**
1. Take a blank sheet
2. Try to redraw the Memory Map from that section
3. Write down every formula you remember
4. Any gaps = exactly what you need to review

---

## Visual Note Techniques by Scenario

### 1. Understanding a System/Architecture

**Technique: Block Diagram**

```text
┌──────────┐       ┌──────────┐       ┌──────────┐
│  Client  │──────→│  Server  │──────→│    DB    │
└──────────┘       └──────────┘       └──────────┘
                        │
                        ▼
                   ┌──────────┐
                   │  Cache   │
                   └──────────┘
```

- Draw each component as a box
- Use arrows to show data flow direction
- Label arrows with what is being sent (e.g., "HTTP request", "query")
- Add a boundary box (dashed rectangle) around grouped components

### 2. Learning a New Concept

**Technique: Concept Map**

```text
              ┌─────────────┐
              │   RAG       │
              └──────┬──────┘
           ┌─────────┼─────────┐
           ▼         ▼         ▼
     ┌──────────┐ ┌────────┐ ┌──────────┐
     │ Retrieve │ │Augment │ │ Generate │
     └────┬─────┘ └────┬───┘ └────┬─────┘
          ▼             ▼          ▼
     Vector DB     Prompt +    LLM Output
                   Context
```

- Central concept at the top or center
- Branch out to sub-concepts
- Add one-line definitions under each node
- Use "is a", "has a", "uses" as arrow labels

### 3. Following a Process/Algorithm

**Technique: Flowchart**

```text
    ┌───────┐
    │ Start │
    └───┬───┘
        ▼
  ┌───────────┐
  │ Get Input │
  └─────┬─────┘
        ▼
    ◇ Valid? ◇
   /          \
  Yes          No
  ▼             ▼
┌─────┐    ┌────────┐
│Process│   │ Error  │
└──┬──┘    └────────┘
   ▼
┌──────┐
│ End  │
└──────┘
```

- Use diamonds for decisions
- Keep one path going down (happy path)
- Branch sideways for errors/alternatives
- Number the steps if sequence matters

### 4. Comparing Options/Trade-offs

**Technique: Comparison Grid or T-Chart**

```text
    SQL                    vs                NoSQL
┌──────────────┐                    ┌──────────────┐
│ Structured   │                    │ Flexible     │
│ ACID         │                    │ Eventual     │
│ Joins        │                    │ Denormalized │
│ Scale ↕      │                    │ Scale ↔      │
└──────────────┘                    └──────────────┘
        └────────── Use When ──────────┘
         Fixed schema    |    Evolving schema
         Complex queries |    Simple lookups
```

- Two columns side by side
- List properties in each
- Draw a connecting section at the bottom for "when to use which"

### 5. Understanding Code Flow

**Technique: Sequence Diagram (Simplified)**

```text
  User          API           Service         DB
   │              │               │             │
   │──request──→ │               │             │
   │              │──validate──→ │             │
   │              │              │──query──→   │
   │              │              │←──data───   │
   │              │←──result───  │             │
   │←──response── │              │             │
```

- Vertical lines = actors/components (write name at top)
- Horizontal arrows = messages/calls
- Read top to bottom for time sequence
- Add return arrows as dashed lines

### 6. Capturing Mental Models

**Technique: Layered Diagram**

```text
┌─────────────────────────────────┐
│         Application Layer       │
├─────────────────────────────────┤
│         Framework Layer         │
├─────────────────────────────────┤
│         Runtime Layer           │
├─────────────────────────────────┤
│         OS / Hardware           │
└─────────────────────────────────┘
```

- Stack boxes vertically for layers
- Higher = more abstract, lower = more concrete
- Add small notes on the side for "what lives here"
- Draw arrows crossing layers to show which layer talks to which

### 7. Brainstorming/Exploring Ideas

**Technique: Mind Map**

```text
                    ┌── Vector DBs
                    │
        ┌── Storage ┤
        │           └── Graph DBs
        │
  AI ───┼── Models ─── Transformers
        │           └── Diffusion
        │
        └── Tools ──── LangChain
                   └── LlamaIndex
```

- Central topic in the middle
- Branch outward freely
- No need for strict structure
- Add icons or small sketches next to branches

---

## Practical Tips for Better Visual Notes

### Layout Rules

- **Top-to-bottom** for sequences and timelines
- **Left-to-right** for data flows and pipelines
- **Center-outward** for concept maps and mind maps
- **Leave whitespace** — cramped notes are hard to read later
- **Use consistent sizes** — important things get bigger boxes

### Making Them Look Good

- Use a ruler for straight lines (or embrace the hand-drawn style)
- Write labels in CAPS or underline headings
- Keep text inside boxes short (2-4 words max)
- Use indentation to show hierarchy
- Draw borders/frames around complete diagrams

### Pen Strategy (if using multiple colors)

| Color | Use For                                    |
| ----- | ------------------------------------------ |
| Black | Structure, boxes, primary connections      |
| Blue  | Data flow, labels, annotations             |
| Red   | Errors, warnings, gotchas, decision points |
| Green | Happy path, success states, key takeaways  |

### Speed vs Neatness Balance

- During an AI session: speed wins. Messy is fine. Capture relationships.
- After the session (optional): spend 2 minutes redrawing the one diagram that captured the most insight. This redraw is itself a retention exercise.

---

## How Others Use Visual Notes

### Software Engineers

- Whiteboard-style architecture diagrams before writing code
- Sequence diagrams on sticky notes for complex API flows
- Decision trees when choosing between libraries or approaches

### Students (Cornell Method Adapted)

- Left column: key terms/boxes
- Right column: visual relationships and diagrams
- Bottom: one-sentence summary of the page

### Sketchnote Practitioners

- Combine text + icons + containers + connectors on a single page
- Focus on capturing the "story" of a talk or article
- Use typography variation (big/small, bold/light) to create hierarchy

### Bullet Journal / Zettelkasten Users

- One concept per card/page with a small diagram
- Link cards with arrows or reference numbers
- Build a network of visual atomic notes over time

---

## Quick Reference: Which Technique for Which Task

| Task                              | Best Technique                            |
| --------------------------------- | ----------------------------------------- |
| Understanding a new architecture  | Block diagram                             |
| Learning a new concept            | Concept map                               |
| Following a multi-step process    | Flowchart                                 |
| Comparing two approaches          | T-chart / comparison grid                 |
| Tracing code execution            | Simplified sequence diagram               |
| Understanding layers/abstractions | Layered diagram                           |
| Free exploration of a new topic   | Mind map                                  |
| Capturing a key insight           | Single box with a star ★ and one sentence |
