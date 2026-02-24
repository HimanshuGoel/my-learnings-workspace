# Extracted Notes

## React

- Micro-frontend approaches -
  - iframes - Isolation Setup: Full, Complexity: Low, SPA Feel: Poor, Performance: Poor, Team Independence: High
  - Page-based (MPA) - Isolation Setup: Full, Complexity: Low, SPA Feel: None (MPA), Performance: Good, Team Independence: High
  - Web Components + Shadow DOM - Isolation Setup: Medium, Complexity: Medium, SPA Feel: Good, Performance: Good, Team Independence: Medium
  - Module Federation - Isolation Setup: None (manual setup required), Complexity: High, SPA Feel: Native, Performance: Good, Team Independence: High
  - single-spa - Isolation Setup: None (manual setup required), Complexity: High, SPA Feel: Native, Performance: Okay, Team Independence: High
  - Server-Side Composition - Isolation Setup: Full, Complexity: High, SPA Feel: Depends (usually not SPA-like), Performance: Great initial load, Team Independence: High
