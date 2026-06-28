"""
Pandas Exercises — 15 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. AI-relevant exercises are marked with [AI].
Run: python exercises.py
"""

import pandas as pd
import numpy as np

# =============================================================================
# EASY (1-5)
# =============================================================================

# Exercise 1: DataFrame Creation & Inspection
# Create a DataFrame from the dictionary below.
# Print: shape, dtypes, first 3 rows, and statistical summary.
# Expected output:
#   Shape: (5, 3)
#   Dtypes: name-object, age-int64, salary-float64

def exercise_1():
    data = {
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [28, 35, 42, 31, 26],
        "salary": [72000.0, 85000.0, 95000.0, 68000.0, 55000.0]
    }
    # Your code here: create DataFrame, print shape, dtypes, head(3), describe()
    pass


# Exercise 2: Column Selection & Filtering
# From the DataFrame below:
#   a) Select only 'product' and 'revenue' columns
#   b) Filter rows where revenue > 500
#   c) Filter rows where category is "Electronics"
# Expected output:
#   High revenue: 3 rows
#   Electronics: 2 rows

def exercise_2():
    df = pd.DataFrame({
        "product": ["Laptop", "Phone", "Tablet", "Headphones", "Monitor"],
        "category": ["Electronics", "Electronics", "Electronics", "Accessories", "Electronics"],
        "revenue": [1200, 800, 450, 150, 650],
        "units_sold": [10, 25, 15, 50, 8]
    })
    # Your code here
    pass


# Exercise 3: Handling Missing Values
# The dataset below has missing values. Handle them:
#   a) Count NaN per column
#   b) Fill missing 'age' with median age
#   c) Drop rows where 'email' is NaN
#   d) Print resulting shape
# Expected output:
#   NaN counts: age=2, email=1, score=1
#   Final shape: (4, 4) (after dropping email NaN)

def exercise_3():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [28, None, 42, None, 26],
        "email": ["a@x.com", "b@x.com", None, "d@x.com", "e@x.com"],
        "score": [85, 90, None, 72, 88]
    })
    # Your code here
    pass


# Exercise 4: Adding & Transforming Columns
# Given employee data:
#   a) Add 'bonus' column = salary * 0.10
#   b) Add 'tax' column = salary * 0.30
#   c) Add 'net_pay' = salary + bonus - tax
#   d) Add 'level' column: "Senior" if experience > 5, else "Junior"
# Expected output: DataFrame with 4 new columns

def exercise_4():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "salary": [70000, 85000, 95000, 60000],
        "experience": [3, 7, 12, 2]
    })
    # Your code here
    pass


# Exercise 5: Sorting & Ranking
# Given student scores:
#   a) Sort by score descending
#   b) Add a 'rank' column (1 = highest score)
#   c) Find the top 3 students
# Expected output: top 3 names with their ranks

def exercise_5():
    df = pd.DataFrame({
        "student": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
        "score": [88, 92, 75, 95, 83, 91]
    })
    # Your code here
    pass


# =============================================================================
# MEDIUM (6-10)
# =============================================================================

# Exercise 6: GroupBy Aggregation
# Analyze sales by region:
#   a) Total revenue per region
#   b) Average units sold per region
#   c) Count of products per region
#   d) Create a summary DataFrame with all three metrics
# Expected output: summary with 3 regions, 3 metric columns

def exercise_6():
    df = pd.DataFrame({
        "product": ["A", "B", "C", "D", "E", "F", "G", "H"],
        "region": ["North", "South", "North", "East", "South", "East", "North", "South"],
        "revenue": [1200, 800, 950, 1100, 600, 1300, 750, 900],
        "units_sold": [10, 15, 8, 12, 20, 9, 11, 18]
    })
    # Your code here
    pass


# Exercise 7: Merge (JOIN) Operations
# Join employee data with department data:
#   a) Inner join on dept_id
#   b) Left join (keep all employees, even if dept not found)
#   c) Print how many employees have no matching department
# Expected output: inner join rows vs left join rows difference

def exercise_7():
    employees = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "dept_id": [1, 2, 1, 3, 4],
        "salary": [70000, 85000, 65000, 90000, 55000]
    })
    departments = pd.DataFrame({
        "dept_id": [1, 2, 3],
        "dept_name": ["Engineering", "Marketing", "Finance"]
    })
    # Your code here
    pass


# Exercise 8: One-Hot Encoding [AI]
# Prepare categorical data for ML model input:
#   a) One-hot encode the 'color' and 'size' columns
#   b) Drop the first category to avoid multicollinearity
#      (multicollinearity = when features are redundant, confusing the model)
#   c) Print the resulting column names and shape
# Expected output: original 4 cols → more cols after encoding

def exercise_8():
    df = pd.DataFrame({
        "product": ["Shirt", "Pants", "Hat", "Shirt", "Pants"],
        "color": ["Red", "Blue", "Red", "Green", "Blue"],
        "size": ["S", "M", "L", "M", "S"],
        "price": [25, 45, 15, 30, 50]
    })
    # Your code here: use pd.get_dummies with drop_first=True
    pass


# Exercise 9: Feature Engineering [AI]
# Create useful features from raw data for a house price prediction model:
#   a) price_per_sqft = price / sqft
#   b) age_of_house = 2026 - year_built
#   c) is_large = 1 if sqft > 2000, else 0
#   d) price_category = pd.cut(price, bins=3, labels=["low","mid","high"])
# Expected: 4 new derived features added

def exercise_9():
    df = pd.DataFrame({
        "price": [250000, 450000, 180000, 650000, 320000],
        "sqft": [1500, 2200, 1100, 3000, 1800],
        "year_built": [1990, 2005, 1975, 2018, 2000],
        "bedrooms": [3, 4, 2, 5, 3]
    })
    # Your code here
    pass


