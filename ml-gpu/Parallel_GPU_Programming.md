# Parallel and GPU Programming -- Comprehensive Reference

> Last reviewed: 2026-11 · Versions assumed: ROCm 6.4-7.x, CUDA 12.x, CMake 3.21-4.2, Open MPI 5.0

> A deep-dive reference covering MPI, OpenMP, CUDA, and HIP programming for high-performance computing. Each section includes conceptual explanations, comparison tables, code examples, and common interview questions with detailed answers. Complements the *C++ Fundamentals*, *CS Fundamentals*, *DSA Fundamentals*, and *LeetCode Patterns* guides.

> **Related guides:** scaling laws, roofline, and Little's law worked math live in [Performance Engineering](../computer-science/Performance_Engineering.md) ([Amdahl/Gustafson](../computer-science/Performance_Engineering.md#2-amdahls-and-gustafsons-laws), [roofline](../computer-science/Performance_Engineering.md#3-roofline-model)). AMD hardware counters and the rocprof-compute workflow are in [AMD GPU Architecture and Profiling](AMD_GPU_Architecture_and_Profiling.md). Step-by-step kernel optimizations (reduction, transpose, GEMM, scan) are in [GPU Kernel Case Studies](GPU_Kernel_Case_Studies.md). Building HIP with CMake is in [CMake Fundamentals -- HIP and ROCm with CMake](../tools/CMake_Fundamentals.md#64-hip-and-rocm-with-cmake), and combining it with MPI and OpenMP in one CMake build is in [32.6](#326-building-hybrid-mpi--openmp--hip-code-with-cmake).

---

## Table of Contents

### Part 1: MPI (Message Passing Interface)

