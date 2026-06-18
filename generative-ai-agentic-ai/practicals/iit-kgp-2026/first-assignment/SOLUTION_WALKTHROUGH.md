# Classification Models Exercise — Solution Walkthrough

This document explains **what we did, why we did it, what alternatives exist**, and key concepts to remember for each stage of the assignment.

---

## Part 1: Binary Classification — Breast Cancer Prediction

### Stage 1: Data Loading

**What we did:**
- Loaded the Breast Cancer Wisconsin dataset from sklearn
- Converted it to a pandas DataFrame with proper column names
- Remapped the target variable so that `malignant = 1` and `benign = 0`

**Why:**
- sklearn datasets come as Bunch objects (dictionary-like). Converting to a DataFrame makes exploration easier — you get column names, `.describe()`, `.info()`, etc.
- The raw dataset has `0 = malignant` and `1 = benign`. Since sklearn's `recall_score` defaults to `pos_label=1`, we flip the labels so that the "positive" class (the one we care about catching) is malignant. Without this, recall would measure our ability to detect *benign* cases, which defeats the purpose.

**Alternatives:**
- Instead of `y = 1 - data.target`, you could pass `pos_label=0` to every metric function. But remapping once is cleaner and less error-prone.
- You could also use `LabelEncoder` or a dictionary map, but for binary flipping, `1 - target` is the simplest approach.

**Key concept — Why recall for malignant?**
- False Negative = telling a cancer patient they're healthy → catastrophic
- False Positive = extra follow-up test → inconvenient but safe
- Recall = TP / (TP + FN) → maximising this minimises missed cancers

---

### Stage 2: Data Understanding

**What we did:**
- Displayed the first 5 rows using `.head()` to visually inspect the data
- Checked shape (569 rows × 30 features), data types (all float64), and missing values (none)
- Generated summary statistics with `.describe().T` to see ranges, means, and standard deviations
- Plotted class distribution as a bar chart (357 benign, 212 malignant → ~63/37 split)
- Plotted histograms of 6 features coloured by class to see separation

**Why:**
- EDA (Exploratory Data Analysis) is always the first step before modelling. You need to understand what you're working with.
- Summary statistics revealed massive scale differences (area in hundreds vs fractal dimension ~0.06) — this tells us scaling is mandatory for KNN/SVM.
- Class distribution confirmed moderate imbalance — not severe enough to need SMOTE or oversampling, but enough to justify `class_weight='balanced'` and stratified splits.
- Feature distributions showed that some features (like `worst concave points`) separate classes clearly — these will likely be important predictors.

**Alternatives:**
- Instead of histograms, you could use boxplots (`sns.boxplot`) which better show outliers and quartiles.
- You could also use `sns.pairplot` for feature-pair scatterplots, but with 30 features that's impractical.
- Correlation heatmap could identify redundant features (we do this in Part 2).

**Key observations:**
- No missing values → no imputation needed
- All features are numeric → no encoding needed
- Scale differences are large → StandardScaler is essential
- Classes are moderately imbalanced → use stratified sampling and class weights

---

### Stage 3: Data Preprocessing

**What we did:**
- Missing value audit: confirmed 0 missing values (no imputation needed)
- Split data 70/30 into training (398 samples) and test (171 samples) using stratified sampling
- Applied StandardScaler: fit on training data only, transformed both train and test
- Verified shapes and class distributions are preserved

**Why:**
- **Stratified split** ensures both train and test have ~37% malignant / ~63% benign. Without this, the test set might accidentally be unrepresentative.
- **StandardScaler** puts all 30 features on the same scale (mean=0, std=1). Without this, `mean area` (~654) would dominate distance calculations in KNN and SVM over `fractal dimension` (~0.06).
- **Fit on train only** prevents data leakage. If we used test data's mean/std, the model indirectly "sees" test data during training.

**Alternatives:**
- `MinMaxScaler` — scales to [0, 1] range. Less common but useful when you need bounded values.
- `RobustScaler` — uses median/IQR instead of mean/std. Better when data has many outliers.
- For the split ratio, 80/20 is also common. 70/30 gives more test samples for reliable evaluation.

**The Helper Function:**
- `evaluate_model()` calculates accuracy, recall, precision, F1, and confusion matrix in one call
- Returns a dictionary so we can build comparison tables later
- Prints a formatted report with the confusion matrix explained

**Key insight — Reading the confusion matrix:**

```text
                 Predicted Benign  Predicted Malignant
Actual Benign:       TN              FP
Actual Malignant:    FN              TP
```
- FN (False Negatives) = missed cancers — the number we want to minimise
- FP (False Positives) = unnecessary followups — annoying but not dangerous

---

### Stage 4: Model Training & Tuning

**What we did:**
- Trained 4 models, each with GridSearchCV to find optimal hyperparameters
- Used `scoring='recall'` because catching malignant cases is the priority
- Used 5-fold cross-validation for reliable estimates

