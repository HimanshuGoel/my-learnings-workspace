# Generative AI - Agentic AI

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

- Use AI to think clearer and act faster on everyday problems—not to replace your thinking.

- Don't publish first draft from AI - Add: your opinions, your experience, your tone, Break structure, be a bit messy. Basically: Use AI as a helper, not a replacement for thinking.

- Use MCP when: dynamic tool discovery needed, unknown systems, exploratory agents. Avoid MCP when: workflows are fixed, APIs are known, performance matters.

- Claude Routines let you automate development workflows by turning prompts into always-on AI agents triggered by schedule, API, or events.

- 10 practical ways product teams use Claude Code effectively
  - Work in parallel (biggest productivity boost) - Run multiple Claude sessions (e.g., via git worktrees) to handle different tasks simultaneously instead of sequentially.
  - Start complex work in "plan mode" - Before coding, make Claude analyze and plan first, then execute. Better plans → fewer iterations.
  - Maintain a strong CLAUDE.md (memory file) - Treat it like a team knowledge base: Store rules, patterns, mistakes, Continuously update it after corrections, This reduces repeated errors over time.
  - Create reusable "skills" - If you repeat something often: Turn it into a command (e.g., /techdebt), Share via Git for team reuse, Builds automation over time
  - Let Claude fix bugs autonomously - Instead of over-guiding: Paste logs / errors, Simply say "fix".
  - Improve your prompting skills - Better prompts = better output. Think like: Clear intent, Constraints, Context.
  - Optimize your environment - Use better tooling (terminal setup, shortcuts, workflows) to reduce friction when working with Claude.
  - Use subagents (parallel thinking). Break tasks into smaller agents so Claude can: Analyze, Implement, Review ...in parallel streams.
  - Use Claude for data & analytics. Not just coding—Claude can: Query data, Generate insights, Automate reporting.
  - Treat it as a learning system - Continuously refine: Prompts, Rules, Workflows. Over time, Claude becomes more aligned with your team’s style.

- What is the "Paper Computer"? It’s not a literal device. It’s a workflow / mindset: You write thoughts, problems, or instructions on paper. AI helps interpret, expand, or execute them. The interface becomes your notebook, not a screen. The goal: make computing feel more like thinking and writing, less like operating software.. The notebook becomes the IDE. A future where: your notebook = workspace, your thoughts = input, AI = execution engine. This is closer to how: mathematicians, writers, designers, already work.


## Kiro

- Requirement clarity (WHAT), Design constraints (HOW), Execution plan (TASKS)

- File Importance Why - requirement.md (Prevents over-engineering), design.md	(Keeps upgrade controlled), tasks.md (Executes safely)

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

- Similar to existing tools like Cursor, Claude Code. Many believe: Models are already "good enough". The actual limitation is: Poor context, Weak prompts, Lack of structured inputs. This aligns strongly with: Spec-driven development, Kiro’s design philosophy. Shift from "how to code" → "what to build".

- Your success depends on: requirements.md quality, design.md clarity, task breakdown. Invest heavily in: Spec templates, Review process.

- If you see these, trouble is coming: Specs written casually, No review process, Kiro used for everything, Devs bypassing Kiro, Increasing bugs despite AI.

- Actions: Pick 1 simple feature: Example: Customer search, Follow full flow: Spec → Design → Tasks → Code, Use: ChatGPT for thinking and Kiro for structured generation

- AWS treats systems correctness (ensuring systems behave exactly as intended under all conditions) as a foundational principle for reliability, security, and scalability.

- Instead of relying only on testing, AWS combines: Formal methods (math-based verification), Semi-formal methods (advanced testing techniques). This combination enables high confidence, faster development, and fewer production failures. Tools like TLA+ are hard to learn. They look more like math than programming. Many engineers struggled to adopt them initially

- Circular specification problem = you discover requirements by building, Observer effect = users change requirements after seeing the system. Software development is driven by two fundamentally different but unavoidable forces—internal discovery and external feedback—and successful teams explicitly design their process to handle both, not just one.

- Development is moving from "writing code" → "designing, reviewing, and orchestrating agents"

- A developer spent ~3 hours total vs ~2 days traditionally. Workflow described: 2.5 hours: Planning with AI agents, Iterating on design, 12 minutes: AI generated working implementation, Final step: Multiple AI agents reviewed code quality

- Old world: Coding = main effort, Design = secondary, New world: Design = main effort, Coding = almost automated. Developers become system designers + validators, not coders.

- Hidden Insight: AI Rewards Good Thinkers. If you: Think clearly. Structure problems well.

- Real-world stack: ChatGPT → ideation + PRD, Claude → coding, Kiro → documentation + system reasoning

- Ask me clarifying questions first"Ask Questions First" Pattern. Instead of: Build a payment system. Do: Ask me clarifying questions first. This dramatically improves: Output quality, Architecture decisions.

- AI Spec-Driven delivery transforms SDLC from a linear, labor-intensive process to a structured, repeatable, and auditable lifecycle that scales with the complexity of modern software systems, combining the capabilities of AI with the oversight of human expertise.

- SOPs define how each of these artefacts is produced in a consistent and repeatable way. In summary, SOPs standardize and operationalize the spec-driven approach, making it more consistent, scalable, and efficient.:

