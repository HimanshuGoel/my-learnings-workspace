"""
=============================================================================
MINI PROJECT: RAG-Powered Documentation Assistant
=============================================================================

PROBLEM STATEMENT:
Build a documentation assistant that answers questions about a codebase or
product by retrieving relevant doc sections and generating grounded answers.

WHAT YOU'LL BUILD:
- Document ingestion pipeline (load, split, embed, store)
- Semantic retrieval with ChromaDB
- RAG chain that generates answers grounded in retrieved context
- Source attribution (which docs were used)
- Conversation follow-up capability

WHY THIS MATTERS:
This is THE project for Module 2 (RAG). Every enterprise AI chatbot
(Notion AI, GitHub Copilot Chat, internal doc bots) uses this exact pattern.
Your capstone (Module 5) will likely include a RAG component.

ESTIMATED TIME: 45-60 minutes

SKILLS PRACTICED:
- Document loading and chunking strategies
- Embedding creation and vector storage
- Retriever configuration (k, filters)
- LCEL chain composition
- Structured output with sources

SETUP:
  pip install langchain langchain-openai langchain-community chromadb
  export OPENAI_API_KEY=your-key
  (Or use HuggingFace embeddings + FakeLLM for testing without API key)

RULES:
- Use LCEL (pipe syntax) for all chains
- Include source attribution in responses
- Handle "I don't know" gracefully when no relevant docs found
- Follow the TODOs in order
=============================================================================
"""

from langchain_core.documents import Document


# =============================================================================
# SETUP: Simulated documentation (in real use, load from files)
# =============================================================================

DOCUMENTATION = [
    Document(
        page_content="""
        Getting Started with Our API
        To authenticate, include your API key in the Authorization header.
        All requests must use HTTPS. Rate limit is 100 requests per minute.
        Base URL: https://api.example.com/v2
        """,
        metadata={"source": "api-guide.md", "section": "authentication"}
    ),
    Document(
        page_content="""
        Error Handling
        The API returns standard HTTP status codes. 400 = bad request,
        401 = unauthorized, 403 = forbidden, 404 = not found, 429 = rate limited,
        500 = server error. All errors include a JSON body with 'error' and 'message' fields.
        Implement exponential backoff for 429 responses.
        """,
        metadata={"source": "api-guide.md", "section": "errors"}
    ),
    Document(
        page_content="""
        User Endpoints
        GET /users - List all users (paginated, 50 per page)
        GET /users/{id} - Get single user
        POST /users - Create user (requires name, email)
        PUT /users/{id} - Update user
        DELETE /users/{id} - Delete user (admin only)
        """,
        metadata={"source": "api-guide.md", "section": "users"}
    ),
    Document(
        page_content="""
        Webhooks
        Configure webhooks to receive real-time notifications.
        Supported events: user.created, user.updated, order.completed, payment.failed.
        Webhook payloads are signed with HMAC-SHA256. Verify the signature header.
        Retry policy: 3 attempts with exponential backoff (1s, 5s, 30s).
        """,
        metadata={"source": "api-guide.md", "section": "webhooks"}
    ),
    Document(
        page_content="""
        Pagination
        All list endpoints support cursor-based pagination.
        Parameters: limit (default 50, max 100), cursor (opaque string).
        Response includes 'next_cursor' field. When null, no more pages.
        Do NOT use offset-based pagination for large datasets.
        """,
        metadata={"source": "api-guide.md", "section": "pagination"}
    ),
    Document(
        page_content="""
        SDKs and Libraries
        Official SDKs available for Python, JavaScript, Go, and Ruby.
        Python: pip install example-sdk
        JavaScript: npm install @example/sdk
        All SDKs handle authentication, retries, and pagination automatically.
        """,
        metadata={"source": "api-guide.md", "section": "sdks"}
    ),
    Document(
        page_content="""
        Rate Limiting
        Default rate limit is 100 requests per minute per API key.
        Enterprise plans get 1000 requests/minute.
        When rate limited, the response includes Retry-After header.
        Best practice: implement client-side rate limiting to stay under limits.
        """,
        metadata={"source": "api-guide.md", "section": "rate-limiting"}
    ),
    Document(
        page_content="""
        Data Export
        Use POST /exports to create an export job. Supports CSV and JSON formats.
        Large exports are processed asynchronously. Poll GET /exports/{id} for status.
        Export files are available for download for 24 hours after completion.
        Maximum export size: 10GB.
        """,
        metadata={"source": "api-guide.md", "section": "exports"}
    ),
]


# =============================================================================
# TODO 1: Document Splitting
# =============================================================================
# Split the documentation into smaller chunks for better retrieval.
# Use RecursiveCharacterTextSplitter with:
#   - chunk_size=200 (small for precise retrieval)
#   - chunk_overlap=30 (preserve context at boundaries)
# Return the list of chunks.

def split_documents(documents):
    """Split documents into retrieval-optimized chunks."""
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    # TODO: Create splitter
    # TODO: Split documents
    # TODO: Print stats (num original docs vs num chunks)
    # TODO: Return chunks
    pass


