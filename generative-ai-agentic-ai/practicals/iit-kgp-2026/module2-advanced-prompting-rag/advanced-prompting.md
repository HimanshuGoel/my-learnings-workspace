# Advanced Prompting

## The Problem You're Solving

Basic prompts (zero-shot, simple instructions) work for toy examples but fail unpredictably in production — inconsistent output format, missed edge cases, hallucinated reasoning, and no way to systematically improve. You need engineering discipline around prompt design.

## Options Available

| Technique | When to Use | Pros | Cons |
|-----------|-------------|------|------|
| Zero-shot | Simple, well-defined tasks | Fast, no examples needed | Inconsistent on complex tasks |
| Few-shot | Need consistent format/style | Reliable output structure | Token-expensive, example selection matters |
| Chain-of-Thought (CoT) | Multi-step reasoning | Better accuracy on reasoning tasks | Slower, more tokens, can hallucinate steps |
| Self-Consistency | High-stakes reasoning | Reduces variance via majority voting | 3-5x cost (multiple completions) |
| ReAct | Tool use + reasoning | Structured thought-action loops | Complex prompt, may loop indefinitely |
| Tree-of-Thought | Complex problem solving | Explores multiple paths | Very expensive, niche use cases |
| Prompt Chaining | Multi-step workflows | Each step is simple and testable | More API calls, orchestration complexity |

## Recommended Approach

**Start with Few-shot + CoT for most production RAG scenarios.**

Why: You're building a RAG system where the LLM needs to (a) reason over retrieved context and (b) produce consistent output. Few-shot gives format reliability, CoT gives reasoning quality. Add self-consistency only for high-stakes answers.

## Step-by-Step Implementation

### 1. Design the System Prompt

```python
SYSTEM_PROMPT = """You are a technical documentation assistant.

Rules:
1. Answer ONLY based on the provided context
2. If the context doesn't contain the answer, say "Not found in documentation"
3. Cite the source document for each claim
4. Use bullet points for multi-part answers
5. Never speculate beyond what the context states"""
```

### 2. Add Few-Shot Examples

```python
FEW_SHOT_EXAMPLES = [
    {
        "context": "FastAPI supports async endpoints using Python's asyncio...",
        "question": "Does FastAPI support async?",
        "answer": "Yes. FastAPI natively supports async endpoints using Python's asyncio. [Source: fastapi-docs.md]"
    },
    {
        "context": "The maximum batch size is 32 for GPU inference...",
        "question": "What's the recommended batch size?",
        "answer": "The maximum batch size is 32 for GPU inference. [Source: deployment-guide.md]"
    }
]
```

### 3. Add Chain-of-Thought for Complex Queries

```python
COT_INSTRUCTION = """
Think step-by-step:
1. Which retrieved passages are relevant to the question?
2. What specific information from those passages answers the question?
3. Are there any contradictions between passages?
4. Formulate your answer citing only what the passages state.
"""
```

### 4. Compose the Full Prompt

```python
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "Context: {context}\nQuestion: {question}"),
    ("ai", "{answer}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=FEW_SHOT_EXAMPLES,
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    few_shot_prompt,
    ("human", "Context: {context}\n\n{cot_instruction}\n\nQuestion: {question}")
])
```

### 5. Implement Self-Consistency (When Needed)

```python
import collections

def self_consistent_answer(prompt, n=3, temperature=0.7):
    """Generate multiple answers and pick the majority."""
    responses = [
        llm.invoke(prompt, temperature=temperature)
        for _ in range(n)
    ]
    # Extract final answers (after reasoning)
    answers = [extract_final_answer(r) for r in responses]
    # Majority vote
    counter = collections.Counter(answers)
    return counter.most_common(1)[0][0]
```

### 6. Prompt Versioning and Testing

```python
# prompt_registry.py
PROMPTS = {
    "rag_answer_v1": {
        "template": final_prompt,
        "version": "1.0.0",
        "description": "Few-shot + CoT for documentation QA",
        "metrics": {"faithfulness": 0.92, "relevancy": 0.88}
    }
}

def get_prompt(name: str, version: str = "latest"):
    """Retrieve versioned prompt template."""
    return PROMPTS[f"{name}_{version}" if version != "latest" else name]
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Temperature | 0.0 for factual QA, 0.3-0.7 for creative | Lower = more deterministic, higher = more diverse |
| Max tokens | 500-1000 for answers | Prevents runaway generation, controls cost |
| Few-shot count | 2-3 examples | Diminishing returns after 3, saves context window |
| System prompt length | < 500 tokens | Leaves room for context + question |
| CoT trigger | "Think step-by-step" or "Let's work through this" | Explicit trigger more reliable than hoping model reasons |
| Stop sequences | `["\n\nQuestion:", "\n\nContext:"]` | Prevents model from generating its own follow-up |
| Top-p | 0.95 | Standard for most use cases |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Inconsistent output format | Missing/weak few-shot examples | Add 2-3 format-matching examples |
| Ignores context, uses own knowledge | System prompt not strict enough | Add "ONLY use provided context" + "say I don't know" |
| Hallucinated sources/citations | No citation enforcement | Add few-shot with citation format, validate post-generation |
| CoT produces wrong reasoning | Temperature too high or weak CoT prompt | Lower temperature, add reasoning examples |
| Output too verbose | No length constraint | Add "Answer in 2-3 sentences" or max_tokens |
| Model refuses to answer | Over-constraining system prompt | Relax "I don't know" threshold, add edge case examples |
| Prompt too long (context window exceeded) | Too many few-shot examples + long context | Reduce examples to 2, summarize context, use smaller chunks |

## Production Considerations

### Latency
- Few-shot adds ~100-200 tokens input → negligible latency impact
- CoT adds ~200-500 tokens output → 1-3s additional generation time
- Self-consistency multiplies latency by N (typically 3-5x)

### Cost
- Input tokens are cheaper than output tokens (for most APIs)
- CoT increases output cost significantly
- Cache common system prompts where possible (Anthropic prompt caching, OpenAI system prompt caching)

### Monitoring
- Track: answer length distribution, refusal rate, latency p50/p95
- Alert on: sudden refusal spike (prompt regression), answer length spike (runaway generation)
- A/B test prompts with shadow mode (run both, serve old, compare)

### Scaling
- Prompt templates are stateless — horizontal scaling is trivial
- Version prompts in code, not in databases (git-trackable, reviewable)
- Use prompt registries for multi-tenant apps

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| Format compliance | Regex/schema validation on output | > 95% |
| Faithfulness | Does answer match source context? (LLM-as-judge or RAGAS) | > 0.90 |
| Answer relevancy | Does answer address the question? (embedding similarity) | > 0.85 |
| Refusal accuracy | Does it refuse when context lacks answer? | > 90% |
| Latency | Time to first token / total generation time | < 3s p95 |
| Cost per query | Input + output tokens × price | Track trending |

## Ready to Ship? — Checklist

- [ ] System prompt explicitly constrains behavior (no ambiguity)
- [ ] 2-3 few-shot examples cover the main output format
- [ ] CoT is enabled for reasoning-heavy queries
- [ ] Temperature is set intentionally (not left at default)
- [ ] Output validated against schema/format before returning to user
- [ ] Prompt versioned in code with metrics baseline
- [ ] Failure modes documented and monitored
- [ ] Cost per query estimated and acceptable
- [ ] Edge cases tested: empty context, contradictory context, out-of-scope question
