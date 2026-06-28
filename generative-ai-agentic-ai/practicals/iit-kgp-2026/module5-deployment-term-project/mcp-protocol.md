# MCP Protocol — Deployment Runbook

## 1. What You're Deploying

Model Context Protocol (MCP) standardizes how AI assistants (Claude, Kiro, Cursor, Copilot) connect to external tools and data sources. Instead of building tool integrations per assistant, you build ONE MCP server that works everywhere.

**AI-specific challenge:** Every AI IDE/assistant has its own tool-calling mechanism. MCP provides a universal protocol so your Module 4 tools (search, database, APIs) become available to any MCP-compatible client without rewrites.

**From Module 4:** Your LangGraph agent used tools via `@tool` decorators. MCP wraps those same capabilities in a standardized transport that any AI assistant can discover and invoke.

## 2. Prerequisites & Dependencies

```bash
pip install mcp[cli] httpx pydantic
# For HTTP transport (production)
pip install uvicorn starlette
```

| Requirement | Why |
|-------------|-----|
| Python 3.11+ | MCP SDK requires modern async |
| Module 4 tool implementations | The capabilities you're exposing |
| Understanding of JSON-RPC | MCP uses JSON-RPC 2.0 over stdio/HTTP |

## 3. Step-by-Step Procedure

### 3.1 MCP Server — Basic Structure

```python
# mcp_server/server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource, ResourceTemplate
import json

# Create server instance
server = Server("my-ai-tools")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Declare available tools for AI assistants to discover."""
    return [
        Tool(
            name="search_documents",
            description="Search internal knowledge base using semantic search. "
                        "Returns relevant document chunks with source attribution.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 5
                    },
                    "filter_source": {
                        "type": "string",
                        "description": "Optional: filter by document source",
                        "enum": ["confluence", "github", "docs"]
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="query_database",
            description="Execute read-only SQL queries against the analytics database. "
                        "Only SELECT statements are allowed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "SQL SELECT query"
                    }
                },
                "required": ["sql"]
            }
        ),
        Tool(
            name="create_ticket",
            description="Create a Jira ticket with title, description, and priority.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
                },
                "required": ["title", "description"]
            }
        )
    ]
```

### 3.2 Tool Implementation

```python
# mcp_server/server.py (continued)
from mcp_server.vector_store import search_vectors
from mcp_server.database import execute_readonly_query
from mcp_server.jira_client import create_jira_ticket

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool and return results."""
    match name:
        case "search_documents":
            results = await search_vectors(
                query=arguments["query"],
                top_k=arguments.get("top_k", 5),
                source_filter=arguments.get("filter_source")
            )
            return [TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]

        case "query_database":
            sql = arguments["sql"]
            # Security: reject non-SELECT statements
            if not sql.strip().upper().startswith("SELECT"):
                return [TextContent(type="text", text="Error: Only SELECT queries allowed.")]
            rows = await execute_readonly_query(sql)
            return [TextContent(type="text", text=json.dumps(rows, indent=2))]

        case "create_ticket":
            ticket = await create_jira_ticket(
                title=arguments["title"],
                description=arguments["description"],
                priority=arguments.get("priority", "medium")
            )
            return [TextContent(type="text", text=f"Created ticket: {ticket['key']}")]

        case _:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
```

### 3.3 Resource Definitions (Context for AI)

```python
# mcp_server/server.py (continued)

@server.list_resources()
async def list_resources() -> list[Resource]:
    """Expose data sources the AI can read for context."""
    return [
        Resource(
            uri="docs://architecture/overview",
            name="System Architecture Overview",
            description="High-level architecture document for the platform",
            mimeType="text/markdown"
        ),
        Resource(
            uri="docs://runbooks/incident-response",
            name="Incident Response Runbook",
            description="Step-by-step incident response procedures",
            mimeType="text/markdown"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Return resource content when AI requests it."""
    resource_map = {
        "docs://architecture/overview": "docs/architecture.md",
        "docs://runbooks/incident-response": "docs/incident-response.md",
    }
    file_path = resource_map.get(str(uri))
    if not file_path:
        raise ValueError(f"Resource not found: {uri}")
    with open(file_path) as f:
        return f.read()
```

### 3.4 Server Entry Point

