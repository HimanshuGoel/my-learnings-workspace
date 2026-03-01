# Interview

## React

- Context API - consumer, provider, global state, avoid prop drilling, usage (theme, auth, settings), context re-render (useMemo, useReducer, context splitting)

- Redux/Redux toolkit - difference, steps to configure, handle lifecycle in slice, createApi, fetchBaseQuery, when to use (large enterprise UI, complex async flows, share state across many modules, api caching required, predictable state transitions needed), configuration.

- Performance - how to measure (reach devtools profiler, chrome performance tab, lighthouse, web vitals), what causes it (unnecessary re-renders, large bundle size, show api calls, dom size, blocking js).

- Micro-frontend - monolithic vs. micro-frontend, advantages, shell/host app, state management strategy, data sharing, webpack vs vite.

- Code optimization - writing efficient, scalable, low-re-render, small bundle, fast-executing code.

- The fetch API - hands on, global request/response interceptor.

- Error handling - API errors, global exception interceptors, try-catch, handling runtime errors, async issues, UI crashes.

- Class vs Functional components - versions, differences, hooks vs lifecycle methods, new features of @latest React.

- SSR vs CSR vs SSG - differences, use cases, advantages of each, how state management for each.

## Resume Specific

- What compiler changes happened between Angular 8 and Angular 13?

- After migration, how did bundle size change?

- Why did you choose Angular DataTables instead of CDK Virtual Scroll?

- Did you run any accessibility validation after upgrade?

- Give one CSS class name that changed during Angular Material upgrade.

- Which RxJS function got removed?

- What strict template error surprised you most?

- During Angular 8 → 15 migration, what was your upgrade path — did you go version-by-version or jump?

- Angular 8 still had View Engine — what problems did you face when moving to Ivy?

- Which Angular Material changes affected UI after migration?

- What RxJS changes broke your code when moving beyond Angular 10?

- What Node.js and TypeScript version issues did you face?

- Which CLI migration schematics do you remember running?

- Did strict mode introduce template errors? Give example.

- What tests broke first after upgrade?

- How did you validate zero downtime technically? What deployment strategy?

## Angular Migration Expert

- Our Angular 9 enterprise app has lazy modules, Angular Material, accessibility AA requirement, and no UI redesign allowed. You are migration lead. What are your FIRST steps? (Strong sequence - dependency audit, Node/TS alignment, migration roadmap, Material risk check, accessibility validation, Mentions Angular Update Guide, Talks about RxJS breaking changes, CLI migrations, Deprecation analysis, Strict mode enablement, Red flag - Jumping into refactoring code immediately)

- What version did you migrate from and how did you plan the upgrade path? Strong answer (incremental upgrades, Angular Update Guide, dependency matrix, RxJS + Material planning), Red flag (We ran ng update and fixed errors)

- Which Migration scripts you have run, can you remember during the upgrades.

- What was the hardest breaking change during migration? Listen for (Angular Material MDC, strict template errors, RxJS refactor), Weak (generic answer like "some UI fixes")

- Did you face MDC migration issues? Strong signals (form-field spacing changes, CSS class rename, typography config), Red flag (No major UI changes)

- Have you ever rolled back an upgrade? Why?

- Tell me one decision you made during migration that others disagreed with. (Strong candidates discuss: tradeoffs and risk management)

- How angular compiler evolved (Angular 9 introduced Ivy, but the ecosystem changes happened gradually afterwards. View Engine fully removed later (Angular 13) - Libraries had to be Ivy compatible, Partial compilation format introduced, Faster builds + smaller bundles)

- How change detection evolved across Angular versions?

- What problems do Signals solve compared to RxJS?

- Explain the new template control flow like @if / @for / @switch and how you’d migrate from *ngIf/*ngFor.

- Reactive forms vs template-driven: pros/cons, migration complexity. Typed forms (how they change dev experience).

- What RxJS changes broke apps between Angular 9 and later versions? (Strong candidate mentions: RxJS deprecated and removed toPromise(). Use firstValueFrom() or lastValueFrom(). Refactor async logic, pipeable operators, stricter typing, deprecated patterns)

- What RxJS code typically breaks during upgrades? (Real engineers mention: pipeable operator patterns enforced, toPromise() removed, switchMap migration, strict null handling, takeUntil patterns)

- What memory leak patterns appear after upgrading legacy Angular apps? (Strong signals: missing unsubscribe, nested subscriptions, Subject misuse, takeUntil pattern)

- What unit tests broke after Angular upgrade? Strong answer (TestBed config, async timing, harness updates), Red flag (I didn't handle tests)

- What common test breakages occur in Angular upgrades? (Good answer: TestBed changes, async vs fakeAsync issues, zone stabilization)

- What breaks in Jasmine tests during upgrade? (Strong answer: fakeAsync timing issues, fixture.detectChanges behavior, Dependency & Ecosystem Changes (Real Migration Pain), Angular 9 → 19 involves: Node version jumps, TypeScript jumps, ESLint replacing TSLint, RxJS version upgrades, Zone.js updates, High-Value "Real Experience Detector" Questions)

- Unit Tests Start Failing Randomly. Error: 1 timer(s) still in the queue. Expected undefined to be truthy. (Cause - zone.js timing changes + async behavior updates., Strong candidate mentions: fakeAsync adjustments, flush(), async test stabilization)

- Unexpected Change Detection Errors. Error - ExpressionChangedAfterItHasBeenCheckedError (Why migration exposes it - Stricter checks reveal hidden lifecycle issues., Strong answer: lifecycle timing, async updates)

- TSLint deprecated, Angular CLI moved toward ESLint. (What teams did - Installed @angular-eslint, Ran migration schematics)

- How do you test accessibility in Angular Material?

- How did you measure that improvement?" Strong (bundle analyzer, lazy load split, change detection tuning), Weak (We optimized performance)

- How do you reduce bundle size after migration? (Expected: ESBuild / Vite discussion, Lazy loading optimization, Standalone tree shaking)

- Biggest causes of slow Angular apps you’ve seen.

- How did you render 100k rows without UI freeze? (Strong - CDK Virtual Scroll, trackBy, pagination strategy, Red flag - Backend-only solution)

- Give an example of a "weird" bug you debugged in Angular and how.
