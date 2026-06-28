# PyTorch — Cheatsheet

## Import

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
```

---

## Tensor Creation

```python
torch.tensor([1, 2, 3])                   # from list
torch.zeros(3, 4)                          # zeros
torch.ones(2, 3)                           # ones
torch.randn(3, 4)                          # random normal
torch.rand(3, 4)                           # random uniform [0, 1)
torch.arange(0, 10, 2)                    # [0, 2, 4, 6, 8]
torch.linspace(0, 1, 5)                   # 5 evenly spaced
torch.eye(3)                               # identity
torch.full((2, 3), 7.0)                   # filled with 7
torch.empty(3, 4)                          # uninitialized
```

## NumPy ↔ PyTorch

```python
tensor = torch.from_numpy(numpy_arr)       # numpy → tensor (shared memory)
numpy_arr = tensor.numpy()                 # tensor → numpy (CPU only)
numpy_arr = tensor.detach().cpu().numpy()  # safe conversion from GPU
```

---

## Tensor Properties

```python
t.shape          # dimensions
t.dtype          # data type (float32, int64, etc.)
t.device         # cpu or cuda:0
t.requires_grad  # tracking gradients?
t.ndim           # number of dimensions
t.numel()        # total element count
```

---

## Tensor Operations

```python
# Math (same as NumPy)
a + b    a - b    a * b    a / b    a ** 2
torch.sqrt(a)    torch.exp(a)    torch.log(a)
torch.clamp(a, min=0, max=1)

# Matrix multiply
a @ b                    # operator
torch.matmul(a, b)      # function
torch.mm(a, b)          # strictly 2D

# Reductions
a.sum()    a.mean()    a.std()
a.sum(dim=0)    a.max(dim=1)    a.argmax(dim=1)

# Shape manipulation
a.reshape(3, 4)         # reshape
a.view(3, 4)            # reshape (must be contiguous)
a.unsqueeze(0)          # add dim: (3,) → (1, 3)
a.squeeze()             # remove size-1 dims
a.permute(1, 0, 2)     # reorder dimensions
a.flatten()             # to 1D
torch.cat([a, b], dim=0)    # concatenate
torch.stack([a, b], dim=0)  # stack (new dim)
```

---

## Device Management

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tensor = tensor.to(device)
model = model.to(device)
```

---

## Autograd

```python
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x
y.backward()            # compute gradient
print(x.grad)           # dy/dx = 2*2 + 3 = 7

# Disable gradient tracking
with torch.no_grad():
    inference_output = model(data)

# Detach from computation graph
detached = tensor.detach()
```

---

## nn.Module (Model Definition)

```python
class MyModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.net(x)

model = MyModel(784, 256, 10).to(device)
```

---

## Common Layers

```python
nn.Linear(in, out)          # fully connected
nn.ReLU()                   # activation: max(0, x)
nn.Sigmoid()                # squish to [0, 1]
nn.Softmax(dim=1)           # probabilities (sum to 1)
nn.Dropout(p=0.3)           # regularization
nn.BatchNorm1d(features)    # normalize activations
nn.Conv2d(in_ch, out_ch, k) # convolution (images)
nn.LSTM(input, hidden, layers) # recurrent (sequences)
nn.Embedding(vocab, dim)    # lookup table (tokens → vectors)
nn.LayerNorm(dim)           # Transformer-style norm
nn.MultiheadAttention(dim, heads) # attention mechanism
```

---

## Loss Functions

```python
nn.CrossEntropyLoss()       # multi-class classification (includes softmax)
nn.BCEWithLogitsLoss()      # binary classification (includes sigmoid)
nn.MSELoss()                # regression
nn.L1Loss()                 # MAE regression
nn.NLLLoss()                # with log_softmax output
```

## Optimizers

```python
optim.Adam(model.parameters(), lr=1e-3)         # default choice
optim.AdamW(model.parameters(), lr=1e-3)        # for Transformers
optim.SGD(model.parameters(), lr=0.01, momentum=0.9)  # classic
```

---

## Training Loop

```python
model.train()
for epoch in range(num_epochs):
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)

        optimizer.zero_grad()           # 1. clear gradients
        output = model(X_batch)         # 2. forward pass
        loss = criterion(output, y_batch)  # 3. compute loss
        loss.backward()                 # 4. backprop
        optimizer.step()                # 5. update weights
```

## Evaluation

```python
model.eval()
with torch.no_grad():
    output = model(X_test.to(device))
    preds = output.argmax(dim=1)
    accuracy = (preds == y_test.to(device)).float().mean()
```

---

## DataLoader

```python
dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=2)
```

---

## Save & Load

```python
# Save weights (recommended)
torch.save(model.state_dict(), "model.pth")

# Load
model = MyModel(784, 256, 10)
model.load_state_dict(torch.load("model.pth"))
model.eval()
```

---

## Learning Rate Scheduler

```python
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
# In training loop:
scheduler.step()  # after each epoch

# Or cosine annealing (common for Transformers)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
```

---

## Transfer Learning

```python
# Freeze all layers
for param in model.parameters():
    param.requires_grad = False

# Replace and train only final layer
model.fc = nn.Linear(model.fc.in_features, num_classes)
optimizer = optim.Adam(model.fc.parameters(), lr=1e-3)
```

---

## Quick Reference Links

- Official docs: https://pytorch.org/docs/stable/
- Tutorials: https://pytorch.org/tutorials/
- Cheat sheet: https://pytorch.org/tutorials/beginner/ptcheat.html
