# PyTorch — Notes

## What Problem Does This Library Solve?

PyTorch lets you build, train, and deploy neural networks (deep learning models) with automatic gradient computation — enabling models that learn hierarchical patterns from raw data (images, text, audio) that traditional ML can't handle.

## Mental Model

Think of PyTorch as **Angular + NumPy + Automatic Calculus**. It gives you:
- **Tensors** = NumPy arrays that can run on GPU and track their own math history
- **Autograd** = automatic differentiation (computes gradients for you — no manual calculus)
- **nn.Module** = like Angular Components — self-contained units you compose into larger systems
- **Training loop** = the explicit, customizable lifecycle (unlike sklearn's one-line `.fit()`)

Alternatively: if Scikit-Learn is Spring Boot (convention over configuration, magic `.fit()`), PyTorch is **Express.js** — you write the training loop yourself, but you have full control over every step.

## Where It Fits

```
Preprocessed Data (NumPy arrays / Pandas DataFrames)
        │
        ▼
┌─────────────┐
│   PyTorch    │  ← define model, train loop, backprop (you are here)
└──────┬──────┘
       │
       ├── Trained model weights (.pt / .pth)
       │
       ▼
┌──────────────────────────────┐
│ What Uses PyTorch Under Hood  │
│ • HuggingFace Transformers    │
│ • LangChain (some backends)   │
│ • Stable Diffusion            │
│ • All modern LLM research     │
└──────────────────────────────┘
```

- **Before PyTorch:** Clean data (from Pandas/NumPy), or pre-trained models (from HuggingFace)
- **After PyTorch:** Trained model weights, fine-tuned LLMs, custom architectures
- **Talks to:** NumPy (seamless conversion), HuggingFace Transformers (built on PyTorch), CUDA/GPU (transparent acceleration)

## Core Concepts

### 1. Tensors — GPU-Enabled NumPy Arrays

```python
import torch

# Creating tensors (same as NumPy, different function names)
a = torch.tensor([1, 2, 3, 4])                # from list
b = torch.zeros(3, 4)                          # 3×4 zeros
c = torch.randn(3, 4)                          # random normal
d = torch.ones(2, 3, dtype=torch.float32)      # specify type

# Properties (same concepts as NumPy)
print(c.shape)       # torch.Size([3, 4])
print(c.dtype)       # torch.float32
print(c.device)      # cpu (or cuda:0 if on GPU)

# NumPy ↔ PyTorch conversion (shared memory!)
numpy_array = c.numpy()              # tensor → numpy
tensor_back = torch.from_numpy(numpy_array)  # numpy → tensor

# GPU acceleration (if available)
if torch.cuda.is_available():
    c_gpu = c.to("cuda")     # move to GPU
    c_cpu = c_gpu.to("cpu")  # move back
```

**Key difference from NumPy:** Tensors track computation history for automatic gradient calculation. That's why they exist — not just "NumPy on GPU."

### 2. Autograd — Automatic Differentiation

```python
# Autograd tracks operations on tensors and computes gradients automatically
# gradient = direction to adjust parameters to reduce error

x = torch.tensor([2.0, 3.0], requires_grad=True)  # "track this!"
y = x ** 2 + 3 * x + 1    # forward pass (compute output)
loss = y.sum()             # scalar loss value

loss.backward()            # compute gradients (backpropagation)
print(x.grad)              # dy/dx = 2x + 3 → [7.0, 9.0]
```

**Why this matters:** In neural networks, you need to know "if I nudge each weight slightly, how does the error change?" Autograd answers this for millions of parameters automatically. Without it, you'd compute partial derivatives by hand.

### 3. nn.Module — Building Blocks

```python
import torch.nn as nn

# nn.Module = the base class for all neural network components
# Think of it like Angular's Component class — you extend it

class SimpleClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes):
        super().__init__()
        # Define layers (like component template)
        self.layer1 = nn.Linear(input_dim, hidden_dim)   # fully connected
        self.relu = nn.ReLU()                            # activation function
        self.layer2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        # Define how data flows through layers (like render method)
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

# Usage
model = SimpleClassifier(input_dim=784, hidden_dim=128, num_classes=10)
output = model(input_tensor)  # calls forward() automatically
```

**Mental model:** `nn.Module` is like an Angular Component. `__init__` declares child components (layers). `forward()` defines the template (how data flows). You compose small modules into larger ones.

### 4. The Training Loop — The Heart of Deep Learning

```python
# Unlike sklearn's one-line .fit(), PyTorch makes you write the loop
# This gives you full control over every step

model = SimpleClassifier(784, 128, 10)
criterion = nn.CrossEntropyLoss()          # loss function (measures error)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # updates weights

# Training loop (runs for N epochs)
# epoch = one complete pass through all training data
for epoch in range(num_epochs):
    for batch_X, batch_y in train_loader:
        # 1. Forward pass — compute predictions
        outputs = model(batch_X)

        # 2. Compute loss — how wrong are we?
        loss = criterion(outputs, batch_y)

        # 3. Backward pass — compute gradients
        optimizer.zero_grad()   # reset gradients from last step
        loss.backward()         # compute new gradients

        # 4. Update weights — adjust parameters to reduce loss
        optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

**The 4 steps every iteration:**
1. **Forward** → compute output
2. **Loss** → measure error
3. **Backward** → compute gradients (autograd)
4. **Step** → update weights (optimizer)

### 5. DataLoader — Batching & Shuffling

```python
from torch.utils.data import DataLoader, TensorDataset

# Wrap your data in a Dataset
dataset = TensorDataset(
    torch.tensor(X_train, dtype=torch.float32),
    torch.tensor(y_train, dtype=torch.long)
)

# DataLoader handles batching, shuffling, parallel loading
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Iterating over batches
for batch_X, batch_y in train_loader:
    # batch_X shape: (32, num_features)
    # batch_y shape: (32,)
    pass
```

**Why batches:** You can't fit all data in GPU memory at once. Processing in batches of 32-128 samples is the standard approach. Also provides regularization through noise.

### 6. Common Layer Types

```python
# Fully connected (dense) — like a traditional neuron layer
nn.Linear(in_features, out_features)

# Activation functions — add non-linearity (without these, NN = linear regression)
nn.ReLU()       # most common: max(0, x)
nn.Sigmoid()    # squish to [0, 1] — for probabilities
nn.Softmax(dim=1)  # multi-class probabilities (sum to 1)

# Dropout — randomly disable neurons during training (prevents overfitting)
nn.Dropout(p=0.3)  # 30% of neurons turned off each forward pass

# Batch Normalization — stabilize training
nn.BatchNorm1d(num_features)

# Convolutional (for images)
nn.Conv2d(in_channels, out_channels, kernel_size)

# Recurrent (for sequences)
nn.LSTM(input_size, hidden_size, num_layers)

# Embedding (for token IDs → vectors)
nn.Embedding(vocab_size, embedding_dim)
```

### 7. Loss Functions & Optimizers

```python
# Loss functions (measure how wrong the model is)
nn.CrossEntropyLoss()    # classification (multi-class)
nn.BCELoss()             # binary classification
nn.MSELoss()             # regression (mean squared error)
nn.L1Loss()              # regression (mean absolute error)

# Optimizers (how to update weights)
torch.optim.SGD(model.parameters(), lr=0.01)          # simple, needs momentum
torch.optim.Adam(model.parameters(), lr=0.001)        # default choice (adaptive)
torch.optim.AdamW(model.parameters(), lr=0.001)       # Adam + weight decay (for Transformers)
```

**Rule of thumb:** Start with Adam (lr=0.001) for everything. Switch to AdamW for Transformers. SGD with momentum for computer vision if you want to squeeze extra performance.

### 8. Evaluation Mode & Inference

```python
# During evaluation/inference, disable dropout and batch norm updates
model.eval()
with torch.no_grad():  # don't track gradients (saves memory, faster)
    test_output = model(test_data)
    predictions = test_output.argmax(dim=1)

# Switch back to training mode
model.train()
```

### 9. Saving & Loading Models

```python
# Save model weights (recommended)
torch.save(model.state_dict(), "model.pth")

# Load into same architecture
model = SimpleClassifier(784, 128, 10)
model.load_state_dict(torch.load("model.pth"))
model.eval()
```

### 10. Device Management (CPU ↔ GPU)

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# In training loop, move data to same device as model
for batch_X, batch_y in train_loader:
    batch_X = batch_X.to(device)
    batch_y = batch_y.to(device)
    output = model(batch_X)
```

## Key Functions/Methods

### Tensor Creation

| Function | Purpose |
|----------|---------|
| `torch.tensor(data)` | From Python list/NumPy |
| `torch.zeros(shape)` | Zeros |
| `torch.ones(shape)` | Ones |
| `torch.randn(shape)` | Random normal |
| `torch.arange(start, end)` | Range |
| `torch.from_numpy(arr)` | From NumPy (shared memory) |

### Tensor Operations

| Operation | Purpose |
|-----------|---------|
| `a + b`, `a * b` | Element-wise math |
| `a @ b` / `torch.matmul(a, b)` | Matrix multiply |
| `a.reshape(shape)` | Reshape |
| `a.view(shape)` | Reshape (contiguous only) |
| `a.unsqueeze(dim)` | Add dimension |
| `a.squeeze()` | Remove size-1 dims |
| `torch.cat([a, b], dim)` | Concatenate |
| `torch.stack([a, b])` | Stack along new dim |

### Training Essentials

| Component | Purpose |
|-----------|---------|
| `model.parameters()` | All trainable weights |
| `optimizer.zero_grad()` | Clear old gradients |
| `loss.backward()` | Compute gradients |
| `optimizer.step()` | Update weights |
| `model.train()` | Enable training mode |
| `model.eval()` | Enable eval mode |
| `torch.no_grad()` | Disable gradient tracking |

## Common Patterns

### Complete Training Script Template

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# 1. Data
train_ds = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)

