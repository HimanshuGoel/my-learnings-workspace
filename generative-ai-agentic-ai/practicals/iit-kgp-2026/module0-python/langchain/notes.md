# LangChain — Notes

## What Problem Does This Library Solve?

LangChain provides building blocks for composing LLM-powered applications — chaining together prompts, models, tools, memory, and retrieval into coherent workflows that go beyond single-turn Q&A to multi-step reasoning, RAG pipelines, and autonomous agents.

## Mental Model

Think of LangChain as **Spring Framework for LLM Applications**. Just as Spring gives you IoC containers, middleware, data access, and web layers to build enterprise Java apps, LangChain gives you:
- **Chains** = middleware pipelines (prompt → model → output parser)
- **Retrievers** = data access layer (search your documents)
- **Agents** = controllers with tool-calling capability (model decides what to do)
- **Memory** = session state (conversation history)

Or: **Express.js with middleware** — each step in the chain processes and passes data to the next.

## Where It Fits

```
User Query
    │
    ▼
┌────────────────────────────────────────┐
│            LangChain (Orchestrator)      │  ← you are here
│                                          │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │ Prompts  │→ │  LLM/Chat │→ │ Output │ │
│  │ Templates│  │  Models   │  │ Parser │ │
│  └─────────┘  └──────────┘  └────────┘ │
│                                          │
│  ┌───────────┐  ┌──────────┐            │
│  │ Retrievers │  │  Memory  │            │
│  │ (RAG)     │  │ (History)│            │
│  └───────────┘  └──────────┘            │
│                                          │
│  ┌──────────┐                            │
│  │  Agents  │ ← tools + reasoning        │
│  └──────────┘                            │
└────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────┐
│ External Systems          │
│ • Vector DB (ChromaDB)    │
│ • APIs (search, weather)  │
│ • LLM providers (OpenAI)  │
│ • Files, databases        │
└──────────────────────────┘
```

- **Before LangChain:** Raw API calls to LLMs, manual prompt engineering, no state
- **After LangChain:** Structured applications with retrieval, memory, and tool use
- **Talks to:** OpenAI/HuggingFace (models), ChromaDB/FAISS (vectors), Pydantic (structured output), FastAPI (serving)

## Core Concepts

### 1. LLMs and Chat Models

```python
from langchain_openai import ChatOpenAI
from langchain_community.llms import HuggingFaceHub

# Chat model (recommended — most modern LLMs are chat-based)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Invoke directly
response = llm.invoke("What is machine learning?")
print(response.content)

# With message types (system, human, AI)
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="You are a helpful AI assistant."),
    HumanMessage(content="Explain RAG in one sentence.")
]
response = llm.invoke(messages)
```

### 2. Prompt Templates — Reusable Prompts

```python
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# Simple template
template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}."),
    ("human", "{question}")
])

# Fill template and invoke
prompt = template.invoke({"domain": "machine learning", "question": "What is overfitting?"})
response = llm.invoke(prompt)

# String-based template (for simpler cases)
template = PromptTemplate.from_template(
    "Summarize the following text in {num_sentences} sentences:\n\n{text}"
)
```

### 3. Chains (LCEL) — Composable Pipelines

```python
from langchain_core.output_parsers import StrOutputParser

# LCEL = LangChain Expression Language
# Chain = prompt | model | parser (pipe operator composes them)
chain = template | llm | StrOutputParser()

# Invoke the chain
result = chain.invoke({
    "domain": "AI safety",
    "question": "What are the main risks?"
})

# Chain with multiple steps
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

**Key insight:** LCEL (the `|` pipe syntax) is the modern way to build LangChain apps. It replaces the old `LLMChain` / `SequentialChain` classes.

### 4. RAG — Retrieval-Augmented Generation

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Load documents
loader = TextLoader("document.txt")
documents = loader.load()

# 2. Split into chunks (LLMs have token limits)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 3. Create embeddings and store in vector DB
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 5. RAG chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

rag_prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context:
{context}

Question: {question}
""")

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the refund policy?")
```

### 5. Document Loaders — Get Data In

```python
from langchain_community.document_loaders import (
    TextLoader,           # .txt files
    PyPDFLoader,          # PDF files
    CSVLoader,            # CSV files
    WebBaseLoader,        # Web pages
    DirectoryLoader,      # Entire directories
)

# Load PDF
loader = PyPDFLoader("document.pdf")
pages = loader.load()  # list of Document objects
# Each Document has: .page_content (text) and .metadata (source, page, etc.)
```

### 6. Text Splitters — Chunk Documents

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # max chars per chunk
    chunk_overlap=50,     # overlap between adjacent chunks (preserves context)
    separators=["\n\n", "\n", ". ", " "]  # try splitting at these boundaries
)
chunks = splitter.split_documents(documents)
```

**Why split?** LLMs have token limits (4k-128k). Long documents must be chunked. Overlap ensures context isn't lost at boundaries.

### 7. Output Parsers — Structured Responses

```python
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Define desired output structure
class MovieReview(BaseModel):
    sentiment: str = Field(description="positive or negative")
    confidence: float = Field(description="confidence score 0-1")
    summary: str = Field(description="one sentence summary")

parser = JsonOutputParser(pydantic_object=MovieReview)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract structured info from the review.\n{format_instructions}"),
    ("human", "{review}")
])

chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser
result = chain.invoke({"review": "Amazing movie, loved every scene!"})
# result = {"sentiment": "positive", "confidence": 0.95, "summary": "..."}
```

### 8. Memory — Conversation History

```python
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import MessagesPlaceholder

