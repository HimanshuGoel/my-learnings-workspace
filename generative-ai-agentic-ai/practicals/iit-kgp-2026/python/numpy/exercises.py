"""
NumPy Exercises — 15 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. AI-relevant exercises are marked with [AI].
Run: python exercises.py
"""

import numpy as np

# =============================================================================
# EASY (1-5)
# =============================================================================

# Exercise 1: Array Creation & Properties
# Create a 4×5 array of zeros, then change the dtype to int32.
# Print its shape, ndim, size, and dtype.
# Expected output:
#   Shape: (4, 5)
#   Ndim: 2
#   Size: 20
#   Dtype: int32

def exercise_1():
    # Your code here
    pass


# Exercise 2: Arange & Reshape
# Create a 1D array of numbers 1 through 20, then reshape it to a 4×5 matrix.
# Print the matrix and its shape.
# Expected output:
#   [[ 1  2  3  4  5]
#    [ 6  7  8  9 10]
#    [11 12 13 14 15]
#    [16 17 18 19 20]]

def exercise_2():
    # Your code here
    pass


# Exercise 3: Basic Slicing
# Given the matrix below, extract:
#   a) The second row
#   b) The third column
#   c) The 2×2 sub-matrix from the bottom-right corner
# Expected output:
#   Row: [4, 5, 6]
#   Col: [3, 6, 9]
#   Corner: [[5, 6], [8, 9]]

def exercise_3():
    matrix = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])
    # Your code here
    pass


# Exercise 4: Boolean Filtering
# Given an array of exam scores, find and print:
#   a) All scores above 80
#   b) The count of failing scores (below 60)
#   c) Replace all failing scores with 60 (grade floor)
# Expected output:
#   Above 80: [85, 92, 88, 95]
#   Failing count: 2
#   After floor: [72, 85, 60, 92, 60, 88, 65, 95]

def exercise_4():
    scores = np.array([72, 85, 45, 92, 58, 88, 65, 95])
    # Your code here
    pass


# Exercise 5: Vectorized Math
# A shop has item prices in USD. Convert all to INR (1 USD = 83.5 INR)
# and calculate the total revenue if quantities sold are given.
# Expected output:
#   INR prices: [835.  1670.  4175.  2505. ]
#   Total revenue: 45925.0

def exercise_5():
    usd_prices = np.array([10.0, 20.0, 50.0, 30.0])
    quantities = np.array([3, 5, 2, 4])
    # Your code here (revenue = sum of price_inr * quantity)
    pass


# =============================================================================
# MEDIUM (6-10)
# =============================================================================

# Exercise 6: Broadcasting [AI]
# You have a dataset with 4 samples and 3 features.
# Subtract the column mean from each element (center the data).
# This is the first step in standardization — required before training most ML models.
# Expected output (approx):
#   [[-1.5, -1.5, -1.5],
#    [-0.5, -0.5, -0.5],
#    [ 0.5,  0.5,  0.5],
#    [ 1.5,  1.5,  1.5]]

def exercise_6():
    # Each row = one sample, each column = one feature
    data = np.array([[1.0, 10.0, 100.0],
                     [2.0, 20.0, 200.0],
                     [3.0, 30.0, 300.0],
                     [4.0, 40.0, 400.0]])
    # Your code here: subtract column means using broadcasting
    pass


# Exercise 7: Min-Max Normalization [AI]
# Normalize each feature (column) to the range [0, 1].
# Formula: (x - min) / (max - min) per column.
# This is standard preprocessing before feeding data to neural networks.
# Expected output:
#   [[0.   0.   0.  ]
#    [0.25 0.5  0.2 ]
#    [0.5  0.75 0.6 ]
#    [1.   1.   1.  ]]

def exercise_7():
    data = np.array([[10.0, 2.0, 100.0],
                     [20.0, 4.0, 200.0],
                     [30.0, 5.0, 400.0],
                     [50.0, 8.0, 600.0]])
    # Your code here
    pass


# Exercise 8: Matrix Multiplication
# Multiply a (3×2) matrix by a (2×4) matrix.
# Verify the output shape is (3×4).
# Then compute the dot product of two 1D vectors and print the scalar result.
# Expected output:
#   Product shape: (3, 4)
#   Dot product: 32

def exercise_8():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    B = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8]])
    vec_a = np.array([1, 2, 3])
    vec_b = np.array([4, 5, 6])
    # Your code here
    pass


# Exercise 9: Reshape for Model Input [AI]
# You have 8 grayscale images stored as flat arrays (each image = 16 pixels).
# Reshape them into the format a CNN expects: (batch_size, height, width, channels).
# batch_size=8, height=4, width=4, channels=1
# CNN = Convolutional Neural Network, a model architecture for image data.
# Expected output:
#   Input shape: (8, 16)
#   Model-ready shape: (8, 4, 4, 1)

def exercise_9():
    # Simulating 8 flattened grayscale images (4×4 pixels each)
    flat_images = np.random.randint(0, 256, size=(8, 16))
    # Your code here: reshape to (8, 4, 4, 1)
    pass


# Exercise 10: Statistical Analysis Along Axes
# Given monthly sales data for 3 products over 6 months,
# find: best month per product (argmax along correct axis),
# average monthly revenue, and total sales per product.
# Expected output:
#   Best month per product: [3, 5, 2]
#   Avg monthly revenue: [100.0, 120.0, 155.0, 175.0, 135.0, 165.0]
#   Total per product: [520, 500, 480]

