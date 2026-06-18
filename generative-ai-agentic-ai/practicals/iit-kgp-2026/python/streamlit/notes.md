# Streamlit — Notes

## What Problem Does This Library Solve?

Streamlit lets you build interactive web UIs for your ML models and data apps using only Python — no HTML, CSS, JavaScript, or frontend knowledge needed. Write a script, get a web app.

## Mental Model

Think of Streamlit as **a one-file React app for data people**. You write a Python script top-to-bottom. Streamlit converts it into an interactive web page. Every widget (slider, text input, button) is one line of Python. When the user interacts, the entire script re-runs with the new values — like React's state-driven re-rendering, but without components, hooks, or JSX.

Alternatively: if FastAPI is the backend (returns JSON), Streamlit is the **instant frontend** you put in front of it for demos and presentations.

## Where It Fits

```
AI Backend (RAG / Model / Agent)
        │
        ├── FastAPI (for programmatic access — other services call it)
        │
        └── Streamlit (for human access — demo UI, presentations)
                │
                ▼
        ┌─────────────────────┐
        │   Browser Window     │  ← interactive web app
        │   (you are here)     │
        │   Chat, forms, charts│
        └─────────────────────┘
```

- **Before Streamlit:** Your AI app is a Python script or Jupyter notebook (not shareable)
- **After Streamlit:** A web app anyone can use — no Python install needed for end users
- **Talks to:** FastAPI (backend API), LangChain/LlamaIndex (AI logic), Matplotlib/Plotly (charts), Pandas (data display)

## Core Concepts

### 1. Hello World — One-File Web App

```python
# app.py
import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, World!")

name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}! 👋")

# Run: streamlit run app.py
# Opens: http://localhost:8501
```

That's it. No server setup, no templates, no routing. One file → web app.

### 2. Display Elements

```python
import streamlit as st
import pandas as pd

# Text
st.title("Main Title")
st.header("Section Header")
st.subheader("Subsection")
st.write("Markdown, tables, charts — write() handles everything")
st.markdown("**Bold** and `code` and [links](url)")
st.code("print('hello')", language="python")

# Data
df = pd.DataFrame({"name": ["Alice", "Bob"], "score": [85, 92]})
st.dataframe(df)           # interactive table (sort, filter)
st.table(df)               # static table
st.metric("Accuracy", "92%", "+3%")  # big number with delta

# Media
st.image("photo.png", caption="My photo")
st.json({"key": "value"})  # formatted JSON viewer
```

### 3. Input Widgets

```python
# Text
name = st.text_input("Your name")
query = st.text_area("Your question", height=100)

# Numbers
age = st.number_input("Age", min_value=0, max_value=120, value=25)
temp = st.slider("Temperature", 0.0, 2.0, 0.7, step=0.1)

# Selection
model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
options = st.multiselect("Tags", ["ML", "NLP", "CV", "RAG"])
agree = st.checkbox("I agree to terms")
mode = st.radio("Mode", ["Fast", "Accurate"])

# Files
file = st.file_uploader("Upload PDF", type=["pdf", "txt"])

# Button
if st.button("Submit"):
    st.write("Button clicked!")
```

**Key insight:** Every widget returns its current value. When user changes it, the script re-runs with the new value.

### 4. Layout

```python
# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Left column")
with col2:
    st.write("Right column")

# Sidebar
with st.sidebar:
    st.title("Settings")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    top_k = st.slider("Top K", 1, 10, 3)

# Tabs
tab1, tab2 = st.tabs(["Chat", "Settings"])
with tab1:
    st.write("Chat interface here")
with tab2:
    st.write("Configuration here")

# Expander (collapsible)
with st.expander("Show details"):
    st.write("Hidden content revealed on click")
```

### 5. Chat Interface (For RAG/LLM Apps)

```python
import streamlit as st

st.title("RAG Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("Ask a question"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response (call your RAG chain here)
    response = rag_chain.invoke(prompt)

    # Add assistant message
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

### 6. Session State (Persist Data Across Reruns)

```python
# Problem: script re-runs on every interaction → variables reset
# Solution: st.session_state persists between reruns

# Initialize (only once)
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Modify
if st.button("Increment"):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")

# Store anything: models, chat history, search results
if "index" not in st.session_state:
    st.session_state.index = build_rag_index()  # expensive — do once
```

### 7. Caching (Avoid Recomputing)

```python
# @st.cache_data — cache data (DataFrames, strings, numbers)
@st.cache_data
def load_data(path):
    return pd.read_csv(path)  # only runs once, then cached

# @st.cache_resource — cache global resources (models, DB connections)
@st.cache_resource
def load_model():
    return joblib.load("model.joblib")  # loaded once, shared across users

# Usage
df = load_data("data.csv")      # cached
model = load_model()            # cached
```

### 8. Streaming Output (LLM-Style)

```python
import streamlit as st
import time

