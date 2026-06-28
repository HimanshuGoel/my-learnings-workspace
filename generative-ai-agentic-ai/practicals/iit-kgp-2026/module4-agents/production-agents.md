# Production Agents

## What This Enables

Production deployment turns a notebook prototype into a system that handles real users — with streaming responses, cost controls, human-in-the-loop approvals, observability, and graceful degradation. The gap between "works in a notebook" and "works for 1000 users at 3am" is where most agent projects fail. This covers the engineering patterns that bridge that gap.

## Architecture Overview

### Production Agent Stack

```
┌─────────────────────────────────────────────────────────────┐
│  CLIENT: Streaming UI + approval buttons + retry logic      │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP / SSE
┌──────────────────────────▼──────────────────────────────────┐
│  FastAPI: Auth, rate limiting, timeout, streaming response  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  GUARDRAILS: Step budget, token cap, complexity router,     │
│              content filter, cost cap                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  LangGraph Agent: State machine + checkpoint + tracing      │
└─────────┬────────────────────────────────────┬──────────────┘
          │                                    │
    ┌─────▼─────┐                     ┌────────▼────────┐
    │   TOOLS   │                     │    FALLBACK     │
    │ (APIs, DB │                     │ (simple chain   │
    │  search)  │                     │  if agent fails)│
    └───────────┘                     └─────────────────┘
```

### When NOT to Use an Agent

Use a CHAIN when: task always follows same steps, no tool selection needed, latency <2s, output format is fixed. Use an AGENT when: task varies by input, must choose between tools, user tolerates 5-15s, output depends on findings.

## Key Patterns & When to Use Each

| Pattern | Latency | Cost/Query | Reliability | When to Use |
|---------|---------|-----------|-------------|-------------|
| Direct chain | 0.5-2s | $0.001-0.005 | High | Fixed tasks, summarization |
| Simple agent (1-3 tools) | 2-8s | $0.01-0.05 | Medium | Variable tasks, tool selection |
| Complex agent (planning) | 5-20s | $0.05-0.30 | Lower | Multi-step research |
| Multi-agent | 10-60s | $0.10-1.00 | Lowest | Domain separation needed |

### Cost at Scale

```
At 10,000 queries/day:
  Chain:         $20/day     ($600/month)
  Simple agent:  $80/day     ($2,400/month)
  Complex agent: $350/day    ($10,500/month)
  Multi-agent:   $1,200/day  ($36,000/month)
```

## Implementation with LangGraph/LangChain

### FastAPI Serving with Streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated, AsyncGenerator
from operator import add
import json, time

app = FastAPI(title="Agent API")

@tool
def search_web(query: str) -> str:
    """Search for current information."""
    return f"Results for '{query}': [content]"

@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    allowed = set("0123456789+-*/.(). ")
    if not all(c in allowed for c in expression):
        return "ERROR: Invalid expression."
    return str(eval(expression))

tools = [search_web, calculate]

class AgentState(TypedDict):
    messages: Annotated[list, add]
    step_count: int
    max_steps: int

llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

def agent_node(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response], "step_count": state.get("step_count", 0) + 1}

def should_continue(state: AgentState) -> str:
    if state.get("step_count", 0) >= state.get("max_steps", 10):
        return END  # Budget enforcement
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")
agent = graph.compile(checkpointer=MemorySaver())

@app.post("/chat/stream")
async def chat_stream(query: str, thread_id: str = "default", max_steps: int = 10):
    """Stream agent steps as Server-Sent Events."""
    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator() -> AsyncGenerator[str, None]:
        start = time.time()
        for event in agent.stream(
            {"messages": [HumanMessage(query)], "step_count": 0, "max_steps": max_steps}, config
        ):
            if time.time() - start > 30:  # Timeout
                yield f"data: {json.dumps({'type': 'error', 'content': 'Timed out'})}\n\n"
                break
            for node_name, output in event.items():
                for msg in output.get("messages", []):
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        yield f"data: {json.dumps({'type': 'tool_call', 'tool': msg.tool_calls[0]['name']})}\n\n"
                    elif msg.content:
                        yield f"data: {json.dumps({'type': 'response', 'content': msg.content})}\n\n"
        yield f"data: {json.dumps({'type': 'done', 'ms': int((time.time()-start)*1000)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

### Human-in-the-Loop Interrupt

```python
from langchain_core.messages import ToolMessage

hitl_agent = graph.compile(checkpointer=MemorySaver(), interrupt_before=["tools"])

@app.post("/chat/hitl")
async def chat_with_approval(query: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    result = hitl_agent.invoke(
        {"messages": [HumanMessage(query)], "step_count": 0, "max_steps": 10}, config
    )
    state = hitl_agent.get_state(config)
    if state.next:  # Paused before tool execution
        pending = result["messages"][-1]
        return {
            "status": "awaiting_approval",
            "pending": {"tool": pending.tool_calls[0]["name"],
                        "args": pending.tool_calls[0]["args"],
                        "id": pending.tool_calls[0]["id"]},
        }
    return {"status": "complete", "response": result["messages"][-1].content}

@app.post("/chat/approve")
async def approve_action(thread_id: str, approved: bool):
    config = {"configurable": {"thread_id": thread_id}}
    if approved:
        result = hitl_agent.invoke(None, config)
    else:
        state = hitl_agent.get_state(config)
        tool_call_id = state.values["messages"][-1].tool_calls[0]["id"]
        hitl_agent.update_state(config, {"messages": [
            ToolMessage(content="Rejected by user. Try different approach.", tool_call_id=tool_call_id)
        ]})
        result = hitl_agent.invoke(None, config)
    return {"response": result["messages"][-1].content}
```