- Requirements: Produce requirements.md based on the initiative description, feature details, specifications, and user-provided inputs. Optionally, use the Codebase Summary SOP to understand the existing codebase to provide.

- Design: Created using the PDD SOP, by injecting the requirements.md and, when relevant, the summary markdown files generated by the Codebase Summary.

- Tasks: Generated using the Code Task-Generator SOP.

- Kiro gives the framework. SOPs give the execution discipline

- Framework + Standardization = Scalable development process. SOPs turn AI from an unpredictable assistant into a structured, process-driven engineer by defining exactly how requirements, design, tasks, and code should be generated and executed step by step.

- Steering files are like Cursor rule files

- credit-smart strategies to maximize kiro's potentions

  - Implement tips as per - https://www.youtube.com/watch?v=kS2lnjrFw-M
  - On an existing project clieck agent steering left pane to generate initial docs first based on project
  - Add details for MCP server-info  to use Context 7 whenever using agents or specs
  - Choose if want to have unit tests as optional or not to reduce the credit
  - We can say please start at task 1 and end at task 2.1

- We sql queries we are kind of giving specification what we want

- LLM is kind of compiler for us and creating the abstraction

- what is wrong with vibe coding - tend to lose context, tend to lose bigger picture like architecture or complex components, as a human for us very easy to lose the earlier context or prompts

- For refactoring older codebase use strangled approach by creating api/micorservice to make them self-contained and write spec for it

- A adding layer of abstraction make software development faster and focusing more on user problem

- Main agent and sub-agents so that main context doesn't get pollute.

- Skills vs. mcp servers - mcp server will consume more tokens

- Generate Steering Documentation Early - One of Kiro's features is its ability to generate steering documentation for existing projects. This is not something you have to do, but it’s something that you always should do. As soon as you start working on any project—especially one that's poorly documented—ask Kiro to analyze the codebase and create steering documentation.

- Leverage MCP Server Integration - One of Kiro's most powerful features is its ability to integrate with external tools and data sources through MCP servers. Add MCP servers when you need to interact with data or tools that the language model doesn't know how to access directly. If you're working with project management tools like Jira or need to access specific APIs, setting up the appropriate MCP servers can dramatically expand Kiro's capabilities.

- However, there are times when traditional development approaches are still faster. If you're doing quick debugging, making small tweaks to existing code, or working on problems where you already know the exact solution, it might be quicker to just write the code yourself.

- Kiro will lead to a new paradigm shift in how do we do programming but it will have very less element of creativity which attaracted people earlier in programming. Instead of developer we can become process manager like using the kiro for different project side by side

- Before production - double check, run unit test cases, add another llm for review or writing test, add security related guidelines.

- Agent steering (product features files, project structure files and tech (working with docker, tanstack start, orm, etc))

- We can create multiple session windows in the Kiro ide to have multitasking

- Skills vs. Tools: While MCP servers (tools) provide the "hands" (the ability to read/write to Figma), Skills provide the "brain" (the knowledge of your design system, principles, and workflows).

## Prompt

- Could you summarize this book - i am interested in the main arguments, core principals of author, any interested case studies and author's conclusion.

## Prompt - Research

Step 1 - First plan broad exploration

Act as an organization research.
A 5000-employee professional service firm believes it has a meeting overload problem. EMployees say they are spending too much time in meetings and productivity feels lower.
Before proposing solutions, what dimensions of this problem should we investigate.

Step 2 - Generate specific and measurable research questions

Using the dimensions you listed, generate specific and measurable research questions for a meeting overload audit. Focus on questions that a business operations team could realistically investigate.

Step 3 - Identify data sources

For each research questions, suggest practical data sources and methods for collecting this information. Assume the company has limited analytics resources.

Step 4 - Creating the research plan

Using the research questions and methods we identified, create a four-week research plan for a business operations team conducting a meeting overload audit. The team has limited time and resources, so keep the plan realistic.

Step 5 - Adding external context

Suggest five authoritative articles or studies related to this topic that i use use to further my research. Make sure they'are current and freely accessible. Provide links to the sources.

From this article, extract any quantitative findings or statistics related to meeting, productivity or employee burnout.

Step 6 - generating research questions and hypotheses

Based on the research themes and internal questions we have identified about meeting overload, generate several testable hypotheses related to meetings and employee productivity.

Step 7 - Organizing the knowledge base

Create an annotated bibliography for the three research articles we analyzed earlier. For each resource include - main argument, key statistics, relevance to our meeting overload investigation and any limitations.

Step 8 - 

We are presenting findings from a meeting overload audit to a senior executive team. What do executives typically prioritize when reviewing research findings.

Rewrite these research findings for a senior executive audience. Focus on implications for productivity and organizational performance rather than research methodology.

### Others

Explain it like I am 10 years old.

Explain it like I am a graduate student.

Chose "Study and learn" option and prompt like "I want to learn the difference between IaaS, PaaS and SaaS".

Chose "Quizzes" option and prompt like "Quiz me on cloud computing fundamentals - IaaS, PaaS, SaaS and cloud vs. on-premise".

Chose "Canvas" option and prompt even a particular text from chat response.

- For smaller tasks, use lower-cost models for planning, coordination, clarification and possibly for single file code snippets.