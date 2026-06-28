# Scikit-Learn — Cheatsheet

## Import Convention

```python
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
import numpy as np
import pandas as pd
```

---

## The Universal API

```python
model = SomeEstimator(hyperparams)   # 1. Instantiate
model.fit(X_train, y_train)          # 2. Fit (learn)
predictions = model.predict(X_test)  # 3. Predict
proba = model.predict_proba(X_test)  # 4. Probabilities (classifiers)
score = model.score(X_test, y_test)  # 5. Evaluate (default metric)
```

---

## Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 20% for testing
    random_state=42,     # reproducibility
    stratify=y           # preserve class proportions
)
```

---

## Preprocessing

```python
# Standardize (mean=0, std=1) — needed for SVM, KNN, LogReg
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)    # fit + transform on train
X_test_scaled = scaler.transform(X_test)    # only transform on test!

# Min-Max [0, 1]
minmax = MinMaxScaler()
X_norm = minmax.fit_transform(X_train)

# One-Hot Encode
encoder = OneHotEncoder(sparse_output=False, drop="first")
X_cat = encoder.fit_transform(X_categorical)

# Label Encode (for target)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# PCA (dimensionality reduction)
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_scaled)
```

---

## Pipeline

```python
# Chain preprocessing + model (prevents data leakage)
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(random_state=42))
])
pipe.fit(X_train, y_train)
pipe.score(X_test, y_test)

# ColumnTransformer (different transforms per column type)
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["age", "income", "tenure"]),
    ("cat", OneHotEncoder(drop="first"), ["city", "gender"])
])

full_pipe = Pipeline([
    ("preprocess", preprocessor),
    ("model", LogisticRegression(max_iter=1000))
])
```

---

## Cross-Validation

```python
scores = cross_val_score(model, X, y, cv=5, scoring="f1")
print(f"F1: {scores.mean():.3f} ± {scores.std():.3f}")

# Scoring options: "accuracy", "f1", "precision", "recall",
#                  "roc_auc", "neg_mean_squared_error"
```

---

## Hyperparameter Tuning

```python
# Grid Search (exhaustive)
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 10, None]
}
grid = GridSearchCV(RandomForestClassifier(random_state=42),
                    param_grid, cv=5, scoring="f1", n_jobs=-1)
grid.fit(X_train, y_train)
print(grid.best_params_, grid.best_score_)
best_model = grid.best_estimator_

# Randomized Search (faster for large param spaces)
from sklearn.model_selection import RandomizedSearchCV
random_search = RandomizedSearchCV(model, param_distributions,
                                   n_iter=50, cv=5, random_state=42)
```

---

## Metrics — Classification

```python
from sklearn.metrics import (accuracy_score, precision_score,
    recall_score, f1_score, classification_report, confusion_matrix,
    roc_auc_score)

print(classification_report(y_test, preds))  # full report
cm = confusion_matrix(y_test, preds)

accuracy_score(y_test, preds)
precision_score(y_test, preds, average="weighted")
recall_score(y_test, preds, average="weighted")
f1_score(y_test, preds, average="weighted")
roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
```

## Metrics — Regression

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, preds)
rmse = mean_squared_error(y_test, preds, squared=False)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)
```

---

## Common Models

```python
# Classification
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# Regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# Clustering (unsupervised)
from sklearn.cluster import KMeans, DBSCAN

# Dimensionality Reduction
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
```

---

## Feature Importance

```python
# Tree-based models
importances = model.feature_importances_
sorted_idx = importances.argsort()[::-1]

# Linear models (coefficients)
coefs = model.coef_[0]
```

---

## Model Persistence

```python
import joblib
joblib.dump(model, "model.joblib")           # save
loaded = joblib.load("model.joblib")         # load
```

---

## Imbalanced Data

```python
# Class weights
model = RandomForestClassifier(class_weight="balanced")

# Use appropriate metric
scoring = "f1"  # not "accuracy"
```

---

## Text Classification (TF-IDF)

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
X_text = tfidf.fit_transform(corpus)
# Then feed X_text to any classifier
```

---

## Quick Reference Links

- Official docs: https://scikit-learn.org/stable/
- Cheat sheet (choosing model): https://scikit-learn.org/stable/machine_learning_map.html
- User guide: https://scikit-learn.org/stable/user_guide.html
