# ML Classification — Explained Like You're New Here

No jargon. No code. Just plain language and everyday analogies.

Read this first, then the code will make much more sense.

---

## The Big Picture: What Is Classification?

**Classification = teaching a computer to sort things into categories.**

Examples from daily life:
- Email: Is this spam or not spam? (2 categories)
- Doctor: Is this tumour dangerous or harmless? (2 categories)
- Wine taster: Which vineyard did this wine come from? (3 categories)

That's literally what this entire assignment does. Nothing more.

---

## The Hospital Analogy (Part 1)

Imagine you're training a junior doctor to diagnose tumours from medical scans.

### The Data = Patient Records

You have a filing cabinet with 569 patient files. Each file has:
- **30 measurements** about the tumour (size, texture, shape, etc.) — these are the "features"
- **1 diagnosis** (malignant or benign) — this is the "label" or "target"

In code: the measurements = `X`, the diagnosis = `y`

### Train-Test Split = Study Material vs Exam

You give the junior doctor:
- **70% of files to study from** (training set) — they can see both measurements AND diagnosis
- **30% of files as an exam** (test set) — they only see measurements, must guess the diagnosis

Why? If you test them on files they already studied, you're testing their memory, not their skill. The test set simulates "a new patient walks in."

### Why Stratified?

If by bad luck your exam papers are all benign cases, the doctor never gets tested on catching cancer. **Stratified** means: keep the same ratio of cancer/healthy in both study material and exam.

---

## Scaling = Converting to the Same Units

Imagine comparing:
- Patient height: 170 cm
- Patient temperature: 37.2°C

If you ask "how different are two patients?" and just subtract numbers, height (170 vs 165 = difference of 5) looks way more important than temperature (37.2 vs 39.0 = difference of 1.8). But a 1.8°C fever is actually more alarming!

**Scaling** puts everything on the same yardstick (roughly -3 to +3). Now every measurement contributes fairly.

### Why Fit on Train Only?

The scaling formula needs to know the "average" and "spread" of each measurement. If you peek at the exam papers to calculate these, you're leaking exam information into your study process. That's cheating.

---

## The Models = Different Types of Doctors

Each model is a different approach to making diagnoses:

### Logistic Regression = The Rule-Based Doctor
"I'll give each measurement a weight. Big tumour radius gets +3 points toward 'cancer'. Smooth texture gets -2 points toward 'safe'. Add up all points. If total > 0, I say cancer."

Simple, fast, easy to explain. Works surprisingly well when the relationship is straightforward.

### KNN (K-Nearest Neighbours) = The "Similar Patients" Doctor
"Let me find the 5 patients in my training files that look MOST similar to this new patient. 3 of them had cancer, 2 didn't. Majority vote: I say cancer."

No learning happens. Just comparing to past cases. Like a doctor saying "I've seen this pattern before in patients who had cancer."

### Decision Tree = The Flowchart Doctor
"Is the tumour bigger than 2cm? Yes → Is it irregular shaped? Yes → Cancer. No → Probably safe."

