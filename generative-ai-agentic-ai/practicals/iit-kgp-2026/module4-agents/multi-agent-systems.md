# Multi-Agent Systems

## What This Enables

Multi-agent systems coordinate multiple specialized LLM-powered agents to solve problems that are too complex for a single agent — dividing labor, enabling expertise specialization, and allowing agents to critique/validate each other's work. BUT: most applications don't need this. A single agent with multiple tools handles 90% of real use cases.

## Architecture Overview

### When You Actually Need Multi-Agent

```
Single Agent + Tools (default — use this first):
  One LLM with access to search, calculate, code execution, etc.
  Handles: most queries, tool orchestration, simple workflows
  
Multi-Agent (upgrade only when single agent fails):
  Multiple LLMs, each specialized for a domain or role
  Handles: complex workflows requiring different expertise,
           tasks where one agent can't hold enough context,
           quality control (one agent checks another's work)
```

### Multi-Agent Patterns

```
Pattern 1: SUPERVISOR (most common)
  Supervisor agent routes tasks to specialist agents
  ┌─────────────┐
  │  Supervisor  │ (decides who handles what)
  └──────┬──────┘
    ┌────┼────┐
    ▼    ▼    ▼
  [Research] [Code] [Writing]  (specialist agents)

Pattern 2: PIPELINE (sequential handoff)
  Each agent processes, then passes to the next
  [Researcher] → [Writer] → [Editor] → [Publisher]

Pattern 3: DEBATE (agents critique each other)
  Agent A generates → Agent B critiques → Agent A revises
  Useful for quality improvement

Pattern 4: SWARM (peer agents, dynamic routing)
  Agents hand off to each other based on conversation context
  No central supervisor — agents self-organize
```

## Key Patterns & When to Use Each

| Pattern | When | Complexity | Latency | Best For |
|---------|------|-----------|---------|----------|
| Single agent + tools | 90% of cases (start here!) | Low | 2-10s | Most applications |
| Supervisor + specialists | Different domains need different expertise | Medium | 5-20s | Customer support routing |
| Pipeline | Sequential processing with different roles | Medium | 10-30s | Content creation, code review |
| Debate/critique | Need quality validation | Medium | 10-30s | High-stakes outputs |
| Swarm | Dynamic, unpredictable routing needs | High | Variable | Complex customer conversations |

### When NOT to Use Multi-Agent

- **Single agent can do it** — if tools cover the needed capabilities, don't add agents
- **Context is shared** — if all agents need the same context, one agent is more efficient
- **Latency matters** — each agent handoff adds 1-5s of LLM call time
- **Debugging is hard enough** — multi-agent makes debugging exponentially harder
- **Cost multiplies** — N agents = roughly N× the token cost

## Implementation with LangGraph

### Supervisor Pattern

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated, Literal
from operator import add

class MultiAgentState(TypedDict):
    messages: Annotated[list, add]
    next_agent: str
    final_answer: str

# Specialist agents (each is a simple function)
def research_agent(state: MultiAgentState) -> dict:
    """Agent specialized in finding information."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke([
        {"role": "system", "content": "You are a research specialist. Find relevant information."},
        *state["messages"],
    ])
    return {"messages": [response]}

def code_agent(state: MultiAgentState) -> dict:
    """Agent specialized in writing and reviewing code."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke([
        {"role": "system", "content": "You are a coding specialist. Write clean, tested code."},
        *state["messages"],
    ])
    return {"messages": [response]}

