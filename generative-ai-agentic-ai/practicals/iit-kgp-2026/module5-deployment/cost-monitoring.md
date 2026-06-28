# Cost Monitoring — Deployment Runbook

## 1. What You're Deploying

Token usage tracking, budget enforcement, and cost optimization for your AI services. Without this, a single misconfigured loop or viral spike can generate a $10,000 bill overnight.

**AI-specific challenge:** Unlike traditional APIs where cost scales with compute time, AI costs scale with TOKEN COUNT — invisible to users but directly proportional to input length + output length. A single "summarize this document" request can cost $0.50 with GPT-4o if the document is large.

**From Module 1:** Tokenization determines cost. BPE tokenization means character count ≠ token count. "Hello" = 1 token, but code or non-English text may tokenize to 2-4x more tokens than expected.

## 2. Prerequisites & Dependencies

```bash
pip install tiktoken redis prometheus-client
# tiktoken: fast token counting (OpenAI models)
# redis: budget state storage
# prometheus-client: metrics export
```

| Requirement | Why |
|-------------|-----|
| Auth system (Topic 5) | Track costs per authenticated user |
| Redis | Store running totals and budget state |
| Understanding of model pricing | Know what you're measuring |

**Current Pricing Reference (verify before deployment):**

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3.5 Haiku | $0.25 | $1.25 |

## 3. Step-by-Step Procedure

### 3.1 Token Counting Middleware

```python
# app/cost/token_counter.py
import tiktoken
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    model: str
    cost_usd: float
    latency_ms: float
    user_id: str
    timestamp: float

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

# Pricing per 1M tokens (keep updated!)
MODEL_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku": {"input": 0.25, "output": 1.25},
}

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Count tokens for a given text and model."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")  # Default for newer models
    return len(encoding.encode(text))

def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Calculate USD cost for a request."""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-4o-mini"])
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return round(input_cost + output_cost, 6)
```

### 3.2 Cost Tracking Middleware

```python
# app/cost/tracking_middleware.py
import time
import json
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.cost.token_counter import count_tokens, calculate_cost, TokenUsage
from redis.asyncio import Redis

logger = logging.getLogger("cost_tracker")

class CostTrackingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str = "redis://localhost:6379"):
        super().__init__(app)
        self.redis = Redis.from_url(redis_url)

    async def dispatch(self, request: Request, call_next):
        # Skip non-AI endpoints
        if request.url.path not in ["/query", "/chat", "/chat/stream"]:
            return await call_next(request)

        start = time.perf_counter()
        response = await call_next(request)
        latency = (time.perf_counter() - start) * 1000

        # Extract usage from response headers (set by LLM wrapper)
        usage_header = response.headers.get("X-Token-Usage")
        if usage_header:
            usage_data = json.loads(usage_header)
            user_id = request.state.user_id if hasattr(request.state, "user_id") else "anonymous"

            usage = TokenUsage(
                input_tokens=usage_data["input_tokens"],
                output_tokens=usage_data["output_tokens"],
                model=usage_data["model"],
                cost_usd=calculate_cost(
                    usage_data["input_tokens"],
                    usage_data["output_tokens"],
                    usage_data["model"]
                ),
                latency_ms=latency,
                user_id=user_id,
                timestamp=time.time()
            )

            await self._record_usage(usage)
            logger.info(f"Cost: ${usage.cost_usd:.6f} | Tokens: {usage.total_tokens} | User: {user_id}")

        return response

    async def _record_usage(self, usage: TokenUsage):
        """Store usage in Redis for budget tracking."""
        today = time.strftime("%Y-%m-%d")
        month = time.strftime("%Y-%m")

        pipe = self.redis.pipeline()
        # Daily totals
        pipe.incrbyfloat(f"cost:daily:{today}:total", usage.cost_usd)
        pipe.incrbyfloat(f"cost:daily:{today}:user:{usage.user_id}", usage.cost_usd)
        # Monthly totals
        pipe.incrbyfloat(f"cost:monthly:{month}:total", usage.cost_usd)
        pipe.incrbyfloat(f"cost:monthly:{month}:user:{usage.user_id}", usage.cost_usd)
        # Per-model tracking
        pipe.incrbyfloat(f"cost:monthly:{month}:model:{usage.model}", usage.cost_usd)
        # Token counts
        pipe.incrby(f"tokens:daily:{today}:input", usage.input_tokens)
        pipe.incrby(f"tokens:daily:{today}:output", usage.output_tokens)
        # TTL for daily keys (auto-cleanup)
        pipe.expire(f"cost:daily:{today}:total", 86400 * 7)  # 7 day retention
        await pipe.execute()
```

