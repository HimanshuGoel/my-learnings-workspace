"""
=============================================================================
MINI PROJECT: ML Dataset Preparation Pipeline
=============================================================================

PROBLEM STATEMENT:
You've received a raw customer churn dataset (simulated). Your job is to
prepare it for a classification model that predicts which customers will
cancel their subscription (churn).

WHAT YOU'LL BUILD:
- A complete data loading and inspection workflow
- Missing value handling strategy
- Feature engineering (new columns from existing data)
- Categorical encoding
- Train-ready output (X and y as NumPy arrays)

WHY THIS MATTERS:
This is THE most common real-world Pandas workflow. Every ML project starts
here. In your IIT KGP program, Module 1 (classification), Module 3
(fine-tuning data prep), and your capstone will all need this skill.
Data scientists spend ~80% of their time on data preparation, not modeling.

ESTIMATED TIME: 30-45 minutes

SKILLS PRACTICED:
- read_csv, info, describe, value_counts
- isnull, fillna, dropna
- Feature engineering (apply, np.where, pd.cut)
- get_dummies (one-hot encoding)
- Method chaining
- Train/test split preparation

RULES:
- Use only Pandas + NumPy (no sklearn for preprocessing)
- No Python for-loops — use vectorized Pandas operations
- Follow the TODOs in order
=============================================================================
"""

import pandas as pd
import numpy as np


# =============================================================================
# SETUP: Generate simulated customer dataset
# =============================================================================

def generate_customer_data(n=500, seed=42):
    """Generate a realistic but messy customer churn dataset."""
    rng = np.random.default_rng(seed)

    data = {
        "customer_id": [f"CUST_{i:04d}" for i in range(n)],
        "age": rng.integers(18, 70, n).astype(float),
        "gender": rng.choice(["Male", "Female", "Other"], n, p=[0.48, 0.48, 0.04]),
        "tenure_months": rng.integers(1, 72, n).astype(float),
        "monthly_charges": rng.uniform(20, 120, n).round(2),
        "total_charges": None,  # will compute below
        "contract_type": rng.choice(["Month-to-month", "One year", "Two year"], n, p=[0.5, 0.3, 0.2]),
        "payment_method": rng.choice(["Credit card", "Bank transfer", "Electronic check", "Mailed check"], n),
        "internet_service": rng.choice(["DSL", "Fiber optic", "No"], n, p=[0.35, 0.45, 0.20]),
        "num_support_tickets": rng.integers(0, 10, n),
        "churn": rng.choice([0, 1], n, p=[0.73, 0.27])
    }

    df = pd.DataFrame(data)
    df["total_charges"] = (df["monthly_charges"] * df["tenure_months"] * rng.uniform(0.9, 1.1, n)).round(2)

    # Inject messiness (real data is NEVER clean)
    # Missing values
    age_nan_idx = rng.choice(n, 25, replace=False)
    tenure_nan_idx = rng.choice(n, 15, replace=False)
    charges_nan_idx = rng.choice(n, 20, replace=False)
    df.loc[age_nan_idx, "age"] = np.nan
    df.loc[tenure_nan_idx, "tenure_months"] = np.nan
    df.loc[charges_nan_idx, "total_charges"] = np.nan

    # Some inconsistent casing in payment method
    inconsistent_idx = rng.choice(n, 10, replace=False)
    df.loc[inconsistent_idx, "payment_method"] = df.loc[inconsistent_idx, "payment_method"].str.upper()

    return df


# =============================================================================
# TODO 1: Load and Inspect
# =============================================================================
# Generate the dataset and perform initial inspection:
#   - Print shape
#   - Print info (types, non-null counts)
#   - Print statistical summary
#   - Print target variable distribution (churn: 0 vs 1)
#   - Identify columns with missing values

def inspect_data(df):
    """Perform initial data inspection."""
    # TODO: Print shape
    # TODO: Print df.info()
    # TODO: Print df.describe()
    # TODO: Print df["churn"].value_counts(normalize=True)
    # TODO: Print columns with NaN and their counts
    pass


# =============================================================================
# TODO 2: Clean Data
# =============================================================================
# Handle missing values and inconsistencies:
#   a) Standardize payment_method to title case (fix UPPER inconsistency)
#   b) Fill missing 'age' with median age
#   c) Fill missing 'tenure_months' with median
#   d) Fill missing 'total_charges' with monthly_charges * tenure_months
#   e) Verify: no NaN remaining
#
# Return the cleaned DataFrame.

