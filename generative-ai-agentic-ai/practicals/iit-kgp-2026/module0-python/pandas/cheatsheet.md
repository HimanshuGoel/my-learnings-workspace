# Pandas — Cheatsheet

## Import

```python
import pandas as pd
import numpy as np
```

---

## Loading Data

```python
df = pd.read_csv("file.csv")                    # CSV
df = pd.read_csv("file.csv", usecols=["a","b"]) # specific columns
df = pd.read_csv("file.csv", nrows=1000)         # first 1000 rows
df = pd.read_excel("file.xlsx")                  # Excel
df = pd.read_json("file.json")                   # JSON
df = pd.read_sql(query, connection)              # SQL
```

## Saving Data

```python
df.to_csv("out.csv", index=False)
df.to_excel("out.xlsx", index=False)
df.to_json("out.json", orient="records")
```

---

## Inspection

```python
df.head(5)          # first 5 rows
df.tail(3)          # last 3 rows
df.sample(5)        # random 5 rows
df.shape            # (rows, cols)
df.info()           # types, non-null, memory
df.describe()       # numeric stats
df.dtypes           # column types
df.columns          # column names
df.index            # row labels
df.nunique()        # unique values per column
df["col"].value_counts()  # frequency counts
```

---

## Selection

```python
# Columns
df["col"]                # single → Series
df[["a", "b"]]          # multiple → DataFrame

# Rows by label
df.loc[0]               # row with label 0
df.loc[0:5, "a":"c"]   # slice rows & cols by label

# Rows by position
df.iloc[0]              # first row
df.iloc[0:5, 0:3]      # slice by integer position

# Boolean filter
df[df["age"] > 30]
df[(df["a"] > 1) & (df["b"] < 5)]
df.query("age > 30 and salary > 50000")

# isin filter
df[df["city"].isin(["NYC", "LA"])]
```

---

## Cleaning

```python
# Missing values
df.isnull().sum()                      # count NaN per column
df.dropna()                            # drop rows with any NaN
df.dropna(subset=["col"])              # drop if specific col is NaN
df["col"].fillna(value)                # fill with value
df["col"].fillna(df["col"].median())   # fill with median
df.interpolate()                       # fill with interpolation

# Duplicates
df.drop_duplicates()
df.drop_duplicates(subset=["col"])

# Rename
df.rename(columns={"old": "new"})

# Drop
df.drop(columns=["col"])
df.drop(index=[0, 1])

# Type casting
df["col"] = df["col"].astype(int)
df["date"] = pd.to_datetime(df["date"])
```

---

## Transformation

```python
# New column (vectorized)
df["total"] = df["price"] * df["qty"]

# Apply function
df["col"].apply(func)
df.apply(func, axis=1)       # apply per row

# Map values
df["col"].map({"a": 1, "b": 2})

# Replace
df["col"].replace({"old": "new"})

# Conditional (np.where)
df["flag"] = np.where(df["val"] > 0, "pos", "neg")

# One-hot encoding
pd.get_dummies(df, columns=["cat_col"], drop_first=True)

# Binning
pd.cut(df["age"], bins=[0,18,35,65,100], labels=["kid","young","mid","senior"])
```

---

## Aggregation

```python
# Basic stats
df["col"].sum()  .mean()  .std()  .min()  .max()  .median()

# GroupBy
df.groupby("col")["val"].mean()
df.groupby("col").agg({"val": "mean", "count": "sum"})
df.groupby("col").agg(
    avg=("val", "mean"),
    total=("val", "sum"),
    n=("val", "count")
)

# Pivot table
df.pivot_table(values="val", index="row", columns="col", aggfunc="mean")

# Cross-tab
pd.crosstab(df["a"], df["b"])
```

---

## Sorting

```python
df.sort_values("col", ascending=False)
df.sort_values(["a", "b"], ascending=[True, False])
df.sort_index()
df["col"].rank(ascending=False)
df.nlargest(10, "col")    # top 10 by column
df.nsmallest(5, "col")    # bottom 5
```

---

## Combining

```python
# Merge (SQL JOIN)
pd.merge(left, right, on="key", how="inner")  # inner/left/right/outer
pd.merge(left, right, left_on="a", right_on="b")  # different key names

# Concatenate
pd.concat([df1, df2], axis=0)          # stack rows
pd.concat([df1, df2], axis=1)          # stack columns

# Join on index
df1.join(df2, how="left")
```

---

## String Operations

```python
df["col"].str.lower()
df["col"].str.upper()
df["col"].str.strip()
df["col"].str.contains("pattern", regex=True)
df["col"].str.replace("old", "new")
df["col"].str.split("@").str[0]
df["col"].str.len()
df["col"].str.extract(r"(\d+)")  # regex extract
```

---

## Date/Time

```python
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["dayofweek"] = df["date"].dt.dayofweek
df.set_index("date").resample("M").mean()   # monthly avg
df["rolling"] = df["val"].rolling(7).mean()  # 7-period rolling
```

---

## ML Preparation Pattern

```python
# Load → Clean → Encode → Split
df = pd.read_csv("data.csv")
df.dropna(subset=["target"], inplace=True)
df["feature"].fillna(df["feature"].median(), inplace=True)
df = pd.get_dummies(df, columns=["category"], drop_first=True)
X = df.drop(columns=["target"]).values
y = df["target"].values
```

---

## Quick Reference Links

- Official docs: https://pandas.pydata.org/docs/
- Cheat sheet (official): https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
