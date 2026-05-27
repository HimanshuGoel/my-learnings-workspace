# Extracted Notes

## React

- Micro-frontend approaches -
  - iFrames - Isolation Setup: Full, Complexity: Low, SPA Feel: Poor, Performance: Poor, Team Independence: High
  - Page-based (MPA) - Isolation Setup: Full, Complexity: Low, SPA Feel: None (MPA), Performance: Good, Team Independence: High
  - Web Components + Shadow DOM - Isolation Setup: Medium, Complexity: Medium, SPA Feel: Good, Performance: Good, Team Independence: Medium
  - Module Federation - Isolation Setup: None (manual setup required), Complexity: High, SPA Feel: Native, Performance: Good, Team Independence: High
  - Single-SPA - Isolation Setup: None (manual setup required), Complexity: High, SPA Feel: Native, Performance: Okay, Team Independence: High
  - Server-Side Composition - Isolation Setup: Full, Complexity: High, SPA Feel: Depends (usually not SPA-like), Performance: Great initial load, Team Independence: High

## HTML

- HTML is described as a contract between the developer and the machine. When you use a `<form>` tag, you are telling the browser, "This is a collection of user inputs meant to be submitted." When you bypass this with custom JS logic and no semantic tags, you are breaking that contract and making the web less interoperable.

- The article lists practical issues developers often ignore: Scroll "bleeding" outside modals, Poor text wrapping, Default-looking form inputs, Elements feeling slightly misaligned, Layouts that feel "off" but not clearly broken

- The complexity of “responsive images” (using srcset + sizes) is finally going away because browsers are getting smarter—especially with sizes="auto"—so developers no longer need to manually calculate image sizes.

## UX

The 10 UI Patterns That Are Dying (with replacements)

- Setup Wizards - Old: Step-by-step questions (“fill this, then next”). New: AI infers from context (no interrogation)
- Filter Sidebars - Old: Manually selecting filters. New: Natural language queries (“show cheap flights next weekend”).
- Search Results Pages - Old: List of links. New: Direct AI answers / summaries.
- Data Entry Forms - Old: Users type everything. New: AI fills → user reviews. Shift: typing → validation
- Dashboards - Old: Static charts & metrics. New: AI highlights anomalies & insights. Shift: monitoring → understanding
- CRUD Tables - Old: Row-by-row editing. New: Bulk intent + AI diff review. Example: “Update all inactive users”
- FAQ / Help Centers - Old: Browse articles. New: Contextual AI support (chat-based resolution).
- Onboarding Tours - Old: Guided walkthroughs. New: Inline, just-in-time explanations.
- Notification Feeds - Old: Chronological list. New: AI-prioritized briefings. (what matters, not everything)
- “Create New” Blank States - Old: Empty canvas. New: AI-generated first draft. Users edit instead of starting from scratch
