# Structured Output

## The Problem You're Solving

LLMs return free-form text but your application needs parseable data — JSON objects, typed fields, validated schemas. Without structured output enforcement, you get inconsistent formats, missing fields, invalid types, and brittle regex parsing that breaks with every model update.

## Options Available

| Technique | Reliability | Latency Impact | Supported By |
|-----------|-------------|----------------|--------------|
| Prompt-based ("return JSON") | Low (60-80%) | None | All models |
| JSON mode (response_format) | Medium (90-95%) | None | OpenAI, Anthropic |
| Function calling / Tool use | High (95-99%) | Slight overhead | OpenAI, Anthropic, Gemini |
| Structured Outputs (strict schema) | Very High (99%+) | Slight overhead | OpenAI (gpt-4o+) |
| Pydantic + Instructor library | Very High (99%+) | Retry overhead | Any model via library |
| Output parsing + retry | Medium-High (90-98%) | Retry latency | Any model |
| Grammar-constrained decoding | Very High (99%+) | None | Local models (llama.cpp, vLLM) |

## Recommended Approach

**Use OpenAI Structured Outputs (strict mode) when available. Fall back to Instructor + Pydantic for other models. Always define your schema as a Pydantic model first.**


Why: Pydantic gives you compile-time type safety and runtime validation regardless of LLM. OpenAI's strict mode guarantees schema compliance at the API level. Instructor bridges the gap for models without native structured output support.

## Step-by-Step Implementation

### 1. Define Your Schema (Always Start Here)

```python
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Source(BaseModel):
    filename: str = Field(description="Source document filename")
    section: str = Field(description="Relevant section heading")
    relevance_score: float = Field(ge=0, le=1, description="How relevant this source is")

class RAGAnswer(BaseModel):
    """Structured response from RAG pipeline."""
    answer: str = Field(description="The answer to the user's question")
    confidence: Confidence = Field(description="Confidence level based on context quality")
    sources: list[Source] = Field(description="Sources used to generate the answer")
    follow_up_questions: list[str] = Field(
        default_factory=list,
        max_length=3,
        description="Suggested follow-up questions"
    )
    requires_human_review: bool = Field(
        default=False,
        description="Flag if answer quality is uncertain"
    )
```

### 2. OpenAI Structured Outputs (Strict Mode)

```python
from openai import OpenAI

client = OpenAI()

def get_structured_answer(question: str, context: str) -> RAGAnswer:
    """Use OpenAI's native structured output."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # Structured Outputs requires this or later
        messages=[
            {"role": "system", "content": "Answer based on provided context only."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        response_format=RAGAnswer,  # Pydantic model directly!
    )
    
    return response.choices[0].message.parsed  # Returns RAGAnswer instance
```

### 3. Function Calling (Tool Use)

```python
from openai import OpenAI
import json

client = OpenAI()

# Define tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "provide_answer",
            "description": "Provide a structured answer to the user's question",
            "parameters": RAGAnswer.model_json_schema(),  # Auto-generate from Pydantic
        }
    }
]

def get_answer_via_tools(question: str, context: str) -> RAGAnswer:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Use the provide_answer tool to respond."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "provide_answer"}},
    )
    
    # Parse the function call arguments
    args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    return RAGAnswer.model_validate(args)
```

### 4. Instructor Library (Works with Any Model)

```python
# pip install instructor
import instructor
from openai import OpenAI
from anthropic import Anthropic

# OpenAI + Instructor
client = instructor.from_openai(OpenAI())

def get_structured_openai(question: str, context: str) -> RAGAnswer:
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer based on context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        response_model=RAGAnswer,
        max_retries=3,  # Auto-retry on validation failure
    )

# Anthropic + Instructor
anthropic_client = instructor.from_anthropic(Anthropic())

def get_structured_anthropic(question: str, context: str) -> RAGAnswer:
    return anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        response_model=RAGAnswer,
        max_retries=3,
    )
```

### 5. LangChain with Structured Output

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Method 1: with_structured_output
structured_llm = llm.with_structured_output(RAGAnswer)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer based on the provided context only."),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])

chain = prompt | structured_llm
result: RAGAnswer = chain.invoke({"context": context, "question": question})

# Method 2: PydanticOutputParser (for models without native support)
from langchain.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=RAGAnswer)

