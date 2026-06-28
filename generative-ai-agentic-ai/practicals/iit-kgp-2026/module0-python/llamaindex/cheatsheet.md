# LlamaIndex — Cheatsheet

## Install

```bash
pip install llama-index llama-index-llms-openai llama-index-embeddings-openai
pip install llama-index-vector-stores-chroma  # for ChromaDB backend
```

## Import

```python
from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader, Document,
    Settings, StorageContext, load_index_from_storage
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
```

---

## Global Settings

```python
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.chunk_size = 512
Settings.chunk_overlap = 50

# Or use HuggingFace (local, free)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
```

---

## Load Documents

```python
# Directory (auto-detects PDF, txt, docx, etc.)
docs = SimpleDirectoryReader("./my_data").load_data()
docs = SimpleDirectoryReader("./data", required_exts=[".pdf", ".txt"]).load_data()

# Manual
doc = Document(text="content here", metadata={"source": "manual"})

# Single file
docs = SimpleDirectoryReader(input_files=["file.pdf"]).load_data()
```

---

## Create Index

```python
# VectorStoreIndex (default — best for RAG)
index = VectorStoreIndex.from_documents(docs)

# With custom chunking
from llama_index.core.node_parser import SentenceSplitter
index = VectorStoreIndex.from_documents(
    docs, transformations=[SentenceSplitter(chunk_size=256, chunk_overlap=30)]
)

# Other index types
from llama_index.core import SummaryIndex, TreeIndex
summary_index = SummaryIndex.from_documents(docs)
tree_index = TreeIndex.from_documents(docs)
```

---

## Query Engine

```python
# Basic
engine = index.as_query_engine()
response = engine.query("What is X?")
print(response.response)          # answer text
print(response.source_nodes)      # retrieved chunks

# Configured
engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact",       # compact | refine | tree_summarize | no_text
    streaming=True,
)

# Streaming
streaming_response = engine.query("Explain RAG")
for text in streaming_response.response_gen:
    print(text, end="")
```

---

## Chat Engine

```python
# Conversational (with memory)
chat_engine = index.as_chat_engine(chat_mode="condense_question")
# Modes: "condense_question", "context", "simple"

r1 = chat_engine.chat("What is RAG?")
r2 = chat_engine.chat("How does it handle long documents?")  # follows context
chat_engine.reset()  # clear history
```

---

## Persistence

```python
# Save
index.storage_context.persist(persist_dir="./storage")

# Load (no re-embedding!)
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

---

## Custom Vector Store (ChromaDB)

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("docs")
vector_store = ChromaVectorStore(chroma_collection=collection)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
```

---

## Node Parsers (Chunking)

```python
from llama_index.core.node_parser import (
    SentenceSplitter,        # split by sentence boundaries
    TokenTextSplitter,       # split by token count
    SemanticSplitterNodeParser,  # split by semantic similarity
)

# Sentence-based (most common)
parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = parser.get_nodes_from_documents(docs)
```

---

## Structured Output

```python
from pydantic import BaseModel, Field

class Answer(BaseModel):
    response: str = Field(description="the answer")
    confidence: float = Field(description="0-1 confidence")

engine = index.as_query_engine(output_cls=Answer)
result = engine.query("What is the policy?")  # returns Answer object
```

---

## Sub-Question Query Engine

```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata

tools = [
    QueryEngineTool(query_engine=engine1,
        metadata=ToolMetadata(name="finance", description="Financial data")),
    QueryEngineTool(query_engine=engine2,
        metadata=ToolMetadata(name="product", description="Product docs")),
]
sub_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=tools)
response = sub_engine.query("Compare revenue growth with product launches")
```

---

## Response Modes

| Mode | Behavior | Best For |
|------|----------|----------|
| `compact` | Stuff all context in one prompt | Small retrievals (default) |
| `refine` | Iterate over chunks, refine answer | Many chunks, detailed answers |
| `tree_summarize` | Hierarchical summarization | Very long contexts |
| `no_text` | Return nodes only (no LLM call) | When you just want retrieval |

---

## Minimal RAG (5 Lines)

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
docs = SimpleDirectoryReader("./docs").load_data()
index = VectorStoreIndex.from_documents(docs)
engine = index.as_query_engine()
print(engine.query("What is the return policy?"))
```

---

## Quick Reference Links

- Docs: https://docs.llamaindex.ai/
- LlamaHub (readers): https://llamahub.ai/
- Starter tutorial: https://docs.llamaindex.ai/en/stable/getting_started/starter_example/
