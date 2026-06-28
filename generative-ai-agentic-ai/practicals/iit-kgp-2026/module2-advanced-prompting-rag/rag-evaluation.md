# RAG Evaluation

## The Problem You're Solving

Your RAG system generates answers but you have no systematic way to know if they're good. "It seems to work" isn't engineering. You need measurable metrics for retrieval quality, answer faithfulness, and relevancy — with automated testing that catches regressions before users do.

## Options Available

| Framework | What It Measures | Pros | Cons |
|-----------|-----------------|------|------|
| RAGAS | Faithfulness, relevancy, context precision/recall | Purpose-built for RAG, LLM-as-judge | Requires ground truth for some metrics |
| DeepEval | RAG metrics + hallucination + toxicity | Broader coverage, CI integration | More setup, learning curve |
| TruLens | RAG triad (groundedness, relevance, QS) | Good visualization dashboard | Heavier dependency |
| Custom (LLM-as-judge) | Whatever you define | Full control, domain-specific | Must validate judge reliability |
| Human evaluation | Gold standard for quality | Catches what automated misses | Expensive, slow, not scalable |
| Embedding similarity | Answer vs reference answer similarity | Fast, cheap, no LLM needed | Misses semantic nuance |

## Recommended Approach

**Start with RAGAS (4 core metrics) for automated eval. Add custom LLM-as-judge for domain-specific quality. Use human eval for calibration and edge cases.**

Why: RAGAS gives you the RAG-specific metrics out of the box with minimal setup. It's the industry standard for RAG evaluation. Custom judges handle your specific domain needs. Human eval validates that automated metrics correlate with actual quality.

## Step-by-Step Implementation

### 1. Install and Setup RAGAS

```python
# pip install ragas datasets

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset
```

### 2. Prepare Evaluation Dataset

```python
# You need: question, answer, contexts, ground_truth (reference answer)
eval_data = {
    "question": [
        "What is the rate limit for the API?",
        "How do I authenticate with OAuth?",
        "What Python version is required?",
    ],
    "answer": [
        "The rate limit is 100 requests per minute. [Source: api-docs.md]",
        "Use OAuth 2.0 with client credentials flow. [Source: auth-guide.md]",
        "Python 3.9 or higher is required. [Source: setup.md]",
    ],
    "contexts": [
        ["The API rate limit is 100 requests per minute per API key."],
        ["Authentication uses OAuth 2.0. Supported flows: client credentials, authorization code."],
        ["Requirements: Python 3.9+, pip 21.0+, Docker (optional)."],
    ],
    "ground_truth": [
        "The rate limit is 100 requests per minute per API key.",
        "OAuth 2.0 with client credentials or authorization code flow.",
        "Python 3.9 or higher.",
    ],
}

eval_dataset = Dataset.from_dict(eval_data)
```

### 3. Run RAGAS Evaluation

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

results = evaluate(
    dataset=eval_dataset,
    metrics=[
        faithfulness,        # Is the answer supported by the context?
        answer_relevancy,    # Does the answer address the question?
        context_precision,   # Are retrieved contexts relevant?
        context_recall,      # Did we retrieve all needed context?
    ],
)

print(results)
# {'faithfulness': 0.92, 'answer_relevancy': 0.88, 'context_precision': 0.85, 'context_recall': 0.90}
```

### 4. Understanding Each Metric

```python
"""
RAGAS Core Metrics Explained:

1. FAITHFULNESS (0-1)
   Question: "Is every claim in the answer traceable to the context?"
   How: LLM extracts claims from answer → checks each against context
   Target: > 0.90 (production), > 0.85 (acceptable)
   Failure means: hallucination

2. ANSWER RELEVANCY (0-1)
   Question: "Does the answer actually address what was asked?"
   How: Generate questions from the answer → compare to original question
   Target: > 0.85
   Failure means: off-topic answers, tangential info

3. CONTEXT PRECISION (0-1)
   Question: "Are the retrieved contexts relevant to the question?"
   How: For each context chunk, is it useful for answering?
   Target: > 0.80
   Failure means: retrieval returning noise

4. CONTEXT RECALL (0-1)
   Question: "Did we retrieve everything needed to answer?"
   How: Can the ground truth be attributed to the contexts?
   Target: > 0.85
   Failure means: missing relevant documents
"""
```

### 5. Build an Evaluation Test Set

```python
import json
from pathlib import Path

