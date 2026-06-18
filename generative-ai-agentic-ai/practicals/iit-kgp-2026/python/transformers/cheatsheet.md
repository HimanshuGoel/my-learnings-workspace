# Transformers (HuggingFace) — Cheatsheet

## Imports

```python
from transformers import pipeline
from transformers import AutoTokenizer, AutoModel
from transformers import AutoModelForSequenceClassification
from transformers import AutoModelForCausalLM
from transformers import Trainer, TrainingArguments
import torch
```

---

## pipeline() — One-Line Inference

```python
# Sentiment analysis
pipeline("sentiment-analysis")("I love this!")

# Text generation
pipeline("text-generation", model="gpt2")("Once upon a time", max_length=50)

# Zero-shot classification
pipeline("zero-shot-classification")("Buy groceries", candidate_labels=["shopping","work","travel"])

# Question answering
pipeline("question-answering")(question="What is AI?", context="AI is...")

# Summarization
pipeline("summarization")("Long text...", max_length=100)

# Named entity recognition
pipeline("ner", aggregation_strategy="simple")("Apple was founded by Steve Jobs")

# Translation
pipeline("translation_en_to_fr")("Hello world")

# Fill mask (BERT-style)
pipeline("fill-mask")("Paris is the [MASK] of France")

# Feature extraction (embeddings)
pipeline("feature-extraction")("Get vector for this text")
```

---

## Tokenizer

```python
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Single text
encoded = tokenizer("Hello world", return_tensors="pt")
# → input_ids, attention_mask

# Batch with padding
encoded = tokenizer(
    ["Short", "A much longer sentence"],
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
)

# Decode
tokenizer.decode(encoded["input_ids"][0])
tokenizer.batch_decode(encoded["input_ids"])

# Token info
tokenizer.vocab_size
tokenizer.encode("Hello")          # → [7592]
tokenizer.tokenize("Hello world")  # → ['hello', 'world']
```

---

## Loading Models

```python
# Base model (hidden states / embeddings)
model = AutoModel.from_pretrained("bert-base-uncased")

# Classification
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)

# Text generation (GPT-style)
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Seq2Seq (T5, BART)
from transformers import AutoModelForSeq2SeqLM
model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")

# Token classification (NER)
model = AutoModelForTokenClassification.from_pretrained("bert-base-uncased", num_labels=9)

# Question answering
model = AutoModelForQuestionAnswering.from_pretrained("bert-base-uncased")
```

---

## Forward Pass & Inference

```python
model.eval()
with torch.no_grad():
    outputs = model(**encoded)

# Base model → hidden states
hidden = outputs.last_hidden_state  # (batch, seq_len, hidden_dim)

# Classification → logits
logits = outputs.logits             # (batch, num_labels)
pred = logits.argmax(dim=1)

# Mean pooling (for embeddings)
embedding = hidden.mean(dim=1)      # (batch, hidden_dim)
```

---

## Text Generation

```python
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

input_ids = tokenizer("The future of AI", return_tensors="pt").input_ids
output = model.generate(
    input_ids,
    max_new_tokens=100,
    temperature=0.7,          # randomness (0=greedy, 1=random)
    top_p=0.9,                # nucleus sampling
    top_k=50,                 # top-k sampling
    do_sample=True,           # enable sampling
    repetition_penalty=1.2,   # discourage repetition
    num_beams=1,              # 1=no beam search
)
text = tokenizer.decode(output[0], skip_special_tokens=True)
```

---

## Fine-Tuning with Trainer

```python
from transformers import Trainer, TrainingArguments
from datasets import load_dataset

dataset = load_dataset("imdb")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=256)

tokenized = dataset.map(tokenize, batched=True)
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
    evaluation_strategy="epoch",
)

trainer = Trainer(model=model, args=args,
                  train_dataset=tokenized["train"],
                  eval_dataset=tokenized["test"])
trainer.train()
```

---

## Embeddings (for RAG/Search)

```python
# Option 1: sentence-transformers library (simplest)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(["text1", "text2"])  # numpy arrays

# Option 2: Manual with AutoModel
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
encoded = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
with torch.no_grad():
    output = model(**encoded)
embeddings = output.last_hidden_state.mean(dim=1)  # mean pooling
```

---

## PEFT / LoRA (Efficient Fine-Tuning)

```python
from peft import LoraConfig, get_peft_model, TaskType

config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=8, lora_alpha=16, lora_dropout=0.1,
    target_modules=["query", "value"]
)
model = get_peft_model(model, config)
model.print_trainable_parameters()  # ~0.4% trainable
```

---

## Save & Load

```python
# Save locally
model.save_pretrained("./my-model")
tokenizer.save_pretrained("./my-model")

# Load back
model = AutoModel.from_pretrained("./my-model")
tokenizer = AutoTokenizer.from_pretrained("./my-model")

# Push to Hub
model.push_to_hub("username/model-name")
tokenizer.push_to_hub("username/model-name")
```

---

## Memory Optimization

```python
# 8-bit quantization (reduce memory by ~4x)
model = AutoModel.from_pretrained("large-model", load_in_8bit=True, device_map="auto")

# 4-bit (even smaller)
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
model = AutoModel.from_pretrained("large-model", quantization_config=bnb_config)

# Gradient checkpointing (trade compute for memory)
model.gradient_checkpointing_enable()
```

---

## Popular Models

| Task | Model | Size |
|------|-------|------|
| Embeddings | `all-MiniLM-L6-v2` | 80MB |
| Classification | `distilbert-base-uncased` | 250MB |
| Generation (small) | `gpt2` | 500MB |
| Generation (medium) | `meta-llama/Llama-2-7b` | 14GB |
| Summarization | `facebook/bart-large-cnn` | 1.6GB |
| Translation | `Helsinki-NLP/opus-mt-en-fr` | 300MB |
| Speech | `openai/whisper-base` | 290MB |
| Vision | `openai/clip-vit-base-patch32` | 600MB |

---

## Quick Reference Links

- Hub: https://huggingface.co/models
- Docs: https://huggingface.co/docs/transformers
- Course: https://huggingface.co/learn/nlp-course
