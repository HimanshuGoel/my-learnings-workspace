# Planning and Reasoning

## What This Enables

Planning lets agents decompose complex tasks into manageable steps, execute them in order, and adapt when things go wrong. Without planning, agents attempt everything in a single shot — which works for simple queries but fails for multi-step problems requiring intermediate results, dependency ordering, or iterative refinement.

## Architecture Overview

### Plan-and-Execute Architecture

```
User Query
    │
    ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   PLANNER     │────►│   EXECUTOR    │────►│  REPLANNER    │
│ (decompose    │     │ (run current  │     │ (review,      │
│  into steps)  │     │  step w/tools)│     │  adapt plan)  │
└───────────────┘     └───────────────┘     └──────┬────────┘
                                                    │
                                            ┌───────┴───────┐
                                            ▼               ▼
                                       [Next Step]     [DONE → END]
                                       (loop back)
```

### Self-Reflection Loop

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Generate │────►│ Evaluate │────►│  Refine  │──┐
│  Output  │     │ Quality  │     │  Output  │  │ (if score < threshold)
└──────────┘     └──────────┘     └──────────┘  │
      ▲                                          │
      └──────────────────────────────────────────┘
```

## Key Patterns & When to Use Each

| Pattern | How It Works | When to Use | Latency | Cost |
|---------|-------------|-------------|---------|------|
| Direct execution | LLM answers in one shot | Simple factual, single-tool tasks | 1 call | $ |
| Sequential plan | Plan → Execute step by step | Ordered 3-7 step tasks | N+2 calls | $$ |
| DAG plan | Parallel branches for independent sub-tasks | Sub-tasks with no dependencies | Medium | $$ |
| Iterative refinement | Generate → Critique → Improve loop | Quality-sensitive outputs | 2-5 loops | $$$ |
| Tree search | Explore multiple solution paths | Ambiguous problems | Very high | $$$$ |

### When Planning Helps vs. Hurts

Planning HELPS when: task has 3+ dependent steps, intermediate results feed later steps, task might need adaptation mid-execution. Planning HURTS when: task is single-step, latency budget is tight (<2s), simple retrieval + generation suffices.

## Implementation with LangGraph/LangChain

### Plan-and-Execute Agent

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from typing import TypedDict, Annotated, Optional
from operator import add
from pydantic import BaseModel, Field

class PlanExecuteState(TypedDict):
    messages: Annotated[list, add]
    plan: list[str]
    current_step: int
    step_results: list[str]
    final_answer: Optional[str]
    iteration: int

@tool
def search_web(query: str) -> str:
    """Search the web for current information."""
    return f"Results for '{query}': [relevant information]"

tools = [search_web]
llm = ChatOpenAI(model="gpt-4o-mini")

class Plan(BaseModel):
    steps: list[str] = Field(description="Ordered list of 2-5 steps to complete the task")

def planner_node(state: PlanExecuteState) -> dict:
    """Decompose the task into ordered steps."""
    planner_llm = llm.with_structured_output(Plan)
    response = planner_llm.invoke([
        SystemMessage(content="Break the task into 2-5 concrete, actionable steps."),
        HumanMessage(content=f"Plan: {state['messages'][0].content}")
    ])
    return {"plan": response.steps, "current_step": 0, "step_results": []}

def executor_node(state: PlanExecuteState) -> dict:
    """Execute the current step."""
    step = state["plan"][state["current_step"]]
    previous = "\n".join(f"Step {i+1}: {r}" for i, r in enumerate(state["step_results"]))
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke([
        SystemMessage(content=f"Execute this step. Previous results:\n{previous}"),
        HumanMessage(content=f"Execute: {step}")
    ])
    return {
        "step_results": [response.content or f"Done: {step}"],
        "current_step": state["current_step"] + 1,
        "iteration": state.get("iteration", 0) + 1,
        "messages": [response],
    }

def replanner_node(state: PlanExecuteState) -> dict:
    """Synthesize final answer when all steps complete."""
    all_results = "\n".join(f"Step {i+1}: {r}" for i, r in enumerate(state["step_results"]))
    final = llm.invoke([
        SystemMessage(content="Synthesize step results into a final answer."),
        HumanMessage(content=f"Results:\n{all_results}\n\nQuery: {state['messages'][0].content}")
    ])
    return {"final_answer": final.content}

def should_continue(state: PlanExecuteState) -> str:
    if state.get("iteration", 0) >= 10:
        return "end"
    if state.get("final_answer"):
        return "end"
    if state["current_step"] >= len(state["plan"]):
        return "replan"
    return "execute"

graph = StateGraph(PlanExecuteState)
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("replanner", replanner_node)
graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_conditional_edges("executor", should_continue, {
    "execute": "executor", "replan": "replanner", "end": END,
})
graph.add_edge("replanner", END)

agent = graph.compile()
```

### Self-Reflection Loop

