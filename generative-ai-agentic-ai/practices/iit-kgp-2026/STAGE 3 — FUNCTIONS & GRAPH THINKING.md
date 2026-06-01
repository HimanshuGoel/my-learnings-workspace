# AI Mathematics Roadmap

# Stage 3 — Functions & Graph Thinking (Compact Notes)

---

# Big Picture

Stage 3 is about:

```text
How one thing changes when another thing changes
```

Functions model relationships.

Graphs visualize relationships.

This stage forms foundation for:

* AI
* machine learning
* analytics
* optimization
* software systems
* prediction systems

---

# 1. Functions

A function is:

```text
input → transformation → output
```

Rule:

```text
ONE input → ONE output
```

Example:
[
f(x)=x+2
]

[
f(3)=5
]

Mental model:

* vending machine
* programming function
* AI prediction model

Examples:

* hours worked → salary
* API requests → cost
* image → AI prediction

---

# Domain & Range

## Domain

All valid inputs.

## Range

All possible outputs.

---

# 2. What is NOT a Function?

Invalid if:

```text
ONE input → MULTIPLE outputs
```

Example:

```text
2 → 5
2 → 9
```

NOT a function.

Allowed:

```text
1 → 10
2 → 10
3 → 10
```

Multiple inputs can share same output.

---

# Vertical Line Test

If vertical line touches graph:

* once → function
* multiple times → NOT function

Example:

* circle is NOT a function

---

# 3. Visualising Functions Using Graphs

Graphs are:

```text
behavior visualizers
```

Axes:

* x-axis → input
* y-axis → output

Graphs help visualize:

* growth
* trends
* acceleration
* prediction
* anomalies

Shape tells story.

---

# 4. Linear Functions

Linear functions represent:

```text
constant change
```

General form:
[
y=mx+b
]

Graph:

* straight line

Examples:

* salary/hour
* taxi fare/km
* cloud pricing

Mental model:

```text
same effort → same reward
```

---

# 5. Slope & Intercept

Equation:
[
y=mx+b
]

## Slope (m)

Represents:

```text
rate of change
```

Higher slope:

* steeper line

Negative slope:

* decreasing behavior

Examples:

* speed
* salary growth
* user growth

---

## Intercept (b)

Represents:

```text
starting value
```

Example:
[
y=10x+50
]

* 50 = base fare
* 10 = per km cost

---

# 6. Polynomial Functions

Polynomial functions use:

* powers of x
* coefficients
* constants

Examples:
[
x^2,\ x^3,\ x^5
]

Mental model:

```text
changing change
```

Unlike linear functions:

* growth rate changes dynamically

Used for:

* realistic systems
* curves
* AI modeling
* graphics

---

# 7. General Form of Polynomial

General form:
[
a_nx^n + a_{n-1}x^{n-1} + ... + a_0
]

## Degree

Highest power of x.

Higher degree:

* more bends
* richer behavior

## Coefficients

Control:

* intensity
* steepness
* direction

Polynomial equation is:

```text
recipe for graph behavior
```

---

# 8. Quadratic Functions (Parabola)

General form:
[
y=ax^2+bx+c
]

Graph:

* parabola
* U-shape

Mental model:

```text
acceleration
```

Positive a:

* opens upward

Negative a:

* opens downward

Important ideas:

* vertex
* symmetry
* turning point

Used in:

* optimization
* physics
* AI loss curves
* projectile motion

---

# 9. Cubic Functions

General form:
[
y=ax^3+bx^2+cx+d
]

Graph:

* S-shaped behavior

Mental model:

```text
changing curvature
```

Important idea:

* inflection point

Used in:

* smooth transitions
* animations
* dynamic systems
* AI behavior modeling

---

# 10. Exponential Functions

General form:
[
y=a^x
]

Mental model:

```text
growth that grows itself
```

Linear:

```text
+10 +10 +10
```

Exponential:

```text
×2 ×2 ×2
```

Examples:

* compound interest
* viral growth
* AI scaling
* population growth

Key insight:

```text
starts slow → becomes explosive
```

---

# 11. Bases of Exponential Functions

Base controls:

```text
growth speed
```

Examples:
[
2^x,\ 3^x,\ 10^x
]

Larger base:

* faster growth

---

