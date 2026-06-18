# NumPy — Notes

## What Problem Does This Library Solve?

NumPy makes numerical computation on large datasets fast and memory-efficient by replacing Python lists with fixed-type, contiguous-memory arrays that support vectorized operations — turning loops into single-line math.

## Mental Model

Think of NumPy as **LINQ for number-crunching at C speed**. Python lists are like `ArrayList<Object>` — flexible but slow. NumPy arrays are like `int[]` in Java — fixed type, tightly packed in memory, operated on in bulk. Every operation is a vectorized bulk-transform (like `Array.map()` in JS but running in compiled C under the hood).

## Where It Fits

```text
Raw Data (CSV, JSON, API)
        │
        ▼
   ┌─────────┐
   │  Pandas  │  ← reads/cleans tabular data
   └────┬────┘
        │ .values / .to_numpy()
        ▼
   ┌─────────┐
   │  NumPy   │  ← the computation engine (you are here)
   └────┬────┘
        │
        ▼
   ┌──────────────┐
   │ Scikit-Learn  │  ← expects NumPy arrays as input
   │ PyTorch       │  ← tensors convert to/from NumPy
   │ Matplotlib    │  ← plots NumPy arrays
   └──────────────┘
```

- **Before NumPy:** Pandas (for loading/cleaning) or raw Python data
- **After NumPy:** Scikit-Learn (ML), PyTorch (deep learning), Matplotlib (viz)
- **Talks to:** Everything in the Python data science stack

## Core Concepts

### 1. ndarray — The Fundamental Object

```python
import numpy as np

# 1D array (like a Java int[])
a = np.array([1, 2, 3, 4, 5])

# 2D array (like a matrix or spreadsheet)
b = np.array([[1, 2, 3],
              [4, 5, 6]])

print(b.shape)   # (2, 3) — 2 rows, 3 columns
print(b.dtype)   # int64 — all elements same type
print(b.ndim)    # 2 — number of dimensions
```

Key properties: `shape`, `dtype`, `ndim`, `size` (total elements), `itemsize` (bytes per element).

### 2. Vectorization — No Loops Needed

```python
# Instead of looping through elements...
prices = np.array([100, 200, 300, 400])
discounted = prices * 0.9  # applies to ALL elements at once

# Element-wise operations (like broadcasting map over arrays)
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)    # [5, 7, 9]
print(a * b)    # [4, 10, 18]
print(a ** 2)   # [1, 4, 9]
```

Why: compiled C loops instead of interpreted Python loops → 10-100x faster.

### 3. Broadcasting — Shape Mismatch Handling

```python
# NumPy "stretches" smaller arrays to match larger ones
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])  # shape (2, 3)

row = np.array([10, 20, 30])    # shape (3,)

# row gets "broadcast" to every row of matrix
result = matrix + row
# [[11, 22, 33],
#  [14, 25, 36]]
```

Rule: dimensions are compared right-to-left. They must be equal or one of them must be 1.

### 4. Indexing and Slicing

```python
a = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]])

# Standard slicing (like Python lists but multi-dimensional)
print(a[0, :])     # first row: [1, 2, 3, 4]
print(a[:, 1])     # second column: [2, 6, 10]
print(a[0:2, 1:3]) # sub-matrix: [[2, 3], [6, 7]]

# Boolean indexing (like SQL WHERE)
print(a[a > 5])    # [6, 7, 8, 9, 10, 11, 12]

# Fancy indexing (pick specific indices)
print(a[[0, 2], :]) # rows 0 and 2
```

### 5. Reshaping — Same Data, Different View

```python
a = np.arange(12)          # [0, 1, 2, ..., 11]
b = a.reshape(3, 4)        # 3 rows × 4 cols (same data, new shape)
c = a.reshape(2, 2, 3)    # 3D: 2 "pages" × 2 rows × 3 cols

# -1 means "figure it out"
d = a.reshape(4, -1)       # (4, 3) — NumPy calculates the 3

# Flatten back to 1D
e = b.ravel()              # [0, 1, 2, ..., 11]
```

Critical for ML: models expect specific input shapes. You reshape constantly.

