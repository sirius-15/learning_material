# LLM and ML Fundamentals -- Comprehensive Interview Reference

> An interview-focused reference for the theory under the frameworks: classic ML fundamentals (generalization, backpropagation, normalization, optimizers, metrics), the Transformer architecture with parameter and FLOP accounting, FlashAttention and the online-softmax trick, the math of LLM inference (prefill vs decode, KV cache, batching, serving metrics, quantization), and number formats for mixed-precision training. Every major section ends with interview questions and full answers. Targeted at ML-infra, GPU/HPC, and general big-tech SWE loops. It complements the framework-level [ML and AI Frameworks](../ml-gpu/ML_AI_Frameworks.md) guide and the design-interview walkthroughs in [ML Systems Design](../ml-gpu/ML_Systems_Design.md).

> Last reviewed: 2026-11 · Versions assumed: PyTorch 2.x, FlashAttention 2.x (CUDA, and ROCm via CK or Triton/aiter backends) and FlashAttention-3 (Hopper), vLLM V1 engine, OCP 8-bit floating point (OFP8) and OCP Microscaling (MX) v1.0 specs, AMD Instinct MI300X (CDNA 3) vendor-published dense peaks (1307.4 TFLOP/s FP16/BF16 matrix, 5.3 TB/s HBM3, 192 GB)

Every complete Python program in this file runs with Python 3.10+ and NumPy 1.24+ (the ones that do not import NumPy need only the standard library). Outputs shown were produced by running them. Error magnitudes at the 1e-9 to 1e-15 level (gradient checks, flash-vs-naive differences) depend on the NumPy/BLAS build and may differ in the last digits; the pass/fail conclusions do not.

---

## Table of Contents

### Part 1: ML Fundamentals

