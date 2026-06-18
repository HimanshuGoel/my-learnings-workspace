# Transformers (HuggingFace) — Notes

## What Problem Does This Library Solve?

HuggingFace Transformers gives you instant access to thousands of pre-trained AI models (BERT, GPT, LLaMA, T5, Whisper, CLIP) with a unified API — download a state-of-the-art model, run inference, or fine-tune it in a few lines of code, without training from scratch.

## Mental Model

Think of HuggingFace as **npm/Maven for AI models**. Just as npm lets you `npm install express` and immediately use a production-ready web server, HuggingFace lets you `from_pretrained("bert-base-uncased")` and immediately use a model trained on billions of tokens. The Hub is the registry. `pipeline()` is the quickstart. `AutoModel` + `AutoTokenizer` gives you full control.

Alternatively: if PyTorch is Express.js (build everything from scratch), HuggingFace Transformers is **Next.js** — batteries included, sensible defaults, but you can eject to raw PyTorch when needed.

## Where It Fits

```
Raw Text / Images / Audio
        │
        ▼
┌────────────────────────┐
│  HuggingFace Transformers │  ← load pre-trained models, tokenize, infer, fine-tune
│  (you are here)            │     (built on PyTorch under the hood)
└───────────┬────────────┘
            │
            ├── Embeddings → Vector DB (ChromaDB, FAISS) → RAG
            ├── Fine-tuned model → Deploy (FastAPI)
            └── Base for agents (LangChain, LlamaIndex)
```

- **Before Transformers:** Raw input data (text, images, audio)
- **After Transformers:** Embeddings, classifications, generated text, fine-tuned models
- **Talks to:** PyTorch (engine), Datasets (data loading), PEFT (efficient fine-tuning), ChromaDB/FAISS (vector storage), LangChain (orchestration)

## Core Concepts

### 1. pipeline() — The One-Liner

```python
from transformers import pipeline

# Text classification
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Text generation
generator = pipeline("text-generation", model="gpt2")
output = generator("The future of AI is", max_length=50)

# Question answering
qa = pipeline("question-answering")
answer = qa(question="What is PyTorch?", context="PyTorch is a deep learning framework.")

# Zero-shot classification (classify WITHOUT training)
classifier = pipeline("zero-shot-classification")
result = classifier("I need to buy groceries", candidate_labels=["shopping", "cooking", "travel"])

# Summarization
summarizer = pipeline("summarization")
summary = summarizer(long_text, max_length=100)

# Feature extraction (get embeddings)
extractor = pipeline("feature-extraction")
embeddings = extractor("Hello world")  # returns vector representation
```

**Key insight:** `pipeline()` is for quick prototyping and demos. For production or fine-tuning, use the explicit `AutoModel` + `AutoTokenizer` approach.

### 2. Tokenizer — Text to Numbers

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Tokenize text
encoded = tokenizer("Hello, how are you?", return_tensors="pt")
# encoded contains:
#   input_ids: tensor([[101, 7592, 1010, 2129, 2024, 2017, 1029, 102]])
#   attention_mask: tensor([[1, 1, 1, 1, 1, 1, 1, 1]])

# Decode back to text
text = tokenizer.decode(encoded["input_ids"][0])
# "[CLS] hello, how are you? [SEP]"

# Batch tokenization with padding
batch = tokenizer(
    ["Hello world", "This is a longer sentence for testing"],
    padding=True,          # pad shorter sequences
    truncation=True,       # truncate to max_length
    max_length=128,
    return_tensors="pt"    # return PyTorch tensors
)
```

**Why tokenizers matter:** Models don't understand text — they understand numbers. The tokenizer converts "Hello" → [7592] (a token ID). Different models use different tokenizers (BPE, WordPiece, SentencePiece). Always use the tokenizer that matches your model.

### 3. AutoModel — Load Any Model

```python
from transformers import AutoModel, AutoModelForSequenceClassification

# Load base model (outputs hidden states / embeddings)
model = AutoModel.from_pretrained("bert-base-uncased")

# Load model with a task-specific head
classifier = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=3
)

# Forward pass
outputs = model(**encoded)
# outputs.last_hidden_state: (batch, seq_len, hidden_dim) = (1, 8, 768)

# For classification
logits = classifier(**encoded).logits  # (batch, num_labels)
predicted_class = logits.argmax(dim=1)
```

**AutoModel variants:**
- `AutoModel` — base (embeddings/hidden states)
- `AutoModelForSequenceClassification` — text classification
- `AutoModelForTokenClassification` — NER, POS tagging
- `AutoModelForQuestionAnswering` — extractive QA
- `AutoModelForCausalLM` — text generation (GPT-style)
- `AutoModelForSeq2SeqLM` — translation, summarization (T5-style)

### 4. Embeddings — The Bridge to RAG

```python
from transformers import AutoTokenizer, AutoModel
import torch