**Model-by-model breakdown:**

| Model | Key Hyperparameters | What They Control |
|-------|-------------------|-------------------|
| Logistic Regression | `C` | Regularisation strength (flexibility dial) |
| KNN | `n_neighbors`, `weights` | How many neighbours vote, how votes are weighted |
| Decision Tree | `max_depth`, `min_samples_split`, `min_samples_leaf` | Tree complexity (overfitting control) |
| SVM | `C`, `kernel`, `gamma` | Margin softness, boundary shape, influence radius |

**Why GridSearchCV and not manual tuning?**
- Manual: try C=1, check recall, try C=10, check recall... tedious and error-prone
- GridSearchCV: tries ALL combinations automatically, uses cross-validation (not just one lucky split), returns the winner
- Downside: exhaustive search is slow with large grids (but fine for our small dataset)

**Why `scoring='recall'`?**
- GridSearchCV picks the best model based on this metric
- If we used `scoring='accuracy'`, it might pick a model that predicts mostly benign (high accuracy, low recall)
- `scoring='recall'` ensures the winner is the model that catches the most cancers

**Alternatives:**
- `RandomizedSearchCV`: samples random combinations instead of trying all. Faster for huge grids.
- `BayesSearchCV` (from scikit-optimize): uses Bayesian optimization. Smarter than random/grid.
- Manual threshold tuning (we do this in Stage 6) for additional recall gains.

**Key pattern (same for every model):**
```python
grid = GridSearchCV(estimator, param_grid, scoring='recall', cv=5, n_jobs=-1)
grid.fit(X_train_scaled, y_train)
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test_scaled)
results = evaluate_model('Name', y_test, y_pred)
```

---

### Stage 5: Model Comparison

**What we did:**
- Built a comparison table (DataFrame) showing all 4 models' metrics side by side
- Created a grouped bar chart comparing Recall vs Precision across models
- Ran 5-fold cross-validation on the training set to check stability (mean ± std)
- Extracted feature importances from Decision Tree and plotted top 10

**Why:**
- **Comparison table**: Looking at 4 separate outputs is hard. A table makes the winner obvious at a glance.
- **Bar chart with target line**: The red dashed line at recall=0.95 instantly shows which models meet the clinical target.
- **Cross-validation stability**: A model with recall 0.96±0.02 is far more trustworthy than one with 0.97±0.12. High variance means the model's performance depends heavily on which data it sees.
- **Feature importance**: Explains which features the model relies on. Critical for clinical trust — doctors need to know WHY a model flags a patient.

**How to read cross-validation results:**
- `mean ± std` format (e.g., 0.95 ± 0.03)
- Low std (<0.05) = stable, reliable model
- High std (>0.10) = unreliable, performance fluctuates wildly

**How to read feature importance:**
- Values sum to 1.0 (100% of decision power)
- Higher = more influential in predictions
- Features with importance ~0 contribute almost nothing

**Alternatives:**
- SHAP values: more sophisticated feature importance, works for any model, shows per-sample explanations
- Permutation importance: shuffle a feature, see how much performance drops. Model-agnostic.
- ROC curves: another way to visualise model comparison (we use precision-recall in Stage 6 instead)

---

### Stage 6: Final Model Selection

**What we did:**
- Created a validation split FROM training data (not test!) for threshold tuning
- Retrained SVM on the inner training set and got probability estimates on validation
- Plotted the precision-recall curve showing all possible threshold trade-offs
- Found the optimal threshold where recall ≥ 0.95 while maintaining reasonable precision
- Wrote final recommendation citing specific model, recall, false negatives, and limitations

**Why threshold tuning?**
- Default threshold is 0.5: P(malignant) > 0.5 → predict malignant
- For cancer detection, 0.5 is too conservative. A patient with 35% cancer probability should still get a follow-up test!
- Lowering to e.g. 0.3 means: "if there's even 30% chance, flag it"
- This increases recall (catch more cancers) at the cost of precision (more false alarms)
- The precision-recall curve shows ALL possible trade-offs at once

**Why NOT tune on test set?**
- If we use test data to pick the threshold, our final evaluation on that same test data is dishonest
- It's like choosing exam answers based on the answer key, then claiming you "scored 100%"
- The validation split simulates a clean separation: tune on validation, evaluate on test

**The precision-recall curve:**
- X-axis: Recall (how many cancers caught)
- Y-axis: Precision (how many predictions were truly cancer)
- Top-right corner is ideal (high recall AND precision) but rarely achievable
- Our target: recall ≥ 0.95 (red vertical line) AND precision ≥ 0.60 (orange horizontal line)

**Alternatives:**
- ROC curve + AUC: another way to visualise classifier performance across thresholds. Less informative than PR curve when classes are imbalanced.
- Cost-based threshold: assign actual dollar/life costs to FP and FN, optimise total cost.
- Youden's J statistic: threshold that maximises (sensitivity + specificity - 1).

