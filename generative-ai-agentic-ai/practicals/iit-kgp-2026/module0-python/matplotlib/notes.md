# Matplotlib — Notes

## What Problem Does This Library Solve?

Matplotlib turns numbers into pictures — it renders arrays and DataFrames as charts (line, bar, scatter, heatmap, etc.) so you can visually understand data distributions, relationships, and model behavior before and after training.

## Mental Model

Think of Matplotlib as **the HTML Canvas API for data**. You have a Figure (the browser window) containing one or more Axes (individual `<canvas>` elements). You draw on each Axes by calling methods like `.plot()`, `.bar()`, `.scatter()`. Just as you'd style HTML with CSS, you style plots with parameters. The OO interface (fig, ax) is like working with DOM elements directly — more control than the quick pyplot shortcut.

## Where It Fits

```
Clean Data (Pandas DataFrame / NumPy array)
        │
        ▼
┌─────────────┐
│  Matplotlib  │  ← visualize distributions, relationships, results (you are here)
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ Insights & Decisions  │
│ • Is data balanced?   │
│ • Which features matter?│
│ • Is model improving?  │
│ • Where does it fail?  │
└──────────────────────┘
```

- **Before Matplotlib:** Clean data from Pandas/NumPy
- **After Matplotlib:** Human understanding → better feature engineering, model selection, debugging
- **Talks to:** Pandas (df.plot()), NumPy (array plotting), Scikit-Learn (learning curves, confusion matrices), Seaborn (statistical plots built on top of Matplotlib)

## Core Concepts

### 1. Figure and Axes — The Two-Level Hierarchy

```python
import matplotlib.pyplot as plt
import numpy as np

# The OO (Object-Oriented) way — preferred for control
fig, ax = plt.subplots()         # fig = window, ax = one drawing area
ax.plot([1, 2, 3], [1, 4, 9])   # draw on the axes
ax.set_title("My Plot")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show()

# Multiple subplots (like a grid of charts)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # 2×2 grid
axes[0, 0].plot(x, y)     # top-left
axes[0, 1].bar(x, y)      # top-right
axes[1, 0].scatter(x, y)  # bottom-left
axes[1, 1].hist(data)     # bottom-right
plt.tight_layout()
plt.show()
```

**Key insight:** Always use the OO interface (`fig, ax = plt.subplots()`) over `plt.plot()`. The pyplot shortcut is fine for one-offs but becomes messy with multiple plots.

### 2. The Big 6 Plot Types

```python
# 1. LINE — trends over time
ax.plot(dates, values, color="blue", linewidth=2, label="Revenue")

# 2. SCATTER — relationships between two variables
ax.scatter(x, y, c=colors, s=sizes, alpha=0.6)

# 3. BAR — comparing categories
ax.bar(categories, values, color="steelblue")
ax.barh(categories, values)  # horizontal

# 4. HISTOGRAM — distribution of one variable
ax.hist(data, bins=30, edgecolor="black", alpha=0.7)

# 5. HEATMAP — matrix visualization (correlation, confusion matrix)
im = ax.imshow(matrix, cmap="viridis")
plt.colorbar(im)

# 6. BOX PLOT — distribution summary (median, quartiles, outliers)
ax.boxplot([group1, group2, group3], labels=["A", "B", "C"])
```

### 3. Styling & Customization

```python
# Colors, markers, line styles
ax.plot(x, y, color="#4F46E5", linestyle="--", marker="o", markersize=4)

# Labels and title
ax.set_title("Training Loss Over Epochs", fontsize=12, fontweight="bold")
ax.set_xlabel("Epoch")
ax.set_ylabel("Loss")

# Legend
ax.legend(loc="upper right")

# Grid
ax.grid(True, alpha=0.3)

# Axis limits
ax.set_xlim(0, 100)
ax.set_ylim(0, 1)

# Figure size (set at creation)
fig, ax = plt.subplots(figsize=(10, 6))

# Save to file (for reports, papers, presentations)
fig.savefig("plot.png", dpi=150, bbox_inches="tight")
```

