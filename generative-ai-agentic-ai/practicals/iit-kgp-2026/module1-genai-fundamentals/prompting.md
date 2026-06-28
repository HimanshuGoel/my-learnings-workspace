# Prompting

## What Is This?

Prompting is the art of instructing an LLM to perform a task through natural language input — including system instructions, examples, formatting guidance, and reasoning hints — without changing the model's weights.

## Why Does It Exist?

**The Problem:** You have a pre-trained model with broad capabilities. How do you get it to do YOUR specific task? Two options:
1. Fine-tune (change weights) — expensive, needs data, slow iteration
2. Prompt (change input) — free, instant, iterate in seconds

Prompting lets you use the model's existing knowledge by framing requests effectively.

**The Insight:** The same model gives dramatically different quality answers depending on how you ask. Prompting is cheap steering of an expensive model.

## Mental Model

Think of prompting as **writing a clear ticket/requirement for a smart but literal contractor**. The contractor (LLM) is extremely capable but does exactly what you say — not what you mean. A vague ticket → vague output. A specific, structured ticket → precise output.

Or: like **configuring a framework via configuration files** instead of writing code. You don't change Spring Boot's source — you configure it via application.yml. Prompts configure the LLM's behavior.

## How It Works

### Prompting Strategies (Least → Most Powerful)

| Strategy | Description | When to Use |
|----------|-------------|------------|
| Zero-shot | Just the instruction, no examples | Simple tasks the model knows well |
| Few-shot | Instruction + 2-5 examples | When format/style needs demonstration |
| Chain-of-Thought (CoT) | "Think step by step" | Complex reasoning, math, logic |
| System prompt | Set persona/behavior/constraints | Every production app |
| Structured output | Force JSON/specific format | API responses, data extraction |

### Zero-Shot

```
Classify the sentiment of this review as positive, negative, or neutral:
"The food was amazing but the service was terrible"
```

### Few-Shot (Provide Examples)

```
Classify sentiment:
Review: "Loved it!" → positive
Review: "Terrible experience" → negative
Review: "It was okay" → neutral
Review: "The food was amazing but the service was terrible" →
```

### Chain-of-Thought

```
Solve this step by step:
If a shirt costs $20 and is 25% off, what's the final price?

Step 1: Calculate discount = $20 × 0.25 = $5
Step 2: Final price = $20 - $5 = $15
Answer: $15
```

Adding "Let's think step by step" or "Think through this carefully" dramatically improves reasoning quality.

### System Prompts

```
System: You are a senior Python developer. You write clean, well-documented code.
        Always include error handling. Use type hints.

User: Write a function to validate an email address.
```

### Structured Output

```
Extract the following from this text and return as JSON:
{
  "name": "...",
  "email": "...",
  "sentiment": "positive/negative/neutral",
  "confidence": 0.0-1.0
}

Text: "Hi, I'm Alice (alice@example.com). I absolutely love your product!"
```

## Key Prompting Principles

1. **Be specific** — "Summarize in 3 bullet points, each under 20 words" > "Summarize this"
2. **Provide context** — tell it what it is, what the audience is, what the constraints are
3. **Use examples** — show what good output looks like (few-shot)
4. **Separate instruction from data** — use delimiters (```text```, XML tags, markdown headers)
5. **Constrain the output** — specify format, length, tone, what NOT to include
6. **Iterate** — prompt engineering is experimentation, not one-shot

## Where You'll Use This

| Module | How Prompting Applies |
|--------|----------------------|
| Module 1 | Core skill — everything you do with LLMs starts with a prompt |
| Module 2 | RAG prompts: "Answer based ONLY on this context: {docs}" |
| Module 3 | Instruction datasets for fine-tuning ARE prompt-response pairs |
| Module 4 | Agent prompts: "You have tools: [...]. Decide which to use." |
| Module 5 | Production prompt templates managed as code (versioned, tested) |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "There's one correct prompt" | Prompting is iterative. Multiple phrasings work. Test and compare. |
| "Longer prompt = better" | Concise, clear prompts often outperform verbose ones. Quality > quantity. |
| "CoT always helps" | For simple tasks it adds unnecessary tokens (cost). Use for reasoning tasks. |
| "Prompts are permanent" | They're fragile — model updates can break them. Version and test continuously. |
| "Prompting replaces fine-tuning" | For high-volume, domain-specific tasks, fine-tuning is more reliable and cheaper per-call. |

## Connection to Other Topics

- **Builds on:** Pre-training (prompts work because the model learned language patterns)
- **Enables:** RAG (prompt includes retrieved context), Agents (prompt defines available tools)
- **Related:** Decoding (temperature/top-p affect output from the same prompt)
- **Leads to:** Fine-tuning (when prompting isn't enough for your use case)

## Ready to Move On?

- ☐ I understand zero-shot vs few-shot vs chain-of-thought prompting
- ☐ I can write a system prompt that constrains model behavior
- ☐ I know how to force structured output (JSON) from an LLM
- ☐ I understand that prompting is iterative — test, compare, refine

Next → **Decoding** (how the model chooses which words to generate)
