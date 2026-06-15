# Capstone — Project Ideas

## Evaluation Criteria

| Criteria             | Weight |
| -------------------- | ------ |
| Real-world value     | 30%    |
| Agentic AI usage     | 20%    |
| RAG usage            | 20%    |
| Architecture quality | 15%    |
| Technical depth      | 15%    |

Key rule: Avoid projects that are just `User → LLM → Answer`. Everybody builds those.

---

## Tier 1 — Strongest (Recommended)

### 1. AI-Powered SDLC Assistant ⭐

Automate the software development lifecycle from requirements to deployment.

- **Input:** Requirement document
- **Output:** User stories, acceptance criteria, API contracts, architecture diagrams, test cases, deployment checklist
- **Agent Graph:** Requirements → Architecture → Development → QA → DevOps
- **Covers:** Agentic AI, LangGraph, RAG, Tool Calling, MCP, FastAPI, Enterprise Architecture

Best fit for career growth into AI Architect / GenAI Architect roles.

---

### 2. AI Solution Architect Assistant ⭐

Help developers make technology decisions (RAG vs fine-tuning, vector DB selection, model choice, architecture patterns).

- **Workflow:** Analyze requirements → Search knowledge base → Select architecture → Generate diagram → Estimate cost → Create roadmap
- **Covers:** RAG, Agents, Tool Calling, Vector Search, LangGraph, MCP, FastAPI

---

### 3. Multi-Agent Software Development Assistant ⭐

Multiple specialized agents collaborating on a software project.

- **Agents:** Requirement (user stories), Architect (design), Backend (APIs), Frontend (UI specs), QA (test cases)
- **Workflow:** Requirement → Architect → Developer → QA
- **Covers:** Multi-Agent systems, LangGraph, State management, Orchestration

---

## Tier 2 — Strong

### 4. Enterprise Policy & Compliance Copilot

Employees ask natural language questions about HR/security/legal/compliance policies. Agent retrieves relevant sections, generates answers with citations. Can escalate to HR, draft emails, create compliance reports.

---

### 5. Insurance Knowledge Copilot

Brokers ask "Which policy covers X?", consumers ask "Can I claim Y?" Agent searches policy docs, retrieves clauses, generates answers with citations. High enterprise value.

---

## Tier 3 — Good

### 6. AI Financial Advisor for Indian Families

- **Input:** Salary, SIPs, Expenses, Retirement goal
- **Agents:** Investment, Tax, Risk, Retirement
- **Output:** Complete financial plan
- **Covers:** Multi-agent, tool calling, calculations, RAG

---

### 7. IIT-KGP Learning Companion

Student asks questions, agent finds course notes/transcripts/assignments, generates explanations. Features: quiz generation, interview questions, revision notes, progress tracking.