# Simulate streaming LLM output
def stream_response(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

if prompt := st.chat_input("Ask"):
    with st.chat_message("assistant"):
        st.write_stream(stream_response("This is a streaming response word by word"))
```

### 9. Charts & Visualization

```python
import streamlit as st
import pandas as pd
import numpy as np

# Built-in charts (quick)
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(chart_data)
st.bar_chart(chart_data)
st.area_chart(chart_data)

# Matplotlib
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
st.pyplot(fig)

# Plotly (interactive)
import plotly.express as px
fig = px.scatter(df, x="age", y="salary", color="dept")
st.plotly_chart(fig)
```

### 10. Multi-Page Apps

```
my_app/
├── app.py              ← main page
└── pages/
    ├── 1_Chat.py       ← page 1 (auto-detected)
    ├── 2_Analytics.py  ← page 2
    └── 3_Settings.py   ← page 3
```

Streamlit auto-generates a sidebar navigation from the `pages/` folder. Each file is an independent page.

## Key Functions/Methods

### Display

| Function | Purpose |
|----------|---------|
| `st.title/header/subheader` | Headings |
| `st.write(anything)` | Smart display (text, df, chart, dict) |
| `st.markdown(str)` | Markdown text |
| `st.code(str, language)` | Code block |
| `st.dataframe(df)` | Interactive table |
| `st.metric(label, value, delta)` | KPI metric |
| `st.json(dict)` | JSON viewer |
| `st.image/audio/video` | Media |

### Input

| Function | Returns |
|----------|---------|
| `st.text_input(label)` | str |
| `st.text_area(label)` | str |
| `st.number_input(label, min, max)` | int/float |
| `st.slider(label, min, max, default)` | number |
| `st.selectbox(label, options)` | selected option |
| `st.multiselect(label, options)` | List |
| `st.checkbox(label)` | bool |
| `st.radio(label, options)` | selected option |
| `st.file_uploader(label, type)` | UploadedFile |
| `st.button(label)` | bool (True when clicked) |
| `st.chat_input(placeholder)` | str |

### Layout

| Function | Purpose |
|----------|---------|
| `st.columns(n)` | Side-by-side columns |
| `st.sidebar` | Left sidebar |
| `st.tabs(names)` | Tab panels |
| `st.expander(label)` | Collapsible section |
| `st.container()` | Logical grouping |

### Performance

| Function | Purpose |
|----------|---------|
| `@st.cache_data` | Cache data (dfs, strings) |
| `@st.cache_resource` | Cache resources (models, DBs) |
| `st.session_state` | Persist state across reruns |
| `st.spinner("Loading...")` | Show loading indicator |

## Common Patterns

### RAG Chatbot (Complete)

```python
import streamlit as st

st.title("📚 Document QA")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Results", 1, 10, 3)
    uploaded = st.file_uploader("Upload doc", type=["pdf", "txt"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about your documents"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = rag_chain.invoke(prompt)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

### Model Demo

```python
st.title("🤖 Sentiment Analyzer")
text = st.text_area("Enter text to analyze")
if st.button("Analyze") and text:
    with st.spinner("Processing..."):
        result = model.predict(text)
    col1, col2 = st.columns(2)
    col1.metric("Sentiment", result["label"])
    col2.metric("Confidence", f"{result['score']:.0%}")
```

## AI/ML Connection

- **Where in the AI pipeline:** Streamlit is the presentation/demo layer. It gives humans a way to interact with your AI system without code.

- **Concrete example — Capstone (Module 5):** Build RAG backend (LangChain) + API (FastAPI) + demo UI (Streamlit). Evaluators interact with the Streamlit interface.

- **Concrete example — RAG chatbot:** 30 lines of Streamlit gives you a ChatGPT-like interface over your own documents. Upload PDFs, ask questions, see sources.

- **Which IIT KGP modules use this:** Module 5 (capstone presentation, demo UI). Also useful for Module 2/4 demos.

- **What breaks without it:** You'd present your capstone as a terminal script or Jupyter notebook. Streamlit makes it look like a real product with zero frontend effort.

## Common Mistakes

1. **Not using session_state** — without it, variables reset on every widget interaction. Chat history, model state, counters — all need session_state.

2. **Not caching model loading** — without `@st.cache_resource`, the model reloads on every rerun (slow!).

3. **Putting expensive code outside cache** — any code not in a cache decorator runs on every interaction. Cache data loading and model initialization.

4. **Not using st.spinner** — long operations without a spinner look like the app froze. Always wrap slow calls.

5. **Complex logic without page separation** — one giant script gets unmaintainable. Use the `pages/` folder for multi-page apps.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Production API (machine-to-machine) | FastAPI |
| Complex frontend (custom design, animations) | React + FastAPI |
| Real-time collaboration | Custom web app |
| Mobile app | React Native / Flutter + API |
| Very high traffic (1000+ concurrent users) | Dedicated frontend + backend |

## Ready to Move On?

- ☐ I can build a one-file web app with text input, display, and buttons
- ☐ I can create a chat interface using st.chat_message and st.chat_input
- ☐ I understand session_state for persisting data across reruns
- ☐ I can cache model loading with @st.cache_resource
- ☐ I can add a sidebar with configuration widgets

You're done with the Python library stack! 🎉