# 2. Model
model = MyModel().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# 3. Train
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        output = model(X_batch)
        loss = criterion(output, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}: Loss = {total_loss/len(train_loader):.4f}")

# 4. Evaluate
model.eval()
with torch.no_grad():
    preds = model(X_test_tensor.to(device)).argmax(dim=1)
    accuracy = (preds == y_test_tensor.to(device)).float().mean()
```

### Transfer Learning Pattern (Fine-Tuning)

```python
# Load pre-trained model, replace final layer, fine-tune
from torchvision import models

model = models.resnet18(pretrained=True)

# Freeze all layers (don't update during training)
for param in model.parameters():
    param.requires_grad = False

# Replace final layer (this one WILL be trained)
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Only train the new layer
optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
```

### Early Stopping

```python
best_val_loss = float("inf")
patience = 5
patience_counter = 0

for epoch in range(max_epochs):
    train_loss = train_one_epoch(model, train_loader)
    val_loss = evaluate(model, val_loader)

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), "best_model.pth")
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print("Early stopping!")
            break
```

## AI/ML Connection

- **Where in the AI pipeline:** PyTorch handles model architecture definition, training (forward pass + backprop + weight updates), and inference. It's the engine behind most modern AI research.

- **Concrete example — Transformers (Module 1):** HuggingFace's Transformers library is built on PyTorch. When you load BERT or GPT, you're loading a PyTorch `nn.Module`. Understanding PyTorch means you can peek inside, modify, and fine-tune these models.

- **Concrete example — Fine-Tuning (Module 3):** LoRA, PEFT, and QLoRA (parameter-efficient fine-tuning methods) all operate on PyTorch model parameters. You need PyTorch fundamentals to understand what's being frozen vs trained.

- **Concrete example — Custom Architectures (Module 4):** Building custom agents or multimodal models requires combining pre-trained modules (vision encoder + language model). This is PyTorch module composition.

- **Which IIT KGP modules use this:** Module 1 (understanding transformer internals), Module 3 (fine-tuning with PEFT/LoRA), Module 4 (custom agentic architectures), Module 5 (deployment optimization).

- **What breaks without it:** You can't fine-tune LLMs, understand how Transformers work internally, or build custom model architectures. PyTorch is the language modern AI thinks in.

- **Concrete example — Embeddings:** When you call `model.encode()` on a sentence-transformer, it's running a PyTorch forward pass. Understanding this demystifies "how do embeddings get created?"

- **From sklearn to PyTorch:** sklearn = one-line `.fit()` magic. PyTorch = you control the training loop. This control is necessary when training takes hours/days and you need checkpointing, learning rate scheduling, gradient accumulation, etc.

## Common Mistakes

1. **Forgetting `optimizer.zero_grad()`** — gradients accumulate by default. Without zeroing, each step adds to previous gradients → exploding updates.

2. **Not switching between `model.train()` and `model.eval()`** — dropout and batch norm behave differently during training vs inference. Forgetting `eval()` gives wrong test results.

3. **Forgetting `torch.no_grad()` during evaluation** — wastes memory tracking gradients you don't need. Also slower.

4. **Device mismatch** — model on GPU, data on CPU (or vice versa). Always `.to(device)` both model AND data.

5. **Wrong loss function** — using MSELoss for classification, or CrossEntropyLoss when you've already applied softmax (CrossEntropyLoss includes softmax internally).

6. **Not normalizing inputs** — neural networks train faster with normalized inputs (mean≈0, std≈1). Use the same normalization at inference time.

7. **Learning rate too high** — loss oscillates or explodes. Start with 1e-3 for Adam, reduce if unstable.

## When NOT to Use

| Scenario | Use Instead |
|----------|------------|
| Tabular data < 1M rows | Scikit-Learn (simpler, often better accuracy) |
| Quick prototyping without GPU | Scikit-Learn or XGBoost |
| Production serving (maximum speed) | ONNX Runtime, TensorRT |
| Simple feature extraction from pre-trained models | HuggingFace pipeline (hides PyTorch) |
| Distributed training at massive scale | PyTorch Lightning, DeepSpeed |

**Note:** For most of your IIT KGP coursework, you'll use PyTorch indirectly through HuggingFace. But understanding the fundamentals is essential for Module 3 (fine-tuning) and Module 4 (custom agents).

## Ready to Move On?

- ☐ I can create tensors, move them between CPU/GPU, and convert to/from NumPy
- ☐ I understand autograd (requires_grad, backward, grad) conceptually
- ☐ I can define a simple nn.Module with layers and a forward method
- ☐ I can write a training loop (forward, loss, backward, step)
- ☐ I know the difference between model.train() and model.eval()

Once all checked → move to **Transformers (HuggingFace)**.
