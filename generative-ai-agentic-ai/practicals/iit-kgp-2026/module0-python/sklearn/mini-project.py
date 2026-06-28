"""
=============================================================================
MINI PROJECT: End-to-End Customer Churn Classifier
=============================================================================

PROBLEM STATEMENT:
Build a complete ML classification system to predict customer churn.
This covers the full sklearn workflow: preprocessing, model training,
evaluation, comparison, tuning, and interpretation.

WHAT YOU'LL BUILD:
- Data preprocessing pipeline (handling mixed types)
- Baseline model evaluation (compare 4 algorithms)
- Hyperparameter tuning of the best model
- Final evaluation with detailed metrics
- Feature importance analysis
- Model persistence (save/load)

WHY THIS MATTERS:
This is the exact workflow for your IIT KGP Foundation Bridge classification
assignment and any real-world tabular ML project. Module 5 capstone will
likely include an sklearn baseline comparison against your fine-tuned model.

ESTIMATED TIME: 40-60 minutes

SKILLS PRACTICED:
- Pipeline + ColumnTransformer
- Cross-validation and model comparison
- GridSearchCV for tuning
- Evaluation: classification_report, confusion_matrix
- Feature importance extraction
- joblib save/load

RULES:
- Use only sklearn + numpy + pandas (no XGBoost, LightGBM)
- Build everything inside Pipelines (no data leakage!)
- Follow the TODOs in order
=============================================================================
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# =============================================================================
# SETUP: Generate churn dataset
# =============================================================================

def generate_churn_data(n=1000, seed=42):
    """Generate realistic customer churn dataset with mixed types."""
    rng = np.random.default_rng(seed)

    tenure = rng.integers(1, 72, n)
    monthly_charges = rng.uniform(20, 110, n).round(2)
    total_charges = (monthly_charges * tenure * rng.uniform(0.9, 1.1, n)).round(2)
    age = rng.integers(18, 70, n)
    num_tickets = rng.integers(0, 8, n)
    contract = rng.choice(["Month-to-month", "One year", "Two year"], n, p=[0.5, 0.3, 0.2])
    internet = rng.choice(["DSL", "Fiber", "None"], n, p=[0.35, 0.45, 0.20])
    payment = rng.choice(["Credit card", "Bank transfer", "E-check"], n, p=[0.4, 0.35, 0.25])
    gender = rng.choice(["Male", "Female"], n)

    # Churn depends on features (realistic correlations)
    churn_prob = (
        0.1
        + 0.3 * (contract == "Month-to-month")
        + 0.2 * (internet == "Fiber")
        + 0.15 * (num_tickets > 4)
        + 0.1 * (monthly_charges > 80)
        - 0.2 * (tenure > 36)
        - 0.1 * (contract == "Two year")
    )
    churn_prob = np.clip(churn_prob, 0.05, 0.95)
    churn = rng.binomial(1, churn_prob)

    df = pd.DataFrame({
        "age": age,
        "tenure": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "num_support_tickets": num_tickets,
        "contract_type": contract,
        "internet_service": internet,
        "payment_method": payment,
        "gender": gender,
        "churn": churn,
    })
    return df


# =============================================================================
# TODO 1: Inspect Data
# =============================================================================
# Load and explore the dataset:
#   - Print shape, dtypes, first 5 rows
#   - Check target distribution (churn rate)
#   - Identify numeric vs categorical columns

def inspect_data(df):
    """Explore the dataset."""
    # TODO: Print shape and dtypes
    # TODO: Print churn rate (value_counts normalized)
    # TODO: Identify and return numeric_cols and categorical_cols lists
    pass


# =============================================================================
# TODO 2: Build Preprocessing Pipeline
# =============================================================================
# Create a ColumnTransformer that:
#   - Scales numeric features with StandardScaler
#   - One-hot encodes categorical features (drop="first")
# Return the preprocessor.

def build_preprocessor(numeric_cols, categorical_cols):
    """Build ColumnTransformer for mixed-type preprocessing."""
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    # TODO: Create ColumnTransformer
    pass


# =============================================================================
# TODO 3: Compare Baseline Models
# =============================================================================
# Test 4 models with 5-fold cross-validation (F1 scoring):
#   - Logistic Regression (max_iter=1000)
#   - Random Forest (n_estimators=100)
#   - Gradient Boosting (n_estimators=100)
#   - SVM (kernel="rbf")
# Each wrapped in a Pipeline with the preprocessor.
# Print ranked results. Return name of best model.

def compare_models(X_train, y_train, preprocessor):
    """Compare 4 models with cross-validation."""
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import cross_val_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    # TODO: Define models dict
    # TODO: For each model, build pipeline, cross-validate, store results
    # TODO: Print sorted results, return best model name
    pass


# =============================================================================
# TODO 4: Tune Best Model
# =============================================================================
# Use GridSearchCV on the best model (assume Gradient Boosting).
# Params to tune:
#   - model__n_estimators: [100, 200, 300]
#   - model__max_depth: [3, 5, 7]
#   - model__learning_rate: [0.01, 0.1, 0.2]
# Use 5-fold CV, F1 scoring.
# Print best params and score. Return best pipeline.

def tune_model(X_train, y_train, preprocessor):
    """Tune the best model with GridSearchCV."""
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import GradientBoostingClassifier
    # TODO: Build pipeline
    # TODO: Define param_grid (prefix keys with "model__")
    # TODO: GridSearchCV, fit, print best_params_ and best_score_
    # TODO: Return grid.best_estimator_
    pass


# =============================================================================
# TODO 5: Final Evaluation
# =============================================================================
# Evaluate the tuned model on the held-out test set:
#   - Print classification report
#   - Print confusion matrix
#   - Print accuracy, F1, and ROC-AUC

def evaluate_final(model, X_test, y_test):
    """Final evaluation on test set."""
    from sklearn.metrics import (classification_report, confusion_matrix,
                                 f1_score, roc_auc_score)
    # TODO: Predict on test set
    # TODO: Print classification_report
    # TODO: Print confusion_matrix
    # TODO: Print F1 and ROC-AUC
    pass


# =============================================================================
# TODO 6: Feature Importance
# =============================================================================
# Extract and print top 10 most important features from the tuned model.
# For Gradient Boosting inside a pipeline:
#   model.named_steps["model"].feature_importances_
# Feature names come from the preprocessor's get_feature_names_out()

def analyze_features(model, preprocessor):
    """Extract and display feature importances."""
    # TODO: Get feature names from preprocessor
    # TODO: Get importances from the model step
    # TODO: Sort and print top 10
    pass


# =============================================================================
# TODO 7: Save Model
# =============================================================================
# Save the tuned pipeline using joblib.
# Then load it back and verify it produces same predictions.

def save_and_load(model, X_test):
    """Save model to disk and verify it loads correctly."""
    import joblib
    # TODO: Save with joblib.dump
    # TODO: Load with joblib.load
    # TODO: Verify predictions match
    pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("END-TO-END CUSTOMER CHURN CLASSIFIER")
    print("=" * 60)

    # Generate data
    df = generate_churn_data()

    # Step 1: Inspect
    print("\n--- STEP 1: DATA INSPECTION ---")
    inspect_data(df)

    # Separate features and target
    X = df.drop(columns=["churn"])
    y = df["churn"].values

    numeric_cols = ["age", "tenure", "monthly_charges", "total_charges", "num_support_tickets"]
    categorical_cols = ["contract_type", "internet_service", "payment_method", "gender"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain: {X_train.shape}, Test: {X_test.shape}")

    # Step 2: Preprocessing
    print("\n--- STEP 2: PREPROCESSING ---")
    preprocessor = build_preprocessor(numeric_cols, categorical_cols)

    # Step 3: Compare models
    print("\n--- STEP 3: MODEL COMPARISON ---")
    best_name = compare_models(X_train, y_train, preprocessor)

    # Step 4: Tune
    print("\n--- STEP 4: HYPERPARAMETER TUNING ---")
    best_model = tune_model(X_train, y_train, preprocessor)

    # Step 5: Evaluate
    print("\n--- STEP 5: FINAL EVALUATION ---")
    evaluate_final(best_model, X_test, y_test)

    # Step 6: Features
    print("\n--- STEP 6: FEATURE IMPORTANCE ---")
    analyze_features(best_model, preprocessor)

    # Step 7: Save
    print("\n--- STEP 7: SAVE & LOAD ---")
    save_and_load(best_model, X_test)

    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
