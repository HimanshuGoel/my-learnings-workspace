# Best Practices

- Claude sonnet is the leader model to understand code.

- Don't use ChatGPT to "generate apps." Use it to think better. Explaining tradeoffs. Reviewing architectural ideas. Stress testing decisions. Drafting docs and explanations. It's like rubber‑duck debugging, except the duck answers back. Plus is worth it if you ask good questions. Useless if you don't. Write your problem clearly. Half the solution appears before the answer does.

- A high-quality prompt should include:
  - The Role: Define Claude's persona (e.g., "expert frontend developer and accessibility specialist").
  - The Task: Be specific about what is being built (e.g., "Create a responsive pricing card").
  - The Constraints: Provide strict rules (e.g., "Use Tailwind CSS, use hex code #4F46E5, and no external dependencies").
  - The Edge Cases: Explicitly ask for details like hover states or loading indicators.

- Best practices for Claude Code "skills" (reusable instruction files) so they work efficiently, accurately, and don’t waste tokens.
  1. Keep it focused - One skill = one job. Avoid "do everything" skills. Smaller skills are more accurate and reusable
  2. Use clear role framing - Tell Claude exactly who it is acting as. Be specific (e.g., "UX researcher") instead of vague roles. This improves output quality.
  3. Think of it as a mini-program - Don’t just write instructions. Define: inputs, outputs, steps. Treat it like structured logic, not a casual prompt.
  4. Define clear input & output - Specify: what data the skill expects. what result it should produce. This avoids confusion and randomness
  5. Use structured steps - Break the process into clear steps. Helps Claude follow a consistent workflow. Makes results predictable.
  6. Keep it concise (avoid token bloat) - Large skills = slower + worse performance. Only include what’s necessary. Extra instructions hurt efficiency.
  7. Test and refine - Try the skill on real tasks. Improve based on output quality. Iteration is key to making it reliable.

- During prompt start including "Rewrite our title to attract the attention of our executive team".

- A big task deserve a big prompt - We need to migrate the frontend of this application from Blazor to React. The backend APIs and .Net Aspire orchestration must remain completely unchanged - only the rendering/UI layer changes. Example - Before writing any code, I need you to:
  1. Analyze the existing Blazor frontend architecture - identify all pages, components, routes and shared ui elements.
  2. Map out every API dependency the frontend relies on (endpoints, auth flows, SignalR connections if any)
  3. Produce a detailed migration plan including: proposed React project structure, state management approach, authentication flow and routing strategy.
  4. Define a phased migration order that lets us validate incrementally - which slice do we migrate first and why?
  5. Identify risks, unknowns and decision that need input.

## Sample Prompts - Microsoft Copilot

- Write a Playwright E2E test suite in tests/e2e/ that test the current running Blazon app. Use accessible selectors and test user-visible behavior only - not Blazor-specific DOM. Cover: catalog browsing and filtering, login/logout. Ren them against the current app to confirm they all passes. These tests will our validation contract for every phase of React migration.

- In MS Teams we can ask Copilot to recap the meeting or who are in the calls with their roles and titles.

- In Chat window we can ask about our recent emails and chats for their summarization or tasks to do as per them.

- In MS Word we can point to a company file or PPT and can tell to write a blog by referring those documents.

- Ask the Copilot to prepare for me for the the today's meeting by generating relative content for those meetings.

- To improve the prompt we should refer the Microsoft Prompt Gallery - <https://m365.cloud.microsoft/chat?fromcode=cmmqidzluiz&auth=2>

- Before to it make sure code is locally indexed using command `ctrl + shift + p -> Github Copilot: build local workspace index`

- Please create a project cheat sheet for me that contains the following:
  - Architecture overview - what are the main directories and files?
  - Key components and patterns - what React patterns are being used?
  - APIs and data flow - how does the frontend communicate with the backend?
  - Reusable utilities and helpers - are there existing functions you should use instead of reinventing the wheel?

- Use Notion AI - Organized Thinking at Scale. Summarize long docs. Turn notes into action items. Refactor messy thoughts into clear writing.

- Do you see any components used over and over?

- Create a folder in the root of the project called .github and create a Markdown file in it called copilot-instructions.md containing all of the contents form our project cheat sheet

- Create the authentication context provider to use this authentication system
  - Wrapper you app with AuthProvider
  - use the useAuth hook in components to access authentication state and methods

- The auth state will persist through page reloads using localStorage
  - token management is handled automatically

- Extend the document with common pitfalls and even links to external documentation.

- `#file:UserInventory.js` Show me how the sync functionality works
-
- `#file:UserInventory.js` This UI calls out to an API somewhere to sync. where?

- `/explain` Show me how the sync functionality works. just give me high level details.
-
- `#file:userInventory.js` Generate a summary of everything we talked about. I'm most interested in the function names, their input, output and how they call each other to get to the API call.

- Create a markdown file called sync_journey_map.md which contains an ASCII diagram of the functions used and their relationships where syncing user inventory. Use the above as context if needed.

- Generate a UML diagram using the PlantUML syntax and showing the full dependency tree for the User Inventory Item Sync process.
  Include:
  - Routes
  - Controllers
  - Services
  - External npm packages
  - Relationships between components

- When on the Catalog.js page and I add an item to a batch, how is that price calculated?

## Sample Prompts - Writing or Reading

- Rewrite this to be cleaner and more concise without changing the meaning.

- Restructure this into headings and bullet points for easier scanning.

- Draft a troubleshooting section for a technical audience. the topic is troubleshooting a printer error. use a neutral tone. do not invent features or behavior. assume the reader is a hardware engineer.

- Help me think though what should be included in a good onboarding plan for a new hire. Don't write the plan yet. Just outline the key components.

- Rewrite this email using a professional but friendly tone, written at an 8th grade reading level and avoid passive voice, include three bullet points, don't use jargon, don't sound automated and include a clear call to action.

- Rewrite this email to clear and professional. the goal is to ask for status update without sounding pushy. keep it concise.

- To avoid hallucination write prompt like are there credible studies suggesting multitasking improves cognitive performance? if so, summarize them and note any limitations.

- ELI5 (explain like i'm 5), tl;dr (too long; didn't read) — instant summaries

- Humanize (remove ai voice)

- Rewrite like a sarcastic Redditor

- Rewrite like Alex Hormozi and Steve Jobs

- Before you start, ask me any questions you need so i can give you more context. be extremely comprehensive.

## Sample Prompts - Interviewee

- Act as a expert technical interviewer specializing in senior-level cybersecurity roles. create one strong hybrid behavioral-scenario interview question focused on risk prioritization, stakeholder management under high pressure, and continuous learnability (ability to learn from past experiences, reflect on outcomes and apply lessons to improve future decisions). - start with a behavioral opener: 'tell me about a time when you had to...
