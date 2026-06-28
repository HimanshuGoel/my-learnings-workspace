# Scikit-Learn — Notes

## What Problem Does This Library Solve?

Scikit-Learn provides a unified, consistent API for training, evaluating, and deploying machine learning models — from simple linear regression to random forests — without needing to implement algorithms from scratch.

## Mental Model

Think of Scikit-Learn as **Angular for ML**. Just as Angular enforces a pattern (Component → Template → Service → Module), Scikit-Learn enforces a pattern: **fit → predict → score**. Every model, every transformer, every pipeline follows the same interface. Once you learn one model, you know how to use all 50+. It's opinionated, consistent, and production-oriented.

Alternatively: it's like **Spring Boot's auto-configuration for ML** — sensible defaults, plug-and-play components, and a standard lifecycle.

## Where It Fits

```
Clean Data (Pandas DataFrame / NumPy array)
        │
        ▼
┌───────────────┐
│  Scikit-Learn  │  ← preprocess, train, evaluate, select models (you are here)
└───────┬───────┘
        │
        ├── Model artifacts (.pkl, .joblib)
        ├── Evaluation metrics
        └── Feature insights (importance, coefficients)
        │
        ▼
┌──────────────────────────┐
│ Production / Next Steps   │
│ • Deploy with FastAPI     │
│ • Move to PyTorch (DL)   │
│ • Fine-tune LLMs         │
└──────────────────────────┘
```

- **Before Scikit-Learn:** Clean Pandas DataFrame or NumPy array
- **After Scikit-Learn:** Trained model, predictions, metrics, pipeline artifacts
- **Talks to:** Pandas (input), NumPy (computation), Matplotlib (visualization), joblib (model saving)

## Core Concepts

### 1. The Universal API: fit / predict / transform

```python
from sklearn.linear_model import LogisticRegression

# Every estimator follows this pattern:
model = LogisticRegression()   # 1. Instantiate (configure hyperparameters)
model.fit(X_train, y_train)    # 2. Fit (learn from data)
predictions = model.predict(X_test)  # 3. Predict (apply to new data)
score = model.score(X_test, y_test)  # 4. Score (evaluate)

# Transformers also follow fit/transform:
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)                    # learn mean/std from training data
X_train_scaled = scaler.transform(X_train)  # apply to training
X_test_scaled = scaler.transform(X_test)    # apply same transformation to test
```

**Key insight:** fit() always uses training data only. transform()/predict() can be applied to any data. This prevents data leakage (using test info during training).

### 2. Estimator Types

```python
# CLASSIFIERS — predict discrete labels (cat/dog, spam/not-spam)
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# REGRESSORS — predict continuous values (price, temperature)
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor

# TRANSFORMERS — modify data without predicting
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

# CLUSTERERS — find groups without labels (unsupervised)
from sklearn.cluster import KMeans, DBSCAN
```

### 3. Train/Test Split — Avoiding Data Leakage

```python
from sklearn.model_selection import train_test_split

# Split data: model trains on 80%, evaluates on unseen 20%
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# stratify=y ensures class proportions are preserved in both splits
# random_state=42 for reproducibility (same split every run)
```

**Why:** If you evaluate on data the model has seen, accuracy is meaningless (like grading a test using the answer key during study). The test set simulates real-world unseen data.

### 4. Preprocessing (Transformers)

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# Standardize: mean=0, std=1 (required for SVM, KNN, logistic regression)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)  # fit + transform in one call

# Min-Max: scale to [0, 1]
minmax = MinMaxScaler()
X_normed = minmax.fit_transform(X_train)

# One-Hot Encode categoricals (alternative to pd.get_dummies)
encoder = OneHotEncoder(sparse_output=False, drop="first")
X_encoded = encoder.fit_transform(X_categorical)
```

### 5. Pipelines — Chain Preprocessing + Model

```python
from sklearn.pipeline import Pipeline

# Pipeline = preprocessing + model in one object
# Prevents data leakage: scaler learns ONLY from training fold
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])

pipe.fit(X_train, y_train)       # scales, then trains
pipe.predict(X_test)             # scales, then predicts
pipe.score(X_test, y_test)       # scales, then scores

# ColumnTransformer: apply different preprocessing to different columns
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["age", "income"]),
    ("cat", OneHotEncoder(drop="first"), ["city", "gender"])
])
```

**Mental model:** Pipeline is like Express.js middleware — each step processes data before passing to the next.

### 6. Cross-Validation — Robust Evaluation

```python
from sklearn.model_selection import cross_val_score

