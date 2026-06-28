# Python Libraries — Roadmap

## Learning Order

Each phase builds on the previous one. Mental models in parentheses use familiar analogies.

### Phase 1 — Data Foundation

| Library      | Mental Model                                            |
| ------------ | ------------------------------------------------------- |
| NumPy        | Supercharged Array Engine (Excel calculations at scale) |
| Pandas       | Excel on steroids for developers                        |
| Matplotlib   | Drawing engine for visualization                        |
| Scikit-Learn | Angular of ML (fit, predict, transform, score)          |

Everything else depends on these four.

---

### Phase 2 — Deep Learning

| Library          | Mental Model                                      |
| ---------------- | ------------------------------------------------- |
| PyTorch          | Angular + NumPy + Automatic Gradient Calculation  |
| TensorFlow/Keras | Awareness only — read old code, don't invest time |

Focus on PyTorch — industry momentum is heavily toward it. TensorFlow is legacy in most new AI work.

---

### Phase 3 — NLP & LLMs

| Library      | Mental Model                                                                 |
| ------------ | ---------------------------------------------------------------------------- |
| Transformers | Where the magic starts (HuggingFace)                                         |
| Datasets     | npm registry for AI datasets                                                 |
| spaCy        | Enterprise NLP (fast, production) — optional, Transformers covers most needs |

> NLTK is outdated/academic. Skip it — spaCy and HuggingFace cover everything better and faster.

---

### Phase 4 — RAG & Vector Storage

| Library  | Mental Model                                                               |
| -------- | -------------------------------------------------------------------------- |
| ChromaDB | Local vector database (like SQLite for embeddings)                         |
| FAISS    | Facebook's fast similarity search (low-level, powerful)                    |
| Pydantic | TypeScript interfaces for Python — data validation, structured LLM outputs |

Essential for Module 2 (RAG). Every RAG pipeline needs a vector store + structured data handling.

---

### Phase 5 — Tabular ML

| Library  | Mental Model                        |
| -------- | ----------------------------------- |
| XGBoost  | A committee of smart decision trees |
| LightGBM | Faster XGBoost                      |

Still among the strongest tools for structured/business data (Kaggle winners).

---

### Phase 6 — Agentic AI & RAG Orchestration

| Library    | Mental Model                   |
| ---------- | ------------------------------ |
| LangChain  | Spring Framework for LLM Apps  |
| LlamaIndex | Database access layer for LLMs |

---

### Phase 7 — Production & Deployment

| Library   | Mental Model                                         |
| --------- | ---------------------------------------------------- |
| FastAPI   | Spring Boot for AI Engineers                         |
| MLflow    | GitHub + Jenkins + SonarQube for ML                  |
| Streamlit | Instant demo UI (like a one-file React app for data) |

Streamlit/Gradio takes 30 minutes to learn but makes capstone presentations shine.

---

## Top 12 Priority

For AI engineering, RAG, copilots, and agentic applications:

1. NumPy
2. Pandas
3. Scikit-Learn
4. PyTorch
5. Transformers (HuggingFace)
6. LangChain
7. LlamaIndex
8. ChromaDB / FAISS
9. Pydantic
10. FastAPI
11. MLflow
12. Matplotlib

---

## Aligned to IIT KGP Program Timeline

| Program Phase                         | Dates           | Libraries to Know                          |
| ------------------------------------- | --------------- | ------------------------------------------ |
| Foundation Bridge                     | May 17 – Jun 21 | NumPy, Pandas, Matplotlib, Scikit-Learn    |
| Module 1: Foundations of GenAI & LLMs | May 30 – Jul 18 | PyTorch basics, Transformers (HuggingFace) |
| Module 2: Advanced Prompting & RAG    | Jul 25 – Sep 5  | LangChain, ChromaDB/FAISS, Pydantic        |
| Module 3: Fine-Tuning & Alignment     | Sep 12 – Oct 31 | PyTorch deeper (fine-tuning, LoRA, PEFT)   |
| Module 4: Multimodal & Agentic AI     | Nov 14 – Dec 26 | LangChain Agents, LlamaIndex, LangGraph    |
| Module 5: Deployment & Capstone       | Jan 2 – Feb 6   | FastAPI, MLflow, Streamlit                 |

---

## Deprioritized / Skipped

| Library          | Reason                                                                        |
| ---------------- | ----------------------------------------------------------------------------- |
| NLTK             | Outdated, academic. HuggingFace Transformers does everything better.          |
| TensorFlow/Keras | Industry moved to PyTorch. Read-only awareness is enough.                     |
| OpenCV           | Only if capstone involves computer vision. Otherwise skip.                    |
| Apache Spark     | Data engineering tool, not AI engineering. Not relevant for this certificate. |

---

## Learning Method Per Library

| Day | Focus                                  |
| --- | -------------------------------------- |
| 1   | What problem does this library solve?  |
| 2   | Explain through real business examples |
| 3   | Teach 20% that gives 80% value         |
| 4   | Create exercises for me                |
| 5   | Give me a mini project                 |
| 6   | Review my solution                     |

---

## Practice Folder Structure

```text
python/
├── numpy/       (notes.md, examples.py, cheatsheet.md, projects.md)
├── pandas/
├── matplotlib/
├── sklearn/
├── pytorch/
├── transformers/
├── langchain/
├── llamaindex/
├── chromadb/
├── pydantic/
├── fastapi/
├── mlflow/
└── streamlit/
```