1. [Supervised Learning, Generalization, and Regularization](#1-supervised-learning-generalization-and-regularization)
    - [1.1 The Supervised Learning Setup](#11-the-supervised-learning-setup)
    - [1.2 Bias-Variance Decomposition](#12-bias-variance-decomposition)
    - [1.3 Underfitting vs Overfitting](#13-underfitting-vs-overfitting)
    - [1.4 Regularization: L1, L2, Dropout, Early Stopping](#14-regularization-l1-l2-dropout-early-stopping)
    - [1.5 Weight Decay vs L2 Under Adam](#15-weight-decay-vs-l2-under-adam)
    - [1.6 Interview Questions](#16-interview-questions)
2. [Backpropagation](#2-backpropagation)
    - [2.1 Chain Rule and Reverse-Mode Differentiation](#21-chain-rule-and-reverse-mode-differentiation)
    - [2.2 Softmax + Cross-Entropy Gradient: p - y](#22-softmax--cross-entropy-gradient-p---y)
    - [2.3 Worked Example: a 2-Layer MLP](#23-worked-example-a-2-layer-mlp)
    - [2.4 Vanishing and Exploding Gradients](#24-vanishing-and-exploding-gradients)
    - [2.5 Interview Questions](#25-interview-questions)
3. [Normalization and Optimizers](#3-normalization-and-optimizers)
    - [3.1 BatchNorm vs LayerNorm vs RMSNorm](#31-batchnorm-vs-layernorm-vs-rmsnorm)
    - [3.2 SGD and Momentum](#32-sgd-and-momentum)
    - [3.3 Adam and AdamW](#33-adam-and-adamw)
    - [3.4 Learning-Rate Schedules](#34-learning-rate-schedules)
    - [3.5 Interview Questions](#35-interview-questions)
4. [Evaluation, Data Leakage, and Cross-Validation](#4-evaluation-data-leakage-and-cross-validation)
    - [4.1 Confusion Matrix, Precision, Recall, F1](#41-confusion-matrix-precision-recall-f1)
    - [4.2 ROC-AUC vs PR-AUC](#42-roc-auc-vs-pr-auc)
    - [4.3 Calibration](#43-calibration)
    - [4.4 Perplexity](#44-perplexity)
    - [4.5 Metrics From Scratch](#45-metrics-from-scratch)
    - [4.6 Data Leakage](#46-data-leakage)
    - [4.7 Cross-Validation](#47-cross-validation)
    - [4.8 Interview Questions](#48-interview-questions)

### Part 2: Transformers

5. [Attention](#5-attention)
    - [5.1 Scaled Dot-Product Attention](#51-scaled-dot-product-attention)
    - [5.2 Why the sqrt(d_k) Scaling](#52-why-the-sqrtd_k-scaling)
    - [5.3 Multi-Head Attention Shapes](#53-multi-head-attention-shapes)
    - [5.4 Causal Masking](#54-causal-masking)
    - [5.5 Positional Encodings: Sinusoidal, Learned, RoPE, ALiBi](#55-positional-encodings-sinusoidal-learned-rope-alibi)
    - [5.6 MQA and GQA](#56-mqa-and-gqa)
    - [5.7 Reference Implementation: GQA + RoPE + Causal Mask](#57-reference-implementation-gqa--rope--causal-mask)
    - [5.8 Interview Questions](#58-interview-questions)
6. [The Transformer Decoder Block](#6-the-transformer-decoder-block)
    - [6.1 Pre-Norm vs Post-Norm](#61-pre-norm-vs-post-norm)
    - [6.2 Feed-Forward Networks: GELU and SwiGLU](#62-feed-forward-networks-gelu-and-swiglu)
    - [6.3 Mixture of Experts Routing](#63-mixture-of-experts-routing)
    - [6.4 Parameter Count of a Decoder Layer](#64-parameter-count-of-a-decoder-layer)
    - [6.5 Interview Questions](#65-interview-questions)
7. [FLOP Accounting and Scaling Laws](#7-flop-accounting-and-scaling-laws)
    - [7.1 Forward Pass: About 2N FLOPs per Token](#71-forward-pass-about-2n-flops-per-token)
    - [7.2 Training: About 6ND](#72-training-about-6nd)
    - [7.3 The Attention FLOP Term](#73-the-attention-flop-term)
    - [7.4 Calculator and Worked Training-Time Estimate](#74-calculator-and-worked-training-time-estimate)
    - [7.5 Scaling Laws: Kaplan vs Chinchilla](#75-scaling-laws-kaplan-vs-chinchilla)
    - [7.6 Interview Questions](#76-interview-questions)

### Part 3: FlashAttention

8. [FlashAttention](#8-flashattention)
    - [8.1 Why Standard Attention Is Memory-Bound](#81-why-standard-attention-is-memory-bound)
    - [8.2 The Online Softmax Recurrence](#82-the-online-softmax-recurrence)
    - [8.3 Tiled Forward Pass: NumPy Reference](#83-tiled-forward-pass-numpy-reference)
    - [8.4 Backward Pass and Recomputation](#84-backward-pass-and-recomputation)
    - [8.5 FlashAttention-2](#85-flashattention-2)
    - [8.6 FlashAttention-3](#86-flashattention-3)
    - [8.7 FlashAttention on AMD GPUs](#87-flashattention-on-amd-gpus)
    - [8.8 Interview Questions](#88-interview-questions)

### Part 4: LLM Inference

9. [Prefill, Decode, and the KV Cache](#9-prefill-decode-and-the-kv-cache)
    - [9.1 Prefill vs Decode: Arithmetic Intensity](#91-prefill-vs-decode-arithmetic-intensity)
    - [9.2 KV Cache Sizing With GQA](#92-kv-cache-sizing-with-gqa)
    - [9.3 Decode Throughput Upper Bound and Batching Math](#93-decode-throughput-upper-bound-and-batching-math)
    - [9.4 Interview Questions](#94-interview-questions)
10. [Serving Metrics and Scheduling](#10-serving-metrics-and-scheduling)
    - [10.1 TTFT, TPOT, ITL, Throughput, Goodput](#101-ttft-tpot-itl-throughput-goodput)
    - [10.2 Continuous Batching](#102-continuous-batching)
    - [10.3 Paged Attention](#103-paged-attention)
    - [10.4 Chunked Prefill](#104-chunked-prefill)
    - [10.5 Prefill-Decode Disaggregation](#105-prefill-decode-disaggregation)
    - [10.6 Speculative Decoding](#106-speculative-decoding)
    - [10.7 Interview Questions](#107-interview-questions)
11. [Quantization for Inference](#11-quantization-for-inference)
    - [11.1 Quantization Basics and Granularity](#111-quantization-basics-and-granularity)
    - [11.2 Weight-Only INT8 and INT4](#112-weight-only-int8-and-int4)
    - [11.3 GPTQ, AWQ, and SmoothQuant](#113-gptq-awq-and-smoothquant)
    - [11.4 FP8 Inference](#114-fp8-inference)
    - [11.5 KV-Cache Quantization](#115-kv-cache-quantization)
    - [11.6 Interview Questions](#116-interview-questions)

### Part 5: Mixed Precision and Number Formats

12. [Floating-Point Formats for ML](#12-floating-point-formats-for-ml)
    - [12.1 Bit Layouts and Ranges](#121-bit-layouts-and-ranges)
    - [12.2 FP8: E4M3 vs E5M2, OCP vs FNUZ](#122-fp8-e4m3-vs-e5m2-ocp-vs-fnuz)
    - [12.3 Microscaling Formats: MXFP8, MXFP6, MXFP4](#123-microscaling-formats-mxfp8-mxfp6-mxfp4)
    - [12.4 Interview Questions](#124-interview-questions)
13. [Mixed-Precision Training](#13-mixed-precision-training)
    - [13.1 The Standard Recipe](#131-the-standard-recipe)
    - [13.2 Loss Scaling](#132-loss-scaling)
    - [13.3 FP8 Scaling Recipes](#133-fp8-scaling-recipes)
    - [13.4 Accumulation Precision](#134-accumulation-precision)
    - [13.5 Interview Questions](#135-interview-questions)
14. [Formula Cheat Sheet](#14-formula-cheat-sheet)

---

# Part 1: ML Fundamentals

---

# 1. Supervised Learning, Generalization, and Regularization

## 1.1 The Supervised Learning Setup

We observe `n` i.i.d. samples `(x_i, y_i)` drawn from an unknown distribution `P(x, y)`. We choose a hypothesis class `f_theta` (linear model, tree ensemble, neural network) and a loss `l(f(x), y)`. The quantity we actually care about is the **expected risk** `R(theta) = E_{(x,y)~P}[ l(f_theta(x), y) ]`. We cannot compute it, so we minimize the **empirical risk** on the training set:

```text
theta* = argmin_theta  (1/n) sum_i l(f_theta(x_i), y_i)  +  lambda * Omega(theta)
                         \___________ ERM ____________/      \_ regularizer _/
```

The **generalization gap** is `R(theta*) - R_emp(theta*)`. The whole of "ML methodology" (validation sets, regularization, cross-validation, leakage hygiene) exists to estimate and control that gap.

| Task | Typical output | Loss | Probabilistic view |
|---|---|---|---|
| Regression | real number | MSE `(y - y_hat)^2` | Gaussian likelihood, fixed variance |
| Robust regression | real number | Huber / L1 | Laplace likelihood (L1) |
| Binary classification | logit `z`, `p = sigmoid(z)` | binary cross-entropy `-[y log p + (1-y) log(1-p)]` | Bernoulli likelihood |
| Multiclass | logits `z in R^C`, `p = softmax(z)` | cross-entropy `-log p_y` | Categorical likelihood |
| Language modeling | next-token logits | cross-entropy per token | autoregressive factorization `P(x) = prod_t P(x_t given x_<t)` |
| Ranking / retrieval | scores | pairwise hinge, InfoNCE (contrastive) | softmax over candidates |

Minimizing cross-entropy is maximum-likelihood estimation. Adding an L2 penalty is MAP estimation with a Gaussian prior; L1 corresponds to a Laplace prior.

**Splits.** Train (fit parameters), validation (choose hyperparameters, early-stop, select models), test (touched once, at the end, for an unbiased estimate). Anything you tune on the test set turns it into a validation set and makes the reported number optimistic.

## 1.2 Bias-Variance Decomposition

For squared loss with `y = f(x) + eps`, `E[eps] = 0`, `Var(eps) = sigma^2`, and a model `f_hat_D` trained on a random dataset `D`, the expected test error at a point `x` decomposes as:

```text
E_D,eps[(y - f_hat_D(x))^2] = (E_D[f_hat_D(x)] - f(x))^2   +   E_D[(f_hat_D(x) - E_D[f_hat_D(x)])^2]   +   sigma^2
                              \_______ bias^2 _______/         \______________ variance ______________/   \ noise /
```

Derivation sketch: write `y - f_hat = (f - f_bar) + (f_bar - f_hat) + eps` with `f_bar = E_D[f_hat]`. Expand the square. The cross terms vanish because `E_D[f_bar - f_hat] = 0` and `eps` is independent of `D` with mean zero.

- **Bias**: error from wrong assumptions (a linear model for a quadratic function). It falls as model capacity grows.
- **Variance**: sensitivity to the particular training sample. It rises with capacity and falls with more data.
- **Noise**: irreducible (label noise, missing features). No model can beat it.

The classical U-shaped test-error curve comes from this tradeoff. Modern over-parameterized networks also show **double descent**: test error peaks near the interpolation threshold (parameters ~ samples) and then falls again as capacity grows further, because among the many interpolating solutions, SGD plus implicit regularization picks low-norm, smooth ones. The decomposition still holds; what changes is that variance does not keep growing with parameter count.

## 1.3 Underfitting vs Overfitting

| Symptom | Underfitting (high bias) | Overfitting (high variance) |
|---|---|---|
| Training loss | high | low |
| Validation loss | high, close to training | much higher than training, often rising |
| Learning curve as data grows | both plateau high together | gap closes slowly as data grows |
| Fixes | more capacity, better features, train longer, less regularization, lower LR noise | more data, augmentation, regularization (L2, dropout), early stopping, smaller model, ensembling |

**How to diagnose in an interview.** Always ask for training *and* validation curves. If training loss itself does not go down, it is not an overfitting problem: check the learning rate, data pipeline (shuffled labels? wrong normalization?), and gradients (Section 2.4). A useful sanity check is to overfit a single batch: a correct model and training loop must drive the loss on one small batch to near zero.

## 1.4 Regularization: L1, L2, Dropout, Early Stopping

**L2 (ridge).** `Omega = (lambda/2) ||w||^2`, gradient `lambda * w`. Under plain SGD the update is

```text
w <- w - eta * (g + lambda * w) = (1 - eta * lambda) * w - eta * g
```

so L2 and multiplicative "weight decay" are the **same thing for SGD**. L2 shrinks all weights smoothly and never sets them exactly to zero. For linear regression it has a closed form `w = (X^T X + lambda I)^{-1} X^T y`, and `lambda I` also fixes ill-conditioning.

**L1 (lasso).** `Omega = lambda ||w||_1`, subgradient `lambda * sign(w)`. It produces **exact zeros** (sparse models, feature selection). Two explanations: geometrically, the L1 ball has corners on the axes, so the loss contours tend to touch it there; algebraically, the proximal update is soft-thresholding `w <- sign(w) * max(|w| - eta*lambda, 0)`, which snaps small weights to zero. Elastic net combines both.

**Dropout.** During training, zero each activation with probability `p` and scale survivors by `1/(1-p)` ("inverted dropout") so the expected activation is unchanged and inference needs no rescaling. It prevents co-adaptation and approximates averaging an ensemble of `2^n` thinned networks. Large LLM pretraining usually uses `p = 0` (single epoch over huge data, so overfitting is not the bottleneck), but fine-tuning on small data often uses it.

**Early stopping.** Monitor validation loss and keep the best checkpoint; stop after `patience` evaluations without improvement. For a quadratic loss with gradient descent, stopping after `t` steps with step size `eta` behaves like L2 regularization with `lambda ~ 1/(eta * t)`. It is free and effective, but it uses the validation set, so the validation score of the chosen checkpoint is slightly optimistic.

**Other regularizers.** Data augmentation (the most effective for vision), label smoothing (target `1 - epsilon` on the true class), mixup, stochastic depth, weight sharing, and simply more data.

## 1.5 Weight Decay vs L2 Under Adam

With adaptive optimizers the equivalence in 1.4 **breaks**. If you add `lambda * w` to the gradient and feed it to Adam, the decay term is divided by `sqrt(v_hat)` like everything else (see 3.3). Parameters with a large gradient history get **less** regularization, and parameters with tiny gradients get **more** (their update becomes roughly `lr * sign(w)`). Loshchilov and Hutter (2019) proposed **decoupled weight decay** (AdamW): apply the decay directly to the weights, outside the adaptive normalization:

```text
Adam + L2 :  g <- g + lambda * w ;  w <- w - lr * m_hat / (sqrt(v_hat) + eps)
AdamW     :                         w <- w - lr * ( m_hat / (sqrt(v_hat) + eps) + lambda * w )
```

```python
"""adam_vs_adamw.py -- L2-in-the-gradient is NOT weight decay under Adam."""
import numpy as np


def run(decoupled, lam=0.1, lr=0.01, steps=500, b1=0.9, b2=0.999, eps=1e-8):
    # Two parameters with the same value but very different gradient scales.
    w = np.array([1.0, 1.0])
    m = np.zeros(2); v = np.zeros(2)
    for t in range(1, steps + 1):
        g = np.array([100.0, 0.01]) * (-1.0) ** t   # zero-mean "noise": data gradients cancel out
        if not decoupled:
            g = g + lam * w                       # "Adam + L2": decay term goes through 1/sqrt(v)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        m_hat, v_hat = m / (1 - b1**t), v / (1 - b2**t)
        w = w - lr * m_hat / (np.sqrt(v_hat) + eps)
        if decoupled:
            w = w - lr * lam * w                  # AdamW: decay applied directly, same for every param
    return w


print("Adam + L2 :", run(decoupled=False))  # large-gradient param is barely decayed
print("AdamW     :", run(decoupled=True))   # both params shrink by ~ (1 - lr*lam)^steps
print("(1 - lr*lam)^steps =", (1 - 0.01 * 0.1) ** 500)
```

```text
Adam + L2 : [ 1.01252562e+00 -9.85844280e-05]
AdamW     : [0.61697741 0.6169774 ]
(1 - lr*lam)^steps = 0.6063789448611847
```

Under Adam + L2 the noisy parameter is not decayed at all and the quiet one is driven to zero; AdamW shrinks both by the same factor. This is why every modern LLM recipe uses AdamW (typical `weight_decay = 0.1`, usually not applied to biases, norm gains, or embeddings). Note that in PyTorch `torch.optim.AdamW` the decay is multiplied by the learning rate (`w <- w * (1 - lr * lambda)`), so changing the LR schedule also changes the effective decay.

## 1.6 Interview Questions

**Q1.** Derive the bias-variance decomposition and explain what happens to each term when you double the training set.

Let `f_bar(x) = E_D[f_hat_D(x)]`. Then `y - f_hat = (f - f_bar) + (f_bar - f_hat) + eps`. Squaring and taking expectations over `D` and `eps`: the term `(f - f_bar)^2` is deterministic (bias squared); `E[(f_bar - f_hat)^2]` is the variance; `E[eps^2] = sigma^2` is noise. Cross terms vanish: `E_D[f_bar - f_hat] = 0` by definition, and `eps` is zero-mean and independent of `D`. Doubling the data mostly reduces **variance** (for many estimators it scales like `1/n`). Bias is a property of the hypothesis class and barely moves. Noise is unchanged. So more data helps an overfit model a lot and an underfit model very little. That is the practical diagnostic: if the train/validation gap is small and both errors are high, collecting more data is the wrong investment.

**Q2.** Why does L1 give sparse solutions and L2 does not?

Look at the optimality condition for one weight. With L2 the penalty gradient `lambda * w` goes to zero as `w` goes to zero, so it only balances the data gradient at a nonzero `w` unless the data gradient is exactly zero. With L1 the subgradient at zero is the whole interval `[-lambda, lambda]`, so `w = 0` is optimal whenever `|dL/dw| <= lambda` at zero. That is a finite region, so many weights land exactly at zero. The proximal operator makes this concrete: soft-thresholding `sign(w) max(|w| - t, 0)`. Geometrically, the L1 ball is a cross-polytope with corners on the axes and the level sets of the loss usually hit a corner first.

**Q3.** Is weight decay the same as L2 regularization?

For plain SGD (and SGD with momentum, up to a rescaling of lambda), yes: `w - eta(g + lambda w) = (1 - eta lambda) w - eta g`. For adaptive methods (Adam, RMSProp, Adagrad), no. The L2 gradient is rescaled per coordinate by `1/sqrt(v_hat)`, so weights with large historical gradients are under-regularized and weights with tiny gradients are over-regularized. AdamW decouples the decay so every weight shrinks by the same factor `(1 - lr * lambda)` per step. Follow-up: "Should you decay LayerNorm gains and biases?" Usually not: they are scale/shift parameters, and pulling them toward zero (rather than toward 1 for gains) hurts. Most LLM codebases put them in a no-decay parameter group.

**Q4.** Your model's training loss is 0.01 and validation loss is 2.3 and rising. What do you do, in order?

First rule out bugs: leakage or a mismatch between train and validation preprocessing (Section 4.6), and duplicated examples. Then classic overfitting remedies, cheapest first: early stopping at the validation minimum, data augmentation, stronger weight decay, dropout, smaller model or fewer epochs, and more data. If train and validation come from different distributions (dataset shift), regularization will not help; you need representative training data or domain adaptation. Report the final number on a test set you have not used for any of these decisions.

**Q5.** Why does dropout scale by `1/(1-p)` during training?

To keep the expected value of each activation the same at train and test time: `E[mask * x / (1-p)] = (1-p) * x / (1-p) = x`. Then inference simply turns dropout off with no rescaling. The original paper instead scaled weights by `(1-p)` at test time; both are equivalent in expectation, but inverted dropout keeps the inference graph untouched. A follow-up is that the variance still differs between train and test, which is one reason dropout interacts badly with BatchNorm (the BN running statistics are collected with dropout noise).

---

# 2. Backpropagation

## 2.1 Chain Rule and Reverse-Mode Differentiation

A network is a composition `L = l(f_k(...f_2(f_1(x))))`. The chain rule gives `dL/dx = J_1^T J_2^T ... J_k^T dL/dy_k`, where `J_i` is the Jacobian of layer `i`. **Reverse mode** (backpropagation) evaluates this product from the loss backward as a sequence of **vector-Jacobian products**. Since the loss is a scalar, every intermediate quantity is a vector the size of a layer's activations, and the full Jacobians are never formed.

| | Forward mode | Reverse mode (backprop) |
|---|---|---|
| Propagates | `J v` (tangent) from inputs to outputs | `v^T J` (cotangent) from outputs to inputs |
| Cost for `f: R^n -> R^m` | `O(n)` passes for the full Jacobian | `O(m)` passes |
| Best when | few inputs, many outputs | many inputs (parameters), one output (loss) |
| Memory | no need to store activations | must store (or recompute) forward activations |

For a scalar loss, one backward pass costs a small constant times one forward pass (about 2x in FLOPs for matmul-dominated nets, Section 7.2). The price is memory: the backward pass needs the forward activations, which is why activation checkpointing (recompute instead of store) exists.

**Gradients of a linear layer** `Y = X W + b` with `X: (B, D_in)`, `W: (D_in, D_out)`, upstream `dY: (B, D_out)`:

```text
dW = X^T dY         (D_in, D_out)     -- sum over the batch
db = sum_rows(dY)   (D_out,)
dX = dY W^T         (B, D_in)
```

A useful check is that every gradient has the same shape as the thing it is a gradient of; the only way to make the shapes work is the formula above. Note that the backward pass of a linear layer is **two** GEMMs (`dW` and `dX`), each the same size as the forward GEMM, which is where "backward = 2x forward" comes from.

## 2.2 Softmax + Cross-Entropy Gradient: p - y

Logits `z in R^C`, `p_i = exp(z_i) / sum_k exp(z_k)`, one-hot target `y`, loss `L = -sum_i y_i log p_i`.

**Step 1: softmax Jacobian.** `log p_i = z_i - log sum_k exp(z_k)`, so `d log p_i / d z_j = delta_ij - p_j`. Equivalently `d p_i / d z_j = p_i (delta_ij - p_j)`, i.e. `J = diag(p) - p p^T`.

**Step 2: chain rule.**

```text
dL/dz_j = -sum_i y_i * d log p_i / d z_j
        = -sum_i y_i (delta_ij - p_j)
        = -y_j + p_j * sum_i y_i
        = p_j - y_j                      (since sum_i y_i = 1)
```

So `dL/dz = p - y`. For a batch of `B` examples with a mean-reduced loss, divide by `B`. Why this matters:

- It is **bounded** in `[-1, 1]` per logit, so it does not explode, and it does not vanish when the prediction is confidently wrong (unlike MSE on a sigmoid, whose gradient is multiplied by `sigma'(z)` and vanishes in saturation).
- It is why frameworks fuse softmax and cross-entropy (`F.cross_entropy` takes logits): the fused version never materializes `log` of a tiny probability and is numerically stable via `log_softmax(z) = z - max(z) - log sum exp(z - max(z))`.
- The same form holds for sigmoid + binary cross-entropy: `dL/dz = sigmoid(z) - y`. Both are instances of the general result for exponential-family outputs with their canonical link.
- For LLMs with a 128K vocabulary, the logits tensor `(tokens, V)` is huge; fused/chunked cross-entropy kernels compute `p - y` blockwise without storing full-precision logits.

## 2.3 Worked Example: a 2-Layer MLP

Network: `X (B, D) -> Linear(W1, b1) -> ReLU -> Linear(W2, b2) -> softmax-CE`.

| Forward | Shape | Backward | Shape |
|---|---|---|---|
| `z1 = X W1 + b1` | `(B, H)` | `dz1 = da1 * 1[z1 > 0]` | `(B, H)` |
| `a1 = relu(z1)` | `(B, H)` | `da1 = dz2 W2^T` | `(B, H)` |
| `z2 = a1 W2 + b2` | `(B, C)` | `dW2 = a1^T dz2`, `db2 = sum(dz2)` | `(H, C)`, `(C,)` |
| `p = softmax(z2)` | `(B, C)` | `dz2 = (p - Y) / B` | `(B, C)` |
| `L = mean(-log p_y)` | scalar | `dW1 = X^T dz1`, `db1 = sum(dz1)` | `(D, H)`, `(H,)` |

The code computes these by hand and verifies them with a central-difference gradient check. Gradient checks are a standard interview follow-up ("how do you know your backward is right?").

```python
"""mlp_backprop.py -- 2-layer MLP (Linear -> ReLU -> Linear -> softmax-CE), manual backprop + gradient check."""
import numpy as np

rng = np.random.default_rng(0)
B, D, H, C = 4, 5, 8, 3                     # batch, input dim, hidden dim, classes
X = rng.standard_normal((B, D))
y = rng.integers(0, C, size=B)              # integer class labels
params = {
    "W1": rng.standard_normal((D, H)) * 0.5, "b1": np.zeros(H),
    "W2": rng.standard_normal((H, C)) * 0.5, "b2": np.zeros(C),
}

def forward_backward(p, X, y):
    # ---- forward ----
    z1 = X @ p["W1"] + p["b1"]              # (B, H)
    a1 = np.maximum(z1, 0.0)                # ReLU
    z2 = a1 @ p["W2"] + p["b2"]             # (B, C) logits
    z2s = z2 - z2.max(axis=1, keepdims=True)            # stable softmax
    probs = np.exp(z2s) / np.exp(z2s).sum(axis=1, keepdims=True)
    loss = -np.log(probs[np.arange(len(y)), y]).mean()
    # ---- backward (chain rule, layer by layer) ----
    Y = np.eye(probs.shape[1])[y]           # one-hot
    dz2 = (probs - Y) / len(y)              # dL/dlogits = (p - y) / B
    g = {"W2": a1.T @ dz2, "b2": dz2.sum(axis=0)}
    da1 = dz2 @ p["W2"].T                   # (B, H)
    dz1 = da1 * (z1 > 0)                    # ReLU gate
    g["W1"] = X.T @ dz1
    g["b1"] = dz1.sum(axis=0)
    return loss, g

loss, grads = forward_backward(params, X, y)

# Central-difference gradient check: (L(w+h) - L(w-h)) / 2h
h = 1e-5
for name, W in params.items():
    num = np.zeros_like(W)
    for idx in np.ndindex(W.shape):
        old = W[idx]
        W[idx] = old + h; lp, _ = forward_backward(params, X, y)
        W[idx] = old - h; lm, _ = forward_backward(params, X, y)
        W[idx] = old
        num[idx] = (lp - lm) / (2 * h)
    rel = np.abs(num - grads[name]).max() / max(1e-12, np.abs(num).max() + np.abs(grads[name]).max())
    print(f"{name}: max relative error = {rel:.2e}")
print(f"loss = {loss:.4f}")
```

```text
W1: max relative error = 3.76e-11
b1: max relative error = 1.88e-11
W2: max relative error = 3.08e-11
b2: max relative error = 7.03e-12
loss = 1.1501
```

Gradient-check tips: use float64 (float32 with `h = 1e-5` gives errors around `1e-3` from rounding alone), use central differences (error `O(h^2)` vs `O(h)`), and avoid kinks (ReLU at exactly 0) or check a few random coordinates of huge tensors rather than all of them. Relative error below about `1e-7` in float64 means the backward is right.

## 2.4 Vanishing and Exploding Gradients

Backprop through `k` layers multiplies `k` Jacobians. If their typical singular values are below 1 the gradient shrinks geometrically (vanishes); above 1 it grows geometrically (explodes). Concrete sources:

- **Saturating activations.** `sigmoid'(z) <= 0.25`, so 10 sigmoid layers scale the gradient by at most `0.25^10 ~ 1e-6`. `tanh'` is at most 1 but tiny in saturation.
- **Bad initialization.** If `Var(w) * fan_in` is not about 1 (or 2 for ReLU), activation and gradient variance shrink or grow by that factor per layer.
- **Recurrence.** An RNN applies the same `W_hh` at each timestep, so gradients scale like `lambda_max(W_hh)^T`.
- **Deep post-norm Transformers** without warmup (Section 6.1).

| Fix | Mechanism |
|---|---|
| ReLU / GELU / SiLU | derivative is 1 (or close) on the active side, no saturation |
| Xavier/Glorot init `Var(w) = 2/(fan_in + fan_out)` | keeps variance roughly constant for tanh/linear |
| He/Kaiming init `Var(w) = 2/fan_in` | compensates for ReLU zeroing half the inputs |
| Residual connections `x + F(x)` | Jacobian is `I + dF/dx`, so there is always an identity path for gradients |
| Normalization (BN/LN/RMSNorm) | keeps activations at unit scale, so layer Jacobians are well-conditioned |
| LSTM/GRU gating | additive cell-state path, like a residual through time |
| Gradient clipping by global norm (e.g. 1.0) | caps the update when gradients explode (standard for Transformers) |
| LR warmup | avoids huge early updates when Adam's `v` estimates are still noisy |
| Lower precision care | loss scaling for FP16 underflow (Section 13.2) |

Diagnosis in practice: log the global gradient norm and per-layer gradient norms. Loss spikes followed by NaN usually mean explosion (or an FP16 overflow); early layers with gradient norms many orders of magnitude below later layers mean vanishing.

## 2.5 Interview Questions

**Q1.** Derive the gradient of softmax cross-entropy with respect to the logits.

`L = -sum_i y_i log p_i` and `log p_i = z_i - logsumexp(z)`. Then `d log p_i / d z_j = delta_ij - p_j`, so `dL/dz_j = -sum_i y_i (delta_ij - p_j) = -y_j + p_j sum_i y_i = p_j - y_j` because the targets sum to 1. In vector form `dL/dz = p - y`. It works for soft labels too (label smoothing, distillation) as long as `y` sums to 1. Follow-up: with mean reduction over a batch of `B`, the gradient is `(p - y)/B`; with gradient accumulation over `k` micro-batches you must divide by the total number of tokens or examples, not by `B` per micro-batch, or the effective learning rate changes.

**Q2.** Why is reverse mode used for training instead of forward mode?

The loss is a scalar function of millions or billions of parameters. Reverse mode computes the whole gradient in one backward pass costing about 2x the forward FLOPs. Forward mode computes one directional derivative per pass, so it would need one pass per parameter. The trade is memory: reverse mode stores forward activations (or recomputes them, as in activation checkpointing and the FlashAttention backward pass).

**Q3.** For `Y = XW`, write `dX` and `dW`. Why does the backward pass cost about twice the forward?

`dW = X^T dY` and `dX = dY W^T`. Each is a GEMM with the same `M*N*K` as the forward `XW`, so the backward is two GEMMs for every one in the forward: about 2x the FLOPs. The first layer's `dX` is not needed (inputs are not trainable), which is the small saving people sometimes mention. This is the origin of the `6ND` training estimate: 2 FLOPs per parameter per token forward plus 4 backward.

**Q4.** What is the vanishing gradient problem, and why do residual connections fix it?

In a deep chain the gradient is a product of per-layer Jacobians; if their norms are below 1, the gradient decays exponentially with depth and early layers stop learning. With a residual block `y = x + F(x)`, `dy/dx = I + dF/dx`. Unrolling `k` blocks gives a sum over all paths, including the pure-identity path, so the gradient reaching early layers contains an unattenuated copy of the upstream gradient. Pre-norm Transformers keep this identity path clean (normalization only inside the branch), which is why they train stably without careful warmup.

**Q5.** Why does He initialization use `2/fan_in`?

For `z = sum_i w_i a_i` with independent zero-mean weights, `Var(z) = fan_in * Var(w) * E[a^2]`. For ReLU, `a = max(0, z_prev)` with symmetric `z_prev` gives `E[a^2] = Var(z_prev)/2`. To keep `Var(z) = Var(z_prev)` across layers you need `fan_in * Var(w) / 2 = 1`, so `Var(w) = 2/fan_in`. Xavier derives `Var(w) = 1/fan_in` for the forward pass and `1/fan_out` for the backward pass of a linear/tanh net, then compromises with `2/(fan_in + fan_out)`.

---

# 3. Normalization and Optimizers

## 3.1 BatchNorm vs LayerNorm vs RMSNorm

All three compute a normalized `x_hat` and then apply a learned per-feature gain `gamma` (and, except RMSNorm, a bias `beta`). The difference is **which axis the statistics are computed over**.

```text
BatchNorm (per feature c, over batch and spatial dims):  mu_c = mean_{b,h,w} x,  var_c = var_{b,h,w} x
                                                          y = gamma_c (x - mu_c) / sqrt(var_c + eps) + beta_c
LayerNorm (per token, over the d features):              mu = mean_d x,  var = var_d x
                                                          y = gamma * (x - mu) / sqrt(var + eps) + beta
RMSNorm   (per token, over the d features, no centering): rms = sqrt(mean_d x^2 + eps)
                                                          y = gamma * x / rms
```

| | BatchNorm | LayerNorm | RMSNorm |
|---|---|---|---|
| Statistics over | batch (and H, W) per channel | features of one token | features of one token |
| Depends on other samples | yes | no | no |
| Train vs inference | running mean/var at inference (different behavior) | identical | identical |
| Small batches / variable lengths / padding | breaks down (noisy stats, padding pollutes them) | fine | fine |
| Distributed training | needs SyncBN for small per-GPU batches | no communication | no communication |
| Cost | cheap at inference (can fold into conv weights) | two reductions (mean, var) or Welford | one reduction (sum of squares), no mean subtraction, no beta |
| Typical use | CNNs | original Transformer, BERT, GPT-2 | LLaMA, Mistral, most modern LLMs |

Why Transformers use LayerNorm/RMSNorm: sequence models have variable lengths and padding, autoregressive decoding processes one token at a time (batch statistics would make a token's output depend on other users' requests in the batch), and per-device batches can be tiny in large-scale training. RMSNorm (Zhang and Sennrich, 2019) drops mean-centering: re-scaling invariance turned out to matter more than re-centering, quality is on par, and it saves one reduction, which matters because normalization is a memory-bound kernel that is usually fused with the residual add.

## 3.2 SGD and Momentum

```text
SGD:            w <- w - eta * g
Momentum (PyTorch form):   v <- mu * v + g ;            w <- w - eta * v
Nesterov:                  v <- mu * v + g ;            w <- w - eta * (g + mu * v)
```

Momentum is an exponential moving average of gradients with effective window `1/(1-mu)` (10 steps for `mu = 0.9`). It damps oscillation across steep, narrow valleys (components that flip sign average out) and accelerates along consistent directions (up to `1/(1-mu)` times the step). Nesterov evaluates the gradient at the look-ahead point, which gives better theoretical rates for convex problems and a small practical improvement. SGD + momentum stores one extra tensor per parameter.

## 3.3 Adam and AdamW

```text
m_t = beta1 * m_{t-1} + (1 - beta1) * g_t          # first moment (mean)
v_t = beta2 * v_{t-1} + (1 - beta2) * g_t^2        # second moment (uncentered variance), elementwise
m_hat = m_t / (1 - beta1^t)                        # bias correction: m_0 = v_0 = 0 biases early estimates toward 0
v_hat = v_t / (1 - beta2^t)
w_t = w_{t-1} - lr * ( m_hat / (sqrt(v_hat) + eps)  +  lambda * w_{t-1} )   # the lambda term is AdamW's decoupled decay
```

Typical LLM values: `beta1 = 0.9`, `beta2 = 0.95` (lower than the default 0.999, so `v` adapts faster and large-scale training spikes less), `eps = 1e-8`, weight decay 0.1, gradient clipping at 1.0, warmup then cosine decay.

Intuitions to state in an interview:

- `m_hat / sqrt(v_hat)` is roughly a **signal-to-noise ratio** per coordinate. The step size is about `lr` in each coordinate regardless of gradient scale, which makes Adam robust to badly scaled parameters and is why the same `lr` works across layers.
- **Bias correction** matters early: at `t = 1`, `m_1 = 0.1 g` without correction; dividing by `1 - 0.9 = 0.1` recovers `g`.
- `eps` matters in low precision: if `v_hat` underflows, `eps` caps the step. Optimizer states are kept in FP32 for this reason.

**Memory cost** (the number to quote for training-memory estimates): Adam keeps `m` and `v`, so with mixed precision the per-parameter footprint is

| Item | Bytes/param |
|---|---|
| BF16/FP16 weights (used in forward/backward) | 2 |
| BF16/FP16 gradients | 2 |
| FP32 master weights | 4 |
| FP32 Adam `m` | 4 |
| FP32 Adam `v` | 4 |
| **Total (before activations)** | **16** |

A 70B model therefore needs about `70e9 * 16 = 1.12 TB` of training state before activations, which is why ZeRO/FSDP shards these states across data-parallel ranks (see [ML_AI_Frameworks.md, Section 7](../ml-gpu/ML_AI_Frameworks.md#7-distributed-training)). Memory-lean alternatives: Adafactor (factorized second moment), 8-bit Adam (block-quantized states), and SGD with momentum (one state).

## 3.4 Learning-Rate Schedules

- **Linear warmup** (for example the first 0.1 to 1% of steps): early Adam second-moment estimates are noisy and post-norm networks have large early gradients; ramping the LR from ~0 avoids divergence.
- **Cosine decay** to about 10% of peak, or **warmup-stable-decay** (constant LR, then a short sharp decay; convenient because you can branch off checkpoints for different training lengths).
- **Linear scaling rule** (SGD): when multiplying the batch size by `k`, multiply the LR by `k` (with warmup), up to a critical batch size beyond which returns diminish. For Adam a square-root rule is often closer.

Framework usage of schedulers is in [ML_AI_Frameworks.md, Section 4](../ml-gpu/ML_AI_Frameworks.md#4-optimizers-and-learning-rate-scheduling).

## 3.5 Interview Questions

**Q1.** Why do Transformers use LayerNorm rather than BatchNorm?

BatchNorm's statistics are computed across the batch, so (a) variable-length sequences and padding pollute the statistics, (b) small per-device batches make them noisy, (c) inference uses running averages that differ from training statistics, and (d) at decode time one request's output would depend on which other requests share the batch, which is unacceptable for serving. LayerNorm normalizes each token over its own features, behaves identically in training and inference, and needs no cross-device communication. RMSNorm goes further and drops the mean, saving a reduction with no quality loss.

**Q2.** Write the Adam update and explain bias correction.

`m = b1 m + (1-b1) g`, `v = b2 v + (1-b2) g^2`, `m_hat = m/(1-b1^t)`, `v_hat = v/(1-b2^t)`, `w -= lr m_hat/(sqrt(v_hat)+eps)`. Because `m` and `v` start at zero, the moving averages are biased toward zero for the first `~1/(1-beta)` steps; with `beta2 = 0.999` that is about 1000 steps. Dividing by `1 - beta^t` makes the estimates unbiased if the gradient distribution is stationary. Without it, `v_hat` would be tiny early on and the first steps would be enormous.

**Q3.** How much GPU memory does it take to train a 7B model with AdamW in mixed precision, ignoring activations?

16 bytes per parameter (2 weights + 2 grads + 4 master + 4 m + 4 v): `7e9 * 16 = 112 GB`. That does not fit on an 80 GB GPU but fits on a 192 GB MI300X. With ZeRO-3/FSDP across 8 GPUs it is 14 GB per GPU. Activations come on top and scale with batch size times sequence length times hidden size times layers; activation checkpointing trades about 33% extra compute (one extra forward) to cut them sharply.

**Q4.** Why use `beta2 = 0.95` instead of 0.999 for LLM pretraining?

With 0.999 the second-moment estimate averages over about 1000 steps. When the gradient distribution shifts suddenly (rare tokens, a bad batch, a loss spike), `v` responds slowly and the effective step `g/sqrt(v)` can become very large, which feeds instability. A smaller `beta2` (window of about 20 steps) tracks the current gradient scale more closely, trading some noise for stability. It is an empirical choice that large-scale runs converged on.

**Q5.** What does momentum do on an ill-conditioned quadratic?

Along high-curvature directions the gradient flips sign every step, so the momentum average cancels the oscillation. Along low-curvature directions the gradient is consistent, so momentum accumulates and the effective step grows by up to `1/(1-mu)`. The result is a convergence rate depending on `sqrt(kappa)` instead of `kappa` (the condition number) for heavy-ball / Nesterov on quadratics.

---

# 4. Evaluation, Data Leakage, and Cross-Validation

## 4.1 Confusion Matrix, Precision, Recall, F1

```text
                  predicted +     predicted -
actual +             TP               FN
actual -             FP               TN

precision = TP / (TP + FP)       "of what I flagged, how much was right"
recall    = TP / (TP + FN)       "of what was there, how much did I find"   (= TPR, sensitivity)
FPR       = FP / (FP + TN)       (= 1 - specificity)
F1        = 2 * P * R / (P + R)  harmonic mean, dominated by the smaller of the two
F_beta    = (1 + beta^2) P R / (beta^2 P + R)   beta > 1 weights recall more
accuracy  = (TP + TN) / total    meaningless under heavy class imbalance
```

Choose the metric from the **cost** of errors: fraud and cancer screening care about recall at a tolerable precision; spam filtering and search care about precision. Threshold choice is a business decision made on validation data, after the model is trained. For multiclass, **macro** averaging gives every class equal weight (good when rare classes matter), **micro** averaging pools counts (dominated by frequent classes; equals accuracy for single-label problems).

## 4.2 ROC-AUC vs PR-AUC

- **ROC curve**: TPR vs FPR as the threshold sweeps. **ROC-AUC** equals the probability that a random positive is scored above a random negative (the Mann-Whitney U statistic). 0.5 is random, 1.0 is perfect. It is invariant to class balance and to any monotone transform of the scores.
- **PR curve**: precision vs recall. **PR-AUC** (average precision) has a random baseline equal to the **positive rate**, so it moves sharply with class imbalance.

Under heavy imbalance, ROC-AUC can look excellent while the model is useless at any practical threshold, because FPR divides by the huge number of negatives: 1% FPR on 1,000,000 negatives is 10,000 false alarms. PR-AUC exposes this because precision counts false positives against true positives directly. Rule of thumb: rare positives and you care about the positive class means report PR-AUC (plus precision at a fixed recall); balanced classes or ranking quality across the whole population means ROC-AUC is fine.

## 4.3 Calibration

A model is **calibrated** if, among examples given predicted probability 0.8, about 80% are positive. Ranking metrics (AUC) ignore calibration entirely. Calibration matters whenever probabilities are consumed downstream: expected-value decisions, ad bidding, combining models, risk thresholds, and LLM confidence estimates.

- **Reliability diagram**: bin predictions by confidence and plot observed frequency vs mean confidence.
- **Expected Calibration Error (ECE)**: `sum_b (n_b / n) * |acc_b - conf_b|`.
- **Brier score**: `mean (p - y)^2`, a proper scoring rule that combines calibration and sharpness. Log loss is also proper.
- **Fixes (post hoc, fit on validation data)**: temperature scaling (divide logits by a single learned `T`; preserves ranking and accuracy), Platt scaling (logistic regression on the score), isotonic regression (non-parametric, needs more data).

Modern deep networks are typically **over-confident** after training with cross-entropy to near-zero training loss; temperature scaling with `T > 1` is the standard fix. Training with class re-weighting or under-sampling also mis-calibrates the outputs (probabilities reflect the re-weighted prior), which must be corrected before use.

## 4.4 Perplexity

For a language model on a test sequence of `T` tokens:

```text
PPL = exp( -(1/T) * sum_t log p(x_t given x_<t) )  = exp(mean cross-entropy in nats)
```

Interpretation: the model is as uncertain as a uniform choice among `PPL` tokens. A cross-entropy of 2.0 nats per token is PPL `e^2 ~ 7.4`. Caveats interviewers probe:

- PPL depends on the **tokenizer**: a tokenizer that splits text into more, easier tokens gets lower per-token PPL. Compare across tokenizers with **bits per byte** (or per character): `bpb = (total nats / ln 2) / total bytes`.
- Context length and the evaluation window (sliding window with stride vs disjoint chunks) change the number.
- Lower PPL does not guarantee better downstream task performance or instruction following; it is a pretraining metric. Fine-tuned chat models are evaluated on task benchmarks and human/LLM preference.
- Quantization quality is often reported as PPL delta on WikiText-2 or C4 (Section 11).

## 4.5 Metrics From Scratch

```python
"""metrics.py -- precision/recall/F1, ROC-AUC (rank form), PR-AUC (average precision), ECE. Pure Python."""
import random

random.seed(0)
# Imbalanced problem: 1% positives. Positive scores are higher on average.
y = [1] * 100 + [0] * 9900
s = [random.betavariate(5, 2) for _ in range(100)] + [random.betavariate(2, 5) for _ in range(9900)]


def confusion(y, s, t):
    tp = sum(1 for yi, si in zip(y, s) if si >= t and yi == 1)
    fp = sum(1 for yi, si in zip(y, s) if si >= t and yi == 0)
    fn = sum(1 for yi, si in zip(y, s) if si < t and yi == 1)
    return tp, fp, fn


def roc_auc(y, s):
    """AUC = P(score of random positive > score of random negative) (Mann-Whitney U)."""
    order = sorted(range(len(s)), key=lambda i: s[i])
    rank_sum = sum(r + 1 for r, i in enumerate(order) if y[i] == 1)   # assumes no ties
    P = sum(y); N = len(y) - P
    return (rank_sum - P * (P + 1) / 2) / (P * N)


def average_precision(y, s):
    """Area under the PR curve as sum over positives of precision at that positive's rank."""
    order = sorted(range(len(s)), key=lambda i: -s[i])
    tp, ap = 0, 0.0
    for k, i in enumerate(order, start=1):
        if y[i] == 1:
            tp += 1
            ap += tp / k
    return ap / sum(y)


def ece(y, p, bins=10):
    """Expected calibration error: weighted |accuracy - confidence| over probability bins."""
    total, err = len(y), 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i in range(total) if lo <= p[i] < hi or (b == bins - 1 and p[i] == 1.0)]
        if idx:
            conf = sum(p[i] for i in idx) / len(idx)
            acc = sum(y[i] for i in idx) / len(idx)
            err += len(idx) / total * abs(acc - conf)
    return err


tp, fp, fn = confusion(y, s, 0.5)
prec, rec = tp / (tp + fp), tp / (tp + fn)
print(f"threshold 0.5: TP={tp} FP={fp} FN={fn}  precision={prec:.3f} recall={rec:.3f} "
      f"F1={2 * prec * rec / (prec + rec):.3f}")
print(f"ROC-AUC = {roc_auc(y, s):.3f}   PR-AUC (AP) = {average_precision(y, s):.3f}   (random PR-AUC = 0.01)")
print(f"ECE of raw scores = {ece(y, s):.3f}  (scores are not probabilities)")
```

```text
threshold 0.5: TP=81 FP=1080 FN=19  precision=0.070 recall=0.810 F1=0.128
ROC-AUC = 0.945   PR-AUC (AP) = 0.454   (random PR-AUC = 0.01)
ECE of raw scores = 0.281  (scores are not probabilities)
```

The example is the imbalance trap in numbers: ROC-AUC 0.945 looks great, but at threshold 0.5 only 7% of alerts are real. PR-AUC (0.454 against a 0.01 baseline) gives the honest picture, and the large ECE shows the scores cannot be read as probabilities without calibration.

## 4.6 Data Leakage

Leakage is information in training (or in feature construction) that will not be available at prediction time. It inflates offline metrics and then fails in production.

| Type | Example | Prevention |
|---|---|---|
| Target leakage | feature "account_closed_reason" when predicting churn; "treatment given" when predicting diagnosis | for every feature ask "is this known at prediction time?"; use point-in-time feature snapshots |
| Train-test contamination via preprocessing | fitting the scaler, PCA, imputer, vocabulary, or feature selection on the full dataset before splitting | fit transforms on the training fold only (pipelines inside CV) |
| Temporal leakage | random split of time-series data; features computed with future data (rolling means that include the label day) | split by time; forward-chaining validation; compute features as of the event timestamp |
| Group leakage | same patient, user, or device in train and test; augmented copies of one image on both sides | group-aware splits (`GroupKFold`) |
| Duplicates / near-duplicates | scraped data with repeated documents | dedup (exact hash and MinHash/LSH) before splitting |
| Benchmark contamination (LLMs) | test-set questions present in the pretraining crawl | n-gram overlap checks, held-out and freshly written evals, canary strings |
| Tuning on test | repeatedly checking the test score while choosing hyperparameters | keep a locked test set; use validation or nested CV for selection |

A tell-tale sign of leakage is a validation score that is "too good" (AUC 0.99 on a hard problem) or a single feature with outsized importance.

## 4.7 Cross-Validation

**k-fold CV**: split the data into `k` folds; train on `k-1`, validate on the remaining one; rotate and average. `k = 5` or `10` is typical. It uses all data for both fitting and evaluation and gives a variance estimate. It costs `k` trainings, so it is common for classic ML and small data, and rare for large deep learning (a single held-out validation set is standard there).

| Variant | When |
|---|---|
| Stratified k-fold | classification, keeps the class ratio in each fold (important under imbalance) |
| Group k-fold | samples are clustered (users, patients); keeps each group in one fold |
| Time-series split (forward chaining, expanding or sliding window) | temporal data; always train on the past and validate on the future, optionally with a gap to avoid leakage via lagged features |
| Leave-one-out | very small data; nearly unbiased but high-variance and expensive |
| Nested CV | inner loop selects hyperparameters, outer loop estimates generalization; needed for an unbiased estimate when tuning |

Pitfall: running feature selection or hyperparameter search on the whole dataset and *then* reporting k-fold CV of the final model. The CV estimate is optimistic because the selection already saw every fold. The whole pipeline (preprocessing, selection, tuning) must run inside each fold.

## 4.8 Interview Questions

**Q1.** A fraud model has ROC-AUC 0.97 but the fraud team says it is useless. How can both be true?

Fraud is rare (say 0.1%). ROC-AUC measures ranking over all positive-negative pairs, and FPR divides by the enormous negative count. At an operating point with recall 80% and FPR 2%, on 1M transactions with 1,000 frauds you flag 800 frauds and about 20,000 legitimate transactions: precision about 4%. Investigators drown in false positives. Report PR-AUC and precision at the recall (or alert volume) the team can handle, and choose the threshold from their capacity.

**Q2.** What does ROC-AUC = 0.5 mean? What about 0.3?

0.5 means the model ranks a random positive above a random negative only half the time: no discrimination. 0.3 means it ranks them the wrong way 70% of the time, which is real signal with the sign flipped; inverting the scores gives 0.7. In practice, an AUC well below 0.5 almost always indicates a label or sign bug.

**Q3.** How would you check and fix calibration of a classifier?

Plot a reliability diagram on held-out data and compute ECE and Brier score. If the model is over-confident (typical for deep nets), fit temperature scaling on a validation set: minimize NLL over a single scalar `T` with `p = softmax(z/T)`. It does not change the argmax or ranking, so accuracy and AUC are preserved. Use isotonic regression if the miscalibration is non-monotone in a way a single temperature cannot fix and you have enough data. Re-check on a separate test split.

**Q4.** Define perplexity. Model A has PPL 8 with tokenizer X and model B has PPL 10 with tokenizer Y. Which is better?

`PPL = exp(mean token-level NLL)`. You cannot tell from these numbers: per-token perplexity depends on the tokenization. If Y produces fewer, longer tokens, each token is harder to predict and the per-token PPL is higher even if the model assigns higher probability to the text. Convert to bits per byte: `bpb = (log2 PPL * num_tokens) / num_bytes` and compare on the same text.

**Q5.** You have 3 years of daily sales data. How do you validate a demand forecast model?

Time-ordered splits only: train on the earliest data and validate on a later window, repeated with an expanding (or sliding) window, for example train on months 1-24 and test on 25-27, then train on 1-27 and test on 28-30, and so on. Leave a gap between train and validation if features use lags or rolling windows that could include validation-period labels. Compute all features as of the forecast time. Random k-fold leaks the future into training and overstates accuracy.

---

# Part 2: Transformers

---

# 5. Attention

## 5.1 Scaled Dot-Product Attention

Attention is a **differentiable dictionary lookup**. Each position emits a query `q`, a key `k`, and a value `v` (linear projections of its hidden state). A query is compared against every key; the similarities become weights through a softmax; the output is the weighted average of the values:

```text
Attention(Q, K, V) = softmax( Q K^T / sqrt(d_k) + M ) V

Q: (n_q, d_k)    K: (n_k, d_k)    V: (n_k, d_v)    M: (n_q, n_k) mask of 0 / -inf
S = Q K^T / sqrt(d_k)       (n_q, n_k)   scores
P = softmax_rows(S + M)     (n_q, n_k)   each row sums to 1
O = P V                     (n_q, d_v)
```

Derivation from first principles: we want output `o_i = sum_j a_ij v_j` with weights that are (a) non-negative, (b) sum to 1, (c) larger for keys more similar to the query, and (d) differentiable. The dot product is the cheapest similarity that maps onto GEMMs; `exp` makes weights positive and emphasizes the largest similarities; normalizing by the row sum gives (b). That is exactly `softmax(q_i . k_j)`. A hard lookup (`argmax`) is the zero-temperature limit.

Costs for self-attention over `n` tokens with model width `d`: `S = QK^T` and `PV` are each `2 n^2 d` FLOPs, and the naive implementation materializes the `n x n` matrices `S` and `P`, so memory is `O(n^2)` per head. That quadratic memory traffic, not the FLOPs, is what FlashAttention removes (Part 3).

## 5.2 Why the sqrt(d_k) Scaling

Assume the components of `q` and `k` are independent with mean 0 and variance 1 (roughly what LayerNorm plus a well-initialized projection gives). Then

```text
q . k = sum_{i=1..d_k} q_i k_i
E[q_i k_i] = E[q_i] E[k_i] = 0
Var(q_i k_i) = E[q_i^2] E[k_i^2] - 0 = 1
Var(q . k) = d_k          ->  std(q . k) = sqrt(d_k)
```

With `d_k = 128`, raw scores have standard deviation about 11. Softmax over logits that spread over tens of units is nearly one-hot. The softmax Jacobian `diag(p) - p p^T` goes to zero as `p` approaches one-hot, so gradients through the attention weights vanish and learning stalls. Dividing by `sqrt(d_k)` restores unit variance regardless of head size, so the softmax starts in its sensitive regime.

```python
"""why_sqrt_dk.py -- dot products of unit-variance vectors have variance d_k; unscaled softmax saturates."""
import numpy as np

rng = np.random.default_rng(0)
n_keys = 64
for d_k in (16, 128, 1024):
    q = rng.standard_normal((2000, d_k))
    k = rng.standard_normal((2000, n_keys, d_k))
    s = np.einsum("bd,bnd->bn", q, k)                      # raw scores
    for name, logits in (("raw", s), ("scaled", s / np.sqrt(d_k))):
        p = np.exp(logits - logits.max(-1, keepdims=True))
        p /= p.sum(-1, keepdims=True)
        # softmax Jacobian diag p(1-p) -> small when p is ~one-hot; report mean max-prob
        print(f"d_k={d_k:5d} {name:6s} std(score)={logits.std():6.2f}  mean max prob={p.max(-1).mean():.3f}")
```

```text
d_k=   16 raw    std(score)=  3.99  mean max prob=0.581
d_k=   16 scaled std(score)=  1.00  mean max prob=0.107
d_k=  128 raw    std(score)= 11.30  mean max prob=0.855
d_k=  128 scaled std(score)=  1.00  mean max prob=0.108
d_k= 1024 raw    std(score)= 31.87  mean max prob=0.950
d_k= 1024 scaled std(score)=  1.00  mean max prob=0.106
```

Follow-ups: the scale is a temperature, so it can be learned or replaced (QK-norm normalizes `q` and `k` per head, which also prevents attention-logit growth in very large models; muP uses `1/d_k` instead of `1/sqrt(d_k)` for hyperparameter transfer across widths). In kernels the scale is folded into `Q` once (`n * d` multiplies) rather than applied to `S` (`n^2` multiplies), and it is often combined with `log2(e)` so the kernel can use the fast `exp2` instruction.

## 5.3 Multi-Head Attention Shapes

Instead of one attention with `d_k = d`, use `H` heads of size `d_h = d/H`, each with its own projections, then concatenate and project back. Total FLOPs and parameters are the same as one big head, but each head can attend to different positions for different reasons (syntax, coreference, copying), and each head's softmax is a separate distribution.

```text
x                     (B, T, D)
Q = x W_Q             (B, T, H*d_h)  -> reshape (B, T, H, d_h) -> transpose (B, H, T, d_h)
K = x W_K, V = x W_V  same as Q for MHA (GQA: H_kv heads instead of H, Section 5.6)
S = Q K^T / sqrt(d_h) (B, H, T, T)     <- the quadratic tensor
P = softmax(S + M)    (B, H, T, T)
O = P V               (B, H, T, d_h) -> transpose (B, T, H, d_h) -> reshape (B, T, D)
y = O W_O             (B, T, D)

Parameters (MHA, H*d_h = D): W_Q, W_K, W_V, W_O each D x D -> 4 D^2
```

Concrete numbers, LLaMA-3-70B: `D = 8192`, `H = 64`, `d_h = 128`. For `B = 1`, `T = 8192`, one layer's score tensor is `64 * 8192^2 = 4.3e9` elements, which is 8.6 GB in BF16 per layer if materialized. That is why nobody materializes it.

## 5.4 Causal Masking

A decoder-only LM predicts `x_t` from `x_<t`, so position `i` may only attend to `j <= i`. Add `M_ij = -inf` for `j > i` before the softmax (`exp(-inf) = 0`). This lets training compute the next-token loss at **all** `T` positions in one parallel forward pass ("teacher forcing"); the mask guarantees no position sees its own target.

Practical details interviewers like:

- **Inference with a KV cache**: a single new query token at position `t` attends to all cached keys `0..t`, which are all in the past, so no mask is needed for that row. Masks are needed for prefill, chunked prefill (the chunk attends causally to itself and fully to the cache), and speculative verification.
- **`-inf` pitfalls**: a row whose entries are all masked gives `softmax = 0/0 = NaN`. This happens with left padding or fully masked chunks. Kernels guard against it, and some code uses a large finite negative (`torch.finfo(dtype).min`) instead of `-inf`; in FP16 adding that to a score can overflow to `-inf` anyway.
- **Compute savings**: a causal mask leaves about half of the `T x T` tiles fully masked; FlashAttention skips them entirely, so causal attention costs about half the FLOPs of non-causal attention.
- **Padding masks** (variable-length batches) and **document masks** (packing several documents in one sequence without cross-attention) are the same mechanism; varlen kernels avoid padding by using cumulative sequence-length offsets.

## 5.5 Positional Encodings: Sinusoidal, Learned, RoPE, ALiBi

Self-attention is **permutation-equivariant**: shuffling the input tokens shuffles the outputs identically. Without positional information "dog bites man" equals "man bites dog". (A causal mask does leak some positional signal, but explicit encodings work much better.)

**Sinusoidal (original Transformer).** Added to the input embeddings:

```text
PE(pos, 2i)   = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

Wavelengths form a geometric sequence from `2*pi` to `10000 * 2*pi`. For any fixed offset `k`, `PE(pos + k)` is a linear function (a rotation of each sin/cos pair) of `PE(pos)`, which makes relative offsets easy to learn. No parameters; extrapolation beyond trained lengths is poor in practice.

**Learned absolute.** A trainable table of shape `(max_len, d)` added to embeddings (BERT, GPT-2). Simple and effective but cannot represent positions beyond `max_len`.

**RoPE (rotary position embedding, Su et al.).** Instead of adding to embeddings, **rotate** `q` and `k` in every layer. Split the head dimension into `d_h/2` pairs; rotate pair `i` of the vector at position `m` by angle `m * theta_i`, with `theta_i = base^(-2i/d_h)`:

```text
[q'_{2i}  ]   [cos(m theta_i)  -sin(m theta_i)] [q_{2i}  ]
[q'_{2i+1}] = [sin(m theta_i)   cos(m theta_i)] [q_{2i+1}]

<R_m q, R_n k> = <q, R_m^T R_n k> = <q, R_{n-m} k>     -> the score depends only on the offset n - m
```

Properties: relative position enters the attention score directly; no extra parameters; `V` is not rotated; the cost is a cheap elementwise op usually fused into the QKV projection or attention kernel. Low-index pairs rotate fast (encode local position), high-index pairs rotate slowly (long-range). Base: 10,000 in LLaMA-1/2; LLaMA-3 raised it to 500,000 for longer contexts. **Context extension** methods modify the frequencies: position interpolation (scale positions down), NTK-aware scaling (raise the base), and YaRN (per-frequency interpolation plus an attention temperature), each followed by a short fine-tune at the longer length.

**ALiBi (Press et al.).** No position embeddings at all; add a static, head-specific linear bias to the attention scores:

```text
S_ij = q_i . k_j / sqrt(d_h)  -  m_h * (i - j)        for j <= i
slopes m_h: geometric sequence, for H = 8 heads: 1/2, 1/4, ..., 1/256   (start and ratio 2^(-8/H))
```

Distant tokens are penalized linearly, with different heads having different "attention spans". It extrapolates to longer sequences than seen in training well (BLOOM, MPT used it), but it has largely been displaced by RoPE in recent LLMs.

| Scheme | Where applied | Relative? | Parameters | Length extrapolation | Used by |
|---|---|---|---|---|---|
| Sinusoidal | added to input embeddings | implicitly learnable | none | poor | original Transformer |
| Learned absolute | added to input embeddings | no | `max_len x d` | none beyond `max_len` | BERT, GPT-2, GPT-3 |
| RoPE | rotates Q and K in every layer | yes (exactly) | none | moderate; good with interpolation / YaRN | LLaMA, Mistral, Qwen, most current LLMs |
| ALiBi | bias on attention scores | yes | none (fixed slopes) | good | BLOOM, MPT |

## 5.6 MQA and GQA

The KV cache (Section 9.2) stores K and V for every past token, every layer, every **KV head**. Reducing the number of KV heads shrinks it proportionally.

```text
H      = number of query heads
H_kv   = number of key/value heads
g      = H / H_kv   query heads per KV head (group size)

MHA (multi-head):        H_kv = H        g = 1
GQA (grouped-query):     1 < H_kv < H    g = H / H_kv     (LLaMA-2-70B, LLaMA-3: H_kv = 8)
MQA (multi-query):       H_kv = 1        g = H            (PaLM, Falcon-7B)

K/V projection parameters:  2 * D * H_kv * d_h      (MHA: 2 D^2)
KV cache bytes per token:   2 * n_layers * H_kv * d_h * bytes_per_elem
```

**Worked: LLaMA-3-70B** (`H = 64`, `H_kv = 8`, `d_h = 128`, 80 layers, BF16). GQA KV cache is `2 * 80 * 8 * 128 * 2 = 327,680 B/token`; MHA would be 8x that, `2,621,440 B/token` (2.6 MB). At a 128K context, one sequence's cache is 42.9 GB with GQA instead of 344 GB.

Why GQA rather than MQA: MQA saves the most memory but loses quality and training stability. GQA with 8 groups recovers nearly all of MHA's quality with most of MQA's savings (Ainslie et al., 2023, who also showed an existing MHA checkpoint can be "uptrained" to GQA by mean-pooling its K/V heads and continuing training for about 5% of the original compute).

Two second-order effects worth mentioning:

- **Decode arithmetic intensity.** In decode each KV element loaded from HBM is used by `g` query heads, so the attention part of decode does about `g` times more FLOPs per byte (Section 9.1). GQA makes decode attention less memory-bound, not just smaller.
- **Tensor parallelism.** Heads are split across TP ranks. With `H_kv = 8` and TP = 16, KV heads must be **replicated** (each KV head stored on 2 ranks), so the per-GPU KV saving stops scaling beyond TP = `H_kv`.

**MLA** (multi-head latent attention, DeepSeek-V2/V3) goes further: it caches a compressed low-rank latent per token (plus a small decoupled RoPE key) and up-projects to per-head K and V, cutting the cache well below GQA at similar quality.

## 5.7 Reference Implementation: GQA + RoPE + Causal Mask

```python
"""gqa_rope.py -- multi-head / grouped-query causal attention with RoPE, shapes annotated."""
import numpy as np


def rope(x, base=10000.0):
    """x: (..., T, d_head). Rotate each pair (x[2i], x[2i+1]) by angle pos * base^(-2i/d)."""
    T, d = x.shape[-2], x.shape[-1]
    inv_freq = base ** (-np.arange(0, d, 2) / d)             # (d/2,)
    ang = np.arange(T)[:, None] * inv_freq[None, :]          # (T, d/2)
    cos, sin = np.cos(ang), np.sin(ang)
    x1, x2 = x[..., 0::2], x[..., 1::2]
    out = np.empty_like(x)
    out[..., 0::2] = x1 * cos - x2 * sin
    out[..., 1::2] = x1 * sin + x2 * cos
    return out


def gqa_attention(x, Wq, Wk, Wv, Wo, n_heads, n_kv_heads):
    B, T, D = x.shape
    dh = D // n_heads
    g = n_heads // n_kv_heads                                # query heads per KV head
    q = (x @ Wq).reshape(B, T, n_heads, dh).transpose(0, 2, 1, 3)       # (B, H,   T, dh)
    k = (x @ Wk).reshape(B, T, n_kv_heads, dh).transpose(0, 2, 1, 3)    # (B, Hkv, T, dh)
    v = (x @ Wv).reshape(B, T, n_kv_heads, dh).transpose(0, 2, 1, 3)    # (B, Hkv, T, dh)
    q, k = rope(q), rope(k)                                  # positions enter only via Q and K
    k = np.repeat(k, g, axis=1)                              # (B, H, T, dh): each KV head serves g query heads
    v = np.repeat(v, g, axis=1)
    s = q @ k.transpose(0, 1, 3, 2) / np.sqrt(dh)            # (B, H, T, T)
    s = np.where(np.tril(np.ones((T, T), dtype=bool)), s, -np.inf)     # causal mask
    p = np.exp(s - s.max(-1, keepdims=True)); p /= p.sum(-1, keepdims=True)
    o = (p @ v).transpose(0, 2, 1, 3).reshape(B, T, D)       # concat heads
    return o @ Wo


rng = np.random.default_rng(0)
B, T, D, H, Hkv = 2, 10, 64, 8, 2
dh = D // H
x = rng.standard_normal((B, T, D))
Wq, Wo = rng.standard_normal((D, D)) / 8, rng.standard_normal((D, D)) / 8
Wk, Wv = rng.standard_normal((D, Hkv * dh)) / 8, rng.standard_normal((D, Hkv * dh)) / 8
y = gqa_attention(x, Wq, Wk, Wv, Wo, H, Hkv)
print("output shape:", y.shape, " K/V projection shape:", Wk.shape)

# Causality: changing a future token must not change earlier outputs.
x2 = x.copy(); x2[:, -1] += 1.0
print("causal ok:", np.allclose(y[:, :-1], gqa_attention(x2, Wq, Wk, Wv, Wo, H, Hkv)[:, :-1]))

# RoPE: <rope(q)_m, rope(k)_n> depends only on m - n.
qv, kv = rng.standard_normal(dh), rng.standard_normal(dh)
seq_q = rope(np.tile(qv, (50, 1))); seq_k = rope(np.tile(kv, (50, 1)))
print("relative-position ok:", np.isclose(seq_q[7] @ seq_k[3], seq_q[40] @ seq_k[36]))
```

```text
output shape: (2, 10, 64)  K/V projection shape: (64, 16)
causal ok: True
relative-position ok: True
```

Production kernels never call `repeat` on K/V: they index the shared KV head (`kv_head = q_head // g`) so the cache is read once per group. The interleaved pair layout above (`0::2`, `1::2`) is the RoPE paper's; Hugging Face LLaMA uses the "rotate half" layout (pairs `i` and `i + d/2`). They are equivalent up to a fixed permutation of the projection weights, but mixing conventions between a checkpoint and a kernel is a classic silent-accuracy bug.

## 5.8 Interview Questions

**Q1.** Why divide by `sqrt(d_k)` and not `d_k`?

If `q` and `k` have i.i.d. unit-variance components, `q . k` has variance `d_k` and standard deviation `sqrt(d_k)`. Dividing by `sqrt(d_k)` makes the logits unit-variance independent of head size, which keeps the softmax out of saturation, where its Jacobian `diag(p) - pp^T` is nearly zero and gradients vanish. Dividing by `d_k` would shrink the variance to `1/d_k`, making attention nearly uniform for large heads at initialization. (muP deliberately uses `1/d_k` because under its parameterization `q` and `k` become correlated during training and the dot product grows like `d_k`; that is a follow-up, not the default answer.)

**Q2.** Give the shapes in multi-head attention for batch `B`, sequence `T`, model dim `D`, `H` heads.

Input `(B, T, D)`. Q, K, V after projection and reshape: `(B, H, T, d_h)` with `d_h = D/H`. Scores and probabilities: `(B, H, T, T)`. Output per head `(B, H, T, d_h)`, transposed and reshaped to `(B, T, D)`, then `W_O` gives `(B, T, D)`. Parameters `4D^2` for MHA. FLOPs: projections `8 B T D^2`, attention core `4 B T^2 D` (non-causal).

**Q3.** How does RoPE encode relative position, and why is it applied to Q and K but not V?

It rotates each 2-D pair of `q` and `k` by an angle proportional to the token's position. Rotations are orthogonal, so `<R_m q, R_n k> = <q, R_(n-m) k>`: the attention score depends on the content and on the offset `n - m` only. Position needs to influence *which* tokens are attended to, which is decided entirely by the `q . k` scores; `V` carries the content that gets mixed, so rotating it would only scramble the output. RoPE has no parameters, works with the KV cache (keys are cached already rotated at their absolute positions), and extends to longer contexts via frequency scaling (position interpolation, NTK scaling, YaRN).

**Q4.** A model has 64 query heads and 8 KV heads. What changes compared with MHA in parameters, KV cache, and decode speed?

K and V projections shrink from `2D^2` to `2D * 8 * d_h = D^2/4` (an 8x reduction for those two matrices; total layer parameters drop modestly). The KV cache shrinks 8x. Decode attention reads 8x fewer bytes per token and its arithmetic intensity rises from about 1 to about 8 FLOP/byte (each loaded KV element serves 8 query heads). Memory saved can be spent on larger batches or longer contexts, which is usually where the real throughput gain comes from. Attention FLOPs do not change because there are still 64 query heads.

**Q5.** Why does a causal decoder train on all positions in parallel but generate one token at a time?

In training the whole target sequence is known, so with a causal mask every position computes its next-token prediction in one forward pass using only past tokens: `T` training signals per sequence, fully parallel. In generation, token `t+1` does not exist until token `t` has been sampled, so the dependency is sequential. The KV cache avoids recomputing keys and values of the prefix, but each step still needs a full forward pass for one new token, which makes decode memory-bound (Section 9.1).

---

# 6. The Transformer Decoder Block

## 6.1 Pre-Norm vs Post-Norm

```text
Post-norm (original Transformer, BERT):   x = Norm(x + Attn(x));       x = Norm(x + FFN(x))
Pre-norm  (GPT-2 onward, LLaMA):          x = x + Attn(Norm(x));       x = x + FFN(Norm(x))
                                           ... final Norm before the LM head
```

| | Post-norm | Pre-norm |
|---|---|---|
| Residual path | passes through a normalization after every block | pure identity from input to output |
| Gradient at initialization | large near the output, so it needs careful LR warmup (Xiong et al., 2020) | well-behaved; trains without long warmup |
| Depth scaling | unstable for very deep stacks without tricks (DeepNorm) | stable to 100+ layers |
| Final quality when it trains | sometimes slightly better | slightly worse per layer: the residual stream grows with depth, so later layers contribute relatively less |
| Extra piece | none | needs a final norm before the output projection |

Pre-norm won because stability at scale matters more than a small quality edge. Variants address its weaknesses: sandwich norm (norm before and after each branch), QK-norm (normalize `q` and `k` to stop attention logits from growing), and scaled residual initialization (scale the output projection of each block by `1/sqrt(2 * n_layers)` at init, as in GPT-2).

## 6.2 Feed-Forward Networks: GELU and SwiGLU

```text
Classic FFN:   FFN(x) = W_2 GELU(W_1 x)                          W_1: D -> 4D, W_2: 4D -> D,  params 8 D^2
SwiGLU FFN:    FFN(x) = W_down( SiLU(W_gate x) * (W_up x) )      three matrices, D <-> d_ff,   params 3 D d_ff
               SiLU(z) = z * sigmoid(z)    (also called Swish)
```

Gated linear units (Shazeer, "GLU Variants Improve Transformer", 2020) multiply a gated branch by a linear branch, giving multiplicative interactions; SwiGLU consistently improves quality per FLOP. To keep parameters equal to the classic `8D^2`, set `d_ff = (2/3) * 4D = 8D/3`, then round to a hardware-friendly multiple: LLaMA-2-7B uses `D = 4096`, `d_ff = 11008`. LLaMA-3-70B uses `d_ff = 28672 = 3.5D`, a little wider than parameter-neutral.

The FFN holds about two thirds of the parameters and FLOPs of a dense layer. Kernel-wise, `W_gate` and `W_up` are usually concatenated into one GEMM, and the `SiLU(a) * b` is fused into its epilogue.

## 6.3 Mixture of Experts Routing

An MoE layer replaces the single FFN with `E` expert FFNs and a **router**. Each token runs through only `k` experts, so parameter count grows with `E` while FLOPs per token grow only with `k`.

```text
router logits  r = x W_r                     W_r: (D, E)
top-k          idx = topk(r, k)
gates          g = softmax(r[idx])           (or softmax over all E, then take top-k and renormalize)
output         y = sum_{i in idx} g_i * Expert_i(x)
```

Key mechanics:

- **Load balancing.** Without pressure, the router collapses onto a few experts. Switch Transformer adds an auxiliary loss `L_aux = alpha * E * sum_i f_i * P_i`, where `f_i` is the fraction of tokens routed to expert `i` and `P_i` the mean router probability for `i` (`alpha ~ 0.01`); it is minimized by a uniform distribution. DeepSeek-V3 instead adds a per-expert bias to the routing scores, nudged up or down depending on load ("auxiliary-loss-free" balancing).
- **Capacity factor.** With static shapes each expert processes at most `capacity = CF * k * tokens / E` tokens; overflow tokens are dropped (they skip the layer via the residual). Dropless implementations (MegaBlocks-style grouped GEMMs) avoid this at the cost of variable-size work.
- **Expert parallelism (EP).** Experts live on different GPUs. Each MoE layer does an **all-to-all** to dispatch tokens to expert owners and another to combine results, so interconnect bandwidth and routing skew dominate performance.
- **Shared experts.** Some designs (DeepSeek) add always-on shared experts for common knowledge plus many fine-grained routed experts.

Examples: Mixtral 8x7B: 8 experts, top-2, about 46.7B total parameters, about 12.9B active per token. DeepSeek-V3: 671B total, 37B active, 1 shared + 256 routed experts with top-8 routing.

Inference implications: **memory scales with total parameters** (all experts must be resident), **compute with active parameters**. At batch 1, decode reads only the chosen experts' weights, but at large batch nearly every expert is hit each step, so the bytes read per step approach the full model while FLOPs stay at the active count. MoE decode is therefore even more memory-bound than dense decode at moderate batch sizes.

## 6.4 Parameter Count of a Decoder Layer

General formula (no biases, `H * d_h = D`):

```text
Attention:   W_Q: D x D,   W_K, W_V: D x (H_kv d_h) each,   W_O: D x D     ->  2 D^2 + 2 D H_kv d_h
FFN:         SwiGLU: 3 D d_ff          classic GELU with d_ff = 4D: 8 D^2
Norms:       2 D (two gains; LayerNorm adds 2 D biases)
Layer total (MHA + classic 4D FFN):   4 D^2 + 8 D^2 = 12 D^2
Model:       N ~ 12 * n_layers * D^2  +  V D (embedding)  [+ V D if the LM head is untied]
```

**Sanity check, GPT-3 175B** (`n_layers = 96`, `D = 12288`, `V = 50257`, tied): `12 * 96 * 12288^2 = 173.9B`, plus `50257 * 12288 = 0.62B` embedding, about 174.6B. That matches the published 175B, and it is the standard "derive it at the whiteboard" check.

**Worked: LLaMA-3-70B** (`n_layers = 80`, `D = 8192`, `H = 64`, `H_kv = 8`, `d_h = 128`, `d_ff = 28672`, `V = 128256`, untied):

| Component | Formula | Parameters |
|---|---|---|
| `W_Q` | `8192 x 8192` | 67,108,864 |
| `W_K` and `W_V` | `2 x 8192 x 1024` | 16,777,216 |
| `W_O` | `8192 x 8192` | 67,108,864 |
| FFN (gate, up, down) | `3 x 8192 x 28672` | 704,643,072 |
| 2 RMSNorm gains | `2 x 8192` | 16,384 |
| **Per layer** | | **855,654,400** |
| 80 layers | | 68,452,352,000 |
| Embedding + LM head | `2 x 128256 x 8192` | 2,101,346,304 |
| Final norm | | 8,192 |
| **Total** | | **70,553,706,496 (70.6B)** |

Observations: the FFN is 82% of each layer; GQA makes attention only 18%; embeddings are 3% of the total (much more for small models with large vocabularies: in LLaMA-3-8B they are about 13%).

## 6.5 Interview Questions

**Q1.** Derive the `12 D^2` per-layer parameter count. Where does the rest of a model's parameter count come from?

Attention has four `D x D` projections (Q, K, V, O): `4D^2`. The FFN has `D x 4D` and `4D x D`: `8D^2`. Biases and norms add `O(D)`, which is negligible. So `N ~ 12 L D^2` for the stack, plus the embedding `V D` (and an untied LM head, another `V D`). With GQA the K and V projections shrink to `2 D H_kv d_h`; with SwiGLU the FFN is `3 D d_ff`, which equals `8D^2` when `d_ff = 8D/3`.

**Q2.** Why did pre-norm replace post-norm?

In post-norm the normalization sits on the residual path, so the gradient flowing to early layers passes through every LayerNorm, and at initialization the gradients near the output are large; training diverges without a long, carefully tuned warmup, and very deep stacks are unstable. Pre-norm keeps a clean identity path from the loss to every layer, so gradients flow like in a ResNet and deep models train with standard schedules. The cost is that the residual stream's norm grows with depth so each later layer's relative contribution shrinks, which slightly reduces quality per parameter. A final norm before the LM head is required.

**Q3.** Mixtral 8x7B is called a "47B model with 13B active parameters". What does that mean for training and serving?

Each token's forward pass goes through attention (shared) and 2 of 8 expert FFNs, so FLOPs per token are those of a ~13B dense model: training costs about `6 * 12.9e9` FLOPs per token and decode compute is about `2 * 12.9e9` per token. But all 46.7B parameters must sit in memory (about 93 GB in BF16), and at realistic batch sizes most experts are activated each step, so decode reads close to the full weight set: it is memory-bound like a ~47B model while computing like a ~13B one. Expert parallelism adds all-to-all communication, and routing imbalance causes stragglers.

**Q4.** What is the purpose of the load-balancing loss in MoE, and what happens without it?

Routers have a rich-get-richer dynamic: an expert that gets more tokens trains faster, becomes better, and attracts more tokens. Without balancing, a few experts take most of the traffic, the rest are wasted parameters, and with capacity limits many tokens get dropped; with expert parallelism the overloaded GPUs become stragglers. The auxiliary loss `E * sum f_i P_i` is minimized when routing is uniform. Too strong a weight hurts quality (it overrides the router's preferences), which motivated bias-based balancing that does not add gradient interference.

**Q5.** Why does SwiGLU use `d_ff = 8D/3` instead of `4D`?

SwiGLU has three weight matrices instead of two. With `d_ff = 4D` it would have `12D^2` FFN parameters instead of `8D^2`. Choosing `d_ff = (2/3) * 4D` keeps the parameter count and FLOPs equal to the classic FFN, so comparisons are fair; the result is rounded to a multiple of 64 or 256 for efficient GEMM tiling (11008 for `D = 4096`).

---

# 7. FLOP Accounting and Scaling Laws

## 7.1 Forward Pass: About 2N FLOPs per Token

A matrix-vector product with a `m x n` weight matrix costs `m * n` multiply-adds, which is `2mn` FLOPs. In a Transformer almost every parameter is a GEMM weight used exactly once per token. So:

```text
forward FLOPs per token ~ 2 N     (N = non-embedding parameters + LM head; embedding lookups are free)
```

For a prompt of `T` tokens, prefill costs about `2 N T` plus attention (7.3). Each generated token costs about `2N` plus attention over the cache. LLaMA-3-70B: `2 * 70.6e9 = 1.41e11` FLOPs per token; a 2,000-token prompt is about `2.8e14` FLOPs, which takes about 0.22 s at a perfectly utilized 1307 TFLOP/s and longer in practice.

## 7.2 Training: About 6ND

The backward pass computes two GEMMs per forward GEMM (`dX` and `dW`, Section 2.1), so it costs about `4N` FLOPs per token. Forward plus backward:

```text
training FLOPs  C ~ 6 N D        (D = number of training tokens)
with full activation recomputation: ~ 8 N D (one extra forward)
```

**Model FLOPs Utilization (MFU)** = `(6 N * tokens per second) / (number of GPUs * peak FLOP/s)`. It counts only the useful `6N` (recomputation does not count; that variant is "hardware FLOPs utilization", HFU). Good large-scale dense training runs reach roughly 35-55% MFU; communication, pipeline bubbles, memory-bound ops (norms, activations, optimizer), and stragglers eat the rest.

## 7.3 The Attention FLOP Term

The `2N` rule ignores the score and value products, which have no parameters. Per token per layer, attending over a context of `n_ctx` tokens costs `2 * n_ctx * D` for `q K^T` and `2 * n_ctx * D` for `P V` (summed over heads, `H * d_h = D`):

```text
non-causal, per token, forward:   4 * n_layers * n_ctx * D
causal (average context n_ctx/2): 2 * n_layers * n_ctx * D        <- Kaplan et al.'s term
forward per token ~ 2N + 2 n_layers n_ctx D;   training per token ~ 6N + 6 n_layers n_ctx D

ratio attention / dense ~ (2 n_layers n_ctx D) / (2 * 12 n_layers D^2) = n_ctx / (12 D)
```

So attention FLOPs are a small correction until `n_ctx` approaches `12D`. For LLaMA-3-70B (`D = 8192`): about 2% at 2K context, 8% at 8K, 30% at 32K, and they dominate beyond about 100K. Note that GQA does not reduce attention FLOPs (there are still `H` query heads); it reduces bytes.

## 7.4 Calculator and Worked Training-Time Estimate

```python
"""llm_calc.py -- parameter count, FLOPs, and KV-cache size for a LLaMA-style decoder."""
from dataclasses import dataclass


@dataclass
class Cfg:
    name: str
    n_layers: int
    d_model: int
    n_heads: int
    n_kv_heads: int
    d_ff: int          # SwiGLU hidden size
    vocab: int
    tied_embeddings: bool = False

    @property
    def d_head(self) -> int:
        return self.d_model // self.n_heads

    def layer_params(self) -> int:
        d, kv = self.d_model, self.n_kv_heads * self.d_head
        attn = d * d + 2 * d * kv + d * d          # Wq, Wk, Wv, Wo (no biases in LLaMA)
        ffn = 3 * d * self.d_ff                    # W_gate, W_up, W_down
        norms = 2 * d                              # two RMSNorm gains
        return attn + ffn + norms

    def total_params(self) -> int:
        emb = self.vocab * self.d_model
        head = 0 if self.tied_embeddings else self.vocab * self.d_model
        return self.n_layers * self.layer_params() + emb + head + self.d_model  # + final norm

    def kv_bytes_per_token(self, bytes_per_elem: float = 2) -> float:
        return 2 * self.n_layers * self.n_kv_heads * self.d_head * bytes_per_elem   # 2 = K and V


llama3_70b = Cfg("LLaMA-3-70B", n_layers=80, d_model=8192, n_heads=64, n_kv_heads=8,
                 d_ff=28672, vocab=128256)
llama3_8b = Cfg("LLaMA-3-8B", n_layers=32, d_model=4096, n_heads=32, n_kv_heads=8,
                d_ff=14336, vocab=128256)

if __name__ == "__main__":
    for c in (llama3_8b, llama3_70b):
        N = c.total_params()
        kv = c.kv_bytes_per_token(2)
        print(f"{c.name}: params = {N / 1e9:.2f} B  (per layer {c.layer_params() / 1e6:.1f} M)")
        print(f"  KV cache (BF16) = {kv:,.0f} B/token = {kv / 2**20:.3f} MiB/token; "
              f"MHA would be {kv * c.n_heads // c.n_kv_heads:,.0f} B/token")
    c = llama3_70b
    N = c.total_params()
    W = 2 * N                                     # BF16 weights, bytes
    print(f"\n{c.name} BF16 weights = {W / 1e9:.1f} GB")
    print(f"Training FLOPs on 15T tokens ~ 6ND = {6 * N * 15e12:.2e}")
    for ctx in (2048, 8192, 32768):
        attn = 2 * c.n_layers * ctx * c.d_model   # causal-average attention FLOPs/token (forward)
        print(f"  forward FLOPs/token @ ctx {ctx:>5}: 2N = {2 * N:.3e}, attention = {attn:.3e} "
              f"({attn / (2 * N):.1%} of 2N)")
    days = 6 * N * 15e12 / (1024 * 0.40 * 1307.4e12) / 86400
    print(f"  on 1024 GPUs at 1307.4 TFLOP/s peak and 40% MFU: {days:.0f} days")
```

```text
LLaMA-3-8B: params = 8.03 B  (per layer 218.1 M)
  KV cache (BF16) = 131,072 B/token = 0.125 MiB/token; MHA would be 524,288 B/token
LLaMA-3-70B: params = 70.55 B  (per layer 855.7 M)
  KV cache (BF16) = 327,680 B/token = 0.312 MiB/token; MHA would be 2,621,440 B/token

LLaMA-3-70B BF16 weights = 141.1 GB
Training FLOPs on 15T tokens ~ 6ND = 6.35e+24
  forward FLOPs/token @ ctx  2048: 2N = 1.411e+11, attention = 2.684e+09 (1.9% of 2N)
  forward FLOPs/token @ ctx  8192: 2N = 1.411e+11, attention = 1.074e+10 (7.6% of 2N)
  forward FLOPs/token @ ctx 32768: 2N = 1.411e+11, attention = 4.295e+10 (30.4% of 2N)
  on 1024 GPUs at 1307.4 TFLOP/s peak and 40% MFU: 137 days
```

**Worked estimate (the interview version).** "How long to train a 70B model on 15T tokens on 1024 MI300X?" `C = 6 * 70e9 * 15e12 = 6.3e24` FLOPs. Sustained throughput is `1024 * 1.31e15 * 0.4 = 5.4e17` FLOP/s. Time is `6.3e24 / 5.4e17 = 1.2e7 s`, about 137 days. State the assumptions (MFU, BF16 dense peak, no failures) and the levers: more GPUs, FP8 (2x peak matrix FLOPs), better MFU, fewer tokens.

## 7.5 Scaling Laws: Kaplan vs Chinchilla

Empirically, pretraining loss follows smooth power laws in parameters `N`, data `D`, and compute `C ~ 6ND`, over many orders of magnitude. The practical question is: **for a fixed compute budget, how should `C` be split between `N` and `D`?**

| | Kaplan et al. (OpenAI, 2020) | Hoffmann et al. "Chinchilla" (DeepMind, 2022) |
|---|---|---|
| Compute-optimal allocation | `N_opt ~ C^0.73`, `D_opt ~ C^0.27` | `N_opt ~ C^0.5`, `D_opt ~ C^0.5` |
| Implied recipe | grow the model much faster than the data | grow both equally: about **20 tokens per parameter** |
| Example | GPT-3: 175B params, 300B tokens (~1.7 tokens/param) | Chinchilla: 70B params, 1.4T tokens, beat Gopher (280B params, 300B tokens) at the same compute |
| Loss form | separate power laws `L(N)`, `L(D)`, `L(C)` | `L(N, D) = E + A / N^alpha + B / D^beta` (paper's fit: `E = 1.69`, `A = 406.4`, `B = 410.7`, `alpha = 0.34`, `beta = 0.28`) |

Why they disagree: Kaplan's runs used a learning-rate schedule that was not matched to each run's token count (so models trained on more tokens looked worse than they would with a properly decayed schedule), smaller models, and non-embedding parameter counts. Chinchilla tuned the cosine schedule to each run's length and fit across three independent methods. A later replication (Besiroglu et al., 2024) found issues in the paper's parametric fit, but the roughly 20 tokens-per-parameter conclusion held.

**Worked Chinchilla allocation.** With `C = 6ND` and `D = 20N`, `C = 120 N^2`, so `N = sqrt(C / 120)`. For `C = 1e24` FLOPs: `N = sqrt(8.3e21) ~ 91B` parameters and `D ~ 1.8T` tokens. Check against Chinchilla itself: `6 * 70e9 * 1.4e12 = 5.9e23`, and `sqrt(5.9e23 / 120) = 70B`.

**Compute-optimal is not deployment-optimal.** Chinchilla minimizes *training* compute for a target loss. Serving cost scales with `N` times tokens served, so it pays to **over-train** a smaller model well past 20 tokens per parameter: LLaMA-3-8B saw about 15T tokens, roughly 1,900 tokens per parameter, and loss was still improving. Other caveats: the data wall (high-quality tokens are finite; repeated epochs give diminishing returns after about 4), downstream abilities do not track loss perfectly, and inference-time compute (reasoning models, sampling more) is a separate scaling axis.

## 7.6 Interview Questions

**Q1.** Where does `6ND` come from?

Each parameter participates in one multiply-add per token in the forward pass: 2 FLOPs per parameter per token, so `2N` per token. The backward pass needs, for every weight matrix, the gradient with respect to its input (`dY W^T`) and with respect to the weight (`X^T dY`), each as expensive as the forward GEMM: `4N`. Total `6N` per token, `6ND` for `D` tokens. It ignores attention-score FLOPs (relative size `n_ctx / 12D`), norms and activations (memory-bound, few FLOPs), and recomputation (adds `2N` if all activations are recomputed).

**Q2.** Estimate the per-token decode FLOPs of LLaMA-3-70B at a 32K context and say whether attention matters.

Dense part: `2N = 1.41e11`. Attention: `2 * n_layers * n_ctx * D = 2 * 80 * 32768 * 8192 = 4.3e10` (causal average) or about `8.6e10` for a token at the very end of a 32K context (it attends to all 32K keys, so use the non-causal per-token formula `4 * n_layers * n_ctx * D`). So attention adds 30-60% to the FLOPs at that length. But decode is memory-bound, so the more important number is bytes: the KV cache at 32K is `32768 * 327,680 B = 10.7 GB` per sequence, compared with 141 GB of weights shared by the whole batch.

**Q3.** You have a budget of `1e23` FLOPs. What model size and token count does Chinchilla suggest? Would you actually use it?

`N = sqrt(1e23 / 120) = sqrt(8.3e20) ~ 29B` parameters, `D = 20N ~ 580B` tokens. If the model will be served heavily, I would choose a smaller model trained on more tokens (for example 8-13B on 1.3-2T tokens): slightly higher training cost for the same loss, but much cheaper inference, and the total cost over the model's lifetime is lower. I would also check that 580B+ unique high-quality tokens are available.

**Q4.** What is MFU and why is it never 100%?

MFU = achieved model FLOPs per second (`6N` times tokens per second) divided by aggregate peak FLOP/s. Losses come from memory-bound ops (norms, softmax, activations, optimizer step, embedding), communication not overlapped with compute (all-reduce, all-gather, pipeline bubbles), GEMM shapes that do not fill the matrix units, kernel launch gaps, data loading, and failures/restarts. Peak numbers also assume ideal clocks; sustained clocks under power limits are lower. 40-50% is good for large dense models.

**Q5.** Why does attention's FLOP share grow with context but its byte share matters even more for inference?

FLOP share is `n_ctx / 12D`, which is linear in context. For decode, though, the binding constraint is bytes: weights are read once per step and shared across the batch, but each sequence's KV cache is read in full every step and is not shared. At long contexts and large batches the KV reads exceed the weight reads (Section 9.3), so attention dominates decode time long before it dominates FLOPs.

---

# Part 3: FlashAttention

---

# 8. FlashAttention

FlashAttention (Dao et al., 2022) computes **exact** attention (not an approximation) without ever writing the `N x N` score or probability matrices to HBM. It is the canonical example of an **IO-aware** algorithm: same math, far fewer bytes moved. For framework-level usage and the Triton tutorial kernel see [ML_AI_Frameworks.md, Section 27](../ml-gpu/ML_AI_Frameworks.md#27-key-triton-kernels-matmul-attention-softmax); for a kernel-level walkthrough see [GPU Kernel Case Studies](../ml-gpu/GPU_Kernel_Case_Studies.md); for the roofline reasoning used below see [Performance Engineering, Section 3](../computer-science/Performance_Engineering.md#3-roofline-model).

## 8.1 Why Standard Attention Is Memory-Bound

The naive implementation runs three kernels, each round-tripping an `N x N` tensor through HBM:

```text
S = Q K^T            write S (N^2)
P = softmax(S)       read S, write P (N^2 + N^2)
O = P V              read P (N^2)
HBM traffic ~ 4 N^2 + 4 N d elements;  extra memory O(N^2)
```

**Worked numbers, one head, `N = 8192`, `d = 128`, FP16:** Q, K, V, O are 2 MiB each; S and P are 128 MiB each. Traffic is about `4 * 128 MiB + 8 MiB ~ 545 MB`. FLOPs are `4 N^2 d = 3.4e10`. Arithmetic intensity is `3.4e10 / 5.45e8 ~ 63 FLOP/B`, well below MI300X's FP16 ridge point of about 247 FLOP/B, so the naive version is memory-bound: about 103 us of HBM time vs 26 us of matrix-core time. The softmax kernel in the middle has an intensity of a few FLOP/B and is purely bandwidth-limited.

**FlashAttention's idea:** tile Q into row blocks and stream K and V through on-chip memory (registers and LDS/shared memory) block by block, computing the softmax **incrementally** so `S` and `P` live only on chip. The extra memory drops to `O(N)` (one running max and sum per row). The paper proves an HBM-access bound of `Theta(N^2 d^2 / M)` for on-chip memory size `M`, versus `Theta(N d + N^2)` for the standard algorithm, and shows that no exact algorithm can do asymptotically better for all `M`. In practice the K/V re-reads across query blocks of the same head are served mostly by L2 / Infinity Cache (all query blocks of a head stream the same K/V at about the same time), so HBM traffic approaches the `4 N d` minimum. With `4Nd` elements of traffic the same example has an intensity of about 4,000 FLOP/B: it becomes **compute-bound**, and the remaining bottlenecks are matrix-core utilization and the throughput of `exp`, which is what FlashAttention-2 and -3 attack.

## 8.2 The Online Softmax Recurrence

Safe softmax subtracts the max for numerical stability: `softmax(x)_i = exp(x_i - m) / sum_j exp(x_j - m)` with `m = max_j x_j`. Done naively that needs three passes (max, sum, normalize). The **online softmax** (Milakov and Gimelshein, 2018) computes the max and the normalizer in one pass by **rescaling** the partial sum whenever the max increases:

```text
m_0 = -inf,  l_0 = 0
for j = 1..n:
    m_j = max(m_{j-1}, x_j)
    l_j = l_{j-1} * exp(m_{j-1} - m_j) + exp(x_j - m_j)

Invariant: l_j = sum_{i<=j} exp(x_i - m_j)
Proof (induction): l_{j-1} * exp(m_{j-1} - m_j) = sum_{i<j} exp(x_i - m_{j-1}) * exp(m_{j-1} - m_j)
                                               = sum_{i<j} exp(x_i - m_j)        then add the j-th term.
```

The same trick extends to the attention **output**, which is what makes FlashAttention possible. Keep an unnormalized accumulator `o`:

```text
o_j = o_{j-1} * exp(m_{j-1} - m_j) + exp(x_j - m_j) * v_j        final output O = o_n / l_n
```

**Block form** (what the kernel actually does, for a block of query rows and a block of keys `S_blk = Q_blk K_blk^T / sqrt(d)`):

```text
m_new = max(m, rowmax(S_blk))
P~    = exp(S_blk - m_new)                    (on chip only)
alpha = exp(m - m_new)                        (per-row rescale factor for the old state)
l     = alpha * l + rowsum(P~)
O     = alpha * O + P~ V_blk                  (diag(alpha) times O)
m     = m_new
... after the last key block:  O = O / l,   save L = m + log(l) for the backward pass
```

```python
"""online_softmax.py -- one pass over x computing max and normalizer together."""
import math

def online_softmax(xs):
    m, l = -math.inf, 0.0
    for x in xs:                       # single streaming pass
        m_new = max(m, x)
        l = l * math.exp(m - m_new) + math.exp(x - m_new)
        m = m_new
    return [math.exp(x - m) / l for x in xs]   # second pass only to emit outputs

xs = [3.0, 1.0, 1000.0, -2.0]
ref_m = max(xs)
ref = [math.exp(x - ref_m) / sum(math.exp(t - ref_m) for t in xs) for x in xs]
print(online_softmax(xs))
print(all(abs(a - b) < 1e-15 for a, b in zip(online_softmax(xs), ref)))
```

```text
[0.0, 0.0, 1.0, 0.0]
True
```

**The state is mergeable.** Two partial results `(m1, l1, o1)` and `(m2, l2, o2)` over disjoint key ranges combine associatively: `m = max(m1, m2)`, `l = e^(m1-m) l1 + e^(m2-m) l2`, `o = e^(m1-m) o1 + e^(m2-m) o2`. That is what **Flash-Decoding / split-KV** uses at decode time: with one query token per sequence there is too little parallelism across queries, so the KV length is split across workgroups and the partial states are reduced at the end. The same merge combines attention over a shared prefix cache with attention over per-request suffixes, and the ring-attention / context-parallel algorithms merge partial states across GPUs.

```python
"""split_kv_merge.py -- partial attention states (m, l, o) over disjoint key ranges merge exactly (Flash-Decoding)."""
import numpy as np

rng = np.random.default_rng(7)
d, n = 64, 1000
q = rng.standard_normal(d)                       # one decode query
K, V = rng.standard_normal((n, d)), rng.standard_normal((n, d))


def partial(q, K, V):
    s = K @ q / np.sqrt(d)
    m = s.max()
    p = np.exp(s - m)
    return m, p.sum(), p @ V                     # running max, sum, unnormalized output


def merge(a, b):
    (m1, l1, o1), (m2, l2, o2) = a, b
    m = max(m1, m2)
    c1, c2 = np.exp(m1 - m), np.exp(m2 - m)
    return m, c1 * l1 + c2 * l2, c1 * o1 + c2 * o2


# Split the 1000 keys across 4 "workgroups", compute independently, then reduce.
parts = [partial(q, K[i:i + 250], V[i:i + 250]) for i in range(0, n, 250)]
m, l, o = parts[0]
for p in parts[1:]:
    m, l, o = merge((m, l, o), p)
m_ref, l_ref, o_ref = partial(q, K, V)
print("merged == full:", np.allclose(o / l, o_ref / l_ref))
```

```text
merged == full: True
```

## 8.3 Tiled Forward Pass: NumPy Reference

This is a faithful, loop-level model of the FlashAttention-2 forward pass: outer loop over query blocks (one workgroup each on a GPU), inner loop streaming key/value blocks, causal block skipping, and one normalization at the end. It matches naive attention to machine precision, including for a sequence length that is not a multiple of the block sizes and for logits large enough that an unstabilized `exp` would overflow.

```python
"""flash_attention_ref.py -- tiled attention forward with online softmax (FlashAttention-2 style), checked against naive."""
import numpy as np


def naive_attention(Q, K, V, causal=False):
    """Materializes the full (N, N) score matrix: O(N^2) extra memory."""
    d = Q.shape[-1]
    S = Q @ K.T / np.sqrt(d)                          # (Nq, Nk)
    if causal:
        S = np.where(np.tril(np.ones_like(S, dtype=bool)), S, -np.inf)
    S = S - S.max(axis=-1, keepdims=True)
    P = np.exp(S)
    return (P / P.sum(axis=-1, keepdims=True)) @ V


def flash_attention(Q, K, V, Br=16, Bc=32, causal=False):
    """Never materializes more than a (Br, Bc) block of scores.

    Per query row i we keep: m_i (running max of scores), l_i (running sum of
    exp(s - m_i)), and O_i (unnormalized output = sum_j exp(s_ij - m_i) v_j).
    When a new key block raises the max from m_old to m_new, every old term is
    off by exp(m_old - m_new), so we rescale l and O by that factor.
    """
    N, d = Q.shape
    scale = 1.0 / np.sqrt(d)
    O = np.zeros_like(Q)
    L = np.zeros(N)                                    # logsumexp, saved for backward
    for qs in range(0, N, Br):                         # outer loop: query blocks (parallel on GPU)
        q = Q[qs:qs + Br] * scale                      # (br, d) -- lives in registers/LDS
        br = q.shape[0]
        m = np.full(br, -np.inf)                       # running max
        l = np.zeros(br)                               # running denominator
        acc = np.zeros((br, d))                        # running unnormalized output
        kv_end = min(N, qs + br) if causal else N      # skip fully-masked key blocks
        for ks in range(0, kv_end, Bc):                # inner loop: stream K/V blocks
            k, v = K[ks:ks + Bc], V[ks:ks + Bc]
            s = q @ k.T                                # (br, bc) scores
            if causal:
                qi = np.arange(qs, qs + br)[:, None]
                kj = np.arange(ks, ks + k.shape[0])[None, :]
                s = np.where(kj <= qi, s, -np.inf)
            m_new = np.maximum(m, s.max(axis=1))
            alpha = np.exp(m - m_new)                  # rescale factor for old state (exp(-inf)=0 at start)
            p = np.exp(s - m_new[:, None])             # (br, bc), masked entries -> 0
            l = alpha * l + p.sum(axis=1)
            acc = alpha[:, None] * acc + p @ v
            m = m_new
        O[qs:qs + br] = acc / l[:, None]               # single normalization at the end (FA2)
        L[qs:qs + br] = m + np.log(l)
    return O, L


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    N, d = 100, 64                                     # N deliberately not a multiple of the block sizes
    Q, K, V = (rng.standard_normal((N, d)) for _ in range(3))
    Q *= 4.0                                           # large logits: naive exp without max-subtraction would overflow in fp16
    for causal in (False, True):
        ref = naive_attention(Q, K, V, causal)
        out, lse = flash_attention(Q, K, V, causal=causal)
        print(f"causal={causal!s:5}  max |flash - naive| = {np.abs(out - ref).max():.2e}  "
              f"allclose={np.allclose(out, ref, atol=1e-10)}")
```

```text
causal=False  max |flash - naive| = 2.66e-15  allclose=True
causal=True   max |flash - naive| = 2.22e-15  allclose=True
```

Points to call out when walking through this in an interview:

- **Mapping to the GPU.** Each `(batch, head, query block)` is one workgroup. `q`, `m`, `l`, and `acc` stay in registers for the whole inner loop; K/V tiles are staged through LDS (shared memory), ideally double-buffered so the next tile loads while the current one is in the matrix cores. The two matmuls (`q @ k.T`, `p @ v`) map to MFMA / Tensor Core instructions, accumulating in FP32.
- **Causal skipping.** `kv_end` stops the inner loop at the diagonal, which skips about half of all tiles. Only diagonal tiles need the element-wise mask.
- **The `-inf` edge case.** At the first block `m = -inf`, so `alpha = exp(-inf) = 0`, which correctly discards the empty state. If an entire row of a tile is masked while `m` is still `-inf`, `m_new = -inf` and `exp(-inf - (-inf))` is NaN. With causal masking and key blocks starting at 0, every row sees key 0 first, so it cannot happen here; real kernels with arbitrary masks (padding, sliding window, document masks) must guard for it, for example by substituting 0 for a `-inf` max.
- **Precision.** In a real kernel `p` is cast to FP16/BF16 (or FP8) before the `p @ v` matmul and the accumulator stays FP32. `l` and `m` are FP32.

## 8.4 Backward Pass and Recomputation

The forward saves only `O` (`N x d`) and the per-row logsumexp `L = m + log(l)` (`N` floats). The backward pass **recomputes** `S` and `P` tile by tile from `Q`, `K`, and `L` instead of reading a stored `N x N` matrix. Recomputation costs extra FLOPs (one more `QK^T`), but since the standard backward is memory-bound, it is still faster, and it saves `O(N^2)` memory.

```text
P    = exp(Q K^T / sqrt(d) - L)          recomputed exactly per tile
dV   = P^T dO
dP   = dO V^T
D_i  = rowsum(dO_i * O_i)                 (= sum_j P_ij dP_ij; precomputed in a small pre-kernel)
dS   = P * (dP - D)                       softmax backward, elementwise
dQ   = dS K / sqrt(d)
dK   = dS^T Q / sqrt(d)
```

The identity `sum_j P_ij dP_ij = dO_i . O_i` (because `dP_ij = dO_i . v_j` and `O_i = sum_j P_ij v_j`) is the trick that makes the softmax backward local to a tile: without it, each `dS` tile would need a full row of `P` and `dP`.

```python
"""flash_backward_ref.py -- FlashAttention backward formulas using only Q, K, V, O, dO and logsumexp L."""
import numpy as np

rng = np.random.default_rng(1)
N, d = 12, 8
Q, K, V, dO = (rng.standard_normal((N, d)) for _ in range(4))
scale = 1 / np.sqrt(d)


def forward(Q, K, V):
    S = Q @ K.T * scale
    m = S.max(axis=1, keepdims=True)
    P = np.exp(S - m)
    l = P.sum(axis=1, keepdims=True)
    return (P / l) @ V, (m + np.log(l)).ravel()          # O and logsumexp L (all FA saves)


O, L = forward(Q, K, V)

# Backward as FlashAttention does it: recompute P from L, never store it between passes.
P = np.exp(Q @ K.T * scale - L[:, None])                 # exact softmax probabilities, recomputed
dV = P.T @ dO
dP = dO @ V.T
Drow = (dO * O).sum(axis=1, keepdims=True)              # D_i = rowsum(dO_i * O_i) = sum_j P_ij dP_ij
dS = P * (dP - Drow)                                     # softmax backward
dQ = dS @ K * scale
dK = dS.T @ Q * scale

# Check against central differences of the scalar f = sum(O * dO).
def num_grad(X):
    g, h = np.zeros_like(X), 1e-6
    for idx in np.ndindex(X.shape):
        old = X[idx]
        X[idx] = old + h; fp = (forward(Q, K, V)[0] * dO).sum()
        X[idx] = old - h; fm = (forward(Q, K, V)[0] * dO).sum()
        X[idx] = old
        g[idx] = (fp - fm) / (2 * h)
    return g

for name, X, G in (("dQ", Q, dQ), ("dK", K, dK), ("dV", V, dV)):
    print(f"{name}: max abs error vs finite differences = {np.abs(num_grad(X) - G).max():.1e}")
```

```text
dQ: max abs error vs finite differences = 7.7e-10
dK: max abs error vs finite differences = 1.4e-09
dV: max abs error vs finite differences = 4.9e-10
```

In the kernel, the backward parallelizes over **key blocks** (each workgroup owns a `K_j, V_j` tile and accumulates `dK_j`, `dV_j` in registers while looping over query blocks); `dQ` contributions from different key blocks are accumulated with atomic adds in FP32 or written per block and reduced. Those atomics are one source of run-to-run non-determinism in attention backward; deterministic modes serialize the reduction at some speed cost.

## 8.5 FlashAttention-2

FlashAttention-2 (Dao, 2023) kept the algorithm and reorganized the work. Roughly 2x faster than FA1, reaching 50-73% of A100 peak in the forward pass.

| Change | Why it helps |
|---|---|
| Fewer non-matmul FLOPs: keep `O` unnormalized and divide by `l` once at the end; save only `L = m + log l` instead of both `m` and `l` | Non-matmul FLOPs (FP32 vector ALU, `exp`) are an order of magnitude slower than matrix-core FLOPs (A100: 312 TFLOP/s FP16 matrix vs 19.5 TFLOP/s FP32 vector), so every rescale removed matters |
| Parallelize over the sequence (query blocks) in addition to batch and heads | Long sequences with small batch had too few workgroups to fill all SMs/CUs |
| Swap the loop order in the forward: outer loop over Q blocks, inner over K/V | Each workgroup owns its output rows; no need to write partial `O` back to HBM per K/V block |
| Split Q (not K/V) across warps inside a workgroup | FA1 split K/V across warps ("split-K"), so warps had to exchange partial results through shared memory and synchronize; with Q split, each warp computes its rows independently |
| Support head dimension up to 256, MQA/GQA, varlen | Broader model coverage |

## 8.6 FlashAttention-3

FlashAttention-3 (Shah et al., 2024) is specific to NVIDIA Hopper (H100). The FA2 design left Hopper's asynchronous hardware idle and reached only about 35% of H100 peak. FA3 reaches about 740 TFLOP/s in FP16 (75% of peak) and close to 1.2 PFLOP/s in FP8.

| Technique | What it does |
|---|---|
| Warp specialization (producer/consumer) | Producer warps issue TMA (Tensor Memory Accelerator) asynchronous bulk copies of K/V tiles into shared memory; consumer warpgroups only run WGMMA (asynchronous warpgroup matrix multiply) and softmax. Registers are reallocated toward the consumers |
| Ping-pong scheduling between warpgroups | While warpgroup 1 runs its softmax, warpgroup 2 runs its GEMMs, and vice versa. The motivation: H100 SXM5 has 989 TFLOP/s of FP16 matmul but only about 3.9 TFLOP/s of special-function (`exp`) throughput, so softmax can otherwise stall the matrix units |
| Intra-warpgroup pipelining | Overlap the softmax of block `j` with the `QK^T` GEMM of block `j+1` |
| FP8 support | Block quantization (one scale per tile instead of per tensor) and "incoherent processing": multiply Q and K by a random orthogonal (Hadamard) matrix, which leaves `QK^T` unchanged but spreads outlier values, cutting FP8 quantization error. Also handles FP8 WGMMA's operand-layout requirement for V with in-kernel transposes |

The general lesson for an interview: once a kernel is compute-bound, the next limits are (1) overlapping data movement with compute and (2) keeping the low-throughput non-matmul work (here `exp`) from serializing with the matrix units. Those techniques depend on the hardware's async features, which is why each GPU generation gets its own FlashAttention variant.

## 8.7 FlashAttention on AMD GPUs

| Path | What it is | Notes |
|---|---|---|
| `ROCm/flash-attention`, CK backend (default) | Port of the `flash-attn` FA2 API built on Composable Kernel (CK) templates | Supports MI200 series, MI300X, MI355X, and RDNA 3/4; FP16/BF16 forward and backward |
| `ROCm/flash-attention`, Triton backend | Same Python API, Triton kernels provided by AMD's `aiter` package; enabled with `FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"` at install and run time | CDNA (MI200, MI300) and RDNA; FP16/BF16/FP32, FP8 through the FA3-style interface; causal, varlen, MQA/GQA, dropout, rotary, ALiBi, paged attention |
| PyTorch `scaled_dot_product_attention` on ROCm | The flash and memory-efficient SDPA backends are implemented with AOTriton (ahead-of-time compiled Triton kernels) | No extra install; what `torch.nn.functional.scaled_dot_product_attention` uses by default on ROCm |
| AITER (AI Tensor Engine for ROCm) | AMD's library of tuned kernels (CK-based, Triton, and hand-written assembly) for attention (prefill, decode, paged), MoE, GEMM, norms | Used by vLLM and SGLang on ROCm for MI300-class inference |

Porting considerations (why FA3's Hopper design does not transfer as-is, and what tuning looks like on CDNA):

- **Wavefront 64** instead of a 32-wide warp changes how rows of a tile map to lanes and how row reductions (`rowmax`, `rowsum`) are done (DPP/cross-lane ops).
- **MFMA instructions** (for example 32x32 and 16x16 output tiles on CDNA 3) replace `mma`/WGMMA; the accumulator layout determines how the softmax reads the `S` tile from registers.
- **LDS capacity** is 64 KB per CU on MI300X (CDNA 3; CDNA 4 on MI355X raises it to 160 KB), versus up to 228 KB of shared memory per SM on H100, which constrains tile sizes and the depth of double buffering.
- There is no TMA/warpgroup-async equivalent on CDNA 3, so overlap comes from software pipelining, multiple waves per SIMD, and instruction scheduling; Triton exposes AMD knobs such as `waves_per_eu`, `matrix_instr_nonkdim`, and `kpack`.
- MI300X's FP8 is the FNUZ variant (Section 12.2), so FP8 attention kernels and checkpoints must use the matching format or rescale.

In a profiler (rocprof-compute), a healthy FlashAttention forward shows high MFMA utilization, modest HBM bandwidth (most K/V traffic hits L2/MALL), and LDS bank conflicts near zero; a naive attention shows the opposite pattern (HBM-bound, low MFMA busy). See [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) for the counters.

## 8.8 Interview Questions

**Q1.** Explain the online softmax. Why is rescaling by `exp(m_old - m_new)` correct?

We maintain, for each query row, the running max `m` and `l = sum exp(s_i - m)` over the keys seen so far, plus `o = sum exp(s_i - m) v_i`. When a new block raises the max to `m_new`, each old term `exp(s_i - m_old)` should become `exp(s_i - m_new) = exp(s_i - m_old) * exp(m_old - m_new)`, so multiplying the old `l` and `o` by `exp(m_old - m_new)` makes them consistent with the new reference point; then add the new block's terms. Because `m_new >= m_old`, the factor is at most 1, so nothing overflows. At the end, `O = o / l` equals the exact softmax-weighted sum. The state is associative, so blocks can be processed in any order or in parallel and merged.

**Q2.** FlashAttention does more FLOPs than standard attention (in the backward it recomputes `QK^T`). Why is it faster?

Standard attention is memory-bound: it writes and reads `N x N` matrices to HBM several times, and the softmax kernel has an arithmetic intensity of a few FLOP/B. FlashAttention keeps `S` and `P` on chip, so HBM traffic drops from `O(N^2)` to roughly `O(Nd)` (with cache reuse), and the kernel becomes compute-bound on the matrix units. Time is `max(FLOPs / peak, bytes / bandwidth)`; reducing the dominant term (bytes) by 10-100x more than pays for about 25% more FLOPs. It also eliminates the `O(N^2)` activation memory, which is what enables long-context training.

**Q3.** What does FlashAttention save for the backward pass, and how does the backward compute `dS` without the full row of `P`?

It saves `O` and the per-row logsumexp `L` (plus the RNG state if dropout is used). In the backward it recomputes `P = exp(QK^T/sqrt(d) - L)` tile by tile. The softmax gradient is `dS_ij = P_ij (dP_ij - sum_k P_ik dP_ik)`, and the row sum equals `dO_i . O_i`, which is precomputed once per row (`D_i`). So each tile's `dS` needs only its own `P` and `dP` tiles plus the per-row scalar `D_i`.

**Q4.** What changed in FlashAttention-2 and FlashAttention-3?

FA2: fewer non-matmul FLOPs (normalize once at the end, store only logsumexp), parallelism over the query-sequence dimension, Q split across warps instead of K/V (removing inter-warp communication), the forward loop order swapped, and support for larger head dims and GQA. Result: about 2x over FA1. FA3 (Hopper): producer/consumer warp specialization with TMA asynchronous loads and asynchronous WGMMA, ping-pong scheduling so one warpgroup's softmax overlaps another's GEMMs (`exp` throughput is about 250x lower than FP16 matmul throughput on H100), intra-warpgroup pipelining, and FP8 with block scaling plus Hadamard "incoherent processing". Result: about 75% of H100 peak in FP16.

**Q5.** At decode time (one query token per sequence), why does a standard FlashAttention kernel under-utilize the GPU, and what fixes it?

FA parallelizes over batch, heads, and query blocks. In decode there is one query per sequence, so the grid is just `batch * heads` workgroups, each streaming a long KV cache serially; with small batches most CUs are idle and the latency is the time for one workgroup to stream the whole cache. Flash-Decoding (split-KV) splits the KV length across workgroups, each producing a partial `(m, l, o)`, then a small reduction merges them with the rescaling formula. Paged-attention decode kernels do the same over KV blocks. With GQA, kernels also process all `g` query heads that share a KV head together, so each KV tile is loaded once and used `g` times.

**Q6.** How would you test a new FlashAttention kernel for correctness?

Compare against a naive FP32 (or FP64) reference on random inputs across a grid of shapes: sequence lengths that are not multiples of the tile sizes, `N_q != N_k` (decode and chunked prefill), head dims 64/128/256, causal and non-causal, GQA ratios, varlen batches with padding, and large-magnitude inputs to stress the max-subtraction. Use tolerances appropriate for the dtype (for BF16 outputs roughly `atol ~ 1e-2`; better, compare the error against the error of the reference computed in the same low precision). Check the backward with the same grid plus gradient checks in FP64 on tiny shapes, test that fully masked rows do not produce NaNs, and test determinism (or document non-determinism) of `dQ`.

---

# Part 4: LLM Inference

---

For how vLLM and SGLang implement these ideas see [ML_AI_Frameworks.md, Sections 30-33](../ml-gpu/ML_AI_Frameworks.md#30-vllm-architecture-and-pagedattention); for an end-to-end "design an LLM serving system" walkthrough with capacity planning see [ML Systems Design](../ml-gpu/ML_Systems_Design.md).

# 9. Prefill, Decode, and the KV Cache

## 9.1 Prefill vs Decode: Arithmetic Intensity

Autoregressive generation has two phases with very different hardware behavior:

- **Prefill**: process the whole prompt (`T` tokens) in one forward pass, write its K/V into the cache, and produce the first output token.
- **Decode**: generate one token per sequence per forward pass, reading the whole cache, appending one K/V entry per layer.

**Weight GEMMs.** For a linear layer `d_in -> d_out` processing `T` tokens in BF16:

```text
FLOPs = 2 * T * d_in * d_out
bytes = 2 * d_in * d_out  (weights)  +  2 * T * (d_in + d_out)  (activations)
AI    = T * d_in * d_out / (d_in * d_out + T * (d_in + d_out))  ~  T      when T << d
```

So the arithmetic intensity of the weight GEMMs is roughly the **number of tokens in the forward pass**. Prefill with `T = 2048` and `d = 8192`: `AI ~ 1365 FLOP/B`. Decode with batch `B`: `T = B` tokens per step, so `AI ~ B`. MI300X's BF16 ridge point is about 247 FLOP/B (1307.4 TFLOP/s / 5.3 TB/s), so decode GEMMs stay memory-bound until roughly 250 sequences are batched together, and in practice KV memory capacity usually runs out first.

**Attention in decode.** Per new token per layer, attention does `4 * H * d_h * L` FLOPs (scores plus weighted sum over `L` cached tokens) and reads `2 * H_kv * d_h * L * 2` bytes of BF16 K and V:

```text
AI_attention(decode) = 4 H d_h L / (4 H_kv d_h L) = H / H_kv = g      (FP8 KV cache: 2g)
```

This does **not** improve with batch size: every sequence has its own cache. MHA decode attention runs at 1 FLOP/B; LLaMA-3-70B's GQA at 8 FLOP/B. Both are deep in memory-bound territory.

| | Prefill | Decode |
|---|---|---|
| Tokens per forward pass | `T` (prompt length; thousands) | `B` (one per active sequence) |
| Weight GEMM intensity | about `T` FLOP/B: compute-bound | about `B` FLOP/B: memory-bound |
| Attention | `O(T^2)` FLOPs, FlashAttention, compute-bound | reads the whole KV cache, intensity `g`, memory-bound |
| Bottleneck resource | matrix-core FLOP/s | HBM bandwidth (and KV capacity) |
| User-facing metric | TTFT | TPOT / ITL |
| Main optimizations | FlashAttention, FP8 GEMMs, chunking, prefix caching (skip recomputation) | batching, GQA/MLA, KV and weight quantization, paged attention, speculative decoding, split-KV kernels |

## 9.2 KV Cache Sizing With GQA

```text
KV bytes per token = 2 (K and V) * n_layers * n_kv_heads * d_head * bytes_per_element
KV bytes total     = KV bytes per token * sum over active sequences of (current length)
```

**Worked: LLaMA-3-70B** (80 layers, 8 KV heads, `d_head = 128`, FP16/BF16):

```text
2 * 80 * 8 * 128 * 2 = 327,680 bytes ~ 0.33 MB per token
8K-token sequence:   327,680 * 8192    = 2.68 GB
128K-token sequence: 327,680 * 131072  = 42.9 GB
MHA (64 KV heads) would be 8x:          2.6 MB per token
```

| Model | Layers | KV heads x d_head | Attention | KV bytes/token (16-bit) |
|---|---|---|---|---|
| LLaMA-2-7B | 32 | 32 x 128 | MHA | 524,288 (0.5 MB) |
| LLaMA-3-8B | 32 | 8 x 128 | GQA (g = 4) | 131,072 (0.13 MB) |
| LLaMA-3-70B | 80 | 8 x 128 | GQA (g = 8) | 327,680 (0.33 MB) |
| Same, FP8 KV cache | 80 | 8 x 128 | GQA | 163,840 (0.16 MB) |

**Capacity planning.** On one MI300X (192 GB) the BF16 weights (141 GB) leave about 32 GB after reserving 10% for activations and workspace: about 97K tokens of KV, only 11 concurrent 8K-token sequences. With 8 GPUs and TP = 8: `0.9 * 1536 - 141 = 1,241 GB`, about 3.8M tokens, or 462 concurrent 8K-token sequences. This is why KV capacity, not FLOPs, usually caps the batch size, and why GQA, FP8 KV, and weight quantization translate directly into throughput.

## 9.3 Decode Throughput Upper Bound and Batching Math

A decode step must read every weight once (shared by the batch) and every active sequence's KV cache once (not shared). In the memory-bound regime:

```text
step time (= TPOT)  >=  (weight bytes + sum_b L_b * KV bytes per token) / HBM bandwidth
throughput          <=  B / step time   (tokens/s)
compute check:          2 N B / peak FLOP/s  must be << step time for the bound to hold
```

```python
"""decode_bound.py -- memory-bandwidth upper bound on decode throughput for LLaMA-3-70B (BF16 weights and KV)."""

N = 70.55e9                     # parameters (see llm_calc.py)
W = 2 * N                       # BF16 weight bytes read once per decode step
KV_PER_TOKEN = 2 * 80 * 8 * 128 * 2          # 327,680 B: K and V x layers x KV heads x head_dim x 2 B
HBM_BW, HBM_CAP, PEAK = 5.3e12, 192e9, 1307.4e12   # MI300X: B/s, bytes, dense BF16 FLOP/s
N_DEV = 8                       # tensor parallel over 8 GPUs, assume perfect sharding, ignore comms

print(f"{'batch':>5} {'ctx':>7} {'KV GB':>7} {'fits':>5} {'TPOT ms':>8} {'tok/s':>7} {'compute ms':>10}")
for B, L in ((1, 4096), (32, 4096), (128, 4096), (256, 8192), (64, 131072)):
    kv_total = B * L * KV_PER_TOKEN                  # worst case: every sequence at full context
    step = (W + kv_total) / (N_DEV * HBM_BW)         # one decode step = read all weights + all KV once
    compute = 2 * N * B / (N_DEV * PEAK)             # 2N FLOPs per token (attention FLOPs ignored)
    fits = "yes" if W + kv_total < 0.9 * N_DEV * HBM_CAP else "NO"
    print(f"{B:>5} {L:>7} {kv_total / 1e9:>7.1f} {fits:>5} {step * 1e3:>8.2f} {B / step:>7.0f} {compute * 1e3:>10.3f}")

L = 8192
print(f"\nB -> infinity at ctx {L}: tok/s -> N_DEV*BW / (L * kv) = {N_DEV * HBM_BW / (L * KV_PER_TOKEN):,.0f}")
print(f"Single GPU, batch 1: BF16 weights {W / 1e9:.0f} GB -> <= {HBM_BW / W:.0f} tok/s; "
      f"INT4 weights (+1/64 B/param scales) -> <= {HBM_BW / (N * (0.5 + 1 / 64)):.0f} tok/s")
```

```text
batch     ctx   KV GB  fits  TPOT ms   tok/s compute ms
    1    4096     1.3   yes     3.36     298      0.013
   32    4096    42.9   yes     4.34    7372      0.432
  128    4096   171.8   yes     7.38   17345      1.727
  256    8192   687.2   yes    19.54   13105      3.454
   64  131072  2748.8    NO    68.16     939      0.863

B -> infinity at ctx 8192: tok/s -> N_DEV*BW / (L * kv) = 15,795
Single GPU, batch 1: BF16 weights 141 GB -> <= 38 tok/s; INT4 weights (+1/64 B/param scales) -> <= 146 tok/s
```

How to read it (each of these is a classic interview point):

1. **Batching is almost free at first.** From `B = 1` to `B = 32`, TPOT grows from 3.4 to 4.3 ms while throughput grows 25x, because the weight read is amortized across the batch.
2. **Then the KV cache takes over.** At `B = 256` and 8K context, KV reads (687 GB) are 5x the weights (141 GB). Throughput *falls* compared with `B = 128` at 4K, and approaches the ceiling `aggregate BW / (L * KV bytes per token)` (15.8K tok/s at 8K context) no matter how large the batch. Long contexts are expensive because of bytes, not FLOPs.
3. **Compute is never the limit here.** The compute column stays far below the step time, which confirms the memory-bound model. Decode would become compute-bound only near `B ~ 250` with short contexts.
4. **Capacity is a hard wall.** 64 sequences at 128K do not fit even on 8 GPUs; the scheduler must cap concurrency or preempt.
5. **These are upper bounds.** Achievable HBM bandwidth is typically 70-85% of the peak, and tensor parallelism adds two all-reduces per layer (160 per step for 80 layers); at small batch their latency is a significant fraction of a 3-4 ms step.

**Little's law for sizing** (see [Performance Engineering, Section 4](../computer-science/Performance_Engineering.md#4-littles-law-and-queueing)): concurrency = arrival rate x time in system. To serve 20 requests/s, each generating 500 tokens at a 20 ms TPOT (10 s of decode each), you need about `20 * 10 = 200` sequences in flight. At an average context of 3,000 tokens that is `200 * 3000 * 0.33 MB ~ 197 GB` of KV cache for LLaMA-3-70B, which sets the minimum GPU count before any FLOP calculation.

## 9.4 Interview Questions

**Q1.** Why is decode memory-bound while prefill is compute-bound? Quantify it.

Weight GEMM arithmetic intensity is about the number of tokens processed per forward pass. Prefill processes the whole prompt (thousands of tokens), giving intensity in the thousands of FLOP/B, above MI300X's BF16 ridge of about 247, so it is compute-bound. Decode processes one token per sequence, so intensity is about the batch size `B`; it stays memory-bound until `B` approaches 250. Decode attention has intensity `H/H_kv` (1 for MHA, 8 for LLaMA-3-70B) independent of batch, since each sequence reads its own cache.

**Q2.** Compute the KV cache for LLaMA-3-70B serving 32 users at 16K context in BF16. Does it fit on one MI300X?

Per token: `2 * 80 * 8 * 128 * 2 = 327,680 B`. Tokens: `32 * 16384 = 524,288`. Total: `1.72e11 B = 172 GB`. Plus 141 GB of weights is 313 GB, more than 192 GB. Options: tensor parallelism across 2 or more GPUs, FP8 KV cache (86 GB), INT4/FP8 weights (35-71 GB), or fewer concurrent users. A common answer is FP8 weights + FP8 KV on two GPUs, or TP = 4 for headroom.

**Q3.** What is the theoretical maximum decode speed of a 70B BF16 model at batch 1 on one MI300X, and how would you make it faster?

Every token must read all 141 GB of weights: `5.3 TB/s / 141 GB ~ 38 tok/s` (about 26 ms per token), and realistically 70-80% of that. To go faster: quantize weights (INT4 weight-only: about 36 GB including scales, upper bound about 146 tok/s; FP8: about 75 tok/s), split across GPUs with tensor parallelism (aggregate bandwidth; 8 GPUs gives about 300 tok/s minus communication), or use speculative decoding to emit several tokens per weight read. A smaller model (distillation) is the other lever.

**Q4.** Your serving throughput stops improving when you increase the batch size from 128 to 256. Why?

Likely one of: (a) the KV cache bytes now dominate the step (each sequence's cache is read every step and is not amortized), so throughput approaches `BW / (L * KV bytes per token)`; (b) KV capacity is exhausted, so the scheduler is preempting or queueing and the effective batch is smaller than configured; (c) the weight GEMMs have reached the ridge point and become compute-bound (only at short contexts). Check by measuring the actual running batch size, KV-cache utilization, and achieved HBM bandwidth vs achieved FLOP/s per step in a profiler.

**Q5.** Why does GQA help decode throughput more than the KV-size reduction alone suggests?

Smaller per-token KV means (1) more sequences fit, so the weight read is amortized over a larger batch, (2) each decode step reads fewer KV bytes, so TPOT at a given batch is lower, and (3) attention's arithmetic intensity rises from 1 to `g`, which lets the decode attention kernel use the bandwidth more efficiently (one KV tile serves `g` query heads). Effects (1) and (2) compound.

---

# 10. Serving Metrics and Scheduling

## 10.1 TTFT, TPOT, ITL, Throughput, Goodput

| Metric | Definition | Dominated by | Who cares |
|---|---|---|---|
| **TTFT** (time to first token) | request arrival to first output token | queueing + prefill (+ tokenization, network) | interactive chat, perceived responsiveness |
| **TPOT** (time per output token) | `(E2E - TTFT) / (output_tokens - 1)`, averaged per request | decode step time, which grows with batch size and context | streaming smoothness, long outputs |
| **ITL** (inter-token latency) | gap between consecutive tokens, a per-token *distribution* | decode steps, plus stalls when prefills are scheduled in between | p99 ITL exposes stutters that the TPOT average hides |
| **E2E latency** | `TTFT + TPOT * (n_out - 1)` | both | non-streaming APIs, agents and tool chains |
| **Throughput** | output tokens/s (or total tokens/s, or requests/s) per GPU or per node | batch size, utilization | cost per token |
| **Goodput** | requests/s that **meet the SLOs** (for example p90 TTFT <= 500 ms and p90 TPOT <= 50 ms) | balance of all of the above | the metric you actually optimize in production (DistServe) |

The fundamental tradeoff is **throughput vs latency**: larger batches raise tokens/s but increase TPOT (more KV bytes per step) and TTFT (requests queue behind a full batch). Raw throughput can be increased by letting latency explode; goodput penalizes that. Rough targets for chat: TTFT under about 0.5-1 s, TPOT around 20-50 ms (people read about 4-5 words, roughly 6 tokens, per second, so anything under about 150 ms per token feels fluent; agents chaining many calls want much lower E2E).

| Technique | Throughput | TTFT | TPOT / ITL | Notes |
|---|---|---|---|---|
| Larger max batch | up | up (queueing) | up | until KV capacity or compute bound |
| Prioritize prefill (vLLM's original default) | up | down | ITL spikes when a long prefill stalls decodes | |
| Chunked prefill | up (piggybacking) | slightly up for the long prompt | smooth, bounded ITL | token budget per step is the knob |
| Prefill-decode disaggregation | depends on pool sizing | stable | stable | KV transfer cost, more moving parts |
| Speculative decoding | down at high load | unchanged | down at low/medium load | wasted verification compute at high batch |
| Prefix caching | up | down for shared prefixes | unchanged | system prompts, multi-turn chat, few-shot |
| Quantization (weights/KV) | up | down (FP8 prefill) | down | accuracy must be validated |

## 10.2 Continuous Batching

**Static batching** forms a batch, runs it until the *longest* sequence finishes, and only then admits new requests. Finished sequences leave idle slots, and new requests wait for the whole batch. **Continuous (iteration-level) batching** (Orca, 2022) re-forms the batch at **every decode step**: finished sequences leave immediately and waiting requests join (their prefill is scheduled into the next step). Because output lengths vary widely (10 to 2,000 tokens), this raises throughput several-fold at the same latency.

Implementation details: the linear layers run over a flattened `(total_tokens, D)` tensor containing every sequence's tokens for that step (prefill chunks and decode tokens together); only attention needs per-sequence structure, handled by varlen/paged attention kernels with per-sequence offsets. The scheduler enforces a token budget per step and a KV-capacity check, and preempts (swap to CPU or recompute later) when the cache runs out.

## 10.3 Paged Attention

Naive serving reserves a contiguous KV region of `max_len` tokens per request, which wastes memory to over-reservation and fragmentation (the vLLM paper measured that existing systems used only 20-40% of KV memory for actual tokens). **PagedAttention** borrows virtual memory's idea:

- KV is stored in fixed-size **blocks** (vLLM's default is 16 tokens per block); a per-sequence **block table** maps logical block `i` to a physical block.
- Blocks are allocated on demand as the sequence grows; waste is under one block per sequence.
- Blocks can be **shared**: parallel samples and beam search share the prompt's blocks with copy-on-write; **prefix caching** hashes full blocks by content (and their prefix) so a new request with the same system prompt reuses them and skips that part of prefill.
- Cost: the attention kernel gathers K/V through the block table (an indirection, and blocks are not contiguous), and very small blocks hurt memory-access efficiency.

Details of the vLLM implementation are in [ML_AI_Frameworks.md, Section 30](../ml-gpu/ML_AI_Frameworks.md#30-vllm-architecture-and-pagedattention).

## 10.4 Chunked Prefill

A 32K-token prompt's prefill can take hundreds of milliseconds. If the scheduler runs it as one step, every decoding sequence stalls for that long (an ITL spike). **Chunked prefill** (Sarathi-Serve) splits long prompts into chunks (for example 512-2048 tokens) and builds each step from a **token budget**: all pending decode tokens first, then as much prefill as fits.

Why it works: decode steps are memory-bound and leave matrix cores idle; prefill chunks are compute-bound. Mixing them gives a step that reads the weights once and uses them for both, so decodes "piggyback" on prefill compute nearly for free, and ITL stays bounded by the budget. Costs: a chunked prompt's TTFT is a bit higher (each chunk attends to the KV of earlier chunks, and the weights are re-read per chunk), and the budget is a tuning knob: small budgets give smooth ITL, large ones better TTFT and throughput. vLLM's V1 engine enables chunked prefill by default, with the budget set by `max_num_batched_tokens`.

## 10.5 Prefill-Decode Disaggregation

Run prefill and decode on **separate GPU pools** (DistServe, Splitwise, Mooncake; available in vLLM, SGLang, and NVIDIA Dynamo via KV-transfer connectors). A prefill instance computes the prompt's KV cache and ships it to a decode instance, which then generates tokens.

| Pros | Cons |
|---|---|
| No interference: decode ITL is not disturbed by prefills, TTFT is not delayed by long decode batches | KV transfer: a 4K-token LLaMA-3-70B prompt is `4096 * 0.33 MB = 1.34 GB`; over a 400 Gb/s (50 GB/s) RDMA link that is about 27 ms (can be overlapped layer by layer) |
| Each pool gets its own parallelism and batch settings (prefill: compute-optimized, TP for low TTFT; decode: large batches, memory capacity) | Needs a fast interconnect and a KV-transfer layer, more components and failure modes |
| Pools scale independently with the workload's input/output length ratio | Pool ratio must track traffic mix; at low load, a colocated system is simpler and as good |

Rule of thumb: disaggregation pays off at scale when there are strict TTFT and ITL SLOs simultaneously and long prompts; colocated with chunked prefill is the right default for smaller deployments.

## 10.6 Speculative Decoding

Because decode is memory-bound, verifying `gamma + 1` tokens in one forward pass costs about the same as generating one: the weights are read once either way. Speculative decoding (Leviathan et al.; Chen et al., 2023) exploits this:

1. A cheap **draft** proposes `gamma` tokens autoregressively (`x_1 ... x_gamma` from distributions `q`).
2. The **target** model scores all of them in one forward pass, giving its distributions `p` at each position.
3. For each `i`, accept `x_i` with probability `min(1, p(x_i) / q(x_i))`. On the first rejection, resample that position from `norm(max(0, p - q))` and stop. If all are accepted, sample one bonus token from the target's next distribution.

This rejection scheme makes the output distribution **exactly** the target's (lossless, not an approximation). With a per-token acceptance rate `alpha` (assumed i.i.d.), the expected number of tokens per target forward pass is

```text
E[tokens] = (1 - alpha^(gamma + 1)) / (1 - alpha)
speedup   ~ E[tokens] / (1 + gamma * c)      c = cost of one draft step / cost of one target step
```

```python
"""spec_decode.py -- speculative sampling preserves the target distribution; expected tokens per target pass."""
import numpy as np

rng = np.random.default_rng(0)
V = 5
p = np.array([0.40, 0.25, 0.15, 0.15, 0.05])     # target model's next-token distribution
q = np.array([0.30, 0.40, 0.10, 0.10, 0.10])     # cheaper draft model's distribution


def speculative_sample():
    x = rng.choice(V, p=q)                         # draft proposes x ~ q
    if rng.random() < min(1.0, p[x] / q[x]):       # accept with prob min(1, p/q)
        return x, True
    residual = np.maximum(p - q, 0.0)              # on reject, resample from norm(max(0, p - q))
    return rng.choice(V, p=residual / residual.sum()), False


draws = [speculative_sample() for _ in range(200_000)]
freq = np.bincount([x for x, _ in draws], minlength=V) / len(draws)
alpha = np.mean([a for _, a in draws])
print("target p     :", p)
print("empirical    :", freq.round(3))
print(f"acceptance   : {alpha:.3f}  (theory: sum min(p, q) = {np.minimum(p, q).sum():.3f})")

print("\nexpected tokens per target forward = (1 - a^(g+1)) / (1 - a); speedup with draft cost c = 0.05")
for a in (0.6, 0.8, 0.9):
    row = []
    for g in (2, 4, 8):
        e = (1 - a ** (g + 1)) / (1 - a)
        row.append(f"g={g}: {e:4.2f} tok, {e / (1 + g * 0.05):4.2f}x")
    print(f"a={a}:  " + "   ".join(row))
```

```text
target p     : [0.4  0.25 0.15 0.15 0.05]
empirical    : [0.401 0.25  0.149 0.15  0.05 ]
acceptance   : 0.801  (theory: sum min(p, q) = 0.800)

expected tokens per target forward = (1 - a^(g+1)) / (1 - a); speedup with draft cost c = 0.05
a=0.6:  g=2: 1.96 tok, 1.78x   g=4: 2.31 tok, 1.92x   g=8: 2.47 tok, 1.77x
a=0.8:  g=2: 2.44 tok, 2.22x   g=4: 3.36 tok, 2.80x   g=8: 4.33 tok, 3.09x
a=0.9:  g=2: 2.71 tok, 2.46x   g=4: 4.10 tok, 3.41x   g=8: 6.13 tok, 4.38x
```

The acceptance rate equals `sum_x min(p(x), q(x)) = 1 - TV(p, q)`, so a draft that matches the target closely is what matters. Longer drafts help only when `alpha` is high; at `alpha = 0.6` going from 4 to 8 draft tokens makes things *slower*.

Draft sources: a small model from the same family (same tokenizer), extra decoding heads on the target (Medusa), a lightweight feature-level draft head with tree-structured candidates (EAGLE), multi-token-prediction heads trained with the model (DeepSeek-V3's MTP), and model-free n-gram / prompt-lookup drafting (very effective for code edits and RAG, where outputs copy the input). **When it hurts**: at high batch sizes the GPU is already closer to compute-bound, so the FLOPs spent verifying rejected tokens are no longer free; servers typically disable or shorten speculation under heavy load.

## 10.7 Interview Questions

**Q1.** Define TTFT, TPOT, ITL, and goodput. Which would you optimize for a chat product and which for an offline batch job?

TTFT: arrival to first token (queueing plus prefill). TPOT: average time per output token after the first. ITL: the distribution of gaps between consecutive tokens (its p99 reveals stalls). Goodput: request rate that meets all SLOs (for example p90 TTFT and p90 TPOT targets). Chat: goodput under TTFT and ITL SLOs, because users notice the first-token delay and stutters. Offline batch (evals, synthetic data): pure throughput per dollar, so maximize batch size and ignore latency.

**Q2.** Explain continuous batching and why it improves throughput.

Static batching keeps a batch until its longest sequence finishes, so short sequences leave idle slots and new requests wait. Continuous batching schedules at the iteration level: after every decode step, finished sequences leave and waiting ones join, so the batch stays full. Since decode is memory-bound, a fuller batch amortizes the weight read over more tokens; throughput improves several-fold with heavy-tailed output lengths. It requires kernels that handle a ragged batch (varlen/paged attention) and a scheduler that tracks KV capacity.

**Q3.** What problem does chunked prefill solve, and what does it cost?

Long prefills scheduled as one step block all decodes for hundreds of milliseconds (ITL spikes, poor p99). Chunked prefill splits prompts into chunks and fills each step up to a token budget with decodes first, then prefill. ITL stays bounded, and memory-bound decodes ride along with compute-bound prefill chunks, improving utilization. Costs: slightly higher TTFT for the chunked request (weights re-read per chunk, attention over prior chunks), and a budget that must be tuned for the latency/throughput balance.

**Q4.** Prove that speculative decoding with `min(1, p/q)` acceptance samples from `p`.

For a token `x`, P(output `x`) = P(draft proposes `x` and it is accepted) + P(some proposal is rejected) * P(resample gives `x`). The first term is `q(x) min(1, p(x)/q(x)) = min(p(x), q(x))`. The total rejection probability is `1 - sum_y min(p(y), q(y)) = sum_y max(0, p(y) - q(y))`. The resample distribution is `max(0, p(x) - q(x)) / sum_y max(0, p(y) - q(y))`. Multiplying gives `max(0, p(x) - q(x))`. Sum: `min(p, q) + max(0, p - q) = p(x)`. Applying this per position (stopping at the first rejection) gives exactly the target's autoregressive distribution.

**Q5.** When would you choose prefill-decode disaggregation?

When serving at scale with both tight TTFT and tight ITL SLOs and long prompts (RAG, agents, long documents), where colocated scheduling forces a bad tradeoff between the two phases. Disaggregation lets each pool use its own parallelism and batch size and scale independently. It requires fast RDMA between pools (a 4K-token prompt's KV for a 70B GQA model is about 1.3 GB) and adds operational complexity, so for smaller deployments colocated serving with chunked prefill is usually the better choice.

---

# 11. Quantization for Inference

## 11.1 Quantization Basics and Granularity

**Uniform affine quantization** maps a real tensor to `b`-bit integers:

```text
q = clamp(round(x / s) + z, q_min, q_max)       x_hat = s * (q - z)
symmetric (z = 0):  s = max|x| / (2^(b-1) - 1)     INT8: max|x| / 127,  INT4: max|x| / 7
rounding error is uniform in [-s/2, s/2]: noise variance s^2 / 12
```

A single outlier inflates `max|x|`, hence `s`, hence the error for every other element sharing that scale. So **granularity** is the main accuracy lever:

| Granularity | One scale per | Typical use |
|---|---|---|
| Per-tensor | whole tensor | FP8 activations with good scaling; simplest kernels |
| Per-channel | output channel (row of W) | INT8 weights; the scale factors out of the GEMM sum |
| Per-group / block | group of 32-128 consecutive weights along the input dim | INT4 weights (group 128 is common), MX formats (block 32) |
| Per-token | each row of the activation matrix | INT8/FP8 activations computed on the fly |

Naming: `WxAy` = x-bit weights, y-bit activations (W4A16 = weight-only INT4, W8A8 = both 8-bit), plus KV-cache precision (KV8).

The LLM-specific difficulty: activations in large Transformers have a few **outlier feature channels** with magnitudes 10-100x the rest (LLM.int8() observed them emerging at around 6.7B parameters). Weights are well-behaved and easy to quantize; activations are not. That asymmetry is why weight-only quantization came first and why W8A8 needs tricks.

## 11.2 Weight-Only INT8 and INT4

Weights are stored in INT8/INT4 and **dequantized inside the GEMM kernel** (load packed integers, convert to FP16/BF16 in registers using the group scale, run the matrix instruction in 16-bit). There is no compute saving, only fewer bytes:

- **Decode (memory-bound): large win.** Weight bytes drop 2x (INT8) or about 3.9x (INT4 with group-128 FP16 scales: `0.5 + 2/128 = 0.516` bytes per weight). LLaMA-3-70B in INT4 is about 36 GB: it fits on one MI300X with about 120 GB left for KV, and the batch-1 decode bound rises from 38 to about 146 tok/s.
- **Prefill and large-batch decode (compute-bound): little or negative gain.** Dequantization adds ALU work to a kernel that is already limited by the matrix units.
- **Quality**: INT8 weight-only is near-lossless. INT4 with good methods (GPTQ, AWQ) typically costs a small perplexity increase; it can hurt more on math, code, and long-context tasks, so always evaluate on downstream tasks.

## 11.3 GPTQ, AWQ, and SmoothQuant

All three are **post-training quantization** (PTQ) using a small calibration set (often about 128 sequences); no retraining.

**GPTQ** (Frantar et al., 2022). Layer by layer, minimize the output reconstruction error `||W X - W_hat X||^2` on calibration activations `X`. It quantizes the weight matrix one column (input channel) at a time; after quantizing a column, it updates the not-yet-quantized columns to compensate for that column's error using the inverse Hessian `H^-1` with `H = 2 X X^T` (the Optimal Brain Surgeon update). Lazy block updates and a Cholesky formulation make it fast: a 175B model quantizes in a few GPU-hours. Strong at 4 bits and below; can overfit the calibration set.

**AWQ** (activation-aware weight quantization, Lin et al., 2023). Observation: about 1% of weight channels are **salient**, and saliency is determined by the *activation* magnitude of the corresponding input channel, not by the weight magnitude. Instead of keeping them in FP16 (mixed precision is hardware-unfriendly), AWQ multiplies each input channel of `W` by a scale `s_j` (larger for salient channels) and divides the activations by `s_j` (folded into the previous operator), which is mathematically a no-op in full precision but reduces the relative quantization error of salient weights. It searches a single exponent `s_j = mean|x_j|^alpha` on the calibration set. No backpropagation and no reconstruction, so it generalizes well across domains.

**SmoothQuant** (Xiao et al., 2022), for **W8A8**. Activations have outlier channels; weights do not. Migrate the difficulty: `Y = (X diag(s)^-1)(diag(s) W)` with `s_j = max|X_j|^alpha / max|W_j|^(1-alpha)`, `alpha ~ 0.5`. The smoothed activations are easy to quantize per-tensor or per-token, and the weights absorb a manageable amount of extra range. This enables true INT8 GEMMs (2x matrix throughput over FP16) for both prefill and decode.

| Method | Targets | Core idea | Needs |
|---|---|---|---|
| RTN (round to nearest) | W8, W4 with groups | baseline | nothing |
| GPTQ | W4/W3 weight-only | sequential column quantization with Hessian-based error compensation | calibration data, a few GPU-hours |
| AWQ | W4 weight-only | per-channel scaling guided by activation magnitude to protect salient channels | calibration data, minutes |
| SmoothQuant | W8A8 INT8 | move activation outliers into weights with a per-channel scale | calibration data |
| FP8 (E4M3) W8A8 | weights and activations | floating-point grid handles dynamic range; per-tensor or per-channel/per-token scales | calibration (static) or on-the-fly (dynamic) scales |

## 11.4 FP8 Inference

FP8 W8A8 (E4M3 for weights and activations, Section 12.2) is the default "fast and safe" quantization on hardware with FP8 matrix units (MI300X: 2,614.9 TFLOP/s dense FP8 vs 1,307.4 BF16):

- Prefill gets about 2x matrix throughput; decode gets 2x fewer weight bytes. One format helps both phases, unlike weight-only INT4.
- Floating point has roughly constant *relative* error across its range, so activation outliers are much less damaging than with INT8; per-tensor scales often suffice, with per-channel weight / per-token activation scales for extra accuracy.
- Accuracy is typically very close to BF16.
- **AMD detail:** MI300X (gfx942) implements the FNUZ FP8 variants (E4M3 max 240) rather than OCP E4M3FN (max 448). Checkpoints quantized for OCP FP8 must be converted (rescaled so values fit the smaller range) to run on MI300X; MI355X (CDNA 4) supports the OCP formats.

## 11.5 KV-Cache Quantization

Storing K/V in FP8 halves the per-token cache (LLaMA-3-70B: 0.33 MB to 0.16 MB per token). That doubles the number of tokens that fit, so larger batches or longer contexts, and halves the bytes read by decode attention, so TPOT drops at long context. Scales are per-tensor or per-head (sometimes calibrated, sometimes computed on the fly), and the attention kernel dequantizes K/V tiles after loading them.

Lower-bit KV (INT4, INT2) is an active research area. A key finding (KIVI and others) is that **keys** have outlier channels and should be quantized per channel, while **values** are better quantized per token. Pitfalls: quantization errors in keys perturb the softmax logits, which matters most for long-context retrieval tasks ("needle in a haystack"), so evaluate on long-context benchmarks, not only perplexity.

## 11.6 Interview Questions

**Q1.** Why does weight-only INT4 speed up decode but not prefill?

Decode is memory-bound: the time per step is about the bytes of weights read divided by bandwidth, so 4x fewer bytes gives up to about 3.9x faster steps at small batch. The GEMM still runs in FP16 after in-register dequantization, so there are no extra FLOP/s; prefill is compute-bound and gets nothing (or slows slightly from dequantization overhead). To speed up prefill you need lower-precision *compute*: W8A8 INT8 or FP8.

**Q2.** Compare GPTQ and AWQ.

Both are post-training, weight-only, calibration-based methods targeting 4 bits. GPTQ minimizes layer output error by quantizing columns sequentially and adjusting remaining weights using second-order (inverse Hessian) information, a principled reconstruction approach that can overfit the calibration data. AWQ protects the roughly 1% of salient channels (found from activation magnitudes) by scaling them up before quantization and scaling activations down to compensate; it does not reconstruct, so it is faster to apply and tends to generalize across domains. In practice both reach similar perplexity at W4 with group size 128; kernels and tooling support often decide.

**Q3.** Why is INT8 activation quantization hard for LLMs and how does SmoothQuant fix it?

A few hidden-dimension channels carry outliers 10-100x larger than the rest, and they appear in nearly every token. Per-tensor INT8 must stretch its scale to cover them, leaving the normal channels with only a handful of quantization levels; per-channel activation scales do not factor out of the GEMM efficiently. SmoothQuant divides each activation channel by `s_j` and multiplies the matching weight row by `s_j`, choosing `s_j` to balance the ranges (`alpha ~ 0.5`). The product is unchanged, activations become easy to quantize, and weights remain easy.

**Q4.** How does FP8 KV cache affect a long-context decode workload?

At long context, KV reads dominate the decode step (Section 9.3). Halving KV bytes nearly halves TPOT in that regime and doubles the tokens that fit in memory, so batch size or context can double. The cost is small accuracy risk, mainly in key precision affecting attention logits; measure on long-context retrieval tasks. Kernels must support FP8 KV with scales; on MI300X it is the FNUZ format.

**Q5.** A customer reports that the INT4 model is fine on chat but bad on math. Why could that be, and what would you try?

Quantization error is not uniform across abilities: multi-step reasoning compounds small logit errors over long generations, and arithmetic depends on precise token probabilities. The calibration data may also be chat-heavy, so GPTQ/AWQ protected the wrong channels. Options: calibrate on math/code-heavy data, use a smaller group size (64), keep sensitive layers (first/last layers, `down_proj`) in higher precision, move to FP8 or INT8 weights, or use quantization-aware fine-tuning. Evaluate on GSM8K/MATH-style benchmarks, not perplexity.

---

# Part 5: Mixed Precision and Number Formats

---

# 12. Floating-Point Formats for ML

## 12.1 Bit Layouts and Ranges

A binary floating-point value is `(-1)^S * 1.M * 2^(E - bias)` for normal numbers (and `0.M * 2^(1 - bias)` for subnormals). **Exponent bits set the range; mantissa bits set the precision** (relative spacing `2^-M`).

```text
FP32   S EEEEEEEE MMMMMMMMMMMMMMMMMMMMMMM   1-8-23   bias 127
TF32   S EEEEEEEE MMMMMMMMMM                 1-8-10   (19 bits; a matrix-unit compute mode, stored as FP32)
FP16   S EEEEE MMMMMMMMMM                    1-5-10   bias 15
BF16   S EEEEEEEE MMMMMMM                    1-8-7    bias 127 (the top half of an FP32)
E4M3   S EEEE MMM                            1-4-3    bias 7  (OCP)  / 8  (FNUZ)
E5M2   S EEEEE MM                            1-5-2    bias 15 (OCP)  / 16 (FNUZ)
E2M1   S EE M                                1-2-1    bias 1  (FP4 element of MXFP4)
E8M0   EEEEEEEE                              8-bit power-of-two scale (MX block scale), no sign, no mantissa
```

```python
"""fp_formats.py -- derive range/precision of floating-point formats from (exponent bits, mantissa bits, bias, special-value rule)."""

FORMATS = [  # name, E, M, bias, rule for the top exponent code
    ("FP32",        8, 23, 127, "ieee"),
    ("TF32",        8, 10, 127, "ieee"),   # 19-bit compute format, stored in 32-bit registers
    ("FP16",        5, 10,  15, "ieee"),
    ("BF16",        8,  7, 127, "ieee"),
    ("FP8 E4M3FN",  4,  3,   7, "fn"),     # OCP: no inf; only S.1111.111 is NaN
    ("FP8 E5M2",    5,  2,  15, "ieee"),   # OCP: IEEE-like, has inf/NaN
    ("E4M3FNUZ",    4,  3,   8, "fnuz"),   # MI300 (gfx942): no inf, no -0, NaN = 0x80
    ("E5M2FNUZ",    5,  2,  16, "fnuz"),   # (the single NaN code does not affect max or min)
    ("FP6 E3M2",    3,  2,   3, "none"),   # MX element types: no inf/NaN
    ("FP6 E2M3",    2,  3,   1, "none"),
    ("FP4 E2M1",    2,  1,   1, "none"),
]


def describe(E, M, bias, rule):
    top = 2**E - 1
    if rule == "ieee":            # top exponent reserved for inf/NaN
        max_exp, max_man = top - 1 - bias, 2 - 2**-M
    elif rule == "fn":            # top exponent usable, but all-ones mantissa is NaN
        max_exp, max_man = top - bias, 2 - 2 * 2**-M
    else:                         # "fnuz" or "none": top exponent is an ordinary finite binade
        max_exp, max_man = top - bias, 2 - 2**-M
    return {
        "max": max_man * 2.0**max_exp,
        "min_normal": 2.0 ** (1 - bias),
        "min_subnormal": 2.0 ** (1 - bias - M),
        "eps": 2.0**-M,           # gap between 1.0 and the next value
        "decimal_digits": (M + 1) * 0.30103,
    }


if __name__ == "__main__":
    print(f"{'format':12} {'bits':>9} {'max':>11} {'min normal':>11} {'min subnorm':>11} {'eps':>9} {'~digits':>7}")
    for name, E, M, bias, rule in FORMATS:
        r = describe(E, M, bias, rule)
        print(f"{name:12} {f'1-{E}-{M}':>9} {r['max']:>11.6g} {r['min_normal']:>11.4g} "
              f"{r['min_subnormal']:>11.4g} {r['eps']:>9.3g} {r['decimal_digits']:>7.1f}")
    print("FP4 E2M1 representable magnitudes:",
          sorted({m * 2.0**e for e in range(0, 3) for m in (1.0, 1.5)} | {0.0, 0.5}))
```

```text
format            bits         max  min normal min subnorm       eps ~digits
FP32            1-8-23 3.40282e+38   1.175e-38   1.401e-45  1.19e-07     7.2
TF32            1-8-10 3.40116e+38   1.175e-38   1.148e-41  0.000977     3.3
FP16            1-5-10       65504   6.104e-05    5.96e-08  0.000977     3.3
BF16             1-8-7 3.38953e+38   1.175e-38   9.184e-41   0.00781     2.4
FP8 E4M3FN       1-4-3         448     0.01562    0.001953     0.125     1.2
FP8 E5M2         1-5-2       57344   6.104e-05   1.526e-05      0.25     0.9
E4M3FNUZ         1-4-3         240    0.007812   0.0009766     0.125     1.2
E5M2FNUZ         1-5-2       57344   3.052e-05   7.629e-06      0.25     0.9
FP6 E3M2         1-3-2          28        0.25      0.0625      0.25     0.9
FP6 E2M3         1-2-3         7.5           1       0.125     0.125     1.2
FP4 E2M1         1-2-1           6           1         0.5       0.5     0.6
FP4 E2M1 representable magnitudes: [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
```

| Format | Why it exists | Typical role |
|---|---|---|
| FP32 | full precision, about 7 decimal digits | master weights, optimizer states, accumulators, reductions, loss |
| TF32 | FP32 range with FP16-like precision, so FP32 code gets matrix-unit speed with no changes | opt-in for FP32 GEMMs (`torch.backends.cuda.matmul.allow_tf32`) |
| FP16 | 10-bit mantissa (more precise than BF16) but max 65,504 and gradients underflow | inference; training only with loss scaling |
| BF16 | FP32's exponent range with 3 significant digits; a cheap truncation of FP32 | default training dtype; no loss scaling needed |
| FP8 E4M3 | more precision, less range | forward weights and activations, inference |
| FP8 E5M2 | more range, less precision | gradients in the "hybrid" FP8 training recipe |
| FP6 / FP4 (MX) | 2-4x denser than FP8, only usable with fine-grained block scales | inference weights (MXFP4), some activations |

**BF16 vs FP16 in one sentence:** BF16 trades 3 mantissa bits for 3 exponent bits, so it has FP32's normal range (about 1.2e-38 to 3.4e38): it overflows and underflows essentially where FP32 does (only FP32's deeper subnormals are lost), which is exactly what training needs; FP16 is more precise but needs loss scaling and overflow care. Converting FP32 to BF16 is just rounding off the low 16 bits, which also makes it cheap in hardware.

## 12.2 FP8: E4M3 vs E5M2, OCP vs FNUZ

With only 8 bits, every bit is a range/precision trade:

- **E4M3**: 3 mantissa bits after the leading one (4 significant bits, relative step 2^-3 = 12.5%), range about `2^-9` to 448. Used for weights and activations, which have moderate dynamic range once scaled.
- **E5M2**: 2 mantissa bits after the leading one (relative step 2^-2 = 25%), range about `2^-16` to 57,344. Used for gradients in the hybrid recipe, since gradient magnitudes span many orders.

Two incompatible families of 8-bit encodings are in use:

| | OCP OFP8 E4M3FN | OCP E5M2 | FNUZ E4M3 | FNUZ E5M2 |
|---|---|---|---|---|
| Exponent bias | 7 | 15 | 8 | 16 |
| Infinity | none | yes | none | none |
| NaN encoding | `S.1111.111` (2 codes) | IEEE-style | `0x80` only (the "negative zero" pattern) | `0x80` only |
| Negative zero | yes | yes | no | no |
| Max finite | 448 | 57,344 | 240 | 57,344 |
| Hardware | NVIDIA Hopper/Blackwell, AMD MI355X (CDNA 4) | same | AMD MI300X (CDNA 3, gfx942) | same |

"FN" means finite (no infinity), "UZ" means unsigned zero (no negative zero). The same bit pattern decodes to a value in FNUZ that is half the OCP value (bias one higher), and E4M3FNUZ has a smaller maximum. Converting by value saturates any OCP E4M3FN value above 240. Reinterpreting the raw bits instead halves every value and turns 0x80 (OCP negative zero) into NaN. So loaders (for example vLLM's `normalize_e4m3fn_to_e4m3fnuz`) reinterpret the bits as FNUZ, rewrite 0x80 to 0, and double the per-tensor scale so the dequantized values are unchanged. In PyTorch the dtypes are distinct: `torch.float8_e4m3fn`, `torch.float8_e5m2`, `torch.float8_e4m3fnuz`, `torch.float8_e5m2fnuz`.

## 12.3 Microscaling Formats: MXFP8, MXFP6, MXFP4

A single per-tensor scale cannot serve a 4-bit format: E2M1 has only 8 magnitudes (`0, 0.5, 1, 1.5, 2, 3, 4, 6`). The **OCP Microscaling (MX) v1.0** specification attaches a shared scale to every **block of 32 elements**:

```text
MX block = 32 elements (FP8 E4M3/E5M2, FP6 E2M3/E3M2, FP4 E2M1, or INT8)  +  one E8M0 scale (a pure power of two, 2^-127 .. 2^127)
value_i  = 2^(scale_exponent) * element_i
scale    = 2^( floor(log2(max|x| in block)) - emax_element )     e.g. emax = 2 for E2M1, 8 for E4M3
bits per element: MXFP8 = 8.25, MXFP6 = 6.25, MXFP4 = 4.25
```

The power-of-two scale is applied by adding to the exponent, which is cheap in hardware; the matrix instruction consumes the scales directly, so dequantization is not a separate kernel. The cost is coarser scaling (up to a factor of 2 lost) than a floating-point scale. NVIDIA's **NVFP4** variant uses 16-element blocks with an FP8 E4M3 scale plus a per-tensor FP32 scale for better accuracy. Hardware: NVIDIA Blackwell and AMD MI355X (CDNA 4) execute MX formats natively. MXFP4 is used for released inference weights (for example the MoE weights of OpenAI's gpt-oss models), and MXFP8 for training on hardware that supports it.

```python
"""mxfp4_demo.py -- quantize to MXFP4 (OCP MX: 32-element blocks, E8M0 power-of-two scale, E2M1 elements)."""
import numpy as np

FP4_GRID = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0])   # E2M1 magnitudes; max 6.0 = 1.5 * 2^2
EMAX_FP4 = 2                                                      # exponent of the largest normal (2^2)


def quantize_mxfp4(x, block=32):
    x = x.reshape(-1, block)
    amax = np.abs(x).max(axis=1, keepdims=True)
    # Shared scale per OCP MX v1.0: 2^(floor(log2(amax)) - emax_elem), stored as an 8-bit exponent (E8M0)
    scale = 2.0 ** (np.floor(np.log2(np.maximum(amax, 2.0**-127))) - EMAX_FP4)
    y = np.clip(np.abs(x) / scale, 0, FP4_GRID[-1])               # values above 6 saturate
    idx = np.abs(y[..., None] - FP4_GRID).argmin(axis=-1)         # round to nearest grid point
    return (np.sign(x) * FP4_GRID[idx] * scale).ravel()


def quantize_int4_per_tensor(x):
    s = np.abs(x).max() / 7
    return np.clip(np.round(x / s), -7, 7) * s


rng = np.random.default_rng(0)
w = rng.standard_normal(4096) * np.repeat(rng.uniform(0.01, 1.0, 128), 32)   # blocks with very different ranges
w[123] = 25.0                                                                  # one outlier
for name, wq in (("INT4 per-tensor", quantize_int4_per_tensor(w)), ("MXFP4 block-32", quantize_mxfp4(w))):
    rel = np.linalg.norm(wq - w) / np.linalg.norm(w)
    print(f"{name:16s} relative L2 error = {rel:.3f}   exact zeros produced = {(wq == 0).mean():.1%}")
print(f"MXFP4 storage: 4 + 8/32 = {4 + 8 / 32} bits per element")
```

```text
INT4 per-tensor  relative L2 error = 0.800   exact zeros produced = 98.5%
MXFP4 block-32   relative L2 error = 0.100   exact zeros produced = 8.0%
MXFP4 storage: 4 + 8/32 = 4.25 bits per element
```

With one outlier, a per-tensor INT4 scale crushes 98.5% of the weights to zero; 32-element blocks confine the outlier's damage to its own block. This is the same argument as per-group INT4 (Section 11.1), built into the number format.

## 12.4 Interview Questions

**Q1.** Why did BF16 replace FP16 for training?

BF16 has 8 exponent bits like FP32, so its range (about `1e-38` to `3e38`) matches FP32: activations do not overflow at 65,504 and small gradients do not underflow below FP16's `6e-8` subnormal floor. That removes the need for loss scaling and most overflow handling. The cost is precision (8 significant bits vs 11), which is acceptable because master weights and accumulations stay in FP32. Conversion from FP32 is a rounding of the high half, which is cheap.

**Q2.** What are E4M3 and E5M2, and when is each used?

Both are 8-bit floats. E4M3 has 4 exponent and 3 mantissa bits: finer precision, range to 448 (OCP) or 240 (FNUZ); used for weights and activations in the forward pass and for inference. E5M2 has 5 exponent and 2 mantissa bits: range to 57,344 with coarser precision; used for gradients, whose dynamic range is larger. With fine-grained (block) scaling, some recipes (DeepSeek-V3) use E4M3 everywhere because the per-block scales already handle range.

**Q3.** What is the difference between OCP FP8 and FNUZ FP8, and why does it matter on MI300X?

FNUZ uses an exponent bias one larger, has no infinities and no negative zero, and encodes NaN as `0x80`. As a result E4M3FNUZ's maximum is 240 instead of 448 and the same bits mean half the value. MI300X's matrix cores implement FNUZ; NVIDIA Hopper/Blackwell and AMD MI355X implement OCP. Quantized checkpoints and scale factors must be converted between them (rescaling to fit 240), and kernels or libraries must be built for the right dtype, or results will be off by a factor of 2 or saturate.

**Q4.** Why do MX formats use a block size of 32 and a power-of-two scale?

A shared scale lets very low-bit elements cover tensors with large dynamic range: each block adapts its range locally, limiting outlier damage to 32 elements. 32 is a compromise between accuracy (smaller blocks track local range better) and overhead (8 bits per 32 elements is 0.25 bits per element). A power-of-two scale is applied by integer addition to the exponent, so the hardware can fold it into the matrix instruction without multipliers. NVFP4 trades more overhead (an FP8 scale per 16 elements) for better accuracy.

**Q5.** What is the largest FP16 number, and what is the machine epsilon of BF16?

FP16 max is `(2 - 2^-10) * 2^15 = 65,504`. BF16 has 7 explicit mantissa bits, so the spacing just above 1.0 is `2^-7 = 0.0078125` (about 2-3 significant decimal digits); some texts quote the unit roundoff `2^-8`, half of that.

---

# 13. Mixed-Precision Training

## 13.1 The Standard Recipe

The mixed-precision recipe (Micikevicius et al., 2018), as implemented by PyTorch AMP:

1. Keep **FP32 master weights** and FP32 optimizer states. Small updates (`lr * grad` of about `1e-6` relative to the weight) would be lost if added to BF16 weights, whose relative spacing is about `4e-3`.
2. Run forward and backward with **autocast**: GEMMs and convolutions in FP16/BF16 (FP32 accumulation inside the matrix units); numerically sensitive ops (softmax, layer/RMS norm statistics, loss, exp/log, large reductions) in FP32.
3. With FP16, use **loss scaling** (13.2). With BF16, it is not needed.
4. Unscale, clip, and apply the optimizer update in FP32, then cast to 16-bit for the next forward pass (or keep a 16-bit copy).

Memory per parameter is the 16 bytes of Section 3.3. Speedup comes from 2x (or more) matrix-unit throughput and half the activation memory and bandwidth.

## 13.2 Loss Scaling

FP16's smallest subnormal is `5.96e-8` and smallest normal `6.1e-5`. Many activation gradients are smaller and flush to zero, which silently stops learning in some layers. Because backpropagation is linear in the loss, multiplying the loss by `S` multiplies every gradient by `S`, shifting them into the representable range; dividing by `S` in FP32 before the optimizer step restores the true values.

```python
"""loss_scaling_demo.py -- why FP16 training needs loss scaling and BF16 usually does not."""
import numpy as np

grads = np.array([3e-4, 2e-6, 4e-8, 1e-9], dtype=np.float32)   # typical small activation gradients
scale = np.float32(2.0**16)                                      # 65536, GradScaler's default init_scale

print("fp16 unscaled :", grads.astype(np.float16))                # 1e-9 flushes to 0; 4e-8 is a coarse subnormal
scaled = (grads * scale).astype(np.float16)                       # backward runs on scaled loss
print("fp16 scaled   :", scaled)
print("unscaled fp32 :", scaled.astype(np.float32) / scale)       # unscale in FP32 before the optimizer step
print("rel. error    :", np.abs(scaled.astype(np.float32) / scale - grads) / grads)

# BF16 has FP32's exponent range, so 1e-9 is representable (with only ~3 significant digits).
# numpy has no bfloat16; emulate by truncating the low 16 bits of the FP32 bit pattern.
bf16 = (grads.view(np.uint32) & np.uint32(0xFFFF0000)).view(np.float32)
print("bf16 (trunc)  :", bf16)
```

```text
fp16 unscaled : [3.e-04 2.e-06 6.e-08 0.e+00]
fp16 scaled   : [1.966e+01 1.311e-01 2.621e-03 6.557e-05]
unscaled fp32 : [2.9993057e-04 2.0004809e-06 3.9988663e-08 1.0004442e-09]
rel. error    : [0.00023147 0.00024045 0.00028342 0.0004442 ]
bf16 (trunc)  : [2.9945374e-04 1.9967556e-06 3.9814040e-08 9.9680619e-10]
```

**Dynamic loss scaling** (what `torch.amp.GradScaler` does): start large (default `init_scale = 2^16`); after each backward, check gradients for inf/NaN. If found, **skip** the optimizer step and halve the scale (`backoff_factor = 0.5`). After `growth_interval = 2000` consecutive good steps, double it (`growth_factor = 2.0`). The scale hovers just below the overflow point, maximizing the use of FP16's range. Pitfalls: unscale **before** gradient clipping (`scaler.unscale_(optimizer)`), or clipping thresholds are compared against scaled norms; and occasional skipped steps are normal, but a scale that keeps collapsing indicates a real overflow (an exploding activation or a bad batch).

## 13.3 FP8 Scaling Recipes

FP8's range is so narrow that **every tensor needs its own scale** (`x_fp8 = cast(x * scale)`, with `scale ~ FP8_MAX / amax(x)`). The recipes differ in where `amax` comes from and how many values share a scale:

| Recipe | Scale granularity | Where amax comes from | Pros | Cons |
|---|---|---|---|---|
| Per-tensor **delayed** scaling (Transformer Engine's original recipe) | whole tensor | max over a history of `amax` values from previous iterations; `scale = FP8_MAX / amax / 2^margin` | quantize in the same kernel that produces the tensor; no extra pass | a sudden spike saturates for a step; history is state to checkpoint |
| Per-tensor **current** (just-in-time) scaling | whole tensor | `amax` of the current tensor | robust to spikes | an extra reduction pass over the tensor (or a fused one) |
| **Block / fine-grained** scaling (DeepSeek-V3) | activations: 1 x 128 tiles (per token, per 128 channels); weights: 128 x 128 blocks | computed online per tile | outliers only affect their tile, E4M3 for all tensors | scales must be applied inside the GEMM (per-K-block), more complex kernels |
| **MXFP8** | 32-element blocks, E8M0 scales | computed per block when quantizing | hardware-native; scales consumed by the matrix instruction | needs MX-capable hardware |

What stays in higher precision in every recipe: master weights and optimizer states (FP32), the attention softmax and normalization statistics, embeddings and the LM head (often), and the gradient all-reduce (often BF16). FP8 is applied mainly to the three GEMMs of each linear layer: forward (fprop), input gradient (dgrad), and weight gradient (wgrad).

## 13.4 Accumulation Precision

Products of two FP8 or FP16 numbers are exact in a slightly wider format, but a GEMM sums `K` of them, and summation error grows with `K`. Matrix units therefore accumulate in **FP32** even when inputs are FP16/BF16/FP8 (CDNA 3 MFMA: FP16, BF16, and FP8 inputs with FP32 accumulators; INT8 with INT32 accumulators). The result is rounded to 16-bit only in the epilogue.

```python
"""accumulation.py -- why GEMM/reduction accumulators must be FP32 even when inputs are FP16/FP8."""
import numpy as np

rng = np.random.default_rng(0)
x = rng.random(10_000).astype(np.float16)          # values in [0, 1), true sum ~ 5000

acc16 = np.float16(0)
for v in x:                                         # sequential FP16 accumulator (what you must NOT do)
    acc16 = np.float16(acc16 + v)
acc32 = np.float32(0)
for v in x:                                         # FP16 inputs, FP32 accumulator (what matrix cores do)
    acc32 += np.float32(v)

print(f"exact (float64)      : {x.astype(np.float64).sum():.2f}")
print(f"FP32 accumulator     : {acc32:.2f}")
print(f"FP16 accumulator     : {float(acc16):.2f}   <- stalls: FP16 spacing at 2048 is 2.0")
print(f"FP16 spacing at 2048 : {float(np.spacing(np.float16(2048)))}")
```

```text
exact (float64)      : 4994.10
FP32 accumulator     : 4994.10
FP16 accumulator     : 2048.00   <- stalls: FP16 spacing at 2048 is 2.0
FP16 spacing at 2048 : 2.0
```

A 16-bit accumulator **stalls**: once the running sum reaches 2048, the FP16 spacing is 2.0, so adding any value below 1.0 rounds back to the same number. With `K = 8192` (a typical hidden size) that is a real problem, not a corner case. Related points interviewers probe:

- Even "FP32" accumulation in hardware may be narrower than IEEE FP32 in some units: DeepSeek-V3 reported that FP8 GEMM accumulation on H800 Tensor Cores retained only about 14 bits, and promoted partial sums to FP32 CUDA-core registers every 128 elements of `K`.
- Summation order changes the rounding, so split-K GEMMs, atomics, and different tile sizes give run-to-run or machine-to-machine differences; pairwise or compensated (Kahan) summation reduces error growth from `O(n eps)` to `O(log n * eps)` or `O(eps)`. See [Performance Engineering, Section 9](../computer-science/Performance_Engineering.md#9-floating-point-numerics-and-reproducibility).
- Reductions in normalization layers and softmax are done in FP32 for the same reason, even inside BF16 kernels.

## 13.5 Interview Questions

**Q1.** Walk through what happens in an FP16 mixed-precision training step with dynamic loss scaling.

Forward in FP16 under autocast (sensitive ops in FP32), compute the loss in FP32, multiply by the current scale `S`, backward (all gradients are scaled by `S`), unscale gradients by `1/S` in FP32, check for inf/NaN: if any, skip the update and halve `S`; otherwise clip, run the optimizer on FP32 master weights, copy to FP16, and after 2000 clean steps double `S`. The goal is to keep small gradients above FP16's underflow threshold without overflowing large ones.

**Q2.** Why keep FP32 master weights if the forward pass uses BF16?

Updates are tiny relative to weights: with `lr = 3e-4` and normalized Adam steps, the relative change per step is often `1e-5` to `1e-4`, below BF16's relative spacing (`2^-8` to `2^-7`, about `4e-3` to `8e-3`). Adding them directly to BF16 weights rounds most of them away (stagnation). FP32 master weights accumulate the updates exactly enough; the BF16 copy is re-derived each step. Alternatives: stochastic rounding into BF16, or Kahan-compensated BF16 weights, both used by memory-saving optimizers.

**Q3.** Compare delayed scaling and block scaling for FP8 training.

Delayed scaling uses one scale per tensor computed from the maximum `amax` seen over recent iterations, so the cast can be fused into the producing kernel without a pre-pass, but a sudden outlier saturates the tensor until the history catches up, and one outlier channel forces a coarse scale for the whole tensor. Block scaling computes scales per small tile (1x128 activations, 128x128 weights in DeepSeek-V3, or 32-element MX blocks), which contains outliers locally and permits E4M3 everywhere, but the GEMM must apply scales per K-block, which needs kernel or hardware support (MX formats put it in hardware).

**Q4.** Why must GEMM accumulators be FP32 even with FP8 inputs?

The accumulation runs over `K` (thousands) of products. In a low-precision accumulator, once the partial sum is large, each new small term is below half the spacing and is rounded away (swamping); the example above stalls at 2048 out of about 4994. Error also grows roughly linearly with `K` for sequential summation. FP32 accumulators have 24 bits of significand, so error stays near FP32 rounding for realistic `K`. The output can then be rounded to BF16 or FP8 once.

**Q5.** A BF16 training run is bit-for-bit non-reproducible across runs on the same machine. Is something broken?

Not necessarily. Floating-point addition is not associative; split-K GEMMs, atomic adds in attention backward and embedding backward, and non-deterministic reduction orders in collectives all change rounding between runs. Differences at the level of BF16 rounding are expected and should not change convergence. If bitwise reproducibility is required (debugging, regression tests), enable deterministic algorithms (`torch.use_deterministic_algorithms(True)`, deterministic attention backward), fix seeds, and accept the slowdown. Large divergences are a bug or an instability, not rounding.

---

# 14. Formula Cheat Sheet

| Quantity | Formula | LLaMA-3-70B / MI300X example |
|---|---|---|
| Softmax-CE gradient | `dL/dz = p - y` | |
| Attention | `softmax(Q K^T / sqrt(d_k) + M) V` | `d_h = 128` |
| Per-layer parameters (MHA, 4D FFN) | `12 D^2` | GQA + SwiGLU: 855.7M per layer |
| Total parameters | `~12 L D^2 + V D (+ V D untied)` | 70.55B |
| Forward FLOPs per token | `~2N + 2 n_layers n_ctx D` | `1.41e11` + attention |
| Training FLOPs | `~6 N D` | 15T tokens: `6.35e24` |
| Chinchilla optimum | `D ~ 20 N`, `N = sqrt(C / 120)` | `C = 1e24`: 91B params, 1.8T tokens |
| KV cache per token | `2 * n_layers * n_kv_heads * d_head * bytes` | 327,680 B (0.33 MB) BF16 |
| Decode step time (memory-bound) | `(weight bytes + sum KV bytes) / HBM BW` | batch 1, 1 GPU: 141 GB / 5.3 TB/s = 27 ms |
| Weight-GEMM arithmetic intensity | `~ tokens per forward pass` | ridge ~247 FLOP/B (BF16) |
| Decode attention intensity | `H / H_kv` (x2 for FP8 KV) | 8 FLOP/B |
| Speculative decoding | `E = (1 - a^(g+1)) / (1 - a)` | `a = 0.8, g = 4`: 3.36 tokens |
| Training memory (AdamW, mixed) | 16 bytes/param + activations | 1.12 TB |
| Online softmax | `m' = max(m, x)`, `l' = l e^(m - m') + e^(x - m')`, `O' = O e^(m - m') + e^(x - m') v` | |
| Perplexity | `exp(mean NLL)` | |
| FP16 / BF16 / E4M3 / E5M2 max | 65,504 / 3.39e38 / 448 (240 FNUZ) / 57,344 | |