def exercise_10():
    # Rows = products, Columns = months
    sales = np.array([[50, 60, 80, 120, 90, 120],   # Product A
                      [70, 80, 95, 85,  65, 105],   # Product B
                      [80, 100, 130, 145, 115, 110]]) # Product C — wait, let me fix
    # NOTE: these numbers are illustrative. Compute anyway and print results.
    # Your code here
    pass


# =============================================================================
# HARD (11-15)
# =============================================================================

# Exercise 11: Cosine Similarity [AI]
# Implement cosine similarity between two vectors WITHOUT using sklearn.
# cosine_sim = dot(a, b) / (norm(a) * norm(b))
# Then compute similarity between a query and 5 stored document embeddings.
# Return the index of the most similar document.
# embedding = a numerical vector representation of text, used in search/RAG systems.
# Expected output:
#   Similarities: [0.98, 0.71, 0.45, 0.89, 0.62] (approx)
#   Most similar document index: 0

def exercise_11():
    query = np.array([0.5, 0.3, 0.8, 0.1, 0.9])
    documents = np.array([
        [0.4, 0.3, 0.9, 0.1, 0.8],   # doc 0
        [0.1, 0.9, 0.2, 0.8, 0.3],   # doc 1
        [0.9, 0.1, 0.1, 0.9, 0.1],   # doc 2
        [0.3, 0.4, 0.7, 0.2, 0.7],   # doc 3
        [0.2, 0.8, 0.3, 0.7, 0.4],   # doc 4
    ])
    # Your code here
    pass


# Exercise 12: Softmax Function [AI]
# Implement the softmax function: softmax(x_i) = exp(x_i) / sum(exp(x_j))
# This converts raw model outputs (logits) into probabilities that sum to 1.
# logits = raw scores from the last layer of a neural network, before conversion to probabilities.
# Apply it to a batch of 3 samples (2D array, softmax per row).
# Expected: each row sums to 1.0

def exercise_12():
    # 3 samples, 4 classes each (e.g., classifying into 4 categories)
    logits = np.array([[2.0, 1.0, 0.1, 0.5],
                       [0.1, 3.0, 0.2, 0.7],
                       [1.0, 1.0, 1.0, 1.0]])
    # Your code here: implement stable softmax (subtract max per row first)
    # Expected: each row sums to ~1.0, highest logit gets highest probability
    pass


# Exercise 13: Batch Cosine Similarity Matrix [AI]
# Given N document embeddings (N×D matrix), compute the full N×N similarity matrix.
# similarity[i][j] = cosine similarity between doc i and doc j.
# The diagonal should be 1.0 (each doc is perfectly similar to itself).
# This is how search engines pre-compute document relationships.
# Expected output: a 4×4 matrix with 1.0 on the diagonal.

def exercise_13():
    # 4 documents, each with 6-dimensional embedding
    embeddings = np.array([
        [0.1, 0.3, 0.5, 0.7, 0.2, 0.4],
        [0.9, 0.1, 0.2, 0.3, 0.8, 0.1],
        [0.2, 0.4, 0.6, 0.8, 0.3, 0.5],
        [0.8, 0.2, 0.1, 0.4, 0.7, 0.2],
    ])
    # Your code here: compute full similarity matrix using vectorized operations
    # Hint: normalize each row, then matrix multiply by its transpose
    pass


# Exercise 14: Implement Cross-Entropy Loss [AI]
# Cross-entropy loss measures how wrong a classification model's predictions are.
# Formula: -sum(y_true * log(y_pred)) averaged over samples.
# y_true = one-hot encoded true labels
# y_pred = predicted probabilities (from softmax)
# Lower loss = better predictions.
# Expected output: a single float (the loss value)

def exercise_14():
    # 4 samples, 3 classes
    y_true = np.array([[1, 0, 0],
                       [0, 1, 0],
                       [0, 0, 1],
                       [1, 0, 0]])

    y_pred = np.array([[0.9, 0.05, 0.05],
                       [0.1, 0.8,  0.1],
                       [0.2, 0.3,  0.5],
                       [0.7, 0.2,  0.1]])
    # Your code here
    # Hint: add small epsilon (1e-15) to y_pred to avoid log(0)
    pass


# Exercise 15: K-Nearest Neighbors (Distance Calculation) [AI]
# Given a query point and a dataset of points, find the K closest points
# using Euclidean distance. Return their indices.
# KNN = a classification algorithm that labels a point based on its closest neighbors.
# Expected output: indices of the 3 closest points to the query.

def exercise_15():
    # 10 points in 3D space
    dataset = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [1.5, 2.5, 3.5],
        [7.0, 8.0, 9.0],
        [1.2, 2.2, 3.2],
        [5.0, 5.0, 5.0],
        [0.8, 1.8, 2.8],
        [3.0, 3.0, 3.0],
        [6.0, 7.0, 8.0],
        [2.0, 2.0, 2.0],
    ])
    query = np.array([1.0, 2.0, 3.0])
    k = 3
    # Your code here: compute Euclidean distance from query to all points,
    # then return indices of k smallest distances.
    # Hint: np.linalg.norm with axis parameter, then np.argsort
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