def writing_agent(state: MultiAgentState) -> dict:
    """Agent specialized in clear technical writing."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke([
        {"role": "system", "content": "You are a technical writer. Write clear documentation."},
        *state["messages"],
    ])
    return {"messages": [response]}

# Supervisor (routes to the right specialist)
def supervisor(state: MultiAgentState) -> dict:
    """Decide which specialist should handle the current task."""
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(
        # Returns: {"next": "research" | "code" | "writing" | "FINISH"}
    )
    decision = llm.invoke([
        {"role": "system", "content": """Route to the best specialist:
        - research: for finding information, answering questions
        - code: for writing or reviewing code
        - writing: for documentation, explanations, summaries
        - FINISH: when the task is complete"""},
        *state["messages"],
    ])
    return {"next_agent": decision.next}

def route_supervisor(state: MultiAgentState) -> str:
    return state["next_agent"]

# Build graph
graph = StateGraph(MultiAgentState)
graph.add_node("supervisor", supervisor)
graph.add_node("research", research_agent)
graph.add_node("code", code_agent)
graph.add_node("writing", writing_agent)
graph.set_entry_point("supervisor")

graph.add_conditional_edges("supervisor", route_supervisor, {
    "research": "research",
    "code": "code",
    "writing": "writing",
    "FINISH": END,
})
# After each specialist finishes, go back to supervisor
graph.add_edge("research", "supervisor")
graph.add_edge("code", "supervisor")
graph.add_edge("writing", "supervisor")

multi_agent = graph.compile()
```

### Pipeline Pattern (Sequential)

```python
# Content creation pipeline: Research → Write → Edit

def researcher(state):
    """Gather information on the topic."""
    response = research_llm.invoke(state["messages"] + [
        {"role": "user", "content": f"Research this topic thoroughly: {state['topic']}"}
    ])
    return {"research_output": response.content}

def writer(state):
    """Write content based on research."""
    response = writer_llm.invoke([
        {"role": "user", "content": f"Write an article based on this research:\n{state['research_output']}"}
    ])
    return {"draft": response.content}

def editor(state):
    """Review and improve the draft."""
    response = editor_llm.invoke([
        {"role": "user", "content": f"Edit this draft for clarity and accuracy:\n{state['draft']}"}
    ])
    return {"final_output": response.content}

# Linear pipeline
graph = StateGraph(PipelineState)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.add_node("editor", editor)
graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", "editor")
graph.add_edge("editor", END)
```

### Debate Pattern (Critique + Revise)

```python
def generator(state):
    """Generate initial response."""
    response = llm.invoke(state["messages"])
    return {"draft": response.content, "iteration": state.get("iteration", 0) + 1}

def critic(state):
    """Critique the draft."""
    critique = llm.invoke([
        {"role": "user", "content": f"Critique this response for accuracy and completeness:\n{state['draft']}"}
    ])
    return {"critique": critique.content}

def reviser(state):
    """Revise based on critique."""
    revised = llm.invoke([
        {"role": "user", "content": f"Original:\n{state['draft']}\n\nCritique:\n{state['critique']}\n\nRevise:"}
    ])
    return {"draft": revised.content}

def should_stop(state) -> str:
    if state["iteration"] >= 3 or "no issues" in state.get("critique", "").lower():
        return END
    return "critic"

graph.add_conditional_edges("reviser", should_stop, {END: END, "critic": "critic"})
```

## State Management & Memory

- **Shared state:** All agents read/write the same state dict (simple coordination)
- **Message passing:** Agents communicate through the messages list (natural for LLMs)
- **Separate contexts:** Each agent can have its own system prompt (specialization)
- **Accumulation:** Use Annotated[list, add] for results that each agent contributes to

## Error Handling & Guardrails

| Failure Mode | Symptom | Fix |
|-------------|---------|-----|
| Supervisor loops between agents | Task bounces without progress | Max handoff counter (limit to 5-10 transitions) |
| Agent generates for wrong role | Code agent writes prose | Stronger system prompts, structured output |
| Agents contradict each other | Conflicting information in pipeline | Add reconciliation step, use debate pattern |
| Token budget explodes | Long messages passed between all agents | Summarize between handoffs, limit context per agent |
| Single agent failure cascades | One broken agent blocks the pipeline | Add timeout + fallback per agent node |
| Over-engineering | Multi-agent for simple task | Start with single agent, measure if quality is insufficient |

## Testing & Debugging

```python
# Test supervisor routing:
def test_supervisor_routes_code_to_code_agent():
    result = multi_agent.invoke({"messages": [HumanMessage("Write a sorting function")]})
    # Verify code agent was invoked (check message trail or logging)

# Test pipeline end-to-end:
def test_pipeline_produces_output():
    result = pipeline.invoke({"topic": "Kubernetes deployments", "messages": []})
    assert result["final_output"]  # Non-empty
    assert len(result["final_output"]) > 200  # Substantive

# Debug with LangSmith: See every agent's inputs/outputs in a trace
```

## Production Considerations

### Latency
- Each agent handoff = 1 LLM call (1-3s)
- Supervisor pattern: 2-6 handoffs typical = 5-20s total
- Pipeline: N agents × 1-3s = linear scaling
- For user-facing: Stream intermediate results ("Researching...", "Writing...")

### Cost
- N agents each making LLM calls = N× cost vs single agent
- Supervisor adds overhead (routing decision = extra LLM call each step)
- Budget: Set max_steps and track per-conversation token usage

### When to Deploy Multi-Agent vs Single Agent

| Metric | Single Agent | Multi-Agent |
|--------|-------------|-------------|
| Task complexity | Simple to moderate | Complex, multi-domain |
| Latency requirement | < 5s | 10-30s acceptable |
| Quality improvement | N/A | > 20% over single agent |
| Development cost | Low | 3-5× more code to maintain |
| Debugging ease | Manageable | Significantly harder |

## Integration Points

- **Module 2 (RAG):** Each specialist agent can have its own RAG retriever
- **Module 3 (Fine-Tuning):** Specialist agents can use fine-tuned models for their domain
- **Module 4 (LangGraph):** LangGraph is the orchestration layer for all multi-agent patterns
- **Module 5 (Deployment):** Serve multi-agent graph as single API endpoint

## Architecture Decision Record

**Decision:** Default to single agent + tools. Use multi-agent only when proven necessary.

**Why:** Multi-agent adds latency (2-5× slower), cost (N× more LLM calls), and debugging complexity (exponentially harder). Most applications don't need it. The single agent with good tools and a strong system prompt handles 90% of cases.

**When multi-agent is justified:**
1. Single agent quality is demonstrably insufficient (measured, not assumed)
2. Task naturally decomposes into independent expertise domains
3. Latency of 10-30s is acceptable for the use case
4. You have the engineering capacity to maintain and debug the system

**Trade-off accepted:** Occasionally miss the quality boost multi-agent could provide for edge cases. Worth it for simplicity, speed, and maintainability.
