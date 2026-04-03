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
