# RAG Pipeline Architecture

## The Problem You're Solving

You have individual components (chunker, embedder, vector store, retriever, LLM) but no coherent end-to-end system. Without intentional architecture, you get spaghetti notebooks that can't be tested, monitored, or evolved. You need a composable pipeline with clear boundaries between stages.

## Options Available

| Architecture | When to Use | Pros | Cons |
|-------------|-------------|------|------|
| Simple sequential (retrieve → generate) | Single-domain QA, small corpus | Easy to build and debug | No fallback, limited quality levers |
| Retrieve → Rerank → Generate | Production QA with precision needs | Better answer quality | Added latency from reranker |
| Multi-index routing | Multiple document types/domains | Right content for right queries | Router logic complexity |
| Iterative refinement (query → retrieve → reflect → re-query) | Complex questions, research tasks | Higher answer quality | 2-5x latency, more LLM calls |
| Map-reduce (retrieve → summarize each → combine) | Long-form synthesis, report generation | Handles many docs | Expensive, loses cross-doc relationships |
| Parent-child retrieval | Need precision + context | Best of both worlds | Complex indexing setup |
| Conversational RAG (with memory) | Chatbot interfaces | Context-aware follow-ups | Memory management complexity |

## Recommended Approach

**Start with: Retrieve → Rerank → Generate (with metadata filtering and conversation memory). This covers 80% of production use cases.**

Why: It's the minimum viable production architecture. Simple sequential lacks quality. Agentic is overkill for most initial deployments. This middle ground gives you quality levers (re-ranking, filtering) without orchestration complexity.

## Step-by-Step Implementation

### 1. Define the Pipeline Stages

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐    ┌────────────┐
│  Query      │ →  │  Retrieval   │ →  │  Reranking  │ →  │  Augmentation│ →  │  Generation│
│  Processing │    │  (Vector +   │    │  (Cross-    │    │  (Prompt     │    │  (LLM Call)│
│             │    │   BM25)      │    │   encoder)  │    │   Assembly)  │    │            │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘    └────────────┘
       │                   │                   │                   │                  │
  - Classify intent   - Top-20 candidates  - Top-3 final     - System prompt    - Structured
  - Expand query      - Metadata filter    - Score threshold  - Context inject   - Streaming
  - Route to index    - Hybrid search      - Min-score gate   - Few-shot         - Validation
```

### 2. Query Processing Stage

```python
from enum import Enum
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class QueryIntent(str, Enum):
    FACTUAL = "factual"          # "What is the rate limit?"
    HOWTO = "howto"              # "How do I set up OAuth?"
    COMPARISON = "comparison"    # "Difference between v1 and v2?"
    TROUBLESHOOT = "troubleshoot"  # "Why is auth failing?"

class ProcessedQuery(BaseModel):
    original: str
    intent: QueryIntent
    expanded_queries: list[str]
    target_collection: str
    metadata_filters: dict

def process_query(query: str, llm: ChatOpenAI) -> ProcessedQuery:
    """Classify, expand, and route the query."""
    # Intent classification
    intent = classify_intent(query, llm)
    
    # Query expansion (generate variants for multi-query retrieval)
    expanded = expand_query(query, llm, n_variants=3)
    
    # Route to appropriate collection
    collection = route_to_collection(query, intent)
    
    # Determine metadata filters based on query
    filters = extract_filters(query)  # e.g., version, date range
    
    return ProcessedQuery(
        original=query,
        intent=intent,
        expanded_queries=expanded,
        target_collection=collection,
        metadata_filters=filters,
    )
```

### 3. Retrieval Stage

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_chroma import Chroma

class RetrievalStage:
    def __init__(self, vectorstore: Chroma, documents: list):
        self.vector_retriever = vectorstore.as_retriever(
            search_kwargs={"k": 15}
        )
        self.bm25_retriever = BM25Retriever.from_documents(documents, k=15)
        self.hybrid_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.vector_retriever],
            weights=[0.3, 0.7],
        )
    
    def retrieve(self, processed_query: ProcessedQuery) -> list:
        """Retrieve candidates using hybrid search + filters."""
        # Apply metadata filter
        self.vector_retriever.search_kwargs["filter"] = processed_query.metadata_filters
        
        # Multi-query: retrieve for each expanded query, union results
        all_docs = []
        for query_variant in processed_query.expanded_queries:
            docs = self.hybrid_retriever.invoke(query_variant)
            all_docs.extend(docs)
        
        # Deduplicate by content hash
        seen = set()
        unique_docs = []
        for doc in all_docs:
            content_hash = hash(doc.page_content)
            if content_hash not in seen:
                seen.add(content_hash)
                unique_docs.append(doc)
        
        return unique_docs[:20]  # Cap at 20 for reranker
```

