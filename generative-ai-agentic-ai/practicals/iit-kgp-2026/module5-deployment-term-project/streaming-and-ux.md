# Streaming & UX — Deployment Runbook

## 1. What You're Deploying

Real-time streaming for AI responses — token-by-token output plus intermediate agent steps ("Searching knowledge base...", "Analyzing results..."). Without streaming, users stare at a blank screen for 5-30 seconds.

**AI-specific challenge:** LLM responses are generated sequentially (autoregressive). Unlike database queries that return all-at-once, you can stream partial results as they're generated. Agents add complexity: multiple tool calls interleaved with LLM reasoning, each needing status updates.

**From Module 4:** Your LangGraph agent has multiple nodes (retriever → reasoner → tool caller → synthesizer). Each node transition is a streaming opportunity to show progress.

## 2. Prerequisites & Dependencies

```bash
pip install sse-starlette fastapi langchain-core langgraph
# Client-side: no packages needed (native EventSource API)
```

| Requirement | Why |
|-------------|-----|
| FastAPI app running (Topic 1) | Server to add streaming to |
| LangGraph agent (Module 4) | Multi-step agent to stream |
| Understanding of async generators | Python pattern for streaming |

## 3. Step-by-Step Procedure

### 3.1 Server-Sent Events (SSE) — Token Streaming

```python
# app/streaming.py
import json
import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from langchain_core.messages import HumanMessage

router = APIRouter()

async def stream_llm_tokens(messages: list[dict]) -> AsyncGenerator[dict, None]:
    """Stream individual tokens from the LLM."""
    from app.deps import get_llm

    llm = get_llm()
    langchain_messages = [HumanMessage(content=m["content"]) for m in messages if m["role"] == "user"]

    async for chunk in llm.astream(langchain_messages):
        yield {
            "event": "token",
            "data": json.dumps({"content": chunk.content, "type": "token"})
        }

    yield {"event": "done", "data": json.dumps({"type": "done"})}

@router.post("/chat/stream")
async def chat_stream(request: Request):
    """SSE endpoint for token-by-token streaming."""
    body = await request.json()
    messages = body.get("messages", [])

    return EventSourceResponse(stream_llm_tokens(messages))
```

### 3.2 Agent Step Streaming (Intermediate Status Updates)

```python
# app/agent_streaming.py
import json
from typing import AsyncGenerator
from langgraph.graph import StateGraph
from app.agent_graph import build_graph, AgentState

async def stream_agent_steps(query: str, session_id: str) -> AsyncGenerator[dict, None]:
    """Stream agent execution: status updates + final tokens."""
    graph = build_graph()

    # Stream events from LangGraph
    async for event in graph.astream_events(
        {"messages": [{"role": "user", "content": query}]},
        config={"configurable": {"session_id": session_id}},
        version="v2"
    ):
        kind = event["event"]

        # Node transitions → status updates
        if kind == "on_chain_start" and event.get("name"):
            node_name = event["name"]
            status_map = {
                "retrieve": "Searching knowledge base...",
                "grade_documents": "Evaluating relevance...",
                "generate": "Generating response...",
                "web_search": "Searching the web...",
                "tool_executor": f"Using tool: {event.get('data', {}).get('tool', 'unknown')}..."
            }
            if node_name in status_map:
                yield {
                    "event": "status",
                    "data": json.dumps({
                        "type": "status",
                        "step": node_name,
                        "message": status_map[node_name]
                    })
                }

        # LLM token streaming within generate node
        elif kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield {
                    "event": "token",
                    "data": json.dumps({"type": "token", "content": content})
                }

        # Tool results
        elif kind == "on_tool_end":
            yield {
                "event": "tool_result",
                "data": json.dumps({
                    "type": "tool_result",
                    "tool": event.get("name", "unknown"),
                    "result_preview": str(event["data"].get("output", ""))[:200]
                })
            }

    # Final event
    yield {"event": "done", "data": json.dumps({"type": "done"})}
```

### 3.3 SSE Event Protocol Design

```python
# Event types your client should handle:
EVENT_TYPES = {
    "status":       "Intermediate step notification (show as status bar)",
    "token":        "Single token from LLM (append to response text)",
    "tool_result":  "Tool execution completed (show in collapsible section)",
    "source":       "Retrieved source document (show as citation)",
    "error":        "Something went wrong (show error UI)",
    "done":         "Stream complete (finalize UI state)",
}

# Example SSE wire format:
# event: status
# data: {"type": "status", "step": "retrieve", "message": "Searching knowledge base..."}
#
# event: token
# data: {"type": "token", "content": "Based"}
#
# event: token
# data: {"type": "token", "content": " on"}
#
# event: done
# data: {"type": "done"}
```

### 3.4 Client-Side Implementation