prompt_with_format = ChatPromptTemplate.from_messages([
    ("system", "Answer the question. {format_instructions}"),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt_with_format | llm | parser
```

### 6. Validation and Error Recovery

```python
from pydantic import ValidationError

class StructuredOutputHandler:
    """Handle structured output with validation and retries."""
    
    def __init__(self, llm, max_retries: int = 3):
        self.llm = llm
        self.max_retries = max_retries
    
    def generate(self, messages, response_model: type[BaseModel]):
        """Generate structured output with automatic retry on validation failure."""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                raw_response = self.llm.invoke(messages)
                
                # Try to parse as JSON
                json_str = self._extract_json(raw_response.content)
                result = response_model.model_validate_json(json_str)
                return result
                
            except (ValidationError, json.JSONDecodeError) as e:
                last_error = e
                # Add error feedback for next attempt
                messages.append({"role": "assistant", "content": raw_response.content})
                messages.append({
                    "role": "user",
                    "content": f"Validation error: {e}. Fix the JSON and try again."
                })
        
        raise StructuredOutputError(f"Failed after {self.max_retries} attempts: {last_error}")
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from markdown code blocks or raw text."""
        if "```json" in text:
            return text.split("```json")[1].split("```")[0].strip()
        if "```" in text:
            return text.split("```")[1].split("```")[0].strip()
        return text.strip()
```

### 7. Streaming with Structured Output

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI())

# Partial streaming — get fields as they're generated
from instructor import Partial

async def stream_structured(question: str, context: str):
    """Stream structured output field-by-field."""
    response = client.chat.completions.create_partial(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        response_model=RAGAnswer,
    )
    
    for partial_answer in response:
        # partial_answer has fields populated as they stream in
        # e.g., first iteration: answer="The rate..." (partial)
        # next: answer="The rate limit is 100/min", confidence="high"
        yield partial_answer
```

## Configuration Checklist

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| Primary method | Structured Outputs (OpenAI) or Instructor | Highest reliability |
| Fallback method | JSON mode + Pydantic validation | Works when strict mode unavailable |
| Max retries | 3 | Diminishing returns after 3 |
| Temperature | 0.0 for structured output | Determinism = consistent schema compliance |
| Schema complexity | Flat preferred (< 3 nesting levels) | Deep nesting increases failure rate |
| Field descriptions | Always include | Guides the model on what to generate |
| Enums vs free text | Enums for categorical fields | Prevents invalid values |
| Optional fields | Use for non-critical data | Prevents failures on uncertain info |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| JSON parsing fails | Model outputs markdown code fence around JSON | Strip code blocks before parsing |
| Missing required fields | Schema too complex or field unclear | Add Field(description=...), simplify schema |
| Enum field has invalid value | Model invents values not in enum | Use Literal types or stricter enums |
| Nested objects malformed | Model struggles with deep nesting | Flatten schema, or generate in stages |
| Instructor retries exhausted | Schema too complex for model capability | Simplify schema, use stronger model, reduce constraints |
| Structured output + streaming breaks | Not all methods support streaming + structure | Use Instructor's create_partial or accept non-streaming |
| Schema change breaks existing code | Response model updated without migration | Version schemas, handle both old/new format |

## Production Considerations

### Performance
- Structured Outputs (OpenAI strict): No meaningful latency overhead
- Instructor retries: Each retry = full LLM call (adds 1-3s)
- Function calling: Slight overhead (~100-200ms) vs plain completion
- Grammar-constrained (local): Actually faster (model constrained to valid tokens)

### Cost
- Retries multiply cost linearly (3 retries = 3x cost)
- Function calling schema tokens count as input tokens
- Instructor's validation retry is usually 1 retry max (2x worst case)

### Reliability by Method
| Method | Success Rate | Notes |
|--------|-------------|-------|
| OpenAI Structured Outputs (strict) | 99.9% | API guarantees schema compliance |
| Instructor + retries | 99%+ | Depends on model + schema complexity |
| Function calling (tool_choice forced) | 98%+ | Model rarely refuses |
| JSON mode + validation | 90-95% | May need retries |
| Prompt-only ("return JSON") | 60-80% | Not production-grade |

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| Schema compliance rate | % of responses that parse without error | > 99% |
| Retry rate | % of requests needing > 1 attempt | < 5% |
| Field accuracy | Are field values correct (not just parseable)? | > 95% |
| Latency overhead | Structured vs unstructured same query | < 200ms additional |
| Cost overhead | Extra tokens from schema / retries | < 20% increase |

## Ready to Ship? — Checklist

- [ ] Schema defined as Pydantic model with descriptions and validators
- [ ] Primary method chosen (Structured Outputs / Instructor / Function Calling)
- [ ] Fallback for parsing failures (retry with error feedback)
- [ ] Temperature set to 0 for structured output calls
- [ ] Schema complexity appropriate for model capability
- [ ] Streaming works with structured output (if needed)
- [ ] Schema versioned (can evolve without breaking consumers)
- [ ] Edge cases handled: empty fields, unexpected values, refusals
- [ ] Validation errors logged and monitored (catch drift)
