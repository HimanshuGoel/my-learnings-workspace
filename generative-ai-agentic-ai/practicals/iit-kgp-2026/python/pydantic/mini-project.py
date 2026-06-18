"""
=============================================================================
MINI PROJECT: LLM Output Validator & Schema Generator
=============================================================================

PROBLEM STATEMENT:
Build a system that defines structured schemas for LLM outputs, validates
responses, generates format instructions for prompts, and handles retries
when the LLM returns invalid data.

WHAT YOU'LL BUILD:
- Schema definitions for various AI tasks (classification, extraction, QA)
- A validator that checks LLM JSON output against schemas
- A format instruction generator (tells the LLM what shape to produce)
- A retry mechanism that feeds validation errors back to the LLM
- A schema registry for managing multiple output types

WHY THIS MATTERS:
Production AI apps CANNOT accept free-form text from LLMs. You need
guaranteed structure (JSON with specific fields, types, constraints).
This is exactly how LangChain's JsonOutputParser and OpenAI's function
calling work under the hood. Module 2 (structured RAG output) and
Module 5 (API responses) both need this pattern.

ESTIMATED TIME: 30-45 minutes

SETUP: pip install pydantic

RULES:
- Use Pydantic v2 syntax (model_dump, model_validate, model_json_schema)
- Handle all edge cases (malformed JSON, missing fields, wrong types)
- Follow the TODOs in order
=============================================================================
"""

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Literal, Dict, Any
import json


# =============================================================================
# TODO 1: Define Output Schemas for AI Tasks
# =============================================================================
# Define Pydantic models for common LLM output structures.
# Include Field descriptions (the LLM uses these to understand what to produce).

# Schema 1: Sentiment Analysis
class SentimentOutput(BaseModel):
    """Expected output from sentiment analysis."""
    # TODO: Define fields
    # sentiment: Literal["positive", "negative", "neutral"]
    # confidence: float (0-1)
    # reasoning: str (brief explanation)
    pass


# Schema 2: Named Entity Extraction
class Entity(BaseModel):
    """A single extracted entity."""
    # TODO: name, entity_type (person/org/location/date), context (surrounding text)
    pass

class EntityExtractionOutput(BaseModel):
    """Expected output from entity extraction."""
    # TODO: entities: List[Entity], total_count: int
    pass


# Schema 3: RAG Question Answering
class SourceReference(BaseModel):
    """A source document reference."""
    # TODO: document_name, page/section, relevance_score (0-1)
    pass

class RAGOutput(BaseModel):
    """Expected output from RAG QA."""
    # TODO: answer, confidence (0-1), sources: List[SourceReference],
    #       needs_clarification: bool, follow_up_questions: List[str]
    pass


# Schema 4: Classification with Explanation
class ClassificationOutput(BaseModel):
    """Expected output from classification."""
    # TODO: label, confidence, reasoning, alternative_labels: List with scores
    pass


# =============================================================================
# TODO 2: Format Instruction Generator
# =============================================================================
# Generate human-readable format instructions from a Pydantic model.
# These instructions are included in the LLM prompt to tell it what shape
# to return its answer in.
# Example output:
#   "Return your response as JSON matching this schema:
#    {
#      "sentiment": "positive, negative, or neutral",
#      "confidence": "float between 0 and 1",
#      ...
#    }"

def generate_format_instructions(model_class) -> str:
    """Generate LLM-friendly format instructions from a Pydantic model."""
    # TODO: Get model_json_schema()
    # TODO: Format as readable instructions
    # TODO: Include field descriptions and constraints
    # TODO: Return as a string to embed in prompts
    pass


# =============================================================================
# TODO 3: Output Validator
# =============================================================================
# Validate a raw string (potentially from an LLM) against a Pydantic model.
# Handle cases:
#   - Valid JSON matching schema → return parsed object
#   - Valid JSON but wrong structure → return error details
#   - Invalid JSON (parse error) → return error details
#   - Empty/None input → return error

def validate_output(raw_output: str, model_class) -> Dict[str, Any]:
    """
    Validate LLM output against a Pydantic model.
    Returns: {"success": bool, "data": parsed_object or None, "errors": list or None}
    """
    # TODO: Try to parse JSON
    # TODO: Try to validate with model_class
    # TODO: Return structured result with success/failure info
    pass