```javascript
// client/chat.js — Vanilla JS (no framework needed)
class AIStreamClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
    this.controller = null;
  }

  async streamChat(messages, callbacks) {
    // AbortController for cancellation
    this.controller = new AbortController();

    const response = await fetch(`${this.baseUrl}/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages }),
      signal: this.controller.signal
    });

    if (!response.ok) {
      callbacks.onError?.(`HTTP ${response.status}: ${response.statusText}`);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep incomplete line in buffer

        let currentEvent = '';
        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.slice(7);
          } else if (line.startsWith('data: ') && currentEvent) {
            const data = JSON.parse(line.slice(6));
            this.handleEvent(currentEvent, data, callbacks);
            currentEvent = '';
          }
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        callbacks.onError?.(err.message);
      }
    }

    callbacks.onComplete?.();
  }

  handleEvent(event, data, callbacks) {
    switch (event) {
      case 'status':
        callbacks.onStatus?.(data.message);
        break;
      case 'token':
        callbacks.onToken?.(data.content);
        break;
      case 'tool_result':
        callbacks.onToolResult?.(data);
        break;
      case 'error':
        callbacks.onError?.(data.message);
        break;
      case 'done':
        // Stream finished — handled by reader loop exit
        break;
    }
  }

  cancel() {
    this.controller?.abort();
  }
}

// Usage:
const client = new AIStreamClient('http://localhost:8000');
let fullResponse = '';

client.streamChat(
  [{ role: 'user', content: 'Explain RAG architecture' }],
  {
    onStatus: (msg) => showTypingIndicator(msg),
    onToken: (token) => { fullResponse += token; updateResponseUI(fullResponse); },
    onToolResult: (result) => showCollapsibleToolResult(result),
    onError: (err) => showErrorBanner(err),
    onComplete: () => hideTypingIndicator()
  }
);
```

### 3.5 Error Recovery and Reconnection

```javascript
// client/resilient-stream.js
async function streamWithRetry(messages, callbacks, maxRetries = 3) {
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      await client.streamChat(messages, callbacks);
      return; // Success
    } catch (err) {
      attempt++;
      if (attempt >= maxRetries) {
        callbacks.onError?.(`Failed after ${maxRetries} attempts: ${err.message}`);
        return;
      }
      // Exponential backoff
      const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
      callbacks.onStatus?.(`Connection lost. Retrying in ${delay/1000}s...`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
}
```

### 3.6 Timeout and Cancellation (Server Side)

```python
# app/streaming.py — add timeout protection
import asyncio
from fastapi import HTTPException

async def stream_with_timeout(generator, timeout_seconds=120):
    """Wrap async generator with overall timeout."""
    try:
        async with asyncio.timeout(timeout_seconds):
            async for event in generator:
                yield event
    except asyncio.TimeoutError:
        yield {
            "event": "error",
            "data": json.dumps({
                "type": "error",
                "message": "Response generation timed out. Try a shorter query."
            })
        }
```

## 4. Configuration Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAM_TIMEOUT_SECONDS` | Max time for full stream | `120` |
| `SSE_KEEPALIVE_INTERVAL` | Ping interval to keep connection alive | `15` |
| `MAX_TOKENS_STREAM` | Token limit for streaming responses | `2048` |
| `ENABLE_STEP_STREAMING` | Show intermediate agent steps | `true` |

## 5. Verification & Smoke Tests

```bash
# Test SSE stream is working (should see events flowing)
curl -N -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'

# Verify event format
curl -N -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Search for deployment guides"}]}' \
  2>&1 | head -20
# Should see: event: status, event: token, event: done
```

## 6. Monitoring & Alerting

| Metric | Alert Threshold | Why |
|--------|----------------|-----|
| Stream duration p95 | > 30s | Slow generation or stuck agent |
| Abandoned streams | > 20% | UX issue — users giving up |
| Time to first token | > 3s | Cold start or slow retrieval |
| SSE connection errors | > 5% | Network/proxy issues |

## 7. Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| No streaming, full response at once | Reverse proxy buffering | Set `X-Accel-Buffering: no` header, disable nginx buffering |
| Stream cuts off mid-response | Proxy timeout (30s default) | Increase proxy timeout, add keepalive pings |
| Duplicate tokens | Client reconnecting without offset tracking | Implement event IDs, resume from last-event-id |
| "Failed to fetch" on client | CORS not configured for streaming | Add SSE content-type to allowed headers |
| Tokens arrive in bursts, not smoothly | LLM batching tokens before flush | This is normal for some providers; add artificial smoothing client-side if needed |

## 8. Security & Compliance

- Validate session ownership before streaming (user can only stream their own requests)
- Rate limit stream connections per user (prevent resource exhaustion)
- Don't stream internal tool results containing sensitive data — filter before emitting
- Set max connection duration to prevent indefinite open connections

## 9. Cost Management

- Streaming doesn't cost more tokens — same input/output, just delivered incrementally
- BUT: abandoned streams still consume full token budget (generation already happened)
- Implement client-side "stop generating" that signals server to abort LLM call
- Track abandoned stream rate — high rates suggest poor UX or slow responses

## 10. Maintenance & Updates

- **SSE vs WebSocket decision:** SSE is simpler, works through proxies, sufficient for AI UX (server→client only). Use WebSocket only if you need bidirectional (e.g., collaborative editing)
- **Adding new event types:** Add to server, update client switch statement, backward-compatible
- **Load balancing:** SSE is long-lived HTTP — ensure load balancer supports connection persistence
- **Proxy config:** Nginx needs `proxy_buffering off;` and `proxy_read_timeout 300s;` for SSE
