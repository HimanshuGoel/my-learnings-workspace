"""
PyTorch Exercises — 15 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. AI-relevant exercises are marked with [AI].
Run: python exercises.py
(No GPU required — all exercises run on CPU)
"""

import torch
import torch.nn as nn
import numpy as np

# =============================================================================
# EASY (1-5)
# =============================================================================

# Exercise 1: Tensor Creation & Properties
# Create tensors using different methods. Print shape, dtype, and device.
# a) 3×4 zeros (float32)
# b) 2×3 random normal
# c) 1D tensor from a Python list [10, 20, 30, 40, 50]
# d) 4×4 identity matrix
# Expected: correct shapes and types printed

def exercise_1():
    # Your code here
    pass


# Exercise 2: NumPy ↔ PyTorch Conversion
# a) Create a NumPy array of shape (3, 4) with values 1-12
# b) Convert to PyTorch tensor
# c) Modify the tensor (multiply by 2)
# d) Convert back to NumPy
# e) Verify the NumPy array was also modified (shared memory!)
# Expected: demonstrate shared memory behavior

def exercise_2():
    # Your code here
    pass


# Exercise 3: Tensor Operations
# Given two tensors a and b:
#   a) Element-wise addition, multiplication
#   b) Matrix multiplication (a @ b.T)
#   c) Sum along axis 0 and axis 1
#   d) Find argmax along axis 1 (which column has max value per row?)
# Expected: correct results for each operation

def exercise_3():
    a = torch.tensor([[1.0, 2.0, 3.0],
                      [4.0, 5.0, 6.0]])
    b = torch.tensor([[7.0, 8.0, 9.0],
                      [10.0, 11.0, 12.0]])
    # Your code here
    pass


# Exercise 4: Reshaping Tensors
# a) Create tensor of shape (2, 3, 4) with values 0-23
# b) Reshape to (6, 4)
# c) Reshape to (24,) (flatten)
# d) Add a batch dimension: (2,3,4) → (1,2,3,4) using unsqueeze
# e) Remove it back using squeeze
# Expected: correct shapes after each operation

def exercise_4():
    # Your code here
    pass


# Exercise 5: Autograd Basics [AI]
# Demonstrate automatic differentiation:
# a) Create x = tensor([3.0]), requires_grad=True
# b) Compute y = x^3 + 2*x^2 + x
# c) Call y.backward()
# d) Print x.grad (should be dy/dx = 3x^2 + 4x + 1 = 27 + 12 + 1 = 40)
# autograd = automatic computation of derivatives (how the model "learns")
# Expected: x.grad = 40.0

def exercise_5():
    # Your code here
    pass


# =============================================================================
# MEDIUM (6-10)
# =============================================================================

# Exercise 6: Define a Neural Network [AI]
# Create a simple feedforward network using nn.Module:
#   Input: 10 features
#   Hidden layer 1: 64 neurons + ReLU
#   Hidden layer 2: 32 neurons + ReLU
#   Output: 3 classes
# Print the model architecture and total parameter count.
# neural network = function with millions of adjustable parameters that learns patterns
# Expected: model summary and param count (~3000-4000 parameters)

def exercise_6():
    # Your code here: define class, instantiate, count params
    pass


# Exercise 7: Forward Pass [AI]
# Create a model from Exercise 6 and pass a batch of data through it.
# a) Create random input: batch of 8 samples, 10 features each
# b) Pass through model (forward pass)
# c) Print output shape (should be 8×3)
# d) Apply softmax to get probabilities
# e) Get predicted class for each sample (argmax)
# forward pass = computing the model's output for given input
# Expected: output shape (8, 3), predictions shape (8,)

def exercise_7():
    # Your code here (reuse model from ex6 or define new)
    pass


# Exercise 8: Loss Functions [AI]
# Compute loss for a classification task:
# a) Create fake model output (logits): shape (4, 3) — 4 samples, 3 classes
# b) Create true labels: [0, 2, 1, 0]
# c) Compute CrossEntropyLoss
# d) Also compute for "perfect" predictions and "terrible" predictions
# e) Verify: better predictions → lower loss
# loss = single number measuring how wrong predictions are (lower = better)
# Expected: perfect_loss < real_loss < terrible_loss

def exercise_8():
    # Your code here
    pass


