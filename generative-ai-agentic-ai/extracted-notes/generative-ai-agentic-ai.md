# Extracted Notes

## Foundations & Core Concepts

- Generative AI is just brain — can't take any action, but agentic AI is like also having body parts which can take action and have goals, planning, memory, reasoning, autonomy.

- Stable diffusion is a latent text-to-image diffusion model capable of generating realistic photo images given any text input. The model employs a technique called diffusion modelling, which works by incrementally reducing the noise in a sample over several iterations, eventually producing a final output. Diffusion model is a type of model that generates a chain of increasingly noisy images by adding Gaussian noise to an image and then training a model to predict the noise added to an image from one step to following one. It uses a fixed and finite number of steps to generate images, resulting in a stable repeatable image generation.

- Local LLMs are advanced AI models that have been optimized to run on personal devices without the need for constant internet connectivity like GPT-2 Mobile, ALBERT, DistilBERT.

| Traditional Software | AI Systems       |
| -------------------- | ---------------- |
| Deterministic        | Probabilistic    |
| Reproducible         | Non-reproducible |
| Exact logic          | Pattern-based    |
| Debuggable           | Harder to debug  |

- LLM is kind of compiler for us and creating the abstraction.

- In 2026 - models will improve drastically but very marginally, however the tools which use the models will be drastically improved.

## AI Tools & Ecosystem

### Tool Landscape

- These are the repositories that are currently getting a lot of attention in the AI/open-source ecosystem because they focus on: AI agents, Local LLMs, RAG (Retrieval-Augmented Generation), AI workflow builders, Open-source SaaS replacements, Developer productivity

| Priority | Project     | Why                          |
| -------- | ----------- | ---------------------------- |
| 1        | Ollama      | Run models locally           |
| 2        | AnythingLLM | Learn RAG visually           |
| 3        | Flowise     | Similar to low-code thinking |
| 4        | LangGraph   | Advanced agent workflows     |
| 5        | CrewAI      | Agent collaboration          |
| 6        | OpenHands   | Future of coding agents      |
| 7        | Dify        | Production AI apps           |
| 8        | Supabase    | AI app backend stack         |

- Some of the best no-code platforms to build AI agents for free include Zapier, Make, N8N, Relevance AI, MindStudio, Lindy and Voiceflow.

- AI usage scenario based - slides (gamma, beautiful.ai), workflow automation (zapier, n8n), coding (open ai codex, cursor, claude code), diagrams (napkin), app building (lovable, bolt.new, replit), search (perplexity), learning (notebooklm), general brainstorms ideas (chatgpt, gemini).

- Stick with JSON for: Traditional REST/GraphQL APIs, mobile/web app configurations, and systems where strict machine-to-machine deterministic behavior is required. Switch to TOON (or similar) for: AI prompt engineering, RAG (Retrieval-Augmented Generation) datasets, and when asking an LLM to output structured data for internal processing.

- Use MCP when: dynamic tool discovery needed, unknown systems, exploratory agents. Avoid MCP when: workflows are fixed, APIs are known, performance matters.

### Claude & Claude Code

- Claude Routines let you automate development workflows by turning prompts into always-on AI agents triggered by schedule, API, or events.

- 9 important sections every DESIGN.md should contain: Problem Statement, Goals and Non-Goals, Architecture Overview, Data Model / State Design, API Contracts, Key Technical Decisions, Edge Cases and Failure Modes, Testing Strategy, Rollout / Migration Plan.

- A serious setup uses a .claude/ architecture, not just prompts:
  - CLAUDE.md → central memory (short, focused context)
  - rules/ → scoped behavioral constraints (testing, typing, etc.)
  - agents/ → specialized sub-agents (reviewer, evaluator, auditor)
  - skills/ → reusable workflows (like commands)
  - hooks → automated guardrails
  - MCP servers → external integrations

- Using less tokens - Short, clear prompts (Let the AI ask questions instead of guessing), Break tasks into smaller sessions, Avoid long chat history (Start fresh frequently, Prevent context buildup), Use lighter formats (like .txt / .md instead of PDF), Be precise upfront (Reduce rework cycles)