# Memory stores conversation turns
memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# In a conversation loop, memory accumulates history
# (Modern approach uses RunnableWithMessageHistory)
```

### 9. Agents — Models That Use Tools

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool

# Define tools the agent can use
@tool
def search_web(query: str) -> str:
    """Search the web for current information."""
    # In reality, call a search API
    return f"Search results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

# Create agent
tools = [search_web, calculate]
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Agent decides which tools to call
result = executor.invoke({"input": "What is 15% of 230?"})
```

### 10. LangChain Expression Language (LCEL) Patterns

```python
from langchain_core.runnables import RunnableParallel, RunnableLambda

# Parallel execution
parallel = RunnableParallel(
    summary=summary_chain,
    translation=translation_chain,
    keywords=keyword_chain,
)
results = parallel.invoke({"text": "..."})

# Conditional routing
from langchain_core.runnables import RunnableBranch
branch = RunnableBranch(
    (lambda x: "code" in x["question"], code_chain),
    (lambda x: "math" in x["question"], math_chain),
    default_chain,
)

# Fallback (try A, if fails try B)
chain_with_fallback = primary_chain.with_fallbacks([backup_chain])
```

## Key Functions/Methods

### Core Components

| Component | Purpose |
|-----------|---------|
| `ChatOpenAI(model, temperature)` | Load a chat model |
| `ChatPromptTemplate.from_messages(...)` | Create prompt template |
| `StrOutputParser()` | Parse LLM output as string |
| `JsonOutputParser(pydantic_object)` | Parse as structured JSON |
| `template \| llm \| parser` | LCEL chain (pipe syntax) |

### RAG Components

| Component | Purpose |
|-----------|---------|
| `TextLoader / PyPDFLoader` | Load documents |
| `RecursiveCharacterTextSplitter` | Chunk documents |
| `OpenAIEmbeddings / HuggingFaceEmbeddings` | Create embeddings |
| `Chroma.from_documents(chunks, embeddings)` | Store in vector DB |
| `vectorstore.as_retriever(k=3)` | Create retriever |

### Agent Components

| Component | Purpose |
|-----------|---------|
| `@tool` decorator | Define a tool |
| `create_tool_calling_agent(llm, tools, prompt)` | Create agent |
| `AgentExecutor(agent, tools)` | Run agent loop |

## Common Patterns

### Basic Q&A Chain

```python
chain = prompt | llm | StrOutputParser()
answer = chain.invoke({"question": "What is AI?"})
```

### RAG Pipeline (Complete)

```python
# Load → Split → Embed → Store → Retrieve → Generate
docs = loader.load()
chunks = splitter.split_documents(docs)
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(k=3)
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | parser
```

### Conversational RAG (with Memory)

```python
# RAG + conversation history = chatbot over your docs
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

combine_docs_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
```

## AI/ML Connection

- **Where in the AI pipeline:** LangChain is the application layer — it orchestrates models, data retrieval, tools, and memory into complete AI products. It doesn't train models; it uses them.

- **Concrete example — RAG (Module 2):** Load company docs → chunk → embed with sentence-transformers → store in ChromaDB → retrieve relevant chunks for user query → generate answer with context. This entire flow is LangChain.

- **Concrete example — Agents (Module 4):** Build an AI assistant that can search the web, query databases, call APIs, and reason about results. LangChain provides the agent framework for this.

- **Concrete example — Structured Output:** Force an LLM to return JSON matching a Pydantic schema (Module 2 — structured retrieval results, Module 5 — API responses).

- **Which IIT KGP modules use this:** Module 2 (RAG pipelines), Module 4 (agentic AI, tool-calling, multi-step reasoning), Module 5 (production AI application architecture).

- **What breaks without it:** You'd manually handle prompt construction, tool routing, memory management, and retrieval orchestration — hundreds of lines of boilerplate for each application.

- **Concrete example — Capstone:** Your Module 5 capstone will likely be a RAG or agentic application. LangChain is the standard framework for building these.

## Common Mistakes

1. **Using old LangChain syntax** — `LLMChain`, `SequentialChain`, `ConversationChain` are deprecated. Use LCEL (`|` pipe syntax) for everything new.

2. **Not chunking documents properly** — too large chunks exceed context windows; too small chunks lose meaning. Start with 500-1000 chars, 50-100 overlap.

3. **Ignoring metadata in retrieval** — documents carry metadata (source, page, date). Filter on metadata for better results.

4. **Agent loops** — agents can get stuck calling tools repeatedly. Set `max_iterations` in AgentExecutor.

5. **Not handling rate limits** — LLM APIs have rate limits. Add retry logic or use `with_retry()` on chains.

6. **Over-engineering** — not everything needs LangChain. A simple `openai.chat.completions.create()` call might be enough for basic tasks.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Simple single-turn LLM call | Direct OpenAI/Anthropic SDK |
| Training or fine-tuning models | HuggingFace Transformers + Trainer |
| Very latency-sensitive serving | Custom code with vLLM/ONNX |
| Simple rule-based routing | If-else logic |
| Static FAQ lookup | Vector DB direct query |

## Ready to Move On?

- ☐ I can build a chain with LCEL (prompt | llm | parser)
- ☐ I understand the RAG pipeline (load → split → embed → retrieve → generate)
- ☐ I can create a simple agent with tools
- ☐ I know the difference between chains, retrievers, and agents
- ☐ I can use output parsers to get structured JSON from an LLM

Once all checked → move to **ChromaDB** (vector storage) or **LlamaIndex** (alternative RAG framework).