## Exponential Decay

If:
[
0<a<1
]

Example:
[
(\frac12)^x
]

Represents:

* decay
* shrinking systems

---

## Special Number e

[
e \approx 2.718
]

Represents:

```text
natural continuous growth
```

Very important in:

* AI
* optimization
* probability
* statistics

---

# 12. Logarithmic Functions

Logarithm is:

```text
inverse of exponential
```

Example:
[
2^3=8
]

Equivalent:
[
\log_2(8)=3
]

Mental model:

```text
counting multiplication steps
```

Used for:

* compression
* scaling
* binary search
* information theory

---

# Growth Comparison

| Type        | Behavior  |
| ----------- | --------- |
| Linear      | steady    |
| Polynomial  | curved    |
| Exponential | explosive |
| Logarithmic | slowing   |

---

# 13. Composite Functions

Composite function:

```text
function inside function
```

Notation:
[
f(g(x))
]

Meaning:

* apply g first
* then f

Mental model:

```text
transformation pipeline
```

Used in:

* middleware
* AI pipelines
* neural networks
* functional programming

Neural network:

```text
many composite functions stacked together
```

---

# 14. Inverse Functions

Inverse function:

```text
undoes transformation
```

Example:
[
f(x)=x+3
]

Inverse:
[
f^{-1}(x)=x-3
]

Mental model:

* encode/decode
* encrypt/decrypt
* serialize/deserialize

Important:

* not every function has inverse

Need:

```text
unique reversibility
```

---

# 15. Piecewise Functions

Piecewise functions:

```text
different rules for different regions
```

Mathematical if-else logic.

Example:
[
f(x)=
\begin{cases}
x & x<0 \
x^2 & x\ge0
\end{cases}
]

Used in:

* tax slabs
* pricing systems
* business rules
* AI activations

---

## ReLU Function

Very important in AI:
[
f(x)=
\begin{cases}
0 & x<0 \
x & x\ge0
\end{cases}
]

Negative values:

* blocked

Positive values:

* pass through

---

# 16. Continuous Functions

Continuous function:

```text
smooth without breaks
```

Mental model:

```text
draw without lifting pen
```

Key intuition:

```text
small input change
→
small output change
```

Examples:

* motion
* temperature
* sound waves
* AI loss curves

Continuity is foundational for:

* calculus
* gradients
* optimization

---

# 17. Discontinuity Types

Discontinuity:

```text
broken smoothness
```

---

## Jump Discontinuity

Sudden jump.

Example:

* tax slab change
* hard threshold

---

## Hole Discontinuity

Graph mostly smooth but missing point.

---

## Infinite Discontinuity

Function explodes toward infinity.

Example:
[
y=\frac1x
]

---

# Final Mental Model of Stage 3

Functions:

```text
model relationships
```

Graphs:

```text
visualize behavior
```

Linear systems:

```text
constant change
```

Polynomial systems:

```text
changing change
```

Exponential systems:

```text
self-growing growth
```

Logarithms:

```text
count exponential steps
```

Composite functions:

```text
chained transformations
```

Inverse functions:

```text
undo transformations
```

Piecewise functions:

```text
conditional behavior
```

Continuity:

```text
smooth behavior
```

Discontinuity:

```text
broken behavior
```

---

# What Stage 3 Really Built

You now understand mathematically:

```text
how systems behave and change
```

This is the foundation for:

* machine learning
* neural networks
* optimization
* AI training
* analytics
* dynamic systems
* software modeling

---

# Next Stage

# Stage 4 — Calculus Intuition

Topics:

* limits
* derivatives
* gradients
* optimization
* integration
* gradient descent
* why neural networks learn

| Function | Growth Style                |
| -------- | --------------------------- |
| (x)      | linear                      |
| (x^2)    | polynomial                  |
| (2^x)    | exponential                 |
| (10^x)   | very aggressive exponential |
| (e^x)    | natural continuous growth   |


# Stage 3 — Quick Revision Table

