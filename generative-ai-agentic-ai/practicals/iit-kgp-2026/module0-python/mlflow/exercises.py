"""
MLflow Exercises — 10 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. All exercises are AI-relevant.

SETUP: pip install mlflow scikit-learn
(No cloud services needed — all runs locally)

Run: python exercises.py
View: mlflow ui --port 5000 (after running exercises)
"""

import mlflow
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score

# =============================================================================
# EASY (1-4)
# =============================================================================

# Exercise 1: Basic Experiment Tracking
# a) Set experiment name to "exercise-tracking"
# b) Start a run named "first_run"
# c) Log 3 parameters: model_type, n_estimators, max_depth
# d) Log 2 metrics: accuracy, f1_score
# e) End the run
# f) Verify by printing the run ID
# Expected: run appears in mlflow UI

def exercise_1():
    # Your code here
    pass


# Exercise 2: Log Metrics Over Steps (Training Curve)
# Simulate a training loop:
# a) Start a run
# b) For 20 "epochs", log decreasing loss and increasing accuracy
# c) Log final metrics
# Expected: in mlflow UI, you can see loss/accuracy curves over steps

def exercise_2():
    # Simulated training metrics
    np.random.seed(42)
    losses = 2.0 * np.exp(-0.1 * np.arange(20)) + np.random.normal(0, 0.05, 20)
    accuracies = 0.5 + 0.4 * (1 - np.exp(-0.15 * np.arange(20)))
    # Your code here: log per-step metrics
    pass


# Exercise 3: Auto-Logging with Sklearn
# a) Enable mlflow.sklearn.autolog()
# b) Train a RandomForestClassifier (no manual logging needed!)
# c) Check that params, metrics, and model were automatically logged
# Expected: everything captured with zero manual mlflow calls

def exercise_3():
    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Your code here: autolog + train
    pass


# Exercise 4: Log Artifacts
# a) Create a simple text file with experiment notes
# b) Create a CSV with feature importances
# c) Log both as artifacts
# d) Verify they appear in the run's artifact viewer
# Expected: files downloadable from mlflow UI

def exercise_4():
    import os
    # Your code here: create files, log as artifacts, cleanup
    pass


# =============================================================================
# MEDIUM (5-7)
# =============================================================================

# Exercise 5: Compare Multiple Models
# Train 4 models on the same data, logging each as a separate run:
#   - Logistic Regression
#   - Random Forest (100 trees)
#   - Random Forest (200 trees)
#   - Gradient Boosting
# All in the same experiment. Log model type, params, and F1 score.
# Expected: 4 runs visible in UI, sortable by F1

def exercise_5():
    mlflow.set_experiment("model-comparison")
    X, y = make_classification(n_samples=1000, n_features=20,
                               n_informative=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Your code here: train each model in its own run
    pass


# Exercise 6: Search and Find Best Run
# After Exercise 5:
# a) Use mlflow.search_runs() to find all runs in "model-comparison"
# b) Filter: F1 > 0.80
# c) Sort by F1 descending
# d) Print the best run's params and metrics
# e) Get the best run's ID (for model loading)
# Expected: programmatically find the best performing experiment

def exercise_6():
    # Your code here: search_runs with filters
    pass


# Exercise 7: Register a Model
# a) Train a model and log it with registered_model_name
# b) Load it back from the registry
# c) Make predictions with the loaded model
# d) Verify predictions match
# Expected: model accessible by name (not just run ID)

def exercise_7():
    X, y = make_classification(n_samples=200, n_features=5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Your code here: train, log with registered name, load, predict
    pass


# =============================================================================
# HARD (8-10)
# =============================================================================

# Exercise 8: Hyperparameter Sweep with Tracking
# Run a grid of hyperparameter combinations, logging each:
#   n_estimators: [50, 100, 200]
#   max_depth: [3, 5, 10]
# That's 9 runs. Find the best combination.
# This replaces manual GridSearchCV — you get visual comparison for free.
# Expected: 9 runs logged, best combo identifiable in UI

def exercise_8():
    mlflow.set_experiment("hyperparam-sweep")
    X, y = make_classification(n_samples=500, n_features=15, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Your code here: nested loop over params, log each
    pass


# Exercise 9: Custom Python Model (PyFunc)
# Create a custom model wrapper using mlflow.pyfunc:
# a) Define a class that wraps any sklearn model + preprocessing
# b) Log it as a pyfunc model
# c) Load and use for prediction
# This is how you deploy complex pipelines (preprocessing + model together).
# Expected: custom model logged, loaded, and working

def exercise_9():
    # Your code here: define PythonModel class, log, load, predict
    pass


# Exercise 10: Complete ML Lifecycle
# Full workflow:
# a) Create experiment "lifecycle-demo"
# b) Train 3 models with different params (log all)
# c) Find the best model (search_runs)
# d) Register the best model
# e) Load from registry
# f) Make predictions
# g) Log evaluation metrics as a new run (linked to the model)
# This is the complete MLOps workflow you'll use in Module 5.
# Expected: end-to-end lifecycle from training to deployment

def exercise_10():
    # Your code here: complete lifecycle
    pass


# =============================================================================
# Run all exercises
# =============================================================================

if __name__ == "__main__":
    exercises = [exercise_1, exercise_2, exercise_3, exercise_4, exercise_5,
                 exercise_6, exercise_7, exercise_8, exercise_9, exercise_10]

    for i, ex in enumerate(exercises, 1):
        print(f"\n{'='*60}")
        print(f"Exercise {i}")
        print('='*60)
        try:
            ex()
        except Exception as e:
            print(f"  [Error: {type(e).__name__}: {e}]")

    print("\n\n" + "="*60)
    print("View results: mlflow ui --port 5000")
    print("Open: http://localhost:5000")
    print("="*60)