### 6. Axes — The Dimension You Operate Along

```python
data = np.array([[1, 2, 3],
                 [4, 5, 6]])

print(data.sum(axis=0))  # [5, 7, 9]  — collapse rows (sum down columns)
print(data.sum(axis=1))  # [6, 15]    — collapse columns (sum across rows)
```

Think of `axis=0` as "operate vertically" and `axis=1` as "operate horizontally."

## Key Functions/Methods

### Creating Arrays

| Function                       | Purpose                                         |
| ------------------------------ | ----------------------------------------------- |
| `np.array(list)`               | Convert Python list to ndarray                  |
| `np.zeros((r, c))`             | Array of zeros with given shape                 |
| `np.ones((r, c))`              | Array of ones                                   |
| `np.full((r, c), val)`         | Array filled with a specific value              |
| `np.arange(start, stop, step)` | Like `range()` but returns ndarray              |
| `np.linspace(start, stop, n)`  | n evenly spaced values between start and stop   |
| `np.eye(n)`                    | n×n identity matrix                             |
| `np.random.randn(r, c)`        | Random values from standard normal distribution |

### Shape Manipulation

| Function                       | Purpose                                   |
| ------------------------------ | ----------------------------------------- |
| `.reshape(new_shape)`          | Change shape without changing data        |
| `.ravel()` / `.flatten()`      | Collapse to 1D                            |
| `.T`                           | Transpose (swap rows and columns)         |
| `np.expand_dims(a, axis)`      | Add a dimension (useful for model inputs) |
| `np.squeeze(a)`                | Remove dimensions of size 1               |
| `np.concatenate([a, b], axis)` | Join arrays along an axis                 |
| `np.stack([a, b], axis)`       | Stack arrays along a new axis             |

### Math & Statistics

| Function                  | Purpose                  |
| ------------------------- | ------------------------ |
| `np.sum(a, axis)`         | Sum along axis           |
| `np.mean(a, axis)`        | Mean along axis          |
| `np.std(a, axis)`         | Standard deviation       |
| `np.min / np.max`         | Min/max values           |
| `np.argmin / np.argmax`   | Index of min/max         |
| `np.dot(a, b)` or `a @ b` | Matrix multiplication    |
| `np.sqrt(a)`              | Element-wise square root |
| `np.exp(a)`               | Element-wise e^x         |
| `np.log(a)`               | Element-wise natural log |

### Comparison & Filtering

| Function               | Purpose                                 |
| ---------------------- | --------------------------------------- |
| `a > 5`                | Element-wise comparison → boolean array |
| `a[a > 5]`             | Filter using boolean mask               |
| `np.where(cond, x, y)` | Ternary on arrays (like SQL CASE WHEN)  |
| `np.any(a > 5)`        | True if any element matches             |
| `np.all(a > 0)`        | True if all elements match              |

### Linear Algebra (np.linalg)

| Function            | Purpose                      |
| ------------------- | ---------------------------- |
| `np.linalg.norm(a)` | Vector/matrix norm (length)  |
| `np.linalg.inv(a)`  | Matrix inverse               |
| `np.linalg.eig(a)`  | Eigenvalues and eigenvectors |
| `np.linalg.svd(a)`  | Singular value decomposition |

## Common Patterns

### Normalize a Dataset (min-max scaling)

```python
# Scale values to 0-1 range — required before feeding to most ML models
data = np.array([[100, 0.5], [200, 0.8], [150, 0.3]])
normalized = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
```

### Compute Cosine Similarity

```python
# Measures how similar two vectors are (used in RAG, search, recommendations)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

embedding_1 = np.array([0.2, 0.5, 0.1])
embedding_2 = np.array([0.3, 0.4, 0.2])
print(cosine_similarity(embedding_1, embedding_2))  # ~0.96
```

### One-Hot Encoding

```python
# Convert categorical labels to binary vectors (needed for classification)
labels = np.array([0, 2, 1, 0, 2])
one_hot = np.eye(3)[labels]
# [[1,0,0], [0,0,1], [0,1,0], [1,0,0], [0,0,1]]
```

### Batch Processing

