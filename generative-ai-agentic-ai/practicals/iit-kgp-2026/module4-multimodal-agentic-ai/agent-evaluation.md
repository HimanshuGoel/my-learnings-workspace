# Agent Evaluation

## What This Enables

Agent evaluation lets you measure whether your agent completes tasks correctly, efficiently, and reliably — despite non-deterministic behavior. Unlike testing a function (same input → same output), testing agents means evaluating TRAJECTORIES: the sequence of decisions, tool calls, and reasoning steps. This is how you build confidence before shipping and catch regressions when you change prompts or models.

## Architecture Overview

### Why Agent Testing Is Different

```
Traditional: Input → Function → Output          (assert output == expected)

Agent:       Input → [Step1 → Step2 → StepN] → Output
                      ~~~~~ TRAJECTORY ~~~~~
             Assert:
               • Right answer? (outcome)
               • Right tools? (tool accuracy)
               • Too many steps? (efficiency)
               • Sound reasoning? (trajectory quality)
```

### Evaluation Architecture

```
┌────────────┐    ┌──────────────┐    ┌─────────────────────┐
│  TEST CASE │───►│    AGENT     │───►│    EVALUATORS       │
│            │    │  UNDER TEST  │    │                     │
│ • query    │    │              │    │ • Output correct?   │
│ • expected │    │ Returns:     │    │ • Tools correct?    │
│   output   │    │ trajectory + │    │ • Steps ≤ budget?   │
│ • ref tools│    │ final answer │    │ • LLM judge score   │
└────────────┘    └──────────────┘    └──────────┬──────────┘
                                                  │
                                          ┌───────▼───────┐
                                          │   METRICS     │
                                          │ pass rate,    │
                                          │ cost, flaky % │
                                          └───────────────┘
```

## Key Patterns & When to Use Each

| Pattern | What It Checks | Complexity | When to Use |
|---------|---------------|-----------|-------------|
| Output-only eval | Final answer matches expected | Low | Simple Q&A, factual queries |
| Trajectory matching | Steps match reference path | Medium | Workflow agents with known-good paths |
| Step budget | Completed in ≤ N steps | Low | Cost-sensitive, efficiency testing |
| Tool accuracy | Correct tools with correct args | Medium | Tool-heavy agents, API orchestrators |
| LLM-as-judge | Another LLM rates quality | High | Complex reasoning, subjective output |
| Regression suite | Same tests after every change | Medium | CI/CD for agents, prompt changes |

## Implementation with LangGraph/LangChain

### Trajectory Logging

```python
from dataclasses import dataclass, field
from langchain_core.messages import HumanMessage
from datetime import datetime

@dataclass
class TrajectoryStep:
    node: str
    action: str
    output_summary: str
    timestamp: float

@dataclass
class AgentTrajectory:
    query: str
    steps: list[TrajectoryStep] = field(default_factory=list)
    final_output: str = ""
    tools_called: list[str] = field(default_factory=list)
    total_time_ms: float = 0

    @property
    def step_count(self) -> int:
        return len(self.steps)

class TrajectoryCapture:
    """Wraps an agent to capture execution traces."""

    def __init__(self, agent):
        self.agent = agent

    def invoke_with_trace(self, query: str, config: dict = None) -> AgentTrajectory:
        trajectory = AgentTrajectory(query=query)
        start = datetime.now()

        for event in self.agent.stream({"messages": [HumanMessage(query)]}, config):
            for node_name, output in event.items():
                step = TrajectoryStep(
                    node=node_name,
                    action=self._extract_action(output),
                    output_summary=str(output)[:200],
                    timestamp=datetime.now().timestamp(),
                )
                trajectory.steps.append(step)

                for msg in output.get("messages", []):
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            trajectory.tools_called.append(tc["name"])

        trajectory.total_time_ms = (datetime.now() - start).total_seconds() * 1000
        trajectory.final_output = str(output.get("messages", [""])[-1].content)
        return trajectory

    def _extract_action(self, output: dict) -> str:
        messages = output.get("messages", [])
        if not messages:
            return "no_output"
        last = messages[-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return f"tool_call:{last.tool_calls[0]['name']}"
        return "response"
```