```python
# mcp_server/__main__.py
import asyncio
from mcp.server.stdio import stdio_server
from mcp_server.server import server

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.5 HTTP Transport (for Remote Deployment)

```python
# mcp_server/http_transport.py
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp_server.server import server

sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())

routes = [
    Route("/sse", endpoint=handle_sse),
    Mount("/messages/", app=sse.handle_post_message),
]

app = Starlette(routes=routes)

# Run with: uvicorn mcp_server.http_transport:app --host 0.0.0.0 --port 8080
```

### 3.6 Client Configuration

```json
// mcp.json — used by Claude Desktop, Kiro, Cursor
{
  "mcpServers": {
    "my-ai-tools": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "cwd": "/path/to/mcp_server",
      "env": {
        "VECTOR_DB_URL": "http://localhost:8001",
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}",
        "DB_CONNECTION_STRING": "${DB_CONNECTION_STRING}"
      }
    }
  }
}
```

For remote HTTP transport:

```json
{
  "mcpServers": {
    "my-ai-tools-remote": {
      "url": "https://mcp.your-company.com/sse",
      "headers": {
        "Authorization": "Bearer ${MCP_AUTH_TOKEN}"
      }
    }
  }
}
```

## 4. Configuration Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `VECTOR_DB_URL` | ChromaDB/Qdrant endpoint | `http://localhost:8001` |
| `DB_CONNECTION_STRING` | Read-only database connection | (required for query tool) |
| `JIRA_API_TOKEN` | Jira Cloud API token | (required for ticket tool) |
| `JIRA_BASE_URL` | Jira instance URL | (required for ticket tool) |
| `MCP_AUTH_TOKEN` | Bearer token for HTTP transport | (required for remote) |
| `MCP_LOG_LEVEL` | Server logging verbosity | `info` |
| `MAX_SEARCH_RESULTS` | Cap on search results returned | `10` |

## 5. Verification & Smoke Tests

```bash
# Test with MCP CLI inspector (built into mcp package)
mcp dev mcp_server/server.py

# List available tools
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' | python -m mcp_server

# Test tool invocation
echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "search_documents", "arguments": {"query": "deployment guide"}}, "id": 2}' | python -m mcp_server

# Verify in Claude Desktop: check MCP icon shows your tools
# Verify in Kiro: power should appear after mcp.json configuration
```

## 6. Monitoring & Alerting

| Metric | Alert Threshold | Why |
|--------|----------------|-----|
| Tool call latency | > 5s | Underlying service degraded |
| Tool error rate | > 10% | Integration broken |
| Resource read failures | Any | File/DB access issue |
| Concurrent connections | > 50 | May need scaling |

## 7. Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Tools not appearing in AI assistant | `mcp.json` path wrong or server crash on start | Check `cwd`, run server manually to see errors |
| "Connection reset" errors | Server process died | Add restart policy, check for unhandled exceptions |
| Tool returns empty results | Vector DB not populated or query mismatch | Verify DB has embeddings, test search directly |
| Slow tool responses freeze the assistant | Blocking I/O in async handler | Use `asyncio.to_thread()` for sync libraries |
| SQL injection via query tool | No input sanitization | Enforce read-only user, validate SQL AST |

## 8. Security & Compliance

- **Read-only database user:** The DB connection should ONLY have SELECT permissions
- **Input validation:** Validate all tool arguments against schema before execution
- **Secret management:** Never log API tokens; use environment variables
- **Audit logging:** Log every tool call (who invoked, what arguments, what was returned)
- **Network isolation:** HTTP transport should require authentication

## 9. Cost Management

- MCP tools calling LLM APIs incur token costs — apply same budgets as direct API calls
- Cache search results (same query within 5 minutes = cached response)
- Rate limit tool calls per session to prevent runaway loops
- Monitor which tools are called most frequently — optimize those first

## 10. Maintenance & Updates

- **Adding new tools:** Add to `list_tools()` and `call_tool()`, restart server
- **Updating tool schemas:** Backward-compatible changes (new optional fields) are safe; breaking changes need client updates
- **Version strategy:** Semantic versioning for your MCP server; document breaking changes
- **Testing updates:** Use `mcp dev` inspector to verify before deploying to production