# Exercise 9: Single Training Step [AI]
# Perform ONE complete training step:
# a) Define model, criterion (CrossEntropyLoss), optimizer (Adam)
# b) Create one batch of random data (16 samples, 10 features, 3 classes)
# c) Forward pass → loss → backward → step
# d) Print loss before and after the step (should decrease)
# This is the atomic unit of neural network training.
# Expected: loss_after < loss_before

def exercise_9():
    # Your code here
    pass


# Exercise 10: DataLoader [AI]
# Create a DataLoader and iterate through it:
# a) Generate 100 samples (10 features) and labels (3 classes)
# b) Wrap in TensorDataset
# c) Create DataLoader with batch_size=16, shuffle=True
# d) Iterate through ALL batches, print each batch's shape
# e) Verify: 100 samples / 16 batch_size = 6 full batches + 1 partial
# DataLoader = handles batching, shuffling, and parallel loading
# Expected: 7 batches (6×16 + 1×4)

def exercise_10():
    from torch.utils.data import DataLoader, TensorDataset
    # Your code here
    pass


# =============================================================================
# HARD (11-15)
# =============================================================================

# Exercise 11: Complete Training Loop [AI]
# Train a classifier for 20 epochs on synthetic data:
# a) Generate: 500 samples, 20 features, 4 classes (use make_classification)
# b) Split into train (400) and test (100)
# c) Create DataLoaders
# d) Define model, loss, optimizer
# e) Write full training loop (20 epochs)
# f) Print loss every 5 epochs
# g) Evaluate on test set, print accuracy
# Expected: loss decreases, accuracy > 0.7

def exercise_11():
    from sklearn.datasets import make_classification
    from torch.utils.data import DataLoader, TensorDataset
    # Your code here: full training pipeline
    pass


# Exercise 12: Embedding Layer [AI]
# Demonstrate how nn.Embedding works (foundational for Transformers):
# a) Create vocabulary of size 1000, embedding dimension 64
# b) Create input: batch of 4 sentences, each 10 token IDs
# c) Pass through embedding layer
# d) Print output shape (should be 4×10×64)
# e) Verify: same token ID always maps to same vector
# embedding = lookup table that maps integer IDs to dense vectors
# This is the FIRST layer in every LLM (GPT, BERT, etc.)
# Expected: output shape (4, 10, 64)

def exercise_12():
    # Your code here
    pass


# Exercise 13: Transfer Learning Setup [AI]
# Simulate fine-tuning a pre-trained model:
# a) Create a "pre-trained" model (3 layers, trained = has random weights)
# b) Freeze all layers (requires_grad = False)
# c) Replace the final layer with a new one for 5 classes
# d) Verify: only new layer has requires_grad=True
# e) Count trainable vs frozen parameters
# This is exactly what happens when you fine-tune BERT for a new task.
# Expected: most params frozen, only final layer trainable

def exercise_13():
    # Your code here
    pass


# Exercise 14: Custom Loss Function [AI]
# Implement a custom loss function (Focal Loss):
# Focal Loss reduces the contribution of easy examples, focusing on hard ones.
# Formula: FL = -alpha * (1 - p_t)^gamma * log(p_t)
# Where p_t = probability assigned to the true class.
# This is used for heavily imbalanced datasets (e.g., object detection).
# a) Implement as a function taking (logits, targets) → scalar loss
# b) Compare with standard CrossEntropyLoss on same input
# Expected: focal loss penalizes confident wrong predictions more

def exercise_14():
    # Your code here
    # Hint: use nn.functional.cross_entropy as reference
    pass


# Exercise 15: Attention Mechanism (Simplified) [AI]
# Implement scaled dot-product attention from scratch:
# attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V
# a) Create Q, K, V tensors: batch=2, seq_len=5, d_k=8
# b) Compute attention scores: Q @ K^T / sqrt(d_k)
# c) Apply softmax along last dimension
# d) Multiply by V to get output
# e) Verify output shape: (2, 5, 8) — same as input
# This is the core computation inside every Transformer (GPT, BERT).
# Expected: output shape (2, 5, 8), attention weights sum to 1 per row

def exercise_15():
    # Your code here
    pass


# =============================================================================
# Run all exercises
# =============================================================================

if __name__ == "__main__":
    exercises = [exercise_1, exercise_2, exercise_3, exercise_4, exercise_5,
                 exercise_6, exercise_7, exercise_8, exercise_9, exercise_10,
                 exercise_11, exercise_12, exercise_13, exercise_14, exercise_15]

    for i, ex in enumerate(exercises, 1):
        print(f"\n{'='*60}")
        print(f"Exercise {i}")
        print('='*60)
        ex()
