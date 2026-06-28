# Pydantic — Cheatsheet

## Install

```bash
pip install pydantic pydantic-settings
```

## Import

```python
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from typing import Optional, List, Literal
from enum import Enum
```

---

## Define Models

```python
class User(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True                # default
    tags: List[str] = []                  # default list
    bio: Optional[str] = None             # optional (nullable)
```

---

## Field Constraints

```python
class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, description="Must be positive")
    quantity: int = Field(ge=0, le=10000)
    sku: str = Field(pattern=r"^[A-Z]{2}\d{4}$")  # regex
    category: str = Field(default="general")
    
# Number: gt, ge, lt, le
# String: min_length, max_length, pattern
# All: default, default_factory, description, alias, examples
```

---

## Create & Validate

```python
# From keyword args
user = User(name="Alice", age=30, email="a@x.com")

# From dict
user = User.model_validate({"name": "Bob", "age": 25, "email": "b@x.com"})

# From JSON string
user = User.model_validate_json('{"name": "Eve", "age": 28, "email": "e@x.com"}')

# Type coercion (auto-converts when possible)
user = User(name="Alice", age="30", email="a@x.com")  # "30" → 30 ✓

# Handle errors
try:
    user = User(name=123, age="bad", email="x")
except ValidationError as e:
    print(e.errors())  # list of error dicts
```

---

## Serialize (Output)

```python
user.model_dump()                    # → dict
user.model_dump(exclude={"email"})   # exclude fields
user.model_dump(include={"name"})    # include only
user.model_dump_json()               # → JSON string
user.model_dump_json(indent=2)       # pretty JSON
```

---

## JSON Schema (for APIs/LLMs)

```python
schema = User.model_json_schema()
# Returns JSON Schema dict — used by:
# - FastAPI for OpenAPI docs
# - OpenAI for function calling
# - LangChain for JsonOutputParser
```

---

## Nested Models

```python
class Address(BaseModel):
    street: str
    city: str

class Company(BaseModel):
    name: str
    address: Address              # nested
    tags: List[str] = []

# Nested dicts are auto-converted
c = Company(name="X", address={"street": "123 Main", "city": "NYC"})
```

---

## Validators

```python
from pydantic import field_validator, model_validator

class Order(BaseModel):
    quantity: int
    price: float
    discount: float = 0

    @field_validator("quantity")
    @classmethod
    def check_quantity(cls, v):
        if v < 1:
            raise ValueError("quantity must be >= 1")
        return v

    @model_validator(mode="after")
    def check_total(self):
        if self.discount > self.price * self.quantity:
            raise ValueError("discount exceeds total")
        return self
```

---

## Enums & Literals

```python
class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Task(BaseModel):
    status: Status                                    # enum
    priority: Literal["low", "medium", "high"]        # literal
    category: Literal["bug", "feature", "docs"]
```

---

## Optional & Union

```python
from typing import Optional, Union

class Response(BaseModel):
    data: Optional[str] = None              # can be None
    error: Optional[str] = None
    count: Union[int, float]                # either type
    items: List[str] = Field(default_factory=list)  # mutable default
```

---

## Settings (Environment Variables)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str                     # reads OPENAI_API_KEY from env
    debug: bool = False
    port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()  # auto-reads environment
```

---

## LLM Structured Output Pattern

```python
# Define desired output shape
class AnalysisResult(BaseModel):
    summary: str = Field(description="one paragraph summary")
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0, le=1, description="0-1 score")
    key_points: List[str] = Field(description="3-5 bullet points")

# LangChain
from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser(pydantic_object=AnalysisResult)

# LlamaIndex
engine = index.as_query_engine(output_cls=AnalysisResult)

# OpenAI function calling
schema = AnalysisResult.model_json_schema()
```

---

## FastAPI Integration

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    # request is already validated!
    return QueryResponse(answer="...", sources=["doc1"], confidence=0.9)
```

---

## Quick Reference Links

- Docs: https://docs.pydantic.dev/latest/
- Migration v1→v2: https://docs.pydantic.dev/latest/migration/
- Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
