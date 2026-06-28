# LangChain — Cheatsheet

## Install

```bash
pip install langchain langchain-openai langchain-community chromadb
```

## Imports (Common)

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.messages import SystemMessage, HumanMessage
```

---

## Models

```python
# Chat model (recommended)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Direct invoke
response = llm.invoke("Hello")
print(response.content)

# With messages
from langchain_core.messages import SystemMessage, HumanMessage
response = llm.invoke([
    SystemMessage(content="You are helpful."),
    HumanMessage(content="What is AI?")
])
```

---

## Prompt Templates

```python
# Chat template (recommended)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}."),
    ("human", "{question}")
])

# String template
prompt = PromptTemplate.from_template("Summarize: {text}")

# Invoke template
formatted = prompt.invoke({"domain": "AI", "question": "What is RAG?"})
```

---

## Chains (LCEL — Pipe Syntax)

```python
# Basic chain
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"domain": "AI", "question": "What is RAG?"})

# Multi-step
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Parallel
parallel = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain,
)

# Batch invoke
results = chain.batch([{"q": "A"}, {"q": "B"}])

# Stream
for chunk in chain.stream({"question": "explain"}):
    print(chunk, end="")
```

---

## RAG Pipeline (Complete)

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. Load
docs = PyPDFLoader("doc.pdf").load()

# 2. Split
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. Embed + Store
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())

# 4. Retrieve
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 5. Generate
rag_prompt = ChatPromptTemplate.from_template("""
Answer based on context only:
{context}

Question: {question}
""")

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)
answer = rag_chain.invoke("What is the return policy?")
```

---

## Document Loaders

```python
from langchain_community.document_loaders import (
    TextLoader,          # .txt
    PyPDFLoader,         # .pdf
    CSVLoader,           # .csv
    WebBaseLoader,       # web pages
    DirectoryLoader,     # entire folder
    JSONLoader,          # .json
)
docs = PyPDFLoader("file.pdf").load()
# → [Document(page_content="...", metadata={source, page})]
```

---

## Text Splitters

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_documents(docs)
```

---

## Output Parsers

```python
# String output
StrOutputParser()

# JSON output (with Pydantic schema)
from langchain_core.pydantic_v1 import BaseModel, Field

class Answer(BaseModel):
    response: str = Field(description="the answer")
    confidence: float = Field(description="0-1 confidence")

parser = JsonOutputParser(pydantic_object=Answer)
chain = prompt.partial(
    format_instructions=parser.get_format_instructions()
) | llm | parser
```

---

## Agents & Tools

```python
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

@tool
def calculator(expr: str) -> str:
    """Evaluate math."""
    return str(eval(expr))

tools = [search, calculator]
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful. Use tools when needed."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)
result = executor.invoke({"input": "What is 15% of 340?"})
```

---

## Memory (Conversation History)

```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}
def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain, get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
result = chain_with_history.invoke(
    {"input": "Hi!"},
    config={"configurable": {"session_id": "user1"}}
)
```

---

## Embeddings

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# OpenAI
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# HuggingFace (local, free)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Use
vector = embeddings.embed_query("Hello world")
vectors = embeddings.embed_documents(["doc1", "doc2"])
```

---

## Streaming

```python
# Stream output token by token
for chunk in chain.stream({"question": "Explain AI"}):
    print(chunk, end="", flush=True)

# Async streaming
async for chunk in chain.astream({"question": "Explain AI"}):
    print(chunk, end="")
```

---

## Quick Reference Links

- Docs: https://python.langchain.com/docs/
- LCEL: https://python.langchain.com/docs/expression_language/
- Hub (prompts): https://smith.langchain.com/hub