| Topic                  | Core Idea                              | Mental Model             | Key Formula / Shape | AI / Software Connection     |
| ---------------------- | -------------------------------------- | ------------------------ | ------------------- | ---------------------------- |
| Functions              | Input produces output                  | transformation machine   | (f(x))              | AI model = giant function    |
| Not a Function         | One input cannot have multiple outputs | ambiguity                | invalid mapping     | unstable APIs / bad labels   |
| Graphs                 | Visualize behavior                     | behavior visualizer      | x-axis & y-axis     | dashboards, analytics        |
| Linear Functions       | Constant change                        | steady growth            | (y=mx+b)            | linear regression            |
| Slope                  | Rate of change                         | steepness                | (m)                 | learning trend, scalability  |
| Intercept              | Starting value                         | base amount              | (b)                 | base pricing, default values |
| Polynomial Functions   | Changing change                        | curved behavior          | (x^2,x^3...)        | realistic system modeling    |
| Polynomial Degree      | Complexity of behavior                 | richer curves            | highest power       | advanced prediction          |
| Quadratic Functions    | Acceleration                           | parabola                 | (ax^2+bx+c)         | optimization, loss curves    |
| Cubic Functions        | Changing curvature                     | S-shape                  | (ax^3+bx^2+cx+d)    | smooth transitions           |
| Exponential Functions  | Self-growing growth                    | compounding              | (a^x)               | AI scaling, viral growth     |
| Exponential Base       | Controls growth speed                  | multiplier per step      | (2^x,10^x,e^x)      | compute explosion            |
| Exponential Decay      | Rapid shrinking                        | fading system            | ((1/2)^x)           | decay, learning rate         |
| Number e               | Natural continuous growth              | continuous compounding   | (e \approx 2.718)   | optimization, statistics     |
| Logarithms             | Reverse of exponential                 | count growth steps       | (\log_a(x))         | binary search, compression   |
| Composite Functions    | Functions chained together             | pipeline                 | (f(g(x)))           | neural networks              |
| Inverse Functions      | Undo transformation                    | reverse operation        | (f^{-1}(x))         | encode/decode                |
| Piecewise Functions    | Different rules in regions             | mathematical if-else     | piecewise notation  | business rules engine        |
| ReLU                   | Negative blocked, positive passes      | threshold gate           | piecewise graph     | deep learning activation     |
| Continuous Functions   | Smooth behavior                        | draw without lifting pen | smooth curves       | gradients, optimization      |
| Jump Discontinuity     | Sudden jump                            | cliff edge               | abrupt graph jump   | threshold systems            |
| Hole Discontinuity     | Missing point                          | broken tile              | hole in graph       | missing/corrupt data         |
| Infinite Discontinuity | Explodes near point                    | instability              | (1/x)               | unstable systems             |

---

# Growth Behavior Summary

| Function Type | Behavior              |
| ------------- | --------------------- |
| Linear        | constant growth       |
| Quadratic     | accelerating growth   |
| Cubic         | changing acceleration |
| Exponential   | explosive growth      |
| Logarithmic   | slowing growth        |

---

# Shape Recognition Cheat Sheet

| Function       | Typical Shape          |
| -------------- | ---------------------- |
| Linear         | straight line          |
| Quadratic      | U-shape                |
| Cubic          | S-shape                |
| Exponential    | hockey-stick explosion |
| Logarithmic    | fast then flattening   |
| Absolute Value | V-shape                |

---

# Most Important Equations

| Concept            | Equation           |
| ------------------ | ------------------ |
| Linear             | (y=mx+b)           |
| Quadratic          | (y=ax^2+bx+c)      |
| Cubic              | (y=ax^3+bx^2+cx+d) |
| Exponential        | (y=a^x)            |
| Logarithm          | (\log_a(x))        |
| Composite Function | (f(g(x)))          |
| Inverse Function   | (f^{-1}(x))        |

---

# AI Intuition Summary

| Mathematical Idea  | AI Meaning                        |
| ------------------ | --------------------------------- |
| Function           | prediction mapping                |
| Graph              | behavior visualization            |
| Slope              | learning direction                |
| Polynomial         | non-linear modeling               |
| Exponential        | scaling behavior                  |
| Logarithm          | compression & probability         |
| Composite Function | neural network layers             |
| Piecewise Function | activation behavior               |
| Continuity         | stable optimization               |
| Discontinuity      | unstable learning/system behavior |

---

# Final One-Line Summary

```text
Stage 3 taught:
how systems transform, grow, bend, scale, connect, reverse, and behave.
```