### 3.3 Budget Enforcement

```python
# app/cost/budget_guard.py
import os
from fastapi import HTTPException, Depends
from redis.asyncio import Redis
import time

DAILY_BUDGET = float(os.environ.get("DAILY_BUDGET_USD", "50.0"))
MONTHLY_BUDGET = float(os.environ.get("MONTHLY_BUDGET_USD", "500.0"))
USER_DAILY_BUDGET = float(os.environ.get("USER_DAILY_BUDGET_USD", "5.0"))

async def check_budget(user_id: str, redis: Redis) -> dict:
    """Check if request is within budget. Raises HTTPException if over."""
    today = time.strftime("%Y-%m-%d")
    month = time.strftime("%Y-%m")

    # Get current spend
    daily_total = float(await redis.get(f"cost:daily:{today}:total") or 0)
    monthly_total = float(await redis.get(f"cost:monthly:{month}:total") or 0)
    user_daily = float(await redis.get(f"cost:daily:{today}:user:{user_id}") or 0)

    # Check global daily budget
    if daily_total >= DAILY_BUDGET:
        raise HTTPException(status_code=429, detail={
            "error": "daily_budget_exceeded",
            "message": f"Daily budget of ${DAILY_BUDGET} reached. Resets at midnight UTC.",
            "current_spend": daily_total
        })

    # Check global monthly budget
    if monthly_total >= MONTHLY_BUDGET:
        raise HTTPException(status_code=429, detail={
            "error": "monthly_budget_exceeded",
            "message": f"Monthly budget of ${MONTHLY_BUDGET} reached.",
            "current_spend": monthly_total
        })

    # Check per-user daily budget
    if user_daily >= USER_DAILY_BUDGET:
        raise HTTPException(status_code=429, detail={
            "error": "user_budget_exceeded",
            "message": f"Your daily budget of ${USER_DAILY_BUDGET} reached.",
            "current_spend": user_daily,
            "upgrade_hint": "Contact admin to increase your limit."
        })

    return {
        "daily_remaining": DAILY_BUDGET - daily_total,
        "monthly_remaining": MONTHLY_BUDGET - monthly_total,
        "user_remaining": USER_DAILY_BUDGET - user_daily
    }
```

### 3.4 Smart Model Routing (Cost Optimization)

```python
# app/cost/model_router.py

def select_model(query: str, user_tier: str, complexity_hint: str = "auto") -> str:
    """Route to cheapest adequate model based on query characteristics."""

    # Simple classification heuristic
    if complexity_hint == "simple" or len(query) < 100:
        return "gpt-4o-mini"  # 20x cheaper than gpt-4o

    if complexity_hint == "complex":
        return "gpt-4o"

    # Auto-detect: use cheap model for common patterns
    simple_patterns = [
        "summarize", "translate", "list", "define",
        "what is", "how to", "explain"
    ]
    if any(p in query.lower() for p in simple_patterns):
        return "gpt-4o-mini"

    # Default to quality model for enterprise tier
    if user_tier == "enterprise":
        return "gpt-4o"

    return "gpt-4o-mini"
```

### 3.5 Semantic Cache (Avoid Redundant LLM Calls)

```python
# app/cost/semantic_cache.py
import hashlib
import json
from redis.asyncio import Redis
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticCache:
    """Cache LLM responses for semantically similar queries."""

    def __init__(self, redis: Redis, similarity_threshold: float = 0.95):
        self.redis = redis
        self.threshold = similarity_threshold
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    async def get(self, query: str) -> dict | None:
        """Check if a similar query has been answered recently."""
        # Exact match (fast path)
        exact_key = f"cache:exact:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await self.redis.get(exact_key)
        if cached:
            return json.loads(cached)
        return None  # Semantic search is heavier — implement if needed

    async def set(self, query: str, response: dict, ttl: int = 3600):
        """Cache a response for 1 hour by default."""
        exact_key = f"cache:exact:{hashlib.md5(query.encode()).hexdigest()}"
        await self.redis.setex(exact_key, ttl, json.dumps(response))

# Usage: check cache before LLM call
# cached = await cache.get(query)
# if cached: return cached
# result = await llm.generate(query)
# await cache.set(query, result)
```

