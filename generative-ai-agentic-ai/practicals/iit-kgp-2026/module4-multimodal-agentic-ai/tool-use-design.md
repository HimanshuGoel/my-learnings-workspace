# Tool Use Design

## What This Enables

Tools turn LLMs from text generators into action-takers. A well-designed tool interface lets agents search databases, call APIs, execute code, and modify systems — reliably. Poor tool design leads to hallucinated parameters, wrong tool selection, and silent failures. This topic covers how to design tool interfaces that agents can use correctly and recover from gracefully.

## Architecture Overview

### How Tool Use Works

```
1. LLM sees tool definitions (name, description, parameters schema)
2. LLM decides which tool to call and with what arguments (structured output)
3. Runtime validates arguments against schema
4. Tool function executes
5. Result is returned to LLM as a ToolMessage
6. LLM incorporates result and decides next step (call another tool or respond)
```

### The Tool Contract

```python
@tool
def search_documentation(
    query: str,           # What to search for
    collection: str,      # Which doc set to search
    max_results: int = 5, # How many results
) -> str:
    """Search technical documentation for relevant passages.
    
    Use this when the user asks about API usage, configuration,
    or troubleshooting. Returns relevant text passages with sources.
    """
    # Implementation...
```

The LLM sees: name + docstring + parameter schema. The docstring IS your prompt to the LLM about when/how to use the tool.

## Key Patterns & When to Use Each

| Pattern | When | Example |
|---------|------|---------|
| Simple tool | Stateless computation | Calculator, unit conversion |
| Tool with confirmation | Destructive/expensive actions | Delete file, send email |
| Tool with retries | Unreliable external APIs | Web search, DB queries |
| Authenticated tool | Access-controlled resources | Internal APIs, databases |
| Multi-step tool | Complex operations | "Create and configure a VM" |
| Tool with schema validation | Strict input requirements | API calls with specific formats |

## Implementation with LangChain

### Basic Tool Design

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Simple tool
@tool
def get_weather(city: str, units: str = "celsius") -> str:
    """Get current weather for a city. Use when user asks about weather conditions."""
    # Implementation
    return f"Weather in {city}: 22°{units[0].upper()}, sunny"

# Tool with Pydantic schema (more control)
class SearchInput(BaseModel):
    query: str = Field(description="The search query")
    collection: str = Field(description="Which collection to search: 'docs', 'code', 'issues'")
    max_results: int = Field(default=5, ge=1, le=20, description="Number of results (1-20)")

@tool(args_schema=SearchInput)
def search_docs(query: str, collection: str, max_results: int = 5) -> str:
    """Search documentation, code examples, or GitHub issues.
    
    Use 'docs' for API documentation and guides.
    Use 'code' for code examples and implementations.
    Use 'issues' for bug reports and feature requests.
    """
    results = vector_store.similarity_search(query, k=max_results, 
                                              filter={"collection": collection})
    return "\n---\n".join([f"[{r.metadata['source']}] {r.page_content}" for r in results])
