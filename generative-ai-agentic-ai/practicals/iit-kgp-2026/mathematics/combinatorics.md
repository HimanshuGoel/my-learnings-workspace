# STAGE 2 — COMBINATORICS

# Mathematics of Counting, Arrangements & Possibilities

---

# BIG IDEA OF COMBINATORICS

Combinatorics answers:

```text id="a1"
“How many possible ways can something happen?”
```

Used heavily in:

* AI search spaces
* token generation
* recommendation systems
* planning systems
* workflow orchestration
* probability
* feature engineering

---

# 1. Addition Rule

## Meaning

Used when choices are:

```text id="a2"
OR choices
```

## Formula

```text id="a3"
m + n
```

## Example

* 3 pizza options
* 2 burger options

Total:

```text id="a4"
3 + 2 = 5
```

## Important Condition

Choices should not overlap.

## AI Connection

Different AI response modes:

* retrieval
* generation
* cached answer

## Mental Model

Separate alternatives → ADD

---

# 2. Multiplication Rule

## Meaning

Used when choices happen:

```text id="a5"
step-by-step / together
```

## Formula

```text id="a6"
m × n
```

## Example

* 3 shirts
* 2 pants

Total:

```text id="a7"
3 × 2 = 6
```

## AI Connection

Workflow combinations, token generation, agent planning

## Mental Model

Sequential choices → MULTIPLY

---

# 3. Slot Label Method

## Meaning

Represent positions as:

```text id="a8"
slots
```

Then:

* count choices per slot
* multiply them

## Example

2-digit PIN:

```text id="a9"
[_] [_]
10 × 10 = 100
```

## AI Connection

LLM token positions, workflow generation

## Mental Model

Count possibilities slot-by-slot

---

# 4. Permutations of Distinct Elements

## Meaning

Arrangement where:

```text id="a10"
ORDER matters
```

## Formula

```text id="a11"
n!
```

## Example

```text id="a12"
A,B,C
```

Arrangements:

```text id="a13"
ABC, ACB, BAC, BCA, CAB, CBA
```

Total:

```text id="a14"
3! = 6
```

## AI Connection

Token order, workflow order, rankings

## Mental Model

Different order = different arrangement

---

# 5. Permutations Using Product Rule

## Meaning

Permutation is:

```text id="a15"
repeated multiplication rule
```

## Example

Arrange:

```text id="a16"
A,B,C
```

Slots:

```text id="a17"
3 × 2 × 1
```

## Key Insight

Factorial comes from shrinking choices.

## AI Connection

Sequential planning paths

## Mental Model

Fill slots sequentially

---

# 6. Permutations of k Objects out of n

## Meaning

Arrange only:

```text id="a18"
some objects,
not all
```

## Formula

```text id="a19"
nPk = n! / (n-k)!
```

## Example

```text id="a20"
5P3 = 5×4×3 = 60
```

## AI Connection

Top-k ranking, beam search, candidate workflows

## Mental Model

Select AND arrange subset

---

# 7. Generalization of Permutations

## Meaning

Permutations with:

* restrictions
* constraints
* fixed positions

## Example

```text id="a21"
A cannot come first
```

## Problem Solving Style

* slot thinking
* subtract invalid cases
* apply restrictions

## AI Connection

Grammar constraints, safe workflows, dependency rules

## Mental Model

Arrangement under constraints

---

# 8. Permutations with Repetitions

## Meaning

Repetition allowed.

## Formula

```text id="a22"
n^k
```

## Example

3 digits, 2 slots:

```text id="a23"
3² = 9
```

## Important Difference

Choices do NOT reduce.

## AI Connection

LLM token generation

## Mental Model

Every slot keeps full choices

---

# 9. Generalization of Permutations with Repetitions

## Meaning

Repetition allowed:

```text id="a24"
BUT with constraints
```

## Examples

* first digit cannot be 0
* no repeated consecutive letters

## AI Connection

Constrained decoding, safe generation, retry limits

## Mental Model

Controlled sequence generation

---

# 10. Permutations of Identical Objects

## Meaning

Repeated identical objects reduce arrangements.

## Formula

```text id="a25"
n! / (a! × b! × c!)
```

## Example

```text id="a26"
AAB
```

Unique arrangements:

```text id="a27"
3!/2! = 3
```

## Important Insight

Swapping identical items creates no new arrangement.

## AI Connection

Repeated tokens, NLP redundancy, compression

## Mental Model

Correcting duplicate overcounting

---

# 11. Combinations

## Meaning

Selection where:

```text id="a28"
ORDER does NOT matter
```

## Formula

```text id="a29"
nCk = n! / (k!(n-k)!)
```

## Example

Choose 2 from:

```text id="a30"
A,B,C,D
```

Possible:

```text id="a31"
AB AC AD BC BD CD
```

## AI Connection

Feature selection, retrieval systems

## Mental Model

Form groups, not arrangements