### 3.6 Cost Dashboard Endpoint

```python
# app/cost/dashboard.py
from fastapi import APIRouter, Depends
from redis.asyncio import Redis
import time

router = APIRouter(prefix="/admin/cost")

@router.get("/summary")
async def cost_summary(redis: Redis = Depends(get_redis)):
    """Current cost summary for dashboard."""
    today = time.strftime("%Y-%m-%d")
    month = time.strftime("%Y-%m")

    return {
        "daily": {
            "total_usd": float(await redis.get(f"cost:daily:{today}:total") or 0),
            "budget_usd": DAILY_BUDGET,
            "input_tokens": int(await redis.get(f"tokens:daily:{today}:input") or 0),
            "output_tokens": int(await redis.get(f"tokens:daily:{today}:output") or 0),
        },
        "monthly": {
            "total_usd": float(await redis.get(f"cost:monthly:{month}:total") or 0),
            "budget_usd": MONTHLY_BUDGET,
        },
        "cost_per_query_avg": await _calculate_avg_cost(redis, today),
    }
```

## 4. Configuration Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DAILY_BUDGET_USD` | Global daily spend cap | `50.0` |
| `MONTHLY_BUDGET_USD` | Global monthly spend cap | `500.0` |
| `USER_DAILY_BUDGET_USD` | Per-user daily cap | `5.0` |
| `CACHE_TTL_SECONDS` | Semantic cache expiry | `3600` |
| `DEFAULT_MODEL` | Fallback model for routing | `gpt-4o-mini` |
| `REDIS_URL` | Budget state storage | `redis://localhost:6379` |
| `COST_ALERT_WEBHOOK` | Slack/Teams webhook for alerts | (optional) |

## 5. Verification & Smoke Tests

```bash
# Check current budget status
curl http://localhost:8000/admin/cost/summary -H "X-API-Key: admin-key"

# Verify cost tracking after a query
curl -X POST http://localhost:8000/query \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'

# Check Redis for recorded cost
redis-cli GET "cost:daily:$(date +%Y-%m-%d):total"

# Test budget enforcement (set very low budget temporarily)
# DAILY_BUDGET_USD=0.001 → next request should be rejected with 429
```

## 6. Monitoring & Alerting

| Metric | Alert Threshold | Why |
|--------|----------------|-----|
| Daily spend | > 80% of budget | Approaching limit |
| Single request cost | > $1.00 | Unusually expensive query |
| Cost spike | > 3x hourly average | Possible abuse or loop |
| Cache hit rate | < 10% | Cache not effective |
| Per-user daily spend | > $3.00 | Individual user spike |

## 7. Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Unexpected high daily cost | Long documents in prompts | Add input length limits, truncate or summarize first |
| Cost not being tracked | Middleware not registered or header missing | Verify middleware order, check X-Token-Usage header |
| Budget check always passes | Redis not persisting (restart) | Check Redis persistence config (AOF or RDB) |
| Cache not reducing costs | Queries too varied | Lower similarity threshold or use exact-match only |
| Token count doesn't match bill | Using wrong tokenizer | Ensure tiktoken model matches actual model used |

## 8. Security & Compliance

- Cost dashboard should be admin-only (separate auth)
- Don't expose individual user spend to other users
- Audit trail: log who hit budget limits and when
- Consider GDPR: usage tracking is personal data if tied to user

## 9. Cost Management

**Optimization Hierarchy (highest impact first):**

1. **Cache responses** — identical/similar queries skip LLM entirely
2. **Model routing** — use mini models for simple queries (20x savings)
3. **Prompt compression** — remove redundant context from RAG chunks
4. **Token limits** — cap max_tokens per endpoint (prevent runaway generation)
5. **Batch requests** — group multiple queries where possible (API discount)

## 10. Maintenance & Updates

- **Update pricing:** Check provider pricing monthly, update `MODEL_PRICING` dict
- **Adjust budgets:** Review actual spend weekly for first month, then monthly
- **Cache tuning:** Monitor hit rate, adjust TTL and similarity threshold
- **New models:** Add to pricing dict and routing logic when switching models
- **Cost reports:** Generate weekly summary → email to stakeholders
