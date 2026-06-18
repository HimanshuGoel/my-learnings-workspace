"""
=============================================================================
MINI PROJECT: ML Experiment Report — Visual Dashboard
=============================================================================

PROBLEM STATEMENT:
You've trained 3 classification models on a customer churn dataset. Now you
need to create a professional visual report comparing their performance.
This is exactly what you'd present in your IIT KGP capstone or any ML project.

WHAT YOU'LL BUILD:
A single multi-panel figure (saved as PNG/PDF) containing:
  1. Training loss curves for all 3 models
  2. Accuracy comparison bar chart
  3. Confusion matrix for the best model
  4. Feature importance chart for the best model
  5. ROC-style curve comparison
  6. Summary text box with key findings

WHY THIS MATTERS:
Every ML project ends with a report. Your Module 5 capstone evaluation,
Kaggle submissions, and real-world stakeholder presentations need
professional visualizations. This project teaches you to compose multiple
charts into one cohesive figure — publication-quality output.

ESTIMATED TIME: 30-45 minutes

SKILLS PRACTICED:
- Multi-panel subplot layout (gridspec)
- Multiple plot types in one figure
- Styling: colors, fonts, annotations, legends
- Saving high-quality output (PNG + PDF)

RULES:
- Use only Matplotlib + NumPy (no Seaborn)
- The final output should be ONE figure with 6 panels
- Make it look professional (consistent colors, readable text)
- Follow the TODOs in order
=============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


# =============================================================================
# SETUP: Simulated experiment results
# =============================================================================

def generate_experiment_data(seed=42):
    """Simulate training results for 3 models."""
    rng = np.random.default_rng(seed)
    epochs = np.arange(1, 51)

    results = {
        "models": ["Random Forest", "XGBoost", "Neural Network"],
        "colors": ["#4F46E5", "#f59e0b", "#059669"],
        "epochs": epochs,

        # Training losses (simulated)
        "train_losses": [
            0.7 * np.exp(-0.06 * epochs) + 0.15 + rng.normal(0, 0.02, 50),
            0.7 * np.exp(-0.08 * epochs) + 0.10 + rng.normal(0, 0.02, 50),
            0.7 * np.exp(-0.05 * epochs) + 0.12 + rng.normal(0, 0.025, 50),
        ],
        "val_losses": [
            0.7 * np.exp(-0.05 * epochs) + 0.20 + 0.05 * (epochs/50)**2 + rng.normal(0, 0.02, 50),
            0.7 * np.exp(-0.07 * epochs) + 0.15 + 0.03 * (epochs/50)**2 + rng.normal(0, 0.02, 50),
            0.7 * np.exp(-0.04 * epochs) + 0.18 + 0.08 * (epochs/50)**2 + rng.normal(0, 0.025, 50),
        ],

        # Final metrics
        "accuracies": [0.847, 0.891, 0.863],
        "precisions": [0.82, 0.88, 0.85],
        "recalls": [0.79, 0.86, 0.81],
        "f1_scores": [0.805, 0.870, 0.830],

        # Confusion matrix for best model (XGBoost)
        "confusion_matrix": np.array([
            [342, 23],
            [32, 103]
        ]),
        "class_names": ["No Churn", "Churn"],

        # Feature importances for best model
        "features": ["tenure", "monthly_charges", "total_charges", "contract_type",
                     "num_tickets", "internet_type", "payment_method", "age",
                     "has_partner", "num_services"],
        "importances": np.array([0.21, 0.18, 0.15, 0.12, 0.09, 0.08, 0.07, 0.05, 0.03, 0.02]),

        # ROC-style curves (simulated)
        "fpr": np.linspace(0, 1, 100),
        "tpr_models": [
            np.clip(1 - np.exp(-3.5 * np.linspace(0, 1, 100)) + rng.normal(0, 0.02, 100), 0, 1),
            np.clip(1 - np.exp(-4.5 * np.linspace(0, 1, 100)) + rng.normal(0, 0.015, 100), 0, 1),
            np.clip(1 - np.exp(-3.8 * np.linspace(0, 1, 100)) + rng.normal(0, 0.02, 100), 0, 1),
        ],
        "auc_scores": [0.88, 0.93, 0.90],
    }
    return results


# =============================================================================
# TODO 1: Create the figure layout
# =============================================================================
# Create a figure with a 2×3 grid of subplots using GridSpec.
# Layout:
#   [0,0] Loss curves    [0,1] Accuracy bars   [0,2] ROC curves
#   [1,0] Confusion mat  [1,1] Feature import  [1,2] Summary text
#
# Set figure size to (16, 10) for good readability.
# Add a main title (suptitle) for the entire figure.

def create_figure():
    """Create the figure layout with GridSpec."""
    # TODO: Create figure with gridspec (2 rows, 3 cols)
    # TODO: Create axes for each panel
    # TODO: Add suptitle
    # Return fig and list/dict of axes
    pass


# =============================================================================
# TODO 2: Plot training loss curves (top-left panel)
# =============================================================================
# Plot validation loss for all 3 models (not train loss — too cluttered).
# Mark the best epoch for each model with a star marker.
# Add legend, labels, and grid.

def plot_loss_curves(ax, results):
    """Plot validation loss curves for all models."""
    # TODO: Plot val_loss for each model with its color
    # TODO: Find and mark best epoch (min val_loss) for each
    # TODO: Add labels, legend, grid
    pass


# =============================================================================
# TODO 3: Plot accuracy comparison (top-middle panel)
# =============================================================================
# Grouped bar chart showing accuracy, precision, recall, F1 for each model.
# Annotate the best score in each metric group.

def plot_metrics_comparison(ax, results):
    """Plot grouped bar chart of model metrics."""
    # TODO: Create grouped bars (3 models × 4 metrics)
    # TODO: Add x-tick labels, legend, and value annotations
    pass


# =============================================================================
# TODO 4: Plot ROC curves (top-right panel)
# =============================================================================
# Plot ROC curve for each model with AUC in legend.
# Add diagonal reference line (random classifier).
# Shade the area under the best model's curve.

def plot_roc_curves(ax, results):
    """Plot ROC curves with AUC scores."""
    # TODO: Plot each model's ROC curve
    # TODO: Add diagonal reference
    # TODO: Shade area under best model
    # TODO: Legend with AUC values
    pass


# =============================================================================
# TODO 5: Plot confusion matrix (bottom-left panel)
# =============================================================================
# Create a heatmap of the confusion matrix for the best model.
# Annotate each cell with the count.
# Color intensity represents the count.

def plot_confusion_matrix(ax, results):
    """Plot confusion matrix heatmap."""
    # TODO: imshow the confusion matrix
    # TODO: Annotate each cell with count (white text on dark, black on light)
    # TODO: Add class labels on both axes
    # TODO: Add title indicating which model
    pass


# =============================================================================
# TODO 6: Plot feature importance (bottom-middle panel)
# =============================================================================
# Horizontal bar chart, sorted by importance (highest at top).
# Color gradient based on importance value.

def plot_feature_importance(ax, results):
    """Plot horizontal bar chart of feature importances."""
    # TODO: Sort features by importance
    # TODO: Create horizontal bars with color gradient
    # TODO: Add importance values as text
    pass


# =============================================================================
# TODO 7: Add summary text (bottom-right panel)
# =============================================================================
# Turn off axes for this panel and display a text summary:
#   - Best model name and accuracy
#   - Key insight (e.g., "XGBoost outperforms by 3-4%")
#   - Top 3 features
#   - Recommendation

def plot_summary(ax, results):
    """Display text summary of findings."""
    # TODO: Turn off axes (ax.axis("off"))
    # TODO: Use ax.text() to display formatted summary
    pass


# =============================================================================
# MAIN: Assemble the dashboard
# =============================================================================

def main():
    print("Generating ML Experiment Report...")

    results = generate_experiment_data()

    # Create figure
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("Customer Churn — Model Comparison Report",
                 fontsize=14, fontweight="bold", y=0.98)

    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)

    ax_loss = fig.add_subplot(gs[0, 0])
    ax_metrics = fig.add_subplot(gs[0, 1])
    ax_roc = fig.add_subplot(gs[0, 2])
    ax_cm = fig.add_subplot(gs[1, 0])
    ax_feat = fig.add_subplot(gs[1, 1])
    ax_summary = fig.add_subplot(gs[1, 2])

    # Fill each panel
    plot_loss_curves(ax_loss, results)
    plot_metrics_comparison(ax_metrics, results)
    plot_roc_curves(ax_roc, results)
    plot_confusion_matrix(ax_cm, results)
    plot_feature_importance(ax_feat, results)
    plot_summary(ax_summary, results)

    # Save
    fig.savefig("plots_output/ml_report.png", dpi=150, bbox_inches="tight")
    fig.savefig("plots_output/ml_report.pdf", bbox_inches="tight")
    print("Saved: plots_output/ml_report.png")
    print("Saved: plots_output/ml_report.pdf")
    plt.close(fig)

    print("\nDone! Open ml_report.png to review your dashboard.")


if __name__ == "__main__":
    import os
    os.makedirs("plots_output", exist_ok=True)
    main()
