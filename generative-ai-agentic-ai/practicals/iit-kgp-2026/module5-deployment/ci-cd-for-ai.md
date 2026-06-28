# CI/CD for AI

## What You're Deploying

A continuous integration and deployment pipeline for AI systems — where outputs are non-deterministic, "correctness" is probabilistic, and traditional unit tests (assert output == expected) don't work. You need eval-based quality gates that catch regressions in AI behavior before they reach users.

## Prerequisites & Dependencies

- Working AI service with FastAPI (Topic 1)
- Containerized with Docker (Topic 3)
- Evaluation test set from Module 2 (RAG) or Module 4 (agents)
- GitHub/GitLab repo with CI runner access
- LangSmith or equivalent for tracing (Topic 9)

## Step-by-Step Procedure

### 1. Define the AI-Specific Testing Pyramid

```
┌─────────────────────────────────┐
│    E2E: Full pipeline test       │  (5-10 cases, expensive, slow)
│    "Does the user get a good answer?"
├─────────────────────────────────┤
│    Integration: Component tests  │  (20-50 cases, moderate)
│    "Does retrieval return right docs?"
│    "Does agent use correct tools?"
├─────────────────────────────────┤
│    Unit: Deterministic logic     │  (100+ cases, fast, cheap)
│    "Does chunker split correctly?"
│    "Does schema validate?"
│    "Does tool parse args?"
└─────────────────────────────────┘
```

### 2. Unit Tests (Deterministic — Standard)

```python
# test_chunker.py — these are normal, deterministic tests
def test_chunk_respects_max_size():
    chunks = chunker.split("long text...", max_size=512)
    assert all(len(c) <= 512 for c in chunks)

def test_metadata_preserved():
    docs = chunker.split_documents(documents)
    assert all("source" in d.metadata for d in docs)

# test_schema.py
def test_chat_request_validates():
    req = ChatRequest(message="hello", stream=True)
    assert req.message == "hello"

def test_chat_request_rejects_empty():
    with pytest.raises(ValidationError):
        ChatRequest(message="")
```

### 3. Integration Tests (AI Components — Semi-Deterministic)

```python
# test_retrieval.py — retrieval should be fairly deterministic
def test_retrieval_returns_relevant_docs():
    docs = retriever.invoke("How to authenticate with OAuth?")
    assert len(docs) >= 3
    assert any("auth" in d.page_content.lower() for d in docs)

def test_retrieval_respects_filter():
    docs = retriever.invoke("rate limit", filter={"doc_type": "api_doc"})
    assert all(d.metadata["doc_type"] == "api_doc" for d in docs)

# test_tools.py — tool execution is deterministic
def test_calculator_tool():
    result = calculate.invoke({"expression": "15 * 0.15"})
    assert "2.25" in result

def test_tool_handles_invalid_input():
    result = calculate.invoke({"expression": "DROP TABLE users"})
    assert "ERROR" in result or "Invalid" in result
```

### 4. Eval-Based Quality Gates (Non-Deterministic — THE NEW PART)

```python
# test_eval.py — probabilistic tests with thresholds
import json
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

def test_rag_quality_above_threshold():
    """Run RAGAS evaluation — MUST pass before deploy."""
    results = evaluate(dataset=eval_dataset, metrics=[faithfulness, answer_relevancy])
    
    assert results["faithfulness"] >= 0.85, \
        f"Faithfulness {results['faithfulness']:.2f} below threshold 0.85"
    assert results["answer_relevancy"] >= 0.80, \
        f"Relevancy {results['answer_relevancy']:.2f} below threshold 0.80"

def test_agent_task_completion():
    """Agent completes test tasks within budget."""
    test_cases = load_test_cases("agent_eval_set.json")
    passed = 0
    
    for tc in test_cases:
        result = agent.invoke({"messages": [HumanMessage(tc["query"])]})
        if tc["expected_contains"] in result["messages"][-1].content:
            passed += 1
    
    pass_rate = passed / len(test_cases)
    assert pass_rate >= 0.80, f"Pass rate {pass_rate:.0%} below 80% threshold"

def test_no_regression_vs_baseline():
    """Current version must not be worse than last deployed version."""
    current_scores = run_eval_suite(current_model)
    baseline_scores = load_baseline_scores("baseline.json")
    
    for metric, current in current_scores.items():
        baseline = baseline_scores[metric]
        regression = baseline - current
        assert regression < 0.05, \
            f"{metric} regressed by {regression:.2f} (current={current:.2f}, baseline={baseline:.2f})"
```

### 5. GitHub Actions Pipeline