### 4. Plotting from Pandas Directly

```python
# Pandas has built-in Matplotlib integration
df["salary"].hist(bins=20)
df.plot(x="date", y="revenue", kind="line")
df.groupby("dept")["salary"].mean().plot(kind="bar")
df.plot.scatter(x="age", y="salary", c="department", colormap="viridis")

# Correlation heatmap
import seaborn as sns
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
```

### 5. Subplots for Comparison

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(train_data, bins=30, alpha=0.7, label="Train")
axes[0].hist(test_data, bins=30, alpha=0.7, label="Test")
axes[0].set_title("Distribution Comparison")
axes[0].legend()

axes[1].plot(epochs, train_loss, label="Train Loss")
axes[1].plot(epochs, val_loss, label="Val Loss")
axes[1].set_title("Learning Curves")
axes[1].legend()

axes[2].bar(models, accuracies)
axes[2].set_title("Model Comparison")

plt.tight_layout()
plt.show()
```

### 6. Color Maps (cmap)

```python
# Sequential: "viridis", "plasma", "inferno" — for ordered data
# Diverging: "coolwarm", "RdBu" — for data with a meaningful center (e.g., correlation)
# Categorical: "tab10", "Set2" — for discrete categories

ax.scatter(x, y, c=values, cmap="viridis")  # color by value
plt.colorbar()
```

## Key Functions/Methods

### Creating Plots

| Function | Purpose |
|----------|---------|
| `plt.subplots(nrows, ncols)` | Create figure + axes grid |
| `ax.plot(x, y)` | Line plot |
| `ax.scatter(x, y)` | Scatter plot |
| `ax.bar(x, height)` / `ax.barh()` | Bar plot (vertical/horizontal) |
| `ax.hist(data, bins)` | Histogram |
| `ax.imshow(matrix)` | Heatmap / image |
| `ax.boxplot(data)` | Box-and-whisker plot |
| `ax.pie(sizes, labels)` | Pie chart (use sparingly) |

### Customization

| Function | Purpose |
|----------|---------|
| `ax.set_title(str)` | Plot title |
| `ax.set_xlabel(str)` / `set_ylabel(str)` | Axis labels |
| `ax.legend()` | Show legend |
| `ax.grid(True)` | Show grid |
| `ax.set_xlim(a, b)` / `set_ylim(a, b)` | Set axis range |
| `ax.set_xticks(list)` | Custom tick positions |
| `ax.annotate(text, xy, xytext)` | Add annotation arrow |
| `ax.axhline(y, ...)` / `ax.axvline(x, ...)` | Reference lines |

### Output

| Function | Purpose |
|----------|---------|
| `plt.show()` | Display plot |
| `fig.savefig(path, dpi, bbox_inches)` | Save to file |
| `plt.tight_layout()` | Auto-fix spacing between subplots |
| `plt.close()` | Close figure (free memory) |

## Common Patterns

### Training Loss Curve

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(range(1, epochs+1), train_losses, label="Train", color="#4F46E5")
ax.plot(range(1, epochs+1), val_losses, label="Validation", color="#f59e0b")
ax.set_xlabel("Epoch")
ax.set_ylabel("Loss")
ax.set_title("Training Progress")
ax.legend()
ax.grid(True, alpha=0.3)
```

### Confusion Matrix Heatmap

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_true, y_pred)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
ax.set_title("Confusion Matrix")
```

### Feature Importance Bar Chart

```python
importances = model.feature_importances_
features = X.columns
sorted_idx = importances.argsort()[::-1][:10]  # top 10

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(features[sorted_idx][::-1], importances[sorted_idx][::-1])
ax.set_xlabel("Importance")
ax.set_title("Top 10 Feature Importances")
```

### Distribution Check (Before Training)

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for i, col in enumerate(["feature_a", "feature_b", "feature_c"]):
    axes[i].hist(df[col], bins=30, edgecolor="black", alpha=0.7)
    axes[i].set_title(f"{col} Distribution")
    axes[i].axvline(df[col].mean(), color="red", linestyle="--", label="Mean")
    axes[i].legend()
plt.tight_layout()
```