Creates a series of yes/no questions. Very easy to explain to patients! But can get overly specific ("if radius is exactly 14.3 AND texture is 19.7 AND..." — that's memorising, not understanding).

### SVM (Support Vector Machine) = The Boundary-Drawing Doctor
"I'll draw a line (or curve) between cancer cases and safe cases in my data. New patient falls on the cancer side? Cancer."

Tries to make this boundary as wide as possible (maximum margin) for confidence.

### MLP (Neural Network) = The Intuition Doctor
"I can't explain my reasoning step by step, but after studying thousands of cases, I just... know. The patterns are too complex to write as simple rules."

Powerful but impossible to explain. A "black box."

---

## Hyperparameters = Adjusting Each Doctor's Behaviour

Every model has "knobs" you can turn:

- **KNN's K value**: "Should I look at 3 similar patients or 15?" (3 = quick judgment, 15 = more cautious)
- **Decision Tree's max_depth**: "How many questions can I ask?" (1 question = too simple, 20 questions = overthinking)
- **SVM's C**: "How much do I care about getting every training case right?" (Low = relaxed, High = perfectionist)

**GridSearchCV** = trying every combination of knob settings and seeing which combo scores best. It's like saying "try K=3, K=5, K=7... and tell me which works best."

---

## Evaluation = How Good Is This Doctor?

### Confusion Matrix = A Report Card

Think of it as a 2×2 table:

```
                    Doctor Said Safe    Doctor Said Cancer
Actually Safe:        "Correct! ✓"       "False alarm"
Actually Cancer:      "MISSED IT! ⚠️"    "Caught it! ✓"
```

### The Metrics (in plain English)

- **Accuracy**: "Out of all patients, what % did the doctor get right?"
  - Problem: if 95% of patients are healthy, saying "everyone is fine" gives 95% accuracy but catches ZERO cancers.

- **Recall**: "Out of all ACTUAL cancer patients, what % did the doctor catch?"
  - This is what matters for cancer. Missing cancer = patient might die.
  - Recall of 0.95 = caught 95 out of 100 cancer patients.

- **Precision**: "Out of everyone the doctor FLAGGED as cancer, what % actually had it?"
  - Low precision = lots of false alarms (healthy people getting scared).
  - But false alarms are better than missed cancers.

- **F1-Score**: "A balance between recall and precision."
  - Use when both matter equally (like the wine problem where no class is more important).

---

## Cross-Validation = Testing Multiple Times

Imagine you have 100 study files. Instead of one exam:
- **Round 1**: Study files 1-80, exam on 81-100
- **Round 2**: Study files 1-60 + 81-100, exam on 61-80
- **Round 3**: Study files 21-100, exam on 1-20
- ... and so on (5 rounds total)

Average the exam scores. This tells you if the doctor is **consistently good** or just **lucky on one exam**.

A doctor with "95% ± 2%" (stable) is better than one with "97% ± 15%" (unpredictable).

---

## Threshold Tuning = Adjusting How Suspicious the Doctor Is

Default: "I'll say cancer if I'm >50% sure."
Tuned: "I'll say cancer if I'm >30% sure."

Lowering the threshold means:
- ✅ Catches more cancers (higher recall)
- ❌ More false alarms (lower precision)

For cancer screening, we WANT a suspicious doctor. A false alarm means an extra test. A missed cancer means... much worse.

---

## Overfitting vs Underfitting = The Goldilocks Problem

### Underfitting (Too Simple)
A doctor who only knows one rule: "If the tumour exists, it's probably benign."
- Gets many training cases wrong
- Gets many exam cases wrong
- Problem: not enough learning

### Overfitting (Too Complex)
A doctor who memorises every training file: "Patient #347 had radius 14.3 and was benign, so any radius 14.3 is benign."
- Gets EVERY training case right (100%!)
- Fails on new patients because they don't match memorised patterns exactly
- Problem: memorised instead of understood

### Good Fit (Just Right)
A doctor who learned general patterns: "Larger, irregular tumours tend to be cancer."
- Gets most training cases right (~95%)
- Gets most exam cases right too (~93%)
- Small gap between training and exam performance

---

## Binary vs Multiclass = 2 Doors vs 3 Doors

**Binary (Part 1)**: Cancer or not? One important class to catch.
**Multiclass (Part 2)**: Which of 3 wine types? All equally important.

The only difference is:
- Binary → use Recall (catch the dangerous class)
- Multiclass → use Macro-F1 (be fair to all classes)

---

## The Learning Path (What to Focus On First)

Don't try to understand everything at once. Here's the priority:

### Understand First (Essential)
1. What is X (features) and y (target)?
2. Why split into train and test?
3. What does "train a model" mean? (show it examples, it finds patterns)
4. What is accuracy, recall, precision?

### Understand Next (Important)
5. Why scaling matters
6. What is a confusion matrix?
7. What is overfitting?
8. What does GridSearchCV do (at a high level)?

### Understand Later (Can Wait)
9. How each specific model works internally
10. Threshold tuning
11. Cross-validation mechanics
12. Specific hyperparameters and their effects

---

## One Final Thought

Every ML practitioner felt exactly what you're feeling right now. The terminology is designed to sound complicated, but the ideas behind them are mostly common sense:

- "Don't test on what you studied" → train-test split
- "Try different settings and pick the best" → GridSearchCV
- "Don't memorise, understand" → avoid overfitting
- "Missing cancer is worse than false alarms" → optimise recall
- "Put measurements on the same scale" → StandardScaler
- "Test multiple times to be sure" → cross-validation

You already understand the logic. The rest is just vocabulary.
