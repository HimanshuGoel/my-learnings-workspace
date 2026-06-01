The Four Pillars Of Modern AI

| Area           | Purpose            |
| -------------- | ------------------ |
| Linear Algebra | Representation     |
| Calculus       | Optimization       |
| Probability    | Uncertainty        |
| Statistics     | Learning From Data |

Statistics is fundamentally asking:

"Given a large amount of data, what patterns can we discover?"

The Hidden Connection To Probability

Remember Stage 6.

Probability asked:

How uncertain are outcomes?

Variance is one of the main mathematical ways to quantify uncertainty.

Small variance:

Predictable

Large variance:

Uncertain

This connection becomes extremely important later in AI.


The Hidden Connection To Probability

Remember Stage 6.

Probability asked:

How uncertain are outcomes?

Variance is one of the main mathematical ways to quantify uncertainty.

Small variance:

Predictable

Large variance:

Uncertain

This connection becomes extremely important later in AI.


# Stage 7 — Statistics & Learning From Data

## Quick Reference Summary Tables

---

# Table 1 — Statistics Fundamentals

| Topic                  | Key Question                  | Core Idea                            | AI Importance                 |
| ---------------------- | ----------------------------- | ------------------------------------ | ----------------------------- |
| Descriptive Statistics | What does the data look like? | Summarize existing data              | EDA, dashboards, monitoring   |
| Inferential Statistics | What can a sample tell us?    | Generalize from sample to population | A/B testing, experimentation  |
| Discrete Data          | Countable values?             | Whole-number counts                  | Clicks, users, purchases      |
| Continuous Data        | Measurable values?            | Can take any value                   | Time, latency, height, weight |

---

# Table 2 — Central Tendency

| Measure | Meaning             | How It Works         | Strength             | Weakness                         |
| ------- | ------------------- | -------------------- | -------------------- | -------------------------------- |
| Mean    | Average             | Sum ÷ Count          | Uses all data        | Sensitive to outliers            |
| Median  | Middle value        | Sort and find center | Robust to outliers   | Ignores exact distances          |
| Mode    | Most frequent value | Highest frequency    | Works for categories | May not exist or may be multiple |

---

# Table 3 — Mean vs Median vs Mode

| Situation                  | Best Measure |
| -------------------------- | ------------ |
| Normally distributed data  | Mean         |
| Outlier-heavy data         | Median       |
| Most common category/value | Mode         |
| Salary analysis            | Median       |
| Product popularity         | Mode         |
| Average performance        | Mean         |

---

# Table 4 — Distribution & Position

| Concept     | Meaning                  | Division         |
| ----------- | ------------------------ | ---------------- |
| Quantiles   | General division of data | Any equal groups |
| Quartiles   | Divide into 4 groups     | 25% each         |
| Deciles     | Divide into 10 groups    | 10% each         |
| Percentiles | Divide into 100 groups   | 1% each          |

---

# Table 5 — Quartiles

| Quartile | Equivalent Percentile | Meaning             |
| -------- | --------------------- | ------------------- |
| Q1       | P25                   | 25% of values below |
| Q2       | P50                   | Median              |
| Q3       | P75                   | 75% of values below |

---

# Table 6 — Important Percentiles

| Percentile | Meaning         | Common Usage            |
| ---------- | --------------- | ----------------------- |
| P50        | Median          | Typical value           |
| P75        | Better than 75% | Ranking                 |
| P90        | Better than 90% | System monitoring       |
| P95        | Better than 95% | API latency             |
| P99        | Better than 99% | Reliability engineering |

---

# Table 7 — Variability Measures

| Measure            | Meaning                             | Uses All Data? | Outlier Sensitive? |
| ------------------ | ----------------------------------- | -------------- | ------------------ |
| Range              | Max − Min                           | No             | Very High          |
| MAD                | Average absolute distance from mean | Yes            | Moderate           |
| Variance           | Average squared distance from mean  | Yes            | High               |
| Standard Deviation | Typical distance from mean          | Yes            | High               |

---

# Table 8 — Variability Hierarchy

| Measure            | Formula Idea              | Interpretation        |
| ------------------ | ------------------------- | --------------------- |
| Range              | Max − Min                 | Total spread          |
| MAD                | Average absolute distance | Typical deviation     |
| Variance           | Average squared distance  | Statistical spread    |
| Standard Deviation | √Variance                 | Human-readable spread |

---

# Table 9 — Variance vs Standard Deviation

| Aspect              | Variance      | Standard Deviation |
| ------------------- | ------------- | ------------------ |
| Units               | Squared units | Original units     |
| Interpretation      | Harder        | Easier             |
| Mathematical Use    | Very common   | Very common        |
| Human Understanding | Lower         | Higher             |
| ML Usage            | Extensive     | Extensive          |

---

# Table 10 — Standard Deviation Interpretation

| Standard Deviation | Meaning                   |
| ------------------ | ------------------------- |
| Very Small         | Highly consistent data    |
| Small              | Low variability           |
| Medium             | Moderate spread           |
| Large              | High variability          |
| Very Large         | Highly unpredictable data |

---

# Table 11 — Covariance

