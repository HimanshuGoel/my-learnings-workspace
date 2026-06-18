"""
LangChain Exercises — 12 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. All exercises are AI-relevant.

SETUP: pip install langchain langchain-openai langchain-community chromadb
NOTE: Exercises requiring OpenAI need OPENAI_API_KEY env variable.
      Exercises 1-4 can use HuggingFace models (free, local) instead.

Run: python exercises.py
"""

# =============================================================================
# EASY (1-4)
# =============================================================================

# Exercise 1: Prompt Templates
# Create a ChatPromptTemplate that takes {topic} and {audience} variables.
# System message: "You explain {topic} for {audience}. Be concise."
# Human message: "Explain {topic}"
# Print the formatted messages (don't invoke a model yet).
# Expected: formatted messages with variables filled in

def exercise_1():
    from langchain_core.prompts import ChatPromptTemplate
    # Your code here: create template, invoke with variables, print messages
    pass


# Exercise 2: Basic Chain (LCEL)
# Build a chain: prompt | model | parser
# Use any available LLM (OpenAI or a mock for testing).
# Chain should: take a topic → generate a one-sentence explanation.
# LCEL = LangChain Expression Language (the | pipe syntax for composing steps)
# Expected: working chain that takes input and returns string

def exercise_2():
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    # If you have OpenAI key:
    # from langchain_openai import ChatOpenAI
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # Otherwise: use a fake LLM for testing the chain structure
    from langchain_core.language_models.fake import FakeListLLM
    # Your code here: build chain, invoke
    pass


# Exercise 3: Output Parser — Structured JSON
# Create a chain that returns structured output (JSON).
# Define a Pydantic model for a "BookRecommendation":
#   - title: str
#   - author: str  
#   - reason: str (why this book is recommended)
# Use JsonOutputParser to get structured response.
# Expected: parsed dict with title, author, reason

def exercise_3():
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.pydantic_v1 import BaseModel, Field
    from langchain_core.prompts import ChatPromptTemplate
    # Your code here: define Pydantic model, parser, chain
    pass


# Exercise 4: Document Loading & Splitting
# Create 3 fake documents (strings), wrap as Document objects.
# Split them using RecursiveCharacterTextSplitter (chunk_size=100, overlap=20).
# Print: number of chunks, first chunk's content and metadata.
# Expected: more chunks than original docs due to splitting

def exercise_4():
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document

    documents = [
        Document(page_content="Machine learning is a subset of artificial intelligence. "
                 "It allows systems to learn from data without being explicitly programmed. "
                 "ML algorithms improve through experience and can identify patterns.",
                 metadata={"source": "ml_intro.txt", "page": 1}),
        Document(page_content="Deep learning uses neural networks with many layers. "
                 "It excels at tasks like image recognition and natural language processing. "
                 "Training deep models requires large datasets and significant compute.",
                 metadata={"source": "dl_intro.txt", "page": 1}),
        Document(page_content="Transformers revolutionized NLP in 2017. "
                 "The attention mechanism allows models to weigh different parts of input. "
                 "BERT and GPT are both based on the transformer architecture.",
                 metadata={"source": "transformers.txt", "page": 1}),
    ]
    # Your code here: split, print stats
    pass


# =============================================================================
# MEDIUM (5-8)
# =============================================================================

# Exercise 5: Vector Store & Retrieval
# Create an in-memory vector store with ChromaDB:
# a) Take the chunks from Exercise 4
# b) Embed them using HuggingFace embeddings (free, local)
# c) Store in Chroma
# d) Query with a question, get top-2 results
# e) Print retrieved chunks with their scores
# Expected: relevant chunks retrieved for the query

def exercise_5():
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document
    # Your code here: create chunks, embed, store, query
    pass


# Exercise 6: RAG Chain (Complete Pipeline)
# Build a full RAG chain:
# a) Use the vector store from Exercise 5 as retriever
# b) Create a RAG prompt template
# c) Chain: retriever → format → prompt → llm → parse
# d) Ask a question and get an answer grounded in the documents
# This is THE core pattern of Module 2.
# Expected: answer that references information from the documents

