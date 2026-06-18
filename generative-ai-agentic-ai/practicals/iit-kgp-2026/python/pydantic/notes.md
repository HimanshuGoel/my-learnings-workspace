# Pydantic — Notes

## What Problem Does This Library Solve?

Pydantic enforces data validation and type safety at runtime in Python — ensuring that data entering your application (from APIs, LLMs, files, user input) matches the expected structure and types, with automatic coercion and clear error messages when it doesn't.

## Mental Model

Think of Pydantic as **TypeScript interfaces for Python**. Just as TypeScript's `interface User { name: string; age: number; }` guarantees shape and types at compile time, Pydantic's `class User(BaseModel)` guarantees shape and types at runtime. It's also like **Java DTOs with built-in validation** — data transfer objects that reject invalid data before it reaches your business logic.

In the AI context: Pydantic is how you force an LLM to return structured, typed JSON instead of free-form text. It's the bridge between "creative AI output" and "reliable application data."

## Where It Fits

```
Unstructured/Untrusted Data Sources
├── LLM output (free-form text → structured JSON)
├── API requests (user input → validated objects)
├── Config files (YAML/JSON → typed settings)
├── Database rows (dict → typed model)
│
▼
┌──────────────┐
│   Pydantic    │  ← validate, coerce, reject bad data (you are here)
└──────┬───────┘
       │ clean, typed Python objects
       ▼
┌──────────────────────────────┐
│ Your Application Logic        │
│ • FastAPI request/response    │
│ • LangChain structured output │
│ • LlamaIndex output schemas   │
│ • Config management           │
└──────────────────────────────┘
```

- **Before Pydantic:** Raw dicts, untyped data, no validation
- **After Pydantic:** Typed objects with guaranteed structure and valid values
- **Talks to:** FastAPI (request/response validation), LangChain (JsonOutputParser), LlamaIndex (output_cls), OpenAI (function calling schemas)

## Core Concepts

### 1. BaseModel — Define Your Data Shape

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True              # default value
    tags: List[str] = []                # default empty list
    bio: Optional[str] = None           # optional field

# Create instance (validates automatically)
user = User(name="Alice", age=30, email="alice@example.com")
print(user.name)        # "Alice"
print(user.model_dump()) # {'name': 'Alice', 'age': 30, ...}

# Type coercion (Pydantic converts when possible)
user2 = User(name="Bob", age="25", email="bob@x.com")  # "25" → 25 ✓

# Validation error (rejects invalid data)
# User(name="Eve", age="not_a_number", email="bad")  # → ValidationError!
```

### 2. Field — Constraints and Descriptions

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Product name")
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, le=10000, description="Stock quantity")
    category: str = Field(pattern=r"^[a-z]+$", description="Lowercase category")
    rating: float = Field(ge=0, le=5, description="Rating 0-5")

# Field constraints:
# Strings: min_length, max_length, pattern (regex)
# Numbers: gt, ge, lt, le (greater than, greater or equal, etc.)
# General: default, description, alias, examples
```

### 3. Validation — Automatic Type Checking

```python
from pydantic import BaseModel, ValidationError

class Config(BaseModel):
    host: str
    port: int
    debug: bool

# Valid
config = Config(host="localhost", port=8080, debug=True)

# Invalid — raises ValidationError with detailed errors
try:
    bad = Config(host=123, port="not_a_port", debug="maybe")
except ValidationError as e:
    print(e.errors())
    # [{'type': 'string_type', 'loc': ('host',), 'msg': 'Input should be a valid string'},
    #  {'type': 'int_parsing', 'loc': ('port',), 'msg': 'Input should be a valid integer'}]
```

### 4. Nested Models — Compose Complex Structures

```python
class Address(BaseModel):
    street: str
    city: str
    country: str = "US"

class Company(BaseModel):
    name: str
    address: Address              # nested model
    employees: List["Employee"]   # list of nested models

class Employee(BaseModel):
    name: str
    role: str
    company: Optional[Company] = None  # circular reference OK

# Usage
company = Company(
    name="Acme",
    address={"street": "123 Main", "city": "NYC"},  # dict auto-converted!
    employees=[{"name": "Alice", "role": "Engineer"}]
)
```