### 4. Reranking Stage

```python
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

class RerankingStage:
    def __init__(self, top_n: int = 3, min_score: float = 0.3):
        self.model = HuggingFaceCrossEncoder(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
        )
        self.top_n = top_n
        self.min_score = min_score
    
    def rerank(self, query: str, documents: list) -> list:
        """Rerank and filter by minimum relevance score."""
        pairs = [(query, doc.page_content) for doc in documents]
        scores = self.model.predict(pairs)
        
        # Pair scores with docs, sort descending
        scored_docs = sorted(
            zip(scores, documents), key=lambda x: x[0], reverse=True
        )
        
        # Apply min score threshold and top_n
        filtered = [
            (score, doc) for score, doc in scored_docs
            if score >= self.min_score
        ][:self.top_n]
        
        if not filtered:
            # Fallback: return top-1 even if below threshold
            return [scored_docs[0][1]] if scored_docs else []
        
        return [doc for _, doc in filtered]
```

### 5. Augmentation Stage (Prompt Assembly)

```python
from langchain.prompts import ChatPromptTemplate

class AugmentationStage:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._system_prompt()),
            ("human", self._user_template()),
        ])
    
    def _system_prompt(self) -> str:
        return """You are a technical documentation assistant.
Rules:
1. Answer ONLY based on the provided context
2. If context doesn't contain the answer, say "I couldn't find this in the documentation"
3. Cite sources using [Source: filename] format
4. Be concise — aim for 2-4 sentences unless asked for detail"""
    
    def _user_template(self) -> str:
        return """Context:
{context}

---
Question: {question}

Provide a clear, cited answer based on the context above."""
    
    def build_prompt(self, query: str, documents: list) -> str:
        """Assemble the final prompt with retrieved context."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "unknown")
            context_parts.append(f"[{i}] (Source: {source})\n{doc.page_content}")
        
        context = "\n\n".join(context_parts)
        return self.prompt.format_messages(context=context, question=query)
```

### 6. Generation Stage

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class RAGResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: str  # "high", "medium", "low"

class GenerationStage:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
    
    def generate(self, messages) -> RAGResponse:
        """Generate answer from augmented prompt."""
        response = self.llm.invoke(messages)
        
        # Parse response into structured format
        return self._parse_response(response.content)
    
    async def generate_stream(self, messages):
        """Stream response tokens for low-latency UX."""
        async for chunk in self.llm.astream(messages):
            yield chunk.content
```

### 7. Full Pipeline Orchestration

```python
class RAGPipeline:
    def __init__(self, vectorstore, documents):
        self.query_processor = QueryProcessor()
        self.retrieval = RetrievalStage(vectorstore, documents)
        self.reranking = RerankingStage(top_n=3, min_score=0.3)
        self.augmentation = AugmentationStage()
        self.generation = GenerationStage()
    
    def run(self, user_query: str) -> RAGResponse:
        """Execute the full RAG pipeline."""
        # Stage 1: Process query
        processed = self.query_processor.process(user_query)
        
        # Stage 2: Retrieve candidates
        candidates = self.retrieval.retrieve(processed)
        
        # Stage 3: Rerank
        top_docs = self.reranking.rerank(processed.original, candidates)
        
        # Stage 4: Build prompt
        messages = self.augmentation.build_prompt(processed.original, top_docs)
        
        # Stage 5: Generate
        response = self.generation.generate(messages)
        
        return response
    
    def run_with_tracing(self, user_query: str) -> dict:
        """Execute with full observability for debugging."""
        trace = {"query": user_query, "stages": {}}
        
        import time
        start = time.time()
        
        processed = self.query_processor.process(user_query)
        trace["stages"]["query_processing"] = {
            "intent": processed.intent,
            "expanded_queries": processed.expanded_queries,
            "time_ms": (time.time() - start) * 1000,
        }
        
        t = time.time()
        candidates = self.retrieval.retrieve(processed)
        trace["stages"]["retrieval"] = {
            "candidates_count": len(candidates),
            "time_ms": (time.time() - t) * 1000,
        }
        
        t = time.time()
        top_docs = self.reranking.rerank(processed.original, candidates)
        trace["stages"]["reranking"] = {
            "final_count": len(top_docs),
            "time_ms": (time.time() - t) * 1000,
        }
        
        t = time.time()
        messages = self.augmentation.build_prompt(processed.original, top_docs)
        response = self.generation.generate(messages)
        trace["stages"]["generation"] = {
            "answer_length": len(response.answer),
            "time_ms": (time.time() - t) * 1000,
        }
        
        trace["total_time_ms"] = (time.time() - start) * 1000
        trace["response"] = response
        
        return trace
