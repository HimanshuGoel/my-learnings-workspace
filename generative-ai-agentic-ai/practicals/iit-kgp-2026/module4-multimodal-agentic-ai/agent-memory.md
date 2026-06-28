# Agent Memory

## What This Enables

Memory gives agents the ability to maintain context across conversation turns and sessions — remembering user preferences, past interactions, and learned facts. Without memory, every invocation starts from zero. With well-designed memory, agents build up knowledge over time and personalize responses — like a colleague who remembers what you discussed last week.

## Architecture Overview

### Memory Types

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENT MEMORY                              │
├──────────────────┬──────────────────┬───────────────────────────┤
│  WORKING MEMORY  │  SHORT-TERM      │  LONG-TERM               │
│                  │                  │                           │
│  Current task    │  This session    │  Across sessions          │
│  state, plan,    │  message history │  • Semantic (vector)      │
│  intermediate    │  (in context     │  • Episodic (past events) │
│  results         │   window)        │  • Summary (compressed)   │
│                  │                  │                           │
│  Lives in:       │  Lives in:       │  Lives in:                │
│  Graph state     │  Checkpoint      │  Vector store / DB        │
└──────────────────┴──────────────────┴───────────────────────────┘
```

### Memory Flow Per Turn

```
User Message → RETRIEVE (semantic search + checkpoint) → AGENT LLM → STORE (if noteworthy)
                    │                                         │              │
                    └── context window contains:              │              └── save to vector
                        system prompt + memories +            │                  store for future
                        recent messages + query              │
                                                            ▼
                                                       Response
```

## Key Patterns & When to Use Each

| Pattern | What It Stores | Context Cost | Persistence | Best For |
|---------|---------------|-------------|-------------|----------|
| Buffer (all) | Every message verbatim | High (grows) | Session | Short conversations (<20 turns) |
| Window (last N) | Last N messages only | Fixed | Session | Chat UIs with predictable length |
| Summary | Compressed history | Low (fixed) | Persistent | Long conversations, cost-sensitive |
| Semantic (vector) | Facts retrieved on demand | Variable (top-k) | Persistent | Cross-session knowledge |
| Hybrid | Summary + semantic | Medium | Persistent | Production assistants |

### Context Window Budget

```
Total: 128K tokens (GPT-4o)
  System prompt:       ~500 tokens
  Retrieved memories: ~1000 tokens
  Summary:             ~300 tokens
  Recent messages:    ~2000 tokens
  Tool definitions:    ~800 tokens
  ─────────────────────────────────
  USED:              ~4800 tokens  → plenty of room

For 4K-16K models, budget is TIGHT — memory management is critical.
```

## Implementation with LangGraph/LangChain

### Built-in Checkpointing (Short-Term Memory)

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]

llm = ChatOpenAI(model="gpt-4o-mini")

def agent_node(state: State) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

agent = graph.compile(checkpointer=MemorySaver())

# Same thread_id = same conversation (memory persists)
config = {"configurable": {"thread_id": "user-42-session-1"}}
agent.invoke({"messages": [HumanMessage("I'm working on a Python project")]}, config)
agent.invoke({"messages": [HumanMessage("What language am I using?")]}, config)
# → "You're working on Python."
```

### Conversation Summarization

```python
from langchain_core.messages import SystemMessage

def summarize_conversation(messages: list, max_messages: int = 10) -> list:
    """Summarize older messages when conversation exceeds max length."""
    if len(messages) <= max_messages:
        return messages

    old_messages = messages[1:-max_messages]
    recent_messages = messages[-max_messages:]

    summary = llm.invoke([
        SystemMessage(content="Summarize this conversation in 2-3 sentences."),
        HumanMessage(content="\n".join(f"{m.type}: {m.content}" for m in old_messages))
    ]).content

    return [
        messages[0],  # Original system message
        SystemMessage(content=f"[Previous conversation summary: {summary}]"),
        *recent_messages,
    ]
```

### Semantic Memory (Vector Store for Long-Term Facts)

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool
from datetime import datetime

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
memory_store = FAISS.from_texts(["initialized"], embeddings)

@tool
def remember(fact: str, category: str = "general") -> str:
    """Store an important fact for future reference.
    Use when user shares preferences, project context, or asks you to remember.
    Categories: 'preference', 'project', 'personal', 'general'."""
    doc = Document(
        page_content=fact,
        metadata={"category": category, "timestamp": datetime.now().isoformat()}
    )
    memory_store.add_documents([doc])
    return f"Stored: '{fact}' (category: {category})"

@tool
def recall(query: str, k: int = 3) -> str:
    """Retrieve relevant memories. Use when you need context about the user."""
    results = memory_store.similarity_search(query, k=k)
    if not results:
        return "No relevant memories found."
    return "Memories:\n" + "\n".join(f"- [{r.metadata.get('category')}] {r.page_content}" for r in results)
