# Observability

## What You're Deploying

Observability infrastructure for your AI system — so you can answer "what happened?" when things go wrong at 3am. Traditional logging isn't enough for AI: you need to trace multi-step LLM reasoning, track token costs, monitor quality metrics, and debug non-deterministic behavior. This covers LangSmith tracing, structured logging, Prometheus metrics, and debugging production AI issues.

## Prerequisites & Dependencies

- Running AI service (FastAPI + LangGraph/LangChain)
- LangSmith account (free tier works for learning)
- Prometheus + Grafana (or cloud equivalent)
- Structured logging library (structlog or loguru)

## Step-by-Step Procedure

### 1. LangSmith Tracing (AI-Specific Observability)

```python
# .env — enable tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your_key_here
LANGCHAIN_PROJECT=my-ai-service-production

# That's it! All LangChain/LangGraph calls are now traced automatically.
# Each trace shows: inputs → LLM calls → tool executions → outputs
# With: latency per step, token count, model used, full prompts
```

```python
# Add metadata per request for filtering in LangSmith
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    metadata={
        "user_id": request.user_id,
        "environment": "production",
        "version": "1.2.3",
    },
    tags=["production", "tier-1-user"],
)
result = agent.invoke({"messages": [...]}, config)
```

### 2. Structured Logging

```python
# app/middleware/logging.py
import structlog
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        start = time.time()
        
        structlog.contextvars.bind_contextvars(request_id=request_id)
        
        try:
            response = await call_next(request)
            latency_ms = (time.time() - start) * 1000
            
            logger.info("request_completed",
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                latency_ms=round(latency_ms, 1),
                user_id=request.state.user_id if hasattr(request.state, "user_id") else None,
            )
            return response
            
        except Exception as e:
            logger.error("request_failed",
                method=request.method,
                path=request.url.path,
                error=str(e),
                error_type=type(e).__name__,
            )
            raise
```

### 3. Prometheus Metrics (Quantitative Monitoring)

```python
# app/middleware/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import APIRouter
from fastapi.responses import Response

# Define metrics
request_count = Counter(
    "ai_requests_total", "Total requests", ["endpoint", "status", "cached"]
)
request_latency = Histogram(
    "ai_request_duration_seconds", "Request latency",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)
tokens_used = Counter(
    "ai_tokens_total", "Tokens consumed", ["model", "direction"]  # direction: input/output
)
active_requests = Gauge(
    "ai_active_requests", "Currently processing requests"
)
agent_steps = Histogram(
    "ai_agent_steps", "Steps per agent invocation",
    buckets=[1, 2, 3, 5, 7, 10, 15, 20]
)
cache_hits = Counter(
    "ai_cache_hits_total", "Cache hit/miss", ["result"]  # hit/miss
)
retrieval_empty = Counter(
    "ai_retrieval_empty_total", "Queries with zero retrieval results"
)

# Metrics endpoint for Prometheus scraping
metrics_router = APIRouter()

@metrics_router.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

### 4. AI-Specific Metrics (Beyond Standard Web Metrics)

```python
# Track AI-specific signals that standard web monitoring misses

class AIMetrics:
    """Metrics specific to AI system health."""
    
    def record_llm_call(self, model: str, input_tokens: int, output_tokens: int, latency_ms: float):
        tokens_used.labels(model=model, direction="input").inc(input_tokens)
        tokens_used.labels(model=model, direction="output").inc(output_tokens)
        # Cost tracking
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        self.daily_cost += cost
    
    def record_retrieval(self, query: str, result_count: int, latency_ms: float):
        if result_count == 0:
            retrieval_empty.inc()
            logger.warning("empty_retrieval", query=query[:100])
    
    def record_agent_run(self, steps: int, tools_used: list[str], success: bool):
        agent_steps.observe(steps)
        if steps >= 10:
            logger.warning("agent_high_steps", steps=steps, tools=tools_used)
    
    def record_quality_signal(self, has_citation: bool, answer_length: int, is_refusal: bool):
        """Proxy quality signals (no ground truth needed)."""
        if answer_length > 2000:
            logger.warning("long_answer", length=answer_length)
        if not has_citation and not is_refusal:
            logger.warning("missing_citation")
```

### 5. Dashboard Layout (Grafana)

```
┌─────────────────────────────────────────────────────────────────┐
│  ROW 1: REQUEST OVERVIEW                                         │
│  [Request Rate] [Latency p50/p95/p99] [Error Rate] [Active Reqs] │
├─────────────────────────────────────────────────────────────────┤
│  ROW 2: AI-SPECIFIC                                              │
│  [Token Usage/hr] [Cost/hr] [Cache Hit Rate] [Empty Retrieval %] │
├─────────────────────────────────────────────────────────────────┤
│  ROW 3: AGENT HEALTH                                             │
│  [Steps Distribution] [Tool Usage] [Step Limit Hits] [Timeouts]  │
├─────────────────────────────────────────────────────────────────┤
│  ROW 4: QUALITY SIGNALS                                          │
│  [Answer Length Dist] [Citation Rate] [Refusal Rate] [Feedback]  │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Alerting Rules

