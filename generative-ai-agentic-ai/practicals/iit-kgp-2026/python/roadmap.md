# Python Libraries — Roadmap

## Learning Order

Each phase builds on the previous one. Mental models in parentheses use familiar analogies.

### Phase 1 — Data Foundation

| Library      | Mental Model                                             |
| ------------ | -------------------------------------------------------- |
| NumPy        | Supercharged Array Engine (Excel calculations at scale)  |
| Pandas       | Excel on steroids for developers                         |
| Matplotlib   | Drawing engine for visualization                         |
| Scikit-Learn | Angular of ML (fit, predict, transform, score)           |

Everything else depends on these four.

---

### Phase 2 — Deep Learning

| Library    | Mental Model                                       |
| ---------- | -------------------------------------------------- |
| PyTorch    | Angular + NumPy + Automatic Gradient Calculation   |
| TensorFlow | Learn enough to understand                         |
| Keras      | Spring Boot Starter for Deep Learning              |

Focus mostly on PyTorch — industry momentum is heavily toward it.

---

### Phase 3 — NLP & LLMs

| Library      | Mental Model                          |
| ------------ | ------------------------------------- |
| Transformers | Where the magic starts (HuggingFace) |
| Datasets     | npm registry for AI datasets          |
| spaCy        | Enterprise NLP (fast, production)     |
| NLTK         | Traditional NLP toolbox               |

---

### Phase 4 — Tabular ML

| Library  | Mental Model                         |
| -------- | ------------------------------------ |
| XGBoost  | A committee of smart decision trees  |
| LightGBM | Faster XGBoost                       |

Still among the strongest tools for structured/business data.

---

### Phase 5 — Production AI

| Library | Mental Model                              |
| ------- | ----------------------------------------- |
| FastAPI | Spring Boot for AI Engineers              |
| MLflow  | GitHub + Jenkins + SonarQube for ML       |

---

### Phase 6 — Agentic AI & RAG

| Library    | Mental Model                              |
| ---------- | ----------------------------------------- |
| LangChain  | Spring Framework for LLM Apps             |
| LlamaIndex | Database access layer for LLMs            |

---

### Phase 7 — Specialized

| Library      | Mental Model       |
| ------------ | ------------------ |
| OpenCV       | Computer vision    |
| Apache Spark | Distributed Pandas |

---

## Top 10 Priority

For AI engineering, RAG, copilots, and agentic applications:

1. NumPy
2. Pandas
3. Scikit-Learn
4. PyTorch
5. Transformers
6. FastAPI
7. LangChain
8. LlamaIndex
9. MLflow
10. Matplotlib

---

## Learning Method Per Library

| Day | Focus                                       |
| --- | ------------------------------------------- |
| 1   | What problem does this library solve?       |
| 2   | Explain through real business examples      |
| 3   | Teach 20% that gives 80% value             |
| 4   | Create exercises for me                     |
| 5   | Give me a mini project                      |
| 6   | Review my solution                          |

---

## Practice Folder Structure

```text
AI-Learning/
├── numpy/       (notes.md, examples.py, cheatsheet.md, projects.md)
├── pandas/
├── matplotlib/
├── sklearn/
├── pytorch/
├── transformers/
├── langchain/
├── llamaindex/
├── fastapi/
└── mlflow/
```