def exercise_6():
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    # Your code here: build full RAG chain
    # (Use FakeListLLM if no API key, or ChatOpenAI if available)
    pass


# Exercise 7: Tool Definition & Agent
# Create 2 custom tools:
# a) word_count(text) — returns the word count of input text
# b) reverse_text(text) — returns the reversed string
# Create an agent that decides which tool to use based on the question.
# agent = LLM that reasons about which tools to call and in what order
# Expected: agent uses correct tool for each query

def exercise_7():
    from langchain_core.tools import tool
    # Your code here: define tools, create agent
    # Note: Agent creation requires a real LLM (tool-calling capable)
    # If no API key, just define the tools and show their schemas
    pass


# Exercise 8: RunnableParallel — Multiple Chains at Once
# Create a parallel chain that processes text in 3 ways simultaneously:
# a) Chain 1: count words
# b) Chain 2: extract first sentence
# c) Chain 3: convert to uppercase
# Use RunnableParallel to run all at once.
# RunnableParallel = execute multiple chains simultaneously on same input
# Expected: dict with results from all 3 chains

def exercise_8():
    from langchain_core.runnables import RunnableParallel, RunnableLambda
    # Your code here: create 3 simple chains, run in parallel
    pass


# =============================================================================
# HARD (9-12)
# =============================================================================

# Exercise 9: Conversational RAG (Memory + Retrieval)
# Build a RAG system that remembers conversation history:
# a) Set up vector store with some documents
# b) Add conversation memory
# c) First query: ask a question (retrieves and answers)
# d) Follow-up query: ask about "it" (should understand from context)
# This is how production chatbots over documents work.
# Expected: follow-up question correctly references previous context

def exercise_9():
    # Your code here
    # This is a conceptual exercise — show the architecture and components
    # Even without an API key, diagram the flow and show code structure
    pass


# Exercise 10: Multi-Step Chain with Routing
# Build a chain that routes to different sub-chains based on input:
# a) If question contains "code" → route to code_chain
# b) If question contains "math" → route to math_chain
# c) Otherwise → route to general_chain
# Use RunnableBranch for conditional routing.
# routing = directing input to different processing paths based on content
# Expected: different handling based on question type

def exercise_10():
    from langchain_core.runnables import RunnableBranch, RunnableLambda
    # Your code here: define 3 chains, create routing logic
    pass


# Exercise 11: Custom Document QA with Sources
# Build a QA system that:
# a) Returns the answer
# b) Also returns the source documents used
# c) Includes confidence indication
# d) Formats output as structured JSON
# This is production-grade RAG with attribution.
# Expected: answer + sources + confidence in structured format

def exercise_11():
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.pydantic_v1 import BaseModel, Field
    # Your code here: chain that returns answer + metadata
    pass


# Exercise 12: Build a Simple Agent Loop (No LangChain Agent)
# Implement a basic agent loop manually to understand what LangChain agents do:
# a) Define available tools as functions
# b) Create a prompt that lists tools and asks LLM to decide
# c) Parse LLM output to determine which tool to call
# d) Call the tool
# e) Feed result back to LLM for final answer
# This demystifies what AgentExecutor does internally.
# Expected: working manual agent that picks and uses tools

def exercise_12():
    # Your code here: implement the agent loop manually
    # This is educational — shows what happens inside AgentExecutor
    # Pseudocode structure:
    # 1. prompt = "You have tools: [search, calculate]. Question: {q}. Which tool?"
    # 2. llm_decision = llm.invoke(prompt)
    # 3. tool_result = call_tool(llm_decision)
    # 4. final_answer = llm.invoke(f"Tool returned: {tool_result}. Answer: ")
    pass


# =============================================================================
# Run all exercises
# =============================================================================

if __name__ == "__main__":
    exercises = [exercise_1, exercise_2, exercise_3, exercise_4,
                 exercise_5, exercise_6, exercise_7, exercise_8,
                 exercise_9, exercise_10, exercise_11, exercise_12]

    for i, ex in enumerate(exercises, 1):
        print(f"\n{'='*60}")
        print(f"Exercise {i}")
        print('='*60)
        try:
            ex()
        except Exception as e:
            print(f"  [Error: {type(e).__name__}: {e}]")
