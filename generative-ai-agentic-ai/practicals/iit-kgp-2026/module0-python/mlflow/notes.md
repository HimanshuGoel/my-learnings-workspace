# MLflow — Notes

## What Problem Does This Library Solve?

MLflow tracks ML experiments (parameters, metrics, artifacts), manages model versions, and provides a standardized deployment interface — so you can compare runs, reproduce results, and serve models without losing track of what worked.

## Mental Model

Think of MLflow as **GitHub + Jenkins + SonarQube for ML**:
- **Tracking** = Git commit history (log every experiment with params + metrics)
- **Model Registry** = GitHub Releases (version and stage your models: staging → production)
- **Projects** = Dockerfile/Makefile (package code for reproducible runs)
- **Serving** = Jenkins deploy (serve any registered model as an API)

Or: MLflow is the **experiment lab notebook** that a scientist keeps — but automated, searchable, and connected to deployment.

## Where It Fits

```
Training Experiments (many runs with different params)
        │
        ▼
┌────────────────┐
│     MLflow      │  ← track, compare, version, deploy (you are here)
└───────┬────────┘
        │
        ├── Tracking UI (compare experiments visually)
        ├── Model Registry (version → staging → production)
        └── Model Serving (deploy with one command)
```

- **Before MLflow:** Manual notes, scattered CSV files, "which model was best again?"
- **After MLflow:** Searchable experiment history, reproducible runs, deployment pipeline
- **Talks to:** Scikit-Learn, PyTorch, HuggingFace (auto-logging), FastAPI (serving), S3/GCS (artifact storage)

## Core Concepts

### 1. Experiment Tracking — Log Everything

```python
import mlflow

# Start tracking an experiment
mlflow.set_experiment("customer-churn-v2")

with mlflow.start_run(run_name="random_forest_baseline"):
    # Log parameters (input settings)
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("data_version", "v2.1")

    # Train your model
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)

    # Log metrics (output results)
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", 0.87)
    mlflow.log_metric("auc_roc", 0.92)

    # Log the model itself
    mlflow.sklearn.log_model(model, "model")

    # Log artifacts (any file: plots, data, configs)
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("feature_importance.csv")
```

### 2. Auto-Logging — Zero-Code Tracking

```python
import mlflow

# Automatically log everything for supported frameworks
mlflow.sklearn.autolog()    # sklearn models
mlflow.pytorch.autolog()    # PyTorch
mlflow.transformers.autolog()  # HuggingFace

# Now just train normally — MLflow captures everything
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
# Params, metrics, model artifact all logged automatically!
```

### 3. Comparing Runs (UI)

```bash
# Launch the tracking UI
mlflow ui --port 5000
# Open: http://localhost:5000
```

The UI shows:
- All runs in a table (params + metrics side-by-side)
- Sort/filter by any metric
- Compare runs visually (charts)
- Download artifacts
- View logged models

### 4. Logging Metrics Over Time (Training Curves)

```python
# Log metrics at each step (e.g., loss per epoch)
with mlflow.start_run():
    for epoch in range(50):
        train_loss = train_one_epoch(model)
        val_loss = evaluate(model)

        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_loss", val_loss, step=epoch)

    # Final metrics
    mlflow.log_metric("final_accuracy", 0.93)
```

### 5. Model Registry — Version & Stage Models

```python
import mlflow

# Register a model (after training)
with mlflow.start_run():
    mlflow.sklearn.log_model(model, "model", registered_model_name="churn-predictor")

# The registry tracks versions:
# churn-predictor/version 1 → Staging
# churn-predictor/version 2 → Production
# churn-predictor/version 3 → Archived

# Transition stages via UI or code:
from mlflow import MlflowClient
client = MlflowClient()
client.transition_model_version_stage(
    name="churn-predictor", version=2, stage="Production"
)
```

### 6. Loading Models (For Inference)

```python
# Load from a run
model = mlflow.sklearn.load_model("runs:/abc123def/model")

# Load from registry (by stage)
model = mlflow.sklearn.load_model("models:/churn-predictor/Production")

# Load from registry (by version)
model = mlflow.sklearn.load_model("models:/churn-predictor/2")

# Generic load (works for any framework)
model = mlflow.pyfunc.load_model("models:/churn-predictor/Production")
predictions = model.predict(X_test)
```

### 7. MLflow with PyTorch / HuggingFace

```python
# PyTorch
import mlflow.pytorch

with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
    mlflow.log_param("epochs", 50)

    # Training loop
    for epoch in range(50):
        loss = train(model)
        mlflow.log_metric("loss", loss, step=epoch)

    mlflow.pytorch.log_model(model, "model")

# HuggingFace Transformers
import mlflow.transformers

with mlflow.start_run():
    mlflow.transformers.log_model(
        transformers_model={"model": model, "tokenizer": tokenizer},
        artifact_path="hf_model"
    )
```

### 8. Projects — Reproducible Runs

```yaml
# MLproject file (like Dockerfile for ML)
name: my-ml-project
conda_env: conda.yaml

entry_points:
  main:
    parameters:
      lr: {type: float, default: 0.001}
      epochs: {type: int, default: 10}
    command: "python train.py --lr {lr} --epochs {epochs}"
```

```bash
# Run a project (local or from git)
mlflow run . -P lr=0.01 -P epochs=50
mlflow run https://github.com/user/repo -P lr=0.01
```