---

# 12. Relation Between Permutations & Combinations

## Core Relationship

```text id="a32"
nPk = nCk × k!
```

## Meaning

Permutation =

```text id="a33"
selection + arrangement
```

## Example

* choose team
* assign positions

## AI Connection

Retrieval + ranking systems

## Mental Model

First choose, then arrange

---

# 13. Application of Product Rule

## Meaning

Break problem into:

```text id="a34"
sequential stages
```

Multiply possibilities at each stage.

## Example

* 2 starters
* 3 drinks
* 4 desserts

Total:

```text id="a35"
2×3×4 = 24
```

## AI Connection

Search spaces, workflows, prompt experiments

## Mental Model

Multi-stage branching

---

# 14. Pigeonhole Principle

## Meaning

If:

```text id="a36"
objects > containers
```

then:

```text id="a37"
some container must repeat
```

## Example

13 people, 12 months:

```text id="a38"
at least 2 share birth month
```

## AI Connection

Hash collisions, embedding overlaps, clustering

## Mental Model

Repetition becomes guaranteed

---

# MOST IMPORTANT FORMULAS

| Concept                | Formula               |
| ---------------------- | --------------------- |
| Addition Rule          | `m + n`               |
| Multiplication Rule    | `m × n`               |
| Factorial              | `n!`                  |
| Permutation            | `n!`                  |
| Partial Permutation    | `nPk = n!/(n-k)!`     |
| Repetition Permutation | `n^k`                 |
| Identical Objects      | `n!/(a!b!c!)`         |
| Combination            | `nCk = n!/(k!(n-k)!)` |
| Relation               | `nPk = nCk × k!`      |

---

# MOST IMPORTANT DIFFERENCES

| Concept     | Order Matters? |
| ----------- | -------------- |
| Permutation | YES            |
| Combination | NO             |

---

# EASY MEMORY TRICKS

| Concept              | Memory Trick                             |
| -------------------- | ---------------------------------------- |
| Addition Rule        | OR → Add                                 |
| Multiplication Rule  | AND → Multiply                           |
| Permutation          | Arrangement                              |
| Combination          | Group Selection                          |
| Factorial            | Shrinking choices                        |
| Repetition Allowed   | Choices stay same                        |
| No Repetition        | Choices reduce                           |
| Identical Objects    | Divide duplicate arrangements            |
| Pigeonhole Principle | Too many objects → repetition guaranteed |

---

# BIG AI CONNECTIONS

| Topic                   | AI Usage                |
| ----------------------- | ----------------------- |
| Multiplication Rule     | Search space growth     |
| Permutations            | Token ordering          |
| Combinations            | Feature selection       |
| Repetition Permutations | LLM generation          |
| Constraint Permutations | Structured decoding     |
| Product Rule            | Workflow orchestration  |
| Pigeonhole Principle    | Embedding collisions    |
| Factorials              | Computational explosion |

---

# BIGGEST LESSONS FROM STAGE 2

## 1. Search Spaces Grow VERY Fast

Small increases create huge combinations.

---

## 2. AI Systems Cannot Explore Everything

Why?
Because combinational explosion happens quickly.

---

## 3. Most AI Problems Involve:

* selection
* arrangement
* branching
* ranking
* sequence generation

which are all combinatorics problems.

---

# MOST IMPORTANT CONCEPTS FOR AI

Priority order:

1. Multiplication Rule
2. Permutations
3. Combinations
4. Search Space Growth
5. Repetition-Based Generation
6. Constraint-Based Generation
7. Product Rule Applications

---

# STAGE 2 BIG PICTURE

Stage 2 teaches:

* counting
* arrangements
* selection
* branching
* search spaces
* combinational explosion
* workflow possibilities

This becomes foundation for:

* probability
* machine learning
* LLM generation
* planning systems
* retrieval systems
* recommendation engines
* agentic AI


# STAGE 2 — COMBINATORICS QUICK REFERENCE TABLE