### EDA Grid (Quick Overview)

```python
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()  # easier to iterate

numeric_cols = df.select_dtypes(include="number").columns[:6]
for i, col in enumerate(numeric_cols):
    axes[i].hist(df[col], bins=25, alpha=0.7)
    axes[i].set_title(col)
plt.tight_layout()
```

## AI/ML Connection

- **Where in the AI pipeline:** Matplotlib operates at exploration (EDA before training), monitoring (during training), and evaluation (after training). It's NOT in the computation pipeline — it's for human understanding.

- **Concrete example — EDA:** Before building any model, you plot feature distributions (histograms), target balance (bar), and feature correlations (heatmap) to understand what you're working with.

- **Concrete example — Training Monitoring:** Plot train loss vs validation loss over epochs. If val_loss diverges from train_loss → model is overfitting. This visual is how you decide when to stop training.

- **Concrete example — Model Evaluation:** Confusion matrix heatmap shows where the model is confusing classes. ROC curve shows trade-off between false positives and true positives.

- **Which IIT KGP modules use this:** Module 1 (plot attention weights, token probabilities), Module 2 (retrieval quality visualizations), Module 3 (fine-tuning loss curves, before/after comparison), Module 5 (capstone presentation charts).

- **What breaks without it:** You'd be training blind. Without visualization, you can't spot overfitting, class imbalance, feature skewness, or outliers. Debugging a model without plots is like debugging code without logs.

- **Concrete example — Capstone Presentations:** Your Module 5 capstone evaluation will require professional-looking charts. Matplotlib + a few styling tweaks produces publication-quality figures.

- **Concrete example — Embedding Visualization:** Using t-SNE/UMAP (from sklearn) to reduce 768D embeddings to 2D, then scatter-plotting them colored by class to see if the model separates concepts well.

## Common Mistakes

1. **Using pyplot (plt.plot) for complex figures** — fine for one quick chart, but leads to spaghetti code with multiple plots. Use the OO interface: `fig, ax = plt.subplots()`.

2. **Forgetting `plt.tight_layout()`** — subplots overlap and labels get cut off. Always call it before `show()` or `savefig()`.

3. **Not setting `figsize`** — default size is too small for most uses. Start with `figsize=(10, 6)` and adjust.

4. **Using pie charts** — almost always inferior to bar charts for comparison. Humans are bad at comparing angles. Use bar charts instead.

5. **Overplotting scatter plots** — too many points overlap. Use `alpha=0.3` for transparency, or use `hexbin()` / density plots for large datasets.

6. **Forgetting to close figures** — in loops creating many plots, memory leaks. Use `plt.close(fig)` after saving.

7. **Not labeling axes** — a chart without labels is useless. Always add `set_xlabel`, `set_ylabel`, `set_title`.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Interactive dashboards | Plotly, Dash |
| Quick statistical plots (less code) | Seaborn (built on Matplotlib) |
| Web-based interactive charts | Plotly, Bokeh |
| Real-time updating plots | Plotly Dash, Streamlit |
| 3D visualizations | Plotly, PyVista |
| Simple EDA (auto-generated) | pandas-profiling, sweetviz |

**Note:** Seaborn is not a replacement — it's a wrapper. Under the hood, it uses Matplotlib. Learn Matplotlib's OO interface first; Seaborn becomes trivial after that.

## Ready to Move On?

- ☐ I can create a figure with subplots and draw line, scatter, bar, and histogram charts
- ☐ I can customize titles, labels, legends, colors, and save to file
- ☐ I can plot training loss curves (train vs validation over epochs)
- ☐ I can visualize a confusion matrix as a heatmap
- ☐ I know when to use Seaborn/Plotly instead of raw Matplotlib

Once all checked → move to **Scikit-Learn**.
