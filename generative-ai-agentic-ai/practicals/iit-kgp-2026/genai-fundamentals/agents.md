# Agents

## What Is This?

An AI agent is an LLM-powered system that can autonomously decide which actions to take (call tools, search databases, execute code) in a multi-step reasoning loop to accomplish a goal — going beyond single-turn Q&A to multi-step problem solving.

## Why Does It Exist?

**The Problem:** Standard LLMs can only generate text. They can't:
- Check real-time information (weather, stock prices, latest news)
- Execute actions (send emails, create files, query databases)
- Verify their own answers (can't run code to check if it works)
- Break complex tasks into steps and execute them sequentially

**The Solution:** Give the LLM access to **tools** (functions it can call) and a **reasoning loop** (think → act → observe → repeat). The model decides WHICH tool to use and WHAT arguments to pass, based on the current situation.

## Mental Model

Think of an agent as a **junior developer with access to Stack Overflow, a terminal, and documentation**. You give them a task. They:
1. Think about what they need to do
2. Search for relevant info (tool: search)
3. Try an approach (tool: execute code)
4. Check if it worked (tool: verify)
5. Iterate until done or ask for help

Or: like **a microservice orchestrator** (Kubernetes controller). It observes the current state, decides what action is needed, executes it, observes the new state, and loops until the desired state is achieved.

## How It Works

### The Agent Loop (ReAct Pattern)

```
User Goal: "What's the weather in London and should I bring an umbrella?"
    │
    ▼
┌─────────────────┐
│ THINK (Reason)   │ → "I need to check London weather. I'll use the weather tool."
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ACT (Tool Call)  │ → weather_api("London") → returns "Rainy, 12°C, 80% precipitation"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ OBSERVE (Result) │ → "Got weather data: rainy, 80% rain probability"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ THINK (Reason)   │ → "80% precipitation = bring umbrella. I have enough info to answer."
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ RESPOND          │ → "London is rainy (12°C, 80% chance of rain). Yes, bring an umbrella."
└─────────────────┘
```

### Core Components

| Component | What It Does | Example |
|-----------|-------------|---------|
| LLM (brain) | Reasons, decides next action | GPT-4, Claude |
| Tools | Functions the agent can call | search_web(), calculate(), query_db() |
| Prompt | Defines available tools and behavior | "You have tools: [...]. Use them to answer." |
| Memory | Tracks conversation and past actions | Chat history, scratchpad |
| Orchestrator | Manages the think-act-observe loop | LangChain AgentExecutor |

### Tool Definition

```python
@tool
def search_web(query: str) -> str:
    """Search the internet for current information."""
    return search_api.query(query)

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return str(eval(expression))

@tool
def query_database(sql: str) -> str:
    """Run a SQL query against the customer database."""
    return db.execute(sql)
```

The LLM sees the tool names, descriptions, and parameter schemas. It decides which to call based on the user's question.

### Agent Types

| Type | How It Decides | Best For |
|------|---------------|----------|
| ReAct | Think → Act → Observe → Repeat | General purpose, most common |
| Plan-and-Execute | Plan all steps first, then execute | Complex multi-step tasks |
| Tool-calling | Model directly outputs structured tool calls | Simple tool use (OpenAI function calling) |
| Multi-agent | Multiple specialized agents collaborate | Complex workflows (researcher + coder + reviewer) |

## Where You'll Use This

| Module | How Agents Apply |
|--------|-----------------|
| Module 4 | THE entire module — build agents with LangChain/LangGraph |
| Module 2 | RAG can be a tool an agent uses (along with other tools) |
| Module 5 | Capstone may include an agentic component |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "Agents are autonomous AI" | They're LLMs in a loop with tools. Still need guardrails and limits. |
| "Agents always succeed" | They can get stuck in loops, call wrong tools, or hallucinate tool arguments. |
| "More tools = better agent" | Too many tools confuse the model. 3-7 well-defined tools is optimal. |
| "Agents replace human judgment" | They handle routine multi-step tasks. Complex decisions still need humans. |
| "Agents need fine-tuning" | Most agents work with prompted base models + good tool definitions. |

## Connection to Other Topics

- **Builds on:** Prompting (agent prompt defines tools), RAG (retrieval as a tool), LLMs (the reasoning engine)
- **Uses:** LangChain (AgentExecutor), Tools/APIs (what agents call), Memory (conversation state)
- **Key insight:** Agent = LLM + tools + loop. The "intelligence" comes from the LLM deciding what to do.

## Ready to Move On?

- ☐ I understand the agent loop: Think → Act (tool call) → Observe → Repeat
- ☐ I know what tools are (functions the LLM can call) and how they're defined
- ☐ I can explain the difference between standard prompting and agentic behavior
- ☐ I understand that agents can fail (loops, wrong tools) and need guardrails

Next → **Evaluation** (how to measure if your LLM/RAG/agent is working correctly)
