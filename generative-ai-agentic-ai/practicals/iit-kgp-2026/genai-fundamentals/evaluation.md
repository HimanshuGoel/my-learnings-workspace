# Evaluation

## What Is This?

Evaluation is measuring how well your LLM application works — covering accuracy, faithfulness, relevance, safety, and user satisfaction through automated metrics and human judgment.

## Why Does It Exist?

**The Problem:** Unlike traditional ML (where accuracy/F1 on test set is clear), LLM outputs are:
- Open-ended (no single "correct" answer)
- Subjective (what counts as "good"?)
- Multi-dimensional (factual accuracy, helpfulness, safety, format compliance — all matter)
- Hard to automate (need LLM-as-judge or human evaluators)

Without evaluation, you're flying blind. "It seems to work" isn't enough for production.

## Mental Model

Think of evaluation as **code reviews + automated testing + QA combined**:
- **Unit tests** = automated metrics (does the response contain the right info?)
- **Code review** = LLM-as-judge (is the response well-written and helpful?)
- **QA testing** = human evaluation (does this actually satisfy users?)
- **CI/CD checks** = continuous monitoring (is quality degrading over time?)

## How It Works

### Evaluation Dimensions

| Dimension | What It Measures | Example Question |
|-----------|-----------------|-----------------|
| **Faithfulness** | Does the answer match the provided context? | "Is the response supported by the retrieved docs?" |
| **Relevance** | Does the answer address the question? | "Does this actually answer what was asked?" |
| **Correctness** | Is the answer factually accurate? | "Are the stated facts true?" |
| **Harmlessness** | Is the output safe and appropriate? | "Does it contain harmful/biased content?" |
| **Helpfulness** | Does it solve the user's problem? | "Would a user be satisfied?" |
| **Format compliance** | Does it follow the specified format? | "Is it valid JSON matching the schema?" |

### RAG-Specific Metrics

| Metric | What It Measures | Formula Intuition |
|--------|-----------------|-------------------|
| Context Precision | Are retrieved docs relevant? | relevant_retrieved / total_retrieved |
| Context Recall | Did we retrieve all relevant docs? | relevant_retrieved / total_relevant |
| Faithfulness | Is the answer grounded in context? | claims_in_context / total_claims |
| Answer Relevance | Does the answer address the question? | LLM-judged relevance score |

### Evaluation Methods

| Method | How | When |
|--------|-----|------|
| **Automated metrics** | BLEU, ROUGE, exact match | Translation, summarization baselines |
| **LLM-as-Judge** | Use GPT-4 to score outputs | Scalable quality evaluation |
| **Human evaluation** | Humans rate on 1-5 scale | Gold standard, expensive |
| **A/B testing** | Compare two versions with real users | Production optimization |
| **Reference-free** | Evaluate without ground truth | When no "correct answer" exists |

### LLM-as-Judge Pattern

```
System: You are an expert evaluator. Rate the following response on:
1. Faithfulness (1-5): Is it supported by the context?
2. Relevance (1-5): Does it answer the question?
3. Completeness (1-5): Does it cover all aspects?

Context: {retrieved_documents}
Question: {user_question}
Response: {model_response}

Provide scores and brief justification for each.
```

### Evaluation Frameworks

| Framework | What It Does |
|-----------|-------------|
| RAGAS | Automated RAG evaluation (faithfulness, relevance, context quality) |
| DeepEval | General LLM evaluation with multiple metrics |
| LangSmith | Tracing, evaluation, and monitoring for LangChain apps |
| OpenAI Evals | Evaluation harness for comparing model outputs |

### Hallucination Detection

Hallucination = model generates confident but factually wrong content.

Detection strategies:
1. **Ground in context** — "Answer ONLY from provided docs" (RAG)
2. **Self-consistency** — ask same question 5 times, check if answers agree
3. **Claim extraction** — extract individual claims, verify each against source
4. **Confidence calibration** — model reports its own confidence (if trained for it)

## Where You'll Use This

| Module | How Evaluation Applies |
|--------|------------------------|
| Module 2 | Evaluate RAG quality (precision, recall, faithfulness) |
| Module 3 | Compare fine-tuned vs base model (did fine-tuning help?) |
| Module 4 | Agent evaluation (did it complete the task? How many steps?) |
| Module 5 | Capstone evaluation — proving your system works to evaluators |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "Accuracy is enough" | LLM outputs are multi-dimensional — faithfulness, helpfulness, safety all matter |
| "Automated metrics are sufficient" | BLEU/ROUGE miss quality. LLM-as-judge or human eval needed for real quality. |
| "One test set is enough" | Need diverse test cases: edge cases, adversarial, multi-lingual, domain-specific |
| "Evaluation is one-time" | Continuous monitoring is essential — model behavior changes with updates |
| "If it works in demos, it works in production" | Demo queries ≠ real user queries. Always eval on real usage patterns. |

## Connection to Other Topics

- **Builds on:** RAG (what to evaluate in retrieval systems), Fine-tuning (measuring improvement)
- **Uses:** LLMs as judges (GPT-4 evaluating outputs), Statistics (metrics computation)
- **Enables:** Production confidence, iteration (know what to improve), safety guarantees

## Ready to Move On?

- ☐ I understand the key evaluation dimensions (faithfulness, relevance, correctness, safety)
- ☐ I know the difference between automated metrics, LLM-as-judge, and human eval
- ☐ I can explain RAG-specific metrics (context precision/recall, faithfulness)
- ☐ I understand why continuous evaluation matters (not just one-time testing)

🎉 You've completed all 12 GenAI Fundamental topics!
