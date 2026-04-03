# Generative AI

- AI behaves like a mid-level dev with amazing memory but weak system intuition. It knows patterns: "Zod schema error", "Next.js loading.tsx", "Suspense query fix". But it doesn't understand: Why your architecture exists, Long-term trade-offs, Enterprise constraints.

- People who combine coding knowledge with other skills (AI, product thinking, systems design) will stay relevant. Coding is becoming a thinking skill, not just a typing skill.

- Some of the best no-code platforms to build AI agents for free include Zapier, Make, N8N, Relevance AI, MindStudio, Lindy and Voiceflow.

- AI usage scenario based - slides (gamma, beautiful.ai), workflow automation (zapier, n8n), coding (open ai codex, cursor, claude code), diagrams (napkin), app building (lovable, bolt.new, replit), search (perplexity), learning (notebooklm), general brainstorms ideas (chatgpt, gemini).

- "Breadth first, depth later" is such an underrated mindset in the AI era.

- Typically, developers start with Claude to shape and refine ideas, then use Cursor to assist with writing code and finally turn to Codex for large-scale bug fixing or comprehensive code review. One developer told me, "I talk to Claude before I open my editor. It helps me clear my head." Once the plan feels right, you move into Cursor. You write code with AI suggestions flowing inline, adjusting and refining as you go. When a task grows boring, Codex steps in. Codex handles the heavy lifting, CUrsor keeps me grounded and Claude keeps me sane.

- The engineers I work with are not writing code from scratch anymore. They are reviewing, testing, validating, and deploying. The AI does the grunt work. They do the parts that actually require human judgment.

- AI is gasoline for people who know how to use it.

- If your job is implementing what someone else designed, you are in trouble. If your job is designing what needs to be built, understanding systems, validating solutions, and making judgment calls, you are fine. Better than fine. You now have leverage you did not have before. Position yourself as the person who validates, integrates, and makes judgment calls. Let AI do the grunt work. You do the thinking.

- The uncomfortable part is that for every one person who becomes ten times more productive, there are nine people who are no longer needed.

- Stick with JSON for: Traditional REST/GraphQL APIs, mobile/web app configurations, and systems where strict machine-to-machine deterministic behavior is required. Switch to TOON (or similar) for: AI prompt engineering, RAG (Retrieval-Augmented Generation) datasets, and when asking an LLM to output structured data for internal processing.

## Kiro

- A very practical workflow, This gives you Speed + safety balance -
  - Use ChatGPT to Understand problem, explore approaches
  - Use GitHub Copilot to Implement fast
  - Use Kiro to Validate + safely fix critical issues

- Kiro is excellent for stabilizing systems, but for greenfield projects we should first optimize for speed, then gradually introduce Kiro where correctness becomes critical.

- Better model: Prompt → Requirements → Design → Tasks → Code.
  - PO → defines business intent
  - Architect → defines boundaries + constraints
  - AI (Kiro) → generates controlled implementation
  - Engineers → validate, refine, integrate

- Introduce "Human checkpoints". Follow this flow: Spec → (Review) → Design → (Review) → Tasks → (Review) → Code

- Use "Steering files" early by creating .kiro/steering/: coding standards, API patterns, naming conventions, security rules

- Love the separation of modes - Vibe for ideation, Spec for clarity, and Agent Hooks for ongoing maintenance. The spec driven approach feels like a natural evolution beyond the typical AI prototype tools.

- Kiro's approach changes AI-powered development from vibe coding to a real, durable, collaboration between the programmer and the AI development agent.

- Tech Design-first works especially well when you have a pre-defined architecture, when you're prototyping to see if something is feasible, or when you're working with strict non-functional requirements that constrain your design choices. It's ideal when the technical approach is the starting point, not the destination. Developers who used Specs to successfully fix bugs shared two characteristics. First, they defined the detailed scenario that caused the error, not just the error message itself. Second, they explicitly stated what should not be modified. This is how experienced developers think about bugfixes, they fix what's broken but don't touch anything else.

- What makes this work well is the unique way Kiro does testing. Kiro generates property-based tests (PBTs) for all three categories. Tests that verify the current implementation has the bug. Tests that verify your fix resolves it. And tests that verify unchanged behavior continues working exactly as before. Without these PBTs, it's difficult to check if the agent actually fixed the bug for a comprehensive set of conditions, and that the changes were indeed surgical.

- Kiro and Cursor represent the frontier of this movement, but they take dramatically different approaches to AI-assisted development. With property-aware code evolution, you and Kiro work from the same contract. Kiro drafts the boundary and the hypothesis. You can push back, redraw, tighten the scope, or ask for a different approach. By the time code is written, you've both agreed on what changes and what doesn't. For now, remember: the next time you file a bug, you're drawing a boundary. Draw it with Kiro, and the properties keep the fix on the right side.
