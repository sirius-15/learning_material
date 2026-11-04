# GPU Kernel Case Studies -- Comprehensive Optimization Ladders in HIP

> Last reviewed: 2026-11 · Versions assumed: HIP/ROCm 7.0+ (ROCm 6.2-6.4 need two `-D` flags, see the build note in 0.2; code compile-checked with `hipcc --offload-arch=gfx942` from a ROCm 10.1 nightly; numbers measured on MI350X / gfx950), rocprofv3 (rocprofiler-sdk 1.3.5) and rocprof-compute 3.9.0, hipCUB/rocPRIM, rocWMMA, hipBLAS. CUDA 12.x equivalents are noted inline.

> Version note: ROCm 10.0.0 (Aug 2026) and 10.1.0 are public releases of the ROCm Core SDK, built with TheRock since 7.14. This line succeeded the 7.x releases (the 7.0-7.2 production stream and the 7.9-7.14 technology previews). The "ROCm 10.1 nightly" used for the measurements here is a pre-release build of 10.1.0 (`10.1.0a20260825`), not the published 10.1.0 package. Other files in this repo state their own assumed versions (some still say ROCm 6.4-7.x) in their header lines, so check those headers when a flag or tool name differs.

> Eight canonical "optimize this kernel" case studies, each built as a ladder: a naive kernel, then one change at a time, with the reason each step helps stated in counter terms (coalescing, LDS bank conflicts, occupancy, VALU utilization), the arithmetic intensity, and the bandwidth or FLOP rate actually measured. All code is HIP and is written for **64-lane wavefronts** (AMD CDNA). Every place where wave64 and NVIDIA's warp32 differ is called out. Section 8 is a graded exercise list with hints in [Answers](#answers). Companion files: [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) (hardware, counters, top-down method), [Performance Engineering -- Roofline Model](../computer-science/Performance_Engineering.md#3-roofline-model) (arithmetic intensity, ridge points), and [Parallel and GPU Programming](../ml-gpu/Parallel_GPU_Programming.md) (HIP/CUDA basics).

---

## Table of Contents

