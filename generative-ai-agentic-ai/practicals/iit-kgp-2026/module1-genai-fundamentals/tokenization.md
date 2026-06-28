# Tokenization

## What Is This?

Tokenization is the process of converting raw text into a sequence of integer IDs that a model can process — splitting "Hello world" into tokens like ["Hel", "lo", " world"] → [15496, 995, 995].

## Why Does It Exist?

**The Problem:** Neural networks only understand numbers. They can't process the string "Hello" directly. You need a consistent, reversible mapping from text → numbers that:
- Handles any text (including rare words, code, emojis, other languages)
- Keeps vocabulary size manageable (can't have one ID per word — too many words exist)
- Preserves enough information to reconstruct the original text

**Before modern tokenization:**
- Word-level: split by spaces → vocabulary explodes (millions of unique words), can't handle typos or new words
- Character-level: each letter = one token → sequence becomes extremely long, model loses word-level meaning

**The Solution:** Subword tokenization (BPE, WordPiece) — split text into frequently-occurring chunks that balance vocabulary size with sequence length. Common words stay whole ("the" → one token), rare words get split ("unhappiness" → "un" + "happiness").

## Mental Model

Think of tokenization as **UTF-8 encoding for AI models**. Just as UTF-8 maps characters → bytes using a variable-length encoding (common chars = fewer bytes), tokenizers map text → token IDs using variable-length splitting (common words = fewer tokens).

Or: like **compression**. A ZIP file doesn't store every character individually — it finds patterns. Tokenizers do the same: frequently-seen text chunks get short IDs, rare text gets split into smaller known pieces.

## How It Works

### Step 1: Build a Vocabulary (Training the Tokenizer)

1. Start with all individual characters as the base vocabulary
2. Count all pairs of adjacent tokens in the training text
3. Merge the most frequent pair into a new token
4. Repeat steps 2-3 until vocabulary reaches target size (e.g., 50,000)

This is **Byte Pair Encoding (BPE)** — the method used by GPT models.

### Step 2: Encode Text (At Inference Time)

```
Input:  "unhappiness"
Step 1: Split into characters → ["u", "n", "h", "a", "p", "p", "i", "n", "e", "s", "s"]
Step 2: Apply learned merges → ["un", "happiness"] (if these exist in vocab)
Step 3: Look up IDs → [348, 14372]
```

### Step 3: Decode Back

```
IDs:    [348, 14372]
Lookup: [348 → "un", 14372 → "happiness"]
Join:   "unhappiness"
```

### Tokenizer Types

| Type | Used By | How It Differs |
|------|---------|---------------|
| BPE (Byte Pair Encoding) | GPT-2, GPT-4, LLaMA | Merges most frequent pairs bottom-up |
| WordPiece | BERT | Similar to BPE but uses likelihood, not frequency |
| SentencePiece | T5, LLaMA | Language-agnostic, treats space as a character |
| Unigram | Some multilingual models | Starts big, prunes unlikely tokens |

## Concrete Example

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

text = "Tokenization is fascinating!"
tokens = tokenizer.tokenize(text)
# ['Token', 'ization', ' is', ' fascinating', '!']

ids = tokenizer.encode(text)
# [30642, 1634, 318, 12913, 0]

# Notice: "Tokenization" → 2 tokens, " is" includes the space, "!" is its own token
```

**Key observations:**
- Common words like "is" are one token (including the leading space)
- Rarer words get split: "Tokenization" → "Token" + "ization"
- Punctuation is typically its own token
- The same word can tokenize differently depending on context (capitalization, position)

## Special Tokens

| Token | Purpose | Example |
|-------|---------|---------|
| [CLS] / \<s\> | Start of sequence | BERT uses [CLS] at the beginning |
| [SEP] / \</s\> | End of sequence / separator | Marks boundaries |
| [PAD] | Padding (fill shorter sequences) | Makes batches uniform length |
| [MASK] | Masked token (BERT training) | "The [MASK] sat on the mat" |
| [UNK] | Unknown token (not in vocab) | Rare in modern tokenizers |

## Where You'll Use This

| Module | How Tokenization Applies |
|--------|--------------------------|
| Module 1 | Understanding model input format, token limits, why prompts have max lengths |
| Module 2 | Chunking documents — you chunk by tokens not characters. Token count = cost. |
| Module 3 | Fine-tuning data needs tokenization. Different models = different tokenizers. |
| Module 5 | API pricing is per token. Optimizing token usage = saving money. |

## Common Misconceptions

| Wrong | Correct |
|-------|---------|
| "1 word = 1 token" | Average is ~1.3 tokens per English word. "Extraordinary" might be 3 tokens. |
| "All models use the same tokenizer" | Each model family has its own. BERT ≠ GPT ≠ LLaMA tokenizers. |
| "Tokenization is just splitting by spaces" | Subword tokenization is much smarter — handles any text including code and emojis. |
| "More tokens = more understanding" | More tokens = longer sequence = more computation and cost. Efficiency matters. |
| "Tokenizer is a minor detail" | Wrong tokenizer with a model = garbage output. They're paired. |

## Connection to Other Topics

- **Builds on:** Why LLMs Exist (models need numbers, not text)
- **Enables:** Embeddings (each token ID gets mapped to a vector)
- **Practical impact:** Token count determines cost, context window limits, and chunking strategy in RAG

## Ready to Move On?

- ☐ I understand why subword tokenization exists (not word-level, not character-level)
- ☐ I can explain BPE at a high level (merge frequent pairs until vocab size reached)
- ☐ I know that different models have different tokenizers (always pair them)
- ☐ I understand that token count ≠ word count and affects cost/context limits

Next → **Embeddings** (how token IDs become meaning vectors)