```python
class ReflectionState(TypedDict):
    messages: Annotated[list, add]
    draft: str
    critique: str
    iteration: int
    quality_score: float

def generate_node(state: ReflectionState) -> dict:
    prompt = (f"Improve based on feedback:\nDraft: {state['draft']}\nFeedback: {state['critique']}"
              if state.get("critique") else state["messages"][0].content)
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"draft": response.content, "iteration": state.get("iteration", 0) + 1}

def evaluate_node(state: ReflectionState) -> dict:
    response = llm.invoke([
        SystemMessage(content="Rate 0.0-1.0. Format: SCORE: X.X\nFEEDBACK: ..."),
        HumanMessage(content=f"Evaluate:\n{state['draft']}")
    ])
    score = float(response.content.split("SCORE:")[1].split("\n")[0].strip())
    feedback = response.content.split("FEEDBACK:")[1].strip()
    return {"quality_score": score, "critique": feedback}

def should_refine(state: ReflectionState) -> str:
    if state.get("quality_score", 0) >= 0.8 or state.get("iteration", 0) >= 3:
        return "done"
    return "refine"

reflection_graph = StateGraph(ReflectionState)
reflection_graph.add_node("generate", generate_node)
reflection_graph.add_node("evaluate", evaluate_node)
reflection_graph.set_entry_point("generate")
reflection_graph.add_edge("generate", "evaluate")
reflection_graph.add_conditional_edges("evaluate", should_refine, {"refine": "generate", "done": END})
reflection_agent = reflection_graph.compile()
```

## State Management & Memory

| Concern | Strategy |
|---------|----------|
| Plan persistence | Stored as list[str] in graph state — survives across nodes |
| Step results | Append-only list — each executor adds its result |
| Replanning | Replanner can overwrite plan with updated steps |
| Cross-session | Checkpoint graph to resume multi-step tasks after interruption |
| Context growth | Summarize old step results when tokens exceed budget |

## Error Handling & Guardrails

| Failure Mode | Symptom | Prevention |
|-------------|---------|-----------|
| Over-planning | 15-step plan for a 2-step task | Prompt: "2-5 steps maximum" |
| Plan drift | Steps become irrelevant mid-execution | Replanner checks alignment with original goal |
| Infinite refinement | Quality score never reaches threshold | Hard cap: max 3 loops |
| Step failure | One step fails, breaks chain | Executor returns error, replanner adapts |
| Circular reasoning | Agent plans to plan to plan | Detect "plan" in steps, force execution |

## Testing & Debugging

```python
def test_planner_step_count():
    result = agent.invoke({"messages": [HumanMessage("What's the weather?")], "iteration": 0})
    assert len(result.get("plan", [])) <= 3  # Simple query, few steps

def test_max_iterations_enforced():
    state = {"iteration": 10, "plan": ["step"], "current_step": 0,
             "step_results": [], "messages": []}
    assert should_continue(state) == "end"

# Debug: stream plan execution
for event in agent.stream({"messages": [HumanMessage("Research X")], "iteration": 0}):
    for node, output in event.items():
        print(f"[{node}] step={output.get('current_step', '—')}")
```

## Production Considerations

### Latency & Cost

- Planning adds 1-2 LLM calls upfront (500ms-2s)
- Each step: 1-3 LLM calls. Total 5-step plan: 8-15 calls (4-15s)
- Plan-and-Execute: 3-5x more expensive than direct execution
- Break-even: Planning saves cost when it prevents wasted tool calls from wrong approaches

### Complexity Router (Skip Planning for Simple Queries)

```python
def complexity_router(state: dict) -> str:
    """Route simple queries directly, complex ones through planner."""
    query = state["messages"][0].content
    response = llm.invoke([
        SystemMessage(content="Reply SIMPLE or COMPLEX. SIMPLE = answerable in 1 step."),
        HumanMessage(content=query)
    ])
    return "direct" if "SIMPLE" in response.content else "planner"
```

## Integration Points

- **Module 2 (RAG):** Retriever as a tool in executor steps
- **Module 4 (LangGraph):** Plan-and-Execute IS a LangGraph pattern — nodes + conditional edges
- **Module 4 (Multi-Agent):** Planner can delegate steps to specialist sub-agents
- **Module 4 (Memory):** Long-running plans benefit from checkpointing
- **Module 5 (Deployment):** Stream plan progress to user ("Step 2/5: Searching...")

## Architecture Decision Record

**Decision:** Use Plan-and-Execute only for tasks with 3+ dependent steps. Route simple queries directly.

**Why:** Planning adds 1-2 LLM calls of overhead. For "What's the weather?" this is pure waste. For "Research X, compare with Y, write a report" it prevents the agent from going in circles. A cheap complexity router saves planning overhead on 70-80% of queries.

**Trade-off accepted:** Router can misclassify — occasionally sending a complex query direct (fails and retries) or a simple query through planning (wastes ~1s). Both failure modes are recoverable.

**When to reconsider:** If 90%+ tasks are complex, skip the router and always plan. If 90%+ are simple, skip planning entirely and use a basic ReAct agent.