```

### Error Wrapping (Critical for Agent Reliability)

```python
@tool
def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the analytics database.
    Only SELECT queries are allowed. Returns results as formatted table."""
    try:
        if not sql.strip().upper().startswith("SELECT"):
            return "ERROR: Only SELECT queries are allowed. Please rewrite as a SELECT statement."
        
        result = db.execute(sql)
        if not result:
            return "Query returned no results. Consider broadening your search criteria."
        
        return format_as_table(result)
    
    except SyntaxError as e:
        return f"SQL syntax error: {e}. Please fix the query and try again."
    except TimeoutError:
        return "Query timed out (>30s). Try adding LIMIT or narrowing the WHERE clause."
    except Exception as e:
        return f"Database error: {type(e).__name__}: {e}. Please try a different approach."
```

### Tool with Confirmation Pattern

```python
from typing import Literal

class DeleteAction(BaseModel):
    target: str = Field(description="What to delete")
    confirmed: bool = Field(default=False, description="Set to true to confirm deletion")

@tool(args_schema=DeleteAction)
def delete_resource(target: str, confirmed: bool = False) -> str:
    """Delete a resource. REQUIRES confirmed=true to actually execute.
    First call with confirmed=false to see what would be deleted.
    Then call again with confirmed=true to execute."""
    
    if not confirmed:
        return f"PREVIEW: Would delete '{target}'. Call again with confirmed=true to proceed."
    
    # Actually delete
    perform_delete(target)
    return f"Successfully deleted '{target}'."
```

### Binding Tools to LLM

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_weather, search_docs, query_database, delete_resource]
llm_with_tools = llm.bind_tools(tools)

# LLM now sees all tool schemas and can call them
response = llm_with_tools.invoke("What's the weather in Mumbai?")
# response.tool_calls = [{"name": "get_weather", "args": {"city": "Mumbai"}}]
```

### In LangGraph

```python
from langgraph.prebuilt import ToolNode

# ToolNode automatically executes tool calls from the LLM
tool_node = ToolNode(tools)

# In graph:
graph.add_node("agent", call_model)
graph.add_node("tools", tool_node)
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")
```

## State Management & Memory

- Tool results are added to message history (LLM sees previous tool calls + results)
- For long conversations: summarize old tool results to save tokens
- Tool execution is stateless by default — add state via closure or dependency injection
- Track tool usage count in graph state (for budgeting)

## Error Handling & Guardrails

| Failure Mode | Symptom | Prevention |
|-------------|---------|-----------|
| Tool hallucination | LLM calls tool that doesn't exist | Bind only available tools, validate tool name |
| Wrong tool selected | LLM picks search when it should calculate | Better tool descriptions, add "use this when..." |
| Invalid arguments | LLM passes wrong types or missing required fields | Pydantic schema validation, helpful error messages |
| Tool timeout | External API hangs | Timeout wrapper, return error message (not exception) |
| Infinite tool loop | Agent calls same tool repeatedly with same args | Track call history in state, detect repetition |
| Sensitive data exposure | Tool returns PII or secrets | Filter tool output before returning to LLM |

### Tool Description Best Practices

```python
# BAD: Vague description (LLM won't know when to use it)
@tool
def search(q: str) -> str:
    """Search for information."""

# GOOD: Specific, with usage guidance
@tool
def search_company_docs(query: str) -> str:
    """Search internal company documentation for policies, procedures, and guides.
    
    Use this when the user asks about:
    - Company policies (HR, security, travel)
    - Internal processes (onboarding, approvals)
    - Technical standards and guidelines
    
    Do NOT use for: general knowledge questions, current events, code examples.
    """
```

## Testing & Debugging

```python
# Test tools independently (they're just functions)
def test_search_docs():
    result = search_docs.invoke({"query": "authentication", "collection": "docs", "max_results": 3})
    assert "auth" in result.lower()
    assert len(result) > 0

# Test tool selection (does the agent pick the right tool?)
def test_agent_selects_correct_tool():
    response = llm_with_tools.invoke("What is 15% of 200?")
    assert response.tool_calls[0]["name"] == "calculate"  # Not search_docs!

# Test error handling (does the agent recover from tool errors?)
def test_agent_handles_tool_error():
    result = agent.invoke({"messages": [HumanMessage("Run query: DELEET FROM users")]})
    # Agent should get error message and either fix the query or tell user
    assert "error" not in result["messages"][-1].content.lower() or "syntax" in result["messages"][-1].content.lower()
```

## Production Considerations

### Latency
- Tool execution adds 100ms-5s per call (depends on what tool does)
- Multiple sequential tool calls: latency stacks
- Strategy: parallelize independent tool calls where possible

### Cost
- Each tool call = 1 LLM round-trip (input: messages + tool result, output: next action)
- More tools in the schema = more tokens per request (schema is sent every time)
- Strategy: Only bind relevant tools (don't give agent 50 tools if it needs 5)

### Security
- Never execute arbitrary code from LLM output without sandboxing
- Validate ALL tool inputs against schema before execution
- Rate-limit tool calls (especially destructive ones)
- Log all tool executions for audit trail

## Integration Points

- **Module 2 (RAG):** Retriever as a tool (search_documents)
- **Module 4 (LangGraph):** Tools are nodes in the agent graph
- **Module 4 (Multi-Agent):** Each sub-agent can have its own tool set
- **Module 5 (Deployment):** Tools may call external APIs (auth, rate limits matter)

## Architecture Decision Record

**Decision:** Design tools with explicit error messages (never raise exceptions to the LLM).

**Why:** When a tool raises an unhandled exception, the agent can't recover. When it returns a helpful error STRING, the agent can understand what went wrong and try a different approach. This is the single most important tool design decision.

**Trade-off accepted:** More boilerplate in each tool (try/except + formatted error messages). Worth it for agent reliability.

**When to reconsider:** For internal tools that truly can't fail (pure computation), exceptions are fine. For any external dependency (APIs, DBs, files), always wrap.