### 5. Serialization — To/From JSON and Dicts

```python
class User(BaseModel):
    name: str
    age: int
    email: str

user = User(name="Alice", age=30, email="a@x.com")

# To dict
data = user.model_dump()               # {'name': 'Alice', 'age': 30, 'email': 'a@x.com'}
data = user.model_dump(exclude={"email"})  # exclude fields

# To JSON string
json_str = user.model_dump_json()      # '{"name":"Alice","age":30,"email":"a@x.com"}'

# From dict
user2 = User.model_validate({"name": "Bob", "age": 25, "email": "b@x.com"})

# From JSON string
user3 = User.model_validate_json('{"name": "Eve", "age": 28, "email": "e@x.com"}')

# Get JSON Schema (used by OpenAI function calling, LangChain, etc.)
schema = User.model_json_schema()
```

### 6. Custom Validators — Business Logic

```python
from pydantic import BaseModel, field_validator, model_validator

class Booking(BaseModel):
    check_in: str
    check_out: str
    guests: int
    room_type: str

    @field_validator("guests")
    @classmethod
    def validate_guests(cls, v):
        if v < 1 or v > 10:
            raise ValueError("Guests must be between 1 and 10")
        return v

    @field_validator("room_type")
    @classmethod
    def validate_room(cls, v):
        allowed = ["single", "double", "suite"]
        if v not in allowed:
            raise ValueError(f"room_type must be one of {allowed}")
        return v

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self
```

### 7. LLM Structured Output — The AI Use Case

```python
from pydantic import BaseModel, Field

# Define what you want the LLM to return
class SentimentResult(BaseModel):
    sentiment: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(ge=0, le=1, description="confidence score")
    reasoning: str = Field(description="brief explanation")

# Use with LangChain
from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser(pydantic_object=SentimentResult)

# Use with OpenAI function calling
schema = SentimentResult.model_json_schema()
# Pass schema as function parameter definition → LLM returns matching JSON

# Use with LlamaIndex
engine = index.as_query_engine(output_cls=SentimentResult)
```

### 8. Settings Management

```python
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    """Reads from environment variables automatically."""
    openai_api_key: str
    database_url: str = "sqlite:///local.db"
    debug: bool = False
    max_retries: int = 3

    class Config:
        env_file = ".env"  # reads from .env file

# Usage (reads OPENAI_API_KEY from environment)
settings = AppSettings()
print(settings.openai_api_key)
```

### 9. Enums and Literal Types

```python
from pydantic import BaseModel
from enum import Enum
from typing import Literal

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    priority: Priority                           # enum validation
    status: Literal["todo", "in_progress", "done"]  # literal validation

task = Task(title="Fix bug", priority="high", status="in_progress")
# Task(title="X", priority="invalid", status="invalid")  → ValidationError!
```

### 10. Schema Generation for APIs

```python
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    
class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "gpt-4o-mini"
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=1000, gt=0, le=4096)

# FastAPI uses this schema automatically for:
# - Request body validation
# - OpenAPI/Swagger documentation
# - Type hints in your IDE

# Get the JSON Schema
print(ChatRequest.model_json_schema())
```

## Key Functions/Methods

### Model Operations

| Method | Purpose |
|--------|---------|
| `Model(field=value)` | Create and validate instance |
| `Model.model_validate(dict)` | Create from dict |
| `Model.model_validate_json(str)` | Create from JSON string |
| `instance.model_dump()` | Convert to dict |
| `instance.model_dump_json()` | Convert to JSON string |
| `Model.model_json_schema()` | Get JSON Schema (for APIs, LLMs) |
| `Model.model_fields` | Inspect field definitions |

### Field Constraints

| Constraint | Type | Example |
|-----------|------|---------|
| `gt, ge, lt, le` | Numbers | `Field(gt=0, le=100)` |
| `min_length, max_length` | Strings | `Field(min_length=1)` |
| `pattern` | Strings (regex) | `Field(pattern=r"^\d{3}$")` |
| `default` | Any | `Field(default="hello")` |
| `description` | Docs | `Field(description="user name")` |
| `alias` | Rename | `Field(alias="userName")` |
| `examples` | Docs | `Field(examples=["Alice", "Bob"])` |

