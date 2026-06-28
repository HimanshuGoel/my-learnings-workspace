# Agent Architectures

## What This Enables

Choosing the right agent architecture determines whether your system handles complex tasks reliably or spirals into infinite loops and wasted tokens. This is the foundational decision — every subsequent topic (tools, memory, multi-agent) builds on the architecture you pick here.

## Architecture Overview

### The Agent Loop (All Patterns Share This)

```text
┌─────────────────────────────────────────────────────┐
│                    AGENT LOOP                         │
│                                                      │
│  Input ──→ LLM Reasoning ──→ Action Decision         │
│              ▲                      │                 │
│              │                      ▼                 │
│         Observation ◄──── Execute Action (tool/stop)  │
│                                                      │
│  Loop terminates when: LLM decides "I have enough"   │
│  Loop FAILS when: max iterations hit, or cost budget │
└─────────────────────────────────────────────────────┘
```

### Pattern Family Tree

```text
Simple ──────────────────────────────────────────── Complex
   │                                                    │
   ▼                                                    ▼
ReAct          Tool-Calling       Plan-and-Execute    LLM Compiler    Reflexion
(think+act)    (structured)       (plan then do)      (parallel)      (self-critique)
   │                │                   │                  │               │
   └── Default ─────┘                   │                  │               │
       for most                         │                  │               │
       use cases                   Multi-step         Latency-         Quality-
                                   complex tasks      critical         critical
```

## Key Patterns & When to Use Each

| Pattern | How It Works | When to Use | Complexity | Latency | Reliability | Max Steps |
|---------|-------------|-------------|------------|---------|-------------|-----------|
| **ReAct** | Think → Act → Observe → Repeat | Default for most tasks | Low | Low (1-5 steps) | High | 3-10 |
| **Tool-Calling** | LLM outputs structured function calls | API integration, structured output | Low | Low | High | 1-5 |
| **Plan-and-Execute** | Create plan first, then execute steps | Complex multi-step tasks | Medium | High (planning overhead) | Medium | 10-30 |
| **LLM Compiler** | Decompose into parallel-executable tasks | Latency-critical complex tasks | High | Medium (parallelism) | Medium | 5-20 |
| **Reflexion** | Execute → Evaluate → Retry with feedback | Quality-critical tasks, code gen | High | Very High (multiple passes) | High (eventually) | 3-5 attempts |

### Decision Flowchart

```text
Is the task simple (1-3 tool calls)?
  YES → ReAct or Tool-Calling Agent
  NO ↓

Does it need a multi-step plan?
  YES → Plan-and-Execute
  NO ↓

Can subtasks run in parallel?
  YES → LLM Compiler
  NO ↓

Does quality matter more than speed?
  YES → Reflexion (self-critique loop)
  NO → Plan-and-Execute with step budget
```

## Implementation with LangGraph

### Pattern 1: ReAct Agent (The Default — Start Here)

```python
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


# --- State Definition ---
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# --- Tools ---
@tool
def search_database(query: str) -> str:
    """Search the internal knowledge base for information."""
    # Simulated — replace with real DB search
    return f"Found 3 results for: {query}"


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression))  # In production: use a safe parser
    except Exception as e:
        return f"Error: {e}"


tools = [search_database, calculate]


# --- LLM with tools bound ---
llm = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)


# --- Nodes ---
def call_model(state: AgentState) -> dict:
    """The reasoning node — LLM decides what to do next."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# --- Conditional Edge: should we continue or stop? ---
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


# --- Build the Graph ---
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")  # After tool execution, go back to agent

app = workflow.compile()

# --- Run ---
result = app.invoke({
    "messages": [HumanMessage(content="What's 25 * 4 + 10?")]
})
print(result["messages"][-1].content)
```

### Pattern 2: Plan-and-Execute (For Complex Tasks)

```python
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


class PlanExecuteState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    plan: list[str]           # The steps to execute
    current_step: int         # Which step we're on
    results: list[str]        # Results from each step
    final_answer: str         # The synthesized answer


planner_llm = ChatOpenAI(model="gpt-4o", temperature=0)
executor_llm = ChatOpenAI(model="gpt-4o", temperature=0)


def create_plan(state: PlanExecuteState) -> dict:
    """Planner: decompose the task into steps."""
    task = state["messages"][-1].content
    response = planner_llm.invoke([
        SystemMessage(content=(
            "You are a planner. Break the task into 3-7 sequential steps. "
            "Return ONLY a numbered list. Each step should be independently executable."
        )),
        HumanMessage(content=f"Task: {task}"),
    ])
    steps = [line.strip() for line in response.content.split("\n") if line.strip()]
    return {"plan": steps, "current_step": 0, "results": []}


def execute_step(state: PlanExecuteState) -> dict:
    """Executor: execute the current step."""
    step = state["plan"][state["current_step"]]
    context = "\n".join(state["results"]) if state["results"] else "No previous results."

    response = executor_llm.invoke([
        SystemMessage(content="Execute this step. Use the context from previous steps."),
        HumanMessage(content=f"Step: {step}\n\nPrevious results:\n{context}"),
    ])
    new_results = state["results"] + [f"Step {state['current_step'] + 1}: {response.content}"]
    return {"results": new_results, "current_step": state["current_step"] + 1}


def synthesize(state: PlanExecuteState) -> dict:
    """Combine all step results into a final answer."""
    all_results = "\n".join(state["results"])
    response = executor_llm.invoke([
        SystemMessage(content="Synthesize these step results into a final coherent answer."),
        HumanMessage(content=all_results),
    ])
    return {"final_answer": response.content}


def should_continue_executing(state: PlanExecuteState) -> str:
    if state["current_step"] >= len(state["plan"]):
        return "synthesize"
    return "execute"


# --- Build Graph ---
workflow = StateGraph(PlanExecuteState)
workflow.add_node("plan", create_plan)
workflow.add_node("execute", execute_step)
workflow.add_node("synthesize", synthesize)

workflow.set_entry_point("plan")
workflow.add_edge("plan", "execute")
workflow.add_conditional_edges("execute", should_continue_executing, {
    "execute": "execute",
    "synthesize": "synthesize",
})
workflow.add_edge("synthesize", END)

app = workflow.compile()
```