```yaml
# prometheus/alerts.yml
groups:
  - name: ai_service
    rules:
      - alert: HighErrorRate
        expr: rate(ai_requests_total{status="5xx"}[5m]) / rate(ai_requests_total[5m]) > 0.02
        for: 5m
        annotations:
          summary: "Error rate > 2% for 5 minutes"
          action: "Check logs, verify LLM API status"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(ai_request_duration_seconds_bucket[5m])) > 10
        for: 5m
        annotations:
          summary: "p95 latency > 10s"
          action: "Check agent step count, LLM API latency"
      
      - alert: CostSpike
        expr: increase(ai_tokens_total[1h]) > 500000
        annotations:
          summary: "Token usage spike (>500K tokens/hr)"
          action: "Check for agent loops, high traffic, or abuse"
      
      - alert: EmptyRetrieval
        expr: rate(ai_retrieval_empty_total[15m]) / rate(ai_requests_total[15m]) > 0.1
        for: 15m
        annotations:
          summary: "> 10% queries returning zero results"
          action: "Check vector store health, filter configuration"
```

### 7. Debugging Production Issues with Traces

```python
# When a user reports "bad answer" — how to debug:

# 1. Find the trace in LangSmith by request_id or user_id
# 2. See exact: input messages, retrieved docs, LLM prompt, LLM response
# 3. Identify which step went wrong:

# Common debugging patterns:
# - Bad retrieval → check embedding model, chunking, query
# - Hallucination → check if answer is grounded in retrieved context
# - Wrong tool used → check tool descriptions, schema clarity
# - Agent looping → check conditional edge logic, termination conditions
# - Slow response → check which step took longest (LLM? Tool? Retrieval?)

# Pro tip: Add custom metadata to traces for easy filtering
config = RunnableConfig(
    metadata={"query_category": "technical", "user_tier": "premium"}
)
```

## Configuration Reference

| Setting | Value | Purpose |
|---------|-------|---------|
| LANGCHAIN_TRACING_V2 | true | Enable LangSmith tracing |
| LANGCHAIN_PROJECT | service-name-env | Group traces by service |
| Metrics scrape interval | 15s | Prometheus scraping frequency |
| Log retention | 30d (detailed), 90d (metrics) | Balance cost vs debug ability |
| Alert evaluation interval | 1m | How often rules are checked |
| Trace sampling (high traffic) | 10-100% | Reduce cost at scale |

## Verification & Smoke Tests

```bash
# Verify observability is working:
# 1. LangSmith: Make a request → check trace appears within 30s
# 2. Prometheus: curl http://localhost:8000/metrics | grep ai_requests
# 3. Logs: Make request → check structured log entry appears
# 4. Alerts: Trigger test alert → verify notification received
```

## Monitoring & Alerting

| Metric | Normal | Alert Threshold | Action |
|--------|--------|-----------------|--------|
| Error rate | < 0.5% | > 2% for 5 min | Check LLM API, review errors |
| Latency p95 | < 5s | > 10s for 5 min | Check agent steps, LLM latency |
| Token usage | Baseline | > 2× baseline/hr | Check for loops, abuse |
| Empty retrieval | < 5% | > 10% for 15 min | Check vector store health |
| Cache hit rate | > 30% | < 15% for 1hr | New query patterns, cache issue |
| Agent step limit hits | < 5% | > 10% | Agent struggling, review prompts |

## Troubleshooting Guide

| Symptom | Where to Look | Module 1 Connection |
|---------|---------------|---------------------|
| Hallucinated answers | LangSmith trace → check retrieved context vs answer | Faithfulness = context grounding |
| Inconsistent outputs | Check temperature setting in trace | Decoding/temperature (Module 1) |
| Token limit errors | Check total token count in trace | Context windows (Module 1) |
| Slow responses | LangSmith → find slowest step in trace | Usually LLM call or retrieval |
| High cost | Token metrics → which model/endpoint is expensive | Token pricing awareness |
| Agent loops | Agent steps metric + trace → see repetitive pattern | — |

## Security & Compliance

- Trace data may contain user messages — restrict LangSmith access
- Don't log full request/response bodies in general logs (only in traces)
- Metrics are safe to expose (no PII in counters/histograms)
- Retain audit trail of who accessed traces

## Cost Management

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| LangSmith (free tier) | $0 | 5K traces/month |
| LangSmith (plus) | $39/user | Unlimited traces |
| Prometheus + Grafana (self-hosted) | ~$0 (compute) | Runs alongside service |
| Prometheus (cloud — Grafana Cloud) | $0-50 | Free tier generous |
| Log storage (30 days) | ~$5-20 | Depends on volume |

## Maintenance & Updates

- **Adding new metrics:** Add Prometheus metric → restart service → update dashboard
- **Trace sampling:** If cost grows, sample 10-50% of traces (keep 100% for errors)
- **Dashboard updates:** Add panels as you discover new failure modes
- **Alert tuning:** Start noisy (low thresholds), tighten as you learn normal ranges
