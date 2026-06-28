# RAG (Retrieval-Augmented Generation)

## What Is This?

RAG is an architecture that combines information retrieval (searching your documents) with text generation (LLM answering) — so the model answers questions grounded in YOUR data rather than relying solely on what it learned during pre-training.

## Why Does It Exist?

**The Problem:** LLMs have three fundamental limitations:
1. **Knowledge cutoff** — don't know anything after their training date
2. **No access to private data** — haven't seen your company docs, policies, codebase
3. **Hallucination** — confidently generate false information when they don't know

**The Solution:** Before asking the LLM to answer, FIRST retrieve relevant documents from your data. Then pass those documents as context with the question. The LLM generates an answer grounded in the retrieved evidence.

RAG = **give the model an open-book exam** instead of asking it to answer from memory.

## Mental Model

Think of RAG as **a developer answering a question using documentation**. Instead of guessing from memory (hallucination risk), they:
1. Search the docs for relevant sections
2. Read those sections
3. Formulate an answer based on what they found
4. Cite their sources

Or: like **Stack Overflow for LLMs**. The model searches for relevant Q&As first, then synthesizes an answer. Without the search step, it's just guessing.

## How It Works

### The RAG Pipeline

```
User Question
    │
    ▼
┌─────────────────┐
│ 1. EMBED query   │ → convert question to a vector
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. RETRIEVE      │ → find top-K similar document chunks in vector DB
│    (ChromaDB)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. AUGMENT       │ → insert retrieved chunks into prompt as context
│    prompt        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. GENERATE      │ → LLM answers based ONLY on provided context
│    (LLM)         │
└────────┬────────┘
         │
         ▼
    Answer + Sources
```

### Ingestion Phase (Done Once)

1. **Load documents** (PDFs, web pages, docs, databases)
2. **Chunk** them into 500-1000 token pieces (with overlap)
3. **Embed** each chunk (sentence-transformers → 384/768-dim vectors)
4. **Store** embeddings + text + metadata in vector database (ChromaDB)

### Query Phase (Every Question)

1. **Embed the question** (same model used for documents)
2. **Search** vector DB for top-K similar chunks (cosine similarity)
3. **Build prompt**: "Answer based on this context: {chunks}\n\nQuestion: {question}"
4. **Generate**: LLM produces answer grounded in retrieved context
5. **Return** answer + source documents (for attribution/trust)

### The RAG Prompt Pattern

```
System: You are a helpful assistant. Answer ONLY based on the provided context.
If the context doesn't contain the answer, say "I don't have that information."

Context:
{retrieved_chunk_1}
{retrieved_chunk_2}
{retrieved_chunk_3}

Question: {user_question}

Answer:
```

## Key Design Decisions

| Decision | Options | Trade-off |
|----------|---------|-----------|
| Chunk size | 256 / 512 / 1024 tokens | Smaller = more precise retrieval, larger = more context per chunk |
| Chunk overlap | 0 / 50 / 100 tokens | More overlap = preserves context at boundaries, costs more storage |
| Top-K | 3 / 5 / 10 chunks | More = less risk of missing info, but more noise and cost |
| Embedding model | MiniLM (384d) / mpnet (768d) / OpenAI (1536d) | Larger = better quality, slower + more expensive |
| Retrieval strategy | Vector only / Hybrid (vector + keyword) / Re-ranking | More stages = better precision, more complexity |

## RAG vs Fine-Tuning

| Factor | RAG | Fine-Tuning |
|--------|-----|-------------|
| When data changes | Just re-index (minutes) | Retrain (hours/days) |
| Source attribution | Built-in (show which docs) | Not possible |
| Hallucination risk | Lower (grounded in docs) | Higher (model may still hallucinate) |
| Latency | Higher (retrieval step adds time) | Lower (direct answer) |
| Private data handling | Data stays in your DB | Data baked into model weights |
| Cost model | Per-query retrieval + generation | One-time training + cheap inference |

**Rule of thumb:** Use RAG when data changes frequently, attribution matters, or you can't afford fine-tuning. Use fine-tuning when you need consistent format/style and have stable training data.

## Where You'll Use This

| Module | How RAG Applies |
|--------|----------------|
| Module 2 | THE entire module — build RAG pipelines with LangChain/LlamaIndex |
| Module 4 | Agents use RAG to access knowledge bases as tools |
| Module 5 | Capstone likely includes a RAG component |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "RAG = just copying text from documents" | The LLM synthesizes, summarizes, and reasons over retrieved context |
| "Bigger chunks = better" | Too big = noise (irrelevant content dilutes signal). 500 tokens is a good start. |
| "RAG eliminates hallucination" | Reduces it significantly but doesn't eliminate it. Model can still misinterpret context. |
| "RAG replaces fine-tuning" | They solve different problems. RAG for knowledge access, fine-tuning for behavior change. |
| "One retrieval step is enough" | Production systems often re-rank, filter, and multi-step retrieve for quality. |

## Connection to Other Topics

- **Builds on:** Embeddings (retrieval uses similarity search), LLMs (generation), Prompting (RAG prompt design)
- **Uses:** ChromaDB (vector storage), LangChain/LlamaIndex (orchestration), Pydantic (structured output)
- **Enables:** Agents (RAG as a tool), Production apps (FastAPI serving RAG endpoints)

## Ready to Move On?

- ☐ I can explain the RAG pipeline: embed → retrieve → augment prompt → generate
- ☐ I understand why RAG exists (knowledge cutoff, private data, reduce hallucination)
- ☐ I know key design decisions (chunk size, top-k, embedding model)
- ☐ I can articulate when to use RAG vs fine-tuning

Next → **Agents** (LLMs that use tools and reason in multi-step loops)
