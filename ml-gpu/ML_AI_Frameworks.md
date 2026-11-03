# ML and AI Frameworks -- Comprehensive Reference

> Last reviewed: 2026-11 · Versions assumed: PyTorch 2.8+, vLLM 0.10+, ROCm 6.4-7.x; section 8.8 checked with JAX 0.12, IREE 3.13, Apache TVM 0.27

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
45. [Training Memory Math: ZeRO, Activations, and Offload](#45-training-memory-math-zero-activations-and-offload)
46. [Mixture of Experts and Expert Parallelism](#46-mixture-of-experts-and-expert-parallelism)
47. [The ROCm ML Stack](#47-the-rocm-ml-stack)
48. [Debugging a Slow Training Step](#48-debugging-a-slow-training-step)

> Within Part 1, see also [8.6 torch.compile Internals](#86-torchcompile-internals-dynamo-aotautograd-inductor), [8.7 Number Formats and Mixed-Precision Numerics](#87-number-formats-and-mixed-precision-numerics), and [8.8 ML Compiler Stacks: MLIR, XLA, TVM, and IREE](#88-ml-compiler-stacks-mlir-xla-tvm-and-iree). For transformer fundamentals (attention, GQA, FLOP counting) see [LLM and ML Fundamentals](../ml-gpu/LLM_and_ML_Fundamentals.md); for interview-style system design (serving, training clusters) see [ML Systems Design](../ml-gpu/ML_Systems_Design.md).

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

Model-state memory per GPU, in BYTES, for P parameters, N GPUs,
mixed precision + Adam (FSDP keeps the sharded params in fp32 and casts
to bf16 for the all-gather; grads reduced in fp32):
  Sharded fp32 params:     4P / N
  Sharded fp32 grads:      4P / N
  Sharded Adam m and v:    8P / N
  Total sharded state:    16P / N bytes
  + transient unsharded bf16 params of the FSDP unit(s) being
    all-gathered (current + prefetched), + activations

DDP with AMP + Adam keeps all of it replicated: 16P bytes per GPU.
Example, P = 7e9, N = 8:  DDP 112 GB/GPU  vs  FSDP 14 GB/GPU (+ working set).
```

The 16 bytes/param figure is the same whether you count it as "fp32 params + fp32 grads + 8 B Adam" (PyTorch AMP/FSDP) or as "2 B bf16 weights + 2 B bf16 grads + 12 B fp32 master/m/v" (Megatron/DeepSpeed style). Section 45 works through the ZeRO-1/2/3 per-GPU formulas, activations, and offload: see [Training Memory Math](#45-training-memory-math-zero-activations-and-offload).

**FSDP2 (`fully_shard`).** FSDP1 (the `FullyShardedDataParallel` wrapper below) flattens each wrapped unit's parameters into one `FlatParameter`. FSDP2 is the replacement API. It shards each parameter individually as a `DTensor` on a `DeviceMesh`, so per-parameter dtypes, freezing (LoRA), and composition with tensor parallelism are much simpler. Its memory accounting is also more deterministic. FSDP2 is public as `torch.distributed.fsdp.fully_shard` from PyTorch 2.6.

```python
# fragment -- FSDP2 on a 1-D data-parallel mesh
from torch.distributed.device_mesh import init_device_mesh
from torch.distributed.fsdp import fully_shard, MixedPrecisionPolicy

mesh = init_device_mesh("cuda", (8,), mesh_dim_names=("dp",))   # "cuda" is also correct on ROCm
mp = MixedPrecisionPolicy(param_dtype=torch.bfloat16, reduce_dtype=torch.float32)
for block in model.layers:            # shard each transformer block = one all-gather unit
    fully_shard(block, mesh=mesh, mp_policy=mp)
fully_shard(model, mesh=mesh, mp_policy=mp)   # root: embeddings, final norm, head
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

For guards, graph breaks, recompiles, AOTAutograd, Inductor codegen, and the cases where compile hurts, see [8.6](#86-torchcompile-internals-dynamo-aotautograd-inductor).

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
| FP8 (H100, MI300X and later) | ~4x speedup | ~75% reduction | Requires careful tuning |

Section [8.7](#87-number-formats-and-mixed-precision-numerics) covers bit layouts (FP16/BF16/TF32/FP8/MX), FP8 scaling recipes, accumulation precision, and non-determinism.

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

For a full method for reading these traces (record_function, Perfetto, sync points, comm overlap, rocprofv3 correlation), see [48. Debugging a Slow Training Step](#48-debugging-a-slow-training-step).

## 8.6 `torch.compile` Internals: Dynamo, AOTAutograd, Inductor

```text
 Python function / nn.Module.forward
        │  PEP 523 frame-evaluation hook
        ▼
 TorchDynamo ── symbolically executes CPython bytecode
        │        - records torch ops into an FX graph
        │        - installs GUARDS (conditions under which the graph is valid)
        │        - on unsupported code: GRAPH BREAK (run that bit in Python,
        │          then resume tracing in a new graph)
        ▼
 FX graph (Torch IR, still Python-level ops)
        │
        ▼
 AOTAutograd ── traces forward AND backward ahead of time into a joint graph
        │        - functionalization (removes in-place mutation / aliasing)
        │        - decomposes to the core ATen op set
        │        - min-cut partitioner: chooses what to SAVE vs RECOMPUTE for backward
        ▼
 forward graph + backward graph (ATen IR)
        │
        ▼
 TorchInductor ── lowers to loop-level IR, schedules and FUSES
        │          pointwise/reduction ops, plans buffers
        │          - GPU: generates Triton kernels (CUDA and ROCm alike)
        │          - CPU: C++/OpenMP
        │          - GEMM/conv: "extern" calls to vendor BLAS (cuBLAS / hipBLASLt)
        │            unless max-autotune finds a faster Triton template
        ▼
 Compiled callable, cached per (code object, guard set)
```

### Guards and recompilation

Each compiled frame keeps a cache of `(guards -> compiled code)` entries. Guards check everything the trace assumed: tensor dtype, device, rank, sizes and strides (unless the dimension is dynamic), `requires_grad`, the values of Python scalars and constants, `nn.Module` identity and attributes, global flags, and grad mode. On every call the guards are evaluated. If no entry matches, Dynamo **recompiles**. After `torch._dynamo.config.recompile_limit` entries (default 8; the older name is `cache_size_limit`), that frame falls back to eager with a warning, and the speedup silently disappears.

**Dynamic shapes.** The first compile specializes on concrete sizes. When a size changes, the default `dynamic=None` ("automatic dynamic") recompiles once with that dimension as a symbolic `SymInt`. Later sizes reuse the dynamic graph. Sizes 0 and 1 are always specialized. For dimensions you know will vary (batch, sequence length), use `torch._dynamo.mark_dynamic(x, dim)` before the first call to skip the wasted static compile.

```python
# compile_demo.py -- run: TORCH_LOGS="graph_breaks,recompiles" python compile_demo.py
import torch
import torch._dynamo as dynamo

def f(x, scale):
    y = torch.sin(x) * scale
    if y.sum() > 0:           # data-dependent branch -> graph break
        y = y + 1
    print("side effect")      # print() -> graph break (Python side effect)
    return torch.relu(y)

# 1) Count graphs and graph breaks
explanation = dynamo.explain(f)(torch.ones(8), 2.0)   # sum > 0: branch taken
print(f"graphs={explanation.graph_count} breaks={explanation.graph_break_count}")
for reason in explanation.break_reasons:
    print("  break:", reason.reason.splitlines()[0])

# 2) Recompilation: guards on the Python float `s` and on shapes
g = torch.compile(lambda x, s: torch.sin(x) * s)
g(torch.randn(8), 2.0)
g(torch.randn(8), 3.0)     # guard "s == 2.0" fails -> recompile
g(torch.randn(16), 3.0)    # size guard fails -> recompile with dim 0 dynamic
g(torch.randn(32), 3.0)    # reuses the dynamic-shape graph: no recompile
print("done")
```

On recent PyTorch (checked on 2.15) this prints `graphs=3 breaks=2`. The count depends on which branch the data takes, which is why the input is fixed. The `recompiles` log names the failing guard each time (`s == 2.0`, then `tensor 'x' size mismatch at index 0. expected 8, actual 16`). The fix for the scalar case is to pass `s` as a 0-d tensor (or let Dynamo treat it as dynamic) rather than a Python float that keeps changing, for example a learning rate or a step counter.

### Diagnostics toolbox

| Tool | What it shows |
|---|---|
| `TORCH_LOGS="graph_breaks"` | Every graph break, with reason and user stack |
| `TORCH_LOGS="recompiles"` (or `recompiles_verbose`) | Which guard failed and caused each recompile |
| `TORCH_LOGS="guards"` | The full guard set of each compiled graph |
| `TORCH_LOGS="output_code"` | The generated Triton/C++ source |
| `TORCH_LOGS="aot_graphs"`, `"post_grad_graphs"` | Forward/backward graphs after AOTAutograd / Inductor passes |
| `TORCH_LOGS="perf_hints"` | Missed optimizations, e.g. CUDA graphs skipped and why |
| `TORCH_LOGS="+dynamo"` | Verbose Dynamo tracing (the `+` sets DEBUG level) |
| `torch._dynamo.explain(fn)(*args)` | Graph count, break count, and reasons, without a profiler |
| `TORCH_TRACE=/tmp/tr` then `tlparse /tmp/tr/*` | HTML report of every compile, break, and guard (tlparse is a separate pip package) |
| `torch.compile(..., fullgraph=True)` | Raise an error on any graph break (use in CI) |
| `torch.compiler.set_stance("fail_on_recompile")` | Raise an error instead of silently recompiling in steady state |
| `TORCHINDUCTOR_MAX_AUTOTUNE=1`, `TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS=TRITON,ATEN` | Control Inductor autotuning (also listed in AMD's MI300X tuning guide) |

### What fusion buys: a memory-traffic calculation

`y = gelu(x * w + b)` on N = 64M bf16 elements (`w` and `b` are broadcast vectors, so their traffic is negligible):

```text
Eager: 3 kernels, each reads 2N bytes and writes 2N bytes  -> 12N = 768 MB
Fused: 1 kernel, reads x once and writes y once              ->  4N = 256 MB
At ~5.3 TB/s HBM (MI300X peak): 145 us vs 48 us, plus 2 fewer kernel launches.
```

Pointwise and reduction chains are memory-bound (see [Roofline](../computer-science/Performance_Engineering.md#3-roofline-model)), so cutting the bytes moved is the speedup. AOTAutograd's partitioner adds a second, less obvious win: it can choose to **recompute** cheap pointwise ops in backward instead of saving their outputs, which lowers activation memory without any code change.

### CUDA/HIP graphs mode (`mode="reduce-overhead"`)

`reduce-overhead` records each compiled graph into a CUDA graph ("cudagraph trees"). On ROCm, `torch.cuda.CUDAGraph` is backed by HIP graphs, so the same mode works. A whole step's kernels then replay with one launch, which removes the per-op CPU dispatch and launch cost (a few µs to roughly 20 µs per op in eager PyTorch). That matters most for small batches and decode.

- **Requirements:** static shapes (one graph is recorded per distinct shape), no CPU-GPU sync inside the region, and no CPU tensors or data-dependent control flow. Inductor skips cudagraphs and says why under `TORCH_LOGS=perf_hints`.
- **Memory cost:** graphs own a private memory pool, and inputs are copied into static buffers. Peak memory rises.
- **Pitfall:** outputs live in the graph's pool and are overwritten by the next replay. Clone outputs you keep across iterations, or call `torch.compiler.cudagraph_mark_step_begin()` at each step boundary when the step structure is unusual.

### When `torch.compile` hurts

| Situation | Why | Mitigation |
|---|---|---|
| Short jobs, notebooks, many model variants | Compile takes seconds to minutes per graph and shape | Inductor/AOTAutograd caches (on by default; `TORCHINDUCTOR_CACHE_DIR`), regional compile (compile the repeated block, not the whole model) |
| Recompilation storms | Changing Python scalars, new shapes, mutated module attributes | `TORCH_LOGS=recompiles`, `mark_dynamic`, pass scalars as tensors |
| Many graph breaks | Small graphs lose fusion and pay per-graph guard and launch overhead | `fullgraph=True` to find them; `torch.cond`, branchless `torch.where`, custom ops |
| GEMM-dominated, already GPU-bound | GEMMs still go to vendor BLAS; there is little left to fuse | Measure first; try `max-autotune` only for GEMM-heavy inference |
| `reduce-overhead` with varying shapes | One graph per shape, so memory and capture time multiply | Pad or bucket shapes, or use `default` mode |
| Bit-exact comparisons against eager | Fusion keeps intermediates in fp32 registers and changes reduction order | Compare with tolerances (see 8.7) |

### Interview Questions

**Q1.** Your compiled training loop got slower after a refactor. `TORCH_LOGS=recompiles` shows dozens of recompiles of `forward`. What are the likely causes and fixes?

**A.** Each recompile means some guard failed. Common causes: (1) A Python scalar whose value changes every step (step counter, dropout probability, scheduler LR) is passed into the compiled region. Dynamo specializes on its value, so every new value is a new graph. Pass it as a tensor, or hoist it out of the compiled region. (2) Varying shapes, such as sequence length. After the first change Dynamo marks the dim dynamic, but sizes 0/1 or changes in other dims keep recompiling. Use `mark_dynamic`, or pad or bucket to a few lengths. (3) Module attributes mutated in `forward` (`self.counter += 1`) or switching between `train()` and `eval()`. (4) Hitting `recompile_limit` (8). After that the frame silently runs eagerly, which explains the slowdown. Confirm with `torch.compiler.set_stance("fail_on_recompile")` in a test.

**Q2.** What does AOTAutograd do that Dynamo alone doesn't?

**A.** Dynamo only sees the forward Python code. AOTAutograd traces the backward pass at compile time by running autograd on the captured forward with fake tensors. This produces a joint forward+backward graph. It then functionalizes the graph (no in-place mutation, so the compiler can reorder freely) and decomposes ops to a smaller core ATen set. A min-cut partitioner then splits the joint graph into forward and backward graphs and decides which intermediates to save and which to recompute. The backward pass becomes compilable and fusible too, and activation memory often drops because cheap pointwise results are recomputed instead of stored.

**Q3.** How does `torch.compile` work on AMD GPUs? What differs?

**A.** The frontend is identical, because Dynamo and AOTAutograd are device-agnostic. Inductor emits the same Triton source, and Triton's AMD backend compiles it to AMDGCN instead of PTX. Differences that matter: (1) a warp is a 64-lane wavefront on CDNA, so `num_warps=4` means 256 threads; (2) the autotuning space includes AMD-specific knobs (`waves_per_eu`, `matrix_instr_nonkdim`); (3) extern GEMMs go to hipBLASLt or rocBLAS, and TunableOp can tune them; (4) `reduce-overhead` uses HIP graphs. See [47.4](#474-triton-on-amd-backend-specifics).

**Q4.** When would you NOT enable `torch.compile`?

**A.** When compile time exceeds the time saved: short runs, or rapidly changing shapes such as variable-resolution images without bucketing. Also when the model is GEMM-bound and you measured no gain, and when you need bit-exact parity with eager. It is also the wrong first step when the step is not GPU-compute-bound at all, for example when the dataloader or communication is the bottleneck. Profile first (section 48).

---

## 8.7 Number Formats and Mixed-Precision Numerics

See [LLM and ML Fundamentals](../ml-gpu/LLM_and_ML_Fundamentals.md) for how these formats are used in quantized inference, and [CS Fundamentals](../computer-science/CS_Fundamentals.md) for IEEE 754 basics.

| Format | Sign/Exp/Mantissa bits | Max finite | Epsilon (2^-mantissa) | Notes |
|---|---|---|---|---|
| FP32 | 1/8/23 | 3.4e38 | 1.2e-7 | Master weights, optimizer state, accumulators |
| TF32 | 1/8/10 | ~3.4e38 | 9.8e-4 | A matrix-unit *math mode* for FP32 inputs, not a storage type |
| FP16 | 1/5/10 | 65504 | 9.8e-4 | Min normal 6.1e-5, so small gradients underflow and need loss scaling |
| BF16 | 1/8/7 | 3.39e38 | 7.8e-3 | FP32 range with coarse precision; no loss scaling needed |
| FP8 E4M3 (OCP "E4M3FN") | 1/4/3 | 448 | 0.125 | No infinities; forward pass (weights, activations) |
| FP8 E5M2 | 1/5/2 | 57344 | 0.25 | IEEE-like, has inf; used for gradients (needs range) |
| FP8 E4M3FNUZ / E5M2FNUZ | 1/4/3, 1/5/2 | 240 / 57344 | same | Exponent bias +1, no negative zero, single NaN (0x80). This is the FP8 on MI300 (gfx942) |
| FP4 E2M1 | 1/2/1 | 6 | -- | Representable magnitudes: 0, 0.5, 1, 1.5, 2, 3, 4, 6; only usable with block scales |
| MX formats (MXFP8/6/4) | elements + shared E8M0 scale per 32-element block | -- | -- | OCP Microscaling spec; hardware block scaling on MI350-series (CDNA4) and NVIDIA Blackwell |

PyTorch dtypes: `torch.float8_e4m3fn`, `torch.float8_e5m2`, `torch.float8_e4m3fnuz`, `torch.float8_e5m2fnuz`, `torch.float8_e8m0fnu` (MX scale), `torch.float4_e2m1fn_x2` (two FP4 values packed per byte).

**AMD FP8 pitfall.** An OCP E4M3FN checkpoint, the format most published FP8 models use, cannot be fed bit-for-bit to MI300 FP8 instructions. Because the exponent bias differs by one, the same bit pattern means half the value in FNUZ, and 0x80 (negative zero in OCP) is NaN in FNUZ. Loaders convert by remapping 0x80 to 0, reinterpreting the bits, and doubling the scale. vLLM does this on ROCm. MI350-series GPUs support OCP FP8 natively.

### FP8 scaling recipes

FP8 has only about 2 significant decimal digits and a narrow range, so every FP8 tensor carries a scale. The stored value is `q = cast_fp8(x * s)`, and it dequantizes as `x ≈ q / s`.

| Recipe | Scale chosen from | Trade-off |
|---|---|---|
| Per-tensor, dynamic ("current") | `amax(x)` of this tensor now: `s = fp8_max / amax` | Accurate, but needs an extra reduction pass over the tensor |
| Per-tensor, delayed | Max of an amax *history* from previous steps (NVIDIA Transformer Engine) | No extra pass; overflows if activations spike |
| Per-row / per-channel | amax per row of activations and per output channel of weights | Handles outlier channels; scales applied in the GEMM epilogue |
| Block-wise | amax per tile, e.g. 1x128 activation tiles and 128x128 weight blocks (DeepSeek-V3) | Robust to outliers; needs a block-scaled GEMM kernel |
| MX (microscaling) | Power-of-two E8M0 scale per 32 contiguous elements, applied in hardware | Fine granularity with little overhead; MXFP4/MXFP6 make FP4/FP6 training and inference viable |

A typical FP8 training recipe: E4M3 for weights and activations in forward, E5M2 (or E4M3 with finer scaling) for gradients. Master weights, optimizer state, softmax, normalization, loss, and the residual stream stay in BF16/FP32.

### Accumulation precision

Matrix units (AMD MFMA, NVIDIA Tensor Cores) take low-precision inputs and accumulate in FP32. This matters because adding a small number to a large BF16 running sum loses it entirely. In BF16 the spacing between representable values in [256, 512) is 2, so `256 + 1 == 256`. Summing 1000 ones sequentially in BF16 stalls at **256**. With FP32 accumulation it returns 1000. The same effect is why **FP32 master weights** are needed: with BF16 weights, an update `lr * grad` smaller than about `|w| * 2^-9` rounds away and that parameter stops learning. (DeepSeek-V3 also found the FP8 GEMM accumulator on H100 to be narrower than full FP32, and periodically promoted partial sums to FP32.)

### Non-determinism and compensated summation

Floating-point addition is not associative. In fp32, `(1e8 + -1e8) + 1 = 1` but `1e8 + (-1e8 + 1) = 0`. Run-to-run differences on GPUs come from anything that changes the **order** of additions:

- `atomicAdd`-based reductions (`index_add_`, `scatter_add_`, embedding backward), where arrival order varies.
- Split-K GEMMs, and tuned kernel selection. TunableOp, Inductor autotuning, and the hipBLASLt heuristics can pick a different kernel for the same shape on a different run or GPU.
- Collective algorithms: ring and tree all-reduce sum in different orders, and RCCL/NCCL choose between them by message size and topology.
- Different world sizes or micro-batch splits.

`torch.use_deterministic_algorithms(True)` makes PyTorch raise on known non-deterministic ops (or pick deterministic variants). It does not make results identical across different GPU models, library versions, or world sizes. Tests therefore compare with `torch.testing.assert_close` (dtype-aware rtol/atol), never `==`.

Compensated (Kahan) summation carries the rounding error forward:

```python
# kahan.py -- naive vs compensated summation in float32 (requires numpy)
import numpy as np

def naive_sum(xs):
    s = np.float32(0.0)
    for x in xs:
        s = np.float32(s + x)
    return s

def kahan_sum(xs):
    s = np.float32(0.0)
    c = np.float32(0.0)              # running compensation (lost low-order bits)
    for x in xs:
        y = np.float32(x - c)
        t = np.float32(s + y)
        c = np.float32((t - s) - y)  # what got rounded away when forming t
        s = t
    return s

xs = np.full(1_000_000, 0.1, dtype=np.float32)
exact = 1_000_000 * float(np.float32(0.1))   # true sum of the float32 inputs
naive, kahan, pairwise = naive_sum(xs), kahan_sum(xs), xs.sum()
print(f"naive   : {naive:.4f}  err={abs(naive - exact):.4f}")     # ~100958, err ~958
print(f"kahan   : {kahan:.4f}  err={abs(kahan - exact):.4f}")     # 100000.0000, err 0
print(f"pairwise: {pairwise:.4f}  err={abs(pairwise - exact):.4f}")  # np.sum, err ~0.008
```

GPU reductions are tree-shaped (pairwise), so their error grows like O(log n)·eps instead of O(n)·eps. That is one reason a GPU sum can be *more* accurate than a naive CPU loop, even though it is not bitwise reproducible.

### Interview Questions

**Q1.** Why two FP8 formats? Which goes where?

**A.** With 8 bits you trade range against precision. E4M3 has 3 mantissa bits (relative step 2^-3 = 12.5%) and range up to ±448. E5M2 has 2 mantissa bits and range up to ±57344. Forward tensors (weights, activations) have a bounded, well-understood range and benefit from precision, so they use E4M3. Gradients span many orders of magnitude across layers and steps, so they need range and use E5M2. Fine-grained scaling (block-wise or MX) narrows each block's range enough that some recipes use E4M3 everywhere.

**Q2.** Why does BF16 training not need a GradScaler, yet still keeps FP32 master weights?

**A.** These are two different problems. GradScaler addresses *range*: FP16's minimum normal of 6e-5 makes small gradients underflow, and BF16 has FP32's 8-bit exponent, so it doesn't underflow. Master weights address *precision*. BF16 has 8 significant bits, so `w + lr*g` with `|lr*g| < |w|·2^-9` rounds back to `w`. With typical LRs (1e-5 to 1e-4) and weights around 0.01-1, many updates are rounded away or heavily quantized, and that gets worse as LR decays late in training. The optimizer therefore updates an FP32 copy and casts it to BF16 for compute, at a cost of 4 extra bytes per parameter (see section 45).

**Q3.** Two identical training runs on the same 8 GPUs diverge in loss after a few thousand steps. Is that a bug?

**A.** Not necessarily. Atomics, split-K kernels, autotuned kernel choice, and collective reduction order all change summation order, which produces last-bit differences, and chaotic training dynamics amplify them over thousands of steps. To decide: (1) enable `torch.use_deterministic_algorithms(True)`, fix seeds, disable autotuning and TunableOp tuning, and use a fixed kernel table; (2) check that the step-0 loss and gradient norms match to tolerance; (3) bisect the step where they first diverge beyond fp rounding. A bug shows up as an early, large divergence. Rounding noise shows up as slow divergence with statistically equal final loss.

**Q4.** A customer's FP8 checkpoint produces garbage on MI300X but works on H100. What would you check first?

**A.** The FP8 variant. The checkpoint is almost certainly OCP E4M3FN (max 448), and MI300 computes in E4M3FNUZ (max 240, bias +1, 0x80 = NaN). The loader must convert the weights (map 0x80 to 0 and double the scales) or dequantize. Also check that any value above 240 after rescaling is clamped, and that activation scales computed on H100 are rescaled the same way.

---

## 8.8 ML Compiler Stacks: MLIR, XLA, TVM, and IREE

Section 8.6 covered one compiler, `torch.compile`, in depth. This section covers the other stacks that come up in ML-compiler, kernel, and accelerator interviews: MLIR (the infrastructure most new compilers are built on), XLA (JAX/TensorFlow), TVM (schedule search), and IREE (an MLIR-based compiler plus runtime that AMD contributes to heavily). It ends with fusion rules that apply to all of them.

See also: [Elementwise Fusion and Kernel Launch Overhead](GPU_Kernel_Case_Studies.md#7-elementwise-fusion-and-kernel-launch-overhead) (hand-fused HIP kernels with measurements), [Tiled GEMM Progression](GPU_Kernel_Case_Studies.md#6-tiled-gemm-progression) (the schedule a compiler has to find, written by hand), [Loop Interchange and Tiling for Matmul](../computer-science/Performance_Engineering.md#54-loop-interchange-and-tiling-for-matmul), [Roofline Model](../computer-science/Performance_Engineering.md#3-roofline-model), and [Triton Compilation Pipeline](#254-compilation-pipeline).

### The common shape of an ML compiler

```text
 Framework program (PyTorch, JAX, TensorFlow, ONNX)
      │  capture: tracing (JAX, tf.function), bytecode analysis (Dynamo), export
      ▼
 GRAPH IR        FX/ATen, HLO/StableHLO, Relax, MLIR torch/tosa dialects
      │  graph passes: decomposition, CSE, constant folding, layout assignment,
      │  SPMD partitioning, and FUSION (which ops share one kernel)
      ▼
 TENSOR/LOOP IR  Inductor loop IR, MLIR linalg, TVM TIR
      │  SCHEDULE: tile, reorder, vectorize, map loops to workgroups and waves,
      │  stage operands through LDS, software-pipeline, pick an MFMA shape
      │  <- autotuning searches over these choices
      ▼
 TARGET IR       LLVM IR + AMDGPU/NVPTX intrinsics, SPIR-V, Triton TTGIR
      ▼
 ISA + runtime   hsaco/cubin, host launch code, HIP/CUDA graphs, VM bytecode
```

Every stack makes two separate decisions:

1. **Fusion** (graph level): which ops become one kernel. This decides how many bytes go to and from HBM, so it dominates for memory-bound ops.
2. **Schedule** (kernel level): how the loop nest of one kernel maps onto the hardware. This decides how close a compute-bound kernel gets to peak FLOP/s.

GEMMs and convolutions often skip step 2 entirely. The compiler emits a call to a vendor library (hipBLASLt, rocBLAS, MIOpen, cuBLAS, cuDNN), and fusion is limited to whatever epilogue the library supports.

| Stack | Origin | Input | Graph IR | Kernel codegen | Tuning | Typical use |
|---|---|---|---|---|---|---|
| `torch.compile` / Inductor | PyTorch (Meta) | Python bytecode via Dynamo | FX graph of ATen ops | Triton (GPU), C++/OpenMP (CPU); extern GEMM calls | `max-autotune` benchmarks a list of Triton configs and GEMM backends | PyTorch training and inference, JIT in-process |
| XLA | Google, now OpenXLA | JAX, TensorFlow, PyTorch/XLA, via StableHLO | HLO | Own LLVM IR emitters; Triton for GEMM/softmax fusions on NVIDIA; library custom calls | Analytical cost model for fusion; GEMM autotuning | JAX, TPUs, large SPMD training |
| Apache TVM | UW research (2018) | ONNX, PyTorch, TF into Relax (formerly Relay) | Relax | TIR, lowered to LLVM, CUDA, ROCm, Vulkan, Metal | AutoTVM, Ansor, MetaSchedule search with learned cost models | Deployment to many hardware targets; MLC-LLM |
| IREE | Google origin; AMD (via Nod.ai) is a major contributor | StableHLO, TOSA, torch-mlir, ONNX | MLIR (`linalg`, `flow`, `stream`, `hal`) | MLIR codegen for LLVM-CPU, ROCm/HIP, CUDA, SPIR-V/Vulkan, Metal | Tuning specs written in the Transform dialect | Ahead-of-time deployment, from mobile to MI300X |
| Triton | OpenAI | `@triton.jit` Python | None (kernel-level only) | MLIR: `ttir` → `ttgir` → LLVM IR → AMDGCN/PTX | `triton.autotune` over a config list | Hand-written kernels; Inductor's GPU backend |
| MIGraphX | AMD | ONNX, Torch-MIGraphX | Own graph IR | Library calls (rocBLAS/hipBLASLt, MIOpen) plus generated kernels for fused ops | Optional exhaustive tuning | ONNX inference on AMD GPUs; ONNX Runtime execution provider |

### MLIR: dialects and progressive lowering

**What MLIR is.** MLIR is not a compiler for any particular language. It is LLVM-project infrastructure for *building* compilers: an SSA IR whose instruction set is extensible. Its building blocks:

- **Operation.** Everything is an op, including modules, functions, and loops. An op has a name `dialect.op`, SSA operands and results, compile-time **attributes**, and optional nested **regions** (blocks of ops). Regions are how a loop body or a GPU kernel body lives inside its parent op.
- **Dialect.** A namespace of ops, types, and attributes at one level of abstraction, for example `linalg`, `scf`, `gpu`, or `rocdl`. A single module can mix dialects freely.
- **Interfaces.** Ops declare capabilities such as `TilingInterface` or `DestinationStyleOpInterface`. A tiling pass written once against the interface then works for every op that implements it, from any dialect.
- **Passes and the conversion framework.** A pass rewrites the IR. A *conversion* declares target dialects legal and source dialects illegal, then applies rewrite patterns until no illegal op remains. Canonicalization and CSE run between passes.
- **Tools.** `mlir-opt` runs passes, `mlir-translate` exports the `llvm` dialect to real LLVM IR. Downstream projects ship their own drivers (`iree-opt`, `triton-opt`).

**Why not lower straight to LLVM IR?** LLVM IR has only scalars, vectors, loads, stores, and branches. Once a matmul becomes three loops with loads and stores, the fact that it was a matmul is gone, and recovering it ("raising") is fragile. Tiling for LDS, choosing an MFMA instruction, or fusing a bias add is easy while the IR still says "matmul" and hard afterwards. MLIR keeps each abstraction level as its own dialect and lowers one step at a time (**progressive lowering**). Each pass does one job at the level where that job is easy. Frontends and backends also share the middle dialects, so N frameworks and M targets need roughly N + M lowerings instead of N × M.

| Level | Dialects | What the IR holds |
|---|---|---|
| Framework / graph | `torch` (torch-mlir), `stablehlo`, `tosa`, `tt` (Triton) | Whole-tensor ops with framework semantics |
| Structured tensor ops | `linalg`, `tensor` | Ops described as loop nests by indexing maps; tiling and fusion happen here |
| Buffers | `memref`, `bufferization` | Memory with shapes, strides, and layouts; `tensor` to `memref` conversion |
| Loops and vectors | `scf`, `affine`, `vector` | Explicit loops and n-D vector ops |
| Parallel hardware | `gpu`, `amdgpu`, `nvgpu` | Kernel launches, workgroup/thread ids, barriers, MFMA/WMMA ops |
| Target | `llvm`, `rocdl`, `nvvm` | 1:1 with LLVM IR and target intrinsics; exported with `mlir-translate` |
| Cross-cutting | `arith`, `math`, `func`, `cf`, `transform` | Scalar math, functions, control flow, schedules written as IR |

A complete program in upstream dialects, `relu(x @ w + b)`. It compiles and runs with IREE (shown later), and `iree-opt`/`mlir-opt` can lower it pass by pass:

```text
// mlp.mlir -- y = relu(x @ w + b), written in upstream MLIR dialects
#map_bias = affine_map<(i, j) -> (j)>
#map_id   = affine_map<(i, j) -> (i, j)>
func.func @mlp(%x: tensor<4x8xf32>, %w: tensor<8x16xf32>,
               %b: tensor<16xf32>) -> tensor<4x16xf32> {
  %zero = arith.constant 0.0 : f32
  %empty = tensor.empty() : tensor<4x16xf32>
  %acc = linalg.fill ins(%zero : f32) outs(%empty : tensor<4x16xf32>) -> tensor<4x16xf32>
  %mm = linalg.matmul ins(%x, %w : tensor<4x8xf32>, tensor<8x16xf32>)
                      outs(%acc : tensor<4x16xf32>) -> tensor<4x16xf32>
  %y = linalg.generic
         {indexing_maps = [#map_id, #map_bias, #map_id],
          iterator_types = ["parallel", "parallel"]}
         ins(%mm, %b : tensor<4x16xf32>, tensor<16xf32>)
         outs(%empty : tensor<4x16xf32>) {
    ^bb0(%m: f32, %bias: f32, %out: f32):
      %s = arith.addf %m, %bias : f32
      %r = arith.maximumf %s, %zero : f32
      linalg.yield %r : f32
  } -> tensor<4x16xf32>
  return %y : tensor<4x16xf32>
}
```

Three ideas in this snippet carry most of MLIR-based codegen:

- **`linalg.generic` is a loop nest written as data.** The `indexing_maps` say which element of each operand iteration `(i, j)` touches (the bias map `(i, j) -> (j)` is a broadcast), and `iterator_types` mark each loop as parallel or reduction. From these alone, a pass knows the loop bounds, which loops it may parallelize, and exactly which slice of each operand a tile needs. That is why tiling, fusion, interchange, and vectorization can be written once for all ops.
- **Value semantics first, memory later.** `tensor` values are immutable SSA values, so rewrites cannot break aliasing. Buffers (`memref`) are introduced late by **bufferization**.
- **Destination-passing style.** `outs(...)` names where a result should go, which lets bufferization write in place instead of allocating.

Running `iree-opt mlp.mlir --one-shot-bufferize="bufferize-function-boundaries" --convert-linalg-to-loops --canonicalize` shows two lowering steps (abridged output):

```text
// fragment -- abridged output of the pass pipeline above
func.func @mlp(%arg0: memref<4x8xf32, strided<[?, ?], offset: ?>>, ...) -> memref<4x16xf32> {
  %alloc = memref.alloc() alignment = 64 : memref<4x16xf32>   // ONE buffer
  scf.for %i = %c0 to %c4 step %c1 {                           // linalg.fill
    scf.for %j = %c0 to %c16 step %c1 {
      memref.store %cst, %alloc[%i, %j] : memref<4x16xf32> } }
  scf.for %i = %c0 to %c4 step %c1 {                           // linalg.matmul
    scf.for %j = %c0 to %c16 step %c1 {
      scf.for %k = %c0 to %c8 step %c1 {
        %a = memref.load %arg0[%i, %k] ...
        %b = memref.load %arg1[%k, %j] ...
        %c = memref.load %alloc[%i, %j] ...
        %p = arith.mulf %a, %b : f32
        %s = arith.addf %c, %p : f32
        memref.store %s, %alloc[%i, %j] : memref<4x16xf32> } } }
  scf.for %i ... { scf.for %j ... {                            // bias + relu, IN PLACE
        %v = memref.load %alloc[%i, %j] ...
        ...  arith.addf, arith.maximumf ...
        memref.store %r, %alloc[%i, %j] : memref<4x16xf32> } }
  return %alloc : memref<4x16xf32>
}
```

The bias+relu `generic` had `outs(%empty)`, but bufferization saw that `%mm` is dead after it and reused the matmul's buffer. Only one 4×16 allocation remains. The output also shows why fusion must happen *before* this point: after lowering to `scf` loops, the three loop nests are just loads and stores.

**Schedules as IR: the Transform dialect.** A *transform script* is MLIR that manipulates other MLIR. It plays the role of a TVM schedule (below), and IREE accepts tuning specs in this form. This script tiles a 128×256×64 matmul into 32×16 output tiles (one per workgroup) with a sequential K loop of step 8:

```text
// tile.mlir -- run: iree-opt tile.mlir --transform-interpreter --canonicalize
func.func @matmul(%a: tensor<128x256xf32>, %b: tensor<256x64xf32>,
                  %c: tensor<128x64xf32>) -> tensor<128x64xf32> {
  %r = linalg.matmul ins(%a, %b : tensor<128x256xf32>, tensor<256x64xf32>)
                     outs(%c : tensor<128x64xf32>) -> tensor<128x64xf32>
  return %r : tensor<128x64xf32>
}

module attributes {transform.with_named_sequence} {
  transform.named_sequence @__transform_main(%root: !transform.any_op {transform.readonly}) {
    %mm = transform.structured.match ops{["linalg.matmul"]} in %root
        : (!transform.any_op) -> !transform.any_op
    // Tile M and N by 32x16 into an scf.forall (one tile per workgroup / thread)
    %tiled, %forall = transform.structured.tile_using_forall %mm tile_sizes [32, 16]
        : (!transform.any_op) -> (!transform.any_op, !transform.any_op)
    // Inside each tile, tile K by 8 with a sequential scf.for (the reduction loop)
    %tiled2, %kloop = transform.structured.tile_using_for %tiled tile_sizes [0, 0, 8]
        : (!transform.any_op) -> (!transform.any_op, !transform.any_op)
    transform.yield
  }
}
```

The result is an `scf.forall (%i, %j) in (4, 4)` whose body extracts a 32×256 slice of A and a 256×16 slice of B, then runs `scf.for %k = 0 to 256 step 8` around a 32×8 by 8×16 `linalg.matmul`. That is the same structure as the hand-written LDS-tiled GEMM, produced by a 3-line schedule. Changing `[32, 16]` to `[64, 64]` is a one-token change. That is what makes schedules searchable.

**Triton is an MLIR compiler too.** Its stages, as cached under `~/.triton/cache`, are `.ttir` (`tt` dialect: block-level `tt.load`, `tt.dot`), `.ttgir` (`ttg` dialect: the same ops annotated with **layout encodings** such as `#blocked`, `#ttg.amd_mfma`, `#ttg.nvidia_mma`, and `#ttg.shared`, which say which thread holds which element), `.llir` (LLVM IR, via the `llvm` and `rocdl`/`nvvm` dialects), and finally `.amdgcn` + `.hsaco` on AMD or `.ptx` + `.cubin` on NVIDIA. "Triton IR" and TTIR in the [25.4 diagram](#254-compilation-pipeline) are the same `tt` dialect. The interesting AMD passes run on TTGIR: converting `tt.dot` to MFMA layouts, stream pipelining through LDS, and instruction scheduling hints. `MLIR_ENABLE_DUMP=1` prints the IR after every pass (see [47.4](#474-triton-on-amd-backend-specifics)).

### XLA: HLO, StableHLO, and fusion

**HLO** (High Level Operations) is XLA's graph IR: about 100 coarse ops (`dot`, `convolution`, `reduce`, `broadcast`, `while`, `conditional`, `all-reduce`, ...). It is purely functional, its shapes are **static**, and each array carries an explicit layout (`f32[1024,4096]{1,0}` means dimension 1 is minor, i.e. row-major). Control flow and collectives are ops in the graph, so XLA sees and schedules the whole program, including communication.

**StableHLO** is the portable, versioned MLIR dialect in front of XLA, with backward-compatibility guarantees for serialized programs. JAX emits StableHLO. PyTorch/XLA and torch-mlir can produce it, and both XLA and IREE consume it.

The XLA:GPU pipeline, in order:

1. **SPMD partitioning** (GSPMD, or the newer Shardy propagation): sharding annotations are propagated, and the compiler inserts the collectives. This is how `jax.jit` with `NamedSharding` works (section 20).
2. **Simplification**: algebraic simplifier, CSE, constant folding, and layout assignment.
3. **GEMM handling**: `dot` ops are rewritten into library custom calls (cuBLASLt on NVIDIA, hipBLASLt/rocBLAS on ROCm), absorbing bias and activation epilogues where the library supports them. On NVIDIA, many GEMM fusions go to Triton instead, and XLA autotunes the choice.
4. **Fusion**: **priority fusion**. For each producer, an analytical cost model estimates run time with the producer duplicated and fused into *all* of its consumers versus unfused. The estimate is max(compute time, memory time) plus launch overhead. The most beneficial fusions are applied first, and producers with negative benefit are left alone. Then **multi-output fusion** merges siblings that read the same input, and a producer whose result is also needed elsewhere. **Horizontal fusion** batches many small independent ops into one launch.
5. **Scheduling**: the latency-hiding scheduler orders ops so asynchronous collectives overlap with compute.
6. **Buffer assignment**: whole-program liveness analysis assigns and reuses buffers. Peak memory is known at compile time.
7. **Codegen**: XLA emits LLVM IR directly for loop, reduction, and transpose fusions and compiles it with the LLVM NVPTX or AMDGPU backend. It uses Triton for GEMM and softmax-style fusions on NVIDIA and calls libraries for the rest. ROCm builds use hipBLASLt/rocBLAS, MIOpen, and RCCL in the corresponding places.

Fusion kinds you will see in dumps: `kLoop` (elementwise, iterating over the output shape), `kInput` (reduction-rooted, iterating over the reduction's input), `kOutput`, and `kCustom` (Triton GEMM fusions and library fusions).

**Worked example.** One GELU layer plus a row sum, inspected without a GPU:

```python
# jax_hlo.py -- run: XLA_FLAGS="--xla_dump_to=/tmp/xla --xla_dump_hlo_as_text" python jax_hlo.py
import jax
import jax.numpy as jnp

def f(x, w, b):
    y = jax.nn.gelu(x * w + b, approximate=True)
    return y, jnp.sum(y, axis=-1)

x = jnp.ones((1024, 4096), jnp.float32)
w = jnp.ones((4096,), jnp.float32)
b = jnp.zeros((4096,), jnp.float32)

lowered = jax.jit(f).lower(x, w, b)
print(lowered.as_text())             # StableHLO: what JAX hands to XLA
print(lowered.compile().as_text())   # optimized HLO: after fusion, layouts, buffers
```

The StableHLO has 11 full-size elementwise ops (`multiply`, `add`, the tanh-GELU polynomial, `tanh`) plus a `reduce`. The optimized HLO (checked with JAX 0.12 on CPU) collapses all 11 into one `kLoop` fusion, with the reduction in a second fusion:

```text
// fragment -- abridged optimized HLO
%multiply_multiply_fusion = f32[1024,4096]{1,0} fusion(%b.1, %x.1, %w.1),
    kind=kLoop, calls=%fused_computation.1, metadata={op_name="jit(f)/mul" ...}
%ynn_fusion = f32[1024]{0} fusion(%multiply_multiply_fusion), kind=kCustom, ...
ROOT %tuple.1 = (f32[1024,4096]{1,0}, f32[1024]{0}) tuple(...)
```

Each 1024×4096 f32 tensor is 16 MiB. Run unfused, the 11 elementwise ops read 14 full-size operands and write 11 results: 25 × 16 MiB = 400 MiB of traffic. The fused loop reads `x` once and writes `y` once (32 MiB), which is 12.5× less. The reduction then reads `y` again (16 MiB). On GPU, multi-output fusion can produce `y` and the row sums from one kernel and save that re-read. The `metadata={op_name=...}` on every fused instruction is how a profiler maps a kernel back to user code. The `--xla_dump_to` directory holds `*.before_optimizations.txt` and `*.<platform>_after_optimizations.txt` (for example `gpu_after_optimizations.txt`) for every compiled module.

**Static shapes are the price.** `jax.jit` caches one executable per (shapes, dtypes, static arguments). A new sequence length means a retrace and a full XLA compile. The standard fix is to pad or bucket inputs to a few sizes (for example powers of two) and mask the padding. Inductor took the opposite approach with symbolic `SymInt` sizes (section 8.6).

**XLA vs Inductor:**

| Aspect | XLA | TorchInductor |
|---|---|---|
| Capture | Trace a pure function; Python control flow runs at trace time | Dynamo bytecode analysis with guards; unsupported code causes graph breaks |
| Graph IR | HLO: about 100 coarse ops, static shapes, explicit layouts | FX graph of core ATen ops, then Inductor's loop-level IR |
| Dynamic shapes | Static; each new shape is a new compile | Symbolic sizes ("automatic dynamic" after the first change) |
| Fusion decision | Priority fusion driven by an analytical cost model, plus multi-output and horizontal fusion | Greedy scheduler: scores node pairs by memory traffic saved, checks loop compatibility; vertical and horizontal fusion; epilogue fusion into Triton GEMM templates under `max-autotune` |
| Kernel codegen | LLVM IR emitters, Triton (GEMM/softmax fusions on NVIDIA), library custom calls | Triton source (GPU), C++/OpenMP (CPU), extern library GEMMs |
| Control flow | First-class `while`/`conditional` ops (`lax.scan`, `lax.cond`) | `torch.cond`/`while_loop` higher-order ops; otherwise graph breaks or unrolling |
| Distribution | Inside the compiler: SPMD partitioner inserts collectives, scheduler overlaps them | Mostly outside: DDP/FSDP2/DTensor; compiled functional collectives |
| Memory planning | Whole-program buffer assignment; donated inputs | Buffer reuse within each graph; caching allocator between graphs |
| Fallback | None: the whole function must be traceable | Falls back to eager at graph breaks and after `recompile_limit` |
| Inspect | `XLA_FLAGS=--xla_dump_to=...`, `lowered.as_text()` | `TORCH_LOGS=output_code`, `tlparse` |
| Kernel names in a trace | Named after the fusion, such as `loop_multiply_fusion`, `input_reduce_fusion`, `triton_gemm_dot.6` (names vary by version) | `triton_poi_fused_*` (pointwise), `triton_red_fused_*` (reduction), `triton_per_fused_*` (persistent reduction), `triton_tem_fused_*` (template GEMM) |

The practical consequence: XLA rewards programs written as one big static, functional graph and gives you whole-program optimization, including communication. Inductor accepts arbitrary PyTorch and optimizes whatever it can capture, at the cost of guards, graph breaks, and recompiles.

### TVM: separating the algorithm from the schedule, then searching

TVM borrowed Halide's central idea: the **algorithm** (what to compute) is written once, and the **schedule** (loop order, tiling, parallel mapping, memory staging) is a separate program of transformations that cannot change the result. Relax (formerly Relay) is the graph IR, and TIR is the loop-level IR that schedules transform.

| Schedule primitive | Effect | GPU/CPU meaning |
|---|---|---|
| `split(loop, factors)` | One loop becomes several nested loops | Creates tile levels |
| `reorder(...)` | Permutes loops | Puts the unit-stride loop innermost; the tile loops outermost |
| `fuse(l1, l2)` | Merges two loops into one | Flattens before binding to a 1-D grid |
| `parallel` / `bind(loop, "blockIdx.x")` | Maps a loop to threads | CPU threads; GPU workgroups and threads |
| `vectorize`, `unroll` | Inner-loop code shape | SIMD lanes; ILP |
| `cache_read` / `cache_write` | Stages a tile in a faster scope | LDS (`shared`) or registers (`local`) |
| `compute_at` / `reverse_compute_at` | Moves a producer inside a consumer's loop | Loop-level fusion |
| `decompose_reduction`, `rfactor` | Splits init from update; parallelizes a reduction | Hoists `C = 0`; splits K across threads |
| `tensorize` | Replaces an inner loop nest with a hardware intrinsic | MFMA / Tensor Core / VNNI instructions |

The script below writes a 1024³ matmul once, then builds it with the default schedule and with a hand-written one. It is verified with `apache-tvm` 0.27 on CPU. TVM's Python API changes between releases: older versions spell these `tvm.tir.Schedule`, `sch.get_block`, and `tvm.nd.array`, and accept target strings like `"llvm -mcpu=..."`, which 0.27 rejects in favor of a JSON-style dict.

```python
# tvm_sched.py -- algorithm vs schedule (apache-tvm 0.27, CPU/LLVM, requires numpy)
import time
import numpy as np
import tvm
from tvm import te, s_tir

M = N = K = 1024
# ---- Algorithm: WHAT to compute (no loop order, no tiling) ----
A = te.placeholder((M, K), "float32", name="A")
B = te.placeholder((K, N), "float32", name="B")
k = te.reduce_axis((0, K), name="k")
C = te.compute((M, N), lambda i, j: te.sum(A[i, k] * B[k, j], axis=k), name="C")
func = te.create_prim_func([A, B, C])

def build(mod):
    return tvm.compile(mod, target="llvm")

def bench(lib):
    dev = tvm.cpu()
    a = tvm.runtime.tensor(np.random.rand(M, K).astype("float32"), dev)
    b = tvm.runtime.tensor(np.random.rand(K, N).astype("float32"), dev)
    c = tvm.runtime.tensor(np.zeros((M, N), "float32"), dev)
    lib(a, b, c)  # warm-up
    t0 = time.perf_counter(); lib(a, b, c); dt = time.perf_counter() - t0
    np.testing.assert_allclose(c.numpy(), a.numpy() @ b.numpy(), rtol=1e-3)
    return dt

# ---- Schedule 1: default loop nest (i, j, k) ----
naive = build(tvm.IRModule({"main": func}))

# ---- Schedule 2: HOW to compute it -- tile, reorder, vectorize, parallelize ----
sch = s_tir.Schedule(func)
blk = sch.get_sblock("C")
i, j, kk = sch.get_loops(blk)
io, ii = sch.split(i, factors=[None, 32])
jo, ji = sch.split(j, factors=[None, 64])
ko, ki = sch.split(kk, factors=[None, 4])
sch.reorder(io, jo, ko, ii, ki, ji)   # ji innermost: unit stride in B and C
sch.parallel(io)
sch.vectorize(ji)
sch.decompose_reduction(blk, ko)      # hoist C = 0 out of the k loop
tuned = build(sch.mod)

print(f"naive: {bench(naive)*1e3:8.1f} ms")
print(f"tiled: {bench(tuned)*1e3:8.1f} ms")
print(sch.mod.script())               # the transformed TIR
```

On a 96-core EPYC 9655 this printed `naive: 4822 ms` and `tiled: 3.2 ms`. The 1500× combines three effects: parallelizing the outer loop over cores, vectorizing the inner loop, and the reorder. The default `(i, j, k)` order walks `B` down a column with a 4 KiB stride, so nearly every access misses cache. The numerical result is identical. Only the schedule changed.

**Why schedules must be searched.** Count the tilings of one 1024³ GEMM in Ansor's GPU tile structure, which splits each spatial loop into 5 levels and the reduction loop into 3:

```python
# space.py -- size of a TVM/Ansor-style tiling search space for one GEMM
from math import comb

def splits(n, parts):
    """Ordered factorizations of n into `parts` factors (n a power of two)."""
    e = n.bit_length() - 1                    # n = 2**e
    return comb(e + parts - 1, parts - 1)     # stars and bars over the exponent

M = N = K = 1024
# GPU multi-level tiling "SSSRRSRS": spatial loops split 5 ways, reduction 3 ways
spatial = splits(M, 5) * splits(N, 5)
reduction = splits(K, 3)
unroll_choices = 4                            # e.g. auto_unroll_max_step in {0,16,64,512}
total = spatial * reduction * unroll_choices
print(f"spatial={spatial:,} reduction={reduction} total~{total:,}")
print(f"at 0.5 s per measured trial: {total*0.5/86400/365:.1f} years")
```

Output: `spatial=1,002,001 reduction=66 total~264,528,264` and `4.2 years`. That is for a single shape, before counting vectorization, LDS staging, and thread-binding choices. Exhaustive measurement is out of the question, which explains the design of TVM's three tuners:

| Tuner | Search space comes from | Search strategy | Weakness |
|---|---|---|---|
| **AutoTVM** (2018) | A human-written schedule **template** with knobs (`cfg.define_split(...)`) | Simulated annealing guided by a gradient-boosted-tree (XGBoost) cost model trained online on measured configs | Template quality caps performance; one template per op and target |
| **Ansor** (`auto_scheduler`, OSDI 2020) | Generated automatically: **sketches** from derivation rules (multi-level tiling `SSRSRS` on CPU / `SSSRRSRS` on GPU, inline elementwise ops, fuse consumers into tiles, add cache stages, `rfactor`), then **random annotation** of tile sizes, unroll, vectorize, and parallel | Evolutionary search (mutate tile sizes and annotations, crossover) scored by a learned cost model on program features; measure the top candidates on hardware; retrain; a **task scheduler** spends trials on the subgraphs that matter most for end-to-end latency | Hours of tuning per model; rules cannot invent new algorithms such as FlashAttention |
| **MetaSchedule** (TVM Unity, 2022) | A schedule written as a **probabilistic program**: ordinary primitives plus sampling instructions (`sample_perfect_tile`, `sample_categorical`) | Same evolutionary search and cost model; the sampled decisions form a replayable **trace** | Same cost; unifies hand-written and automatic schedules in one API |

Why the learned cost model: measuring one candidate costs about 0.1-1 s (compile, copy, warm-up, repeated timing), while the model scores thousands of candidates per second. Only the model's top-k are measured, and each measurement becomes new training data. A typical run is 1,000-20,000 measured trials per model. The results go to a tuning log keyed by (op, shape, dtype, target) and are reused at build time.

Common pitfalls: tuned schedules are shape-specific (decode with batch 1 vs prefill with 4096 tokens need different tiles), so a dynamic-shape model needs bucketing or a fallback. GPU clocks boost and throttle, so use repeated runs with min or median. Tuning runs each kernel with a hot cache, which can mislead for kernels that run once per step in a real model. A schedule tuned on one GPU SKU (MI300X) may not be best on another (MI325X or MI355X).

`triton.autotune`, Inductor's `max-autotune`, and PyTorch TunableOp (section 47.3) use the same measure-and-pick idea with no cost model. They work from a short hand-curated list (tens of configs) or a library's prebuilt solution list, which is why they finish in seconds to minutes. The core loop of any autotuner fits in a page of C++:

```cpp
// mini_autotune.cpp -- measure-driven search over one schedule knob (tile sizes)
// Build: g++ -O3 -march=native -std=c++17 mini_autotune.cpp -o mini_autotune
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <random>
#include <vector>

constexpr int N = 512;  // C[N][N] += A[N][N] * B[N][N], row-major

// The ALGORITHM is fixed; (TI, TJ, TK) is the SCHEDULE.
void matmul_tiled(const float* A, const float* B, float* C, int TI, int TJ, int TK) {
    std::fill(C, C + N * N, 0.0f);
    for (int i0 = 0; i0 < N; i0 += TI)
        for (int k0 = 0; k0 < N; k0 += TK)
            for (int j0 = 0; j0 < N; j0 += TJ)
                for (int i = i0; i < std::min(i0 + TI, N); ++i)
                    for (int k = k0; k < std::min(k0 + TK, N); ++k) {
                        const float a = A[i * N + k];
                        for (int j = j0; j < std::min(j0 + TJ, N); ++j)  // unit stride: vectorizable
                            C[i * N + j] += a * B[k * N + j];
                    }
}

struct Config { int ti, tj, tk; double ms; };

int main() {
    std::vector<float> A(N * N), B(N * N), C(N * N), ref(N * N, 0.0f);
    std::mt19937 rng(42);
    std::uniform_real_distribution<float> dist(-1.0f, 1.0f);
    for (auto& x : A) x = dist(rng);
    for (auto& x : B) x = dist(rng);
    for (int i = 0; i < N; ++i)                       // reference, plain i-k-j order
        for (int k = 0; k < N; ++k)
            for (int j = 0; j < N; ++j) ref[i * N + j] += A[i * N + k] * B[k * N + j];

    const int tiles[] = {8, 16, 32, 64, 128, 256, 512};
    std::vector<Config> results;
    for (int ti : tiles) for (int tj : tiles) for (int tk : tiles) {
        double best = 1e30;
        for (int rep = 0; rep < 3; ++rep) {           // best of 3 runs damps noise
            auto t0 = std::chrono::steady_clock::now();
            matmul_tiled(A.data(), B.data(), C.data(), ti, tj, tk);
            auto t1 = std::chrono::steady_clock::now();
            best = std::min(best, std::chrono::duration<double, std::milli>(t1 - t0).count());
        }
        for (int idx = 0; idx < N * N; ++idx)         // every candidate must be correct
            if (std::fabs(C[idx] - ref[idx]) > 1e-3f) { std::printf("WRONG\n"); return 1; }
        results.push_back({ti, tj, tk, best});
    }
    std::sort(results.begin(), results.end(),
              [](const Config& a, const Config& b) { return a.ms < b.ms; });
    const double gflop = 2.0 * N * N * N / 1e9;
    std::printf("%zu configs measured\n", results.size());
    for (int r = 0; r < 3; ++r)
        std::printf("best #%d: TI=%3d TJ=%3d TK=%3d  %6.2f ms  %5.1f GFLOP/s\n", r + 1,
                    results[r].ti, results[r].tj, results[r].tk, results[r].ms, gflop / results[r].ms * 1e3);
    const Config& w = results.back();
    std::printf("worst  : TI=%3d TJ=%3d TK=%3d  %6.2f ms  (%.1fx slower than best)\n",
                w.ti, w.tj, w.tk, w.ms, w.ms / results[0].ms);
}
```

On one EPYC 9655 core it measured 343 configs. The best was about 5.4 ms (49 GFLOP/s, with several configs within 1%), and the worst (`TI=8 TJ=8 TK=512`) was 9.3× slower. Both shapes are typical: the optimum is a flat plateau with many near-ties, and a bad schedule is an order of magnitude off. The rest of a real tuner is engineering around this loop: a cost model to prune, timeouts for configs that hang, isolating measurements from each other, and a persistent cache of results.

### IREE: a whole-program MLIR compiler and runtime

IREE compiles the **whole program**, including the host-side code that allocates buffers and schedules kernels, ahead of time into one deployable module. It runs that module with a small C runtime. Compare `torch.compile`, which only compiles kernels and graphs inside a live Python process.

- **Inputs:** StableHLO (JAX), TOSA (TFLite), torch-mlir (PyTorch via `iree-turbine`), ONNX (`iree-import-onnx`).
- **Output:** a `.vmfb` FlatBuffer holding VM bytecode for the host program and the compiled kernels for each target.
- **Runtime HAL drivers:** `local-sync`, `local-task` (CPU), `hip`, `cuda`, `vulkan` (plus `metal` on Apple platforms).

The compiler's phases are the values of `iree-compile --compile-to=`: `input` → `abi` → `preprocessing` → `global-optimization` → `dispatch-creation` → `flow` → `stream` → `executable-sources` → `executable-configurations` → `executable-targets` → `hal` → `vm` → `end`. The important ones:

| Phase / dialect | Job |
|---|---|
| Global optimization | Whole-program rewrites: constant hoisting, propagating transposes and layouts across ops, data-tiling encodings |
| Dispatch creation / `flow` | **Fusion.** Groups a root op (matmul, conv, reduction) with its elementwise producers and consumers into one dispatch region, which becomes one kernel |
| `stream` | Asynchronous execution: partitions dispatches into command buffers, plans buffer lifetimes and allocation, and inserts timepoints (fences) |
| `hal` | Per-target executables. Codegen (MLIR all the way down) picks a strategy per dispatch, then tiles to workgroups and subgroups, promotes to LDS, vectorizes, and maps to MFMA |
| `vm` | Lowers the host program to a compact bytecode, or to C via EmitC |

The `mlp.mlir` program from the MLIR section, compiled and run with the pip packages `iree-base-compiler` and `iree-base-runtime` (3.13):

```bash
# CPU: compile and run (x = 1, w = 0.5, b = -3  ->  relu(8*0.5 - 3) = 1 everywhere)
iree-compile mlp.mlir --iree-hal-target-device=local \
  --iree-hal-local-target-device-backends=llvm-cpu --iree-llvmcpu-target-cpu=host -o mlp.vmfb
iree-run-module --module=mlp.vmfb --device=local-task --function=mlp \
  --input="4x8xf32=1" --input="8x16xf32=0.5" --input="16xf32=-3"
# -> result[0]: hal.buffer_view  4x16xf32=[1 1 1 ... 1]...

# See the fusion decision: stop after dispatch formation
iree-compile mlp.mlir --iree-hal-target-device=local \
  --iree-hal-local-target-device-backends=llvm-cpu --compile-to=flow

# AMD GPU (MI300X = gfx942); compiling needs no GPU, running does
iree-compile mlp.mlir --iree-hal-target-device=hip --iree-rocm-target=gfx942 -o mlp_hip.vmfb
iree-run-module --module=mlp_hip.vmfb --device=hip --function=mlp --input=...
```

The `--compile-to=flow` output contains exactly one `flow.executable` named `@mlp_dispatch_0_matmul_4x16x8_f32`, and its body holds the `linalg.fill`, the `linalg.matmul`, and the bias+relu `linalg.generic`. The matmul is the root, and the epilogue was fused into the same kernel. Dispatch names encode the root op and its shape, which helps when you read a `rocprofv3` kernel trace of an IREE program.

For a 1024×1024 f16 matmul targeting gfx942, `--compile-to=executable-configurations` shows the strategy IREE chose: `pipeline = #iree_gpu.pipeline<TileAndFuse>`, `mma_kind = #iree_gpu.mma_layout<MFMA_F32_16x16x16_F16>`, `workgroup_size = [256, 1, 1]`, `subgroup_size = 64`. `--iree-hal-dump-executable-files-to=DIR` writes the intermediate `.ll`, the `.hsaco`, and a `.rocmasm` disassembly; that one contained 128 `v_mfma` instructions. Flag spellings have moved between releases (some earlier 3.x versions used `--iree-hip-target`), so check `iree-compile --help` against your version.

When to choose IREE over `torch.compile`: you need deployment without Python, one compiler for several targets (CPU, AMD/NVIDIA GPUs, Vulkan on mobile), or whole-program memory planning. It is also AMD's own MLIR-based path (the SHARK / shark-ai stack). The costs: the whole model must be captured (there are no graph breaks to fall back on), and op coverage and performance depend on the import path. Dynamic dimensions are supported in the types (`tensor<?x4096xf16>`).

### Fusion rules every ML compiler applies

| Fusion | Example | Legal? | Profitable? |
|---|---|---|---|
| Vertical elementwise | `gelu(x*w + b)` | Always (same iteration space) | Almost always: removes a full HBM round trip per intermediate |
| Reduction + producers | `sum(exp(x))` | Yes, the producer becomes the reduction's prologue | Yes |
| Reduction + consumers | softmax: `exp(x - max) / sum(...)` | Needs the reduction result first. One kernel if a row fits in one workgroup (Inductor's "persistent reduction", XLA reduction emitters); otherwise multi-pass or an online algorithm | Yes when the row fits |
| GEMM epilogue | bias, activation, residual add, output cast | Yes: applied to the accumulator tile before the store | Yes; supported by hipBLASLt epilogues, Triton templates, and XLA's GEMM rewriter |
| GEMM prologue | dequantize or cast weights on load | Yes, but each A element is reloaded once per N-tile | Only if the prologue is cheap (see below) |
| GEMM → GEMM | attention: `softmax(QKᵀ) V` | Not by generic rules. It needs an algorithmic change (online softmax), which is FlashAttention | Huge, but pattern-matched or hand-written |
| Horizontal | per-parameter optimizer updates | Yes (independent ops) | Yes for many tiny kernels: saves launches (foreach / multi-tensor apply) |
| Multi-output | `y` and `sum(y)` from one pass | Yes | Saves re-reading `y` |

**Fusion can lose.** Three classic cases:

1. **Recompute.** XLA's priority fusion duplicates a producer into *every* consumer. If an expensive producer (an `erf`/`exp` chain) feeds 3 consumers, fusing computes it 3 times. For a GEMM prologue the factor is the number of output tiles that reload each input element: with N = 4096 and `BLOCK_N` = 128, each element of A is loaded and transformed 32 times. That is fine for a cast or an int4 dequantize (a few ALU ops against a compute-bound GEMM) and wasteful for a transcendental.
2. **Register pressure and occupancy.** A fused kernel holds every intermediate in VGPRs. On CDNA3, 512 VGPRs per SIMD lane are shared by the resident waves: a kernel using 64 VGPRs can keep 8 waves per SIMD, 128 VGPRs allows 4, and 256 allows 2. Fewer waves means less latency hiding, and spills go to scratch memory.
3. **Lost library kernels.** Fusing an elementwise op into a GEMM can move the GEMM from a tuned hipBLASLt kernel to a generated one that is slower than the library kernel plus a separate cheap elementwise kernel. This is why Inductor benchmarks template-with-epilogue against extern-plus-separate-kernel under `max-autotune` before choosing.

### Interview Questions

**Q1.** What problem does MLIR solve that LLVM IR doesn't?

**A.** LLVM IR is a single, low abstraction level: scalars, vectors, memory, and branches. ML compilers need to make decisions at higher levels: "this is a matmul, tile it for LDS and use MFMA", "these two tensor ops can fuse", "this tensor can be written in place". Once you are in LLVM IR, that structure is gone and recovering it is fragile. MLIR makes the IR extensible through dialects, so each level (`stablehlo`/`torch` → `linalg` → `memref`/`scf`/`vector` → `gpu`/`amdgpu` → `llvm`/`rocdl`) is first-class. Lowering is progressive, with each pass working where its job is easy. Interfaces such as `TilingInterface` let one transformation serve many ops, and projects reuse the middle of the stack: Triton, IREE, torch-mlir, rocMLIR, and XLA's newer emitters all build on MLIR. Follow-up, "what's the cost?": dialect sprawl, a moving upstream API (downstream projects pin an LLVM commit), and the need to define legality and conversion carefully at every level.

**Q2.** Walk through how a `linalg.matmul` on tensors becomes AMDGCN.

**A.** (1) Choose a strategy and tile sizes per target: for example IREE's TileAndFuse with `MFMA_F32_16x16x16_F16`, 256 threads per workgroup, wave64. (2) Tile and distribute: the outer tile loops become an `scf.forall` mapped to workgroups, and the inner level is mapped to subgroups (waves). Elementwise consumers are fused into the tile. (3) Tile the K reduction as a sequential `scf.for`, and promote A and B tiles to LDS (shared memory) so each element is loaded from HBM once per workgroup. (4) Vectorize: the inner tile becomes `vector` ops, then `amdgpu.mfma` (MFMA intrinsics) with the register layout that instruction requires. (5) Bufferize: `tensor` becomes `memref`, ideally in place through destination-passing style. (6) Lower `scf`/`vector`/`gpu`/`amdgpu` to the `llvm` + `rocdl` dialects, translate to LLVM IR, and let the LLVM AMDGPU backend handle register allocation, scheduling, and ISA emission into a `.hsaco` code object. Follow-ups: software pipelining (prefetch the next K tile into LDS or registers while computing the current one), LDS bank-conflict padding, and VGPR budget versus occupancy.

**Q3.** Compare how XLA and TorchInductor decide what to fuse. Why does JAX need static shapes, and how do you serve variable-length inputs with it?

**A.** XLA works on HLO, a static-shaped, whole-program graph. Its priority fusion pass uses an analytical cost model (max of compute and memory time, plus launch overhead) to estimate whether duplicating each producer into all its consumers lowers the total time. It applies the best fusions first, then adds multi-output and horizontal fusion. Inductor works on ATen graphs captured by Dynamo. Its scheduler greedily fuses pairs of nodes with compatible loop structure, ranked by memory traffic saved, and it can fuse epilogues into Triton GEMM templates when autotuning shows a win. Static shapes let XLA plan every buffer and pick every kernel at compile time, and they are a natural fit for TPUs. The price is a recompile for every new shape. For variable lengths: bucket to a few padded sizes (powers of two, or multiples of 128), mask the padding, and precompile each bucket at startup. Watch the trade-off between padding waste (compute on pad tokens) and compile count.

**Q4.** Explain algorithm vs schedule. How does Ansor find a fast schedule without templates, and why does it need a learned cost model?

**A.** The algorithm defines each output element mathematically (`C[i,j] = Σ_k A[i,k]·B[k,j]`). The schedule picks loop order, tiling, parallel mapping, vectorization, and memory staging, and cannot change the result. Separating them lets you keep one correct definition and search over performance. Ansor builds the space automatically. Derivation rules turn the compute DAG into a few *sketches* (multi-level tiling such as `SSSRRSRS` on GPU, inlined elementwise ops, consumers fused into tiles, cache stages). Random annotation fills in tile sizes and unroll/vectorize/parallel choices, and evolutionary search mutates the best programs. The space is astronomically large: about 2.6×10⁸ tilings for one 1024³ GEMM even before other knobs. A hardware measurement costs about 0.1-1 s, so Ansor ranks candidates with a learned cost model (gradient-boosted trees over program features) and measures only the top few. Each measurement then retrains the model. A task scheduler spreads the trial budget across a model's subgraphs according to their contribution to end-to-end latency. Follow-up, "why not just use a library?": libraries cover common ops and shapes. Search covers unusual shapes, fused ops, and new hardware before the libraries catch up.

**Q5.** What is IREE, and when would you pick it over `torch.compile` or vLLM?

**A.** IREE is an MLIR-based ahead-of-time compiler plus a small runtime. It compiles the whole program, kernels and the host scheduling logic alike, into a `.vmfb` module that runs without Python on CPU, ROCm/HIP, CUDA, Vulkan, or Metal. Its fusion is "dispatch region formation" in the `flow` phase: a root op such as a matmul with its elementwise producers and consumers becomes one kernel. Scheduling and memory planning happen in `stream`, and codegen happens per target in `hal`. Pick it for deployment without a Python runtime, many targets from one compiler, or embedded and mobile constraints. AMD also uses it in its SHARK stack. Pick `torch.compile` for PyTorch training and research, where eager fallback and quick iteration matter. Pick vLLM or SGLang for LLM serving, where the hard problems are scheduling and the KV cache (PagedAttention, continuous batching), not graph compilation.

**Q6.** A profile of a compiled model shows hundreds of short kernels with generated names. As a profiling-tools engineer, how do you attribute GPU time back to framework ops?

**A.** Use the compiler's naming and metadata, then join on kernel name. Inductor names kernels by kind and the ops fused into them (`triton_poi_fused_add_mul_0`, `triton_red_...`, `triton_per_...`, `triton_tem_...`). `TORCH_LOGS=output_code` shows each kernel's source annotated with the ATen ops it came from, and `torch.profiler` `record_function` ranges give the module context. XLA attaches `metadata={op_name="jit(f)/..." stack_frame_id=...}` to every HLO instruction, so the `--xla_dump_to` after-optimizations file maps each fusion name to user source lines. IREE dispatch names encode the root op and shape (`..._dispatch_0_matmul_4x16x8_f32`). In a `rocprofv3 --kernel-trace` capture, group by kernel name, sum durations, and join with the compiler's map. Hundreds of tiny kernels usually point to graph breaks, a disabled fusion, or missing HIP-graph capture, in which case launch overhead dominates. Check `TORCH_LOGS=graph_breaks,perf_hints` before tuning any single kernel. See [ROCm Profiling Tools](AMD_GPU_Architecture_and_Profiling.md#4-rocm-profiling-tools).

**Q7.** When does fusion make things slower?

**A.** (1) Recompute: duplicating an expensive producer into several consumers, or into a GEMM prologue where each input element is reloaded N/`BLOCK_N` times (32× for N = 4096, `BLOCK_N` = 128). (2) Register pressure: more live intermediates mean more VGPRs, lower occupancy (on CDNA3, 128 VGPRs allows 4 waves per SIMD and 256 allows 2), and possibly spills. (3) Losing a tuned library kernel: a generated GEMM with a fused epilogue can be slower than hipBLASLt plus a separate cheap elementwise kernel. (4) Lost parallelism: fusing a reduction with a large consumer can force a launch with too few workgroups to fill 304 CUs. Every compiler handles this with a cost model or by benchmarking alternatives, and that is the right answer in an interview: estimate bytes saved against recompute and occupancy cost, then measure.

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

See also [8.8 ML Compiler Stacks](#88-ml-compiler-stacks-mlir-xla-tvm-and-iree) for HLO/StableHLO, XLA's priority fusion, and a comparison with TorchInductor.

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

See also [8.8 ML Compiler Stacks](#88-ml-compiler-stacks-mlir-xla-tvm-and-iree) for MLIR dialects and progressive lowering, and for what the `ttir`/`ttgir` stages hold.

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

Triton supports AMD GPUs through a ROCm backend that generates AMDGPU ISA instead of PTX. The same Triton kernel source code works on both NVIDIA and AMD hardware -- only the compilation backend changes. Running correctly is not the same as running fast, though. On AMD a "warp" is a 64-wide wavefront, MFMA instruction shape and occupancy are tuned through AMD-only knobs (`matrix_instr_nonkdim`, `waves_per_eu`), and good `num_stages` values differ from NVIDIA's. See [47.4 Triton on AMD: Backend Specifics](#474-triton-on-amd-backend-specifics).

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
KV-cache bytes per token:
  2 (K + V) × n_layers × n_kv_heads × head_dim × dtype_bytes

Example (LLaMA-2/3-70B, BF16/FP16): 80 layers, 64 query heads but only
8 KV heads (grouped-query attention, GQA), head_dim 128:
  2 × 80 × 8 × 128 × 2 B = 327,680 B ≈ 0.33 MB (320 KiB) per token
  2048-token sequence     = 671 MB ≈ 0.67 GB per request
  128K-token context      ≈ 43 GB per request

Same shape with plain multi-head attention (MHA, n_kv_heads = 64):
  2 × 80 × 64 × 128 × 2 B ≈ 2.6 MB per token -> 5.4 GB per 2048 tokens (8× more)
```

**Use `n_kv_heads`, not `n_heads`.** In MHA every query head has its own K/V head. GQA shares one K/V head across a group of query heads (LLaMA-2/3-70B: 64 query heads, 8 KV heads, groups of 8). MQA is the extreme case of a single KV head. The KV cache, and the HBM bytes read per decode step, shrink by `n_heads / n_kv_heads`. Quality stays close to MHA, which is why most modern LLMs use GQA. Reading `num_key_value_heads` (not `num_attention_heads`) from the model's `config.json` is the standard interview check.

**Capacity sanity check (one MI300X, 192 GB):** 70B BF16 weights take about 140 GB. At `gpu-memory-utilization=0.9` (about 173 GB usable), roughly 30 GB remains for KV cache after activations and workspace. That is ~30e9 / 327,680 ≈ 90K tokens total, for example ~45 concurrent 2K-token requests. FP8 KV cache doubles it, and TP=2 more than doubles it because the weights are split. See [LLM and ML Fundamentals](../ml-gpu/LLM_and_ML_Fundamentals.md) for the attention math, and [ML Systems Design](../ml-gpu/ML_Systems_Design.md) for serving capacity planning.

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
| `enforce-eager` | Disable CUDA graphs (HIP graphs on ROCm) | Debugging only |
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
Bytes per parameter (BF16 model params, FP32 main grads -- Megatron's default):
  BF16 params 2 + FP32 grads 4 + FP32 main params 4 + Adam m 4 + Adam v 4

Without distributed optimizer (replicated on every DP rank):
  2 + 4 + 12                 = 18 bytes per parameter
  (16 bytes if grads are kept in BF16: 2 + 2 + 12)

With distributed optimizer (only the 12 B of FP32 main params + Adam
state is sharded; BF16 params and the grad buffer stay full-size):
  2 + 4 + 12/DP bytes per parameter   (e.g. DP = 8 -> 7.5 B instead of 18 B)
  Communication: reduce-scatter grads after backward (each rank gets the
  grads for its shard), local Adam step, all-gather updated BF16 params.
  Same element count as the all-reduce it replaces (about P per phase per
  rank). With FP32 grads and a BF16 param all-gather it actually moves fewer
  bytes: 4 + 2 instead of 4 + 4 per element.
```

The general ZeRO-1/2/3 formulas, a 70B worked example, and offload are in [section 45](#45-training-memory-math-zero-activations-and-offload).

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
| Offloading | CPU offload (FSDP `CPUOffload`, FSDP2 `CPUOffloadPolicy`) | Limited (optimizer CPU offload in recent Megatron-Core) | CPU/NVMe offload (ZeRO-Offload/Infinity) |
| Model scale | Medium (1-30B easy) | Large (100B+ designed for) | Large (supports offloading) |
| Ease of setup | Moderate | Complex | Moderate (config-based) |
| Ecosystem | PyTorch native | NVIDIA-led (AMD maintains a ROCm port) | Microsoft, open-source |

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
| Mixture-of-Experts training | Megatron-Core MoE (EP + TP + PP) or DeepSpeed-MoE; see section 46 |
| Running any of the above on AMD Instinct | Same stacks on ROCm builds; see section 47 |

---

# 45. Training Memory Math: ZeRO, Activations, and Offload

---

"Will it fit, and on how many GPUs?" is the first question in any large-training design interview. Training memory has four parts: **model state** (weights, gradients, optimizer state), **activations** saved for backward, **temporary buffers** (communication buckets, gathered parameters, workspace), and **fragmentation**. Model state is exact arithmetic. Activations are an estimate you then confirm with a memory snapshot.

## 45.1 Bytes per Parameter: Mixed-Precision Adam

| Component | Dtype | Bytes/param | Why it exists |
|---|---|---|---|
| Weights used in forward/backward | BF16 | 2 | Matrix units run at BF16 rate |
| Gradients | BF16 | 2 | Output of backward |
| Master weights | FP32 | 4 | BF16 updates would round away (see [8.7](#87-number-formats-and-mixed-precision-numerics)) |
| Adam first moment `m` | FP32 | 4 | Momentum |
| Adam second moment `v` | FP32 | 4 | Per-parameter adaptive LR |
| **Total** | | **16** | 2 + 2 + 12 |

Variants change the constant but not the method:
- FP32 gradient accumulation with a separate persistent BF16 weight copy (Megatron default) gives 2 + 4 + 12 = **18 B**. FSDP with `reduce_dtype=float32` stays at **16 B** (fp32 sharded params 4 + fp32 grads 4 + Adam 8) because its BF16 weights exist only transiently during the all-gather (see [7.4](#74-fsdp-fully-sharded-data-parallel)).
- Pure FP32 training with Adam gives 4 + 4 + 8 = **16 B** (no separate master copy).
- 8-bit Adam states (bitsandbytes) give roughly 2 + 2 + 4 + 2 = **10 B**.
- SGD with momentum and no master copy gives 2 + 2 + 4 = **8 B**.
- Inference keeps weights only: **2 B** (BF16), **1 B** (FP8/INT8), or **0.5 B** (INT4), plus KV cache.

Write the formula as `(w + g + K) * P` with K = 12 for mixed-precision Adam. That is the notation of the ZeRO paper (Rajbhandari et al., 2020), which uses Ψ for P.

## 45.2 ZeRO Stages: Per-GPU Formulas

With P parameters and N data-parallel ranks:

| Stage | What is sharded | Model-state bytes per GPU | Communication per step (elements) |
|---|---|---|---|
| DDP (ZeRO-0) | Nothing | `(2 + 2 + 12) P = 16P` | All-reduce grads ≈ 2P (reduce-scatter + all-gather) |
| ZeRO-1 (`P_os`) | Optimizer state | `4P + 12P/N` | 2P: reduce-scatter grads, all-gather updated params |
| ZeRO-2 (`P_os+g`) | + gradients | `2P + 14P/N` | 2P: same as DDP, but grads are reduce-scattered bucket by bucket and freed |
| ZeRO-3 (`P_os+g+p`) / FSDP `FULL_SHARD` | + parameters | `16P/N` | **3P**: all-gather params in forward, all-gather again in backward, reduce-scatter grads (1.5× DDP) |
| HSDP / ZeRO++ hpZ | ZeRO-3 within a node, replicate across nodes | `16P/N_node` | Slow inter-node link carries only the gradient all-reduce |

ZeRO-1 and ZeRO-2 cost the same communication as DDP: an all-reduce *is* a reduce-scatter plus an all-gather, and ZeRO just runs the optimizer between the two halves. That is why ZeRO-1/2 is almost always worth enabling. ZeRO-3 adds one extra parameter all-gather, which must be overlapped by prefetching the next layer's parameters. See [Collective Communication](../ml-gpu/Parallel_GPU_Programming.md#3-collective-communication) for ring all-reduce cost.

## 45.3 Worked Example: 70B Model on 64 GPUs

P = 70e9, N = 64 (8 nodes × 8 MI300X, 192 GB HBM each; the same numbers apply to 80 GB parts, which are stricter):

```python
# zero_memory.py -- per-GPU training memory for mixed-precision Adam under ZeRO stages
GB = 1e9

def model_state_bytes(params: float, n_dp: int, stage: int,
                      w_bytes: int = 2, g_bytes: int = 2, opt_bytes: int = 12) -> float:
    """ZeRO paper accounting: bf16 weights (2) + bf16 grads (2) + fp32 master/m/v (12)."""
    if stage == 0:   # plain DDP: everything replicated
        return params * (w_bytes + g_bytes + opt_bytes)
    if stage == 1:   # shard optimizer state
        return params * (w_bytes + g_bytes) + params * opt_bytes / n_dp
    if stage == 2:   # + shard gradients
        return params * w_bytes + params * (g_bytes + opt_bytes) / n_dp
    if stage == 3:   # + shard parameters
        return params * (w_bytes + g_bytes + opt_bytes) / n_dp
    raise ValueError(stage)

def activation_bytes(seq: int, mbs: int, hidden: int, layers: int, tp: int = 1,
                     full_recompute: bool = False) -> float:
    """Korthikanti et al. 2022, 16-bit activations, flash attention (no s^2 term), SP with TP."""
    per_layer = 34 * seq * mbs * hidden / tp
    if full_recompute:   # keep only each layer's input; recompute one layer at a time
        return layers * 2 * seq * mbs * hidden / tp + per_layer
    return layers * per_layer

P, N = 70e9, 64
for stage in range(4):
    print(f"ZeRO-{stage}: {model_state_bytes(P, N, stage) / GB:8.1f} GB/GPU model state")

layer_params = P / 80                         # ~0.875e9 params per transformer layer
working = 2 * layer_params * 2 + layer_params * 2  # 2 gathered bf16 layers (prefetch) + 1 layer of grads
print(f"ZeRO-3 working set (gathered layers + unsharded grads): {working / GB:.1f} GB")

for rc in (False, True):
    a = activation_bytes(seq=4096, mbs=1, hidden=8192, layers=80, full_recompute=rc)
    print(f"activations (s=4096, b=1, h=8192, L=80, recompute={rc}): {a / GB:.1f} GB")
```

Output and interpretation:

```text
ZeRO-0:   1120.0 GB/GPU model state      -> impossible (16 B x 70e9)
ZeRO-1:    293.1 GB/GPU model state      -> 4 x 70 = 280 GB of bf16 weights+grads alone: no
ZeRO-2:    155.3 GB/GPU model state      -> fits 192 GB on paper, ~37 GB left for activations: impractical
ZeRO-3:     17.5 GB/GPU model state      -> fits easily
ZeRO-3 working set (gathered layers + unsharded grads): 5.2 GB
activations (s=4096, b=1, h=8192, L=80, recompute=False): 91.3 GB
activations (s=4096, b=1, h=8192, L=80, recompute=True): 6.5 GB
```

Total for ZeRO-3 with full activation recompute: ≈ 17.5 + 5.2 + 6.5 ≈ **29 GB** per GPU plus allocator overhead. That fits comfortably and leaves room for a larger micro-batch, or for turning recompute off for some layers. Without recompute, 17.5 + 5.2 + 91 ≈ 114 GB fits a 192 GB MI300X but not an 80 GB GPU. There you would add TP = 8 within the node, which divides both the weight shards and, with sequence parallelism, the activations by 8.

## 45.4 Activation Memory and Checkpointing

Korthikanti et al. (2022, "Reducing Activation Recomputation in Large Transformer Models") estimate the activations of one GPT-style layer, in bytes with 16-bit activations, as:

```text
per layer ≈ s · b · h · (34 + 5 · a · s / h)
  s = sequence length, b = micro-batch, h = hidden size, a = attention heads
  34·sbh     : QKV/MLP inputs and outputs, GeLU input, LayerNorm inputs, dropout masks
  5·a·s²·b   : attention scores, softmax output, softmax dropout mask -> NOT stored with FlashAttention
with TP = t and sequence parallelism: divide everything by t
full recompute: keep only each layer's input, 2·s·b·h bytes, and recompute the layer in backward
```

The coefficient 34 assumes a 4h GeLU MLP and MHA. LLaMA's SwiGLU (three matrices, about 3.5h intermediate) and GQA shift it. Use the formula for order of magnitude, then confirm with `torch.cuda.memory._record_memory_history()` and the snapshot viewer (see 8.4).

| Strategy | Saved per layer | Extra compute | Typical use |
|---|---|---|---|
| None | everything (~34·sbh) | 0 | Small models, short sequences |
| Selective (Megatron `--recompute-activations`) | all but the attention core (the `5as/h` term) | ~2-5% | Large models without fused attention. FlashAttention already avoids storing the s² tensors, so it gains little there |
| Full (`--recompute-granularity full`, `torch.utils.checkpoint`) | layer input only (2·sbh) | ~1 extra forward ≈ +33% of step FLOPs | Long sequences, memory-bound configs |
| Offload activations to CPU | none on GPU | PCIe traffic | Last resort |

**FLOP accounting:** training costs about 6·N_params FLOPs per token (2 forward, 4 backward). Full recompute adds another 2 forward, for 8. **MFU** (model FLOPs utilization) counts only the 6, while **HFU** (hardware FLOPs utilization) counts the 8. Report MFU when comparing configurations, otherwise recompute looks like a win.

```python
# fragment -- full activation checkpointing per transformer block
from torch.utils.checkpoint import checkpoint
def forward(self, x):
    for blk in self.blocks:
        x = checkpoint(blk, x, use_reentrant=False)  # non-reentrant: works with FSDP/compile, kwargs
    return x
```

## 45.5 ZeRO-Offload and ZeRO-Infinity

When GPU count is the constraint (fine-tuning a 70B model on one node, say), trade bandwidth for capacity:

| Technique | Where state lives | Who runs the optimizer | Bottleneck |
|---|---|---|---|
| **ZeRO-Offload** (DeepSpeed) | FP32 master + Adam state (+ grads) in CPU DRAM; BF16 weights on GPU | CPU (vectorized "CPU Adam") | PCIe: grads to host (2 B/param), updated params back (2 B/param) each step; CPU Adam throughput |
| **ZeRO-Infinity** | Params, grads, and optimizer state in CPU DRAM **and/or NVMe** | CPU, overlapped | NVMe/PCIe bandwidth; it partitions offload traffic across all GPUs ("bandwidth-centric") and prefetches |
| FSDP CPU offload | FSDP1 `CPUOffload(offload_params=True)`; FSDP2 `fully_shard(..., offload_policy=CPUOffloadPolicy())` | CPU | Same PCIe limits |

Back-of-envelope for ZeRO-Offload on 70B: about 140 GB of gradients go host-bound and 140 GB of BF16 params come back each step, *spread across* the GPUs that share the work. On 8 GPUs that is 17.5 GB each way per GPU. At an effective ~50 GB/s per PCIe Gen5 x16 link, that is ≈ 0.35 s per direction per step, before CPU Adam time (840 GB of FP32 state to stream through host memory). Offload is viable when steps are long anyway (large batch, long sequences). It is a poor fit for throughput-oriented pretraining, where adding GPUs or TP is cheaper.

## 45.6 Interview Questions

**Q1.** Estimate the GPUs needed to full-fine-tune a 7B model with AdamW in BF16 mixed precision on 80 GB GPUs.

**A.** Model state is 16 B × 7e9 = 112 GB, so plain DDP does not fit on one 80 GB GPU. With ZeRO-3/FSDP over N GPUs the state is 112/N GB: N = 2 gives 56 GB, which leaves ~20 GB for activations (tight). N = 4 gives 28 GB and is comfortable. ZeRO-2 on 4 GPUs gives 2×7 + 14×7/4 = 14 + 24.5 = 38.5 GB, which also works and saves the extra parameter all-gather. Answer: 4 GPUs, with ZeRO-2 or FSDP, plus activation checkpointing if sequences are long. Mention the 18 B variant if grads are FP32.

**Q2.** Why is ZeRO-1/2 "free" in communication but ZeRO-3 is not?

**A.** DDP's ring all-reduce is a reduce-scatter followed by an all-gather, about 2P elements per rank. ZeRO-1/2 splits those two halves: after the reduce-scatter each rank owns the summed gradient shard for its optimizer partition, steps it, and all-gathers the updated parameters. The total is the same 2P. ZeRO-3 also discards the parameters after use, so they must be all-gathered again for backward, for 3P total (1.5×). It also puts the all-gathers on the critical path unless they are prefetched one layer ahead.

**Q3.** When would you choose HSDP (hybrid sharding) over full sharding?

**A.** When inter-node bandwidth is much lower than intra-node bandwidth (xGMI/NVLink at hundreds of GB/s vs a 400 Gb/s = 50 GB/s NIC) and the model fits when sharded within one node. HSDP shards within the node, so the per-layer all-gathers stay on the fast fabric, and only gradient all-reduces across replicas go over the network. Memory per GPU is 16P/8 instead of 16P/N_total.

**Q4.** You're at the memory limit. Rank these by preference: activation checkpointing, larger TP, ZeRO-3, CPU offload, smaller micro-batch.

**A.** It depends on what dominates. If model state dominates, use ZeRO-3/FSDP first (communication cost overlappable), then TP within a node (also cuts activations, but adds per-layer all-reduces on the critical path). If activations dominate, use selective or full recompute (~2-33% compute), then sequence/context parallelism. A smaller micro-batch hurts GEMM efficiency and, with pipelining, increases the bubble. CPU offload comes last because PCIe-bound steps are slow. Always confirm with a memory snapshot. Fragmentation (`expandable_segments:True` in the allocator config) can explain "OOM with 10 GB free".

---

# 46. Mixture of Experts and Expert Parallelism

---

## 46.1 What MoE Changes

A Mixture-of-Experts layer replaces the dense FFN in a transformer block with **E expert FFNs** and a **router**. Each token is processed by only its top-k experts, so **parameters scale with E while FLOPs per token scale with k**.

| Model | Total params | Active params/token | Experts | Routing |
|---|---|---|---|---|
| Switch Transformer | up to 1.6T | ~dense base | up to 2048 | top-1 |
| Mixtral 8x7B | 46.7B | 12.9B | 8 per layer | top-2 |
| DeepSeek-V3 | 671B | 37B | 256 routed + 1 shared per MoE layer | top-8, auxiliary-loss-free balancing |

```text
            x (token, hidden h)
                 │
        router: logits = x·W_g  (h × E), softmax
                 │ top-k
     ┌───────────┼───────────┐
     ▼           ▼           ▼
  expert 3    expert 7    (others skipped)
     │           │
     └── weighted sum by renormalized gate probs ──► y
```

Consequences you should state in an interview:
- **Memory** scales with *total* params, because every expert must be resident somewhere. **Compute** scales with *active* params. A 671B MoE needs 671B-model memory but runs at roughly 37B-dense FLOPs per token.
- Decode for small batches is memory-bandwidth-bound on the experts actually hit. At large batch almost every expert is hit each step, so you read all expert weights.
- A *dynamic, data-dependent* communication pattern appears: tokens have to travel to wherever their experts live.

## 46.2 Routing, Capacity Factor, and Token Dropping

Fixed-shape kernels and buffers need a bound on how many tokens an expert receives:

```text
capacity C = ceil(capacity_factor × T × k / E)
  T = tokens in the routing group (e.g. per device micro-batch), k = experts per token
  capacity_factor 1.0-1.25 is typical for training; larger values for eval
Tokens routed to a full expert are DROPPED: they skip the FFN and pass through the residual.
```

Example: T = 4096 tokens, E = 8, k = 2, CF = 1.25 gives C = ceil(1.25 × 4096 × 2 / 8) = 1280 slots per expert. Perfect balance would put 1024 tokens in each. A hot expert receiving 2000 drops 720.

**Dropless MoE** (MegaBlocks; Megatron-Core with `--moe-grouped-gemm` and no capacity factor) avoids dropping. Experts take variable-sized batches through a grouped or block-sparse GEMM, at the cost of variable-size all-to-all and load imbalance showing up as stragglers rather than as quality loss.

## 46.3 Load-Balancing Losses

Without pressure, the router collapses onto a few experts: they get trained more, so they get chosen more. The **Switch Transformer auxiliary loss**:

```text
L_aux = α · E · Σ_i f_i · P_i
  f_i = fraction of token assignments dispatched to expert i   (hard counts, no gradient)
  P_i = mean router probability for expert i over the batch    (differentiable)
  α ≈ 1e-2;  L_aux / α = 1.0 at perfect balance, larger when skewed
```

Gradients flow through `P_i`, which pushes probability mass away from over-used experts. Related techniques:
- **Router z-loss** (ST-MoE): `mean(logsumexp(logits)^2)`, which keeps router logits small for numerical stability.
- **Auxiliary-loss-free balancing** (DeepSeek-V3): a per-expert bias added to the logits *only for top-k selection*, nudged up or down after each step according to load. It balances without an extra loss term that fights the language-modeling objective.
- **Device- or node-limited routing**: cap the number of devices or nodes a token's experts may span, which bounds all-to-all fan-out.

```python
# moe.py -- top-k MoE layer with capacity factor and Switch-style load-balancing loss (CPU-runnable)
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class TopKMoE(nn.Module):
    def __init__(self, d_model, d_ff, n_experts, k=2, capacity_factor=1.25, aux_coeff=1e-2):
        super().__init__()
        self.E, self.k, self.cf, self.aux_coeff = n_experts, k, capacity_factor, aux_coeff
        self.router = nn.Linear(d_model, n_experts, bias=False)
        self.w1 = nn.Parameter(torch.randn(n_experts, d_model, d_ff) * d_model ** -0.5)
        self.w2 = nn.Parameter(torch.randn(n_experts, d_ff, d_model) * d_ff ** -0.5)

    def forward(self, x):                                  # x: [T, d_model] (batch*seq flattened)
        T, E, k = x.shape[0], self.E, self.k
        probs = self.router(x).softmax(dim=-1)             # [T, E]
        top_p, top_e = probs.topk(k, dim=-1)               # [T, k]
        top_p = top_p / top_p.sum(dim=-1, keepdim=True)    # renormalize over chosen experts

        # Switch-Transformer load-balancing loss: E * sum_i f_i * P_i  (== 1.0 when perfectly uniform)
        f = F.one_hot(top_e, E).float().sum(dim=1).mean(dim=0) / k   # fraction of assignments per expert
        P = probs.mean(dim=0)                                        # mean router prob per expert
        aux = self.aux_coeff * E * torch.sum(f * P)

        capacity = math.ceil(self.cf * T * k / E)          # slots per expert
        flat_e = top_e.reshape(-1)                         # [T*k]
        flat_t = torch.arange(T).repeat_interleave(k)      # token id of each assignment
        flat_p = top_p.reshape(-1)
        out = torch.zeros_like(x)
        dropped = 0
        for e in range(E):                                 # real kernels: one grouped GEMM over all experts
            idx = (flat_e == e).nonzero(as_tuple=True)[0]
            if idx.numel() > capacity:                     # overflow: drop (token keeps its residual path)
                dropped += idx.numel() - capacity
                idx = idx[:capacity]
            tok = flat_t[idx]
            h = F.silu(x[tok] @ self.w1[e]) @ self.w2[e]
            out.index_add_(0, tok, h * flat_p[idx, None])
        return out, aux, dropped, capacity

torch.manual_seed(0)
moe = TopKMoE(d_model=64, d_ff=256, n_experts=8, k=2)
x = torch.randn(1024, 64)
y, aux, dropped, cap = moe(x)
print(f"capacity/expert={cap}  dropped={dropped}  balance={aux.item() / moe.aux_coeff:.3f} (1.0 = uniform)")

with torch.no_grad():                                      # skew the router toward expert 0
    moe.router.weight[0] += 0.05                       # expert 0 favored for inputs along all-ones
y, aux, dropped, cap = moe(x + 1.0)                        # shifted inputs -> hot expert
print(f"skewed router:     dropped={dropped}  balance={aux.item() / moe.aux_coeff:.3f}")
(y.pow(2).mean() + aux).backward()                         # aux loss pushes the router back toward balance
print("router grad norm:", round(moe.router.weight.grad.norm().item(), 4))
```

On CPU this prints `capacity/expert=320 dropped=0 balance=1.001`, then for the skewed router `dropped=1099 balance=2.884`. A hot expert both drops more than half of the 2048 assignments and raises the auxiliary loss.

## 46.4 Expert Parallelism and All-to-All

With **expert parallelism (EP)** of degree `ep`, each rank holds `E/ep` experts. Attention and other dense parts are usually data-parallel (or TP) across the same ranks. A MoE layer then runs:

```text
1. route locally                  (each rank: its T tokens -> top-k expert ids)
2. all-to-all DISPATCH            (send each token's hidden vector to the rank owning its expert)
3. grouped GEMM over local experts (variable tokens per expert)
4. all-to-all COMBINE             (send results back to the token's home rank)
5. weighted sum + residual
Backward repeats 2 and 4 in reverse: 4 all-to-alls per MoE layer per training step.
```

**Volume per all-to-all, per rank:** `T × k × h × bytes × (ep - 1)/ep`. Example: T = 8192 tokens per GPU, k = 2, h = 4096, BF16 gives 8192 × 2 × 4096 × 2 B ≈ **134 MB**. Across a 50 GB/s (400 Gb/s) NIC that is ~2.7 ms. With 32 MoE layers × 4 all-to-alls = 128 per step, that is ≈ **0.34 s per step** if nothing overlaps. Hence the standard practices:
- Keep EP inside a node where possible (xGMI/NVLink), or limit nodes per token.
- Overlap dispatch/combine with shared-expert or attention compute.
- Use FP8 dispatch.
- Balance load: all-to-all latency is set by the *most loaded* rank.

Unlike all-reduce, all-to-all has no reduction, so it does not shrink with ring tricks. Every byte must cross the network once (see the all-to-all section in [Collective Communication](../ml-gpu/Parallel_GPU_Programming.md#3-collective-communication)).

**Framework knobs.**
- Megatron-Core: `--num-experts`, `--moe-router-topk`, `--expert-model-parallel-size`, `--moe-aux-loss-coeff`, `--moe-grouped-gemm`, `--moe-token-dispatcher-type alltoall`. EP is carved out of the DP dimension, so expert gradients are reduced over `DP/EP` replicas.
- DeepSpeed-MoE offers equivalent options.
- vLLM inference: `--enable-expert-parallel`. On ROCm, fused MoE kernels come from AITER when `VLLM_ROCM_USE_AITER=1` (section 47).

## 46.5 Interview Questions

**Q1.** Mixtral 8x7B has 46.7B parameters but is "as fast as a 13B model." Explain, and say when that claim breaks.

**A.** Only the attention blocks (shared) and 2 of 8 expert FFNs run per token, about 12.9B active parameters, so FLOPs per token match a ~13B dense model. The claim breaks for (1) **memory**: all 46.7B must be resident (93 GB in BF16); (2) **large-batch decode**: different tokens hit different experts, so each step reads nearly all expert weights and the step is bandwidth-bound like a 47B model; (3) **multi-GPU**: all-to-all and load imbalance add latency that a dense 13B model doesn't pay.

**Q2.** What is the capacity factor and what happens if you set it too low or too high?

**A.** It sets per-expert buffer slots as `CF × T·k/E`. Too low (≤1.0): imbalance causes tokens to be dropped (skipping the FFN), which hurts quality, especially early in training. Too high: wasted compute and memory on padding, and larger all-to-all buffers. Dropless implementations remove the trade-off by using variable-size grouped GEMMs, moving the cost to load-imbalance stragglers.

**Q3.** Derive the Switch auxiliary loss's minimum and explain why it uses both `f` and `P`.

**A.** `L/α = E·Σ f_i P_i`. With uniform routing f_i = P_i = 1/E, giving E·E·(1/E²) = 1. Because f is produced by top-k on the same probabilities, f ≈ P. Then E·Σ P_i² ≥ E·(Σ P_i)²/E = 1 by Cauchy-Schwarz, with equality only at P_i = 1/E. So 1.0 is the minimum, and any skew raises it. (For arbitrary unrelated f and P the product could be smaller; the bound relies on their coupling.) `f_i` (hard dispatch fraction) measures the actual load but is not differentiable through the top-k. `P_i` is differentiable, so the product applies gradient to the probabilities in proportion to the actual load.

**Q4.** You add EP=8 to a model and step time rises 40%. Where do you look?

**A.** In the trace, look at the all-to-all kernels: their duration, whether they overlap with compute, and their skew across ranks. Then check tokens per expert per rank (router imbalance makes one rank the straggler), whether EP crosses nodes (switch to intra-node EP or node-limited routing), grouped-GEMM efficiency with small per-expert batches (many experts with few tokens each makes the GEMMs memory-bound), and whether dispatch is padding to capacity. Fixes: rebalance (aux coefficient or bias-based balancing), keep EP intra-node, overlap dispatch with shared-expert compute, and use FP8 dispatch.

---

# 47. The ROCm ML Stack

---

How the frameworks in this guide run on AMD Instinct GPUs (MI300X/MI325X = gfx942, MI350X/MI355X = gfx950), and which libraries actually execute each op. HIP-level programming is covered in [HIP Fundamentals](../ml-gpu/Parallel_GPU_Programming.md#25-hip-fundamentals-and-portability) and the [ROCm library map](../ml-gpu/Parallel_GPU_Programming.md#31-rocm-ecosystem-and-libraries). Hardware details and counters are in [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md).

## 47.1 How PyTorch Runs on ROCm

- **Hipify at build time.** PyTorch has one CUDA-flavored source tree. A ROCm build first runs the hipify step (`tools/amd_build/build_amd.py`), which rewrites CUDA sources and APIs into HIP: `cudaMalloc` becomes `hipMalloc`, cuBLAS calls go to hipBLAS/hipBLASLt, cuDNN calls go to MIOpen, and NCCL calls go to RCCL. The result is compiled with the ROCm clang toolchain for the architectures in `PYTORCH_ROCM_ARCH` (e.g. `gfx942;gfx950`). This is source translation, not runtime emulation.
- **The `cuda` name is kept on purpose.** Dispatch keys, `torch.cuda.*`, the `"cuda"` device string, `torch.cuda.Stream/Event/CUDAGraph`, and the `"nccl"` process-group backend all keep their names. On ROCm they are backed by HIP streams, events, and graphs and by RCCL, so unmodified model code runs.
- **Detecting ROCm:** `torch.version.hip` is a version string on ROCm builds and `None` on CUDA builds, while `torch.version.cuda` is `None` on ROCm. `torch.cuda.get_device_properties(0).gcnArchName` returns e.g. `gfx942:sramecc+:xnack-`.
- **C++/CUDA extensions:** `torch.utils.cpp_extension.CUDAExtension` and `load()` hipify `.cu` sources automatically on ROCm builds. Inline PTX, warp-size-32 assumptions (`__shfl_sync` with a 32-bit mask, `if (lane < 32)`), and cuBLAS-only features are the usual porting breakages (see [CUDA-to-HIP Porting](../ml-gpu/Parallel_GPU_Programming.md#29-cuda-to-hip-porting)).
- **Device visibility:** `ROCR_VISIBLE_DEVICES` filters at the ROCr (HSA) runtime level and is what AMD recommends for isolation on Linux. Schedulers set it. `HIP_VISIBLE_DEVICES` (and `CUDA_VISIBLE_DEVICES`, also honored by HIP) filter at the HIP level, *indexing into whatever ROCr already exposes*. Setting both with physical IDs is a classic "no GPUs found" bug. MI300X compute-partition modes (SPX/DPX/QPX/CPX) change how many logical GPUs one package exposes, up to 8 in CPX.

## 47.2 Which Library Runs Each Op

| PyTorch op family | CUDA library | ROCm library | Notes |
|---|---|---|---|
| `mm`, `addmm`, `bmm`, `linear` | cuBLAS / cuBLASLt | **hipBLASLt** (preferred on MI300-class) or **rocBLAS** via hipBLAS | Selection by heuristic; `TORCH_BLAS_PREFER_HIPBLASLT=1/0` or `torch.backends.cuda.preferred_blas_library()` overrides. Both use Tensile-generated kernels (names start with `Cijk_`) |
| FP8 GEMM (`torch._scaled_mm`) | cuBLASLt | hipBLASLt | FNUZ FP8 on gfx942, OCP FP8 on gfx950 (see 8.7) |
| Convolution, BatchNorm (the `cudnn` path) | cuDNN | **MIOpen** | `torch.backends.cudnn.*` flags apply to MIOpen. Its find/tuning results are cached in `~/.config/miopen` (user DB) and `~/.cache/miopen` (kernels) |
| SDPA flash / mem-efficient attention | FlashAttention / cuDNN | **AOTriton** (default) or **Composable Kernel** | `torch.backends.cuda.preferred_rocm_fa_library("ck")` or `TORCH_ROCM_FA_PREFER_CK=1` |
| Collectives (`backend="nccl"`) | NCCL | **RCCL** | Honors `NCCL_*` env vars (`NCCL_DEBUG=INFO`) |
| FFT, RNG, sparse, linalg | cuFFT, cuRAND, cuSPARSE, cuSOLVER | rocFFT/hipFFT, rocRAND/hipRAND, rocSPARSE/hipSPARSE, rocSOLVER/hipSOLVER | |
| Inductor-generated pointwise/reduction/GEMM templates | Triton (PTX) | Triton (AMDGCN) | Section 47.4 |
| LLM inference kernels (vLLM/SGLang) | FlashInfer, CUTLASS, custom CUDA | **AITER** | Section 47.5 |

- **Composable Kernel (CK):** AMD's C++ template library for tile-based, MFMA-aware kernels (GEMM with fused epilogues, fused attention forward and backward, grouped GEMM, convolution). It is AMD's counterpart to CUTLASS/CuTe. MIOpen, PyTorch's CK SDPA backend, the ROCm FlashAttention port, and AITER build on it.
- **AITER (AI Tensor Engine for ROCm):** a Python-callable operator library of the hottest LLM ops: MHA/MLA attention (prefill and decode), fused MoE, block-scaled FP8 GEMM, RMSNorm, RoPE, and custom all-reduce. Each op is implemented with whichever backend is fastest (CK, Triton, or hand-written assembly). vLLM and SGLang call it when enabled. The first run JIT-builds kernels into `~/.cache/aiter`.

## 47.3 TunableOp and GEMM Selection

BLAS heuristics pick a kernel per GEMM shape without benchmarking, and for unusual shapes the choice can be far from optimal. **TunableOp** benchmarks every candidate rocBLAS and hipBLASLt solution for each GEMM shape the program actually runs, records the winner in a CSV, and reuses it afterwards. It also works on CUDA, where it ranks cuBLASLt heuristic candidates.

```bash
# Phase 1 -- tune on a representative run (slow: each new shape is benchmarked)
PYTORCH_TUNABLEOP_ENABLED=1 PYTORCH_TUNABLEOP_TUNING=1 \
PYTORCH_TUNABLEOP_FILENAME=tunableop_results.csv \
    python train.py --steps 50          # writes tunableop_results0.csv, ...1.csv: device ordinal inserted per GPU

# Phase 2 -- production: read the table, never tune
PYTORCH_TUNABLEOP_ENABLED=1 PYTORCH_TUNABLEOP_TUNING=0 \
PYTORCH_TUNABLEOP_FILENAME=tunableop_results.csv python train.py

# Offline variant: record untuned shapes cheaply (-> tunableop_untuned0.csv), tune later;
# mgpu_tune_gemm_in_file("tunableop_untuned?.csv", num_gpus) spreads tuning over GPUs
PYTORCH_TUNABLEOP_ENABLED=1 PYTORCH_TUNABLEOP_TUNING=0 PYTORCH_TUNABLEOP_RECORD_UNTUNED=1 python serve.py
python -c "import torch.cuda.tunable as t; t.enable(); t.tuning_enable(); t.tune_gemm_in_file('tunableop_untuned0.csv')"
```

Pitfalls:
1. Results are specific to GPU model, ROCm, and library versions. The CSV header records validators, and mismatched entries are ignored.
2. Workloads with many distinct shapes (LLM serving with variable batch × sequence) can spend a long time tuning. Record offline, or tune only the steady-state shapes.
3. Tuning on a busy or thermally throttled GPU picks wrong winners.
4. Retuning can change the selected kernel and therefore the last bits of results (see non-determinism in 8.7).

Also set `PYTORCH_TUNABLEOP_VERBOSE=1` once to confirm TunableOp is actually engaged.

## 47.4 Triton on AMD: Backend Specifics

| Concept | NVIDIA | AMD CDNA (MI200/MI300/MI350) |
|---|---|---|
| SIMT width | warp = 32 threads | **wavefront = 64** lanes (RDNA consumer GPUs default to wave32) |
| `num_warps=4` means | 128 threads per CTA | **256** work-items per workgroup |
| Matrix instruction | `mma` / `wgmma` | **MFMA** (`v_mfma_f32_16x16x16_bf16`, `32x32x8`, ...) |
| On-chip scratchpad | shared memory (up to ~228 KB/SM on H100) | **LDS**: 64 KB per CU on MI300X, 160 KB on MI350-series |
| Async copy / TMA | `cp.async`, TMA, warp specialization | No TMA on CDNA3; software pipelining through registers and LDS |

AMD-specific `triton.Config` knobs (from AMD's MI300X workload-optimization guide and the Triton HIP tutorials):

| Knob | Meaning | Guidance |
|---|---|---|
| `matrix_instr_nonkdim` | MFMA tile shape: 16 → `mfma_16x16`, 32 → `mfma_32x32` | On MI300X, 16 usually wins |
| `waves_per_eu` | Occupancy hint: the compiler limits VGPRs per wave so that N waves fit per SIMD (EU) | Try 0 (no hint), 1, 2, 3. Higher means fewer registers per wave and possible spills |
| `num_stages` | Software-pipelining depth | AMD guidance: **2** for a single GEMM, **1** for fused GEMM chains and non-GEMM kernels (stages cost LDS) |
| `num_warps` | Wavefronts per workgroup | 4 or 8 typical for GEMM. Remember each is 64 lanes |
| `BLOCK_M/N/K` | Tile sizes | Constrained by LDS: a 256×64 A tile plus a 64×256 B tile in BF16 is 32 KB + 32 KB = the whole 64 KB, so `num_stages=2` does not fit on MI300X ("out of resources: shared memory") |

```python
# fragment -- AMD-aware autotune configs (AMD knobs ride in the kwargs dict)
import triton

def is_hip() -> bool:
    return triton.runtime.driver.active.get_current_target().backend == "hip"

def gemm_configs():
    if is_hip():
        return [
            triton.Config({"BLOCK_M": 256, "BLOCK_N": 256, "BLOCK_K": 32, "GROUP_M": 8,
                           "waves_per_eu": 2, "matrix_instr_nonkdim": 16}, num_warps=8, num_stages=2),
            triton.Config({"BLOCK_M": 128, "BLOCK_N": 128, "BLOCK_K": 64, "GROUP_M": 8,
                           "waves_per_eu": 0, "matrix_instr_nonkdim": 16}, num_warps=4, num_stages=2),
        ]
    return [triton.Config({"BLOCK_M": 128, "BLOCK_N": 256, "BLOCK_K": 64, "GROUP_M": 8},
                          num_warps=8, num_stages=3)]
```

**Inspecting what the compiler did:**
- `AMDGCN_ENABLE_DUMP=1` prints the ISA. Check the VGPR/SGPR counts, the LDS size, and any `scratch` (register spills).
- `MLIR_ENABLE_DUMP=1` dumps every MLIR pass, which shows layouts and whether `tl.dot` became MFMA.
- Compiled artifacts (`.amdgcn`, `.hsaco`, `.json` metadata) are cached under `~/.triton/cache` (`TRITON_CACHE_DIR`).

Occupancy is VGPR-limited far more often than on NVIDIA: 512 VGPRs per SIMD lane shared among resident waves means a kernel using 256 VGPRs gets at most 2 waves per SIMD.

## 47.5 vLLM and SGLang on ROCm

- **Builds:** AMD publishes ROCm images (`rocm/vllm`, `rocm/sgl-dev`, and upstream `lmsysorg/sglang:*-rocm*`) with tuned PyTorch, Triton, hipBLASLt, RCCL, and AITER already combined. Prefer them over building from source unless you are developing the stack.
- **AITER switch:** in vLLM, `VLLM_ROCM_USE_AITER=1` (default off) is the master switch. Per-op sub-switches (`VLLM_ROCM_USE_AITER_MHA`, `_MLA`, `_MOE`, `_RMSNORM`, `_LINEAR`, ...) default to on once it is set. SGLang uses `SGLANG_USE_AITER=1` with `--attention-backend aiter`. `--attention-backend triton` is the fallback when an AITER kernel fails on a given GPU or dtype.
- **Other ROCm-specific paths in vLLM:**
  - "Skinny" GEMM kernels for the small-M GEMMs of low-batch decode (`VLLM_ROCM_USE_SKINNY_GEMM`).
  - Quick Reduce, a quantized custom all-reduce for TP (`VLLM_ROCM_QUICK_REDUCE_QUANTIZATION`).
  - FP8 weight padding.
  - FP8 OCP-to-FNUZ checkpoint conversion on gfx942.
- **Memory changes the parallelism choice.** At 192 GB (MI300X) or 256 GB (MI325X), a 70B model in BF16 (~140 GB) fits on **one** GPU. For throughput, 8 independent TP=1 replicas (or DP attention) often beat one TP=8 instance because they skip the all-reduces. TP=2-8 is chosen for latency (TTFT/TPOT) or for longer contexts that need KV-cache room. Running the numbers per model is the interview answer. See [ML Systems Design](../ml-gpu/ML_Systems_Design.md).
- **Graphs:** vLLM captures HIP graphs for a set of decode batch sizes, just as on CUDA. `--enforce-eager` disables them, which is useful for debugging and costly for small-batch latency.

## 47.6 Environment Variable Cheat Sheet

| Variable | Purpose |
|---|---|
| `ROCR_VISIBLE_DEVICES`, `HIP_VISIBLE_DEVICES` | GPU selection (ROCr-level vs HIP-level; see 47.1) |
| `TORCH_BLAS_PREFER_HIPBLASLT=1` | Prefer hipBLASLt over rocBLAS for GEMMs |
| `PYTORCH_TUNABLEOP_ENABLED/TUNING/FILENAME/VERBOSE/RECORD_UNTUNED` | TunableOp (47.3) |
| `TORCH_ROCM_FA_PREFER_CK=1` | CK instead of AOTriton for SDPA flash attention |
| `PYTORCH_HIP_ALLOC_CONF=expandable_segments:True` | Caching-allocator config (the HIP spelling of `PYTORCH_CUDA_ALLOC_CONF`); reduces fragmentation OOMs |
| `TORCHINDUCTOR_MAX_AUTOTUNE=1`, `TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS` | Inductor autotuning |
| `MIOPEN_FIND_MODE` (`NORMAL`/`FAST`/default `DYNAMIC_HYBRID`), `MIOPEN_USER_DB_PATH` | Convolution solver search vs startup time; where tuning results persist |
| `NCCL_DEBUG=INFO`, `NCCL_MIN_NCHANNELS=112` | RCCL logging; more channels (AMD's MI300X recommendation for end-to-end workloads) |
| `HIP_FORCE_DEV_KERNARG=1` | Put kernel arguments in device memory (lower launch latency; in AMD's MI300X tuning guide) |
| `AMD_SERIALIZE_KERNEL=3` | Serialize kernel launches so errors surface at the faulting call (the ROCm analog of `CUDA_LAUNCH_BLOCKING=1`) |
| `AMD_LOG_LEVEL=3` (1-4) | HIP runtime API logging |
| `VLLM_ROCM_USE_AITER=1`, `SGLANG_USE_AITER=1` | AITER kernels in vLLM / SGLang |
| `AMDGCN_ENABLE_DUMP=1`, `MLIR_ENABLE_DUMP=1`, `TRITON_CACHE_DIR` | Triton ISA/IR inspection |

Version caveat: these names are current for ROCm 6.4-7.x and PyTorch 2.8+. vLLM's `VLLM_ROCM_*` flags in particular change between releases. Check `vllm/envs.py` for the version you deploy.

## 47.7 Interview Questions

**Q1.** "How can `torch.cuda.is_available()` be True on an AMD GPU?"

**A.** PyTorch's ROCm build is produced by hipifying the CUDA sources at build time and compiling them with the ROCm toolchain. The Python and dispatcher layers deliberately keep the `cuda` names, so `torch.cuda`, `"cuda"` devices, streams, events, graphs, and the `"nccl"` backend are HIP- and RCCL-backed. Model code is unchanged. You tell the builds apart with `torch.version.hip`. Custom CUDA extensions are hipified too, but warp-32 assumptions and inline PTX must be fixed by hand.

**Q2.** A GEMM-heavy training step is 30% slower on MI300X than expected from peak-FLOP ratios. What do you check, in order?

**A.**
1. Profile and confirm GEMMs dominate. Check which library ran: Tensile `Cijk_*` kernels from hipBLASLt vs rocBLAS, or Triton kernels from Inductor.
2. Check dtypes: an FP32 matmul without TF32 runs at a fraction of BF16 throughput.
3. Run TunableOp on the real shapes, and try `TORCH_BLAS_PREFER_HIPBLASLT=1`.
4. Check shape alignment: dimensions that are not multiples of 64/128 cause padding or slow paths.
5. Check SDPA: confirm it hit AOTriton or CK flash attention rather than the math fallback, which materializes s².
6. Check Triton/Inductor kernels for NVIDIA-tuned configs (enable max-autotune, which includes the AMD knobs).
7. For multi-GPU, check RCCL settings and comm/compute overlap, and remember that RCCL kernels occupy CUs.
8. Rule out clocks or power capping (`amd-smi metric`).
9. Then go per kernel: rocprof-compute roofline and counters on the top kernel.

**Q3.** A Triton kernel autotuned on H100 is slow on MI300X. Why, and what do you change?

**A.** Its configs encode NVIDIA assumptions:
- `num_warps` means twice as many threads on AMD (wave64), which raises register pressure per workgroup.
- `num_stages=3-4` assumes cp.async/TMA and up to ~228 KB of shared memory, while MI300X has 64 KB LDS per CU and AMD recommends `num_stages=2` for GEMMs.
- Tile shapes should match MFMA shapes (`matrix_instr_nonkdim=16`).
- `waves_per_eu` should be tuned to balance occupancy against spills.

Add AMD-specific configs gated on `is_hip()`. Check ISA for VGPR count and scratch spills with `AMDGCN_ENABLE_DUMP=1`, and re-autotune on the target.

**Q4.** Why does AITER exist if hipBLASLt, MIOpen, and CK already exist?

**A.** LLM serving is dominated by a handful of fused, shape-specific ops: paged/MLA decode attention, fused MoE with block-scaled FP8, fused RMSNorm+quant, and small-message all-reduce. General libraries don't cover these or are not optimal for them. AITER is a curated, Python-callable collection of the fastest available implementation per op (CK, Triton, or hand-tuned assembly), wired into vLLM and SGLang behind flags. It is the AMD analog of FlashInfer plus the custom kernels inside NVIDIA-tuned serving stacks.

**Q5.** You deploy Llama-70B on an 8×MI300X node. TP=8 or 8×TP=1?

**A.** Weights are ~140 GB in BF16, so TP=1 fits but leaves only ~30 GB for KV cache (~90K tokens at 0.33 MB/token). 8×TP=1 maximizes aggregate throughput (no all-reduce, independent schedulers) but limits per-replica concurrency and context length. TP=8 gives each request 8× the HBM bandwidth (lower TPOT) and ~1.2 TB of KV space in one instance (≈3.8M tokens at 0.33 MB/token): about 40× a single TP=1 replica and about 5× the combined KV space of eight replicas, because the 140 GB of weights is stored once instead of 8 times. The cost is 2 all-reduces per layer. A middle ground such as 4×TP=2 or 2×TP=4 is often the throughput-under-SLO optimum. Measure goodput (requests/s meeting TTFT/TPOT targets) for the real traffic mix. FP8 weights (~70 GB) shift the answer toward more, smaller replicas.

---

# 48. Debugging a Slow Training Step

---

"Your training job got 2× slower" or "GPU utilization is 40%, fix it" is a very common ML-infra interview prompt. A strong answer is a **method**: measure, classify the bottleneck, test the hypothesis with a cheap experiment, fix, and re-measure. See also [Performance Engineering](../computer-science/Performance_Engineering.md#3-roofline-model) for roofline thinking, [Timing GPUs](../computer-science/Performance_Engineering.md#87-timing-gpus), and [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md).

## 48.1 Step-Time Anatomy and MFU

```text
step time = data wait + H2D copy + forward + backward + exposed communication
          + optimizer + host-device sync stalls + logging/checkpoint I/O
```

Start from **throughput (tokens/s or samples/s)** and **MFU**, not "GPU utilization". `amd-smi`/`nvidia-smi` utilization only reports that *some* kernel was running during the sample window. A single tiny kernel at a time shows 100%.

```text
MFU = (model FLOPs per step / step time) / (num_GPUs × peak FLOP/s)
dense transformer training: model FLOPs ≈ 6 × N_params × tokens  (+ attention term 12·L·h·s per token)

Example: 8B model, 8 × MI300X (peak dense BF16 ≈ 1307 TFLOP/s each), 80K tokens/s total
  6 × 8e9 × 80,000 = 3.84e15 FLOP/s  /  (8 × 1.307e15)  =  37% MFU
Healthy large-scale dense training is typically ~35-55% MFU; under ~25% means something is wrong.
```

## 48.2 Classify the Regime

| Regime | Trace signature | Quick confirming experiment | Typical fixes |
|---|---|---|---|
| **Input-bound** (dataloader starvation) | GPU idle at the start of each step; long `enumerate(DataLoader)#_next_data` on CPU | Replace the loader with one cached batch reused forever. If step time drops, it was data | More `num_workers`, `pin_memory`, prefetch, move augmentation to GPU, pre-tokenize, faster storage |
| **CPU launch-bound** | GPU stream full of short kernels with gaps between them; Python thread at 100% | Double the batch size. If step time barely changes, it was launch-bound | `torch.compile` (fusion), CUDA/HIP graphs (`reduce-overhead`), bigger batch, fused optimizers (`foreach`/`fused=True`) |
| **GPU compute-bound** | Back-to-back kernels, GEMM/attention dominate | Per-kernel achieved TFLOP/s vs peak | Better kernels (TunableOp, flash attention), FP8, avoid FP32 matmuls |
| **GPU memory-bound** | Elementwise, norm, and softmax kernels take a large share | Roofline of the top kernels | Fusion (`torch.compile`), fused norms and optimizers, fewer dtype casts |
| **Communication-bound** | Long RCCL/NCCL kernels not overlapped with compute; scaling efficiency falls with node count | Compare 1 GPU vs 8 vs 64 at fixed per-GPU batch | Bucket tuning, overlap, gradient accumulation (`no_sync`), HSDP, check topology and NIC binding |
| **Sync-bound** | `hipStreamSynchronize`/`cudaStreamSynchronize` or `aten::_local_scalar_dense` on the CPU row, GPU idle right after | `torch.cuda.set_sync_debug_mode("warn")` | Remove `.item()`/`print`/`.cpu()` from the hot loop; log every N steps |
| **Straggler** (multi-node) | All ranks wait in the same all-reduce; one rank's compute is longer | Per-rank step-time histogram | Find the bad node: clocks or thermals, ECC errors, slow NIC, noisy CPU neighbor |

## 48.3 Dataloader Starvation

| Knob | What it does | Guidance |
|---|---|---|
| `num_workers` | Worker *processes* producing batches in parallel | Start at the number of CPU cores per GPU (e.g. 8-12), then measure. Too many costs RAM (each worker holds a copy of the dataset object) and causes contention |
| `pin_memory=True` | Batches land in page-locked host memory | Enables truly async H2D copies with `.to(dev, non_blocking=True)`. Pageable copies are staged and synchronous with respect to the host |
| `prefetch_factor` | Batches each worker prepares ahead (default 2) | Raise it to absorb jitter in per-batch cost; memory grows with `workers × prefetch` |
| `persistent_workers=True` | Keep workers alive across epochs | Avoids re-forking and re-initializing (opening files, tokenizers) every epoch |
| Placement | Data decode on CPU vs GPU | Heavy image or video decode belongs on the GPU (DALI, torchvision GPU decode). Text should be pre-tokenized offline |

```python
# data_wait.py -- measure how much of each step is spent waiting for the DataLoader
import time
import torch
from torch.utils.data import DataLoader, Dataset

class SlowDecode(Dataset):
    """Simulates CPU-heavy decode/augmentation: ~2 ms per sample."""
    def __len__(self):
        return 2048
    def __getitem__(self, i):
        time.sleep(0.002)
        return torch.randn(3, 64, 64), i % 10

def run(num_workers: int, device: str) -> None:
    loader = DataLoader(SlowDecode(), batch_size=32, num_workers=num_workers,
                        pin_memory=(device == "cuda"), persistent_workers=num_workers > 0,
                        prefetch_factor=4 if num_workers > 0 else None)
    model = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(3 * 64 * 64, 10)).to(device)
    opt = torch.optim.SGD(model.parameters(), lr=0.01)
    wait = compute = 0.0
    t0 = time.perf_counter()
    for x, y in loader:
        t1 = time.perf_counter()
        wait += t1 - t0                                    # time blocked in next(loader)
        x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
        loss = torch.nn.functional.cross_entropy(model(x), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if device == "cuda":
            torch.cuda.synchronize()                       # demo only: make compute time honest
        t0 = time.perf_counter()
        compute += t0 - t1
    total = wait + compute
    print(f"num_workers={num_workers}: total {total:5.2f}s, waiting for data {100 * wait / total:4.1f}%")

if __name__ == "__main__":                                 # guard required for worker processes
    dev = "cuda" if torch.cuda.is_available() else "cpu"   # "cuda" is also the ROCm device string
    for w in (0, 4, 8):
        run(w, dev)
```

On a CPU-only machine this prints roughly 4.4 s / 1.7 s / 0.6 s total, with the data-wait share still above 90% at 8 workers. The arithmetic explains it: one batch costs 32 × 2 ms = 64 ms of CPU, so keeping up with a step of S ms needs at least `64 / S` workers. When compute per step is tiny, no reasonable worker count keeps up, and the decode itself has to get cheaper. Run the same arithmetic in an interview: per-sample CPU cost × batch ÷ step time = workers needed.

## 48.4 Host-Device Sync Points

PyTorch GPU ops are asynchronous: the CPU enqueues kernels and runs ahead. Anything that needs a GPU *value* on the CPU blocks until the queue drains. That empties the pipeline, and the GPU then idles while Python launches the next kernels.

| Hidden sync | Why it syncs | Alternative |
|---|---|---|
| `loss.item()`, `float(t)`, `t.tolist()`, `print(t)` | Copies a value to the host | Accumulate on device (`running += loss.detach()`), read every N steps |
| `if (t > 0).any():` and Python control flow on tensors | Needs the boolean on the host | `torch.where`, masking, `torch.cond` |
| `x[mask]`, `torch.nonzero`, `torch.unique`, `torch.masked_select` | Output **shape** depends on data | Fixed-shape formulations (`torch.where`, padding, `torch.nonzero_static` where available) |
| `.cpu()`, `.to("cpu")`, `.numpy()` | D2H copy | `non_blocking=True` into pinned memory, then sync once |
| `torch.cuda.synchronize()`, `torch.cuda.empty_cache()` in the loop | Explicit or implicit sync | Remove from the hot path |
| Gradient clipping that checks for `inf` in Python, some `GradScaler` paths | Reads the found-inf flag | Use the fused or foreach implementations, which keep the flag on device |

Detection: `torch.cuda.set_sync_debug_mode("warn")` (or `"error"`) reports every synchronizing call with a stack trace. In a trace, look for long `hipStreamSynchronize`/`cudaStreamSynchronize`/`hipMemcpyWithStream` calls on the CPU row followed by a GPU gap.

## 48.5 Reading a `torch.profiler` Trace

```python
# fragment -- profile a few steady-state steps with named regions
from torch.profiler import profile, record_function, schedule, ProfilerActivity

def trace_handler(p):
    p.export_chrome_trace(f"trace_rank{rank}_step{p.step_num}.json")   # open in https://ui.perfetto.dev
    print(p.key_averages().table(sort_by="self_cuda_time_total", row_limit=15))

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],  # CUDA activity = HIP on ROCm
             schedule=schedule(skip_first=10, wait=1, warmup=2, active=3, repeat=1),
             on_trace_ready=trace_handler, record_shapes=True, with_stack=False) as prof:
    for step, batch in enumerate(loader):
        with record_function("## data_to_device ##"):
            batch = {k: v.to(device, non_blocking=True) for k, v in batch.items()}
        with record_function("## forward ##"):
            loss = model(**batch).loss
        with record_function("## backward ##"):
            loss.backward()
        with record_function("## optimizer ##"):
            optimizer.step(); optimizer.zero_grad(set_to_none=True)
        prof.step()                                    # advances the schedule
```

- **Schedule:** `skip_first` skips compile and warmup steps, `wait` steps are ignored, `warmup` steps are traced but discarded (profiler startup overhead), and `active` steps are recorded. Profile steady state only, a few steps, and only on rank 0 plus one suspicious rank. Traces get large fast. `with_stack=True` and `profile_memory=True` add significant overhead.
- **Reading it in Perfetto:**
  1. Find the step boundaries (`ProfilerStep#N`).
  2. On the **GPU stream rows**, look for gaps. Idle GPU time is the money.
  3. Click a kernel to follow the **flow arrow** back to the CPU op that launched it. If kernels start right after their launch, the GPU is starving: launch-bound or sync-bound. If launches run far ahead of execution, the GPU is the bottleneck, which is good.
  4. On the communication stream, check whether RCCL kernels overlap compute kernels.
  5. Use your `record_function` ranges to attribute time to phases.
- **Distributed:** Holistic Trace Analysis (HTA, `pip install HolisticTraceAnalysis`) reads per-rank traces and reports idle, compute, and communication breakdowns and the comm/compute overlap percentage per rank.

## 48.6 Overlapping Communication with Compute

- **DDP** buckets gradients (`bucket_cap_mb`, default 25) and launches each bucket's all-reduce as soon as its gradients are ready, overlapping with the rest of backward. The *last* bucket (first layers) cannot overlap. Exposed comm ≈ last bucket + any slow collective. Tune `bucket_cap_mb`: bigger buckets mean fewer, more efficient collectives but less overlap. `gradient_as_bucket_view=True` saves a copy.
- **Gradient accumulation:** wrap the non-final micro-steps in `model.no_sync()` (DDP) or the FSDP equivalent, so you all-reduce once per optimizer step instead of once per micro-batch.
- **FSDP/ZeRO-3:** overlap is all about *prefetching* the next unit's all-gather (FSDP1 `backward_prefetch=BACKWARD_PRE`, `forward_prefetch=True`; FSDP2 prefetches by default). Unit granularity matters: one unit per transformer block is the norm.
- **Comm kernels use CUs.** On AMD (and NVIDIA) collective kernels run on compute units. Overlapped compute kernels slow down a little, and more RCCL channels (`NCCL_MIN_NCHANNELS`) means faster comm but more CUs taken from compute. Measure end-to-end.
- **Cost check:** ring all-reduce time ≈ `2(N-1)/N × bytes / busbw`. Measure `busbw` with `rccl-tests` (`all_reduce_perf`) on the same nodes, and compare with what the trace shows. If the trace is much slower, suspect topology (NIC-GPU NUMA affinity), the wrong transport, or contention. See [Collective Communication](../ml-gpu/Parallel_GPU_Programming.md#3-collective-communication).

## 48.7 Going Below PyTorch: rocprofv3, rocprof-sys, rocprof-compute

`torch.profiler` (Kineto) gives framework ops, kernels, and correlation, but no hardware counters and limited host-side visibility. The ROCm tools fill in the rest:

| Question | Tool | Example |
|---|---|---|
| Which kernels, API calls, and copies, and for how long? | `rocprofv3` (rocprofiler-sdk) | `rocprofv3 --runtime-trace --stats --output-format pftrace -d ./prof -- python train.py --steps 20` |
| Only some kernels / my phase markers | `rocprofv3` filters and markers | `--kernel-include-regex 'Cijk_.*'`; `--marker-trace` for ROCTx ranges |
| Whole-system timeline: Python stacks, CPU threads, sampling, GPU activity, RCCL in one Perfetto view | `rocprof-sys` (ROCm Systems Profiler) | `rocprof-sys-python -- train.py` |
| Why is *this kernel* slow (roofline, occupancy, cache hit rates, LDS bank conflicts)? | `rocprof-compute` (ROCm Compute Profiler) | `rocprof-compute profile -n step -k <kernel_name> -- python train.py`, then `rocprof-compute analyze -p workloads/step/<gpu>` |

**Correlating across tools:**
1. Use **the same few steady-state steps**: gate them with an environment flag or step range in your script, because the overhead of these tools is significant.
2. **Kernel names** are the join key between the torch.profiler trace and rocprofv3 output. GEMMs show up as Tensile `Cijk_*`, Triton kernels as `triton_*` names from Inductor.
3. **ROCTx ranges** let you see phases in rocprofv3 and rocprof-sys timelines: emit them around forward, backward, and optimizer. On ROCm builds, `torch.cuda.nvtx.range_push/pop` is backed by ROCTx. Verify with a one-line test that the ranges appear under `--marker-trace` for your PyTorch/ROCm pairing, since the backing library has changed across releases.
4. Avoid stacking profilers (torch.profiler and rocprofv3 in the same run): both subscribe to the same runtime callbacks, which adds overhead and can drop records.

The workflow is: torch.profiler finds the slow *phase*, rocprofv3 or rocprof-sys show *what the GPU and host were doing*, and rocprof-compute explains *why a specific kernel* is slow. See [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md) and [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md).

## 48.8 Hangs and Stragglers at Scale

- **Straggler:** every rank's all-reduce time is long except one rank's, because everyone else is waiting for it. Log per-rank step and compute time, and compare. Typical causes are a throttled GPU (check clocks and temperature with `amd-smi`), a degraded link, ECC page retirement, or a CPU-side issue (another process, wrong NUMA binding).
- **Hang:** a collective mismatch (one rank skipped a collective, or ranks issued them in a different order). Tools:
  - `NCCL_DEBUG=INFO` (RCCL honors it).
  - The process-group timeout (`init_process_group(timeout=...)`).
  - PyTorch's NCCL **Flight Recorder**: `TORCH_NCCL_TRACE_BUFFER_SIZE=N` (records the last N collectives per rank) plus `TORCH_NCCL_DUMP_ON_TIMEOUT=1` (writes one file per rank on timeout, prefix set by `TORCH_FR_DUMP_TEMP_FILE`, default `/tmp/nccl_trace_rank_`). Diff the dumps across ranks (e.g. with `torchfrtrace`) to find the odd one out.
  - `py-spy dump --pid` on every rank to see Python stacks.

## 48.9 Interview Questions

**Q1.** "Our training job went from 1.0 s/step to 2.0 s/step after last week's changes. Walk me through debugging it."

**A.**
1. **Reproduce and bound it.** Is it every step or periodic? All ranks or one? Diff the changes (code, data, container or ROCm version, cluster). Periodic slowness points at checkpointing, eval, or GC. One rank points at a straggler.
2. **Measure the phases.** Capture a torch.profiler trace of 3 steady-state steps, before and after if possible, with `record_function` ranges.
3. **Classify:**
   - A GPU gap at step start means data.
   - Short kernels with gaps mean launch-bound, often a new graph break or `torch.compile` falling back to eager after recompiles.
   - Long sync calls mean a newly added `.item()` or `print`.
   - Longer comm kernels mean communication: a topology change, a NIC down, or a changed bucket size.
   - Longer GEMMs mean a library or kernel-selection change (new ROCm, TunableOp table invalidated, dtype silently FP32).
4. **Confirm with a cheap experiment:** synthetic data, 1-node vs multi-node, `TORCH_LOGS=recompiles`, `set_sync_debug_mode`.
5. **Fix, re-measure, and add a regression guard,** such as a step-time and MFU check in CI on a small config.

**Q2.** GPU utilization reads 100% but MFU is 15%. How is that possible?

**A.** Utilization counts time with *any* kernel resident, not how much of the GPU it uses. Low MFU with "100% utilization" means the time goes to kernels far from peak:
- Memory-bound elementwise or norm kernels.
- Small GEMMs that can't fill 304 CUs.
- FP32 instead of BF16.
- Unfused attention.
- Comm kernels counted as busy.
- Recompute (HFU > MFU).

Fixes come from the per-kernel time breakdown: fuse (compile), use bigger tiles or batches, use flash attention, and check dtypes. Then use rocprof-compute on the top kernels to see achieved vs peak.

**Q3.** Why is `print(f"loss={loss.item()}")` every step a problem, and how do you log without it?

**A.** `.item()` forces a device-to-host copy, which waits for every queued kernel (the whole forward and backward) to finish. The CPU can no longer run ahead to enqueue the next step, so the GPU idles during Python's launch overhead at the start of every step. That is a few percent to tens of percent of throughput for small models. Instead, accumulate `loss.detach()` into a device tensor and call `.item()` every N steps, or copy to pinned memory with `non_blocking=True` and read it a step later.

**Q4.** How do you tell whether a job is communication-bound, and what are your levers?

**A.** In the trace, measure *exposed* comm time: collective kernels that don't overlap compute. Compare step time at 1, 8, and 64 GPUs with a fixed per-GPU batch. Weak-scaling efficiency below ~90% across nodes, with the extra time in collectives, indicates comm-bound. Then validate bandwidth with rccl-tests against the alpha-beta estimate `2(N-1)/N × bytes / busbw`. Levers:
- Overlap (buckets, prefetch).
- Fewer bytes: BF16 gradient reduction, ZeRO-1/2 instead of 3, gradient accumulation with `no_sync`.
- Topology-aware parallelism: TP inside a node only, HSDP, EP intra-node.
- Fabric fixes: NIC/GPU affinity, RCCL channels.
- Larger per-GPU batch to raise the compute-to-communication ratio.

**Q5.** Compute the MFU: 70B dense model, 512 GPUs at 1300 TFLOP/s peak BF16, global batch of 4M tokens per step, 25 s per step.

**A.** Model FLOPs per step ≈ 6 × 70e9 × 4e6 = 1.68e18. Achieved = 1.68e18 / 25 s = 6.72e16 FLOP/s. Peak = 512 × 1.3e15 = 6.656e17 FLOP/s. MFU ≈ **10.1%**, which is poor. Expect 35-50%. Suspects: excessive recompute (check HFU), exposed PP bubbles or communication, small micro-batches, or data starvation. Next step: profile one rank's step and apply the 48.2 classification.
