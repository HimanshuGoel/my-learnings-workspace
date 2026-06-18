# Pandas — Notes

## What Problem Does This Library Solve?

Pandas makes loading, cleaning, transforming, and analyzing tabular data (rows and columns) fast and expressive — replacing manual CSV parsing and loop-based data wrangling with a spreadsheet-like API in code.

## Mental Model

Think of Pandas as **Excel on steroids for developers**. A DataFrame is like an Excel sheet where every column can have a different type, and instead of clicking through menus, you chain method calls like LINQ queries. If NumPy is `int[]` (raw number crunching), Pandas is `DataTable` in .NET — structured, labeled, mixed-type tabular data with built-in querying.

## Where It Fits

```
Raw Data Sources
├── CSV, Excel, JSON, SQL, APIs
│
▼
┌──────────┐
│  Pandas   │  ← load, clean, explore, transform (you are here)
└────┬─────┘
     │ .values / .to_numpy()
     ▼
┌──────────┐
│  NumPy    │  ← pure numerical computation
└────┬─────┘
     │
     ▼
┌──────────────┐
│ Scikit-Learn  │  ← model training (expects clean arrays/DataFrames)
│ Matplotlib   │  ← visualization (plots from DataFrames directly)
│ PyTorch      │  ← deep learning (after conversion to tensors)
└──────────────┘
```

- **Before Pandas:** Raw files (CSV, JSON, SQL dumps, Excel)
- **After Pandas:** NumPy arrays for computation, Scikit-Learn for ML, Matplotlib for plots
- **Talks to:** Everything — Pandas is the universal data interchange format in Python data science

## Core Concepts

### 1. Series — A Single Column

```python
import pandas as pd

# A Series is a 1D labeled array — like a single column in Excel
prices = pd.Series([100, 200, 150, 300], name="price")
print(prices.mean())    # 187.5
print(prices[prices > 150])  # filter like NumPy boolean indexing

# Custom index (labels instead of 0,1,2,3)
stock = pd.Series([150, 2800, 3400], index=["AAPL", "GOOG", "AMZN"])
print(stock["GOOG"])    # 2800
```

Think of Series as a dictionary with superpowers — labeled values that support vectorized math.

### 2. DataFrame — The Core Object

```python
# A DataFrame is a 2D table — like one sheet in Excel or one SQL table
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [30, 25, 35],
    "salary": [70000, 50000, 90000]
})

print(df.shape)      # (3, 3) — 3 rows, 3 columns
print(df.dtypes)     # name: object, age: int64, salary: int64
print(df.columns)    # Index(['name', 'age', 'salary'])
print(df.info())     # summary of types, non-null counts, memory
```

Key properties: `shape`, `dtypes`, `columns`, `index`, `values` (underlying NumPy array).

### 3. Reading Data

```python
# From CSV (most common in ML)
df = pd.read_csv("data.csv")

# From Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# From JSON
df = pd.read_json("data.json")

# From SQL (needs sqlalchemy)
# df = pd.read_sql("SELECT * FROM users", connection)

# Quick peek
df.head()       # first 5 rows
df.tail(3)      # last 3 rows
df.sample(5)    # random 5 rows
df.describe()   # statistics for numeric columns
```

### 4. Selecting Data

```python
# Column selection
df["age"]              # single column → Series
df[["name", "age"]]   # multiple columns → DataFrame

# Row selection by label
df.loc[0]              # row with index label 0
df.loc[0:2, "name":"age"]  # rows 0-2, columns name through age

# Row selection by position (like array indexing)
df.iloc[0]             # first row
df.iloc[0:3, 0:2]     # first 3 rows, first 2 columns

# Boolean filtering (like SQL WHERE)
df[df["age"] > 30]
df[(df["age"] > 25) & (df["salary"] > 60000)]
df.query("age > 25 and salary > 60000")  # SQL-like string syntax
```

**Mental model:** `.loc` = label-based (like dictionary lookup), `.iloc` = integer-based (like array indexing).

### 5. Cleaning Data

```python
# Check for missing values
df.isnull().sum()           # count NaN per column

# Drop rows with any NaN
df.dropna()

# Fill missing values
df["age"].fillna(df["age"].median(), inplace=True)

# Drop duplicate rows
df.drop_duplicates()

# Rename columns
df.rename(columns={"old_name": "new_name"})

# Change data types
df["age"] = df["age"].astype(int)

# Remove a column
df.drop(columns=["unwanted_col"])
```

### 6. Transforming Data