# =============================================================================
# TODO 2: Create Vector Store
# =============================================================================
# Embed chunks and store in ChromaDB:
#   - Use HuggingFaceEmbeddings (free, local) or OpenAIEmbeddings
#   - Create a Chroma collection from the chunks
# Return the vectorstore.

def create_vectorstore(chunks):
    """Create ChromaDB vector store from document chunks."""
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    # TODO: Initialize embedding model
    # TODO: Create Chroma from documents
    # TODO: Return vectorstore
    pass


# =============================================================================
# TODO 3: Create Retriever
# =============================================================================
# Configure the retriever:
#   - Return top 3 most relevant chunks
#   - (Optional) Add metadata filtering capability
# Return the retriever.

def create_retriever(vectorstore):
    """Create a retriever from the vector store."""
    # TODO: Create retriever with search_kwargs={"k": 3}
    # TODO: Test with a sample query, print results
    # TODO: Return retriever
    pass


# =============================================================================
# TODO 4: Build RAG Prompt
# =============================================================================
# Create a prompt template for RAG:
#   - System: "You are a documentation assistant. Answer based ONLY on the
#     provided context. If the context doesn't contain the answer, say
#     'I don't have information about that in the documentation.'"
#   - Include {context} and {question} variables
# Return the prompt template.

def build_rag_prompt():
    """Create the RAG prompt template."""
    from langchain_core.prompts import ChatPromptTemplate
    # TODO: Create prompt with system instruction + context + question
    pass


# =============================================================================
# TODO 5: Build RAG Chain
# =============================================================================
# Compose the full RAG chain using LCEL:
#   retriever → format_docs → prompt → llm → parser
# Include source tracking (which docs were retrieved).
# Return the chain.

def build_rag_chain(retriever, llm):
    """Build the complete RAG chain."""
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough, RunnableParallel
    # TODO: Define format_docs function
    # TODO: Build chain with LCEL pipe syntax
    # TODO: Return chain
    pass


# =============================================================================
# TODO 6: Query with Source Attribution
# =============================================================================
# Create a wrapper that:
#   a) Runs the RAG chain
#   b) Also returns the source documents that were retrieved
#   c) Formats output as: {"answer": "...", "sources": [...]}

def query_with_sources(chain, retriever, question):
    """Query and return answer with source attribution."""
    # TODO: Get retrieved docs
    # TODO: Get answer from chain
    # TODO: Extract source metadata
    # TODO: Return structured result
    pass


# =============================================================================
# TODO 7: Handle Edge Cases
# =============================================================================
# Test and handle:
#   a) Question completely unrelated to docs → "I don't have info..."
#   b) Ambiguous question → ask for clarification or give best match
#   c) Question that spans multiple sections → combine info

def test_edge_cases(chain, retriever):
    """Test edge cases and fallback behavior."""
    test_questions = [
        "How do I authenticate API requests?",          # clear match
        "What is the meaning of life?",                  # unrelated
        "Tell me about rate limits and error handling",  # multi-section
        "How do I use webhooks with Python?",            # combines sections
    ]
    # TODO: Query each, print results and sources
    pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("RAG-POWERED DOCUMENTATION ASSISTANT")
    print("=" * 60)

    # Step 1: Split
    print("\n--- STEP 1: DOCUMENT SPLITTING ---")
    chunks = split_documents(DOCUMENTATION)

    # Step 2: Vector Store
    print("\n--- STEP 2: CREATE VECTOR STORE ---")
    vectorstore = create_vectorstore(chunks)

    # Step 3: Retriever
    print("\n--- STEP 3: CREATE RETRIEVER ---")
    retriever = create_retriever(vectorstore)

    # Step 4: Prompt
    print("\n--- STEP 4: BUILD PROMPT ---")
    prompt = build_rag_prompt()

    # Step 5: Chain
    print("\n--- STEP 5: BUILD RAG CHAIN ---")
    # Use FakeLLM for testing or ChatOpenAI for real results
    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    except Exception:
        from langchain_core.language_models.fake import FakeListLLM
        llm = FakeListLLM(responses=["Based on the documentation, ..."])
        print("  (Using FakeLLM — set OPENAI_API_KEY for real answers)")

    chain = build_rag_chain(retriever, llm)

    # Step 6: Query
    print("\n--- STEP 6: QUERY WITH SOURCES ---")
    questions = [
        "How do I authenticate API requests?",
        "What happens when I exceed the rate limit?",
        "How do I export data?",
    ]
    for q in questions:
        print(f"\nQ: {q}")
        result = query_with_sources(chain, retriever, q)
        if result:
            print(f"A: {result.get('answer', 'N/A')}")
            print(f"Sources: {result.get('sources', [])}")

    # Step 7: Edge Cases
    print("\n--- STEP 7: EDGE CASES ---")
    test_edge_cases(chain, retriever)

    print("\n" + "=" * 60)
    print("Done! You've built a RAG documentation assistant.")
    print("=" * 60)


if __name__ == "__main__":
    main()
