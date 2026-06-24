# Agentic RAG

## The Problem You're Solving

Simple retrieve-then-generate pipelines fail on complex questions that need multiple retrieval steps, query decomposition, cross-document reasoning, or dynamic routing. When a user asks "Compare the auth approaches in v1 vs v2 and recommend which to migrate to," a single retrieval pass won't cut it. You need an agent that plans, retrieves iteratively, and synthesizes.

## Options Available

| Pattern | When to Use | Complexity | Latency |
|---------|-------------|------------|---------|
| Single-shot RAG | Simple factual questions | Low | 1-3s |
| Query routing | Multiple document collections/domains | Medium | 1-3s |
| Query decomposition | Multi-part questions | Medium | 3-8s |
| Iterative retrieval (self-RAG) | Need to verify/refine answers | High | 5-15s |
| Multi-hop reasoning | Questions requiring chained facts | High | 5-20s |
| Agentic with tools | Need calculation, API calls, or actions | High | 5-30s |
| Corrective RAG (CRAG) | Need to detect and fix bad retrieval | High | 5-15s |

## Recommended Approach

**Start with query routing + decomposition. Add iterative retrieval only for complex use cases. Use LangGraph for stateful agent orchestration.**


Why: Most questions (70-80%) are answerable with simple RAG. Routing handles multi-domain corpora cheaply. Decomposition handles complex questions. Full agentic loops are expensive and slow — only justified for high-value complex queries. LangGraph gives you explicit control over the agent's state machine.

## Step-by-Step Implementation

### 1. Query Router (Direct to Right Source)

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from enum import Enum

class RouteTarget(str, Enum):
    API_DOCS = "api_docs"
    TUTORIALS = "tutorials"
    CHANGELOGS = "changelogs"
    GENERAL = "general"

class QueryRoute(BaseModel):
    target: RouteTarget = Field(description="Which collection to search")
    reasoning: str = Field(description="Why this route was chosen")

router_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(QueryRoute)

def route_query(question: str) -> QueryRoute:
    """Route query to the most appropriate collection."""
    return router_llm.invoke(
        f"""Classify this question into the best search target:
        - api_docs: API endpoints, parameters, authentication, rate limits
        - tutorials: How-to guides, setup instructions, examples
        - changelogs: Version changes, deprecations, new features
        - general: Everything else
        
        Question: {question}"""
    )

# Use the route
route = route_query("What changed in the auth API in v2.1?")
# → RouteTarget.CHANGELOGS
retriever = retrievers[route.target]
docs = retriever.invoke(question)
```

### 2. Query Decomposition (Break Complex Questions)

```python
class SubQueries(BaseModel):
    queries: list[str] = Field(
        description="2-4 sub-questions that together answer the original",
        min_length=2,
        max_length=4,
    )
    strategy: str = Field(description="How to combine sub-answers")

decomposer = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(SubQueries)

def decompose_query(question: str) -> SubQueries:
    """Break a complex question into retrievable sub-questions."""
    return decomposer.invoke(
        f"""Break this complex question into 2-4 simpler sub-questions
        that can each be answered independently from a document search.
        
        Question: {question}
        
        Rules:
        - Each sub-question should be self-contained
        - Together they should fully answer the original
        - Describe how to combine the sub-answers"""
    )

# Example
result = decompose_query("Compare auth in v1 vs v2 and recommend migration path")
# queries: ["How does authentication work in API v1?",
#           "How does authentication work in API v2?",
#           "What are the migration steps from v1 to v2 auth?"]
# strategy: "Compare v1 vs v2 approaches, then present migration recommendation"
```

### 3. Self-RAG (Iterative Retrieve-Reflect-Revise)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class SelfRAGState(TypedDict):
    question: str
    retrieved_docs: list
    answer: str
    is_grounded: bool
    is_relevant: bool
    iteration: int

def retrieve(state: SelfRAGState) -> SelfRAGState:
    """Retrieve documents for the current question."""
    docs = retriever.invoke(state["question"])
    return {"retrieved_docs": docs, "iteration": state["iteration"] + 1}

def generate(state: SelfRAGState) -> SelfRAGState:
    """Generate answer from retrieved documents."""
    context = "\n".join([d.page_content for d in state["retrieved_docs"]])
    answer = llm.invoke(f"Context: {context}\n\nQuestion: {state['question']}")
    return {"answer": answer.content}

def check_grounding(state: SelfRAGState) -> SelfRAGState:
    """Verify answer is supported by retrieved context."""
    check = llm.invoke(
        f"""Is this answer fully supported by the context? Answer yes/no.
        Context: {state['retrieved_docs']}
        Answer: {state['answer']}"""
    )
    return {"is_grounded": "yes" in check.content.lower()}

def check_relevance(state: SelfRAGState) -> SelfRAGState:
    """Verify answer addresses the question."""
    check = llm.invoke(
        f"""Does this answer address the question? Answer yes/no.
        Question: {state['question']}
        Answer: {state['answer']}"""
    )
    return {"is_relevant": "yes" in check.content.lower()}

def should_retry(state: SelfRAGState) -> str:
    """Decide whether to retry or accept the answer."""
    if state["iteration"] >= 3:
        return "accept"  # Max retries reached
    if state["is_grounded"] and state["is_relevant"]:
        return "accept"
    return "retry"

# Build the graph
graph = StateGraph(SelfRAGState)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_node("check_grounding", check_grounding)
graph.add_node("check_relevance", check_relevance)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", "check_grounding")
graph.add_edge("check_grounding", "check_relevance")
graph.add_conditional_edges("check_relevance", should_retry, {
    "accept": END,
    "retry": "retrieve",
})

self_rag = graph.compile()
```

