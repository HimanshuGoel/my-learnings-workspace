"""
Pydantic Exercises — 12 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. AI-relevant exercises are marked with [AI].

SETUP: pip install pydantic pydantic-settings
(No API keys needed — all runs locally)

Run: python exercises.py
"""

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from typing import Optional, List, Literal
from enum import Enum

# =============================================================================
# EASY (1-4)
# =============================================================================

# Exercise 1: Basic Model Definition
# Define a model for a "Book" with:
#   - title: str (required)
#   - author: str (required)
#   - pages: int (required, must be > 0)
#   - rating: float (optional, 0-5)
#   - genres: list of strings (default empty)
# Create 3 valid instances and print their dict representation.
# Expected: typed, validated Book objects

def exercise_1():
    # Your code here: define Book model, create instances, print
    pass


# Exercise 2: Validation & Error Handling
# Using the Book model from Exercise 1:
# a) Try creating a Book with pages=-10 (should fail)
# b) Try creating with rating=6 (should fail)
# c) Try creating with title=None (should fail)
# d) Catch ValidationError and print the error details
# e) Show that age="100" gets coerced to int 100 (type coercion)
# Expected: clear error messages for invalid data

def exercise_2():
    # Your code here: test validation, catch errors
    pass


# Exercise 3: Nested Models
# Define a model for an "Order" system:
#   - Customer: name, email
#   - Item: name, price (>0), quantity (>=1)
#   - Order: customer (Customer), items (List[Item]), total (computed)
# Create an order by passing nested dicts (auto-conversion).
# Expected: nested validation works with plain dicts as input

def exercise_3():
    # Your code here: define nested models, create from dicts
    pass


# Exercise 4: Serialization (To/From JSON)
# a) Create a model instance
# b) Convert to dict (model_dump)
# c) Convert to JSON string (model_dump_json)
# d) Recreate from dict (model_validate)
# e) Recreate from JSON string (model_validate_json)
# f) Round-trip: verify original == recreated
# Expected: lossless serialization round-trip

def exercise_4():
    # Your code here: demonstrate full serialization cycle
    pass


# =============================================================================
# MEDIUM (5-8)
# =============================================================================

# Exercise 5: Custom Validators
# Define a "UserRegistration" model with:
#   - username: str (3-20 chars, alphanumeric only)
#   - password: str (min 8 chars, must contain digit + uppercase)
#   - confirm_password: str (must match password)
#   - email: str (must contain @)
# Use @field_validator for username and password.
# Use @model_validator for password confirmation.
# Expected: custom validation logic with clear errors

def exercise_5():
    # Your code here: model with custom validators
    pass


# Exercise 6: Enum and Literal Types [AI]
# Define a model for an "LLM Request":
#   - model: Literal["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
#   - temperature: float (0-2)
#   - messages: List of Message (role + content)
#   - role must be Literal["system", "user", "assistant"]
# Test valid and invalid combinations.
# This mimics the OpenAI Chat Completions request structure.
# Expected: only valid models and roles accepted

def exercise_6():
    # Your code here
    pass


# Exercise 7: LLM Structured Output Schema [AI]
# Define schemas for common LLM output structures:
# a) SentimentResult: sentiment, confidence, reasoning
# b) EntityExtraction: entities (list of Entity with name, type, context)
# c) RAGResponse: answer, sources, confidence, needs_clarification
# Print the JSON Schema for each (model_json_schema).
# These schemas are passed to LangChain/LlamaIndex for structured output.
# Expected: valid JSON Schemas ready for LLM tooling

def exercise_7():
    # Your code here: define 3 schemas, print their JSON schemas
    pass


# Exercise 8: Settings from Environment [AI]
# Define an AppSettings model using pydantic-settings:
#   - openai_api_key: str (required)
#   - model_name: str (default "gpt-4o-mini")
#   - temperature: float (default 0.7, 0-2)
#   - chunk_size: int (default 512)
#   - top_k: int (default 5)
# Show that it reads from environment variables.
# This is how production AI apps manage configuration.
# Expected: settings loaded from env with validation

def exercise_8():
    import os
    # Set fake env vars for testing
    os.environ["OPENAI_API_KEY"] = "sk-test-fake-key"
    os.environ["TEMPERATURE"] = "0.5"
    # Your code here: define Settings, instantiate, print
    # Remember to clean up: del os.environ["OPENAI_API_KEY"]
    pass


# =============================================================================
# HARD (9-12)
# =============================================================================

# Exercise 9: API Request/Response Models (FastAPI Pattern) [AI]
# Define models for a RAG API:
#   Request:  QueryRequest(question: str, top_k: int, filter_source: Optional[str])
#   Response: QueryResponse(answer: str, sources: List[Source], confidence: float)
#   Source:   Source(document: str, page: int, relevance_score: float)
# Simulate: validate a request, create a response, serialize both.
# This is the exact pattern you'll use in Module 5 (FastAPI deployment).
# Expected: clean request → validated → response → JSON

def exercise_9():
    # Your code here
    pass


# Exercise 10: Dynamic Model Creation [AI]
# Create Pydantic models dynamically based on a schema definition:
# Given a list of field specs: [("name", str, True), ("age", int, False), ...]
# Generate a Pydantic model at runtime.
# This is useful when LLM tools have dynamic schemas.
# Expected: dynamically created model that validates correctly

def exercise_10():
    from pydantic import create_model
    # Field specs: (name, type, required)
    field_specs = [
        ("title", str, True),
        ("rating", float, False),
        ("year", int, True),
        ("genre", str, False),
    ]
    # Your code here: use create_model to build dynamic model
    pass


# Exercise 11: Complex LLM Tool Schema [AI]
# Define a complete tool definition for OpenAI function calling:
# Tool: "search_products"
# Parameters:
#   - query: str (the search query)
#   - category: optional enum (electronics, clothing, food)
#   - price_range: optional object with min/max
#   - sort_by: literal (relevance, price_asc, price_desc, rating)
# Generate the function calling schema from the Pydantic model.
# Expected: schema compatible with OpenAI's function calling format

def exercise_11():
    # Your code here: define complex nested schema
    pass


# Exercise 12: Validate LLM Output (Retry Pattern) [AI]
# Simulate the pattern of:
# 1. LLM returns JSON (possibly malformed)
# 2. Validate with Pydantic
# 3. If invalid, format error message and ask LLM to fix
# 4. Validate again
# This retry-with-feedback pattern is standard in production.
# Expected: demonstrate graceful handling of bad LLM output

def exercise_12():
    # Simulated LLM outputs (some valid, some not)
    llm_outputs = [
        '{"answer": "Paris is the capital", "confidence": 0.95, "sources": ["geo.txt"]}',  # valid
        '{"answer": "Unknown", "confidence": 1.5, "sources": []}',  # confidence > 1 (invalid)
        '{"answer": "", "sources": ["doc.pdf"]}',  # missing confidence (invalid)
        'This is not JSON at all',  # completely invalid
    ]
    # Your code here: validate each, handle errors gracefully
    pass


# =============================================================================
# Run all exercises
# =============================================================================

if __name__ == "__main__":
    exercises = [exercise_1, exercise_2, exercise_3, exercise_4, exercise_5,
                 exercise_6, exercise_7, exercise_8, exercise_9, exercise_10,
                 exercise_11, exercise_12]

    for i, ex in enumerate(exercises, 1):
        print(f"\n{'='*60}")
        print(f"Exercise {i}")
        print('='*60)
        try:
            ex()
        except Exception as e:
            print(f"  [Error: {type(e).__name__}: {e}]")
