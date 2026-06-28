# LangGraph Fundamentals

## What This Enables

LangGraph lets you build agents as explicit state machines — graphs where nodes are functions, edges are transitions, and state flows through the system. Unlike chains (linear) or simple ReAct loops (implicit), LangGraph gives you FULL CONTROL over agent behavior: conditional routing, parallel execution, human-in-the-loop, persistence, and streaming. It's the orchestration layer for everything in Module 4.

## Architecture Overview

### Core Concepts

```
StateGraph = a directed graph where:
  - STATE = a TypedDict that flows through the graph (your "context object")
  - NODES = functions that take state, do work, return state updates
  - EDGES = connections between nodes (unconditional or conditional)
  - ENTRY = where execution starts
  - END = where execution stops

Execution: State enters at entry → flows through nodes → each node reads/writes state → conditional edges route based on state → terminates at END
```

### Mental Model

**Software analogy:** LangGraph is like a workflow engine (think Temporal, Step Functions, or even a Spring State Machine). Each node is a "task handler" that processes the current state and decides what happens next. The graph defines all possible execution paths. State is your "message bus" between components.

### Graph Structure

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from operator import add

# 1. Define State (what data flows through the graph)
class AgentState(TypedDict):
    messages: Annotated[list, add]  # append-only message history
    next_step: str                  # routing decision
    tool_results: list              # accumulated tool outputs
    iteration: int                  # loop counter (for safety)

# 2. Define Nodes (functions that process state)
def agent_node(state: AgentState) -> dict:
    """LLM decides what to do next."""
    response = llm.invoke(state["messages"])
    return {"messages": [response], "iteration": state["iteration"] + 1}

def tool_node(state: AgentState) -> dict:
    """Execute the tool the agent chose."""
    last_msg = state["messages"][-1]
    result = execute_tool(last_msg.tool_calls[0])
    return {"messages": [result], "tool_results": [result.content]}

# 3. Define Routing (conditional edges)
def should_continue(state: AgentState) -> str:
    last_msg = state["messages"][-1]
    if last_msg.tool_calls:
        return "tools"      # Agent wants to use a tool
    return "end"            # Agent is done (no tool call = final answer)

# 4. Build the Graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "agent")  # After tool execution, go back to agent

# 5. Compile and Run
app = graph.compile()
result = app.invoke({"messages": [HumanMessage("What's the weather?")], "iteration": 0})
```

## Key Patterns & When to Use Each

| Pattern | Structure | When to Use | Complexity |
|---------|-----------|-------------|-----------|
| Linear chain | A → B → C → END | Simple sequential processing | Low |
| Agent loop | Agent ↔ Tools (conditional exit) | Standard tool-using agent | Medium |
| Branching | Router → Branch A / Branch B → Merge | Multi-path workflows | Medium |
| Parallel | Node → [A, B, C] parallel → Merge | Independent sub-tasks | Medium |
| Human-in-the-loop | Agent → INTERRUPT → Human approval → Continue | High-stakes actions | Medium |
| Supervisor | Supervisor → Sub-agent 1/2/3 → Supervisor | Multi-agent coordination | High |
| Iterative refinement | Generate → Evaluate → Refine (loop) | Quality improvement | Medium |

## Implementation with LangGraph

### Complete Working Agent

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from typing import TypedDict, Annotated
from operator import add

# Define tools
@tool
def search_web(query: str) -> str:
    """Search the web for current information."""
    return f"Search results for: {query}..."

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return str(eval(expression))

tools = [search_web, calculate]

# Define state
class State(TypedDict):
    messages: Annotated[list, add]

# LLM with tools bound
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

# Node functions
def call_model(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END

# Build graph
graph = StateGraph(State)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

agent = graph.compile()

# Run
result = agent.invoke({"messages": [HumanMessage("What is 15% of 340?")]})
print(result["messages"][-1].content)
```

### Checkpointing (State Persistence)

```python
from langgraph.checkpoint.memory import MemorySaver

# Add checkpointer for persistence across sessions
checkpointer = MemorySaver()  # In-memory; use SqliteSaver or PostgresSaver for production

agent = graph.compile(checkpointer=checkpointer)

# Each conversation gets a thread_id
config = {"configurable": {"thread_id": "user-123-session-1"}}

# First message
result = agent.invoke({"messages": [HumanMessage("My name is Himanshu")]}, config)

# Later (even after restart with persistent checkpointer):
result = agent.invoke({"messages": [HumanMessage("What's my name?")]}, config)
# → "Your name is Himanshu" (remembers from checkpoint)
```

### Human-in-the-Loop (Interrupt Before Action)

```python
from langgraph.graph import StateGraph, END

# Compile with interrupt_before on dangerous nodes
agent = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["tools"],  # Pause before executing any tool
)

# First invocation runs until interrupt point
result = agent.invoke({"messages": [HumanMessage("Delete all logs")]}, config)
# → Agent decides to call delete_logs tool
# → Execution PAUSES here (state saved to checkpoint)

# Human reviews the pending tool call:
pending_tool = result["messages"][-1].tool_calls[0]
print(f"Agent wants to call: {pending_tool['name']}({pending_tool['args']})")

# If approved, resume:
result = agent.invoke(None, config)  # None = "continue from where you paused"

# If rejected, modify state and resume:
from langchain_core.messages import ToolMessage
agent.update_state(config, {
    "messages": [ToolMessage(content="Action rejected by human.", tool_call_id=pending_tool["id"])]
})
result = agent.invoke(None, config)
```