```

### Full Memory-Augmented Agent

```python
from langgraph.prebuilt import ToolNode

class MemoryState(TypedDict):
    messages: Annotated[list, add]
    memory_context: str

def retrieve_memories_node(state: MemoryState) -> dict:
    """Auto-retrieve relevant memories before agent responds."""
    last_msg = next((m.content for m in reversed(state["messages"]) if m.type == "human"), "")
    results = memory_store.similarity_search(last_msg, k=3)
    context = "\n".join(f"- {r.page_content}" for r in results) if results else ""
    return {"memory_context": context}

def agent_node(state: MemoryState) -> dict:
    prefix = f"\n[Known about user:\n{state['memory_context']}]" if state.get("memory_context") else ""
    messages = [SystemMessage(content=f"You are helpful.{prefix}"), *state["messages"]]
    response = llm.bind_tools([remember, recall]).invoke(messages)
    return {"messages": [response]}

def should_continue(state: MemoryState) -> str:
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END

graph = StateGraph(MemoryState)
graph.add_node("retrieve", retrieve_memories_node)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode([remember, recall]))
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

memory_agent = graph.compile(checkpointer=MemorySaver())
```

## State Management & Memory

| Layer | Mechanism | Lifetime | Size Limit |
|-------|-----------|----------|-----------|
| Working | LangGraph state (TypedDict) | Single invocation | Keep lean |
| Short-term | Checkpointing (thread_id) | Conversation session | Grows with messages |
| Long-term | Vector store (FAISS/Pinecone) | Forever | Storage-limited |
| Compressed | Summary messages | Session | Fixed (~300 tokens) |

## Error Handling & Guardrails

| Failure Mode | Symptom | Prevention |
|-------------|---------|-----------|
| Context overflow | Messages exceed model window | Summarize old messages, enforce window |
| Stale memories | Outdated facts retrieved | Timestamps, prefer recent, allow "forget" |
| Memory hallucination | Agent "remembers" unstored things | Only retrieve from actual store |
| Irrelevant retrieval | Wrong memories injected | Tune similarity threshold, filter by category |
| Checkpoint bloat | DB grows unbounded | TTL on old threads, archive completed sessions |

```python
def enforce_memory_budget(memories: str, budget_tokens: int = 1000) -> str:
    """Truncate retrieved memories to fit token budget."""
    max_chars = budget_tokens * 4  # ~1 token ≈ 4 chars
    if len(memories) <= max_chars:
        return memories
    return memories[:max_chars] + "\n[...older memories omitted]"
```

## Testing & Debugging

```python
def test_checkpoint_persistence():
    config = {"configurable": {"thread_id": "test-thread"}}
    memory_agent.invoke({"messages": [HumanMessage("My name is Alice")]}, config)
    result = memory_agent.invoke({"messages": [HumanMessage("What's my name?")]}, config)
    assert "Alice" in result["messages"][-1].content

def test_remember_and_recall():
    result = remember.invoke({"fact": "Prefers dark mode", "category": "preference"})
    assert "Stored" in result
    assert "dark mode" in recall.invoke({"query": "UI preferences"})

# Debug: inspect checkpoint
state = memory_agent.get_state({"configurable": {"thread_id": "test"}})
print(f"Messages: {len(state.values['messages'])}")
```

## Production Considerations

### Latency & Cost

- Checkpoint load: 5-50ms (memory) / 20-200ms (Postgres)
- Vector search: 10-50ms (FAISS local) / 50-200ms (cloud)
- Summarization: 500-1500ms (one LLM call, batch or async)
- Main cost driver: How much memory context goes into each LLM call

### Storage Planning

- Checkpoints: ~2KB per turn
- Vector store: ~1.5KB per memory
- 1000 users × 50 sessions × 20 turns = ~2GB checkpoint data

## Integration Points

- **Module 2 (RAG):** Semantic memory IS a RAG retriever — same vector store patterns
- **Module 4 (LangGraph):** Checkpointing is built into LangGraph compilation
- **Module 4 (Planning):** Plans stored in working memory (graph state)
- **Module 4 (Multi-Agent):** Shared memory via common vector store
- **Module 5 (Deployment):** PostgresSaver for production, Redis for fast access

## Architecture Decision Record

**Decision:** Hybrid memory — LangGraph checkpointing for short-term + vector store for long-term + summarization for compression.

**Why:** No single mechanism handles all needs. Checkpointing handles multi-turn flow. Vectors handle cross-session recall. Summarization prevents context overflow. The combination covers all practical cases.

**Trade-off accepted:** More infrastructure (checkpoint store + vector store + summarization). Three moving parts. Worth it for production assistants that need all three layers.

**When to reconsider:** Short sessions (<10 turns): checkpointing alone. Knowledge-heavy bots: prioritize semantic memory. Cost-sensitive: skip summarization, just window last N messages.
