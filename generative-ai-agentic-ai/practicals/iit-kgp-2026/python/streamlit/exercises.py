"""
Streamlit Exercises — 8 Problems (Easy → Medium → Hard)
Each exercise is a separate mini-app. AI-relevant exercises marked with [AI].

SETUP: pip install streamlit pandas numpy plotly
RUN:   streamlit run exercises.py  (or run each exercise as separate file)

NOTE: Unlike other exercise files, these are best tested by running each
as its own Streamlit app. Copy each exercise to a temp file and run it.
"""

import streamlit as st
import pandas as pd
import numpy as np

# =============================================================================
# EASY (1-3)
# =============================================================================

# Exercise 1: Personal Dashboard
# Build a simple personal dashboard with:
# a) Title and your name
# b) A sidebar with: age (number_input), city (selectbox), interests (multiselect)
# c) Main area shows: greeting, and a summary of what you entered
# d) A button that says "Generate Bio" — when clicked, displays a fake bio
# Expected: interactive page that updates as you change widgets

def exercise_1():
    st.title("👤 Personal Dashboard")
    # Your code here
    pass


# Exercise 2: Data Explorer
# Build a data exploration tool:
# a) Generate a random DataFrame (100 rows, 5 columns)
# b) Show the DataFrame with st.dataframe()
# c) Add a column selector (multiselect) to filter displayed columns
# d) Add a row filter (slider for min/max of first column)
# e) Show basic stats (mean, std) for filtered data using st.metric()
# Expected: interactive data filtering and exploration

def exercise_2():
    st.title("📊 Data Explorer")
    # Your code here
    pass


# Exercise 3: Calculator App
# Build a calculator:
# a) Two number inputs (a and b)
# b) A selectbox for operation (+, -, *, /, **)
# c) A "Calculate" button
# d) Display result as a big metric
# e) Handle division by zero gracefully (st.error)
# Expected: working calculator with error handling

def exercise_3():
    st.title("🧮 Calculator")
    # Your code here
    pass


# =============================================================================
# MEDIUM (4-6)
# =============================================================================

# Exercise 4: ML Model Demo [AI]
# Build a demo UI for a "sentiment analyzer":
# a) Text area for input
# b) Slider for confidence threshold
# c) Button to "Analyze"
# d) Display result with colored metrics (positive=green, negative=red)
# e) Show a "confidence bar" using st.progress()
# Simulate the model (no real model needed).
# Expected: looks like a real ML demo app

def exercise_4():
    st.title("🎭 Sentiment Analyzer")
    # Simulated model
    def fake_predict(text):
        score = len(text) % 100 / 100  # fake "confidence"
        label = "Positive" if score > 0.5 else "Negative"
        return {"label": label, "score": score}
    # Your code here
    pass


# Exercise 5: Chat Interface [AI]
# Build a chatbot UI:
# a) Initialize message history in session_state
# b) Display all previous messages with st.chat_message
# c) Accept new input with st.chat_input
# d) Generate a fake response (echo back or use a simple rule)
# e) Add a "Clear History" button in sidebar
# This is the exact pattern for your RAG capstone demo.
# Expected: working chat with persistent history

def exercise_5():
    st.title("💬 Chatbot")
    # Your code here
    pass


# Exercise 6: File Upload & Analysis [AI]
# Build a document analyzer:
# a) File uploader accepting .txt and .csv
# b) If CSV: show dataframe, basic stats, column chart
# c) If TXT: show word count, character count, first 500 chars
# d) Add a "summary" section (fake — just show first sentence)
# This mimics the "upload docs → analyze" pattern in RAG apps.
# Expected: different display based on file type

def exercise_6():
    st.title("📁 File Analyzer")
    # Your code here
    pass


# =============================================================================
# HARD (7-8)
# =============================================================================

# Exercise 7: RAG Demo App (Complete) [AI]
# Build a complete RAG demo interface:
# a) Sidebar: model selection, top_k slider, file upload area
# b) Main: chat interface for questions
# c) Below chat: expandable "Sources" section showing retrieved docs
# d) Metrics bar: response time, confidence, source count
# e) Use session_state for chat history and "indexed" documents
# f) Simulate RAG (no real backend needed)
# This is your Module 5 capstone frontend template.
# Expected: production-looking RAG demo (simulated backend)

def exercise_7():
    st.set_page_config(page_title="RAG Demo", layout="wide")
    st.title("📚 RAG Document QA")
    # Your code here: sidebar config, chat, sources, metrics
    pass


# Exercise 8: Multi-Page App Structure [AI]
# Build a multi-page app skeleton with:
# Page 1 (main): Overview dashboard with metrics
# Page 2: Chat interface
# Page 3: Document management (upload, list, delete)
# Page 4: Settings (model config, API keys)
# NOTE: For this exercise, put all pages in one file using tabs
# (real multi-page uses pages/ folder)
# Expected: organized multi-section app with navigation

def exercise_8():
    st.set_page_config(page_title="AI Platform", layout="wide")
    st.title("🤖 AI Platform")
    # Your code here: use st.tabs for 4 "pages"
    pass


# =============================================================================
# Main (runs exercise 1 by default — change to test others)
# =============================================================================

if __name__ == "__main__":
    st.sidebar.title("Exercise Selector")
    exercise = st.sidebar.radio(
        "Pick exercise",
        ["Ex 1: Dashboard", "Ex 2: Data Explorer", "Ex 3: Calculator",
         "Ex 4: Sentiment", "Ex 5: Chat", "Ex 6: File Upload",
         "Ex 7: RAG Demo", "Ex 8: Multi-Page"]
    )

    exercises = {
        "Ex 1: Dashboard": exercise_1,
        "Ex 2: Data Explorer": exercise_2,
        "Ex 3: Calculator": exercise_3,
        "Ex 4: Sentiment": exercise_4,
        "Ex 5: Chat": exercise_5,
        "Ex 6: File Upload": exercise_6,
        "Ex 7: RAG Demo": exercise_7,
        "Ex 8: Multi-Page": exercise_8,
    }

    exercises[exercise]()
