AI behaves like a mid-level dev with amazing memory but weak system intuition. It knows patterns: “Zod schema error”, “Next.js loading.tsx”, “Suspense query fix”. But it doesn’t understand: Why your architecture exists, Long-term trade-offs, Enterprise constraints.


# Angular Application Migration Expert

Phase 1 (10–15 min): migration ownership + past upgrades + approach
Phase 2 (45–60 min): Angular/RxJS/Material deep dive + upgrade design scenario
Phase 3 (20–30 min): testing + accessibility (WCAG 2.1 AA) + debugging
Optional (45–90 min practical): “mini-migration” or “fix broken build/tests” exercise


Great — with your context (very complex **NgModule-heavy** Angular 9 app, **Angular Material**, **services + RxJS**, **reactive forms**, **Karma/Jasmine**, **no SSR**, **no real CI/CD**, and **must meet WCAG 2.1 AA**, and the candidate will be the **sole migration owner**) the interview should heavily test **migration leadership + deep Angular upgrade battle scars**.

Below is an **extremely comprehensive** question bank you can pick from (I’m including *what a strong answer should touch* and *red flags*). I’m also grounding this in internal references you already have around Angular/Material migrations and accessibility standards, plus Angular’s current update guidance. [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1), [\[SBNG-Latest | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1), [\[Angular 6→...and Risks | PDF\]](https://axwaysoftware-my.sharepoint.com/personal/himanshu_goel_sbs-software_com/Documents/Microsoft%20Teams%20Chat%20Files/Angular%206%e2%86%9219%20Upgrade%20%e2%80%93%20Checklist%20of%20Common%20Issues%20and%20Risks.pdf?web=1), [\[angular.dev\]](https://angular.dev/update-guide), [\[angular.dev\]](https://angular.dev/guide/templates/control-flow), [\[Angular 21...deprecated | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEMAABfRF4ogk5QR4LPCRkCDtrGAACldD74AAA%3d&exvsurl=1&viewmodel=ReadMessageItem), [\[angular.dev\]](https://angular.dev/events/v21), [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[Assessment...0908_FOP40 | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-3800's/MSSFOP_RQM-3886/Assessment_20250908_FOP40.html?web=1)

***

## 0) Recommended interview structure (so you cover everything efficiently)

**Phase 1 (10–15 min):** migration ownership + past upgrades + approach  
**Phase 2 (45–60 min):** Angular/RxJS/Material deep dive + upgrade design scenario  
**Phase 3 (20–30 min):** testing + accessibility (WCAG 2.1 AA) + debugging  
**Optional (45–90 min practical):** “mini-migration” or “fix broken build/tests” exercise

***

# 1) Migration ownership & roadmap (SOLE OWNER — must be strong)

### A. Discovery & planning

1.  **If you join on day 1, what are the first 10 things you do before running any `ng update`?**  
    Strong: inventory dependencies, Node/TS versions, lockfile, build commands, baseline tests, identify blockers (Angular Material, custom webpack), create upgrade branch + checkpoints.

2.  **Do you upgrade Angular 9 → 21 directly or version-by-version? Why?**  
    Strong: incremental major-by-major, keep build green at each step; avoid “big bang” because failures compound.

3.  **How do you identify and manage “breaking change hotspots” in a large codebase?**  
    Strong: deprecations, Angular Material breaking changes, TS strictness, RxJS, routing, polyfills, build pipeline.

4.  **What’s your strategy if a third‑party library blocks the upgrade?**  
    Strong: options—upgrade/replace/fork/isolate behind wrapper, remove unused tech to reduce scope (this is explicitly called out as a workload reducer in internal upgrade discussions). [\[NWB - Angular gap | Teams\]](https://teams.microsoft.com/l/message/19:c9886a3209cb4efe87345e0e860903a4@thread.v2/1764766814505?context=%7B%22contextType%22:%22chat%22%7D)

5.  **How do you estimate and communicate risk without CI/CD and with limited tests?**  
    Strong: introduce minimal “safety net” (smoke tests + key flows), define acceptance gates per version.

6.  **What does your “migration checklist” contain for each major version bump?**  
    Strong: build, lint, unit tests, smoke, Material sanity, accessibility quick checks.

7.  **How do you document and do knowledge transfer if you’re the only migration owner?**  
    Strong: ADRs, upgrade log per version, “why” notes, known issues playbook.

***

## B. Concrete upgrade mechanics (expect hands-on knowledge)

8.  **How do you use the Angular Update Guide in practice, and what do you always tick/select for our case (Material + reactive forms)?** [\[angular.dev\]](https://angular.dev/update-guide), [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1)

9.  **When would you use `--force` and what are the risks?**  
    Strong: only when peer deps temporarily block, and you track and reconcile later (internal migration guidance explicitly mentions peer dep conflicts often require `--force`). [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1), [\[SBNG-Latest | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1)

10. **How do you keep the app deployable when build output paths change?**  
    Strong: knows build system migrations can affect `outputPath` expectations; internal notes warn misconfigured output path can work locally but fail in deployment contexts. [\[SBNG-Latest | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1), [\[SBNG-19.0.2 | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-19.0.2.pdf?web=1)

11. **Describe your branch/commit strategy during a long multi-version migration.**  
    Strong: “checkpoint commits” per major, reversible steps.

***

# 2) Angular core depth (NgModule-heavy app)

### A. Modules, boundaries, and architecture

12. **How do you approach migrating a large NgModule architecture safely?**
13. **Feature modules vs shared modules: what anti-patterns create upgrade pain?**
14. **How do you prevent circular dependencies across modules?**
15. **When (if ever) would you introduce standalone components during this migration?**  
    Strong: “not necessary” but can be incremental later—focus on migration stability first.

### B. Change detection & template stability

16. **Explain OnPush vs Default change detection and how RxJS services interact with it.**

17. **How do you debug `ExpressionChangedAfterItHasBeenCheckedError` during upgrades?**  
    (This class of error is a real upgrade pain point in past Angular upgrades.) [\[RE: angula...rs details | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEJAABfRF4ogk5QR4LPCRkCDtrGAAAFlQGyAAA%3d&exvsurl=1&viewmodel=ReadMessageItem), [\[angular 10...rade notes | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEJAABfRF4ogk5QR4LPCRkCDtrGAAAFlQGGAAA%3d&exvsurl=1&viewmodel=ReadMessageItem)

18. **How do you avoid unnecessary re-renders in huge Material-heavy screens?**  
    Strong: trackBy, immutability, slicing views, CDK virtual scroll, avoid expensive pipes.

***

# 3) Angular Material (MDC migration + theming) — *this is a major risk area*

Your environment uses Angular Material, and internal migration notes highlight that **legacy Material components get removed** in later versions and recommend running the **MDC migration schematic**:  
`ng generate @angular/material:mdc-migration` (tick all components) [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1)

### Must-ask questions

19. **What is Angular Material “MDC migration” and what does the schematic change?** [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1)

20. **How do you handle “design is broken but app runs” after MDC migration?**  
    Strong: functional correctness first, then styling pass; internal notes explicitly say design may be broken but that’s acceptable early. [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1)

21. **What theming/scss issues do you expect across major versions?**  
    Strong: prebuilt theme paths may change; custom theme mixins can need rewrites; allocate time. [\[Angular 6→...and Risks | PDF\]](https://axwaysoftware-my.sharepoint.com/personal/himanshu_goel_sbs-software_com/Documents/Microsoft%20Teams%20Chat%20Files/Angular%206%e2%86%9219%20Upgrade%20%e2%80%93%20Checklist%20of%20Common%20Issues%20and%20Risks.pdf?web=1)

22. **How do you validate Material components for accessibility after migration (keyboard/focus/aria)?**  
    Strong: focus traps in dialogs/menus, tab order, aria-labels for icon buttons (see internal a11y assessments showing `aria-label` patterns on Material buttons). [\[Assessment...0908_FOP40 | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-3800's/MSSFOP_RQM-3886/Assessment_20250908_FOP40.html?web=1), [\[Accessibil...tDisplayed | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-2600's/MSSFOP_RQM-2632/AccessibilityAssessment_RQM-856_NoProductDisplayed.html?web=1)

***

# 4) Reactive Forms — scale, correctness, and accessibility

23. **How do you structure very large reactive forms to avoid performance problems?**
24. **Typed forms vs untyped forms: when do you migrate and why?**
25. **Cross-field validation and async validation patterns you use?**
26. **How do you make error messages accessible (WCAG 2.1 AA) — association, focus, announcements?**  
    Strong: programmatic labels, error linkage, predictable focus, no “silent” errors. (Internal standards emphasize WCAG 2.1 AA target and audit guidance.) [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[SBS_Archit...Repository | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBS_Architecture_Repository/SBS_Architecture_Repository.pdf?web=1)

***

# 5) RxJS + services-based state management (your current approach)

### Operator mastery (ask for examples)

27. **Difference between `switchMap`, `mergeMap`, `concatMap`, `exhaustMap` — give a real UI example for each.**
28. **How do you prevent memory leaks in a big app?**
29. **How do you handle cancellation, race conditions, and stale responses?**
30. **Caching strategy in service layer (shareReplay pitfalls)?**
31. **Error handling strategy: where do you catch, where do you rethrow, user messaging?**

### Architecture & maintainability

32. **How do you prevent “observable soup” in components?**
33. **When would you introduce a formal store (NgRx) vs keep services?**  
    Strong: keep scope controlled during migration; avoid introducing new architecture while upgrading.

***

# 6) Testing with Karma/Jasmine — “fix existing if breaks”

You explicitly want someone who can **keep Karma/Jasmine working and fix breakages**.

34. **How do you stabilize a broken test suite after a major upgrade? (order of operations)**

35. **How do you mock Http calls and interceptors cleanly?**

36. **How do you reduce flakiness in async tests?**

37. **When TestBed behavior changes, what do you look for first?**  
    Note: internal Angular 21 pre-release notes mention TestBed-related changes (PlatformLocation + error rethrowing) and TypeScript version constraints—great to see if candidate can reason about test failures from framework shifts. [\[Angular 21...deprecated | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEMAABfRF4ogk5QR4LPCRkCDtrGAACldD74AAA%3d&exvsurl=1&viewmodel=ReadMessageItem)

38. **If coverage drops after migration, how do you recover without boiling the ocean?**  
    Strong: prioritize critical modules/flows, fix highest-value tests first.

***

# 7) Toolchain & build system (even if “nothing as such” in CI/CD)

Internal upgrade docs recommend accepting the **new Angular build system migration** when prompted. [\[SBNG-Latest | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1), [\[SBNG-19.0.2 | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-19.0.2.pdf?web=1)

39. **What build system changes do you expect in modern Angular and how do you troubleshoot build failures?** [\[SBNG-Latest | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1), [\[SBNG-19.0.2 | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-19.0.2.pdf?web=1)
40. **How do you handle peer dependency conflicts safely over many versions?** [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1), [\[SBNG-Latest | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1)
41. **What’s your approach to lockfile hygiene and reproducible builds?**
42. **How would you introduce minimal CI checks even if pipelines aren’t mature?**  
    Strong: at least lint + unit tests + build artifact check.

***

# 8) TypeScript / compiler constraints (very relevant for v21 era)

Internal notes call out: **TypeScript < 5.9 not supported** and potential new type issues (e.g., host bindings). [\[Angular 21...deprecated | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEMAABfRF4ogk5QR4LPCRkCDtrGAACldD74AAA%3d&exvsurl=1&viewmodel=ReadMessageItem)

43. **How do you handle a TypeScript major bump causing hundreds of errors?**
44. **What do you do when host binding type checks start failing?** [\[Angular 21...deprecated | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEMAABfRF4ogk5QR4LPCRkCDtrGAACldD74AAA%3d&exvsurl=1&viewmodel=ReadMessageItem)
45. **Strict mode: enable during migration or after? Why?**  
    Strong: staged—don’t explode scope during already risky migration.

***

# 9) Accessibility (WCAG 2.1 AA) — non-negotiable

Your org references **AA as the target level** for SBS apps.   
And internal accessibility assessments show concrete patterns like Material buttons requiring `aria-label`. [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[SBS_Archit...Repository | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBS_Architecture_Repository/SBS_Architecture_Repository.pdf?web=1) [\[Assessment...0908_FOP40 | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-3800's/MSSFOP_RQM-3886/Assessment_20250908_FOP40.html?web=1), [\[Accessibil...tDisplayed | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-2600's/MSSFOP_RQM-2632/AccessibilityAssessment_RQM-856_NoProductDisplayed.html?web=1)

46. **Explain WCAG 2.1 AA in practical terms: what do you actively verify?** [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[SBS_Archit...Repository | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBS_Architecture_Repository/SBS_Architecture_Repository.pdf?web=1)
47. **Keyboard navigation & focus management for dialogs/menus/sidenavs in Angular Material — how do you validate?**
48. **Accessible names: how do you ensure icon-only buttons/controls have correct labels?** [\[Assessment...0908_FOP40 | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-3800's/MSSFOP_RQM-3886/Assessment_20250908_FOP40.html?web=1), [\[Accessibil...tDisplayed | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-2600's/MSSFOP_RQM-2632/AccessibilityAssessment_RQM-856_NoProductDisplayed.html?web=1)
49. **Forms accessibility: label association, error announcements, required fields, focus on submit errors.**
50. **How do you prevent accessibility regressions during migration (quick checks you run each version)?**
51. **What tooling have you used (axe, Lighthouse, manual screen reader checks) and how do you integrate pragmatically?**
52. **If design breaks after Material MDC migration, how do you ensure accessibility isn’t broken too?** [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1), [\[Assessment...0908_FOP40 | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-3800's/MSSFOP_RQM-3886/Assessment_20250908_FOP40.html?web=1)

***

# 10) “Make them prove it” practical scenarios (best signal for a sole migration owner)

### Scenario 1 — migration plan (whiteboard)

53. **Draft a 6–10 step migration plan from Angular 9 → 21 for a complex NgModule + Material app. Include checkpoints, risks, and how you keep the app usable.**  
    Look for: incremental upgrades, Material MDC early, tests as gate, accessible checks, minimal scope creep. [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1), [\[angular.dev\]](https://angular.dev/update-guide), [\[angular.dev\]](https://angular.dev/guide/templates/control-flow)

### Scenario 2 — Material + theming break

54. **After upgrading Material, the UI looks “visually broken”. What do you do first, and how do you systematically fix?**  
    Look for: run MDC schematic, then theme fixes, then layout regression checklist. [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1), [\[Angular 6→...and Risks | PDF\]](https://axwaysoftware-my.sharepoint.com/personal/himanshu_goel_sbs-software_com/Documents/Microsoft%20Teams%20Chat%20Files/Angular%206%e2%86%9219%20Upgrade%20%e2%80%93%20Checklist%20of%20Common%20Issues%20and%20Risks.pdf?web=1)

### Scenario 3 — tests exploding

55. **Karma/Jasmine tests fail after upgrade — what is your triage order?**  
    Look for: build first, then unit tests, fix environment/polyfills, then flaky async.

### Scenario 4 — accessibility regression

56. **A11y audit reports missing accessible names on buttons — show how you’d fix and prevent recurrence.**  
    Look for: `aria-label`, use native elements, shared component wrappers, automated checks. [\[Assessment...0908_FOP40 | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-3800's/MSSFOP_RQM-3886/Assessment_20250908_FOP40.html?web=1), [\[Accessibil...tDisplayed | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-2600's/MSSFOP_RQM-2632/AccessibilityAssessment_RQM-856_NoProductDisplayed.html?web=1)

***

# 11) Evaluation rubric + red flags (use this while interviewing)

### Strong hire signals

*   Has **done multi-major Angular upgrades** and explains tradeoffs crisply (incremental, checkpoints).
*   Knows **Material MDC migration** and expects styling churn. [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1), [\[Angular 6→...and Risks | PDF\]](https://axwaysoftware-my.sharepoint.com/personal/himanshu_goel_sbs-software_com/Documents/Microsoft%20Teams%20Chat%20Files/Angular%206%e2%86%9219%20Upgrade%20%e2%80%93%20Checklist%20of%20Common%20Issues%20and%20Risks.pdf?web=1)
*   Can **stabilize tests** and won’t hand-wave failures.
*   Treats **WCAG 2.1 AA** as engineering quality, not “add aria-label at end”. [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[Assessment...0908_FOP40 | HTML\]](https://axwaysoftware.sharepoint.com/teams/tm.sbs.FOP/Shared%20Documents/Test%20Evidences/MSSFOP_RQM/MSSFOP_RQM-3800's/MSSFOP_RQM-3886/Assessment_20250908_FOP40.html?web=1)
*   Understands toolchain shifts and TS constraints (e.g., TS >= 5.9 in v21 era notes). [\[Angular 21...deprecated | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEMAABfRF4ogk5QR4LPCRkCDtrGAACldD74AAA%3d&exvsurl=1&viewmodel=ReadMessageItem)

### Red flags

*   “Let’s upgrade straight to 21 and fix later” (scope explosion).
*   Doesn’t know how to approach Material migration (MDC).
*   Thinks accessibility is “QA’s job”.
*   Can’t reason about RxJS operator choices with real examples.
*   Overuses `--force` without a reconciliation plan. [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1), [\[SBNG-Latest | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1)

***

## Extra (useful): internal references you can keep handy during interview

*   [SBNG-Releases.pdf](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1\&EntityRepresentationId=251c068e-09c6-4395-814b-878407d9ebdb) (explicit MDC migration command + sequencing) [\[SBNG-Releases | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-Releases.pdf?web=1)
*   [SBNG-Latest.pdf](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1\&EntityRepresentationId=57de4186-2701-4398-9ec2-ebbc4e15dc8d) / [SBNG-19.0.2.pdf](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-19.0.2.pdf?web=1\&EntityRepresentationId=f3cd11f1-7877-4033-a2df-63ad9063ce4e) (builder migration notes + output path gotcha) [\[SBNG-Latest | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/processed/Digital%20Core%20Components/SBNG-Latest.pdf?web=1), [\[SBNG-19.0.2 | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBNG/SBNG-19.0.2.pdf?web=1)
*   [Angular 21 deprecated](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEMAABfRF4ogk5QR4LPCRkCDtrGAACldD74AAA%3d\&exvsurl=1\&viewmodel=ReadMessageItem\&EntityRepresentationId=c47839b4-81fa-484d-b49e-ecec0744b252) (TS version + TestBed/host binding type-check notes) [\[Angular 21...deprecated | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkAGRjZTExZmFmLWI1ZDgtNDZkMy1hMGQ5LTkxNTc2MDQ0OWNhZQBGAAAAAAA9V310F2RjSqOvQ0tbIQXmBwBfRF4ogk5QR4LPCRkCDtrGAAAAAAEMAABfRF4ogk5QR4LPCRkCDtrGAACldD74AAA%3d&exvsurl=1&viewmodel=ReadMessageItem)
*   Architecture.pdf (states AA target for SBS apps) [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1)

***

If you want, I can also convert this into a **ready-to-print interview scorecard** (same content, condensed into checkbox sections and a scoring rubric) — but you already have everything needed above to start interviewing immediately.


I pulled a bit of internal context first: **your tenant search returned *“2 results for PeopleInferenceAnswer domains, 1 results for File domains, 1405 results for File, External domains”***.   
Most relevant bits I found: [\[office.com\]](https://www.office.com/search?q=Mithilesh+KUMAR), [\[Accessibil...chivedChat | HTML\]](https://axwaysoftware-my.sharepoint.com/personal/parul_bhagat_sbs-software_com/Documents/Microsoft%20Teams%20Chat%20Files/Accessibility%20Standards%20-%20Frontier-Parul%20BHAGAT,Prateek%20AGARWAL,Himanshu%20GOEL-2025-05-17-7199169-ArchivedChat.html?web=1)

*   There are **two** people named Mithilesh; the most complete profile match is **[Mithilesh KUMAR](https://www.office.com/search?q=Mithilesh+KUMAR\&EntityRepresentationId=31ae84f7-018a-4291-b16d-c3f553f0f993)** with email **<mithilesh.kumar@sbs-software.com>** (also found **[Mithilesh YADAV](https://www.office.com/search?q=Mithilesh+YADAV\&EntityRepresentationId=df84ed34-7198-4b67-ab3a-1fa55b634426)**). [\[office.com\]](https://www.office.com/search?q=Mithilesh+KUMAR), [\[office.com\]](https://www.office.com/search?q=Mithilesh+YADAV)
*   Internal docs indicate **AA is the target accessibility conformance level for SBS applications**, based on **WCAG 2.1** (and include practical audit guidance like image alt text). [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[SBS_Archit...Repository | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBS_Architecture_Repository/SBS_Architecture_Repository.pdf?web=1)
*   Angular v21 sources emphasize **zoneless change detection (default)**, **Signal Forms**, **built-in HttpClient defaults**, and modern template control-flow like **@if/@for/@switch**. [\[angular.dev\]](https://angular.dev/events/v21), [\[angular.love\]](https://angular.love/angular-21-whats-new), [\[angular.dev\]](https://angular.dev/guide/templates/control-flow), [\[angular.dev\]](https://angular.dev/update-guide)

***

## First—quick context questions (so I can tailor the interview)

You asked me to ask for context *before* I start. I’ll keep these crisp, but they materially change what “good” looks like for this role:

1.  **App size & complexity**: roughly how many screens/modules and how many devs have touched it?
2.  **Architecture today**: is it **NgModule-heavy**, already partly **standalone**, or mixed?
3.  **State management**: NgRx / Akita / NGXS / services+RxJS / signals already?
4.  **UI libraries**: Angular Material? PrimeNG? AG-Grid? custom design system?
5.  **Forms**: mostly reactive forms, template-driven, or both? Any dynamic form engines?
6.  **Testing**: current unit runner (Karma/Jasmine/Jest/Vitest?), e2e (Cypress/Playwright?) and coverage expectations?
7.  **Build & CI/CD**: Webpack customizations? Nx monorepo? Azure DevOps/GitHub Actions?
8.  **SSR / hydration**: is it SPA-only or using Angular Universal / SSR?
9.  **Key risks**: any critical third-party deps that historically block upgrades?
10. **Accessibility**: is **WCAG 2.1 AA** required for this application specifically (sounds likely)? [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[SBS_Archit...Repository | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBS_Architecture_Repository/SBS_Architecture_Repository.pdf?web=1)
11. **Timeline & approach**: “big-bang” vs incremental releases? parallel feature dev during migration?
12. **Ownership expectations**: will the candidate be the sole migration owner or mentoring a team?

> Even without your answers, I’ll give you a **very comprehensive** interview question bank below (with optional deep-dives depending on what you say).

***

# Extremely Comprehensive Interview Questions (Angular 9 → Angular 21 Migration)

## How to use this bank (recommended structure)

**Round A (10–15 min):** quick screen on fundamentals + migration experience  
**Round B (45–60 min):** deep technical (Angular, RxJS, tooling) + migration design scenario  
**Round C (30 min):** testing + performance + accessibility + collaboration  
**Optional practical (45–90 min):** hands-on debugging or mini-migration exercise

***

## A) Opening / Role-fit (screening)

1.  Walk me through the **largest Angular app** you’ve worked on: size, team, your role.
2.  What’s the **biggest framework upgrade** you’ve done (Angular or otherwise)? What broke?
3.  If you had to upgrade **Angular 9 to 21**, would you do it in one jump or step-wise? Why?
4.  What are the **top 5 risks** you’d flag before touching code?
5.  How do you ensure migration work doesn’t stall feature delivery?
6.  Describe a time you had to persuade stakeholders to accept a technical approach (e.g., incremental).
7.  What do you do when “it builds locally” but fails in CI?
8.  How do you decide when to refactor vs. minimally patch during migration?
9.  What’s your approach to **documentation and knowledge transfer** (explicit JD requirement)?
10. What’s your comfort level owning a migration roadmap end-to-end?

***

## B) Migration strategy & roadmap (Angular 9 → Angular 21)

### Discovery & planning

1.  What files do you inspect first to understand an Angular workspace (angular.json, tsconfig, package.json, etc.)?
2.  How do you inventory **deprecated APIs**, breaking changes, and risky dependencies?
3.  How do you identify third-party libraries blocking upgrades (peer deps, abandoned packages)?
4.  What’s your strategy for **Node/TypeScript/RxJS version alignment** across steps?
5.  What’s your “definition of done” after each upgrade step (build/test/lint/e2e)?
6.  How do you plan **branching** and “upgrade checkpoints” (tags/commits per major)?
7.  How do you decide which modules/features to migrate first?

### Upgrade mechanics & tooling

8.  Explain how `ng update` works at a high level. When would you use `--force` and when would you avoid it? (Red-flag if they always force.) [\[angular.dev\]](https://angular.dev/cli/update), [\[angular.dev\]](https://angular.dev/update)
9.  How do you use the **Angular Update Guide** in practice? [\[angular.dev\]](https://angular.dev/update-guide), [\[angular.dev\]](https://angular.dev/update)
10. What’s your approach to upgrading **one major at a time** vs skipping? When is skipping acceptable?
11. What are common failure modes after upgrading: TypeScript errors, template type-checking, build pipeline, RxJS changes—how do you triage?

### Angular 21 ecosystem changes (must-know topics)

12. What does **zoneless change detection** mean and what kinds of bugs can appear during migration? [\[angular.love\]](https://angular.love/angular-21-whats-new), [\[kellton.com\]](https://www.kellton.com/kellton-tech-blog/angular-21-release-features-benefits-migration-guide), [\[versionlog.com\]](https://versionlog.com/angular/21.0/)
13. If zone.js is no longer default (new apps), how do you reason about UI updates and async tasks? [\[angular.love\]](https://angular.love/angular-21-whats-new), [\[versionlog.com\]](https://versionlog.com/angular/21.0/)
14. What are **Signals**, and how do they affect architecture decisions (state, performance)?
15. What are **Signal Forms** (at a concept level) and when would you adopt them vs staying on classic reactive forms? [\[angular.dev\]](https://angular.dev/events/v21), [\[angular.love\]](https://angular.love/angular-21-whats-new), [\[infoq.com\]](https://www.infoq.com/news/2025/11/angular-21-released/)
16. Explain the new template **control flow** like **@if / @for / @switch** and how you’d migrate from `*ngIf/*ngFor`. [\[angular.dev\]](https://angular.dev/guide/templates/control-flow), [\[angular.io\]](https://angular.io/guide/control_flow), [\[dev.to\]](https://dev.to/cristiansifuentes/mastering-the-new-control-flow-syntax-in-angular-19-dmn)
17. What changes in testing defaults/tooling are you aware of in newer Angular (e.g., modern runners)? (See if they mention shifts away from Karma in v21 ecosystem discussions.) [\[dev.to\]](https://dev.to/turingsoracle/angular-20-to-21-upgrade-the-practical-survival-guide-1km9), [\[kellton.com\]](https://www.kellton.com/kellton-tech-blog/angular-21-release-features-benefits-migration-guide)
18. What build system shifts do you expect as Angular modernizes build tooling (e.g., esbuild/app builder)? [\[versionlog.com\]](https://versionlog.com/angular/21.0/), [\[kellton.com\]](https://www.kellton.com/kellton-tech-blog/angular-21-release-features-benefits-migration-guide)
19. How does “HttpClient available by default” affect app bootstrap/config and tests? [\[versionlog.com\]](https://versionlog.com/angular/21.0/), [\[dev.to\]](https://dev.to/turingsoracle/angular-20-to-21-upgrade-the-practical-survival-guide-1km9)

### Practical migration scenario questions (excellent signal)

20. Suppose the app uses Angular Material, RxJS-heavy state, and custom webpack config. Give me your **week-1 plan**.
21. Show me how you’d create a **migration checklist**: environment, deps, linting, tests, CI.
22. How would you measure whether each step made things better or worse (bundle size, build time, runtime)?
23. If a critical lib is incompatible beyond Angular 14, what options do you propose? (fork, replace, isolate, wrap, micro-frontend boundary).
24. How do you keep the codebase “green” while migrating (feature flags, release trains, migration branch strategy)?

***

## C) Angular fundamentals (deep dive—separates real Angular engineers)

### Components, templates, and change detection

1.  Explain component lifecycle hooks and where they’re typically misused.
2.  Default vs OnPush—tradeoffs, pitfalls, and debugging strategy.
3.  How do you avoid memory leaks in components?
4.  How do you handle change detection with async streams?
5.  `async` pipe vs manual subscribe—when and why?
6.  TrackBy strategies (or `track` in `@for`) and why it matters. [\[angular.dev\]](https://angular.dev/guide/templates/control-flow)
7.  Content projection (`ng-content`) and advanced projection patterns.
8.  ViewChild/ContentChild pitfalls and timing issues.
9.  Structural directives: how they work conceptually; when to build your own.
10. Template type checking—why upgrading often surfaces hidden template issues.

### Routing

11. Lazy loading, preloading strategies, and route guards/resolvers.
12. CanLoad vs CanActivate nuances (legacy vs modern patterns).
13. Router performance considerations and route-level code splitting.
14. Handling deep links, 404s, and auth flows cleanly.
15. Route reuse strategy—what it is, when you need it.

### Forms

16. Reactive forms vs template-driven: pros/cons, migration complexity.
17. Typed forms (how they change dev experience).
18. Dynamic validators, async validators, and performance pitfalls.
19. Form arrays at scale—patterns to keep sane.
20. Cross-field validation and error display patterns.

### DI and providers

21. ProvidedIn root vs module vs component scope: how you decide.
22. Multi providers, injection tokens, and configuration patterns.
23. Interceptors ordering, retry/backoff patterns.
24. When to use `inject()` style vs constructor injection.

### Modules vs Standalone

25. What problems do standalone components solve?
26. Migrating a large NgModule app to standalone—incremental strategy.
27. How do you structure shared UI libs and feature boundaries?

***

## D) TypeScript & modern JavaScript (ES6+)

1.  Explain `unknown` vs `any`, and how stricter TS helps migrations.
2.  Generics in services/models—how you keep them readable.
3.  `readonly`, `as const`, discriminated unions—real examples.
4.  How do TS config changes (strictness) change compile output and bug discovery?
5.  Common TS upgrade issues you’ve handled (lib dom types, node types, etc.).
6.  What’s your approach to typing API responses safely?

***

## E) RxJS & reactive programming (critical for Angular migrations)

### Core concepts

1.  Cold vs hot observables; subject types (Subject/BehaviorSubject/ReplaySubject).
2.  `switchMap` vs `mergeMap` vs `concatMap` vs `exhaustMap`—real scenarios.
3.  `shareReplay` pitfalls (refCount, memory).
4.  Error handling patterns (`catchError`, `retryWhen`) and avoiding silent failures.
5.  Subscription management patterns (takeUntil, async pipe, destroyRef patterns).
6.  Scheduler basics—when it matters.
7.  Backpressure: handling rapid UI events safely.

### Architecture & state

8.  When do you choose RxJS services vs NgRx vs signals?
9.  How do you model state: loading/error/data; caching; invalidation?
10. Preventing “observable soup” in components—how you refactor.
11. Testing RxJS logic—marble tests vs pragmatic tests.

***

## F) Build tooling, Angular CLI, pipelines

1.  Explain your mental model of the Angular build: AOT, optimization, configurations.
2.  How do you manage multiple env configs and secrets safely?
3.  Webpack customization: when it’s justified, when it’s tech debt.
4.  How do you debug build failures after upgrades?
5.  What’s your approach to linting migrations (TSLint→ESLint scenarios)?
6.  Monorepos: Nx vs plain workspaces—why/when.
7.  CI best practices: caching node\_modules, deterministic builds, lockfile discipline.
8.  Versioning strategy for internal libs in a monorepo.
9.  How do you keep build times under control as the app grows?
10. How do you validate that tree-shaking works (sideEffects flags, barrel exports pitfalls)?

***

## G) Testing (unit, integration, E2E) — migration safety net

### Unit testing

1.  Test pyramid for this app: what do you put where?
2.  How do you isolate services with HttpClient (mocks, test controllers)?
3.  Component testing: shallow vs deep; harnesses for Material.
4.  How to test async code reliably (fakeAsync/tick vs async/await).
5.  Snapshot testing pros/cons for Angular.

### Runner/framework decisions

6.  Karma/Jasmine vs Jest vs Vitest—how you pick for speed and maintainability. (See if they’re aware of modern shifts discussed for v21.) [\[dev.to\]](https://dev.to/turingsoracle/angular-20-to-21-upgrade-the-practical-survival-guide-1km9), [\[kellton.com\]](https://www.kellton.com/kellton-tech-blog/angular-21-release-features-benefits-migration-guide)
7.  Migrating tests across runners: common blockers (globals, dom env, config).

### E2E

8.  Cypress vs Playwright selection criteria.
9.  Flaky test triage strategy.
10. Visual regression: do you use it? when is it worth it?
11. Contract testing for APIs (if applicable).

***

## H) Debugging & troubleshooting (pragmatic, senior-ish signal)

1.  Give an example of a “weird” bug you debugged in Angular and how.
2.  How do you debug change detection issues (ExpressionChanged errors)?
3.  What tooling do you use: Angular DevTools, performance profiler, source maps?
4.  How do you trace RxJS streams in production?
5.  How do you handle production-only issues (minified stack traces, sourcemaps in secure setup)?
6.  What’s your strategy for logging without leaking sensitive data?

***

## I) Performance profiling & optimization

1.  Biggest causes of slow Angular apps you’ve seen.
2.  Measuring performance: what metrics matter (LCP/TTI, bundle size, runtime)?
3.  Optimizing large lists (virtual scroll, track, OnPush).
4.  Reducing bundle size (lazy loading, shared deps, removing moment-like libs).
5.  Preventing unnecessary re-renders (memoization patterns, signals).
6.  API performance: caching, debounce, pagination strategies.
7.  How do you validate that an optimization actually helped?

***

## J) Accessibility (WCAG 2.1 AA) — include if it’s in scope (Nice-to-have in JD; likely required)

Given your internal standard references **WCAG 2.1 AA as target** for SBS apps: [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[SBS_Archit...Repository | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBS_Architecture_Repository/SBS_Architecture_Repository.pdf?web=1)

Ask:

1.  What does WCAG “A vs AA vs AAA” mean in practice? (Do they know AA is typically required?) [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[SBS_Archit...Repository | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBS_Architecture_Repository/SBS_Architecture_Repository.pdf?web=1)
2.  How do you ensure **keyboard navigation** works across custom components?
3.  ARIA basics: when to use roles vs native elements; “no ARIA is better than bad ARIA”.
4.  How do you handle accessible names/labels for icon buttons and inputs?
5.  Focus management patterns for dialogs, menus, toasts.
6.  Screen reader testing: what tools/process have you used?
7.  Common Angular accessibility pitfalls (dynamic content announcements, aria-live usage).
8.  Form errors: how do you present them accessibly?
9.  Tables/accordions: what patterns do you follow?
10. During migration, how do you prevent accessibility regressions (automation + manual checks)?
11. Do you integrate automated a11y testing in CI? (axe, eslint plugins, Playwright checks).
12. How do you document a11y decisions and audit results?

Bonus: Angular 21 ecosystem discussions mention improved ARIA/focus tooling and an Angular Aria package preview—see if they track framework direction. [\[angular.dev\]](https://angular.dev/events/v21), [\[infoq.com\]](https://www.infoq.com/news/2025/11/angular-21-released/)

***

## K) Collaboration, documentation, and “migration owner” behaviors

1.  Show me an example of **technical documentation** you created (structure, audience).
2.  How do you do knowledge transfer—pairing, brown bags, ADRs?
3.  How do you communicate risk and timelines without overpromising?
4.  How do you handle disagreements on architecture during migrations?
5.  How do you work with QA/product during a migration release?
6.  If you’re blocked by another team/library, how do you unblock?

***

# Practical exercises (highly recommended)

## 1) Migration design exercise (30–45 min)

**Prompt:** “You inherit an Angular 9 enterprise app. Make a migration plan to Angular 21.”  
Expect them to cover:

*   Step-wise upgrades, dependency audit, CI safety net, risk register, rollout strategy
*   Test strategy and accessibility regression plan
*   Tooling shifts (modern builder/test runner direction) [\[kellton.com\]](https://www.kellton.com/kellton-tech-blog/angular-21-release-features-benefits-migration-guide), [\[versionlog.com\]](https://versionlog.com/angular/21.0/), [\[dev.to\]](https://dev.to/turingsoracle/angular-20-to-21-upgrade-the-practical-survival-guide-1km9)

## 2) Debugging exercise (20–30 min)

Give a small snippet with:

*   Memory leak due to manual subscriptions
*   Wrong `switchMap/mergeMap` usage causing race condition
*   Change detection not updating (OnPush misuse)  
    Ask them to fix + explain tradeoffs.

## 3) Refactor exercise (20–30 min)

Template with nested `*ngIf/*ngFor` → ask them to rewrite using **@if/@for** and track properly. [\[angular.dev\]](https://angular.dev/guide/templates/control-flow)

## 4) Accessibility mini-audit (15–20 min)

Show a dialog/menu form snippet and ask them to identify 6–8 issues: missing labels, focus trap, tab order, aria attributes, error association.

***

# Interview scorecard (useful to stay consistent)

Use these dimensions (rate 1–5 internally):

*   **Migration strategy & risk management**
*   **Angular fundamentals & architecture**
*   **RxJS/TS competence**
*   **Tooling/CI/testing maturity**
*   **Debugging strength**
*   **Performance awareness**
*   **Accessibility (WCAG AA)** [\[Architecture | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Production/SBS%20Docsite%20Documention/29thJuly2025/Digital%20Core%20Engineering/Architecture.pdf?web=1), [\[SBS_Archit...Repository | PDF\]](https://axwaysoftware.sharepoint.com/teams/SKT-TEAM-001/Shared%20Documents/SBCP-COPILOT-AGENT-ARTIFACTS/Documentation/SBS%20Internal%20Portal%20Captured%20PDFs/28-07-2025/sbs-docs-downloads/SBS_Architecture_Repository/SBS_Architecture_Repository.pdf?web=1)
*   **Communication & documentation**

**Red flags**

*   Wants to “upgrade straight to 21” without checkpoints/testing
*   Overuses `--force` / ignores peer dependency warnings
*   Can’t explain RxJS operator differences with examples
*   Treats accessibility as “add aria-labels later”
*   No plan for CI safety net or regression coverage

***

## About “Start sharing CVs… to Mithilesh”

If you want, I can help you draft a short message/email to send internally. I found **[Mithilesh KUMAR](https://www.office.com/search?q=Mithilesh+KUMAR\&EntityRepresentationId=31ae84f7-018a-4291-b16d-c3f553f0f993)** at **<mithilesh.kumar@sbs-software.com>** (and another **[Mithilesh YADAV](https://www.office.com/search?q=Mithilesh+YADAV\&EntityRepresentationId=df84ed34-7198-4b67-ab3a-1fa55b634426)**).   
*(Tell me which Mithilesh you mean, and whether you want email or Teams message.)* [\[office.com\]](https://www.office.com/search?q=Mithilesh+KUMAR), [\[office.com\]](https://www.office.com/search?q=Mithilesh+YADAV)

***

## One quick follow-up (so I tailor the *best* version of this)

Is your application currently **NgModule-based** or already using **standalone components**, and what do you use for **state management** (NgRx vs services/RxJS vs signals)?