```yaml
# .github/workflows/deploy.yml
name: AI Service CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-test.txt
      
      - name: Unit tests (fast, deterministic)
        run: pytest tests/unit/ -v
      
      - name: Integration tests (moderate)
        run: pytest tests/integration/ -v
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Eval quality gate (slow, expensive)
        run: pytest tests/eval/ -v --timeout=300
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Build Docker image
        run: docker build -t ai-service:${{ github.sha }} .
      
      - name: Smoke test container
        run: |
          docker run -d -p 8000:8000 --env-file .env.test ai-service:${{ github.sha }}
          sleep 10
          curl -f http://localhost:8000/health

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Push image, update deployment, verify
          echo "Deploy steps here..."
      
      - name: Post-deploy smoke test
        run: curl -f ${{ secrets.PROD_URL }}/ready
      
      - name: Save baseline scores
        run: python scripts/save_baseline.py
```

### 6. Handling Flaky Tests (Non-Determinism)

```python
import pytest

@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_llm_output_contains_expected():
    """LLM tests may vary — allow retries."""
    result = llm.invoke("What is 2+2?")
    assert "4" in result.content

# Strategy for non-deterministic tests:
# 1. Run 3-5 times, pass if >= 80% succeed
# 2. Use "contains" not "equals" for output checks
# 3. Test PROPERTIES not exact outputs ("answer mentions X")
# 4. Set temperature=0 for reproducibility where possible
# 5. Accept slightly flaky tests — but track flakiness over time
```

### 7. Canary Deployments for AI

```python
# Route 5% of traffic to new version, compare metrics
# If new version quality drops → auto-rollback

CANARY_CONFIG = {
    "canary_weight": 0.05,       # 5% traffic to new version
    "observation_period": "2h",   # Watch for 2 hours
    "rollback_threshold": {
        "error_rate": 0.02,       # > 2% errors → rollback
        "latency_p95": 5.0,       # > 5s → rollback
        "quality_score": 0.80,    # < 0.80 avg quality → rollback
    },
}
```

## Configuration Reference

| Setting | Value | Purpose |
|---------|-------|---------|
| Eval test set size | 50-100 examples | Statistical confidence |
| Quality threshold (faithfulness) | >= 0.85 | Blocks deploy if too much hallucination |
| Quality threshold (relevancy) | >= 0.80 | Blocks deploy if off-topic |
| Regression tolerance | 5% drop max | Prevents shipping worse models |
| Flaky test reruns | 3 | Accounts for LLM non-determinism |
| Eval cost budget per CI run | ~$5-10 | 50 examples × RAGAS evaluation |
| Canary percentage | 5% | Safe rollout |
| Canary observation period | 2 hours | Enough data to judge |

## Verification & Smoke Tests

```bash
# Post-deploy verification:
curl -f https://my-service.com/health           # Process alive
curl -f https://my-service.com/ready            # Dependencies connected
curl -X POST https://my-service.com/v1/chat \
  -d '{"message": "ping", "stream": false}'     # End-to-end working
```

## Monitoring & Alerting

| Metric | Alert | After Deploy |
|--------|-------|-------------|
| Error rate | > 2% for 5 min | Rollback |
| Latency p95 | > 2× baseline | Investigate |
| Quality score (sampled) | < 0.80 | Rollback |
| Token cost/day | > 2× baseline | Investigate |

## Troubleshooting Guide

| Problem | Cause | Fix |
|---------|-------|-----|
| Eval tests fail in CI but pass locally | Different API model version in CI | Pin model version, use same env |
| All eval tests suddenly fail | API key expired or rate limited | Check secrets, add retry logic |
| Flaky tests > 20% failure rate | Output too variable or threshold too strict | Loosen threshold or add temperature=0 |
| Deploy succeeds but quality drops | Eval test set doesn't cover edge case | Add failing case to eval set, tighten gate |
| Docker build slow (10+ min) | Downloading model files every build | Cache model in base image or volume |

## Security & Compliance

- API keys in CI secrets (never in repo)
- Eval datasets may contain sensitive examples — keep in private repo
- Don't log full LLM responses in CI output (may contain PII from test data)
- Audit trail: every deploy tagged with git SHA + eval scores

## Cost Management

| Activity | Cost Per Run | Frequency |
|----------|-------------|-----------|
| Unit tests | Free | Every push |
| Integration tests | ~$0.50 | Every push |
| Eval quality gate | ~$5-10 | Every push to main |
| Canary monitoring | Production cost (sampled) | Every deploy |
| Total CI/CD monthly | ~$100-200 | With daily deploys |

## Maintenance & Updates

- **Adding new eval cases:** When a production failure occurs, add it to the eval set (never remove, only add)
- **Updating thresholds:** If model improves, raise thresholds (ratchet up, never down)
- **Baseline rotation:** After successful deploy, new scores become the regression baseline
- **Model upgrade:** Change model → eval gate catches any quality drop before it reaches users
