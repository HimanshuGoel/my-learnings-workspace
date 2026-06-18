# Matplotlib — Cheatsheet

## Import

```python
import matplotlib.pyplot as plt
import numpy as np
```

---

## Create Figure & Axes

```python
fig, ax = plt.subplots()                    # single plot
fig, ax = plt.subplots(figsize=(10, 6))     # with size
fig, axes = plt.subplots(2, 3, figsize=(14, 8))  # 2×3 grid
fig, (ax1, ax2) = plt.subplots(1, 2)       # unpack 1×2
```

---

## Plot Types

```python
# Line
ax.plot(x, y, color="blue", linewidth=2, linestyle="--", marker="o", label="Line")

# Scatter
ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap="viridis")

# Bar (vertical / horizontal)
ax.bar(categories, values, color="steelblue", edgecolor="black")
ax.barh(categories, values)

# Histogram
ax.hist(data, bins=30, edgecolor="black", alpha=0.7, density=True)

# Heatmap
im = ax.imshow(matrix, cmap="viridis", aspect="auto")
plt.colorbar(im, ax=ax)

# Box plot
ax.boxplot([g1, g2, g3], labels=["A", "B", "C"])

# Pie (avoid when possible)
ax.pie(sizes, labels=labels, autopct="%1.1f%%")

# Fill between (confidence intervals)
ax.fill_between(x, y_low, y_high, alpha=0.2)

# Error bars
ax.errorbar(x, y, yerr=errors, fmt="o", capsize=3)
```

---

## Customization

```python
# Title & labels
ax.set_title("Title", fontsize=12, fontweight="bold")
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")

# Legend
ax.legend(loc="upper right")  # or "best", "lower left", etc.

# Grid
ax.grid(True, alpha=0.3, linestyle="--")

# Axis limits
ax.set_xlim(0, 100)
ax.set_ylim(0, 1)

# Ticks
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=45)

# Reference lines
ax.axhline(y=0.5, color="red", linestyle="--", alpha=0.5)
ax.axvline(x=50, color="gray", linestyle=":")

# Annotations
ax.annotate("Peak", xy=(x_pt, y_pt), xytext=(x_pt+5, y_pt+0.1),
            arrowprops=dict(arrowstyle="->"))

# Text
ax.text(x, y, "label", fontsize=8, ha="center")
```

---

## Styling

```python
# Line styles: "-", "--", "-.", ":"
# Markers: "o", "s", "^", "D", "x", "+", "."
# Colors: "blue", "#4F46E5", "C0" (cycle color 0), (0.2, 0.4, 0.8)

# Use a style preset
plt.style.use("seaborn-v0_8-whitegrid")  # clean look
# Others: "ggplot", "dark_background", "bmh", "fivethirtyeight"

# Color maps (cmap)
# Sequential: "viridis", "plasma", "inferno", "magma"
# Diverging: "coolwarm", "RdBu", "seismic"
# Categorical: "tab10", "Set2", "Paired"
```

---

## Layout & Output

```python
plt.tight_layout()                              # fix overlapping
plt.subplots_adjust(hspace=0.3, wspace=0.3)    # manual spacing
fig.savefig("plot.png", dpi=150, bbox_inches="tight")  # save
fig.savefig("plot.pdf", bbox_inches="tight")    # vector format
plt.show()                                      # display
plt.close(fig)                                  # free memory
```

---

## Pandas Integration

```python
df["col"].hist(bins=20)
df.plot(x="date", y="value", kind="line")
df.plot.scatter(x="a", y="b", c="label", cmap="viridis")
df.groupby("cat")["val"].mean().plot(kind="bar")
df.boxplot(column="val", by="group")
```

---

## Seaborn (Statistical Layer on Matplotlib)

```python
import seaborn as sns

sns.heatmap(df.corr(), annot=True, cmap="coolwarm")  # correlation
sns.pairplot(df, hue="target")                        # all vs all
sns.countplot(x="category", data=df)                  # count bars
sns.boxplot(x="group", y="value", data=df)            # grouped box
sns.kdeplot(data=df["col"], fill=True)                # density
```

---

## Common ML Plot Recipes

```python
# Training curve
ax.plot(epochs, train_loss, label="Train")
ax.plot(epochs, val_loss, label="Val")
ax.legend(); ax.set_xlabel("Epoch"); ax.set_ylabel("Loss")

# Confusion matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_predictions(y_true, y_pred, ax=ax, cmap="Blues")

# Feature importance
ax.barh(feature_names, importances)

# ROC curve
from sklearn.metrics import RocCurveDisplay
RocCurveDisplay.from_predictions(y_true, y_scores, ax=ax)

# Class distribution
df["target"].value_counts().plot(kind="bar", ax=ax)
```

---

## Quick Reference Links

- Official docs: https://matplotlib.org/stable/
- Gallery (copy-paste examples): https://matplotlib.org/stable/gallery/
- Seaborn: https://seaborn.pydata.org/