- Two Types of Skills (Important Insight) - Capability Skills (add new abilities, Example: web scraping, file processing), Preference Skills (Encode your way of doing things, Example: PR format, coding standards, documentation style)

- Agent Skills cover end-to-end engineering - Define (Clarify idea, Write spec), Plan (Break into small tasks), Build (Incremental implementation), Verify (Testing (TDD, debugging)), Review (Code quality, security, performance), Ship (CI/CD, release, documentation)

- Claude Code → architecture, frontend refinement, reasoning-heavy work. Codex → implementation acceleration, automation, repetitive engineering tasks, repo-wide changes. Codex for execution, Claude Code for thinking and refinement.

### Multi-Tool Workflows

- Typically, developers start with Claude to shape and refine ideas, then use Cursor to assist with writing code and finally turn to Codex for large-scale bug fixing or comprehensive code review. One developer told me, "I talk to Claude before I open my editor. It helps me clear my head." Once the plan feels right, you move into Cursor. You write code with AI suggestions flowing inline, adjusting and refining as you go. When a task grows boring, Codex steps in. Codex handles the heavy lifting, Cursor keeps me grounded and Claude keeps me sane.

- Real-world stack: ChatGPT → ideation + PRD, Claude → coding, Kiro → documentation + system reasoning

- For smaller tasks, use lower-cost models for planning, coordination, clarification and possibly for single file code snippets.

## Kiro

### Philosophy & Approach

- Requirement clarity (WHAT), Design constraints (HOW), Execution plan (TASKS)

- File Importance Why - requirements.md (Prevents over-engineering), design.md (Keeps upgrade controlled), tasks.md (Executes safely)

- Better model: Prompt → Requirements → Design → Tasks → Code.
  - PO → defines business intent
  - Architect → defines boundaries + constraints
  - AI (Kiro) → generates controlled implementation
  - Engineers → validate, refine, integrate

- Kiro's approach changes AI-powered development from vibe coding to a real, durable, collaboration between the programmer and the AI development agent.

- Love the separation of modes - Vibe for ideation, Spec for clarity, and Agent Hooks for ongoing maintenance. The spec driven approach feels like a natural evolution beyond the typical AI prototype tools.

- Kiro is excellent for stabilizing systems, but for greenfield projects we should first optimize for speed, then gradually introduce Kiro where correctness becomes critical.

- Similar to existing tools like Cursor, Claude Code. Many believe: Models are already "good enough". The actual limitation is: Poor context, Weak prompts, Lack of structured inputs. This aligns strongly with: Spec-driven development, Kiro's design philosophy. Shift from "how to code" → "what to build".

- Kiro will lead to a new paradigm shift in how we do programming but it will have very less element of creativity which attracted people earlier in programming. Instead of developer we can become process manager like using Kiro for different projects side by side.

### Workflows & Best Practices

- A very practical workflow, This gives you Speed + safety balance -
  - Use ChatGPT to Understand problem, explore approaches
  - Use GitHub Copilot to Implement fast
  - Use Kiro to Validate + safely fix critical issues

- Introduce "Human checkpoints". Follow this flow: Spec → (Review) → Design → (Review) → Tasks → (Review) → Code

- Use "Steering files" early by creating .kiro/steering/: coding standards, API patterns, naming conventions, security rules

- Your success depends on: requirements.md quality, design.md clarity, task breakdown. Invest heavily in: Spec templates, Review process.

- If you see these, trouble is coming: Specs written casually, No review process, Kiro used for everything, Devs bypassing Kiro, Increasing bugs despite AI.

- Actions: Pick 1 simple feature: Example: Customer search, Follow full flow: Spec → Design → Tasks → Code, Use: ChatGPT for thinking and Kiro for structured generation

- Before production - double check, run unit test cases, add another LLM for review or writing tests, add security related guidelines.

- However, there are times when traditional development approaches are still faster. If you're doing quick debugging, making small tweaks to existing code, or working on problems where you already know the exact solution, it might be quicker to just write the code yourself.