### Evaluation Harness

```python
from dataclasses import dataclass
from enum import Enum

class EvalResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"

@dataclass
class TestCase:
    query: str
    expected_output_contains: list[str]
    expected_tools: list[str] = None
    forbidden_tools: list[str] = None
    max_steps: int = 10

@dataclass
class EvalScore:
    output_correct: EvalResult
    tools_correct: EvalResult
    within_budget: EvalResult

def evaluate_trajectory(trajectory: AgentTrajectory, tc: TestCase) -> EvalScore:
    """Evaluate trajectory against test case expectations."""
    # Output correctness
    output_ok = EvalResult.PASS
    for expected in tc.expected_output_contains:
        if expected.lower() not in trajectory.final_output.lower():
            output_ok = EvalResult.FAIL
            break

    # Tool accuracy
    tools_ok = EvalResult.PASS
    if tc.expected_tools:
        for t in tc.expected_tools:
            if t not in trajectory.tools_called:
                tools_ok = EvalResult.FAIL
                break
    if tc.forbidden_tools:
        for t in tc.forbidden_tools:
            if t in trajectory.tools_called:
                tools_ok = EvalResult.FAIL
                break

    # Step budget
    budget_ok = EvalResult.PASS if trajectory.step_count <= tc.max_steps else EvalResult.FAIL

    return EvalScore(output_correct=output_ok, tools_correct=tools_ok, within_budget=budget_ok)
```

### LLM-as-Judge on Trajectories

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

