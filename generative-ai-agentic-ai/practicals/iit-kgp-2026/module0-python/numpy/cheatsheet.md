# NumPy — Cheatsheet

## Import

```python
import numpy as np
```

---

## Creating Arrays

```python
np.array([1, 2, 3])                  # from list
np.zeros((3, 4))                     # 3×4 of zeros
np.ones((2, 3))                      # 2×3 of ones
np.full((2, 2), 7)                   # 2×2 filled with 7
np.eye(3)                            # 3×3 identity matrix
np.arange(0, 10, 2)                  # [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)                 # [0, 0.25, 0.5, 0.75, 1.0]
np.empty((2, 3))                     # uninitialized (fast, use with care)
```

## Random

```python
rng = np.random.default_rng(42)      # reproducible generator
rng.random((3, 3))                   # uniform [0, 1)
rng.standard_normal((3, 3))          # normal (mean=0, std=1)
rng.integers(0, 10, size=(2, 3))     # random ints in [0, 10)
rng.choice([1, 2, 3], size=5)        # random picks with replacement
rng.shuffle(arr)                     # in-place shuffle
```

---

## Inspecting

```python
a.shape       # (rows, cols, ...)
a.ndim        # number of dimensions
a.size        # total element count
a.dtype       # data type (int64, float64, etc.)
a.itemsize    # bytes per element
```

---

## Reshaping

```python
a.reshape(3, 4)          # new shape (must have same total elements)
a.reshape(-1, 1)         # column vector (auto-calculate rows)
a.ravel()                # flatten to 1D (returns view)
a.flatten()              # flatten to 1D (returns copy)
a.T                      # transpose
np.expand_dims(a, 0)    # add axis: (3,) → (1, 3)
np.squeeze(a)            # remove axes of size 1
```

---

## Indexing & Slicing

```python
a[0]                     # first element (1D) or first row (2D)
a[1, 2]                  # row 1, col 2
a[:, 0]                  # all rows, first column
a[0:3, :]               # rows 0-2, all columns
a[::2]                   # every other element
a[-1]                    # last element/row
```

## Boolean & Fancy Indexing

```python
a[a > 5]                 # elements where condition is true
a[(a > 2) & (a < 8)]   # combine conditions (use & not 'and')
np.where(a > 5, a, 0)  # keep if > 5, else 0
a[[0, 2, 4]]            # pick specific indices
```

---

## Math (Element-wise)

```python
a + b          # addition
a - b          # subtraction
a * b          # element-wise multiply (NOT matrix multiply)
a / b          # division
a ** 2         # power
np.sqrt(a)     # square root
np.exp(a)      # e^x
np.log(a)      # natural log
np.abs(a)      # absolute value
np.clip(a, 0, 1)  # clamp values to [0, 1]
```

## Aggregation

```python
a.sum()              # sum all
a.sum(axis=0)        # sum along rows (column totals)
a.sum(axis=1)        # sum along columns (row totals)
a.mean(axis=0)       # mean per column
a.std()              # standard deviation
a.min() / a.max()   # min/max value
a.argmin() / a.argmax()  # index of min/max
np.cumsum(a)         # cumulative sum
```

---

## Linear Algebra

```python
a @ b                    # matrix multiply (same as np.dot for 2D)
np.dot(a, b)             # dot product / matrix multiply
np.linalg.norm(a)        # L2 norm (vector length)
np.linalg.inv(a)         # matrix inverse
np.linalg.det(a)         # determinant
np.linalg.eig(a)         # eigenvalues + eigenvectors
np.linalg.svd(a)         # singular value decomposition
```

---

## Combining Arrays

```python
np.concatenate([a, b], axis=0)   # stack vertically
np.concatenate([a, b], axis=1)   # stack horizontally
np.vstack([a, b])                # vertical stack (shorthand)
np.hstack([a, b])                # horizontal stack (shorthand)
np.stack([a, b], axis=0)         # stack along new axis
```

## Splitting Arrays

```python
np.split(a, 3, axis=0)           # split into 3 equal parts
np.hsplit(a, 2)                  # split horizontally
np.vsplit(a, 2)                  # split vertically
```

---

## Broadcasting Rules

```text
Shape A     Shape B     Result
(3, 4)      (4,)        (3, 4)    ✓ row added to each row
(3, 4)      (3, 1)      (3, 4)    ✓ column broadcast
(3, 4)      (3,)        ERROR     ✗ trailing dims don't match
```

Rule: compare shapes right-to-left. Each dimension must be equal or one must be 1.

---

## Copying

```python
b = a[1:3]       # VIEW — changes to b affect a
b = a.copy()     # COPY — independent
```

---

## Type Conversion

```python
a.astype(np.float32)     # cast to float32 (saves memory)
a.astype(int)            # cast to int
```

---

## Common AI Patterns

```python
# Normalize (min-max → 0 to 1)
norm = (a - a.min()) / (a.max() - a.min())

# Standardize (z-score → mean=0, std=1)
std = (a - a.mean()) / a.std()

# Cosine similarity
cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Softmax (convert scores to probabilities)
exp_a = np.exp(a - a.max())  # subtract max for numerical stability
softmax = exp_a / exp_a.sum()

# One-hot encoding
one_hot = np.eye(num_classes)[label_indices]
```

---

## Quick Reference Links

- [Official docs](https://numpy.org/doc/stable/)
- [Array creation routines](https://numpy.org/doc/stable/reference/routines.array-creation.html)