# Instead of one train/test split, use K splits (folds)
# Each fold: train on K-1 parts, test on remaining 1. Average all K scores.
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print(f"Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

**Why:** A single train/test split can be lucky or unlucky. Cross-validation gives a confidence interval. 5-fold is standard.

### 7. Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

# Try all combinations of hyperparameters
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 10, None],
    "min_samples_split": [2, 5, 10]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid, cv=5, scoring="accuracy", n_jobs=-1
)
grid.fit(X_train, y_train)

print(grid.best_params_)       # best combination
print(grid.best_score_)        # best CV score
best_model = grid.best_estimator_  # trained model with best params
```

### 8. Evaluation Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

# Classification
print(classification_report(y_test, predictions))
# Shows precision, recall, F1 per class + overall accuracy

# Confusion matrix
cm = confusion_matrix(y_test, predictions)

# For imbalanced datasets, accuracy is misleading. Use F1 instead.
# precision = "of all I predicted positive, how many actually were?"
# recall = "of all actual positives, how many did I catch?"
# F1 = harmonic mean of precision and recall (balances both)
```

### 9. Feature Importance

```python
# Tree-based models expose feature importances
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

importances = model.feature_importances_  # array of importance per feature
sorted_idx = importances.argsort()[::-1]

# Plot top 10
for i in sorted_idx[:10]:
    print(f"{feature_names[i]}: {importances[i]:.4f}")
```

### 10. Model Persistence (Save/Load)

```python
import joblib

# Save trained model
joblib.dump(model, "model.joblib")

# Load later (for serving predictions)
loaded_model = joblib.load("model.joblib")
predictions = loaded_model.predict(new_data)
```

## Key Functions/Methods

### Model Training Lifecycle

| Step | Code | Purpose |
|------|------|---------|
| Instantiate | `model = RandomForestClassifier()` | Create with hyperparameters |
| Train | `model.fit(X_train, y_train)` | Learn from data |
| Predict | `model.predict(X_test)` | Get predictions |
| Probability | `model.predict_proba(X_test)` | Get confidence scores |
| Evaluate | `model.score(X_test, y_test)` | Default metric |

### Preprocessing

| Transformer | Purpose | When |
|------------|---------|------|
| `StandardScaler` | Mean=0, std=1 | SVM, KNN, Logistic Regression |
| `MinMaxScaler` | Scale to [0, 1] | Neural networks, distance-based |
| `OneHotEncoder` | Categories → binary columns | All models (for categorical features) |
| `LabelEncoder` | Labels → integers | Target variable encoding |
| `PCA` | Reduce dimensions | High-dimensional data, visualization |
| `TfidfVectorizer` | Text → numeric vectors | NLP classification |

### Model Selection

| Function | Purpose |
|----------|---------|
| `train_test_split(X, y, test_size)` | Split into train/test |
| `cross_val_score(model, X, y, cv)` | K-fold cross-validation |
| `GridSearchCV(model, params, cv)` | Exhaustive hyperparameter search |
| `RandomizedSearchCV(model, params)` | Random hyperparameter search (faster) |

### Common Models (Classification)

| Model | When to Use | Strengths |
|-------|-------------|-----------|
| `LogisticRegression` | Baseline, interpretable | Fast, probabilistic, linear boundary |
| `RandomForestClassifier` | Default choice for tabular | Robust, handles non-linear, feature importance |
| `GradientBoostingClassifier` | Maximum accuracy (tabular) | State-of-art for structured data |
| `SVC` | Small datasets, clear margin | Good with high-dimensional data |
| `KNeighborsClassifier` | Simple, no training phase | Easy to explain, instance-based |

### Common Models (Regression)

| Model | When to Use |
|-------|-------------|
| `LinearRegression` | Baseline, interpretable |
| `Ridge / Lasso` | Regularized linear (avoid overfitting) |
| `RandomForestRegressor` | Non-linear, robust |
| `GradientBoostingRegressor` | Best accuracy on tabular |

## Common Patterns

### Complete Classification Pipeline

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Build pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42))
])

# 3. Cross-validate
scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="f1")
print(f"CV F1: {scores.mean():.3f} ± {scores.std():.3f}")

# 4. Train final model
pipe.fit(X_train, y_train)