```python
# Split data into batches (batch = a chunk of data processed together in training)
data = np.arange(100).reshape(100, 1)
batch_size = 32
batches = [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
```

### Random Seed for Reproducibility

```python
# Same random numbers every run — essential for debugging ML experiments
rng = np.random.default_rng(seed=42)
weights = rng.standard_normal((3, 4))  # initial model weights
```

## AI/ML Connection

- **Where in the AI pipeline:** NumPy operates at preprocessing, training, and evaluation stages. It is the computation substrate — every library (Pandas, Scikit-Learn, PyTorch) converts data to/from NumPy arrays internally.

- **Concrete example — RAG:** When you build a RAG system (Module 2), document embeddings are NumPy arrays. You compute cosine similarity between a query embedding and all stored embeddings using `np.dot()` and `np.linalg.norm()` to find the most relevant documents.

- **Concrete example — Neural Networks:** PyTorch tensors (Module 1, 3) are NumPy arrays with GPU support and autograd. Converting between them is one call: `tensor.numpy()` / `torch.from_numpy(array)`. Understanding NumPy shapes and broadcasting transfers directly.

- **Concrete example — Feature Engineering:** Before training any model (Module 1), you normalize features (`(x - mean) / std`), handle missing values (`np.nan`), and reshape inputs — all NumPy operations.

- **Which IIT KGP modules use this:** All of them. Module 1 (tensor operations, embeddings), Module 2 (similarity search in RAG), Module 3 (weight matrices in fine-tuning), Module 4 (multimodal array manipulation), Module 5 (serving model outputs).

- **What breaks without it:** Without NumPy, computing dot products over 10,000 embedding vectors in Python lists takes seconds instead of milliseconds. Every ML library's `.fit()` and `.predict()` expects NumPy arrays — you can't train a single model without it.

- **Concrete example — Evaluation:** Metrics like accuracy, precision, recall are computed via NumPy boolean operations: `np.mean(predictions == labels)`.

- **Concrete example — Data Augmentation:** In computer vision (Module 4), image data is a NumPy array of shape `(height, width, channels)`. Flipping, rotating, and normalizing pixel values are all NumPy operations.

## Common Mistakes

1. **Modifying a view instead of a copy** — Slices return views (not copies). Modifying a slice modifies the original. Use `.copy()` when you need independence.

```python
a = np.array([1, 2, 3, 4])
b = a[1:3]   # b is a VIEW, not a copy
b[0] = 99    # a is now [1, 99, 3, 4] — surprise!
```

2. **Shape mismatch in broadcasting** — `(3,)` and `(3, 1)` are different shapes. Reshape explicitly when in doubt.

3. **Using Python `*` vs `@` for matrix multiplication** — `*` is element-wise, `@` (or `np.dot`) is matrix multiplication. Mixing them up is a silent bug.

4. **Integer overflow** — Default `int64` is fine, but if you explicitly use `int8` or `int16` for memory savings, values can overflow silently.

5. **Forgetting axis parameter** — `np.sum(matrix)` sums everything into one number. You usually want `np.sum(matrix, axis=0)` or `axis=1`.

6. **Comparing floats with `==`** — Floating point math is imprecise. Use `np.allclose(a, b)` instead of `a == b`.

## When NOT to Use

| Scenario                                          | Use Instead        |
| ------------------------------------------------- | ------------------ |
| Tabular data with mixed types (strings + numbers) | Pandas             |
| GPU-accelerated computation                       | PyTorch / CuPy     |
| Symbolic math (derivatives, integrals)            | SymPy              |
| Sparse matrices (mostly zeros)                    | SciPy.sparse       |
| Very large datasets that don't fit in RAM         | Dask, Polars       |
| Simple list operations without math               | Plain Python lists |

## Ready to Move On?

- ☐ I can create arrays using `array`, `zeros`, `ones`, `arange`, `linspace`, and `random`
- ☐ I can reshape, slice, and index multi-dimensional arrays without looking up docs
- ☐ I understand broadcasting rules and can predict the output shape of `a + b`
- ☐ I can compute dot products, norms, and cosine similarity
- ☐ I know the difference between a view and a copy

Once all checked → move to **Pandas**.