# Load a sentence-transformer model (designed for embeddings)
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text):
    """Convert text to a fixed-size embedding vector."""
    encoded = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        output = model(**encoded)
    # Mean pooling: average all token embeddings
    embedding = output.last_hidden_state.mean(dim=1)
    return embedding.squeeze().numpy()

# Use for similarity search (RAG Module 2)
query_emb = get_embedding("What is machine learning?")
doc_emb = get_embedding("ML is a subset of AI that learns from data")
similarity = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
```

### 5. Text Generation (Causal LM)

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Generate text
input_ids = tokenizer("The meaning of life is", return_tensors="pt").input_ids
output = model.generate(
    input_ids,
    max_new_tokens=50,
    temperature=0.7,       # randomness (lower = more deterministic)
    top_p=0.9,             # nucleus sampling
    do_sample=True,        # enable sampling (vs greedy)
    repetition_penalty=1.2
)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
```

**Generation parameters:**
- `temperature` — controls randomness (0 = greedy, 1 = full random)
- `top_p` — nucleus sampling (consider only top P% probability tokens)
- `top_k` — only consider top K most likely tokens
- `max_new_tokens` — how many tokens to generate
- `do_sample=True` — enable stochastic generation

### 6. Fine-Tuning with Trainer

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import load_dataset

# Load data
dataset = load_dataset("imdb")

# Tokenize
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
def tokenize_fn(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=256)
tokenized = dataset.map(tokenize_fn, batched=True)

# Model
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
)

# Training config
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    learning_rate=2e-5,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_steps=100,
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
)
trainer.train()
```

### 7. PEFT / LoRA — Efficient Fine-Tuning (Module 3 Preview)

```python
from peft import LoraConfig, get_peft_model, TaskType

# Configure LoRA (Low-Rank Adaptation)
# Only trains ~0.1% of parameters instead of all of them
lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=8,                    # rank (lower = fewer params, less expressive)
    lora_alpha=16,          # scaling factor
    lora_dropout=0.1,
    target_modules=["query", "value"]  # which layers to adapt
)

# Apply LoRA to model
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# "trainable params: 294,912 || all params: 66,955,010 || trainable%: 0.44"
```

### 8. The Hub — Model Registry

```python
# Browse: https://huggingface.co/models

# Popular models by task:
# Text classification: "distilbert-base-uncased", "roberta-base"
# Embeddings: "sentence-transformers/all-MiniLM-L6-v2"
# Generation: "gpt2", "meta-llama/Llama-2-7b"
# Summarization: "facebook/bart-large-cnn", "t5-base"
# Translation: "Helsinki-NLP/opus-mt-en-fr"
# Image: "openai/clip-vit-base-patch32"
# Speech: "openai/whisper-base"

# Push your model to Hub
model.push_to_hub("my-username/my-fine-tuned-model")
tokenizer.push_to_hub("my-username/my-fine-tuned-model")
```

## Key Functions/Methods

### Quick Start

| Function | Purpose |
|----------|---------|
| `pipeline(task, model)` | One-line inference for any task |
| `AutoTokenizer.from_pretrained(name)` | Load tokenizer |
| `AutoModel.from_pretrained(name)` | Load base model |
| `AutoModelForXxx.from_pretrained(name)` | Load task-specific model |

### Tokenizer Operations

| Method | Purpose |
|--------|---------|
| `tokenizer(text, return_tensors="pt")` | Tokenize text |
| `tokenizer.decode(ids)` | IDs → text |
| `tokenizer.batch_decode(ids)` | Batch decode |
| `tokenizer.vocab_size` | Vocabulary size |
| `tokenizer.encode(text)` | Text → list of IDs |

### Model Operations

| Method | Purpose |
|--------|---------|
| `model(**inputs)` | Forward pass |
| `model.generate(input_ids, ...)` | Generate text (causal LM) |
| `model.save_pretrained(path)` | Save to disk |
| `model.push_to_hub(name)` | Upload to HuggingFace Hub |
| `model.eval()` | Inference mode |

### Trainer

| Component | Purpose |
|-----------|---------|
| `TrainingArguments(...)` | Configure training (epochs, lr, batch size) |
| `Trainer(model, args, datasets)` | High-level training loop |
| `trainer.train()` | Start training |
| `trainer.evaluate()` | Run evaluation |
| `trainer.predict(test_data)` | Get predictions |

## Common Patterns

### Sentiment Analysis (Classification)

```python
from transformers import pipeline
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
results = classifier(["I love this!", "This is terrible."])
```

### Semantic Search (Embeddings + Cosine Similarity)

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
query_emb = model.encode("How to train a model?")
doc_embs = model.encode(["Training guide...", "Cooking recipes...", "ML tutorial..."])
similarities = np.dot(doc_embs, query_emb) / (
    np.linalg.norm(doc_embs, axis=1) * np.linalg.norm(query_emb)
)
most_relevant = np.argmax(similarities)
```