```python
# Add a new column (vectorized — no loops!)
df["bonus"] = df["salary"] * 0.1

# Apply a function to a column
df["name_upper"] = df["name"].apply(str.upper)

# Map values (like a lookup table)
df["dept_code"] = df["department"].map({"Engineering": 1, "Sales": 2})

# Conditional column (like SQL CASE WHEN)
df["senior"] = df["age"].apply(lambda x: "Yes" if x > 30 else "No")
# Or with NumPy (faster):
import numpy as np
df["senior"] = np.where(df["age"] > 30, "Yes", "No")
```

### 7. Grouping & Aggregation

```python
# GroupBy = SQL GROUP BY (split-apply-combine pattern)
df.groupby("department")["salary"].mean()
df.groupby("department").agg({"salary": "mean", "age": "max"})

# Multiple aggregations
df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    headcount=("name", "count"),
    oldest=("age", "max")
)

# Pivot table (like Excel pivot)
df.pivot_table(values="salary", index="department", columns="level", aggfunc="mean")
```

**Mental model:** GroupBy is like SQL's `GROUP BY` + aggregate functions, or C#'s LINQ `.GroupBy().Select()`.

### 8. Sorting & Ranking

```python
df.sort_values("salary", ascending=False)          # sort by column
df.sort_values(["department", "salary"])           # multi-column sort
df["salary_rank"] = df["salary"].rank(ascending=False)  # rank values
```

### 9. Merging DataFrames

```python
# Like SQL JOIN
merged = pd.merge(employees, departments, on="dept_id", how="left")

# Join types: 'inner', 'left', 'right', 'outer'
# Concatenate (stack vertically or horizontally)
combined = pd.concat([df1, df2], axis=0)  # stack rows
combined = pd.concat([df1, df2], axis=1)  # stack columns
```

### 10. String Operations

```python
# Vectorized string methods (no loops)
df["name"].str.lower()
df["name"].str.contains("ali", case=False)
df["email"].str.split("@").str[1]  # extract domain
df["text"].str.len()               # string lengths
```

## Key Functions/Methods

### Loading Data

| Function | Purpose |
|----------|---------|
| `pd.read_csv(path)` | Load CSV file |
| `pd.read_excel(path)` | Load Excel file |
| `pd.read_json(path)` | Load JSON |
| `pd.read_sql(query, conn)` | Load from SQL database |
| `df.to_csv(path)` | Save to CSV |

### Inspection

| Function | Purpose |
|----------|---------|
| `df.head(n)` / `df.tail(n)` | First/last n rows |
| `df.shape` | (rows, columns) tuple |
| `df.info()` | Column types, non-null counts, memory |
| `df.describe()` | Statistical summary of numeric columns |
| `df.dtypes` | Data type of each column |
| `df.value_counts()` | Frequency of each unique value |

### Selection & Filtering

| Function | Purpose |
|----------|---------|
| `df["col"]` | Select single column |
| `df[["a","b"]]` | Select multiple columns |
| `df.loc[row, col]` | Select by label |
| `df.iloc[row, col]` | Select by position |
| `df[df["col"] > x]` | Boolean filter |
| `df.query("col > x")` | SQL-like filter string |

### Cleaning

| Function | Purpose |
|----------|---------|
| `df.isnull().sum()` | Count missing per column |
| `df.dropna()` | Drop rows with NaN |
| `df.fillna(value)` | Replace NaN |
| `df.drop_duplicates()` | Remove duplicate rows |
| `df.rename(columns={})` | Rename columns |
| `df.astype(type)` | Cast column type |

### Transformation

| Function | Purpose |
|----------|---------|
| `df.apply(func)` | Apply function to each element/row/col |
| `df.map(dict)` | Map values using dictionary |
| `df.replace(old, new)` | Replace specific values |
| `pd.get_dummies(df, columns=[])` | One-hot encode categorical columns |
| `pd.cut(col, bins)` | Bin continuous values into categories |

### Aggregation

| Function | Purpose |
|----------|---------|
| `df.groupby("col").agg()` | Group and aggregate |
| `df.pivot_table()` | Pivot like Excel |
| `df["col"].value_counts()` | Count unique values |
| `df.sum() / mean() / std()` | Column-wise statistics |

### Combining

| Function | Purpose |
|----------|---------|
| `pd.merge(a, b, on, how)` | SQL-style join |
| `pd.concat([a, b], axis)` | Stack DataFrames |
| `df.join(other)` | Join on index |

## Common Patterns

### ML Data Preparation Pipeline

```python
# Typical flow before training a model
df = pd.read_csv("dataset.csv")

# 1. Inspect
print(df.shape, df.dtypes)
print(df.isnull().sum())

# 2. Clean
df.dropna(subset=["target"], inplace=True)
df["feature_a"].fillna(df["feature_a"].median(), inplace=True)

# 3. Encode categoricals
df = pd.get_dummies(df, columns=["category_col"], drop_first=True)

# 4. Split features and target
X = df.drop(columns=["target"])
y = df["target"]

# 5. Convert to NumPy for sklearn
X_array = X.values  # or X.to_numpy()
```

