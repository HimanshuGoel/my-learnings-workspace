# Stage 3 — Functions & Graph Thinking

## One-Line Summary

> Functions model how one thing changes when another changes — the mathematical foundation for every AI prediction, every neural network layer, and every optimization curve.

---

## Why This Matters for AI

- An AI model IS a function: input features → prediction. Training a model means finding the right function.
- Loss curves, learning rates, and optimization landscapes are all visualized through graphs of functions
- Neural network layers are composite functions chained together: `f(g(h(x)))`
- Activation functions (ReLU, sigmoid, softmax) are piecewise or special functions that give networks their power
- Understanding function behavior (growth, decay, continuity) builds intuition for model training dynamics

---

## Core Concepts

## 3.1 Function Basics

At its core, a function is a rule that takes an input and produces exactly one output. This simple idea is the building block for all of machine learning — every model is a function from features to predictions.

### 1. Functions

- **Meaning** — A function is a rule that assigns exactly one output to each input. It's a transformation machine: put something in, get something out, with no ambiguity.
- **Why It Exists** — We need a precise way to describe how things relate to each other. "Hours worked → salary earned" or "image pixels → classification label" — these are all functions.
- **Formula** — `f(x) = expression`. Example: `f(x) = x + 2`
- **Example** — `f(3) = 3 + 2 = 5`. Input 3, output 5. Always. Every time. No exceptions.
- **Mental Model** — A vending machine: insert a specific coin (input), get exactly one item (output). Same coin always gives same item.
- **AI Connection** — A trained neural network IS a function: `f(image) = "cat"`. The entire goal of training is to find the right function that maps inputs to correct outputs.
- **Common Mistake** — A function must give ONE output per input. Multiple inputs can map to the same output (that's fine), but one input cannot map to multiple outputs (that's not a function).

### 2. Domain & Range