## State Management & Memory

| Pattern | State Complexity | What to Persist |
|---------|-----------------|-----------------|
| ReAct | Low — just messages | Message history (for multi-turn) |
| Plan-and-Execute | Medium — plan + progress | Plan, current step, intermediate results |
| Reflexion | High — attempts + evaluations | All attempts, evaluation scores, best result |

**Key insight:** ReAct state is just a message list. Plan-and-Execute needs structured state (plan array, step counter). Choose your state complexity based on how much the agent needs to "remember" within a single task.

## Error Handling & Guardrails

| Failure Mode | Symptom | Mitigation |
|-------------|---------|------------|
| Infinite loop | Agent keeps calling same tool | Max iteration limit (default: 10) |
| Tool hallucination | Agent calls tool that doesn't exist | Strict tool binding, validate before execute |
| Plan too granular | 20+ steps for a simple task | Limit plan to 7 steps max, force replanning |
| Plan too vague | "Do the thing" as a step | Few-shot examples in planner prompt |
| Wrong pattern choice | ReAct for 15-step research task | Architecture selection checklist (above) |
| Cost spiral | Agent burns $5 on a $0.10 task | Token budget per invocation, step budget |

### Step Budget Implementation

```python
MAX_ITERATIONS = 10

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    # Count tool calls so far
    tool_call_count = sum(1 for m in state["messages"] if hasattr(m, "tool_calls") and m.tool_calls)

    if tool_call_count >= MAX_ITERATIONS:
        return END  # Force stop — prevent infinite loops
    if last_message.tool_calls:
        return "tools"
    return END
```

## Testing & Debugging

```python
# Test an agent by asserting on trajectory, not just final output
def test_react_agent():
    result = app.invoke({
        "messages": [HumanMessage(content="What's 25 * 4?")]
    })
    messages = result["messages"]

    # Assert: agent used the calculate tool
    tool_calls = [m for m in messages if hasattr(m, "tool_calls") and m.tool_calls]
    assert len(tool_calls) >= 1, "Agent should have called a tool"
    assert tool_calls[0].tool_calls[0]["name"] == "calculate"

    # Assert: final answer is correct
    assert "100" in messages[-1].content

    # Assert: didn't take too many steps (efficiency)
    assert len(messages) <= 5, "Simple calculation shouldn't need 5+ messages"
```

## Production Considerations

| Concern | ReAct | Plan-and-Execute | Reflexion |
|---------|-------|-------------------|-----------|
| Avg latency | 2-5s | 10-30s | 30-120s |
| Avg cost per task | $0.01-0.05 | $0.05-0.20 | $0.20-1.00 |
| Predictability | High | Medium | Low |
| When it fails | Wrong tool choice | Bad plan | Never converges |
| Recovery | Retry the single call | Replan from failed step | Fallback to simpler agent |

**Production rule:** Start with ReAct. Only upgrade to Plan-and-Execute when you can demonstrate that ReAct fails on your specific task class. Only use Reflexion for high-value tasks where quality justifies 10x cost.

## Integration Points

- **Module 2 (RAG):** ReAct agent with a retrieval tool is the most common production pattern (RAG + agent)
- **Module 3 (Fine-Tuning):** Fine-tuned models as the LLM inside an agent (better tool selection, lower cost)
- **Module 5 (Deployment):** Agent architecture choice directly impacts deployment topology and scaling strategy

## Architecture Decision Record

**Decision:** Default to ReAct pattern, upgrade to Plan-and-Execute only for tasks requiring 5+ sequential steps.

**Context:** We evaluated five agent architectures across 50 sample tasks from our target domain.

**Why ReAct as default:** 80% of real tasks need 1-3 tool calls. ReAct handles these with minimal latency and cost. The Think-Act-Observe loop matches how LLMs naturally reason with tools.

**When to upgrade:** If task completion rate drops below 70% with ReAct, or if tasks consistently need 5+ sequential steps, switch to Plan-and-Execute. Document the specific failure cases that triggered the upgrade.

**Trade-off accepted:** ReAct will fail on complex research tasks that need upfront planning. We accept this — those tasks are routed to Plan-and-Execute via a task classifier.

**When to reconsider:** If more than 30% of incoming tasks need Plan-and-Execute, evaluate whether a smarter routing layer (LLM Compiler) would reduce overall latency.