| Topic                               | Simple Meaning                                       | Key Formula / Symbol   | Real-Life Analogy    | AI / Software Connection | Mental Model                            |
| ----------------------------------- | ---------------------------------------------------- | ---------------------- | -------------------- | ------------------------ | --------------------------------------- |
| Addition Rule                       | Count separate OR choices                            | `m + n`                | Tea OR Coffee        | Multiple response modes  | Separate alternatives → Add             |
| Multiplication Rule                 | Count sequential AND choices                         | `m × n`                | Shirt AND Pant       | Workflow combinations    | Sequential choices → Multiply           |
| Slot Label Method                   | Fill positions step-by-step                          | `[_][_][_ ]`           | PIN/password slots   | Token positions          | Count slot-by-slot                      |
| Permutations of Distinct Elements   | Arrangement where order matters                      | `n!`                   | Seating order        | Token ordering           | Different order = different arrangement |
| Permutations Using Product Rule     | Permutation via shrinking choices                    | `n × (n-1) × ...`      | Filling seats        | Sequential planning      | Fill slots sequentially                 |
| Permutations of k out of n          | Arrange only some objects                            | `nPk = n!/(n-k)!`      | Medal positions      | Top-k ranking            | Select + arrange subset                 |
| Generalized Permutations            | Arrangement under restrictions                       | Constraint-based       | Fixed seating rules  | Safe workflows           | Constrained arrangements                |
| Permutations with Repetition        | Reuse allowed                                        | `n^k`                  | PIN codes            | LLM generation           | Choices stay same                       |
| Generalized Repetition Permutations | Repetition + constraints                             | Slot restrictions      | Password rules       | Structured decoding      | Controlled generation                   |
| Permutations of Identical Objects   | Duplicate items reduce arrangements                  | `n!/(a!b!c!)`          | AAB arrangements     | NLP redundancy           | Remove duplicate counting               |
| Combinations                        | Selection where order ignored                        | `nCk = n!/(k!(n-k)!)`  | Team selection       | Feature selection        | Form groups only                        |
| Relation of P & C                   | Permutation = combination + arrangement              | `nPk = nCk × k!`       | Team + positions     | Retrieval + ranking      | First choose, then arrange              |
| Application of Product Rule         | Multi-stage counting                                 | Multiply each stage    | Meal combinations    | Workflow orchestration   | Branching stages                        |
| Pigeonhole Principle                | More objects than containers → repetition guaranteed | `objects > containers` | 13 people, 12 months | Hash collisions          | Repetition unavoidable                  |

---

# QUICK FORMULA REFERENCE

| Concept                      | Formula               |
| ---------------------------- | --------------------- |
| Addition Rule                | `m + n`               |
| Multiplication Rule          | `m × n`               |
| Factorial                    | `n! = n×(n-1)×...×1`  |
| Permutation of n Objects     | `n!`                  |
| Partial Permutation          | `nPk = n!/(n-k)!`     |
| Repetition Allowed           | `n^k`                 |
| Identical Object Permutation | `n!/(a!b!c!)`         |
| Combination                  | `nCk = n!/(k!(n-k)!)` |
| Relation Between P & C       | `nPk = nCk × k!`      |

---

# PERMUTATION vs COMBINATION

| Feature        | Permutation    | Combination       |
| -------------- | -------------- | ----------------- |
| Order Matters? | YES            | NO                |
| Focus          | Arrangement    | Selection         |
| Example        | Race ranking   | Team selection    |
| AI Example     | Token ordering | Feature selection |
| Formula        | `nPk`          | `nCk`             |

---

# IMPORTANT GROWTH PATTERNS

| Type           | Growth Style | Example           |
| -------------- | ------------ | ----------------- |
| Addition       | Linear       | `5 + 5 = 10`      |
| Multiplication | Rapid        | `5 × 5 × 5 = 125` |
| Factorial      | Explosive    | `10! = 3,628,800` |
| Exponential    | Massive      | `1000^5`          |

---

# IMPORTANT AI CONNECTIONS

| Concept                 | AI Relevance             |
| ----------------------- | ------------------------ |
| Multiplication Rule     | Search space explosion   |
| Permutations            | Ordered token generation |
| Repetition Permutations | LLM sequence generation  |
| Combinations            | Feature selection        |
| Product Rule            | Workflow orchestration   |
| Constraints             | Structured generation    |
| Pigeonhole Principle    | Embedding collisions     |
| Factorials              | Computational complexity |

---

# EASY MEMORY TRICKS

| Concept              | Memory Trick                             |
| -------------------- | ---------------------------------------- |
| Addition Rule        | OR → Add                                 |
| Multiplication Rule  | AND → Multiply                           |
| Permutation          | Position matters                         |
| Combination          | Group matters                            |
| Factorial            | Shrinking choices                        |
| Repetition Allowed   | Choices stay constant                    |
| No Repetition        | Choices reduce                           |
| Identical Objects    | Divide duplicate arrangements            |
| Pigeonhole Principle | Too many objects → repetition guaranteed |

---

# BIGGEST LESSONS FROM STAGE 2

| Lesson                       | Meaning                                                |
| ---------------------------- | ------------------------------------------------------ |
| Search Spaces Grow Fast      | Small increases create huge possibilities              |
| AI Cannot Explore Everything | Exhaustive search becomes impossible                   |
| Constraints Matter           | Real systems restrict possibilities                    |
| Selection vs Arrangement     | Core distinction in problem solving                    |
| Sequential Decisions Explode | Multi-step AI systems become computationally expensive |

---

# STAGE 2 BIG PICTURE

Stage 2 teaches:

* counting
* arrangements
* selection
* branching
* constraints
* search spaces
* combinational explosion

Foundation for:

* probability
* machine learning
* LLM generation
* planning systems
* retrieval systems
* recommendation engines
* agentic AI