### Zero-Shot Classification (No Training Needed)

```python
classifier = pipeline("zero-shot-classification")
result = classifier(
    "I need to schedule a dentist appointment",
    candidate_labels=["health", "finance", "travel", "food"]
)
# label: "health", score: 0.92
```

### Summarization

```python
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(long_article, max_length=130, min_length=30)
```

## AI/ML Connection

- **Where in the AI pipeline:** Transformers IS the pipeline for modern NLP/multimodal AI. It handles tokenization, model loading, inference, fine-tuning, and deployment — the full lifecycle for pre-trained models.

- **Concrete example — RAG (Module 2):** Encode documents with a sentence-transformer → store in ChromaDB → at query time, encode query → find similar docs → feed to LLM for answer generation. The encoding step is HuggingFace Transformers.

- **Concrete example — Fine-Tuning (Module 3):** Load a pre-trained model, apply LoRA adapters (PEFT), train on your instruction dataset using Trainer, push to Hub. The entire workflow is HuggingFace.

- **Concrete example — Agents (Module 4):** LangChain calls HuggingFace models for generation and embedding. Understanding the model loading/inference pattern helps debug agent issues.

- **Which IIT KGP modules use this:** Module 1 (Transformer architecture, prompting, APIs), Module 2 (embeddings for RAG), Module 3 (fine-tuning with PEFT/LoRA), Module 4 (model composition for agents), Module 5 (model serving).

- **What breaks without it:** You'd need to train models from scratch (requires months + millions of dollars in compute). Pre-trained models are the foundation of modern AI — HuggingFace is how you access them.

- **Concrete example — Zero-shot:** Need to classify customer tickets into categories but have no labeled data? Zero-shot classification lets you define categories and classify immediately — no training needed.

- **Relationship to PyTorch:** Every HuggingFace model IS a PyTorch nn.Module. `model.parameters()`, `model.eval()`, `torch.no_grad()` — everything from PyTorch applies directly.

## Common Mistakes

1. **Using wrong tokenizer for model** — always load tokenizer and model from the same checkpoint. They're paired (different vocab, different special tokens).

2. **Forgetting `return_tensors="pt"`** — without it, tokenizer returns Python lists, not PyTorch tensors. The model needs tensors.

3. **Not padding/truncating for batches** — sequences have different lengths. Use `padding=True, truncation=True` or the model will crash.

4. **OOM (Out of Memory)** — large models don't fit in RAM/VRAM. Solutions: use smaller models (distilbert, MiniLM), reduce batch size, use quantization (4-bit/8-bit), or use `device_map="auto"`.

5. **Fine-tuning the entire model when LoRA is enough** — full fine-tuning needs massive compute. PEFT/LoRA trains 0.1-1% of parameters with nearly same quality.

6. **Not using `torch.no_grad()` for inference** — wastes memory and slows down. Always wrap inference in `with torch.no_grad():`.

7. **Confusing model types** — using `AutoModelForCausalLM` when you need `AutoModelForSequenceClassification`. Each task has its own model head.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Tabular/structured data | Scikit-Learn, XGBoost |
| Simple keyword search | Elasticsearch, regex |
| Real-time low-latency serving | ONNX Runtime, vLLM |
| Very small text datasets (< 100 samples) | Rule-based or zero-shot |
| Tasks that don't involve language/vision/audio | Traditional ML |
| Production LLM APIs (don't want to self-host) | OpenAI API, Anthropic API |

## Ready to Move On?

- ☐ I can use pipeline() for quick inference on any task
- ☐ I understand tokenizer → model → output flow
- ☐ I can load a model with AutoModel and get embeddings
- ☐ I know the difference between AutoModel, AutoModelForCausalLM, AutoModelForSequenceClassification
- ☐ I understand how fine-tuning works at a high level (Trainer + TrainingArguments)

Once all checked → move to **LangChain** (Phase 6: Agentic AI).