# Exercise 10: Method Chaining
# Using method chaining (fluent API), perform all operations in one expression:
#   a) Filter: salary > 50000
#   b) Group by department
#   c) Compute mean salary per department
#   d) Sort descending
#   e) Take top 3
# Expected output: top 3 departments by avg salary (single chained expression)

def exercise_10():
    df = pd.DataFrame({
        "name": ["A","B","C","D","E","F","G","H","I","J"],
        "department": ["Eng","Sales","Eng","HR","Sales","Eng","HR","Sales","Eng","HR"],
        "salary": [90000, 60000, 85000, 55000, 65000, 95000, 50000, 70000, 88000, 52000]
    })
    # Your code here: single chained expression
    pass


# =============================================================================
# HARD (11-15)
# =============================================================================

# Exercise 11: Complete ML Data Prep Pipeline [AI]
# Prepare a messy dataset for model training:
#   a) Drop rows where target is NaN
#   b) Fill numeric NaN with column median
#   c) One-hot encode categorical columns
#   d) Split into X (features) and y (target)
#   e) Convert to NumPy arrays
# This is the standard preprocessing pipeline before sklearn.fit()
# Expected output: X shape and y shape (NumPy arrays)

def exercise_11():
    df = pd.DataFrame({
        "age": [25, None, 35, 28, 42, None, 31, 55],
        "income": [50000, 60000, None, 45000, 80000, 70000, None, 90000],
        "education": ["BS", "MS", "BS", "PhD", "MS", "BS", "MS", "PhD"],
        "city": ["NYC", "LA", "NYC", "SF", "LA", "SF", "NYC", "LA"],
        "purchased": [0, 1, 0, 1, 1, None, 0, 1]  # target variable
    })
    # Your code here
    pass


# Exercise 12: Time Series Feature Extraction [AI]
# Given daily sales data, create features commonly used in time series forecasting:
#   a) Parse 'date' to datetime and set as index
#   b) Add: day_of_week, month, is_weekend columns
#   c) Add: rolling 7-day average of sales
#   d) Add: lag_1 (previous day's sales) and lag_7 (7 days ago)
# lag features = using past values as features for predicting future values
# Expected output: DataFrame with 5 new feature columns

def exercise_12():
    dates = pd.date_range("2026-01-01", periods=30, freq="D")
    np.random.seed(42)
    df = pd.DataFrame({
        "date": dates,
        "sales": np.random.randint(100, 500, size=30)
    })
    # Your code here
    pass


# Exercise 13: Exploratory Data Analysis (EDA) [AI]
# Perform a complete EDA workflow:
#   a) Check class balance of target variable (value_counts normalized)
#   b) Find top 5 features most correlated with target
#   c) Identify columns with >20% missing values
#   d) Find potential outliers (values > 3 std from mean) in numeric columns
# This is the standard first step before any ML project.
# Expected output: print findings for each step

def exercise_13():
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "feature_a": np.random.normal(50, 10, n),
        "feature_b": np.random.normal(100, 25, n),
        "feature_c": np.random.normal(0, 1, n),
        "feature_d": np.random.choice(["cat", "dog", "bird"], n),
        "feature_e": np.random.normal(75, 15, n),
        "target": np.random.choice([0, 1], n, p=[0.7, 0.3])
    })
    # Inject some NaN
    df.loc[np.random.choice(n, 50, replace=False), "feature_a"] = np.nan
    df.loc[np.random.choice(n, 10, replace=False), "feature_b"] = np.nan
    # Inject outliers
    df.loc[0, "feature_b"] = 500
    df.loc[1, "feature_c"] = 15
    # Your code here
    pass


# Exercise 14: Pivot & Reshape for Reporting [AI]
# Transform transaction data into a report format:
#   a) Create pivot table: months as rows, categories as columns, sum of amount as values
#   b) Add a 'total' column (row-wise sum)
#   c) Add a 'total' row (column-wise sum)
#   d) Find the month with highest total spending
# This mimics how you'd prepare data for stakeholder dashboards.
# Expected output: pivot table with totals

def exercise_14():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-01-15","2026-01-20","2026-02-10",
                                "2026-02-25","2026-03-05","2026-03-18",
                                "2026-01-08","2026-02-14","2026-03-22"]),
        "category": ["Food","Transport","Food","Entertainment",
                     "Food","Transport","Entertainment","Transport","Food"],
        "amount": [150, 80, 200, 120, 180, 95, 60, 110, 160]
    })
    # Your code here
    pass


# Exercise 15: Fine-Tuning Data Format Preparation [AI]
# Convert raw Q&A data into the JSONL format required for LLM fine-tuning:
#   a) Create 'instruction' column = "Answer the following question:"
#   b) Create 'input' column = the question
#   c) Create 'output' column = the answer
#   d) Drop rows where answer is empty or NaN
#   e) Export to JSONL format (one JSON object per line)
# JSONL = JSON Lines format, where each line is a valid JSON object.
# This is the standard format for fine-tuning datasets (Module 3).
# Expected output: a JSONL file with clean instruction-input-output records

def exercise_15():
    df = pd.DataFrame({
        "question": [
            "What is photosynthesis?",
            "Explain gravity",
            "What is DNA?",
            "Define osmosis",
            "What is entropy?"
        ],
        "answer": [
            "The process by which plants convert sunlight to energy",
            "A force of attraction between objects with mass",
            None,  # missing answer
            "Movement of water through a semipermeable membrane",
            ""     # empty answer
        ],
        "source": ["bio101", "physics", "bio101", "chem", "physics"]
    })
    # Your code here
    # Hint: use df.to_json("output.jsonl", orient="records", lines=True)
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