- Credit-smart strategies to maximize Kiro's potential:
  - Implement tips as per - https://www.youtube.com/watch?v=kS2lnjrFw-M
  - On an existing project click agent steering left pane to generate initial docs first based on project
  - Add details for MCP server-info to use Context7 whenever using agents or specs
  - Choose if want to have unit tests as optional or not to reduce the credit
  - We can say please start at task 1 and end at task 2.1

- We can create multiple session windows in the Kiro IDE to have multitasking

- For refactoring older codebase use strangler approach by creating api/microservice to make them self-contained and write spec for it

### Technical Features

- Tech Design-first works especially well when you have a pre-defined architecture, when you're prototyping to see if something is feasible, or when you're working with strict non-functional requirements that constrain your design choices. It's ideal when the technical approach is the starting point, not the destination. Developers who used Specs to successfully fix bugs shared two characteristics. First, they defined the detailed scenario that caused the error, not just the error message itself. Second, they explicitly stated what should not be modified.

- What makes this work well is the unique way Kiro does testing. Kiro generates property-based tests (PBTs) for all three categories. Tests that verify the current implementation has the bug. Tests that verify your fix resolves it. And tests that verify unchanged behavior continues working exactly as before.

- Kiro and Cursor represent the frontier of this movement, but they take dramatically different approaches to AI-assisted development. With property-aware code evolution, you and Kiro work from the same contract. Kiro drafts the boundary and the hypothesis. You can push back, redraw, tighten the scope, or ask for a different approach.

- Generate Steering Documentation Early - One of Kiro's features is its ability to generate steering documentation for existing projects. As soon as you start working on any project—especially one that's poorly documented—ask Kiro to analyze the codebase and create steering documentation.

- Leverage MCP Server Integration - One of Kiro's most powerful features is its ability to integrate with external tools and data sources through MCP servers. Add MCP servers when you need to interact with data or tools that the language model doesn't know how to access directly.

- Main agent and sub-agents so that main context doesn't get polluted.

- Skills vs. MCP servers - MCP server will consume more tokens.

- Skills vs. Tools: While MCP servers (tools) provide the "hands" (the ability to read/write to Figma), Skills provide the "brain" (the knowledge of your design system, principles, and workflows).

- Agent steering (product features files, project structure files and tech (working with docker, tanstack start, orm, etc))

- Steering files are like Cursor rule files.

## Spec-Driven Development (SDD)

- AI Spec-Driven delivery transforms SDLC from a linear, labor-intensive process to a structured, repeatable, and auditable lifecycle that scales with the complexity of modern software systems, combining the capabilities of AI with the oversight of human expertise.

- Key Components of a Good Spec:
  1. Outcome Definition - What must be true when done
  2. Constraints - Performance, Security, Compliance
  3. Task Breakdown - Step-by-step execution
  4. Verification Criteria - How to prove it works
  5. Architecture Plan - APIs, DB changes, system design

- SOPs define how each of these artefacts is produced in a consistent and repeatable way. In summary, SOPs standardize and operationalize the spec-driven approach, making it more consistent, scalable, and efficient:
  - Requirements: Produce requirements.md based on the initiative description, feature details, specifications, and user-provided inputs.
  - Design: Created using the PDD SOP, by injecting the requirements.md and, when relevant, the summary markdown files generated by the Codebase Summary.
  - Tasks: Generated using the Code Task-Generator SOP.

- Kiro gives the framework. SOPs give the execution discipline.

- Framework + Standardization = Scalable development process. SOPs turn AI from an unpredictable assistant into a structured, process-driven engineer by defining exactly how requirements, design, tasks, and code should be generated and executed step by step.

- SDD = turn specs into executable constraints for AI (not just documentation). Meaning: AI doesn't "guess" from prompts, It follows structured, enforceable specifications. The biggest mistake developers make is adding more instructions instead of better constraints.

- Old mindset: "Let me document everything in CLAUDE.md". New mindset: "Let me control AI behavior with minimal, high-impact rules".

