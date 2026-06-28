# Streamlit — Cheatsheet

## Install & Run

```bash
pip install streamlit
streamlit run app.py
# Opens: http://localhost:8501
```

## Import

```python
import streamlit as st
```

---

## Display

```python
st.title("Title")
st.header("Header")
st.subheader("Subheader")
st.write("Anything — text, df, dict, chart")
st.markdown("**Bold** `code` [link](url)")
st.code("print('hi')", language="python")
st.latex(r"E = mc^2")

# Data
st.dataframe(df)         # interactive table
st.table(df)             # static table
st.metric("Acc", "92%", "+3%")
st.json({"key": "val"})

# Media
st.image("img.png", caption="Caption")
st.audio("audio.mp3")
st.video("video.mp4")
```

---

## Input Widgets

```python
# Text
name = st.text_input("Name")
text = st.text_area("Message", height=100)

# Numbers
n = st.number_input("Count", min_value=0, max_value=100, value=10)
val = st.slider("Temperature", 0.0, 2.0, 0.7, step=0.1)

# Selection
choice = st.selectbox("Pick one", ["A", "B", "C"])
choices = st.multiselect("Pick many", ["A", "B", "C"])
on = st.checkbox("Enable")
mode = st.radio("Mode", ["Fast", "Accurate"])

# File
file = st.file_uploader("Upload", type=["pdf", "txt", "csv"])

# Button
if st.button("Submit"):
    st.write("Clicked!")

# Chat input
if prompt := st.chat_input("Ask something"):
    st.write(prompt)
```

---

## Layout

```python
# Columns
col1, col2, col3 = st.columns(3)
col1.write("Left")
col2.write("Middle")
col3.write("Right")

# Sidebar
with st.sidebar:
    st.title("Config")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])

# Tabs
tab1, tab2 = st.tabs(["Chat", "Settings"])
with tab1:
    st.write("Chat here")

# Expander
with st.expander("Details"):
    st.write("Hidden content")

# Container
with st.container():
    st.write("Grouped content")
```

---

## Chat Interface

```python
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        response = get_answer(prompt)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

---

## Session State

```python
# Initialize (only first run)
if "key" not in st.session_state:
    st.session_state.key = default_value

# Read/write
st.session_state.counter += 1
st.write(st.session_state.counter)
```

---

## Caching

```python
# Cache data (DataFrames, strings, lists)
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

# Cache resources (models, DB connections, indexes)
@st.cache_resource
def load_model():
    return joblib.load("model.joblib")
```

---

## Status & Progress

```python
with st.spinner("Loading..."):
    result = slow_function()

st.success("Done!")
st.error("Something went wrong")
st.warning("Be careful")
st.info("FYI")

bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1)
```

---

## Charts

```python
# Built-in (quick)
st.line_chart(df)
st.bar_chart(df)
st.area_chart(df)
st.scatter_chart(df, x="a", y="b")

# Matplotlib
st.pyplot(fig)

# Plotly (interactive)
st.plotly_chart(fig)
```

---

## Streaming

```python
# Stream text (LLM-style)
st.write_stream(generator_function())

# Manual streaming
placeholder = st.empty()
for word in words:
    full_response += word
    placeholder.write(full_response)
```

---

## Multi-Page

```
app.py              ← main entry
pages/
├── 1_Chat.py       ← auto-detected pages
├── 2_Dashboard.py
└── 3_Settings.py
```

---

## Quick Reference Links

- Docs: https://docs.streamlit.io/
- Cheat sheet: https://docs.streamlit.io/develop/quick-reference/cheat-sheet
- Gallery: https://streamlit.io/gallery
