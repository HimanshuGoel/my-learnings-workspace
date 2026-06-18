# MLflow — Cheatsheet

## Install

```bash
pip install mlflow
mlflow ui --port 5000  # Launch tracking UI
```

## Import

```python
import mlflow
import mlflow.sklearn
import mlflow.pytorch
import mlflow.transformers
from mlflow import MlflowClient
```

---

## Experiment Tracking

```python
# Set experiment
mlflow.set_experiment("my-experiment")

# Start a run
with mlflow.start_run(run_name="my_run"):
    # Log parameters
    mlflow.log_param("lr", 0.001)
    mlflow.log_param("epochs", 50)
    mlflow.log_params({"model": "rf", "n_estimators": 100})

    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("f1", 0.87)
    mlflow.log_metrics({"precision": 0.89, "recall": 0.85})

    # Log metric per step (training curve)
    for epoch in range(50):
        mlflow.log_metric("loss", loss_value, step=epoch)

    # Log artifacts (files)
    mlflow.log_artifact("plot.png")
    mlflow.log_artifacts("./output_dir")

    # Tags
    mlflow.set_tag("team", "ml-platform")
```

---

## Auto-Logging

```python
mlflow.sklearn.autolog()         # sklearn
mlflow.pytorch.autolog()         # PyTorch
mlflow.transformers.autolog()    # HuggingFace

# Now just train — everything logged automatically
model.fit(X_train, y_train)
```

---

## Log Models

```python
# Sklearn
mlflow.sklearn.log_model(model, "model")
mlflow.sklearn.log_model(model, "model", registered_model_name="my-model")

# PyTorch
mlflow.pytorch.log_model(model, "model")

# HuggingFace
mlflow.transformers.log_model(
    transformers_model={"model": model, "tokenizer": tokenizer},
    artifact_path="hf_model"
)

# Generic Python function
mlflow.pyfunc.log_model("model", python_model=my_wrapper)
```

---

## Load Models

```python
# From run ID
model = mlflow.sklearn.load_model("runs:/RUN_ID/model")

# From registry (by stage)
model = mlflow.sklearn.load_model("models:/my-model/Production")

# From registry (by version)
model = mlflow.sklearn.load_model("models:/my-model/3")

# Generic (any framework)
model = mlflow.pyfunc.load_model("models:/my-model/Production")
preds = model.predict(X_test)
```

---

## Model Registry

```python
from mlflow import MlflowClient
client = MlflowClient()

# Register during logging
mlflow.sklearn.log_model(model, "model", registered_model_name="churn-predictor")

# Transition stage
client.transition_model_version_stage(
    name="churn-predictor", version=2, stage="Production"
)
# Stages: "None", "Staging", "Production", "Archived"

# Search models
results = client.search_registered_models()
versions = client.search_model_versions("name='churn-predictor'")
```

---

## Search & Query Runs

```python
# Search runs in an experiment
runs = mlflow.search_runs(
    experiment_names=["my-experiment"],
    filter_string="metrics.f1 > 0.85",
    order_by=["metrics.f1 DESC"]
)
# Returns a Pandas DataFrame!

# Get best run
best_run = runs.iloc[0]
print(best_run["run_id"], best_run["metrics.f1"])
```

---

## MLflow UI

```bash
mlflow ui --port 5000
# http://localhost:5000
# Features: compare runs, view charts, download artifacts, manage registry
```

---

## MLflow Projects (Reproducibility)

```yaml
# MLproject file
name: my-project
conda_env: conda.yaml
entry_points:
  main:
    parameters:
      lr: {type: float, default: 0.001}
    command: "python train.py --lr {lr}"
```

```bash
mlflow run . -P lr=0.01
mlflow run https://github.com/user/repo
```

---

## Quick Reference Links

- Docs: https://mlflow.org/docs/latest/
- Tracking: https://mlflow.org/docs/latest/tracking.html
- Registry: https://mlflow.org/docs/latest/model-registry.html