- Where SDD helps: upgrade plans, migration rules, architecture constraints, acceptance criteria, compatibility checks, dependency mapping. Where SDD breaks: changing priorities, shifting framework versions, unexpected library conflicts, new business requirements, evolving architectural understanding. In practice, experienced engineers end up doing: continuous steering, context correction, architectural decisions, and selective overrides. This author argues: SDD is useful, but ultimately temporary, because real engineering is too dynamic for rigid specification trees.

- Instead of writing huge specs, teams should focus on writing: executable facts, tests, constraints, schemas, validations, and measurable behavior.

- AWS treats systems correctness (ensuring systems behave exactly as intended under all conditions) as a foundational principle for reliability, security, and scalability. Instead of relying only on testing, AWS combines: Formal methods (math-based verification), Semi-formal methods (advanced testing techniques). Tools like TLA+ are hard to learn. They look more like math than programming.

- Circular specification problem = you discover requirements by building, Observer effect = users change requirements after seeing the system. Software development is driven by two fundamentally different but unavoidable forces—internal discovery and external feedback—and successful teams explicitly design their process to handle both, not just one.

- What is wrong with vibe coding - tend to lose context, tend to lose bigger picture like architecture or complex components, as a human for us very easy to lose the earlier context or prompts.

- With SQL queries we are kind of giving specification what we want.

- Adding a layer of abstraction makes software development faster and focuses more on user problem.

## AI & The Developer Role

### Evolution of the Developer

- GitHub CEO Thomas Dohmke has outlined four stages of evolution of developers in the AI era:
  - AI Skeptic – Dabbling with code completions and basic prompts.
  - AI Explorer – Using AI for debugging and boilerplate generation
  - AI Collaborator – Co-creating with AI across multi-step tasks
  - AI Strategist – Delegating and verifying complex implementations with multi-agent workflows

- Level 3 – AI Collaborator - AI writes larger chunks/features. You mainly review and guide, not write everything. Risk: you may ship code faster than you truly understand it.
- Level 4 – AI Team (Orchestrator) - You manage multiple AI agents (coding, testing, reviewing). You act like a tech lead/manager, not an individual coder. Focus shifts to system design and orchestration.
- Level 5 – Autonomous ("Dark Factory") - You define requirements → AI builds everything. Humans don't write or even read code. Still rare, but direction industry is heading.

- The golden age of being paid well simply for writing code may be ending, but the golden age for engineers who combine architecture, domain knowledge, AI, and business understanding may just be beginning.

- People who combine coding knowledge with other skills (AI, product thinking, systems design) will stay relevant. Coding is becoming a thinking skill, not just a typing skill.

- The engineers I work with are not writing code from scratch anymore. They are reviewing, testing, validating, and deploying. The AI does the grunt work. They do the parts that actually require human judgment.

- Development is moving from "writing code" → "designing, reviewing, and orchestrating agents".

- A developer spent ~3 hours total vs ~2 days traditionally. Workflow described: 2.5 hours: Planning with AI agents, Iterating on design, 12 minutes: AI generated working implementation, Final step: Multiple AI agents reviewed code quality.

- Old world: Coding = main effort, Design = secondary. New world: Design = main effort, Coding = almost automated. Developers become system designers + validators, not coders.

- AI becomes foundational to how software is built. AI as a baseline expectation, agents as collaborators, open source as a force multiplier. Developers are able to delegate entire tasks to AI agents and orchestrate a fleet of them. Teams of developers working with a swarm of these AI agents, while a developer really orchestrates and ensures everything is going right.

- Move from "Task estimation" to Constraint-based solution design + risk communication.

### AI as a Collaborator (Not a Replacement)

- AI behaves like a mid-level dev with amazing memory but weak system intuition. It knows patterns: "Zod schema error", "Next.js loading.tsx", "Suspense query fix". But it doesn't understand: Why your architecture exists, Long-term trade-offs, Enterprise constraints.

- If your job is implementing what someone else designed, you are in trouble. If your job is designing what needs to be built, understanding systems, validating solutions, and making judgment calls, you are fine. Better than fine. You now have leverage you did not have before. Position yourself as the person who validates, integrates, and makes judgment calls. Let AI do the grunt work. You do the thinking.

