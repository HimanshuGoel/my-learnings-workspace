"""
Scikit-Learn Exercises — 15 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. AI-relevant exercises are marked with [AI].
Run: python exercises.py
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression, load_iris

# =============================================================================
# EASY (1-5)
# =============================================================================

# Exercise 1: Train/Test Split
# Load the iris dataset, split into 80/20 train/test.
# Print shapes of all 4 resulting arrays.
# Verify class proportions are preserved (use stratify).
# Expected output:
#   X_train: (120, 4), X_test: (30, 4)
#   y_train: (120,), y_test: (30,)
#   Class proportions preserved: True

def exercise_1():
    from sklearn.model_selection import train_test_split
    iris = load_iris()
    X, y = iris.data, iris.target
    # Your code here
    pass


# Exercise 2: Fit / Predict / Score
# Train a LogisticRegression on iris data.
# Print training accuracy and test accuracy.
# Print first 5 predictions vs actual values.
# Expected output:
#   Train accuracy: ~0.97
#   Test accuracy: ~0.97
#   Predictions: [0, 0, 2, ...] Actual: [0, 0, 2, ...]

def exercise_2():
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    # Your code here: instantiate, fit, predict, score
    pass


# Exercise 3: Preprocessing — StandardScaler
# Scale the iris features using StandardScaler.
# Print mean and std of first feature before and after scaling.
# Expected output:
#   Before: mean=5.84, std=0.83
#   After: mean≈0.0, std≈1.0

def exercise_3():
    from sklearn.preprocessing import StandardScaler
    iris = load_iris()
    X = iris.data
    # Your code here: fit scaler on X, transform, verify mean/std
    pass


# Exercise 4: Cross-Validation
# Evaluate a RandomForestClassifier on iris using 5-fold cross-validation.
# Print mean accuracy ± std.
# Expected output:
#   CV Accuracy: 0.960 ± 0.027 (approximately)

def exercise_4():
    from sklearn.model_selection import cross_val_score
    from sklearn.ensemble import RandomForestClassifier
    iris = load_iris()
    X, y = iris.data, iris.target
    # Your code here
    pass


# Exercise 5: Classification Report
# Train a KNeighborsClassifier on iris, predict on test set.
# Print the full classification report (precision, recall, F1 per class).
# Expected output: a table with per-class metrics

def exercise_5():
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import classification_report
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    # Your code here: train, predict, print classification_report
    pass


# =============================================================================
# MEDIUM (6-10)
# =============================================================================

# Exercise 6: Pipeline [AI]
# Build a Pipeline that:
#   1. Scales features (StandardScaler)
#   2. Trains a Logistic Regression
# Evaluate with 5-fold cross-validation.
# pipeline = preprocessing + model bundled together to prevent data leakage
# Expected output: CV accuracy ~0.96

def exercise_6():
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    iris = load_iris()
    X, y = iris.data, iris.target
    # Your code here: build pipeline, cross_val_score
    pass


# Exercise 7: Model Comparison [AI]
# Compare 4 models on a binary classification dataset:
#   - Logistic Regression
#   - Random Forest
#   - Gradient Boosting
#   - SVM
# Use 5-fold CV with F1 scoring. Print results sorted by score.
# F1 = harmonic mean of precision and recall (best single metric for imbalanced data)
# Expected output: ranked list of models with mean F1 ± std

def exercise_7():
    from sklearn.model_selection import cross_val_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    X, y = make_classification(n_samples=500, n_features=20,
                               n_informative=10, random_state=42)
    # Your code here: loop over models, evaluate, sort
    pass


# Exercise 8: Hyperparameter Tuning [AI]
# Use GridSearchCV to find the best Random Forest hyperparameters:
#   - n_estimators: [50, 100, 200]
#   - max_depth: [3, 5, 10, None]
# Use 5-fold CV, F1 scoring.
# hyperparameter = model setting you choose BEFORE training (not learned from data)
# Print best params and best score.

def exercise_8():
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import RandomForestClassifier
    X, y = make_classification(n_samples=500, n_features=20,
                               n_informative=10, random_state=42)
    # Your code here
    pass


# Exercise 9: Feature Importance [AI]
# Train a Random Forest and extract feature importances.
# Print top 5 most important features with their scores.
# feature importance = how much each feature contributes to predictions
# Expected output: sorted list of top 5 features

def exercise_9():
    from sklearn.ensemble import RandomForestClassifier
    X, y = make_classification(n_samples=500, n_features=10,
                               n_informative=5, random_state=42)
    feature_names = [f"feature_{i}" for i in range(10)]
    # Your code here: train, get feature_importances_, sort, print top 5
    pass


# Exercise 10: Confusion Matrix Analysis [AI]
# Train a model on imbalanced data, compute confusion matrix.
# Calculate: true positives, false positives, false negatives, true negatives.
# Explain what each means in a real context (e.g., spam detection).
# confusion matrix = table of correct vs incorrect predictions per class
# Expected output: cm values + interpretation

def exercise_10():
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import confusion_matrix
    # Create imbalanced dataset (90% class 0, 10% class 1)
    X, y = make_classification(n_samples=1000, n_features=10,
                               weights=[0.9, 0.1], random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    # Your code here: train, predict, confusion_matrix, interpret
    pass


# =============================================================================
# HARD (11-15)
# =============================================================================

# Exercise 11: Full ML Pipeline with ColumnTransformer [AI]
# Build a complete pipeline for mixed-type data:
#   - Numeric columns: StandardScaler
#   - Categorical columns: OneHotEncoder
#   - Model: GradientBoostingClassifier
# Evaluate with cross-validation.
# ColumnTransformer = apply different preprocessing to different column types
# Expected output: CV F1 score

def exercise_11():
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import cross_val_score

    # Synthetic mixed-type dataset
    rng = np.random.default_rng(42)
    n = 500
    df = pd.DataFrame({
        "age": rng.integers(18, 65, n),
        "income": rng.normal(60000, 20000, n),
        "tenure": rng.integers(1, 20, n),
        "city": rng.choice(["NYC", "LA", "Chicago", "Houston"], n),
        "plan": rng.choice(["Basic", "Premium", "Enterprise"], n),
    })
    y = (df["income"] > 70000).astype(int).values
    # Your code here: build ColumnTransformer + Pipeline, evaluate
    pass


# Exercise 12: Learning Curve Analysis [AI]
# Plot how training and validation scores change as training set size increases.
# This reveals: underfitting (both scores low) vs overfitting (gap between them).
# learning curve = model performance as a function of training data amount
# Expected output: description of what the curve shows (no actual plot needed)

def exercise_12():
    from sklearn.model_selection import learning_curve
    from sklearn.ensemble import RandomForestClassifier
    X, y = make_classification(n_samples=1000, n_features=20,
                               n_informative=10, random_state=42)
    # Your code here:
    # Use learning_curve() to get train_sizes, train_scores, test_scores
    # Print average train/test score at each size
    # Interpret: is the model underfitting or overfitting?
    pass


# Exercise 13: Text Classification with TF-IDF [AI]
# Build a text classifier using TF-IDF + Logistic Regression pipeline.
# Classify movie reviews as positive or negative.
# TF-IDF = term frequency-inverse document frequency (converts text to numbers)
# Expected output: classification accuracy on test set

def exercise_13():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split

    # Synthetic movie reviews
    texts = [
        "This movie was amazing and wonderful",
        "Terrible film, waste of time",
        "Great acting and beautiful cinematography",
        "Boring and predictable plot",
        "Loved every minute of it",
        "Awful, couldn't finish watching",
        "A masterpiece of modern cinema",
        "Dull and uninspiring performance",
        "Brilliant direction and screenplay",
        "One of the worst movies ever made",
        "Highly entertaining and fun",
        "Disappointing and overrated",
        "Superb storytelling and characters",
        "Tedious and way too long",
        "An absolute delight to watch",
        "Horrible acting ruined it completely",
    ]
    labels = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]  # 1=positive, 0=negative
    # Your code here: TF-IDF pipeline, split, train, evaluate
    pass


# Exercise 14: Embeddings + Sklearn Classifier [AI]
# Simulate: take pre-computed embeddings from a language model,
# then train a sklearn classifier on top.
# This is the "embeddings as features" pattern used in Module 1.
# embedding = numerical vector produced by a pre-trained model (e.g., BERT)
# Expected output: accuracy of sklearn classifier on embeddings

def exercise_14():
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline

    # Simulate: 500 documents, each with 768-dim embedding (like BERT output)
    rng = np.random.default_rng(42)
    n_docs = 500
    n_classes = 5

    # Embeddings are NOT random — simulate clusters (like real embeddings)
    centers = rng.standard_normal((n_classes, 768))
    labels = rng.integers(0, n_classes, n_docs)
    embeddings = centers[labels] + rng.normal(0, 0.5, (n_docs, 768))
    # Your code here: split, build pipeline (scale + LogReg), cross-validate
    pass


# Exercise 15: Complete Model Selection Workflow [AI]
# Full workflow:
#   a) Split data (train/test)
#   b) Compare 3 models with cross-validation
#   c) Pick best model
#   d) Tune best model with GridSearchCV
#   e) Final evaluation on test set
#   f) Print confusion matrix and classification report
# This is the standard ML workflow for any classification task.
# Expected output: final test metrics for the tuned best model

def exercise_15():
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import classification_report, confusion_matrix

    X, y = make_classification(n_samples=1000, n_features=20,
                               n_informative=12, n_classes=3,
                               n_clusters_per_class=1, random_state=42)
    # Your code here: full workflow steps a-f
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
