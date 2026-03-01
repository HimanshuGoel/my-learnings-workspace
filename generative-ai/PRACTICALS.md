# Practicals

## Microsoft Copilot

- In MS Teams we can ask Copilot to recap the meeting or who are in the calls with their roles and titles.
- In Chat window we can ask about our recent emails and chats for their summarization or tasks to do as per them.
- In MS Word we can point to a company file or PPT and can tell to write a blog by referring those documents.
- Ask the Copilot to prepare for me for the the today's meeting by generating relative content for those meetings.
- To improve the prompt we should refer the Microsoft Prompt Gallery - <https://m365.cloud.microsoft/chat?fromcode=cmmqidzluiz&auth=2>

## Microsoft Github Copilot

- Add Github Copilot to CLI command of VS Code and then in VS Code CLI command, type this to explain some command like `gh copilot explain "npm start"`.

- Sample Prompts
  
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

## AI Agents

- Some of the best no-code platforms to build AI agents for free include Zapier, Make, N8N, Relevance AI, MindStudio, Lindy and Voiceflow.