- The uncomfortable part is that for every one person who becomes ten times more productive, there are nine people who are no longer needed.

- Use AI to think clearer and act faster on everyday problems—not to replace your thinking.

- AI is gasoline for people who know how to use it.

- Hidden Insight: AI Rewards Good Thinkers. If you think clearly and structure problems well.

- Programming is not dead, typing code was not a job, the job is thinking with brain. It's like airplane pilot — fly plane 95% on autopilot and pilot is monitoring and tasks which need more difficulty which auto-pilot can't do then pilot takes over.

- "To grow skills, people need to go through hardship. They need to develop the muscle to think through problems. How would someone question if AI is accurate if they don't have critical thinking?"

- We are like tailor, we get cloth and based on our talent and tools we can either make it from handkerchief but with better tooling and experience we can create a great craft.

### The UX Illusion & Psychology

- The problem is not only that coding agents make mistakes. The problem is that their human-like conversational style tricks our brains into treating them like coworkers. And once that happens, repeated mistakes feel emotionally irritating in a very human way. Coding agents: speak politely, apologize, reassure you, "reflect" on mistakes, promise improvement, maintain conversational continuity. So psychologically, they feel like a junior teammate, pair programmer, consultant, or coworker. But unlike humans, they: do not truly learn during the session, do not develop judgment, do not reliably remember lessons, do not actually feel accountability. That mismatch creates frustration. This creates a kind of UX illusion: the interface signals "person" but the underlying system behaves like a stochastic text generator and our brains keep bouncing painfully between those two realities.

- Companies that embraced AI too eagerly have had to contend with frustrated customers and declining service quality.

- If AI is going to speak for me, it needs to ask more than just permission... it needs to know when to step back. Because being helpful doesn't give it the right to become me.

### AI & Jobs Impact

- Jobs Most At Risk (High AI Applicability) - AI tackles a lot of repetitive, communication-heavy, or content-focused tasks, making roles like these particularly vulnerable: Interpreters & translators, Historians, Flight attendants/passenger attendants, Writers, authors, and editors, Customer service reps and call operators, Sales agents and PR professionals, Radio DJs and broadcast announcers.

- Jobs Less Vulnerable (Low AI Applicability) - Roles requiring physical presence, manual labor, emotion, or nuanced human judgment remain safer: Phlebotomists, nursing assistants, massage therapists, Roofers, construction laborers, cement finishers, Various machinery operators (dredge, logging equipment, water treatment), Embalmers, bridge/lock tenders, dishwasher staff, cleaning roles, Data scientists and technical analysts.

- Focus on uniquely human skills: Critical thinking, creativity, emotional intelligence, and adaptability still matter. Stay ahead through learning: Build AI literacy, sharpen prompt-writing skills, and understand AI's limits — none of this alone guaranteed job security, but they do offer a competitive edge.

### AI Code Review

- Greptile's stance:
  - Independence: A code review agent should be separate from code generation — akin to an independent auditor — so reviews aren't biased by the same system that wrote the code.
  - Autonomy: Greptile predicts that much of code validation (review + QA) will eventually be fully automated, with human involvement only for high-level decisions.
  - Feedback loops: They envision iterative loops where humans define intent, one AI writes the code, and another AI reviews it until acceptable — minimizing human review overhead.

- AI code review tools are proliferating rapidly, and while many promise improved speed or quality, the real game-changer will be independent, autonomous systems that genuinely integrate into dev workflows rather than just replicating human reviewer tasks.

## AI Content & Creativity

- AI may make low-quality content more abundant, but it also highlights the value of thoughtful, human craft. Rather than replacing deep understanding or creativity, AI could free space for more meaningful, human-driven work—if we choose to value and cultivate it.

- Don't publish first draft from AI - Add: your opinions, your experience, your tone, Break structure, be a bit messy. Basically: Use AI as a helper, not a replacement for thinking.

- AI hasn't yet replaced professional software development—but it has collapsed the cost of building "good enough" tools for yourself, and that alone is already reshaping the software landscape.