# =============================================================================
# TODO 4: Error Feedback Generator
# =============================================================================
# When validation fails, generate a clear message to send back to the LLM
# so it can fix its response. Include:
#   - What was wrong
#   - What was expected
#   - The original response (for context)

def generate_retry_prompt(original_output: str, errors: list, model_class) -> str:
    """Generate a retry prompt when LLM output is invalid."""
    # TODO: Format errors in a way the LLM can understand
    # TODO: Include the original output
    # TODO: Include the expected schema
    # TODO: Return prompt string
    pass


# =============================================================================
# TODO 5: Schema Registry
# =============================================================================
# Manage multiple output schemas for different tasks.
# Register schemas by task name, retrieve when needed.

class SchemaRegistry:
    """Registry for managing multiple Pydantic output schemas."""
    
    def __init__(self):
        self._schemas: Dict[str, type] = {}
    
    def register(self, task_name: str, schema_class):
        """Register a schema for a task."""
        # TODO: Store schema
        pass
    
    def get_schema(self, task_name: str):
        """Get schema class by task name."""
        # TODO: Retrieve schema
        pass
    
    def get_instructions(self, task_name: str) -> str:
        """Get format instructions for a task."""
        # TODO: Generate instructions for the task's schema
        pass
    
    def validate(self, task_name: str, raw_output: str) -> Dict[str, Any]:
        """Validate output against the task's schema."""
        # TODO: Validate using the registered schema
        pass
    
    def list_tasks(self) -> List[str]:
        """List all registered task names."""
        # TODO: Return list of registered task names
        pass


# =============================================================================
# TODO 6: Full Validation Pipeline Demo
# =============================================================================
# Simulate the complete flow:
# 1. Register schemas
# 2. Generate prompt instructions
# 3. "LLM" returns output (simulated)
# 4. Validate
# 5. If invalid, generate retry prompt
# 6. "LLM" retries (simulated)
# 7. Validate again

def demo_pipeline():
    """Demonstrate the full validation pipeline."""
    # Simulated LLM outputs (some good, some bad)
    simulated_outputs = {
        "sentiment": [
            '{"sentiment": "positive", "confidence": 0.92, "reasoning": "Enthusiastic language"}',
            '{"sentiment": "very_positive", "confidence": 1.5, "reasoning": ""}',  # bad
        ],
        "rag": [
            '{"answer": "The return policy allows 30 days", "confidence": 0.88, "sources": [{"document_name": "policy.pdf", "page": 3, "relevance_score": 0.91}], "needs_clarification": false, "follow_up_questions": ["What about opened items?"]}',
            'I think the return policy is 30 days but I am not sure.',  # not JSON
        ],
    }
    # TODO: Walk through the pipeline for each task
    pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("LLM OUTPUT VALIDATOR & SCHEMA GENERATOR")
    print("=" * 60)

    # Step 1: Register schemas
    print("\n--- STEP 1: REGISTER SCHEMAS ---")
    registry = SchemaRegistry()
    registry.register("sentiment", SentimentOutput)
    registry.register("entities", EntityExtractionOutput)
    registry.register("rag", RAGOutput)
    registry.register("classification", ClassificationOutput)
    print(f"Registered tasks: {registry.list_tasks()}")

    # Step 2: Generate instructions
    print("\n--- STEP 2: FORMAT INSTRUCTIONS ---")
    for task in registry.list_tasks():
        print(f"\n[{task}]")
        instructions = registry.get_instructions(task)
        if instructions:
            print(instructions[:200] + "..." if len(instructions) > 200 else instructions)

    # Step 3: Validate sample outputs
    print("\n--- STEP 3: VALIDATE OUTPUTS ---")
    test_cases = [
        ("sentiment", '{"sentiment": "positive", "confidence": 0.9, "reasoning": "Great tone"}'),
        ("sentiment", '{"sentiment": "bad_value", "confidence": 2.0}'),
        ("rag", 'not json at all'),
    ]
    for task, output in test_cases:
        print(f"\nTask: {task}")
        print(f"Input: {output[:60]}...")
        result = registry.validate(task, output)
        if result:
            print(f"Valid: {result.get('success')}")
            if not result.get('success'):
                print(f"Errors: {result.get('errors')}")

    # Step 4: Demo retry pipeline
    print("\n--- STEP 4: RETRY PIPELINE ---")
    demo_pipeline()

    print("\n" + "=" * 60)
    print("Done! Schema validation system complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