### Conditional Branching

```python
def route_by_intent(state: State) -> str:
    """Route to different sub-graphs based on query intent."""
    last_msg = state["messages"][-1].content.lower()
    if "code" in last_msg:
        return "code_agent"
    elif "search" in last_msg:
        return "search_agent"
    return "general_agent"

graph.add_conditional_edges("classifier", route_by_intent, {
    "code_agent": "code_agent",
    "search_agent": "search_agent",
    "general_agent": "general_agent",
})
```

### Streaming (Real-Time Output)

```python
# Stream node outputs as they execute
async for event in agent.astream_events(
    {"messages": [HumanMessage("Explain quantum computing")]},
    config,
    version="v2",
):
    if event["event"] == "on_chat_model_stream":
        # Token-by-token from LLM
        print(event["data"]["chunk"].content, end="", flush=True)
    elif event["event"] == "on_tool_end":
        # Tool finished executing
        print(f"\n[Tool result: {event['data']['output']}]")
```

## State Management & Memory

| Mechanism | How | When |
|-----------|-----|------|
| State TypedDict | Data passed between nodes within one run | Always (core mechanism) |
| Checkpointing | State saved/restored across runs (thread_id) | Multi-turn conversations |
| Annotated[list, add] | Append-only state fields (message history) | Accumulating data |
| State reducers | Custom logic for merging state updates | Complex state management |

### State Design Best Practices

```python
class WellDesignedState(TypedDict):
    # Message history (always append-only)
    messages: Annotated[list, add]
    
    # Current step tracking
    current_plan: list[str]     # Task decomposition
    completed_steps: list[str]  # What's done
    
    # Loop safety
    iteration_count: int        # Prevent infinite loops
    max_iterations: int         # Hard limit
    
    # Routing
    next_action: str            # What to do next
    
    # Results accumulation
    gathered_info: dict         # Key-value store for intermediate results
```

## Error Handling & Guardrails

| Failure Mode | Cause | Prevention |
|-------------|-------|-----------|
| Infinite loop | Agent keeps calling tools without converging | Max iteration counter in state + conditional exit |
| Tool call with bad args | LLM hallucinates tool parameters | Pydantic validation on tool inputs, return helpful error |
| Node exception | Unhandled error in node function | Try/except in nodes, fallback state update |
| State grows unbounded | Messages accumulate forever | Summarize old messages, window the history |
| Deadlock | Conditional edge has no matching route | Always have a default/fallback route |
| Checkpoint corruption | Inconsistent state saved | Use transactions (PostgresSaver), validate on load |

```python
# Safety pattern: Max iterations
def should_continue(state: State) -> str:
    if state.get("iteration_count", 0) >= 10:
        return END  # Force stop after 10 iterations
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END
```

## Testing & Debugging

```python
# Test strategy for LangGraph agents:
# 1. Unit test individual nodes (they're just functions)
# 2. Test routing logic with known states
# 3. Integration test full graph with known queries + expected tool usage

def test_agent_uses_calculator():
    result = agent.invoke({"messages": [HumanMessage("What is 2+2?")]})
    # Check that calculator tool was called
    tool_calls = [m for m in result["messages"] if hasattr(m, "tool_calls") and m.tool_calls]
    assert len(tool_calls) > 0
    assert tool_calls[0].tool_calls[0]["name"] == "calculate"
    # Check final answer
    assert "4" in result["messages"][-1].content

# Debugging: Visualize the graph
graph_image = agent.get_graph().draw_mermaid_png()
# Shows nodes, edges, and routing conditions visually
```

## Production Considerations

### Latency
- Each node = 1 LLM call (200-2000ms) or tool execution (variable)
- 3-node agent (agent → tool → agent): 1-5s total
- Complex graphs (5-10 nodes): 5-20s total
- Streaming hides latency for user-facing apps

### Cost
- Each LLM node = token cost ($0.0001-0.005 depending on model)
- More iterations = more cost (linear scaling)
- Set max_iterations to control cost ceiling
- Monitor: tokens per conversation, iterations per task

### Observability
- LangSmith integration (automatic tracing of every node execution)
- Custom logging in nodes (structured logging per step)
- Checkpoint inspection (see state at any point in execution)

## Integration Points

- **Module 2 (RAG):** RAG retriever as a tool node in the agent graph
- **Module 3 (Fine-Tuning):** Fine-tuned model as the LLM in specific nodes
- **Module 4 (All topics):** LangGraph is the implementation framework for topics 5-10
- **Module 5 (Deployment):** Serve compiled graph via FastAPI + LangServe

## Architecture Decision Record

**Decision:** Use LangGraph as primary agent orchestration framework.

**Why:** Explicit state machines give full control over agent behavior. Unlike AutoGen/CrewAI (opinionated, less control) or raw code (no structure), LangGraph balances flexibility with structure. First-party LangChain integration. Growing ecosystem.

**Trade-off accepted:** More boilerplate than simple chain. Learning curve for graph-based thinking. Worth it for anything beyond a simple ReAct loop.

**When to reconsider:** For trivial agents (single tool, no branching), a plain LangChain AgentExecutor is simpler. For distributed multi-agent systems at massive scale, consider custom orchestration.