- "Breadth first, depth later" is such an underrated mindset in the AI era.

## AI Privacy & Ethics

- The piece warns that as AI becomes a default interface for thinking and asking questions, we may lose one of the most important human freedoms: the ability to think privately and anonymously—and that could subtly but deeply change behavior.

## The "Paper Computer" Concept

- What is the "Paper Computer"? It's not a literal device. It's a workflow / mindset: You write thoughts, problems, or instructions on paper. AI helps interpret, expand, or execute them. The interface becomes your notebook, not a screen. The goal: make computing feel more like thinking and writing, less like operating software. The notebook becomes the IDE. A future where: your notebook = workspace, your thoughts = input, AI = execution engine. This is closer to how mathematicians, writers, designers already work.

## Prompting Techniques

### General Prompting

- Instead of generic prompts, ask things like: "Find performance issues", "Check for security risks", "Suggest edge cases"

- "Ask me clarifying questions first" pattern. Instead of: Build a payment system. Do: Ask me clarifying questions first. This dramatically improves: Output quality, Architecture decisions.

- Could you summarize this book - I am interested in the main arguments, core principals of author, any interested case studies and author's conclusion.

- Explain it like I am 10 years old.

- Explain it like I am a graduate student.

- Choose "Study and learn" option and prompt like "I want to learn the difference between IaaS, PaaS and SaaS".

- Choose "Quizzes" option and prompt like "Quiz me on cloud computing fundamentals - IaaS, PaaS, SaaS and cloud vs. on-premise".

- Choose "Canvas" option and prompt even a particular text from chat response.

### Research Workflow Prompts

- Step 1 - First plan broad exploration: Act as an organization researcher. A 5000-employee professional service firm believes it has a meeting overload problem. Before proposing solutions, what dimensions of this problem should we investigate.

- Step 2 - Generate specific and measurable research questions: Using the dimensions you listed, generate specific and measurable research questions for a meeting overload audit. Focus on questions that a business operations team could realistically investigate.

- Step 3 - Identify data sources: For each research question, suggest practical data sources and methods for collecting this information. Assume the company has limited analytics resources.

- Step 4 - Creating the research plan: Using the research questions and methods we identified, create a four-week research plan for a business operations team conducting a meeting overload audit. The team has limited time and resources, so keep the plan realistic.

- Step 5 - Adding external context: Suggest five authoritative articles or studies related to this topic. Make sure they are current and freely accessible. Provide links to the sources. From this article, extract any quantitative findings or statistics related to meetings, productivity or employee burnout.

- Step 6 - Generating hypotheses: Based on the research themes and internal questions we have identified about meeting overload, generate several testable hypotheses related to meetings and employee productivity.

- Step 7 - Organizing the knowledge base: Create an annotated bibliography for the three research articles we analyzed earlier. For each resource include - main argument, key statistics, relevance to our meeting overload investigation and any limitations.

- Step 8 - Executive communication: We are presenting findings from a meeting overload audit to a senior executive team. What do executives typically prioritize when reviewing research findings. Rewrite these research findings for a senior executive audience. Focus on implications for productivity and organizational performance rather than research methodology.

## AI for Personal Use

- The biggest advantage of using AI as a wellness coach isn't that it knows a million exercises or diets - that information is everywhere. The real advantage is that - it is always available, it is patient, it can adapt plans to your actual life and it can turn vague intentions into clear, repeatable workflows.

- I am based in Noida. I have 60000 for flights and stays. I want a 5-7 day trip between March and May with mountains or hills, good vegetarian food, not insanely crowded. Suggest 5 destinations that fit with rough flight costs and why each place matches this vibe.

- I tried reading book_name and found it too heavy. Suggest 3 alternative books that cover similar ideas in a lighter, more story-driven way.

- Ten years ago: Know Angular = valuable. Today: Know Angular + Architecture = valuable. Tomorrow: Know Architecture + AI workflows + Product thinking = valuable. Framework knowledge is becoming a smaller percentage of total engineering value.