```

### 8. Conversational RAG (With Memory)

```python
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

class ConversationalRAG:
    def __init__(self, vectorstore, llm):
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=5,  # keep last 5 turns
        )
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
            memory=self.memory,
            return_source_documents=True,
        )
    
    def chat(self, message: str) -> dict:
        """Process a conversational turn with context."""
        result = self.chain.invoke({"question": message})
        return {
            "answer": result["answer"],
            "sources": [doc.metadata["source"] for doc in result["source_documents"]],
        }
```

## Configuration Checklist

| Component | Recommended Config | Why |
|-----------|-------------------|-----|
| Query expansion | 3 variants via gpt-4o-mini | Covers rephrasing gaps, low cost |
| Retrieval top-K | 15-20 initial candidates | Over-retrieve for reranker to filter |
| Hybrid weights | 0.3 BM25 / 0.7 vector | Semantic dominates, keywords catch exact matches |
| Reranker | cross-encoder/ms-marco-MiniLM-L-6-v2 | Best speed/quality ratio |
| Reranker top_n | 3 (factual), 5 (howto/synthesis) | More context for complex queries |
| LLM model | gpt-4o-mini (cost), gpt-4o (quality) | 4o-mini for most QA, 4o for synthesis |
| Temperature | 0.0 for factual, 0.3 for synthesis | Determinism for facts, creativity for summaries |
| Conversation memory | Last 5 turns | Enough context without token bloat |
| Streaming | Always for user-facing apps | Perceived latency reduction |

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Pipeline works in notebook, breaks in production | Stateful components (in-memory BM25) | Externalize state, use proper vector DB |
| Answers are hallucinated despite good retrieval | Context not reaching LLM (prompt too long, truncated) | Check actual token count, reduce context if needed |
| Conversation loses context after 3-4 turns | Memory buffer too small or not connected | Verify memory_key matches, increase window |
| Latency > 5s | Reranker + LLM generation stacking | Profile each stage, parallelize where possible |
| Inconsistent answer quality | No query routing — same pipeline for all intents | Add intent-based routing (factual vs synthesis) |
| Empty results occasionally | Metadata filter too strict + no fallback | Add fallback: if filtered returns 0, retry without filter |
| Sources cited don't match answer | LLM generating fake citations | Validate citations post-generation against actual sources |

## Production Considerations

### Latency Breakdown (Typical)

| Stage | Latency | Notes |
|-------|---------|-------|
| Query processing | 200-500ms | LLM call for intent + expansion |
| Retrieval | 50-200ms | Vector search + BM25 |
| Reranking | 50-200ms | Cross-encoder on 20 candidates |
| Prompt assembly | < 10ms | String operations |
| Generation | 500-3000ms | LLM inference (varies by model/length) |
| **Total** | **800ms - 4s** | Streaming hides generation latency |

### Cost Per Query

| Component | Cost | Notes |
|-----------|------|-------|
| Query expansion (gpt-4o-mini) | ~$0.0001 | ~200 input + 300 output tokens |
| Embedding (text-embedding-3-small) | ~$0.000001 | Single query embedding |
| Reranking | Free | Local cross-encoder |
| Generation (gpt-4o-mini) | ~$0.0005 | ~1000 input + 300 output tokens |
| **Total per query** | **~$0.0006** | At 10K queries/day = ~$6/day |

### Observability
- Log every pipeline trace (stages, latencies, result counts)
- Track: queries per second, latency p50/p95, error rate, empty results rate
- Alert on: latency > 2x baseline, error rate > 1%, empty results > 5%

## Evaluation Criteria

| Metric | How to Measure | Target |
|--------|----------------|--------|
| End-to-end latency | Time from query to first streamed token | < 2s p95 |
| Answer faithfulness | RAGAS faithfulness score | > 0.90 |
| Answer relevancy | RAGAS answer relevancy | > 0.85 |
| Context utilization | % of retrieved context actually used in answer | > 60% |
| Pipeline success rate | % of queries that produce valid answer | > 98% |
| Cost per query | Sum of all API calls | < $0.001 |

## Ready to Ship? — Checklist

- [ ] All 5 stages implemented and individually testable
- [ ] Pipeline traceable end-to-end (every stage logs inputs/outputs)
- [ ] Fallback handling: empty retrieval, reranker failure, LLM timeout
- [ ] Streaming enabled for user-facing responses
- [ ] Conversation memory working across turns
- [ ] Cost per query estimated and within budget
- [ ] Latency within acceptable range (< 2s to first token)
- [ ] Error handling: graceful degradation, not hard failures
- [ ] Integration tests: known query → expected behavior verified
- [ ] Monitoring dashboard: latency, error rate, cost, query volume