## Key Functions/Methods

### Tracking

| Function | Purpose |
|----------|---------|
| `mlflow.set_experiment("name")` | Set active experiment |
| `mlflow.start_run(run_name="...")` | Start tracking a run |
| `mlflow.log_param("key", value)` | Log a hyperparameter |
| `mlflow.log_params(dict)` | Log multiple params |
| `mlflow.log_metric("key", value, step)` | Log a metric |
| `mlflow.log_metrics(dict)` | Log multiple metrics |
| `mlflow.log_artifact("path")` | Log a file |
| `mlflow.log_artifacts("dir")` | Log all files in directory |
| `mlflow.set_tag("key", "value")` | Add metadata tag |

### Model Logging

| Function | Purpose |
|----------|---------|
| `mlflow.sklearn.log_model(model, "path")` | Log sklearn model |
| `mlflow.pytorch.log_model(model, "path")` | Log PyTorch model |
| `mlflow.transformers.log_model(...)` | Log HuggingFace model |
| `mlflow.pyfunc.log_model(...)` | Log generic Python model |

### Model Loading

| Function | Purpose |
|----------|---------|
| `mlflow.sklearn.load_model("runs:/id/path")` | Load from run |
| `mlflow.sklearn.load_model("models:/name/stage")` | Load from registry |
| `mlflow.pyfunc.load_model(uri)` | Load any model type |

### Auto-Logging

| Function | Framework |
|----------|-----------|
| `mlflow.sklearn.autolog()` | Scikit-Learn |
| `mlflow.pytorch.autolog()` | PyTorch |
| `mlflow.transformers.autolog()` | HuggingFace |

## Common Patterns

### Complete Experiment Workflow

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report

mlflow.set_experiment("churn-prediction")

params = {"n_estimators": 200, "max_depth": 7, "class_weight": "balanced"}

with mlflow.start_run(run_name="rf_balanced"):
    mlflow.log_params(params)

    model = RandomForestClassifier(**params, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mlflow.log_metric("f1", f1_score(y_test, preds))
    mlflow.log_metric("accuracy", model.score(X_test, y_test))
    mlflow.sklearn.log_model(model, "model", registered_model_name="churn-model")
```

### Compare Multiple Models

```python
models = {
    "logistic": LogisticRegression(max_iter=1000),
    "rf_100": RandomForestClassifier(n_estimators=100),
    "rf_200": RandomForestClassifier(n_estimators=200),
    "gbm": GradientBoostingClassifier(),
}

for name, model in models.items():
    with mlflow.start_run(run_name=name):
        model.fit(X_train, y_train)
        score = f1_score(y_test, model.predict(X_test))
        mlflow.log_param("model_type", name)
        mlflow.log_metric("f1", score)
        mlflow.sklearn.log_model(model, "model")
```

## AI/ML Connection

- **Where in the AI pipeline:** MLflow sits alongside the entire training lifecycle — it doesn't do the training, it observes and records it. Think of it as the monitoring/versioning layer.

- **Concrete example — Capstone (Module 5):** Track all your experiment runs (different models, hyperparameters, data versions). Present the comparison table to evaluators. Deploy the best model via the registry.

- **Concrete example — Fine-tuning (Module 3):** Log LoRA configs (r, alpha, target_modules), training loss curves, final eval metrics. Compare different fine-tuning runs to pick the best configuration.

- **Concrete example — RAG Evaluation (Module 2):** Log retrieval metrics (precision@k, recall@k) and generation metrics (faithfulness, relevancy) across different chunk sizes and embedding models.

- **Which IIT KGP modules use this:** Module 5 (experiment tracking, model management, deployment), Module 3 (fine-tuning experiment comparison).

- **What breaks without it:** You'd track experiments in spreadsheets, lose old model weights, and have no way to reproduce "that run from last week that worked." MLflow makes ML work reproducible and auditable.

## Common Mistakes

1. **Not setting experiment name** — all runs go to "Default" experiment. Set `mlflow.set_experiment("name")` at the start.

2. **Logging too much or too little** — log params that matter for comparison, metrics that define success, and models you might want to reuse. Don't log every intermediate variable.

3. **Not using autolog for supported frameworks** — `mlflow.sklearn.autolog()` saves manual logging. Use it.

4. **Forgetting to end runs** — use `with mlflow.start_run():` context manager (auto-closes). Never leave runs open.

5. **Not versioning data** — MLflow tracks model + params, but not the data. Log a data hash or version tag so you know which data produced which results.

6. **Running UI in wrong directory** — `mlflow ui` reads from `./mlruns` by default. Run it from the directory where your experiments are stored.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Simple one-off script (no comparison needed) | Just print results |
| Very large-scale distributed training | Weights & Biases (W&B) |
| Production model monitoring (drift detection) | Evidently, WhyLabs |
| CI/CD pipeline for ML | DVC + GitHub Actions |
| Just need model serving (no tracking) | FastAPI directly |

## Ready to Move On?

- ☐ I can track an experiment with params, metrics, and model logging
- ☐ I can use autolog for sklearn/PyTorch
- ☐ I can view and compare runs in the MLflow UI
- ☐ I understand the model registry (versions + stages)
- ☐ I can load a model from the registry for inference

All libraries complete! You now have the full foundation for your IIT KGP program.