0. [Conventions, Hardware Numbers, and Measurement Harness](#0-conventions-hardware-numbers-and-measurement-harness)
1. [Reduction Ladder](#1-reduction-ladder)
2. [Matrix Transpose](#2-matrix-transpose)
3. [Prefix Scan](#3-prefix-scan)
4. [Histogram](#4-histogram)
5. [Softmax and LayerNorm](#5-softmax-and-layernorm)
6. [Tiled GEMM Progression](#6-tiled-gemm-progression)
7. [Elementwise Fusion and Kernel Launch Overhead](#7-elementwise-fusion-and-kernel-launch-overhead)
8. [Kernel Exercise List](#8-kernel-exercise-list)
- [Answers](#answers)

---

# 0. Conventions, Hardware Numbers, and Measurement Harness

## 0.1 How to Read the Numbers

Every case study reports numbers **measured on one MI350X (gfx950, CDNA4, 2.2 GHz peak engine clock)** with a ROCm 10.1 nightly. The MI355X is the same gfx950 chip at 2.4 GHz and a higher power limit, so its peaks are about 9% higher; the "% of peak" figures below use MI350X peaks. The same sources were compile-checked for MI300X (`--offload-arch=gfx942`, CDNA3). Treat the absolute numbers as one data point. What carries over to other GPUs, and what you should quote in an interview, is:

- the **ranking** of the variants and the **ratio** between rungs;
- the **fraction of the achievable ceiling** (a copy or read kernel on the same machine), not of the data-sheet peak;
- the **counter evidence** that explains each step.

On MI300X, expect bandwidth-bound kernels to land at a similar fraction of *its* measured ceiling. Its HBM peak is 5.3 TB/s instead of 8 TB/s, so absolute GB/s will be lower. Measure the ceiling with the copy kernel rather than scaling these numbers.

## 0.2 Wave64 vs Warp32: The Porting Checklist

HIP and CUDA kernels look almost identical. The differences that actually break code are about the **wavefront width**: 64 lanes on every CDNA GPU (MI100 to MI355X), 32 on NVIDIA, and 32 by default on RDNA (Radeon) GPUs.

| Concept | AMD CDNA (HIP) | NVIDIA (CUDA) | Pitfall |
|---|---|---|---|
| SIMT group | wavefront, **64 lanes** | warp, 32 threads | Hard-coded `32`, `tid & 31`, `tid >> 5` |
| Width query | `warpSize` (a runtime value in recent HIP) | `warpSize` (32) | Use a `constexpr` (this file: `kWave`) when sizing arrays |
| Lane masks | `unsigned long long` (64-bit) | `unsigned` (32-bit) | `__ballot` returns 64 bits; `1u << lane` is UB for lane >= 32, use `1ull << lane` |
| Bit ops on masks | `__popcll`, `__ffsll`, `__clzll` | `__popc`, `__ffs`, `__clz` | 32-bit versions silently drop lanes 32-63 |
| Sync shuffles | `__shfl_down_sync(mask, v, d)` with a **64-bit mask** (opt-in on ROCm 6.2-6.4, default since 7.0) | `__shfl_down_sync(0xffffffff, v, d)` | Recent HIP has a `static_assert`: *"The mask must be a 64-bit integer"* |
| Non-sync shuffles | `__shfl_down(v, d, width)` | deprecated since CUDA 9 | Fine on AMD; lanes in a wave run in lockstep |
| Reduction steps | `log2(64) = 6` (offsets 32, 16, ..., 1) | 5 (offsets 16, ..., 1) | Starting at 16 on AMD silently reduces only half the wave |
| Block size | multiple of 64 | multiple of 32 | A 32-thread block wastes half of every wave |
| Shared memory | LDS: 64 KB/CU (CDNA3), 160 KB/CU (CDNA4) | shared memory, up to 228 KB/SM (H100) | A block may use the whole LDS (`sharedMemPerBlock` = 160 KB on gfx950); CUDA needs an explicit opt-in above 48 KB of dynamic shared memory |
| Matrix units | MFMA (`__builtin_amdgcn_mfma_*`, rocWMMA) | Tensor Cores (`mma.sync`, WMMA) | Different operand layouts per lane |

The classic CUDA reduction tail `if (tid < 32) { volatile float* s = ...; s[tid] += s[tid + 32]; ... }` is wrong twice over. On wave64 the first wave holds lanes 0-63, so the tail must start at `+64`, and the "implicit warp synchronization" it relies on has been undefined behaviour on NVIDIA since Volta. Use shuffles (Section 1.4) instead.

**Build note for ROCm 6.2-6.4.** Two programs here use APIs that became the default only in ROCm 7.0. Compile with `-DHIP_ENABLE_WARP_SYNC_BUILTINS` (required for `__match_any` in `histogram.hip` and for every `*_sync` warp builtin; on by default since ROCm 7.0) and `-DHIPBLAS_V2` (`gemm.hip` calls `hipblasGemmEx` with `hipDataType` / `hipblasComputeType_t`, which is the default signature only from hipBLAS 3.0 / ROCm 7.0). The runtime (non-`constexpr`) `warpSize` is also a ROCm 7.0 change.

## 0.3 Hardware Numbers Used in This File

| | MI300X (gfx942, CDNA3) | MI350X (gfx950, CDNA4; measured here) | MI355X (gfx950, CDNA4) |
|---|---|---|---|
| CUs (XCDs x CUs) | 304 (8 x 38) | 256 (8 x 32) | 256 (8 x 32) |
| Peak engine clock | 2.1 GHz | 2.2 GHz | 2.4 GHz |
| HBM | 192 GB HBM3, **5.3 TB/s** | 288 GB HBM3E, **8.0 TB/s** | 288 GB HBM3E, **8.0 TB/s** |
| Infinity Cache (MALL) | 256 MB | 256 MB | 256 MB |
| L2 | 4 MB per XCD (not coherent across XCDs) | 4 MB per XCD | 4 MB per XCD |
| LDS per CU | 64 KB, **32 banks** x 4 B | 160 KB, **64 banks** x 4 B | 160 KB, **64 banks** x 4 B |
| Max waves per SIMD (4 SIMDs per CU) | 8 | 8 | 8 |
| FP32 vector peak (packed `v_pk_fma_f32`; non-packed is half) | 163.4 TFLOP/s (81.7 without packing) | 144.2 TFLOP/s (72.1) | 157.3 TFLOP/s (78.6) |
| FP16/BF16 matrix peak (dense) | 1307.4 TFLOP/s | ~2.3 PFLOP/s | ~2.5 PFLOP/s |
| Ridge point, FP32 vector | 163.4 / 5.3 = **30.8 FLOP/B** | 144.2 / 8.0 = **18.0 FLOP/B** | 157.3 / 8.0 = **19.7 FLOP/B** |
| Ridge point, FP16 matrix | **247 FLOP/B** | **~288 FLOP/B** | **~315 FLOP/B** |

Peaks are from AMD's product pages ([MI300X](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html), [MI350X](https://www.amd.com/en/products/accelerators/instinct/mi350/mi350x.html), [MI355X](https://www.amd.com/en/products/accelerators/instinct/mi350/mi355x.html)); LDS and bank counts are from the [CDNA3](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instruction-set-architectures/amd-instinct-mi300-cdna3-instruction-set-architecture.pdf) and [CDNA4](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instruction-set-architectures/amd-instinct-cdna4-instruction-set-architecture.pdf) ISA guides. AMD's CDNA3/CDNA4 "FP32 vector" figure already counts packed FP32 (256 FLOP/clk/CU: 144.2 = 256 CUs x 2.2 GHz x 256).

**Measured ceilings on our MI350X** (simple `float4` grid-stride kernels, 1 GiB buffers): read-only **5.3-5.6 TB/s**, copy (read + write) **4.0-4.7 TB/s**, `hipMemcpy` device-to-device 4.7 TB/s. That is 50-70% of the 8 TB/s data-sheet number. Every "% of ceiling" below is relative to these measured values.

**Occupancy rule of thumb (CDNA3/CDNA4):** waves per SIMD = `min(8, floor(512 / VGPRs allocated))`, with VGPRs allocated in granules of 8. So 96 VGPRs gives 5 waves, 104 gives 4, and 240 gives 2. LDS also limits it: `floor(LDS per CU / LDS per block)` blocks per CU. Do not compute this by hand in practice. Ask the compiler:

```bash
hipcc -O3 --offload-arch=gfx942 -c kernel.hip -Rpass-analysis=kernel-resource-usage
# remark: Function Name: _Z17softmax_wave_regs...
#     VGPRs: 100   AGPRs: 0   Occupancy [waves/SIMD]: 4   VGPRs Spill: 0   LDS Size [bytes/block]: 0
hipcc -O3 --offload-arch=gfx942 --save-temps -c kernel.hip   # keeps the .s ISA for reading
```

## 0.4 Measurement Harness

Every program in this file includes this header. Save it next to the `.hip` files.

```cpp
// common.hpp -- shared helpers for every program in this file
#pragma once
#include <hip/hip_runtime.h>
#include <cstdio>
#include <cstdlib>

#define HIP_CHECK(expr)                                                    \
  do {                                                                     \
    hipError_t e_ = (expr);                                                \
    if (e_ != hipSuccess) {                                                \
      std::fprintf(stderr, "HIP error '%s' at %s:%d: %s\n", #expr,         \
                   __FILE__, __LINE__, hipGetErrorString(e_));             \
      std::exit(1);                                                        \
    }                                                                      \
  } while (0)

// Wavefront size. CDNA (MI100..MI355X) = 64. RDNA (wave32 mode) and NVIDIA = 32.
// warpSize is a runtime value in recent HIP, so kernels that size arrays by it
// use this compile-time constant instead.
#if defined(__HIP_PLATFORM_NVIDIA__)
constexpr int kWave = 32;
#else
constexpr int kWave = 64;
#endif

// Warm up once, then return the average milliseconds per call over `iters` calls.
template <class Launch>
float time_ms(Launch&& launch, int iters = 20) {
  launch();
  HIP_CHECK(hipGetLastError());
  HIP_CHECK(hipDeviceSynchronize());
  hipEvent_t start, stop;
  HIP_CHECK(hipEventCreate(&start));
  HIP_CHECK(hipEventCreate(&stop));
  HIP_CHECK(hipEventRecord(start));
  for (int i = 0; i < iters; ++i) launch();
  HIP_CHECK(hipEventRecord(stop));
  HIP_CHECK(hipEventSynchronize(stop));
  float ms = 0.f;
  HIP_CHECK(hipEventElapsedTime(&ms, start, stop));
  HIP_CHECK(hipEventDestroy(start));
  HIP_CHECK(hipEventDestroy(stop));
  return ms / iters;
}

inline double gbps(double bytes, float ms) { return bytes / (ms * 1e-3) / 1e9; }
inline double tflops(double flops, float ms) { return flops / (ms * 1e-3) / 1e12; }

inline int num_cus() {
  int dev = 0, cus = 0;
  HIP_CHECK(hipGetDevice(&dev));
  HIP_CHECK(hipDeviceGetAttribute(&cus, hipDeviceAttributeMultiprocessorCount, dev));
  return cus;
}
```

Methodology rules that the numbers below follow (and that interviewers probe):

1. **Working set larger than the 256 MB Infinity Cache.** Otherwise you measure MALL bandwidth, not HBM. Most tests here use 512 MB-1 GB per buffer.
2. **Warm up once, then average many launches** with events on the same stream. The first launch pays code-object loading and page-table setup.
3. **Count algorithmic bytes** (the minimum traffic: every input read once, every output written once) and report GB/s against them. When diagnosing, also read the *measured* traffic (`FETCH_SIZE`, `WRITE_SIZE`). The gap between the two is your cache inefficiency.
4. **Check correctness every time.** A fast wrong kernel is the most common benchmarking mistake.

## 0.5 Counters and Metrics Used

| Counter / metric | What it measures | Where it shows up |
|---|---|---|
| `SQ_WAVES` | Waves launched | Normalize other counters per wave |
| `SQ_INSTS_VALU`, `SQ_INSTS_LDS`, `SQ_INSTS_SALU` | Instructions issued (per wave instruction, not per lane) | Reduction overheads |
| `SQ_THREAD_CYCLES_VALU / SQ_ACTIVE_INST_VALU` | Average active lanes per VALU instruction (rocprof-compute "VALU Active Threads") | Divergence (Section 1) |
| `SQ_LDS_BANK_CONFLICT` | Cycles the LDS stalled on bank conflicts | Transpose, scan, GEMM |
| `TCP_TCC_READ_REQ_sum`, `TCP_TCC_WRITE_REQ_sum` | Requests from vector L1 to L2 | Coalescing (Section 2) |
| `FETCH_SIZE`, `WRITE_SIZE` | KB read from / written to memory beyond L2 | Real HBM traffic, measured AI (Section 6) |
| `TCC_ATOMIC_sum`, `TCC_EA0_ATOMIC_sum` | Atomics at L2, and atomics forwarded past L2 | Histogram (Section 4) |
| `SQ_INSTS_VALU_MFMA_*`, `SQ_VALU_MFMA_BUSY_CYCLES` | Matrix-core work | GEMM |
| rocprof-compute 2.1.15 / 7.2.7 Wavefront Occupancy | Achieved waves per CU | All |
| rocprof-compute 12.1.3 / 12.2.3 LDS Bank Conflict Rate, Bank Conflicts/Access | LDS efficiency | Transpose, scan |
| rocprof-compute 16.1.3 vL1D Coalescing | How well lanes' addresses merge into cache lines | Transpose, softmax |
| rocprof-compute 17.1.5 HBM Bandwidth | Achieved DRAM bandwidth | All memory-bound kernels |

Metric IDs are from rocprof-compute 3.9 for gfx942. They move between releases, so check with `rocprof-compute analyze --list-metrics gfx942` (any supported arch), or `rocprof-compute profile --list-available-metrics` for the GPU in the machine. Both flags exist in 3.9.0. The commands:

```bash
# Per-kernel timing and statistics
rocprofv3 --kernel-trace --stats -d out -o run --output-format csv -- ./transpose
# Raw counters (one pass; add more --pmc groups for counters that cannot be collected together)
rocprofv3 --pmc SQ_LDS_BANK_CONFLICT SQ_INSTS_LDS TCP_TCC_WRITE_REQ_sum \
          --kernel-include-regex 'transpose' -d out -o run --output-format csv -- ./transpose
# Derived metrics, filtered to the LDS (12) and vector L1 (16) blocks
rocprof-compute profile -n transpose -b 12 16 --no-roof -- ./transpose
rocprof-compute analyze -p workloads/transpose/<gpu-dir>/ -b 12.1 16.1
```

Newer rocprofv3 builds default to the rocpd (SQLite) format and warn that direct CSV output is deprecated. If your build warns, use `--output-format rocpd` (or omit the flag) and then convert with `rocpd convert -i <db> --output-format csv` (or the `rocpd2csv -i <db>` shortcut).

> **See also:** [Performance Engineering -- Measured vs Theoretical Ceilings](../computer-science/Performance_Engineering.md#35-measured-vs-theoretical-ceilings); [Parallel GPU Programming -- Wavefront Occupancy and Register Usage](../ml-gpu/Parallel_GPU_Programming.md#302-wavefront-occupancy-and-register-usage); [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) for the full counter catalogue and the top-down method.

---

# 1. Reduction Ladder

## 1.1 Problem and Roofline Position

Sum `n = 2^28` floats (1 GiB). Each element is read once and takes part in one add: **AI = 1 FLOP / 4 B = 0.25 FLOP/B**, 72-123x below the FP32 ridge point (18.0-30.8 FLOP/B). The kernel is memory-bound on every GPU ever built. The **target is the read-bandwidth ceiling** (5.3-5.6 TB/s on our MI350X, which works out to about 0.19-0.20 ms). Every rung of the ladder removes overhead that keeps the kernel from streaming at that rate.

The ladder follows Mark Harris's classic CUDA reduction talk, adapted to wave64. Each rung changes exactly one thing.

## 1.2 Rungs R1-R4: LDS Tree Reductions

```cpp
// fragment: reduction.hip part 1 of 4 -- concatenate parts 1-4 in order to build
// reduction.hip -- the reduction optimization ladder (sum of N floats)
// Build: hipcc -O3 --offload-arch=gfx942 reduction.hip -o reduction
#include "common.hpp"
#include <hipcub/hipcub.hpp>
#include <cmath>
#include <utility>
#include <vector>

constexpr int kBlock = 256;  // 4 wavefronts on CDNA, 8 warps on NVIDIA

// R1: interleaved addressing, divergent branch (tid % (2*s)).
__global__ void reduce_r1(const float* in, float* out, int n) {
  __shared__ float s[kBlock];
  unsigned tid = threadIdx.x, i = blockIdx.x * blockDim.x + threadIdx.x;
  s[tid] = (i < n) ? in[i] : 0.f;
  __syncthreads();
  for (unsigned stride = 1; stride < blockDim.x; stride *= 2) {
    if (tid % (2 * stride) == 0) s[tid] += s[tid + stride];  // half the lanes idle, then 3/4...
    __syncthreads();
  }
  if (tid == 0) out[blockIdx.x] = s[0];
}

// R2: interleaved addressing, strided index: no divergence inside a wave for the
// first (small) strides; from stride 4 the single remaining wave is partially
// active. Costs LDS bank conflicts (index = 2*stride*tid).
__global__ void reduce_r2(const float* in, float* out, int n) {
  __shared__ float s[kBlock];
  unsigned tid = threadIdx.x, i = blockIdx.x * blockDim.x + threadIdx.x;
  s[tid] = (i < n) ? in[i] : 0.f;
  __syncthreads();
  for (unsigned stride = 1; stride < blockDim.x; stride *= 2) {
    unsigned idx = 2 * stride * tid;
    if (idx < blockDim.x) s[idx] += s[idx + stride];
    __syncthreads();
  }
  if (tid == 0) out[blockIdx.x] = s[0];
}

// R3: sequential addressing: contiguous active lanes, conflict-free LDS.
__global__ void reduce_r3(const float* in, float* out, int n) {
  __shared__ float s[kBlock];
  unsigned tid = threadIdx.x, i = blockIdx.x * blockDim.x + threadIdx.x;
  s[tid] = (i < n) ? in[i] : 0.f;
  __syncthreads();
  for (unsigned stride = blockDim.x / 2; stride > 0; stride >>= 1) {
    if (tid < stride) s[tid] += s[tid + stride];
    __syncthreads();
  }
  if (tid == 0) out[blockIdx.x] = s[0];
}

// R4: first add during load: each block consumes 2*blockDim elements,
// so half as many blocks and no idle threads in the first step.
__global__ void reduce_r4(const float* in, float* out, int n) {
  __shared__ float s[kBlock];
  unsigned tid = threadIdx.x;
  unsigned i = blockIdx.x * (2 * blockDim.x) + threadIdx.x;
  float v = (i < n) ? in[i] : 0.f;
  if (i + blockDim.x < n) v += in[i + blockDim.x];
  s[tid] = v;
  __syncthreads();
  for (unsigned stride = blockDim.x / 2; stride > 0; stride >>= 1) {
    if (tid < stride) s[tid] += s[tid + stride];
    __syncthreads();
  }
  if (tid == 0) out[blockIdx.x] = s[0];
}
```

**R1: interleaved addressing with a divergent branch.** At step `stride = s`, only threads with `tid % 2s == 0` work, so the active lanes are *spread across every wave*. All 4 waves of the block keep issuing every instruction for the first 6 of the 8 steps, even when only 1 lane in 64 is active. The `%` costs extra VALU instructions too.
Counters (per wave, gfx950): **21.5 LDS instructions, 37.8 VALU instructions, 44 average active lanes per VALU instruction**. There are no bank conflicts: the active lanes of a wave address `s[tid]` and `s[tid + s]`, which are the lanes' own distinct indices plus a constant, so they fall in distinct banks.

**R2: strided index.** Thread `tid` works on `s[2*s*tid]`, so the active threads are *contiguous* (threads 0..127, then 0..63, ...). Whole waves drop out early, so divergence is confined to the last few (large-stride) steps, where the single remaining wave is partially active (32, 16, ... lanes). The price is a strided LDS access: at `s = 1`, lanes 0 and 32 (on a 64-bank LDS) or lanes 0 and 16 (on a 32-bank LDS) hit the same bank. **`SQ_LDS_BANK_CONFLICT` jumps from 0 to 110M cycles** (about 26 stall cycles per wave). R2 runs no faster than R1 because the conflicts eat the divergence win.

**R3: sequential addressing.** `s[tid] += s[tid + stride]` with `stride = blockDim/2, /4, ...`. The active threads are contiguous (no divergence once `stride >= 64`), and consecutive lanes touch consecutive words (conflict-free). Counters: **8 LDS and 20.8 VALU instructions per wave, 0 conflict cycles**.

**R4: first add during load.** In R3, half the threads go idle after the first step, and each block reads only 1 KB per 9 barriers. Having each thread load and add **two** elements halves the number of blocks and doubles the bytes per barrier. Time drops by **1.9x**. This is the first rung that changes the *bytes-per-overhead* ratio, which is what actually matters for a memory-bound kernel.

## 1.3 Why R1-R3 Are So Close

All of R1-R3 move 1 GiB at 1.2-1.3 TB/s. The bottleneck is the same in all three: **one element per thread**. That means 4M waves, each doing about 9 barrier-separated LDS steps for 256 bytes of useful loads. The LDS and divergence fixes are real (the counters prove it), but they optimize a part of the time that is not dominant. **In interviews, say this explicitly:** "the profile shows the fix worked, but the kernel wasn't bound by that; the next step is more work per thread."

## 1.4 Rung R5: Wave Shuffles

```cpp
// fragment: reduction.hip part 2 of 4 -- concatenate parts 1-4 in order to build
// Wave-level reduction with cross-lane shuffles: log2(64) = 6 steps on CDNA,
// log2(32) = 5 on NVIDIA. No LDS, no barriers. Lane 0 ends with the total.
__device__ __forceinline__ float wave_reduce_sum(float v) {
  for (int offset = kWave / 2; offset > 0; offset >>= 1)
    v += __shfl_down(v, offset, kWave);
  return v;
}

// Block reduction built on wave_reduce_sum: one LDS slot per wave.
__device__ __forceinline__ float block_reduce_sum(float v) {
  __shared__ float wave_sums[kBlock / kWave];
  int lane = threadIdx.x % kWave, wave = threadIdx.x / kWave;
  v = wave_reduce_sum(v);
  if (lane == 0) wave_sums[wave] = v;
  __syncthreads();
  v = (threadIdx.x < kBlock / kWave) ? wave_sums[lane] : 0.f;
  if (wave == 0) v = wave_reduce_sum(v);
  return v;  // valid in thread 0
}

// R5: first add during load + wave shuffles (one barrier per block).
__global__ void reduce_r5(const float* in, float* out, int n) {
  unsigned i = blockIdx.x * (2 * blockDim.x) + threadIdx.x;
  float v = (i < n) ? in[i] : 0.f;
  if (i + blockDim.x < n) v += in[i + blockDim.x];
  v = block_reduce_sum(v);
  if (threadIdx.x == 0) out[blockIdx.x] = v;
}
```

A wave can reduce 64 values entirely in registers with `__shfl_down`: 6 steps (offsets 32, 16, 8, 4, 2, 1) with no LDS stores and **no barriers**, since the lanes of a wave execute in lockstep. Only one LDS slot per wave and **one** `__syncthreads` per block remain, compared with 9 barriers in R4.

What the compiler generates on AMD (from `--save-temps`, gfx942):

```text
ds_bpermute_b32 v2, v1, v4      ; lane i reads v4 from lane (v1[i] / 4)
v_add_f32_e32   v4, v4, v2
ds_bpermute_b32 v3, v2, v4
...                             ; 6 x (bpermute + add), then one ds_write_b32 and s_barrier
```

- `__shfl_*` lowers to **`ds_bpermute_b32`**. It goes through the LDS crossbar but allocates no LDS. It is counted in `SQ_INSTS_LDS`, which is why R5 still shows about 8.75 LDS instructions per wave.
- rocPRIM/hipCUB use **DPP** (data-parallel primitives) instead: `v_add_f32_dpp ... row_ror:4`, `row_bcast:15`, `row_bcast:31`, `quad_perm:[1,0,3,2]`. These are VALU instructions with a cross-lane source modifier and never touch the LDS crossbar. That is one reason library reductions are hard to beat (see R7).
- With the `_sync` variants, the mask must be 64-bit: `__shfl_down_sync(0xFFFFFFFFFFFFFFFFull, v, off)`. Passing `0xFFFFFFFFu` fails to compile in recent HIP.

## 1.5 Rungs R6-R7: Grid-Stride, `float4`, and Finishing the Reduction

```cpp
// fragment: reduction.hip part 3 of 4 -- concatenate parts 1-4 in order to build
// R6: grid-stride loop with float4 loads; a fixed grid sized to fill the GPU.
// Requires `in` 16-byte aligned (hipMalloc guarantees 256 B); tail handled.
__device__ __forceinline__ float thread_partial_sum(const float* in, int n) {
  float v = 0.f;
  const float4* in4 = reinterpret_cast<const float4*>(in);
  int n4 = n / 4;
  for (int k = blockIdx.x * blockDim.x + threadIdx.x; k < n4; k += gridDim.x * blockDim.x) {
    float4 q = in4[k];
    v += (q.x + q.y) + (q.z + q.w);
  }
  for (int k = 4 * n4 + blockIdx.x * blockDim.x + threadIdx.x; k < n; k += gridDim.x * blockDim.x)
    v += in[k];
  return v;
}

// R6a: two-pass. Pass 1 writes one partial per block, pass 2 = one block.
__global__ void reduce_r6_partials(const float* in, float* partials, int n) {
  float v = block_reduce_sum(thread_partial_sum(in, n));
  if (threadIdx.x == 0) partials[blockIdx.x] = v;
}

// R6b: single pass, one float atomicAdd per block. Result order is
// nondeterministic (float addition is not associative) and *out must be zeroed.
__global__ void reduce_r6_atomic(const float* in, float* out, int n) {
  float v = block_reduce_sum(thread_partial_sum(in, n));
  if (threadIdx.x == 0) atomicAdd(out, v);
}

// R6c: single pass, deterministic: the last block to finish sums the partials
// in a fixed order. Needs a zeroed counter; the kernel resets it for reuse.
__global__ void reduce_r6_lastblock(const float* in, float* partials,
                                    unsigned* counter, float* out, int n) {
  __shared__ bool am_last;
  float v = block_reduce_sum(thread_partial_sum(in, n));
  if (threadIdx.x == 0) {
    partials[blockIdx.x] = v;
    __threadfence();  // make the partial visible device-wide before signalling
    unsigned done = atomicAdd(counter, 1u);
    am_last = (done == gridDim.x - 1);
  }
  __syncthreads();
  if (am_last) {
    __threadfence();  // acquire side: observe other blocks' partials
    float t = 0.f;
    for (int k = threadIdx.x; k < (int)gridDim.x; k += blockDim.x)
      t += partials[k];
    t = block_reduce_sum(t);
    if (threadIdx.x == 0) { *out = t; *counter = 0; }
  }
}

// R7: hipCUB block primitive (wave-size aware; rocPRIM underneath on AMD).
__global__ void reduce_cub_block(const float* in, float* partials, int n) {
  using BlockReduce = hipcub::BlockReduce<float, kBlock>;
  __shared__ typename BlockReduce::TempStorage temp;
  float v = BlockReduce(temp).Sum(thread_partial_sum(in, n));
  if (threadIdx.x == 0) partials[blockIdx.x] = v;
}
```

**R6: many elements per thread.** Launch a fixed grid that just fills the GPU (8 blocks x 256 threads per CU = 32 waves/CU, the most CDNA allows per CU at 8 waves/SIMD). Each thread then streams through the array with `float4` loads (`global_load_dwordx4`, 16 B per lane, 1 KB per wave instruction). Per-block overhead is now amortized over about 512 KB per block (1 GiB / 2,048 blocks) instead of 2 KB. This rung reaches **5.1 TB/s, about 95% of the read ceiling**.

Three ways to combine the per-block partials:

| Variant | Kernels | Deterministic? | Notes |
|---|---|---|---|
| R6a two-pass | 2+ (partials, then reduce partials) | Yes | Simplest and robust; the second pass is tiny |
| R6b atomic | 1 | **No**: float add order varies run to run | One `atomicAdd` per block; output must be zeroed first |
| R6c last-block | 1 | Yes | Fence + counter; the last block sums the partials in a fixed order |

R6c was **slower** here (3.7-3.8 TB/s). Each block runs a device-scope `__threadfence()` before signalling. On a multi-XCD GPU, device-scope release/acquire must make data visible across the 8 non-coherent L2s, so a device-scope fence costs much more than on a single-die GPU. Two-pass is usually the better default unless launch latency dominates (small `n`).

**Determinism:** R6b's relative error differed between runs (7.3e-8 in one run, 6.2e-9 in another), while all the other variants were bit-identical every time. Float addition is not associative, so the order in which atomics land changes the rounding. If a test compares against a golden value with `==`, an atomic reduction will make it flaky. See [Performance Engineering -- Floating-Point Numerics and Reproducibility](../computer-science/Performance_Engineering.md#9-floating-point-numerics-and-reproducibility).

**R7: hipCUB.** `hipcub::BlockReduce<float, 256>` matches the hand-written R6. `hipcub::DeviceReduce::Sum` (rocPRIM underneath) is the fastest variant at 5.4 TB/s. **In production, use the library.** Write your own only when you need to fuse the reduction into a larger kernel (for example, a reduction epilogue inside a GEMM or a norm).

## 1.6 Driver and Results

```cpp
// fragment: reduction.hip part 4 of 4 -- concatenate parts 1-4 in order to build
int main() {
  const int n = 1 << 28;  // 1 GiB of floats: well beyond the 256 MB Infinity Cache
  std::vector<float> h(n);
  for (int i = 0; i < n; ++i) h[i] = static_cast<float>(i % 7) * 0.25f;  // exact in fp32 per block
  double ref = 0.0;
  for (int i = 0; i < n; ++i) ref += h[i];

  float *d_in, *d_part, *d_out, *d_tmp;
  unsigned* d_counter;
  const int max_blocks = (n + kBlock - 1) / kBlock;
  HIP_CHECK(hipMalloc(&d_in, sizeof(float) * n));
  HIP_CHECK(hipMalloc(&d_part, sizeof(float) * max_blocks));
  HIP_CHECK(hipMalloc(&d_tmp, sizeof(float) * max_blocks));
  HIP_CHECK(hipMalloc(&d_out, sizeof(float)));
  HIP_CHECK(hipMalloc(&d_counter, sizeof(unsigned)));
  HIP_CHECK(hipMemset(d_counter, 0, sizeof(unsigned)));
  HIP_CHECK(hipMemcpy(d_in, h.data(), sizeof(float) * n, hipMemcpyHostToDevice));

  const double bytes = sizeof(float) * double(n);
  const int grid_fixed = num_cus() * 8;  // 8 blocks of 256 = 32 waves per CU
  float result = 0.f;

  // Finishes a multi-block reduction: repeatedly reduce partials with R5.
  auto finish = [&](float* part, int count) {
    float *src = part, *dst = d_tmp;
    while (count > 1) {
      int blocks = (count + 2 * kBlock - 1) / (2 * kBlock);
      reduce_r5<<<blocks, kBlock>>>(src, dst, count);
      count = blocks;
      std::swap(src, dst);
    }
    HIP_CHECK(hipMemcpyAsync(d_out, src, sizeof(float), hipMemcpyDeviceToDevice));
  };
  auto report = [&](const char* name, float ms) {
    HIP_CHECK(hipMemcpy(&result, d_out, sizeof(float), hipMemcpyDeviceToHost));
    std::printf("%-28s %8.3f ms %8.1f GB/s  rel.err %.2e\n", name, ms, gbps(bytes, ms),
                std::fabs(result - ref) / ref);
  };

  int b1 = max_blocks, b2 = (n + 2 * kBlock - 1) / (2 * kBlock);
  report("R1 interleaved divergent", time_ms([&] { reduce_r1<<<b1, kBlock>>>(d_in, d_part, n); finish(d_part, b1); }));
  report("R2 interleaved strided", time_ms([&] { reduce_r2<<<b1, kBlock>>>(d_in, d_part, n); finish(d_part, b1); }));
  report("R3 sequential addressing", time_ms([&] { reduce_r3<<<b1, kBlock>>>(d_in, d_part, n); finish(d_part, b1); }));
  report("R4 first add during load", time_ms([&] { reduce_r4<<<b2, kBlock>>>(d_in, d_part, n); finish(d_part, b2); }));
  report("R5 + wave shuffle", time_ms([&] { reduce_r5<<<b2, kBlock>>>(d_in, d_part, n); finish(d_part, b2); }));
  report("R6a grid-stride, two-pass", time_ms([&] {
    reduce_r6_partials<<<grid_fixed, kBlock>>>(d_in, d_part, n); finish(d_part, grid_fixed); }));
  report("R6b grid-stride, atomic", time_ms([&] {
    HIP_CHECK(hipMemsetAsync(d_out, 0, sizeof(float)));
    reduce_r6_atomic<<<grid_fixed, kBlock>>>(d_in, d_out, n); }));
  report("R6c grid-stride, last block", time_ms([&] {
    reduce_r6_lastblock<<<grid_fixed, kBlock>>>(d_in, d_part, d_counter, d_out, n); }));
  report("R7 hipcub::BlockReduce", time_ms([&] {
    reduce_cub_block<<<grid_fixed, kBlock>>>(d_in, d_part, n); finish(d_part, grid_fixed); }));

  // Library baseline: hipcub::DeviceReduce::Sum (two calls: size query, then run).
  size_t temp_bytes = 0;
  HIP_CHECK(hipcub::DeviceReduce::Sum(nullptr, temp_bytes, d_in, d_out, n));
  void* d_temp = nullptr;
  HIP_CHECK(hipMalloc(&d_temp, temp_bytes));
  report("hipcub::DeviceReduce::Sum", time_ms([&] {
    HIP_CHECK(hipcub::DeviceReduce::Sum(d_temp, temp_bytes, d_in, d_out, n)); }));

  HIP_CHECK(hipFree(d_temp));
  HIP_CHECK(hipFree(d_in)); HIP_CHECK(hipFree(d_part)); HIP_CHECK(hipFree(d_tmp));
  HIP_CHECK(hipFree(d_out)); HIP_CHECK(hipFree(d_counter));
  return 0;
}
```

Measured on MI350X (1 GiB of FP32; read ceiling 5.3-5.6 TB/s):

| Rung | Time (ms) | GB/s | % of read ceiling | What changed (counter evidence) |
|---|---|---|---|---|
| R1 interleaved, divergent | 0.915 | 1,170 | 21% | 21.5 LDS + 37.8 VALU instr/wave; 44/64 active lanes |
| R2 interleaved, strided | 0.914 | 1,175 | 21% | Less divergence (whole waves retire); 110M LDS conflict cycles |
| R3 sequential addressing | 0.806 | 1,330 | 24% | 8 LDS + 20.8 VALU/wave, 0 conflicts |
| R4 first add during load | 0.433 | 2,480 | 45% | Half the waves, 2x bytes per barrier |
| R5 wave shuffle | 0.343 | 3,130 | 57% | 1 barrier instead of 9; 61/64 active lanes |
| R6a grid-stride `float4`, two-pass | 0.208 | 5,150 | 94% | 1 KB per wave load instruction, fixed grid |
| R6b grid-stride, `atomicAdd` | 0.207 | 5,190 | 94% | Same; nondeterministic result |
| R6c grid-stride, last block | 0.281 | 3,820 | 70% | Device-scope fences across XCDs |
| R7 `hipcub::BlockReduce` | 0.208 | 5,160 | 94% | DPP wave reduction |
| `hipcub::DeviceReduce::Sum` | 0.198 | 5,420 | ~99% | Library tuning |

## 1.7 Interview Questions

**Q1.** Why is a reduction memory-bound, and what number should you compare against?

Its AI is 0.25 FLOP/B (one add per 4-byte element), while the FP32 ridge point is 20-30 FLOP/B on MI300-class GPUs. The roofline caps it at `0.25 x BW`, far below peak compute. Compare achieved GB/s (`4n / time`) against a **measured** read-bandwidth ceiling from a trivial streaming kernel on the same machine, not against TFLOP/s. A good reduction reaches 90%+ of that ceiling.

**Q2.** R2 removed the divergence of R1 but was not faster. Why, and how would you prove it?

The strided index `2*s*tid` makes lanes in the same wave hit the same LDS bank, so the LDS serializes them. Prove it with `SQ_LDS_BANK_CONFLICT` (0 for R1, 110M cycles for R2), or rocprof-compute's "LDS Bank Conflicts/Access". The general lesson: a fix that removes one stall can expose or add another. Measure both counters, not just the time.

**Q3.** How does a wave-level shuffle reduction work on AMD, and what changes from CUDA?

Each step does `v += __shfl_down(v, off)` with `off = 32, 16, 8, 4, 2, 1`, which is 6 steps for 64 lanes, against 5 starting at 16 on NVIDIA. After the loop, lane 0 holds the sum. It needs no LDS and no barrier because the lanes of a wave execute together. On AMD it compiles to `ds_bpermute_b32` (or DPP in rocPRIM). The `_sync` variants need 64-bit masks, and any code that assumes 32 lanes (`tid & 31`, a `[blockDim/32]` array, a `tid < 32` tail) must be fixed.

**Q4.** How many blocks do you launch for a grid-stride reduction, and why not one thread per element?

Enough to fill every CU at full occupancy and no more: here `CUs x 8` blocks of 256 threads. More blocks only add partials and launch overhead. Fewer leave CUs idle or reduce the bytes in flight, and with them Little's-law bandwidth. One thread per element makes per-block fixed costs (index math, barriers, a write of the partial) dominate. With a grid stride, each thread amortizes them over hundreds of elements and can issue wide `float4` loads.

**Q5.** Your reduction result differs in the last bits between runs. Is that a bug?

Not necessarily. If partials are combined with `atomicAdd` on floats, the order of additions depends on block scheduling, and float addition is not associative. Fixes: two-pass or last-block with a fixed combine order (deterministic for a fixed grid size), accumulation in double or Kahan/pairwise summation to reduce the error, or integer/fixed-point accumulation for bit-exact results. Note that "deterministic" usually still changes if the grid size (that is, the GPU model) changes.

**Q6.** In R6c, why are two `__threadfence()` calls needed, and why is that variant slower on MI300X/MI350X?

The writer must make its partial visible before the counter increment can be observed (release). The last block must not read partials until after it has seen the final count (acquire). Without the fences, the last block can read stale partials from its L1/L2. On CDNA3/CDNA4 each XCD has its own L2, and those L2s are not coherent with one another. A device-scope fence must write back or invalidate cache contents so other XCDs can see the data, which costs far more than the same fence on a single-die GPU. The 2,048 fences cost about 70 us here.

**Q7.** What would you look at in rocprof-compute to decide which rung you are on?

Speed-of-light HBM bandwidth (far below ceiling means not streaming), Wavefront Occupancy, "VALU Active Threads" (divergence), "LDS Bank Conflicts/Access", instruction counts per wave (`SQ_INSTS_LDS`, `SQ_INSTS_VALU` divided by `SQ_WAVES`), and the instruction mix. A healthy final reduction shows HBM bandwidth near the ceiling, almost no LDS, and only a few VALU instructions per loaded byte.

---

# 2. Matrix Transpose

## 2.1 Problem and Roofline Position

`out[c][r] = in[r][c]` for an 8192 x 8192 FP32 matrix (256 MiB in, 256 MiB out). There is no arithmetic at all (**AI = 0**), so the only figure of merit is bandwidth. The **speed of light is a straight copy** of the same bytes with both sides coalesced, because a transpose can never beat a copy. The whole case study is about making the *write* side as cheap as the read side.

## 2.2 Code: Copy Baseline, Naive, LDS Tiled, Padded

```cpp
// transpose.hip -- out[c][r] = in[r][c] for a rows x cols row-major matrix
// Build: hipcc -O3 --offload-arch=gfx942 transpose.hip -o transpose
#include "common.hpp"
#include <vector>

constexpr int TILE = 64;      // tile edge = one wavefront wide on CDNA
constexpr int ROWS_PER = 4;   // block = 64 x 4 threads, each thread moves 16 elements

// Baseline: straight copy (same bytes, both sides coalesced) = the speed-of-light.
__global__ void copy_kernel(const float* __restrict__ in, float* __restrict__ out,
                            int rows, int cols) {
  int c = blockIdx.x * TILE + threadIdx.x;
  for (int r = blockIdx.y * TILE + threadIdx.y; r < blockIdx.y * TILE + TILE; r += ROWS_PER)
    if (r < rows && c < cols) out[(size_t)r * cols + c] = in[(size_t)r * cols + c];
}

// T1 naive: reads coalesced (consecutive threadIdx.x -> consecutive c),
// writes strided by `rows` floats -> every lane of a wave hits a different cache line.
__global__ void transpose_naive(const float* __restrict__ in, float* __restrict__ out,
                                int rows, int cols) {
  int c = blockIdx.x * TILE + threadIdx.x;
  for (int r = blockIdx.y * TILE + threadIdx.y; r < blockIdx.y * TILE + TILE; r += ROWS_PER)
    if (r < rows && c < cols) out[(size_t)c * rows + r] = in[(size_t)r * cols + c];
}

// T2 LDS tiled: coalesced read of a tile row into LDS, coalesced write of a tile
// column out of LDS. The column read tile[threadIdx.x][...] has a stride of TILE
// floats -> every lane maps to the same LDS bank (TILE % banks == 0).
template <int PAD>
__global__ void transpose_lds(const float* __restrict__ in, float* __restrict__ out,
                              int rows, int cols) {
  __shared__ float tile[TILE][TILE + PAD];  // PAD = 1 shifts each row by one bank
  int bx = blockIdx.x * TILE, by = blockIdx.y * TILE;
  int c = bx + threadIdx.x;
  for (int j = threadIdx.y; j < TILE; j += ROWS_PER) {
    int r = by + j;
    if (r < rows && c < cols) tile[j][threadIdx.x] = in[(size_t)r * cols + c];
  }
  __syncthreads();
  // Output tile is at (row block bx, col block by) of the cols x rows result.
  int oc = by + threadIdx.x;
  for (int j = threadIdx.y; j < TILE; j += ROWS_PER) {
    int orow = bx + j;
    if (orow < cols && oc < rows) out[(size_t)orow * rows + oc] = tile[threadIdx.x][j];
  }
}

int main() {
  const int rows = 8192, cols = 8192;  // 256 MiB in + 256 MiB out
  const size_t n = (size_t)rows * cols;
  std::vector<float> h(n), back(n);
  for (size_t i = 0; i < n; ++i) h[i] = static_cast<float>(i % 1000003);
  float *d_in, *d_out;
  HIP_CHECK(hipMalloc(&d_in, n * sizeof(float)));
  HIP_CHECK(hipMalloc(&d_out, n * sizeof(float)));
  HIP_CHECK(hipMemcpy(d_in, h.data(), n * sizeof(float), hipMemcpyHostToDevice));

  dim3 block(TILE, ROWS_PER), grid((cols + TILE - 1) / TILE, (rows + TILE - 1) / TILE);
  const double bytes = 2.0 * n * sizeof(float);  // read once + write once
  auto check = [&](const char* name, float ms, bool is_transpose) {
    HIP_CHECK(hipMemcpy(back.data(), d_out, n * sizeof(float), hipMemcpyDeviceToHost));
    bool ok = true;
    for (int r = 0; r < rows && ok; r += 97)
      for (int c = 0; c < cols && ok; c += 89)
        ok = is_transpose ? back[(size_t)c * rows + r] == h[(size_t)r * cols + c]
                          : back[(size_t)r * cols + c] == h[(size_t)r * cols + c];
    std::printf("%-22s %7.3f ms %8.1f GB/s %s\n", name, ms, gbps(bytes, ms), ok ? "OK" : "WRONG");
  };
  check("copy (speed of light)", time_ms([&] { copy_kernel<<<grid, block>>>(d_in, d_out, rows, cols); }), false);
  check("T1 naive", time_ms([&] { transpose_naive<<<grid, block>>>(d_in, d_out, rows, cols); }), true);
  check("T2 LDS tiled", time_ms([&] { transpose_lds<0><<<grid, block>>>(d_in, d_out, rows, cols); }), true);
  check("T3 LDS tiled + pad", time_ms([&] { transpose_lds<1><<<grid, block>>>(d_in, d_out, rows, cols); }), true);
  HIP_CHECK(hipFree(d_in));
  HIP_CHECK(hipFree(d_out));
  return 0;
}
```

## 2.3 Why Each Step Helps

**T1 naive.** Reads are coalesced: 64 consecutive lanes read 256 contiguous bytes. Writes go to `out[c * rows + r]`, so consecutive lanes are `rows x 4 = 32 KB` apart and every lane of a wave hits a different cache line. Counter evidence: **`TCP_TCC_WRITE_REQ_sum` = 67.1M for T1 vs 4.19M for copy**, a 16x increase in L1-to-L2 write requests, or one request per element. rocprof-compute shows the same as low "vL1D Coalescing". Result: 20% of copy bandwidth.

**T2 LDS tiled.** Stage a 64 x 64 tile in LDS. Read it row-wise (coalesced global reads), then write it out column-wise (coalesced global writes), doing the transposition *inside LDS* where scattered access is cheap. L2 write requests fall back to 4.19M, the same as copy. The new problem is that the column read `tile[threadIdx.x][j]` has a stride of 64 words. With 64 banks (CDNA4) **all 64 lanes hit the same bank**. With 32 banks (CDNA3), each group of 32 lanes does. **`SQ_LDS_BANK_CONFLICT` = 65M cycles**, about 62 extra cycles per LDS read instruction on gfx950, which matches a 64-way conflict.

**T3 padding.** Declaring `tile[64][65]` shifts each row by one bank: element `[x][j]` lives at word `65x + j`, so `bank = (65x + j) mod B` differs for every `x` when B is 32 or 64. **Conflicts drop to 0** with no change to the global access pattern. Result: 3.66 TB/s, **about 90% of the copy kernel**.

Bank-conflict arithmetic you should be able to do on a whiteboard (4-byte words, B banks):

```text
bank(word_index) = word_index mod B
column access, row length L:  lane x -> word x*L + j  -> bank (x*L + j) mod B
distinct banks among B lanes = B / gcd(L, B)   ->   gcd(L, B)-way conflict
L = 64, B = 64: gcd = 64 -> 1 distinct bank  -> 64-way conflict
L = 65, B = 64: gcd = 1  -> 64 distinct      -> conflict-free
L = 64, B = 32: gcd = 32 -> 1 distinct bank  -> 32-way (per 32-lane half)
L = 33, B = 32: gcd = 1  -> conflict-free  (the CUDA "TILE_DIM + 1" idiom)
```

Padding is not free. It wastes 1/65 of the LDS, and it breaks 16-byte alignment of rows. If you later want `ds_read_b128` along a row, pad by 4 words or use an **XOR swizzle** (`col ^ row`) instead, which avoids conflicts without wasting space. Section 6 shows a measured case where padding broke vectorization and made a GEMM slower.

## 2.4 Results

Measured on MI350X (8192 x 8192 FP32; bytes counted = read + write = 537 MB):

| Variant | Time (ms) | GB/s | % of copy | `TCP_TCC_WRITE_REQ_sum` | `SQ_LDS_BANK_CONFLICT` |
|---|---|---|---|---|---|
| Copy (speed of light) | 0.131-0.134 | 4,010-4,090 | 100% | 4.19M | 0 |
| T1 naive | 0.668 | 803 | 20% | **67.1M** | 0 |
| T2 LDS tiled | 0.179 | 2,995 | 74% | 4.19M | **65.0M** |
| T3 LDS tiled + pad | 0.146 | 3,660-3,690 | ~90% | 4.19M | 0 |

Design choices worth defending:

- **Tile 64 x 64 with a 64 x 4 block.** Tile width equals the wave width, so one wave row-read is one fully used 256-byte segment. Each thread moves 16 elements, which amortizes index math and gives each wave 16 independent loads in flight (memory-level parallelism).
- **`__restrict__`** tells the compiler `in` and `out` do not alias, so it can keep loads in flight across stores.
- Non-square or non-multiple sizes need the bounds checks shown. In-place square transpose swaps tile `(i, j)` with tile `(j, i)` using two LDS tiles, with diagonal tiles handled once.
- **CDNA4** adds LDS "read with transpose" instructions aimed at feeding matrix cores with transposed fragments. Libraries use them, but the padding technique above is what interviews expect.

## 2.5 Interview Questions

**Q1.** Why is the naive transpose 5x slower than copy when both move the same bytes?

Coalescing. The hardware merges the 64 lane addresses of one wave memory instruction into as few cache-line requests as possible. Naive writes put every lane in a different line, so one store instruction becomes 64 separate L2 requests, each writing 4 useful bytes of a 64- or 128-byte line. The DRAM sees partial-line writes (read-modify-write in the worst case), and the L1-L2 fabric is flooded. `TCP_TCC_WRITE_REQ_sum` rises 16x and the vL1D Coalescing metric collapses.

**Q2.** What is an LDS bank conflict, and how do you compute whether an access pattern has one?

LDS is split into B banks (32 on CDNA3, 64 on CDNA4), each 4 bytes wide, and each bank serves one address per cycle. Lanes in the same access group that hit **different addresses in the same bank** serialize. Lanes reading the *same* address get a broadcast and do not conflict. For word index `w`, `bank = w mod B`. A column read with row length L gives `B / gcd(L, B)` distinct banks. Make `gcd(L, B) = 1` (pad by 1) or permute columns with an XOR swizzle.

**Q3.** Why pad with +1 rather than, say, +4?

+1 makes the row length odd, so `gcd(L, B) = 1` for any power-of-two bank count: 4-byte column accesses are conflict-free on both CDNA3 and CDNA4 (and NVIDIA). +4 gives `gcd(68, 64) = 4`, a 4-way conflict for 4-byte column reads. It is the right choice only when each lane reads a 16-byte vector (`ds_read_b128`), because then the unit of access is 4 words and rows must stay 16-byte aligned. An XOR swizzle gets both properties without wasting LDS.

**Q4.** How would you verify a transpose is "done"?

Compare it to a copy kernel with the same grid shape and bytes on the same GPU. If it reaches 85-95% of copy, stop. Confirm with counters: L2 write requests equal to copy's, zero bank conflicts, HBM bandwidth near the ceiling. Any further gain must come from fusing the transpose into its producer or consumer, so the data is never written transposed at all.

**Q5.** The transpose is part of a larger pipeline (for example `X^T W`). What do you do?

Do not materialize it. Pass a transposed layout flag to the GEMM (BLAS `op(A) = A^T`), or have the consumer read with a transposed index from a tile in LDS. Materializing a transpose costs a full read and a full write of the matrix through HBM, and that can easily cost more than the computation it feeds.

---

# 3. Prefix Scan

## 3.1 Problem and Algorithms

Inclusive scan `out[i] = in[0] + ... + in[i]` (exclusive: up to `i-1`) over `n = 2^28` ints. Like reduction, it is memory-bound: about one add per 8 bytes moved (AI around 0.125 op/B). The ideal traffic is **read n + write n = 2n elements**, so the target is copy bandwidth.

| Algorithm | Work | Steps (depth) | Notes |
|---|---|---|---|
| Sequential | n | n | Baseline; what each thread does on its own items |
| Hillis-Steele | n log n | log n | Simple, step-efficient, not work-efficient; needs double buffering |
| Blelloch (up-sweep + down-sweep) | 2n | 2 log n | Work-efficient, exclusive by construction; strided LDS access means bank conflicts |
| Wave shuffle + raking | n + small | log 64 + log(waves) | What CUB/rocPRIM do inside a block |
| Reduce-then-scan (3 phases) | ~2n | 3 kernels | Reads input twice: **3n traffic** |
| Chained scan with **decoupled look-back** | n | 1 pass | **2n traffic**; the single-pass algorithm in CUB/rocPRIM |

## 3.2 Block-Level Scans: Hillis-Steele and Blelloch

```cpp
// fragment: scan.hip part 1 of 5 -- concatenate parts 1-5 in order to build
// scan.hip -- prefix sums: block-level algorithms and a full-array scan
// Build: hipcc -O3 --offload-arch=gfx942 scan.hip -o scan
#include "common.hpp"
#include <hipcub/hipcub.hpp>
#include <vector>

constexpr int SEG = 1024;     // segment length for the block-level comparisons
constexpr int kLogBanks = 5;  // 32 LDS banks on CDNA3 (gfx942); CDNA4 (gfx950) has 64 -> 6

// ---------- S1: Hillis-Steele (inclusive, O(n log n) work, log n steps) ----------
__global__ void scan_hillis_steele(const int* __restrict__ in, int* __restrict__ out) {
  __shared__ int buf[2][SEG];  // double buffer: read one, write the other
  int t = threadIdx.x;
  size_t base = (size_t)blockIdx.x * SEG;
  int cur = 0;
  buf[cur][t] = in[base + t];
  __syncthreads();
  for (int off = 1; off < SEG; off <<= 1) {
    int nxt = 1 - cur;
    buf[nxt][t] = buf[cur][t] + (t >= off ? buf[cur][t - off] : 0);
    cur = nxt;
    __syncthreads();
  }
  out[base + t] = buf[cur][t];
}

// ---------- S2: Blelloch (exclusive, O(n) work, 2 log n steps) ----------
template <bool PAD>
__device__ __forceinline__ int pad(int i) { return PAD ? i + (i >> kLogBanks) : i; }

template <bool PAD>
__global__ void scan_blelloch(const int* __restrict__ in, int* __restrict__ out) {
  __shared__ int s[SEG + SEG / 32];  // room for padding
  int t = threadIdx.x;                 // SEG/2 threads, 2 elements each
  size_t base = (size_t)blockIdx.x * SEG;
  s[pad<PAD>(t)] = in[base + t];
  s[pad<PAD>(t + SEG / 2)] = in[base + t + SEG / 2];
  int off = 1;
  for (int d = SEG >> 1; d > 0; d >>= 1) {  // up-sweep (reduce) phase
    __syncthreads();
    if (t < d) {
      int a = off * (2 * t + 1) - 1, b = off * (2 * t + 2) - 1;
      s[pad<PAD>(b)] += s[pad<PAD>(a)];
    }
    off <<= 1;
  }
  if (t == 0) s[pad<PAD>(SEG - 1)] = 0;   // clear the root
  for (int d = 1; d < SEG; d <<= 1) {     // down-sweep phase
    off >>= 1;
    __syncthreads();
    if (t < d) {
      int a = off * (2 * t + 1) - 1, b = off * (2 * t + 2) - 1;
      int x = s[pad<PAD>(a)];
      s[pad<PAD>(a)] = s[pad<PAD>(b)];
      s[pad<PAD>(b)] += x;
    }
  }
  __syncthreads();
  out[base + t] = s[pad<PAD>(t)];
  out[base + t + SEG / 2] = s[pad<PAD>(t + SEG / 2)];
}
```

**Hillis-Steele.** At step `off`, each element adds the element `off` positions to its left. That gives 10 steps for 1024 elements and `n log n` adds in total. It needs **two buffers**, because element `t` must read the *old* value of `t - off` while another thread may be overwriting it. A single-buffer version is a classic interview bug (a race).

**Blelloch.** The **up-sweep** builds a reduction tree in place (the root ends up holding the total). Set the root to 0, then the **down-sweep** pushes prefixes down the tree: each node passes its value to its left child and passes value + left-child sum to its right child. That is 2(n-1) adds, which is work-efficient. The index pattern `off*(2t+1)-1` has a power-of-two stride that grows each level, so it hits the same bank repeatedly. The fix from GPU Gems 3 (chapter 39) is to pad every B words: `i + (i >> log2(B))`. Here it gave only a small gain (0.88 ms to 0.85 ms), partly because `kLogBanks = 5` is tuned for CDNA3's 32 banks and the run was on 64-bank gfx950.

## 3.3 What Libraries Actually Do: Registers + Wave Shuffles

```cpp
// fragment: scan.hip part 2 of 5 -- concatenate parts 1-5 in order to build
// ---------- S3: wave-shuffle scan (what libraries actually do) ----------
__device__ __forceinline__ int wave_inclusive_scan(int v) {
  int lane = threadIdx.x % kWave;
  for (int off = 1; off < kWave; off <<= 1) {  // 6 steps on wave64, 5 on warp32
    int up = __shfl_up(v, off, kWave);
    if (lane >= off) v += up;
  }
  return v;
}

// Inclusive scan across the block; also returns the block total.
// Reuses static LDS (wave_tot): if called repeatedly, separate calls with a
// __syncthreads() after all reads of the result (see small_inclusive_scan).
template <int BLOCK>
__device__ __forceinline__ int block_inclusive_scan(int v, int& total) {
  constexpr int kWaves = BLOCK / kWave;
  __shared__ int wave_tot[kWaves];
  int lane = threadIdx.x % kWave, wave = threadIdx.x / kWave;
  v = wave_inclusive_scan(v);
  if (lane == kWave - 1) wave_tot[wave] = v;
  __syncthreads();
  if (wave == 0) {
    int w = (lane < kWaves) ? wave_tot[lane] : 0;
    w = wave_inclusive_scan(w);
    if (lane < kWaves) wave_tot[lane] = w;
  }
  __syncthreads();
  if (wave > 0) v += wave_tot[wave - 1];
  total = wave_tot[kWaves - 1];
  return v;
}

constexpr int kScanBlock = 256, kItems = 4;  // 4 consecutive ints per thread = one int4
static_assert(kScanBlock * kItems == SEG, "segment size");

// Thread-local scan of 4 items, block scan of thread totals, add the exclusive prefix.
// `seed` is an offset added to every output (used by the full-array scan).
__device__ __forceinline__ int scan_tile(const int4* in4, int4* out4, size_t tile, int seed) {
  int4 q = in4[tile * kScanBlock + threadIdx.x];
  q.y += q.x; q.z += q.y; q.w += q.z;      // sequential scan in registers
  int total;
  int incl = block_inclusive_scan<kScanBlock>(q.w, total);
  int excl = incl - q.w + seed;
  q.x += excl; q.y += excl; q.z += excl; q.w += excl;
  out4[tile * kScanBlock + threadIdx.x] = q;
  return total;
}

__global__ void scan_wave_segmented(const int4* __restrict__ in4, int4* __restrict__ out4) {
  scan_tile(in4, out4, blockIdx.x, 0);
}
```

Each thread first scans its **4 consecutive items sequentially in registers** (one `int4` load). The block then scans only the 256 per-thread totals: a 6-step `__shfl_up` scan inside each wave, a scan of the 4 wave totals by wave 0, and one add. The result is **2 barriers per tile**, compared with 21 for Blelloch, plus vector loads and almost no LDS traffic. Segmented throughput went from 2.4 TB/s (Blelloch) to **4.7-4.8 TB/s**, about the speed of copy. More items per thread (8-16) amortizes further; rocPRIM tunes this per architecture.

## 3.4 Full-Array Scan: Reduce-Then-Scan

```cpp
// fragment: scan.hip part 3 of 5 -- concatenate parts 1-5 in order to build
// ---------- Full-array scan: reduce-then-scan (~3n memory traffic) ----------
// Pass 1: one sum per tile of SEG elements.
__global__ void tile_sums(const int4* __restrict__ in4, int* __restrict__ sums) {
  __shared__ int ws[kScanBlock / kWave];
  int4 q = in4[(size_t)blockIdx.x * kScanBlock + threadIdx.x];
  int v = q.x + q.y + q.z + q.w;
  for (int off = kWave / 2; off > 0; off >>= 1) v += __shfl_down(v, off, kWave);
  if (threadIdx.x % kWave == 0) ws[threadIdx.x / kWave] = v;
  __syncthreads();
  if (threadIdx.x == 0) {
    int t = 0;
    for (int w = 0; w < kScanBlock / kWave; ++w) t += ws[w];
    sums[blockIdx.x] = t;
  }
}
// Base case: inclusive scan of a short array with ONE block (in place is fine).
__global__ void small_inclusive_scan(const int* in, int* out, int count) {
  __shared__ int carry;
  if (threadIdx.x == 0) carry = 0;
  __syncthreads();
  for (int base = 0; base < count; base += kScanBlock) {
    int i = base + threadIdx.x;
    int v = (i < count) ? in[i] : 0, total;
    int incl = block_inclusive_scan<kScanBlock>(v, total);
    int c = carry;
    if (i < count) out[i] = c + incl;
    __syncthreads();  // everyone has read carry and wave_tot before they change
    if (threadIdx.x == 0) carry = c + total;
    __syncthreads();
  }
}
// Pass 3: rescan each tile, seeded with the inclusive sum of all previous tiles.
__global__ void scan_tiles_seeded(const int4* in4, int4* out4, const int* incl_tile_sums) {
  int seed = blockIdx.x ? incl_tile_sums[blockIdx.x - 1] : 0;
  scan_tile(in4, out4, blockIdx.x, seed);
}
// Recursive driver: count must be a multiple of SEG unless count <= 4 * SEG.
// scratch needs count/SEG + count/SEG^2 + ... ints. In-place (in == out) is allowed.
void inclusive_scan(const int* d_in, int* d_out, int count, int* scratch) {
  if (count <= 4 * SEG) {
    small_inclusive_scan<<<1, kScanBlock>>>(d_in, d_out, count);
    return;
  }
  int tiles = count / SEG;
  tile_sums<<<tiles, kScanBlock>>>(reinterpret_cast<const int4*>(d_in), scratch);
  inclusive_scan(scratch, scratch, tiles, scratch + tiles);  // scan the tile sums
  scan_tiles_seeded<<<tiles, kScanBlock>>>(reinterpret_cast<const int4*>(d_in),
                                           reinterpret_cast<int4*>(d_out), scratch);
}
```

Phase 1 reads the input once to compute a sum per 1024-element tile. Phase 2 scans the 262,144 tile sums (recursively, with a one-block base case). Phase 3 reads the input **again**, scans each tile, and adds the tile's prefix. Traffic is **3n**: the measured 0.65 ms is 3.3 TB/s against the 2n ideal, which corresponds to about 5 TB/s of actual traffic, so the kernel streams well. A first version scanned the 262K tile sums with a **single block** in a loop. That alone took 0.9 ms (1,024 sequential iterations, each with barriers) and made the whole scan 2.4x slower. **Never leave a serial one-block phase on the critical path of a large problem.**

## 3.5 Single Pass: Decoupled Look-Back

```cpp
// fragment: scan.hip part 4 of 5 -- concatenate parts 1-5 in order to build
// ---------- S6: single-pass scan with decoupled look-back (simplified) ----------
// Each tile publishes a 64-bit status word {flag, value}: flag 1 = "aggregate
// (my tile's sum) ready", flag 2 = "inclusive prefix (sum of tiles 0..me) ready".
// A tile walks backwards adding aggregates until it meets an inclusive prefix.
// Traffic: read n + write n (plus tiny status array) -> 2n, vs 3n for reduce-then-scan.
constexpr unsigned long long kFlagAggregate = 1ull << 32, kFlagPrefix = 2ull << 32;

__device__ __forceinline__ void publish(unsigned long long* p, unsigned long long flag, int value) {
  __hip_atomic_store(p, flag | (unsigned)value, __ATOMIC_RELAXED, __HIP_MEMORY_SCOPE_AGENT);
}

__global__ void scan_decoupled_lookback(const int4* __restrict__ in4, int4* __restrict__ out4,
                                        unsigned long long* status, unsigned* tile_counter) {
  __shared__ int tile_s, prefix_s;
  // Tiles are numbered in the order blocks START, not by blockIdx: a tile only
  // ever waits on tiles that are already running, so the spin cannot deadlock.
  if (threadIdx.x == 0) tile_s = atomicAdd(tile_counter, 1u);
  __syncthreads();
  const size_t tile = tile_s;
  int4 q = in4[tile * kScanBlock + threadIdx.x];
  q.y += q.x; q.z += q.y; q.w += q.z;
  int total;
  int incl = block_inclusive_scan<kScanBlock>(q.w, total);
  if (threadIdx.x == 0) {
    int exclusive = 0;
    if (tile == 0) {
      publish(&status[0], kFlagPrefix, total);
    } else {
      publish(&status[tile], kFlagAggregate, total);  // let successors start early
      for (size_t look = tile - 1;; --look) {         // production code looks back a whole wave at once
        unsigned long long s;
        do {
          s = __hip_atomic_load(&status[look], __ATOMIC_RELAXED, __HIP_MEMORY_SCOPE_AGENT);
        } while ((s >> 32) == 0);                       // predecessor has not published yet
        exclusive += (int)(unsigned)s;
        if ((s >> 32) == 2) break;                      // found an inclusive prefix: done
      }
      publish(&status[tile], kFlagPrefix, exclusive + total);
    }
    prefix_s = exclusive;
  }
  __syncthreads();
  int excl = prefix_s + incl - q.w;
  q.x += excl; q.y += excl; q.z += excl; q.w += excl;
  out4[tile * kScanBlock + threadIdx.x] = q;
}
```

The idea (Merrill and Garland, 2016) is to make the scan **one pass**, with traffic 2n, by chaining tiles:

1. Each block takes a **dynamic tile index** from an atomic counter. Tiles are then processed in the order they *start*, so a tile only ever waits on tiles that are already running. With `blockIdx.x` instead, tile 1000 could be resident and spinning while tile 999 never gets scheduled, which deadlocks the GPU.
2. Each tile scans locally, then **publishes its aggregate** (flag A) right away.
3. It then **looks back** over its predecessors: it adds aggregates until it finds a predecessor that has published an **inclusive prefix** (flag P), then publishes its own inclusive prefix.
4. The flag and value are packed into **one 64-bit word** written atomically, so a reader can never see a flag without its value. That is why relaxed atomics are enough here.

The simple version above is **correct but slow** (0.66 TB/s). Its look-back is serial: one lane polls one predecessor at a time with device-scope atomic loads. On a multi-XCD GPU those loads cannot be served by the local L2, so each poll is a long round trip. Production implementations (CUB, rocPRIM) look back **a whole wave at a time** (64 predecessors per poll, combined with a ballot and a wave reduction), use bigger tiles (thousands of items) so there are fewer tiles, and tune per architecture. On our MI350X and nightly build, `hipcub::DeviceScan::InclusiveSum` ran at 2.3 TB/s-equivalent, *slower* than the 3-kernel reduce-then-scan (3.3 TB/s-equivalent). On multi-XCD parts the cross-XCD flag latency can outweigh the saved n of traffic. **Measure; do not assume single-pass wins.**

## 3.6 Driver and Results

```cpp
// fragment: scan.hip part 5 of 5 -- concatenate parts 1-5 in order to build
int main() {
  const int n = 1 << 28, segs = n / SEG;
  std::vector<int> h(n), back(n);
  for (int i = 0; i < n; ++i) h[i] = (i * 7 + 3) % 3;  // values 0..2: no int32 overflow
  int *d_in, *d_out, *d_sums;
  HIP_CHECK(hipMalloc(&d_in, sizeof(int) * n));
  HIP_CHECK(hipMalloc(&d_out, sizeof(int) * n));
  HIP_CHECK(hipMalloc(&d_sums, sizeof(int) * 2 * segs));  // >= sum of all levels
  HIP_CHECK(hipMemcpy(d_in, h.data(), sizeof(int) * n, hipMemcpyHostToDevice));
  auto in4 = reinterpret_cast<const int4*>(d_in);
  auto out4 = reinterpret_cast<int4*>(d_out);

  // segmented: each SEG block scanned independently; global: one scan over all n
  auto verify = [&](bool segmented, bool exclusive) {
    HIP_CHECK(hipMemcpy(back.data(), d_out, sizeof(int) * n, hipMemcpyDeviceToHost));
    long long run = 0;
    for (int i = 0; i < n; ++i) {
      if (segmented && i % SEG == 0) run = 0;
      long long expect = exclusive ? run : run + h[i];
      if (back[i] != expect) return false;
      run += h[i];
    }
    return true;
  };
  const double bytes2 = 2.0 * sizeof(int) * n;  // ideal traffic: read n + write n
  auto report = [&](const char* name, float ms, bool ok) {
    std::printf("%-34s %7.3f ms %8.1f GB/s (vs 2n bytes) %s\n", name, ms, gbps(bytes2, ms), ok ? "OK" : "WRONG");
  };
  float ms;
  ms = time_ms([&] { scan_hillis_steele<<<segs, SEG>>>(d_in, d_out); });
  report("S1 Hillis-Steele (segmented)", ms, verify(true, false));
  ms = time_ms([&] { scan_blelloch<false><<<segs, SEG / 2>>>(d_in, d_out); });
  report("S2 Blelloch (segmented)", ms, verify(true, true));
  ms = time_ms([&] { scan_blelloch<true><<<segs, SEG / 2>>>(d_in, d_out); });
  report("S2 Blelloch + pad (segmented)", ms, verify(true, true));
  ms = time_ms([&] { scan_wave_segmented<<<segs, kScanBlock>>>(in4, out4); });
  report("S3 wave shuffle (segmented)", ms, verify(true, false));

  ms = time_ms([&] { inclusive_scan(d_in, d_out, n, d_sums); });
  report("S4 reduce-then-scan (full array)", ms, verify(false, false));

  unsigned long long* d_status;
  unsigned* d_counter;
  HIP_CHECK(hipMalloc(&d_status, sizeof(unsigned long long) * segs));
  HIP_CHECK(hipMalloc(&d_counter, sizeof(unsigned)));
  ms = time_ms([&] {
    HIP_CHECK(hipMemsetAsync(d_status, 0, sizeof(unsigned long long) * segs));
    HIP_CHECK(hipMemsetAsync(d_counter, 0, sizeof(unsigned)));
    scan_decoupled_lookback<<<segs, kScanBlock>>>(in4, out4, d_status, d_counter);
  });
  report("S6 decoupled look-back (simple)", ms, verify(false, false));
  HIP_CHECK(hipFree(d_status));
  HIP_CHECK(hipFree(d_counter));

  size_t temp_bytes = 0;
  HIP_CHECK(hipcub::DeviceScan::InclusiveSum(nullptr, temp_bytes, d_in, d_out, n));
  void* d_temp;
  HIP_CHECK(hipMalloc(&d_temp, temp_bytes));
  ms = time_ms([&] { HIP_CHECK(hipcub::DeviceScan::InclusiveSum(d_temp, temp_bytes, d_in, d_out, n)); });
  report("S5 hipcub DeviceScan (look-back)", ms, verify(false, false));

  HIP_CHECK(hipFree(d_temp)); HIP_CHECK(hipFree(d_in));
  HIP_CHECK(hipFree(d_out)); HIP_CHECK(hipFree(d_sums));
  return 0;
}
```

Measured on MI350X (`n = 2^28` int32; GB/s computed against 2n bytes):

| Variant | Scope | Time (ms) | GB/s (2n) | Notes |
|---|---|---|---|---|
| S1 Hillis-Steele | per 1024-segment | 1.18 | 1,815 | 10 steps, 11 barriers, n log n adds |
| S2 Blelloch | per segment | 0.88 | 2,430 | Work-efficient; bank conflicts |
| S2 Blelloch + pad | per segment | 0.85 | 2,540 | Conflict padding |
| S3 registers + wave shuffle | per segment | 0.45-0.46 | 4,690-4,810 | ~copy speed |
| S4 reduce-then-scan | full array | 0.65 | 3,300 | 3n traffic, ~5 TB/s actual |
| S6 decoupled look-back (simple) | full array | 3.23 | 664 | Serial look-back latency |
| S5 `hipcub::DeviceScan::InclusiveSum` | full array | 0.92 | 2,335 | Library single-pass |

## 3.7 Interview Questions

**Q1.** Compare Hillis-Steele and Blelloch. When would you choose Hillis-Steele?

Hillis-Steele does `n log n` work in `log n` steps. Blelloch does `2n` work in `2 log n` steps. When there are as many processors as elements (a wave scanning 64 values in registers), step count matters more than total work, and Hillis-Steele's simple shuffle pattern wins. That is exactly what the wave-level `__shfl_up` scan is. For large arrays, work efficiency wins, so libraries use sequential per-thread scans plus a small parallel scan of the totals.

**Q2.** What race does a single-buffer Hillis-Steele have?

At step `off`, thread `t` reads `s[t - off]` while thread `t - off` may already have overwritten it with its new value in the same step. The result then depends on scheduling. Fix it with double buffering (as in the code), or by reading into a register, `__syncthreads()`, then writing, then `__syncthreads()` again.

**Q3.** Explain decoupled look-back and why it needs a dynamic tile ID.

Each tile publishes its local aggregate early, then walks backwards summing predecessors' aggregates until it reaches one that has published its inclusive prefix. Most tiles therefore find a prefix within a few steps, without waiting for a full serial chain. A dynamic tile ID (an atomic counter at block start) guarantees that every predecessor of a tile has already been scheduled, so spinning on it cannot deadlock. GPUs do not guarantee that a block with a lower `blockIdx` is scheduled earlier or concurrently.

**Q4.** What is the minimum memory traffic for a scan, and how do the algorithms compare?

The minimum is 2n (read and write once). Single-pass chained scan achieves it. Reduce-then-scan uses 3n (it reads the input twice). Scan-then-propagate (scan tiles and write them, scan the sums, then add the offsets in place) uses 4n. That makes single-pass 33-50% less traffic in theory. In practice, synchronization latency can eat that advantage, as the MI350X measurement shows.

**Q5.** Where do scans appear in real systems?

Stream compaction and filtering (scan of keep-flags gives output indices), radix sort (scan of digit histograms), sparse matrix construction (CSR row pointers are an exclusive scan of row counts), memory allocation for variable-size outputs, MoE token routing (offsets per expert), and cumulative sums in sampling (top-p).

---

# 4. Histogram

## 4.1 Problem and Why It Is Different

Count 256 bins over 1 GiB of bytes. Reads are perfectly regular, but the **writes are data-dependent**: many threads update the same few counters. The arithmetic is trivial (one increment per byte), so the target is the read ceiling, 5.3-5.6 TB/s. The obstacle is **atomic contention and atomic throughput**, and both depend on the *data distribution*. Every variant is therefore measured on two datasets: uniform random bytes (best case) and all bytes equal (worst case, every update to one bin).

## 4.2 Code: Global Atomics, LDS Privatization, Aggregation

```cpp
// fragment: histogram.hip part 1 of 2 -- concatenate parts 1-2 in order to build
// histogram.hip -- 256-bin histogram of bytes
// Build: hipcc -O3 --offload-arch=gfx942 histogram.hip -o histogram
#include "common.hpp"
#include <algorithm>
#include <cstring>
#include <random>
#include <vector>

constexpr int BINS = 256, BLOCK = 256;

// H1: one global atomic per byte. All CUs hammer 256 addresses in L2.
__global__ void hist_global(const uchar4* __restrict__ in4, int n4, unsigned* hist) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n4; i += gridDim.x * blockDim.x) {
    uchar4 q = in4[i];
    atomicAdd(&hist[q.x], 1u); atomicAdd(&hist[q.y], 1u);
    atomicAdd(&hist[q.z], 1u); atomicAdd(&hist[q.w], 1u);
  }
}

// H2: privatization: per-block histogram in LDS (ds_add_u32 atomics),
// then one global atomic per non-zero bin per block. COPIES > 1 gives each
// wave its own sub-histogram to cut same-address contention inside the block.
template <int COPIES>
__global__ void hist_lds(const uchar4* __restrict__ in4, int n4, unsigned* hist) {
  __shared__ unsigned local[COPIES][BINS];
  for (int b = threadIdx.x; b < COPIES * BINS; b += blockDim.x) (&local[0][0])[b] = 0;
  __syncthreads();
  unsigned* mine = local[(threadIdx.x / kWave) % COPIES];
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n4; i += gridDim.x * blockDim.x) {
    uchar4 q = in4[i];
    atomicAdd(&mine[q.x], 1u); atomicAdd(&mine[q.y], 1u);
    atomicAdd(&mine[q.z], 1u); atomicAdd(&mine[q.w], 1u);
  }
  __syncthreads();
  for (int b = threadIdx.x; b < BINS; b += blockDim.x) {
    unsigned v = 0;
    for (int c = 0; c < COPIES; ++c) v += local[c][b];
    if (v) atomicAdd(&hist[b], v);
  }
}

// H3: privatization + aggregation: each thread accumulates runs of the same
// bin in a register and issues one LDS atomic per run (PMPP-style).
// Wins on data with long runs (images, sorted keys); slight loss on random data.
__global__ void hist_lds_aggregate(const uchar4* __restrict__ in4, int n4, unsigned* hist) {
  __shared__ unsigned local[BINS];
  for (int b = threadIdx.x; b < BINS; b += blockDim.x) local[b] = 0;
  __syncthreads();
  int prev = -1;
  unsigned run = 0;
  auto add = [&](int bin) {
    if (bin == prev) { ++run; return; }
    if (run) atomicAdd(&local[prev], run);
    prev = bin; run = 1;
  };
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n4; i += gridDim.x * blockDim.x) {
    uchar4 q = in4[i];
    add(q.x); add(q.y); add(q.z); add(q.w);
  }
  if (run) atomicAdd(&local[prev], run);
  __syncthreads();
  for (int b = threadIdx.x; b < BINS; b += blockDim.x)
    if (local[b]) atomicAdd(&hist[b], local[b]);
}

// H4: wave-aggregated atomics: lanes with the same bin elect a leader that adds
// popcount(peers). On AMD __match_any is a software loop (one iteration per
// distinct value in the wave), so this only pays off when values repeat a lot.
__global__ void hist_wave_aggregate(const uchar4* __restrict__ in4, int n4, unsigned* hist) {
  __shared__ unsigned local[BINS];
  for (int b = threadIdx.x; b < BINS; b += blockDim.x) local[b] = 0;
  __syncthreads();
  const int lane = threadIdx.x % kWave;
  for (int base = blockIdx.x * blockDim.x; base < n4; base += gridDim.x * blockDim.x) {
    int i = base + threadIdx.x;  // loop bound depends only on base: waves stay converged
    uchar4 q = (i < n4) ? in4[i] : make_uchar4(0, 0, 0, 0);
    unsigned char vals[4] = {q.x, q.y, q.z, q.w};
    for (int k = 0; k < 4; ++k) {
      int bin = (i < n4) ? vals[k] : -1;   // -1 = padding lane
      unsigned long long peers = __match_any(bin);
      int leader = __ffsll(static_cast<long long>(peers)) - 1;  // lowest lane with this bin
      if (lane == leader && bin >= 0) atomicAdd(&local[bin], (unsigned)__popcll(peers));
    }
  }
  __syncthreads();
  for (int b = threadIdx.x; b < BINS; b += blockDim.x)
    if (local[b]) atomicAdd(&hist[b], local[b]);
}
```

```cpp
// fragment: histogram.hip part 2 of 2 -- concatenate parts 1-2 in order to build
int main() {
  const int n = 1 << 30, n4 = n / 4;  // 1 GiB of bytes
  std::vector<unsigned char> h(n);
  std::mt19937 rng(42);
  for (int i = 0; i < n; i += 4) {
    unsigned r = rng();
    std::memcpy(&h[i], &r, 4);
  }
  unsigned char* d_in;
  unsigned* d_hist;
  HIP_CHECK(hipMalloc(&d_in, n));
  HIP_CHECK(hipMalloc(&d_hist, BINS * sizeof(unsigned)));
  auto in4 = reinterpret_cast<const uchar4*>(d_in);
  const int grid = num_cus() * 8;

  for (int dataset = 0; dataset < 2; ++dataset) {
    if (dataset == 1) std::fill(h.begin(), h.end(), 7);  // worst case: every byte in one bin
    HIP_CHECK(hipMemcpy(d_in, h.data(), n, hipMemcpyHostToDevice));
    std::vector<unsigned> ref(BINS, 0), got(BINS);
    for (int i = 0; i < n; ++i) ++ref[h[i]];
    std::printf("dataset: %s\n", dataset == 0 ? "uniform random bytes" : "all bytes equal");
    auto run = [&](const char* name, auto kernel, int iters = 5) {
      float ms = time_ms([&] {
        HIP_CHECK(hipMemsetAsync(d_hist, 0, BINS * sizeof(unsigned)));
        kernel<<<grid, BLOCK>>>(in4, n4, d_hist);
      }, iters);
      HIP_CHECK(hipMemcpy(got.data(), d_hist, BINS * sizeof(unsigned), hipMemcpyDeviceToHost));
      std::printf("  %-30s %8.3f ms %8.1f GB/s %s\n", name, ms, gbps(n, ms), got == ref ? "OK" : "WRONG");
    };
    run("H1 global atomics", hist_global, 1);  // seconds per run on the skewed data
    run("H2 LDS private, 1 copy", hist_lds<1>);
    run("H2 LDS private, 1 copy/wave", hist_lds<BLOCK / kWave>);
    run("H3 LDS + run aggregation", hist_lds_aggregate);
    run("H4 LDS + wave match_any", hist_wave_aggregate);
  }
  HIP_CHECK(hipFree(d_in));
  HIP_CHECK(hipFree(d_hist));
  return 0;
}
```

## 4.3 Why Each Step Helps

**H1: global atomics.** Every byte becomes one `global_atomic_add` to one of 256 addresses. On our MI350X this ran at **2.2 GB/s (uniform) and 0.09 GB/s (all equal)**, more than 1000x below the read ceiling. The counters show where the atomics went: on a smaller run, **`TCC_EA0_ATOMIC_sum` equalled `TCC_ATOMIC_sum`** (6.49M each) and the L2 hit count was close to zero. Every atomic that reached L2 was forwarded past it to the memory side, so each one paid a fabric round trip, and same-address atomics serialized there. That is consistent with how a multi-XCD GPU keeps device-wide atomics coherent across 8 separate L2s. On single-die GPUs, L2 atomics are much faster, but H1 is still the slowest variant there too. **Lesson: on MI300-class parts, high-rate global atomics to a few addresses are a disaster. Always privatize.**

**H2: LDS privatization.** Each block keeps its own 256-bin histogram in LDS (`ds_add_u32`, executed inside the CU's LDS) and merges into global memory with at most 256 atomics per block at the end, which is 512K global atomics instead of 1G. Uniform data: **2.77 TB/s, about 50% of the read ceiling**. The remaining limit is LDS atomic throughput: 4 LDS atomics per 4-byte load, with random bins colliding on banks. Skewed data: **190-280 GB/s**. When all 64 lanes of a `ds_add_u32` target the *same address*, the LDS applies the 64 updates one after another.

**H2 with one copy per wave** spreads waves across 4 sub-histograms. It did *not* help on the skewed data (3.83 ms vs 3.84-5.7 ms across runs), because the contention is **inside one instruction** (64 lanes, one address), not between waves. Replication only helps if it separates the lanes that collide, for example a copy per lane group indexed by `lane % R`, at R times the LDS.

**H3: aggregation (run-length in registers).** Each thread remembers the last bin it saw and a run count, and issues one atomic per *run*, not per element. On skewed data this is **10-14x faster than H2 (2.7 TB/s, about 50% of the ceiling)** because the atomics nearly disappear. On uniform data it costs about 12% (extra compares and branches). Real data such as images, sorted keys, or sensor streams has long runs, which is why PMPP (Kirk and Hwu) teaches privatization + coarsening + aggregation as a set.

**H4: wave-aggregated atomics with `__match_any`.** The lanes holding the same bin elect a leader, and the leader adds `popcount(peers)`. On NVIDIA, `__match_any_sync` is a hardware instruction. **On AMD it is a software loop** (in `amd_warp_sync_functions.h`: `readfirstlane` the candidate value, ballot the matches, repeat), one iteration per *distinct* value in the wave. With 256 random bins, 64 lanes hold about 57 distinct values on average (`256 x (1 - (255/256)^64)`), so H4 is 100x slower on uniform data (25-28 GB/s), and only 0.78 TB/s on skewed data. **Know your platform's intrinsics: the same source code has a very different cost model.**

## 4.4 Results

Measured on MI350X (1 GiB of bytes, 256 bins; read ceiling 5.3-5.6 TB/s):

| Variant | Uniform: ms | Uniform: GB/s | All-equal: ms | All-equal: GB/s |
|---|---|---|---|---|
| H1 global atomics | 491-507 | 2.2 | 12,200 | 0.09 |
| H2 LDS private, 1 copy | 0.386 | 2,780 | 3.8-5.7 | 190-280 |
| H2 LDS private, 1 copy per wave | 0.392 | 2,740 | 3.83 | 280 |
| H3 LDS + run aggregation | 0.437 | 2,455 | 0.40 | 2,700 |
| H4 LDS + `__match_any` | 38-42 | 25-28 | 1.37 | 782 |

Design notes:

- **Many bins** (say 64K) do not fit one LDS copy per block. Options: privatize a *range* of bins per block and loop over ranges, use 16-bit or 8-bit LDS counters with periodic flushing, or **sort then run-length encode** (rocPRIM's `run_length_encode`), which turns contention into a streaming problem.
- **Adaptive kernels** sample the input and choose aggregation when the data is skewed. Libraries such as hipCUB's `DeviceHistogram` handle the common cases.
- For **floating-point histograms** (binning by value), compute the bin with `min(int((x - lo) * inv_width), bins - 1)`. Watch for NaN and inf inputs: casting NaN to int is undefined behaviour in C++.

## 4.5 Interview Questions

**Q1.** Why is privatization the first optimization for histograms?

It moves contention from a scarce, long-latency resource (global atomics at L2 or beyond, shared by every CU) to a fast, local one (LDS atomics inside each CU, shared by one block), and reduces global atomics by a factor of `elements per block / bins`. Here that is 1G updates down to 512K global atomics, with a 1000x speedup.

**Q2.** Your privatized histogram is fast on random data but 15x slower on real images. Why, and what do you do?

Real images have large uniform regions, so many lanes in one instruction hit the same bin, and same-address LDS atomics serialize within the instruction. Fixes: aggregation (count runs in registers before issuing an atomic), wave-level aggregation (cheap on NVIDIA with hardware `match_any`; on AMD only when few distinct values are expected), replication indexed by lane (`lane % R`) so colliding lanes land in different copies, or sort-based approaches.

**Q3.** What does `TCC_EA0_ATOMIC_sum == TCC_ATOMIC_sum` tell you?

Every atomic that reached L2 was forwarded to the memory side (the "EA" interface to the fabric) rather than being completed in L2. Atomic throughput is then bounded by fabric round trips and memory-side serialization. The fix is algorithmic: perform fewer global atomics by privatizing or aggregating, not by tuning launch parameters.

**Q4.** Is the global result deterministic?

For integer counts, yes. Integer addition is associative, so the order of atomics does not matter. For floating-point accumulation (for example a weighted histogram) it is not deterministic. Use a fixed-order reduction of the per-block histograms (write them out, then reduce) if you need bit-reproducibility.

---

# 5. Softmax and LayerNorm

## 5.1 The Math

**Numerically stable softmax.** `softmax(x)_j = exp(x_j - m) / sum_k exp(x_k - m)` with `m = max_k x_k`. Subtracting the max does not change the result (the factor `e^(-m)` cancels) and guarantees every exponent is <= 0, so nothing overflows. The test data here goes up to 100, and `expf(100) = 2.7e43` overflows FP32 (max about 3.4e38), so the naive formula returns `inf/inf = NaN`.

**Online softmax** (Milakov and Gimelshein, 2018; the core of FlashAttention) computes `m` and the denominator `l` in **one pass**:

```text
m_0 = -inf, l_0 = 0
for each x_j:   m_j = max(m_{j-1}, x_j)
                l_j = l_{j-1} * exp(m_{j-1} - m_j) + exp(x_j - m_j)      # rescale old sum to the new max
merge two partial states (m_a, l_a), (m_b, l_b):
                m = max(m_a, m_b)
                l = l_a * exp(m_a - m) + l_b * exp(m_b - m)
```

The merge is associative and commutative, so the state can be reduced across lanes, waves, blocks, or even GPUs, exactly like a sum. FlashAttention adds a third component: the output accumulator `O` is rescaled the same way, `O = O_a e^(m_a - m) + O_b e^(m_b - m)`.

**LayerNorm.** `y = (x - mean) * rsqrt(var + eps) * gamma + beta`, with the biased variance `var = mean((x - mean)^2)` as in PyTorch. Do **not** compute `var = E[x^2] - E[x]^2` in FP32. For `x` around 1e4 with standard deviation 1, `E[x^2]` is about 1e8, and FP32's 24-bit mantissa leaves an absolute error of about 6 in a quantity whose true value is 1. That is catastrophic cancellation. Either keep the row in registers and do two passes over registers (as in the code), or use **Welford** with the Chan merge when streaming:

```text
per element:  n += 1;  d = x - mean;  mean += d / n;  M2 += d * (x - mean)
merge (a, b): n = n_a + n_b;  d = mean_b - mean_a
              mean = mean_a + d * n_b / n;   M2 = M2_a + M2_b + d^2 * n_a * n_b / n
variance = M2 / n
```

RMSNorm (LLaMA-style) drops the mean: `y = x * rsqrt(mean(x^2) + eps) * gamma`. It has one reduction instead of two, and no cancellation issue.

## 5.2 Roofline Position

Per element, softmax does roughly a max, a subtract, an exp, an add, and a multiply. That is about 5-10 operations (`__expf` lowers to `v_exp_f32` plus a multiply; transcendentals run at a reduced rate) per 8 bytes (read x, write y). The AI is about 1 op/B, 20-30x below the ridge point. **Softmax and LayerNorm are memory-bound**, so the target is copy bandwidth with **one read and one write per element**. Each extra pass over HBM costs directly in time.

## 5.3 Code: From Thread-per-Row to Wave-per-Row in Registers

```cpp
// fragment: softmax_layernorm.hip part 1 of 4 -- concatenate parts 1-4 in order to build
// softmax_layernorm.hip -- row-wise softmax and LayerNorm over an M x N matrix
// Build: hipcc -O3 --offload-arch=gfx942 softmax_layernorm.hip -o softmax_layernorm
#include "common.hpp"
#include <cmath>
#include <vector>

// ---------- wave reductions (64 lanes on CDNA) ----------
__device__ __forceinline__ float wave_max(float v) {
  for (int o = kWave / 2; o > 0; o >>= 1) v = fmaxf(v, __shfl_xor(v, o, kWave));
  return v;  // butterfly (xor): every lane gets the result
}
__device__ __forceinline__ float wave_sum(float v) {
  for (int o = kWave / 2; o > 0; o >>= 1) v += __shfl_xor(v, o, kWave);
  return v;
}

// SM1 naive: one THREAD per row, three passes. Adjacent lanes are N floats apart:
// every load of a wave touches 64 different cache lines (uncoalesced).
__global__ void softmax_thread_per_row(const float* x, float* y, int M, int N) {
  int r = blockIdx.x * blockDim.x + threadIdx.x;
  if (r >= M) return;
  const float* row = x + (size_t)r * N;
  float m = -INFINITY, s = 0.f;
  for (int j = 0; j < N; ++j) m = fmaxf(m, row[j]);
  for (int j = 0; j < N; ++j) s += __expf(row[j] - m);
  for (int j = 0; j < N; ++j) y[(size_t)r * N + j] = __expf(row[j] - m) / s;
}

// SM2: one WAVE per row, online softmax: a single read pass keeps a running
// (max m, sum l) per lane; when the max grows, rescale l by exp(m_old - m_new).
// Lanes then merge their (m, l) pairs. A second pass re-reads x (often from L2)
// and writes y. Works for any N.
__global__ void softmax_wave_online(const float* __restrict__ x, float* __restrict__ y, int M, int N) {
  int wave = (blockIdx.x * blockDim.x + threadIdx.x) / kWave;
  int lane = threadIdx.x % kWave;
  if (wave >= M) return;  // wave-uniform exit
  const float* row = x + (size_t)wave * N;
  float m = -INFINITY, l = 0.f;
  for (int j = lane; j < N; j += kWave) {
    float v = row[j];
    float m_new = fmaxf(m, v);
    l = l * __expf(m - m_new) + __expf(v - m_new);  // exp(-inf) = 0 handles the first step
    m = m_new;
  }
  // merge (m, l) across lanes: l_total = sum_i l_i * exp(m_i - M)
  float M_row = wave_max(m);
  float L_row = wave_sum(l * __expf(m - M_row));
  float inv = 1.f / L_row;
  for (int j = lane; j < N; j += kWave)
    y[(size_t)wave * N + j] = __expf(row[j] - M_row) * inv;
}
```

```cpp
// fragment: softmax_layernorm.hip part 2 of 4 -- concatenate parts 1-4 in order to build
// SM3: one WAVE per row, the row lives in registers (N known at compile time).
// Exactly one read and one write of every element = the memory-bound optimum.
template <int N>
__global__ void softmax_wave_regs(const float* __restrict__ x, float* __restrict__ y, int M) {
  static_assert(N % (4 * kWave) == 0, "N must be a multiple of 4 * wave size");
  constexpr int V = N / (4 * kWave);  // float4 chunks per lane (N=4096 -> 16 -> 64 VGPRs)
  int wave = (blockIdx.x * blockDim.x + threadIdx.x) / kWave;
  int lane = threadIdx.x % kWave;
  if (wave >= M) return;
  const float4* row = reinterpret_cast<const float4*>(x + (size_t)wave * N);
  float4 v[V];
  float m = -INFINITY;
#pragma unroll
  for (int k = 0; k < V; ++k) {  // chunk k of lane = float4 index lane + k*64: coalesced
    v[k] = row[lane + k * kWave];
    m = fmaxf(m, fmaxf(fmaxf(v[k].x, v[k].y), fmaxf(v[k].z, v[k].w)));
  }
  m = wave_max(m);
  float s = 0.f;
#pragma unroll
  for (int k = 0; k < V; ++k) {
    v[k].x = __expf(v[k].x - m); v[k].y = __expf(v[k].y - m);
    v[k].z = __expf(v[k].z - m); v[k].w = __expf(v[k].w - m);
    s += (v[k].x + v[k].y) + (v[k].z + v[k].w);
  }
  float inv = 1.f / wave_sum(s);
  float4* out = reinterpret_cast<float4*>(y + (size_t)wave * N);
#pragma unroll
  for (int k = 0; k < V; ++k)
    out[lane + k * kWave] = make_float4(v[k].x * inv, v[k].y * inv, v[k].z * inv, v[k].w * inv);
}
```

```cpp
// fragment: softmax_layernorm.hip part 3 of 4 -- concatenate parts 1-4 in order to build
// LN: one WAVE per row, row in registers. Two-step variance (mean first, then
// sum of squared deviations) is free because the data is already in registers
// and avoids the catastrophic cancellation of E[x^2] - E[x]^2.
template <int N>
__global__ void layernorm_wave_regs(const float* __restrict__ x, const float* __restrict__ gamma,
                                    const float* __restrict__ beta, float* __restrict__ y,
                                    int M, float eps) {
  constexpr int V = N / (4 * kWave);
  int wave = (blockIdx.x * blockDim.x + threadIdx.x) / kWave;
  int lane = threadIdx.x % kWave;
  if (wave >= M) return;
  const float4* row = reinterpret_cast<const float4*>(x + (size_t)wave * N);
  float4 v[V];
  float s = 0.f;
#pragma unroll
  for (int k = 0; k < V; ++k) {
    v[k] = row[lane + k * kWave];
    s += (v[k].x + v[k].y) + (v[k].z + v[k].w);
  }
  const float mean = wave_sum(s) / N;
  float ss = 0.f;
#pragma unroll
  for (int k = 0; k < V; ++k) {
    float a = v[k].x - mean, b = v[k].y - mean, c = v[k].z - mean, d = v[k].w - mean;
    ss += (a * a + b * b) + (c * c + d * d);
  }
  const float rstd = rsqrtf(wave_sum(ss) / N + eps);  // biased variance, as in PyTorch
  const float4* g4 = reinterpret_cast<const float4*>(gamma);
  const float4* b4 = reinterpret_cast<const float4*>(beta);
  float4* out = reinterpret_cast<float4*>(y + (size_t)wave * N);
#pragma unroll
  for (int k = 0; k < V; ++k) {
    float4 g = g4[lane + k * kWave], b = b4[lane + k * kWave];  // tiny, stays in cache
    out[lane + k * kWave] = make_float4((v[k].x - mean) * rstd * g.x + b.x, (v[k].y - mean) * rstd * g.y + b.y,
                                        (v[k].z - mean) * rstd * g.z + b.z, (v[k].w - mean) * rstd * g.w + b.w);
  }
}
```

```cpp
// fragment: softmax_layernorm.hip part 4 of 4 -- concatenate parts 1-4 in order to build
int main() {
  constexpr int N = 4096;
  const int M = 32768;  // 512 MiB in, 512 MiB out
  const size_t total = (size_t)M * N;
  std::vector<float> h(total), out(total), g(N), b(N);
  for (size_t i = 0; i < total; ++i) h[i] = 20.f * std::sin(0.001f * float(i % 100003)) + 80.f;  // up to 100: expf(100) overflows fp32
  for (int j = 0; j < N; ++j) { g[j] = 1.f + 0.001f * j; b[j] = 0.01f * (j % 7); }
  float *dx, *dy, *dg, *db;
  HIP_CHECK(hipMalloc(&dx, total * sizeof(float)));
  HIP_CHECK(hipMalloc(&dy, total * sizeof(float)));
  HIP_CHECK(hipMalloc(&dg, N * sizeof(float)));
  HIP_CHECK(hipMalloc(&db, N * sizeof(float)));
  HIP_CHECK(hipMemcpy(dx, h.data(), total * sizeof(float), hipMemcpyHostToDevice));
  HIP_CHECK(hipMemcpy(dg, g.data(), N * sizeof(float), hipMemcpyHostToDevice));
  HIP_CHECK(hipMemcpy(db, b.data(), N * sizeof(float), hipMemcpyHostToDevice));

  const double bytes = 2.0 * total * sizeof(float);
  auto check_softmax = [&](const char* name, float ms) {
    HIP_CHECK(hipMemcpy(out.data(), dy, total * sizeof(float), hipMemcpyDeviceToHost));
    double max_err = 0;
    for (int r = 0; r < M; r += 4099) {  // spot-check rows against a double reference
      const float* xr = &h[(size_t)r * N];
      double m = -1e300, s = 0;
      for (int j = 0; j < N; ++j) m = std::fmax(m, xr[j]);
      for (int j = 0; j < N; ++j) s += std::exp(xr[j] - m);
      for (int j = 0; j < N; ++j)
        max_err = std::fmax(max_err, std::fabs(out[(size_t)r * N + j] - std::exp(xr[j] - m) / s) * N);
    }
    std::printf("%-28s %7.3f ms %8.1f GB/s  max err*N %.1e\n", name, ms, gbps(bytes, ms), max_err);
  };
  const int wpb = 256 / kWave;  // waves (rows) per 256-thread block
  check_softmax("SM1 thread per row", time_ms([&] { softmax_thread_per_row<<<(M + 255) / 256, 256>>>(dx, dy, M, N); }, 3));
  check_softmax("SM2 wave per row, online", time_ms([&] { softmax_wave_online<<<(M + wpb - 1) / wpb, 256>>>(dx, dy, M, N); }));
  check_softmax("SM3 wave per row, in regs", time_ms([&] { softmax_wave_regs<N><<<(M + wpb - 1) / wpb, 256>>>(dx, dy, M); }));

  float ms = time_ms([&] { layernorm_wave_regs<N><<<(M + wpb - 1) / wpb, 256>>>(dx, dg, db, dy, M, 1e-5f); });
  HIP_CHECK(hipMemcpy(out.data(), dy, total * sizeof(float), hipMemcpyDeviceToHost));
  double max_err = 0;
  for (int r = 0; r < M; r += 4099) {
    const float* xr = &h[(size_t)r * N];
    double mean = 0, var = 0;
    for (int j = 0; j < N; ++j) mean += xr[j];
    mean /= N;
    for (int j = 0; j < N; ++j) var += (xr[j] - mean) * (xr[j] - mean);
    double rstd = 1.0 / std::sqrt(var / N + 1e-5);
    for (int j = 0; j < N; ++j)
      max_err = std::fmax(max_err, std::fabs(out[(size_t)r * N + j] - ((xr[j] - mean) * rstd * g[j] + b[j])));
  }
  std::printf("%-28s %7.3f ms %8.1f GB/s  max abs err %.1e\n", "LN wave per row, in regs", ms, gbps(bytes, ms), max_err);
  HIP_CHECK(hipFree(dx)); HIP_CHECK(hipFree(dy)); HIP_CHECK(hipFree(dg)); HIP_CHECK(hipFree(db));
  return 0;
}
```

## 5.4 Why Each Step Helps

**SM1: thread per row.** Lane `r` reads row `r`, so the 64 lanes of a wave read addresses `N x 4 = 16 KB` apart, and every load instruction touches 64 cache lines (vL1D Coalescing near its minimum). It also makes three passes over the row, and the sequential sum of 4096 terms has visibly larger rounding error. Result: **390 GB/s, under 10% of copy**.

**SM2: one wave per row, online softmax.** Lanes now read consecutive elements (perfectly coalesced), and the max and sum come from **one read pass** using the `(m, l)` recurrence, merged across lanes with `__shfl_xor` butterflies (every lane ends with the result, so no broadcast is needed). It still reads `x` a second time to write `y`, which makes traffic 1.5x the ideal. Result: **2.56 TB/s**. This version works for any `N`.

**SM3: one wave per row, row in registers.** With `N` known at compile time (4096), each lane holds `4096 / 64 = 64` floats in 16 `float4` registers. The kernel reads the row once (16 independent `global_load_dwordx4` per lane in flight, which gives high memory-level parallelism), reduces the max, exponentiates in place, reduces the sum, scales, and writes once. Traffic equals the minimum. Result: **4.55 TB/s, at the copy ceiling**. With 100 VGPRs the occupancy is 4 waves/SIMD, which is enough. The 16 outstanding 16-byte loads per lane supply the bytes in flight that Little's law requires, so lower occupancy costs nothing here.

**Why not one block per row?** For `N <= ~8K` a wave per row avoids **all** LDS traffic and barriers: reductions are 6 shuffle steps, and there is no `__syncthreads`. Block-per-row adds LDS round trips and barriers for no gain. It becomes the right choice when the row no longer fits in one wave's registers.

**LN.** The same structure: mean via a wave sum, then the variance from **registers** (squared deviations from the mean, which is numerically safe and costs no extra memory traffic), then the affine transform. `gamma` and `beta` are 16 KB each and stay in cache. Result: **4.57 TB/s**.

| Row length `N` | Mapping | Why |
|---|---|---|
| <= 128 | Several rows per wave (`__shfl_xor(v, o, width)` with `width` = 16 or 32) | Otherwise most lanes idle |
| 256 to ~8K | One wave per row, row in registers (SM3 / LN) | One read, one write; no LDS, no barriers |
| ~8K to ~64K | One block per row, wave partials combined via LDS | The row exceeds the register budget (8K floats = 128 VGPRs per lane) |
| Larger, or a few huge rows | Split a row over several blocks; merge `(m, l)` or Welford states in a second tiny pass | Not enough rows to fill the GPU |

## 5.5 Results

Measured on MI350X (32,768 x 4,096 FP32; bytes counted = read + write = 1.07 GB; copy ceiling 4.0-4.7 TB/s):

| Variant | Time (ms) | GB/s | VGPRs / waves per SIMD | Notes |
|---|---|---|---|---|
| SM1 thread per row | 2.75-2.81 | 382-391 | 13 / 8 | Uncoalesced, 3 passes |
| SM2 wave per row, online | 0.417-0.419 | 2,560-2,580 | 14 / 8 | 2 reads + 1 write |
| SM3 wave per row, in registers | 0.236-0.238 | 4,515-4,550 | 100 / 4 | 1 read + 1 write |
| LN wave per row, in registers | 0.234-0.235 | 4,570-4,590 | 108 / 4 | Two-pass variance in registers |

All variants agree with a double-precision reference to `|err| x N < 2e-4` (softmax) and `|err| < 4e-6` (LayerNorm).

## 5.6 Interview Questions

**Q1.** Why subtract the max in softmax, and what happens to fully masked rows?

`exp` overflows FP32 above about 88.7, so `exp(x_j)` for large logits gives `inf/inf = NaN`. Subtracting the row max makes every exponent <= 0 without changing the result. For a fully masked row (all `-inf`), `m = -inf` and `x - m = -inf - (-inf) = NaN`. Production kernels special-case `m == -inf` (use 0 as the reference, or output zeros) and document what a fully masked row returns.

**Q2.** Derive the online softmax update and explain why it enables FlashAttention.

Keep the running max `m` and the running denominator `l` relative to `m`. When a new element raises the max to `m'`, the old denominator was computed relative to the old max, so multiply it by `e^(m - m')` before adding `e^(x - m')`. Two partial states merge the same way, so the computation is a parallel reduction. In attention, the full row of scores `QK^T` is never materialized: each tile of keys updates `(m, l, O)` and is discarded, so the `N x N` score matrix never goes to HBM. That changes attention from memory-bound on the score matrix to compute-bound on the two GEMMs.

**Q3.** Why does SM3 reach the copy ceiling with only 4 waves per SIMD?

Bandwidth needs enough bytes in flight (Little's law: bytes in flight = bandwidth x latency). Each lane issues 16 independent 16-byte loads before it needs any of them, so each wave has 16 KB in flight. Across 16 waves per CU and 256 CUs, that is far more than `8 TB/s x ~1 us` of latency needs. Occupancy is one way to get memory-level parallelism. Independent loads per thread (ILP) are another, and here they are enough.

**Q4.** How would you implement LayerNorm for `N = 64K` with only 512 rows?

512 rows cannot fill a 256-304 CU GPU with one wave per row (that is 512 waves against 8K+ wave slots), and a row is too big for registers. Split each row across several blocks. Each block computes Welford `(n, mean, M2)` for its chunk. Merge the chunk states with the Chan formula (a second tiny kernel, or a last-block-done pattern), then normalize in a final pass. The cost is 2 reads + 1 write, or a cooperative launch with a grid barrier and 1 read + 1 write if the chunk stays in registers.

**Q5.** Why is `E[x^2] - E[x]^2` dangerous, and when is it acceptable?

It subtracts two large, nearly equal numbers when the mean is large relative to the standard deviation, so the leading digits cancel and only rounding error remains. It can even produce a negative variance, which makes `rsqrt` return NaN. It is acceptable with FP64 accumulation, or when inputs are known to be roughly zero-mean (as after a previous normalization). Clamping `var` to >= 0 is a common guard, but the two-pass or Welford form is the correct fix.

> **See also:** [ML and AI Frameworks -- Flash Attention in Triton](../ml-gpu/ML_AI_Frameworks.md#272-flash-attention-in-triton); [LLM and ML Fundamentals](../ml-gpu/LLM_and_ML_Fundamentals.md) for why normalization layers exist; [Performance Engineering -- Floating-Point Numerics and Reproducibility](../computer-science/Performance_Engineering.md#9-floating-point-numerics-and-reproducibility).

---

# 6. Tiled GEMM Progression

## 6.1 Problem and Arithmetic Intensity at Each Level

`C = A x B`, row-major, `M = N = K = 4096`, FP32 (then FP16 on matrix cores). FLOPs = `2MNK = 137.4 GFLOP`. The compulsory traffic is A + B + C = 3 x 64 MiB, so the **ideal HBM AI is `2n^3 / (12 n^2) = n/6 = 683 FLOP/B`**, far right of every ridge point. A well-written GEMM is compute-bound. Every step of this ladder raises the AI at *some* level of the memory hierarchy until compute becomes the limit.

| Level of reuse | Per-step traffic | AI at that level (FP32) |
|---|---|---|
| None (each FMA loads its A and B element) | 8 B per FMA | 0.25 FLOP/B |
| `T x T` LDS tile, 1 output per thread | Global: `2 T^2` floats per `T^3` FMAs | Global: `T/4` = 8 FLOP/B for T=32 |
| `BM x BN` block tile in LDS + `TM x TN` thread tile in registers | Global: `(BM + BN) x BK` per `BM x BN x BK` FMAs; LDS: `TM + TN` floats per `TM x TN` FMAs | Global: `BM BN / (2(BM + BN))` = 32 FLOP/B at 128x128; LDS: `TM TN / (2(TM + TN))` = **2 FLOP/B** at 8x8 (vs 0.25) |
| MFMA 16x16x16 per wave | Registers feed 8,192 FLOPs per instruction | Limited by how often fragments are reloaded |

The last column of the table is the key interview insight. **Tiling is how you move a kernel to the right on the roofline**: LDS tiles raise the global-memory AI, register tiles raise the LDS AI, and MFMA raises FLOPs per register byte.

## 6.2 G1 Naive and G2 LDS Tiling

```cpp
// fragment: gemm.hip part 1 of 6 -- concatenate parts 1-6 in order to build
// gemm.hip -- C = A * B, row-major, A: M x K, B: K x N, C: M x N
// Build: hipcc -O3 --offload-arch=gfx942 gemm.hip -o gemm -lhipblas
#include "common.hpp"
#include <hipblas/hipblas.h>
#include <rocwmma/rocwmma.hpp>
#include <cmath>
#include <vector>

// ---------- G1 naive: one thread per C element ----------
__global__ void gemm_naive(const float* A, const float* B, float* C, int M, int N, int K) {
  int col = blockIdx.x * blockDim.x + threadIdx.x;  // consecutive lanes -> consecutive columns
  int row = blockIdx.y * blockDim.y + threadIdx.y;
  if (row >= M || col >= N) return;
  float acc = 0.f;
  for (int k = 0; k < K; ++k) acc += A[(size_t)row * K + k] * B[(size_t)k * N + col];
  C[(size_t)row * N + col] = acc;
}

// ---------- G2 LDS tiling: T x T tiles of A and B staged in LDS ----------
constexpr int T = 32;
__global__ void gemm_lds(const float* A, const float* B, float* C, int M, int N, int K) {
  __shared__ float As[T][T], Bs[T][T];  // unpadded rows keep As[r][k..k+3] 16-byte aligned
  int tx = threadIdx.x, ty = threadIdx.y;       // block = 32 x 8 threads, 4 outputs each
  int row0 = blockIdx.y * T, col = blockIdx.x * T + tx;
  float acc[T / 8] = {};
  for (int k0 = 0; k0 < K; k0 += T) {
    for (int r = ty; r < T; r += 8) {             // coalesced loads along rows
      As[r][tx] = A[(size_t)(row0 + r) * K + k0 + tx];
      Bs[r][tx] = B[(size_t)(k0 + r) * N + col];
    }
    __syncthreads();
    for (int k = 0; k < T; ++k) {
      float b = Bs[k][tx];                        // one LDS read reused 4 times
#pragma unroll
      for (int i = 0; i < T / 8; ++i) acc[i] += As[ty + 8 * i][k] * b;  // As read = broadcast
    }
    __syncthreads();
  }
#pragma unroll
  for (int i = 0; i < T / 8; ++i) C[(size_t)(row0 + ty + 8 * i) * N + col] = acc[i];
}
```

**G1** maps consecutive lanes to consecutive columns, so B reads are coalesced and A reads are a broadcast (all lanes of a row read the same element). Each FMA still needs two load *instructions*, so the kernel is bound by the vector-memory pipeline (address processing, L1 bandwidth), not by HBM. Its **measured HBM traffic is 24.7 GB** (`FETCH_SIZE`) for 137 GFLOP, an AI of 5.6 FLOP/B. The L2 and Infinity Cache already capture most of the reuse, yet it reaches only 3.8 TFLOP/s, far below the 45 TFLOP/s HBM roof at that AI. **A kernel far below every roof is issue- or latency-bound.**

**G2** stages 32 x 32 tiles of A and B in LDS. Each thread computes 4 outputs (the block is 32 x 8), so one `Bs[k][tx]` value is reused 4 times. The compiler turns the `As[ty + 8i][k]` reads into `ds_read_b128` along `k`, because the rows are 16-byte aligned. Measured HBM traffic falls to **4.2 GB** (AI 32 FLOP/B) and performance rises 7x to **26.9 TFLOP/s**. Now the bottleneck is LDS bandwidth: about 2.5 FMAs per LDS instruction.

**Padding pitfall (measured):** adding `+1` padding to `As` (the transpose reflex) dropped G2 from 26.9 to **23.3 TFLOP/s**. The odd row length broke the 16-byte alignment, the compiler fell back from `ds_read_b128` to narrower loads, and the bank conflicts that padding would have removed did not exist on this access pattern (the counters showed 0). **Check `SQ_LDS_BANK_CONFLICT` before padding, and check the ISA after.**

## 6.3 G3 Register Blocking and G4 Vectorized Loads

```cpp
// fragment: gemm.hip part 2 of 6 -- concatenate parts 1-6 in order to build
// ---------- G3/G4/G5: register-blocked thread tiles ----------
// Block tile BM x BN, K-slice BK, each of 256 threads owns a TM x TN sub-tile.
constexpr int BM = 128, BN = 128, BK = 8, TM = 8, TN = 8;
constexpr int kThreads = (BM / TM) * (BN / TN);  // 256
static_assert(BM * BK == 4 * kThreads && BN * BK == 4 * kThreads, "one float4 per thread per tile");

// Inner product over one BK slice held in LDS. As is stored transposed (As[k][m])
// so both operands are contiguous along the thread's TM / TN direction.
template <bool VEC>
__device__ __forceinline__ void compute_slice(const float (*As)[BM], const float (*Bs)[BN],
                                              float (&acc)[TM][TN], int tr, int tc) {
#pragma unroll
  for (int k = 0; k < BK; ++k) {
    float a[TM], b[TN];
    if constexpr (VEC) {  // 2 x ds_read_b128 per operand
      *reinterpret_cast<float4*>(&a[0]) = *reinterpret_cast<const float4*>(&As[k][tr * TM]);
      *reinterpret_cast<float4*>(&a[4]) = *reinterpret_cast<const float4*>(&As[k][tr * TM + 4]);
      *reinterpret_cast<float4*>(&b[0]) = *reinterpret_cast<const float4*>(&Bs[k][tc * TN]);
      *reinterpret_cast<float4*>(&b[4]) = *reinterpret_cast<const float4*>(&Bs[k][tc * TN + 4]);
    } else {
#pragma unroll
      for (int i = 0; i < TM; ++i) a[i] = As[k][tr * TM + i];
#pragma unroll
      for (int j = 0; j < TN; ++j) b[j] = Bs[k][tc * TN + j];
    }
#pragma unroll
    for (int i = 0; i < TM; ++i)
#pragma unroll
      for (int j = 0; j < TN; ++j) acc[i][j] += a[i] * b[j];  // 64 FMAs per 16 LDS values
  }
}

// G3 (VEC=false): scalar global and LDS accesses. G4 (VEC=true): float4 everywhere.
template <bool VEC>
__global__ __launch_bounds__(kThreads) void gemm_regblock(const float* A, const float* B, float* C,
                                                          int M, int N, int K) {
  __shared__ float As[BK][BM];  // transposed A slice
  __shared__ float Bs[BK][BN];
  const int t = threadIdx.x, tr = t / (BN / TN), tc = t % (BN / TN);
  const float* Ab = A + (size_t)blockIdx.y * BM * K;
  const float* Bb = B + (size_t)blockIdx.x * BN;
  const int a_row = t / (BK / 4), a_col = (t % (BK / 4)) * 4;  // A tile: 128 rows x 8 cols
  const int b_row = t / (BN / 4), b_col = (t % (BN / 4)) * 4;  // B tile: 8 rows x 128 cols
  float acc[TM][TN] = {};
  for (int k0 = 0; k0 < K; k0 += BK) {
    if constexpr (VEC) {
      float4 a = *reinterpret_cast<const float4*>(&Ab[(size_t)a_row * K + k0 + a_col]);
      As[a_col + 0][a_row] = a.x; As[a_col + 1][a_row] = a.y;
      As[a_col + 2][a_row] = a.z; As[a_col + 3][a_row] = a.w;
      *reinterpret_cast<float4*>(&Bs[b_row][b_col]) =
          *reinterpret_cast<const float4*>(&Bb[(size_t)(k0 + b_row) * N + b_col]);
    } else {
      for (int i = 0; i < 4; ++i) {
        As[a_col + i][a_row] = Ab[(size_t)a_row * K + k0 + a_col + i];
        Bs[b_row][b_col + i] = Bb[(size_t)(k0 + b_row) * N + b_col + i];
      }
    }
    __syncthreads();
    compute_slice<VEC>(As, Bs, acc, tr, tc);
    __syncthreads();
  }
  float* Cb = C + (size_t)(blockIdx.y * BM + tr * TM) * N + blockIdx.x * BN + tc * TN;
#pragma unroll
  for (int i = 0; i < TM; ++i) {
    *reinterpret_cast<float4*>(&Cb[(size_t)i * N]) = make_float4(acc[i][0], acc[i][1], acc[i][2], acc[i][3]);
    *reinterpret_cast<float4*>(&Cb[(size_t)i * N + 4]) = make_float4(acc[i][4], acc[i][5], acc[i][6], acc[i][7]);
  }
}
```

Each of the 256 threads owns an **8 x 8 tile of C in 64 registers**. Per `k`, it reads 8 values of A and 8 of B from LDS (four `ds_read_b128`) and performs 64 FMAs, which raises LDS AI from about 0.4 (G2; 0.25 with one output per thread) to 2 FLOP/B. `As` is stored **transposed** (`As[k][m]`) so that a thread's 8 A values are contiguous and can be loaded as `float4`s. Counter evidence across G2 to G3:

| Kernel | `SQ_INSTS_LDS` | `TCP_TCC_READ_REQ_sum` | `FETCH_SIZE` | HBM AI | TFLOP/s |
|---|---|---|---|---|---|
| G1 naive | 0 | 611M | 24.7 GB | 5.6 | 3.8 |
| G2 LDS 32x32 | 436M | 133M | 4.2 GB | 32 | 26.9 |
| G3 register blocked | **73M** (6x fewer) | 76M | 0.78 GB | 177 | 92.9 |
| G4 + `float4` global loads | 73M | 74M | 0.78 GB | 176 | 98.7 |

Things the ISA shows (`--save-temps`, gfx942):

- The compiler emits **`v_pk_fma_f32`** (packed FP32: 2 FMAs per instruction, 256 per BK slice). That is why G3/G4 exceed the "non-packed" FP32 peak (72.1 TFLOP/s on MI350X) and why AMD quotes 163.4 TFLOP/s FP32 vector for MI300X and 144.2 for MI350X. G4 reaches **68% of the packed peak** on MI350X.
- G3 already had the same `SQ_INSTS_LDS` as G4: the compiler merged the scalar LDS reads into `ds_read_b128` by itself. G4's gain (6%) comes from the **global** `float4` loads (`global_load_dwordx4`).
- `SQ_LDS_BANK_CONFLICT` is 151M cycles, about 2 per LDS instruction. Lanes `tc` and `tc + 8` read `Bs[k][tc*8..]`, 64 words apart, and land in the same banks on 64-bank gfx950 (on 32-bank CDNA3, lanes `tc` and `tc + 4` collide). Swizzling the LDS layout is the next fix (exercise E9).
- The A-tile load (`a_row = t / 2`) reads only 32 contiguous bytes per row. Production kernels use BK = 16-64 so each row segment fills whole cache lines.

## 6.4 G5 Double Buffering (and Why It Lost Here)

```cpp
// fragment: gemm.hip part 3 of 6 -- concatenate parts 1-6 in order to build
// G5: double buffering. Global loads for slice k+1 are issued into registers
// before computing slice k, then written to the other LDS buffer: the global
// latency hides behind 512 FMAs/thread and there is ONE barrier per slice.
__global__ __launch_bounds__(kThreads) void gemm_double_buffer(const float* A, const float* B, float* C,
                                                               int M, int N, int K) {
  __shared__ float As[2][BK][BM];
  __shared__ float Bs[2][BK][BN];
  const int t = threadIdx.x, tr = t / (BN / TN), tc = t % (BN / TN);
  const float* Ab = A + (size_t)blockIdx.y * BM * K;
  const float* Bb = B + (size_t)blockIdx.x * BN;
  const int a_row = t / (BK / 4), a_col = (t % (BK / 4)) * 4;
  const int b_row = t / (BN / 4), b_col = (t % (BN / 4)) * 4;
  auto load = [&](int k0, float4& a, float4& b) {
    a = *reinterpret_cast<const float4*>(&Ab[(size_t)a_row * K + k0 + a_col]);
    b = *reinterpret_cast<const float4*>(&Bb[(size_t)(k0 + b_row) * N + b_col]);
  };
  auto store = [&](int buf, const float4& a, const float4& b) {
    As[buf][a_col + 0][a_row] = a.x; As[buf][a_col + 1][a_row] = a.y;
    As[buf][a_col + 2][a_row] = a.z; As[buf][a_col + 3][a_row] = a.w;
    *reinterpret_cast<float4*>(&Bs[buf][b_row][b_col]) = b;
  };
  float acc[TM][TN] = {};
  float4 ra, rb;
  load(0, ra, rb);
  store(0, ra, rb);
  __syncthreads();
  int buf = 0;
  for (int k0 = 0; k0 < K; k0 += BK) {
    const bool has_next = k0 + BK < K;
    if (has_next) load(k0 + BK, ra, rb);          // in flight during the math below
    compute_slice<true>(As[buf], Bs[buf], acc, tr, tc);
    if (has_next) store(buf ^ 1, ra, rb);         // other buffer: nobody is reading it
    __syncthreads();
    buf ^= 1;
  }
  float* Cb = C + (size_t)(blockIdx.y * BM + tr * TM) * N + blockIdx.x * BN + tc * TN;
#pragma unroll
  for (int i = 0; i < TM; ++i) {
    *reinterpret_cast<float4*>(&Cb[(size_t)i * N]) = make_float4(acc[i][0], acc[i][1], acc[i][2], acc[i][3]);
    *reinterpret_cast<float4*>(&Cb[(size_t)i * N + 4]) = make_float4(acc[i][4], acc[i][5], acc[i][6], acc[i][7]);
  }
}
```

The idea: issue global loads for slice `k+1` into registers, compute slice `k` from LDS, then write the registers into the *other* LDS buffer. Global latency overlaps the math, and there is one barrier per slice instead of two. On NVIDIA (fewer resident warps, `cp.async`) this is a standard, large win. **Here it lost 10%**:

| | G4 | G5 double buffer | G5 + `amdgpu_waves_per_eu(3)` | G5 + `amdgpu_waves_per_eu(4)` |
|---|---|---|---|---|
| VGPRs | 102 | **240** | 168 (+103 spilled) | 128 (+205 spilled) |
| Waves per SIMD | 4 | **2** | 3 | 4 |
| TFLOP/s | 98.7 | 88.5 | 11.2 | 5.2 |

The scheduler hoisted LDS reads to overlap them with the in-flight global loads, and register use more than doubled. That halved occupancy. Forcing occupancy back with `__attribute__((amdgpu_waves_per_eu(N)))` made it **spill to scratch**, which was 8-17x slower. Lessons interviewers like:

1. **AMD hides latency with occupancy or with ILP, that is, enough bytes in flight per wave** (see [Latency Hiding Quantified](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#3-latency-hiding-quantified)). Either route works, but here the extra in-flight loads cost VGPRs, occupancy fell from 4 to 2 waves per SIMD, and the kernel lost more latency hiding than the pipelining gained. Software pipelining that costs registers can be a net loss. Always check `-Rpass-analysis=kernel-resource-usage` and the "VGPRs Spill" line.
2. Production AMD kernels double-buffer without staging through VGPRs, using **direct-to-LDS loads** (`global_load_lds_*` / `buffer_load ... lds`; 32 bits per lane on CDNA3, up to 128 bits on CDNA4), plus explicit scheduling hints. Libraries (hipBLASLt, Composable Kernel) handle this.
3. Never assume an optimization from a CUDA tutorial transfers. Measure it.

## 6.5 G6 Matrix Cores: MFMA Intrinsics and rocWMMA

```cpp
// fragment: gemm.hip part 4 of 6 -- concatenate parts 1-6 in order to build
// ---------- G6a: MFMA intrinsic, one wave per 16x16 C tile (teaching version) ----------
// v_mfma_f32_16x16x16_f16 (CDNA1-CDNA4): D(16x16 fp32) = A(16x16 fp16) * B(16x16 fp16) + C.
// Operand layout per lane l (0..63): A[l%16][4*(l/16)+i], B[4*(l/16)+i][l%16],
// D[4*(l/16)+i][l%16] for i = 0..3. No LDS reuse here, so it is far from peak.
typedef _Float16 half4_t __attribute__((ext_vector_type(4)));
typedef float float4_t __attribute__((ext_vector_type(4)));

__global__ void gemm_mfma_naive(const _Float16* A, const _Float16* B, float* C, int M, int N, int K) {
  const int lane = threadIdx.x % 64;
  const int wave = (blockIdx.x * blockDim.x + threadIdx.x) / 64;
  const int tiles_n = N / 16;
  const int tm = (wave / tiles_n) * 16, tn = (wave % tiles_n) * 16;
  if (tm >= M) return;
  float4_t acc = {0.f, 0.f, 0.f, 0.f};
  for (int k0 = 0; k0 < K; k0 += 16) {
    half4_t a, b;
    for (int i = 0; i < 4; ++i) {
      a[i] = A[(size_t)(tm + lane % 16) * K + k0 + 4 * (lane / 16) + i];
      b[i] = B[(size_t)(k0 + 4 * (lane / 16) + i) * N + tn + lane % 16];
    }
    acc = __builtin_amdgcn_mfma_f32_16x16x16f16(a, b, acc, 0, 0, 0);
  }
  for (int i = 0; i < 4; ++i) C[(size_t)(tm + 4 * (lane / 16) + i) * N + tn + lane % 16] = acc[i];
}

// ---------- G6b: the same with rocWMMA fragments (portable to CUDA WMMA-style code) ----------
__global__ void gemm_rocwmma_naive(const rocwmma::float16_t* A, const rocwmma::float16_t* B, float* C,
                                   int M, int N, int K) {
  using namespace rocwmma;
  const int wave = (blockIdx.x * blockDim.x + threadIdx.x) / 64;
  const int tiles_n = N / 16;
  const int tm = (wave / tiles_n) * 16, tn = (wave % tiles_n) * 16;
  if (tm >= M) return;
  fragment<matrix_a, 16, 16, 16, float16_t, row_major> fa;
  fragment<matrix_b, 16, 16, 16, float16_t, row_major> fb;
  fragment<accumulator, 16, 16, 16, float> fc;
  fill_fragment(fc, 0.0f);
  for (int k0 = 0; k0 < K; k0 += 16) {
    load_matrix_sync(fa, A + (size_t)tm * K + k0, K);
    load_matrix_sync(fb, B + (size_t)k0 * N + tn, N);
    mma_sync(fc, fa, fb, fc);
  }
  store_matrix_sync(C + (size_t)tm * N + tn, fc, N, mem_row_major);
}
```

`v_mfma_f32_16x16x16_f16` computes a 16x16x16 product (8,192 FLOPs) per **wave** instruction. Inputs and outputs are spread across the 64 lanes: each lane supplies 4 halves of A, 4 halves of B, and holds 4 floats of the C tile. The layout in the comment was verified against a CPU reference (max error 0). **Getting the lane layout wrong is the #1 MFMA bug.** Look it up in the [AMD Matrix Instruction Calculator](https://github.com/ROCm/amd_matrix_instruction_calculator) for each instruction and architecture.

| Instruction family | Shape (M x N x K) | Types | Arch |
|---|---|---|---|
| `v_mfma_f32_32x32x8_f16`, `16x16x16_f16` | 32x32x8, 16x16x16 | FP16 in, FP32 accumulate (BF16 equivalents from CDNA2) | CDNA1+ |
| `v_mfma_f32_16x16x32_f16` | 16x16x32 | FP16/BF16 | **CDNA4 only** (`needs target feature gfx950-insts` on gfx942) |
| `v_mfma_f32_16x16x4f32`, `32x32x2f32` | | FP32 | CDNA1+ |
| FP8 / FP6 / FP4 (`..._f8f6f4`, scaled MX formats) | | Low precision | FP8 CDNA3, FP6/FP4 CDNA4 |

**rocWMMA** wraps MFMA in the CUDA-WMMA-style API (`fragment`, `load_matrix_sync`, `mma_sync`, `store_matrix_sync`). It generated the same instruction, with identical performance (53 TFLOP/s). Use it for prototyping and portability. Production GEMMs use hipBLASLt (Tensile/TensileLite) or Composable Kernel.

**Why the teaching MFMA kernel reaches only 53 TFLOP/s (2% of FP16 peak):** every MFMA is fed by 8 scalar 2-byte global loads per lane with no LDS or register reuse, so it is load-issue-bound (measured HBM AI 80 FLOP/B, while the roof at that AI is about 640 TFLOP/s). The production structure combines everything from G2-G5 with matrix cores:

1. A block tile (for example 256 x 256 x 64) is staged in LDS with direct-to-LDS loads and an XOR-swizzled layout, so fragment reads are conflict-free.
2. Each wave owns a large sub-tile (for example 64 x 128) and keeps **many accumulators** (AGPRs/VGPRs). Each A fragment loaded from LDS is reused across all N sub-tiles and each B fragment across all M sub-tiles. This is register blocking again, at fragment granularity.
3. LDS reads for the next k-step are interleaved with the MFMAs of the current one (software pipelining). The epilogue (scale, bias, activation, type conversion) is fused before the store.

`hipblasGemmEx` (FP16 in, FP32 accumulate) did the same 4096^3 problem in **0.14 ms = 980-995 TFLOP/s, about 43% of MI350X's dense FP16 peak (2.3 PFLOP/s)** at this size. Larger and better-shaped problems get closer to the peak.

## 6.6 G7 Split-K and Stream-K

```cpp
// fragment: gemm.hip part 5 of 6 -- concatenate parts 1-6 in order to build
// ---------- G7: split-K for skinny problems (few output tiles, long K) ----------
// blockIdx.z selects a K-range; each split writes its own partial C into a
// workspace, then a tiny kernel sums the splits in a fixed order (deterministic).
__global__ __launch_bounds__(kThreads) void gemm_splitk_partial(const float* A, const float* B, float* work,
                                                                int M, int N, int K, int k_per_split) {
  __shared__ float As[BK][BM];
  __shared__ float Bs[BK][BN];
  const int t = threadIdx.x, tr = t / (BN / TN), tc = t % (BN / TN);
  const float* Ab = A + (size_t)blockIdx.y * BM * K;
  const float* Bb = B + (size_t)blockIdx.x * BN;
  const int a_row = t / (BK / 4), a_col = (t % (BK / 4)) * 4;
  const int b_row = t / (BN / 4), b_col = (t % (BN / 4)) * 4;
  const int k_begin = blockIdx.z * k_per_split, k_end = k_begin + k_per_split;
  float acc[TM][TN] = {};
  for (int k0 = k_begin; k0 < k_end; k0 += BK) {
    float4 a = *reinterpret_cast<const float4*>(&Ab[(size_t)a_row * K + k0 + a_col]);
    As[a_col + 0][a_row] = a.x; As[a_col + 1][a_row] = a.y;
    As[a_col + 2][a_row] = a.z; As[a_col + 3][a_row] = a.w;
    *reinterpret_cast<float4*>(&Bs[b_row][b_col]) =
        *reinterpret_cast<const float4*>(&Bb[(size_t)(k0 + b_row) * N + b_col]);
    __syncthreads();
    compute_slice<true>(As, Bs, acc, tr, tc);
    __syncthreads();
  }
  float* Wb = work + (size_t)blockIdx.z * M * N + (size_t)(blockIdx.y * BM + tr * TM) * N + blockIdx.x * BN + tc * TN;
#pragma unroll
  for (int i = 0; i < TM; ++i)
#pragma unroll
    for (int j = 0; j < TN; ++j) Wb[(size_t)i * N + j] = acc[i][j];
}
__global__ void splitk_reduce(const float* work, float* C, int MN, int splits) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < MN; i += gridDim.x * blockDim.x) {
    float s = 0.f;
    for (int z = 0; z < splits; ++z) s += work[(size_t)z * MN + i];
    C[i] = s;
  }
}
```

**The problem: too few output tiles.** `M = N = 512` with 128 x 128 tiles gives **16 tiles for 256 CUs**, so 94% of the GPU idles while each tile loops over K = 16,384. G4 manages **3.2 TFLOP/s**.

**Split-K** cuts K into S chunks, launching `tiles x S` blocks. Each writes a partial tile, and a tiny kernel sums the S partials in a fixed order (deterministic). An `atomicAdd` epilogue is faster but nondeterministic. The extra traffic is `2 x S x M x N x 4 B = 32 MB` for S = 16, small next to the 64 MB of A and B. Measured: **0.22 ms = 38 TFLOP/s, a 12x speedup**. Choose S so that `tiles x S` is about 1-2x the CU count.

**Wave quantization** is the general form of the problem. With `T` tiles and `P` concurrent slots (CUs x blocks per CU), efficiency = `T / (ceil(T / P) x P)`. For example, 300 tiles on 256 slots gives 2 waves with the second only 17% full, so 59% efficiency.

**Stream-K** (Osama, Merrill et al., 2023) removes quantization entirely. It launches a **persistent** grid with exactly one workgroup per slot and splits the *total MAC-loop iterations* (tiles x k-steps) evenly. A workgroup's range may start in the middle of one tile and end in another. Partial tiles are completed through a workspace with flags (the same "publish, then fix up" idea as decoupled look-back), and hybrid schedules run whole tiles data-parallel first and Stream-K only on the remainder. hipBLASLt and Composable Kernel ship Stream-K variants.

## 6.7 Driver and Roofline Summary

```cpp
// fragment: gemm.hip part 6 of 6 -- concatenate parts 1-6 in order to build
int main() {
  const int M = 4096, N = 4096, K = 4096;
  const double flops = 2.0 * M * N * K;
  std::vector<float> hA((size_t)M * K), hB((size_t)K * N), hC((size_t)M * N), ref((size_t)M * N);
  for (size_t i = 0; i < hA.size(); ++i) hA[i] = float((i * 37) % 17) / 16.f - 0.5f;  // exact in fp16
  for (size_t i = 0; i < hB.size(); ++i) hB[i] = float((i * 11) % 13) / 16.f - 0.375f;
  std::vector<_Float16> hA16(hA.begin(), hA.end()), hB16(hB.begin(), hB.end());
  float *dA, *dB, *dC, *dRef;
  _Float16 *dA16, *dB16;
  HIP_CHECK(hipMalloc(&dA, sizeof(float) * hA.size()));
  HIP_CHECK(hipMalloc(&dB, sizeof(float) * hB.size()));
  HIP_CHECK(hipMalloc(&dC, sizeof(float) * hC.size()));
  HIP_CHECK(hipMalloc(&dRef, sizeof(float) * hC.size()));
  HIP_CHECK(hipMalloc(&dA16, sizeof(_Float16) * hA.size()));
  HIP_CHECK(hipMalloc(&dB16, sizeof(_Float16) * hB.size()));
  HIP_CHECK(hipMemcpy(dA, hA.data(), sizeof(float) * hA.size(), hipMemcpyHostToDevice));
  HIP_CHECK(hipMemcpy(dB, hB.data(), sizeof(float) * hB.size(), hipMemcpyHostToDevice));
  HIP_CHECK(hipMemcpy(dA16, hA16.data(), sizeof(_Float16) * hA.size(), hipMemcpyHostToDevice));
  HIP_CHECK(hipMemcpy(dB16, hB16.data(), sizeof(_Float16) * hB.size(), hipMemcpyHostToDevice));

  hipblasHandle_t handle;
  if (hipblasCreate(&handle) != HIPBLAS_STATUS_SUCCESS) return 1;
  const float alpha = 1.f, beta = 0.f;
  // Row-major C = A*B is column-major C^T = B^T * A^T: swap operands, keep "N".
  auto sgemm = [&] { hipblasSgemm(handle, HIPBLAS_OP_N, HIPBLAS_OP_N, N, M, K, &alpha, dB, N, dA, K, &beta, dRef, N); };
  auto hgemm = [&] {
    hipblasGemmEx(handle, HIPBLAS_OP_N, HIPBLAS_OP_N, N, M, K, &alpha, dB16, HIP_R_16F, N, dA16, HIP_R_16F, K,
                  &beta, dC, HIP_R_32F, N, HIPBLAS_COMPUTE_32F, HIPBLAS_GEMM_DEFAULT);
  };
  float ms = time_ms(sgemm);
  HIP_CHECK(hipMemcpy(ref.data(), dRef, sizeof(float) * ref.size(), hipMemcpyDeviceToHost));
  std::printf("%-26s %8.3f ms %7.1f TFLOP/s\n", "hipblasSgemm (fp32)", ms, tflops(flops, ms));

  auto run = [&](const char* name, auto launch) {
    HIP_CHECK(hipMemset(dC, 0, sizeof(float) * hC.size()));
    float t = time_ms(launch, 5);
    HIP_CHECK(hipMemcpy(hC.data(), dC, sizeof(float) * hC.size(), hipMemcpyDeviceToHost));
    double err = 0;
    for (size_t i = 0; i < hC.size(); i += 997) err = std::fmax(err, std::fabs(hC[i] - ref[i]));
    std::printf("%-26s %8.3f ms %7.1f TFLOP/s  max err %.1e\n", name, t, tflops(flops, t), err);
  };
  run("G1 naive", [&] { gemm_naive<<<dim3(N / 16, M / 16), dim3(16, 16)>>>(dA, dB, dC, M, N, K); });
  run("G2 LDS tiled 32x32", [&] { gemm_lds<<<dim3(N / T, M / T), dim3(T, 8)>>>(dA, dB, dC, M, N, K); });
  run("G3 register blocked 8x8", [&] { gemm_regblock<false><<<dim3(N / BN, M / BM), kThreads>>>(dA, dB, dC, M, N, K); });
  run("G4 + float4", [&] { gemm_regblock<true><<<dim3(N / BN, M / BM), kThreads>>>(dA, dB, dC, M, N, K); });
  run("G5 + double buffer", [&] { gemm_double_buffer<<<dim3(N / BN, M / BM), kThreads>>>(dA, dB, dC, M, N, K); });
  const int waves = (M / 16) * (N / 16);
  run("G6a MFMA f16, no LDS", [&] { gemm_mfma_naive<<<waves / 4, 256>>>(dA16, dB16, dC, M, N, K); });
  run("G6b rocWMMA f16, no LDS", [&] {
    gemm_rocwmma_naive<<<waves / 4, 256>>>(reinterpret_cast<const rocwmma::float16_t*>(dA16),
                                           reinterpret_cast<const rocwmma::float16_t*>(dB16), dC, M, N, K); });
  run("hipblasGemmEx f16->f32", hgemm);

  // Skinny case: 512 x 512 output = only 16 tiles of 128x128 for 256+ CUs, K = 16384.
  {
    const int m = 512, nn = 512, k = 16384, splits = 16;
    float *a2, *b2, *c2, *ref2, *work;
    HIP_CHECK(hipMalloc(&a2, sizeof(float) * m * k));
    HIP_CHECK(hipMalloc(&b2, sizeof(float) * k * nn));
    HIP_CHECK(hipMalloc(&c2, sizeof(float) * m * nn));
    HIP_CHECK(hipMalloc(&ref2, sizeof(float) * m * nn));
    HIP_CHECK(hipMalloc(&work, sizeof(float) * splits * m * nn));
    HIP_CHECK(hipMemcpy(a2, hA.data(), sizeof(float) * m * k, hipMemcpyHostToDevice));   // reuse host data
    HIP_CHECK(hipMemcpy(b2, hB.data(), sizeof(float) * k * nn, hipMemcpyHostToDevice));
    const double f2 = 2.0 * m * nn * k;
    float t0 = time_ms([&] { gemm_regblock<true><<<dim3(nn / BN, m / BM), kThreads>>>(a2, b2, ref2, m, nn, k); });
    float t1 = time_ms([&] {
      gemm_splitk_partial<<<dim3(nn / BN, m / BM, splits), kThreads>>>(a2, b2, work, m, nn, k, k / splits);
      splitk_reduce<<<num_cus() * 4, 256>>>(work, c2, m * nn, splits);
    });
    std::vector<float> r1(m * nn), r2(m * nn);
    HIP_CHECK(hipMemcpy(r1.data(), ref2, sizeof(float) * m * nn, hipMemcpyDeviceToHost));
    HIP_CHECK(hipMemcpy(r2.data(), c2, sizeof(float) * m * nn, hipMemcpyDeviceToHost));
    double err = 0;
    for (int i = 0; i < m * nn; ++i) err = std::fmax(err, std::fabs(r1[i] - r2[i]));
    std::printf("512x512x16384: G4 %.3f ms (%.1f TFLOP/s), split-K x%d %.3f ms (%.1f TFLOP/s), max diff %.1e\n",
                t0, tflops(f2, t0), splits, t1, tflops(f2, t1), err);
    for (float* p : {a2, b2, c2, ref2, work}) HIP_CHECK(hipFree(p));
  }
  hipblasDestroy(handle);
  HIP_CHECK(hipFree(dA)); HIP_CHECK(hipFree(dB)); HIP_CHECK(hipFree(dC)); HIP_CHECK(hipFree(dRef));
  HIP_CHECK(hipFree(dA16)); HIP_CHECK(hipFree(dB16));
  return 0;
}
```

Measured on MI350X (`M = N = K = 4096`; FP32 vector ridge 18.0 FLOP/B, FP16 matrix ridge about 288 FLOP/B; percentages are of MI350X peaks, 144.2 TFLOP/s packed FP32 and 2.3 PFLOP/s dense FP16):

| Step | Time (ms) | TFLOP/s | % of relevant peak | Measured HBM AI (FLOP/B) | Roofline position / binding resource |
|---|---|---|---|---|---|
| G1 naive | 36.1 | 3.8 | 2.6% (FP32) | 5.6 | Left of ridge but far below the HBM roof: memory-instruction issue |
| G2 LDS 32x32 | 5.11 | 26.9 | 19% | 32 | Right of ridge; LDS bandwidth |
| G3 register 8x8 | 1.48 | 92.9 | 64% | 177 | Compute side; VALU issue, LDS conflicts |
| G4 + `float4` | 1.39 | 98.7 | 68% | 176 | Compute side |
| G5 + double buffer | 1.55 | 88.5 | 61% | 172 | Occupancy 4 to 2 (240 VGPRs) |
| G6a MFMA FP16, no LDS | 2.58 | 53 | 2% (FP16) | 80 | Far below roof: load issue |
| G6b rocWMMA, no LDS | 2.58 | 53 | 2% | | Same instructions as G6a |
| `hipblasSgemm` | 1.10 | 125 | 87% | | Library (FP32) |
| `hipblasGemmEx` FP16 | 0.14 | 980-995 | ~43% | | Library (matrix cores) |
| G7 split-K, 512x512x16384 | 0.22 | 38 | 26% | | 16x more parallelism than G4 (3.2) |

## 6.8 Interview Questions

**Q1.** Walk through optimizing SGEMM from naive. What does each step fix, and what metric proves it?

Naive is memory-instruction-bound (two loads per FMA; huge `TCP_TCC_READ_REQ`). LDS tiling gives each global element `T` reuses (`FETCH_SIZE` 24.7 GB down to 4.2 GB) but becomes LDS-bound (`SQ_INSTS_LDS` huge, LDS utilization high). Register blocking reuses each LDS value 8 times (`SQ_INSTS_LDS` down about 6x) and gets close to compute-bound. Vectorized loads cut instruction count and improve coalescing. Double buffering overlaps latency, but only if it does not cost occupancy (check VGPRs). Matrix cores raise the compute roof 8-16x, after which the whole problem becomes feeding them: LDS layout, fragment reuse, pipelining.

**Q2.** Derive the global-memory AI of a `BM x BN` block tile with K-slice `BK`.

Per slice the block loads `(BM + BN) x BK` elements of 4 bytes and performs `BM x BN x BK` FMAs = `2 BM BN BK` FLOPs. AI = `2 BM BN BK / (4 BK (BM + BN)) = BM BN / (2 (BM + BN))`. For 128 x 128 that is 32 FLOP/B, above MI300X's FP32 ridge of 30.8. `BK` cancels: it trades LDS capacity and barrier frequency, not AI. Bigger tiles raise AI but need more registers and LDS (lower occupancy) and create fewer tiles (worse wave quantization).

**Q3.** Why might double buffering make an AMD kernel slower?

It keeps two slices' worth of data live (registers for the in-flight global loads plus LDS for two buffers), and the compiler's scheduling around it can raise VGPR use further. Here it went from 102 to 240 VGPRs, and occupancy dropped from 4 to 2 waves/SIMD. CDNA relies on many resident waves to hide latency, so losing occupancy outweighed the overlap. Forcing occupancy back caused spills. The fix is direct-to-LDS loads (no register staging) and careful tile sizing.

**Q4.** When do you use split-K vs Stream-K?

Split-K is simple and helps when there are far fewer output tiles than CUs and K is long (skinny GEMMs, small batch). Its cost is S partial tiles of extra traffic plus a reduction. Stream-K generalizes it: it balances work perfectly for *any* tile count, removing the wave-quantization tail, at the cost of a persistent kernel and fix-up logic. Libraries pick the strategy per problem shape using heuristics or tuning tables.

**Q5.** How do you read MFMA utilization in a profile?

`SQ_VALU_MFMA_BUSY_CYCLES` relative to elapsed cycles (rocprof-compute "MFMA Utilization", metric 2.1.10), `SQ_INSTS_VALU_MFMA_MOPS_*` for matrix FLOPs by type, and the roofline's MFMA FLOP/s against the per-type peak. Low MFMA utilization with high LDS utilization or bank conflicts means the feed path is the bottleneck. Low utilization with low occupancy usually means register or LDS pressure, or a schedule problem.

**Q6.** What is wave quantization? Compute the efficiency for 1,000 tiles on MI300X with 1 block per CU.

With P = 304 slots, `ceil(1000 / 304) = 4` waves give 1,216 slots for 1,000 tiles: 82% efficiency, because the last wave is 29% full. Fixes: choose a tile size that makes the tile count a multiple of the slot count, use split-K to multiply the work items, or use Stream-K.

> **See also:** [Performance Engineering -- Roofline Model](../computer-science/Performance_Engineering.md#3-roofline-model) and its [Loop Interchange and Tiling for Matmul](../computer-science/Performance_Engineering.md#54-loop-interchange-and-tiling-for-matmul) (the CPU version of the same ladder); [Parallel GPU Programming -- Matrix Multiplication](../ml-gpu/Parallel_GPU_Programming.md#185-matrix-multiplication); [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) for MFMA and LDS details.

---

# 7. Elementwise Fusion and Kernel Launch Overhead

## 7.1 The Cost Model

For a chain of memory-bound kernels:

```text
t_unfused ~= sum_i bytes_i / BW  +  k x t_launch          (k kernels, intermediates round-trip HBM)
t_fused   ~= bytes_in_out / BW   +  t_launch
```

For `w = gelu(a*x + b) + r`, the unfused version moves `(x, y) + (y, z) + (z, r, w) = 7n` floats, and the fused version moves `(x, r, w) = 3n`. **Ideal speedup = 7/3 = 2.33x**, from bytes alone.

## 7.2 Code

```cpp
// fusion.hip -- elementwise fusion and launch overhead
// Build: hipcc -O3 --offload-arch=gfx942 fusion.hip -o fusion
#include "common.hpp"
#include <chrono>
#include <cmath>
#include <vector>

__device__ __forceinline__ float gelu(float v) {  // tanh approximation
  return 0.5f * v * (1.f + tanhf(0.7978845608f * (v + 0.044715f * v * v * v)));
}
// Unfused: three kernels, each a full round trip through HBM.
__global__ void scale_bias(const float* x, float* y, float a, float b, int n) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += gridDim.x * blockDim.x) y[i] = a * x[i] + b;
}
__global__ void gelu_kernel(const float* y, float* z, int n) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += gridDim.x * blockDim.x) z[i] = gelu(y[i]);
}
__global__ void add_residual(const float* z, const float* r, float* w, int n) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += gridDim.x * blockDim.x) w[i] = z[i] + r[i];
}
// Fused: intermediates live in registers. Traffic 3n floats instead of 7n.
__global__ void fused(const float* x, const float* r, float* w, float a, float b, int n) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += gridDim.x * blockDim.x)
    w[i] = gelu(a * x[i] + b) + r[i];
}
__global__ void empty_kernel() {}

int main() {
  const int n = 1 << 27;  // 512 MiB per array
  float *x, *r, *y, *z, *w;
  for (float** p : {&x, &r, &y, &z, &w}) HIP_CHECK(hipMalloc(p, sizeof(float) * n));
  std::vector<float> h(n);
  for (int i = 0; i < n; ++i) h[i] = std::sin(0.001f * (i % 10007));
  HIP_CHECK(hipMemcpy(x, h.data(), sizeof(float) * n, hipMemcpyHostToDevice));
  HIP_CHECK(hipMemcpy(r, h.data(), sizeof(float) * n, hipMemcpyHostToDevice));
  const int grid = num_cus() * 8, block = 256;
  const double fb = sizeof(float) * double(n);

  float ms_unfused = time_ms([&] {
    scale_bias<<<grid, block>>>(x, y, 1.5f, 0.1f, n);
    gelu_kernel<<<grid, block>>>(y, z, n);
    add_residual<<<grid, block>>>(z, r, w, n);
  });
  float ms_fused = time_ms([&] { fused<<<grid, block>>>(x, r, w, 1.5f, 0.1f, n); });
  std::printf("unfused (3 kernels): %.3f ms, %.0f GB/s effective on 7n bytes\n", ms_unfused, gbps(7 * fb, ms_unfused));
  std::printf("fused   (1 kernel) : %.3f ms, %.0f GB/s on 3n bytes, speedup %.2fx\n", ms_fused,
              gbps(3 * fb, ms_fused), ms_unfused / ms_fused);

  // Launch overhead: 1000 back-to-back empty launches (throughput) ...
  const int launches = 1000;
  float ms = time_ms([&] { for (int i = 0; i < launches; ++i) empty_kernel<<<1, 64>>>(); }, 5);
  std::printf("empty kernel, async stream : %6.2f us per launch\n", 1000.f * ms / launches);
  // ... launch + synchronize each time (latency) ...
  ms = time_ms([&] { for (int i = 0; i < 100; ++i) { empty_kernel<<<1, 64>>>(); HIP_CHECK(hipDeviceSynchronize()); } }, 3);
  std::printf("empty kernel, launch + sync: %6.2f us per launch\n", 1000.f * ms / 100);
  // ... and the same 1000 launches captured once into a HIP graph.
  hipStream_t s;
  HIP_CHECK(hipStreamCreate(&s));
  hipGraph_t graph;
  hipGraphExec_t exec;
  HIP_CHECK(hipStreamBeginCapture(s, hipStreamCaptureModeGlobal));
  for (int i = 0; i < launches; ++i) empty_kernel<<<1, 64, 0, s>>>();
  HIP_CHECK(hipStreamEndCapture(s, &graph));
  HIP_CHECK(hipGraphInstantiate(&exec, graph, nullptr, nullptr, 0));
  ms = time_ms([&] { HIP_CHECK(hipGraphLaunch(exec, s)); }, 5);
  std::printf("empty kernel, HIP graph    : %6.2f us per kernel\n", 1000.f * ms / launches);

  // Host-side cost only: how long the CPU spends enqueueing (no waiting).
  auto host_us = [](auto&& f) {
    auto t0 = std::chrono::steady_clock::now();
    f();
    return std::chrono::duration<double, std::micro>(std::chrono::steady_clock::now() - t0).count();
  };
  HIP_CHECK(hipDeviceSynchronize());
  double cpu_launch = host_us([&] { for (int i = 0; i < launches; ++i) empty_kernel<<<1, 64, 0, s>>>(); });
  HIP_CHECK(hipStreamSynchronize(s));
  double cpu_graph = host_us([&] { HIP_CHECK(hipGraphLaunch(exec, s)); });
  HIP_CHECK(hipStreamSynchronize(s));
  std::printf("CPU enqueue time: %.0f us for %d launches vs %.0f us for one graph launch\n",
              cpu_launch, launches, cpu_graph);
  HIP_CHECK(hipGraphExecDestroy(exec));
  HIP_CHECK(hipGraphDestroy(graph));
  HIP_CHECK(hipStreamDestroy(s));
  for (float* p : {x, r, y, z, w}) HIP_CHECK(hipFree(p));
  return 0;
}
```

## 7.3 Results and What They Mean

Measured on MI350X (`n = 2^27` floats, 512 MiB per array):

| Measurement | Result |
|---|---|
| Unfused, 3 kernels | 0.855 ms (4.40 TB/s effective on 7n bytes: each kernel streams near copy speed) |
| Fused, 1 kernel | 0.404-0.406 ms (3.97-3.99 TB/s on 3n bytes) |
| **Speedup** | **2.11x** (ideal 2.33x; the fused kernel does all the `tanhf` math per byte, so it streams slightly below copy speed) |
| Empty kernel, back-to-back on one stream | **1.7 us per kernel** (GPU-side dispatch throughput) |
| Empty kernel, launch + `hipDeviceSynchronize` | **10-11 us** round trip |
| CPU time to enqueue 1,000 launches | 700-825 us (0.7-0.8 us each) |
| CPU time for one `hipGraphLaunch` of the same 1,000 kernels | **9-18 us** |
| GPU time per kernel inside the graph | 2.8-3.1 us |

Interpretation:

- **A kernel that moves less than about 10 MB (2 us at 5 TB/s) is launch-dominated.** Batch it, fuse it, or make it persistent.
- **Graphs cut CPU submission cost by about 40-80x** (one API call instead of 1,000). That matters when the CPU is the bottleneck: Python frameworks dispatching thousands of small kernels per step, or the decode loop of LLM inference. On this ROCm build the GPU-side cost per graph node was *not* lower than back-to-back stream launches. Measure on your stack, and do not claim graphs make kernels faster on the GPU.
- `launch + sync` (10 us) is what a naive benchmark measures when it synchronizes after each launch. Always time many back-to-back launches between events.

## 7.4 When to Fuse and When Not To

| Fuse | Do not fuse (or think twice) |
|---|---|
| Elementwise chains (bias, activation, residual, scale, cast) | When the fused kernel's register pressure drops occupancy below what hides latency |
| Reduction epilogues: add + LayerNorm, softmax + scale + mask | When fusion breaks a GEMM's tiling. Fuse *into the GEMM epilogue* instead (hipBLASLt epilogues, CK) |
| Producer-consumer pairs with the same iteration space | When the intermediate is needed later (backward pass). Then it is recompute vs store; activation checkpointing makes that trade explicitly |
| Many tiny kernels (launch-bound) | When different parts need different launch shapes (a reduction then a broadcast). Use a two-phase or cooperative kernel instead |

Compilers do this automatically. `torch.compile` (Inductor) generates fused Triton kernels for pointwise and reduction chains. XLA fuses HLO ops. Hand fusion is still needed around library GEMMs and attention.

## 7.5 Interview Questions

**Q1.** You fuse three elementwise kernels and get 2.1x. Was that expected? What is the upper bound?

Yes. The bound is the traffic ratio: 7n to 3n floats gives 2.33x if every kernel runs at the same bandwidth and launch overhead is negligible. A fused kernel can fall short if it becomes slightly compute-heavy per byte (transcendentals) or uses more registers. It can beat the ratio when the original kernels were launch-dominated, because then the saved launches count too.

**Q2.** How do you find fusion and launch-overhead opportunities in a real application?

`rocprofv3 --kernel-trace --stats` lists kernels by count and total time. Look for many short kernels (a few us each) with high call counts, and compute each kernel's achieved bandwidth (bytes / duration). A timeline (rocprofv3 output in Perfetto, or rocprof-sys) shows gaps between kernels, which means CPU-bound submission. Chains of memory-bound kernels on the same tensor shape are fusion candidates. Idle gaps call for graphs or a framework-level fix (`torch.compile` mode `reduce-overhead` uses CUDA/HIP graphs).

**Q3.** What exactly is "kernel launch overhead"?

There are two parts. **Host-side**: the API call validates arguments, writes the kernarg buffer, and builds an AQL dispatch packet in a user-mode queue, then rings the doorbell (sub-us to a few us of CPU). **Device-side**: the command processor fetches the packet, sets up the dispatch, the workgroup manager launches waves, and the end-of-kernel signal completes (about 1-3 us between back-to-back kernels). Synchronizing adds the round trip of the completion signal back to the host (10 us here). Graphs amortize the host part; persistent kernels and fusion remove both.

**Q4.** A kernel processes 4 KB of data per launch and is called 100,000 times per second. What do you do?

At about 2 us of launch cost per call, the GPU spends about 0.2 s of each second on overhead alone, and the CPU spends 0.07-0.08 s just enqueueing. Batch the calls (process many 4 KB items per launch, with an index in the kernel), or use a persistent kernel that pulls work from a device-side queue, or capture the repeated sequence in a graph if the shapes are static. Also question whether the GPU is the right place for 4 KB tasks at all.

> **See also:** [ML and AI Frameworks -- torch.compile Internals](../ml-gpu/ML_AI_Frameworks.md#86-torchcompile-internals-dynamo-aotautograd-inductor) (what Inductor fuses and the memory-traffic arithmetic); [Parallel GPU Programming -- CUDA Graphs](../ml-gpu/Parallel_GPU_Programming.md#224-cuda-graphs); [Performance Engineering -- Roofline Model](../computer-science/Performance_Engineering.md#3-roofline-model).

---

# 8. Kernel Exercise List

## 8.1 How to Use This List

Write each kernel in HIP, starting from `common.hpp` (Section 0.4). For every exercise, report four things: (1) the algorithmic bytes and FLOPs, (2) your achieved GB/s or TFLOP/s, (3) the result as a percentage of the **measured ceiling on your machine**, and (4) one counter that explains the remaining gap. Measure the two ceilings first with a `float4` grid-stride kernel on a 1 GiB buffer:

- **R** = read-only ceiling (our MI350X: about 5.4 TB/s)
- **C** = copy ceiling, read + write (our MI350X: about 4.4 TB/s)

On MI300X, measure your own R and C. Do not scale ours. Levels: 1 = warm-up, 2 = standard interview question, 3 = strong-candidate question, 4 = take-home or onsite deep dive. Hints are in [Answers](#answers). Try each exercise before reading them.

| # | Exercise | Level | Algorithmic traffic (work) | AI | Target | Core skill |
|---|---|---|---|---|---|---|
| E1 | Vector add `c = a + b`, `n = 2^28` FP32 | 1 | 12n B | 0.083 | >= 85% of C | Grid-stride, `float4`, tail handling |
| E2 | SAXPY `y = a x + y` | 1 | 12n B (2n FLOP) | 0.167 | >= 90% of C; also report time at `n = 2^16` | Launch-bound regime |
| E3 | Reduction: sum, max, argmax | 2 | 4n B | 0.25 | >= 90% of R | Wave64 shuffles, determinism |
| E4 | Transpose: 8192 x 8192 and 8191 x 5000 | 2 | 8 B per element | 0 | >= 85% of a copy kernel with the same grid (about 80% of C), zero LDS bank conflicts | LDS tiles, padding, bounds |
| E5 | Inclusive scan, `2^28` int32 | 3 | 8n B (ideal) | n/a | >= 60% of C measured against 2n | Reduce-then-scan; look-back stretch |
| E6 | 256-bin byte histogram (uniform and all-equal) | 2 | n B | n/a | >= 45% of R on **both** datasets | Privatization, aggregation |
| E7 | Row softmax: 32768 x 4096, 32768 x 1000, with masked rows | 2 | 8 B per element | ~1 | >= 85% of C at N = 4096 | Wave per row, online softmax |
| E8 | LayerNorm forward (backward as stretch) | 3 | 8 B per element | ~1 | >= 85% of C; rel. error < 1e-5 on mean-1e4 data | Registers, Welford |
| E9 | Tiled SGEMM 4096^3 (MFMA FP16 as stretch) | 4 | 137 GFLOP | 683 (ideal) | >= 50% of packed FP32 peak; stretch >= 30% of FP16 peak | Tiling, register blocking, LDS layout |
| E10 | Top-k per row, k = 8 and 64, 32768 x 4096 | 3 | 4 B per element + output | low | >= 70% of R for k <= 32 | Register lists, wave merge, radix select |
| E11 | 2D 5-point Jacobi stencil, 8192 x 8192 FP32 | 3 | 8 B per point | 0.5 | >= 80% of C | Halo tiling, cache reuse |
| E12 | SpMV CSR: 2D Laplacian and a power-law matrix | 4 | `nnz x 8 + rows x 12` B (+ `x` gathers) | ~0.2 | Laplacian >= 65% of R; power-law >= 40% of R | Row-to-lane mapping, load balance |

## 8.2 Exercise Specifications

**E1. Vector add.** `c[i] = a[i] + b[i]` for `n = 2^28` floats, plus `n = 2^28 + 3` to exercise the tail. Write it two ways: one thread per element, and grid-stride with `float4`. Verify against the CPU. Report GB/s on 12n bytes and the ratio to C. Explain any difference between the two versions using `SQ_INSTS_VMEM_RD` / `SQ_WAVES`.

**E2. SAXPY.** Same harness, `y = a*x + y` (y is read and written). Then run with `n = 2^16` and report microseconds per call. Explain why GB/s collapses at small `n` and what you would do about it in a real application.

**E3. Reduction.** Sum, max, and argmax of `2^28` floats. Requirements: wave64-correct shuffles with no hard-coded 32, a deterministic two-pass version, and argmax ties broken toward the **lowest index**. State your NaN semantics (propagate or ignore) and test them.

**E4. Transpose.** Out-of-place transpose for square and non-multiple-of-tile shapes. Show with `SQ_LDS_BANK_CONFLICT` that your tiled version has zero conflicts. Report % of a copy kernel with the same bytes.

**E5. Scan.** Full-array inclusive scan of `2^28` int32 (values 0-2 so it cannot overflow), for any `n` (not only multiples of the tile). Base: reduce-then-scan. Stretch: single-pass decoupled look-back with a wave-parallel look-back, compared against `hipcub::DeviceScan::InclusiveSum`.

**E6. Histogram.** 256 bins over 1 GiB of bytes. Hit the target on **both** uniform random data and data where every byte is equal. Stretch: 4,096 bins of 16-bit keys.

**E7. Softmax.** Row-wise softmax over FP32 matrices with N = 4096 (fast path) and N = 1000 (general path). Logits up to 100 (naive `exp` overflows). Include a row that is entirely `-inf` and document what your kernel returns for it. Check accuracy against an FP64 reference.

**E8. LayerNorm.** Forward with `gamma`, `beta`, `eps = 1e-5`, N = 4096. Test data: mean 1e4, standard deviation 1. Show that `E[x^2] - E[x]^2` in FP32 fails on this data and your kernel does not. Stretch: backward (`dx`, `dgamma`, `dbeta`), with deterministic `dgamma`/`dbeta`.

**E9. Tiled GEMM.** FP32, row-major, `M = N = K = 4096`. Walk the Section 6 ladder yourself. At each step record VGPRs and occupancy (`-Rpass-analysis=kernel-resource-usage`), `SQ_LDS_BANK_CONFLICT`, and TFLOP/s. Stretch: an FP16 MFMA kernel with LDS staging and fragment reuse, compared with `hipblasGemmEx`.

**E10. Top-k.** For each row of a 32768 x 4096 FP32 matrix, return the k largest values and their indices, sorted descending, with k = 8 and k = 64. Ties go to the lower index. Stretch: global top-1000 of `10^8` elements.

**E11. Stencil.** `out[i][j] = 0.25 * (in[i-1][j] + in[i+1][j] + in[i][j-1] + in[i][j+1])` on the interior, with fixed boundary values. Run 100 iterations with ping-pong buffers. Report GB/s per iteration on 8 B per point. Stretch: temporal blocking (2-4 time steps per pass) and explain why it can beat the "bandwidth bound".

**E12. SpMV.** `y = A x` in CSR with FP32 values and int32 column indices. Matrices: a 5-point 2D Laplacian (4,096^2 rows, about 5 nonzeros per row) and a power-law matrix (row lengths from 1 to 10^5). Implement scalar CSR (thread per row) and vector CSR (wave or sub-wave per row), and compare with `rocsparse_spmv`.

## Answers

**E1.** Grid of `CUs x 4-8` blocks of 256 threads. A `float4` main loop over `n / 4`, then a scalar tail loop, which handles `2^28 + 3`. Use `size_t` indices once `n` can exceed 2^31. Mark the pointers `__restrict__`. Both versions should reach 85-95% of C on large `n`. One thread per element works but issues 4x the memory instructions (`SQ_INSTS_VMEM_RD` per wave shows it). An add and three streams make this exactly the copy ceiling problem. Nothing can be gained from arithmetic tricks.

**E2.** At `n = 2^16` the kernel moves 768 KB, which is 0.2 us at 4 TB/s, but a launch costs about 1.7 us back-to-back and about 10 us with a synchronize. You are measuring launch overhead, not bandwidth. Real fixes: fuse SAXPY into its producer or consumer, batch many small vectors into one launch, or capture the sequence in a graph if the CPU is the bottleneck (Section 7).

**E3.** Use the R6 pattern: grid-stride `float4` partials, `block_reduce` with `__shfl_down(v, off, 64)` from `off = 32`, two-pass for determinism. For **max**, the identity is `-INFINITY`. For **argmax**, shuffle the value and the index together and combine with `(v_b > v_a) || (v_b == v_a && i_b < i_a)`. `fmaxf` *ignores* NaN, while PyTorch's `max` *propagates* it, so pick one and test it with `isnan`. An atomic version cannot do argmax directly. Pack `key = (uint64(ordered_bits(v)) << 32) | (0xFFFFFFFFu - idx)`, where `ordered_bits(v) = (bits & 0x80000000) ? ~bits : bits | 0x80000000`, and use `atomicMax` on `unsigned long long`. Decode `idx = 0xFFFFFFFFu - (uint32)key`. Inverting the index makes ties resolve to the lowest index (with the raw index in the low bits, `atomicMax` would pick the highest). Or keep it two-pass.

**E4.** Use T3 from Section 2: a 64 x 65 tile and 64 x 4 threads. For 8191 x 5000, keep both the read-phase check `(r < rows && c < cols)` and the write-phase check `(orow < cols && oc < rows)`, and size the grid with `ceil` divisions over the *input* dimensions. The bank-conflict counter should be exactly 0, and a copy kernel with the same grid is the bar to compare against. If you are below 85%, check that each wave writes 256 contiguous bytes (vL1D Coalescing) and that each thread moves at least 8-16 elements.

**E5.** Start from Section 3.4. Pad the last tile with the identity (0) on load and skip out-of-range stores. Use `int4` loads with 4-16 items per thread and 2 barriers per tile. Recurse on the tile sums until they fit one block. For the look-back stretch: lane `j` of the looking wave reads the status of tile `t - 1 - j`, wave 0 does `__ballot` on "flag == P" (a 64-bit mask) and finds the nearest such lane with `__ffsll`, sums the aggregates of the lanes before it (a wave reduction), and repeats if no P flag was found. Spin only while some lane still sees flag 0. Remember to reset the status array (or use epoch-tagged flags) between runs.

**E6.** Use LDS privatization (Section 4 H2) with **run aggregation** (H3) in the same kernel. The uniform case is LDS-atomic-bound at about 50% of R, and aggregation keeps the all-equal case at the same rate. To go further on uniform data, use per-wave or per-lane-group sub-histograms with 16-bit counters, flushed before they overflow. For 4,096 bins: 16 KB of LDS per copy still fits, so privatize and merge only non-zero bins. For 64K bins, sort-then-RLE beats atomics.

**E7.** N = 4096: use SM3 (one wave per row, 16 `float4` per lane in registers, `__shfl_xor` butterflies). N = 1000: either use the online SM2 path, or use registers with predicated loads, where out-of-range lanes contribute `-inf` to the max and 0 to the sum. Fully masked row: when `m == -inf`, define the output (zeros is the common choice) instead of producing `NaN` from `-inf - (-inf)`. Accuracy: `|y - y_ref| x N` should be around 1e-5. Pack 4 rows per 256-thread block. Wave-per-row needs no LDS and no barriers.

**E8.** Forward: the Section 5 LN kernel. The two-pass variance from registers handles mean-1e4 data. With `E[x^2] - E[x]^2` you will see variance errors of order 1-10 on data whose true variance is 1, sometimes negative, giving NaN from `rsqrt`. If N does not fit in registers, use Welford per lane and merge lanes with the Chan formula via shuffles. Backward, with `xhat = (x - mean) * rstd` and `g = dy * gamma`: `dx = rstd * (g - mean(g) - xhat * mean(g * xhat))`. `dgamma = sum over rows of dy * xhat` and `dbeta = sum over rows of dy` are **column** reductions. Have each block accumulate partials for a slab of rows in registers or LDS, write `[blocks x N]` partials, then reduce them in a second kernel in a fixed order (deterministic, no float atomics).

**E9.** Expect roughly the Section 6 numbers: naive 2-3% of peak, LDS tile 15-20%, register-blocked 60-70% of packed FP32 peak. To pass 50%: 128 x 128 block tile, 8 x 8 thread tile (64 accumulators), `As` transposed, `float4` global and LDS accesses, at most about 128 VGPRs (4 waves/SIMD), no spills, and `v_pk_fma_f32` in the ISA. Kill the remaining conflicts with an XOR swizzle on the `Bs` column index, and try BK = 16 for more work per barrier. Do not add double buffering without checking VGPRs. MFMA stretch: stage 128 x 128 x 32 tiles in LDS. Each wave computes a 64 x 64 sub-tile as a 4 x 4 grid of `16x16x16` MFMAs, loading 4 A fragments and 4 B fragments per k-step and reusing each 4 times. 30% of the FP16 peak needs conflict-free fragment reads, and `hipblasGemmEx` is the ceiling to compare against.

**E10.** For k <= 32: one wave per row. Each lane scans its 64 elements, keeping a sorted top-k list in registers with insertion that exits early when the value is below the current k-th. Then merge across lanes in k rounds: wave argmax via shuffles, the winning lane pops its head, repeat. Alternatively, write the 64 x k candidates to LDS and bitonic-sort them. This is read-bound for small k. For k = 64 and larger, use **radix select**: build a histogram of the top 8 bits of the order-preserving uint transform of the floats, find the bucket containing the k-th element, refine on the next 8 bits, then gather everything above the threshold and sort only those. This is how PyTorch's `topk` works. For global top-1000 of 10^8: per-block top-k, then a second pass over the `blocks x k` candidates. Handle ties with `(value desc, index asc)` and decide where NaN sorts.

**E11.** The naive version (one thread per output, 64 x 4 blocks) often reaches 70-80% of C already, because L1/L2 capture the neighbour reuse. Check `FETCH_SIZE` against `rows x cols x 4` to confirm each input is fetched from HBM about once. LDS tiling with a halo (a 66 x 6 tile for a 64 x 4 block) guarantees it. Never update in place: Jacobi needs the old values, so ping-pong two buffers and swap pointers between launches. **Temporal blocking** computes 2-4 time steps on an LDS tile (with a halo of width equal to the number of steps) before writing. Each HBM byte then supports several steps of FLOPs, so the AI rises above the single-step 0.5 FLOP/B and the per-iteration bandwidth bound no longer applies. The cost is redundant halo computation.

**E12.** Scalar CSR (thread per row) is uncoalesced, because lanes read different rows' nonzeros, and on power-law matrices one long row stalls a whole wave. Vector CSR with a full wave per row is coalesced but wastes 59 of 64 lanes on the Laplacian (5 nonzeros per row). Use a **sub-wave group per row** sized to the average row length (4-8 lanes for the Laplacian, reduced with `__shfl_xor(v, o, width)`). For power-law matrices, bin rows by length (short rows: group per row; long rows: a block or several blocks per row, combined with atomics or a second pass), or use merge-path / CSR-adaptive load balancing (rocSPARSE's adaptive and LRB algorithms). Bytes per nonzero: 4 (value) + 4 (column) + 4 (`x`, mostly cached for banded matrices). The `x` gather is the irregular part. Reordering (for example RCM) improves its locality. Compare against `rocsparse_spmv` and report GB/s on the bytes above.

> **See also:** [Coding Problem List](../practice/Coding_Problem_List.md) for CPU-side algorithm practice; [Performance Engineering](../computer-science/Performance_Engineering.md) for roofline, Little's law, and benchmarking rigor; [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) for the counters used to explain each gap; [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md) for presenting a profile -> diagnose -> fix -> re-profile story in interviews.