# 5. Evaluate on test
predictions = pipe.predict(X_test)
print(classification_report(y_test, predictions))
```

### Model Comparison

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

models = {
    "Logistic": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Gradient Boost": GradientBoostingClassifier(random_state=42),
    "SVM": SVC(random_state=42),
}

for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="f1")
    print(f"{name:20s} F1: {scores.mean():.3f} ± {scores.std():.3f}")
```

### Handling Imbalanced Data

```python
# Option 1: Class weights (most models support this)
model = RandomForestClassifier(class_weight="balanced", random_state=42)

# Option 2: Use F1/recall instead of accuracy for evaluation
scoring = "f1"  # or "recall" if catching all positives matters most

# Option 3: Oversample minority (SMOTE — from imbalanced-learn library)
```

## AI/ML Connection

- **Where in the AI pipeline:** Scikit-Learn covers the entire traditional ML lifecycle — preprocessing, model training, evaluation, selection, and deployment. It's the standard for tabular/structured data.

- **Concrete example — Foundation Bridge:** Your IIT KGP classification assignment (Grader Rubric) uses Scikit-Learn models directly. fit() → predict() → classification_report() is the workflow.

- **Concrete example — Feature Preprocessing for LLMs:** Before fine-tuning (Module 3), you might use sklearn's TfidfVectorizer for baseline text classification, or its train_test_split for properly splitting your instruction dataset.

- **Concrete example — RAG Evaluation (Module 2):** After retrieval, you evaluate answer quality. Scikit-Learn's metrics (precision, recall, F1) are the standard measurement tools.

- **Which IIT KGP modules use this:** Foundation Bridge (classification exercise), Module 1 (baseline comparisons), Module 2 (evaluation metrics), Module 3 (data splitting for fine-tuning), Module 5 (MLflow integrates with sklearn models).

- **What breaks without it:** You'd need to implement gradient descent, cross-validation, grid search, and every metric from scratch. Scikit-Learn gives you 50+ algorithms with a consistent 3-method API.

- **Concrete example — Embeddings + Classification:** Get embeddings from a transformer model (Module 1), then use sklearn's LogisticRegression or SVM on those embeddings for downstream classification. This "embeddings + sklearn classifier" pattern is extremely common.

- **Concrete example — Capstone:** For Module 5 capstone, you might compare an sklearn baseline (Random Forest on features) against your fine-tuned LLM to show improvement.

## Common Mistakes

1. **Data leakage via preprocessing** — fitting scaler on full data (including test) before splitting. Use Pipeline to prevent this — it fits transformers only on training folds.

```python
# BAD: leakage
scaler.fit(X)  # sees test data statistics!
X_scaled = scaler.transform(X)
X_train, X_test = train_test_split(X_scaled, ...)

# GOOD: no leakage
X_train, X_test = train_test_split(X, ...)
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

2. **Using accuracy on imbalanced data** — 95% accuracy means nothing if 95% of samples are one class. Use F1, precision/recall, or AUC-ROC instead.

3. **Not scaling features for distance-based models** — SVM, KNN, and Logistic Regression need scaled features. Random Forest and Gradient Boosting don't (tree-based = scale-invariant).

4. **Overfitting to validation score during tuning** — GridSearchCV's best_score_ is optimistic. Always evaluate final model on a held-out test set that was never used in tuning.

5. **Forgetting `random_state`** — results change every run without it. Always set for reproducibility during development.

6. **Using fit_transform on test data** — test data should only be transformed (using parameters learned from training), never fit.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Deep learning (images, text, sequences) | PyTorch, TensorFlow |
| GPU-accelerated training | PyTorch, XGBoost (GPU), LightGBM |
| Very large datasets (100M+ rows) | Spark MLlib, Dask-ML |
| LLM fine-tuning | HuggingFace Transformers |
| Reinforcement learning | Stable Baselines3, RLlib |
| Production serving at scale | ONNX, TensorRT, BentoML |

**Note:** Scikit-Learn is unbeatable for tabular data < 1M rows. For deep learning tasks (NLP, vision), use it for preprocessing/evaluation but not for the model itself.

## Ready to Move On?

- ☐ I can train a model using the fit/predict/score pattern
- ☐ I understand train/test split and why data leakage is dangerous
- ☐ I can build a Pipeline combining preprocessing + model
- ☐ I can evaluate using cross-validation and interpret precision/recall/F1
- ☐ I know when to use Random Forest vs Logistic Regression vs SVM

Once all checked → move to **PyTorch**.