### 4. Corrective RAG (CRAG)

```python
class CRAGState(TypedDict):
    question: str
    retrieved_docs: list
    doc_relevance: list[str]  # "relevant", "ambiguous", "irrelevant"
    action: str  # "use_docs", "refine_query", "web_search"
    answer: str

def grade_documents(state: CRAGState) -> CRAGState:
    """Grade each retrieved document for relevance."""
    grades = []
    for doc in state["retrieved_docs"]:
        grade = llm.invoke(
            f"""Grade this document's relevance to the question.
            Question: {state['question']}
            Document: {doc.page_content[:500]}
            Grade as: relevant, ambiguous, or irrelevant"""
        )
        grades.append(grade.content.strip().lower())
    return {"doc_relevance": grades}

def decide_action(state: CRAGState) -> str:
    """Decide next action based on document grades."""
    relevant_count = state["doc_relevance"].count("relevant")
    total = len(state["doc_relevance"])
    
    if relevant_count / total > 0.5:
        return "generate"      # Enough good docs, generate answer
    elif relevant_count > 0:
        return "refine"        # Some good docs, refine query for more
    else:
        return "web_search"    # No good docs, try web search fallback

def refine_query(state: CRAGState) -> CRAGState:
    """Rewrite query based on what was missing."""
    refined = llm.invoke(
        f"""The original query didn't retrieve good results.
        Original: {state['question']}
        Rewrite it to be more specific and likely to match relevant documents."""
    )
    return {"question": refined.content}
```

### 5. Multi-Hop Reasoning

```python
class MultiHopState(TypedDict):
    original_question: str
    current_sub_question: str
    accumulated_facts: list[str]
    remaining_hops: list[str]
    final_answer: str

def plan_hops(state: MultiHopState) -> MultiHopState:
    """Plan the chain of questions needed."""
    plan = decomposer.invoke(state["original_question"])
    return {
        "remaining_hops": plan.queries,
        "current_sub_question": plan.queries[0],
    }

def retrieve_and_extract(state: MultiHopState) -> MultiHopState:
    """Retrieve for current sub-question and extract key fact."""
    docs = retriever.invoke(state["current_sub_question"])
    
    fact = llm.invoke(
        f"""Extract the key fact that answers this question.
        Question: {state['current_sub_question']}
        Context: {docs[0].page_content}
        Return just the fact, one sentence."""
    )
    
    new_facts = state["accumulated_facts"] + [fact.content]
    remaining = state["remaining_hops"][1:]
    
    return {
        "accumulated_facts": new_facts,
        "remaining_hops": remaining,
        "current_sub_question": remaining[0] if remaining else "",
    }

def synthesize(state: MultiHopState) -> MultiHopState:
    """Combine accumulated facts into final answer."""
    facts_text = "\n".join(f"- {f}" for f in state["accumulated_facts"])
    
    answer = llm.invoke(
        f"""Using these facts, answer the original question.
        
        Original question: {state['original_question']}
        
        Facts gathered:
        {facts_text}
        
        Synthesize a complete answer."""
    )
    return {"final_answer": answer.content}
```

### 6. Agentic RAG with Tools (LangGraph)

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

@tool
def search_docs(query: str, collection: str = "default") -> str:
    """Search documentation for relevant passages."""
    docs = retrievers[collection].invoke(query)
    return "\n---\n".join([d.page_content for d in docs[:3]])

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return str(eval(expression))  # In production: use a safe evaluator

@tool
def get_current_version(product: str) -> str:
    """Get the current version of a product/API."""
    versions = {"auth_api": "2.1.0", "sdk": "3.4.2"}
    return versions.get(product, "unknown")

# Create agent with tools
tools = [search_docs, calculate, get_current_version]
llm_with_tools = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

class AgentState(TypedDict):
    messages: list
    
def agent_node(state: AgentState) -> AgentState:
    """Agent decides whether to use tools or respond."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def should_continue(state: AgentState) -> str:
    """Check if agent wants to use tools or is done."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "end"

# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "agent")