### Exploratory Data Analysis (EDA)

```python
# Quick stats
df.describe()
df["target"].value_counts(normalize=True)  # class distribution

# Correlation matrix (which features relate to target?)
df.corr()["target"].sort_values(ascending=False)

# Group analysis
df.groupby("category")["target"].mean()
```

### Time Series Basics

```python
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
df.resample("M").mean()  # monthly averages
df["rolling_avg"] = df["value"].rolling(window=7).mean()
```

### Method Chaining (Fluent API)

```python
# Chain operations like LINQ or builder pattern
result = (
    df
    .query("age > 25")
    .groupby("department")
    .agg(avg_salary=("salary", "mean"))
    .sort_values("avg_salary", ascending=False)
    .head(10)
)
```

## AI/ML Connection

- **Where in the AI pipeline:** Pandas operates at data loading, cleaning, exploration, and feature engineering stages — everything BEFORE the model sees the data.

- **Concrete example — Dataset Preparation:** Every Kaggle competition and real ML project starts with `pd.read_csv()` followed by cleaning, encoding, and feature creation. Without Pandas, preparing a 100k-row dataset with 50 columns would require hundreds of lines of manual code.

- **Concrete example — Feature Engineering:** Creating interaction features (`df["price_per_sqft"] = df["price"] / df["sqft"]`), encoding categoricals (`pd.get_dummies()`), and binning continuous values (`pd.cut()`) are all Pandas operations that directly improve model accuracy.

- **Concrete example — EDA for RAG (Module 2):** Before building a RAG system, you'd load your document metadata into a DataFrame, analyze document lengths, check for duplicates, filter by category — all Pandas.

- **Which IIT KGP modules use this:** Module 1 (loading datasets for experiments), Module 2 (metadata handling for document retrieval), Module 3 (preparing fine-tuning datasets in specific formats), Module 5 (evaluation metrics tables, experiment tracking).

- **What breaks without it:** Without Pandas, loading a CSV with mixed types, handling missing values, and encoding categoricals would take 10x more code. Every ML tutorial assumes you know Pandas — it's the entry ticket.

- **Concrete example — Model Evaluation:** After predictions, you'd create a DataFrame comparing actual vs predicted, compute per-group metrics with groupby, and export results to CSV for reporting.

- **Concrete example — Fine-tuning Data Prep (Module 3):** Fine-tuning LLMs requires data in specific formats (instruction, input, output columns). Pandas is how you load raw data, clean it, and export it as the JSONL format models expect.

## Common Mistakes

1. **SettingWithCopyWarning** — modifying a slice of a DataFrame might not modify the original. Use `.loc[]` for assignment or `.copy()` to be explicit.

```python
# BAD — might not work, triggers warning
df[df["age"] > 30]["salary"] = 0

# GOOD — explicit loc assignment
df.loc[df["age"] > 30, "salary"] = 0
```

2. **Forgetting `inplace=True`** — most operations return a new DataFrame. Without `inplace=True` or reassignment, changes are lost.

```python
# BAD — df unchanged
df.dropna()

# GOOD
df = df.dropna()
# or
df.dropna(inplace=True)
```

3. **Using `apply()` when vectorized operations exist** — `apply()` is just a Python loop in disguise. Use built-in vectorized operations first.

```python
# SLOW
df["doubled"] = df["price"].apply(lambda x: x * 2)

# FAST (vectorized)
df["doubled"] = df["price"] * 2
```

4. **Index confusion** — after filtering or dropping rows, the index has gaps. Use `reset_index(drop=True)` to clean up.

5. **Loading entire file when you only need a subset** — use `usecols` and `nrows` parameters in `read_csv()` for large files.

6. **String dtype "object"** — Pandas uses "object" for strings, which is memory-inefficient. For large text datasets, consider `dtype="string"` or `category`.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Pure numerical computation (matrix math) | NumPy |
| Data larger than RAM (10GB+) | Polars, Dask, PySpark |
| Maximum speed on simple operations | Polars (Rust-based, faster) |
| Real-time streaming data | Kafka, Flink |
| Graph/network data | NetworkX |
| Image/audio data | NumPy arrays directly |

## Ready to Move On?

- ☐ I can load CSV/Excel files and inspect with head(), info(), describe()
- ☐ I can filter rows with boolean conditions and select columns with loc/iloc
- ☐ I can handle missing values (detect, drop, fill)
- ☐ I can use groupby + agg for split-apply-combine analysis
- ☐ I can prepare a dataset for ML (encode categoricals, split X/y, handle NaN)

Once all checked → move to **Matplotlib**.