### Validators

| Decorator | Scope |
|-----------|-------|
| `@field_validator("field_name")` | Single field |
| `@model_validator(mode="after")` | Entire model (cross-field) |
| `@model_validator(mode="before")` | Before type coercion |

## Common Patterns

### API Request/Response Models

```python
class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(pattern=r"^[\w.+-]+@[\w-]+\.[\w.]+$")
    age: int = Field(ge=18, le=120)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str
```

### LLM Output Schema (RAG/Agents)

```python
class RAGResponse(BaseModel):
    answer: str = Field(description="the answer to the question")
    confidence: float = Field(ge=0, le=1, description="how confident 0-1")
    sources: List[str] = Field(description="list of source document names")
    needs_clarification: bool = Field(description="whether question is ambiguous")
```

### Config with Environment Variables

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    chroma_persist_dir: str = "./chroma_db"
    chunk_size: int = 512
    top_k: int = 5
    model_name: str = "gpt-4o-mini"
    
    class Config:
        env_file = ".env"
```

## AI/ML Connection

- **Where in the AI pipeline:** Pydantic validates data at every boundary — API inputs, LLM outputs, config loading, database records. It's the "type safety layer" for AI applications.

- **Concrete example — Structured LLM Output (Module 2):** Force an LLM to return JSON matching a Pydantic schema. Instead of parsing free text, you get `response.answer`, `response.confidence`, `response.sources` — typed, validated, guaranteed.

- **Concrete example — FastAPI + RAG (Module 5):** Your capstone API endpoint accepts a `QueryRequest(question: str, top_k: int)` and returns a `QueryResponse(answer: str, sources: List[str])`. Pydantic validates both directions.

- **Concrete example — LangChain JsonOutputParser:** LangChain's `JsonOutputParser(pydantic_object=MySchema)` uses your Pydantic model to generate format instructions for the LLM and validate the response.

- **Concrete example — OpenAI Function Calling:** `model_json_schema()` generates the exact JSON Schema format OpenAI needs for function/tool definitions. Define a Pydantic model → get a function schema for free.

- **Which IIT KGP modules use this:** Module 2 (structured RAG output), Module 4 (agent tool schemas, structured responses), Module 5 (FastAPI request/response, config management).

- **What breaks without it:** Without Pydantic, you'd manually check every field (`if "name" in data and isinstance(data["name"], str) and len(data["name"]) > 0 ...`). Pydantic replaces hundreds of lines of validation boilerplate with declarative models.

## Common Mistakes

1. **Confusing Pydantic v1 and v2 syntax** — v2 uses `model_dump()` not `dict()`, `model_validate()` not `parse_obj()`. LangChain still uses some v1 internally (imports from `langchain_core.pydantic_v1`).

2. **Forgetting `Field(description=...)` for LLM schemas** — the LLM uses descriptions to understand what each field means. Without them, it guesses (often wrong).

3. **Not handling ValidationError** — wrap model creation in try/except when data comes from external sources (user input, LLM output).

4. **Over-constraining** — don't add regex patterns or strict limits unless you actually need them. Over-validation makes the LLM fail to match the schema.

5. **Mutable defaults** — use `Field(default_factory=list)` instead of `Field(default=[])` for mutable defaults (lists, dicts).

6. **Not using Optional for nullable fields** — `name: str` rejects None. Use `name: Optional[str] = None` if the field can be absent.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Internal data you trust completely | Plain dataclasses or dicts |
| Performance-critical tight loops (millions/sec) | dataclasses (no validation overhead) |
| Simple config (few values) | Plain dict or os.environ |
| Schema-less exploration (notebooks) | Raw dicts |
| Database ORM models | SQLAlchemy models (with Pydantic for API layer) |

## Ready to Move On?

- ☐ I can define a BaseModel with typed fields and constraints
- ☐ I can use Field() for validation rules and descriptions
- ☐ I can serialize to/from dict and JSON (model_dump, model_validate)
- ☐ I can create schemas for LLM structured output (with LangChain/LlamaIndex)
- ☐ I understand model_json_schema() and its use in APIs/function calling

Once all checked → move to **FastAPI**.
