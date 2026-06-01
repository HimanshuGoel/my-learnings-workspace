# Project Structure

## Layout

```
/
├── generative-ai-agentic-ai/       # Generative AI, agentic AI, ML/DS practices
├── system-design/                   # System design patterns and architecture
├── __others__/                      # Secondary/archived topic folders
│   ├── angular-react/               # React and Angular learnings
│   ├── java-node-js-asp-net/        # Java, Node.js, ASP.NET learnings
│   ├── mongo-db-my-sql/             # MongoDB and MySQL learnings
│   ├── typescript-javascript/       # TypeScript and JavaScript concepts
│   ├── soft-skills/                 # Communication, leadership, professional growth
│   ├── wellness-philosophy-lifestyle/  # Health, mindset, habits
│   ├── tech-gadgets-games-science/  # Tech trends, gadgets, science
│   └── stumble-upon/                # Memes, images, wallpapers, random finds
├── .kiro/                           # Kiro AI assistant config and steering
├── .vscode/                         # VS Code workspace settings
├── PRACTICALS.md                    # Hands-on practice tasks by domain
├── LICENSE
└── README.md                        # Project overview
```

## Two-Tier Organization

- **Root-level topic folders** (`generative-ai-agentic-ai/`, `system-design/`) are actively maintained and frequently updated.
- **`__others__/`** contains secondary or archived topic folders that are less actively maintained but follow the same internal conventions.

## Topic Folder Convention

Each topic folder follows a consistent structure:

- `README.md` — short description of the folder's scope
- `BEST_PRACTICES.md` — curated best practices for the domain
- `INTERVIEW.md` — interview prep questions (present in some folders)
- `extracted-notes/` — markdown and docx files with detailed notes
  - `{topic}.md` — consolidated extracted notes in markdown
  - `{topic}-part-N-{source}.docx` — source documents (numbered parts with source attribution)
- `__rearrange__/` — raw/unprocessed materials awaiting review and extraction (optional)
- `practices/` — hands-on projects and exercises (optional)
- `certificates/` — relevant certificates and awards (optional)
- `presentations/` — slide decks and PDFs (optional)
- `images/` — visual references (optional)
- `awards/` — award documents (optional, e.g., in soft-skills)
- `resume/` — resume files (optional, e.g., in soft-skills)
- `memes/` — meme images (optional, e.g., in stumble-upon)
- `wallpapers/` — wallpaper images (optional, e.g., in stumble-upon)

## The `__rearrange__/` Subdirectory

Present within individual topic folders. Contains raw, unreviewed learning materials for that topic. This is a personal backlog — content will be reviewed when time permits and selectively moved into the parent topic's proper subfolders. May contain its own `extracted-notes/`, `images/`, or `presentations/` subfolders. Do not treat `__rearrange__/` content as finalized or authoritative.

## Naming Rules

- Folder names: lowercase kebab-case (e.g., `generative-ai-agentic-ai`)
- Markdown files: lowercase kebab-case (e.g., `angular-react.md`)
- Extracted note parts: `{topic}-part-N-{source}.docx` or `{topic}-part-N.pdf`
- Images/memes: lowercase with hyphens (e.g., `tabs-vs-spaces.jpg`)