- **Meaning** — The domain is the set of all valid inputs a function can accept. The range is the set of all possible outputs the function can produce.
- **Why It Exists** — Not every input makes sense for every function (you can't divide by zero, can't take √ of a negative in reals). Domain and range define the function's boundaries.
- **Example** — For `f(x) = √x`: domain = `[0, ∞)` (can't take square root of negative), range = `[0, ∞)` (output is always non-negative).
- **Mental Model** — Domain = all the keys on a keyboard that the machine accepts. Range = all the outputs the screen can display.
- **AI Connection** — Input validation: a model trained on images 224×224 has that as its domain. Feeding it a 1000×1000 image is "outside the domain." Output range defines possible predictions.

### 3. What is NOT a Function (Vertical Line Test)

- **Meaning** — If a single input can produce multiple different outputs, it's NOT a function. The vertical line test: if a vertical line crosses a graph at more than one point, it's not a function.
- **Why It Exists** — Functions require determinism — same input, same output. Ambiguous mappings (one input → multiple outputs) create unpredictable systems.
- **Example** — A circle `x² + y² = 1` is NOT a function because for x = 0, y can be +1 or -1 (two outputs for one input).
- **Mental Model** — A vending machine that randomly gives you chips OR soda for the same coin — that's broken (not a function).
- **AI Connection** — Unstable APIs, non-deterministic models (same prompt → different responses due to temperature sampling). Strictly speaking, a model with temperature > 0 is not a pure function — it's a stochastic process.

---

## 3.2 Function Visualization

Graphs let us SEE how functions behave — where they grow, shrink, bend, or break. This visual intuition is essential for understanding loss landscapes and training dynamics.

### 4. Graphs of Functions

- **Meaning** — A graph plots every (input, output) pair as a point on a coordinate plane, creating a visual picture of the function's behavior over its entire domain.
- **Why It Exists** — Humans understand patterns visually far better than through equations alone. A graph instantly reveals growth, decline, acceleration, anomalies, and trends.
- **Example** — The graph of `f(x) = x²` is a U-shaped parabola. You can immediately see it decreases, hits a minimum at x=0, then increases.
- **Mental Model** — A behavior visualizer. The x-axis is the input dial, the y-axis shows what happens.
- **AI Connection** — Loss curves (training progress), learning rate schedules, activation function shapes, model performance vs. data size curves — all are function graphs that guide ML decisions.

---

## 3.3 Linear Functions

The simplest meaningful functions: constant, predictable change. They form the backbone of linear regression and are the starting point for understanding more complex behaviors.

### 5. Linear Functions

- **Meaning** — A function where the output changes at a constant rate. The graph is always a straight line. Equal input increments produce equal output increments.
- **Why It Exists** — Many real-world relationships are approximately linear over reasonable ranges: cost per unit, salary per hour, distance per time at constant speed.
- **Formula** — `y = mx + b` where m = slope (rate of change) and b = y-intercept (starting value)
- **Example** — Taxi fare: `cost = 10 × km + 50`. Base fare ₹50 (intercept) + ₹10 per km (slope). At 5km: `10(5) + 50 = ₹100`.
- **Mental Model** — Walking on a perfectly flat ramp. Same effort per step gives same elevation gain.
- **AI Connection** — Linear regression (simplest ML model), the linear part of each neural network layer (`Wx + b`), and the baseline all more complex models are compared against.

### 6. Slope & Intercept

- **Meaning** — Slope (m) is the rate of change — how steep the line is, how much output changes per unit of input. Intercept (b) is the output value when input is zero — the starting point.
- **Why It Exists** — These two numbers completely define a line. Understanding them separately lets you reason about trends (slope) independently from baselines (intercept).
- **Formula** — In `y = mx + b`: slope = `(y₂ - y₁) / (x₂ - x₁)`, intercept = value of y when x = 0
- **Example** — `y = 3x + 100`. Slope = 3 (output grows by 3 for every 1 unit of input). Intercept = 100 (starting value).
- **Mental Model** — Slope = steepness of a hill. Intercept = altitude at the starting line.
- **AI Connection** — In gradient descent, the slope of the loss function tells you the learning direction. A positive slope means "move left to reduce loss," negative means "move right." The slope IS the gradient in 1D. (→ See calculus.md § Derivative)

---

## 3.4 Polynomial Functions

When relationships aren't constant (the rate of change itself changes), polynomials model this "changing change." They introduce curves, acceleration, and richer behavior.

### 7. Polynomial Functions

- **Meaning** — Functions that use powers of x combined with coefficients and constants. Unlike linear functions where growth is constant, polynomials have growth rates that change dynamically.
- **Why It Exists** — Most real systems don't grow linearly. Revenue accelerates, populations plateau, physics involves squares and cubes. Polynomials capture these curved behaviors.
- **Formula** — General: `aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₁x + a₀`
- **Example** — `f(x) = 2x³ - 5x² + 3x + 1` — a cubic polynomial with degree 3.
- **Mental Model** — Linear = constant speed. Polynomial = acceleration (speed itself is changing).
- **AI Connection** — Non-linear modeling: real-world data rarely fits straight lines. Polynomial features in regression, loss function shapes, and the theoretical capacity of neural networks to approximate any function.

### 8. Degree and Coefficients

- **Meaning** — The degree is the highest power of x (determines complexity and number of curves). Coefficients control the intensity and direction of each term.
- **Why It Exists** — Degree tells you the maximum complexity of behavior (how many turns the graph can make). Coefficients fine-tune the shape.
- **Example** — Degree 1: straight line (1 behavior). Degree 2: one curve. Degree 3: up to two curves (S-shape). Degree n: up to n-1 turns.
- **Mental Model** — Degree = how many bends in the road. Coefficients = how sharp each bend is.
- **AI Connection** — Higher-degree polynomials can fit more complex data but risk overfitting — the bias-variance tradeoff.

### 9. Quadratic Functions (Parabola)

- **Meaning** — Polynomial of degree 2. The graph is a U-shaped curve (parabola) with exactly one turning point (vertex). Represents acceleration or deceleration.
- **Why It Exists** — Quadratics model anything with a peak or valley: projectile paths, optimization problems, diminishing returns. They're the simplest functions with a minimum or maximum.
- **Formula** — `y = ax² + bx + c`. If a > 0: opens upward (has minimum). If a < 0: opens downward (has maximum).
- **Example** — `y = x² - 4x + 3` has vertex at x=2 (minimum point). This is like a loss function with an optimal point.
- **Mental Model** — A ball thrown upward: rises (decelerating), reaches peak, then falls (accelerating). The vertex is the turning point.
- **AI Connection** — Mean Squared Error loss function is quadratic in the parameters (for linear models). The U-shape guarantees a single minimum — gradient descent will find it. This is why MSE is so popular.

### 10. Cubic Functions

- **Meaning** — Polynomial of degree 3. The graph has an S-shaped curve with an inflection point where the curvature changes direction.
- **Why It Exists** — Cubics model transitions: systems that accelerate, then decelerate (or vice versa). They capture more complex dynamics than quadratics.
- **Formula** — `y = ax³ + bx² + cx + d`
- **Example** — An adoption curve: slow start (few users), rapid growth (viral phase), then plateau. The inflection point is where growth is fastest.
- **Mental Model** — Changing curvature: the road bends one way, then bends the other way. The inflection point is where it switches.
- **AI Connection** — S-shaped activation functions (sigmoid, tanh), technology adoption curves, and learning curves often follow cubic-like behavior with inflection points.

---

## 3.5 Exponential & Logarithmic Functions

These functions model the most extreme behaviors: explosive growth and its inverse (compression). Understanding them is essential for AI scaling laws, probability, and information theory.

### 11. Exponential Functions

- **Meaning** — Functions where the variable is in the exponent: `y = aˣ`. Growth multiplies rather than adds — the output grows proportionally to its current value.
- **Why It Exists** — Many real phenomena grow multiplicatively: compound interest, viral spread, bacterial growth, compute scaling. Exponential growth starts slow then becomes explosive.
- **Formula** — `y = aˣ` where a > 1 for growth, 0 < a < 1 for decay
- **Example** — `2ˣ`: at x=1 → 2, x=5 → 32, x=10 → 1024, x=20 → 1,048,576. Doubles each step.
- **Mental Model** — Linear: `+10, +10, +10`. Exponential: `×2, ×2, ×2`. Same operation (multiplication) but the numbers themselves grow, making each step larger than the last.
- **AI Connection** — AI compute scaling (training cost doubles per model generation), combinatorial explosion, softmax function uses `eˣ`, neural scaling laws show exponential relationships between compute and performance.

### 12. The Number e and Exponential Bases

- **Meaning** — `e ≈ 2.718` is a special mathematical constant representing "natural continuous growth." It appears whenever growth is continuous rather than discrete. The base of an exponential controls growth speed.
- **Why It Exists** — `e` emerges naturally from compound interest taken to its limit. It makes calculus clean (derivative of eˣ = eˣ) and appears in probability, statistics, and information theory.
- **Formula** — `eˣ` for natural growth. Larger bases (10ˣ) grow faster. `(1/2)ˣ` represents decay.
- **Example** — Continuous compound interest: invest ₹1 at 100% interest compounded continuously = ₹e ≈ ₹2.72 after one year (not ₹2).
- **Mental Model** — `e` is the "speed limit" of how fast something can grow when growth is continuous and proportional to current size.
- **AI Connection** — Softmax: `eˣ / Σeˣ` converts raw scores to probabilities. Natural log loss. Learning rate decay schedules. The entire probability framework of ML rests on `e`.

### 13. Logarithmic Functions

- **Meaning** — The logarithm is the inverse of the exponential: if `aˣ = y`, then `logₐ(y) = x`. It answers: "what power do I need to raise a to, in order to get y?"
- **Why It Exists** — Exponentials grow too fast to work with directly. Logarithms compress massive ranges into manageable ones. They convert multiplication into addition, making computation easier.
- **Formula** — `logₐ(y) = x` means `aˣ = y`. Common: log₁₀, Natural: ln = logₑ, Binary: log₂
- **Example** — `log₂(8) = 3` because `2³ = 8`. How many times must you double 1 to reach 8? Answer: 3 times.
- **Mental Model** — "How many multiplication steps does it take to reach this number?" Logarithm counts the growth steps.
- **AI Connection** — Cross-entropy loss uses log. Information theory (bits = log₂). Binary search is O(log n). Log-scale plots for visualizing training over many orders of magnitude. Log-probability is used everywhere in NLP to avoid numerical underflow.

| Function | Growth Style | Shape |
| -------- | ------------ | ----- |
| Linear `x` | Steady | Straight line |
| Quadratic `x²` | Accelerating | U-curve |
| Exponential `2ˣ` | Explosive | Hockey stick |
| Logarithmic `log(x)` | Slowing | Fast then flattening |

---

## 3.6 Function Composition & Transformation

Real AI systems don't use single functions — they chain many functions together. This section covers how functions combine and undo each other.

### 14. Composite Functions

- **Meaning** — A composite function applies one function after another: feed the output of g(x) into f. The result is `f(g(x))` — a pipeline of transformations.
- **Why It Exists** — Complex transformations are built from simple ones chained together. A neural network is literally many simple functions composed: `layer3(layer2(layer1(input)))`.
- **Formula** — `(f ∘ g)(x) = f(g(x))` — apply g first, then f to the result
- **Example** — `g(x) = x + 1`, `f(x) = x²`. Then `f(g(3)) = f(4) = 16`. First add 1, then square.
- **Mental Model** — A factory assembly line: raw material passes through machine g, the output goes into machine f, and you get the final product.
- **AI Connection** — A neural network with 3 layers IS `f₃(f₂(f₁(x)))` — three composite functions. The depth of the network = depth of composition. This is what makes deep learning "deep."
- **Common Mistake** — Order matters! `f(g(x)) ≠ g(f(x))` in general. Squaring then adding 1 is different from adding 1 then squaring.

### 15. Inverse Functions

- **Meaning** — An inverse function undoes what the original function did. If `f(x) = y`, then `f⁻¹(y) = x`. It reverses the transformation.
- **Why It Exists** — Sometimes we need to go backwards: decode what was encoded, decrypt what was encrypted, recover original data from transformed data.
- **Formula** — `f⁻¹(f(x)) = x` and `f(f⁻¹(x)) = x`
- **Example** — `f(x) = x + 3` → `f⁻¹(x) = x - 3`. `f(x) = 2x` → `f⁻¹(x) = x/2`. Each undoes the other.
- **Mental Model** — Encode/decode, encrypt/decrypt, serialize/deserialize — any reversible transformation has an inverse.
- **AI Connection** — Autoencoders (encoder + decoder), invertible neural networks (normalizing flows), tokenization/detokenization, lossy vs lossless compression.
- **Common Mistake** — Not every function has an inverse. A function must be one-to-one (different inputs give different outputs) to be invertible. `f(x) = x²` has no inverse because both 3 and -3 map to 9.

---

## 3.7 Special Function Types

These function types appear constantly in AI systems — from activation functions to pricing models to stability analysis.

### 16. Piecewise Functions

- **Meaning** — A function that uses different rules for different regions of its input. It's mathematical if-else logic: "if x < 0, do this; if x ≥ 0, do that."
- **Why It Exists** — Many real systems behave differently under different conditions: tax slabs, tiered pricing, thresholds. Piecewise functions model these discontinuous rules.
- **Formula** — `f(x) = { rule₁ if condition₁; rule₂ if condition₂; ... }`
- **Example** — ReLU activation: `f(x) = 0 if x < 0; f(x) = x if x ≥ 0`. Blocks negative values, passes positive values through.
- **Mental Model** — A road with different speed limits in different zones. Same road, different rules depending on where you are.
- **AI Connection** — ReLU (most popular activation function in deep learning) is piecewise. Tax calculations, tiered API pricing, learning rate schedules with warmup — all piecewise functions.

**ReLU Deep Dive:** ReLU's simplicity (`max(0, x)`) makes it computationally efficient and avoids the vanishing gradient problem. It's the default activation in modern networks.

### 17. Continuous Functions

- **Meaning** — A function where small input changes produce small output changes — no sudden jumps, no gaps, no breaks. You can draw the graph without lifting your pen.
- **Why It Exists** — Continuity is the foundation for calculus and optimization. Gradient descent REQUIRES continuity — you can't smoothly slide downhill if there are cliffs.
- **Formula** — Formally: for any ε > 0, there exists δ > 0 such that |x - a| < δ implies |f(x) - f(a)| < ε
- **Example** — Temperature over time is continuous (it doesn't teleport between values). Stock prices are approximately continuous at fine time scales.
- **Mental Model** — Draw without lifting your pen. Smooth, connected, no teleportation.
- **AI Connection** — Neural network optimization assumes loss functions are continuous (and ideally smooth). Discontinuous loss = gradient descent breaks. This is why smooth activation functions (sigmoid, tanh, GELU) and smooth loss functions are preferred.

### 18. Discontinuity Types

- **Meaning** — A discontinuity is where a function "breaks" — where small input changes cause large or undefined output changes.
- **Why It Exists** — Understanding discontinuities helps identify where optimization will fail, where models become unstable, and where careful handling is needed.
- **Types:**
  - **Jump Discontinuity** — sudden jump to a different value (like tax brackets)
  - **Hole Discontinuity** — function is smooth everywhere except one missing point
  - **Infinite Discontinuity** — function explodes toward infinity (like `1/x` at x=0)
- **Mental Model** — Jump = cliff edge. Hole = missing tile in an otherwise smooth floor. Infinite = bottomless pit.
- **AI Connection** — Exploding gradients (infinite discontinuity in loss landscape), threshold-based decisions (jump discontinuity), missing data points (hole discontinuity). Understanding these helps diagnose training failures.

---

## Quick Reference Tables

### Table 1 — Function Types Overview

| Function | Growth Behavior | Graph Shape | AI Connection |
| -------- | --------------- | ----------- | ------------- |
| Linear `y = mx + b` | Constant change | Straight line | Linear regression, neuron pre-activation |
| Quadratic `y = ax² + bx + c` | Accelerating change | U-shape (parabola) | MSE loss function, optimization |
| Cubic `y = ax³ + ...` | Changing acceleration | S-shape | Sigmoid-like transitions |
| Exponential `y = aˣ` | Explosive (self-growing) | Hockey stick | Scaling laws, softmax, growth |
| Logarithmic `y = logₐ(x)` | Slowing (compressed) | Fast then flat | Cross-entropy loss, information theory |
| Piecewise | Region-dependent | Broken/segmented | ReLU activation, tiered pricing |

---

### Table 2 — Key Equations

| Concept | Equation | What It Represents |
| ------- | -------- | ------------------ |
| Linear | `y = mx + b` | Constant rate of change |
| Quadratic | `y = ax² + bx + c` | Single peak/valley optimization |
| Cubic | `y = ax³ + bx² + cx + d` | Inflection and transition |
| Exponential | `y = aˣ` | Multiplicative growth |
| Natural Exponential | `y = eˣ` | Continuous natural growth |
| Logarithm | `y = logₐ(x)` | Inverse of exponential |
| Composite | `f(g(x))` | Chained transformations |
| Inverse | `f⁻¹(f(x)) = x` | Undo a transformation |

---

### Table 3 — AI Translation Table

| Mathematical Idea | AI Meaning |
| ----------------- | ---------- |
| Function | Prediction model (input → output) |
| Domain | Valid input space |
| Range | Possible output space |
| Graph | Behavior visualization (loss curves, metrics) |
| Slope | Learning direction, gradient (1D) |
| Polynomial | Non-linear modeling capability |
| Exponential | Scaling behavior, compute growth |
| Logarithm | Compression, cross-entropy, information |
| Composite Function | Neural network layers stacked together |
| Inverse Function | Encoder/decoder, tokenizer/detokenizer |
| Piecewise Function | Activation function (ReLU), business rules |
| Continuity | Requirement for smooth optimization |
| Discontinuity | Training instability, exploding gradients |

---

### Table 4 — Shape Recognition

| Function | Typical Shape | Quick Identifier |
| -------- | ------------- | ---------------- |
| Linear | Straight line | Constant slope |
| Quadratic | U-shape or ∩-shape | One turning point |
| Cubic | S-shape | One inflection point |
| Exponential | Hockey stick | Accelerating forever |
| Logarithmic | Fast rise then flat | Decelerating forever |
| Absolute Value | V-shape | Sharp corner at origin |
| ReLU | Flat then rising | Zero left, linear right |

---

## Memory Map

```text
Function Basics
  ├── What is a function? (input → one output)
  ├── Domain (valid inputs) & Range (possible outputs)
  └── Vertical Line Test (validates it's a function)
      ↓
Linear Functions (constant change)
  ├── y = mx + b
  ├── Slope = rate of change
  └── Intercept = starting value
      ↓
Polynomial Functions (changing change)
  ├── Quadratic: U-shape, one min/max
  ├── Cubic: S-shape, inflection point
  └── Higher degree: more bends, richer behavior
      ↓
Exponential & Logarithmic (extreme behaviors)
  ├── Exponential: multiplicative growth (aˣ)
  ├── e ≈ 2.718: natural continuous growth
  └── Logarithm: inverse of exponential, compression
      ↓
Function Composition & Transformation
  ├── Composite: f(g(x)) = pipeline = neural network depth
  └── Inverse: f⁻¹ = undo = decoder
      ↓
Special Types
  ├── Piecewise: different rules per region (ReLU)
  ├── Continuous: smooth, no jumps (optimization works)
  └── Discontinuous: breaks (optimization fails)
      ↓
Foundation for:
  ├── Calculus (rates of change OF functions)
  ├── Neural Networks (composed functions)
  ├── Optimization (finding function minima)
  └── Training Dynamics (loss function behavior)
```

---

## Interview / Revision Summary

| Concept | Remember This |
| ------- | ------------- |
| Function | Input → exactly one output; an AI model IS a function |
| Domain & Range | Valid inputs and possible outputs |
| Linear | Constant change; `y = mx + b`; simplest model |
| Slope | Rate of change = gradient in 1D |
| Quadratic | U-shape with one min/max; MSE loss is quadratic |
| Exponential | Self-multiplying growth; scaling laws, softmax |
| e ≈ 2.718 | Natural growth constant; derivative of eˣ is eˣ |
| Logarithm | Inverse of exponential; cross-entropy, information |
| Composite | f(g(x)); neural network = stacked compositions |
| Inverse | Undo; encode/decode pairs |
| Piecewise | Different rules per region; ReLU = `max(0, x)` |
| Continuity | Smooth = optimization works; breaks = instability |

---

### If Someone Asks: "How do functions relate to neural networks?"

> A neural network is fundamentally a large composite function. Each layer applies a linear transformation (`Wx + b`) followed by a nonlinear activation function (like ReLU), and these are composed: `output = f₃(f₂(f₁(input)))`. The "depth" of a deep network is literally the depth of function composition. Training means finding the parameters (weights) that make this composite function map inputs to correct outputs. The loss function measures how wrong the current function is, and gradient descent uses the slope (derivative) of the loss to improve it. Continuity of the loss function is required for gradient-based optimization to work, which is why smooth activations are preferred. The entire field of deep learning is the study of parameterized composite functions and how to optimize them.
