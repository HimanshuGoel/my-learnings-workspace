"""
Matplotlib Exercises — 15 Problems (Easy → Medium → Hard)
Each exercise teaches ONE concept. AI-relevant exercises are marked with [AI].
Run: python exercises.py
(Each exercise saves output to a PNG file for review)
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Create output directory for saved plots
os.makedirs("plots_output", exist_ok=True)


# =============================================================================
# EASY (1-5)
# =============================================================================

# Exercise 1: Basic Line Plot
# Plot a simple sine wave from 0 to 2π.
# Add title, x-label, y-label, and grid.
# Save to plots_output/ex01_line.png
# Expected: smooth sine curve with labels

def exercise_1():
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    # Your code here: create fig, ax, plot, label, save
    pass


# Exercise 2: Bar Chart
# Plot average monthly temperatures for 6 months.
# Use different colors for above/below 20°C.
# Save to plots_output/ex02_bar.png
# Expected: bar chart with conditional coloring

def exercise_2():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    temps = [5, 8, 14, 19, 24, 28]
    # Your code here: color bars differently based on temp threshold
    pass


# Exercise 3: Scatter Plot
# Plot random 2D points with color based on distance from origin.
# Add a colorbar to show the distance scale.
# Save to plots_output/ex03_scatter.png
# Expected: scatter with color gradient showing distance

def exercise_3():
    rng = np.random.default_rng(42)
    x = rng.standard_normal(100)
    y = rng.standard_normal(100)
    distances = np.sqrt(x**2 + y**2)
    # Your code here: scatter with c=distances, add colorbar
    pass


# Exercise 4: Histogram
# Plot the distribution of 1000 random samples from a normal distribution.
# Overlay a vertical line at the mean.
# Add text annotation showing mean and std.
# Save to plots_output/ex04_hist.png
# Expected: bell curve histogram with mean line and annotation

def exercise_4():
    rng = np.random.default_rng(42)
    data = rng.normal(loc=50, scale=15, size=1000)
    # Your code here: hist + axvline at mean + text annotation
    pass


# Exercise 5: Multiple Subplots
# Create a 2×2 grid showing 4 different plot types using the same data:
#   top-left: line plot
#   top-right: scatter plot
#   bottom-left: bar plot (first 10 values)
#   bottom-right: histogram
# Save to plots_output/ex05_subplots.png
# Expected: 4 clean plots with titles in one figure

def exercise_5():
    x = np.arange(50)
    y = np.cumsum(np.random.default_rng(42).standard_normal(50))
    # Your code here: fig, axes = plt.subplots(2, 2, ...)
    pass


# =============================================================================
# MEDIUM (6-10)
# =============================================================================

# Exercise 6: Training Loss Curve [AI]
# Plot training loss and validation loss over 50 epochs.
# Highlight the "best epoch" (lowest val loss) with a marker.
# Add a legend and a vertical dashed line at best epoch.
# loss curve = how the model's error decreases during training
# Save to plots_output/ex06_loss_curve.png
# Expected: two curves with best epoch highlighted

def exercise_6():
    rng = np.random.default_rng(42)
    epochs = np.arange(1, 51)
    # Simulated losses (train decreases steadily, val has a valley then rises = overfitting)
    train_loss = 2.0 * np.exp(-0.05 * epochs) + rng.normal(0, 0.05, 50)
    val_loss = 2.0 * np.exp(-0.04 * epochs) + 0.1 * (epochs / 50) ** 2 + rng.normal(0, 0.05, 50)
    # Your code here: plot both, find best epoch, mark it
    pass


# Exercise 7: Class Distribution Bar Chart [AI]
# Visualize the class distribution of a classification dataset.
# Show both count and percentage on each bar.
# Highlight the minority class in red.
# class imbalance = when one class has far fewer samples (hurts model performance)
# Save to plots_output/ex07_class_dist.png
# Expected: bar chart with counts and percentages annotated

def exercise_7():
    classes = ["Cat", "Dog", "Bird", "Fish", "Rabbit"]
    counts = np.array([450, 420, 85, 30, 15])
    # Your code here: bar chart with annotation and minority highlighting
    pass


# Exercise 8: Correlation Heatmap [AI]
# Create a heatmap of the correlation matrix for a synthetic dataset.
# Annotate each cell with the correlation value.
# Use a diverging colormap centered at 0.
# correlation = how linearly related two features are (-1 to +1)
# Save to plots_output/ex08_heatmap.png
# Expected: annotated heatmap with diverging colors

def exercise_8():
    rng = np.random.default_rng(42)
    # Create correlated features
    n = 200
    a = rng.normal(0, 1, n)
    b = a * 0.8 + rng.normal(0, 0.5, n)   # correlated with a
    c = -a * 0.6 + rng.normal(0, 0.7, n)  # anti-correlated with a
    d = rng.normal(0, 1, n)                # independent
    e = b * 0.5 + d * 0.5                  # mix
    data = np.column_stack([a, b, c, d, e])
    features = ["Feature A", "Feature B", "Feature C", "Feature D", "Feature E"]
    corr_matrix = np.corrcoef(data.T)
    # Your code here: imshow with annotations
    pass


# Exercise 9: Before/After Comparison [AI]
# Compare feature distributions before and after normalization.
# Show 3 features side by side (original on top, normalized on bottom).
# normalization = scaling features to [0,1] so model treats them equally
# Save to plots_output/ex09_normalization.png
# Expected: 2×3 grid showing raw vs normalized distributions

def exercise_9():
    rng = np.random.default_rng(42)
    # Features with very different scales
    age = rng.normal(35, 10, 500)            # 15-55
    salary = rng.normal(75000, 20000, 500)   # 35k-115k
    score = rng.normal(0.7, 0.15, 500)       # 0.2-1.0
    features = [age, salary, score]
    names = ["Age", "Salary", "Score"]
    # Normalize each to [0, 1]
    normalized = [(f - f.min()) / (f.max() - f.min()) for f in features]
    # Your code here: 2×3 subplot grid
    pass


# Exercise 10: Styled Multi-Line Plot
# Plot 4 different model accuracies over epochs on one figure.
# Use different colors, line styles, and markers.
# Add a horizontal reference line at 0.9 (target accuracy).
# Add a shaded region showing "acceptable range" (0.85-0.95).
# Save to plots_output/ex10_multi_line.png
# Expected: professional-looking comparison chart

def exercise_10():
    rng = np.random.default_rng(42)
    epochs = np.arange(1, 31)
    model_a = 0.5 + 0.4 * (1 - np.exp(-0.1 * epochs)) + rng.normal(0, 0.01, 30)
    model_b = 0.5 + 0.35 * (1 - np.exp(-0.08 * epochs)) + rng.normal(0, 0.01, 30)
    model_c = 0.5 + 0.45 * (1 - np.exp(-0.15 * epochs)) + rng.normal(0, 0.015, 30)
    model_d = 0.5 + 0.30 * (1 - np.exp(-0.05 * epochs)) + rng.normal(0, 0.01, 30)
    # Your code here: 4 lines + reference line + shaded band
    pass


# =============================================================================
# HARD (11-15)
# =============================================================================

# Exercise 11: Confusion Matrix Visualization [AI]
# Create a confusion matrix heatmap for a 4-class classifier.
# Annotate cells with counts. Color intensity = count.
# Add class labels on both axes.
# confusion matrix = table showing correct vs incorrect predictions per class
# Save to plots_output/ex11_confusion.png
# Expected: annotated heatmap with class labels

def exercise_11():
    # Simulated predictions for 4 classes
    # confusion_matrix[true_class][predicted_class] = count
    cm = np.array([
        [45, 3, 1, 1],   # Class 0: mostly correct
        [2, 38, 5, 5],   # Class 1: some confusion with 2 and 3
        [1, 4, 42, 3],   # Class 2: mostly correct
        [0, 6, 4, 40],   # Class 3: some confusion with 1
    ])
    class_names = ["Cat", "Dog", "Bird", "Fish"]
    # Your code here: imshow + annotate each cell + labels
    pass


# Exercise 12: Feature Importance Chart [AI]
# Create a horizontal bar chart of feature importances from a model.
# Sort by importance (most important at top).
# Color bars by importance level (high=green, medium=blue, low=gray).
# Add the importance value as text at the end of each bar.
# feature importance = how much each input contributes to predictions
# Save to plots_output/ex12_importance.png
# Expected: sorted horizontal bar chart with value labels

def exercise_12():
    features = ["age", "income", "tenure", "num_products", "credit_score",
                "balance", "is_active", "country_de", "country_fr", "gender"]
    importances = np.array([0.15, 0.22, 0.08, 0.12, 0.05,
                           0.18, 0.03, 0.07, 0.06, 0.04])
    # Your code here: sort, color by level, annotate
    pass


# Exercise 13: Embedding Visualization (2D Scatter) [AI]
# Simulate t-SNE reduced embeddings for 5 document categories.
# Plot each category with a different color and marker.
# Add a legend showing category names.
# embedding = numerical vector representing meaning (reduced to 2D for visualization)
# t-SNE = algorithm that reduces high-dimensional data to 2D/3D for plotting
# Save to plots_output/ex13_embeddings.png
# Expected: clustered scatter plot with 5 colored groups

def exercise_13():
    rng = np.random.default_rng(42)
    # Simulate 5 clusters (like t-SNE output of document embeddings)
    categories = ["Sports", "Politics", "Tech", "Health", "Finance"]
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#9b59b6", "#f39c12"]
    centers = [(2, 3), (-2, -1), (4, -2), (-3, 3), (0, -4)]
    # Your code here: scatter each cluster with different color/marker
    pass


# Exercise 14: Multi-Panel EDA Dashboard [AI]
# Create a 2×3 dashboard showing:
#   (0,0) Target distribution (bar)
#   (0,1) Age distribution (histogram)
#   (0,2) Income vs Age (scatter, colored by target)
#   (1,0) Correlation heatmap (top 5 features)
#   (1,1) Box plot of income by target class
#   (1,2) Feature means by target class (grouped bar)
# This is a standard EDA figure you'd create before any ML project.
# Save to plots_output/ex14_dashboard.png
# Expected: professional 6-panel overview

def exercise_14():
    rng = np.random.default_rng(42)
    n = 300
    age = rng.normal(40, 12, n).clip(18, 70)
    income = age * 1500 + rng.normal(0, 15000, n)
    score = rng.normal(650, 80, n).clip(300, 850)
    tenure = rng.integers(1, 15, n)
    target = (income > 65000).astype(int)  # simplified binary target
    # Your code here: 2×3 figure with all 6 panels
    pass


# Exercise 15: Animated-Style Training Progress (Multiple Snapshots) [AI]
# Create a 1×4 subplot showing model decision boundary at epochs 1, 10, 30, 50.
# Simulate a binary classification with 2D data.
# At each epoch, show data points + a simple linear decision boundary.
# This simulates how a model "learns" to separate classes over time.
# Save to plots_output/ex15_learning.png
# Expected: 4 panels showing increasingly better class separation

def exercise_15():
    rng = np.random.default_rng(42)
    # Generate 2-class data
    class_0 = rng.normal([-1, -1], 0.8, (50, 2))
    class_1 = rng.normal([1, 1], 0.8, (50, 2))
    # Simulate decision boundary improving over epochs
    # boundary: w1*x + w2*y + b = 0
    # At epoch 1: random (bad), at epoch 50: well-separated
    weights_over_time = [
        (0.1, 0.3, 0.5),    # epoch 1: nearly random
        (0.5, 0.5, 0.1),    # epoch 10: getting better
        (0.8, 0.8, 0.0),    # epoch 30: good
        (1.0, 1.0, 0.0),    # epoch 50: well-separated
    ]
    epoch_labels = [1, 10, 30, 50]
    # Your code here: 1×4 subplot, each showing data + boundary line
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

    print(f"\n\nAll plots saved to ./plots_output/")
    print("Open them in any image viewer to check your work.")