agent = graph.compile()
```

### 7. When to Use What (Decision Logic)

```python
def select_pipeline(question: str) -> str:
    """Decide which RAG pattern to use for a given question."""
    complexity = assess_complexity(question)
    
    if complexity == "simple":
        return "single_shot_rag"       # "What is X?" → retrieve + generate
    elif complexity == "routed":
        return "routed_rag"            # Clear domain → route + retrieve + generate
    elif complexity == "multi_part":
        return "decomposed_rag"        # "Compare X and Y" → decompose + parallel retrieve
    elif complexity == "needs_verification":
        return "self_rag"              # High-stakes → retrieve + generate + verify
    else:
        return "agentic_rag"           # Complex, multi-step → full agent

def assess_complexity(question: str) -> str:
    """Quick classification of question complexity."""
    # Simple heuristics (augment with LLM classification if needed)
    if any(w in question.lower() for w in ["compare", "vs", "difference"]):
        return "multi_part"
    if any(w in question.lower() for w in ["how to", "steps", "guide"]):
        return "routed"
    if len(question.split()) > 20:
        return "multi_part"
    return "simple"
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Router model | gpt-4o-mini | Cheap, fast, good enough for classification |
| Max iterations (self-RAG) | 3 | Diminishing returns, cost control |
| Decomposition max sub-queries | 4 | More = more latency, rarely needed |
| Tool timeout | 5s per tool call | Prevent hanging on external APIs |
| Agent max steps | 10 | Prevent infinite loops |
| Complexity threshold for agentic | Only multi-step/comparison | Don't over-engineer simple questions |
| Grounding check model | Same as generator (gpt-4o-mini) | Consistency, lower cost |
| State persistence | Required for multi-turn | LangGraph checkpointing |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Agent loops forever | No termination condition or max_steps | Set max iterations, add explicit END condition |
| Decomposition generates bad sub-questions | Sub-questions too vague or overlapping | Constrain decomposer prompt, add examples |
| Router sends to wrong collection | Training data for router insufficient | Add router examples, use few-shot classification |
| Self-RAG keeps retrying (never accepts) | Grounding check too strict | Lower grounding threshold, accept "partially grounded" |
| Multi-hop loses context between hops | Accumulated facts not passed to next step | Ensure state carries all facts through graph |
| Agentic is too slow for production | Using agentic for simple questions | Add complexity classifier, route simple queries to simple RAG |
| Tool calls fail silently | No error handling in tools | Wrap tools with try/except, return error messages |

## Production Considerations

### Latency Impact

| Pattern | Typical Latency | LLM Calls | When to Use |
|---------|----------------|-----------|-------------|
| Single-shot RAG | 1-3s | 1 | 80% of queries |
| Routed RAG | 1.5-3.5s | 2 (route + generate) | Multi-domain |
| Decomposed RAG | 3-8s | 3-5 | Complex questions |
| Self-RAG | 5-15s | 3-9 | High-stakes answers |
| Full agentic | 5-30s | 5-15 | Research/analysis tasks |

### Cost Impact
- Each LLM call = $0.0001-0.001 (gpt-4o-mini) or $0.003-0.03 (gpt-4o)
- Agentic with 10 steps: 10-50x cost of single-shot
- Router adds ~$0.0001 per query (negligible)
- Budget: classify 80% as simple, 15% as routed/decomposed, 5% as agentic

### When NOT to Go Agentic
- Simple factual lookup → single-shot RAG is better (faster, cheaper, more reliable)
- High-throughput low-latency requirements → agentic is too slow
- When you can pre-compute (batch processing) → avoid real-time agentic loops
- When the corpus is small and well-organized → simple RAG with good chunking is enough

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| Correct pattern selection | Does complexity classifier choose right pipeline? | > 90% |
| Answer quality (complex queries) | RAGAS faithfulness on multi-hop questions | > 0.85 |
| Iteration efficiency | Average iterations before accepting answer | < 2.5 |
| Tool call success rate | % of tool invocations that return valid results | > 95% |
| Total latency | End-to-end for agentic queries | < 15s p95 |
| Cost per agentic query | Total LLM calls × pricing | < $0.01 |
| Routing accuracy | % of queries sent to correct collection | > 92% |

## Ready to Ship? — Checklist

- [ ] Complexity classifier routes 80%+ queries to simple RAG (fast path)
- [ ] Router tested with representative queries from each domain
- [ ] Decomposition produces useful sub-questions (manual review of 20 examples)
- [ ] Self-RAG terminates reliably (max iterations enforced)
- [ ] Agent has explicit termination conditions (max steps, timeout)
- [ ] All tools have error handling (no silent failures)
- [ ] Latency acceptable for the use case (agentic queries may be 5-15s)
- [ ] Cost monitored per query pattern (simple vs agentic)
- [ ] State management working for multi-turn conversations
- [ ] Fallback: if agentic fails, degrade to simple RAG gracefully
