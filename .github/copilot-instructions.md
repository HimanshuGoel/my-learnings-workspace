# GitHub Copilot Instructions

## Project Overview

This is a personal knowledge hub for documenting weekly learnings — notes from tutorials, research, best practices, and summarized insights across various technology and non-technology domains. This is a content-only repository with no application code, build system, or runtime.

## Project Structure

```
/
├── angular-react/            # React and Angular learnings
├── docker-kubernetes-cloud/  # Docker, Kubernetes, cloud platforms
├── generative-ai/            # Generative AI tools, prompts, experiments
├── system-design/            # System design patterns and architecture
├── typescript-javascript/    # TypeScript and JavaScript concepts
├── soft-skills/              # Communication, leadership, professional growth
├── wellness-philosophy-lifestyle/  # Health, mindset, habits
├── tech-gadgets-games-science/     # Tech trends, gadgets, science
├── stumble-upon/             # Memes, images, random internet finds
├── __future__/               # Raw materials to review and selectively move into main folders
├── PRACTICALS.md             # Hands-on practice tasks by domain
├── REARRANGE.md              # Content reorganization notes
└── README.md                 # Project overview
```

## Topic Folder Convention

Each topic folder follows a consistent structure:

- `README.md` — short description of the folder's scope
- `BEST_PRACTICES.md` — curated best practices for the domain
- `INTERVIEW.md` — interview prep questions (present in some folders)
- `extracted-notes/` — markdown and docx files with detailed notes
  - `{topic}.md` — consolidated extracted notes in markdown
  - `{topic}-part-N.docx` — source documents (numbered parts)
- `certificates/` — relevant certificates and awards (optional)
- `presentations/` — slide decks and PDFs (optional)

## The `__future__/` Directory

Contains raw, unreviewed learning materials organized by topic. This is a personal backlog — content here will be reviewed when time permits and selectively moved into the corresponding main topic folders. Do not treat `__future__/` content as finalized or authoritative.

## Content Formats

- Markdown (`.md`) — primary format for notes, best practices, and extracted learnings
- Word documents (`.docx`) — source material pending extraction into markdown
- PDFs (`.pdf`) — source material, certificates, and presentations
- Images (`.jpg`, `.jpeg`, `.png`, `.webp`) — certificates, awards, memes, visual references

## Documentation Standards

### Markdown Conventions

- Use `#` for the document title, `##` for sections, `###` for subsections
- Use bullet points (`-`) for key points and lists
- Include code examples with proper language-tagged fenced blocks when relevant
- Keep content accurate, clear, and concise
- Prefer present tense

### Writing Style

- Prefer the doc-as-code approach
- Content should have accuracy, clarity, and conciseness
- Use headings, subheadings, bulleted lists, and clear visual hierarchy
- Include visual elements (screenshots, diagrams, charts) where helpful

## Naming Conventions

- Folder names: lowercase kebab-case (e.g., `docker-kubernetes-cloud`)
- Markdown files: lowercase kebab-case (e.g., `angular-react.md`)
- Extracted note parts: `{topic}-part-N.docx` or `{topic}-part-N.pdf`
- Images: lowercase with hyphens (e.g., `tabs-vs-spaces.jpg`)

## Commit Message Format

```
<type>: <description>

Types: feat, fix, docs, refactor, style, test
```

## Important Notes

- This is a living repository — many files are stubs or work-in-progress and will be populated over time.
- Empty `BEST_PRACTICES.md` or `extracted-notes/*.md` files are intentional placeholders.
- Do not generate application code (React, Angular, etc.) unless explicitly asked — this repo is for documentation and notes only.
- When suggesting content, match the existing style: concise bullet points with practical insights.

## Contact

For feedback or questions: [email]. Issues tracked via [GitHub Issues](https://github.com/HimanshuGoel/my-learnings-app/issues/new/choose).
