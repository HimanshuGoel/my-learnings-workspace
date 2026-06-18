"""
=============================================================================
MINI PROJECT: ML Experiment Dashboard (Train → Track → Compare → Deploy)
=============================================================================

PROBLEM STATEMENT:
Build a complete experiment tracking workflow: train multiple models with
different configurations, track everything in MLflow, find the best one,
register it, and prepare it for deployment.

WHAT YOU'LL BUILD:
- Automated training of 6+ model configurations
- Full MLflow tracking (params, metrics, artifacts)
- Programmatic run comparison and best model selection
- Model registry with version staging
- Deployment-ready model loading

WHY THIS MATTERS:
Module 5 capstone evaluation includes "experiment documentation." MLflow
provides this automatically. This project gives you a reusable template
for tracking ANY ML experiment — classification, fine-tuning, RAG evaluation.

ESTIMATED TIME: 30-45 minutes

SETUP: pip install mlflow scikit-learn matplotlib

RULES:
- Use MLflow for ALL tracking (no manual CSV/print-based tracking)
- Log at least: model type, hyperparams, metrics, model artifact
- Use autolog where possible
- Follow the TODOs in order

VIEW RESULTS: mlflow ui --port 5000 (after running)
=============================================================================
"""

import mlflow
import mlflow.sklearn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (f1_score, accuracy_score, precision_score,
                             recall_score, confusion_matrix, classification_report)
import os


# =============================================================================
# SETUP: Generate dataset
# =============================================================================

def create_dataset():
    """Create a realistic binary classification dataset."""
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=12,
        n_redundant=4, random_state=42, flip_y=0.05
    )
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# =============================================================================
# TODO 1: Define Model Configurations
# =============================================================================
# Create a list of model configurations to try:
# At least 6 configurations covering different algorithms and hyperparams.
# Each config: {"name": "...", "model": ModelClass(...), "needs_scaling": bool}

def get_model_configs():
    """Return list of model configurations to evaluate."""
    # TODO: Define 6+ configurations
    # Example:
    # configs = [
    #     {"name": "logistic_reg", "model": LogisticRegression(max_iter=1000), "needs_scaling": True},
    #     {"name": "rf_100_d5", "model": RandomForestClassifier(n_estimators=100, max_depth=5), ...},
    #     ...
    # ]
    pass


# =============================================================================
# TODO 2: Train and Log One Model
# =============================================================================
# Train a single model and log everything to MLflow:
#   - Parameters (model type, all hyperparams)
#   - Metrics (accuracy, f1, precision, recall)
#   - Model artifact
#   - Confusion matrix plot (as artifact)

def train_and_log(config, X_train, X_test, y_train, y_test):
    """Train a model and log to MLflow."""
    # TODO: Start run with config["name"]
    # TODO: Log params (model type + hyperparams from model.get_params())
    # TODO: Fit model
    # TODO: Predict and compute metrics
    # TODO: Log metrics
    # TODO: Create and log confusion matrix plot
    # TODO: Log model
    pass


# =============================================================================
# TODO 3: Run All Experiments
# =============================================================================
# Train all model configurations within one experiment.
# Print a summary table of results.

def run_experiments(X_train, X_test, y_train, y_test):
    """Run all model configurations and log to MLflow."""
    mlflow.set_experiment("model-selection")
    configs = get_model_configs()
    # TODO: Loop through configs, call train_and_log for each
    # TODO: Print summary table (name, f1, accuracy)
    pass


# =============================================================================
# TODO 4: Find Best Model
# =============================================================================
# Use mlflow.search_runs() to find the best model:
#   - Search the "model-selection" experiment
#   - Sort by F1 score descending
#   - Return the best run ID and its metrics

def find_best_model():
    """Find the best performing model from logged experiments."""
    # TODO: search_runs with sorting
    # TODO: Print best model details
    # TODO: Return best run ID
    pass


# =============================================================================
# TODO 5: Register Best Model
# =============================================================================
# Register the best model in the MLflow Model Registry:
#   - Register with a name (e.g., "best-classifier")
#   - Transition to "Production" stage
#   - Print registry info

def register_best(run_id):
    """Register the best model in the MLflow registry."""
    # TODO: Register model from run
    # TODO: Transition to Production stage
    pass


# =============================================================================
# TODO 6: Load and Verify
# =============================================================================
# Load the production model from registry and verify it works:
#   - Load by name + stage
#   - Make predictions on test data
#   - Print metrics

def verify_deployment(X_test, y_test):
    """Load production model and verify predictions."""
    # TODO: Load from registry
    # TODO: Predict
    # TODO: Print verification metrics
    pass


# =============================================================================
# TODO 7: Generate Experiment Report
# =============================================================================
# Create a summary report (text file) with:
#   - All runs and their metrics
#   - Best model details
#   - Recommendation
# Log as an artifact.

def generate_report():
    """Generate and log an experiment report."""
    # TODO: Search all runs
    # TODO: Format as readable report
    # TODO: Save to file and log as artifact
    pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("ML EXPERIMENT DASHBOARD")
    print("=" * 60)

    # Setup
    X_train, X_test, y_train, y_test = create_dataset()
    print(f"Dataset: {X_train.shape[0]} train, {X_test.shape[0]} test, {X_train.shape[1]} features")

    # Step 1: Run experiments
    print("\n--- STEP 1: RUN EXPERIMENTS ---")
    run_experiments(X_train, X_test, y_train, y_test)

    # Step 2: Find best
    print("\n--- STEP 2: FIND BEST MODEL ---")
    best_run_id = find_best_model()

    # Step 3: Register
    print("\n--- STEP 3: REGISTER MODEL ---")
    if best_run_id:
        register_best(best_run_id)

    # Step 4: Verify
    print("\n--- STEP 4: VERIFY DEPLOYMENT ---")
    verify_deployment(X_test, y_test)

    # Step 5: Report
    print("\n--- STEP 5: GENERATE REPORT ---")
    generate_report()

    print("\n" + "=" * 60)
    print("Done! View results: mlflow ui --port 5000")
    print("Open: http://localhost:5000")
    print("=" * 60)


if __name__ == "__main__":
    main()