---

---

## Part 2: Multiclass Classification — Wine

### Stage 1: Data Loading

**What we did:**
- Loaded the Wine dataset from sklearn (178 samples, 13 features, 3 classes)
- Converted to DataFrame with proper column names
- Separated features (X_wine) and target (y_wine)
- No target remapping needed — classes are already 0, 1, 2

**Why no remapping?**
- Unlike Part 1, there's no "positive" class to prioritize
- All 3 cultivars matter equally → macro-averaged metrics handle this

**Key difference from Part 1:**
- Primary metric: Macro-F1 (not Recall)
- No class_weight='balanced' needed (classes are roughly balanced)
- 5 models instead of 4 (adding MLP neural network)

---

### Stage 2: Data Understanding

**What we did:**
- Basic inspection: 178 rows, 13 features, all float64, no missing values
- Class distribution: Class 0 (59), Class 1 (71), Class 2 (48) — roughly balanced
- Summary statistics showing massive scale differences (proline ~278-1680 vs nonflavanoid_phenols ~0.13-0.66)
- Correlation heatmap revealing which features move together

**Key observations:**
- Dataset is small (178 samples) — overfitting is a real risk
- Scale differences are extreme → scaling is mandatory
- Several feature pairs are highly correlated (redundant information)
- Classes are balanced enough that macro-F1 is fair

---

### Stage 3: Data Preprocessing

**What we did:**
- Stratified 70/30 split (124 train, 54 test)
- StandardScaler fit on train, transform both
- Verified class ratios preserved in both splits

**Same principles as Part 1, but:**
- Smaller dataset → each sample matters more
- Stratification is even more critical with only ~48 samples in smallest class

---

### Stage 4: Model Training & Tuning

**What we did:**
- Trained 5 models with GridSearchCV using `scoring='f1_macro'`
- Models: Logistic Regression, KNN, Decision Tree, SVM, MLP (new!)

**The MLP (Neural Network) — what's new:**
- First non-classical model in the assignment
- Hyperparameters control ARCHITECTURE (layer sizes), activation function, and regularisation
- `early_stopping=True` prevents overfitting by monitoring internal validation loss
- On small datasets like Wine, MLP usually doesn't significantly outperform classical models

**Why MLP doesn't dominate here:**
- Neural networks need lots of data to learn useful representations
- 124 training samples is tiny — risk of memorisation is high
- The 13 features are already informative (not raw pixels or text)
- Classical models with proper tuning are already near-optimal

---

### Stage 5: Model Comparison

**What we did:**
- Built comparison table with Accuracy, Macro-Precision, Macro-Recall, Macro-F1
- Bar chart of Macro-F1 scores across all 5 models
- Cross-validation stability check (5-fold, f1_macro)

**Expected findings:**
- SVM and Logistic Regression likely top performers
- MLP competitive but not clearly superior
- Decision Tree likely weakest (overfitting risk on small data)
- All models may show higher variance due to small dataset

---

### Stage 6: Final Recommendation + Overfitting Study

**What we did:**
- Answered final model selection questions (best classical, best overall, most interpretable)
- Trained 3 Decision Tree variants to demonstrate underfitting vs overfitting:
  - max_depth=1: underfits (too simple, low train AND test accuracy)
  - max_depth=None: overfits (100% train accuracy, lower test accuracy)
  - Tuned tree: good fit (reasonable accuracy, small train-test gap)

**The overfitting study teaches:**
- Model complexity is a dial, not a switch
- Too simple → misses patterns (bias error)
- Too complex → memorises noise (variance error)
- Hyperparameter tuning finds the sweet spot (bias-variance trade-off)

**Alternatives for controlling overfitting:**
- Regularisation (alpha in MLP, C in SVM/LR)
- Early stopping (MLP)
- Ensemble methods (Random Forest = many constrained trees averaged)
- Cross-validation to detect overfitting during tuning

---

## Quick Reference

| Term | Meaning |
|------|---------|
| Recall (Sensitivity) | Of all actual positives, how many did we catch? TP/(TP+FN) |
| Precision | Of all predicted positives, how many were correct? TP/(TP+FP) |
| F1-Score | Harmonic mean of precision and recall |
| Macro-F1 | Average F1 across all classes (each class weighted equally) |
| GridSearchCV | Tries all hyperparameter combinations with cross-validation, picks the best |
| StandardScaler | Transforms features to mean=0, std=1. Required for distance-based models |
| Stratified Split | Preserves class ratio in both train and test sets |
| Data Leakage | When test set information leaks into training (e.g., scaling on full data) |
| Cross-Validation | Splits training data into K folds, trains K times, averages performance |
| Overfitting | Model memorises training data, fails on new data (high train acc, low test acc) |
| Underfitting | Model is too simple to capture patterns (low train acc, low test acc) |
