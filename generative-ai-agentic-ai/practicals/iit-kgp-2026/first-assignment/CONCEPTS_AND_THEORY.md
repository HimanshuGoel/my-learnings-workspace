# Concepts & Theory — Classification Models

A reference document covering the ML concepts used in this assignment. Useful for revision and interview prep.

---

## 1. Classification Types

### Binary Classification
- Two classes: positive and negative (e.g., malignant vs benign)
- Models output a probability; a threshold (default 0.5) decides the class
- You can tune the threshold to trade off precision vs recall

### Multiclass Classification
- Three or more classes (e.g., wine cultivar 0, 1, 2)
- Models use strategies like One-vs-Rest (OvR) or softmax to handle multiple classes
- Metrics need averaging: macro (equal weight per class), micro (equal weight per sample), weighted

---

## 2. Models Used

### Logistic Regression
- Despite the name, it is a **classification** algorithm
- Learns a linear decision boundary using the sigmoid function
- `C` parameter controls regularisation: small C = more regularisation = simpler model
- `class_weight='balanced'` adjusts for imbalanced classes by penalising mistakes on the minority class more
- Fast, interpretable, works well when classes are linearly separable

### K-Nearest Neighbours (KNN)
- Non-parametric: no training phase, just stores the data
- Classifies by majority vote of the K closest training samples
- **Sensitive to feature scale** — if one feature ranges 0-1000 and another 0-1, the large one dominates distance
- `weights='distance'` gives closer neighbours more influence
- Simple but slow at prediction time on large datasets

### Decision Tree
- Splits data at feature thresholds to create a tree of decisions
- `max_depth`, `min_samples_split`, `min_samples_leaf` control complexity
- Prone to **overfitting** without constraints (can memorise training data perfectly)
- **Not sensitive to feature scale** — splits are based on thresholds, not distances
- Highly interpretable (you can visualise the tree)

### Support Vector Machine (SVM)
- Finds the hyperplane that separates classes with the maximum margin
- `C` controls the trade-off between a wide margin and misclassifications
- `kernel='rbf'` allows non-linear boundaries via the "kernel trick"
- `gamma` controls how far the influence of a single training example reaches
- **Sensitive to feature scale** — requires standardisation
- `probability=True` enables `predict_proba()` (uses Platt scaling, slower)

### Multi-Layer Perceptron (MLP)
- A feedforward neural network with one or more hidden layers
- `hidden_layer_sizes=(100, 50)` means layer 1 has 100 neurons, layer 2 has 50
- `activation` defines the non-linearity (relu, tanh)
- `alpha` is L2 regularisation to prevent overfitting
- `early_stopping=True` stops training when validation loss plateaus
- More powerful but less interpretable than classical models
- **Sensitive to feature scale**

---

## 3. Key Preprocessing Concepts

### StandardScaler
- Transforms each feature to have mean=0 and standard deviation=1
- Formula: `z = (x - mean) / std`
- **Fit on training data only**, then transform both train and test
- Why? If you fit on the full dataset, the scaler learns test set statistics (mean, std), which is information your model shouldn't have during training

### Train-Test Split
- Splits data into training (model learns) and test (model is evaluated)
- **Never use test data during training or tuning** — it simulates "unseen" real-world data
- Typical ratios: 70/30, 80/20

### Stratified Sampling
- Preserves the class ratio in both splits
- Important when classes are imbalanced (e.g., 63% benign, 37% malignant)
- Without stratification, one split might accidentally get mostly one class

---

## 4. Evaluation Metrics

### Confusion Matrix
```
                Predicted
              Neg     Pos
Actual Neg [  TN      FP  ]
Actual Pos [  FN      TP  ]
```

### Accuracy
- `(TP + TN) / Total`
- Misleading when classes are imbalanced (e.g., 95% benign → always predicting benign gives 95% accuracy)

### Recall (Sensitivity / True Positive Rate)
- `TP / (TP + FN)`
- Of all actual positives, how many did we catch?
- Critical when missing a positive is dangerous (cancer detection)

### Precision (Positive Predictive Value)
- `TP / (TP + FP)`
- Of all predicted positives, how many were correct?
- Critical when false alarms are expensive

### F1-Score
- `2 * (Precision * Recall) / (Precision + Recall)`
- Harmonic mean — balances precision and recall
- Use when you need a single number that respects both

### Macro vs Micro Averaging (Multiclass)
- **Macro**: Calculate metric per class, then average. Treats all classes equally.
- **Micro**: Pool all TP, FP, FN globally, then calculate. Equivalent to accuracy for multiclass.
- **Weighted**: Like macro but weighted by class size.
- Use **macro** when all classes matter equally (wine dataset).