def clean_data(df):
    """Clean and fix data quality issues."""
    df = df.copy()
    # TODO: Standardize payment_method casing
    # TODO: Fill age NaN with median
    # TODO: Fill tenure_months NaN with median
    # TODO: Fill total_charges NaN with computed value
    # TODO: Assert no NaN remaining
    return df


# =============================================================================
# TODO 3: Feature Engineering
# =============================================================================
# Create new features that might help the model:
#   a) avg_monthly_charge = total_charges / tenure_months
#   b) tenure_category: pd.cut into ["New (0-12)", "Mid (13-36)", "Long (37+)"]
#   c) is_high_spender: 1 if monthly_charges > 80, else 0
#   d) charge_per_ticket: total_charges / (num_support_tickets + 1) — avoid div by 0
#   e) has_fiber: 1 if internet_service == "Fiber optic", else 0
#
# Return the DataFrame with new features added.

def engineer_features(df):
    """Create derived features for the model."""
    df = df.copy()
    # TODO: Add avg_monthly_charge
    # TODO: Add tenure_category using pd.cut
    # TODO: Add is_high_spender
    # TODO: Add charge_per_ticket
    # TODO: Add has_fiber
    return df


# =============================================================================
# TODO 4: Encode Categoricals
# =============================================================================
# Prepare categorical columns for the model:
#   a) One-hot encode: contract_type, payment_method, internet_service,
#      tenure_category, gender
#   b) Use drop_first=True to avoid multicollinearity
#   c) Drop the original customer_id column (not a feature)
#
# Return the fully encoded DataFrame.

def encode_categoricals(df):
    """One-hot encode categorical columns."""
    df = df.copy()
    # TODO: Drop customer_id
    # TODO: One-hot encode categorical columns with drop_first=True
    return df


# =============================================================================
# TODO 5: Split Features and Target
# =============================================================================
# Prepare final arrays for model training:
#   a) Separate into X (all columns except 'churn') and y ('churn')
#   b) Convert both to NumPy arrays
#   c) Print final shapes
#
# Return X and y as NumPy arrays.

def prepare_for_training(df):
    """Split into features and target, convert to NumPy."""
    # TODO: X = all columns except 'churn'
    # TODO: y = 'churn' column
    # TODO: Convert to numpy
    # TODO: Print shapes
    return None, None  # return X, y


# =============================================================================
# TODO 6: Summary Report
# =============================================================================
# Print a summary of the entire pipeline:
#   - Original shape
#   - Final shape (after encoding)
#   - Number of features
#   - Target balance (% churn vs not)
#   - Any notable insights (e.g., "Fiber optic customers may churn more")

def print_summary(original_df, final_X, final_y):
    """Print pipeline summary report."""
    # TODO: Print original vs final shape
    # TODO: Print number of features
    # TODO: Print target balance
    # TODO: Print one insight from the data
    pass


# =============================================================================
# MAIN: Run the full pipeline
# =============================================================================

def main():
    print("=" * 60)
    print("ML DATASET PREPARATION PIPELINE")
    print("=" * 60)

    # Generate raw data
    raw_df = generate_customer_data()

    # Step 1: Inspect
    print("\n--- STEP 1: INSPECTION ---")
    inspect_data(raw_df)

    # Step 2: Clean
    print("\n--- STEP 2: CLEANING ---")
    clean_df = clean_data(raw_df)

    # Step 3: Feature Engineering
    print("\n--- STEP 3: FEATURE ENGINEERING ---")
    featured_df = engineer_features(clean_df)

    # Step 4: Encode
    print("\n--- STEP 4: ENCODING ---")
    encoded_df = encode_categoricals(featured_df)

    # Step 5: Train-ready split
    print("\n--- STEP 5: TRAIN-READY SPLIT ---")
    X, y = prepare_for_training(encoded_df)

    # Step 6: Summary
    print("\n--- STEP 6: SUMMARY ---")
    print_summary(raw_df, X, y)

    print("\n" + "=" * 60)
    print("Pipeline complete! X and y are ready for sklearn.fit()")
    print("=" * 60)


if __name__ == "__main__":
    main()