class RAGEvalTestSet:
    """Manage a growing test set for regression testing."""
    
    def __init__(self, path: str = "eval_dataset.json"):
        self.path = Path(path)
        self.data = self._load()
    
    def _load(self) -> list[dict]:
        if self.path.exists():
            return json.loads(self.path.read_text())
        return []
    
    def add_example(
        self,
        question: str,
        ground_truth: str,
        relevant_docs: list[str],
        tags: list[str] = None,
    ):
        """Add a new test case."""
        self.data.append({
            "question": question,
            "ground_truth": ground_truth,
            "relevant_docs": relevant_docs,
            "tags": tags or [],
        })
        self.path.write_text(json.dumps(self.data, indent=2))
    
    def get_by_tag(self, tag: str) -> list[dict]:
        """Filter test set by tag for targeted evaluation."""
        return [ex for ex in self.data if tag in ex.get("tags", [])]
    
    def to_ragas_dataset(self, pipeline) -> Dataset:
        """Run pipeline on test set and format for RAGAS."""
        questions, answers, contexts, ground_truths = [], [], [], []
        
        for example in self.data:
            # Run through your actual pipeline
            result = pipeline.run(example["question"])
            
            questions.append(example["question"])
            answers.append(result.answer)
            contexts.append([doc.page_content for doc in result.source_docs])
            ground_truths.append(example["ground_truth"])
        
        return Dataset.from_dict({
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths,
        })
```

### 6. Custom LLM-as-Judge (Domain-Specific)

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class JudgeScore(BaseModel):
    score: int          # 1-5
    reasoning: str
    issues: list[str]

JUDGE_PROMPT = """You are evaluating a RAG system's answer quality.

Question: {question}
Context provided: {context}
Answer generated: {answer}
Reference answer: {ground_truth}

Score the answer from 1-5:
5 = Perfect: accurate, complete, well-cited, concise
4 = Good: minor omission or unnecessary detail
3 = Acceptable: correct but missing important info or poorly structured
2 = Poor: partially incorrect or mostly irrelevant
1 = Bad: hallucinated, wrong, or completely off-topic

Evaluate on:
- Factual accuracy (vs context, not your own knowledge)
- Completeness (does it cover the key points?)
- Citation quality (are sources referenced?)
- Conciseness (no unnecessary filler?)

Return JSON: {{"score": <1-5>, "reasoning": "<why>", "issues": ["<issue1>", ...]}}"""

def judge_answer(question: str, context: str, answer: str, ground_truth: str) -> JudgeScore:
    judge_llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    response = judge_llm.invoke(
        JUDGE_PROMPT.format(
            question=question,
            context=context,
            answer=answer,
            ground_truth=ground_truth,
        )
    )
    return JudgeScore.model_validate_json(response.content)
```

### 7. Automated Regression Testing

```python
import json
from datetime import datetime

class RAGRegressionTest:
    """Run on every pipeline change to catch regressions."""
    
    def __init__(self, pipeline, test_set: RAGEvalTestSet, thresholds: dict):
        self.pipeline = pipeline
        self.test_set = test_set
        self.thresholds = thresholds  # {"faithfulness": 0.90, "relevancy": 0.85}
    
    def run(self) -> dict:
        """Execute full regression suite."""
        dataset = self.test_set.to_ragas_dataset(self.pipeline)
        results = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        )
        
        # Check against thresholds
        passed = True
        failures = []
        for metric, threshold in self.thresholds.items():
            if results[metric] < threshold:
                passed = False
                failures.append(f"{metric}: {results[metric]:.3f} < {threshold}")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "passed": passed,
            "scores": dict(results),
            "failures": failures,
            "test_set_size": len(self.test_set.data),
        }
        
        # Save history for trending
        self._save_report(report)
        return report
    
    def _save_report(self, report: dict):
        history_file = Path("eval_history.jsonl")
        with history_file.open("a") as f:
            f.write(json.dumps(report) + "\n")
```

### 8. Component-Level Evaluation

```python
def evaluate_retrieval_only(test_set: list[dict], retriever) -> dict:
    """Evaluate retrieval quality independent of generation."""
    recall_at_5 = 0
    mrr = 0
    
    for example in test_set:
        retrieved = retriever.invoke(example["question"])
        retrieved_texts = [doc.page_content for doc in retrieved]
        
        # Check if relevant docs are in retrieved set
        for rank, text in enumerate(retrieved_texts, 1):
            if any(rel in text for rel in example["relevant_docs"]):
                recall_at_5 += 1
                mrr += 1 / rank
                break
    
    n = len(test_set)
    return {
        "recall@5": recall_at_5 / n,
        "mrr": mrr / n,
    }


def evaluate_generation_only(test_set: list[dict], generation_stage) -> dict:
    """Evaluate generation with known-good contexts (isolate from retrieval)."""
    scores = []
    for example in test_set:
        # Feed ground truth context directly (skip retrieval)
        messages = build_prompt(example["question"], example["relevant_docs"])
        answer = generation_stage.generate(messages)
        
        score = judge_answer(
            example["question"],
            "\n".join(example["relevant_docs"]),
            answer.answer,
            example["ground_truth"],
        )
        scores.append(score.score)
    
    return {
        "avg_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores),
    }
```

### 9. A/B Testing Setup