class TrajectoryJudgment(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    reasoning: str
    issues: list[str] = Field(default_factory=list)

judge_llm = ChatOpenAI(model="gpt-4o").with_structured_output(TrajectoryJudgment)

def llm_judge_trajectory(trajectory: AgentTrajectory) -> TrajectoryJudgment:
    """LLM evaluates trajectory quality (reasoning, efficiency, correctness)."""
    steps_text = "\n".join(
        f"Step {i+1} [{s.node}]: {s.action} → {s.output_summary[:80]}"
        for i, s in enumerate(trajectory.steps)
    )
    return judge_llm.invoke([
        SystemMessage(content="""Rate 0.0-1.0. Consider: logical path, necessary tool calls,
        no wasted steps, complete answer. 1.0=optimal, 0.7=correct but inefficient, 0.0=wrong."""),
        HumanMessage(content=f"Query: {trajectory.query}\n\nTrajectory:\n{steps_text}\n\nOutput: {trajectory.final_output}")
    ])
```

### Agent Test Suite (Regression Testing)

```python
class AgentTestSuite:
    def __init__(self, agent, name: str = "agent_tests"):
        self.capture = TrajectoryCapture(agent)
        self.name = name

    def run(self, test_cases: list[TestCase], runs_per_case: int = 3) -> dict:
        """Run all tests multiple times to measure reliability."""
        summary = {"total": 0, "passed": 0, "failed": 0, "flaky": 0}

        for tc in test_cases:
            pass_count = 0
            for _ in range(runs_per_case):
                traj = self.capture.invoke_with_trace(tc.query)
                score = evaluate_trajectory(traj, tc)
                if score.output_correct == EvalResult.PASS:
                    pass_count += 1

            summary["total"] += 1
            if pass_count == runs_per_case:
                summary["passed"] += 1
            elif pass_count == 0:
                summary["failed"] += 1
            else:
                summary["flaky"] += 1

        return summary

# Usage
test_cases = [
    TestCase(query="What is 15% of 200?", expected_output_contains=["30"],
             expected_tools=["calculate"], max_steps=3),
    TestCase(query="Search for Python 3.13 features", expected_output_contains=["Python"],
             expected_tools=["search_web"], forbidden_tools=["calculate"], max_steps=4),
]

suite = AgentTestSuite(agent)
results = suite.run(test_cases, runs_per_case=5)
# → {"total": 2, "passed": 1, "failed": 0, "flaky": 1}
```

## State Management & Memory

| Concern | Approach |
|---------|----------|
| Trajectory storage | Log all traces to file/DB for later analysis |
| Baseline | Store "golden" trajectories as reference for regression |
| Drift detection | Compare current distribution to baseline weekly |
| Versioning | Tag trajectories with prompt hash + model name |

## Error Handling & Guardrails

| Failure Mode | Symptom | Prevention |
|-------------|---------|-----------|
| Non-determinism masks bugs | Passes 3/5 times | Run 5-10x, flag flaky (>0% and <100%) |
| Judge too strict | Penalizes valid alternative approaches | Judge outcome, not style |
| Reference too rigid | Agent finds valid different path | Allow multiple valid trajectories |
| Test suite cost explosion | 50 cases × 5 runs × $0.01 = $2.50/run | Use cheap model for eval, cache deterministic parts |
| Stale expectations | Tests don't match updated agent | Review tests when changing prompts |

## Testing & Debugging

```python
# Meta-test: ensure evaluator catches wrong tool usage
def test_evaluator_detects_wrong_tool():
    fake_traj = AgentTrajectory(query="Calculate 2+2", tools_called=["search_web"], final_output="4")
    fake_traj.steps = [TrajectoryStep(node="agent", action="tool_call:search_web", output_summary="", timestamp=0)]
    tc = TestCase(query="Calculate 2+2", expected_output_contains=["4"], expected_tools=["calculate"])
    score = evaluate_trajectory(fake_traj, tc)
    assert score.tools_correct == EvalResult.FAIL

# Pretty-print trajectory for debugging
def print_trajectory(traj: AgentTrajectory):
    print(f"Query: {traj.query} | Steps: {traj.step_count} | {traj.total_time_ms:.0f}ms")
    for i, s in enumerate(traj.steps):
        print(f"  {i+1}. [{s.node}] {s.action}")
    print(f"  → {traj.final_output[:150]}")
```

## Production Considerations

### What to Monitor

- Step count distribution (p50, p95) — detect efficiency regressions
- Step-limit hit rate (>5% = agent is struggling)
- Tool error rate by tool name
- Latency p95 — catches planning explosions
- User feedback (thumbs up/down) correlated with trajectory metrics

### Cost of Evaluation

- Full suite (50 cases × 5 runs): ~$2.50 with GPT-4o-mini
- LLM-as-judge adds ~$1.25 (50 judgments with GPT-4o)
- Run full suite: weekly or on major changes
- Smoke tests (5 cases × 1 run): every deployment

## Integration Points

- **Module 2 (RAG):** RAG eval patterns (retrieval recall) apply to agent retriever tools
- **Module 4 (LangGraph):** Trajectory = node execution sequence in the graph
- **Module 4 (Planning):** Evaluate plan quality (step count, ordering) separately from execution
- **Module 4 (Production):** Production monitoring IS continuous evaluation on live traffic
- **Module 5 (Deployment):** Regression suite in CI before deploying new agent version

## Architecture Decision Record

**Decision:** Evaluate on trajectories (not just output) using deterministic checks (tools, budget) + LLM-as-judge (reasoning quality).

**Why:** Output-only misses efficiency problems (right answer in 15 steps instead of 3). Tool-only misses creative solutions. LLM-as-judge handles subjective quality that rules can't capture. The combination gives confidence across all dimensions.

**Trade-off accepted:** LLM-as-judge is expensive and non-deterministic. Mitigate: use sparingly (weekly), calibrate with human scores, treat as one signal among many.

**When to reconsider:** Fully deterministic tasks (one right path): skip LLM judge, use deterministic eval only. Cost-constrained: output-only eval, add trajectory checks for failing cases only.