1. [MPI Fundamentals](#1-mpi-fundamentals)
2. [Point-to-Point Communication](#2-point-to-point-communication)
3. [Collective Communication](#3-collective-communication)
4. [MPI Data Types and Derived Types](#4-mpi-data-types-and-derived-types)
5. [Communicator Management and Topologies](#5-communicator-management-and-topologies)
6. [One-Sided Communication (RMA)](#6-one-sided-communication-rma)
7. [MPI I/O (Parallel File I/O)](#7-mpi-io-parallel-file-io)
8. [Advanced MPI Topics](#8-advanced-mpi-topics)

### Part 2: OpenMP

9. [OpenMP Fundamentals](#9-openmp-fundamentals)
10. [Work-Sharing Constructs](#10-work-sharing-constructs)
11. [Data Environment and Scoping](#11-data-environment-and-scoping)
12. [Synchronization](#12-synchronization)
13. [Tasking Model](#13-tasking-model)
14. [SIMD and Vectorization](#14-simd-and-vectorization)
15. [OpenMP Target Offloading (GPU)](#15-openmp-target-offloading-gpu)
16. [OpenMP Best Practices](#16-openmp-best-practices)

### Part 3: CUDA

17. [GPU Architecture Fundamentals](#17-gpu-architecture-fundamentals)
18. [CUDA Programming Model](#18-cuda-programming-model)
19. [CUDA Memory Model](#19-cuda-memory-model)
20. [Memory Optimization](#20-memory-optimization)
21. [Thread Synchronization and Cooperation](#21-thread-synchronization-and-cooperation)
22. [Streams, Events, and Concurrency](#22-streams-events-and-concurrency)
23. [Performance Optimization](#23-performance-optimization)
24. [Advanced CUDA](#24-advanced-cuda)

### Part 4: HIP (Heterogeneous-Compute Interface for Portability)

25. [HIP Fundamentals and Portability](#25-hip-fundamentals-and-portability)
26. [HIP Programming Model](#26-hip-programming-model)
27. [HIP Memory Management](#27-hip-memory-management)
28. [HIP Streams, Events, and Synchronization](#28-hip-streams-events-and-synchronization)
29. [CUDA-to-HIP Porting](#29-cuda-to-hip-porting)
30. [HIP Performance Tuning for AMD GPUs](#30-hip-performance-tuning-for-amd-gpus)
31. [ROCm Ecosystem and Libraries](#31-rocm-ecosystem-and-libraries)

### Part 5: Cross-Cutting Topics

32. [Hybrid Programming Patterns](#32-hybrid-programming-patterns)
33. [Comprehensive Comparison Tables](#33-comprehensive-comparison-tables)

### Part 6: Multi-GPU Communication and Portability

34. [Collective Communication Algorithms and Cost Model](#34-collective-communication-algorithms-and-cost-model)
35. [Multi-GPU Programming Beyond Peer Copies (HIP)](#35-multi-gpu-programming-beyond-peer-copies-hip)
36. [Portable Programming Models and AMD Wave-Level Primitives](#36-portable-programming-models-and-amd-wave-level-primitives)

---

# Part 1: MPI (Message Passing Interface)

---

# 1. MPI Fundamentals

---

## 1.1 Programming Model

MPI is a **distributed-memory** parallel programming standard. Each process has its own private address space, and processes communicate by explicitly sending and receiving messages over a network (or shared memory on the same node). MPI follows the **SPMD** (Single Program, Multiple Data) paradigm: all processes execute the same program but operate on different portions of the data, using their **rank** (unique integer ID) to determine their role.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Process 0│    │ Process 1│    │ Process 2│    │ Process 3│
│ (rank 0) │    │ (rank 1) │    │ (rank 2) │    │ (rank 3) │
│          │    │          │    │          │    │          │
│ Private  │    │ Private  │    │ Private  │    │ Private  │
│ Memory   │    │ Memory   │    │ Memory   │    │ Memory   │
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │               │
     └───────────────┴───────────────┴───────────────┘
                    Network / Interconnect
```

| Feature | MPI (Distributed Memory) | Shared Memory (e.g., Pthreads) | OpenMP (Shared Memory) |
|---|---|---|---|
| Memory model | Each process has private memory | All threads share address space | All threads share address space |
| Communication | Explicit messages (Send/Recv) | Read/write shared variables | Read/write shared variables |
| Synchronization | Messages, barriers, fences | Mutexes, condition variables | Directives (critical, barrier) |
| Scalability | Thousands of nodes | Single node | Single node (typically) |
| Data races | Impossible (no shared state) | Possible | Possible |
| Ease of use | More complex (explicit comms) | Moderate | Easiest (directive-based) |
| Typical hardware | Clusters, supercomputers | Multi-core CPUs | Multi-core CPUs |

## 1.2 Initialization and Finalization

Every MPI program must call `MPI_Init` before any other MPI call and `MPI_Finalize` at the end:

```c
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    printf("Hello from process %d of %d\n", rank, size);

    MPI_Finalize();
    return 0;
}
```

**Key rules:**
- `MPI_Init` must be called exactly once, before any other MPI function
- `MPI_Finalize` must be the last MPI call; no MPI calls are valid after it
- `MPI_Init` may modify `argc`/`argv` to strip MPI-specific arguments

### Thread Support Levels

For multithreaded MPI programs, use `MPI_Init_thread` instead:

```c
int provided;
MPI_Init_thread(&argc, &argv, MPI_THREAD_MULTIPLE, &provided);

if (provided < MPI_THREAD_MULTIPLE) {
    printf("Warning: MPI does not support full thread safety\n");
}
```

| Level | Value | Meaning |
|---|---|---|
| `MPI_THREAD_SINGLE` | 0 | Only one thread will execute |
| `MPI_THREAD_FUNNELED` | 1 | Multiple threads, but only the main thread makes MPI calls |
| `MPI_THREAD_SERIALIZED` | 2 | Multiple threads may make MPI calls, but only one at a time |
| `MPI_THREAD_MULTIPLE` | 3 | Multiple threads may make MPI calls concurrently |

## 1.3 Communicators, Rank, and Size

A **communicator** defines a group of processes that can communicate with each other. `MPI_COMM_WORLD` is the default communicator containing all processes.

```c
int rank, size;

MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // 0-based unique ID within communicator
MPI_Comm_size(MPI_COMM_WORLD, &size);  // total number of processes
```

- **Rank**: integer in range `[0, size-1]`, unique within a communicator
- **Size**: total number of processes in the communicator
- A process can belong to multiple communicators and have a different rank in each

## 1.4 Compilation and Execution

```bash
# Compile (C)
mpicc -o my_program my_program.c

# Compile (C++)
mpicxx -o my_program my_program.cpp

# Compile (Fortran)
mpifort -o my_program my_program.f90

# Run with 4 processes
mpirun -np 4 ./my_program

# Alternative launch command
mpiexec -n 4 ./my_program

# Run across multiple nodes (hostfile)
mpirun -np 16 --hostfile hosts.txt ./my_program
```

`mpicc`, `mpicxx`, and `mpifort` are wrapper scripts that add the correct include paths and link against the MPI library. They delegate to the underlying compiler (e.g., `gcc`, `g++`, `gfortran`).

> **See also:** in a CMake project, do not make `mpicxx` the compiler. Use `find_package(MPI REQUIRED COMPONENTS CXX)` and link `MPI::MPI_CXX`, as shown in [32.6 Building Hybrid MPI + OpenMP + HIP Code with CMake](#326-building-hybrid-mpi--openmp--hip-code-with-cmake). How Find modules work is covered in [CMake Fundamentals -- find_package](../tools/CMake_Fundamentals.md#28-find_package-module-mode-vs-config-mode).

## 1.5 MPI Program Structure Pattern

```c
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Divide work based on rank
    int N = 1000;
    int chunk = N / size;
    int start = rank * chunk;
    int end = (rank == size - 1) ? N : start + chunk;

    // Each process works on its portion
    double local_sum = 0.0;
    for (int i = start; i < end; i++) {
        local_sum += (double)i * i;
    }

    // Combine results
    double global_sum;
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        printf("Total sum = %f\n", global_sum);
    }

    MPI_Finalize();
    return 0;
}
```

---

# 2. Point-to-Point Communication

---

## 2.1 Blocking Communication

Blocking calls do not return until the operation is locally complete (the buffer can be safely reused).

### MPI_Send and MPI_Recv

```c
int MPI_Send(const void* buf, int count, MPI_Datatype datatype,
             int dest, int tag, MPI_Comm comm);

int MPI_Recv(void* buf, int count, MPI_Datatype datatype,
             int source, int tag, MPI_Comm comm, MPI_Status* status);
```

```c
if (rank == 0) {
    int data = 42;
    MPI_Send(&data, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
} else if (rank == 1) {
    int data;
    MPI_Status status;
    MPI_Recv(&data, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
    printf("Received: %d\n", data);  // 42
}
```

**Parameters:**
- `buf`: pointer to the data buffer
- `count`: number of elements (not bytes)
- `datatype`: MPI datatype of each element
- `dest`/`source`: rank of the target/source process
- `tag`: integer message tag (use `MPI_ANY_TAG` to match any tag)
- `comm`: communicator
- `status`: information about the received message (source, tag, count)

### MPI_Status

```c
MPI_Status status;
MPI_Recv(buf, max_count, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, comm, &status);

int actual_source = status.MPI_SOURCE;
int actual_tag    = status.MPI_TAG;
int actual_count;
MPI_Get_count(&status, MPI_INT, &actual_count);
```

### MPI_Sendrecv

Performs a send and receive simultaneously, avoiding deadlock in common exchange patterns:

```c
int MPI_Sendrecv(const void* sendbuf, int sendcount, MPI_Datatype sendtype,
                 int dest, int sendtag,
                 void* recvbuf, int recvcount, MPI_Datatype recvtype,
                 int source, int recvtag,
                 MPI_Comm comm, MPI_Status* status);
```

```c
// Ring exchange: each process sends to right neighbor, receives from left
int left  = (rank - 1 + size) % size;
int right = (rank + 1) % size;

int send_val = rank;
int recv_val;
MPI_Sendrecv(&send_val, 1, MPI_INT, right, 0,
             &recv_val, 1, MPI_INT, left,  0,
             MPI_COMM_WORLD, MPI_STATUS_IGNORE);
```

## 2.2 Communication Modes

MPI provides four send modes, each with different semantics regarding when the send can complete:

| Mode | Function | Completes When | Buffering |
|---|---|---|---|
| **Standard** | `MPI_Send` | Implementation-dependent (may buffer or synchronize) | May or may not buffer |
| **Buffered** | `MPI_Bsend` | Always returns immediately; data copied to user-supplied buffer | Always buffers |
| **Synchronous** | `MPI_Ssend` | Only when matching receive has started | Never buffers |
| **Ready** | `MPI_Rsend` | Matching receive must already be posted (undefined otherwise) | Never buffers |

```c
// Buffered send: user manages the buffer
int buf_size = MPI_BSEND_OVERHEAD + 100 * sizeof(int);
void* buffer = malloc(buf_size);
MPI_Buffer_attach(buffer, buf_size);

MPI_Bsend(data, 100, MPI_INT, dest, tag, comm);

MPI_Buffer_detach(&buffer, &buf_size);
free(buffer);

// Synchronous send: guaranteed handshake
MPI_Ssend(data, 100, MPI_INT, dest, tag, comm);
```

## 2.3 Non-Blocking Communication

Non-blocking calls return immediately with an `MPI_Request` handle. The actual communication happens in the background. The buffer must not be modified until the operation completes.

```c
int MPI_Isend(const void* buf, int count, MPI_Datatype datatype,
              int dest, int tag, MPI_Comm comm, MPI_Request* request);

int MPI_Irecv(void* buf, int count, MPI_Datatype datatype,
              int source, int tag, MPI_Comm comm, MPI_Request* request);
```

### Completion Functions

```c
int MPI_Wait(MPI_Request* request, MPI_Status* status);      // block until complete
int MPI_Test(MPI_Request* request, int* flag, MPI_Status* status); // non-blocking check

int MPI_Waitall(int count, MPI_Request requests[], MPI_Status statuses[]);
int MPI_Waitany(int count, MPI_Request requests[], int* index, MPI_Status* status);
int MPI_Waitsome(int count, MPI_Request requests[], int* outcount,
                 int indices[], MPI_Status statuses[]);
```

### Overlapping Communication and Computation

```c
double *send_buf, *recv_buf;
MPI_Request requests[2];

// Initiate non-blocking operations
MPI_Isend(send_buf, N, MPI_DOUBLE, dest, tag, comm, &requests[0]);
MPI_Irecv(recv_buf, N, MPI_DOUBLE, src,  tag, comm, &requests[1]);

// Perform independent computation while communication proceeds
compute_interior(local_data);

// Wait for communication to complete before using boundary data
MPI_Waitall(2, requests, MPI_STATUSES_IGNORE);

// Now safe to use recv_buf
compute_boundary(recv_buf, local_data);
```

## 2.4 Deadlock Scenarios and Prevention

### Common Deadlock Pattern

```c
// DEADLOCK: both processes try to send first
if (rank == 0) {
    MPI_Send(buf_a, N, MPI_INT, 1, 0, comm);  // blocked waiting for rank 1 to recv
    MPI_Recv(buf_b, N, MPI_INT, 1, 0, comm, &status);
} else if (rank == 1) {
    MPI_Send(buf_a, N, MPI_INT, 0, 0, comm);  // blocked waiting for rank 0 to recv
    MPI_Recv(buf_b, N, MPI_INT, 0, 0, comm, &status);
}
```

### Prevention Strategies

```c
// Strategy 1: Alternate send/recv order by rank
if (rank == 0) {
    MPI_Send(buf_a, N, MPI_INT, 1, 0, comm);
    MPI_Recv(buf_b, N, MPI_INT, 1, 0, comm, &status);
} else if (rank == 1) {
    MPI_Recv(buf_b, N, MPI_INT, 0, 0, comm, &status);  // recv first
    MPI_Send(buf_a, N, MPI_INT, 0, 0, comm);
}

// Strategy 2: Use MPI_Sendrecv
MPI_Sendrecv(buf_a, N, MPI_INT, partner, 0,
             buf_b, N, MPI_INT, partner, 0,
             comm, &status);

// Strategy 3: Use non-blocking calls
MPI_Isend(buf_a, N, MPI_INT, partner, 0, comm, &req[0]);
MPI_Irecv(buf_b, N, MPI_INT, partner, 0, comm, &req[1]);
MPI_Waitall(2, req, MPI_STATUSES_IGNORE);
```

| Strategy | Pros | Cons |
|---|---|---|
| Ordered Send/Recv | Simple, no extra buffers | Only works for simple patterns |
| `MPI_Sendrecv` | Deadlock-free, clean API | May internally buffer |
| Non-blocking | Most flexible, enables overlap | More complex (request management) |
| Buffered send | Always returns | User manages buffer memory |

---

# 3. Collective Communication

---

## 3.1 Overview

Collective operations involve **all processes** in a communicator. They are blocking by default (MPI-3 added non-blocking variants prefixed with `I`). The MPI implementation is free to use optimized algorithms (trees, rings, etc.).

**Rules:**
- All processes in the communicator must call the collective
- Tags are managed internally (no user tags)
- Collective and point-to-point calls do not interfere with each other

## 3.2 Broadcast

One process (root) sends data to all other processes:

```c
int MPI_Bcast(void* buffer, int count, MPI_Datatype datatype,
              int root, MPI_Comm comm);
```

```c
int data[100];
if (rank == 0) {
    // Root initializes the data
    for (int i = 0; i < 100; i++) data[i] = i;
}

// After this call, all processes have the same data
MPI_Bcast(data, 100, MPI_INT, 0, MPI_COMM_WORLD);
```

```
Before:  Rank 0: [A]    Rank 1: [?]    Rank 2: [?]    Rank 3: [?]
After:   Rank 0: [A]    Rank 1: [A]    Rank 2: [A]    Rank 3: [A]
```

## 3.3 Scatter and Gather

### MPI_Scatter

Root distributes equal-sized chunks of data to each process:

```c
int MPI_Scatter(const void* sendbuf, int sendcount, MPI_Datatype sendtype,
                void* recvbuf, int recvcount, MPI_Datatype recvtype,
                int root, MPI_Comm comm);
```

```c
int *global_data = NULL;
int local_data[25];

if (rank == 0) {
    global_data = malloc(100 * sizeof(int));
    for (int i = 0; i < 100; i++) global_data[i] = i;
}

// Each of 4 processes receives 25 elements
MPI_Scatter(global_data, 25, MPI_INT,
            local_data,  25, MPI_INT,
            0, MPI_COMM_WORLD);
```

```
Before (root):  [0..24 | 25..49 | 50..74 | 75..99]
After:   Rank 0: [0..24]   Rank 1: [25..49]   Rank 2: [50..74]   Rank 3: [75..99]
```

### MPI_Gather

Inverse of scatter: root collects equal-sized chunks from all processes:

```c
int MPI_Gather(const void* sendbuf, int sendcount, MPI_Datatype sendtype,
               void* recvbuf, int recvcount, MPI_Datatype recvtype,
               int root, MPI_Comm comm);
```

```c
int local_result = rank * 10;
int *all_results = NULL;
if (rank == 0) all_results = malloc(size * sizeof(int));

MPI_Gather(&local_result, 1, MPI_INT,
           all_results,   1, MPI_INT,
           0, MPI_COMM_WORLD);
// Root now has: [0, 10, 20, 30]
```

### MPI_Allgather

Every process receives the full gathered result (no root):

```c
int MPI_Allgather(const void* sendbuf, int sendcount, MPI_Datatype sendtype,
                  void* recvbuf, int recvcount, MPI_Datatype recvtype,
                  MPI_Comm comm);
```

```
Before:  Rank 0: [A]    Rank 1: [B]    Rank 2: [C]    Rank 3: [D]
After:   Rank 0: [ABCD] Rank 1: [ABCD] Rank 2: [ABCD] Rank 3: [ABCD]
```

## 3.4 Reduce Operations

### MPI_Reduce

Combines data from all processes using an operation, stores result at root:

```c
int MPI_Reduce(const void* sendbuf, void* recvbuf, int count,
               MPI_Datatype datatype, MPI_Op op, int root, MPI_Comm comm);
```

```c
double local_sum = compute_partial_sum(rank);
double global_sum;

MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

if (rank == 0) {
    printf("Global sum = %f\n", global_sum);
}
```

### Built-in Reduction Operations

| Operation | Meaning |
|---|---|
| `MPI_SUM` | Sum |
| `MPI_PROD` | Product |
| `MPI_MAX` | Maximum |
| `MPI_MIN` | Minimum |
| `MPI_MAXLOC` | Max value and location |
| `MPI_MINLOC` | Min value and location |
| `MPI_LAND` | Logical AND |
| `MPI_LOR` | Logical OR |
| `MPI_LXOR` | Logical XOR |
| `MPI_BAND` | Bitwise AND |
| `MPI_BOR` | Bitwise OR |
| `MPI_BXOR` | Bitwise XOR |

### MPI_Allreduce

Like `MPI_Reduce`, but the result is available to all processes:

```c
int MPI_Allreduce(const void* sendbuf, void* recvbuf, int count,
                  MPI_Datatype datatype, MPI_Op op, MPI_Comm comm);
```

```c
double local_val = rank + 1.0;
double global_max;

MPI_Allreduce(&local_val, &global_max, 1, MPI_DOUBLE, MPI_MAX, MPI_COMM_WORLD);
// All processes now know the global maximum
```

### MPI_Scan (Prefix Scan)

Inclusive prefix reduction -- process `i` receives the reduction of values from processes `0..i`:

```c
int MPI_Scan(const void* sendbuf, void* recvbuf, int count,
             MPI_Datatype datatype, MPI_Op op, MPI_Comm comm);
```

```c
int local_val = rank + 1;  // ranks 0,1,2,3 have values 1,2,3,4
int prefix_sum;

MPI_Scan(&local_val, &prefix_sum, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
// Rank 0: 1, Rank 1: 3, Rank 2: 6, Rank 3: 10
```

### User-Defined Reduction Operations

```c
void my_max_abs(void* invec, void* inoutvec, int* len, MPI_Datatype* type) {
    double* in    = (double*)invec;
    double* inout = (double*)inoutvec;
    for (int i = 0; i < *len; i++) {
        if (fabs(in[i]) > fabs(inout[i])) {
            inout[i] = in[i];
        }
    }
}

MPI_Op my_op;
MPI_Op_create(my_max_abs, 1 /* commutative */, &my_op);
MPI_Reduce(sendbuf, recvbuf, count, MPI_DOUBLE, my_op, 0, comm);
MPI_Op_free(&my_op);
```

## 3.5 All-to-All

Every process sends a distinct chunk to every other process:

```c
int MPI_Alltoall(const void* sendbuf, int sendcount, MPI_Datatype sendtype,
                 void* recvbuf, int recvcount, MPI_Datatype recvtype,
                 MPI_Comm comm);
```

```
4 processes, sendcount=1:
Send buffer at each rank: [to_rank0, to_rank1, to_rank2, to_rank3]

Before:  Rank 0: [a0,a1,a2,a3]  Rank 1: [b0,b1,b2,b3]  ...
After:   Rank 0: [a0,b0,c0,d0]  Rank 1: [a1,b1,c1,d1]  ...
```

## 3.6 Variable-Length Variants

For unequal data distributions:

```c
int MPI_Scatterv(const void* sendbuf, const int sendcounts[], const int displs[],
                 MPI_Datatype sendtype, void* recvbuf, int recvcount,
                 MPI_Datatype recvtype, int root, MPI_Comm comm);

int MPI_Gatherv(const void* sendbuf, int sendcount, MPI_Datatype sendtype,
                void* recvbuf, const int recvcounts[], const int displs[],
                MPI_Datatype recvtype, int root, MPI_Comm comm);
```

```c
// Distribute N elements unevenly across processes
int N = 103;
int base = N / size;
int remainder = N % size;

int *sendcounts = NULL, *displs = NULL;
if (rank == 0) {
    sendcounts = malloc(size * sizeof(int));
    displs     = malloc(size * sizeof(int));
    for (int i = 0; i < size; i++) {
        sendcounts[i] = base + (i < remainder ? 1 : 0);
        displs[i] = (i == 0) ? 0 : displs[i-1] + sendcounts[i-1];
    }
}

int local_count = base + (rank < remainder ? 1 : 0);
double* local_data = malloc(local_count * sizeof(double));

MPI_Scatterv(global_data, sendcounts, displs, MPI_DOUBLE,
             local_data, local_count, MPI_DOUBLE,
             0, MPI_COMM_WORLD);
```

## 3.7 Barrier

Blocks all processes until every process in the communicator has reached the barrier:

```c
MPI_Barrier(MPI_COMM_WORLD);
```

Use sparingly -- barriers are synchronization points that can hurt performance. Prefer non-blocking collectives or point-to-point synchronization when possible.

## 3.8 Non-Blocking Collectives (MPI-3)

All collectives have non-blocking variants (prefixed with `I`):

```c
MPI_Request req;
MPI_Iallreduce(&local, &global, 1, MPI_DOUBLE, MPI_SUM, comm, &req);
// ... do other work ...
MPI_Wait(&req, MPI_STATUS_IGNORE);
```

## 3.9 Collective Operations Summary

| Operation | Root? | Data Flow | Result Location |
|---|---|---|---|
| `MPI_Bcast` | Yes | Root → All | All processes |
| `MPI_Scatter` | Yes | Root → All (split) | Each process gets a piece |
| `MPI_Gather` | Yes | All → Root (join) | Root only |
| `MPI_Allgather` | No | All → All (join) | All processes |
| `MPI_Reduce` | Yes | All → Root (combine) | Root only |
| `MPI_Allreduce` | No | All → All (combine) | All processes |
| `MPI_Scan` | No | Prefix reduction | Process i gets reduction of 0..i |
| `MPI_Alltoall` | No | All → All (transpose) | All processes |
| `MPI_Barrier` | No | Synchronization only | N/A |

> **See also:** [Collective Communication Algorithms and Cost Model](#34-collective-communication-algorithms-and-cost-model) for how these collectives are implemented (ring, tree, recursive doubling), the alpha-beta cost derivations, and the GPU collective libraries (NCCL/RCCL).

---

# 4. MPI Data Types and Derived Types

---

## 4.1 Predefined Types

MPI defines types that correspond to C/C++ types:

| MPI Type | C Type |
|---|---|
| `MPI_CHAR` | `char` |
| `MPI_SHORT` | `short` |
| `MPI_INT` | `int` |
| `MPI_LONG` | `long` |
| `MPI_LONG_LONG` | `long long` |
| `MPI_UNSIGNED` | `unsigned int` |
| `MPI_FLOAT` | `float` |
| `MPI_DOUBLE` | `double` |
| `MPI_LONG_DOUBLE` | `long double` |
| `MPI_BYTE` | 1 byte (raw, no conversion) |
| `MPI_PACKED` | Packed data |

## 4.2 Derived Datatypes

Derived types allow sending non-contiguous or heterogeneous data without packing into a temporary buffer.

### Contiguous

A block of consecutive elements of the same type:

```c
MPI_Datatype row_type;
MPI_Type_contiguous(N, MPI_DOUBLE, &row_type);
MPI_Type_commit(&row_type);

MPI_Send(matrix[row], 1, row_type, dest, tag, comm);

MPI_Type_free(&row_type);
```

### Vector

Strided blocks of elements (e.g., a column of a row-major matrix):

```c
MPI_Datatype col_type;
// count=N blocks, blocklength=1 element each, stride=M elements apart
MPI_Type_vector(N, 1, M, MPI_DOUBLE, &col_type);
MPI_Type_commit(&col_type);

// Send column `col` of an N×M matrix stored row-major
MPI_Send(&matrix[0][col], 1, col_type, dest, tag, comm);

MPI_Type_free(&col_type);
```

### Struct

Heterogeneous data with varying types and arbitrary displacements:

```c
typedef struct {
    int    id;
    double x, y;
    char   label;
} Particle;

MPI_Datatype particle_type;
int          block_lengths[3] = {1, 2, 1};
MPI_Aint     displacements[3];
MPI_Datatype types[3] = {MPI_INT, MPI_DOUBLE, MPI_CHAR};

Particle p;
MPI_Aint base_addr;
MPI_Get_address(&p,       &base_addr);
MPI_Get_address(&p.id,    &displacements[0]);
MPI_Get_address(&p.x,     &displacements[1]);
MPI_Get_address(&p.label, &displacements[2]);

displacements[0] -= base_addr;
displacements[1] -= base_addr;
displacements[2] -= base_addr;

MPI_Type_create_struct(3, block_lengths, displacements, types, &particle_type);

// Handle padding: resize to match sizeof(Particle)
MPI_Datatype resized_type;
MPI_Type_create_resized(particle_type, 0, sizeof(Particle), &resized_type);
MPI_Type_commit(&resized_type);

Particle particles[100];
MPI_Send(particles, 100, resized_type, dest, tag, comm);

MPI_Type_free(&resized_type);
MPI_Type_free(&particle_type);
```

### Indexed

Variable-length blocks at variable displacements:

```c
int block_lengths[] = {3, 2, 4};
int displacements[] = {0, 5, 10};

MPI_Datatype indexed_type;
MPI_Type_indexed(3, block_lengths, displacements, MPI_DOUBLE, &indexed_type);
MPI_Type_commit(&indexed_type);
// Sends elements at positions: 0,1,2, 5,6, 10,11,12,13
```

### Subarray

For multi-dimensional array slices:

```c
int array_size[2]    = {100, 100};   // full array dimensions
int subarray_size[2] = {50, 50};     // subarray dimensions
int start[2]         = {25, 25};     // starting coordinates

MPI_Datatype subarray_type;
MPI_Type_create_subarray(2, array_size, subarray_size, start,
                         MPI_ORDER_C, MPI_DOUBLE, &subarray_type);
MPI_Type_commit(&subarray_type);
```

## 4.3 Packing and Unpacking

An alternative to derived types: manually pack data into a contiguous buffer.

```c
int position = 0;
char buffer[1000];

int    id = 42;
double coords[3] = {1.0, 2.0, 3.0};

MPI_Pack(&id,     1, MPI_INT,    buffer, 1000, &position, comm);
MPI_Pack(coords,  3, MPI_DOUBLE, buffer, 1000, &position, comm);

MPI_Send(buffer, position, MPI_PACKED, dest, tag, comm);

// Receiving side
MPI_Recv(buffer, 1000, MPI_PACKED, src, tag, comm, &status);
position = 0;
MPI_Unpack(buffer, 1000, &position, &id,     1, MPI_INT,    comm);
MPI_Unpack(buffer, 1000, &position, coords,  3, MPI_DOUBLE, comm);
```

| Approach | Pros | Cons |
|---|---|---|
| Derived types | Zero-copy, reusable, MPI can optimize | More complex setup |
| Pack/Unpack | Simple, flexible | Extra copy, manual buffer management |

---

# 5. Communicator Management and Topologies

---

## 5.1 Splitting Communicators

`MPI_Comm_split` partitions processes into non-overlapping sub-communicators:

```c
int MPI_Comm_split(MPI_Comm comm, int color, int key, MPI_Comm* newcomm);
```

```c
// Split into row communicators for a 2D process grid
int rows = 4, cols = 4;
int my_row = rank / cols;
int my_col = rank % cols;

MPI_Comm row_comm;
MPI_Comm_split(MPI_COMM_WORLD, my_row, my_col, &row_comm);
// Processes with the same `color` (my_row) end up in the same communicator
// `key` (my_col) determines the rank ordering within the new communicator

MPI_Comm col_comm;
MPI_Comm_split(MPI_COMM_WORLD, my_col, my_row, &col_comm);

// Use MPI_UNDEFINED to exclude a process from any new communicator
MPI_Comm worker_comm;
int color = (rank == 0) ? MPI_UNDEFINED : 1;
MPI_Comm_split(MPI_COMM_WORLD, color, rank, &worker_comm);
// rank 0 gets MPI_COMM_NULL

// Always free communicators when done
if (worker_comm != MPI_COMM_NULL)
    MPI_Comm_free(&worker_comm);
```

### Other Communicator Operations

```c
MPI_Comm new_comm;
MPI_Comm_dup(MPI_COMM_WORLD, &new_comm);   // duplicate (independent message space)
MPI_Comm_free(&new_comm);                  // release resources
```

## 5.2 Cartesian Topologies

Map processes onto a multi-dimensional grid for structured communication patterns:

```c
int dims[2]    = {4, 4};   // 4×4 grid
int periods[2] = {0, 1};   // non-periodic in dim 0, periodic in dim 1
int reorder    = 1;         // allow MPI to reorder ranks for better mapping

MPI_Comm cart_comm;
MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, reorder, &cart_comm);

// Get coordinates of this process
int coords[2];
MPI_Cart_coords(cart_comm, rank, 2, coords);

// Get rank from coordinates
int target_rank;
int target_coords[2] = {1, 2};
MPI_Cart_rank(cart_comm, target_coords, &target_rank);

// Shift: find neighbors along a given dimension
int left, right, up, down;
MPI_Cart_shift(cart_comm, 0, 1, &up,   &down);   // dimension 0, displacement 1
MPI_Cart_shift(cart_comm, 1, 1, &left, &right);  // dimension 1, displacement 1
// Returns MPI_PROC_NULL for non-existent neighbors (safe to send/recv with)
```

### Dimension Helper

Let MPI choose optimal dimensions for a given number of processes:

```c
int dims[2] = {0, 0};
MPI_Dims_create(16, 2, dims);  // 16 processes in 2D -> dims = {4, 4}
```

## 5.3 Graph Topologies

For irregular communication patterns:

```c
// 4 processes with adjacency: 0-1, 0-2, 1-3, 2-3
int index[4]   = {2, 3, 5, 6};     // cumulative degree: process i has edges in edges[index[i-1]..index[i]-1]
int edges[6]   = {1, 2, 3, 0, 3, 1}; // adjacency list

MPI_Comm graph_comm;
MPI_Graph_create(MPI_COMM_WORLD, 4, index, edges, 0, &graph_comm);
```

MPI-3 introduced `MPI_Dist_graph_create_adjacent` for scalable distributed graph topologies where each process only specifies its own neighbors.

## 5.4 Intercommunicators vs Intracommunicators

| Feature | Intracommunicator | Intercommunicator |
|---|---|---|
| Groups | Single group of processes | Two distinct groups |
| Point-to-point | Ranks within same group | Ranks address processes in the other group |
| Collectives | All processes in the group | Varies by operation |
| Example | `MPI_COMM_WORLD`, result of `MPI_Comm_split` | Result of `MPI_Intercomm_create`, `MPI_Comm_spawn` |

---

# 6. One-Sided Communication (RMA)

---

## 6.1 Overview

One-sided (Remote Memory Access) communication allows a process to read/write another process's memory without the remote process explicitly participating. This decouples data movement from synchronization.

```
Two-sided:                          One-sided:
  Process A      Process B            Process A      Process B
  MPI_Send  -->  MPI_Recv             MPI_Put   --> [Window]
  (both participate)                  (only A actively participates)
```

## 6.2 Window Creation

A **window** exposes a region of memory for remote access:

```c
// Create window from existing buffer
double* data = malloc(N * sizeof(double));
MPI_Win win;
MPI_Win_create(data, N * sizeof(double), sizeof(double), MPI_INFO_NULL, comm, &win);

// Allocate window memory (MPI manages allocation)
double* win_data;
MPI_Win_allocate(N * sizeof(double), sizeof(double), MPI_INFO_NULL, comm, &win_data, &win);

// Shared memory window (for processes on the same node)
MPI_Win_allocate_shared(N * sizeof(double), sizeof(double), MPI_INFO_NULL, comm, &win_data, &win);

// Dynamic window (attach/detach memory later)
MPI_Win_create_dynamic(MPI_INFO_NULL, comm, &win);
MPI_Win_attach(win, data, N * sizeof(double));
// ... later ...
MPI_Win_detach(win, data);

MPI_Win_free(&win);
```

## 6.3 RMA Operations

```c
// Put: write to remote window
MPI_Put(origin_buf, count, MPI_DOUBLE,
        target_rank, target_disp, target_count, MPI_DOUBLE, win);

// Get: read from remote window
MPI_Get(origin_buf, count, MPI_DOUBLE,
        target_rank, target_disp, target_count, MPI_DOUBLE, win);

// Accumulate: remote update with reduction
MPI_Accumulate(origin_buf, count, MPI_DOUBLE,
               target_rank, target_disp, target_count, MPI_DOUBLE,
               MPI_SUM, win);

// Get_accumulate: atomic read-modify-write
MPI_Get_accumulate(origin_buf, count, MPI_DOUBLE,
                   result_buf, count, MPI_DOUBLE,
                   target_rank, target_disp, target_count, MPI_DOUBLE,
                   MPI_SUM, win);

// Compare_and_swap: atomic CAS
MPI_Compare_and_swap(origin, compare, result, MPI_INT,
                     target_rank, target_disp, win);

// Fetch_and_op: atomic fetch-and-operate
MPI_Fetch_and_op(origin, result, MPI_INT, target_rank, target_disp, MPI_SUM, win);
```

## 6.4 Synchronization Modes

RMA operations are only guaranteed to be complete after synchronization:

### Fence (Active Target)

Collective synchronization -- simplest but least flexible:

```c
MPI_Win_fence(0, win);
// RMA operations here
MPI_Put(buf, 10, MPI_DOUBLE, target, 0, 10, MPI_DOUBLE, win);
MPI_Win_fence(0, win);
// Data is now visible
```

### Lock/Unlock (Passive Target)

No participation from the target process required:

```c
MPI_Win_lock(MPI_LOCK_EXCLUSIVE, target_rank, 0, win);
MPI_Put(buf, 10, MPI_DOUBLE, target_rank, 0, 10, MPI_DOUBLE, win);
MPI_Win_unlock(target_rank, win);

// Shared lock allows concurrent reads
MPI_Win_lock(MPI_LOCK_SHARED, target_rank, 0, win);
MPI_Get(buf, 10, MPI_DOUBLE, target_rank, 0, 10, MPI_DOUBLE, win);
MPI_Win_unlock(target_rank, win);

// Lock all: lock all processes at once
MPI_Win_lock_all(0, win);
MPI_Get(buf, 10, MPI_DOUBLE, target_rank, 0, 10, MPI_DOUBLE, win);
MPI_Win_flush(target_rank, win);  // ensure completion without unlock
MPI_Win_unlock_all(win);
```

### Post-Start-Complete-Wait (PSCW)

Fine-grained synchronization between specific pairs:

```c
MPI_Group group;
MPI_Comm_group(comm, &group);

// Target side: expose window to origin processes
MPI_Win_post(origin_group, 0, win);
// ... target can do local work ...
MPI_Win_wait(win);

// Origin side: access target windows
MPI_Win_start(target_group, 0, win);
MPI_Put(buf, 10, MPI_DOUBLE, target, 0, 10, MPI_DOUBLE, win);
MPI_Win_complete(win);
```

| Synchronization | Type | Target Participates? | Collective? | Use Case |
|---|---|---|---|---|
| Fence | Active | Yes | Yes (all in comm) | BSP-style bulk phases |
| Lock/Unlock | Passive | No | No | Irregular, asynchronous access |
| PSCW | Active | Yes | No (pairs) | Fine-grained producer-consumer |

---

# 7. MPI I/O (Parallel File I/O)

---

## 7.1 Overview

MPI I/O (also called MPI-IO or ROMIO) provides portable, high-performance parallel file access. Multiple processes can read/write a shared file concurrently.

## 7.2 File Operations

```c
MPI_File fh;

// Open
MPI_File_open(MPI_COMM_WORLD, "output.dat",
              MPI_MODE_CREATE | MPI_MODE_WRONLY,
              MPI_INFO_NULL, &fh);

// Write at explicit offset
MPI_Offset offset = rank * N * sizeof(double);
MPI_File_write_at(fh, offset, local_data, N, MPI_DOUBLE, MPI_STATUS_IGNORE);

// Close
MPI_File_close(&fh);
```

### File Access Modes

| Mode | Meaning |
|---|---|
| `MPI_MODE_RDONLY` | Read only |
| `MPI_MODE_WRONLY` | Write only |
| `MPI_MODE_RDWR` | Read and write |
| `MPI_MODE_CREATE` | Create file if it does not exist |
| `MPI_MODE_EXCL` | Error if file already exists (with CREATE) |
| `MPI_MODE_DELETE_ON_CLOSE` | Delete file when closed |
| `MPI_MODE_APPEND` | Set initial position to end of file |

## 7.3 File Views

A **view** defines each process's visible portion of the file, enabling complex data partitioning:

```c
MPI_File_set_view(fh, disp, etype, filetype, "native", MPI_INFO_NULL);
```

```c
// Each process writes every `size`-th element (interleaved)
MPI_Datatype filetype;
MPI_Type_vector(N/size, 1, size, MPI_DOUBLE, &filetype);
MPI_Type_commit(&filetype);

MPI_Offset disp = rank * sizeof(double);
MPI_File_set_view(fh, disp, MPI_DOUBLE, filetype, "native", MPI_INFO_NULL);
MPI_File_write(fh, local_data, N/size, MPI_DOUBLE, MPI_STATUS_IGNORE);

MPI_Type_free(&filetype);
```

## 7.4 Collective vs Independent I/O

```c
// Independent: each process performs I/O independently
MPI_File_write_at(fh, offset, buf, count, MPI_DOUBLE, &status);

// Collective: all processes call together (enables optimizations)
MPI_File_write_at_all(fh, offset, buf, count, MPI_DOUBLE, &status);
```

Collective I/O allows the MPI implementation to aggregate small requests and reorder access patterns for better performance (two-phase I/O).

| Approach | Function Suffix | Performance | When to Use |
|---|---|---|---|
| Independent | (none) | Lower (many small I/Os) | Irregular, infrequent access |
| Collective | `_all` | Higher (aggregation) | Regular patterns, large-scale I/O |

---

# 8. Advanced MPI Topics

---

## 8.1 Dynamic Process Management

```c
MPI_Comm intercomm;
int errcodes[4];

// Spawn 4 new worker processes
MPI_Comm_spawn("./worker", MPI_ARGV_NULL, 4,
               MPI_INFO_NULL, 0, MPI_COMM_WORLD,
               &intercomm, errcodes);

// In the spawned worker program:
MPI_Comm parent_comm;
MPI_Comm_get_parent(&parent_comm);
if (parent_comm != MPI_COMM_NULL) {
    // This is a spawned process
}
```

## 8.2 Error Handling

By default, MPI aborts on errors. You can change this:

```c
// Set error handler to return errors instead of aborting
MPI_Comm_set_errhandler(MPI_COMM_WORLD, MPI_ERRORS_RETURN);

int err = MPI_Send(buf, count, MPI_INT, dest, tag, comm);
if (err != MPI_SUCCESS) {
    char error_string[MPI_MAX_ERROR_STRING];
    int len;
    MPI_Error_string(err, error_string, &len);
    fprintf(stderr, "MPI Error: %s\n", error_string);
}
```

## 8.3 Performance Best Practices

| Technique | Description |
|---|---|
| **Latency hiding** | Use non-blocking calls to overlap communication with computation |
| **Message aggregation** | Combine many small messages into fewer large ones |
| **Derived datatypes** | Avoid unnecessary packing; let MPI handle non-contiguous data |
| **Collective optimization** | Use collective calls instead of manual point-to-point trees |
| **Load balancing** | Distribute work evenly; consider dynamic scheduling |
| **Topology-aware mapping** | Use Cartesian topologies to match communication to network layout |
| **Avoid barriers** | Replace `MPI_Barrier` with point-to-point synchronization where possible |
| **Non-blocking collectives** | Overlap collective operations with computation (MPI-3) |

## 8.4 Hybrid MPI + OpenMP

```c
int provided;
MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);

int rank;
MPI_Comm_rank(MPI_COMM_WORLD, &rank);

#pragma omp parallel
{
    int tid = omp_get_thread_num();
    // Each thread works on its portion
    compute_chunk(local_data, tid);
}

// Only the main thread makes MPI calls (FUNNELED)
MPI_Allreduce(MPI_IN_PLACE, local_data, N, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

MPI_Finalize();
```

## 8.5 Hybrid MPI + CUDA

```c
MPI_Init(&argc, &argv);
int rank;
MPI_Comm_rank(MPI_COMM_WORLD, &rank);

// Assign GPU based on local rank
cudaSetDevice(rank % num_gpus);

double *d_data;
cudaMalloc(&d_data, N * sizeof(double));

// Launch kernel
my_kernel<<<blocks, threads>>>(d_data, N);

// With CUDA-aware MPI: pass device pointers directly
MPI_Sendrecv(d_data, N, MPI_DOUBLE, partner, 0,
             d_recv,  N, MPI_DOUBLE, partner, 0,
             MPI_COMM_WORLD, MPI_STATUS_IGNORE);

// Without CUDA-aware MPI: must copy to host first
cudaMemcpy(h_data, d_data, N * sizeof(double), cudaMemcpyDeviceToHost);
MPI_Sendrecv(h_data, N, MPI_DOUBLE, partner, 0, ...);
```

---

## Common Interview Questions -- MPI

**Q: What is the difference between `MPI_Send` and `MPI_Ssend`?**

`MPI_Send` uses standard mode where the MPI implementation decides whether to buffer the message or synchronize with the receiver. For small messages it typically buffers (copies data to an internal buffer and returns immediately); for large messages it may block until the receiver posts a matching `MPI_Recv`. `MPI_Ssend` (synchronous send) always blocks until the receiver has started the matching receive, guaranteeing a handshake. This makes `MPI_Ssend` useful for debugging (it exposes deadlocks that `MPI_Send` might hide through buffering) but potentially slower.

**Q: How do you avoid deadlock in MPI?**

Common strategies: (1) Order send/recv operations so that for any pair, one process sends first while the other receives first. (2) Use `MPI_Sendrecv`, which handles both operations atomically. (3) Use non-blocking calls (`MPI_Isend`/`MPI_Irecv`) that return immediately, followed by `MPI_Waitall`. (4) Use buffered sends (`MPI_Bsend`) so sends never block. The classic deadlock pattern is when two processes both call `MPI_Send` to each other before either calls `MPI_Recv`.

**Q: What is the difference between `MPI_Reduce` and `MPI_Allreduce`?**

Both combine values from all processes using an operation (sum, max, etc.), but `MPI_Reduce` stores the result only at the root process, while `MPI_Allreduce` distributes the result to all processes. `MPI_Allreduce` is equivalent to `MPI_Reduce` followed by `MPI_Bcast`, but implementations can be more efficient (e.g., using a recursive doubling algorithm).

**Q: Why use derived datatypes instead of `MPI_Pack`/`MPI_Unpack`?**

Derived datatypes are zero-copy -- MPI reads non-contiguous data directly from the source buffer during the send. `MPI_Pack` requires an explicit copy into a contiguous buffer before sending, doubling memory usage and adding overhead. Derived types are also reusable and allow MPI to apply platform-specific optimizations (e.g., RDMA scatter/gather). Use `MPI_Pack` only when the data layout is truly dynamic and cannot be described by a single derived type.

**Q: When would you use one-sided communication over two-sided?**

One-sided (RMA) is advantageous when: (1) the data access pattern is irregular or data-dependent (e.g., hash table lookups across processes), making it hard to predict which processes need to communicate; (2) you want to decouple data movement from synchronization for better overlap; (3) the target process is busy computing and should not be interrupted. Two-sided is simpler and performs well for regular, predictable communication patterns.

**Q: Explain the concept of communicators and why they are important.**

A communicator encapsulates a group of processes and a communication context. They prevent message interference between different libraries or phases of a program -- messages sent in one communicator cannot be received in another, even if the processes overlap. `MPI_COMM_WORLD` includes all processes, but you can create sub-communicators with `MPI_Comm_split` to isolate groups (e.g., row/column communicators for matrix operations). Libraries should `MPI_Comm_dup` the user's communicator to get a private context.

---

# Part 2: OpenMP

---

# 9. OpenMP Fundamentals

---

## 9.1 Fork-Join Execution Model

OpenMP uses a **fork-join** model: the program starts with a single **master thread**. When it encounters a parallel region, it forks a **team of threads**. At the end of the region, threads join back and only the master continues.

```
Master thread ─────┬──── Thread 0 ────┬───── Master thread ──────
                   ├──── Thread 1 ────┤
                   ├──── Thread 2 ────┤
                   └──── Thread 3 ────┘
                   Fork              Join
```

All threads in the team execute the same code in the parallel region. Work-sharing constructs distribute iterations or sections among them.

## 9.2 Basic Parallel Region

```c
#include <omp.h>
#include <stdio.h>

int main() {
    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        int nthreads = omp_get_num_threads();
        printf("Thread %d of %d\n", tid, nthreads);
    }
    // Implicit barrier and join here
    return 0;
}
```

### Compilation

```bash
# GCC
gcc -fopenmp -o program program.c

# Clang
clang -fopenmp -o program program.c

# Intel (icx)
icx -fiopenmp -o program program.c

# MSVC
cl /openmp program.c
```

> **See also:** in CMake, use `find_package(OpenMP REQUIRED COMPONENTS CXX)` and `target_link_libraries(app PRIVATE OpenMP::OpenMP_CXX)`. The flag is applied only to CXX sources, so OpenMP pragmas in `.hip` files are silently ignored. See [32.6](#326-building-hybrid-mpi--openmp--hip-code-with-cmake).

## 9.3 Controlling Thread Count

```c
// Method 1: Environment variable (highest priority for default)
// export OMP_NUM_THREADS=8

// Method 2: Runtime function (before parallel region)
omp_set_num_threads(8);

// Method 3: Clause on directive (highest priority)
#pragma omp parallel num_threads(4)
{
    // Exactly 4 threads here
}
```

## 9.4 Runtime Library Functions

| Function | Description |
|---|---|
| `omp_get_thread_num()` | Current thread's ID (0-based) |
| `omp_get_num_threads()` | Number of threads in the current team |
| `omp_get_max_threads()` | Max threads available for next parallel region |
| `omp_get_num_procs()` | Number of available processors |
| `omp_set_num_threads(n)` | Set default number of threads |
| `omp_in_parallel()` | Returns non-zero if inside a parallel region |
| `omp_set_nested(1)` | Enable nested parallelism (deprecated in 5.0; use `omp_set_max_active_levels`) |
| `omp_get_wtime()` | Wall clock time in seconds (for benchmarking) |
| `omp_get_wtick()` | Timer resolution in seconds |

## 9.5 Key Environment Variables

| Variable | Description | Example |
|---|---|---|
| `OMP_NUM_THREADS` | Default number of threads | `OMP_NUM_THREADS=8` |
| `OMP_SCHEDULE` | Default loop schedule | `OMP_SCHEDULE="dynamic,100"` |
| `OMP_PROC_BIND` | Thread binding policy | `OMP_PROC_BIND=close` |
| `OMP_PLACES` | Thread placement | `OMP_PLACES=cores` |
| `OMP_STACKSIZE` | Stack size per thread | `OMP_STACKSIZE=64M` |
| `OMP_NESTED` | Enable nested parallelism | `OMP_NESTED=true` |
| `OMP_MAX_ACTIVE_LEVELS` | Max nesting depth | `OMP_MAX_ACTIVE_LEVELS=2` |
| `OMP_DISPLAY_ENV` | Print OpenMP settings | `OMP_DISPLAY_ENV=true` |

## 9.6 Conditional Parallelism

```c
// Only create threads if N is large enough to justify overhead
#pragma omp parallel for if(N > 1000)
for (int i = 0; i < N; i++) {
    work(i);
}
```

---

# 10. Work-Sharing Constructs

---

## 10.1 Parallel For

Distributes loop iterations among threads:

```c
#pragma omp parallel for
for (int i = 0; i < N; i++) {
    a[i] = b[i] + c[i];
}

// Equivalent expanded form:
#pragma omp parallel
{
    #pragma omp for
    for (int i = 0; i < N; i++) {
        a[i] = b[i] + c[i];
    }
}
```

**Loop restrictions:** The loop must be a canonical form -- the iteration variable is integer, the bounds and increment are loop-invariant, and comparison uses `<`, `<=`, `>`, or `>=`.

## 10.2 Schedule Clause

Controls how iterations are assigned to threads:

```c
#pragma omp parallel for schedule(static)
#pragma omp parallel for schedule(static, 100)
#pragma omp parallel for schedule(dynamic)
#pragma omp parallel for schedule(dynamic, 50)
#pragma omp parallel for schedule(guided)
#pragma omp parallel for schedule(guided, 10)
#pragma omp parallel for schedule(auto)
#pragma omp parallel for schedule(runtime)  // determined by OMP_SCHEDULE
```

| Schedule | Chunk Assignment | Overhead | Best For |
|---|---|---|---|
| `static` | Equal contiguous blocks (round-robin if chunk given) | Lowest | Uniform workload, good cache locality |
| `static,k` | Round-robin in chunks of k | Low | Mostly uniform, small imbalance |
| `dynamic` | Threads grab chunks on demand | Higher | Variable workload per iteration |
| `dynamic,k` | Threads grab k iterations at a time | Moderate | Variable workload, reduce overhead |
| `guided` | Decreasing chunk sizes (starts large) | Moderate | Variable workload, fewer scheduling events |
| `guided,k` | Decreasing chunks, min size k | Moderate | Variable workload with min granularity |
| `auto` | Implementation decides | Varies | Let the runtime optimize |
| `runtime` | Set by `OMP_SCHEDULE` at runtime | Varies | Tuning without recompilation |

### Example: Load-Imbalanced Work

```c
// Dynamic scheduling handles iterations with varying cost
#pragma omp parallel for schedule(dynamic, 10)
for (int i = 0; i < N; i++) {
    // Cost depends on i (e.g., triangular matrix operations)
    for (int j = 0; j < i; j++) {
        process(i, j);
    }
}
```

## 10.3 Collapse Clause

Combines nested loops into a single iteration space for better load balancing:

```c
// Without collapse: only outer loop is parallelized
#pragma omp parallel for
for (int i = 0; i < M; i++) {
    for (int j = 0; j < N; j++) {
        matrix[i][j] = compute(i, j);
    }
}

// With collapse: M*N iterations are distributed across threads
#pragma omp parallel for collapse(2)
for (int i = 0; i < M; i++) {
    for (int j = 0; j < N; j++) {
        matrix[i][j] = compute(i, j);
    }
}
```

`collapse` is especially useful when the outer loop has too few iterations to keep all threads busy.

## 10.4 Sections

Assigns different code blocks to different threads (functional parallelism):

```c
#pragma omp parallel sections
{
    #pragma omp section
    {
        compute_fft(data_a);
    }
    #pragma omp section
    {
        compute_fft(data_b);
    }
    #pragma omp section
    {
        compute_fft(data_c);
    }
}
// Implicit barrier at end
```

Limitations: the number of sections is fixed at compile time; cannot scale dynamically with thread count.

## 10.5 Single and Master

```c
#pragma omp parallel
{
    // All threads execute this
    compute_local();

    #pragma omp single
    {
        // Exactly one thread executes this (implementation chooses which)
        printf("Intermediate result\n");
    }
    // Implicit barrier after single (unless `nowait` is used)

    #pragma omp master
    {
        // Only the master thread (thread 0) executes this
        printf("Master thread reporting\n");
    }
    // No implicit barrier after master

    // All threads continue
    compute_more();
}
```

| Construct | Which Thread | Implicit Barrier | `nowait` Allowed |
|---|---|---|---|
| `single` | Any one (implementation picks) | Yes | Yes |
| `master` | Only thread 0 | No | No |
| `masked` (OpenMP 5.1) | Specified thread (default 0) | No | No |

## 10.6 Nowait Clause

Removes the implicit barrier at the end of a work-sharing construct:

```c
#pragma omp parallel
{
    #pragma omp for nowait
    for (int i = 0; i < N; i++) {
        a[i] = expensive(i);
    }

    // Threads that finish early can start this immediately
    #pragma omp for
    for (int i = 0; i < N; i++) {
        b[i] = cheap(a[i]);  // careful: a[i] might not be computed yet by another thread!
    }
}
```

Use `nowait` only when there are no data dependencies between consecutive work-sharing regions.

---

# 11. Data Environment and Scoping

---

## 11.1 Data-Sharing Clauses

| Clause | Meaning | Initialization | Final Value |
|---|---|---|---|
| `shared(x)` | All threads share the same variable | Original value | Modified by all threads |
| `private(x)` | Each thread gets its own uninitialized copy | **Undefined** | Lost (original unchanged) |
| `firstprivate(x)` | Each thread gets a copy initialized from original | **Copy of original** | Lost (original unchanged) |
| `lastprivate(x)` | Like private, but the value from the last iteration is written back | **Undefined** | Value from sequentially last iteration |
| `threadprivate` | Global/static variable replicated per thread | Persists across parallel regions | Persists |

```c
int x = 10, y = 20, z = 30, w = 0;

#pragma omp parallel for private(x) firstprivate(y) lastprivate(w) shared(z)
for (int i = 0; i < 100; i++) {
    // x is undefined at start of each thread's first iteration
    // y starts as 20 in each thread
    // z is shared -- all threads see the same z (need synchronization for writes)
    x = i;
    w = i + y;
    // z += x;  // data race without synchronization!
}
// After: x is still 10 (original), y is still 20, z is shared (possibly modified)
// w = 99 + 20 = 119 (from the last iteration i=99)
```

## 11.2 Reduction Clause

Safely combines values from all threads:

```c
double sum = 0.0;
double max_val = -1e30;

#pragma omp parallel for reduction(+:sum) reduction(max:max_val)
for (int i = 0; i < N; i++) {
    sum += data[i];
    if (data[i] > max_val) max_val = data[i];
}
// sum and max_val contain correct results (no data race)
```

### Built-in Reduction Operators

| Operator | Identity Value | Meaning |
|---|---|---|
| `+` | 0 | Sum |
| `-` | 0 | Subtraction (treated as addition of negation) |
| `*` | 1 | Product |
| `&` | ~0 | Bitwise AND |
| `\|` | 0 | Bitwise OR |
| `^` | 0 | Bitwise XOR |
| `&&` | 1 | Logical AND |
| `\|\|` | 0 | Logical OR |
| `max` | Smallest representable | Maximum |
| `min` | Largest representable | Minimum |

### User-Defined Reduction (OpenMP 4.0+)

```c
typedef struct { double re, im; } Complex;

// Declare a custom reduction
#pragma omp declare reduction(complex_add : Complex : \
    omp_out.re += omp_in.re, omp_out.im += omp_in.im) \
    initializer(omp_priv = {0.0, 0.0})

Complex total = {0.0, 0.0};
#pragma omp parallel for reduction(complex_add : total)
for (int i = 0; i < N; i++) {
    total.re += data[i].re;
    total.im += data[i].im;
}
```

## 11.3 Default Clause

```c
// All variables default to shared (the actual default if no clause given)
#pragma omp parallel default(shared)

// No default -- must explicitly scope every variable (recommended for safety)
#pragma omp parallel default(none) shared(a, b, N) private(i, temp)
for (int i = 0; i < N; i++) {
    int temp = a[i];
    b[i] = temp * 2;
}

// firstprivate as default (OpenMP 5.0+)
#pragma omp parallel default(firstprivate) shared(result)
```

**Best practice**: Use `default(none)` to force explicit scoping and avoid accidental sharing.

## 11.4 Threadprivate and Copyin

```c
int counter = 0;
#pragma omp threadprivate(counter)

// Each thread has its own persistent copy of counter
#pragma omp parallel copyin(counter)
{
    // counter starts with the master thread's value
    counter += omp_get_thread_num();
}

// counter persists across parallel regions for each thread
#pragma omp parallel
{
    counter++;  // each thread increments its own copy
}
```

## 11.5 Copyprivate

Broadcasts a `private` variable from one thread to all others after a `single` block:

```c
int value;
#pragma omp parallel private(value)
{
    #pragma omp single copyprivate(value)
    {
        value = read_input();  // one thread reads
    }
    // All threads now have the same value
    process(value);
}
```

---

# 12. Synchronization

---

## 12.1 Barrier

All threads must reach the barrier before any can proceed:

```c
#pragma omp parallel
{
    phase1();

    #pragma omp barrier

    phase2();  // guaranteed phase1 is complete for all threads
}
```

Implicit barriers exist at the end of `parallel`, `for`, `sections`, and `single` (unless `nowait` is specified).

## 12.2 Critical Section

Mutual exclusion -- only one thread at a time can execute the block:

```c
#pragma omp parallel for
for (int i = 0; i < N; i++) {
    double val = compute(i);

    #pragma omp critical
    {
        global_list.push_back(val);
    }
}

// Named critical sections: different names allow different locks
#pragma omp critical(update_x)
{ x += local_x; }

#pragma omp critical(update_y)
{ y += local_y; }
// update_x and update_y can execute concurrently
```

## 12.3 Atomic Operations

More efficient than `critical` for simple operations on a single memory location:

```c
// Update (default): x++, x--, x += expr, x *= expr, etc.
#pragma omp atomic update
sum += local_val;

// Read: atomically read a value
#pragma omp atomic read
local = shared_var;

// Write: atomically write a value
#pragma omp atomic write
shared_var = expr;

// Capture: atomically update and capture old or new value
#pragma omp atomic capture
{
    old_val = counter;
    counter++;
}

// Compare (OpenMP 5.1): atomic compare-and-swap
#pragma omp atomic compare
if (shared_var == expected) shared_var = desired;
```

## 12.4 Locks

For fine-grained locking beyond `critical`:

```c
omp_lock_t lock;
omp_init_lock(&lock);

#pragma omp parallel for
for (int i = 0; i < N; i++) {
    double val = compute(i);

    omp_set_lock(&lock);
    update_shared(val);
    omp_unset_lock(&lock);
}

omp_destroy_lock(&lock);

// Nestable lock (can be acquired multiple times by the same thread)
omp_nest_lock_t nest_lock;
omp_init_nest_lock(&nest_lock);
// omp_set_nest_lock / omp_unset_nest_lock / omp_test_nest_lock
omp_destroy_nest_lock(&nest_lock);
```

## 12.5 Ordered

Executes iterations in sequential order:

```c
#pragma omp parallel for ordered
for (int i = 0; i < N; i++) {
    double result = compute(i);  // parallel

    #pragma omp ordered
    {
        printf("i=%d result=%f\n", i, result);  // sequential order
    }
}
```

## 12.6 Flush

Ensures memory consistency (makes a thread's writes visible to other threads):

```c
// Explicit flush
#pragma omp flush
#pragma omp flush(x, y)  // flush specific variables

// Implicit flush occurs at: barrier, entry/exit of critical/ordered/parallel,
// lock/unlock operations, and task scheduling points
```

In practice, `atomic` and `critical` provide sufficient memory ordering for most programs.

## 12.7 Synchronization Summary

| Mechanism | Granularity | Overhead | Best For |
|---|---|---|---|
| `barrier` | All threads | High | Phase synchronization |
| `critical` | Code block | Moderate | Multi-statement mutual exclusion |
| `atomic` | Single variable | Low | Simple increments, assignments |
| `lock` | User-defined | Low-moderate | Fine-grained, multiple lock instances |
| `ordered` | Loop iteration | High | Sequential output in parallel loop |
| `single` | One thread | Low | One-time initialization |

---

# 13. Tasking Model

---

## 13.1 Task Basics

Tasks enable parallelism for irregular structures (recursion, linked lists, while loops) that cannot be expressed as parallel for loops:

```c
#pragma omp parallel
{
    #pragma omp single
    {
        for (Node* p = head; p != NULL; p = p->next) {
            #pragma omp task firstprivate(p)
            {
                process(p);
            }
        }
    }
}
```

A task is a unit of work that can be executed by any thread in the team. The runtime defers and schedules tasks dynamically.

## 13.2 Task Clauses

```c
#pragma omp task if(expr)           // create task only if expr is true; else execute immediately
#pragma omp task final(expr)        // if true, task and all descendants are included (non-deferred)
#pragma omp task untied             // task can resume on a different thread after suspension
#pragma omp task mergeable          // implementation may merge with parent
#pragma omp task priority(n)        // higher priority tasks are preferred (hint only)
#pragma omp task shared(x) private(y) firstprivate(z)
```

## 13.3 Task Synchronization

```c
#pragma omp parallel
{
    #pragma omp single
    {
        #pragma omp task
        { task_A(); }

        #pragma omp task
        { task_B(); }

        #pragma omp taskwait
        // All child tasks of the current task must complete before proceeding

        // This task depends on results from A and B
        #pragma omp task
        { task_C(); }
    }
}
```

### Taskgroup

```c
#pragma omp taskgroup
{
    // All tasks created within this block (including descendants) must complete
    // before execution proceeds past the taskgroup
    #pragma omp task
    {
        #pragma omp task  // nested task also included
        { sub_work(); }
        work();
    }
}
```

### Taskyield

```c
#pragma omp task
{
    while (!done) {
        partial_work();
        #pragma omp taskyield  // allow the runtime to schedule another task
    }
}
```

## 13.4 Task Dependencies

Enforce ordering between tasks without explicit synchronization:

```c
int x, y;

#pragma omp parallel
#pragma omp single
{
    #pragma omp task depend(out: x)
    { x = compute_x(); }

    #pragma omp task depend(out: y)
    { y = compute_y(); }

    #pragma omp task depend(in: x, y)
    { result = combine(x, y); }  // waits for both x and y tasks
}
```

| Dependency | Meaning |
|---|---|
| `depend(in: x)` | Task reads x; must wait for prior `out`/`inout` on x |
| `depend(out: x)` | Task writes x; must wait for prior `in`/`out`/`inout` on x |
| `depend(inout: x)` | Task reads and writes x; combines `in` and `out` semantics |
| `depend(mutexinoutset: x)` | Tasks with this on same x are mutually exclusive but unordered |

## 13.5 Recursive Task Parallelism

```c
int fib(int n) {
    if (n < 2) return n;

    int x, y;
    #pragma omp task shared(x) if(n > 20)
    { x = fib(n - 1); }

    #pragma omp task shared(y) if(n > 20)
    { y = fib(n - 2); }

    #pragma omp taskwait
    return x + y;
}

int main() {
    int result;
    #pragma omp parallel
    #pragma omp single
    {
        result = fib(40);
    }
    printf("fib(40) = %d\n", result);
}
```

### Tree Traversal

```c
void traverse(Node* node) {
    if (!node) return;

    #pragma omp task firstprivate(node)
    traverse(node->left);

    #pragma omp task firstprivate(node)
    traverse(node->right);

    #pragma omp taskwait
    process(node);  // process after children are done
}

#pragma omp parallel
#pragma omp single
traverse(root);
```

---

# 14. SIMD and Vectorization

---

## 14.1 SIMD Directive

Instructs the compiler to generate SIMD (vector) instructions for a loop:

```c
#pragma omp simd
for (int i = 0; i < N; i++) {
    a[i] = b[i] + c[i];
}

// Combined with parallel for
#pragma omp parallel for simd
for (int i = 0; i < N; i++) {
    a[i] = b[i] * c[i] + d[i];
}
```

## 14.2 SIMD Clauses

```c
// simdlen: preferred vector length
#pragma omp simd simdlen(8)
for (int i = 0; i < N; i++) { a[i] += b[i]; }

// aligned: assert pointer alignment for optimal SIMD loads/stores
#pragma omp simd aligned(a, b, c : 32)
for (int i = 0; i < N; i++) { a[i] = b[i] + c[i]; }

// linear: variable changes linearly with loop iteration
#pragma omp simd linear(j : 2)
for (int i = 0; i < N; i++) { a[i] = b[j]; j += 2; }

// reduction with SIMD
#pragma omp simd reduction(+ : sum)
for (int i = 0; i < N; i++) { sum += a[i]; }
```

## 14.3 Declare SIMD

Creates SIMD-enabled (vectorized) versions of functions:

```c
#pragma omp declare simd uniform(coeff) linear(i : 1)
double scaled_add(double x, double y, double coeff, int i) {
    return x + coeff * y;
}

#pragma omp simd
for (int i = 0; i < N; i++) {
    result[i] = scaled_add(a[i], b[i], 2.5, i);
}
```

---

# 15. OpenMP Target Offloading (GPU)

---

## 15.1 Overview

OpenMP 4.0+ can offload computation to accelerators (GPUs). The programming model uses directives similar to CPU OpenMP but targets a different device.

```c
#pragma omp target
{
    // This code runs on the device (GPU)
}
```

## 15.2 Data Mapping

```c
double a[N], b[N], c[N];

// map(to:)      -- copy host → device at entry
// map(from:)    -- copy device → host at exit
// map(tofrom:)  -- copy both ways
// map(alloc:)   -- allocate on device, no transfer

#pragma omp target map(to: a[0:N], b[0:N]) map(from: c[0:N])
{
    for (int i = 0; i < N; i++) {
        c[i] = a[i] + b[i];
    }
}
```

## 15.3 Target Data Regions

Persist device allocations across multiple target regions:

```c
#pragma omp target data map(to: a[0:N]) map(tofrom: b[0:N])
{
    #pragma omp target
    { kernel1(a, b, N); }

    // Host code can execute here (data stays on device)
    host_work();

    #pragma omp target
    { kernel2(a, b, N); }
}
// Data is copied back and freed here
```

### Explicit Data Movement

```c
#pragma omp target enter data map(to: a[0:N])
// ... a is on the device ...

#pragma omp target
{ compute(a, N); }

#pragma omp target update from(a[0:N])   // device → host
// ... modify a on host ...
#pragma omp target update to(a[0:N])     // host → device

#pragma omp target exit data map(from: a[0:N])
```

## 15.4 Teams and Distribute

Map OpenMP parallelism to GPU hardware:

```c
// Full GPU offload pattern:
// teams: creates league of thread teams (maps to GPU blocks/workgroups)
// distribute: distributes iterations across teams
// parallel for: parallelizes within each team (maps to threads within a block)
#pragma omp target teams distribute parallel for \
        map(to: a[0:N], b[0:N]) map(from: c[0:N])
for (int i = 0; i < N; i++) {
    c[i] = a[i] + b[i];
}

// Control team and thread count
#pragma omp target teams num_teams(128) thread_limit(256) \
        distribute parallel for
for (int i = 0; i < N; i++) {
    c[i] = a[i] * b[i];
}
```

```
GPU Mapping:
  teams          → thread blocks / workgroups
  threads/team   → threads per block
  distribute     → distribute iterations across teams
  parallel for   → distribute iterations within a team
```

## 15.5 Declare Target

Mark functions for device compilation:

```c
#pragma omp declare target
double device_func(double x) {
    return x * x + 1.0;
}
#pragma omp end declare target

#pragma omp target teams distribute parallel for
for (int i = 0; i < N; i++) {
    result[i] = device_func(data[i]);
}
```

## 15.6 Target vs CUDA/HIP Comparison

| Feature | OpenMP Target | CUDA/HIP |
|---|---|---|
| Approach | Directive-based (incremental) | Explicit API |
| Portability | Any compliant compiler + device | NVIDIA only / AMD + NVIDIA |
| Control | Moderate (compiler decides details) | Full (manual thread management) |
| Memory management | `map` clauses | `cudaMalloc`/`hipMalloc` |
| Kernel launch | Compiler-generated | `<<<blocks, threads>>>` |
| Performance potential | Good (compiler-dependent) | Maximum (hand-tuned) |
| Learning curve | Lower (if you know OpenMP) | Steeper |
| Best for | Gradual offloading of existing code | Performance-critical GPU code |

---

# 16. OpenMP Best Practices

---

## 16.1 False Sharing

False sharing occurs when threads modify variables on the same cache line:

```c
// BAD: false sharing -- counters are adjacent in memory
int counters[NUM_THREADS];  // likely on same cache line

#pragma omp parallel
{
    int tid = omp_get_thread_num();
    for (int i = 0; i < WORK; i++) {
        counters[tid]++;  // cache line ping-pongs between cores
    }
}

// GOOD: pad to separate cache lines
#define CACHE_LINE 64
typedef struct { int val; char pad[CACHE_LINE - sizeof(int)]; } PaddedInt;
PaddedInt counters[NUM_THREADS];

#pragma omp parallel
{
    int tid = omp_get_thread_num();
    for (int i = 0; i < WORK; i++) {
        counters[tid].val++;
    }
}

// BEST: use local variable and reduce
int total = 0;
#pragma omp parallel for reduction(+:total)
for (int i = 0; i < WORK; i++) {
    total++;
}
```

## 16.2 Thread Affinity and Binding

```bash
# Bind each thread to a core (no migration)
export OMP_PROC_BIND=close   # bind to nearby cores
export OMP_PLACES=cores      # one thread per core

# For NUMA: spread threads across sockets
export OMP_PROC_BIND=spread
export OMP_PLACES=sockets

# Fine-grained control
export OMP_PLACES="{0,1},{2,3},{4,5},{6,7}"
```

| `OMP_PROC_BIND` | Behavior |
|---|---|
| `false` | No binding (OS schedules freely) |
| `true` | Implementation-defined binding |
| `close` | Threads placed close together (same socket/NUMA domain) |
| `spread` | Threads spread across places (maximize memory bandwidth) |
| `master` | Threads placed close to the master thread |

## 16.3 NUMA Awareness

```c
// First-touch policy: memory is allocated on the NUMA node that first writes to it
// Initialize data in parallel so each thread's data lands on its local NUMA node

#pragma omp parallel for schedule(static)
for (int i = 0; i < N; i++) {
    a[i] = 0.0;  // first touch -- allocated on executing thread's NUMA node
}

// Subsequent parallel access with same static schedule will be local
#pragma omp parallel for schedule(static)
for (int i = 0; i < N; i++) {
    a[i] = compute(i);  // accesses local memory
}
```

## 16.4 Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Missing `private` | Threads share loop temp variables | Use `private` or declare inside parallel block |
| Race on `shared` | Multiple threads write without sync | Use `reduction`, `atomic`, or `critical` |
| `critical` bottleneck | All threads serialize at critical | Use `atomic`, fine-grained locks, or restructure |
| Excessive `barrier` | Unnecessary synchronization overhead | Use `nowait` where safe |
| Nested parallelism | Too many threads (threads × threads) | Disable or limit nesting |
| Wrong `schedule` | Load imbalance or cache thrashing | Profile and tune schedule |
| Stack overflow | Large arrays in private scope | Increase `OMP_STACKSIZE` or use heap |

---

## Common Interview Questions -- OpenMP

**Q: What is the difference between `shared` and `private` in OpenMP?**

`shared` means all threads access the same memory location for that variable -- reads see other threads' writes, and writes can cause data races. `private` gives each thread its own uninitialized copy; the original variable is not affected. Use `firstprivate` when the private copy needs to be initialized with the original value, and `lastprivate` when the value from the sequentially last iteration should be preserved after the parallel region.

**Q: Explain false sharing and how to avoid it.**

False sharing occurs when threads modify different variables that happen to occupy the same CPU cache line (typically 64 bytes). Even though there is no logical data sharing, the hardware invalidation protocol forces the cache line to bounce between cores, severely degrading performance. Solutions: (1) Pad data structures to cache-line boundaries, (2) Use thread-local variables or `reduction` instead of per-thread array elements, (3) Align arrays with `_aligned_malloc` or `aligned_alloc`.

**Q: When would you use tasks instead of parallel for?**

Tasks are needed for: (1) Irregular loop structures like linked list traversal or while loops with unknown iteration count, (2) Recursive parallelism (divide and conquer, tree traversal), (3) Producer-consumer patterns, (4) When the amount of work per "iteration" varies dramatically and can itself spawn sub-work. Parallel for requires a canonical counted loop with known bounds, which tasks do not.

**Q: What is the fork-join model?**

In OpenMP's fork-join model, a program begins with a single master thread. When a parallel region is encountered, the master forks (creates) a team of worker threads. All threads in the team execute the parallel region concurrently. At the end of the parallel region, threads synchronize at an implicit barrier (join) and only the master thread continues. This can happen multiple times throughout the program.

**Q: How does `reduction` work internally?**

Each thread gets a private copy of the reduction variable initialized to the identity element for the operator (0 for `+`, 1 for `*`, etc.). Threads accumulate into their local copies without synchronization. At the end of the parallel region, all private copies are combined using the reduction operator to produce the final result. This is both correct (no data races) and efficient (no synchronization during computation).

**Q: Compare `atomic` and `critical` in OpenMP.**

`atomic` operates on a single memory location using hardware atomic instructions (compare-and-swap, fetch-and-add); it has very low overhead but is limited to simple expressions (`x++`, `x += val`, `x = expr`). `critical` uses a mutex to protect an arbitrary code block and can contain multiple statements, but has higher overhead and serializes all threads. Named critical sections with different names can execute concurrently. For simple updates, `atomic` is always preferred.

---

# Part 3: CUDA

---

# 17. GPU Architecture Fundamentals

---

## 17.1 NVIDIA GPU Architecture

A GPU is a massively parallel processor optimized for throughput rather than latency:

```
GPU
├── Streaming Multiprocessors (SMs) × N
│   ├── CUDA Cores (ALUs) × M
│   ├── Tensor Cores (matrix ops, if present)
│   ├── Warp Schedulers × S
│   ├── Register File (per SM)
│   ├── Shared Memory / L1 Cache (configurable split)
│   └── Constant Cache
├── L2 Cache (shared across all SMs)
├── Global Memory (HBM / GDDR)
└── Memory Controllers
```

### Key Concepts

- **Streaming Multiprocessor (SM)**: The fundamental processing unit. Each SM can execute multiple warps concurrently.
- **CUDA Core**: A single-precision floating-point / integer ALU. An SM contains dozens to hundreds of CUDA cores.
- **Warp**: A group of 32 threads that execute in lockstep (SIMT -- Single Instruction, Multiple Threads). All threads in a warp execute the same instruction at each cycle.
- **Warp Scheduler**: Selects ready warps for execution. SMs have multiple warp schedulers to issue instructions from different warps each cycle.

## 17.2 Thread Hierarchy

```
Grid
├── Block (0,0)
│   ├── Thread (0,0) ─┐
│   ├── Thread (1,0)  ├── Warp 0 (threads 0-31)
│   ├── ...           │
│   ├── Thread (31,0) ┘
│   ├── Thread (32,0) ─┐
│   ├── ...             ├── Warp 1 (threads 32-63)
│   └── Thread (63,0) ──┘
├── Block (1,0)
│   └── ...
├── Block (0,1)
│   └── ...
└── ...
```

| Level | Maps To | Communication | Max Size |
|---|---|---|---|
| **Thread** | Single CUDA core execution | Registers (private) | N/A |
| **Warp** | 32 threads in lockstep | Warp shuffle intrinsics | 32 threads (fixed) |
| **Block** | Runs on one SM | Shared memory + `__syncthreads` | 1024 threads |
| **Grid** | Entire GPU | Global memory + atomics | Up to 2³¹-1 blocks per dim |

## 17.3 SIMT Execution Model

All threads in a warp execute the same instruction simultaneously. When threads diverge (take different branches), the warp executes both paths serially, masking inactive threads:

```
// If threads 0-15 take the if-branch and threads 16-31 take the else-branch:
// Step 1: Execute if-branch (threads 16-31 masked/idle)
// Step 2: Execute else-branch (threads 0-15 masked/idle)
// Performance cost: both paths execute sequentially

if (threadIdx.x < 16) {
    path_A();  // only threads 0-15 active
} else {
    path_B();  // only threads 16-31 active
}
// All threads reconverge here
```

## 17.4 Compute Capability

Each GPU generation has a compute capability that determines available features:

| Compute Capability | Architecture | Key Features |
|---|---|---|
| 3.x | Kepler | Dynamic parallelism, Hyper-Q |
| 5.x | Maxwell | Improved power efficiency |
| 6.x | Pascal | Unified memory with page migration, fp16 |
| 7.0 | Volta | Tensor cores, independent thread scheduling |
| 7.5 | Turing | RT cores, INT8 tensor ops |
| 8.0 | Ampere (A100) | TF32, BF16, sparsity, async copy |
| 8.9 | Ada Lovelace | FP8, shader execution reordering |
| 9.0 | Hopper (H100) | Thread block clusters, TMA, DPX |

## 17.5 CPU vs GPU Architecture Comparison

| Feature | CPU | GPU |
|---|---|---|
| Design philosophy | Latency-optimized | Throughput-optimized |
| Cores | 4-128 powerful cores | Thousands of simple cores |
| Clock speed | 3-5+ GHz | 1-2+ GHz |
| Cache per core | Large (MB) | Small (KB shared per SM) |
| Control logic | Complex (branch prediction, OoO) | Simple (in-order, hardware multithreading) |
| Thread switching | Expensive (OS context switch) | Near-zero cost (hardware) |
| Memory bandwidth | ~50-100 GB/s | ~1-3+ TB/s (HBM) |
| Best for | Serial, branchy, latency-sensitive | Parallel, uniform, throughput workloads |

---

# 18. CUDA Programming Model

---

## 18.1 Kernel Definition

CUDA extends C/C++ with function qualifiers:

| Qualifier | Called From | Executes On | Returns |
|---|---|---|---|
| `__global__` | Host (or device with dynamic parallelism) | Device | `void` only |
| `__device__` | Device | Device | Any type |
| `__host__` | Host | Host | Any type |
| `__host__ __device__` | Both | Both (compiled for each) | Any type |

```cpp
__global__ void vector_add(float* a, float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

__device__ float square(float x) {
    return x * x;
}

__host__ __device__ float clamp(float val, float lo, float hi) {
    return fminf(fmaxf(val, lo), hi);
}
```

## 18.2 Kernel Launch Syntax

```cpp
kernel<<<gridDim, blockDim, sharedMemBytes, stream>>>(args...);

// gridDim:       number of blocks (dim3 or int)
// blockDim:      threads per block (dim3 or int)
// sharedMemBytes: dynamic shared memory per block (optional, default 0)
// stream:        CUDA stream (optional, default 0)
```

```cpp
int N = 1000000;
int threads_per_block = 256;
int blocks = (N + threads_per_block - 1) / threads_per_block;

vector_add<<<blocks, threads_per_block>>>(d_a, d_b, d_c, N);
```

### 2D and 3D Configurations

```cpp
// 2D grid of 2D blocks (e.g., for image processing)
dim3 block(16, 16);           // 256 threads per block
dim3 grid((width + 15) / 16,
          (height + 15) / 16);

image_kernel<<<grid, block>>>(d_image, width, height);

// Inside kernel:
__global__ void image_kernel(float* img, int width, int height) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x < width && y < height) {
        int idx = y * width + x;
        img[idx] = process(img[idx]);
    }
}
```

## 18.3 Thread Indexing

```cpp
// Built-in variables (dim3 type with .x, .y, .z components):
threadIdx   // thread index within block (0 to blockDim-1)
blockIdx    // block index within grid (0 to gridDim-1)
blockDim    // threads per block
gridDim     // blocks per grid
warpSize    // warp size (always 32 on NVIDIA)

// 1D global thread ID:
int tid = blockIdx.x * blockDim.x + threadIdx.x;

// 2D global thread ID:
int x = blockIdx.x * blockDim.x + threadIdx.x;
int y = blockIdx.y * blockDim.y + threadIdx.y;

// Grid-stride loop (handles arbitrary N with fixed grid size):
for (int i = blockIdx.x * blockDim.x + threadIdx.x;
     i < N;
     i += blockDim.x * gridDim.x) {
    process(i);
}
```

## 18.4 Complete Example: Vector Addition

```cpp
#include <cuda_runtime.h>
#include <stdio.h>

__global__ void vector_add(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    int N = 1 << 20;
    size_t bytes = N * sizeof(float);

    float *h_a, *h_b, *h_c;
    h_a = (float*)malloc(bytes);
    h_b = (float*)malloc(bytes);
    h_c = (float*)malloc(bytes);

    for (int i = 0; i < N; i++) {
        h_a[i] = 1.0f;
        h_b[i] = 2.0f;
    }

    float *d_a, *d_b, *d_c;
    cudaMalloc(&d_a, bytes);
    cudaMalloc(&d_b, bytes);
    cudaMalloc(&d_c, bytes);

    cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice);

    int block_size = 256;
    int grid_size = (N + block_size - 1) / block_size;
    vector_add<<<grid_size, block_size>>>(d_a, d_b, d_c, N);

    cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost);

    printf("c[0] = %f\n", h_c[0]);  // 3.0

    cudaFree(d_a); cudaFree(d_b); cudaFree(d_c);
    free(h_a); free(h_b); free(h_c);
    return 0;
}
```

> **See also:** building `.cu` files with CMake's CUDA language (`CMAKE_CUDA_ARCHITECTURES`, `CUDA::cudart`), and the matching HIP setup, are compared side by side in [CMake Fundamentals -- CUDA vs HIP in CMake](../tools/CMake_Fundamentals.md#646-cuda-vs-hip-in-cmake).

## 18.5 Matrix Multiplication

```cpp
__global__ void matmul(const float* A, const float* B, float* C,
                       int M, int N, int K) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < M && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < K; k++) {
            sum += A[row * K + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

// Launch: each thread computes one element of C
dim3 block(16, 16);
dim3 grid((N + 15) / 16, (M + 15) / 16);
matmul<<<grid, block>>>(d_A, d_B, d_C, M, N, K);
```

---

# 19. CUDA Memory Model

---

## 19.1 Memory Hierarchy

```
Register File (per thread)      ← Fastest, private
    ↓
Shared Memory / L1 Cache (per SM/block)  ← Fast, shared within block
    ↓
L2 Cache (per GPU)              ← Moderate, shared across all SMs
    ↓
Global Memory (HBM/GDDR)       ← Slowest, accessible by all threads and host
    ↓
Host Memory (CPU DRAM)          ← Accessible via PCIe/NVLink transfers
```

| Memory | Scope | Lifetime | Latency | Size | Cached |
|---|---|---|---|---|---|
| **Registers** | Thread | Thread | ~1 cycle | ~255 per thread | N/A |
| **Local memory** | Thread | Thread | ~200+ cycles | Up to global | L1/L2 |
| **Shared memory** | Block | Block | ~5-30 cycles | 48-228 KB per SM | N/A (explicit) |
| **L1 cache** | SM | Automatic | ~30 cycles | 48-228 KB per SM | Automatic |
| **L2 cache** | GPU | Automatic | ~200 cycles | 4-50 MB | Automatic |
| **Global memory** | GPU + Host | Application | ~200-800 cycles | 8-80+ GB | L1/L2 |
| **Constant memory** | GPU | Application | ~5 cycles (cached) | 64 KB | Dedicated cache |
| **Texture memory** | GPU | Application | ~200+ cycles | Global size | Dedicated cache |

## 19.2 Global Memory Management

```cpp
float* d_ptr;

// Allocate device memory
cudaMalloc((void**)&d_ptr, N * sizeof(float));

// Copy host → device
cudaMemcpy(d_ptr, h_ptr, N * sizeof(float), cudaMemcpyHostToDevice);

// Copy device → host
cudaMemcpy(h_ptr, d_ptr, N * sizeof(float), cudaMemcpyDeviceToHost);

// Copy device → device
cudaMemcpy(d_dst, d_src, N * sizeof(float), cudaMemcpyDeviceToDevice);

// Initialize device memory
cudaMemset(d_ptr, 0, N * sizeof(float));

// Free device memory
cudaFree(d_ptr);
```

## 19.3 Pinned (Page-Locked) Memory

Pinned memory enables faster transfers and is required for asynchronous copies:

```cpp
float* h_pinned;

// Allocate pinned host memory
cudaMallocHost(&h_pinned, N * sizeof(float));
// or: cudaHostAlloc(&h_pinned, N * sizeof(float), cudaHostAllocDefault);

// Use like normal memory on host
for (int i = 0; i < N; i++) h_pinned[i] = i;

// Transfers are faster (DMA, no staging through a pageable buffer)
cudaMemcpy(d_ptr, h_pinned, N * sizeof(float), cudaMemcpyHostToDevice);

// Async copy (requires pinned memory + non-default stream)
cudaMemcpyAsync(d_ptr, h_pinned, N * sizeof(float),
                cudaMemcpyHostToDevice, stream);

// Free
cudaFreeHost(h_pinned);
```

| Memory Type | Allocator | Transfer Speed | Async Support | OS Paging |
|---|---|---|---|---|
| Pageable | `malloc` | Slower (staged) | No | Can be swapped |
| Pinned | `cudaMallocHost` | Faster (DMA direct) | Yes | Locked in physical RAM |
| Write-combining | `cudaHostAlloc(WC)` | Fastest H→D | Yes | Not cached on CPU |

## 19.4 Unified Memory

Automatically migrates data between host and device:

```cpp
float* data;
cudaMallocManaged(&data, N * sizeof(float));

// Access from host
for (int i = 0; i < N; i++) data[i] = i;

// Access from device (automatic migration)
my_kernel<<<blocks, threads>>>(data, N);
cudaDeviceSynchronize();

// Access from host again (automatic migration back)
printf("%f\n", data[0]);

cudaFree(data);
```

### Prefetching (Performance Optimization)

```cpp
cudaMallocManaged(&data, bytes);

// Prefetch to GPU before kernel launch
cudaMemPrefetchAsync(data, bytes, deviceId, stream);
kernel<<<blocks, threads, 0, stream>>>(data, N);

// Prefetch back to CPU before host access
cudaMemPrefetchAsync(data, bytes, cudaCpuDeviceId, stream);
cudaStreamSynchronize(stream);
printf("%f\n", data[0]);
```

### Memory Advice Hints

```cpp
// Data is mostly read by the device
cudaMemAdvise(data, bytes, cudaMemAdviseSetReadMostly, deviceId);

// Data will be accessed by a specific device
cudaMemAdvise(data, bytes, cudaMemAdviseSetPreferredLocation, deviceId);

// Data is accessed by both host and device
cudaMemAdvise(data, bytes, cudaMemAdviseSetAccessedBy, deviceId);
```

## 19.5 Shared Memory

Declared within a kernel, shared by all threads in a block:

```cpp
// Static shared memory
__global__ void kernel() {
    __shared__ float sdata[256];
    sdata[threadIdx.x] = global_data[threadIdx.x];
    __syncthreads();
    // all threads can now read any element of sdata
}

// Dynamic shared memory (size specified at launch)
__global__ void kernel() {
    extern __shared__ float sdata[];
    sdata[threadIdx.x] = global_data[threadIdx.x];
    __syncthreads();
}

kernel<<<blocks, threads, shared_mem_bytes>>>(args);
```

## 19.6 Constant Memory

Read-only from device, written from host. Broadcast efficiently when all threads read the same address:

```cpp
__constant__ float coefficients[256];

// Host: copy to constant memory
float h_coeff[256];
cudaMemcpyToSymbol(coefficients, h_coeff, 256 * sizeof(float));

__global__ void kernel(float* data) {
    // Fast broadcast when all threads in a warp read the same index
    float c = coefficients[blockIdx.x % 256];
    data[threadIdx.x] *= c;
}
```

---

# 20. Memory Optimization

---

## 20.1 Global Memory Coalescing

When threads in a warp access consecutive memory locations, the hardware combines them into fewer memory transactions. **Coalesced access** is critical for performance.

```cpp
// GOOD: Coalesced -- consecutive threads access consecutive elements
// Thread 0 → data[0], Thread 1 → data[1], ..., Thread 31 → data[31]
__global__ void coalesced(float* data) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    data[i] = data[i] * 2.0f;
}

// BAD: Strided -- threads skip elements
// Thread 0 → data[0], Thread 1 → data[stride], Thread 2 → data[2*stride]
__global__ void strided(float* data, int stride) {
    int i = (blockIdx.x * blockDim.x + threadIdx.x) * stride;
    data[i] = data[i] * 2.0f;  // up to 32× slower for stride=32
}

// BAD: Random access
__global__ void random_access(float* data, int* indices) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    data[indices[i]] = 0.0f;  // scattered writes
}
```

### AoS vs SoA

```cpp
// AoS (Array of Structures) -- BAD for GPU
struct Particle_AoS {
    float x, y, z;
    float vx, vy, vz;
};
Particle_AoS particles[N];
// Thread i accesses particles[i].x → stride of sizeof(Particle_AoS) = 24 bytes

// SoA (Structure of Arrays) -- GOOD for GPU
struct Particles_SoA {
    float x[N], y[N], z[N];
    float vx[N], vy[N], vz[N];
};
Particles_SoA particles;
// Thread i accesses particles.x[i] → coalesced, stride of 4 bytes
```

## 20.2 Shared Memory Bank Conflicts

Shared memory is divided into 32 banks (one per warp thread). Accesses to different addresses in the same bank are serialized.

```cpp
// Bank assignment: bank = (address / 4) % 32

// NO conflict: consecutive threads → consecutive banks
sdata[threadIdx.x] = val;  // thread k → bank k

// NO conflict: all threads access the same address (broadcast)
val = sdata[0];  // broadcast to all threads

// CONFLICT: stride-2 access → threads 0,16 hit bank 0; threads 1,17 hit bank 1; etc.
sdata[threadIdx.x * 2] = val;  // 2-way bank conflict

// WORST: stride-32 access → all threads hit the same bank
sdata[threadIdx.x * 32] = val;  // 32-way bank conflict (serialized)
```

### Padding to Avoid Conflicts

```cpp
// Example: transposing a tile using shared memory
// Without padding: column reads have 32-way bank conflicts
__shared__ float tile[32][32];
tile[threadIdx.y][threadIdx.x] = input[...];  // row write: no conflict
__syncthreads();
output[...] = tile[threadIdx.x][threadIdx.y];  // column read: 32-way conflict!

// With padding: add 1 extra column to shift bank alignment
__shared__ float tile[32][33];  // 33 instead of 32
tile[threadIdx.y][threadIdx.x] = input[...];
__syncthreads();
output[...] = tile[threadIdx.x][threadIdx.y];  // no conflict!
```

## 20.3 Constant Memory Optimization

- 64 KB total constant memory
- Cached in a dedicated constant cache per SM
- When all threads in a warp read the same address: single cache read + broadcast (very fast)
- When threads read different addresses: serialized reads (can be slow)

```cpp
// GOOD: all threads read the same filter coefficient
__constant__ float filter[FILTER_SIZE];
float val = filter[k];  // k is same for all threads → broadcast

// BAD: each thread reads a different constant address
float val = filter[threadIdx.x];  // serialized in constant cache
// Better: use shared memory for divergent reads
```

## 20.4 Memory Access Pattern Summary

| Pattern | Throughput | Technique |
|---|---|---|
| Coalesced global reads/writes | Maximum | Consecutive threads → consecutive addresses |
| Shared memory (no bank conflicts) | Maximum | Avoid stride multiples of 32 |
| Constant memory broadcast | Maximum | All threads read same address |
| SoA data layout | High | Separate arrays per field |
| Texture memory (2D locality) | High | Use for read-only 2D spatial access |
| AoS data layout | Low | Strided access per field |
| Random global access | Low | Consider sorting or using shared memory |
| Strided global access | Low | Restructure to coalesced pattern |

---

# 21. Thread Synchronization and Cooperation

---

## 21.1 Block-Level Synchronization

```cpp
__syncthreads();  // all threads in the block must reach this point before any proceed
```

All threads in a block must reach `__syncthreads()` or the behavior is undefined. Never place it inside a conditional unless all threads take the same branch.

```cpp
// CORRECT
__shared__ float sdata[256];
sdata[threadIdx.x] = global[idx];
__syncthreads();
float val = sdata[255 - threadIdx.x];

// WRONG: conditional syncthreads
if (threadIdx.x < 128) {
    __syncthreads();  // UB: threads >= 128 never reach this
}
```

## 21.2 Warp-Level Primitives

Since all threads in a warp execute in lockstep, warp-level operations require no explicit synchronization (but require a mask in modern CUDA):

### Warp Shuffle

Exchange data between threads within a warp without shared memory:

```cpp
// __shfl_sync: read from an arbitrary lane
int val = __shfl_sync(0xFFFFFFFF, my_val, src_lane);
// All threads get the value from thread `src_lane`

// __shfl_up_sync: read from a lower lane
int val = __shfl_up_sync(0xFFFFFFFF, my_val, delta);
// Thread i gets value from thread (i - delta), or its own if i < delta

// __shfl_down_sync: read from a higher lane
int val = __shfl_down_sync(0xFFFFFFFF, my_val, delta);
// Thread i gets value from thread (i + delta), or its own if i >= warpSize - delta

// __shfl_xor_sync: read from XOR-paired lane (butterfly pattern)
int val = __shfl_xor_sync(0xFFFFFFFF, my_val, lane_mask);
// Thread i gets value from thread (i ^ lane_mask)
```

### Warp Reduction Using Shuffles

```cpp
__device__ float warp_reduce_sum(float val) {
    for (int offset = warpSize / 2; offset > 0; offset >>= 1) {
        val += __shfl_down_sync(0xFFFFFFFF, val, offset);
    }
    return val;  // result is valid only in lane 0
}
```

### Warp Vote Functions

```cpp
unsigned mask = 0xFFFFFFFF;

// All: true if predicate is true for ALL threads in mask
int all_true = __all_sync(mask, predicate);

// Any: true if predicate is true for ANY thread in mask
int any_true = __any_sync(mask, predicate);

// Ballot: returns a bitmask where bit i is set if thread i's predicate is true
unsigned ballot = __ballot_sync(mask, predicate);
int count = __popc(ballot);  // population count
```

### Match Functions (Compute 7.0+)

```cpp
// Find which threads have the same value
unsigned peers = __match_any_sync(mask, value);
// `peers` is a bitmask of threads that have the same `value`

unsigned leader = __match_all_sync(mask, value, &pred);
// If all threads have the same value, pred = 1
```

## 21.3 Atomic Operations

Thread-safe read-modify-write on global or shared memory:

```cpp
atomicAdd(&global_sum, local_val);   // global_sum += local_val
atomicSub(&counter, 1);              // counter -= 1
atomicMax(&max_val, my_val);         // max_val = max(max_val, my_val)
atomicMin(&min_val, my_val);         // min_val = min(min_val, my_val)
atomicExch(&slot, new_val);          // swap slot with new_val, return old
atomicCAS(&slot, compare, val);      // if (slot == compare) slot = val; return old
atomicAnd(&flags, mask);             // flags &= mask
atomicOr(&flags, mask);              // flags |= mask
atomicXor(&flags, mask);             // flags ^= mask
atomicInc(&counter, max_val);        // counter = (counter >= max_val) ? 0 : counter + 1
atomicDec(&counter, max_val);        // counter = (counter == 0 || counter > max_val) ? max_val : counter - 1
```

### Efficient Reduction Pattern (Avoiding Atomic Bottleneck)

```cpp
__global__ void reduce(float* input, float* output, int N) {
    __shared__ float sdata[256];
    int tid = threadIdx.x;
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    sdata[tid] = (i < N) ? input[i] : 0.0f;
    __syncthreads();

    // Tree reduction in shared memory
    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        __syncthreads();
    }

    // One atomic per block (not per thread)
    if (tid == 0) {
        atomicAdd(output, sdata[0]);
    }
}
```

## 21.4 Cooperative Groups (CUDA 9+)

A flexible API for synchronization at various granularities:

```cpp
#include <cooperative_groups.h>
namespace cg = cooperative_groups;

__global__ void kernel() {
    // Thread block group
    cg::thread_block block = cg::this_thread_block();
    block.sync();  // equivalent to __syncthreads()

    // Tiled partition (sub-warp groups)
    cg::thread_block_tile<16> tile16 = cg::tiled_partition<16>(block);
    float sum = cg::reduce(tile16, my_val, cg::plus<float>());

    // Warp group
    cg::coalesced_group active = cg::coalesced_threads();
    // Only includes threads that are actually executing (handles divergence)
}

// Grid-level sync (requires cooperative launch)
__global__ void grid_kernel() {
    cg::grid_group grid = cg::this_grid();
    // Phase 1
    compute_phase1();
    grid.sync();  // synchronize entire grid
    // Phase 2 (can read Phase 1 results from any block)
    compute_phase2();
}

// Launch with cooperative kernel
cudaLaunchCooperativeKernel((void*)grid_kernel, grid_dim, block_dim, args);
```

## 21.5 Synchronization Scope Summary

| Mechanism | Scope | Hardware Cost | Use Case |
|---|---|---|---|
| `__syncthreads()` | Block | Low | Shared memory consistency |
| `__syncwarp()` | Warp | Minimal | Warp-level coordination |
| Warp shuffle | Warp | Very low | Data exchange within warp |
| `atomicAdd` etc. | Global/Block | Moderate-high | Thread-safe accumulation |
| Cooperative Groups | Flexible | Varies | Fine-grained sub-groups, grid sync |
| `cudaDeviceSynchronize()` | Device (host call) | High | Wait for all device work |

---

# 22. Streams, Events, and Concurrency

---

## 22.1 CUDA Streams

A stream is a sequence of operations that execute in order on the GPU. Operations in different streams can execute concurrently.

```cpp
cudaStream_t stream1, stream2;
cudaStreamCreate(&stream1);
cudaStreamCreate(&stream2);

// Operations in stream1
cudaMemcpyAsync(d_a, h_a, bytes, cudaMemcpyHostToDevice, stream1);
kernel_a<<<blocks, threads, 0, stream1>>>(d_a);
cudaMemcpyAsync(h_a, d_a, bytes, cudaMemcpyDeviceToHost, stream1);

// Operations in stream2 (can run concurrently with stream1)
cudaMemcpyAsync(d_b, h_b, bytes, cudaMemcpyHostToDevice, stream2);
kernel_b<<<blocks, threads, 0, stream2>>>(d_b);
cudaMemcpyAsync(h_b, d_b, bytes, cudaMemcpyDeviceToHost, stream2);

// Wait for specific stream
cudaStreamSynchronize(stream1);

// Destroy streams
cudaStreamDestroy(stream1);
cudaStreamDestroy(stream2);
```

### Default Stream Behavior

```cpp
// The default stream (stream 0 / NULL stream) has special behavior:
// - Legacy default: serializes with all other streams (blocking)
// - Per-thread default: independent per host thread

// Compile with --default-stream per-thread for per-thread behavior
// Or use cudaStreamNonBlocking flag:
cudaStreamCreateWithFlags(&stream, cudaStreamNonBlocking);
```

## 22.2 Overlapping Compute and Data Transfer

Requires pinned memory and multiple streams:

```cpp
cudaStream_t streams[NUM_STREAMS];
for (int i = 0; i < NUM_STREAMS; i++)
    cudaStreamCreate(&streams[i]);

int chunk_size = N / NUM_STREAMS;

for (int i = 0; i < NUM_STREAMS; i++) {
    int offset = i * chunk_size;

    // Each stream: copy chunk H→D, compute, copy results D→H
    cudaMemcpyAsync(d_in + offset,  h_in + offset,
                    chunk_size * sizeof(float),
                    cudaMemcpyHostToDevice, streams[i]);

    kernel<<<blocks_per_chunk, threads, 0, streams[i]>>>(
        d_in + offset, d_out + offset, chunk_size);

    cudaMemcpyAsync(h_out + offset, d_out + offset,
                    chunk_size * sizeof(float),
                    cudaMemcpyDeviceToHost, streams[i]);
}

// Wait for all streams
for (int i = 0; i < NUM_STREAMS; i++)
    cudaStreamSynchronize(streams[i]);
```

```
Timeline with 3 streams:
Stream 0: [H2D ][Kernel][D2H ]
Stream 1:       [H2D ][Kernel][D2H ]
Stream 2:              [H2D ][Kernel][D2H ]
                ↑ overlap achieves higher throughput
```

## 22.3 CUDA Events

Events mark points in a stream for timing or synchronization:

```cpp
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);

cudaEventRecord(start, stream);
kernel<<<blocks, threads, 0, stream>>>(args);
cudaEventRecord(stop, stream);

cudaEventSynchronize(stop);

float milliseconds = 0;
cudaEventElapsedTime(&milliseconds, start, stop);
printf("Kernel time: %.3f ms\n", milliseconds);

cudaEventDestroy(start);
cudaEventDestroy(stop);
```

### Inter-Stream Synchronization with Events

```cpp
cudaEvent_t event;
cudaEventCreate(&event);

// Stream 1 records an event after its work
kernel_a<<<..., 0, stream1>>>(d_a);
cudaEventRecord(event, stream1);

// Stream 2 waits for the event before proceeding
cudaStreamWaitEvent(stream2, event, 0);
kernel_b<<<..., 0, stream2>>>(d_a, d_b);  // safe: stream1's kernel_a is complete

cudaEventDestroy(event);
```

## 22.4 CUDA Graphs

Capture a sequence of operations as a graph and launch them with reduced overhead:

```cpp
// Method 1: Stream Capture
cudaGraph_t graph;
cudaGraphExec_t instance;

cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);

// Record operations (not executed yet)
cudaMemcpyAsync(d_a, h_a, bytes, cudaMemcpyHostToDevice, stream);
kernel<<<blocks, threads, 0, stream>>>(d_a, d_b, N);
cudaMemcpyAsync(h_b, d_b, bytes, cudaMemcpyDeviceToHost, stream);

cudaStreamEndCapture(stream, &graph);
cudaGraphInstantiate(&instance, graph, NULL, NULL, 0);

// Replay the graph multiple times (very low launch overhead)
for (int iter = 0; iter < 1000; iter++) {
    cudaGraphLaunch(instance, stream);
}
cudaStreamSynchronize(stream);

cudaGraphExecDestroy(instance);
cudaGraphDestroy(graph);
```

Benefits of CUDA Graphs:
- Reduce kernel launch overhead (especially for many small kernels)
- The entire graph is submitted in a single operation
- Driver can optimize the execution plan across the entire graph
- Ideal for iterative workloads where the same sequence repeats

> **See also:** [HIP graphs: stream capture semantics and pitfalls](#353-hip-graphs-stream-capture-semantics-and-pitfalls) (fork/join capture, illegal calls during capture, baked-in parameters, graph update).

---

# 23. Performance Optimization

---

> **See also:** the quantitative side of this section lives elsewhere: [Amdahl's and Gustafson's laws](../computer-science/Performance_Engineering.md#2-amdahls-and-gustafsons-laws), the [roofline model with MI300X ridge-point math](../computer-science/Performance_Engineering.md#3-roofline-model), and [Little's law / bytes in flight](../computer-science/Performance_Engineering.md#42-memory-level-parallelism-bytes-in-flight) for how much occupancy or ILP is enough. For full profile -> diagnose -> fix -> re-profile walkthroughs (reduction ladder, tiled GEMM, transpose, scan), see [GPU Kernel Case Studies](GPU_Kernel_Case_Studies.md).

## 23.1 Occupancy

Occupancy is the ratio of active warps to the maximum warps an SM can support. Higher occupancy generally helps hide memory latency.

**Factors limiting occupancy:**

| Resource | Limit | Impact |
|---|---|---|
| Threads per block | Max 1024 | Too small a block → fewer warps |
| Registers per thread | SM register file / threads | More registers → fewer concurrent threads |
| Shared memory per block | SM shared memory / blocks | More shared memory → fewer concurrent blocks |

```cpp
// Query occupancy
int min_grid_size, optimal_block_size;
cudaOccupancyMaxPotentialBlockSize(&min_grid_size, &optimal_block_size,
                                   my_kernel, 0, 0);
printf("Optimal block size: %d\n", optimal_block_size);

// Limit registers per thread to increase occupancy
__global__ void __launch_bounds__(256, 4) kernel() {
    // Compiler will use at most enough registers to allow
    // 4 blocks of 256 threads per SM
}
```

## 23.2 Warp Divergence

Minimize branch divergence within a warp for best performance:

```cpp
// BAD: threads within same warp take different branches
if (threadIdx.x % 2 == 0) {
    path_A();  // even threads
} else {
    path_B();  // odd threads -- warp executes both paths serially
}

// BETTER: ensure entire warps take the same branch
if (threadIdx.x / 32 < N_warps / 2) {
    path_A();  // entire warps go here
} else {
    path_B();  // entire warps go here -- no divergence within any warp
}
```

## 23.3 Instruction-Level Parallelism (ILP)

Process multiple independent values per thread to keep execution units busy:

```cpp
// Low ILP: single accumulator creates instruction dependency chain
__global__ void low_ilp(float* in, float* out, int N) {
    float sum = 0.0f;
    for (int i = threadIdx.x; i < N; i += blockDim.x) {
        sum += in[i];
    }
    out[threadIdx.x] = sum;
}

// High ILP: multiple independent accumulators
__global__ void high_ilp(float* in, float* out, int N) {
    float sum0 = 0.0f, sum1 = 0.0f, sum2 = 0.0f, sum3 = 0.0f;
    for (int i = threadIdx.x * 4; i < N; i += blockDim.x * 4) {
        sum0 += in[i];
        sum1 += in[i + 1];
        sum2 += in[i + 2];
        sum3 += in[i + 3];
    }
    out[threadIdx.x] = sum0 + sum1 + sum2 + sum3;
}
```

## 23.4 Loop Unrolling

```cpp
#pragma unroll
for (int k = 0; k < 16; k++) {
    sum += A[row * K + k] * B[k * N + col];
}

#pragma unroll 4  // unroll by factor of 4
for (int i = 0; i < N; i++) {
    process(data[i]);
}
```

## 23.5 Minimizing Host-Device Data Transfer

| Technique | Description |
|---|---|
| Batch operations | Combine many small transfers into fewer large ones |
| Pinned memory | Use `cudaMallocHost` for higher bandwidth |
| Async transfers | Overlap with compute using streams |
| Unified Memory | Let the driver handle migration (may be slower but simpler) |
| Compute on GPU | Keep data on GPU; avoid round-trips |
| Compression | Reduce data volume before transfer |

## 23.6 Common Bottlenecks and Solutions

| Bottleneck | Symptom | Solution |
|---|---|---|
| Memory bandwidth | Low compute/memory ratio | Reduce global memory access; use shared memory |
| Uncoalesced access | Low memory throughput | Restructure to coalesced patterns; SoA layout |
| Bank conflicts | Low shared memory throughput | Pad shared arrays; restructure access |
| Warp divergence | Low instruction throughput | Reorganize data to minimize branching |
| Low occupancy | GPU underutilized | Reduce register/shared memory use; tune block size |
| Launch overhead | Many small kernels | Use CUDA Graphs; merge kernels |
| PCIe bottleneck | Slow data transfers | Pinned memory; overlap; keep data on GPU |
| Atomic contention | Serialized updates | Hierarchical reduction; warp-level reduce first |
| Register spilling | Registers overflow to local (global) memory | Reduce per-thread state; `__launch_bounds__` |

## 23.7 Profiling Tools

| Tool | Purpose |
|---|---|
| **Nsight Compute** | Kernel-level profiling (roofline, memory, compute analysis) |
| **Nsight Systems** | System-wide timeline (CPU+GPU, streams, transfers) |
| `nvprof` (legacy) | Command-line profiler (deprecated in favor of Nsight) |
| CUDA Occupancy Calculator | Spreadsheet for occupancy analysis |
| `cuda-memcheck` / `compute-sanitizer` | Memory error detection |

Typical CUDA commands (Nsight Systems is `nsys`, Nsight Compute is `ncu`):

```bash
nsys profile -o timeline --trace=cuda,nvtx,osrt ./app     # timeline (.nsys-rep), open in the Nsight Systems GUI
ncu --set full -k regex:gemm -c 1 -o gemm_report ./app      # one dispatch of kernels matching "gemm", all sections
compute-sanitizer --tool racecheck ./app                    # shared-memory race detection (also memcheck, initcheck, synccheck)
```

> The AMD equivalents are `rocprofv3` (tracing and counters), `rocprof-sys` (timeline, like Nsight Systems), and `rocprof-compute` (kernel analysis, like Nsight Compute). See [30.5 ROCm Profiling Tools](#305-rocm-profiling-tools) and [AMD GPU Architecture and Profiling](AMD_GPU_Architecture_and_Profiling.md).

---

# 24. Advanced CUDA

---

## 24.1 Dynamic Parallelism

Kernels can launch other kernels from the device (Compute Capability 3.5+):

```cpp
__global__ void parent_kernel(float* data, int N) {
    if (N <= THRESHOLD) {
        sequential_process(data, N);
        return;
    }

    int half = N / 2;
    parent_kernel<<<1, 256>>>(data, half);
    parent_kernel<<<1, 256>>>(data + half, N - half);
    cudaDeviceSynchronize();  // wait for child kernels

    merge(data, half, N);
}
```

Use cases: adaptive algorithms, recursive structures, irregular parallelism. Overhead: child kernel launches are more expensive than host launches.

## 24.2 Multi-GPU Programming

```cpp
int device_count;
cudaGetDeviceCount(&device_count);

// Allocate on multiple GPUs
float* d_data[MAX_GPUS];
for (int i = 0; i < device_count; i++) {
    cudaSetDevice(i);
    cudaMalloc(&d_data[i], bytes_per_gpu);
}

// Enable peer access (direct GPU-GPU transfers via NVLink/PCIe)
for (int i = 0; i < device_count; i++) {
    cudaSetDevice(i);
    for (int j = 0; j < device_count; j++) {
        if (i != j) {
            int can_access;
            cudaDeviceCanAccessPeer(&can_access, i, j);
            if (can_access) cudaDeviceEnablePeerAccess(j, 0);
        }
    }
}

// Direct peer-to-peer copy (no staging through host)
cudaMemcpyPeer(d_data[1], 1, d_data[0], 0, bytes);

// Or async with streams
cudaMemcpyPeerAsync(d_data[1], 1, d_data[0], 0, bytes, stream);
```

### Multi-GPU with Host Threads

```cpp
#pragma omp parallel num_threads(device_count)
{
    int dev = omp_get_thread_num();
    cudaSetDevice(dev);

    float* d_local;
    cudaMalloc(&d_local, bytes_per_gpu);
    cudaMemcpy(d_local, h_data + dev * chunk, bytes_per_gpu, cudaMemcpyHostToDevice);

    kernel<<<blocks, threads>>>(d_local, chunk_size);

    cudaMemcpy(h_data + dev * chunk, d_local, bytes_per_gpu, cudaMemcpyDeviceToHost);
    cudaFree(d_local);
}
```

> **See also:** peer copies are only the first step. For collectives (NCCL/RCCL allreduce and its cost model) see [section 34](#34-collective-communication-algorithms-and-cost-model). For IPC handles, graphs, stream-ordered allocation, stream priorities, and GPU sharing (MPS/MIG and AMD partitions) see [section 35](#35-multi-gpu-programming-beyond-peer-copies-hip). The HIP APIs mirror the CUDA ones.

## 24.3 CUDA-Aware MPI

Directly pass device pointers to MPI calls (requires CUDA-aware MPI implementation):

```cpp
// With CUDA-aware MPI (e.g., OpenMPI built with CUDA support):
float* d_send_buf;
cudaMalloc(&d_send_buf, bytes);

// No need to copy to host first!
MPI_Send(d_send_buf, count, MPI_FLOAT, dest, tag, comm);
MPI_Recv(d_recv_buf, count, MPI_FLOAT, src, tag, comm, &status);

// Also works with collectives
MPI_Allreduce(d_local, d_global, count, MPI_FLOAT, MPI_SUM, comm);
```

## 24.4 Error Handling

```cpp
// Check return value of API calls
cudaError_t err = cudaMalloc(&ptr, bytes);
if (err != cudaSuccess) {
    fprintf(stderr, "CUDA error: %s\n", cudaGetErrorString(err));
    exit(1);
}

// Check for kernel launch errors (asynchronous)
kernel<<<blocks, threads>>>(args);
cudaError_t launch_err = cudaGetLastError();
if (launch_err != cudaSuccess) {
    fprintf(stderr, "Kernel launch error: %s\n", cudaGetErrorString(launch_err));
}

// Synchronize and check for execution errors
cudaError_t exec_err = cudaDeviceSynchronize();
if (exec_err != cudaSuccess) {
    fprintf(stderr, "Kernel execution error: %s\n", cudaGetErrorString(exec_err));
}

// Common macro
#define CUDA_CHECK(call) do { \
    cudaError_t err = (call); \
    if (err != cudaSuccess) { \
        fprintf(stderr, "CUDA Error at %s:%d: %s\n", \
                __FILE__, __LINE__, cudaGetErrorString(err)); \
        exit(1); \
    } \
} while(0)

CUDA_CHECK(cudaMalloc(&ptr, bytes));
CUDA_CHECK(cudaMemcpy(dst, src, bytes, cudaMemcpyHostToDevice));
```

## 24.5 CUDA Libraries Overview

| Library | Purpose | Key Functions |
|---|---|---|
| **cuBLAS** | Dense linear algebra | Matrix multiply, dot product, AXPY |
| **cuSPARSE** | Sparse linear algebra | SpMV, SpMM, sparse solvers |
| **cuFFT** | Fast Fourier Transform | 1D/2D/3D FFT, batched FFT |
| **cuDNN** | Deep neural network primitives | Convolution, pooling, normalization, RNN |
| **cuRAND** | Random number generation | Pseudo-random, quasi-random generators |
| **cuSOLVER** | Dense/sparse solvers | LU, QR, SVD, eigensolvers |
| **Thrust** | High-level parallel algorithms | Sort, reduce, scan, transform (STL-like) |
| **CUB** | Block/warp/device collective primitives | Block reduce, block scan, radix sort |
| **NCCL** | Multi-GPU/multi-node collectives | AllReduce, Broadcast, AllGather |

### Thrust Example

```cpp
#include <thrust/device_vector.h>
#include <thrust/sort.h>
#include <thrust/reduce.h>

thrust::device_vector<float> d_vec(h_vec.begin(), h_vec.end());

thrust::sort(d_vec.begin(), d_vec.end());

float sum = thrust::reduce(d_vec.begin(), d_vec.end(), 0.0f, thrust::plus<float>());

// Transform
thrust::transform(d_a.begin(), d_a.end(), d_b.begin(), d_c.begin(),
                  thrust::plus<float>());
```

---

## Common Interview Questions -- CUDA

**Q: What is a warp, and why is warp divergence important?**

A warp is a group of 32 threads that execute the same instruction simultaneously (SIMT model). When threads within a warp take different branches (divergence), the warp executes both paths serially, masking inactive threads at each path. This effectively halves (or worse) the throughput. Minimizing divergence means structuring code so that all 32 threads in a warp follow the same control flow path.

**Q: Explain the difference between shared memory and global memory.**

Global memory is the large (GBs), high-latency (hundreds of cycles) off-chip memory accessible by all threads and the host. Shared memory is a small (tens of KB), low-latency (~5 cycles) on-chip memory shared only by threads within the same block. Shared memory is programmer-managed (explicit `__shared__` declarations), while global memory is cached through L1/L2. The typical optimization pattern is to load data from global to shared memory cooperatively, synchronize with `__syncthreads()`, then compute from shared memory.

**Q: What is memory coalescing?**

Memory coalescing is when threads in a warp access consecutive memory addresses, allowing the hardware to combine these accesses into a minimal number of memory transactions (ideally one 128-byte transaction). Uncoalesced accesses result in multiple transactions, wasting bandwidth. For coalescing: thread `i` should access address `base + i`, use SoA instead of AoS layouts, and avoid strided access patterns.

**Q: How do CUDA streams enable concurrency?**

Operations within a single stream execute in order, but operations in different streams can execute concurrently. This enables overlapping of: (1) host-to-device transfer with kernel execution, (2) kernel execution with device-to-host transfer, (3) multiple kernel executions. Requirements: use non-default streams, pinned memory for async transfers, and ensure the GPU has enough resources (copy engines, SMs) to run operations simultaneously.

**Q: What is occupancy, and is higher always better?**

Occupancy is the ratio of active warps on an SM to the maximum supported. Higher occupancy helps hide memory latency by allowing the scheduler to switch between warps while others wait on memory. However, maximum occupancy is not always optimal: sometimes using more registers or shared memory per thread (reducing occupancy) yields better per-thread performance that outweighs the latency-hiding benefit. The goal is to achieve enough occupancy to saturate the memory system, then optimize per-thread efficiency.

**Q: Explain Unified Memory and its trade-offs.**

Unified Memory (`cudaMallocManaged`) creates a single address space accessible by both CPU and GPU. The CUDA driver automatically migrates pages between host and device memory on demand. Benefits: simpler programming (no explicit copies), enables oversubscription (data can exceed GPU memory). Drawbacks: page faults cause latency spikes, first-touch may trigger unnecessary migration, and performance is generally lower than explicit memory management. Use `cudaMemPrefetchAsync` and `cudaMemAdvise` to guide the driver for better performance.

**Q: What are CUDA Graphs, and when should you use them?**

CUDA Graphs capture a DAG (directed acyclic graph) of kernels, memory copies, and other operations, then replay them with minimal launch overhead. They are beneficial when: (1) launching many small kernels where CPU launch overhead dominates, (2) the same sequence of operations repeats (iterative algorithms, inference), (3) you need deterministic execution ordering. Graphs reduce per-launch overhead from ~5-10 microseconds to near-zero for replays. They should not be used when the workflow is highly dynamic or changes every iteration.

---

# Part 4: HIP (Heterogeneous-Compute Interface for Portability)

---

# 25. HIP Fundamentals and Portability

---

## 25.1 What is HIP?

HIP (Heterogeneous-Compute Interface for Portability) is AMD's GPU programming API designed to be a thin, portable layer over both **AMD ROCm** and **NVIDIA CUDA** backends. HIP code can compile and run on AMD GPUs (via ROCm) and NVIDIA GPUs (via CUDA) with minimal or no changes.

```
                    HIP Source Code (.cpp / .hip)
                           │
                    ┌──────┴──────┐
                    ▼              ▼
              hipcc (AMD)    hipcc (NVIDIA)
                    │              │
                    ▼              ▼
           ROCm / HIP-Clang    nvcc (CUDA)
                    │              │
                    ▼              ▼
              AMD GPU binary   NVIDIA GPU binary
             (GCN/CDNA/RDNA)   (PTX → SASS)
```

## 25.2 HIP vs CUDA API Mapping

HIP's API is a near-1:1 mapping of CUDA. Most code changes are mechanical find-and-replace:

| CUDA | HIP | Notes |
|---|---|---|
| `cudaMalloc` | `hipMalloc` | Identical semantics |
| `cudaFree` | `hipFree` | Identical semantics |
| `cudaMemcpy` | `hipMemcpy` | Identical semantics |
| `cudaMemcpyAsync` | `hipMemcpyAsync` | Identical semantics |
| `cudaMallocHost` | `hipHostMalloc` | Different name pattern |
| `cudaFreeHost` | `hipHostFree` | Different name pattern |
| `cudaMallocManaged` | `hipMallocManaged` | Identical semantics |
| `cudaStreamCreate` | `hipStreamCreate` | Identical semantics |
| `cudaStreamSynchronize` | `hipStreamSynchronize` | Identical semantics |
| `cudaStreamDestroy` | `hipStreamDestroy` | Identical semantics |
| `cudaEventCreate` | `hipEventCreate` | Identical semantics |
| `cudaEventRecord` | `hipEventRecord` | Identical semantics |
| `cudaEventElapsedTime` | `hipEventElapsedTime` | Identical semantics |
| `cudaDeviceSynchronize` | `hipDeviceSynchronize` | Identical semantics |
| `cudaGetDeviceCount` | `hipGetDeviceCount` | Identical semantics |
| `cudaSetDevice` | `hipSetDevice` | Identical semantics |
| `cudaGetLastError` | `hipGetLastError` | Identical semantics |
| `cudaGetErrorString` | `hipGetErrorString` | Identical semantics |
| `cudaMemcpyHostToDevice` | `hipMemcpyHostToDevice` | Identical semantics |
| `cudaMemcpyDeviceToHost` | `hipMemcpyDeviceToHost` | Identical semantics |
| `cudaMemcpyDeviceToDevice` | `hipMemcpyDeviceToDevice` | Identical semantics |
| `__syncthreads()` | `__syncthreads()` | Identical |
| `threadIdx.x` | `threadIdx.x` | Identical |
| `blockIdx.x` | `blockIdx.x` | Identical |
| `blockDim.x` | `blockDim.x` | Identical |
| `gridDim.x` | `gridDim.x` | Identical |
| `__global__` | `__global__` | Identical |
| `__device__` | `__device__` | Identical |
| `__shared__` | `__shared__` | Identical |
| `__constant__` | `__constant__` | Identical |
| `atomicAdd` | `atomicAdd` | Identical |
| `__shfl_down_sync` | `__shfl_down` | AMD uses wavefront-width shuffle |

## 25.3 AMD GPU Architecture

| Concept | NVIDIA Term | AMD Term |
|---|---|---|
| Processing unit | Streaming Multiprocessor (SM) | Compute Unit (CU) |
| Thread group in lockstep | Warp (32 threads) | Wavefront (64 threads, or 32 on RDNA) |
| Thread block | Thread Block | Workgroup |
| Global thread grid | Grid | NDRange |
| Fast on-chip memory | Shared Memory | Local Data Share (LDS) |
| Vector ALUs | CUDA Cores | Stream Processors |
| Scalar ALU | N/A (implicit) | Scalar Unit (SU) |
| Register file | Register File | Vector GPRs (VGPRs) + Scalar GPRs (SGPRs) |

### AMD GPU Architecture Families

| Family | Architecture | Target Market | Wavefront Size |
|---|---|---|---|
| GCN (1-5) | Graphics Core Next | Legacy GPUs | 64 |
| CDNA | Compute DNA (MI100, MI200, MI300) | Data center / HPC | 64 |
| RDNA (1-3) | Radeon DNA | Consumer / Gaming | 32 (native), 64 (wave64 mode) |

## 25.4 ROCm Software Stack

```
Application Code (HIP / OpenCL / OpenMP)
         │
    HIP Runtime API
         │
    ┌────┴────┐
    ▼         ▼
 ROCr      CUDA RT    (runtime backends)
    │         │
    ▼         ▼
 HSA/KFD   NVIDIA     (kernel drivers)
    │      Driver
    ▼         ▼
 AMD GPU   NVIDIA GPU
```

Key ROCm components:
- **hipcc**: HIP compiler (wraps `amdclang++` for AMD or `nvcc` for NVIDIA)
- **ROCr**: ROCm runtime (HSA-based)
- **rocBLAS, rocFFT, rocSOLVER**: Math libraries (CUDA library equivalents)
- **MIOpen**: Deep learning primitives (cuDNN equivalent)
- **RCCL**: Multi-GPU collectives (NCCL equivalent)
- **ROCprofiler-SDK** (`rocprofv3`), **ROCm Compute Profiler** (`rocprof-compute`, formerly Omniperf), **ROCm Systems Profiler** (`rocprof-sys`, formerly Omnitrace): profiling tools. The legacy `rocprof`/`rocprofv2` and the ROCProfiler v1/ROCTracer libraries are deprecated. See [30.5](#305-rocm-profiling-tools).

## 25.5 Compilation

```bash
# AMD GPU target
hipcc -o program program.cpp

# Specific AMD architecture
hipcc --offload-arch=gfx90a -o program program.cpp   # MI210/MI250
hipcc --offload-arch=gfx942 -o program program.cpp   # MI300

# NVIDIA GPU target (on systems with CUDA installed)
hipcc --platform nvidia -o program program.cpp

# Check platform
hipconfig --platform   # prints "amd" or "nvidia"
```

> **See also:** for real projects use CMake's first-class HIP language (`enable_language(HIP)`, `CMAKE_HIP_ARCHITECTURES`, `hip::host` / `hip::device`) rather than wrapping `hipcc`: [CMake Fundamentals -- HIP and ROCm with CMake](../tools/CMake_Fundamentals.md#64-hip-and-rocm-with-cmake).

---

# 26. HIP Programming Model

---

## 26.1 Kernel Definition

Identical to CUDA:

```cpp
#include <hip/hip_runtime.h>

__global__ void vector_add(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}
```

## 26.2 Kernel Launch

HIP supports two launch syntaxes:

```cpp
// Method 1: CUDA-style triple chevron (recommended)
vector_add<<<grid, block, shared_mem, stream>>>(d_a, d_b, d_c, N);

// Method 2: HIP-specific macro (legacy, sometimes needed for portability)
hipLaunchKernelGGL(vector_add, grid, block, shared_mem, stream,
                   d_a, d_b, d_c, N);
```

## 26.3 Complete Example: Vector Addition in HIP

```cpp
#include <hip/hip_runtime.h>
#include <stdio.h>

#define HIP_CHECK(call) do { \
    hipError_t err = (call); \
    if (err != hipSuccess) { \
        fprintf(stderr, "HIP Error at %s:%d: %s\n", \
                __FILE__, __LINE__, hipGetErrorString(err)); \
        exit(1); \
    } \
} while(0)

__global__ void vector_add(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    int N = 1 << 20;
    size_t bytes = N * sizeof(float);

    float *h_a = (float*)malloc(bytes);
    float *h_b = (float*)malloc(bytes);
    float *h_c = (float*)malloc(bytes);

    for (int i = 0; i < N; i++) {
        h_a[i] = 1.0f;
        h_b[i] = 2.0f;
    }

    float *d_a, *d_b, *d_c;
    HIP_CHECK(hipMalloc(&d_a, bytes));
    HIP_CHECK(hipMalloc(&d_b, bytes));
    HIP_CHECK(hipMalloc(&d_c, bytes));

    HIP_CHECK(hipMemcpy(d_a, h_a, bytes, hipMemcpyHostToDevice));
    HIP_CHECK(hipMemcpy(d_b, h_b, bytes, hipMemcpyHostToDevice));

    int block_size = 256;
    int grid_size = (N + block_size - 1) / block_size;
    vector_add<<<grid_size, block_size>>>(d_a, d_b, d_c, N);
    HIP_CHECK(hipGetLastError());

    HIP_CHECK(hipMemcpy(h_c, d_c, bytes, hipMemcpyDeviceToHost));

    printf("c[0] = %f\n", h_c[0]);  // 3.0

    hipFree(d_a); hipFree(d_b); hipFree(d_c);
    free(h_a); free(h_b); free(h_c);
    return 0;
}
```

> **See also:** the same vector add as a multi-file CMake project, with the kernel in a `.hip` file compiled by ROCm clang and host-only code compiled by `g++` against `hip::host`, is in [CMake Fundamentals -- The HIP Language: A Complete Project](../tools/CMake_Fundamentals.md#642-the-hip-language-a-complete-project).

## 26.4 Device Properties

```cpp
int device_count;
hipGetDeviceCount(&device_count);

for (int i = 0; i < device_count; i++) {
    hipDeviceProp_t props;
    hipGetDeviceProperties(&props, i);

    printf("Device %d: %s\n", i, props.name);
    printf("  Compute Units: %d\n", props.multiProcessorCount);
    printf("  Max threads/block: %d\n", props.maxThreadsPerBlock);
    printf("  Warp size: %d\n", props.warpSize);  // 64 on AMD CDNA, 32 on RDNA/NVIDIA
    printf("  Shared mem/block: %zu KB\n", props.sharedMemPerBlock / 1024);
    printf("  Global memory: %zu GB\n", props.totalGlobalMem / (1024*1024*1024));
    printf("  Clock rate: %d MHz\n", props.clockRate / 1000);
    printf("  GCN Arch: gfx%d\n", props.gcnArch);
}
```

---

# 27. HIP Memory Management

---

## 27.1 Device Memory

```cpp
float* d_ptr;
hipMalloc(&d_ptr, N * sizeof(float));
hipMemset(d_ptr, 0, N * sizeof(float));
hipMemcpy(d_ptr, h_ptr, N * sizeof(float), hipMemcpyHostToDevice);
hipMemcpy(h_ptr, d_ptr, N * sizeof(float), hipMemcpyDeviceToHost);
hipFree(d_ptr);
```

## 27.2 Pinned (Page-Locked) Memory

```cpp
float* h_pinned;

// Default pinned memory
hipHostMalloc(&h_pinned, bytes, hipHostMallocDefault);

// Portable: accessible from all GPUs
hipHostMalloc(&h_pinned, bytes, hipHostMallocPortable);

// Mapped: also accessible from device via pointer
hipHostMalloc(&h_pinned, bytes, hipHostMallocMapped);

// Write-combined: best for host-to-device streaming
hipHostMalloc(&h_pinned, bytes, hipHostMallocWriteCombined);

// Get device-accessible pointer for mapped memory
float* d_mapped;
hipHostGetDevicePointer(&d_mapped, h_pinned, 0);

// Free
hipHostFree(h_pinned);
```

## 27.3 Managed Memory

```cpp
float* managed;
hipMallocManaged(&managed, bytes);

// Initialize on host
for (int i = 0; i < N; i++) managed[i] = i;

// Use on device
kernel<<<blocks, threads>>>(managed, N);
hipDeviceSynchronize();

// Access on host (automatic migration)
printf("%f\n", managed[0]);

// Prefetch for performance
hipMemPrefetchAsync(managed, bytes, deviceId, stream);

hipFree(managed);
```

## 27.4 HIP vs CUDA Memory API Comparison

| CUDA Function | HIP Function | Notes |
|---|---|---|
| `cudaMalloc` | `hipMalloc` | Identical |
| `cudaFree` | `hipFree` | Identical |
| `cudaMemcpy` | `hipMemcpy` | Identical |
| `cudaMemcpyAsync` | `hipMemcpyAsync` | Identical |
| `cudaMemset` | `hipMemset` | Identical |
| `cudaMallocHost` | `hipHostMalloc` | Different naming; HIP uses flags |
| `cudaFreeHost` | `hipHostFree` | Different naming |
| `cudaHostAlloc` | `hipHostMalloc` | Unified in HIP |
| `cudaMallocManaged` | `hipMallocManaged` | Identical |
| `cudaMemPrefetchAsync` | `hipMemPrefetchAsync` | Identical |
| `cudaMemAdvise` | `hipMemAdvise` | Identical |
| `cudaMemcpyToSymbol` | `hipMemcpyToSymbol` | Identical |

---

# 28. HIP Streams, Events, and Synchronization

---

## 28.1 Streams

```cpp
hipStream_t stream;
hipStreamCreate(&stream);

hipMemcpyAsync(d_a, h_a, bytes, hipMemcpyHostToDevice, stream);
kernel<<<blocks, threads, 0, stream>>>(d_a, d_b, N);
hipMemcpyAsync(h_b, d_b, bytes, hipMemcpyDeviceToHost, stream);

hipStreamSynchronize(stream);
hipStreamDestroy(stream);

// Non-blocking stream (independent from NULL stream)
hipStream_t nb_stream;
hipStreamCreateWithFlags(&nb_stream, hipStreamNonBlocking);
```

## 28.2 Events

```cpp
hipEvent_t start, stop;
hipEventCreate(&start);
hipEventCreate(&stop);

hipEventRecord(start, stream);
kernel<<<blocks, threads, 0, stream>>>(args);
hipEventRecord(stop, stream);

hipEventSynchronize(stop);

float ms = 0;
hipEventElapsedTime(&ms, start, stop);
printf("Kernel time: %.3f ms\n", ms);

hipEventDestroy(start);
hipEventDestroy(stop);
```

## 28.3 Block and Warp Synchronization

```cpp
// Block barrier (identical to CUDA)
__syncthreads();

// AMD wavefront-aware shuffle operations
// Key difference: AMD CDNA wavefront = 64 threads, NVIDIA warp = 32 threads

// Portable warp/wavefront shuffle
int val = __shfl(source_val, src_lane);           // broadcast from src_lane
int val = __shfl_up(source_val, delta);            // shift up
int val = __shfl_down(source_val, delta);          // shift down
int val = __shfl_xor(source_val, lane_mask);       // butterfly

// On AMD, these operate on 64-lane wavefronts by default
// On NVIDIA backend, these map to the _sync variants with full mask
```

> **See also:** [36.6 AMD cross-lane operations](#366-amd-cross-lane-operations-dpp-ds_swizzle-ds_bpermute-readlane) for the cross-lane mechanisms (DPP, `ds_swizzle`, `ds_bpermute`, `v_readlane`); `__shfl*` itself always compiles to `ds_bpermute_b32`, and [36.7](#367-porting-warp32-code-to-wave64-ballot-masks-and-other-traps) for the 64-bit ballot-mask traps. As of ROCm 7.0, the `_sync` variants (with 64-bit masks) are enabled by default and `warpSize` is no longer `constexpr`.

### Handling Wavefront Size Differences

```cpp
// Portable warp/wavefront size query
int warp_size = warpSize;  // 64 on AMD CDNA, 32 on NVIDIA

// Use warpSize instead of hardcoding 32
__device__ float wavefront_reduce_sum(float val) {
    for (int offset = warpSize / 2; offset > 0; offset >>= 1) {
        val += __shfl_down(val, offset);
    }
    return val;
}

// Do NOT derive the wave size from __HIP_PLATFORM_AMD__: RDNA (gfx10+) is wave32,
// and since ROCm 7.0 warpSize is no longer constexpr. Use the runtime warpSize in
// device code, or rocprim::arch::wavefront::min_size()/max_size() for compile-time
// bounds (see 36.7).
```

## 28.4 Atomic Operations

Identical API to CUDA, fully supported on AMD GPUs:

```cpp
atomicAdd(&sum, val);
atomicMin(&min_val, val);
atomicMax(&max_val, val);
atomicCAS(&slot, compare, val);
atomicExch(&slot, val);
atomicAnd(&flags, mask);
atomicOr(&flags, mask);
atomicXor(&flags, mask);
```

---

# 29. CUDA-to-HIP Porting

---

## 29.1 Hipify Tools

AMD provides automated conversion tools:

```bash
# Perl-based converter (fast, string replacement)
hipify-perl cuda_source.cu > hip_source.cpp

# Clang-based converter (AST-aware, more accurate)
hipify-clang cuda_source.cu -o hip_source.cpp -- -I/path/to/cuda/include

# Convert an entire directory
hipify-perl --inplace --print-stats directory/

# Generate conversion statistics
hipify-perl --print-stats cuda_source.cu
```

### What Hipify Converts

| Category | CUDA | HIP (after hipify) |
|---|---|---|
| Header | `#include <cuda_runtime.h>` | `#include <hip/hip_runtime.h>` |
| Memory | `cudaMalloc`, `cudaFree` | `hipMalloc`, `hipFree` |
| Streams | `cudaStream_t`, `cudaStreamCreate` | `hipStream_t`, `hipStreamCreate` |
| Events | `cudaEvent_t`, `cudaEventRecord` | `hipEvent_t`, `hipEventRecord` |
| Error types | `cudaError_t`, `cudaSuccess` | `hipError_t`, `hipSuccess` |
| Kernel launch | `<<<blocks, threads>>>` | `<<<blocks, threads>>>` (unchanged) |
| Intrinsics | `__syncthreads()` | `__syncthreads()` (unchanged) |
| Device qualifiers | `__global__`, `__device__` | `__global__`, `__device__` (unchanged) |

### What Hipify Does NOT Convert

- Algorithm differences (warp size 64 vs 32 assumptions)
- Inline PTX assembly
- Some advanced CUDA features without direct HIP equivalents
- Performance optimizations specific to NVIDIA hardware

> **See also:** hipify converts the source, but the build must be ported too. In CMake, keep the hipified files named `.cu` and mark them `LANGUAGE HIP` ([Compiling `.cpp` or `.cu` Files as HIP](../tools/CMake_Fundamentals.md#643-compiling-cpp-or-cu-files-as-hip)). Then swap `CUDA` for `HIP` in `project()` and the `*_ARCHITECTURES` variables, and replace `CUDA::cublas` and similar targets with `roc::rocblas` and the other ROCm targets ([CUDA vs HIP in CMake](../tools/CMake_Fundamentals.md#646-cuda-vs-hip-in-cmake)). Relocatable device code needs `-fgpu-rdc`, because HIP has no `CUDA_SEPARABLE_COMPILATION` property.

## 29.2 Platform-Specific Code

```cpp
#ifdef __HIP_PLATFORM_AMD__
    // AMD-specific code
    #include <hip/amd_detail/amd_hip_runtime.h>
#elif defined(__HIP_PLATFORM_NVIDIA__)
    // NVIDIA-specific code (HIP on CUDA backend)
#endif

// Compile-time feature detection
#if defined(__gfx90a__)
    // MI200-specific optimizations
#elif defined(__gfx942__)
    // MI300-specific optimizations
#endif
```

## 29.3 Common Porting Pitfalls

| Issue | CUDA Assumption | AMD Reality | Fix |
|---|---|---|---|
| Warp size | Always 32 | 64 on CDNA, 32 on RDNA | Use `warpSize` variable |
| Shared memory | Up to 48 KB default | Up to 64 KB per CU | Check `hipDeviceProp_t` |
| `__shfl_sync` mask | `0xFFFFFFFF` (32 bits) | 64-bit wavefront needs `0xFFFFFFFFFFFFFFFF` | ROCm 7.0+: `__shfl_sync` etc. require a 64-bit mask (`0xffffffffffffffffull` or `__activemask()`). ROCm 6.2-6.4: opt in with `-DHIP_ENABLE_WARP_SYNC_BUILTINS`, or use the mask-free `__shfl*` |
| Warp ballot | Returns `unsigned int` (32 bits) | Returns `unsigned long long` (64 bits) | Use appropriate type |
| Register pressure | ~255 regs/thread | VGPRs differ per arch | `-Rpass-analysis=kernel-resource-usage` at compile time; `rocprofv3 --kernel-trace` at run time |
| Cooperative groups | Extensive API | Partial support | Check HIP documentation |
| Dynamic parallelism | Supported | Limited support | Restructure if needed |
| Inline PTX | NVIDIA ISA | Not portable | Use HIP intrinsics or inline GCN |
| Texture objects | `cudaTextureObject_t` | `hipTextureObject_t` (partial) | Test thoroughly |

## 29.4 Writing Portable CUDA/HIP Code

```cpp
// Single-source approach using macros
#ifdef __HIP_PLATFORM_AMD__
    #include <hip/hip_runtime.h>
#else
    #include <cuda_runtime.h>
    #define hipMalloc cudaMalloc
    #define hipFree cudaFree
    #define hipMemcpy cudaMemcpy
    #define hipMemcpyHostToDevice cudaMemcpyHostToDevice
    #define hipMemcpyDeviceToHost cudaMemcpyDeviceToHost
    #define hipDeviceSynchronize cudaDeviceSynchronize
    #define hipGetLastError cudaGetLastError
    #define hipSuccess cudaSuccess
    #define hipError_t cudaError_t
    // ... etc
#endif

// Alternatively, just write HIP -- hipcc compiles it for NVIDIA too
```

> **See also:** one CMake build can target either vendor. Set `CMAKE_HIP_PLATFORM=amd|nvidia` (CMake 3.28+) with the HIP language, or keep separate `CUDA` and `HIP` language targets behind an option. See [CMake Fundamentals -- CUDA vs HIP in CMake](../tools/CMake_Fundamentals.md#646-cuda-vs-hip-in-cmake) and [Three Ways to Build HIP Code](../tools/CMake_Fundamentals.md#641-three-ways-to-build-hip-code).

---

# 30. HIP Performance Tuning for AMD GPUs

---

## 30.1 AMD CDNA Architecture Considerations

CDNA (MI100, MI200, MI300 series) is AMD's data center GPU architecture:

| Feature | NVIDIA A100 (Ampere) | AMD MI250X (CDNA2) | AMD MI300X (CDNA3) |
|---|---|---|---|
| Compute Units / SMs | 108 SMs | 220 CUs (2 GCDs) | 304 CUs (8 XCDs) |
| FP64 TFLOPS | 9.7 | 47.9 | 81.7 |
| FP32 TFLOPS | 19.5 | 47.9 | 163.4 |
| Memory | 80 GB HBM2e | 128 GB HBM2e | 192 GB HBM3 |
| Memory BW | 2.0 TB/s | 3.2 TB/s | 5.3 TB/s |
| Interconnect | NVLink | Infinity Fabric | Infinity Fabric |
| Warp/Wavefront | 32 | 64 | 64 |

## 30.2 Wavefront Occupancy and Register Usage

AMD GPUs have two types of general-purpose registers:

- **VGPRs** (Vector General Purpose Registers): per-lane (per-thread) registers
- **SGPRs** (Scalar General Purpose Registers): shared across the wavefront

```
CU Register Budget (CDNA2 example):
  - 512 VGPRs per SIMD unit
  - 4 SIMD units per CU
  - Total: 2048 VGPRs per CU

Occupancy impact:
  - If kernel uses 128 VGPRs/thread → 512/128 = 4 wavefronts/SIMD
  - If kernel uses 256 VGPRs/thread → 512/256 = 2 wavefronts/SIMD
```

```bash
# Compile time: the compiler reports per-kernel resource usage and the
# occupancy those resources allow (no GPU needed).
hipcc -O3 --offload-arch=gfx942 -Rpass-analysis=kernel-resource-usage -c kernel.hip
#   kernel.hip:18:0: Function Name: _Z9block_sumPKiPii
#   kernel.hip:18:0:     TotalSGPRs: 16
#   kernel.hip:18:0:     VGPRs: 14
#   kernel.hip:18:0:     AGPRs: 0
#   kernel.hip:18:0:     ScratchSize [bytes/lane]: 0        <- non-zero means register spills
#   kernel.hip:18:0:     Occupancy [waves/SIMD]: 8
#   kernel.hip:18:0:     LDS Size [bytes/block]: 4224

# Run time: rocprofv3's kernel trace records the resources of every dispatch.
# ROCm 7.x: collect in the default rocpd (SQLite) format, then convert/summarize.
rocprofv3 --kernel-trace -d prof -o run -- ./my_app          # -> prof/run_results.db
rocpd convert -i prof/run_results.db -f csv -d prof_csv      # kernel trace CSV
rocpd summary -i prof/run_results.db                         # per-kernel stats
# ROCm 6.x / quick look (direct CSV is deprecated on 7.x):
rocprofv3 --kernel-trace --stats --output-format csv -d prof -o run -- ./my_app
#   The kernel-trace CSV has VGPR_Count, Accum_VGPR_Count (AGPRs), SGPR_Count,
#   LDS_Block_Size, Scratch_Size per dispatch; the 6.x run_kernel_stats.csv has
#   per-kernel call counts and total/avg/min/max durations.
```

The run-time `VGPR_Count` can be larger than the compile-time `VGPRs` (16 vs 14 for the kernel above). The trace reports the *allocated* count, which is rounded up to the VGPR allocation granule. Occupancy is computed from the rounded value.

> **Legacy note:** older material uses `rocprof --stats` / `rocprof --hsa-trace` (rocprof v1). Those flags still exist on older installs, but the tool is deprecated. Note that in `rocprofv3`, `--hip-trace` and `--hsa-trace` trace **only** the API calls. Kernel dispatches need `--kernel-trace` (or the aggregate `--runtime-trace` / `--sys-trace`), and `--stats` must be combined with a tracing option.

## 30.3 LDS (Local Data Share) Optimization

LDS is AMD's equivalent of CUDA shared memory:

```cpp
// LDS declaration (same as shared memory syntax)
__shared__ float lds_data[256];

// LDS limits per CU:
//   CDNA2 (MI200): 64 KB LDS per CU
//   CDNA3 (MI300): 64 KB LDS per CU
//   RDNA3: 64 KB LDS per WGP (2 CUs)

// LDS bank conflicts:
//   - 32 banks on AMD (same as NVIDIA)
//   - Bank width: 4 bytes
//   - Same conflict avoidance techniques apply (padding, etc.)
```

## 30.4 Memory Coalescing on AMD

AMD GPUs have similar coalescing rules but with wavefront-width considerations:

```cpp
// GOOD: 64 consecutive threads access 64 consecutive elements
// → 2 × 128-byte transactions (coalesced)
data[global_id] = value;

// BAD: stride-2 access with 64-thread wavefront
// → 4 × 128-byte transactions (still somewhat efficient due to cache)
data[global_id * 2] = value;

// AMD L1/L2 cache can mitigate some uncoalesced patterns,
// but coalesced access is still critical for performance
```

## 30.5 ROCm Profiling Tools

This section is a working summary of the commands. Counter meanings, derived metrics, the top-down speed-of-light method, and how a profiler intercepts dispatches without changing the application are covered in [AMD GPU Architecture and Profiling](AMD_GPU_Architecture_and_Profiling.md). How to build a custom rocprofiler-sdk tool library (`find_package(rocprofiler-sdk)`, the `rocprofiler_configure` entry point, hidden visibility) and how to link ROCTx markers is in [CMake Fundamentals -- Linking ROCm Libraries and Profiler SDKs](../tools/CMake_Fundamentals.md#645-linking-rocm-libraries-and-profiler-sdks).

### Tool Map (Current Names and Former Names)

| Tool (binary) | Formerly | Layer | Purpose | NVIDIA analogue |
|---|---|---|---|---|
| **ROCprofiler-SDK** (library) | ROCProfiler v1/v2 + ROCTracer | Library / tool API | Callback and buffered tracing, counter collection, PC sampling, thread trace. Every tool below is built on it | CUPTI |
| **`rocprofv3`** | `rocprof` (v1), `rocprofv2` | CLI on the SDK | API/kernel/memory tracing, `--stats`, hardware counters (`--pmc`) | `nsys` CLI + `ncu --metrics` |
| **`rocprof-sys`** (ROCm Systems Profiler) | Omnitrace (`omnitrace-*`) | Whole-application timeline | CPU sampling + instrumentation, HIP/HSA/RCCL/MPI/OpenMP, GPU activity, Perfetto output | Nsight Systems |
| **`rocprof-compute`** (ROCm Compute Profiler) | Omniperf (`omniperf`) | Per-kernel deep dive | Speed-of-light panels, memory chart, roofline, instruction mix, occupancy limiters | Nsight Compute |
| **`amd-smi`** | `rocm-smi` (still shipped) | Device management | Utilization, power, clocks, partitions, xGMI topology | `nvidia-smi` |
| **`roc-obj-ls` / `roc-obj`** | -- | Binary inspection | List and extract code objects (`.hsaco`) embedded in a fat binary | `cuobjdump` |

The renames took effect in **ROCm 6.3** (December 2024). The packages became `rocprofiler-compute` and `rocprofiler-systems`, and the binaries became `rocprof-compute` and `rocprof-sys-*`. `rocprofv3` with ROCprofiler-SDK became the recommended profiler in the ROCm 6.2-6.4 timeframe. ROCm 6.4 put the legacy `rocprof`, `rocprofv2`, ROCProfiler, and ROCTracer into critical-fixes-only mode, and they are scheduled for end of support. In **ROCm 7.0**, `rocprofv3`'s default output format became **rocpd** (a SQLite database), and `rocprof-compute` switched to `rocprofv3` as its default collection backend.

### rocprofv3: Tracing and Counters

```bash
# Kernel timeline + per-kernel stats (the replacement for "rocprof --stats").
# ROCm 7.x: collect in the default rocpd format (SQLite), then post-process.
rocprofv3 --kernel-trace -d prof -o run -- ./my_app              # -> prof/run_results.db
rocpd summary -i prof/run_results.db                             # per-kernel stats (--format csv|md|json|html)
rocpd convert -i prof/run_results.db -f csv pftrace -d prof_out  # CSV tables + Perfetto trace

# ROCm 6.x / quick look: direct CSV (deprecated on 7.x, see the note below)
rocprofv3 --kernel-trace --stats --output-format csv -d prof -o run -- ./my_app
#   prof/run_kernel_trace.csv  prof/run_kernel_stats.csv

# Everything the HIP runtime does (HIP API, kernels, copies, markers, RCCL) as a Perfetto trace
rocprofv3 --runtime-trace -- ./my_app        # default rocpd .db; rocpd convert -f pftrace -> ui.perfetto.dev
rocprofv3 --sys-trace -- ./my_app            # adds HSA API tracing; default output is rocpd (.db)

# Summary table printed at exit
rocprofv3 --kernel-trace --memory-copy-trace -S -- ./my_app

# Hardware counters. One --pmc group = one pass; several --pmc flags = several application replays
rocprofv3 -L                                                     # list counters available on this GPU
rocprofv3 --pmc SQ_WAVES SQ_INSTS_VALU GRBM_GUI_ACTIVE \
          --kernel-include-regex "gemm" -- ./my_app
#   -> rocpd .db; after rocpd convert -f csv (or --output-format csv on 6.x):
#      *_counter_collection.csv, one row per (dispatch, counter)

# Same thing from an input file (text, YAML or JSON)
printf 'pmc: SQ_WAVES SQ_INSTS_VALU\npmc: TCC_HIT_sum TCC_MISS_sum\n' > counters.txt
rocprofv3 -i counters.txt -- ./my_app

# MPI: put the profiler inside the launcher; one output per rank
mpirun -n 4 rocprofv3 --kernel-trace -- ./my_mpi_app      # one <host>/<pid>_results.db per rank

# rocpd databases can be converted or queried after the run (several -i inputs are allowed)
rocpd convert -i <host>/<pid>_results.db --output-format csv pftrace
rocpd summary -i <host>/<pid>_results.db
```

> **Output-format note (ROCm 7.x):** `rocprofv3 --help` and the ROCprofiler-SDK docs say that direct `csv`, `pftrace`, and `otf2` output is **deprecated**. Use the default `rocpd` output plus `rocpd convert`. Direct formats can omit data for some tracing features (for example hipFILE and rocSHMEM records). Because rocpd is the default from ROCm 7.0, `--stats` on its own no longer gives you the `*_stats.csv` files older guides show. Get per-kernel statistics from `rocpd summary`. `--output-format csv` is still the shortest path on ROCm 6.x installs.

Things to know (interviewers ask about these):
- **`--hip-trace` and `--hsa-trace` trace only API calls** in `rocprofv3`. Use `--kernel-trace` / `--memory-copy-trace`, or the aggregates `--runtime-trace` / `--sys-trace`, to see GPU activity. `--stats` needs at least one tracing option.
- **Counter collection perturbs the run.** Dispatches are serialized so counters can be attributed to one kernel, and counter sets that do not fit in the hardware counter slots need multiple passes (application replay). That only works if the app is deterministic. Derived metrics computed across passes assume each pass did the same work.
- **Filter early**, with `--kernel-include-regex` and `--kernel-iteration-range`, or with ROCTx regions plus `--selected-regions`. A full-application counter run on a training job is slow and produces huge files.
- **Mark regions** with ROCTx (`roctxRangePush/Pop`, link `-lrocprofiler-sdk-roctx`) and trace them with `--marker-trace`. `--kernel-rename` renames kernels by their enclosing ROCTx range.

### rocprof-sys: Whole-Application Timeline

```bash
rocprof-sys-avail --all                                   # list components/settings (ROCPROFSYS_* env vars)
rocprof-sys-instrument -- ./my_app                        # runtime instrumentation (like gdb --args)
rocprof-sys-instrument -o my_app.inst -- ./my_app         # binary rewrite once...
rocprof-sys-run -- ./my_app.inst                          # ...then run the rewritten binary
rocprof-sys-sample -- ./my_app                            # statistical sampling only, lowest overhead
# Output: Perfetto .proto trace (CPU call stacks, threads, HIP/HSA/RCCL/MPI, GPU kernels) + text/JSON profiles
```

Use it first when the question is "where does wall-clock time go?". Typical findings are GPU idle gaps between kernels, host-side launch overhead, synchronous copies, MPI/RCCL waits, and data-loader stalls. It is the right tool for those, and `rocprof-compute` is not.

### rocprof-compute: Kernel-Level Analysis

```bash
# Profile: replays the app for counter passes, then runs roofline microbenchmarks
rocprof-compute profile --name my_app -- ./my_app --size 4096
rocprof-compute profile --name my_app -k gemm --kernel-iteration-range 1 -- ./my_app  # first gemm dispatch (3.10+)
#   Dispatch-filter semantics are version-specific: 3.10 renamed -d/--dispatch to
#   --kernel-iteration-range (1-based per-kernel iteration) and -d now means
#   --output-directory. Older releases used -d/--dispatch, documented as a 0-based
#   dispatch id ("-d 0" = first), though some 3.9 builds already treat it as 1-based
#   per kernel. Check `rocprof-compute profile --help` on the installed version.
rocprof-compute profile --name my_app --roof-only -- ./my_app      # roofline counters only
rocprof-compute profile --list-available-metrics                   # block -> section -> metric ids

# Analyze: results live under workloads/<name>/<gpu_model>/
rocprof-compute analyze -p workloads/my_app/MI300X_A1/ --list-stats   # kernels and dispatch ids
rocprof-compute analyze -p workloads/my_app/MI300X_A1/ -k 0           # CLI report for kernel id 0
rocprof-compute analyze -p workloads/my_app/MI300X_A1/ --output-format db   # SQLite report for ROCm Optiq
```

Version note: the experimental `--gui` and `--tui` analyze interfaces were removed in rocprof-compute 3.11.0, so use the CLI or `--output-format db` with ROCm Optiq. See the version timeline in [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md#4-history-and-version-timeline).

Read the report top-down:
1. **Speed of light (SOL)**: achieved VALU/MFMA FLOP/s and HBM/L2/L1/LDS bandwidth as a percentage of peak. This tells you which ceiling is close.
2. **Roofline**: the kernel's arithmetic intensity against empirically measured ceilings (worked math in [Performance Engineering -- Roofline](../computer-science/Performance_Engineering.md#3-roofline-model)).
3. **Memory chart**: L1/L2 hit rates, HBM traffic, and LDS bank conflicts. Ask whether the data movement is necessary.
4. **Wavefront / occupancy**: VGPR, LDS, or scratch limiters, and why waves stall (waiting on memory, barriers, dependencies).
5. **Instruction mix**: VALU vs MFMA vs VMEM vs SALU vs LDS. A memory-bound kernel that is also VALU-heavy from address arithmetic is a hint.

### Which Tool When

| Question | Tool |
|---|---|
| Which kernels dominate, how long do they take, are there gaps? | `rocprofv3 --kernel-trace` + `rocpd summary` (or `--stats --output-format csv` on 6.x), or `--runtime-trace` + `rocpd convert -f pftrace` + Perfetto |
| Why is end-to-end time high (CPU, I/O, MPI, launch overhead)? | `rocprof-sys` |
| Why is *this kernel* slow (memory vs compute vs latency)? | `rocprof-compute` |
| A specific counter for a specific kernel in CI | `rocprofv3 --pmc ... --kernel-include-regex` |
| Registers, spills, occupancy before running | `-Rpass-analysis=kernel-resource-usage`, `--save-temps` (ISA) |
| Live device health, clocks, partitions | `amd-smi` |

## 30.6 NVIDIA vs AMD GPU Terminology

| Concept | NVIDIA | AMD |
|---|---|---|
| GPU compute unit | Streaming Multiprocessor (SM) | Compute Unit (CU) |
| Thread group (SIMT) | Warp (32 threads) | Wavefront (64 threads CDNA, 32 RDNA) |
| Thread block | Block | Workgroup |
| Grid | Grid | NDRange |
| Shared memory | Shared Memory | LDS (Local Data Share) |
| Vector registers | Registers | VGPRs |
| Scalar registers | N/A | SGPRs |
| L1 cache | L1 / Shared (configurable) | L1 (separate from LDS) |
| L2 cache | L2 | L2 |
| Interconnect | NVLink | Infinity Fabric |
| Multi-GPU comms | NCCL | RCCL |
| Compiler | nvcc | hipcc (amdclang++) |
| ISA | PTX → SASS | AMDGPU IR → GCN/CDNA ISA |
| Profiler | Nsight Compute / Nsight Systems / CUPTI | rocprof-compute (formerly Omniperf) / rocprof-sys (formerly Omnitrace) / rocprofv3 on ROCprofiler-SDK |
| Compute sanitizer | compute-sanitizer | rocm-debug-agent |

---

# 31. ROCm Ecosystem and Libraries

---

## 31.1 Math Libraries

| CUDA Library | ROCm Equivalent | Purpose |
|---|---|---|
| cuBLAS | **rocBLAS** | Dense linear algebra (GEMM, AXPY, DOT) |
| cuBLASLt | **hipBLASLt** | Lightweight BLAS with extended functionality |
| cuSPARSE | **rocSPARSE** | Sparse linear algebra (SpMV, SpMM) |
| cuFFT | **rocFFT** | Fast Fourier Transform |
| cuSOLVER | **rocSOLVER** | Dense solvers (LU, QR, SVD, eigensolvers) |
| cuRAND | **rocRAND** | Random number generation |
| cuDNN | **MIOpen** | Deep learning primitives |
| NCCL | **RCCL** | Multi-GPU/node collectives |
| Thrust | **rocThrust** | High-level parallel algorithms |
| CUB | **hipCUB** | Block/warp/device primitives |
| cuTENSOR | **hipTensor** | Tensor contractions |

> **See also:** link these through their CMake config packages, not with `-lrocblas -I/opt/rocm/include`. Use `find_package(rocblas)` with `roc::rocblas`, `find_package(rccl)` with `roc::rccl`, and so on. The namespaces are inconsistent (`roc::`, `hip::`, none); the full table is in [CMake Fundamentals -- Linking ROCm Libraries and Profiler SDKs](../tools/CMake_Fundamentals.md#645-linking-rocm-libraries-and-profiler-sdks). One `-DCMAKE_PREFIX_PATH=/opt/rocm` finds all of them ([Finding ROCm](../tools/CMake_Fundamentals.md#644-finding-rocm-cmake_prefix_path-hiphost-hipdevice)).

### Example: rocBLAS GEMM

```cpp
#include <rocblas/rocblas.h>

rocblas_handle handle;
rocblas_create_handle(&handle);

// C = alpha * A * B + beta * C
float alpha = 1.0f, beta = 0.0f;
rocblas_sgemm(handle,
              rocblas_operation_none,  // op(A) = A
              rocblas_operation_none,  // op(B) = B
              M, N, K,
              &alpha,
              d_A, M,     // lda
              d_B, K,     // ldb
              &beta,
              d_C, M);    // ldc

rocblas_destroy_handle(handle);
```

### Example: rocThrust

```cpp
#include <thrust/device_vector.h>
#include <thrust/sort.h>
#include <thrust/reduce.h>

thrust::device_vector<float> d_vec(h_vec.begin(), h_vec.end());
thrust::sort(d_vec.begin(), d_vec.end());
float sum = thrust::reduce(d_vec.begin(), d_vec.end());
```

## 31.2 ROCm-Aware MPI

```cpp
// With ROCm-aware MPI (e.g., OpenMPI with UCX/ROCm support):
float* d_buf;
hipMalloc(&d_buf, bytes);

// Pass device pointers directly to MPI
MPI_Send(d_buf, count, MPI_FLOAT, dest, tag, comm);
MPI_Recv(d_buf, count, MPI_FLOAT, src, tag, comm, &status);

// Collectives with device buffers
MPI_Allreduce(d_send, d_recv, count, MPI_FLOAT, MPI_SUM, comm);
```

> **See also:** how to check whether your MPI build is actually ROCm-aware (`MPIX_ROCM_AWARE_SUPPORT` / `MPIX_Query_rocm_support()` in Open MPI 5, `MPICH_GPU_SUPPORT_ENABLED=1` on Cray MPICH), and what fails when it is not, is in [32.6](#326-building-hybrid-mpi--openmp--hip-code-with-cmake).

## 31.3 Multi-GPU with HIP

```cpp
int device_count;
hipGetDeviceCount(&device_count);

// Enable peer access between GPUs
for (int i = 0; i < device_count; i++) {
    hipSetDevice(i);
    for (int j = 0; j < device_count; j++) {
        if (i != j) {
            int can_access;
            hipDeviceCanAccessPeer(&can_access, i, j);
            if (can_access) {
                hipDeviceEnablePeerAccess(j, 0);
            }
        }
    }
}

// Peer-to-peer memory copy
hipMemcpyPeer(d_dest, dest_device, d_src, src_device, bytes);

// Async peer copy
hipMemcpyPeerAsync(d_dest, dest_device, d_src, src_device, bytes, stream);
```

> **See also:** [34. Collective Communication Algorithms and Cost Model](#34-collective-communication-algorithms-and-cost-model) (RCCL API, ring/tree math, env vars, rccl-tests) and [35. Multi-GPU Programming Beyond Peer Copies](#35-multi-gpu-programming-beyond-peer-copies-hip) (IPC, graphs, memory pools, priorities, partitions).

## 31.4 AI/ML Frameworks with ROCm

| Framework | ROCm Support |
|---|---|
| PyTorch | Native support (`torch.cuda` API works transparently) |
| TensorFlow | ROCm-enabled builds available |
| JAX | ROCm support via XLA |
| ONNX Runtime | ROCm execution provider |
| Triton | AMD GPU backend |

```python
# PyTorch with ROCm (API is identical to CUDA):
import torch
device = torch.device("cuda")  # works on AMD GPUs with ROCm
x = torch.randn(1000, 1000, device=device)
y = torch.matmul(x, x.T)
```

---

## Common Interview Questions -- HIP/ROCm

**Q: What is HIP, and how does it differ from CUDA?**

HIP is AMD's GPU programming interface designed for portability. Its API is a near-1:1 mapping of CUDA (e.g., `cudaMalloc` → `hipMalloc`), so code ports trivially. The key difference is that HIP can compile for both AMD GPUs (via ROCm/amdclang++) and NVIDIA GPUs (via the CUDA backend). HIP itself is an API layer, not a new programming model. On AMD hardware, the underlying runtime is HSA-based (ROCr), while on NVIDIA it delegates to CUDA.

**Q: What is the key difference between a warp and a wavefront?**

A warp (NVIDIA) is 32 threads that execute in lockstep; a wavefront (AMD CDNA) is 64 threads. This means AMD processes twice as many threads per instruction issue. When porting CUDA code, hardcoded values of 32 (warp size) must be replaced with the runtime `warpSize` variable. Warp-level primitives like ballot return 32-bit results on NVIDIA but 64-bit on AMD. RDNA GPUs support both wave32 (native) and wave64 modes.

**Q: How do you port a CUDA application to HIP?**

The process: (1) Run `hipify-perl` or `hipify-clang` on the CUDA source files to auto-convert API calls (`cuda*` → `hip*`, headers, error types). (2) Fix any remaining issues: hardcoded warp size (32 → `warpSize`), inline PTX assembly (replace with HIP intrinsics), CUDA-specific features without HIP equivalents. (3) Replace CUDA library calls with ROCm equivalents (cuBLAS → rocBLAS, cuDNN → MIOpen). (4) Compile with `hipcc`. (5) Profile and optimize for AMD architecture (different shared memory sizes, register counts, wavefront width).

**Q: What are VGPRs and SGPRs on AMD GPUs?**

VGPRs (Vector General Purpose Registers) hold per-lane data -- each thread in a wavefront has its own VGPR values. SGPRs (Scalar General Purpose Registers) hold values shared across the entire wavefront (constants, addresses, loop counters). Using SGPRs for uniform values saves VGPR pressure and improves occupancy. NVIDIA GPUs have only one register type (per-thread); the scalar vs. vector distinction is unique to AMD's architecture.

**Q: How does memory coalescing differ between AMD and NVIDIA GPUs?**

The fundamental principle is the same: consecutive threads accessing consecutive memory locations achieves maximum bandwidth. The difference is granularity: NVIDIA coalesces 32 threads (one warp) per transaction, while AMD coalesces 64 threads (one wavefront on CDNA). AMD GPUs also have different cache line sizes and L1/L2 cache behavior. Both architectures benefit from SoA layouts and avoiding strided access, but the exact transaction sizes and cache policies differ.

**Q: What are the main ROCm profiling tools and when would you use each?**

All current tools sit on **ROCprofiler-SDK**, the tool library that replaced ROCProfiler v1/v2 and ROCTracer (the role CUPTI plays on NVIDIA).
- **`rocprofv3`** is the command-line profiler on that SDK. Use it for API/kernel/memory-copy tracing (`--kernel-trace`, `--runtime-trace`, `--sys-trace`), per-kernel statistics (`--stats`), and raw hardware counters (`--pmc`). It is the right tool for "which kernels dominate?" and for scripted counter collection in CI.
- **`rocprof-sys`** (ROCm Systems Profiler, formerly Omnitrace) produces a whole-application Perfetto timeline: CPU sampling, HIP/HSA, RCCL, MPI, OpenMP. Use it when end-to-end time is the question, for example idle gaps, launch overhead, or communication waits. It is the analogue of Nsight Systems.
- **`rocprof-compute`** (ROCm Compute Profiler, formerly Omniperf) is the per-kernel deep dive: speed-of-light panels, memory chart, roofline, occupancy limiters, instruction mix. It is the analogue of Nsight Compute.
- **`amd-smi`** (successor to `rocm-smi`) covers device health, clocks, partitions, and topology.

The workflow is: timeline first, then pick the top kernels, then deep-dive them, then fix and re-measure. The legacy `rocprof` and `rocprofv2` are deprecated. Watch for one behavior change: `rocprofv3 --hip-trace` traces only API calls, so add `--kernel-trace` to see kernels.

**Q: Why were Omniperf and Omnitrace renamed, and why move to ROCprofiler-SDK?**

In ROCm 6.3 the tools were renamed to `rocprof-compute` and `rocprof-sys` to put them under one product family with `rocprofv3`, and they are moving onto one shared collection layer. Before the SDK, there were separate libraries for tracing (ROCTracer) and for counters (ROCProfiler v1/v2), each with its own interception and its own buffering. Tools often could not run together, and every tool re-implemented the same plumbing. ROCprofiler-SDK provides one API for:
- callback and buffered tracing of the HIP/HSA/RCCL/ROCTx APIs,
- kernel-dispatch and memory-copy records,
- dispatch and device counter collection,
- PC sampling and thread trace.

It also adds a single tool-registration model (`rocprofiler_configure`) and stable record formats, now with the rocpd SQLite output. The practical consequences: one interception path means lower overhead and fewer conflicts, new hardware only has to be enabled once, and `rocprof-compute` defaults to `rocprofv3` collection as of ROCm 7.0.

---

# Part 5: Cross-Cutting Topics

---

# 32. Hybrid Programming Patterns

---

## 32.1 MPI + OpenMP (Multi-Node, Multi-Core)

The most common HPC hybrid model: MPI for inter-node communication, OpenMP for intra-node parallelism.

```c
#include <mpi.h>
#include <omp.h>

int main(int argc, char** argv) {
    int provided;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int N = 10000000;
    int chunk = N / size;
    double* local_data = malloc(chunk * sizeof(double));

    // OpenMP parallelism within each MPI process
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < chunk; i++) {
        local_data[i] = compute(rank * chunk + i);
    }

    // MPI communication between nodes (main thread only in FUNNELED mode)
    double local_sum = 0.0;
    #pragma omp parallel for reduction(+:local_sum)
    for (int i = 0; i < chunk; i++) {
        local_sum += local_data[i];
    }

    double global_sum;
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        printf("Global sum: %f\n", global_sum);
    }

    free(local_data);
    MPI_Finalize();
}
```

### Thread Safety Levels for Hybrid MPI+OpenMP

| Pattern | Required Level | Description |
|---|---|---|
| MPI outside parallel regions | `MPI_THREAD_SINGLE` | Simplest, no threading issues |
| MPI in master thread only | `MPI_THREAD_FUNNELED` | OpenMP for compute, main thread for MPI |
| MPI in any thread (serialized) | `MPI_THREAD_SERIALIZED` | Critical sections around MPI calls |
| MPI from any thread concurrently | `MPI_THREAD_MULTIPLE` | Maximum flexibility, highest overhead |

## 32.2 MPI + CUDA/HIP (Multi-Node, Multi-GPU)

```cpp
#include <mpi.h>
#include <hip/hip_runtime.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Each MPI rank uses a different GPU
    int num_gpus;
    hipGetDeviceCount(&num_gpus);
    int local_rank = rank % num_gpus;
    hipSetDevice(local_rank);

    int N = 1000000;
    int chunk = N / size;
    size_t bytes = chunk * sizeof(float);

    float *d_data, *d_result;
    hipMalloc(&d_data, bytes);
    hipMalloc(&d_result, bytes);

    // GPU computation
    kernel<<<(chunk+255)/256, 256>>>(d_data, d_result, chunk);

    // GPU-aware MPI: pass device pointers directly
    // (requires GPU-aware MPI implementation)
    float *d_all_results;
    hipMalloc(&d_all_results, N * sizeof(float));
    MPI_Gather(d_result, chunk, MPI_FLOAT,
               d_all_results, chunk, MPI_FLOAT,
               0, MPI_COMM_WORLD);

    hipFree(d_data);
    hipFree(d_result);
    hipFree(d_all_results);
    MPI_Finalize();
}
```

### Launch Configuration

```bash
# 4 nodes, 4 GPUs per node, 1 MPI rank per GPU
mpirun -np 16 --map-by ppr:4:node ./gpu_app

# With Slurm
srun -N 4 --ntasks-per-node=4 --gpus-per-task=1 ./gpu_app
```

> **Note:** `rank % num_gpus` above is correct only when ranks are packed per node. A placement-independent mapping uses `MPI_Comm_split_type(MPI_COMM_TYPE_SHARED)`. That mapping, plus a tested CMake build of an MPI + OpenMP + HIP executable, is in [32.6](#326-building-hybrid-mpi--openmp--hip-code-with-cmake).

## 32.3 OpenMP + CUDA/HIP (Host Threading + GPU Offload)

```cpp
#include <omp.h>
#include <hip/hip_runtime.h>

int main() {
    int num_gpus;
    hipGetDeviceCount(&num_gpus);

    #pragma omp parallel num_threads(num_gpus)
    {
        int tid = omp_get_thread_num();
        hipSetDevice(tid);

        float* d_data;
        hipMalloc(&d_data, bytes);
        hipMemcpy(d_data, h_data + tid * chunk, bytes, hipMemcpyHostToDevice);

        kernel<<<blocks, threads>>>(d_data, chunk);

        hipMemcpy(h_data + tid * chunk, d_data, bytes, hipMemcpyDeviceToHost);
        hipFree(d_data);
    }
}
```

## 32.4 Full Hybrid: MPI + OpenMP + CUDA/HIP

The ultimate HPC pattern for large-scale GPU clusters:

```cpp
#include <mpi.h>
#include <omp.h>
#include <hip/hip_runtime.h>

int main(int argc, char** argv) {
    int provided;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Each rank manages one or more GPUs
    int num_gpus;
    hipGetDeviceCount(&num_gpus);
    int gpus_per_rank = num_gpus;  // or distribute across MPI ranks

    #pragma omp parallel num_threads(gpus_per_rank)
    {
        int gpu_id = omp_get_thread_num();
        hipSetDevice(gpu_id);

        // Each thread manages its GPU
        float* d_data;
        hipMalloc(&d_data, bytes);

        hipStream_t stream;
        hipStreamCreate(&stream);

        // Async copy + compute
        hipMemcpyAsync(d_data, h_chunk, bytes, hipMemcpyHostToDevice, stream);
        kernel<<<blocks, threads, 0, stream>>>(d_data, chunk_size);
        hipMemcpyAsync(h_result, d_data, bytes, hipMemcpyDeviceToHost, stream);
        hipStreamSynchronize(stream);

        hipStreamDestroy(stream);
        hipFree(d_data);
    }

    // MPI communication between nodes (main thread)
    MPI_Allreduce(MPI_IN_PLACE, h_result, N, MPI_FLOAT, MPI_SUM, MPI_COMM_WORLD);

    MPI_Finalize();
}
```

## 32.5 When to Use Each Combination

| Pattern | Use Case | Typical Scale |
|---|---|---|
| **OpenMP only** | Single multi-core node | 1 node, 4-128 cores |
| **MPI only** | Cluster, distributed memory | 1-10,000+ nodes |
| **MPI + OpenMP** | Cluster with multi-core nodes | 10-10,000 nodes, cores per node |
| **CUDA/HIP only** | Single GPU | 1 GPU |
| **OpenMP + GPU** | Multi-GPU on one node | 1 node, 1-8 GPUs |
| **MPI + GPU** | Multi-node, multi-GPU | 10-10,000 nodes with GPUs |
| **MPI + OpenMP + GPU** | Large-scale HPC clusters | Supercomputer scale |

## 32.6 Building Hybrid MPI + OpenMP + HIP Code with CMake

> See also: [CMake Fundamentals -- HIP and ROCm with CMake](../tools/CMake_Fundamentals.md#64-hip-and-rocm-with-cmake) ([the HIP language project](../tools/CMake_Fundamentals.md#642-the-hip-language-a-complete-project), [finding ROCm and `hip::host`](../tools/CMake_Fundamentals.md#644-finding-rocm-cmake_prefix_path-hiphost-hipdevice), [linking ROCm libraries](../tools/CMake_Fundamentals.md#645-linking-rocm-libraries-and-profiler-sdks)), [find_package module vs config mode](../tools/CMake_Fundamentals.md#28-find_package-module-mode-vs-config-mode), [enable_testing and add_test](../tools/CMake_Fundamentals.md#42-enable_testing-and-add_test).

The command lines in [1.4](#14-compilation-and-execution) (`mpicxx`), [9.2](#92-basic-parallel-region) (`-fopenmp`), and [25.5](#255-compilation) (`hipcc`) are fine for a one-file experiment. They stop working when one executable needs all three, because each wrapper wants to be *the* compiler. In CMake, each programming model maps to a different mechanism, and the three compose:

| Model | CMake mechanism | What you get | Main pitfall |
|---|---|---|---|
| MPI | `find_package(MPI REQUIRED COMPONENTS CXX)` (a Find module shipped with CMake) | `MPI::MPI_CXX` (MPI include dirs + `libmpi`), plus `MPIEXEC_EXECUTABLE`, `MPIEXEC_NUMPROC_FLAG`, `MPIEXEC_PREFLAGS`, `MPIEXEC_POSTFLAGS` for tests | Setting `CMAKE_CXX_COMPILER=mpicxx` instead. It works, but it hides the dependency, and no target can opt out of MPI |
| OpenMP | `find_package(OpenMP REQUIRED COMPONENTS CXX)` | `OpenMP::OpenMP_CXX`, whose compile option is `$<$<COMPILE_LANGUAGE:CXX>:-fopenmp>`, plus the runtime library (`libgomp` for GCC) | FindOpenMP supports only the C, CXX, CUDA, and Fortran components. There is **no HIP component**, so `.hip` files never get `-fopenmp` |
| HIP | `project(p LANGUAGES CXX HIP)` | `.hip` files compiled by ROCm clang with `-x hip --offload-arch=...`; the HIP runtime is linked implicitly | Using `hipcc` as `CMAKE_HIP_COMPILER` (CMake rejects it) or leaving `CMAKE_HIP_ARCHITECTURES` unset |

The working layout keeps the three concerns in separate translation units. GPU code goes in a `.hip` file behind a plain C++ header. MPI and OpenMP code goes in `.cpp` files compiled by the host compiler.

```text
hybrid/
|-- CMakeLists.txt
`-- src/
    |-- kernels.hpp     <- plain C++ interface, no HIP types
    |-- kernels.hip     <- kernel + launcher (ROCm clang)
    `-- main.cpp        <- MPI + OpenMP host code (g++ with -fopenmp)
```

```cmake
cmake_minimum_required(VERSION 3.21...4.2)

# Pin GPU targets before the HIP language is enabled (Section 64.2 of the CMake guide).
set(CMAKE_HIP_ARCHITECTURES "gfx942;gfx950" CACHE STRING "AMD GPU targets")

project(hybrid LANGUAGES CXX HIP)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_HIP_STANDARD 17)
set(CMAKE_HIP_STANDARD_REQUIRED ON)

find_package(MPI REQUIRED COMPONENTS CXX)      # -> MPI::MPI_CXX, MPIEXEC_EXECUTABLE
find_package(OpenMP REQUIRED COMPONENTS CXX)   # -> OpenMP::OpenMP_CXX (no HIP component)

# Device code: compiled by ROCm clang (-x hip --offload-arch=...).
add_library(kernels STATIC src/kernels.hip)
target_include_directories(kernels PUBLIC src)

# Host code: compiled by the system C++ compiler with -fopenmp and MPI include paths.
add_executable(hybrid src/main.cpp)
target_link_libraries(hybrid PRIVATE kernels MPI::MPI_CXX OpenMP::OpenMP_CXX)

enable_testing()
add_test(NAME hybrid_np2
         COMMAND ${MPIEXEC_EXECUTABLE} ${MPIEXEC_NUMPROC_FLAG} 2
                 ${MPIEXEC_PREFLAGS} $<TARGET_FILE:hybrid> ${MPIEXEC_POSTFLAGS})
set_tests_properties(hybrid_np2 PROPERTIES PROCESSORS 2
                     ENVIRONMENT "OMP_NUM_THREADS=4")
```

```cpp
// src/kernels.hpp
#pragma once
#include <cstddef>
// Plain C++ interface: main.cpp never includes a HIP header.
int gpu_device_count();
// y[i] = a * (first + i) + 1 for i in [0, n), computed on GPU `device`.
void gpu_affine(int device, float a, long long first, float* y, std::size_t n);
```

```cpp
// src/kernels.hip
#include <hip/hip_runtime.h>
#include <cstdio>
#include <cstdlib>
#include "kernels.hpp"

#define HIP_CHECK(expr)                                                   \
  do {                                                                    \
    hipError_t err_ = (expr);                                             \
    if (err_ != hipSuccess) {                                             \
      std::fprintf(stderr, "%s:%d: %s\n", __FILE__, __LINE__,             \
                   hipGetErrorString(err_));                              \
      std::exit(EXIT_FAILURE);                                            \
    }                                                                     \
  } while (0)

__global__ void affine_kernel(float a, long long first, float* y, std::size_t n) {
  std::size_t i = blockIdx.x * static_cast<std::size_t>(blockDim.x) + threadIdx.x;
  if (i < n) y[i] = a * static_cast<float>(first + static_cast<long long>(i)) + 1.0f;
}

int gpu_device_count() {
  int count = 0;
  if (hipGetDeviceCount(&count) != hipSuccess) count = 0;
  return count;
}

void gpu_affine(int device, float a, long long first, float* y, std::size_t n) {
  HIP_CHECK(hipSetDevice(device));
  float* dy = nullptr;
  HIP_CHECK(hipMalloc(&dy, n * sizeof(float)));
  const unsigned block = 256;
  const unsigned grid = static_cast<unsigned>((n + block - 1) / block);
  affine_kernel<<<grid, block>>>(a, first, dy, n);
  HIP_CHECK(hipGetLastError());
  HIP_CHECK(hipMemcpy(y, dy, n * sizeof(float), hipMemcpyDeviceToHost));
  HIP_CHECK(hipFree(dy));
}
```

```cpp
// src/main.cpp
#include <mpi.h>
#include <omp.h>
#include <cstdio>
#include <vector>
#include "kernels.hpp"

int main(int argc, char** argv) {
  int provided = 0;
  // Only the main thread calls MPI; OpenMP threads do host compute.
  MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);
  if (provided < MPI_THREAD_FUNNELED) MPI_Abort(MPI_COMM_WORLD, 1);
  int rank = 0, size = 1;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  // Node-local rank -> GPU. rank % ndev is wrong when ranks are not packed per node.
  MPI_Comm node;
  MPI_Comm_split_type(MPI_COMM_WORLD, MPI_COMM_TYPE_SHARED, rank, MPI_INFO_NULL, &node);
  int local_rank = 0;
  MPI_Comm_rank(node, &local_rank);
  const int ndev = gpu_device_count();
  if (ndev == 0) {
    if (rank == 0) std::fprintf(stderr, "no GPU visible\n");
    MPI_Abort(MPI_COMM_WORLD, 1);
  }
  const int device = local_rank % ndev;

  // Block decomposition of [0, N) that also handles N % size != 0.
  const long long N = 1LL << 20;
  const long long begin = N * rank / size, end = N * (rank + 1) / size;
  std::vector<float> y(static_cast<std::size_t>(end - begin));

  const float a = 2.0f;
  gpu_affine(device, a, begin, y.data(), y.size());   // GPU: y = a*x + 1

  double local = 0.0;                                  // CPU threads: reduce
#pragma omp parallel for reduction(+ : local) schedule(static)
  for (long long i = 0; i < static_cast<long long>(y.size()); ++i) local += y[i];

  double global = 0.0;                                 // MPI: across ranks
  MPI_Allreduce(&local, &global, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

  const double expected = a * (double(N) * (N - 1) / 2.0) + double(N);
  if (rank == 0)
    std::printf("ranks=%d threads=%d thread_level=%d sum=%.0f expected=%.0f %s\n",
                size, omp_get_max_threads(), provided, global, expected,
                global == expected ? "OK" : "MISMATCH");
  std::printf("rank %d -> local_rank %d -> GPU %d, elements [%lld, %lld)\n",
              rank, local_rank, device, begin, end);

  MPI_Comm_free(&node);
  MPI_Finalize();
  return global == expected ? 0 : 1;
}
```

The expected sum is exact. With `a = 2` the values are `2x + 1` for `x = 0 .. N-1`, so the sum is `2 * N(N-1)/2 + N = N^2 = 2^40`. Each `float` value is at most `2^21 + 1`, which is below `2^24` and therefore exact, and the `double` running sums stay below `2^53`.

Build, test, and run. This was captured on an MI350X node (gfx950) with Open MPI 5.0.10, GCC 15, CMake 4.2, and a TheRock ROCm nightly. Paths are shortened.

```bash
cmake -S . -B build -G Ninja -DCMAKE_PREFIX_PATH=/opt/rocm -DCMAKE_BUILD_TYPE=Release
cmake --build build -v
ctest --test-dir build --output-on-failure
OMP_NUM_THREADS=4 mpirun -np 2 build/hybrid
```

```text
-- Found MPI_CXX: /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so (found version "3.1")
-- Found OpenMP_CXX: -fopenmp (found version "4.5")
[1/4] /usr/bin/c++ -I src -isystem .../openmpi/include ... -O3 -DNDEBUG -std=gnu++17 -fopenmp -c src/main.cpp
[2/4] /opt/rocm/lib/llvm/bin/clang++ -D__HIP_ROCclr__=1 ... --offload-arch=gfx942 --offload-arch=gfx950 -x hip -c src/kernels.hip
[3/4] ar qc libkernels.a kernels.hip.o
[4/4] /opt/rocm/lib/llvm/bin/clang++ ... main.cpp.o -o hybrid libkernels.a .../libamdhip64.so... .../openmpi/lib/libmpi.so .../gcc/x86_64-linux-gnu/15/libgomp.so ...
1/1 Test #1: hybrid_np2 .......................   Passed    0.54 sec
ranks=2 threads=4 thread_level=1 sum=1099511627776 expected=1099511627776 OK
rank 0 -> local_rank 0 -> GPU 0, elements [0, 524288)
rank 1 -> local_rank 1 -> GPU 1, elements [524288, 1048576)
```

What the verbose build shows:

- **Each file goes to the right compiler.** `main.cpp` is compiled by `g++` with `-fopenmp` and the MPI include paths, which come from the `MPI::MPI_CXX` and `OpenMP::OpenMP_CXX` usage requirements. `kernels.hip` is compiled by ROCm clang with one `--offload-arch` per entry in `CMAKE_HIP_ARCHITECTURES`. It gets no `-fopenmp` and no MPI flags, because nothing in it needs them.
- **The final link is done by ROCm clang**, not `g++`. `hybrid` has only a `.cpp` source, but it links a static library that contains HIP objects. CMake picks the linker language with the highest preference across the target and its static dependencies, which is HIP. The link line still pulls in GCC's `libgomp.so` and `libmpi.so` by full path, so mixing compilers works.
- **`thread_level=1`** is `MPI_THREAD_FUNNELED` in Open MPI's numbering (`SINGLE=0` to `MULTIPLE=3`). Always compare `provided` against what you requested. An MPI library is allowed to return a lower level than you asked for.

**Pitfall (verified): an OpenMP pragma in a `.hip` file is silently ignored.** Put this in `t.hip`, link it with `OpenMP::OpenMP_CXX`, and run it with `OMP_NUM_THREADS=4`:

```cpp
#include <cstdio>
#include <omp.h>
int main() {
  int n = 0;
#pragma omp parallel reduction(+ : n)
  n += 1;
  std::printf("threads that ran the region: %d\n", n);
}
```

It prints `threads that ran the region: 1`. The link line includes `libgomp.so`, but the compile line has no `-fopenmp`, because the target's option is guarded by `$<COMPILE_LANGUAGE:CXX>`. Without `-fopenmp` the compiler drops the pragma and emits no warning by default. Clang reports it only with `-Wsource-uses-openmp`. The same file renamed to `.cpp` prints 4. The fix is the layout above: keep host-parallel loops in `.cpp` files. If a HIP translation unit really needs host OpenMP, add `target_compile_options(t PRIVATE $<$<COMPILE_LANGUAGE:HIP>:-fopenmp>)`. Then make sure only one OpenMP runtime ends up in the process. Clang's `-fopenmp` defaults to LLVM `libomp`, and GCC's uses `libgomp`. Two OpenMP runtimes in one process each create their own thread pool, which oversubscribes the cores.

**Rank-to-GPU mapping.** `rank % ngpus` is correct only when consecutive ranks are packed onto the same node. Take 2 nodes with 4 GPUs each and 8 ranks placed round-robin (`mpirun --map-by node`). Node 0 gets ranks 0, 2, 4, 6, and `rank % 4` gives GPUs 0, 2, 0, 2. Two GPUs are shared and two sit idle. The node-local rank from `MPI_Comm_split_type(..., MPI_COMM_TYPE_SHARED, ...)` gives 0, 1, 2, 3 on every node, whatever the placement. If the launcher already restricts each rank to one GPU (Slurm `--gpus-per-task=1 --gpu-bind=closest` sets the visible-device variables per task), then `ndev == 1` and `local_rank % ndev` is 0. The same code is correct in both cases.

**GPU-aware MPI is a property of the MPI build, not of your code.** This example stages through a host `std::vector`, so it works with any MPI. Passing `hipMalloc` pointers straight to `MPI_Send`/`MPI_Allreduce`, as in [31.2](#312-rocm-aware-mpi), needs a ROCm-aware build: for example Open MPI built with ROCm support (usually through UCX), or Cray MPICH with `MPICH_GPU_SUPPORT_ENABLED=1`. Open MPI 5 reports this in `<mpi-ext.h>`: the compile-time macro `MPIX_ROCM_AWARE_SUPPORT` and the run-time function `MPIX_Query_rocm_support()`. On the distro Open MPI 5.0.10 used above, the header contains `#define MPIX_ROCM_AWARE_SUPPORT 0`. That build is not ROCm-aware, and passing it device pointers would be a bug.

**Testing MPI programs under CTest.** Build the launch command from the `MPIEXEC_*` variables instead of hard-coding `mpirun -np`. `MPIEXEC_NUMPROC_FLAG` is `-n` by default, and `MPIEXEC_PREFLAGS` can carry site flags such as `--oversubscribe` in CI. Set the `PROCESSORS` test property to the rank count, so that `ctest -j` does not schedule more MPI ranks than there are cores.

### Interview Questions -- Building Hybrid Codes

**Q1. Why not just set `CMAKE_CXX_COMPILER=mpicxx`, or `CXX=hipcc`, and be done?**

Both work for small projects, but both are global. Every C++ file in the build, including unit tests and tools that have nothing to do with MPI or GPUs, gets compiled by the wrapper. The dependency is also invisible to CMake. Nothing in `target_link_libraries` says "this target needs MPI", so it cannot be exported to downstream projects through a package config, and a target cannot opt out. The two wrappers also conflict with each other: `mpicxx` wraps `g++` (or whatever `OMPI_CXX` points at), and `hipcc` wraps ROCm clang, so you cannot have both as the C++ compiler. With `MPI::MPI_CXX`, `OpenMP::OpenMP_CXX`, and the HIP language, each target states exactly what it needs, and CMake routes each file to the right compiler. Since CMake 3.21.3, `hipcc` is rejected outright as `CMAKE_HIP_COMPILER`.

**Q2. A loop with `#pragma omp parallel for` scales on the CPU build but runs on one thread after you moved it into a `.hip` file. The code did not change. What happened?**

`OpenMP::OpenMP_CXX` attaches `-fopenmp` only when the language is CXX (`$<$<COMPILE_LANGUAGE:CXX>:...>`), and FindOpenMP has no HIP component. The `.hip` file is compiled without `-fopenmp`, so the compiler ignores the pragma. Linking still succeeds because `libgomp` is on the link line, and calls such as `omp_get_max_threads()` still resolve. Diagnose it with `cmake --build build -v` (check for `-fopenmp` on that file's compile line) or with clang's `-Wsource-uses-openmp`, which prints `unexpected '#pragma omp ...' in program`. Clang's `-Wunknown-pragmas` does not catch this case. Fix it by moving host-parallel code back to a `.cpp` file, or by adding a HIP-guarded `-fopenmp` and making sure only one OpenMP runtime is linked.

**Q3. How do you assign GPUs to MPI ranks, and what goes wrong with `rank % num_gpus`?**

Use the node-local rank: `MPI_Comm_split_type(MPI_COMM_WORLD, MPI_COMM_TYPE_SHARED, rank, MPI_INFO_NULL, &node)` followed by `MPI_Comm_rank(node, &local)`, then `hipSetDevice(local % ndev)`. `rank % ndev` assumes block placement with exactly `ndev` ranks per node. With round-robin placement (8 ranks, 2 nodes, 4 GPUs each), node 0 hosts ranks 0, 2, 4, 6, which map to GPUs 0, 2, 0, 2. Half the GPUs are idle, and the other half run two ranks each, which shows up as roughly 2x slower kernels. Also choose GPUs that are close to the rank's CPU cores and NIC (the NUMA domain). Slurm's `--gpu-bind=closest` or a per-rank wrapper script that sets `ROCR_VISIBLE_DEVICES` does this. Inside the program, `ndev` is then 1. Follow-up: verify the mapping by printing `hipDeviceProp_t::pciBusID` per rank, or with `rocm-smi --showpids`.

**Q4. You pass a `hipMalloc` pointer to `MPI_Allreduce` and the job segfaults inside `libmpi`. Why, and how do you check before it happens?**

The MPI build is not GPU-aware. It treats the buffer as host memory and copies from it with the CPU. A device address from `hipMalloc` is not host-accessible on discrete GPUs, so the copy faults. (On APUs such as MI300A, or with host-accessible allocations such as `hipMallocManaged` under XNACK, the copy may "work" but slowly.) Check at build time with `MPIX_ROCM_AWARE_SUPPORT` from `<mpi-ext.h>` (Open MPI) and at run time with `MPIX_Query_rocm_support()`. Fall back to staging through pinned host memory (`hipHostMalloc`), or use RCCL for GPU-to-GPU collectives ([34.9](#349-the-ncclrccl-api)). For Cray MPICH, the runtime switch is `MPICH_GPU_SUPPORT_ENABLED=1`, and the GTL library must be linked.

**Q5. How do you run an MPI program as a CTest test, and what breaks under `ctest -j 8`?**

Use `add_test(NAME t COMMAND ${MPIEXEC_EXECUTABLE} ${MPIEXEC_NUMPROC_FLAG} <n> ${MPIEXEC_PREFLAGS} $<TARGET_FILE:app> ${MPIEXEC_POSTFLAGS})`. FindMPI fills these variables for the detected implementation. Without `PROCESSORS <n>`, CTest counts each MPI test as one slot, so `-j 8` can start eight 4-rank jobs (32 processes) on an 8-core runner. Open MPI then refuses with "not enough slots" unless `--oversubscribe` is set, or the jobs time out from oversubscription. For GPU tests, also declare GPU resources with `RESOURCE_GROUPS` and a resource spec file, so that two tests are not pinned to the same GPU ([parallel test execution](../tools/CMake_Fundamentals.md#44-parallel-test-execution)).

---

# 33. Comprehensive Comparison Tables

---

## 33.1 MPI vs OpenMP vs CUDA vs HIP Feature Matrix

| Feature | MPI | OpenMP | CUDA | HIP |
|---|---|---|---|---|
| **Memory model** | Distributed | Shared | Shared (device) | Shared (device) |
| **Target hardware** | CPU clusters | Multi-core CPU | NVIDIA GPU | AMD + NVIDIA GPU |
| **Parallelism type** | Process-level | Thread-level | Massive thread-level | Massive thread-level |
| **Communication** | Explicit messages | Implicit (shared vars) | Implicit (shared mem/global) | Implicit (shared mem/global) |
| **Max parallelism** | 100,000s of processes | 100s of threads | 100,000s of threads | 100,000s of threads |
| **Standard/Spec** | MPI Forum standard | OpenMP specification | NVIDIA proprietary | AMD open-source |
| **Language support** | C, C++, Fortran | C, C++, Fortran | C, C++ (extensions) | C, C++ (extensions) |
| **Compilation** | `mpicc` | `-fopenmp` flag | `nvcc` | `hipcc` |
| **Runtime overhead** | Process creation | Thread fork/join | Kernel launch | Kernel launch |
| **Data sharing** | Message passing | Shared variables | Device memory | Device memory |

## 33.2 Memory Model Comparison

| Aspect | MPI | OpenMP | CUDA | HIP |
|---|---|---|---|---|
| **Address space** | Per-process (private) | Per-process (shared) | Host + Device (separate) | Host + Device (separate) |
| **Fastest local store** | CPU cache | CPU cache | Registers + Shared mem | Registers + LDS |
| **Explicit management** | Send/Recv buffers | Private/shared clauses | cudaMalloc/cudaMemcpy | hipMalloc/hipMemcpy |
| **Unified memory** | N/A | Native (shared) | cudaMallocManaged | hipMallocManaged |
| **Data movement cost** | High (network) | Low (cache coherence) | Moderate (PCIe/NVLink) | Moderate (PCIe/Infinity Fabric) |

## 33.3 Synchronization Primitives Comparison

| Mechanism | MPI | OpenMP | CUDA | HIP |
|---|---|---|---|---|
| **Global barrier** | `MPI_Barrier` | `#pragma omp barrier` | Cooperative launch | Cooperative launch |
| **Block/group sync** | N/A | Implicit at work-sharing | `__syncthreads()` | `__syncthreads()` |
| **Mutex/lock** | N/A | `critical`, `omp_lock_t` | `atomicCAS` (spin lock) | `atomicCAS` (spin lock) |
| **Atomic ops** | `MPI_Accumulate` (RMA) | `#pragma omp atomic` | `atomicAdd`, etc. | `atomicAdd`, etc. |
| **Point-to-point sync** | `MPI_Send`/`MPI_Recv` | Task dependencies | Events, streams | Events, streams |
| **Reduction** | `MPI_Reduce` | `reduction` clause | Manual (shared mem + warp shuffle) | Manual (LDS + wavefront shuffle) |
| **Fence** | `MPI_Win_fence` | `#pragma omp flush` | `__threadfence()` | `__threadfence()` |

## 33.4 Performance Characteristics and Use-Case Guidance

| Workload Type | Best Approach | Why |
|---|---|---|
| Embarrassingly parallel, large data | CUDA/HIP | Maximum throughput, simple data parallelism |
| Regular stencil computation (single node) | OpenMP | Simple to parallelize, good cache behavior |
| Regular stencil computation (cluster) | MPI + OpenMP/GPU | Distribute across nodes, local parallelism |
| Irregular/dynamic workload | OpenMP tasks or MPI | Task-based parallelism handles imbalance |
| Dense linear algebra | CUDA/HIP + libraries | cuBLAS/rocBLAS are highly optimized |
| Sparse linear algebra | CUDA/HIP + libraries | cuSPARSE/rocSPARSE for sparse ops |
| Graph algorithms | MPI or CUDA/HIP | Depends on graph size and structure |
| FFT-heavy workloads | CUDA/HIP + cuFFT/rocFFT | Optimized FFT libraries |
| Deep learning training | CUDA/HIP + MPI/NCCL/RCCL | Multi-GPU with communication collectives |
| Legacy Fortran code | MPI + OpenMP | Minimal code changes with directives |
| Cross-platform portability | HIP or OpenMP target | HIP: AMD+NVIDIA; OpenMP: any accelerator |
| Rapid prototyping | OpenMP | Lowest barrier to entry |

## 33.5 API Mapping Quick Reference

| Operation | MPI | OpenMP | CUDA | HIP |
|---|---|---|---|---|
| **Initialize** | `MPI_Init` | (automatic) | `cudaSetDevice` | `hipSetDevice` |
| **Finalize** | `MPI_Finalize` | (automatic) | `cudaDeviceReset` | `hipDeviceReset` |
| **Get ID** | `MPI_Comm_rank` | `omp_get_thread_num` | `threadIdx + blockIdx` | `threadIdx + blockIdx` |
| **Get count** | `MPI_Comm_size` | `omp_get_num_threads` | `blockDim * gridDim` | `blockDim * gridDim` |
| **Allocate** | `malloc` (per process) | `malloc` (shared) | `cudaMalloc` | `hipMalloc` |
| **Synchronize** | `MPI_Barrier` | `#pragma omp barrier` | `cudaDeviceSynchronize` | `hipDeviceSynchronize` |
| **Reduce** | `MPI_Reduce` | `reduction(+:sum)` | `atomicAdd` + shared mem | `atomicAdd` + LDS |
| **Broadcast** | `MPI_Bcast` | `copyprivate` | Shared/constant memory | LDS/constant memory |

---

# Part 6: Multi-GPU Communication and Portability

---

# 34. Collective Communication Algorithms and Cost Model

---

[Section 3](#3-collective-communication) covered the MPI collective *API*. This section covers how collectives are *implemented*, what they cost, and how the GPU collective libraries work. **NCCL** is NVIDIA's library. **RCCL** is AMD's fork of NCCL with the same API and the same `NCCL_*` environment variables, so the code ports by changing the header and the link line. Interviewers for ML-infra and HPC roles very often ask candidates to derive the cost of an allreduce.

## 34.1 Collectives as Data Movement

Let **N** be the number of ranks (GPUs) and **S** the buffer size in bytes. For reduce-scatter, S is the full input per rank. For all-gather, S is the full output per rank.

| Collective | Before -> after | Bytes each rank must send (bandwidth lower bound) | nccl-tests `busbw` factor | Typical ML use |
|---|---|---|---|---|
| Broadcast | S on root -> S everywhere | S (pipelined) | 1 | Initial weights, config |
| Reduce | S each -> sum on root | S (pipelined) | 1 | Metrics to rank 0 |
| **AllReduce** | S each -> sum everywhere | **2(N-1)/N · S** | 2(N-1)/N | DDP gradient sync, tensor-parallel activations |
| ReduceScatter | S each -> 1/N of the sum each | (N-1)/N · S | (N-1)/N | FSDP/ZeRO gradient sharding |
| AllGather | S/N each -> S everywhere | (N-1)/N · S | (N-1)/N | FSDP/ZeRO parameter gathering |
| AllToAll | N blocks of S/N -> transposed | (N-1)/N · S | (N-1)/N | MoE expert dispatch, distributed FFT/transpose |
| Send/Recv | point to point | S | 1 | Pipeline parallelism, halo exchange |

The key identity is **AllReduce = ReduceScatter + AllGather**. Both halves move (N-1)/N · S per rank, which is where the factor of 2 comes from. It also explains why ZeRO-3/FSDP costs about 1.5x the communication of DDP. DDP does one allreduce of the gradients (2Ψ for Ψ bytes of gradients). FSDP does an all-gather of the parameters in forward (Ψ), another in backward (Ψ), and a reduce-scatter of the gradients (Ψ), for 3Ψ in total.

## 34.2 The Alpha-Beta (Hockney) Cost Model

Model the time to send one message of n bytes as

```text
T(n) = α + n·β            (+ n·γ if the receiver also reduces the data)

α  latency per message: software overhead, kernel/proxy wake-up, flag polling, wire + switch latency
β  1 / bandwidth         (seconds per byte on the bottleneck link)
γ  reduction cost per byte (on GPUs this streams from HBM at TB/s and is usually hidden)
```

**When does latency vs. bandwidth dominate?** The two terms are equal at n = α/β, sometimes written n½ because a single message of that size reaches half of peak bandwidth: n / (α + nβ) = 1/(2β) when nβ = α.

| Link (approximate, per direction) | Bandwidth B | Typical α per step | α/β (= α·B) |
|---|---|---|---|
| MI300X xGMI, one peer link | 64 GB/s peak (~48 GB/s achieved) | ~1-3 µs | ~100-200 KB |
| MI300X xGMI, all 7 links (8-GPU mesh) | 448 GB/s peak per GPU | ~1-3 µs | ~1 MB |
| H100 NVLink4 via NVSwitch | 450 GB/s per GPU | ~1-3 µs | ~1 MB |
| PCIe Gen5 x16 | ~64 GB/s theoretical | ~2-5 µs | ~200 KB |
| InfiniBand NDR / 400G RoCE, one NIC | 50 GB/s | ~3-10 µs (end to end, with software) | ~250 KB |

Messages much smaller than α/β are **latency-bound**: you want algorithms with few sequential steps. Messages much larger are **bandwidth-bound**: you want algorithms that send the minimum number of bytes and keep every link busy. Treat the α values as order-of-magnitude assumptions for back-of-envelope work, not as specifications. Measure them with rccl-tests or nccl-tests ([34.10](#3410-environment-variables-debugging-and-rccl-tests)).

**Lower bounds for allreduce.** At least ⌈log2 N⌉ sequential steps are needed, because the number of ranks that hold information from a given rank can at most double per step. So latency ≥ log2 N · α. The bandwidth term is at least 2(N-1)/N · S · β (Patarasuk and Yuan, 2009). In the reduce-scatter half, each rank must receive the (N-1) other contributions to its own S/N shard. In the all-gather half, it must receive the (N-1) shards it does not own.

## 34.3 Ring AllReduce = Reduce-Scatter + All-Gather

Arrange the ranks in a logical ring (r sends to r+1 mod N) and split the buffer into N chunks of S/N bytes.

1. **Reduce-scatter (N-1 steps).** At step t, rank r sends chunk (r - t) mod N to rank r+1, which adds it into its own copy of that chunk. Each chunk travels around the ring collecting one contribution per hop. After N-1 steps, rank r holds the fully reduced chunk (r + 1) mod N.
2. **All-gather (N-1 steps).** At step t, rank r forwards the complete chunk (r + 1 - t) mod N. After N-1 more steps, every rank holds every reduced chunk.

Worked trace for N = 4 (chunks c0..c3; the number in parentheses is how many ranks' contributions the chunk already contains):

| Step | R0 sends to R1 | R1 sends to R2 | R2 sends to R3 | R3 sends to R0 |
|---|---|---|---|---|
| RS 1 | c0 (1) | c1 (1) | c2 (1) | c3 (1) |
| RS 2 | c3 (2) | c0 (2) | c1 (2) | c2 (2) |
| RS 3 | c2 (3) | c3 (3) | c0 (3) | c1 (3) |
| *after RS* | *R0 owns final c1* | *R1 owns final c2* | *R2 owns final c3* | *R3 owns final c0* |
| AG 1 | c1 | c2 | c3 | c0 |
| AG 2 | c0 | c1 | c2 | c3 |
| AG 3 | c3 | c0 | c1 | c2 |

**Cost derivation.** There are 2(N-1) steps. In each step every rank sends S/N bytes and receives S/N bytes, and all N links are busy at the same time:

```text
T_ring = 2(N-1)·(α + (S/N)·β) + (N-1)·(S/N)·γ
       = 2(N-1)·α  +  2·(N-1)/N · S·β  +  (N-1)/N · S·γ
         \_______/    \______________/
         latency:     bandwidth: -> 2·S·β as N grows,
         linear in N  independent of N, equal to the lower bound
```

So the ring is **bandwidth-optimal** but its latency is **linear in N**. It is ideal for large gradient buffers on a moderate number of GPUs and bad for small messages or thousands of ranks. Real implementations also cut each chunk into smaller *slices* so successive steps pipeline. They run several rings ("channels") in parallel over different links, which also hides per-step latency.

The simulation below checks both the result and the 2(N-1)/N · S byte count:

```python
"""Simulate ring allreduce (reduce-scatter + all-gather) on N ranks.

Checks the result and counts the elements each rank sends, to confirm the
2 * (N - 1) / N * S bandwidth term. Pure Python, no dependencies.
"""


def ring_allreduce(data):
    n = len(data)                       # number of ranks
    size = len(data[0])                 # elements per rank (S)
    assert size % n == 0, "pad S to a multiple of N"
    c = size // n                       # chunk size S / N
    buf = [list(d) for d in data]
    sent = [0] * n

    def chunk(k):
        return range(k * c, (k + 1) * c)

    # Phase 1: reduce-scatter. At step t, rank r sends chunk (r - t) mod n to
    # rank r + 1, which adds it into its own copy. All sends in a step happen
    # "simultaneously", so read every outgoing chunk before applying any.
    for t in range(n - 1):
        msgs = [(r, (r - t) % n, [buf[r][i] for i in chunk((r - t) % n)]) for r in range(n)]
        for r, k, payload in msgs:
            dst = (r + 1) % n
            for j, i in enumerate(chunk(k)):
                buf[dst][i] += payload[j]
            sent[r] += c
    # Now rank r owns the fully reduced chunk (r + 1) mod n.

    # Phase 2: all-gather. At step t, rank r forwards chunk (r + 1 - t) mod n.
    for t in range(n - 1):
        msgs = [(r, (r + 1 - t) % n, [buf[r][i] for i in chunk((r + 1 - t) % n)]) for r in range(n)]
        for r, k, payload in msgs:
            dst = (r + 1) % n
            for j, i in enumerate(chunk(k)):
                buf[dst][i] = payload[j]
            sent[r] += c
    return buf, sent


if __name__ == "__main__":
    for n in (2, 4, 8):
        size = 24                                   # divisible by 2, 4, 8
        data = [[(r + 1) * (i + 1) for i in range(size)] for r in range(n)]
        out, sent = ring_allreduce(data)
        expected = [sum(data[r][i] for r in range(n)) for i in range(size)]
        assert all(row == expected for row in out)
        ratio = sent[0] / size
        print(f"N={n}: each rank sent {sent[0]} of S={size} elements "
              f"-> {ratio:.3f} * S (2(N-1)/N = {2 * (n - 1) / n:.3f})")
```

Output:

```text
N=2: each rank sent 24 of S=24 elements -> 1.000 * S (2(N-1)/N = 1.000)
N=4: each rank sent 36 of S=24 elements -> 1.500 * S (2(N-1)/N = 1.500)
N=8: each rank sent 42 of S=24 elements -> 1.750 * S (2(N-1)/N = 1.750)
```

**Worked numbers (8 GPUs, B = 300 GB/s effective, α = 2 µs):**
- S = 1 GiB of BF16 gradients (~537M parameters). Bandwidth term = 1.75 × 1.074 GB / 300 GB/s = **6.26 ms**. Latency term = 14 × 2 µs = **28 µs**. The operation is bandwidth-bound.
- S = 64 KiB. Bandwidth term = 1.75 × 65,536 / 300 GB/s = **0.38 µs**. Latency term = **28 µs**. It is latency-bound by about 70x, so a log-step algorithm wins (see the table in 34.6).

**algbw vs busbw.** rccl-tests and nccl-tests report `algbw = S / T` and `busbw = algbw × 2(N-1)/N` for allreduce. busbw is the number to compare with the per-GPU link bandwidth, because it removes the algorithm's 2(N-1)/N overhead. For the 1 GiB example, T ≈ 6.29 ms gives algbw = 171 GB/s and busbw = 299 GB/s, which matches the 300 GB/s link assumption.

## 34.4 Tree and Double Binary Tree

A **binary tree** allreduce is a reduce up the tree followed by a broadcast down it: 2·log2 N steps. Without pipelining, every step carries the whole buffer, so T = 2·log2 N·(α + S·β). That is good for tiny messages and terrible for large ones. With pipelining, the buffer is cut into k pieces that stream through the tree, and the time approaches 2·log2 N·α + (bandwidth term). The bandwidth term is the problem: an internal node receives from **two** children during the reduce and sends to two children during the broadcast, so its links carry about twice as much as a leaf's. A single pipelined binary tree therefore gets only about half of the link bandwidth.

A **double binary tree** fixes this. NCCL adopted the construction in version 2.4, after Sanders, Speck and Träff (2009). Two binary trees are built so that every rank is an internal node in one tree and a leaf in the other. Each tree carries **half** of the data. Example for N = 8, where tree B is tree A shifted by one rank:

```text
Tree A (internal = odd ranks)          Tree B (= A shifted by +1; internal = even ranks)
            7                                      0
            |                                      |
            3                                      4
          /   \                                  /   \
         1     5                                2     6
        / \   / \                              / \   / \
       0   2 4   6                            1   3 5   7
```

Per-rank traffic, with each tree handling S/2:
- Internal in tree A: during the reduce it receives 2·(S/2) and sends S/2. During the broadcast it receives S/2 and sends 2·(S/2).
- Leaf in tree B: during the reduce it sends S/2. During the broadcast it receives S/2.
- Totals: it sends S/2 + S + S/2 = **2S** and receives S + S/2 + S/2 = **2S**.

That is the same as the ring's 2(N-1)/N · S ≈ 2S, but with **logarithmic** latency:

```text
T_dbt ≈ 2·log2(N)·α + 2·S·β        (pipelined; ignores pipeline fill)
```

NCCL and RCCL use trees mainly *between* nodes. Within a node they use a chain. The tree pays off at large node counts and small-to-medium message sizes, where the ring's 2(N-1)·α term explodes.

## 34.5 Recursive Doubling and Recursive Halving (Rabenseifner)

These are the classic MPI algorithms (MPICH, Open MPI). They assume N is a power of two. Other values of N need an extra pre-step and post-step that fold the extra ranks in.

- **Recursive doubling allreduce.** At step k = 0..log2 N - 1, rank r exchanges its *whole* vector with partner r XOR 2^k and both sides reduce. After log2 N steps everyone has the sum.
  `T = log2 N · (α + S·β + S·γ)`. This is latency-optimal, but it sends log2 N · S bytes, which is bad for large buffers.
- **Rabenseifner's algorithm** has two phases. Reduce-scatter by **recursive halving**: exchange half of the current working set with a partner at distance N/2, then N/4, and so on, sending S/2 + S/4 + ... + S/N = (N-1)/N · S in total. Then all-gather by **recursive doubling**, which mirrors the first phase.
  `T = 2·log2 N·α + 2·(N-1)/N·S·β + (N-1)/N·S·γ`. This is both latency-optimal (up to a factor of 2) and bandwidth-optimal.

GPU libraries favor rings and trees because those map onto fixed physical links with persistent, pre-connected channels. Recursive halving and doubling change partners every step (distance 2^k). On a ring, mesh, or rail-optimized fabric, that means multi-hop or contended paths and new connections.

## 34.6 Comparing the Algorithms: Worked Numbers and the Crossover

| Algorithm | Latency term | Bandwidth term | Best for |
|---|---|---|---|
| Ring | 2(N-1)·α | 2(N-1)/N·S·β | Large S, moderate N |
| Recursive doubling | log2 N·α | log2 N·S·β | Tiny S |
| Rabenseifner (halving + doubling) | 2·log2 N·α | 2(N-1)/N·S·β | Medium/large S, power-of-two N, CPU MPI |
| Double binary tree (pipelined) | ≈ 2·log2 N·α | ≈ 2·S·β | Small/medium S at large N |
| Hierarchical (34.7) | ≈ 2(G-1)·α_intra + [2(M-1) or 2·log2 M]·α_inter | ≈ 2(G-1)/G·S·β_intra + 2(M-1)/M·(S/G)·β_inter | Multi-node clusters |

```python
"""Alpha-beta cost model for allreduce algorithms.

T = (number of sequential steps) * alpha + (bytes on the busiest link) * beta
alpha: per-message latency (s); beta = 1 / bandwidth (s/byte). The reduction
arithmetic (gamma term) is ignored: on a GPU it streams from HBM far faster
than the link delivers bytes.
"""
from math import log2


def ring(n, s, a, b):
    return 2 * (n - 1) * a + 2 * (n - 1) / n * s * b


def recursive_doubling(n, s, a, b):          # n must be a power of two
    return log2(n) * (a + s * b)


def rabenseifner(n, s, a, b):                # halving RS + doubling AG
    return 2 * log2(n) * a + 2 * (n - 1) / n * s * b


def double_binary_tree(n, s, a, b):          # pipelined, fill cost ignored
    return 2 * log2(n) * a + 2 * s * b


ALGOS = {"ring": ring, "rec-doubling": recursive_doubling,
         "rabenseifner": rabenseifner, "dbl-bin-tree": double_binary_tree}


def fmt(t):
    return f"{t * 1e6:,.1f} us" if t < 1e-3 else f"{t * 1e3:,.2f} ms"


def table(title, n, alpha, bw):
    beta = 1.0 / bw
    print(f"\n{title}: N={n}, alpha={alpha * 1e6:g} us, B={bw / 1e9:g} GB/s, "
          f"alpha/beta={alpha * bw / 1e3:,.0f} KB")
    print(f"{'S':>8} | " + " | ".join(f"{k:>13}" for k in ALGOS))
    for s, label in [(8, "8 B"), (64 << 10, "64 KiB"), (1 << 20, "1 MiB"),
                     (64 << 20, "64 MiB"), (1 << 30, "1 GiB")]:
        print(f"{label:>8} | " + " | ".join(f"{fmt(f(n, s, alpha, beta)):>13}"
                                              for f in ALGOS.values()))


if __name__ == "__main__":
    table("Intra-node (8 GPUs, xGMI mesh, multi-ring effective BW)", 8, 2e-6, 300e9)
    table("Inter-node (64 GPUs, one 400 Gb/s NIC per GPU)", 64, 5e-6, 50e9)
```

Output (illustrative α and B; plug in your own measurements):

```text
Intra-node (8 GPUs, xGMI mesh, multi-ring effective BW): N=8, alpha=2 us, B=300 GB/s, alpha/beta=600 KB
       S |          ring |  rec-doubling |  rabenseifner |  dbl-bin-tree
     8 B |       28.0 us |        6.0 us |       12.0 us |       12.0 us
  64 KiB |       28.4 us |        6.7 us |       12.4 us |       12.4 us
   1 MiB |       34.1 us |       16.5 us |       18.1 us |       19.0 us
  64 MiB |      419.5 us |      677.1 us |      403.5 us |      459.4 us
   1 GiB |       6.29 ms |      10.74 ms |       6.28 ms |       7.17 ms

Inter-node (64 GPUs, one 400 Gb/s NIC per GPU): N=64, alpha=5 us, B=50 GB/s, alpha/beta=250 KB
       S |          ring |  rec-doubling |  rabenseifner |  dbl-bin-tree
     8 B |      630.0 us |       30.0 us |       60.0 us |       60.0 us
  64 KiB |      632.6 us |       37.9 us |       62.6 us |       62.6 us
   1 MiB |      671.3 us |      155.8 us |      101.3 us |      101.9 us
  64 MiB |       3.27 ms |       8.08 ms |       2.70 ms |       2.74 ms
   1 GiB |      42.91 ms |     128.88 ms |      42.34 ms |      43.01 ms
```

**Crossover (ring vs. recursive doubling).** Setting the two formulas equal gives:

```text
2(N-1)·α + 2(N-1)/N·S·β = log2N·α + log2N·S·β
=>  S* = (2(N-1) - log2 N) / (log2 N - 2(N-1)/N) · (α/β)

N = 64:  S* = (126 - 6) / (6 - 1.969) · α/β ≈ 29.8 · α/β ≈ 29.8 × 250 KB ≈ 7.4 MB
N = 8:   S* = (14 - 3) / (3 - 1.75)   · α/β = 8.8 · α/β  ≈ 8.8 × 600 KB  ≈ 5.3 MB
```

Below S*, the log-step algorithm wins. Above it, the ring (or Rabenseifner) wins. NCCL and RCCL make this choice automatically for every (collective, size, N, topology) using exactly this kind of latency + size/bandwidth model ([34.8](#348-how-ncclrccl-execute-collectives-channels-algorithms-protocols)).

## 34.7 Hierarchical (Topology-Aware) Collectives

Real clusters have two very different fabrics:

| Fabric | Topology | Per-GPU bandwidth (peak, per direction) | Notes |
|---|---|---|---|
| **AMD Infinity Fabric / xGMI** (MI300X platform) | Fully connected mesh of 8 GPUs | 7 links × 64 GB/s = 448 GB/s; **64 GB/s to any single peer** | A single ring uses one outgoing link per GPU, so RCCL runs many channels over different ring orderings to light up all 7 links |
| **NVIDIA NVLink + NVSwitch** (H100) | Switched | 450 GB/s (900 GB/s bidirectional) to *any* peer | NVSwitch can also reduce in the switch (NVLS) |
| PCIe Gen5 x16 | Tree through switches / root complex | ~64 GB/s | P2P may cross the CPU root complex. Check GPU-NIC-CPU placement |
| **InfiniBand / RoCE** | Fat tree, often "rail-optimized" (GPU i of every node on the same leaf switch) | 50 GB/s per 400 Gb/s NIC, typically 1 NIC per GPU | **GPUDirect RDMA**: the NIC reads and writes GPU memory directly, with no host bounce buffer |

**Hierarchical allreduce** (G GPUs per node, M nodes, N = G·M):

1. **Intra-node reduce-scatter** over xGMI/NVLink. Each GPU ends up owning S/G of the node-local sum.
2. **Inter-node allreduce of each S/G shard** across the M nodes. This runs as G independent operations, one per GPU and its NIC ("rail"), using a ring or a tree.
3. **Intra-node all-gather** to redistribute the result.

```text
T_hier ≈ [2(G-1)α_intra + 2·(G-1)/G·S·β_intra]                      (steps 1 + 3)
       + [2(M-1)α_inter  or  2·log2(M)·α_inter] + 2·(M-1)/M·(S/G)·β_inter   (step 2)
```

The bandwidth on the slow links barely changes compared with a well-built flat multi-rail ring: 2(M-1)/M·S/G vs. 2(N-1)/N·S/G per NIC. The big win is **latency**: the number of slow-link steps drops from 2(N-1) to 2(M-1) or 2·log2 M. Traffic that can stay on the fast intra-node fabric also stays there.

**Worked example: N = 1024 GPUs (M = 128 nodes × G = 8), S = 1 MiB** (a small tensor-parallel or optimizer-state collective). Assume α_inter = 5 µs, B_inter = 50 GB/s, α_intra = 2 µs, B_intra = 300 GB/s.

| Algorithm | Latency term | Bandwidth term | Total |
|---|---|---|---|
| Flat ring over 1024 GPUs | 2·1023·5 µs = 10.23 ms | 2·(1023/1024)·1 MiB / 50 GB/s = 42 µs | **≈ 10.3 ms** |
| Hierarchical, ring between nodes | 7·2 + 254·5 + 7·2 µs = 1.30 ms | 2·3.1 µs (intra) + 5.2 µs (inter) ≈ 11 µs | **≈ 1.3 ms** |
| Hierarchical, double binary tree between nodes | 14 + 2·7·5 + 14 µs = 98 µs | ≈ 11 µs | **≈ 0.11 ms** |

That is a ~95x difference for a 1 MiB message, purely from the latency term. This is why NCCL uses trees between nodes at scale, and why "my allreduce got slower when I scaled from 64 to 1024 GPUs" is a classic interview scenario.

Practical topology checks:
- `amd-smi topology -t` (or `rocm-smi --showtopo`) shows the link type (XGMI/PCIE) between GPU pairs. `nvidia-smi topo -m` shows NVLink/PCIe distances and the NIC affinity.
- Bind each rank to the CPU NUMA node and NIC closest to its GPU. Otherwise GPUDirect RDMA may be disabled (see `NCCL_NET_GDR_LEVEL`) or traffic crosses the inter-socket link.
- `NCCL_TOPO_DUMP_FILE=topo.xml` dumps the topology the library detected. Compare it with what you expect.

## 34.8 How NCCL/RCCL Execute Collectives: Channels, Algorithms, Protocols

- **Collectives are GPU kernels.** A collective is a kernel that copies and reduces through peer-mapped memory (P2P), shared host memory, or a network proxy thread that drives the NIC. Each **channel** is one workgroup/CTA running one ring or tree instance over a slice of the buffer. More channels mean more links in use and more bandwidth, but they also **consume more CUs/SMs**, which compete with your compute kernels during overlap.
- **Algorithms:** `Ring` and `Tree` are common to both libraries (Tree means a double binary tree between nodes and a chain within a node). NVIDIA-specific additions include `CollNet` (in-network reduction with InfiniBand SHARP switches), `NVLS`/`NVLSTree` (NVSwitch multicast and in-switch reduction), and `PAT` (for all-gather and reduce-scatter at one GPU per node, in recent NCCL).
- **Protocols** trade bandwidth for latency:

| Protocol | Mechanism | Bandwidth efficiency | Latency | Used for |
|---|---|---|---|---|
| `LL` (low latency) | 8-byte stores of 4 B data + 4 B flag. The receiver polls the flag, so no separate fence/flag round trip is needed | ~50% | Lowest | Small messages |
| `LL128` | 128-byte lines carrying 120 B data + 8 B flag. Relies on 128-byte store atomicity from the hardware and link | ~94% | Low | Small/medium. Only on platforms where it is validated |
| `Simple` | Large chunks, with a memory fence and then a flag per chunk | ~100% | Highest | Large messages |

- **Tuning model:** for every (collective, algorithm, protocol) pair, the library predicts `time = latency(algo, proto, N) + S / bandwidth(algo, proto, topology)` and picks the minimum. That is the alpha-beta model from 34.2. `NCCL_ALGO` and `NCCL_PROTO` override the choice. Use them for experiments and bug isolation, not as permanent settings.

## 34.9 The NCCL/RCCL API

Core concepts:
- **`ncclUniqueId`**: an opaque 128-byte token. One rank creates it with `ncclGetUniqueId` and it is distributed **out of band** (MPI_Bcast, a TCP key-value store, a file). It identifies the communicator being created.
- **`ncclCommInitRank(&comm, nranks, id, rank)`**: a *collective* call. Each rank creates its communicator for its current device, and the call blocks until all `nranks` ranks have joined.
- **Collectives are asynchronous and stream-ordered.** `ncclAllReduce(send, recv, count, dtype, op, comm, stream)` only enqueues work. Completion is observed through the stream (events, `hipStreamSynchronize`). In-place operation (`send == recv`) is allowed.
- **`ncclGroupStart()` / `ncclGroupEnd()`** serve three purposes:
  1. A single thread can drive several GPUs (initialization and collectives) without deadlocking on the first blocking call.
  2. Several collectives can be fused into one launch.
  3. Matching `ncclSend`/`ncclRecv` pairs can be posted without ordering deadlocks.

Complete single-process example. It drives every visible GPU from one thread and runs as-is on an 8-GPU node:

```cpp
// Single process, one thread, all visible GPUs: allreduce a float buffer.
// Build: hipcc -O2 rccl_allreduce.cpp -lrccl -o rccl_allreduce
#include <hip/hip_runtime.h>
#include <rccl/rccl.h>   // NVIDIA: #include <nccl.h> and the cuda* equivalents
#include <cstdio>
#include <cstdlib>
#include <vector>

#define HIP_CHECK(cmd) do { hipError_t e = (cmd); if (e != hipSuccess) { \
    std::fprintf(stderr, "HIP %s:%d: %s\n", __FILE__, __LINE__, hipGetErrorString(e)); \
    std::exit(1); } } while (0)
#define NCCL_CHECK(cmd) do { ncclResult_t r = (cmd); if (r != ncclSuccess) { \
    std::fprintf(stderr, "NCCL %s:%d: %s\n", __FILE__, __LINE__, ncclGetErrorString(r)); \
    std::exit(1); } } while (0)

int main() {
    int ndev = 0;
    HIP_CHECK(hipGetDeviceCount(&ndev));
    const size_t count = 1 << 24;                 // 16M floats = 64 MiB per GPU

    std::vector<float*> sendbuf(ndev), recvbuf(ndev);
    std::vector<hipStream_t> streams(ndev);
    std::vector<ncclComm_t> comms(ndev);

    for (int d = 0; d < ndev; ++d) {
        HIP_CHECK(hipSetDevice(d));
        HIP_CHECK(hipMalloc(&sendbuf[d], count * sizeof(float)));
        HIP_CHECK(hipMalloc(&recvbuf[d], count * sizeof(float)));
        std::vector<float> h(count, float(d + 1));  // rank d contributes d+1
        HIP_CHECK(hipMemcpy(sendbuf[d], h.data(), count * sizeof(float), hipMemcpyHostToDevice));
        HIP_CHECK(hipStreamCreateWithFlags(&streams[d], hipStreamNonBlocking));
    }

    // 1) One rank creates the unique id; in multi-process jobs it is broadcast
    //    out of band (MPI_Bcast, a TCP store, ...). Here all ranks share it.
    ncclUniqueId id;
    NCCL_CHECK(ncclGetUniqueId(&id));

    // 2) ncclCommInitRank is collective: when one thread drives several GPUs,
    //    the calls must be inside a group or the first call blocks forever.
    NCCL_CHECK(ncclGroupStart());
    for (int d = 0; d < ndev; ++d) {
        HIP_CHECK(hipSetDevice(d));
        NCCL_CHECK(ncclCommInitRank(&comms[d], ndev, id, d));
    }
    NCCL_CHECK(ncclGroupEnd());

    // 3) Enqueue the allreduce on each GPU's stream. The call returns as soon
    //    as the work is enqueued; completion is observed via the stream.
    NCCL_CHECK(ncclGroupStart());
    for (int d = 0; d < ndev; ++d) {
        NCCL_CHECK(ncclAllReduce(sendbuf[d], recvbuf[d], count, ncclFloat, ncclSum,
                                 comms[d], streams[d]));
    }
    NCCL_CHECK(ncclGroupEnd());

    for (int d = 0; d < ndev; ++d) {
        HIP_CHECK(hipSetDevice(d));
        HIP_CHECK(hipStreamSynchronize(streams[d]));
    }

    // Every element should equal 1 + 2 + ... + ndev.
    const float expected = ndev * (ndev + 1) / 2.0f;
    float got = 0.0f;
    HIP_CHECK(hipSetDevice(ndev - 1));
    HIP_CHECK(hipMemcpy(&got, recvbuf[ndev - 1] + count - 1, sizeof(float), hipMemcpyDeviceToHost));
    std::printf("ndev=%d expected=%.1f got=%.1f %s\n", ndev, expected, got,
                got == expected ? "OK" : "MISMATCH");

    for (int d = 0; d < ndev; ++d) {
        NCCL_CHECK(ncclCommDestroy(comms[d]));
        HIP_CHECK(hipSetDevice(d));
        HIP_CHECK(hipStreamDestroy(streams[d]));
        HIP_CHECK(hipFree(sendbuf[d]));
        HIP_CHECK(hipFree(recvbuf[d]));
    }
    return got == expected ? 0 : 1;
}
```

```text
$ hipcc -O2 rccl_allreduce.cpp -lrccl -o rccl_allreduce && ./rccl_allreduce
ndev=8 expected=36.0 got=36.0 OK
```

> **See also:** in CMake, link RCCL with `find_package(rccl REQUIRED)` and `target_link_libraries(app PRIVATE roc::rccl)`. The installed `rccl-targets.cmake` exports `roc::rccl`, even though one ROCm doc table says `rccl`. See [CMake Fundamentals -- Linking ROCm Libraries and Profiler SDKs](../tools/CMake_Fundamentals.md#645-linking-rocm-libraries-and-profiler-sdks).

The production pattern is **one process per GPU**, with the id distributed by MPI:

```cpp
// fragment: one MPI rank per GPU
int rank, nranks;
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &nranks);

MPI_Comm node_comm;                                   // ranks on the same node
MPI_Comm_split_type(MPI_COMM_WORLD, MPI_COMM_TYPE_SHARED, rank, MPI_INFO_NULL, &node_comm);
int local_rank;
MPI_Comm_rank(node_comm, &local_rank);
hipSetDevice(local_rank);                             // BEFORE creating the communicator

ncclUniqueId id;
if (rank == 0) ncclGetUniqueId(&id);
MPI_Bcast(&id, sizeof(id), MPI_BYTE, 0, MPI_COMM_WORLD);

ncclComm_t comm;
ncclCommInitRank(&comm, nranks, id, rank);
ncclAllReduce(grads, grads, count, ncclBfloat16, ncclSum, comm, stream);   // in place
// ... keep enqueueing work; synchronize only when the host needs the result
ncclCommDestroy(comm);
```

All-to-all (MoE token dispatch) built from grouped point-to-point calls:

```cpp
// fragment: grouped send/recv; without the group, a blocking send to a peer
// that is itself blocked in a send would deadlock
ncclGroupStart();
for (int peer = 0; peer < nranks; ++peer) {
    ncclSend(sendbuf + peer * chunk, chunk, ncclFloat, peer, comm, stream);
    ncclRecv(recvbuf + peer * chunk, chunk, ncclFloat, peer, comm, stream);
}
ncclGroupEnd();
```

Rules that cause hangs when broken:
- **Every rank must call the same collectives in the same order, with the same count and datatype.** A rank that skips a collective, or calls collectives in a different order (for example, iterating over a `dict` whose order differs between processes), hangs everyone else.
- A communicator must not be used concurrently from two host threads. Use one communicator per thread, or serialize access.
- When one thread drives several GPUs, wrap the per-GPU calls in a group. Otherwise the first call blocks while it waits for ranks that will never be launched.
- Errors are often asynchronous. Poll `ncclCommGetAsyncError`, and use `ncclCommAbort` from a watchdog with a timeout. PyTorch's NCCL watchdog does exactly this.

## 34.10 Environment Variables, Debugging, and rccl-tests

RCCL keeps the `NCCL_` prefix for compatibility.

| Variable | Purpose |
|---|---|
| `NCCL_DEBUG=INFO` (`WARN`, `TRACE`) | Print the version, detected topology, rings/trees, transports (P2P/SHM/NET), and GDR use |
| `NCCL_DEBUG_SUBSYS=INIT,GRAPH,TUNING,COLL,NET` | Restrict output to subsystems. `COLL` logs every collective call with its size, which is useful for finding the rank that diverged |
| `NCCL_DEBUG_FILE=/tmp/nccl.%h.%p.log` | One log file per host and process |
| `NCCL_ALGO=Ring` / `Tree`, `NCCL_PROTO=Simple` / `LL` / `LL128` | Force an algorithm or protocol (experiments, bug isolation) |
| `NCCL_MIN_NCHANNELS` / `NCCL_MAX_NCHANNELS` | Channel count. More channels give more bandwidth but use more CUs |
| `NCCL_SOCKET_IFNAME=eth0` | Interface for bootstrap and socket traffic |
| `NCCL_IB_HCA=mlx5_0,mlx5_1` | Which InfiniBand/RoCE adapters to use |
| `NCCL_NET_GDR_LEVEL` | Maximum GPU-NIC distance at which GPUDirect RDMA is used |
| `NCCL_P2P_DISABLE=1`, `NCCL_SHM_DISABLE=1` | Turn off a transport to isolate a problem |
| `NCCL_TOPO_DUMP_FILE`, `NCCL_GRAPH_DUMP_FILE` | Dump the detected topology and the computed rings/trees as XML |
| `HSA_FORCE_FINE_GRAIN_PCIE=1` (RCCL) | Enable peer-to-peer access between PCIe-connected AMD GPUs |
| `NCCL_IGNORE_CPU_AFFINITY=1` (RCCL tip) | Use GPU affinity only, ignoring the job's CPU mask. Can help multi-node scaling |

RCCL's own usage-tips page also recommends raising `NCCL_MIN_NCHANNELS` on MI300X systems that use fewer than 8 GPUs. Check the RCCL documentation for your ROCm version, because these tips change between releases.

**rccl-tests / nccl-tests** are the standard microbenchmarks:

```bash
git clone https://github.com/ROCm/rccl-tests && cd rccl-tests
make HIP_HOME=/opt/rocm NCCL_HOME=/opt/rocm             # add MPI=1 MPI_HOME=/path/to/mpi for multi-node

./build/all_reduce_perf -b 8 -e 128M -f 2 -g 8           # 1 process, 8 GPUs, 8 B..128 MB, x2 steps
mpirun -np 64 -N 8 ./build/all_reduce_perf -b 8 -e 8G -f 2 -g 1    # 8 nodes x 8 GPUs
```

How to read the output:
- The `time` column at small sizes is effectively the per-collective latency, roughly steps × α. Its growth with N tells you whether you are on a ring or a tree.
- `busbw` at large sizes should plateau near the bottleneck link bandwidth. If it plateaus well below, check the channel count, whether P2P or GDR is actually used (`NCCL_DEBUG=INFO`), NUMA and NIC binding, and the PCIe link width and generation.
- The `#wrong` column must be 0. Non-zero values point to memory corruption or a broken transport.

**Profiling communication:** `rocprofv3 --rccl-trace --kernel-trace` records RCCL API calls and the communication kernels. `rocprof-sys` shows RCCL waits on the whole-application timeline next to compute.

> **See also:** [Distributed training with DDP/FSDP](ML_AI_Frameworks.md#7-distributed-training) (the framework side of these collectives), [ML Systems Design](ML_Systems_Design.md) (sizing data/tensor/pipeline parallelism and their communication budgets), [Math, Probability, and Estimation](../computer-science/Math_Probability_Estimation.md) (back-of-envelope technique), and [Performance Engineering -- Amdahl and strong/weak scaling](../computer-science/Performance_Engineering.md#2-amdahls-and-gustafsons-laws) (communication as the serial fraction).

## 34.11 Interview Questions -- Collectives

**Q1.** Derive the time for ring allreduce of S bytes on N GPUs. Why is it called bandwidth-optimal?

Ring allreduce is a reduce-scatter followed by an all-gather, each with N-1 steps. In every step each rank sends one S/N-byte chunk to its neighbor, and all links are busy at once. Total: T = 2(N-1)·α + 2(N-1)/N·S·β (+ (N-1)/N·S·γ for the reduction arithmetic). The bandwidth term 2(N-1)/N·S·β equals the proven lower bound for allreduce, and it tends to 2·S·β *independent of N*. Adding GPUs does not increase the bytes per link. The catch is the latency term, which grows linearly with N. Common follow-up: "what changes with 2 GPUs?" The factor 2(N-1)/N = 1, so each GPU sends S bytes, which is the same as just exchanging buffers.

**Q2.** Your allreduce of 1 MiB tensors got about 15x slower going from 64 to 1024 GPUs, but large-gradient allreduces barely changed. Explain it and fix it.

The 1 MiB messages are in the latency regime (S ≲ α/β × a few). With a flat ring, the latency term 2(N-1)·α grows from 126α to 2046α (16.2x), while the bandwidth term stays at about 2·S·β. With the 34.6 numbers (α = 5 µs, B = 50 GB/s): T(64) ≈ 630 + 41 = 671 µs and T(1024) ≈ 10,230 + 42 = 10,272 µs, about 15x. Large buffers are bandwidth-dominated, so they do not notice. Follow-up: if the slowdown were much larger (say 50x or more), the ring latency term alone cannot explain it. A likely cause is that the 64-GPU run used a tree (≈ 2·log2 64·α + 2·S·β ≈ 60 + 42 ≈ 100 µs) while the 1024-GPU run was forced onto a ring, for example by a stale `NCCL_ALGO=Ring`. Fixes:
- Use a tree or hierarchical algorithm (double binary tree between nodes: 2·log2 M·α).
- Make sure the library's tuner is not being overridden by `NCCL_ALGO=Ring` (it is often left set from an old experiment).
- Fuse small tensors into larger buckets so you pay α less often.
- Use the LL/LL128 protocols for small messages.

**Q3.** Why does NCCL use a *double* binary tree instead of one binary tree?

In a pipelined binary tree, internal nodes receive from two children during the reduce and send to two children during the broadcast, so their links carry about 2x the traffic of a leaf. The tree then delivers only about half the bandwidth. With two complementary trees, each rank is internal in one and a leaf in the other, and each tree carries half the data. Every rank then sends and receives about 2S total, the same as the ring, while latency stays logarithmic.

**Q4.** rccl-tests on an 8× MI300X node shows allreduce busbw of 150 GB/s at 1 GB. Good or bad? What would you check?

It is low. Each GPU has 7 xGMI links at 64 GB/s peak per direction (448 GB/s aggregate). AMD reports about 48 GB/s achievable per link, so the practical ceiling is about 300+ GB/s busbw. Check the following:
- Confirm `-g 8` (or 8 ranks) and P2P transport in `NCCL_DEBUG=INFO`, not SHM through host memory.
- Check the channel count. A single ring uses one link per direction, so all 7 links need many channels with different ring orders.
- Make sure no other process is using the GPUs, and check the compute/memory partition mode with `amd-smi`.
- Check the ROCm/RCCL version and the RCCL tuning tips for that platform.
- Check the message size: 1 GB should be well into the bandwidth regime.

**Q5.** Compare the communication volume of DDP, ZeRO-2, and ZeRO-3/FSDP per step for Ψ bytes of gradients/parameters.

- DDP: one gradient allreduce, ≈ 2Ψ per GPU.
- ZeRO-2: reduce-scatter of gradients (Ψ), then all-gather of the updated parameters (Ψ), ≈ 2Ψ. That is the same volume, but with sharded optimizer state and gradients.
- ZeRO-3/FSDP: parameter all-gather in forward (Ψ) + parameter all-gather in backward (Ψ) + gradient reduce-scatter (Ψ) ≈ 3Ψ, or 1.5x DDP. The payoff is that parameters are sharded too, so memory per GPU drops by about N times for parameters, gradients, and optimizer state.

**Q6.** How does PyTorch DDP overlap gradient communication with backward, and what limits the overlap?

Gradients are grouped into **buckets** (default 25 MB) in roughly reverse-layer order. As soon as all the gradients in a bucket are produced, an asynchronous allreduce for that bucket is launched on a separate communication stream, while backward continues on the compute stream. Limits:
- The **last** bucket(s) cannot overlap.
- Buckets that are too small pay α many times. Buckets that are too large delay the start of communication.
- Collective kernels **consume CUs/SMs and memory bandwidth**, so compute slows down while they run.
- All ranks must launch buckets in the same order.
- Host-side synchronization (`.item()`, sync copies) serializes everything.

**Q7.** A 256-GPU job hangs inside an allreduce. How do you debug it?

1. Turn on `NCCL_DEBUG=INFO NCCL_DEBUG_SUBSYS=COLL` (plus `NCCL_DEBUG_FILE` per process) and find the rank whose last collective sequence number or size differs. That is usually a rank that took a different code path, for example one that skipped a step on a NaN or built a different bucket order.
2. Check for a crashed or OOM-killed rank. The other ranks wait forever unless a watchdog or timeout aborts them.
3. Check the network: `NCCL_SOCKET_IFNAME`, `NCCL_IB_HCA`, firewall, IB link state. INIT logs show where bootstrap stalls.
4. Use `py-spy dump` or gdb/rocgdb stack traces on a few ranks to see who is waiting where.
5. Reproduce with rccl-tests on the same nodes to separate infrastructure problems from application problems.

Mitigation: enable async error handling and timeouts so a hang turns into an error with a stack trace.

**Q8.** Why does the topology of an MI300X node (xGMI mesh) change how collectives are implemented compared with an NVSwitch node?

On NVSwitch, every GPU can send to *any* peer at its full NVLink bandwidth, so one ring per direction already saturates the GPU's injection bandwidth, and the switch can even reduce in the network (NVLS). On a fully connected xGMI mesh, each pair has a dedicated 64 GB/s link. A single ring uses only 1 of the 7 outgoing links, about 1/7 of the bandwidth. RCCL therefore runs many channels over different ring orderings (and direct all-to-all style patterns) so that all links carry traffic at once. That costs more CUs for communication kernels. It also means point-to-point bandwidth to one peer is limited to a single link, which matters for pipeline-parallel sends.

---

# 35. Multi-GPU Programming Beyond Peer Copies (HIP)

---

Sections [24.2](#242-multi-gpu-programming) and [31.3](#313-multi-gpu-with-hip) showed peer access and `hipMemcpyPeer`. Production multi-GPU code also needs:
- memory shared *between processes*,
- graphs to remove launch overhead,
- stream-ordered allocation,
- careful use of events and priorities,
- a plan for sharing one GPU among several jobs.

The HIP APIs below mirror CUDA one to one (`hipX` ↔ `cudaX`). Differences are called out where they exist. The complete programs were compiled with `hipcc` and run on an 8-GPU CDNA node.

## 35.1 Process and Device Models

| Model | How | Pros | Cons |
|---|---|---|---|
| **One process per GPU** (MPI, `torchrun`, Slurm) | Each rank calls `hipSetDevice(local_rank)` or sees only one GPU through `HIP_VISIBLE_DEVICES` | Fault isolation; the standard model for training; one RCCL communicator per process | Sharing device memory between ranks on a node needs IPC (libraries do this internally) |
| **One thread per GPU** | `std::thread`/OpenMP, `hipSetDevice` in each thread (the current device is **per-thread** state) | One address space, cheap sharing of host data | One crash kills everything; easy to forget `hipSetDevice` in a new thread |
| **One thread, many GPUs** | A loop with `hipSetDevice(d)` and group calls | Simple demos and tests | Host-side serialization; blocking calls deadlock collectives |

Device visibility: `ROCR_VISIBLE_DEVICES` filters at the ROCr (HSA) level and accepts indices or UUIDs. Batch schedulers and container runtimes usually set it. `HIP_VISIBLE_DEVICES` filters at the HIP level, and its indices refer to the devices that ROCr already exposes. HIP also honors `CUDA_VISIBLE_DEVICES`. Setting more than one of them narrows the list twice, which is a common source of "device 0 is the wrong GPU" bugs.

## 35.2 IPC: Sharing Device Memory Between Processes

`hipIpcGetMemHandle` turns a device allocation into an opaque 64-byte handle. That handle is plain bytes and can be sent over a pipe, a socket, or MPI. Another process on the same node calls `hipIpcOpenMemHandle` and gets a pointer that maps the **same physical memory**. This is how intra-node communication libraries, PyTorch `torch.multiprocessing` CUDA/HIP tensor sharing, and inference servers avoid copying through the host.

```cpp
// Two processes share one device allocation through a HIP IPC handle.
// Build: hipcc -O2 ipc_demo.cpp -o ipc_demo
#include <hip/hip_runtime.h>
#include <sys/wait.h>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>

#define HIP_CHECK(cmd) do { hipError_t e = (cmd); if (e != hipSuccess) { \
    std::fprintf(stderr, "[pid %d] HIP %s:%d: %s\n", getpid(), __FILE__, __LINE__, \
                 hipGetErrorString(e)); std::exit(1); } } while (0)

__global__ void add_one(int* p, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) p[i] += 1;
}

int main() {
    constexpr int N = 1 << 20;
    int to_child[2], to_parent[2];
    if (pipe(to_child) != 0 || pipe(to_parent) != 0) return 1;

    // Fork BEFORE any HIP call: the HIP runtime is not fork-safe, so each
    // process must initialize its own runtime.
    pid_t pid = fork();
    if (pid == 0) {                                   // ---- consumer ----
        hipIpcMemHandle_t handle;
        if (read(to_child[0], &handle, sizeof(handle)) != sizeof(handle)) return 1;
        HIP_CHECK(hipSetDevice(0));
        int* d = nullptr;
        HIP_CHECK(hipIpcOpenMemHandle(reinterpret_cast<void**>(&d), handle,
                                      hipIpcMemLazyEnablePeerAccess));
        add_one<<<(N + 255) / 256, 256>>>(d, N);      // writes the producer's memory
        HIP_CHECK(hipGetLastError());
        HIP_CHECK(hipDeviceSynchronize());            // finish before signalling
        HIP_CHECK(hipIpcCloseMemHandle(d));
        char done = 1;
        if (write(to_parent[1], &done, 1) != 1) return 1;
        return 0;
    }

    // ---- producer ----
    HIP_CHECK(hipSetDevice(0));
    int* d = nullptr;
    HIP_CHECK(hipMalloc(&d, N * sizeof(int)));        // must be a hipMalloc base pointer
    HIP_CHECK(hipMemset(d, 0, N * sizeof(int)));
    HIP_CHECK(hipDeviceSynchronize());
    hipIpcMemHandle_t handle;
    HIP_CHECK(hipIpcGetMemHandle(&handle, d));        // opaque bytes, safe to send
    if (write(to_child[1], &handle, sizeof(handle)) != sizeof(handle)) return 1;

    char done = 0;
    if (read(to_parent[0], &done, 1) != 1) return 1;  // host-side sync point
    int last = -1;
    HIP_CHECK(hipMemcpy(&last, d + N - 1, sizeof(int), hipMemcpyDeviceToHost));
    waitpid(pid, nullptr, 0);
    std::printf("producer sees d[N-1] = %d (%s)\n", last, last == 1 ? "OK" : "FAIL");
    HIP_CHECK(hipFree(d));                            // only after the consumer closed it
    return last == 1 ? 0 : 1;
}
```

```text
$ hipcc -O2 ipc_demo.cpp -o ipc_demo && ./ipc_demo
producer sees d[N-1] = 1 (OK)
```

IPC rules and pitfalls:
- **Fork before initializing HIP.** A forked child must not use the parent's GPU context. Each process initializes its own runtime. Python's `multiprocessing` therefore needs the `spawn` start method with GPU frameworks.
- **The handle describes a whole `hipMalloc` allocation (its base address).** Caching allocators hand out sub-ranges of big blocks, so they send the handle of the block *plus an offset*. PyTorch does exactly this. Memory from `hipMallocManaged`, from host allocations, or from some pools is not exportable through this API.
- **Lifetime is the exporter's responsibility.** The exporter must not `hipFree` while importers still have the memory mapped. Importers call `hipIpcCloseMemHandle`. Opening a handle in the same process that created it fails (`hipErrorInvalidContext` on ROCm).
- **IPC shares memory, not ordering.** You still need a synchronization protocol. The demo uses a host-side message after `hipDeviceSynchronize`. To order GPU work without a host round trip, export an event: create it with `hipEventCreateWithFlags(&ev, hipEventInterprocess | hipEventDisableTiming)`, share it with `hipIpcGetEventHandle` / `hipIpcOpenEventHandle`, and have the consumer call `hipStreamWaitEvent` on it.
- **Modern alternative:** the virtual memory management (VMM) API. `hipMemCreate` with a POSIX file-descriptor handle type, then `hipMemExportToShareableHandle`, sends the FD over a Unix socket (`SCM_RIGHTS`). The importer uses `hipMemImportFromShareableHandle`, `hipMemMap`, and `hipMemSetAccess`. It gives finer control (mapping granularity, access rights, growable reservations), and newer NCCL/RCCL and PyTorch "expandable segments" build on it. IPC-exportable memory pools (`hipMemPoolExportToShareableHandle` / `hipMemPoolExportPointer`) are the stream-ordered equivalent.

## 35.3 HIP Graphs: Stream Capture Semantics and Pitfalls

`hipStreamBeginCapture` switches a stream into **capture mode**. Work submitted to it is *recorded* as graph nodes instead of executed. Recording an event on a capturing stream and making another stream wait on that event pulls the second stream into the same capture (a **fork**). Every forked stream must be **joined** back into the origin stream before `hipStreamEndCapture`. The graph is then instantiated once (validated and optimized into a `hipGraphExec_t`) and launched many times with a single submission per launch.

```cpp
// Capture a fork-join DAG (two streams) into a hipGraph, then replay it.
// Also shows stream-ordered allocation inside the captured region.
// Build: hipcc -O2 graph_demo.cpp -o graph_demo
#include <hip/hip_runtime.h>
#include <cstdio>
#include <cstdlib>

#define HIP_CHECK(cmd) do { hipError_t e = (cmd); if (e != hipSuccess) { \
    std::fprintf(stderr, "HIP %s:%d: %s\n", __FILE__, __LINE__, hipGetErrorString(e)); \
    std::exit(1); } } while (0)

__global__ void scale(float* x, float a, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) x[i] *= a;
}
__global__ void add(const float* a, const float* b, float* out, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) out[i] = a[i] + b[i];
}
__global__ void fill(float* x, float v, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) x[i] = v;
}

int main() {
    const int n = 1 << 20, threads = 256, blocks = (n + threads - 1) / threads;
    float *x, *y;
    HIP_CHECK(hipMalloc(&x, n * sizeof(float)));
    HIP_CHECK(hipMalloc(&y, n * sizeof(float)));

    hipStream_t s0, s1;
    HIP_CHECK(hipStreamCreateWithFlags(&s0, hipStreamNonBlocking));
    HIP_CHECK(hipStreamCreateWithFlags(&s1, hipStreamNonBlocking));
    hipEvent_t fork_ev, join_ev;   // sync-only events: no timestamps needed
    HIP_CHECK(hipEventCreateWithFlags(&fork_ev, hipEventDisableTiming));
    HIP_CHECK(hipEventCreateWithFlags(&join_ev, hipEventDisableTiming));

    // ---------------- capture ----------------
    hipGraph_t graph;
    HIP_CHECK(hipStreamBeginCapture(s0, hipStreamCaptureModeGlobal));
    fill<<<blocks, threads, 0, s0>>>(x, 1.0f, n);
    fill<<<blocks, threads, 0, s0>>>(y, 2.0f, n);
    HIP_CHECK(hipEventRecord(fork_ev, s0));
    HIP_CHECK(hipStreamWaitEvent(s1, fork_ev, 0));      // s1 joins the capture (fork)
    scale<<<blocks, threads, 0, s0>>>(x, 3.0f, n);      // branch A on s0
    scale<<<blocks, threads, 0, s1>>>(y, 4.0f, n);      // branch B on s1
    HIP_CHECK(hipEventRecord(join_ev, s1));
    HIP_CHECK(hipStreamWaitEvent(s0, join_ev, 0));      // join back before EndCapture
    float* tmp = nullptr;                               // becomes a mem-alloc node
    HIP_CHECK(hipMallocAsync(reinterpret_cast<void**>(&tmp), n * sizeof(float), s0));
    add<<<blocks, threads, 0, s0>>>(x, y, tmp, n);      // tmp = 3 + 8 = 11
    HIP_CHECK(hipMemcpyAsync(x, tmp, n * sizeof(float), hipMemcpyDeviceToDevice, s0));
    HIP_CHECK(hipFreeAsync(tmp, s0));                   // becomes a mem-free node
    HIP_CHECK(hipStreamEndCapture(s0, &graph));

    size_t num_nodes = 0;
    HIP_CHECK(hipGraphGetNodes(graph, nullptr, &num_nodes));
    hipGraphExec_t exec;
    HIP_CHECK(hipGraphInstantiateWithFlags(&exec, graph, 0));

    // ---------------- replay ----------------
    for (int iter = 0; iter < 100; ++iter)
        HIP_CHECK(hipGraphLaunch(exec, s0));            // one submission per DAG
    HIP_CHECK(hipStreamSynchronize(s0));

    float h = 0.0f;
    HIP_CHECK(hipMemcpy(&h, x + n - 1, sizeof(float), hipMemcpyDeviceToHost));
    std::printf("graph nodes=%zu  x[n-1]=%.1f (%s)\n", num_nodes, h, h == 11.0f ? "OK" : "FAIL");

    HIP_CHECK(hipGraphExecDestroy(exec));
    HIP_CHECK(hipGraphDestroy(graph));
    HIP_CHECK(hipEventDestroy(fork_ev));
    HIP_CHECK(hipEventDestroy(join_ev));
    HIP_CHECK(hipStreamDestroy(s0));
    HIP_CHECK(hipStreamDestroy(s1));
    HIP_CHECK(hipFree(x));
    HIP_CHECK(hipFree(y));
    return h == 11.0f ? 0 : 1;
}
```

```text
$ hipcc -O2 graph_demo.cpp -o graph_demo && ./graph_demo
graph nodes=8  x[n-1]=11.0 (OK)
```

The 8 nodes are: 2 fills, 2 scales, a mem-alloc node, the add kernel, a memcpy node, and a mem-free node. The two `scale` kernels are siblings in the DAG, so they can run concurrently on replay.

**Capture modes** decide which "potentially unsafe" API calls are rejected while a capture is in progress. Examples are `hipMalloc` and synchronous operations, which could implicitly synchronize with the captured stream:

| Mode | Unsafe calls are prohibited... |
|---|---|
| `hipStreamCaptureModeGlobal` (default choice) | ...in this thread, and in any thread while some *other* thread has a global-mode capture open |
| `hipStreamCaptureModeThreadLocal` | ...only in the thread that owns the capture. Use it when unrelated threads keep allocating |
| `hipStreamCaptureModeRelaxed` | ...nowhere. You take responsibility for not breaking the capture |

**Pitfalls.** The error names below were observed on ROCm. CUDA has the same `cudaErrorStreamCapture*` family.

| Pitfall | What happens | Fix |
|---|---|---|
| Synchronous call during capture (`hipMemcpy`, `hipStreamSynchronize`, `hipDeviceSynchronize`, `hipEventSynchronize`, `hipStreamQuery`) | Returns `hipErrorStreamCaptureImplicit`/`Unsupported` and **invalidates** the capture. `hipStreamEndCapture` then returns `hipErrorStreamCaptureInvalidated` | Use only async APIs inside the region. Do host-side reads after replay |
| `hipMalloc` during a global-mode capture | `hipErrorStreamCaptureUnsupported` | Allocate before capture, or use `hipMallocAsync` (it becomes an alloc node) |
| Forked stream not joined back | `hipStreamEndCapture` returns `hipErrorStreamCaptureUnjoined` | Record an event on every side stream and make the origin stream wait on it |
| Work launched into a stream that is **not** capturing (for example the null stream, while the capturing stream is non-blocking) | **Succeeds silently and runs eagerly. It is not in the graph** | Pass the capturing stream explicitly to every launch and library call (set the library handle's stream) |
| Kernel arguments and copy sizes are **baked in by value** at capture time | Changing a host variable later has no effect on replay. Pointers must stay valid at the **same address** | Keep static buffers. Update with `hipGraphExecKernelNodeSetParams`, or re-capture and use `hipGraphExecUpdate` (cheap when the topology is unchanged). Or pass a device pointer to the changing parameter |
| Host code between the captured calls | Runs **once**, at capture time, and not on replay | Move per-iteration host logic out of the graph, or use host nodes (`hipLaunchHostFunc`) |
| Dynamic shapes / batch sizes | One graph is valid for one shape | Capture one graph per shape bucket. vLLM does this for decode batch sizes |
| Library calls (rocBLAS, hipBLASLt, RCCL) | Must be capture-safe: no internal sync or allocation during the call | Pre-allocate library workspaces, set the handle's stream, and check that your version supports capture (NCCL supports it; RCCL supports it in recent ROCm releases) |
| Launching the same `hipGraphExec_t` concurrently on two streams | Launches of one exec are serialized | Instantiate one exec per concurrent user |

**When graphs pay off:** the GPU time per kernel is comparable to the CPU launch cost (a few µs per launch), for example LLM decode steps with hundreds of small kernels, or iterative solvers. They do not help a workload dominated by a few long kernels.

## 35.4 Stream-Ordered Memory Allocation and Memory Pools

`hipMalloc`/`hipFree` are expensive. They map and unmap pages, and `hipFree` implicitly synchronizes the device. Frameworks work around this with caching allocators. `hipMallocAsync`/`hipFreeAsync` (CUDA: `cudaMallocAsync`) build the same idea into the runtime:

- **Semantics:** the allocation is usable by work enqueued on that stream *after* the `hipMallocAsync`. It becomes free when the stream *reaches* the `hipFreeAsync`. A later `hipMallocAsync` on the same stream can reuse that memory immediately, without waiting on the host.
- **Cross-stream use:** another stream may touch the memory only after waiting on an event recorded after the allocation. A free on stream A followed by reuse on stream B is made safe by the pool, which tracks event dependencies. The pool attributes `hipMemPoolReuseFollowEventDependencies`, `hipMemPoolReuseAllowOpportunistic`, and `hipMemPoolReuseAllowInternalDependencies` control how aggressive reuse is.
- **Release threshold:** by default (threshold 0) the pool returns unused memory to the driver at every synchronization, so the next iteration pays the mapping cost again. Set `hipMemPoolAttrReleaseThreshold` high to keep a warm cache.
- **Pools:** each device has a default pool (`hipDeviceGetDefaultMemPool`). Custom pools (`hipMemPoolCreate`) can be IPC-exportable or have different access settings. `hipMallocFromPoolAsync` selects a pool explicitly.
- **Inside graphs**, `hipMallocAsync`/`hipFreeAsync` become alloc/free nodes ([35.3](#353-hip-graphs-stream-capture-semantics-and-pitfalls)). Their memory can be reused across graph launches.

```cpp
// Stream-ordered allocation with the device's default memory pool, plus a
// high-priority stream. Build: hipcc -O2 mempool_demo.cpp -o mempool_demo
#include <hip/hip_runtime.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

#define HIP_CHECK(cmd) do { hipError_t e = (cmd); if (e != hipSuccess) { \
    std::fprintf(stderr, "HIP %s:%d: %s\n", __FILE__, __LINE__, hipGetErrorString(e)); \
    std::exit(1); } } while (0)

__global__ void iota(float* x, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) x[i] = static_cast<float>(i);
}

int main() {
    int dev = 0, supported = 0;
    HIP_CHECK(hipSetDevice(dev));
    HIP_CHECK(hipDeviceGetAttribute(&supported, hipDeviceAttributeMemoryPoolsSupported, dev));
    if (!supported) { std::printf("memory pools not supported\n"); return 0; }

    // Keep up to 1 GiB cached in the pool across synchronizations instead of
    // returning it to the driver (default threshold 0 = release at every sync).
    hipMemPool_t pool;
    HIP_CHECK(hipDeviceGetDefaultMemPool(&pool, dev));
    uint64_t threshold = 1ull << 30;
    HIP_CHECK(hipMemPoolSetAttribute(pool, hipMemPoolAttrReleaseThreshold, &threshold));

    // Priorities: numerically LOWER = HIGHER priority. Query the legal range.
    int least = 0, greatest = 0;
    HIP_CHECK(hipDeviceGetStreamPriorityRange(&least, &greatest));
    hipStream_t hi, lo;
    HIP_CHECK(hipStreamCreateWithPriority(&hi, hipStreamNonBlocking, greatest));
    HIP_CHECK(hipStreamCreateWithPriority(&lo, hipStreamNonBlocking, least));

    const int n = 1 << 22;
    for (int step = 0; step < 10; ++step) {
        float* tmp = nullptr;
        // Allocation becomes valid in stream order: no device-wide sync, and
        // after the first iteration the pool reuses the same physical memory.
        HIP_CHECK(hipMallocAsync(reinterpret_cast<void**>(&tmp), n * sizeof(float), lo));
        iota<<<(n + 255) / 256, 256, 0, lo>>>(tmp, n);
        HIP_CHECK(hipFreeAsync(tmp, lo));  // freed when the stream reaches this point
    }
    float* small = nullptr;                 // latency-critical work goes to `hi`:
    HIP_CHECK(hipMallocAsync(reinterpret_cast<void**>(&small), 64 * sizeof(float), hi));
    iota<<<1, 64, 0, hi>>>(small, 64);      // dispatched ahead of queued `lo` workgroups
    HIP_CHECK(hipFreeAsync(small, hi));
    HIP_CHECK(hipStreamSynchronize(lo));
    HIP_CHECK(hipStreamSynchronize(hi));

    uint64_t reserved = 0, used = 0;
    HIP_CHECK(hipMemPoolGetAttribute(pool, hipMemPoolAttrReservedMemCurrent, &reserved));
    HIP_CHECK(hipMemPoolGetAttribute(pool, hipMemPoolAttrUsedMemCurrent, &used));
    std::printf("priority range [least=%d, greatest=%d]; pool reserved=%llu MiB used=%llu MiB\n",
                least, greatest, (unsigned long long)(reserved >> 20),
                (unsigned long long)(used >> 20));
    HIP_CHECK(hipStreamDestroy(hi));
    HIP_CHECK(hipStreamDestroy(lo));
    return 0;
}
```

```text
$ hipcc -O2 mempool_demo.cpp -o mempool_demo && ./mempool_demo
priority range [least=1, greatest=-1]; pool reserved=128 MiB used=0 MiB
```

The pool kept 128 MiB reserved after ten 16 MiB allocations and frees. It reserves in large chunks and kept them because of the release threshold, so iterations 2-10 never went back to the driver. This is the same hazard model as PyTorch's caching allocator. There, using a tensor on a second stream without `tensor.record_stream(s)` lets its memory be reused while the second stream is still reading it.

## 35.5 Events, Stream Priorities, and CU Masking

| Event flag | Meaning | Use |
|---|---|---|
| `hipEventDefault` | Records timestamps | `hipEventElapsedTime` measurements |
| `hipEventDisableTiming` | No timestamp; cheaper to record and wait on | Pure dependencies (`hipStreamWaitEvent`); recommended for sync-only events |
| `hipEventBlockingSync` | `hipEventSynchronize` sleeps instead of spin-waiting | Frees a CPU core when waiting on long GPU work |
| `hipEventInterprocess` | Shareable through `hipIpcGetEventHandle` (requires `DisableTiming`) | Cross-process GPU-side ordering |

- `hipStreamWaitEvent(stream, ev)` creates a **GPU-side** dependency. The host does not block. This is the building block for fork/join pipelines and for overlapping communication with compute.
- Event timing measures GPU timestamps on one stream. It includes any idle gaps between the two records. The first launch of a kernel also includes code-object loading, so warm up first.
- **Stream priorities:** `hipDeviceGetStreamPriorityRange(&least, &greatest)`. A **numerically lower value means higher priority**. ROCm reported [least = 1, greatest = -1] on the test system; recent NVIDIA GPUs typically report [0, -5]. When CUs become free, the dispatcher prefers workgroups from higher-priority queues. Workgroups that are already running are not preempted, so priority helps most when the low-priority kernel is made of many short workgroups. Typical uses are communication kernels, latency-critical inference requests, and decode next to background prefill.
- **Streams map to a limited set of hardware queues on AMD.** HIP assigns hardware queues to streams in creation order, with a default of 4 per priority level (`GPU_MAX_HW_QUEUES`). A fifth stream shares a queue with an earlier one, which can serialize work you expected to overlap. On Instinct GPUs the hardware scheduler maps up to 24 user-mode compute queues at once. Beyond that, queues are time-sliced (the driver logs "Runlist is getting oversubscribed").
- **CU masking (AMD-specific):** `hipExtStreamCreateWithCUMask(&stream, num_words, mask)` restricts a stream's kernels to a subset of CUs. This is spatial partitioning inside one process, for example reserving CUs so communication kernels never starve, or running two models side by side with predictable latency.

```cpp
// fragment: restrict a stream to CUs 0..31 (mask is an array of 32-bit words, bit i = CU i)
hipDeviceProp_t prop;
hipGetDeviceProperties(&prop, 0);
std::vector<uint32_t> mask((prop.multiProcessorCount + 31) / 32, 0u);
mask[0] = 0xFFFFFFFFu;
hipStream_t s;
hipExtStreamCreateWithCUMask(&s, static_cast<uint32_t>(mask.size()), mask.data());
```

## 35.6 Sharing One GPU Between Processes: MPS, MIG, and AMD Partitions

**NVIDIA:**
- **Default:** each process has its own context, and kernels from different contexts are **time-sliced**. They do not run at the same time.
- **MPS (Multi-Process Service):** a daemon funnels the work of many client processes into one hardware context, so their kernels **run concurrently**. Since Volta, each client gets an isolated address space and a configurable share of SMs (`CUDA_MPS_ACTIVE_THREAD_PERCENTAGE`). Fault isolation is weaker: a fatal GPU fault in one client can take down the others. Typical uses are many small MPI ranks or inference processes per GPU.
- **MIG (Multi-Instance GPU, A100/H100 and later):** hardware partitions of up to 7 instances, each with dedicated SMs, L2 slices, and memory controllers. This gives real QoS and fault isolation, at the cost of fixed, coarse slices.

**AMD:**
- **No MPS-style daemon is needed for concurrency.** Each process owns its own user-mode queues and GPU virtual address space (VMID). The firmware hardware scheduler maps queues from several processes at once, so kernels from different processes can run concurrently. The limits are hardware queue slots and the number of processes per scheduling quantum. Past those limits the runlist is **oversubscribed** and round-robin time-sliced, and performance drops sharply. Reducing `GPU_MAX_HW_QUEUES` per process helps many processes fit.
- **Spatial partitioning on MI300X (and later):**
  - **Compute partitions:** **SPX** (one GPU with all 8 XCDs), **DPX** (2), **QPX** (4), and **CPX** (8 partitions, one XCD and 38 CUs each).
  - **Memory (NUMA) partitions:** **NPS1** (interleaved across all HBM stacks) and **NPS4** (each quarter of HBM local to its XCDs).
  - CPX + NPS4 turns one MI300X into 8 logical GPUs, 64 per 8-GPU node, each with local memory. That suits many small models and improves memory locality.
  - Partitions are set with `amd-smi set -C CPX` / `amd-smi set -M NPS4` (root, no running workloads). The available modes differ by product; MI350-series parts also support DPX + NPS2.

| Mechanism | Concurrency | Isolation (memory / fault / QoS) | Granularity |
|---|---|---|---|
| Time slicing (NVIDIA default) | No (serialized) | Yes / yes / no | Whole GPU |
| NVIDIA MPS | Yes | Address space yes; fault partial; QoS by SM % | SM fraction |
| NVIDIA MIG | Yes | Yes / yes / yes | Fixed slices (up to 7) |
| AMD multi-process (HWS) | Yes, up to the queue limits | Yes / mostly / no | Whole GPU |
| AMD CU masking | Yes | Same process / no / CU-level QoS | Per CU |
| AMD compute + memory partitions | Yes | Yes / yes / yes | XCD (CPX) and HBM quarter (NPS4) |

## 35.7 Overlapping Communication with Computation

```cpp
// fragment: overlap allreduce of gradient bucket b with backward compute of bucket b+1
for (int b = 0; b < nbuckets; ++b) {
    backward_bucket<<<grid, block, 0, compute>>>(b /*, ... */);   // produces grads[b]
    hipEventRecord(ready[b], compute);
    hipStreamWaitEvent(comm, ready[b], 0);          // comm waits for THIS bucket only
    ncclAllReduce(grads[b], grads[b], count[b], ncclBfloat16, ncclSum, nccl_comm, comm);
}
hipEventRecord(comm_done, comm);
hipStreamWaitEvent(compute, comm_done, 0);           // optimizer waits for all buckets
optimizer_step<<<grid, block, 0, compute>>>(/* ... */);
```

**Exposed communication** = max(0, T_comm − T_overlappable_compute). Worked example: a 7B-parameter model with BF16 gradients (14 GB) on 8 GPUs at 300 GB/s busbw gives T_comm = 2·(7/8)·14 GB / 300 GB/s ≈ 82 ms. If backward takes 200 ms, almost all of it can hide behind compute except the last bucket. Overlap fails when:
- communication runs on the same stream as compute, or on a blocking stream that synchronizes with the null stream;
- host-side synchronization happens inside the loop;
- the collectives' CUs and HBM bandwidth slow compute (use fewer channels, CU masking, or a higher-priority comm stream);
- streams share a hardware queue (35.5).

> **See also:** [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md) (rocgdb, sanitizers, hang debugging), [Containers and CI](../tools/Containers_and_CI.md) (passing `/dev/kfd` and `/dev/dri` and setting `ROCR_VISIBLE_DEVICES` in containers), [AMD GPU Architecture and Profiling](AMD_GPU_Architecture_and_Profiling.md) (XCDs, partitions, and queues from the hardware side), and [CS Fundamentals -- producer/consumer and synchronization](../computer-science/CS_Fundamentals.md#65-classic-concurrency-problems) (the CPU analogue of event-based stream ordering).

## 35.8 Interview Questions -- Multi-GPU Runtime

**Q1.** How does CUDA/HIP IPC work, and what are the pitfalls?

The exporter calls `hipIpcGetMemHandle` on the base pointer of a `hipMalloc` allocation and sends the handle bytes to another process on the same node. The importer calls `hipIpcOpenMemHandle` and gets its own virtual address that maps the same physical memory. Pitfalls:
- Only whole `hipMalloc` allocations are exportable, so caching allocators must also send an offset.
- The exporter must keep the allocation alive until all importers close it.
- Opening a handle in the creating process fails.
- Forking after GPU initialization is unsafe.
- IPC gives no ordering: use IPC events or a host protocol.

The modern replacement is VMM handles passed as file descriptors.

**Q2.** You captured a hipGraph, and on replay the kernel keeps using the old learning rate and an old buffer. Why?

Stream capture records kernel arguments **by value** at capture time, including the scalar learning rate and the buffer pointer. Replay reuses exactly those values. Host code between the captured calls also ran only once. Fixes:
- Store changing scalars in device memory and pass a pointer to them.
- Keep buffers at fixed addresses (static or graph-private pools).
- Update node parameters with `hipGraphExecKernelNodeSetParams`, or re-capture and `hipGraphExecUpdate` the exec.

Follow-up: work launched into a non-capturing stream during capture silently runs eagerly and never appears in the graph.

**Q3.** `hipMallocAsync` vs. `hipMalloc`: what is the difference, and what is the cross-stream hazard?

`hipMalloc` is a synchronous, expensive driver call, and `hipFree` synchronizes the device. `hipMallocAsync` is ordered in a stream and served from a pool, so it is cheap after warm-up and never blocks the host. The memory is valid for work after the allocation *on that stream*. Using it on another stream requires an event dependency. Freeing it on one stream while another stream still reads it is a use-after-free unless the reader is ordered before the free. Set the release threshold, or the pool may return memory to the driver at every sync.

**Q4.** You need to serve 8 small, latency-sensitive models on one MI300X. What are your options?

1. **CPX + NPS4 partitions**: 8 isolated logical GPUs with local memory. Best isolation and locality; the partition is fixed and needs admin rights to reconfigure.
2. **8 processes on an SPX GPU**: concurrency through the hardware scheduler. Simple, but there is no QoS, and you must stay within the hardware queue limits (lower `GPU_MAX_HW_QUEUES`).
3. **One process with CU-masked streams**: fine-grained control, but one failure domain.
4. **Batch the models in one server process**: best utilization if the models allow it.

Pick based on the isolation, QoS, and ops-flexibility requirements.

**Q5.** MPS vs. MIG?

MPS shares one GPU among processes by running their kernels in a common hardware context. It gives high utilization and fine-grained, soft SM limits, but weak fault isolation and no memory-bandwidth or L2 QoS. MIG partitions the hardware itself (SMs, L2, memory controllers) into up to 7 instances, giving strong isolation and predictable performance, but the slices are coarse and fixed. MPS suits cooperative jobs owned by one user. MIG suits multi-tenant clouds.

**Q6.** Does a high-priority stream preempt a running kernel?

Not mid-workgroup. Priority affects which queued workgroups the dispatcher launches next when resources free up. A long-running low-priority kernel with few, long workgroups can still block a high-priority kernel until its workgroups finish. Priority is effective when the background kernel has many short workgroups. For hard guarantees, use spatial partitioning (CU masks, partitions, MIG). Remember that lower numbers mean higher priority.

**Q7.** Communication is on its own stream, yet the profiler shows no overlap. List causes.

- Both streams are actually the same stream, or the comm stream is a blocking stream that syncs with null-stream work.
- The comm stream waits on an event recorded only after all of backward.
- Host-side syncs (`.item()`, synchronous copies, `hipFree`) sit inside the loop.
- On AMD, more than `GPU_MAX_HW_QUEUES` streams makes streams share a hardware queue.
- Compute kernels occupy all CUs, so the collective's workgroups cannot start (the reverse also happens).
- Collectives are launched in different orders on different ranks, so ranks wait on each other.

Verify with a `rocprofv3 --runtime-trace` or `rocprof-sys` timeline: look at the queue/stream rows and the gaps.

---

# 36. Portable Programming Models and AMD Wave-Level Primitives

---

## 36.1 The Landscape: When and Why

| Model | What it is | Backends / vendors | Who uses it | Notes |
|---|---|---|---|---|
| **CUDA** | NVIDIA's C++ language extensions + runtime | NVIDIA | Most GPU code and ML libraries | Richest ecosystem; locked to one vendor |
| **HIP** | AMD's CUDA-shaped C++ extensions + runtime | AMD (native), NVIDIA (thin header layer over CUDA) | ROCm libraries, ported CUDA apps, PyTorch on ROCm | Porting from CUDA is largely mechanical (hipify). Same mental model as CUDA |
| **SYCL 2020** | Khronos standard: single-source *ISO C++* (lambdas + library), no new keywords | Intel oneAPI DPC++ (Intel GPUs; NVIDIA/AMD through Codeplay plugins), **AdaptiveCpp** (formerly hipSYCL / Open SYCL: CUDA, HIP, Level Zero, OpenCL, generic JIT) | Aurora (Argonne) applications, Intel-centric codes, standards-driven projects | One standard, several implementations. Performance portability is not automatic |
| **OpenCL** | Khronos C host API + OpenCL C kernels compiled at run time | Nearly every vendor, including mobile GPUs and FPGAs | Legacy HPC, embedded/mobile, FPGA, some imaging apps | Verbose. OpenCL 3.0 made most 2.x features optional. AMD's "workgroup"/"NDRange" terms come from it |
| **Kokkos** | C++ performance-portability *library* (Sandia; now under the Linux Foundation's HPSF) | CUDA, HIP, SYCL, OpenMP, OpenMP-target, Threads, Serial | Trilinos, LAMMPS, many DOE apps | Abstracts both execution *and* data layout (`View`). One device backend per build |
| **RAJA** (+ Umpire, CHAI) | C++ loop-execution abstraction (LLNL) with policies | CUDA, HIP, SYCL, OpenMP, SIMD | LLNL production codes | Loop-level only. Memory is handled by Umpire (allocation) and CHAI (movement) |
| **OpenMP offload / OpenACC** | Directives on loops ([section 15](#15-openmp-target-offloading-gpu)) | All major vendors' compilers | Fortran/C++ HPC codes | Lowest porting effort. Less control |
| **C++ stdpar** | `std::for_each(std::execution::par_unseq, ...)` offloaded by the compiler | NVIDIA `nvc++ -stdpar=gpu`, AMD `--hipstdpar` (ROCm clang), AdaptiveCpp | Simple data-parallel code | Requires unified/HMM memory or allocation interposition |
| **Triton / DSLs** | Python tile-level kernel language | NVIDIA, AMD | ML kernels (attention, fused ops) | See [Triton Fundamentals](ML_AI_Frameworks.md#25-triton-fundamentals) |

**Decision rules that hold up in interviews:**
- **Existing CUDA code, need AMD:** HIP. It has the lowest effort and the same performance model, and you can keep one source for both vendors.
- **A new decade-long HPC application that must run on Frontier/El Capitan (AMD), Aurora (Intel), and NVIDIA systems:** Kokkos or RAJA (or SYCL). The vendor abstraction is then one dependency that its maintainers keep current. Kokkos also abstracts the data layout, which matters for coalescing.
- **Mostly loops over arrays, often in Fortran:** OpenMP offload or OpenACC.
- **Intel GPUs are a primary target:** SYCL with DPC++.
- **A few hot kernels need vendor-peak performance:** write native HIP/CUDA kernels or call vendor libraries (rocBLAS/hipBLASLt, cuBLAS) for those kernels, and keep the rest portable. Kokkos and SYCL both allow native-kernel interop.

## 36.2 SYCL in One Page

Key concepts and their HIP equivalents:

| SYCL | HIP/CUDA |
|---|---|
| `sycl::queue` (device + in-order or out-of-order) | stream |
| USM: `malloc_device` / `malloc_shared` / `malloc_host` | `hipMalloc` / `hipMallocManaged` / `hipHostMalloc` |
| `buffer` + `accessor` (the runtime builds the dependency DAG from access modes) | No equivalent; you order work by hand with streams and events |
| `nd_range`, work-group, work-item | grid, block, thread |
| sub-group (size chosen by the implementation: e.g. 16/32 on Intel, 32/64 on AMD) | warp / wavefront |
| `local_accessor` | `__shared__` / LDS |
| `group_barrier`, `reduce_over_group`, `joint_exclusive_scan`, `sycl::reduction` | `__syncthreads`, hipCUB `BlockReduce`/`BlockScan` |

Complete SYCL 2020 program. It needs a SYCL compiler, for example DPC++ `icpx -fsycl` or AdaptiveCpp `acpp -O3 --acpp-targets="hip:gfx942"`:

```cpp
#include <sycl/sycl.hpp>
#include <cstdio>

int main() {
    sycl::queue q{sycl::gpu_selector_v, sycl::property_list{sycl::property::queue::in_order{}}};
    const size_t n = 1 << 20;
    const float a = 3.0f;
    float* x = sycl::malloc_device<float>(n, q);
    float* y = sycl::malloc_device<float>(n, q);
    float* sum = sycl::malloc_shared<float>(1, q);
    *sum = 0.0f;

    q.fill(x, 1.0f, n);
    q.fill(y, 2.0f, n);
    q.parallel_for(sycl::range<1>{n}, [=](sycl::id<1> i) { y[i] = a * x[i] + y[i]; });
    q.parallel_for(sycl::range<1>{n}, sycl::reduction(sum, sycl::plus<float>()),
                   [=](sycl::id<1> i, auto& acc) { acc += y[i]; });
    q.wait();

    std::printf("sum = %.1f (expected %.1f) on %s\n", *sum, 5.0f * n,
                q.get_device().get_info<sycl::info::device::name>().c_str());
    sycl::free(x, q);
    sycl::free(y, q);
    sycl::free(sum, q);
    return 0;
}
```

The kernels are ordinary C++ lambdas, with no `__global__` and no `<<<>>>`. On AMD, AdaptiveCpp and the DPC++ AMD plugin both lower to the HIP/ROCm stack, so `rocprofv3` and `rocprof-compute` still see the kernels.

## 36.3 HIP vs. SYCL Trade-offs

| Aspect | HIP | SYCL |
|---|---|---|
| Governance | AMD-led open source; API shaped by CUDA | Khronos open standard; multiple implementations |
| Syntax | C++ plus kernel qualifiers and `<<<>>>` | Pure ISO C++17 (templates, lambdas) |
| Vendors | AMD native; NVIDIA via CUDA | Intel native; NVIDIA/AMD via plugins or AdaptiveCpp |
| Porting from CUDA | Mechanical (`hipify-clang`/`hipify-perl`) | SYCLomatic/`dpct` migration plus manual rewriting |
| Memory/dependencies | Explicit pointers, streams, events | USM pointers, or buffers/accessors with automatic DAG |
| Low-level control | Wave intrinsics, inline asm, `__launch_bounds__`, LDS, everything in ROCm | Sub-group functions; vendor extensions for more; features can lag hardware |
| Wave/sub-group size | `warpSize` (32 or 64), explicit | Chosen by the implementation; request with `reqd_sub_group_size` |
| Libraries | rocBLAS, hipBLASLt, MIOpen, RCCL directly | oneMKL/oneDNN (with cuBLAS/rocBLAS backends); interop for the rest |
| Tooling on AMD | ROCm profilers and debuggers natively | Works through the HIP backend; kernel names and symbols can be less readable |
| Main risk | Tied to the pace of the AMD/NVIDIA ecosystems | Implementation gaps; "portable" code still needs per-target tuning |

The honest answer is "it depends on the target matrix". Choose HIP for CUDA heritage with AMD+NVIDIA targets. Choose SYCL when Intel matters or policy requires a standard. Choose Kokkos for a large HPC code that wants one source *and* layout abstraction.

## 36.4 Kokkos and RAJA

**Kokkos** separates *where* code runs (execution space) from *where* data lives (memory space) and *how* it is laid out (layout):

```cpp
#include <Kokkos_Core.hpp>
#include <cstdio>

int main(int argc, char* argv[]) {
    Kokkos::ScopeGuard guard(argc, argv);             // initialize/finalize
    const int n = 1 << 20;
    Kokkos::View<float*> x("x", n), y("y", n);        // allocated in the default memory space

    Kokkos::parallel_for("init", n, KOKKOS_LAMBDA(const int i) { x(i) = 1.0f; y(i) = 2.0f; });
    const float a = 3.0f;
    Kokkos::parallel_for("axpy", n, KOKKOS_LAMBDA(const int i) { y(i) = a * x(i) + y(i); });

    float sum = 0.0f;
    Kokkos::parallel_reduce("sum", n, KOKKOS_LAMBDA(const int i, float& acc) { acc += y(i); }, sum);
    std::printf("sum = %.1f (expected %.1f) on %s\n", sum, 5.0f * n,
                Kokkos::DefaultExecutionSpace::name());
    return 0;
}
```

```bash
# Build Kokkos once for MI300X, then link apps with find_package(Kokkos) + Kokkos::kokkos
cmake -S kokkos -B build-kokkos -DCMAKE_CXX_COMPILER=hipcc -DKokkos_ENABLE_HIP=ON \
      -DKokkos_ARCH_AMD_GFX942=ON -DCMAKE_INSTALL_PREFIX=$HOME/kokkos-hip
cmake --build build-kokkos --target install
```

> **See also:** Kokkos's own HIP backend is configured with `hipcc` as the C++ compiler, as shown above. For your own HIP code, prefer CMake's HIP language; the reasons are in [CMake Fundamentals -- Three Ways to Build HIP Code](../tools/CMake_Fundamentals.md#641-three-ways-to-build-hip-code). Consuming an installed package such as Kokkos via `find_package(... CONFIG)` is covered in [find_package: Module Mode vs Config Mode](../tools/CMake_Fundamentals.md#28-find_package-module-mode-vs-config-mode).

- **`View` layouts:** a 2-D `View<double**>` defaults to `LayoutLeft` (column-major) on GPU spaces and `LayoutRight` (row-major) on CPU spaces. With the parallel index on the first dimension, `LayoutLeft` makes consecutive threads touch consecutive addresses (coalescing). `LayoutRight` makes each CPU thread stream through its own contiguous row (caches and vectorization). The same source therefore gets the right access pattern on both. Use `create_mirror_view` + `deep_copy` for host-device transfers.
- **Hierarchical parallelism:** `TeamPolicy` maps to workgroups, `TeamThreadRange` to threads, and `ThreadVectorRange` to SIMD lanes. Team scratch memory maps to LDS.
- **Tooling:** Kokkos Tools callbacks name every kernel by its label ("axpy"). Recent `rocprofv3` versions accept `--kokkos-trace`.

**RAJA** abstracts only the loop; you pick the execution policy:

```cpp
// fragment: RAJA forall with a HIP policy (256 threads per block) and a reduction
RAJA::ReduceSum<RAJA::hip_reduce, double> total(0.0);
RAJA::forall<RAJA::hip_exec<256>>(RAJA::RangeSegment(0, n), [=] RAJA_DEVICE (int i) {
    y[i] = a * x[i] + y[i];
    total += y[i];
});
double result = total.get();
// Swap the policy to RAJA::omp_parallel_for_exec / RAJA::seq_exec for CPU builds.
```

## 36.5 OpenCL in Brief

The host program walks a long chain of calls: platform -> device -> context -> command queue -> `clCreateProgramWithSource` + `clBuildProgram` (the kernel is compiled **at run time**) -> kernel -> buffers -> `clSetKernelArg` -> `clEnqueueNDRangeKernel` -> read back.

```c
// fragment: OpenCL C kernel, compiled at run time by clBuildProgram
__kernel void saxpy(const float a, __global const float* x, __global float* y) {
    size_t i = get_global_id(0);
    y[i] = a * x[i] + y[i];
}
```

| OpenCL | HIP/CUDA |
|---|---|
| work-item / work-group / NDRange | thread / block / grid |
| `get_global_id(0)` | `blockIdx.x * blockDim.x + threadIdx.x` |
| `get_local_id(0)` / `get_group_id(0)` | `threadIdx.x` / `blockIdx.x` |
| `__local` / `__global` / `__constant` | `__shared__` / device pointer / `__constant__` |
| `barrier(CLK_LOCAL_MEM_FENCE)` | `__syncthreads()` |
| sub-group (extension / 2.x+) | warp / wavefront |

Why CUDA won the HPC/ML market even though OpenCL is portable: single-source C++ instead of strings compiled at run time, a far better library ecosystem (cuBLAS, cuDNN, NCCL), better tools, and NVIDIA's consistent investment. OpenCL's 2.x features were never universally implemented. ROCm still ships an OpenCL runtime, and OpenCL remains common on mobile and embedded GPUs and FPGAs.

## 36.6 AMD Cross-Lane Operations: DPP, ds_swizzle, ds_bpermute, readlane

CUDA exposes `__shfl_*_sync` as the one cross-lane primitive. GCN/CDNA hardware has several mechanisms with different reach and cost. They matter when you read ISA in `rocprof-compute` or with `--save-temps`, and when you need the last few percent of a reduction or scan:

| Mechanism | Reach | Cost | HIP access | Typical use |
|---|---|---|---|---|
| **DPP** (Data Parallel Primitives) | A VALU *operand modifier*: the source is read from another lane, mostly **within a row of 16 lanes** (`quad_perm`, `row_shl/shr/ror`, `row_mirror`). On gfx9/CDNA, `row_bcast:15/31` and `wave_shr/rol` cross rows | Cheapest: folded into the ALU instruction, no LDS pipeline | `__builtin_amdgcn_update_dpp`, `__builtin_amdgcn_mov_dpp` | Inner steps of wave reductions and scans (rocPRIM uses them) |
| **`ds_swizzle_b32`** | Fixed patterns within **32-lane** groups: bit-mask mode (and/or/xor masks) or quad-perm mode | Goes through the LDS crossbar (needs `s_waitcnt lgkmcnt`) but uses no LDS memory | `__builtin_amdgcn_ds_swizzle(v, pattern)` | Butterflies across 16/32 lanes |
| **`ds_bpermute_b32` / `ds_permute_b32`** | **Arbitrary** gather (bpermute) or scatter (permute) across all 64 lanes; the address is `lane * 4` bytes | LDS-crossbar latency; no LDS allocation | `__builtin_amdgcn_ds_bpermute(addr, v)`. **`__shfl*` always lowers to this**, even for constant offsets (verified with `hipcc -O3 --offload-arch=gfx942`); the compiler does not turn constant xor patterns into DPP | General shuffles |
| **`v_readlane_b32` / `v_readfirstlane_b32`** (and `v_writelane`) | One lane's VGPR value to an **SGPR** (wave-uniform) | Cheap, but serializes when used in a loop | `__builtin_amdgcn_readlane(v, lane)`, `__builtin_amdgcn_readfirstlane(v)` | Broadcasts, final reduction value, making a value provably uniform |

RDNA (gfx10+) changes the DPP set: `row_bcast`/`wave_*` are gone and `v_permlane16_b32`/`v_permlanex16_b32` are added. Hand-written DPP code is therefore architecture-specific.

Complete program comparing the portable shuffle with hand-written cross-lane code, plus a wave-aggregated atomic. It needs a wave64 CDNA GPU:

```cpp
// Three ways to reduce across a 64-lane CDNA wavefront, plus a wave-aggregated
// atomic that uses 64-bit ballot masks. Build for CDNA (wave64), e.g.:
//   hipcc -O3 --offload-arch=gfx942 wave_ops.cpp -o wave_ops
#include <hip/hip_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <vector>

#define HIP_CHECK(cmd) do { hipError_t e = (cmd); if (e != hipSuccess) { \
    std::fprintf(stderr, "HIP %s:%d: %s\n", __FILE__, __LINE__, hipGetErrorString(e)); \
    std::exit(1); } } while (0)

// (a) Portable: HIP's __shfl_xor always lowers to ds_bpermute_b32, even for
//     constant offsets (no automatic DPP). Works for any warpSize.
__device__ int wave_sum_shfl(int v) {
    for (int off = warpSize / 2; off > 0; off >>= 1) v += __shfl_xor(v, off);
    return v;
}

// (b) Hand-written AMDGCN cross-lane ops (gfx9/CDNA, wave64 only).
__device__ int wave_sum_dpp(int v) {
    // DPP: a VALU operand modifier; lanes move only within a 16-lane row.
    // update_dpp(old, src, dpp_ctrl, row_mask, bank_mask, bound_ctrl)
    v += __builtin_amdgcn_update_dpp(0, v, 0xB1, 0xF, 0xF, false);  // quad_perm[1,0,3,2]: lane^1
    v += __builtin_amdgcn_update_dpp(0, v, 0x4E, 0xF, 0xF, false);  // quad_perm[2,3,0,1]: lane^2
    v += __builtin_amdgcn_update_dpp(0, v, 0x124, 0xF, 0xF, false); // row_ror:4
    v += __builtin_amdgcn_update_dpp(0, v, 0x128, 0xF, 0xF, false); // row_ror:8 -> row (16) sum
    // ds_swizzle (bit-mask mode) works within 32-lane halves:
    // offset = and_mask | or_mask << 5 | xor_mask << 10 -> 0x401F = lane ^ 16
    v += __builtin_amdgcn_ds_swizzle(v, 0x401F);                    // 32-lane sum
    // ds_bpermute: arbitrary gather across the whole wave; address is lane*4 bytes.
    int src_lane = static_cast<int>(__lane_id()) ^ 32;
    v += __builtin_amdgcn_ds_bpermute(src_lane << 2, v);            // 64-lane sum
    return v;
}

// (c) Uniform result straight into a scalar register via v_readlane.
__device__ int wave_sum_readlane(int row_sum_in_every_lane_of_row) {
    int v = row_sum_in_every_lane_of_row;
    return __builtin_amdgcn_readlane(v, 0) + __builtin_amdgcn_readlane(v, 16) +
           __builtin_amdgcn_readlane(v, 32) + __builtin_amdgcn_readlane(v, 48);
}

__global__ void reduce_kernel(const int* in, int* out_shfl, int* out_dpp, int* out_rl) {
    int v = in[blockIdx.x * blockDim.x + threadIdx.x];
    int a = wave_sum_shfl(v);
    int b = wave_sum_dpp(v);
    // row sums only (first four DPP steps), then readlane across the 4 rows
    int r = v;
    r += __builtin_amdgcn_update_dpp(0, r, 0xB1, 0xF, 0xF, false);
    r += __builtin_amdgcn_update_dpp(0, r, 0x4E, 0xF, 0xF, false);
    r += __builtin_amdgcn_update_dpp(0, r, 0x124, 0xF, 0xF, false);
    r += __builtin_amdgcn_update_dpp(0, r, 0x128, 0xF, 0xF, false);
    int c = wave_sum_readlane(r);
    if (__lane_id() == 0) {
        int w = (blockIdx.x * blockDim.x + threadIdx.x) / warpSize;
        out_shfl[w] = a; out_dpp[w] = b; out_rl[w] = c;
    }
}

// Wave-aggregated append: one atomic per wave instead of one per lane.
__global__ void compact_positive(const int* in, int n, int* out, int* counter) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    bool keep = (i < n) && in[i] > 0;
    unsigned long long mask = __ballot(keep);          // 64 bits on wave64!
    if (mask == 0) return;
    unsigned lane = __lane_id();
    int leader = __ffsll(static_cast<unsigned long long>(mask)) - 1;
    // Pitfall: (1u << lane) is undefined for lane >= 32. Use a 64-bit literal.
    unsigned long long lanes_below = (1ull << lane) - 1;   // lanes 0..lane-1
    int rank = __popcll(mask & lanes_below);
    int base = 0;
    if (static_cast<int>(lane) == leader) base = atomicAdd(counter, __popcll(mask));
    base = __shfl(base, leader);
    if (keep) out[base + rank] = in[i];
}

int main() {
    hipDeviceProp_t prop;
    HIP_CHECK(hipGetDeviceProperties(&prop, 0));
    if (prop.warpSize != 64) { std::printf("needs a wave64 (CDNA) GPU\n"); return 0; }

    const int n = 1 << 16, threads = 256, blocks = n / threads, waves = n / 64;
    std::vector<int> h(n);
    for (int i = 0; i < n; ++i) h[i] = (i % 7) - 3;    // mix of +, 0, -
    int *d_in, *d_a, *d_b, *d_c, *d_out, *d_cnt;
    HIP_CHECK(hipMalloc(&d_in, n * sizeof(int)));
    HIP_CHECK(hipMalloc(&d_a, waves * sizeof(int)));
    HIP_CHECK(hipMalloc(&d_b, waves * sizeof(int)));
    HIP_CHECK(hipMalloc(&d_c, waves * sizeof(int)));
    HIP_CHECK(hipMalloc(&d_out, n * sizeof(int)));
    HIP_CHECK(hipMalloc(&d_cnt, sizeof(int)));
    HIP_CHECK(hipMemcpy(d_in, h.data(), n * sizeof(int), hipMemcpyHostToDevice));
    HIP_CHECK(hipMemset(d_cnt, 0, sizeof(int)));

    reduce_kernel<<<blocks, threads>>>(d_in, d_a, d_b, d_c);
    compact_positive<<<blocks, threads>>>(d_in, n, d_out, d_cnt);
    HIP_CHECK(hipDeviceSynchronize());

    std::vector<int> a(waves), b(waves), c(waves);
    int cnt = 0;
    HIP_CHECK(hipMemcpy(a.data(), d_a, waves * sizeof(int), hipMemcpyDeviceToHost));
    HIP_CHECK(hipMemcpy(b.data(), d_b, waves * sizeof(int), hipMemcpyDeviceToHost));
    HIP_CHECK(hipMemcpy(c.data(), d_c, waves * sizeof(int), hipMemcpyDeviceToHost));
    HIP_CHECK(hipMemcpy(&cnt, d_cnt, sizeof(int), hipMemcpyDeviceToHost));

    int bad = 0, expect_cnt = 0;
    for (int w = 0; w < waves; ++w) {
        int ref = 0;
        for (int l = 0; l < 64; ++l) ref += h[w * 64 + l];
        bad += (a[w] != ref) + (b[w] != ref) + (c[w] != ref);
    }
    for (int x : h) expect_cnt += x > 0;
    std::printf("reductions mismatches=%d, compacted=%d (expected %d)\n", bad, cnt, expect_cnt);
    HIP_CHECK(hipFree(d_in)); HIP_CHECK(hipFree(d_a)); HIP_CHECK(hipFree(d_b));
    HIP_CHECK(hipFree(d_c)); HIP_CHECK(hipFree(d_out)); HIP_CHECK(hipFree(d_cnt));
    return (bad == 0 && cnt == expect_cnt) ? 0 : 1;
}
```

```text
$ hipcc -O3 wave_ops.cpp -o wave_ops && ./wave_ops
reductions mismatches=0, compacted=28086 (expected 28086)
```

Compiling with `--save-temps --offload-arch=gfx942` and grepping the `.s` file shows the instruction mapping (excerpt; the DPP steps the two reductions share were merged by the compiler):

```text
v_add_u32_dpp v1, v1, v1 quad_perm:[1,0,3,2] row_mask:0xf bank_mask:0xf bound_ctrl:1   ; lane ^ 1
v_add_u32_dpp v1, v1, v1 quad_perm:[2,3,0,1] row_mask:0xf bank_mask:0xf bound_ctrl:1   ; lane ^ 2
v_add_u32_dpp v1, v1, v1 row_ror:4 row_mask:0xf bank_mask:0xf bound_ctrl:1
v_add_u32_dpp v7, v1, v1 row_ror:8 row_mask:0xf bank_mask:0xf bound_ctrl:1             ; 16-lane row sum
ds_swizzle_b32 v1, v7 offset:swizzle(SWAP,16)                                          ; lane ^ 16
ds_bpermute_b32 v4, v6, v3                                                             ; __shfl_xor, lane ^ 32
v_readlane_b32 s1, v7, 16                                                              ; VGPR lane 16 -> SGPR
```

Practical advice: use `__shfl_*` or, better, rocPRIM/hipCUB warp primitives ([36.8](#368-hipcub-and-rocprim-block-warp-and-device-primitives)), which already pick DPP sequences per architecture. Hand-write DPP only when a profile shows that the LDS-pipe shuffles (`ds_bpermute`) are the bottleneck, and guard the code by architecture.

## 36.7 Porting Warp32 Code to Wave64: Ballot Masks and Other Traps

| CUDA (warp32) idiom | What breaks on wave64 | Fix |
|---|---|---|
| `unsigned m = __ballot_sync(0xffffffff, p);` | The ballot is 64 bits on AMD; storing it in 32 bits silently drops lanes 32-63 | `unsigned long long` / `uint64_t`. HIP's `__ballot` returns 64 bits |
| `__popc(m)`, `__ffs(m)` | Count or search only the low 32 bits | `__popcll(m)`, `__ffsll(m)` |
| `1u << lane`, lanemask `(1u << lane) - 1` | **Undefined behavior** for lane ≥ 32 | `1ull << lane`, `(1ull << lane) - 1` |
| Full mask `0xffffffff` in `__shfl_sync` | HIP's `_sync` builtins `static_assert` that the mask is 64-bit, so a 32-bit literal fails to compile. A cast mask means "lanes 0-31 only" | `0xffffffffffffffffull` or `__activemask()`. On ROCm 6.2-6.4 these builtins are opt-in: define `HIP_ENABLE_WARP_SYNC_BUILTINS` before including any HIP header, otherwise a hipified `__shfl_sync` fails as an undeclared identifier rather than on the mask `static_assert`. From 7.0 they are on by default (disable with `HIP_DISABLE_WARP_SYNC_BUILTINS`) |
| `lane = threadIdx.x & 31`, `warp = threadIdx.x >> 5` | Wrong lane and wave ids | `__lane_id()`, `threadIdx.x / warpSize` |
| Shuffle reduction with offsets 16, 8, 4, 2, 1 | Reduces only 32 lanes, leaving two partial sums per wave | Start at `warpSize / 2` |
| `__shared__ float partial[32]` sized "blockDim / 32" | Wrong index math if the code assumes 32 lanes | Size by `blockDim / 32` (an upper bound for both), index by `threadIdx.x / warpSize` |
| `#define WARP_SIZE 32`, or `warpSize` used as a compile-time constant | Wrong on CDNA. **In ROCm 7.0 `warpSize` is no longer `constexpr`**, and `__AMDGCN_WAVEFRONT_SIZE` is deprecated | Use runtime `warpSize` in device code. For compile-time needs, use a per-target macro (CDNA/gfx9 is wave64) or `rocprim::arch::wavefront::min_size()/max_size()` |
| `#ifdef __HIP_PLATFORM_AMD__ -> 64` | Wrong on RDNA, which is wave32 by default | Branch on the architecture (gfx9 vs gfx10+), not the platform |
| Relying on implicit warp-synchronous execution | Works by accident; the compiler may still reorder memory operations | Use explicit primitives. `__syncwarp()` is available by default starting with ROCm 7.0. It belongs to the same warp-sync builtin set, so `HIP_DISABLE_WARP_SYNC_BUILTINS` removes it too. A leftover shim such as `#define __syncwarp __syncthreads` clashes with it on 7.0+ |

The `compact_positive` kernel in 36.6 shows the correct 64-bit pattern: ballot into a 64-bit mask, compute the leader with `__ffsll`, compute this lane's rank with `__popcll(mask & ((1ull << lane) - 1))`, issue one `atomicAdd` per wave, and broadcast the base with `__shfl`. With `1u << lane`, lanes 32-63 compute garbage ranks and the output gets holes and overlapping writes.

## 36.8 hipCUB and rocPRIM: Block, Warp, and Device Primitives

- **rocPRIM** is AMD's native, header-only HIP primitives library. It is tuned per architecture and uses DPP and `ds_bpermute` internally.
- **hipCUB** is a thin wrapper with the CUB API. On AMD it calls rocPRIM; on NVIDIA it calls CUB. Code written against hipCUB therefore runs on both.
- **rocThrust** builds on rocPRIM.

| Level | Examples | Scratch |
|---|---|---|
| Warp | `WarpReduce`, `WarpScan`, `WarpExchange` (logical warp size: a power of two up to the hardware wave) | `TempStorage` in LDS |
| Block | `BlockLoad`/`BlockStore` (direct, striped, warp-transpose), `BlockReduce`, `BlockScan`, `BlockRadixSort`, `BlockExchange`, `BlockHistogram` | `TempStorage` in LDS; reuse it through a `union` plus `__syncthreads()` |
| Device | `DeviceReduce`, `DeviceScan`, `DeviceRadixSort`, `DeviceSelect`, `DeviceSegmentedReduce`, `DeviceHistogram` | Two-phase: call once with `nullptr` to get `temp_bytes`, allocate, call again |

```cpp
// Block-, warp-, and device-level primitives from hipCUB (CUB API on rocPRIM).
// Build: hipcc -O3 hipcub_demo.cpp -o hipcub_demo
#include <hip/hip_runtime.h>
#include <hipcub/hipcub.hpp>
#include <cstdio>
#include <cstdlib>
#include <vector>

#define HIP_CHECK(cmd) do { hipError_t e = (cmd); if (e != hipSuccess) { \
    std::fprintf(stderr, "HIP %s:%d: %s\n", __FILE__, __LINE__, hipGetErrorString(e)); \
    std::exit(1); } } while (0)

constexpr int BLOCK = 256;
constexpr int ITEMS = 4;                     // items per thread (ILP, fewer blocks)
constexpr int LOGICAL_WARP = 16;             // sub-wave groups; must divide the HW wave

// Block-wide sum of BLOCK*ITEMS elements; one partial per block.
__global__ void block_sum(const int* in, int* partials, int n) {
    using BlockLoad   = hipcub::BlockLoad<int, BLOCK, ITEMS, hipcub::BLOCK_LOAD_WARP_TRANSPOSE>;
    using BlockReduce = hipcub::BlockReduce<int, BLOCK>;
    __shared__ union {                       // reuse LDS between the two phases
        typename BlockLoad::TempStorage load;
        typename BlockReduce::TempStorage reduce;
    } tmp;
    int items[ITEMS];
    int base = blockIdx.x * BLOCK * ITEMS;
    BlockLoad(tmp.load).Load(in + base, items, n - base, 0);   // guarded, coalesced
    __syncthreads();                                           // LDS reuse barrier
    int s = BlockReduce(tmp.reduce).Sum(items);                // valid in thread 0 only
    if (threadIdx.x == 0) partials[blockIdx.x] = s;
}

// Segmented sums of 16 consecutive values with a logical-warp reduction.
__global__ void sum_groups_of_16(const int* in, int* out) {
    using WarpReduce = hipcub::WarpReduce<int, LOGICAL_WARP>;
    __shared__ typename WarpReduce::TempStorage tmp[BLOCK / LOGICAL_WARP];
    int gid = blockIdx.x * BLOCK + threadIdx.x;
    int group = threadIdx.x / LOGICAL_WARP;
    int s = WarpReduce(tmp[group]).Sum(in[gid]);               // valid in lane 0 of group
    if (threadIdx.x % LOGICAL_WARP == 0) out[gid / LOGICAL_WARP] = s;
}

int main() {
    const int n = 1 << 20;
    std::vector<int> h(n);
    long long ref = 0;
    for (int i = 0; i < n; ++i) { h[i] = i % 13; ref += h[i]; }

    int *d_in, *d_part, *d_groups, *d_total;
    const int nblocks = (n + BLOCK * ITEMS - 1) / (BLOCK * ITEMS);
    HIP_CHECK(hipMalloc(&d_in, n * sizeof(int)));
    HIP_CHECK(hipMalloc(&d_part, nblocks * sizeof(int)));
    HIP_CHECK(hipMalloc(&d_groups, (n / LOGICAL_WARP) * sizeof(int)));
    HIP_CHECK(hipMalloc(&d_total, sizeof(int)));
    HIP_CHECK(hipMemcpy(d_in, h.data(), n * sizeof(int), hipMemcpyHostToDevice));

    block_sum<<<nblocks, BLOCK>>>(d_in, d_part, n);
    sum_groups_of_16<<<n / BLOCK, BLOCK>>>(d_in, d_groups);

    // Device-wide reduce: call once with nullptr to size the scratch, then run.
    void* d_temp = nullptr;
    size_t temp_bytes = 0;
    HIP_CHECK(hipcub::DeviceReduce::Sum(d_temp, temp_bytes, d_part, d_total, nblocks));
    HIP_CHECK(hipMalloc(&d_temp, temp_bytes));
    HIP_CHECK(hipcub::DeviceReduce::Sum(d_temp, temp_bytes, d_part, d_total, nblocks));
    HIP_CHECK(hipDeviceSynchronize());

    int total = 0, g0 = 0;
    HIP_CHECK(hipMemcpy(&total, d_total, sizeof(int), hipMemcpyDeviceToHost));
    HIP_CHECK(hipMemcpy(&g0, d_groups, sizeof(int), hipMemcpyDeviceToHost));
    int g0_ref = 0;
    for (int i = 0; i < LOGICAL_WARP; ++i) g0_ref += h[i];
    std::printf("total=%d ref=%lld  group0=%d ref=%d\n", total, ref, g0, g0_ref);

    HIP_CHECK(hipFree(d_temp)); HIP_CHECK(hipFree(d_in)); HIP_CHECK(hipFree(d_part));
    HIP_CHECK(hipFree(d_groups)); HIP_CHECK(hipFree(d_total));
    return (total == ref && g0 == g0_ref) ? 0 : 1;
}
```

```text
$ hipcc -O3 hipcub_demo.cpp -o hipcub_demo && ./hipcub_demo
total=6291438 ref=6291438  group0=81 ref=81
```

The native rocPRIM spelling of the block reduction:

```cpp
// fragment: rocPRIM's native block reduction (default operator: rocprim::plus)
#include <rocprim/rocprim.hpp>
using block_reduce = rocprim::block_reduce<int, 256>;
__shared__ typename block_reduce::storage_type storage;
int block_total;
block_reduce().reduce(thread_value, block_total, storage);   // valid in thread 0
```

Gotchas:
- Block and warp reductions return the result **only in thread/lane 0**. Use `BlockReduce(...).Sum()` followed by a broadcast through shared memory if every thread needs it, or use `BlockScan`, which gives every thread a result.
- Reusing `TempStorage` for two collectives needs a `__syncthreads()` between them.
- The block size is a template parameter and must match the launch.
- Device-level calls are asynchronous on the given stream (default: the null stream), and their temporary storage must stay alive until the call completes.

## 36.9 Interview Questions -- Portability and Wave-Level Programming

**Q1.** You are starting a new physics code that must run on Frontier (AMD), Aurora (Intel), and an NVIDIA cluster for 10+ years. HIP, SYCL, or Kokkos?

For a large application maintained over a long time, a portability layer such as Kokkos (or RAJA) is usually the best default:
- It hides the vendor API and the data layout (`View` layouts give coalescing on GPU and cache-friendly order on CPU).
- It has production backends for all three vendors (HIP, SYCL, CUDA) and is maintained by a national-lab community.
- Native kernels can still be dropped in for hotspots.

SYCL is reasonable if Intel is the primary system and the team wants an ISO-C++-style standard, but backend maturity on AMD/NVIDIA varies by implementation. Plain HIP covers AMD + NVIDIA well but not Intel. Name the trade-offs: an extra dependency and abstraction overhead (usually small) against the cost of porting three times.

**Q2.** What does `__shfl_xor(v, 1)` compile to on MI300X, and how could it be cheaper?

By default HIP's shuffles lower to `ds_bpermute_b32`. That instruction routes the value through the LDS crossbar with an address of `lane * 4`, costs LDS-pipe latency, and needs `s_waitcnt lgkmcnt`. A fixed xor-1 pattern can instead be a DPP `quad_perm:[1,0,3,2]` modifier on the add instruction itself, which costs essentially nothing extra. The compiler does **not** make this transformation for you: `__shfl_xor` is implemented as a computed-index `__builtin_amdgcn_ds_bpermute`, so even `__shfl_xor(v, 1)` with a constant offset stays a `ds_bpermute_b32` at `-O3` (you can confirm this with `--save-temps`). To get DPP, use rocPRIM/hipCUB warp primitives, which emit DPP sequences explicitly, or the `__builtin_amdgcn_update_dpp` / `__builtin_amdgcn_mov_dpp` builtins. Patterns that cross 16-lane rows need `row_bcast`, `ds_swizzle` (within 32 lanes), `ds_bpermute`, or `readlane`.

**Q3.** A CUDA warp-aggregated atomic gives wrong counts after hipify on MI250X. What do you look for?

Look for 32-bit assumptions:
- An `unsigned` ballot result, which drops lanes 32-63.
- `__popc`/`__ffs` instead of `__popcll`/`__ffsll`.
- `1u << lane` in the lane mask, which is undefined for lane ≥ 32.
- `threadIdx.x & 31` for the lane id.
- A `0xffffffff` mask.
- Shuffle loops that start at offset 16.

Fix all of them with 64-bit types and `warpSize`-relative code, and test on both wave32 and wave64 targets. Check `hipDeviceProp_t::warpSize` at run time.

**Q4.** ROCm 7 made `warpSize` non-constexpr. How do you size a per-wave shared array?

Size it for the worst case: `blockDim / 32` entries is an upper bound for both wave32 and wave64, or use a template parameter for the block size and divide by the minimum wave size. Where a real compile-time wave size is needed, use a per-architecture macro (wave64 on gfx9/CDNA) or rocPRIM's `arch::wavefront::min_size()`/`max_size()`, and keep run-time logic on `warpSize`. Do not assume that `__HIP_PLATFORM_AMD__` implies 64.

**Q5.** Why would Kokkos store a 2-D array column-major on the GPU but row-major on the CPU?

The parallel loop index is usually the first index `i`. On a GPU, consecutive threads have consecutive `i`, so `LayoutLeft` (i is the fastest-varying index) makes a wave's loads contiguous, which means coalesced transactions. On a CPU, each thread handles one `i` and loops over `j`, so `LayoutRight` (j fastest) gives each thread a contiguous stream for its caches and SIMD units. Kokkos picks the default layout per memory space, so the same source gets the right pattern on both.

**Q6.** When is hand-written DPP worth it instead of rocPRIM?

Rarely. It can be worth it when a profile (instruction mix, LDS-pipe utilization in `rocprof-compute`) shows that cross-lane traffic in a hot inner loop dominates, the pattern is fixed, the target architectures are known, and you can maintain separate paths for gfx9 (CDNA) and gfx10+ (RDNA) DPP semantics. Otherwise rocPRIM's warp primitives already use tuned DPP sequences and stay correct across wave sizes.

**Q7.** Map a CUDA programmer's vocabulary to OpenCL and SYCL.

- thread / block / grid = work-item / work-group / NDRange (SYCL: `nd_item` within an `nd_range`).
- warp = sub-group.
- shared memory = local memory (`__local`, or a SYCL `local_accessor`).
- `__syncthreads()` = `barrier(CLK_LOCAL_MEM_FENCE)` or `sycl::group_barrier(g)`.
- stream = command queue.
- `cudaMalloc` = `clCreateBuffer` / `sycl::malloc_device`.

AMD's own terminology (workgroup, NDRange, LDS) comes from this OpenCL lineage.