| Covariance Value | Meaning                 |
| ---------------- | ----------------------- |
| Positive         | Variables move together |
| Negative         | Variables move opposite |
| Near Zero        | Little relationship     |

---

# Table 12 — Covariance Limitations

| Limitation        | Explanation           |
| ----------------- | --------------------- |
| Scale Dependent   | Units affect result   |
| Hard To Interpret | No intuitive meaning  |
| No Fixed Range    | Difficult comparison  |
| Not Standardized  | Cannot compare easily |

---

# Table 13 — Pearson Correlation Coefficient

| Correlation (r) | Meaning                        |
| --------------- | ------------------------------ |
| +1.0            | Perfect positive relationship  |
| +0.8            | Strong positive relationship   |
| +0.5            | Moderate positive relationship |
| 0               | No linear relationship         |
| -0.5            | Moderate negative relationship |
| -0.8            | Strong negative relationship   |
| -1.0            | Perfect negative relationship  |

---

# Table 14 — Pearson Properties

| Property          | Meaning                             |
| ----------------- | ----------------------------------- |
| Direction         | Positive or negative relationship   |
| Strength          | Magnitude shows strength            |
| Scale Independent | Units do not matter                 |
| Symmetric         | Corr(A,B)=Corr(B,A)                 |
| Linear Measure    | Detects straight-line relationships |
| Outlier Sensitive | Extreme values can distort results  |

---

# Table 15 — Pearson Limitations

| Limitation                      | Why It Matters                  |
| ------------------------------- | ------------------------------- |
| Linear Only                     | Misses nonlinear patterns       |
| Correlation 0 ≠ No Relationship | Curves may exist                |
| Sensitive To Outliers           | One point can distort result    |
| Two Variables Only              | Real systems are more complex   |
| Cannot Prove Causation          | Relationship ≠ Cause            |
| Can Hide Group Effects          | Segments may behave differently |

---

# Table 16 — Correlation vs Causation

| Correlation             | Causation                       |
| ----------------------- | ------------------------------- |
| Variables move together | One variable influences another |
| Useful for prediction   | Useful for explanation          |
| Does not explain why    | Explains why                    |
| Can be accidental       | Represents true influence       |
| Does not prove cause    | Establishes cause               |

---

# Table 17 — Possible Reasons For Correlation

| Situation                   | Example                            |
| --------------------------- | ---------------------------------- |
| X causes Y                  | Exercise → Fitness                 |
| Y causes X                  | Illness → Medicine Usage           |
| Hidden Variable Causes Both | Temperature → Ice Cream & Swimming |
| Coincidence                 | Random pattern                     |

---

# Table 18 — Spurious Correlation

| Cause             | Description                              |
| ----------------- | ---------------------------------------- |
| Hidden Variable   | Third factor influences both             |
| Coincidence       | Random chance                            |
| Sampling Artifact | Dataset issue                            |
| Data Leakage      | Future information accidentally included |
| Measurement Bias  | Collection problem                       |

---

# Table 19 — Correlation Applications In AI

| Area                   | Use Case                         |
| ---------------------- | -------------------------------- |
| Machine Learning       | Feature selection                |
| Data Science           | Exploratory Data Analysis        |
| Recommendation Systems | Similar users/items              |
| Business Analytics     | Revenue and customer analysis    |
| Fraud Detection        | Anomaly detection                |
| Software Engineering   | System monitoring                |
| Search Engines         | Query-click relationships        |
| Deep Learning          | Training analysis                |
| LLMs                   | Dataset and performance analysis |

---

# Table 20 — Statistics Mental Model

| Question                        | Concept                                  |
| ------------------------------- | ---------------------------------------- |
| Where is the center?            | Mean, Median, Mode                       |
| Where does a value stand?       | Quartiles, Deciles, Percentiles          |
| How spread out is the data?     | Range, MAD, Variance, Standard Deviation |
| How do variables move together? | Covariance, Correlation                  |

---

# Table 21 — Stage 7 AI Takeaways

| Concept            | Why AI Uses It                 |
| ------------------ | ------------------------------ |
| Mean               | Understand averages            |
| Median             | Handle skewed data             |
| Percentiles        | P90/P95/P99 monitoring         |
| Variance           | Measure uncertainty and spread |
| Standard Deviation | Feature scaling and evaluation |
| Correlation        | Discover relationships         |
| Correlation Matrix | Understand datasets            |
| Statistics         | Learn patterns from data       |

---

# Final Stage 7 Memory Sheet

| Area                    | One-Sentence Summary                                    |
| ----------------------- | ------------------------------------------------------- |
| Central Tendency        | Finds the center of data                                |
| Distribution & Position | Finds where values stand                                |
| Variability             | Measures spread around the center                       |
| Relationships           | Measures how variables move together                    |
| Correlation             | Measures strength and direction of linear relationships |
| Statistics              | Learns patterns from data                               |

## Ultimate Mental Model

```text
Statistics =
    Center
  + Position
  + Variability
  + Relationships
```

And remember the four mathematical pillars of AI:

```text
Linear Algebra → Representation
Calculus       → Optimization
Probability    → Uncertainty
Statistics     → Learning From Data
```

This completes your Stage 7 reference sheet.
