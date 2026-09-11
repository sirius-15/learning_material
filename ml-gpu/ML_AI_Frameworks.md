# ML and AI Frameworks -- Comprehensive Reference

> A deep-dive reference covering PyTorch, TensorFlow, JAX, Triton, vLLM, SGLang, and Megatron-LM -- the essential frameworks for modern machine learning, GPU kernel development, and large-scale model training and inference. Each section includes conceptual explanations, comparison tables, code examples, ASCII architecture diagrams, and interview questions with detailed answers. Complements the *Parallel and GPU Programming*, *Python Libraries*, and *Python Fundamentals* guides.

---

## Table of Contents

### Part 1: PyTorch

1. [Tensor Fundamentals](#1-tensor-fundamentals)
2. [Autograd and Computational Graphs](#2-autograd-and-computational-graphs)
3. [Neural Network Modules (torch.nn)](#3-neural-network-modules-torchnn)
4. [Optimizers and Learning Rate Scheduling](#4-optimizers-and-learning-rate-scheduling)
5. [Data Loading and Preprocessing](#5-data-loading-and-preprocessing)
6. [Model Saving, Loading, and Export](#6-model-saving-loading-and-export)
7. [Distributed Training](#7-distributed-training)
8. [Performance Optimization](#8-performance-optimization)
9. [PyTorch Ecosystem and Interview Questions](#9-pytorch-ecosystem-and-interview-questions)

### Part 2: TensorFlow

10. [TensorFlow Architecture and Eager vs Graph Execution](#10-tensorflow-architecture-and-eager-vs-graph-execution)
11. [Tensors and Variables](#11-tensors-and-variables)
12. [Keras API and Model Building](#12-keras-api-and-model-building)
13. [Data Pipelines (tf.data)](#13-data-pipelines-tfdata)
14. [SavedModel, Serving, and Deployment](#14-savedmodel-serving-and-deployment)
15. [Distributed Training in TensorFlow](#15-distributed-training-in-tensorflow)
16. [TensorFlow Performance and XLA](#16-tensorflow-performance-and-xla)
17. [TensorFlow Ecosystem and Interview Questions](#17-tensorflow-ecosystem-and-interview-questions)

### Part 3: JAX

18. [JAX Fundamentals](#18-jax-fundamentals)
19. [Transformations: jit, grad, vmap, pmap](#19-transformations-jit-grad-vmap-pmap)
20. [Sharding and Distributed Computing](#20-sharding-and-distributed-computing)
21. [Advanced JAX](#21-advanced-jax)
22. [Flax and Optax](#22-flax-and-optax)
23. [JAX for HPC and Scientific Computing](#23-jax-for-hpc-and-scientific-computing)
24. [JAX Ecosystem and Interview Questions](#24-jax-ecosystem-and-interview-questions)

### Part 4: Triton

25. [Triton Fundamentals](#25-triton-fundamentals)
26. [Writing Triton Kernels](#26-writing-triton-kernels)
27. [Key Triton Kernels: MatMul, Attention, Softmax](#27-key-triton-kernels-matmul-attention-softmax)
28. [Triton Performance and Debugging](#28-triton-performance-and-debugging)
29. [Triton Ecosystem and Interview Questions](#29-triton-ecosystem-and-interview-questions)

### Part 5: vLLM

30. [vLLM Architecture and PagedAttention](#30-vllm-architecture-and-pagedattention)
31. [Serving and API](#31-serving-and-api)
32. [Scheduling and Batching](#32-scheduling-and-batching)
33. [Quantization and Model Optimization](#33-quantization-and-model-optimization)
34. [vLLM Distributed Inference and Interview Questions](#34-vllm-distributed-inference-and-interview-questions)

### Part 6: SGLang

35. [SGLang Architecture and Runtime](#35-sglang-architecture-and-runtime)
36. [Programming Model](#36-programming-model)
37. [Performance Features](#37-performance-features)
38. [SGLang Deployment and Interview Questions](#38-sglang-deployment-and-interview-questions)

### Part 7: Megatron-LM

39. [Megatron-LM Architecture](#39-megatron-lm-architecture)
40. [Tensor Parallelism](#40-tensor-parallelism)
41. [Pipeline Parallelism](#41-pipeline-parallelism)
42. [Sequence Parallelism and Context Parallelism](#42-sequence-parallelism-and-context-parallelism)
43. [Megatron-LM Training Recipes and Interview Questions](#43-megatron-lm-training-recipes-and-interview-questions)

### Part 8: Cross-Cutting Topics

44. [Comprehensive Comparison Tables](#44-comprehensive-comparison-tables)

---

# Part 1: PyTorch

---

# 1. Tensor Fundamentals

---

## 1.1 What Is PyTorch?

PyTorch is an open-source deep learning framework developed by Meta AI (formerly Facebook AI Research). It provides a Python-first, imperative programming experience built around **tensors** -- multi-dimensional arrays with GPU acceleration and automatic differentiation support. PyTorch's **define-by-run** approach builds computation graphs dynamically, making debugging and prototyping natural.

```
┌─────────────────────────────────────────────────────┐
│                    PyTorch Stack                     │
├─────────────────────────────────────────────────────┤
│  User Code (Python)                                 │
│    ├── torch.Tensor          (multi-dim arrays)     │
│    ├── torch.nn              (neural network layers)│
│    ├── torch.optim           (optimizers)           │
│    └── torch.utils.data      (data loading)         │
├─────────────────────────────────────────────────────┤
│  torch.autograd              (automatic diff)       │
├─────────────────────────────────────────────────────┤
│  ATen / C++ Core             (tensor operations)    │
├─────────────────────────────────────────────────────┤
│  Backends: CPU (MKL) │ CUDA │ ROCm │ MPS │ XPU     │
└─────────────────────────────────────────────────────┘
```

## 1.2 Tensor Creation

| Function | Description | Example |
|---|---|---|
| `torch.tensor(data)` | Create from Python list/tuple (infers dtype) | `torch.tensor([1, 2, 3])` |
| `torch.Tensor(shape)` | Uninitialized tensor of given shape (float32) | `torch.Tensor(2, 3)` |
| `torch.zeros(shape)` | All zeros | `torch.zeros(3, 4)` |
| `torch.ones(shape)` | All ones | `torch.ones(2, 3)` |
| `torch.full(shape, val)` | Fill with value | `torch.full((2, 2), 7.0)` |
| `torch.empty(shape)` | Uninitialized (fast alloc) | `torch.empty(3, 3)` |
| `torch.arange(start, end, step)` | Evenly spaced by step | `torch.arange(0, 10, 2)` |
| `torch.linspace(start, end, steps)` | Evenly spaced by count | `torch.linspace(0, 1, 5)` |
| `torch.eye(n)` | Identity matrix | `torch.eye(3)` |
| `torch.rand(shape)` | Uniform [0, 1) | `torch.rand(2, 3)` |
| `torch.randn(shape)` | Standard normal | `torch.randn(2, 3)` |
| `torch.randint(low, high, shape)` | Random integers | `torch.randint(0, 10, (3,))` |
| `torch.from_numpy(ndarray)` | From NumPy (shares memory) | `torch.from_numpy(np_arr)` |
| `torch.zeros_like(t)` | Zeros matching shape/dtype | `torch.zeros_like(existing)` |

```python
import torch

a = torch.tensor([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])

print(a.shape)    # torch.Size([2, 3])
print(a.dtype)    # torch.float32
print(a.device)   # cpu
```

**`torch.tensor` vs `torch.Tensor`:**

| Aspect | `torch.tensor()` | `torch.Tensor()` |
|---|---|---|
| Input | Data (list, ndarray, scalar) | Shape or data |
| Dtype | Inferred from data | Always `float32` |
| Copy | Always copies data | Aliases the class constructor |
| Recommended | Yes | No (ambiguous semantics) |

## 1.3 Data Types (dtypes)

| dtype | Description | Bits | Alias |
|---|---|---|---|
| `torch.float32` | Single-precision float | 32 | `torch.float` |
| `torch.float64` | Double-precision float | 64 | `torch.double` |
| `torch.float16` | Half-precision float | 16 | `torch.half` |
| `torch.bfloat16` | Brain floating point | 16 | `torch.bfloat16` |
| `torch.int32` | 32-bit integer | 32 | `torch.int` |
| `torch.int64` | 64-bit integer | 64 | `torch.long` |
| `torch.int16` | 16-bit integer | 16 | `torch.short` |
| `torch.int8` | 8-bit signed integer | 8 | -- |
| `torch.uint8` | 8-bit unsigned integer | 8 | -- |
| `torch.bool` | Boolean | 1 | -- |
| `torch.complex64` | Complex (2x float32) | 64 | -- |

```python
x = torch.tensor([1, 2, 3])        # int64 (inferred)
y = x.float()                       # cast to float32
z = x.to(torch.float16)            # explicit cast
w = torch.tensor([1.0], dtype=torch.bfloat16)
```

**bfloat16 vs float16:**

| Property | float16 | bfloat16 |
|---|---|---|
| Exponent bits | 5 | 8 (same as float32) |
| Mantissa bits | 10 | 7 |
| Dynamic range | Narrow (6.5 × 10^4) | Wide (3.4 × 10^38) |
| Precision | Higher | Lower |
| Overflow risk | Higher | Lower |
| Training stability | Needs loss scaling | Rarely needs scaling |
| Hardware | All GPUs since Volta | Ampere+, TPUs |

## 1.4 Device Management

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

x = torch.randn(3, 3, device=device)

y = torch.randn(3, 3)
y = y.to(device)                   # move to GPU
y = y.cuda()                       # equivalent (CUDA only)
y_cpu = y.cpu()                    # back to CPU

print(torch.cuda.device_count())   # number of GPUs
print(torch.cuda.current_device()) # current GPU index
print(torch.cuda.get_device_name(0))

x_gpu0 = x.to('cuda:0')
x_gpu1 = x.to('cuda:1')
```

## 1.5 Memory Layout: Contiguous, Strides, and Views

A tensor's **stride** describes how many elements to skip in memory to advance one position along each dimension. A **contiguous** tensor has elements stored in row-major (C) order.

```python
x = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])
print(x.stride())     # (3, 1) -- skip 3 for next row, 1 for next col
print(x.is_contiguous())  # True

xt = x.t()             # transpose is a VIEW (shared memory)
print(xt.stride())     # (1, 3) -- strides swapped
print(xt.is_contiguous())  # False

xc = xt.contiguous()   # creates a new contiguous copy
```

**Views vs Copies:**

| Operation | Returns | Shares Memory |
|---|---|---|
| `view()` | View (must be contiguous) | Yes |
| `reshape()` | View if possible, copy otherwise | Maybe |
| `t()`, `transpose()` | View | Yes |
| `permute()` | View | Yes |
| `contiguous()` | Copy if not contiguous | No (if copy) |
| `clone()` | Always deep copy | No |
| `narrow()`, `select()` | View | Yes |
| `expand()` | View (broadcast) | Yes |

```python
x = torch.randn(4, 4)
y = x.view(2, 8)       # shared storage -- modifying y modifies x
z = x.clone()           # independent copy
```

## 1.6 Tensor Operations Overview

```python
a = torch.randn(3, 4)
b = torch.randn(3, 4)

c = a + b               # element-wise add
c = torch.add(a, b)     # equivalent
a.add_(b)               # in-place (trailing underscore convention)

m = a @ b.T             # matrix multiply
m = torch.matmul(a, b.T)
m = torch.mm(a, b.T)    # 2D only

e = torch.einsum('ij,kj->ik', a, b)  # Einstein summation

s = a.sum()              # scalar sum
s = a.sum(dim=1)         # sum along dim 1
s = a.mean(dim=0)
s = a.max(dim=1)         # returns (values, indices)

mask = a > 0
filtered = a[mask]       # boolean indexing

cat = torch.cat([a, b], dim=0)   # concatenate along dim 0  (6, 4)
stk = torch.stack([a, b], dim=0) # new dim                  (2, 3, 4)
```

**In-place operations** (suffix `_`) save memory but break autograd graphs. Avoid them on tensors that require gradients.

---

# 2. Autograd and Computational Graphs

---

## 2.1 Dynamic Computation Graphs

PyTorch uses **define-by-run** (eager) execution: the computation graph is built on-the-fly as operations execute, then destroyed after `.backward()`. This contrasts with TensorFlow 1.x's static **define-and-run** approach.

```
Forward pass builds the graph:

  x ──┐
      ├── mul ── z ── sum ── loss
  y ──┘                        │
                               ▼
                          backward()
                               │
                    ┌──────────┴──────────┐
                    ▼                      ▼
               x.grad                 y.grad
```

```python
x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)

z = x * y           # MulBackward0
loss = z.sum()       # SumBackward0

loss.backward()      # compute gradients
print(x.grad)        # tensor(3.)  -- dloss/dx = y
print(y.grad)        # tensor(2.)  -- dloss/dy = x
```

## 2.2 `requires_grad` and Gradient Tracking

| Property / Method | Description |
|---|---|
| `requires_grad=True` | Enable gradient tracking on leaf tensor |
| `.grad` | Stores accumulated gradient after `backward()` |
| `.grad_fn` | Reference to the function that created this tensor |
| `.is_leaf` | `True` if created by user (not by an operation) |
| `.backward()` | Compute gradients via reverse-mode AD |
| `.detach()` | Return a new tensor detached from the graph |
| `.requires_grad_(bool)` | In-place toggle of gradient tracking |

```python
w = torch.randn(3, 3, requires_grad=True)
print(w.is_leaf)       # True  -- created directly by user
print(w.grad_fn)       # None  -- leaf tensors have no grad_fn

y = w @ torch.randn(3, 1)
print(y.is_leaf)       # False -- created by operation
print(y.grad_fn)       # MmBackward0
```

## 2.3 Gradient Accumulation and Zeroing

Gradients **accumulate** by default -- they are summed across multiple `backward()` calls. You must zero them explicitly before each optimization step.

```python
optimizer.zero_grad()         # preferred: zero all param grads
# OR
for p in model.parameters():
    p.grad = None              # more efficient (avoids memset)

loss.backward()
optimizer.step()
```

**Gradient accumulation for large effective batch sizes:**

```python
accumulation_steps = 4
for i, (inputs, targets) in enumerate(dataloader):
    outputs = model(inputs)
    loss = criterion(outputs, targets) / accumulation_steps
    loss.backward()                    # gradients accumulate

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

## 2.4 Controlling Gradient Computation

```python
# Context manager -- no gradients computed (inference mode)
with torch.no_grad():
    output = model(input_tensor)

# Inference mode -- stricter, disallows in-place on result tensors
with torch.inference_mode():
    output = model(input_tensor)

# Selective gradient computation
x = torch.randn(3, requires_grad=True)
y = x.detach()         # y has no gradient connection to x
z = x.data             # same storage, no grad tracking (unsafe)

# Enable gradient for a previously frozen tensor
frozen = torch.randn(3)
frozen.requires_grad_(True)
```

| Context | Tracks Grad | Builds Graph | Speed | Use Case |
|---|---|---|---|---|
| Default | Yes | Yes | Baseline | Training |
| `torch.no_grad()` | No | No | Faster | Validation / inference |
| `torch.inference_mode()` | No | No | Fastest | Pure inference |
| `torch.enable_grad()` | Yes | Yes | Baseline | Override no_grad locally |

## 2.5 Custom Autograd Functions

```python
class MyReLU(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return input.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        input, = ctx.saved_tensors
        grad_input = grad_output.clone()
        grad_input[input < 0] = 0
        return grad_input

x = torch.randn(5, requires_grad=True)
y = MyReLU.apply(x)
y.sum().backward()
print(x.grad)
```

## 2.6 Gradient Clipping

```python
# Clip by norm (most common for RNNs/Transformers)
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# Clip by value
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=0.5)
```

## 2.7 Hooks

Hooks allow inspecting or modifying gradients and activations without changing model code.

```python
# Backward hook on a tensor
def grad_hook(grad):
    print(f"Gradient: {grad}")
    return grad * 2   # optionally modify

x = torch.randn(3, requires_grad=True)
x.register_hook(grad_hook)

# Forward hook on a module
activations = {}
def save_activation(name):
    def hook(module, input, output):
        activations[name] = output.detach()
    return hook

model.layer1.register_forward_hook(save_activation('layer1'))

# Backward hook on a module
def backward_hook(module, grad_input, grad_output):
    print(f"Grad output: {grad_output[0].shape}")

model.layer1.register_full_backward_hook(backward_hook)
```

---

# 3. Neural Network Modules (torch.nn)

---

## 3.1 `nn.Module` Lifecycle

Every neural network component in PyTorch inherits from `nn.Module`. It provides parameter management, device movement, serialization, and hooks.

```python
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.fc1 = nn.Linear(in_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, out_dim)

    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))

model = MLP(784, 256, 10)
print(model)
```

**Key `nn.Module` methods:**

| Method | Description |
|---|---|
| `forward(input)` | Define computation (called via `model(input)`) |
| `parameters()` | Iterator over all learnable parameters |
| `named_parameters()` | Iterator yielding `(name, param)` tuples |
| `children()` | Iterator over immediate child modules |
| `modules()` | Recursive iterator over all modules |
| `train()` / `eval()` | Set training / evaluation mode (affects Dropout, BN) |
| `to(device)` | Move all parameters and buffers to device |
| `state_dict()` | Ordered dict of all parameters and buffers |
| `load_state_dict(d)` | Load parameters from a state dict |
| `register_buffer(name, tensor)` | Non-learnable state (saved with model) |
| `apply(fn)` | Apply function recursively to all modules |
| `zero_grad()` | Zero all parameter gradients |

## 3.2 Parameter Registration

```python
class Custom(nn.Module):
    def __init__(self):
        super().__init__()
        # Automatically registered as parameter
        self.weight = nn.Parameter(torch.randn(10, 5))

        # Buffer: saved in state_dict but NOT optimized
        self.register_buffer('running_mean', torch.zeros(5))

        # Plain tensor: NOT saved, NOT optimized
        self.temp = torch.randn(5)
```

| Registration | In `parameters()` | In `state_dict()` | Moved with `.to()` |
|---|---|---|---|
| `nn.Parameter` | Yes | Yes | Yes |
| `register_buffer` | No | Yes | Yes |
| Plain attribute | No | No | No |

## 3.3 Container Modules

```python
# Sequential -- linear chain of modules
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)

# ModuleList -- indexed access (not auto-forwarded)
class MultiHead(nn.Module):
    def __init__(self, n_heads):
        super().__init__()
        self.heads = nn.ModuleList([nn.Linear(64, 64) for _ in range(n_heads)])

    def forward(self, x):
        return [head(x) for head in self.heads]

# ModuleDict -- named access
class Branches(nn.Module):
    def __init__(self):
        super().__init__()
        self.branches = nn.ModuleDict({
            'text': nn.Linear(768, 256),
            'image': nn.Linear(2048, 256),
        })

    def forward(self, x, modality):
        return self.branches[modality](x)
```

**Critical pitfall:** Using a plain Python `list` or `dict` instead of `ModuleList`/`ModuleDict` means the contained modules will NOT be registered -- their parameters will not appear in `model.parameters()` and will not be saved or moved to GPU.

## 3.4 Common Layers

| Layer | Description | Key Parameters |
|---|---|---|
| `nn.Linear(in, out)` | Fully connected (affine) | `bias=True` |
| `nn.Conv1d/2d/3d` | Convolution | `kernel_size`, `stride`, `padding`, `groups` |
| `nn.ConvTranspose2d` | Transposed convolution | Same + `output_padding` |
| `nn.BatchNorm1d/2d` | Batch normalization | `momentum`, `affine`, `track_running_stats` |
| `nn.LayerNorm` | Layer normalization | `normalized_shape`, `elementwise_affine` |
| `nn.GroupNorm` | Group normalization | `num_groups`, `num_channels` |
| `nn.RMSNorm` | Root mean square norm | `normalized_shape` |
| `nn.Dropout(p)` | Random zeroing (train only) | `p` (drop probability) |
| `nn.Embedding(num, dim)` | Lookup table | `padding_idx`, `max_norm` |
| `nn.MultiheadAttention` | Multi-head attention | `embed_dim`, `num_heads`, `dropout` |
| `nn.TransformerEncoder` | Transformer encoder stack | `num_layers`, `norm` |
| `nn.LSTM` / `nn.GRU` | Recurrent layers | `num_layers`, `bidirectional`, `batch_first` |
| `nn.MaxPool2d` / `nn.AvgPool2d` | Pooling | `kernel_size`, `stride` |
| `nn.AdaptiveAvgPool2d` | Adaptive pooling | `output_size` |

## 3.5 Loss Functions

| Loss | Use Case | Formula Key |
|---|---|---|
| `nn.MSELoss` | Regression | (y - y_hat)^2 |
| `nn.L1Loss` | Regression (robust) | |y - y_hat| |
| `nn.SmoothL1Loss` | Regression (Huber) | Quadratic near 0, linear far |
| `nn.CrossEntropyLoss` | Multi-class classification | -log(softmax(logits)[target]) |
| `nn.NLLLoss` | After log_softmax | -log_probs[target] |
| `nn.BCELoss` | Binary classification (after sigmoid) | -(y log p + (1-y) log(1-p)) |
| `nn.BCEWithLogitsLoss` | Binary classification (raw logits) | Numerically stable BCE |
| `nn.KLDivLoss` | Distribution matching | KL divergence |
| `nn.CosineEmbeddingLoss` | Similarity learning | Cosine distance |
| `nn.TripletMarginLoss` | Metric learning | max(d(a,p) - d(a,n) + margin, 0) |
| `nn.CTCLoss` | Sequence-to-sequence (ASR) | CTC algorithm |

```python
criterion = nn.CrossEntropyLoss(
    weight=class_weights,      # handle class imbalance
    label_smoothing=0.1,       # regularization
    ignore_index=-100          # mask padding tokens
)

logits = model(inputs)          # raw scores, shape (B, C)
loss = criterion(logits, targets)  # targets shape (B,), dtype long
```

## 3.6 Weight Initialization

```python
def init_weights(module):
    if isinstance(module, nn.Linear):
        nn.init.kaiming_normal_(module.weight, nonlinearity='relu')
        if module.bias is not None:
            nn.init.zeros_(module.bias)
    elif isinstance(module, nn.Embedding):
        nn.init.normal_(module.weight, mean=0, std=0.02)

model.apply(init_weights)
```

| Initializer | Formula | Best For |
|---|---|---|
| `xavier_uniform_` | U(-sqrt(6/(fan_in+fan_out)), ...) | Sigmoid, Tanh |
| `xavier_normal_` | N(0, sqrt(2/(fan_in+fan_out))) | Sigmoid, Tanh |
| `kaiming_uniform_` | U(-sqrt(6/fan_in), ...) | ReLU |
| `kaiming_normal_` | N(0, sqrt(2/fan_in)) | ReLU |
| `orthogonal_` | QR decomposition | RNNs |
| `normal_` / `uniform_` | Direct distribution | Embeddings |

---

# 4. Optimizers and Learning Rate Scheduling

---

## 4.1 Optimizers

```python
import torch.optim as optim

optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
```

| Optimizer | Key Idea | When to Use |
|---|---|---|
| `SGD` | Vanilla gradient descent | Baseline, CNNs (with momentum) |
| `SGD(momentum=0.9)` | Momentum-accelerated | CNNs, stable training |
| `Adam` | Adaptive LR per parameter (1st + 2nd moment) | Default choice, fast convergence |
| `AdamW` | Adam with decoupled weight decay | Transformers (preferred over Adam) |
| `Adagrad` | Adaptive LR (accumulates squared grads) | Sparse features (NLP embeddings) |
| `RMSprop` | Adagrad with decay (leaky average) | RNNs |
| `LAMB` | Layer-wise adaptive (via `apex`) | Large-batch training |
| `Adafactor` | Memory-efficient Adam variant | Huge models (T5, PaLM) |

**Adam internals:**

```
m_t = β₁ * m_{t-1} + (1 - β₁) * g_t          # 1st moment (mean)
v_t = β₂ * v_{t-1} + (1 - β₂) * g_t²         # 2nd moment (variance)
m̂_t = m_t / (1 - β₁^t)                        # bias correction
v̂_t = v_t / (1 - β₂^t)                        # bias correction
θ_t = θ_{t-1} - lr * m̂_t / (√v̂_t + ε)        # update
```

**Adam vs AdamW:**

| Aspect | Adam | AdamW |
|---|---|---|
| Weight decay | Added to gradient (L2 regularization) | Decoupled from gradient |
| Effective regularization | Weaker (adaptive LR scales it) | Consistent across parameters |
| Recommended for | Legacy code | New projects, Transformers |

## 4.2 Per-Parameter Options

```python
optimizer = optim.AdamW([
    {'params': model.backbone.parameters(), 'lr': 1e-5},    # lower LR
    {'params': model.head.parameters(),     'lr': 1e-3},    # higher LR
], weight_decay=0.01)
```

## 4.3 Learning Rate Schedulers

```python
from torch.optim.lr_scheduler import (
    StepLR, MultiStepLR, ExponentialLR,
    CosineAnnealingLR, CosineAnnealingWarmRestarts,
    OneCycleLR, LinearLR, SequentialLR
)

scheduler = CosineAnnealingLR(optimizer, T_max=100, eta_min=1e-6)

for epoch in range(num_epochs):
    train(...)
    scheduler.step()       # update LR after each epoch
```

| Scheduler | Behavior | Typical Use |
|---|---|---|
| `StepLR(step_size, gamma)` | Multiply LR by gamma every step_size epochs | Simple decay |
| `MultiStepLR(milestones, gamma)` | Decay at specific epochs | ResNet-style |
| `ExponentialLR(gamma)` | Multiply by gamma every epoch | Smooth decay |
| `CosineAnnealingLR(T_max)` | Cosine curve from initial LR to eta_min | Transformers |
| `OneCycleLR(max_lr, ...)` | Warm up then cosine decay (per step) | Super-convergence |
| `LinearLR(start_factor, end_factor)` | Linear interpolation | Warmup phase |
| `SequentialLR([s1, s2], milestones)` | Chain multiple schedulers | Warmup + decay |

**Warmup + Cosine Decay (common for Transformers):**

```python
warmup = LinearLR(optimizer, start_factor=0.01, total_iters=warmup_steps)
cosine = CosineAnnealingLR(optimizer, T_max=total_steps - warmup_steps)
scheduler = SequentialLR(optimizer, [warmup, cosine], milestones=[warmup_steps])
```

## 4.4 Gradient Accumulation Pattern

```python
optimizer.zero_grad()
for i, (x, y) in enumerate(loader):
    loss = model(x, y) / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
```

---

# 5. Data Loading and Preprocessing

---

## 5.1 Dataset and DataLoader

```
┌────────────────┐     ┌──────────────┐     ┌────────────────┐
│   Dataset      │────▶│   Sampler    │────▶│   DataLoader   │
│  __getitem__   │     │  (indices)   │     │  (batches +    │
│  __len__       │     │              │     │   collation +  │
└────────────────┘     └──────────────┘     │   workers)     │
                                            └────────────────┘
```

```python
from torch.utils.data import Dataset, DataLoader

class ImageDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = load_image(self.image_paths[idx])
        if self.transform:
            image = self.transform(image)
        return image, self.labels[idx]

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,            # random order each epoch
    num_workers=4,           # parallel data loading processes
    pin_memory=True,         # faster CPU-to-GPU transfer
    drop_last=True,          # drop incomplete final batch
    prefetch_factor=2,       # batches prefetched per worker
    persistent_workers=True, # keep workers alive between epochs
)
```

## 5.2 IterableDataset

For streaming data (too large for memory, or from network):

```python
from torch.utils.data import IterableDataset

class StreamDataset(IterableDataset):
    def __init__(self, urls):
        self.urls = urls

    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is not None:
            per_worker = len(self.urls) // worker_info.num_workers
            start = worker_info.id * per_worker
            urls = self.urls[start:start + per_worker]
        else:
            urls = self.urls

        for url in urls:
            for record in stream_from(url):
                yield record
```

## 5.3 Samplers

| Sampler | Description |
|---|---|
| `SequentialSampler` | In-order (default when `shuffle=False`) |
| `RandomSampler` | Random permutation (default when `shuffle=True`) |
| `WeightedRandomSampler` | Weighted sampling (class imbalance) |
| `SubsetRandomSampler` | Random from a subset of indices |
| `DistributedSampler` | Splits data across DDP processes |
| `BatchSampler` | Wraps another sampler to yield batches |

```python
from torch.utils.data import WeightedRandomSampler

class_counts = [1000, 100, 50]
weights = 1.0 / torch.tensor(class_counts, dtype=torch.float)
sample_weights = weights[labels]

sampler = WeightedRandomSampler(sample_weights, num_samples=len(labels))
loader = DataLoader(dataset, batch_size=32, sampler=sampler)
```

## 5.4 Custom Collation

```python
def variable_length_collate(batch):
    texts, labels = zip(*batch)
    lengths = [len(t) for t in texts]
    padded = torch.nn.utils.rnn.pad_sequence(texts, batch_first=True)
    return padded, torch.tensor(labels), torch.tensor(lengths)

loader = DataLoader(dataset, collate_fn=variable_length_collate)
```

## 5.5 Data Augmentation with Transforms

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])
```

---

# 6. Model Saving, Loading, and Export

---

## 6.1 State Dict (Recommended)

```python
# Save
torch.save(model.state_dict(), 'model_weights.pth')

# Load
model = MLP(784, 256, 10)
model.load_state_dict(torch.load('model_weights.pth', weights_only=True))
model.eval()
```

## 6.2 Full Model Save (Not Recommended)

```python
# Uses pickle -- fragile, tied to exact class definition
torch.save(model, 'full_model.pth')
model = torch.load('full_model.pth')
```

## 6.3 Checkpointing (Training Resumption)

```python
# Save checkpoint
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'scheduler_state_dict': scheduler.state_dict(),
    'loss': loss,
    'best_val_acc': best_val_acc,
}
torch.save(checkpoint, f'checkpoint_epoch_{epoch}.pt')

# Resume training
checkpoint = torch.load('checkpoint_epoch_10.pt', weights_only=False)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
start_epoch = checkpoint['epoch'] + 1
```

## 6.4 TorchScript

TorchScript converts Python models to a serializable, optimizable intermediate representation.

```python
# Tracing -- records operations on example input (no control flow)
traced = torch.jit.trace(model, example_input)
traced.save('model_traced.pt')

# Scripting -- parses Python source (supports control flow)
scripted = torch.jit.script(model)
scripted.save('model_scripted.pt')

# Load without Python
loaded = torch.jit.load('model_traced.pt')
output = loaded(input_tensor)
```

| Approach | Control Flow | Dynamic Shapes | Ease |
|---|---|---|---|
| `jit.trace` | Not captured | Limited | Easy |
| `jit.script` | Captured | Supported | Harder (type annotations) |

## 6.5 `torch.compile` (PyTorch 2.x)

```python
model = torch.compile(model, mode='reduce-overhead')
# Modes: 'default', 'reduce-overhead', 'max-autotune'
```

## 6.6 ONNX Export

```python
torch.onnx.export(
    model,
    example_input,
    'model.onnx',
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}},
    opset_version=17,
)
```

## 6.7 `torch.export` (PyTorch 2.x)

```python
from torch.export import export

exported = export(model, (example_input,))
# Produces ExportedProgram with full graph capture (no Python dependency)
```

---

# 7. Distributed Training

---

## 7.1 Why Distributed Training?

| Challenge | Solution |
|---|---|
| Model too large for 1 GPU memory | Model parallelism (tensor, pipeline) |
| Training too slow on 1 GPU | Data parallelism |
| Both | 3D parallelism (data + tensor + pipeline) |

```
Data Parallelism:
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│  GPU 0  │  │  GPU 1  │  │  GPU 2  │  │  GPU 3  │
│ Model   │  │ Model   │  │ Model   │  │ Model   │
│ Copy    │  │ Copy    │  │ Copy    │  │ Copy    │
│ Data 0  │  │ Data 1  │  │ Data 2  │  │ Data 3  │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     └────────────┴────────────┴────────────┘
                    All-Reduce Gradients
```

## 7.2 DataParallel vs DistributedDataParallel

| Feature | `DataParallel` (DP) | `DistributedDataParallel` (DDP) |
|---|---|---|
| Process model | Single process, multi-thread | Multi-process (1 per GPU) |
| Communication | GPU 0 bottleneck (gather/scatter) | All-reduce (NCCL ring) |
| GIL impact | Yes (limits scaling) | No (separate processes) |
| Multi-node | No | Yes |
| Speed | Slower at scale | Near-linear scaling |
| Recommended | Quick prototyping | Production training |

## 7.3 DDP Setup

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def cleanup():
    dist.destroy_process_group()

def train(rank, world_size):
    setup(rank, world_size)

    model = MLP(784, 256, 10).to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    sampler = torch.utils.data.distributed.DistributedSampler(
        dataset, num_replicas=world_size, rank=rank
    )
    loader = DataLoader(dataset, batch_size=32, sampler=sampler)

    optimizer = optim.Adam(ddp_model.parameters(), lr=1e-3)

    for epoch in range(num_epochs):
        sampler.set_epoch(epoch)   # ensure different shuffling each epoch
        for x, y in loader:
            x, y = x.to(rank), y.to(rank)
            loss = criterion(ddp_model(x), y)
            optimizer.zero_grad()
            loss.backward()        # gradients all-reduced automatically
            optimizer.step()

    cleanup()

# Launch with torchrun:
# torchrun --nproc_per_node=4 train.py
```

## 7.4 FSDP (Fully Sharded Data Parallel)

FSDP shards model parameters, gradients, and optimizer states across GPUs, materializing full parameters only for the current layer's forward/backward pass.

```
DDP:  Each GPU holds full model copy + full optimizer state
FSDP: Each GPU holds 1/N of parameters + 1/N of optimizer state

FSDP Memory per GPU (approximate):
  Parameters:      P / N
  Gradients:       P / N
  Optimizer State: O / N    (O = 2P for Adam)
  Peak:            ~3P / N  (vs 16P for DDP with Adam)
```

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy

model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD,  # ZeRO-3
    mixed_precision=MixedPrecision(
        param_dtype=torch.bfloat16,
        reduce_dtype=torch.float32,
        buffer_dtype=torch.bfloat16,
    ),
    auto_wrap_policy=size_based_auto_wrap_policy,
    device_id=torch.cuda.current_device(),
)
```

| Sharding Strategy | Parameters | Gradients | Optimizer | Like |
|---|---|---|---|---|
| `NO_SHARD` | Full | Full | Full | DDP |
| `SHARD_GRAD_OP` | Full | Sharded | Sharded | ZeRO-2 |
| `FULL_SHARD` | Sharded | Sharded | Sharded | ZeRO-3 |
| `HYBRID_SHARD` | Shard within node, replicate across | Mixed | Mixed | ZeRO-3 + DDP |

## 7.5 Communication Backends

| Backend | Transport | Multi-node | GPU-GPU | Best For |
|---|---|---|---|---|
| `nccl` | NVIDIA / RCCL | Yes | Yes (direct) | GPU training (default) |
| `gloo` | TCP / shared mem | Yes | Via CPU | CPU training, fallback |
| `mpi` | MPI library | Yes | Depends | HPC clusters |

## 7.6 `torchrun` Launcher

```bash
# Single node, 4 GPUs
torchrun --nproc_per_node=4 train.py

# Multi-node (2 nodes, 4 GPUs each)
# Node 0:
torchrun --nproc_per_node=4 --nnodes=2 --node_rank=0 \
         --master_addr=10.0.0.1 --master_port=29500 train.py
# Node 1:
torchrun --nproc_per_node=4 --nnodes=2 --node_rank=1 \
         --master_addr=10.0.0.1 --master_port=29500 train.py
```

---

# 8. Performance Optimization

---

## 8.1 `torch.compile` (TorchDynamo + TorchInductor)

`torch.compile` is PyTorch 2.x's flagship optimization. TorchDynamo captures the Python-level graph, and TorchInductor generates optimized Triton kernels or C++ code.

```
Python code
    │
    ▼ TorchDynamo (graph capture via bytecode analysis)
FX Graph
    │
    ▼ TorchInductor (backend compiler)
Optimized code (Triton kernels / C++ / CUDA)
```

```python
model = torch.compile(model, mode='max-autotune')

# Compile modes:
# 'default'          -- balanced compile time and speedup
# 'reduce-overhead'  -- minimize framework overhead (CUDA graphs)
# 'max-autotune'     -- try many kernel configs (slow compile, fast run)
```

## 8.2 Mixed Precision Training

```python
scaler = torch.amp.GradScaler()

for x, y in loader:
    optimizer.zero_grad()
    with torch.amp.autocast(device_type='cuda', dtype=torch.float16):
        output = model(x)
        loss = criterion(output, y)

    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    scaler.step(optimizer)
    scaler.update()
```

**Why loss scaling?** float16 has a narrow dynamic range. Small gradients underflow to zero. The `GradScaler` multiplies loss by a large factor before backward, then divides gradients before the optimizer step.

| Precision | Compute | Memory | Accuracy |
|---|---|---|---|
| FP32 only | Baseline | Baseline | Best |
| FP16 + scaling | ~2x speedup | ~50% reduction | Slight loss possible |
| BF16 | ~2x speedup | ~50% reduction | Nearly same as FP32 |
| FP8 (H100) | ~4x speedup | ~75% reduction | Requires careful tuning |

## 8.3 CUDA Graphs

CUDA Graphs capture a sequence of GPU operations and replay them with minimal CPU overhead, eliminating kernel launch latency.

```python
g = torch.cuda.CUDAGraph()
with torch.cuda.graph(g):
    static_output = model(static_input)

# Replay (no CPU-GPU sync, no kernel launch overhead)
static_input.copy_(real_input)
g.replay()
real_output = static_output.clone()
```

## 8.4 Memory Optimization

```python
# Activation checkpointing (gradient checkpointing)
from torch.utils.checkpoint import checkpoint

class TransformerBlock(nn.Module):
    def forward(self, x):
        return checkpoint(self._forward, x, use_reentrant=False)

    def _forward(self, x):
        x = self.attn(x)
        x = self.ffn(x)
        return x

# Memory snapshots
torch.cuda.memory._record_memory_history()
# ... run code ...
torch.cuda.memory._dump_snapshot("memory_snapshot.pickle")
```

| Technique | Memory Saved | Speed Cost |
|---|---|---|
| Activation checkpointing | ~50-70% activations | ~30% slower (recompute) |
| Gradient accumulation | Proportional to steps | Minimal |
| Mixed precision | ~50% | Often faster |
| `del` + `torch.cuda.empty_cache()` | Frees unused | Minimal |

## 8.5 Profiling

```python
with torch.profiler.profile(
    activities=[
        torch.profiler.ProfilerActivity.CPU,
        torch.profiler.ProfilerActivity.CUDA,
    ],
    schedule=torch.profiler.schedule(wait=1, warmup=1, active=3),
    on_trace_ready=torch.profiler.tensorboard_trace_handler('./log'),
    record_shapes=True,
    profile_memory=True,
    with_stack=True,
) as prof:
    for step, (x, y) in enumerate(loader):
        output = model(x)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        prof.step()

print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
```

---

# 9. PyTorch Ecosystem and Interview Questions

---

## 9.1 Ecosystem

| Library | Purpose |
|---|---|
| **TorchVision** | Image models (ResNet, ViT), datasets (ImageNet, CIFAR), transforms |
| **TorchAudio** | Audio processing, models (Wav2Vec2, HuBERT), datasets |
| **TorchText** | Text processing, vocabularies, datasets |
| **TorchRec** | Recommendation systems (embedding tables, sharding) |
| **TorchServe** | Model serving (REST/gRPC, batching, multi-model) |
| **HuggingFace Transformers** | Pre-trained Transformer models (BERT, GPT, LLaMA) |
| **PyTorch Lightning** | Training boilerplate reduction, logging, distributed |
| **ONNX Runtime** | Cross-platform optimized inference |
| **DeepSpeed** | Large-scale training (ZeRO, pipeline parallelism) |

## 9.2 Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Forgetting `model.eval()` | Dropout/BN active during inference | Call `model.eval()` before inference |
| Not zeroing gradients | Exploding/incorrect gradients | `optimizer.zero_grad()` each step |
| Python list instead of `ModuleList` | Parameters not saved/moved | Use `nn.ModuleList` |
| `torch.Tensor` vs `torch.tensor` | Unexpected dtype | Always use `torch.tensor()` |
| `.data` instead of `.detach()` | Silent autograd bugs | Use `.detach()` |
| In-place ops on grad tensors | Autograd errors | Avoid `_` suffix ops on grad tensors |
| `num_workers > 0` on Windows | Freezing/crash | Use `if __name__ == '__main__':` guard |
| Not calling `sampler.set_epoch()` | Same data order every epoch in DDP | Call before each epoch |

## 9.3 Interview Questions

**Q1: What is the difference between `torch.no_grad()` and `torch.inference_mode()`?**

Both disable gradient computation, but `inference_mode` is stricter and faster. It creates "inference tensors" that cannot be used in future autograd computations, enabling additional memory and speed optimizations. Use `no_grad` when you might need to mix inference results with gradient-tracked operations; use `inference_mode` for pure inference.

**Q2: Explain the difference between `view()` and `reshape()`.**

`view()` requires the tensor to be contiguous and always returns a view (shared memory). `reshape()` returns a view if the tensor is contiguous, otherwise it returns a contiguous copy. When you know the tensor is contiguous, `view()` is preferred because it guarantees no hidden copy.

**Q3: How does DDP achieve near-linear scaling?**

DDP uses a ring all-reduce algorithm to average gradients across GPUs. Each process runs its own forward/backward pass independently. Gradient communication is overlapped with backward computation using "buckets" -- as soon as a bucket of gradients is ready, the all-reduce starts while the rest of backward is still computing. This overlap hides most communication latency.

**Q4: What is FSDP and when would you use it over DDP?**

FSDP (Fully Sharded Data Parallel) shards model parameters, gradients, and optimizer states across GPUs. Unlike DDP where each GPU holds a full model copy, FSDP materializes full parameters only for the active layer. Use FSDP when a model is too large to fit on a single GPU (even in half precision), or when optimizer memory (Adam stores 2x model size) exceeds GPU capacity.

**Q5: How does `torch.compile` work internally?**

`torch.compile` uses TorchDynamo to capture computation graphs by analyzing Python bytecode at runtime. It identifies "graph breaks" (unsupported Python constructs) and compiles safe regions into FX graphs. TorchInductor then lowers these graphs into optimized Triton kernels (GPU) or C++ code (CPU), applying operator fusion, memory planning, and kernel auto-tuning.

**Q6: Why does mixed precision use a GradScaler with float16 but not with bfloat16?**

float16 has only 5 exponent bits, giving it a narrow dynamic range (~6.5e4 max). Small gradients underflow to zero, so loss scaling artificially inflates them into representable range. bfloat16 has 8 exponent bits (same as float32), matching float32's dynamic range (~3.4e38), so underflow is rarely an issue and scaling is unnecessary.

**Q7: What happens if you call `backward()` twice without zeroing gradients?**

Gradients accumulate (are summed). The second backward adds to the existing `.grad` attributes rather than replacing them. This is intentional -- it enables gradient accumulation across mini-batches. But if you forget to zero gradients between optimizer steps, you effectively train on the sum of multiple batches' gradients, leading to incorrect updates and potentially divergent training.

---

# Part 2: TensorFlow

---

# 10. TensorFlow Architecture and Eager vs Graph Execution

---

## 10.1 TensorFlow Overview

TensorFlow is an open-source ML framework developed by Google. TF2 uses eager execution by default (like PyTorch) while retaining the ability to convert functions to optimized static graphs via `tf.function`.

```
┌───────────────────────────────────────────────┐
│                TensorFlow 2.x                 │
├───────────────────────────────────────────────┤
│  Keras API        (High-level model building) │
├───────────────────────────────────────────────┤
│  tf.function      (Graph compilation)         │
│  tf.GradientTape  (Eager differentiation)     │
│  tf.data          (Input pipelines)           │
├───────────────────────────────────────────────┤
│  TF Core          (Ops, tensors, variables)   │
├───────────────────────────────────────────────┤
│  XLA / MLIR       (Optimizing compilers)      │
├───────────────────────────────────────────────┤
│  CPU │ GPU (CUDA) │ TPU │ Edge (TFLite)       │
└───────────────────────────────────────────────┘
```

## 10.2 Eager vs Graph Execution

| Aspect | Eager Execution | Graph Execution (`tf.function`) |
|---|---|---|
| Execution | Immediate (imperative) | Deferred (compile then run) |
| Debugging | Standard Python tools | Harder (tracing semantics) |
| Performance | Baseline | Optimized (op fusion, constant folding) |
| Portability | Python-only | Exportable (SavedModel, TFLite) |
| Default in TF2 | Yes | Via decorator |

```python
import tensorflow as tf

# Eager (default in TF2)
a = tf.constant([1.0, 2.0])
b = tf.constant([3.0, 4.0])
c = a + b
print(c.numpy())    # [4. 6.]  -- immediate result

# Graph mode via tf.function
@tf.function
def add_fn(a, b):
    return a + b

result = add_fn(a, b)   # first call: traces and compiles graph
```

## 10.3 `tf.function` and Tracing

When you decorate a function with `@tf.function`, TensorFlow **traces** the function by executing it with abstract tensor objects. Python code runs only during tracing; the resulting graph is replayed for subsequent calls.

```python
@tf.function
def f(x):
    print("Tracing!")       # runs only during tracing
    tf.print("Executing!")  # runs every call (graph op)
    return x + 1

f(tf.constant(1))   # prints "Tracing!" and "Executing!"
f(tf.constant(2))   # prints only "Executing!" (reuses traced graph)
f(tf.constant(1.0)) # prints "Tracing!" again (new input signature)
```

**Tracing pitfalls:**

| Pitfall | Problem | Solution |
|---|---|---|
| Python `print()` in `tf.function` | Only runs during tracing | Use `tf.print()` |
| Python `if` on tensor value | Traces only one branch | Use `tf.cond()` |
| Python `for` loop | Unrolled during tracing | Use `tf.while_loop()` or fixed-length |
| Python state mutation | Captures value at trace time | Use `tf.Variable` |
| Different input dtypes/shapes | Retraces for each signature | Use `input_signature` |

```python
@tf.function(input_signature=[tf.TensorSpec(shape=[None, 10], dtype=tf.float32)])
def predict(x):
    return model(x)
```

## 10.4 `tf.GradientTape`

```python
x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x ** 2

dy_dx = tape.gradient(y, x)   # 6.0

# Higher-order gradients
with tf.GradientTape() as outer:
    with tf.GradientTape() as inner:
        y = x ** 3
    dy = inner.gradient(y, x)       # 3x^2 = 27.0
d2y = outer.gradient(dy, x)        # 6x = 18.0

# Persistent tape (multiple gradient calls)
with tf.GradientTape(persistent=True) as tape:
    y = x ** 2
    z = x ** 3
dy = tape.gradient(y, x)
dz = tape.gradient(z, x)
del tape
```

## 10.5 AutoGraph

AutoGraph converts Python control flow (if, for, while) into TensorFlow graph operations automatically inside `tf.function`:

```python
@tf.function
def relu(x):
    if x > 0:            # AutoGraph converts to tf.cond
        return x
    else:
        return 0.0

@tf.function
def sum_to_n(n):
    result = tf.constant(0)
    for i in tf.range(n):  # AutoGraph converts to tf.while_loop
        result += i
    return result
```

---

# 11. Tensors and Variables

---

## 11.1 `tf.Tensor` vs `tf.Variable`

| Aspect | `tf.Tensor` | `tf.Variable` |
|---|---|---|
| Mutability | Immutable | Mutable (`.assign()`) |
| Created by | Operations, `tf.constant` | `tf.Variable(initial_value)` |
| Gradients | Watched only if explicitly added | Watched automatically by `GradientTape` |
| Use case | Intermediate computations | Model parameters |
| Identity | Value semantics | Reference semantics |

```python
t = tf.constant([[1, 2], [3, 4]])
print(t.shape)    # (2, 2)
print(t.dtype)    # <dtype: 'int32'>
print(t.numpy())  # array as NumPy

v = tf.Variable([[1.0, 2.0]], name='weights')
v.assign([[3.0, 4.0]])
v.assign_add([[1.0, 1.0]])
```

## 11.2 Data Types

| TF dtype | Description | PyTorch Equivalent |
|---|---|---|
| `tf.float32` | Default float | `torch.float32` |
| `tf.float64` | Double precision | `torch.float64` |
| `tf.float16` | Half precision | `torch.float16` |
| `tf.bfloat16` | Brain float | `torch.bfloat16` |
| `tf.int32` | 32-bit integer | `torch.int32` |
| `tf.int64` | 64-bit integer | `torch.int64` |
| `tf.bool` | Boolean | `torch.bool` |
| `tf.string` | Byte string | No direct equivalent |

## 11.3 Ragged and Sparse Tensors

```python
# Ragged: variable-length sequences (no padding needed)
ragged = tf.ragged.constant([[1, 2, 3], [4, 5], [6]])
print(ragged.shape)   # (3, None)

# Sparse: efficient storage for mostly-zero tensors
sparse = tf.sparse.SparseTensor(
    indices=[[0, 0], [1, 2]],
    values=[1.0, 2.0],
    dense_shape=[3, 4]
)
dense = tf.sparse.to_dense(sparse)
```

## 11.4 Device Placement

```python
with tf.device('/GPU:0'):
    a = tf.Variable(tf.ones([1000, 1000]))

print(a.device)   # /job:localhost/replica:0/task:0/device:GPU:0

# Manual placement
with tf.device('/CPU:0'):
    b = tf.matmul(a, a)    # forces CPU even if GPU available

# Check available devices
print(tf.config.list_physical_devices('GPU'))

# Memory growth (prevent TF from grabbing all GPU memory)
gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
```

---

# 12. Keras API and Model Building

---

## 12.1 Three Ways to Build Models

```
┌─────────────────────────────────────────────────────────────┐
│                    Keras Model APIs                         │
├──────────────┬───────────────────┬──────────────────────────┤
│  Sequential  │    Functional     │     Subclassing          │
│  (simplest)  │  (DAG topology)   │  (maximum flexibility)   │
├──────────────┼───────────────────┼──────────────────────────┤
│ Linear stack │ Multi-input/output│ Dynamic control flow     │
│ of layers    │ Shared layers     │ Custom forward pass      │
│              │ Residual conns    │ Imperative style         │
└──────────────┴───────────────────┴──────────────────────────┘
```

**Sequential:**

```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(10, activation='softmax'),
])
```

**Functional:**

```python
inputs = tf.keras.Input(shape=(784,))
x = tf.keras.layers.Dense(256, activation='relu')(inputs)
x = tf.keras.layers.Dropout(0.3)(x)
outputs = tf.keras.layers.Dense(10, activation='softmax')(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
```

**Subclassing:**

```python
class MyModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(256, activation='relu')
        self.dropout = tf.keras.layers.Dropout(0.3)
        self.dense2 = tf.keras.layers.Dense(10)

    def call(self, inputs, training=False):
        x = self.dense1(inputs)
        x = self.dropout(x, training=training)
        return self.dense2(x)
```

## 12.2 Compile and Fit

```python
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint('best_model.keras'),
        tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=2),
        tf.keras.callbacks.TensorBoard(log_dir='./logs'),
    ],
)
```

## 12.3 Custom Training Loop

```python
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        logits = model(x, training=True)
        loss = loss_fn(y, logits)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss

for epoch in range(num_epochs):
    for x_batch, y_batch in train_dataset:
        loss = train_step(x_batch, y_batch)
```

## 12.4 Custom Layers

```python
class LinearWithConstraint(tf.keras.layers.Layer):
    def __init__(self, units, **kwargs):
        super().__init__(**kwargs)
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer='glorot_uniform',
            trainable=True,
            name='kernel',
        )
        self.b = self.add_weight(
            shape=(self.units,),
            initializer='zeros',
            trainable=True,
            name='bias',
        )

    def call(self, inputs):
        return tf.matmul(inputs, self.w) + self.b

    def get_config(self):
        config = super().get_config()
        config.update({'units': self.units})
        return config
```

---

# 13. Data Pipelines (tf.data)

---

## 13.1 `tf.data.Dataset` Basics

```python
# From tensors
dataset = tf.data.Dataset.from_tensor_slices((features, labels))

# From generator
def gen():
    for i in range(1000):
        yield features[i], labels[i]

dataset = tf.data.Dataset.from_generator(
    gen, output_signature=(
        tf.TensorSpec(shape=(28, 28), dtype=tf.float32),
        tf.TensorSpec(shape=(), dtype=tf.int32),
    )
)

# From TFRecords
dataset = tf.data.TFRecordDataset(filenames)
```

## 13.2 Transformation Pipeline

```python
dataset = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .shuffle(buffer_size=10000)
    .map(preprocess_fn, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

| Method | Description | Performance Impact |
|---|---|---|
| `.shuffle(buffer)` | Randomize order within buffer | CPU-bound (larger buffer = better) |
| `.map(fn, parallel)` | Apply transformation | Parallelize with AUTOTUNE |
| `.batch(size)` | Combine elements into batches | -- |
| `.prefetch(n)` | Overlap data prep with training | Always use AUTOTUNE |
| `.cache()` | Cache dataset in memory/disk | First epoch slow, rest instant |
| `.interleave(fn, n)` | Read from multiple files concurrently | I/O-bound workloads |
| `.repeat(n)` | Repeat dataset n times (None=infinite) | Multi-epoch training |
| `.take(n)` / `.skip(n)` | Select/skip elements | Debugging, train/val split |
| `.filter(pred)` | Keep elements matching predicate | Data selection |

## 13.3 Performance Best Practices

```python
# Optimal pipeline ordering
dataset = (
    tf.data.Dataset.list_files(pattern, shuffle=True)
    .interleave(
        tf.data.TFRecordDataset,
        num_parallel_calls=tf.data.AUTOTUNE,
        cycle_length=16,
    )
    .shuffle(10000)
    .map(parse_fn, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

```
Overlap data loading + preprocessing + training:

  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │  Read    │  │  Map     │  │  Train   │
  │ Batch 1  │  │          │  │          │
  └────┬─────┘  │          │  │          │
       │        │          │  │          │
  ┌────▼─────┐  ┌──────────┐  │          │
  │  Read    │  │  Map     │  │  Train   │
  │ Batch 2  │  │ Batch 1  │  │          │
  └────┬─────┘  └────┬─────┘  │          │
       │              │        │          │
  ┌────▼─────┐  ┌────▼─────┐  ┌──────────┐
  │  Read    │  │  Map     │  │  Train   │
  │ Batch 3  │  │ Batch 2  │  │ Batch 1  │
  └──────────┘  └──────────┘  └──────────┘
       Time ────────────────────────────▶
```

---

# 14. SavedModel, Serving, and Deployment

---

## 14.1 Saving and Loading

```python
# Keras format (recommended for Keras models)
model.save('model.keras')
loaded = tf.keras.models.load_model('model.keras')

# SavedModel format (framework-agnostic)
tf.saved_model.save(model, 'saved_model_dir/')
loaded = tf.saved_model.load('saved_model_dir/')

# Weights only
model.save_weights('weights.h5')
model.load_weights('weights.h5')
```

## 14.2 SavedModel Structure

```
saved_model_dir/
├── saved_model.pb          # Graph definition and metadata
├── fingerprint.pb          # Model fingerprint
├── variables/
│   ├── variables.index     # Variable index
│   └── variables.data-*    # Variable values
└── assets/                 # External files (vocab, etc.)
```

## 14.3 Deployment Targets

| Target | Format | Use Case |
|---|---|---|
| TF Serving | SavedModel | Production server (REST/gRPC) |
| TFLite | `.tflite` (FlatBuffer) | Mobile / embedded / edge |
| TF.js | JSON + binary weights | Browser / Node.js |
| TensorRT | SavedModel + TRT optimization | NVIDIA GPU inference |
| ONNX | `.onnx` | Cross-framework inference |

```python
# TFLite conversion
converter = tf.lite.TFLiteConverter.from_saved_model('saved_model_dir/')
converter.optimizations = [tf.lite.Optimize.DEFAULT]    # dynamic range quant
converter.target_spec.supported_types = [tf.float16]    # fp16 quant
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

---

# 15. Distributed Training in TensorFlow

---

## 15.1 `tf.distribute.Strategy`

```python
# MirroredStrategy: single machine, multiple GPUs
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = create_model()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

model.fit(train_dataset, epochs=10)
```

| Strategy | GPUs | Nodes | Synchronous | Use Case |
|---|---|---|---|---|
| `MirroredStrategy` | Multi | 1 | Yes | Single-node multi-GPU |
| `MultiWorkerMirroredStrategy` | Multi | Multi | Yes | Multi-node GPU training |
| `TPUStrategy` | TPU cores | 1 pod | Yes | TPU training |
| `ParameterServerStrategy` | Multi | Multi | Async | Large-scale async training |
| `CentralStorageStrategy` | Multi | 1 | Yes | Asymmetric GPU setup |

## 15.2 Custom Training with Strategy

```python
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = create_model()
    optimizer = tf.keras.optimizers.Adam(1e-3)
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(
        reduction=tf.keras.losses.Reduction.NONE
    )

@tf.function
def distributed_train_step(inputs):
    def step_fn(batch):
        x, y = batch
        with tf.GradientTape() as tape:
            logits = model(x, training=True)
            per_example_loss = loss_fn(y, logits)
            loss = tf.nn.compute_average_loss(per_example_loss)
        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))
        return loss

    per_replica_losses = strategy.run(step_fn, args=(inputs,))
    return strategy.reduce(tf.distribute.ReduceOp.SUM,
                          per_replica_losses, axis=None)
```

---

# 16. TensorFlow Performance and XLA

---

## 16.1 XLA (Accelerated Linear Algebra)

XLA compiles TensorFlow graphs into optimized machine code for the target hardware (CPU, GPU, TPU). It performs:

- **Operator fusion** -- combine multiple ops into one kernel
- **Buffer analysis** -- eliminate intermediate allocations
- **Layout optimization** -- choose optimal tensor layouts per hardware
- **Constant folding** -- precompute static expressions

```python
# Enable XLA for tf.function
@tf.function(jit_compile=True)
def fast_matmul(a, b):
    return tf.matmul(a, b)

# Enable XLA globally
tf.config.optimizer.set_jit(True)
```

## 16.2 Mixed Precision

```python
tf.keras.mixed_precision.set_global_policy('mixed_float16')

model = create_model()
# Dense layers compute in float16, accumulate in float32
# Loss scale applied automatically

# Custom: ensure output is float32 for numerical stability
outputs = tf.keras.layers.Dense(10, dtype='float32')(x)
```

## 16.3 Profiling with TensorBoard

```python
tf.profiler.experimental.start('logdir/')
# ... training steps ...
tf.profiler.experimental.stop()

# Or with callbacks
model.fit(
    data,
    callbacks=[tf.keras.callbacks.TensorBoard(
        log_dir='./logs', profile_batch='10,20'
    )]
)
```

---

# 17. TensorFlow Ecosystem and Interview Questions

---

## 17.1 Ecosystem

| Component | Purpose |
|---|---|
| **TensorBoard** | Visualization (scalars, graphs, histograms, profiling) |
| **TFX** | End-to-end ML pipeline (data validation, training, serving) |
| **TF Hub** | Pre-trained model repository |
| **TF Datasets (TFDS)** | Ready-to-use datasets with `tf.data` integration |
| **TF Lite** | On-device inference (mobile, embedded, IoT) |
| **TF.js** | ML in the browser |
| **TF Probability** | Probabilistic modeling and Bayesian inference |
| **TF Agents** | Reinforcement learning |
| **TF Text** | Text preprocessing ops (tokenizers, n-grams) |
| **TF Recommenders** | Recommendation system models |
| **Model Garden** | Official model implementations (EfficientNet, BERT) |

## 17.2 PyTorch vs TensorFlow

| Aspect | PyTorch | TensorFlow |
|---|---|---|
| Execution model | Eager (dynamic graph) | Eager + `tf.function` (graph) |
| Debugging | Python debugger | `tf.function` complicates debugging |
| Research adoption | Dominant (>80% papers) | Declining in research |
| Production | Growing (TorchServe) | Mature (TF Serving, TFX) |
| Mobile/Edge | TorchMobile (newer) | TFLite (mature) |
| TPU support | Limited (via XLA bridge) | Native |
| Model export | TorchScript, ONNX, torch.export | SavedModel, TFLite, TF.js |
| Compilation | `torch.compile` (2.x) | XLA, `tf.function` |
| Distributed | DDP, FSDP | `tf.distribute` strategies |
| Community | Larger research community | Larger production community |

## 17.3 Interview Questions

**Q1: What is the difference between eager execution and graph execution in TensorFlow?**

Eager execution runs operations immediately as they are called (like PyTorch), returning concrete values. Graph execution (`tf.function`) traces the function once to build a static computation graph, then replays the optimized graph on subsequent calls. Graph mode enables XLA compilation, operator fusion, and deployment to non-Python environments. The trade-off is that graph mode has tracing semantics -- Python side effects only run during tracing, not during execution.

**Q2: What are the pitfalls of `tf.function`?**

The main pitfalls stem from the tracing model: (1) Python side effects (print, list append, file I/O) only execute during tracing, not on subsequent calls. (2) Python `if` statements on tensor values get traced for only one branch. (3) Creating `tf.Variable` inside a `tf.function` causes errors on the second call. (4) Functions are retraced for different input signatures, causing performance issues if called with many different shapes/dtypes. Use `input_signature` to fix the trace.

**Q3: When would you choose TensorFlow over PyTorch?**

TensorFlow excels in production deployment (TF Serving, TFX pipelines), mobile/edge deployment (TFLite has years of maturity), TPU training (native support), and end-to-end ML pipelines (data validation to model monitoring). PyTorch is preferred for research prototyping, when you need maximum flexibility, or when using models from the HuggingFace ecosystem.

**Q4: How does `tf.data` achieve high throughput?**

`tf.data` pipelines use three key strategies: (1) **Prefetching** (`.prefetch()`) overlaps data preprocessing with model training. (2) **Parallelism** (`.map(fn, num_parallel_calls=AUTOTUNE)`) processes multiple elements concurrently. (3) **Interleaving** (`.interleave()`) reads from multiple files simultaneously. Additionally, `.cache()` stores processed data in memory or on disk for subsequent epochs, and AUTOTUNE dynamically tunes the degree of parallelism at runtime.

---

# Part 3: JAX

---

# 18. JAX Fundamentals

---

## 18.1 What Is JAX?

JAX is Google's library for high-performance numerical computing with composable function transformations. It provides a NumPy-compatible API that runs on CPU, GPU, and TPU, combined with four key transformations: `jit` (compilation), `grad` (differentiation), `vmap` (vectorization), and `pmap` (parallelization).

JAX follows a **functional programming** paradigm: functions must be pure (no side effects), arrays are immutable, and random state is explicit.

```
┌───────────────────────────────────────┐
│               JAX                     │
├───────────────────────────────────────┤
│  jax.numpy   (NumPy-compatible API)  │
│  jax.random  (Explicit PRNG keys)    │
│  jax.lax     (Low-level primitives)  │
├───────────────────────────────────────┤
│  Transformations:                     │
│    jit   (JIT compilation via XLA)   │
│    grad  (Automatic differentiation) │
│    vmap  (Auto vectorization)        │
│    pmap  (Multi-device parallelism)  │
├───────────────────────────────────────┤
│  XLA Compiler                        │
├───────────────────────────────────────┤
│  CPU │ GPU (CUDA/ROCm) │ TPU         │
└───────────────────────────────────────┘
```

## 18.2 JAX Arrays and `jax.numpy`

```python
import jax
import jax.numpy as jnp

x = jnp.array([1.0, 2.0, 3.0])
y = jnp.ones((3, 3))
z = jnp.dot(x, y)

# JAX arrays are immutable
# x[0] = 10  # ERROR: JAX arrays do not support item assignment
x = x.at[0].set(10)       # returns a NEW array
x = x.at[1].add(5)        # functional update
```

**Key differences from NumPy:**

| Aspect | NumPy | JAX |
|---|---|---|
| Mutability | In-place operations allowed | Immutable (use `.at[].set()`) |
| Random numbers | Global state (`np.random.seed`) | Explicit keys (`jax.random.key`) |
| Side effects | Allowed | Functions must be pure (for `jit`) |
| Out-of-bounds indexing | Error | Clamps to valid range (no error) |
| Default float | `float64` | `float32` |
| Device | CPU only | CPU, GPU, TPU |

## 18.3 Random Number Handling

JAX requires explicit PRNG (pseudo-random number generator) state to ensure reproducibility and compatibility with `jit`:

```python
key = jax.random.key(42)

# Split key for each use (never reuse a key)
key, subkey = jax.random.split(key)
x = jax.random.normal(subkey, shape=(3, 3))

key, subkey = jax.random.split(key)
y = jax.random.uniform(subkey, shape=(3,))

# Split into multiple keys at once
keys = jax.random.split(key, num=10)
samples = jax.vmap(lambda k: jax.random.normal(k, (5,)))(keys)
```

## 18.4 PyTrees

A PyTree is a container of leaf elements and/or other containers. JAX transformations operate on PyTrees automatically, enabling natural handling of nested structures (dicts, lists, tuples, dataclasses).

```python
params = {
    'linear1': {'w': jnp.ones((3, 4)), 'b': jnp.zeros(4)},
    'linear2': {'w': jnp.ones((4, 2)), 'b': jnp.zeros(2)},
}

# jax.tree.map applies a function to every leaf
doubled = jax.tree.map(lambda x: x * 2, params)

# Leaves count
num_params = sum(x.size for x in jax.tree.leaves(params))
```

---

# 19. Transformations: jit, grad, vmap, pmap

---

## 19.1 `jax.jit` -- JIT Compilation

`jit` compiles a function using XLA, optimizing for the target hardware:

```python
def slow_fn(x):
    return jnp.dot(x, x.T) + jnp.sin(x).sum()

fast_fn = jax.jit(slow_fn)

# Or as a decorator
@jax.jit
def fast_fn(x):
    return jnp.dot(x, x.T) + jnp.sin(x).sum()

x = jnp.ones((1000, 1000))
result = fast_fn(x)  # first call compiles; subsequent calls reuse compiled code
```

**Static arguments:** Values that affect the computation graph structure (not just values) must be marked static:

```python
@functools.partial(jax.jit, static_argnums=(1,))
def f(x, mode):
    if mode == 'train':
        return x + 1
    return x

# Or with static_argnames
@functools.partial(jax.jit, static_argnames=('mode',))
def f(x, mode='train'):
    ...
```

## 19.2 `jax.grad` -- Automatic Differentiation

```python
def loss_fn(w, x, y):
    pred = jnp.dot(x, w)
    return jnp.mean((pred - y) ** 2)

grad_fn = jax.grad(loss_fn)         # gradient w.r.t. first argument (w)
grads = grad_fn(w, x, y)

# Gradient w.r.t. multiple arguments
grad_fn = jax.grad(loss_fn, argnums=(0, 1))  # w.r.t. w and x
dw, dx = grad_fn(w, x, y)

# Value and gradient together
loss, grads = jax.value_and_grad(loss_fn)(w, x, y)

# Jacobian (full matrix of partial derivatives)
jacobian = jax.jacobian(f)(x)

# Hessian (second-order derivatives)
hessian = jax.hessian(loss_fn)(w, x, y)
```

**Forward-mode vs Reverse-mode:**

| Mode | Function | Best For | Complexity |
|---|---|---|---|
| Reverse (`jax.grad`) | `jax.grad`, `jax.vjp` | Scalar output, many inputs (loss functions) | O(1) backward passes |
| Forward (`jax.jvp`) | `jax.jvp` | Many outputs, few inputs (Jacobian columns) | O(n) forward passes |

## 19.3 `jax.vmap` -- Auto-Vectorization

`vmap` transforms a function that operates on single examples into one that operates on batches, without writing explicit batch dimensions:

```python
def predict_single(params, x):
    return jnp.dot(x, params['w']) + params['b']

# Vectorize over the batch dimension of x (not params)
predict_batch = jax.vmap(predict_single, in_axes=(None, 0))

# in_axes=(None, 0) means:
#   params: not batched (shared across batch)
#   x:      batched along axis 0

batch_output = predict_batch(params, x_batch)
```

**Composability -- the power of JAX:**

```python
# Per-example gradients (impossible in PyTorch without loops)
per_example_grads = jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0))
grads = per_example_grads(params, x_batch, y_batch)
```

## 19.4 `jax.pmap` -- Multi-Device Parallelism

```python
@jax.pmap
def train_step(params, x, y):
    loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
    grads = jax.lax.pmean(grads, axis_name='batch')
    return params - lr * grads, loss

# Replicate params across devices
params = jax.device_put_replicated(params, jax.devices())

# Shard data across devices
x_sharded = jnp.reshape(x, (num_devices, -1, *x.shape[1:]))
```

## 19.5 Composability Summary

All four transformations can be arbitrarily composed:

```
jit(grad(vmap(f)))        -- JIT-compiled, batched gradient
vmap(jit(grad(f)))        -- batched JIT-compiled gradient
grad(jit(vmap(f)))        -- gradient of JIT-compiled batched function
pmap(grad(f))             -- parallelized gradient computation
jit(vmap(grad(f)))        -- JIT, per-example gradients
```

---

# 20. Sharding and Distributed Computing

---

## 20.1 Device Mesh and Sharding

```python
from jax.sharding import Mesh, NamedSharding, PartitionSpec as P

devices = jax.devices()  # e.g., 8 GPUs
mesh = Mesh(devices.reshape(2, 4), axis_names=('data', 'model'))

# PartitionSpec maps tensor dimensions to mesh axes
# P('data', 'model') -- shard dim 0 across 'data', dim 1 across 'model'
# P('data', None)    -- shard dim 0 across 'data', replicate dim 1

sharding = NamedSharding(mesh, P('data', None))
x = jax.device_put(x, sharding)  # distribute tensor according to sharding
```

```
Mesh(2, 4) with axis_names=('data', 'model'):

              model axis (4 devices)
            ┌──────┬──────┬──────┬──────┐
  data      │GPU 0 │GPU 1 │GPU 2 │GPU 3 │   data shard 0
  axis      ├──────┼──────┼──────┼──────┤
  (2)       │GPU 4 │GPU 5 │GPU 6 │GPU 7 │   data shard 1
            └──────┴──────┴──────┴──────┘
```

## 20.2 SPMD with `jax.jit` and Sharding

```python
@jax.jit
def matmul_sharded(x, w):
    return x @ w

# Constrain output sharding
@jax.jit
def f(x):
    y = x @ w
    return jax.lax.with_sharding_constraint(y, NamedSharding(mesh, P('data', None)))
```

## 20.3 Collective Operations

| Operation | Description |
|---|---|
| `jax.lax.psum` | Sum across devices |
| `jax.lax.pmean` | Mean across devices |
| `jax.lax.pmax` / `pmin` | Max / min across devices |
| `jax.lax.all_gather` | Gather full tensor on each device |
| `jax.lax.ppermute` | Permute data between devices |
| `jax.lax.all_to_all` | Transpose sharding dimensions |

---

# 21. Advanced JAX

---

## 21.1 Custom Derivatives

```python
@jax.custom_jvp
def safe_log(x):
    return jnp.log(x)

@safe_log.defjvp
def safe_log_jvp(primals, tangents):
    x, = primals
    t, = tangents
    return safe_log(x), t / jnp.maximum(x, 1e-8)  # avoid division by zero

@jax.custom_vjp
def clip_gradient(x):
    return x

def clip_fwd(x):
    return x, x  # (output, residuals)

def clip_bwd(res, g):
    return (jnp.clip(g, -1.0, 1.0),)

clip_gradient.defvjp(clip_fwd, clip_bwd)
```

## 21.2 Control Flow Primitives

Inside `jit`-compiled functions, standard Python control flow depending on traced values must use JAX primitives:

```python
# Conditional
result = jax.lax.cond(pred, true_fn, false_fn, operand)

# While loop
def body_fn(val):
    return val + 1

result = jax.lax.while_loop(lambda val: val < 10, body_fn, init_val=0)

# For loop (scan)
def step(carry, x):
    carry = carry + x
    return carry, carry  # (new_carry, output)

final_carry, outputs = jax.lax.scan(step, init=0.0, xs=jnp.arange(10.0))

# Fori loop (simple iteration)
result = jax.lax.fori_loop(0, 10, lambda i, val: val + i, init_val=0)
```

`jax.lax.scan` is particularly important -- it replaces Python for-loops over sequence dimensions (e.g., RNN unrolling) and enables efficient gradient computation through the loop.

## 21.3 Gradient Checkpointing

```python
from jax.checkpoint import checkpoint  # alias: jax.remat

@checkpoint
def transformer_block(params, x):
    x = attention(params['attn'], x)
    x = ffn(params['ffn'], x)
    return x
```

## 21.4 Debugging

```python
# Print during traced computation
jax.debug.print("x = {x}", x=x)

# Breakpoint during traced computation
jax.debug.breakpoint()

# Disable JIT for debugging
with jax.disable_jit():
    result = f(x)

# Check for NaN
jax.config.update("jax_debug_nans", True)
```

---

# 22. Flax and Optax

---

## 22.1 Flax `nn.Module`

Flax is the primary neural network library for JAX. It follows JAX's functional paradigm -- modules are stateless, and parameters are managed externally.

```python
import flax.linen as nn

class MLP(nn.Module):
    hidden_dim: int
    out_dim: int

    @nn.compact
    def __call__(self, x, training: bool = False):
        x = nn.Dense(self.hidden_dim)(x)
        x = nn.relu(x)
        x = nn.Dropout(rate=0.1, deterministic=not training)(x)
        x = nn.Dense(self.out_dim)(x)
        return x

model = MLP(hidden_dim=256, out_dim=10)
params = model.init(jax.random.key(0), jnp.ones((1, 784)))
output = model.apply(params, x)
```

**Flax vs PyTorch `nn.Module`:**

| Aspect | Flax | PyTorch |
|---|---|---|
| Paradigm | Functional (stateless modules) | Object-oriented (stateful) |
| Parameters | External dict (PyTree) | Internal (`self.weight`) |
| Forward pass | `model.apply(params, x)` | `model(x)` |
| Initialization | `model.init(key, example)` | In `__init__()` |
| Mutability | Immutable params | Mutable parameters |
| Randomness | Explicit PRNG keys | Global state |

## 22.2 Flax Training State

```python
from flax.training import train_state

class TrainState(train_state.TrainState):
    batch_stats: dict  # for BatchNorm

state = TrainState.create(
    apply_fn=model.apply,
    params=params['params'],
    batch_stats=params.get('batch_stats', {}),
    tx=optax.adamw(learning_rate=1e-3, weight_decay=0.01),
)
```

## 22.3 Optax Optimizers

Optax is JAX's optimizer library, built on composable gradient transformations:

```python
import optax

# Simple optimizer
optimizer = optax.adam(learning_rate=1e-3)

# Composed optimizer: warmup + cosine decay + gradient clipping + weight decay
schedule = optax.warmup_cosine_decay_schedule(
    init_value=0.0, peak_value=1e-3,
    warmup_steps=1000, decay_steps=100000,
)

optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adamw(learning_rate=schedule, weight_decay=0.01),
)

opt_state = optimizer.init(params)
updates, opt_state = optimizer.update(grads, opt_state, params)
params = optax.apply_updates(params, updates)
```

| Optax Function | Description |
|---|---|
| `optax.sgd` | SGD with optional momentum |
| `optax.adam` | Adam optimizer |
| `optax.adamw` | AdamW (decoupled weight decay) |
| `optax.chain` | Compose multiple transformations |
| `optax.clip_by_global_norm` | Gradient clipping |
| `optax.scale_by_schedule` | Learning rate scheduling |
| `optax.warmup_cosine_decay_schedule` | Warmup + cosine decay |

## 22.4 Complete Training Loop

```python
@jax.jit
def train_step(state, batch):
    def loss_fn(params):
        logits = state.apply_fn({'params': params}, batch['image'], training=True,
                                rngs={'dropout': jax.random.key(state.step)})
        loss = optax.softmax_cross_entropy_with_integer_labels(
            logits, batch['label']
        ).mean()
        return loss, logits

    grad_fn = jax.value_and_grad(loss_fn, has_aux=True)
    (loss, logits), grads = grad_fn(state.params)
    state = state.apply_gradients(grads=grads)
    return state, loss

for epoch in range(num_epochs):
    for batch in train_loader:
        state, loss = train_step(state, batch)
```

---

# 23. JAX for HPC and Scientific Computing

---

## 23.1 Why JAX for HPC?

| Feature | Benefit for HPC |
|---|---|
| XLA compilation | Hardware-optimized kernels without manual tuning |
| `vmap` | Vectorize simulations over parameter sweeps |
| `grad` | Automatic derivatives for PDE solvers, optimization |
| `pmap` / sharding | Multi-GPU/TPU parallelism without MPI |
| NumPy API | Familiar interface for scientists |
| Functional purity | Reproducible, composable simulations |

## 23.2 FFT and Linear Algebra

```python
# FFT
spectrum = jnp.fft.fft2(image)
filtered = jnp.fft.ifft2(spectrum * kernel_freq)

# Linear algebra
eigenvalues, eigenvectors = jnp.linalg.eigh(symmetric_matrix)
solution = jnp.linalg.solve(A, b)
U, S, Vt = jnp.linalg.svd(matrix)
```

## 23.3 Differentiable Simulation

```python
from jax.experimental.ode import odeint

def dynamics(state, t, params):
    x, v = state
    a = -params['k'] * x - params['damping'] * v
    return jnp.array([v, a])

# Forward solve
trajectory = odeint(dynamics, initial_state, t_span, params)

# Gradient through the ODE solver
grad_params = jax.grad(lambda p: odeint(dynamics, initial_state, t_span, p)[-1].sum())(params)
```

---

# 24. JAX Ecosystem and Interview Questions

---

## 24.1 Ecosystem

| Library | Purpose |
|---|---|
| **Flax** | Neural network modules (primary NN library) |
| **Optax** | Gradient processing and optimization |
| **Orbax** | Checkpointing and persistence |
| **MaxText** | Reference LLM training codebase |
| **Pax** | Large-scale model training (internal Google) |
| **Equinox** | PyTorch-like neural networks for JAX |
| **Diffrax** | Differential equation solvers |
| **jraph** | Graph neural networks |
| **RLax** | Reinforcement learning |

## 24.2 Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Reusing PRNG keys | Same random values | Always `split` before use |
| In-place mutation | Error | Use `.at[].set()` |
| Python control flow in `jit` | Retraces on value change | Use `jax.lax.cond`, `scan` |
| Data-dependent shapes | Trace error | Use padding / fixed shapes |
| Global state | Silent bugs under `jit` | Pass state as arguments |
| `float64` not enabled | Unexpected precision | `jax.config.update("jax_enable_x64", True)` |

## 24.3 Interview Questions

**Q1: What makes JAX different from PyTorch?**

JAX follows a functional programming paradigm where arrays are immutable and functions must be pure (no side effects). This enables composable transformations: you can arbitrarily nest `jit`, `grad`, `vmap`, and `pmap`. PyTorch is object-oriented with mutable tensors and stateful modules. JAX compiles entire computations via XLA, while PyTorch 2.x uses TorchDynamo/Inductor. JAX treats randomness explicitly (PRNG keys must be threaded), while PyTorch uses global state.

**Q2: Explain `vmap` and why it matters.**

`vmap` (vectorizing map) transforms a function that operates on single examples into one that operates on batches by automatically adding a batch dimension. This avoids manually writing batched code and enables operations like per-example gradients (`vmap(grad(loss_fn))`) that are impossible in standard PyTorch without explicit loops. Under the hood, `vmap` doesn't loop -- it transforms the function's operations to use batched primitives, achieving the same performance as hand-written batched code.

**Q3: Why does JAX require explicit PRNG keys?**

JAX functions compiled with `jit` must be pure -- their output must depend only on their inputs. A global random state would be a hidden side effect that changes between calls, breaking this requirement. Explicit PRNG keys make randomness a function argument, ensuring reproducibility and compatibility with all transformations. Keys are split (not reused) using `jax.random.split()` to generate independent random streams.

**Q4: What is `jax.lax.scan` and when would you use it?**

`scan` is JAX's primitive for sequential computation (replacing Python for-loops). It takes a function `f(carry, x) -> (carry, output)` and applies it sequentially over a sequence. Unlike unrolling a Python loop (which creates a huge computation graph), `scan` produces a compact graph that's efficient to compile and differentiate. Use it for RNN unrolling, sequential processing, cumulative operations, or any loop where each iteration depends on the previous result.

---

# Part 4: Triton

---

# 25. Triton Fundamentals

---

## 25.1 What Is Triton?

Triton (OpenAI Triton) is a programming language and compiler for writing highly efficient GPU kernels in Python. It operates at a **block level** rather than CUDA's thread level, automatically handling memory coalescing, shared memory management, thread scheduling, and synchronization.

```
Abstraction Levels:

  CUDA:     Individual threads → warps → blocks
  Triton:   Blocks of data (tiles)  → programs

  ┌─────────────────────────────────────────────┐
  │  Python User Code                           │
  │    triton.jit kernel ──┐                    │
  ├────────────────────────┼────────────────────┤
  │  Triton Compiler       ▼                    │
  │    Triton IR → TTIR → TTGIR → LLVM IR      │
  ├─────────────────────────────────────────────┤
  │  GPU Binary (PTX/AMDGPU)                    │
  └─────────────────────────────────────────────┘
```

## 25.2 Triton vs CUDA

| Aspect | CUDA | Triton |
|---|---|---|
| Language | C/C++ extensions | Python (decorated functions) |
| Abstraction | Thread-level | Block/tile-level |
| Shared memory | Manual (explicit `__shared__`) | Automatic |
| Memory coalescing | Manual | Automatic |
| Synchronization | Manual (`__syncthreads()`) | Automatic |
| Occupancy tuning | Manual | Auto-tuning support |
| Development speed | Slow (low-level) | Fast (high-level) |
| Peak performance | Highest (hand-tuned) | 90-100% of CUDA (for typical kernels) |
| AMD support | No (CUDA = NVIDIA only) | Yes (via ROCm backend) |
| Learning curve | Steep | Moderate |

## 25.3 First Triton Kernel: Vector Addition

```python
import triton
import triton.language as tl

@triton.jit
def add_kernel(
    x_ptr, y_ptr, output_ptr,
    n_elements,
    BLOCK_SIZE: tl.constexpr,
):
    pid = tl.program_id(axis=0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)

    mask = offsets < n_elements

    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.load(y_ptr + offsets, mask=mask)
    output = x + y
    tl.store(output_ptr + offsets, output, mask=mask)

def add(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    output = torch.empty_like(x)
    n = output.numel()
    grid = lambda meta: (triton.cdiv(n, meta['BLOCK_SIZE']),)
    add_kernel[grid](x, y, output, n, BLOCK_SIZE=1024)
    return output
```

**Key concepts:**

| Concept | Description |
|---|---|
| `@triton.jit` | Decorator marking a GPU kernel function |
| `tl.program_id(axis)` | Equivalent to CUDA blockIdx (which program instance) |
| `tl.arange(start, end)` | Vector of consecutive integers (like thread indices within a block) |
| `tl.constexpr` | Compile-time constant (used for block sizes) |
| `tl.load(ptr, mask)` | Load data from global memory (with boundary mask) |
| `tl.store(ptr, val, mask)` | Store data to global memory (with boundary mask) |
| `mask` | Boolean vector preventing out-of-bounds access |
| Grid | Lambda returning the number of program instances to launch |

## 25.4 Compilation Pipeline

```
Python (@triton.jit)
    │
    ▼  Parse and lower
Triton IR (MLIR dialect)
    │
    ▼  Optimizations (tiling, fusion)
TTIR (Triton Target IR)
    │
    ▼  Target-specific lowering
TTGIR (Triton Target GPU IR)
    │
    ▼  Convert to LLVM
LLVM IR
    │
    ▼  Target codegen
PTX (NVIDIA) or AMDGPU ISA (AMD)
    │
    ▼  Assemble
GPU Binary (cubin / hsaco)
```

---

# 26. Writing Triton Kernels

---

## 26.1 Pointer Arithmetic and Memory Access

Triton uses explicit pointer arithmetic rather than array indexing:

```python
@triton.jit
def row_sum_kernel(
    input_ptr, output_ptr,
    n_cols,
    input_row_stride,
    BLOCK_SIZE: tl.constexpr,
):
    row_idx = tl.program_id(0)
    col_offsets = tl.arange(0, BLOCK_SIZE)
    mask = col_offsets < n_cols

    row_start = input_ptr + row_idx * input_row_stride
    row = tl.load(row_start + col_offsets, mask=mask, other=0.0)
    result = tl.sum(row, axis=0)
    tl.store(output_ptr + row_idx, result)
```

## 26.2 2D Tiled Kernel Pattern

```python
@triton.jit
def elementwise_2d_kernel(
    x_ptr, output_ptr,
    M, N,
    stride_m, stride_n,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)

    offs_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)

    mask = (offs_m[:, None] < M) & (offs_n[None, :] < N)

    ptrs = x_ptr + offs_m[:, None] * stride_m + offs_n[None, :] * stride_n
    x = tl.load(ptrs, mask=mask)
    tl.store(output_ptr + offs_m[:, None] * stride_m + offs_n[None, :] * stride_n,
             x * 2, mask=mask)
```

## 26.3 Reduction Kernels

```python
@triton.jit
def softmax_kernel(
    input_ptr, output_ptr,
    n_cols,
    input_row_stride, output_row_stride,
    BLOCK_SIZE: tl.constexpr,
):
    row_idx = tl.program_id(0)

    row_start = input_ptr + row_idx * input_row_stride
    col_offsets = tl.arange(0, BLOCK_SIZE)
    mask = col_offsets < n_cols

    row = tl.load(row_start + col_offsets, mask=mask, other=-float('inf'))

    row_max = tl.max(row, axis=0)
    numerator = tl.exp(row - row_max)
    denominator = tl.sum(numerator, axis=0)
    softmax_output = numerator / denominator

    out_start = output_ptr + row_idx * output_row_stride
    tl.store(out_start + col_offsets, softmax_output, mask=mask)
```

## 26.4 Atomic Operations

```python
@triton.jit
def histogram_kernel(input_ptr, hist_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements

    values = tl.load(input_ptr + offsets, mask=mask)
    bins = values.to(tl.int32)
    tl.atomic_add(hist_ptr + bins, 1, mask=mask)
```

---

# 27. Key Triton Kernels: MatMul, Attention, Softmax

---

## 27.1 Tiled Matrix Multiplication

Matrix multiplication is decomposed into tiles to maximize data reuse in on-chip memory:

```
  A (M×K)         B (K×N)         C (M×N)
┌──────────┐   ┌──────────┐   ┌──────────┐
│          │   │          │   │          │
│  BLOCK_M │   │          │   │  BLOCK_M │
│  ×       │ @ │  BLOCK_K │ = │  ×       │
│  BLOCK_K │   │  ×       │   │  BLOCK_N │
│          │   │  BLOCK_N │   │          │
└──────────┘   └──────────┘   └──────────┘
  Tile of A      Tile of B      Tile of C

Each program computes one BLOCK_M × BLOCK_N tile of C
by accumulating over K in steps of BLOCK_K.
```

```python
@triton.jit
def matmul_kernel(
    a_ptr, b_ptr, c_ptr,
    M, N, K,
    stride_am, stride_ak,
    stride_bk, stride_bn,
    stride_cm, stride_cn,
    BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr,
):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)

    offs_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    offs_k = tl.arange(0, BLOCK_K)

    a_ptrs = a_ptr + offs_m[:, None] * stride_am + offs_k[None, :] * stride_ak
    b_ptrs = b_ptr + offs_k[:, None] * stride_bk + offs_n[None, :] * stride_bn

    accumulator = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)

    for k in range(0, K, BLOCK_K):
        a_mask = (offs_m[:, None] < M) & (offs_k[None, :] + k < K)
        b_mask = (offs_k[:, None] + k < K) & (offs_n[None, :] < N)

        a = tl.load(a_ptrs, mask=a_mask, other=0.0)
        b = tl.load(b_ptrs, mask=b_mask, other=0.0)

        accumulator += tl.dot(a, b)

        a_ptrs += BLOCK_K * stride_ak
        b_ptrs += BLOCK_K * stride_bk

    c_ptrs = c_ptr + offs_m[:, None] * stride_cm + offs_n[None, :] * stride_cn
    c_mask = (offs_m[:, None] < M) & (offs_n[None, :] < N)
    tl.store(c_ptrs, accumulator, mask=c_mask)
```

## 27.2 Flash Attention in Triton

Flash Attention computes exact attention without materializing the full N×N attention matrix, achieving O(N) memory instead of O(N^2):

```
Standard Attention:
  S = Q @ K^T          (N×N matrix -- materialised)
  P = softmax(S)       (N×N matrix -- materialised)
  O = P @ V            Result

Flash Attention:
  For each block of Q:
    For each block of K, V:
      Compute block of S = Q_block @ K_block^T   (small tile)
      Update running softmax statistics
      Accumulate O_block = P_block @ V_block
    Rescale O using final softmax normalization
```

Key innovations:
- **Tiling:** Process Q, K, V in tiles that fit in SRAM
- **Online softmax:** Maintain running max and sum for numerically stable softmax without seeing all values
- **No O(N^2) memory:** Never materialize the full attention matrix
- **IO-awareness:** Minimize HBM reads/writes by fusing operations

## 27.3 Auto-Tuning with `triton.autotune`

```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 128, 'BLOCK_K': 32}, num_warps=4),
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 64,  'BLOCK_K': 32}, num_warps=4),
        triton.Config({'BLOCK_M': 64,  'BLOCK_N': 128, 'BLOCK_K': 32}, num_warps=4),
        triton.Config({'BLOCK_M': 64,  'BLOCK_N': 64,  'BLOCK_K': 64}, num_warps=8),
    ],
    key=['M', 'N', 'K'],
)
@triton.jit
def matmul_kernel(...):
    ...
```

The `key` parameter determines which input properties trigger re-tuning. When the problem dimensions change, Triton benchmarks all configs and caches the best one.

---

# 28. Triton Performance and Debugging

---

## 28.1 Benchmarking

```python
@triton.testing.perf_report(
    triton.testing.Benchmark(
        x_names=['N'],
        x_vals=[2**i for i in range(10, 20)],
        line_arg='provider',
        line_vals=['triton', 'torch'],
        line_names=['Triton', 'PyTorch'],
        ylabel='GB/s',
        plot_name='vector-add',
        args={},
    )
)
def benchmark(N, provider):
    x = torch.rand(N, device='cuda', dtype=torch.float32)
    y = torch.rand(N, device='cuda', dtype=torch.float32)

    if provider == 'triton':
        ms = triton.testing.do_bench(lambda: add(x, y))
    else:
        ms = triton.testing.do_bench(lambda: x + y)

    gbps = 3 * x.numel() * x.element_size() / ms * 1e-6
    return gbps
```

## 28.2 Performance Considerations

| Factor | Impact | Guidance |
|---|---|---|
| Block size | Occupancy, register pressure | Larger blocks = more data reuse, but fewer concurrent blocks |
| Memory coalescing | Bandwidth utilization | Access consecutive memory addresses within a block |
| `num_warps` | Parallelism within a block | Increase for compute-bound; decrease for memory-bound |
| `num_stages` | Pipeline depth | More stages overlap loads with compute (if register budget allows) |
| `tl.dot` precision | Speed vs accuracy | `allow_tf32=True` for tensor cores |
| Masking overhead | Extra instructions | Minimize by choosing block sizes that evenly divide problem |

## 28.3 Debugging Strategies

```python
# Print from kernel (for small inputs)
@triton.jit
def debug_kernel(x_ptr, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    offsets = tl.arange(0, BLOCK_SIZE)
    x = tl.load(x_ptr + offsets)
    tl.device_print("pid", pid)
    tl.device_print("values", x)

# Interpret mode (run on CPU for debugging)
# TRITON_INTERPRET=1 python script.py
```

---

# 29. Triton Ecosystem and Interview Questions

---

## 29.1 Triton for AMD (ROCm)

Triton supports AMD GPUs through a ROCm backend that generates AMDGPU ISA instead of PTX. The same Triton kernel source code works on both NVIDIA and AMD hardware -- only the compilation backend changes.

## 29.2 OpenAI Triton vs NVIDIA Triton Inference Server

| | OpenAI Triton | NVIDIA Triton Inference Server |
|---|---|---|
| What | GPU kernel programming language | Model serving platform |
| Purpose | Write custom GPU kernels in Python | Serve ML models at scale |
| Abstraction | Compiler (code → GPU binary) | Server (model → REST/gRPC API) |
| Competitors | CUDA, HIP, SYCL | TorchServe, TF Serving, vLLM |

## 29.3 Integration with PyTorch

```python
# Custom op via torch.library
@torch.library.custom_op("mylib::add", mutates_args=())
def add(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    output = torch.empty_like(x)
    n = output.numel()
    grid = lambda meta: (triton.cdiv(n, meta['BLOCK_SIZE']),)
    add_kernel[grid](x, y, output, n, BLOCK_SIZE=1024)
    return output

# torch.compile will use the Triton kernel
compiled_model = torch.compile(model)
```

## 29.4 Interview Questions

**Q1: What advantage does Triton's block-level programming model have over CUDA's thread-level model?**

Triton abstracts away low-level concerns like shared memory allocation, thread synchronization, memory coalescing, and warp scheduling. The programmer specifies operations on entire blocks (tiles) of data, and the Triton compiler automatically handles the mapping to hardware. This dramatically reduces development time while achieving ~90-100% of hand-tuned CUDA performance. CUDA requires explicit management of all these details, which is error-prone but allows maximum control.

**Q2: How does Flash Attention reduce memory from O(N^2) to O(N)?**

Standard attention materializes the full N×N attention score matrix and the N×N softmax output in GPU HBM. Flash Attention processes Q, K, V in tiles that fit in on-chip SRAM, computes partial attention scores per tile, and maintains running softmax statistics (max and sum) using an online softmax algorithm. It never writes the full attention matrix to HBM -- only the final output O (N×d). This reduces memory from O(N^2) to O(N) and also reduces HBM I/O, making it faster despite doing the same FLOPs.

**Q3: What is `triton.autotune` and why is it important?**

`triton.autotune` automatically benchmarks a kernel across multiple configurations (block sizes, number of warps, pipeline stages) and selects the fastest one for the given problem size. This is important because optimal kernel parameters depend on the specific hardware (different GPUs have different SRAM sizes, warp counts, memory bandwidth) and problem dimensions. Auto-tuning replaces manual performance engineering with empirical optimization. Results are cached so the tuning cost is paid only once.

**Q4: How does Triton achieve portability across NVIDIA and AMD GPUs?**

Triton's compilation pipeline lowers kernel code through multiple intermediate representations (Triton IR → TTIR → TTGIR → LLVM IR) before generating hardware-specific code. The frontend and middle-end are hardware-agnostic. Only the final backend step differs: generating PTX for NVIDIA GPUs or AMDGPU ISA for AMD GPUs. This means the same kernel source code runs on both vendors' hardware.

---

# Part 5: vLLM

---

# 30. vLLM Architecture and PagedAttention

---

## 30.1 What Is vLLM?

vLLM is a high-throughput, memory-efficient inference and serving engine for Large Language Models (LLMs). Its key innovation is **PagedAttention**, which manages the KV (Key-Value) cache using ideas from OS virtual memory management.

```
┌────────────────────────────────────────────────┐
│                   vLLM Engine                   │
├────────────────────────────────────────────────┤
│  API Layer (OpenAI-compatible / Offline)       │
├────────────────────────────────────────────────┤
│  Scheduler (continuous batching)               │
│    ├── Request queue                           │
│    ├── Preemption (swap / recompute)           │
│    └── Prefix caching                          │
├────────────────────────────────────────────────┤
│  KV Cache Manager (PagedAttention)             │
│    ├── Block allocator                         │
│    ├── Block table (logical → physical)        │
│    └── Copy-on-write                           │
├────────────────────────────────────────────────┤
│  Model Execution                               │
│    ├── Attention backends (FlashAttention, etc)│
│    ├── Tensor parallelism                      │
│    └── Quantization                            │
├────────────────────────────────────────────────┤
│  GPU(s)                                        │
└────────────────────────────────────────────────┘
```

## 30.2 The KV Cache Problem

During autoregressive LLM generation, each token's attention requires the Key and Value tensors of all previous tokens. These KV pairs must be stored in GPU memory.

```
Memory per token per layer:
  2 (K + V) × n_heads × head_dim × dtype_size

Example (LLaMA-70B, FP16):
  2 × 64 heads × 128 dim × 2 bytes × 80 layers = 2.6 MB per token
  2048-token sequence = ~5.3 GB per request
```

**Traditional approach:** Pre-allocate max-length contiguous buffers per request. Problem: massive internal fragmentation (most sequences don't reach max length) and external fragmentation (gaps between sequences).

## 30.3 PagedAttention

PagedAttention manages KV cache like OS virtual memory -- splitting it into fixed-size **blocks** (pages) that need not be contiguous in physical GPU memory.

```
Logical View (per sequence):          Physical GPU Memory:
┌─────┬─────┬─────┬─────┐            ┌─────┐
│Blk 0│Blk 1│Blk 2│Blk 3│            │Phy 7│ ← Seq A Blk 0
└──┬──┴──┬──┴──┬──┴──┬──┘            ├─────┤
   │     │     │     │                │Phy 2│ ← Seq A Blk 1
   ▼     ▼     ▼     ▼               ├─────┤
 Phy 7 Phy 2 Phy 5 Phy 9             │Phy 3│ ← Seq B Blk 0
                                      ├─────┤
Block Table (Seq A):                  │Phy 5│ ← Seq A Blk 2
┌───────┬────────┐                    ├─────┤
│Logical│Physical│                    │Phy 9│ ← Seq A Blk 3
├───────┼────────┤                    ├─────┤
│   0   │   7    │                    │Phy 1│ ← Seq B Blk 1
│   1   │   2    │                    └─────┘
│   2   │   5    │
│   3   │   9    │
└───────┴────────┘
```

**Benefits:**

| Feature | Traditional | PagedAttention |
|---|---|---|
| Internal fragmentation | Up to max_seq_len wasted | < 1 block wasted |
| External fragmentation | Memory holes between seqs | None (block granularity) |
| Memory utilization | ~50-60% | ~95%+ |
| Copy-on-write | Not supported | Supported (parallel sampling) |
| Throughput improvement | Baseline | 2-4x higher (more concurrent seqs) |

## 30.4 Copy-on-Write for Parallel Sampling

When generating multiple outputs from the same prompt (beam search, parallel sampling), PagedAttention shares the prompt's KV cache blocks across all sequences. A block is copied only when one sequence modifies it.

```
Prompt tokens: shared blocks (reference counted)

Seq 1: [shared][shared][shared][own block]
Seq 2: [shared][shared][shared][own block]
Seq 3: [shared][shared][shared][own block]

Memory = 1 × prompt_blocks + N × unique_blocks
vs.
Traditional: N × (prompt_blocks + unique_blocks)
```

---

# 31. Serving and API

---

## 31.1 Offline Inference

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-8B-Instruct")

sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    max_tokens=256,
    repetition_penalty=1.1,
    stop=["</s>", "\n\n"],
)

prompts = ["Explain quantum computing:", "Write a haiku about AI:"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(output.outputs[0].text)
```

## 31.2 Online Serving (OpenAI-Compatible API)

```bash
# Launch server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3-8B-Instruct \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 4096 \
    --port 8000
```

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

response = client.chat.completions.create(
    model="meta-llama/Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=0.7,
    max_tokens=256,
)
print(response.choices[0].message.content)
```

## 31.3 Key `SamplingParams`

| Parameter | Description | Default |
|---|---|---|
| `temperature` | Controls randomness (0 = greedy) | 1.0 |
| `top_p` | Nucleus sampling threshold | 1.0 |
| `top_k` | Top-k filtering | -1 (disabled) |
| `max_tokens` | Maximum tokens to generate | 16 |
| `min_tokens` | Minimum tokens before stop | 0 |
| `repetition_penalty` | Penalize repeated tokens | 1.0 |
| `stop` | Stop strings/tokens | None |
| `n` | Number of output sequences | 1 |
| `best_of` | Generate n, return best (beam search) | 1 |
| `presence_penalty` | Penalize token presence | 0.0 |
| `frequency_penalty` | Penalize token frequency | 0.0 |
| `logprobs` | Return log probabilities | None |

---

# 32. Scheduling and Batching

---

## 32.1 Static vs Continuous Batching

```
Static Batching:
  ┌──────────────────────────────────────┐
  │ Seq 1: ████████████░░░░░░░░░░ (done) │ ← waits for longest
  │ Seq 2: ████████████████████████(done) │
  │ Seq 3: ██████░░░░░░░░░░░░░░░░ (done) │ ← GPU idle time
  └──────────────────────────────────────┘
  All sequences must finish before new batch starts.

Continuous Batching:
  ┌──────────────────────────────────────┐
  │ Seq 1: ████████████                  │
  │ Seq 2: ████████████████████████      │
  │ Seq 3: ██████                        │
  │ Seq 4:       ████████████████        │ ← inserted when Seq 3 finishes
  │ Seq 5:             ████████████      │ ← inserted when Seq 1 finishes
  └──────────────────────────────────────┘
  New sequences inserted at iteration level.
```

| Aspect | Static Batching | Continuous Batching |
|---|---|---|
| Granularity | Request-level | Iteration-level |
| GPU utilization | Low (shortest seqs idle) | High (always filling slots) |
| Throughput | Baseline | 2-3x improvement |
| Latency | High (wait for longest) | Lower (early completion) |
| Implementation | Simple | Complex (per-iteration scheduling) |

## 32.2 Prefill vs Decode Phases

| Phase | Computation | Characteristic |
|---|---|---|
| **Prefill** | Process all prompt tokens in parallel | Compute-bound (large matmul) |
| **Decode** | Generate tokens one at a time | Memory-bound (small matmul, KV cache reads) |

**Chunked prefill:** Split long prompts into chunks and interleave prefill chunks with decode steps from other sequences. This prevents long prefills from blocking decode steps and improves overall latency.

## 32.3 Preemption Strategies

When GPU memory is exhausted, vLLM preempts lower-priority sequences:

| Strategy | Mechanism | Latency Cost | Memory Cost |
|---|---|---|---|
| **Swap** | Move KV blocks to CPU memory | Moderate (PCIe transfer) | CPU memory |
| **Recompute** | Discard KV blocks, recompute later | Higher (redo prefill) | None |

## 32.4 Prefix Caching

Requests sharing the same prompt prefix (e.g., system prompt) can reuse cached KV blocks:

```
Request 1: [System prompt] + "What is AI?"
Request 2: [System prompt] + "Explain GPUs"

With prefix caching:
  [System prompt] KV blocks computed once, shared across requests
  Only unique suffixes require new computation
```

## 32.5 Speculative Decoding

Use a smaller "draft" model to generate candidate tokens quickly, then verify them in parallel with the large "target" model:

```
Draft model (fast):  generates tokens t1, t2, t3, t4, t5
Target model:        verifies all 5 in one forward pass
Accept:              t1 ✓, t2 ✓, t3 ✓, t4 ✗ → keep t1-t3, resample t4

Speedup: up to Nx where N = average accepted tokens per step
```

---

# 33. Quantization and Model Optimization

---

## 33.1 Quantization Methods

| Method | Bits | Type | Calibration | Quality |
|---|---|---|---|---|
| FP16 | 16 | Float | None | Baseline |
| BF16 | 16 | Float | None | ~Same as FP16 |
| INT8 (W8A8) | 8 | Integer | Activation stats | Slight degradation |
| FP8 (E4M3/E5M2) | 8 | Float | None/Activation stats | Near FP16 |
| GPTQ | 4/3/2 | Integer (weights only) | Calibration dataset | Good (4-bit) |
| AWQ | 4 | Integer (weights only) | Activation-aware | Better than GPTQ |
| SqueezeLLM | 4/3 | Mixed (non-uniform) | Sensitivity analysis | Good |
| GGUF/GGML | Variable | Mixed | Various | Flexible |

```python
# Using a pre-quantized model
llm = LLM(model="TheBloke/Llama-2-7B-GPTQ", quantization="gptq")

# FP8 quantization
llm = LLM(model="meta-llama/Llama-3-8B", quantization="fp8")

# AWQ
llm = LLM(model="TheBloke/Llama-2-7B-AWQ", quantization="awq")
```

## 33.2 KV Cache Quantization

Compress the KV cache itself (separate from model weight quantization):

```python
llm = LLM(
    model="meta-llama/Llama-3-8B",
    kv_cache_dtype="fp8",    # quantize KV cache to FP8
)
```

## 33.3 LoRA Serving

vLLM supports serving multiple LoRA adapters on a single base model:

```python
from vllm.lora.request import LoRARequest

llm = LLM(model="meta-llama/Llama-3-8B", enable_lora=True)

output = llm.generate(
    "Translate to French: Hello world",
    SamplingParams(max_tokens=100),
    lora_request=LoRARequest("translator", 1, "/path/to/lora/adapter"),
)
```

---

# 34. vLLM Distributed Inference and Interview Questions

---

## 34.1 Distributed Inference

```bash
# Tensor parallelism (split layers across GPUs)
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3-70B \
    --tensor-parallel-size 4

# Pipeline parallelism (split layers sequentially)
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3-70B \
    --pipeline-parallel-size 2 \
    --tensor-parallel-size 2
```

| Parallelism | How | Latency | Throughput | When |
|---|---|---|---|---|
| Tensor | Split weight matrices across GPUs | +All-reduce overhead | High | Model doesn't fit 1 GPU |
| Pipeline | Split layers across GPUs | +Pipeline bubble | Higher | Many GPUs, large models |
| TP + PP | Combine both | Balanced | Highest | Very large models (70B+) |

## 34.2 Performance Tuning

| Parameter | Effect | Guidance |
|---|---|---|
| `gpu-memory-utilization` | Fraction of GPU memory for KV cache | 0.9 (default), lower if OOM |
| `max-num-seqs` | Max concurrent sequences | Higher = more throughput, more memory |
| `max-model-len` | Maximum sequence length | Lower saves memory |
| `enable-chunked-prefill` | Chunk long prefills | Improves decode latency |
| `enable-prefix-caching` | Cache shared prefixes | Huge win for shared prompts |
| `enforce-eager` | Disable CUDA graphs | Debugging only |
| `dtype` | Model precision | `auto`, `float16`, `bfloat16` |

## 34.3 Interview Questions

**Q1: What is PagedAttention and why is it important?**

PagedAttention manages the KV cache using OS virtual memory concepts. It divides the KV cache into fixed-size blocks that need not be contiguous in physical GPU memory, using a block table to map logical to physical blocks. This eliminates internal fragmentation (pre-allocated max-length buffers) and external fragmentation (memory holes), improving memory utilization from ~50-60% to ~95%+. The result is 2-4x higher throughput because more sequences can be served concurrently.

**Q2: Explain continuous batching vs static batching.**

Static batching groups a fixed set of requests into a batch and processes them until all complete -- shorter sequences waste GPU time waiting for the longest one. Continuous batching operates at the iteration level: as soon as a sequence finishes, a new one is inserted into the batch. This keeps the GPU fully utilized and can improve throughput by 2-3x, especially when generation lengths vary significantly.

**Q3: How does speculative decoding work?**

A small, fast "draft" model generates K candidate tokens autoregressively. The large "target" model then evaluates all K tokens in a single forward pass (parallelizing what would be K sequential steps). If the draft model's predictions match the target model's distribution (verified using a rejection sampling scheme), they are accepted. If token i is rejected, tokens i+1 through K are discarded. On average, N tokens are accepted per step (N > 1), providing a speedup proportional to N while guaranteeing the same output distribution as the target model alone.

**Q4: What is the difference between tensor parallelism and pipeline parallelism in vLLM?**

Tensor parallelism splits each layer's weight matrices across multiple GPUs, with all GPUs processing the same sequence simultaneously and synchronizing via all-reduce after each layer. It adds per-layer communication overhead but doesn't increase latency significantly for few GPUs. Pipeline parallelism assigns different layers to different GPUs and pipelines micro-batches through them. It introduces "pipeline bubbles" (idle time) but reduces per-GPU communication. TP is preferred for low latency; PP is added when the model is too large for TP alone.

---

# Part 6: SGLang

---

# 35. SGLang Architecture and Runtime

---

## 35.1 What Is SGLang?

SGLang (Structured Generation Language) is a framework for fast and controllable LLM inference, combining a frontend DSL for structured LLM programs with a high-performance backend runtime (SGLang Runtime / SRT). Its key innovation is **RadixAttention**, which uses a radix tree to automatically reuse KV cache across requests sharing common prefixes.

```
┌──────────────────────────────────────────────┐
│              SGLang Architecture              │
├──────────────────────────────────────────────┤
│  Frontend (Python DSL)                       │
│    gen(), select(), fork(), @function        │
│    Constrained decoding (regex, JSON schema) │
├──────────────────────────────────────────────┤
│  SGLang Runtime (SRT)                        │
│    ├── RadixAttention (prefix tree KV cache) │
│    ├── Continuous batching scheduler         │
│    ├── FlashInfer attention backend          │
│    ├── CUDA graph caching                    │
│    └── Chunked prefill                       │
├──────────────────────────────────────────────┤
│  Model Backend                               │
│    ├── Tensor parallelism                    │
│    ├── Quantization (FP8, INT4, GPTQ, AWQ)  │
│    └── Speculative decoding                  │
├──────────────────────────────────────────────┤
│  GPU(s)                                      │
└──────────────────────────────────────────────┘
```

## 35.2 RadixAttention

Unlike vLLM's block-based page table, SGLang organizes the KV cache as a **radix tree** (prefix tree), enabling automatic detection and sharing of common prefixes across all requests.

```
Radix Tree of KV Cache:

              [System Prompt]
              /             \
     [Few-shot Ex. 1]    [Few-shot Ex. A]
      /          \            \
[Question 1] [Question 2]  [Question B]

All requests sharing the same prefix automatically
reuse the cached KV blocks up to the branching point.
```

**RadixAttention vs PagedAttention:**

| Aspect | PagedAttention (vLLM) | RadixAttention (SGLang) |
|---|---|---|
| Data structure | Block table (flat mapping) | Radix tree (prefix tree) |
| Prefix sharing | Explicit prefix caching (opt-in) | Automatic (tree structure) |
| Multi-turn reuse | Limited | Natural (tree extension) |
| Few-shot patterns | Manual caching | Automatic dedup |
| Memory overhead | Low (block table) | Slightly higher (tree nodes) |
| Cache eviction | LRU on blocks | LRU on tree nodes |

## 35.3 Request Scheduling

SGLang's scheduler extends continuous batching with:

- **Priority scheduling:** Urgent requests can preempt batch slots
- **Prefix-aware scheduling:** Requests sharing prefixes are co-scheduled
- **Chunked prefill:** Long prompts processed in chunks to avoid blocking
- **Constraint-aware batching:** Groups requests with similar constrained decoding patterns

---

# 36. Programming Model

---

## 36.1 The SGLang DSL

```python
import sglang as sgl

@sgl.function
def multi_turn_qa(s, question1, question2):
    s += sgl.system("You are a helpful assistant.")
    s += sgl.user(question1)
    s += sgl.assistant(sgl.gen("answer1", max_tokens=256))
    s += sgl.user(question2)
    s += sgl.assistant(sgl.gen("answer2", max_tokens=256))

state = multi_turn_qa.run(
    question1="What is machine learning?",
    question2="Give me an example.",
)
print(state["answer1"])
print(state["answer2"])
```

## 36.2 Core Primitives

| Primitive | Description | Example |
|---|---|---|
| `sgl.gen(name, ...)` | Generate text | `sgl.gen("answer", max_tokens=100)` |
| `sgl.select(name, choices)` | Choose from options | `sgl.select("choice", ["yes", "no"])` |
| `sgl.fork(n)` | Parallel generation branches | `forks = s.fork(3)` |
| `sgl.image(...)` | Multi-modal image input | `sgl.image(image_data)` |
| `sgl.system(text)` | System message | `sgl.system("You are...")` |
| `sgl.user(text)` | User message | `sgl.user("Hello")` |
| `sgl.assistant(...)` | Assistant message | `sgl.assistant(sgl.gen(...))` |

## 36.3 Constrained Decoding

```python
@sgl.function
def structured_output(s, query):
    s += sgl.user(query)
    s += sgl.assistant(sgl.gen(
        "response",
        max_tokens=512,
        regex=r'\{"name": "[a-zA-Z ]+", "age": \d+, "city": "[a-zA-Z ]+"\}'
    ))

# JSON schema constraint
@sgl.function
def json_output(s, query):
    s += sgl.user(query)
    s += sgl.assistant(sgl.gen(
        "response",
        max_tokens=512,
        json_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "skills": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["name", "age"]
        }
    ))
```

## 36.4 Forking for Parallel Generation

```python
@sgl.function
def tree_of_thought(s, problem):
    s += sgl.system("Think step by step.")
    s += sgl.user(problem)

    forks = s.fork(3)
    for f in forks:
        f += sgl.assistant(sgl.gen("thought", max_tokens=256, temperature=0.9))

    # All forks share the prompt's KV cache (RadixAttention)
    thoughts = [f["thought"] for f in forks]
    return thoughts
```

---

# 37. Performance Features

---

## 37.1 Performance Techniques

| Feature | Description | Impact |
|---|---|---|
| RadixAttention | Automatic KV cache prefix sharing | Major for multi-turn / few-shot |
| Continuous batching | Iteration-level scheduling | High throughput |
| Chunked prefill | Split long prefills into chunks | Lower decode latency |
| CUDA graph caching | Cache compiled CUDA graphs | Reduced kernel launch overhead |
| FlashInfer backend | Optimized attention kernels | Faster attention computation |
| Tensor parallelism | Split across GPUs | Large model support |
| Speculative decoding | Draft model + verification | Faster generation |
| FP8/INT4 quantization | Reduced precision | Lower memory, higher throughput |
| Torch.compile | Graph compilation | Optimized execution |

## 37.2 Constrained Decoding Performance

SGLang uses a **compressed finite-state machine** for constrained decoding, which is significantly faster than token-by-token constraint checking:

```
Traditional: Check constraint for each generated token → O(vocabulary) per token
SGLang FSM: Pre-compute valid token sets per state → O(1) lookup per token
```

---

# 38. SGLang Deployment and Interview Questions

---

## 38.1 Server Launch

```bash
# Basic server
python -m sglang.launch_server \
    --model-path meta-llama/Llama-3-8B-Instruct \
    --port 30000

# With tensor parallelism
python -m sglang.launch_server \
    --model-path meta-llama/Llama-3-70B-Instruct \
    --tp 4 \
    --port 30000

# With quantization
python -m sglang.launch_server \
    --model-path meta-llama/Llama-3-8B-Instruct \
    --quantization fp8 \
    --port 30000
```

## 38.2 OpenAI-Compatible API

```python
import openai

client = openai.Client(base_url="http://localhost:30000/v1", api_key="none")

response = client.chat.completions.create(
    model="meta-llama/Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

## 38.3 SGLang vs vLLM

| Feature | SGLang | vLLM |
|---|---|---|
| KV cache strategy | RadixAttention (radix tree) | PagedAttention (block table) |
| Prefix caching | Automatic (tree structure) | Explicit (opt-in) |
| Frontend DSL | Rich (gen, select, fork, constraints) | Basic (prompt-in, text-out) |
| Constrained decoding | Built-in (regex, JSON schema, FSM) | Limited |
| Multi-turn optimization | Excellent (tree extension) | Good |
| Structured output | First-class support | Via guided decoding |
| Model support breadth | Growing | Very wide |
| Community size | Smaller but growing | Large |
| Production maturity | Newer | More mature |
| Performance | Comparable to faster | Highly optimized |

## 38.4 Interview Questions

**Q1: What is RadixAttention and how does it differ from PagedAttention?**

RadixAttention organizes the KV cache as a radix tree (prefix tree) where each edge represents a sequence of tokens and nodes represent shared prefixes. When a new request arrives, the runtime traverses the tree to find the longest matching prefix and reuses its KV cache. This happens automatically without explicit configuration. PagedAttention uses a flat block table mapping logical to physical memory blocks. Prefix caching in vLLM requires explicit opt-in and hashing. RadixAttention naturally handles multi-turn conversations (extending tree branches) and few-shot patterns (shared prefix paths).

**Q2: How does SGLang's constrained decoding work?**

SGLang converts regex patterns or JSON schemas into a compressed finite-state machine (FSM). At each decoding step, the FSM state determines which tokens are valid, and invalid tokens are masked before sampling. The FSM states and valid token sets are pre-computed, making the per-token overhead minimal (O(1) lookup). This is more efficient than alternatives that check constraints token-by-token against the full vocabulary.

**Q3: What is the benefit of the `fork()` primitive?**

`fork()` creates multiple parallel generation branches from the same prefix. Because RadixAttention stores the shared prefix's KV cache in the tree, all forks automatically share it without duplication. This enables patterns like tree-of-thought (generate multiple reasoning paths), parallel sampling (best-of-N), and multi-candidate ranking, all with minimal memory overhead. In systems without prefix caching, each fork would redundantly store the full prompt's KV cache.

---

# Part 7: Megatron-LM

---

# 39. Megatron-LM Architecture

---

## 39.1 What Is Megatron-LM?

Megatron-LM is NVIDIA's framework for training large Transformer models (GPT, BERT, T5) at scale using **3D parallelism**: the combination of data parallelism, tensor (model) parallelism, and pipeline parallelism. It is designed for training models with hundreds of billions of parameters across thousands of GPUs.

```
3D Parallelism:

  ┌──────────────────────────────────────────┐
  │           Data Parallelism               │
  │  (replicate model, split data)           │
  │                                          │
  │  ┌────────────────────────────────────┐  │
  │  │      Pipeline Parallelism          │  │
  │  │  (split layers across GPU groups)  │  │
  │  │                                    │  │
  │  │  ┌──────────────────────────────┐  │  │
  │  │  │   Tensor Parallelism         │  │  │
  │  │  │  (split layers within GPUs)  │  │  │
  │  │  └──────────────────────────────┘  │  │
  │  └────────────────────────────────────┘  │
  └──────────────────────────────────────────┘
```

## 39.2 Parallelism Dimensions

| Dimension | Splits | Communication | Granularity |
|---|---|---|---|
| **Data Parallel (DP)** | Training data across replicas | All-reduce gradients | Per training step |
| **Tensor Parallel (TP)** | Weight matrices within a layer | All-reduce / all-gather per layer | Per layer forward/backward |
| **Pipeline Parallel (PP)** | Layers across GPU groups | Point-to-point (activations) | Per micro-batch |

**Typical mapping on a multi-node cluster:**

```
Cluster: 2 nodes × 8 GPUs = 16 GPUs
TP=4, PP=2, DP=2

Node 0:                          Node 1:
┌─────────────────────────┐    ┌─────────────────────────┐
│ TP Group 0 (Layers 0-N/2)│    │ TP Group 0 (Layers 0-N/2)│
│ GPU0 GPU1 GPU2 GPU3     │    │ GPU8  GPU9  GPU10 GPU11 │
│ DP Replica 0            │    │ DP Replica 1             │
├─────────────────────────┤    ├─────────────────────────┤
│ TP Group 1 (Layers N/2-N)│    │ TP Group 1 (Layers N/2-N)│
│ GPU4 GPU5 GPU6 GPU7     │    │ GPU12 GPU13 GPU14 GPU15 │
│ DP Replica 0            │    │ DP Replica 1             │
└─────────────────────────┘    └─────────────────────────┘
     Pipeline Stage 0/1              Pipeline Stage 0/1
```

## 39.3 Supported Architectures

| Model | Architecture | Typical Scale |
|---|---|---|
| GPT | Decoder-only Transformer | 1B - 1T parameters |
| BERT | Encoder-only Transformer | 110M - 4B parameters |
| T5 | Encoder-decoder Transformer | 220M - 11B parameters |

---

# 40. Tensor Parallelism

---

## 40.1 Column-Parallel Linear

Split the weight matrix along columns (output dimension). Each GPU holds a slice and computes a partial output. Results are concatenated or gathered.

```
Input X (replicated on all GPUs):

         W = [W₁ | W₂ | W₃ | W₄]    (split along columns)

GPU 0: Y₁ = X @ W₁     (partial output)
GPU 1: Y₂ = X @ W₂     (partial output)
GPU 2: Y₃ = X @ W₃     (partial output)
GPU 3: Y₄ = X @ W₄     (partial output)

Y = [Y₁ | Y₂ | Y₃ | Y₄]            (concatenate)
```

## 40.2 Row-Parallel Linear

Split the weight matrix along rows (input dimension). Each GPU holds a slice and computes a partial result. Results are summed (all-reduce).

```
Input X split along last dimension: X = [X₁ | X₂ | X₃ | X₄]

         W split along rows:
         ┌─W₁─┐
         │ W₂ │
         │ W₃ │
         └─W₄─┘

GPU 0: Y₁ = X₁ @ W₁    (partial result)
GPU 1: Y₂ = X₂ @ W₂    (partial result)
GPU 2: Y₃ = X₃ @ W₃    (partial result)
GPU 3: Y₄ = X₄ @ W₄    (partial result)

Y = Y₁ + Y₂ + Y₃ + Y₄   (all-reduce sum)
```

## 40.3 Transformer MLP Parallelism

The MLP block uses column-parallel for the first linear and row-parallel for the second, requiring only **one all-reduce** per MLP block:

```
      Input X (replicated)
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
  Col-Par Col-Par Col-Par    (First linear: column-parallel)
  Linear  Linear  Linear     Each GPU: X @ W₁ᵢ
    │     │     │
    ▼     ▼     ▼
   GeLU  GeLU  GeLU          (Activation: local, no communication)
    │     │     │
    ▼     ▼     ▼
  Row-Par Row-Par Row-Par    (Second linear: row-parallel)
  Linear  Linear  Linear     Each GPU: Xᵢ @ W₂ᵢ
    │     │     │
    └─────┼─────┘
          ▼
      All-Reduce              (Sum partial results: one communication)
          │
          ▼
       Output Y
```

## 40.4 Attention Head Parallelism

Multi-head attention is naturally tensor-parallel: each GPU computes a subset of attention heads. Q, K, V projections are column-parallel, and the output projection is row-parallel.

```
Input X (replicated)
    │
    ├──── Q = X @ Wq  (column-parallel: each GPU gets heads/TP heads)
    ├──── K = X @ Wk  (column-parallel)
    └──── V = X @ Wv  (column-parallel)
              │
         Attention (local per GPU, on subset of heads)
              │
         Out = Attn @ Wo  (row-parallel)
              │
         All-Reduce
              │
         Output
```

## 40.5 Communication Analysis

| Layer | Forward | Backward | Communication |
|---|---|---|---|
| Column-parallel linear | No comm (identity) | All-reduce | 1 all-reduce |
| Row-parallel linear | All-reduce | No comm (identity) | 1 all-reduce |
| MLP block (col + row) | 1 all-reduce | 1 all-reduce | 2 all-reduces |
| Attention block | 1 all-reduce | 1 all-reduce | 2 all-reduces |
| Transformer layer | 2 all-reduces | 2 all-reduces | 4 all-reduces |

---

# 41. Pipeline Parallelism

---

## 41.1 Pipeline Stage Assignment

Layers are split into sequential stages, each assigned to a different GPU group:

```
Model: 32 layers, PP=4

Stage 0 (GPU Group 0): Layers  0-7   + Embedding
Stage 1 (GPU Group 1): Layers  8-15
Stage 2 (GPU Group 2): Layers 16-23
Stage 3 (GPU Group 3): Layers 24-31  + Output head
```

## 41.2 GPipe Schedule

Process all micro-batches through each stage before moving to the next. Large pipeline bubble at the start and end.

```
GPipe (4 stages, 8 micro-batches):

Stage 0: F0 F1 F2 F3 F4 F5 F6 F7 ░░░░░░░░░░░░░░░░ B7 B6 B5 B4 B3 B2 B1 B0
Stage 1: ░░ F0 F1 F2 F3 F4 F5 F6 F7 ░░░░░░░░░░░░░░ B7 B6 B5 B4 B3 B2 B1 B0
Stage 2: ░░░░ F0 F1 F2 F3 F4 F5 F6 F7 ░░░░░░░░░░░░ B7 B6 B5 B4 B3 B2 B1 B0
Stage 3: ░░░░░░ F0 F1 F2 F3 F4 F5 F6 F7 ░░░░░░░░░░ B7 B6 B5 B4 B3 B2 B1 B0

░ = Idle (pipeline bubble)
F = Forward pass    B = Backward pass

Bubble fraction = (PP - 1) / (PP - 1 + M)  where M = num micro-batches
```

## 41.3 1F1B (One Forward, One Backward) Schedule

Interleave forward and backward passes to reduce the pipeline bubble:

```
1F1B (4 stages, 8 micro-batches):

Stage 0: F0 F1 F2 F3 B0 F4 B1 F5 B2 F6 B3 F7 B4 B5 B6 B7
Stage 1: ░░ F0 F1 F2 F3 B0 F4 B1 F5 B2 F6 B3 F7 B4 B5 B6 B7
Stage 2: ░░░░ F0 F1 F2 F3 B0 F4 B1 F5 B2 F6 B3 F7 B4 B5 B6 B7
Stage 3: ░░░░░░ F0 F1 F2 F3 B0 F4 B1 F5 B2 F6 B3 F7 B4 B5 B6 B7

Smaller bubble: only (PP - 1) warmup steps instead of PP × M steps idle.
```

**Memory advantage:** 1F1B requires storing activations for at most PP micro-batches at peak, vs M micro-batches for GPipe.

## 41.4 Interleaved 1F1B (Virtual Pipeline Stages)

Assign multiple non-contiguous layer groups to each device, reducing the effective pipeline depth:

```
Physical device 0: Layers 0-3,  Layers 16-19  (Virtual stages 0, 4)
Physical device 1: Layers 4-7,  Layers 20-23  (Virtual stages 1, 5)
Physical device 2: Layers 8-11, Layers 24-27  (Virtual stages 2, 6)
Physical device 3: Layers 12-15,Layers 28-31  (Virtual stages 3, 7)

Bubble fraction ≈ (PP - 1) / (PP - 1 + V × M)
where V = number of virtual stages per device

More virtual stages → smaller bubble, but more communication.
```

## 41.5 Pipeline Bubble Analysis

| Schedule | Bubble Fraction | Memory (activations) |
|---|---|---|
| GPipe | (P-1) / (P-1+M) | O(M × a) |
| 1F1B | (P-1) / (P-1+M) (same time, but...) | O(P × a) (much less) |
| Interleaved 1F1B | (P-1) / (P-1+V×M) | O(P × a) |

Where P = pipeline stages, M = micro-batches, V = virtual stages, a = per-micro-batch activation memory.

---

# 42. Sequence Parallelism and Context Parallelism

---

## 42.1 Sequence Parallelism

In tensor parallelism, operations like LayerNorm and Dropout are replicated across all TP ranks (since they don't involve sharded weights). Sequence parallelism splits the **sequence dimension** of these operations across TP ranks, saving memory.

```
Without Sequence Parallelism:
  LayerNorm input: (batch, seq_len, hidden)      ← replicated on all GPUs
  Dropout:         (batch, seq_len, hidden)      ← replicated on all GPUs

With Sequence Parallelism:
  LayerNorm input: (batch, seq_len/TP, hidden)   ← each GPU has 1/TP of sequence
  Dropout:         (batch, seq_len/TP, hidden)   ← each GPU has 1/TP of sequence

Communication change:
  All-Reduce → All-Gather (before TP region) + Reduce-Scatter (after TP region)
```

**Memory savings:** Activation memory for LayerNorm, Dropout, and residual connections is reduced by factor of TP.

## 42.2 Context Parallelism

For very long sequences (100K+ tokens), even the attention computation's memory and compute become bottlenecks. Context parallelism splits the **sequence across GPUs** for the attention computation.

```
Context Parallelism (CP=4, sequence length=32K):

GPU 0: tokens  0-8K     ← Q₀, K₀, V₀
GPU 1: tokens  8K-16K   ← Q₁, K₁, V₁
GPU 2: tokens  16K-24K  ← Q₂, K₂, V₂
GPU 3: tokens  24K-32K  ← Q₃, K₃, V₃

Attention: Each GPU needs ALL K, V but only its Q chunk.
Ring Attention: K, V blocks circulate in a ring.
```

**Ring Attention:** K and V blocks are passed around a ring of GPUs. Each GPU computes attention with its local Q and the currently held K, V block, then passes K, V to the next GPU. After a full revolution, each GPU has its complete attention output.

```
Step 1: GPU 0 has (Q₀, K₀, V₀), GPU 1 has (Q₁, K₁, V₁), ...
Step 2: K, V shift → GPU 0 has (Q₀, K₃, V₃), GPU 1 has (Q₁, K₀, V₀), ...
Step 3: K, V shift → GPU 0 has (Q₀, K₂, V₂), ...
Step 4: K, V shift → GPU 0 has (Q₀, K₁, V₁), ...
After 4 steps: each GPU has computed full attention for its Q chunk.
```

## 42.3 Parallelism Dimension Summary

| Parallelism | What's Split | Communication | Memory Savings | When to Use |
|---|---|---|---|---|
| Data (DP) | Training data | All-reduce grads | Optimizer state (with ZeRO) | Always |
| Tensor (TP) | Weight matrices | All-reduce per layer | Model parameters | Model > 1 GPU |
| Pipeline (PP) | Layers | Point-to-point activations | Model parameters | Many GPUs |
| Sequence (SP) | Sequence (non-attention) | All-gather/reduce-scatter | Activation memory | With TP |
| Context (CP) | Sequence (attention) | Ring exchange of K, V | Attention memory | Very long sequences |

---

# 43. Megatron-LM Training Recipes and Interview Questions

---

## 43.1 Mixed Precision Training

Megatron-LM uses BF16 or FP16 mixed precision with the following precision rules:

```
Computation:     BF16/FP16 (forward + backward)
Accumulation:    FP32 (matmul accumulators, loss, grad norms)
Master weights:  FP32 (optimizer holds FP32 copy)
Communication:   FP32 or BF16 (all-reduce can use reduced precision)
```

## 43.2 Distributed Optimizer

Shards optimizer states across data-parallel ranks (similar to ZeRO Stage-1):

```
Without distributed optimizer:
  Each DP rank: full model params (FP32) + full Adam states (2 × FP32)
  Memory per rank: 16 bytes per parameter

With distributed optimizer:
  Each DP rank: 1/DP of model params (FP32) + 1/DP of Adam states
  Memory per rank: 16/DP bytes per parameter
  Communication: all-gather params before forward, reduce-scatter grads after backward
```

## 43.3 Activation Checkpointing

```
Full checkpointing:
  Save: only layer inputs
  Recompute: entire layer during backward
  Memory: O(num_layers × activation_size_per_layer)

Selective checkpointing:
  Save: expensive operations (attention output, dropout masks)
  Recompute: cheap operations (GeLU, layer norm)
  Memory: ~50% of full activations
  Speed: ~2-5% overhead (vs 30% for full checkpointing)
```

## 43.4 Typical Training Configuration

```bash
# GPT-175B on 1024 A100-80GB GPUs (128 nodes × 8 GPUs)
python pretrain_gpt.py \
    --tensor-model-parallel-size 8 \
    --pipeline-model-parallel-size 16 \
    --num-layers 96 \
    --hidden-size 12288 \
    --num-attention-heads 96 \
    --seq-length 2048 \
    --micro-batch-size 1 \
    --global-batch-size 1536 \
    --train-iters 100000 \
    --lr 6e-5 \
    --min-lr 6e-6 \
    --lr-decay-style cosine \
    --lr-warmup-iters 2000 \
    --weight-decay 0.1 \
    --adam-beta1 0.9 \
    --adam-beta2 0.95 \
    --clip-grad 1.0 \
    --bf16 \
    --use-distributed-optimizer \
    --sequence-parallel \
    --use-flash-attn \
    --recompute-activations
```

**Configuration math:**

```
Total GPUs = TP × PP × DP
1024      = 8  × 16 × 8

Micro-batches per pipeline = global_batch / (micro_batch × DP)
                           = 1536 / (1 × 8) = 192

Bubble fraction (1F1B) ≈ (16-1) / (16-1+192) ≈ 7.2%
```

## 43.5 Interview Questions

**Q1: Explain tensor parallelism in Megatron-LM.**

Megatron-LM splits weight matrices within each Transformer layer across GPUs. For the MLP, the first linear uses column-parallel (each GPU computes a portion of the output features) and the second uses row-parallel (each GPU computes with its portion and all-reduce sums the results). For attention, Q/K/V projections are column-parallel (each GPU handles a subset of heads) and the output projection is row-parallel. This requires only 2 all-reduces per Transformer layer (one for MLP, one for attention) in the forward pass, and 2 in the backward pass.

**Q2: What is the 1F1B pipeline schedule and why is it preferred over GPipe?**

1F1B (one-forward-one-backward) interleaves forward and backward passes for different micro-batches. After a warmup phase of P-1 forward passes, each device alternates between one forward and one backward pass. This has the same bubble fraction as GPipe but requires storing activations for only P micro-batches (instead of M for GPipe), dramatically reducing memory. Memory savings enable larger micro-batches or models.

**Q3: How does sequence parallelism reduce activation memory?**

In tensor parallelism, operations outside the TP region (LayerNorm, Dropout, residual connections) are replicated across all TP ranks, wasting memory. Sequence parallelism partitions the sequence dimension across TP ranks for these operations, reducing their activation memory by a factor of TP. The communication pattern changes from all-reduce to all-gather (before TP region) and reduce-scatter (after TP region), which has the same total bytes transferred.

**Q4: How do you determine the right TP/PP/DP configuration?**

General guidelines: (1) TP should not exceed GPUs per node (NVLink bandwidth >> inter-node bandwidth). (2) PP is added when TP alone can't fit the model. (3) DP fills the remaining GPUs: DP = total_GPUs / (TP × PP). (4) Increase micro-batches to minimize the pipeline bubble: bubble ≈ (PP-1)/(PP-1+M). (5) Use the distributed optimizer to reduce memory when DP > 1. (6) Enable sequence parallelism whenever TP > 1. (7) Use context parallelism for very long sequences (>32K tokens).

**Q5: What is context parallelism and when is it needed?**

Context parallelism splits the sequence dimension across GPUs specifically for the attention computation. Standard attention has O(N^2) memory and compute in sequence length N. For very long sequences (100K+ tokens), even with FlashAttention (which reduces memory to O(N)), the computation time becomes a bottleneck. Context parallelism distributes the workload: each GPU holds a chunk of Q and computes attention by receiving K, V chunks from other GPUs in a ring pattern. This reduces per-GPU compute and memory by a factor of CP (context parallelism degree).

---

# Part 8: Cross-Cutting Topics

---

# 44. Comprehensive Comparison Tables

---

## 44.1 Training Framework Comparison

| Feature | PyTorch | TensorFlow | JAX |
|---|---|---|---|
| Execution model | Eager (dynamic graph) | Eager + `tf.function` | Traced + JIT (XLA) |
| Paradigm | Object-oriented | Mixed (Keras + functional) | Functional |
| Auto-differentiation | `autograd` (reverse) | `GradientTape` (reverse) | `grad` (forward + reverse) |
| Compilation | `torch.compile` (Inductor) | XLA / `tf.function` | XLA (always) |
| Distributed | DDP, FSDP | `tf.distribute.Strategy` | `pmap`, `jit` + sharding |
| Mixed precision | `torch.amp` | `mixed_precision` policy | Native (bf16 default) |
| Research adoption | Dominant (~85%) | Declining | Growing (Google-internal) |
| Production | Growing | Mature | Emerging |
| TPU support | Via XLA bridge | Native | Native (primary target) |
| Mutability | Mutable tensors | Mutable Variables | Immutable arrays |
| Vectorization | Manual batching | Manual batching | `vmap` (automatic) |
| Random numbers | Global state | Global state | Explicit PRNG keys |

## 44.2 LLM Inference Engine Comparison

| Feature | vLLM | SGLang | TensorRT-LLM |
|---|---|---|---|
| KV cache management | PagedAttention | RadixAttention | Paged KV cache |
| Prefix caching | Opt-in | Automatic (radix tree) | Supported |
| Continuous batching | Yes | Yes | Yes (in-flight batching) |
| Constrained decoding | Limited | Built-in (regex, JSON) | Limited |
| Frontend DSL | No | Yes (gen, select, fork) | No |
| Speculative decoding | Yes | Yes | Yes |
| Quantization | GPTQ, AWQ, FP8 | GPTQ, AWQ, FP8 | INT8, INT4, FP8 |
| Tensor parallelism | Yes | Yes | Yes |
| Pipeline parallelism | Yes | Yes | Yes |
| Multi-LoRA | Yes | Yes | Limited |
| AMD GPU support | Yes (ROCm) | Yes (ROCm) | No (NVIDIA only) |
| API compatibility | OpenAI-compatible | OpenAI-compatible | Custom + Triton Server |
| Primary language | Python | Python | C++ |
| Ease of use | Easy | Easy | Complex (build process) |
| Community | Very large | Growing | NVIDIA-backed |

## 44.3 GPU Kernel Authoring Comparison

| Aspect | CUDA | Triton | HIP |
|---|---|---|---|
| Language | C/C++ | Python | C/C++ (CUDA-like) |
| Abstraction level | Thread-level | Block/tile-level | Thread-level |
| Shared memory | Manual | Automatic | Manual |
| Synchronization | Manual | Automatic | Manual |
| Vendor | NVIDIA only | NVIDIA + AMD | AMD (+ NVIDIA via HIP) |
| Performance ceiling | Highest | ~90-100% of CUDA | Near CUDA on AMD |
| Development speed | Slow | Fast | Moderate |
| Auto-tuning | Manual / CuTe | Built-in (`autotune`) | Manual |
| Integration | CUDA extensions | `torch.compile`, direct | HIP extensions |

## 44.4 Distributed Training Framework Comparison

| Feature | PyTorch DDP/FSDP | Megatron-LM | DeepSpeed |
|---|---|---|---|
| Data parallelism | DDP / FSDP | Yes | ZeRO Stage 1/2/3 |
| Tensor parallelism | Manual / via libs | Built-in (column/row) | Via Megatron integration |
| Pipeline parallelism | `PipelineStage` (new) | 1F1B, interleaved | PipelineModule |
| Sequence parallelism | Not built-in | Built-in | Not built-in |
| Context parallelism | Not built-in | Built-in (ring attention) | Ulysses/Ring |
| Mixed precision | `torch.amp` | BF16/FP16 native | FP16/BF16/FP8 |
| Activation checkpointing | `checkpoint()` | Selective/full | Partition-based |
| Optimizer sharding | FSDP | Distributed optimizer | ZeRO Stage 1/2/3 |
| Offloading | Not built-in | Not built-in | CPU/NVMe offload |
| Model scale | Medium (1-30B easy) | Large (100B+ designed for) | Large (supports offloading) |
| Ease of setup | Moderate | Complex | Moderate (config-based) |
| Ecosystem | PyTorch native | NVIDIA-specific | Microsoft, open-source |

## 44.5 Quantization Methods Comparison

| Method | Bits | Weights | Activations | Calibration | Quality | Speed |
|---|---|---|---|---|---|---|
| FP16 | 16 | Float | Float | None | Baseline | 2x FP32 |
| BF16 | 16 | Float | Float | None | ~FP16 | 2x FP32 |
| FP8 (E4M3) | 8 | Float | Float | Static/dynamic | Near FP16 | 2-4x FP16 |
| INT8 (W8A8) | 8 | Integer | Integer | Static | Good | 2x FP16 |
| GPTQ | 4 | Integer | FP16 | Calibration set | Good | 2-3x FP16 |
| AWQ | 4 | Integer | FP16 | Activation-aware | Better than GPTQ | 2-3x FP16 |
| INT4 (W4A16) | 4/16 | Integer | FP16 | Various | Model-dependent | 2-3x FP16 |
| GGML/GGUF | 2-8 | Mixed | Mixed | Various | Varies | CPU-friendly |

## 44.6 When to Use What

| Scenario | Recommended Stack |
|---|---|
| Research prototyping | PyTorch + HuggingFace |
| Production training (moderate scale) | PyTorch + DDP/FSDP |
| Large-scale training (100B+ params) | Megatron-LM or DeepSpeed + PyTorch |
| TPU training | JAX + Flax + Optax |
| Custom GPU kernels | Triton (or CUDA for peak performance) |
| LLM inference serving | vLLM or SGLang |
| Structured LLM programs | SGLang |
| Mobile/edge deployment | TFLite or ONNX Runtime |
| Multi-framework inference | ONNX Runtime |
| Scientific computing with AD | JAX |
| Long-context training (100K+ tokens) | Megatron-LM with context parallelism |