### LangSmith Tracing

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "production-agent-v1"

# All LangGraph calls now traced. Add metadata per request:
config = {
    "configurable": {"thread_id": "user-123"},
    "metadata": {"user_id": "user-123", "environment": "production"},
    "tags": ["production", "tier-1"],
}
```

### Graceful Degradation (Fallback to Chain)

```python
from langchain_core.messages import SystemMessage

fallback_llm = ChatOpenAI(model="gpt-4o-mini")

async def invoke_with_fallback(query: str, thread_id: str, max_steps: int = 10) -> dict:
    """Agent first. If fails or hits budget, fall back to simple chain."""
    config = {"configurable": {"thread_id": thread_id}}
    try:
        result = agent.invoke(
            {"messages": [HumanMessage(query)], "step_count": 0, "max_steps": max_steps}, config
        )
        if result.get("step_count", 0) >= max_steps:
            return await _fallback(query, "step_limit")
        return {"response": result["messages"][-1].content, "mode": "agent"}
    except Exception as e:
        return await _fallback(query, f"error:{type(e).__name__}")

async def _fallback(query: str, reason: str) -> dict:
    response = fallback_llm.invoke([
        SystemMessage(content="Answer concisely. No tools available."),
        HumanMessage(content=query),
    ])
    return {"response": response.content, "mode": "fallback", "reason": reason}
```

### Complexity Router (Downgrade Agent → Chain)

```python
def select_execution_mode(query: str, user_tier: str) -> str:
    """Route to cheapest viable mode."""
    if user_tier == "free":
        return "chain"
    needs_tools = any(kw in query.lower() for kw in ["search", "calculate", "look up", "find"])
    needs_planning = len(query.split()) > 30 or "and then" in query.lower()
    if needs_planning:
        return "complex_agent"
    elif needs_tools:
        return "simple_agent"
    return "chain"
```

## State Management & Memory

| Concern | Production Approach |
|---------|-------------------|
| Persistence | PostgresSaver (durable, queryable) |
| Session resumption | thread_id per session, load from checkpoint |
| Cleanup | TTL on old threads (30 days), archive to cold storage |
| Concurrency | Each thread_id independent, no cross-contamination |

## Error Handling & Guardrails

| Failure Mode | Symptom | Mitigation |
|-------------|---------|-----------|
| Agent loops | Response never returns | Step budget (10) + timeout (30s) |
| Cost spike | One query costs $5 | Token cap (50K) + cost cap per request |
| Tool API down | Retries forever | Tool timeout (5s) + max 2 retries + fallback |
| LLM rate limited | 429 errors | Exponential backoff + queue + fallback model |
| PII in output | Leaks user data | Output content filter before streaming |
| Concurrent corruption | Two requests same thread | Lock thread or queue requests |

## Testing & Debugging

```python
# Smoke test after deployment
def smoke_test(base_url: str) -> bool:
    import requests
    r = requests.post(f"{base_url}/chat", params={"query": "What is 2+2?", "thread_id": "smoke"})
    return r.status_code == 200 and "4" in r.json().get("response", "")

# Cost bounding test
def test_cost_bounded():
    result = agent.invoke(
        {"messages": [HumanMessage("Research everything about AI")],
         "step_count": 0, "max_steps": 5},
        {"configurable": {"thread_id": "cost-test"}},
    )
    assert result["step_count"] <= 5  # Budget enforced regardless of query
```

## Production Considerations

### Observability Checklist

- Every request logged (query, thread_id, timestamp)
- Every step traced (LangSmith)
- Latency histogram (p50, p95, p99)
- Step count distribution, token usage per request
- Fallback trigger rate, error rate by type

### Deployment Topology

```
Prototype:    FastAPI + LangGraph + SQLite (10-50 users)
Production:   Load Balancer → 2-4 FastAPI + Postgres + Redis + LangSmith (100-1000 users)
Scale:        API Gateway → Auto-scaling + Managed DB + Task Queue (1000+ users)
```

## Integration Points

- **Module 2 (RAG):** Retriever as a tool (most common production pattern)
- **Module 4 (LangGraph):** Production agent IS a compiled graph with checkpointing
- **Module 4 (Memory):** PostgresSaver for durable memory
- **Module 4 (Evaluation):** Production monitoring = continuous eval on live traffic
- **Module 5 (Deployment):** FastAPI + containers + LangSmith is the reference stack

## Architecture Decision Record

**Decision:** Default to simple chains. Use agents only when task requires tool selection or multi-step reasoning. Mandatory guardrails (step budget, timeout, cost cap) on all agent deployments.

**Why:** Agents are 5-50x more expensive, 3-10x slower, and less predictable. Most queries (70-80%) can be handled by a chain. Guardrails prevent tail cases (loops, cost spikes) that make agents unreliable at scale.

**Trade-off accepted:** Complexity router adds one LLM call overhead. Some misclassification (agent query → chain → poor answer → retry). Fallback means users occasionally see simpler answers. All acceptable for reliability and cost control.

**When to reconsider:** If 100% of tasks are complex (research/coding agent), skip the router — but keep guardrails. If cost doesn't matter and reliability is critical, run agent + chain in parallel and pick the better answer.
