# Parallel and GPU Programming -- Comprehensive Reference

> A deep-dive reference covering MPI, OpenMP, CUDA, and HIP programming for high-performance computing. Each section includes conceptual explanations, comparison tables, code examples, and common interview questions with detailed answers. Complements the *C++ Fundamentals*, *CS Fundamentals*, *DSA Fundamentals*, and *LeetCode Patterns* guides.

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

---

# 23. Performance Optimization

---

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
- **rocprof, Omniperf, Omnitrace**: Profiling tools

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

// Compile-time check
#ifdef __HIP_PLATFORM_AMD__
    #define WARP_SIZE 64
#else
    #define WARP_SIZE 32
#endif
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
| `__shfl_sync` mask | `0xFFFFFFFF` (32 bits) | 64-bit wavefront needs `0xFFFFFFFFFFFFFFFF` | Use HIP's mask-free shuffle |
| Warp ballot | Returns `unsigned int` (32 bits) | Returns `unsigned long long` (64 bits) | Use appropriate type |
| Register pressure | ~255 regs/thread | VGPRs differ per arch | Profile with `rocprof` |
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
# Check VGPR/SGPR usage with rocprof
rocprof --stats kernel_app
# Look for vgpr_count and sgpr_count in the output

# Or use --hsa-trace for detailed kernel info
rocprof --hsa-trace ./my_app
```

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

| Tool | Purpose | Usage |
|---|---|---|
| **rocprof** | Kernel profiling (counters, traces) | `rocprof --stats ./app` |
| **Omniperf** | Comprehensive GPU profiling (roofline, memory, compute) | `omniperf profile -n name -- ./app` |
| **Omnitrace** | System-wide tracing (CPU+GPU timeline) | `omnitrace-instrument -- ./app` |
| **rocm-smi** | GPU monitoring (temp, utilization, clocks) | `rocm-smi --showuse` |
| **roc-obj-ls** | List GPU objects in binary | `roc-obj-ls binary` |

### Using rocprof

```bash
# Basic kernel statistics (time, occupancy)
rocprof --stats ./my_app

# Hardware counters
echo "pmc: SQ_WAVES SQ_INSTS_VALU SQ_INSTS_SMEM" > counters.txt
rocprof -i counters.txt ./my_app

# Application trace (timeline)
rocprof --hip-trace ./my_app
rocprof --hsa-trace ./my_app
```

### Using Omniperf

```bash
# Profile
omniperf profile -n my_profile -- ./my_app

# Analyze (launches web-based GUI)
omniperf analyze -p workloads/my_profile/

# Key metrics to examine:
# - Roofline analysis (compute vs memory bound)
# - Memory chart (L1/L2/HBM utilization)
# - Instruction mix (VALU, SALU, VMEM, LDS)
# - Occupancy and limiting factors
```

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
| Profiler | Nsight Compute/Systems | Omniperf / Omnitrace / rocprof |
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

`rocprof` is the low-level command-line profiler for kernel timing, hardware counter collection, and basic tracing. `Omniperf` provides comprehensive analysis including roofline plots, memory charts, instruction mix breakdowns, and occupancy analysis -- use it for deep performance investigation. `Omnitrace` provides system-wide tracing (like Nsight Systems) showing CPU-GPU interaction timelines, MPI communication, and I/O. Use `rocm-smi` for real-time GPU monitoring (temperature, utilization, clock speeds).

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