```python
import random
import hashlib

class ABTest:
    """A/B test between two pipeline configurations."""
    
    def __init__(self, pipeline_a, pipeline_b, split: float = 0.5):
        self.pipeline_a = pipeline_a
        self.pipeline_b = pipeline_b
        self.split = split
        self.results_a = []
        self.results_b = []
    
    def route(self, user_id: str) -> str:
        """Deterministic routing based on user ID."""
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        return "a" if (hash_val % 100) < (self.split * 100) else "b"
    
    def run(self, query: str, user_id: str) -> dict:
        """Run query through assigned pipeline variant."""
        variant = self.route(user_id)
        pipeline = self.pipeline_a if variant == "a" else self.pipeline_b
        
        result = pipeline.run(query)
        
        # Log for analysis
        log_entry = {"query": query, "variant": variant, "answer": result.answer}
        if variant == "a":
            self.results_a.append(log_entry)
        else:
            self.results_b.append(log_entry)
        
        return {**result.dict(), "variant": variant}
    
    def analyze(self) -> dict:
        """Compare metrics between variants."""
        # Run RAGAS on both sets
        # Compare faithfulness, relevancy, latency
        pass
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Test set size | 50+ examples minimum, 200+ ideal | Statistical significance |
| RAGAS judge model | gpt-4o (most accurate) | Cheaper models may miss subtle issues |
| Faithfulness threshold | > 0.90 | Below this = unacceptable hallucination |
| Relevancy threshold | > 0.85 | Below this = answers miss the point |
| Context recall threshold | > 0.85 | Below this = retrieval is broken |
| Eval frequency | Every pipeline change + weekly scheduled | Catch regressions early |
| Human eval sample | 10-20 examples per eval cycle | Calibrate automated metrics |
| A/B test duration | 1-2 weeks or 500+ queries | Enough data for significance |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Faithfulness drops after changing chunking | New chunks don't contain full context | Check chunk boundaries, increase size or overlap |
| Context recall is high but answer quality low | Retrieved context is relevant but not used well | Check prompt template, ensure context position is prominent |
| RAGAS scores good but users complain | Metrics don't capture domain-specific quality | Add custom judge criteria (citation style, technical depth) |
| Judge LLM gives inconsistent scores | Temperature too high or prompt ambiguous | Set temp=0, add rubric with examples |
| All scores suddenly drop | API model updated (silent version change) | Pin model versions, track score trends |
| High faithfulness but low relevancy | Answer is factually correct but doesn't address question | Improve answer relevancy prompt instructions |

## Production Considerations

### Cost of Evaluation
- RAGAS with gpt-4o judge: ~$0.01-0.05 per test case (depends on context length)
- 200-example test suite: ~$2-10 per full run
- Weekly automated runs: ~$8-40/month
- Worth it: catching one hallucination in prod saves more than eval cost

### Continuous Monitoring (Beyond Test Set)
```python
# Real-time quality signals (no ground truth needed)
def monitor_production_quality(answer: str, context: list[str], question: str):
    """Lightweight checks that run on every production query."""
    signals = {
        "answer_length": len(answer),
        "has_citation": "[Source:" in answer,
        "is_refusal": "couldn't find" in answer.lower(),
        "context_used_ratio": estimate_context_usage(answer, context),
    }
    
    # Alert conditions
    if signals["answer_length"] > 2000:  # runaway generation
        alert("answer_too_long", signals)
    if not signals["has_citation"] and not signals["is_refusal"]:
        alert("missing_citation", signals)
    
    log_quality_signal(question, signals)
```

### When to Re-evaluate
- After changing: chunking strategy, embedding model, retrieval parameters, prompt template, LLM model
- After corpus changes: new documents added, documents updated
- Scheduled: weekly (catch model drift, corpus drift)

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| RAGAS Faithfulness | Automated (claims vs context) | > 0.90 |
| RAGAS Answer Relevancy | Automated (generated Q vs original Q) | > 0.85 |
| RAGAS Context Precision | Automated (relevant contexts / total) | > 0.80 |
| RAGAS Context Recall | Automated (ground truth attributable) | > 0.85 |
| Custom Judge Score | LLM-as-judge 1-5 scale | > 4.0 average |
| Human Agreement | Human score vs automated score correlation | > 0.8 Spearman |
| Regression Detection | Score drop > 5% flags CI failure | 100% caught |

## Ready to Ship? — Checklist

- [ ] Test set created with 50+ diverse examples (different intents, edge cases)
- [ ] RAGAS evaluation running and all metrics above threshold
- [ ] Custom judge implemented for domain-specific quality aspects
- [ ] Baseline scores documented (before any optimization)
- [ ] Regression test integrated into deployment pipeline
- [ ] Human evaluation done for calibration (10-20 examples reviewed)
- [ ] Production monitoring signals in place (no ground truth needed)
- [ ] Score trending tracked over time (detect gradual drift)
- [ ] A/B testing framework ready for comparing pipeline variants
- [ ] Eval cost budgeted and acceptable
