"""
=============================================================================
MINI PROJECT: Text Sentiment Classifier (PyTorch from Scratch)
=============================================================================

PROBLEM STATEMENT:
Build a simple neural network that classifies text sentiment (positive/negative)
using a bag-of-words approach. This introduces the full PyTorch workflow on a
text task — directly relevant to your NLP/LLM coursework.

WHAT YOU'LL BUILD:
- A vocabulary builder (text → integer IDs)
- A bag-of-words encoder (sentence → fixed-size vector)
- A 2-layer neural network for binary classification
- A complete training loop with loss tracking
- Evaluation on a test set

WHY THIS MATTERS:
This is a simplified version of what happens inside BERT/GPT:
1. Tokenize text → IDs
2. Convert IDs → vectors (here: bag-of-words; in BERT: embeddings + attention)
3. Pass through neural network layers
4. Output prediction

Understanding this flow makes Transformers (Module 1) and fine-tuning
(Module 3) far less mysterious. You'll see that an LLM is "just" a more
sophisticated version of what you build here.

ESTIMATED TIME: 45-60 minutes

SKILLS PRACTICED:
- Tensor creation and manipulation
- nn.Module with custom forward pass
- Training loop (forward, loss, backward, step)
- DataLoader for batching
- model.train() / model.eval() switching
- torch.no_grad() for inference

RULES:
- Use only PyTorch + NumPy (no sklearn, no HuggingFace)
- No GPU required (runs on CPU)
- Follow the TODOs in order
=============================================================================
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from collections import Counter


# =============================================================================
# SETUP: Training data (simple movie reviews)
# =============================================================================

TRAIN_DATA = [
    ("This movie was absolutely wonderful and amazing", 1),
    ("Terrible waste of time boring awful", 0),
    ("I loved every minute great film", 1),
    ("Worst movie ever seen disappointing", 0),
    ("Beautiful cinematography excellent acting", 1),
    ("Dull predictable plot terrible script", 0),
    ("Highly entertaining fun exciting", 1),
    ("Horrible acting ruined the entire movie", 0),
    ("A masterpiece of modern cinema brilliant", 1),
    ("So boring I fell asleep unwatchable", 0),
    ("Wonderful story well directed loved it", 1),
    ("Awful film no redeeming qualities", 0),
    ("Great performances by the entire cast", 1),
    ("Terrible direction confusing plot pointless", 0),
    ("Incredible movie truly inspiring beautiful", 1),
    ("Worst experience at the cinema ever", 0),
    ("Loved this film fantastic storytelling", 1),
    ("Bad acting bad writing bad everything", 0),
    ("Superb direction and amazing soundtrack", 1),
    ("Painfully slow and utterly boring", 0),
    ("This was genuinely enjoyable and heartwarming", 1),
    ("Complete disaster from start to finish", 0),
    ("Delightful charming and very funny", 1),
    ("Unbearable to watch just terrible", 0),
    ("Outstanding performance truly remarkable film", 1),
    ("Mediocre at best mostly disappointing", 0),
    ("Absolutely loved this heartfelt story", 1),
    ("Dreadful film wasted my evening completely", 0),
    ("Perfect blend of humor and drama wonderful", 1),
    ("Forgettable and uninspired waste of talent", 0),
]

TEST_DATA = [
    ("Amazing film wonderful experience", 1),
    ("Terrible movie hated it", 0),
    ("Great story beautiful acting", 1),
    ("Boring slow waste of time", 0),
    ("Loved it fantastic brilliant", 1),
    ("Awful disappointing terrible film", 0),
    ("Excellent direction superb cast", 1),
    ("Worst movie painfully bad", 0),
]


# =============================================================================
# TODO 1: Build Vocabulary
# =============================================================================
# Create a mapping from words → integer indices.
# Steps:
#   a) Tokenize all training sentences (lowercase, split by space)
#   b) Collect all unique words
#   c) Assign each word an index (starting from 0)
#   d) Return word2idx dict and vocabulary size
#
# Example: {"this": 0, "movie": 1, "was": 2, ...}

def build_vocabulary(data):
    """Build word-to-index mapping from training data."""
    # TODO: Tokenize all sentences
    # TODO: Collect unique words
    # TODO: Create word2idx dict
    # TODO: Return word2idx, vocab_size
    pass


# =============================================================================
# TODO 2: Encode Text as Bag-of-Words
# =============================================================================
# Convert a sentence to a fixed-size vector:
#   - Vector length = vocabulary size
#   - vector[i] = number of times word i appears in the sentence
#   - Unknown words (not in vocab) are ignored
#
# Example: "the movie was great" → [0, 1, 1, 1, 0, ...] (count at each word's index)

def text_to_bow(text, word2idx, vocab_size):
    """Convert text to bag-of-words tensor."""
    # TODO: Tokenize (lowercase, split)
    # TODO: Create zero vector of size vocab_size
    # TODO: For each word, increment its index in the vector
    # TODO: Return as torch.FloatTensor
    pass


# =============================================================================
# TODO 3: Prepare Datasets
# =============================================================================
# Convert all train and test data to tensors:
#   - X = stack of bag-of-words vectors (shape: n_samples × vocab_size)
#   - y = labels tensor (shape: n_samples)
# Create DataLoaders with batch_size=8.

def prepare_data(train_data, test_data, word2idx, vocab_size):
    """Prepare DataLoaders for training and testing."""
    # TODO: Encode all texts to BoW vectors
    # TODO: Stack into X tensors
    # TODO: Create y tensors (float for BCELoss)
    # TODO: Create TensorDatasets and DataLoaders
    # Return train_loader, test_loader, X_test, y_test
    pass


# =============================================================================
# TODO 4: Define the Model
# =============================================================================
# Create a neural network for binary sentiment classification:
#   Input: vocab_size features
#   Hidden 1: 64 neurons + ReLU + Dropout(0.3)
#   Hidden 2: 32 neurons + ReLU
#   Output: 1 neuron (sigmoid for binary probability)
#
# Use nn.Sequential for simplicity.

class SentimentClassifier(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        # TODO: Define layers
        pass

    def forward(self, x):
        # TODO: Pass through layers, return output
        pass


# =============================================================================
# TODO 5: Training Loop
# =============================================================================
# Train the model for 50 epochs:
#   - Loss: BCELoss (binary cross-entropy)
#   - Optimizer: Adam, lr=0.001
#   - Print loss every 10 epochs
#   - Track losses for potential plotting

def train_model(model, train_loader, num_epochs=50, lr=0.001):
    """Train the sentiment classifier."""
    # TODO: Define criterion (BCELoss) and optimizer (Adam)
    # TODO: Training loop with forward, loss, backward, step
    # TODO: Print loss every 10 epochs
    # TODO: Return list of epoch losses
    pass


# =============================================================================
# TODO 6: Evaluation
# =============================================================================
# Evaluate on test set:
#   a) Switch to eval mode
#   b) Disable gradient tracking
#   c) Forward pass on test data
#   d) Convert probabilities to binary predictions (threshold=0.5)
#   e) Compute accuracy
#   f) Print predictions vs actual for each test sample

def evaluate_model(model, X_test, y_test, test_texts):
    """Evaluate model and print results."""
    # TODO: model.eval(), torch.no_grad()
    # TODO: Forward pass
    # TODO: threshold at 0.5
    # TODO: Compute accuracy
    # TODO: Print each prediction with text
    pass


# =============================================================================
# TODO 7: Predict on New Text
# =============================================================================
# Create a function that takes raw text and returns sentiment:

def predict_sentiment(model, text, word2idx, vocab_size):
    """Predict sentiment for a single text string."""
    # TODO: Convert text to BoW
    # TODO: model.eval(), no_grad
    # TODO: Forward pass
    # TODO: Return "Positive" or "Negative" with confidence score
    pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("TEXT SENTIMENT CLASSIFIER (PyTorch)")
    print("=" * 60)

    # Step 1: Vocabulary
    print("\n--- STEP 1: BUILD VOCABULARY ---")
    word2idx, vocab_size = build_vocabulary(TRAIN_DATA)
    print(f"Vocabulary size: {vocab_size}")
    print(f"Sample words: {list(word2idx.items())[:5]}")

    # Step 2: Prepare data
    print("\n--- STEP 2: PREPARE DATA ---")
    train_loader, test_loader, X_test, y_test = prepare_data(
        TRAIN_DATA, TEST_DATA, word2idx, vocab_size
    )
    print(f"Training batches: {len(train_loader)}")
    print(f"Test samples: {len(X_test)}")

    # Step 3: Model
    print("\n--- STEP 3: DEFINE MODEL ---")
    model = SentimentClassifier(vocab_size)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Model architecture:\n{model}")
    print(f"Total parameters: {total_params}")

    # Step 4: Train
    print("\n--- STEP 4: TRAINING ---")
    losses = train_model(model, train_loader, num_epochs=50)

    # Step 5: Evaluate
    print("\n--- STEP 5: EVALUATION ---")
    test_texts = [text for text, _ in TEST_DATA]
    evaluate_model(model, X_test, y_test, test_texts)

    # Step 6: Predict new
    print("\n--- STEP 6: NEW PREDICTIONS ---")
    new_texts = [
        "This was an incredible and moving film",
        "Absolutely hated this boring terrible movie",
        "Decent movie nothing special",
    ]
    for text in new_texts:
        result = predict_sentiment(model, text, word2idx, vocab_size)
        print(f"  '{text}' → {result}")

    # Step 7: Save
    print("\n--- STEP 7: SAVE MODEL ---")
    torch.save(model.state_dict(), "sentiment_model.pth")
    print("Model saved to sentiment_model.pth")

    print("\n" + "=" * 60)
    print("Done! You've built a neural text classifier from scratch.")
    print("=" * 60)


if __name__ == "__main__":
    main()