---

## 5. Hyperparameter Tuning

### GridSearchCV
- Exhaustive search over specified parameter combinations
- Uses cross-validation to evaluate each combination
- Returns the best parameter set based on chosen scoring metric
- Pros: guaranteed to find the best combo in the grid
- Cons: slow if the grid is large (exponential combinations)

### Cross-Validation (K-Fold)
- Splits training data into K folds
- Trains K times, each time using a different fold as validation
- Reports average performance ± std
- **StratifiedKFold** preserves class ratios in each fold

### Overfitting vs Underfitting
- **Overfitting**: Model is too complex. High training accuracy, low test accuracy. "Memorises" the data.
- **Underfitting**: Model is too simple. Low training accuracy, low test accuracy. Can't capture patterns.
- **Good fit**: Train and test accuracy are both high and close together.

---

## 6. Threshold Tuning (Binary Classification)

- Default threshold: 0.5 (if P(malignant) > 0.5 → predict malignant)
- Lowering the threshold: more cases predicted as positive → recall goes up, precision goes down
- Raising the threshold: fewer cases predicted as positive → precision goes up, recall goes down
- **Precision-Recall Curve** shows this trade-off at all thresholds
- **ROC Curve** plots True Positive Rate vs False Positive Rate
- For medical diagnosis, we lower the threshold to maximise recall (catch all cancers)

---

## 7. Common Pitfalls

| Pitfall | Why it matters |
|---------|---------------|
| Scaling before splitting | Leaks test statistics into training |
| Not using stratification | Can distort class ratios in small datasets |
| Using accuracy on imbalanced data | Masks poor performance on minority class |
| Forgetting `random_state` | Results become non-reproducible |
| Tuning on test data | Overfits to the test set, reported metrics are optimistic |
| No cross-validation | Single split results can be lucky/unlucky |
| Ignoring feature scale | KNN, SVM, MLP perform poorly without scaling |

---

## 8. Bias-Variance Trade-off (Underfitting vs Overfitting)

### The Core Idea
Every model has two sources of error:
- **Bias** (underfitting): model is too simple to capture patterns
- **Variance** (overfitting): model is too sensitive to training data quirks

### How to Detect

| Symptom | Train Accuracy | Test Accuracy | Gap | Diagnosis |
|---------|---------------|---------------|-----|-----------|
| Low | Low | Small | **Underfitting** (high bias) |
| ~100% | Lower | Large (>10%) | **Overfitting** (high variance) |
| High | High | Small (<5%) | **Good fit** |

### How to Fix
- **Underfitting**: increase model complexity (deeper tree, more neurons, lower regularisation)
- **Overfitting**: decrease model complexity (shallower tree, more regularisation, fewer features, more data)

### Decision Tree as a Bias-Variance Example
- `max_depth=1`: high bias (only 1 split for 3 classes)
- `max_depth=None`: high variance (memorises every sample)
- `max_depth=5` (tuned): balanced trade-off

---

## 9. Binary vs Multiclass — Key Differences

| Aspect | Binary (Part 1) | Multiclass (Part 2) |
|--------|-----------------|---------------------|
| Classes | 2 (malignant/benign) | 3+ (cultivar 0/1/2) |
| Primary metric | Recall | Macro-F1 |
| Why that metric? | Missing cancer is catastrophic | All classes matter equally |
| class_weight | 'balanced' (compensate imbalance) | Not needed (classes balanced) |
| Threshold tuning | Yes (lower threshold → more recall) | Typically no (multiclass is harder) |
| SVM strategy | Direct binary | One-vs-One (pairs of classifiers) |
| LR strategy | Direct binary | One-vs-Rest (one classifier per class) |
| Confusion matrix | 2×2 (TN, FP, FN, TP) | 3×3 (one row/col per class) |

---

## 10. When to Use Which Model (Decision Guide)

| Scenario | Best Choice | Why |
|----------|------------|-----|
| Need interpretability | Decision Tree or Logistic Regression | Can explain decisions to non-technical people |
| Small dataset (<500 samples) | SVM or Logistic Regression | Less prone to overfitting |
| Features have different scales | ANY model + StandardScaler | Or use Decision Tree (scale-invariant) |
| Classes are imbalanced | Use class_weight='balanced' + recall metric | Prevents model ignoring minority |
| Need probability estimates | LR, SVM (probability=True), MLP | For threshold tuning or confidence scores |
| Large dataset + complex patterns | MLP or ensemble methods | Neural nets shine with more data |
| Fastest training | Logistic Regression | Closed-form solution, very fast |
| No hyperparameter tuning time | KNN | Lazy learner, no training phase |
