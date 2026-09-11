# CS Fundamentals -- Comprehensive Interview Reference

> An interview-focused reference covering essential Computer Science topics beyond data structures and algorithms. Each section includes key concepts, quick-reference tables, and common interview questions with detailed answers. Complements the *DSA Fundamentals* and *LeetCode Patterns* guides.

---

## Table of Contents

1. [Operating Systems](#1-operating-systems)
2. [Computer Networks](#2-computer-networks)
3. [Database Systems](#3-database-systems)
4. [Object-Oriented Programming and Design Patterns](#4-object-oriented-programming-and-design-patterns)
5. [System Design](#5-system-design)
6. [Concurrency and Multithreading](#6-concurrency-and-multithreading)
7. [Computer Architecture](#7-computer-architecture)
8. [Distributed Systems](#8-distributed-systems)
9. [Security](#9-security)

---

# 1. Operating Systems

---

## 1.1 Processes and Threads

### Processes

A **process** is an instance of a program in execution. The OS maintains a **Process Control Block (PCB)** for each process containing:

| PCB Field | Description |
|---|---|
| Process ID (PID) | Unique integer identifier |
| Process State | New, Ready, Running, Waiting, Terminated |
| Program Counter | Address of the next instruction to execute |
| CPU Registers | Saved register values for context switching |
| Memory Info | Page tables, segment tables, base/limit registers |
| I/O Status | List of open files, allocated I/O devices |
| Scheduling Info | Priority, scheduling queue pointers, CPU time used |

**Process states and transitions:**

```
                  ┌──────────────────────┐
                  │                      │
    ┌─────┐   admitted   ┌───────┐  scheduler   ┌─────────┐
    │ New │──────────────▶│ Ready │─────────────▶│ Running │
    └─────┘               └───────┘              └─────────┘
                              ▲                    │     │
                              │   I/O or event     │     │  exit
                              │   completion       │     │
                          ┌─────────┐              │  ┌────────────┐
                          │ Waiting │◀─────────────┘  │ Terminated │
                          └─────────┘  I/O or event   └────────────┘
                                         wait
```

### Threads

A **thread** (lightweight process) is the smallest unit of CPU execution. Threads within the same process share the code section, data section, heap, and open files, but each has its own:

- Thread ID
- Program counter
- Register set
- Stack

### Process vs Thread Comparison

| Aspect | Process | Thread |
|---|---|---|
| Memory | Separate address space | Shared address space within process |
| Creation cost | High (fork + copy page tables) | Low (share existing address space) |
| Context switch cost | Expensive (flush TLB, swap page tables) | Cheap (same address space, swap registers + stack) |
| Communication | IPC required (pipes, sockets, shared memory) | Direct shared memory access |
| Isolation | Full isolation; crash in one does not affect others | No isolation; a crash kills all threads in the process |
| Overhead | Higher memory overhead | Lower memory overhead |

### User-Level vs Kernel-Level Threads

| Aspect | User-Level Threads | Kernel-Level Threads |
|---|---|---|
| Management | Thread library in user space | OS kernel |
| Context switch | Fast (no kernel involvement) | Slower (kernel trap required) |
| Scheduling | Application-controlled | OS scheduler |
| Blocking | One thread blocks → all threads block (many-to-one) | Only the blocking thread is suspended |
| Multicore utilization | Cannot run on multiple cores (many-to-one) | Can run on multiple cores |

**Threading models:** Many-to-One, One-to-One (Linux, Windows), Many-to-Many (Solaris).

---

## 1.2 CPU Scheduling

The **CPU scheduler** selects a process from the ready queue and allocates the CPU to it. Scheduling decisions occur when a process:

1. Switches from running to waiting (I/O request) -- *non-preemptive*
2. Switches from running to ready (interrupt) -- *preemptive*
3. Switches from waiting to ready (I/O completion) -- *preemptive*
4. Terminates -- *non-preemptive*

### Scheduling Criteria

| Metric | Goal |
|---|---|
| **CPU Utilization** | Keep the CPU as busy as possible (target 40-90%) |
| **Throughput** | Maximize processes completed per time unit |
| **Turnaround Time** | Minimize total time from submission to completion |
| **Waiting Time** | Minimize time spent in the ready queue |
| **Response Time** | Minimize time from submission to first response (interactive systems) |

### Scheduling Algorithms

| Algorithm | Type | Description | Pros | Cons |
|---|---|---|---|---|
| **FCFS** | Non-preemptive | First-Come, First-Served | Simple, fair | Convoy effect: short jobs wait behind long ones |
| **SJF** | Non-preemptive | Shortest Job First | Optimal average waiting time | Requires knowing burst time; starvation of long jobs |
| **SRTF** | Preemptive | Shortest Remaining Time First (preemptive SJF) | Better avg waiting time than SJF | Starvation; high overhead |
| **Round Robin** | Preemptive | Fixed time quantum, rotate | Fair, good response time | High context-switch overhead if quantum too small |
| **Priority** | Either | Higher-priority jobs first | Supports urgency levels | Starvation (solved with **aging**) |
| **MLFQ** | Preemptive | Multiple queues with different priorities and quanta | Adapts to job behavior | Complex to tune |

**Round Robin time quantum tradeoff:**
- Too small → excessive context switching overhead
- Too large → degrades to FCFS
- Rule of thumb: 80% of CPU bursts should be shorter than the quantum

**Multilevel Feedback Queue (MLFQ) rules:**
1. If Priority(A) > Priority(B), A runs.
2. If Priority(A) = Priority(B), run in Round Robin.
3. New jobs start at the highest priority.
4. If a job uses its entire time slice, move it down one level.
5. If a job gives up the CPU before the time slice expires, it stays at the same level.
6. Periodically boost all jobs to the highest priority (prevents starvation).

---

## 1.3 Memory Management

### Contiguous Allocation

The simplest scheme: each process gets a contiguous block of memory. Suffers from **external fragmentation** (free memory scattered in small chunks). Mitigated by **compaction** (expensive).

### Paging

Divides physical memory into fixed-size **frames** and logical memory into same-size **pages** (typically 4 KB). A **page table** maps each page to a frame.

```
Logical Address:  [ Page Number | Page Offset ]
                       ↓
                  Page Table
                       ↓
Physical Address: [ Frame Number | Page Offset ]
```

- Eliminates external fragmentation
- Introduces internal fragmentation (last page may not be full, wastes up to page_size - 1 bytes)
- Page table itself can be large → use **multi-level page tables** or **inverted page tables**

### Translation Lookaside Buffer (TLB)

A small, fast hardware cache of recent page-table entries. Without TLB, every memory access requires two memory accesses (page table + actual data). TLB hit rates of 99%+ are typical.

**Effective Access Time (EAT):**

```
EAT = hit_rate × (TLB_access + memory_access) + (1 - hit_rate) × (TLB_access + 2 × memory_access)
```

### Virtual Memory and Demand Paging

Not all pages need to be in physical memory at once. Pages are loaded on demand (when a **page fault** occurs). The OS keeps a **valid/invalid bit** in each page-table entry.

**Page fault handling:**
1. CPU generates a page fault trap to the OS
2. OS checks if the reference is valid; if not, terminate the process
3. Find a free frame (or evict one using a replacement algorithm)
4. Schedule a disk read to bring the page into the frame
5. Update the page table entry
6. Restart the instruction that caused the page fault

### Page Replacement Algorithms

| Algorithm | Description | Optimal? | Notes |
|---|---|---|---|
| **FIFO** | Replace the oldest page | No | Simple; suffers from Belady's anomaly |
| **Optimal (OPT)** | Replace the page that will not be used for the longest time | Yes | Not implementable (requires future knowledge); used as benchmark |
| **LRU** | Replace the least recently used page | No (but good) | Good approximation of OPT; expensive to implement exactly |
| **Clock (Second Chance)** | FIFO with a reference bit; skip pages with bit=1, clear bit | No | Practical approximation of LRU |
| **LFU** | Replace the least frequently used page | No | Counts accesses; can keep stale popular pages |

**Belady's Anomaly:** With FIFO, increasing the number of frames can paradoxically increase page faults. LRU and OPT are immune (they are **stack algorithms**).

**Thrashing:** When a process does not have enough frames, it spends more time paging than executing. The working-set model prevents thrashing by tracking the set of pages a process actively uses.

### Segmentation

Divides memory into variable-size **segments** corresponding to logical units (code, stack, heap, data). Each segment has a base address and a limit. Supports the programmer's view of memory but suffers from external fragmentation.

Modern systems use **segmentation with paging** (e.g., x86 historically) or pure paging (most modern 64-bit OSes).

---

## 1.4 Deadlocks

A **deadlock** occurs when a set of processes are each waiting for a resource held by another process in the set, forming a circular wait.

### Coffman Conditions (all four must hold simultaneously)

| Condition | Description |
|---|---|
| **Mutual Exclusion** | At least one resource is held in a non-sharable mode |
| **Hold and Wait** | A process holds at least one resource while waiting for additional resources |
| **No Preemption** | Resources cannot be forcibly taken from a process |
| **Circular Wait** | A circular chain of processes exists where each waits for a resource held by the next |

### Handling Strategies

| Strategy | Approach | Example |
|---|---|---|
| **Prevention** | Ensure at least one Coffman condition cannot hold | Impose total ordering on resources (breaks circular wait) |
| **Avoidance** | Dynamically check if granting a request is safe | Banker's Algorithm |
| **Detection + Recovery** | Allow deadlocks, detect them, then recover | Resource-allocation graph; kill processes or preempt resources |
| **Ignore** | Assume deadlocks are rare enough to not handle | The "Ostrich Algorithm" (used by most general-purpose OSes) |

### Banker's Algorithm (Avoidance)

Maintains matrices of **Available**, **Max**, **Allocation**, and **Need** (Need = Max - Allocation). Before granting a request, the algorithm checks if the resulting state is **safe** -- meaning there exists at least one sequence of process completions that allows all processes to finish.

A state is **safe** if for every process P_i, the resources P_i still needs can be satisfied by the currently available resources plus resources held by all P_j with j < i in the safe sequence.

---

## 1.5 File Systems

### Key Concepts

| Concept | Description |
|---|---|
| **File** | A named collection of related data stored on secondary storage |
| **Directory** | A file that contains a list of (name, metadata pointer) entries |
| **inode** (Unix) | Data structure storing file metadata (permissions, size, timestamps, pointers to data blocks) |
| **Superblock** | Stores metadata about the filesystem itself (size, block size, free block count) |

### Allocation Methods

| Method | Description | Pros | Cons |
|---|---|---|---|
| **Contiguous** | Each file occupies contiguous blocks | Fast sequential and random access | External fragmentation; file size must be known |
| **Linked** | Each block contains a pointer to the next | No external fragmentation | Slow random access; pointer overhead; reliability issues |
| **Indexed (inode)** | An index block holds pointers to all data blocks | Good random access; no fragmentation | Index block overhead; limited by index block size (use multi-level) |

### Journaling

A **journal** (log) records intended changes before applying them to the filesystem. If the system crashes, the journal is replayed to restore consistency. Modes:

- **Write-ahead logging:** Log both metadata and data changes
- **Ordered mode (ext4 default):** Log metadata; ensure data is written before metadata commit
- **Writeback mode:** Log metadata only; fastest but data can be inconsistent after crash

---

## 1.6 Inter-Process Communication (IPC)

| Mechanism | Description | Use Case |
|---|---|---|
| **Pipe** | Unidirectional byte stream between related processes | Parent-child communication (`ls \| grep`) |
| **Named Pipe (FIFO)** | Like pipe but has a filesystem name; unrelated processes can use it | Communication between independent processes |
| **Message Queue** | Kernel-maintained queue of messages with types | Structured message passing with priority |
| **Shared Memory** | Region of memory mapped into multiple processes' address spaces | High-throughput data sharing (fastest IPC) |
| **Semaphore** | Integer counter for synchronization | Controlling concurrent access to shared resources |
| **Socket** | Bidirectional communication endpoint (local or networked) | Client-server communication, networked IPC |
| **Signal** | Asynchronous notification sent to a process | Interrupt handling (SIGINT, SIGKILL, SIGTERM) |
| **Memory-Mapped File** | File mapped into address space; changes reflected in file | Shared configuration, database engines |

---

## 1.7 System Calls

| System Call | Purpose | Example |
|---|---|---|
| `fork()` | Create a new process (child is a copy of parent) | Returns 0 in child, child PID in parent |
| `exec()` | Replace the current process image with a new program | `execvp("ls", args)` |
| `wait()` | Parent blocks until child terminates | Prevents zombie processes |
| `exit()` | Terminate the calling process | Frees resources, sends SIGCHLD to parent |
| `open()` / `close()` | Open / close a file descriptor | `int fd = open("file.txt", O_RDONLY)` |
| `read()` / `write()` | Read / write bytes from/to a file descriptor | `read(fd, buf, count)` |
| `mmap()` | Map a file or device into memory | Memory-mapped I/O, shared memory |
| `pipe()` | Create a unidirectional data channel | `int pipefd[2]; pipe(pipefd);` |
| `dup2()` | Duplicate a file descriptor to a specific number | Redirect stdin/stdout |
| `kill()` | Send a signal to a process | `kill(pid, SIGTERM)` |

**`fork()` + `exec()` pattern (Unix process creation):**

```
Parent calls fork()
├── Parent (fork returns child PID)
│   └── wait() for child
└── Child (fork returns 0)
    └── exec() replaces child with new program
        └── Program runs
            └── exit() → parent's wait() returns
```

---

## 1.8 I/O Systems

### I/O Methods

| Method | Description | CPU Involvement |
|---|---|---|
| **Programmed I/O (Polling)** | CPU repeatedly checks device status register | High (busy-waiting) |
| **Interrupt-Driven I/O** | Device interrupts CPU when ready | Medium (interrupt handling overhead) |
| **DMA (Direct Memory Access)** | DMA controller transfers data directly to/from memory | Low (CPU only sets up transfer and gets notified on completion) |

### Buffering

- **Single buffer:** OS assigns a kernel buffer for I/O; while device fills buffer, CPU processes previous buffer
- **Double buffer:** Two buffers alternate roles, overlapping I/O and computation
- **Circular buffer:** Ring of buffers for producer-consumer scenarios

---

## 1.9 Operating Systems -- Interview Questions

**Q1: What is the difference between a process and a thread?**

A process is an independent program in execution with its own address space, file descriptors, and system resources. A thread is a unit of execution within a process that shares the process's address space and resources. Creating a thread is cheaper than creating a process because there is no need to duplicate the address space. Context switching between threads of the same process is faster because the TLB and page tables do not need to be flushed. However, threads lack the isolation of processes -- a bug in one thread (e.g., writing to invalid memory) can crash all threads in the process.

**Q2: Explain context switching. Why is it expensive?**

A context switch saves the state (registers, program counter, stack pointer) of the currently running process/thread and loads the state of the next one. It is expensive because: (1) The direct cost of saving/restoring registers takes time. (2) For process switches, the TLB must be flushed since the new process has a different address space, causing TLB misses and extra memory accesses until the TLB warms up. (3) Cache pollution: the new process's data is unlikely to be in the CPU cache, causing cache misses. (4) Pipeline flush: the CPU pipeline must be flushed. Typical context switch times range from 1-10 microseconds on modern hardware, but the indirect costs (cold caches/TLBs) can make the effective cost much higher.

**Q3: What is a deadlock? How can you prevent it?**

A deadlock is a situation where two or more processes are blocked forever, each waiting for a resource held by another. It requires all four Coffman conditions to hold simultaneously: mutual exclusion, hold and wait, no preemption, and circular wait. Prevention strategies break at least one condition. The most practical approach is breaking circular wait by imposing a total ordering on resource types and requiring processes to request resources in increasing order. Another approach is breaking hold-and-wait by requiring a process to request all resources at once before execution.

**Q4: Explain virtual memory and demand paging.**

Virtual memory provides each process with an illusion of a large, contiguous address space, independent of physical RAM size. The OS and MMU (Memory Management Unit) translate virtual addresses to physical addresses using page tables. With demand paging, pages are only loaded into physical memory when first accessed. If a process accesses a page that is not in memory, a page fault occurs. The OS then fetches the page from disk (swap space), places it in a free frame, updates the page table, and restarts the instruction. This allows running programs larger than physical memory and enables efficient memory sharing between processes.

**Q5: Compare FIFO, LRU, and Optimal page replacement algorithms.**

FIFO replaces the page that has been in memory the longest. It is simple but can suffer from Belady's anomaly (more frames can lead to more faults). LRU replaces the page that has not been used for the longest time, based on temporal locality. It is a good practical choice and is immune to Belady's anomaly, but exact implementation requires tracking access times or maintaining a stack, which is expensive. The Optimal algorithm replaces the page that will not be used for the longest time in the future -- it provides the fewest page faults but requires future knowledge, making it useful only as a theoretical benchmark. In practice, the Clock algorithm approximates LRU efficiently using a reference bit.

**Q6: What is thrashing and how do you prevent it?**

Thrashing occurs when a process spends more time handling page faults than executing instructions. It happens when a process has too few frames to hold its working set (the set of pages it is actively using). The system becomes I/O bound as the disk is constantly swapping pages in and out. Prevention strategies include: (1) The working-set model: track each process's working set and ensure enough frames are allocated. (2) Page-fault frequency (PFF): if a process faults too often, give it more frames; if it faults rarely, take frames away. (3) Decrease the degree of multiprogramming by swapping out entire processes.

**Q7: Explain the difference between preemptive and non-preemptive scheduling.**

In non-preemptive (cooperative) scheduling, a running process keeps the CPU until it voluntarily releases it (by blocking on I/O, completing, or yielding). In preemptive scheduling, the OS can forcibly interrupt a running process (via a timer interrupt) and dispatch another one. Preemptive scheduling is used in all modern general-purpose OSes because it ensures responsiveness and prevents a single process from monopolizing the CPU. The downside is the overhead of context switches and the need for synchronization primitives to protect shared data that might be accessed mid-update when preemption occurs.

**Q8: What happens when you type `ls` in a Unix shell?**

1. The shell reads the input and parses "ls".
2. The shell calls `fork()` to create a child process.
3. In the child process, `execvp("ls", args)` is called, which replaces the child's memory image with the `ls` binary.
4. The kernel loads the `ls` program (using demand paging), sets up its stack and registers, and begins execution.
5. `ls` makes system calls like `opendir()`, `readdir()`, and `stat()` to read the directory.
6. `ls` calls `write()` to output the listing to stdout (file descriptor 1).
7. `ls` calls `exit()` to terminate.
8. The parent shell's `wait()` call returns, collecting the child's exit status.
9. The shell prints the next prompt and waits for input.

**Q9: What is the difference between a mutex and a semaphore?**

A mutex (mutual exclusion) is a locking mechanism that allows only one thread to access a critical section at a time. It has ownership: only the thread that locked the mutex can unlock it. A semaphore is a signaling mechanism based on a counter. A **binary semaphore** (count 0 or 1) can mimic a mutex but has no ownership -- any thread can signal (increment) it. A **counting semaphore** allows up to N concurrent accesses, useful for resource pools (e.g., limiting database connections to 10). Mutexes are for mutual exclusion; semaphores are for signaling and controlling concurrent access to a finite number of resources.

**Q10: How does shared memory IPC work? Why is it the fastest IPC mechanism?**

With shared memory, the OS maps a region of physical memory into the virtual address spaces of multiple processes. Once the mapping is set up (via `shmget`/`shmat` or `mmap`), processes read and write directly to the shared region without any kernel involvement -- the data does not need to be copied between user space and kernel space (unlike pipes or message queues where each send/receive requires a copy into/out of the kernel). This zero-copy access makes it the fastest IPC mechanism. The tradeoff is that processes must explicitly synchronize access using semaphores or mutexes to avoid race conditions, since the kernel provides no built-in ordering of reads and writes.

---

# 2. Computer Networks

---

## 2.1 OSI Model and TCP/IP Model

### OSI Model (7 Layers)

| Layer | Name | Function | Key Protocols | Data Unit |
|---|---|---|---|---|
| 7 | **Application** | End-user services and APIs | HTTP, FTP, SMTP, DNS, SSH | Data |
| 6 | **Presentation** | Data format translation, encryption, compression | SSL/TLS, JPEG, ASCII, MPEG | Data |
| 5 | **Session** | Establish, manage, and terminate sessions | NetBIOS, RPC, PPTP | Data |
| 4 | **Transport** | End-to-end communication, reliability, flow control | TCP, UDP | Segment/Datagram |
| 3 | **Network** | Logical addressing, routing across networks | IP, ICMP, ARP, OSPF, BGP | Packet |
| 2 | **Data Link** | Frame delivery between adjacent nodes, error detection | Ethernet, Wi-Fi (802.11), PPP | Frame |
| 1 | **Physical** | Raw bit transmission over physical medium | Ethernet cables, fiber optics, radio | Bits |

### TCP/IP Model (4 Layers)

| TCP/IP Layer | Corresponds to OSI | Key Protocols |
|---|---|---|
| **Application** | OSI 5-7 | HTTP, DNS, FTP, SMTP, SSH |
| **Transport** | OSI 4 | TCP, UDP |
| **Internet** | OSI 3 | IP, ICMP, ARP |
| **Network Access** | OSI 1-2 | Ethernet, Wi-Fi, PPP |

**Mnemonic for OSI (top-down):** All People Seem To Need Data Processing.

### Encapsulation

```
Application Data
    ↓ + [App Header]
Transport Segment: [TCP/UDP Header | Data]
    ↓ + [IP Header]
Network Packet:    [IP Header | TCP Header | Data]
    ↓ + [Frame Header + Trailer]
Data Link Frame:   [Ethernet Header | IP Header | TCP Header | Data | FCS]
    ↓
Physical:          101010010110001... (bits on the wire)
```

---

## 2.2 TCP vs UDP

### TCP (Transmission Control Protocol)

- **Connection-oriented:** Requires a 3-way handshake before data transfer
- **Reliable:** Guarantees delivery, ordering, and error checking
- **Flow control:** Sliding window protocol prevents sender from overwhelming receiver
- **Congestion control:** Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery

**TCP 3-Way Handshake:**

```
Client                    Server
  │                         │
  │──── SYN (seq=x) ──────▶│
  │                         │
  │◀── SYN-ACK (seq=y, ────│
  │     ack=x+1)           │
  │                         │
  │──── ACK (ack=y+1) ────▶│
  │                         │
  │    Connection Established
```

**TCP Connection Termination (4-way):**

```
Client                    Server
  │                         │
  │──── FIN ───────────────▶│
  │◀── ACK ─────────────────│
  │                         │
  │◀── FIN ─────────────────│
  │──── ACK ───────────────▶│
  │                         │
  │  (TIME_WAIT → CLOSED)  │
```

### UDP (User Datagram Protocol)

- **Connectionless:** No handshake; send datagrams independently
- **Unreliable:** No guarantee of delivery, ordering, or duplicate protection
- **Low overhead:** 8-byte header vs TCP's 20-byte minimum header
- **No congestion control:** Can blast data at any rate

### TCP vs UDP Comparison

| Feature | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best-effort |
| Ordering | Maintains order | No ordering |
| Header size | 20-60 bytes | 8 bytes |
| Speed | Slower (overhead) | Faster (minimal overhead) |
| Flow control | Yes (sliding window) | No |
| Congestion control | Yes | No |
| Use cases | HTTP, FTP, email, SSH | DNS, video streaming, gaming, VoIP, IoT |

### TCP Congestion Control

| Phase | Behavior |
|---|---|
| **Slow Start** | cwnd starts at 1 MSS; doubles every RTT (exponential growth) until ssthresh |
| **Congestion Avoidance** | cwnd increases by 1 MSS per RTT (linear growth) |
| **Fast Retransmit** | On 3 duplicate ACKs, retransmit the lost segment immediately (don't wait for timeout) |
| **Fast Recovery** | After fast retransmit, set ssthresh = cwnd/2 and cwnd = ssthresh + 3, then enter congestion avoidance |

---

## 2.3 HTTP / HTTPS

### HTTP Methods

| Method | Idempotent | Safe | Description |
|---|---|---|---|
| **GET** | Yes | Yes | Retrieve a resource |
| **POST** | No | No | Submit data; create a resource |
| **PUT** | Yes | No | Replace/create a resource at a specific URI |
| **PATCH** | No | No | Partial update of a resource |
| **DELETE** | Yes | No | Remove a resource |
| **HEAD** | Yes | Yes | Same as GET but returns only headers |
| **OPTIONS** | Yes | Yes | Describe communication options (used in CORS preflight) |

### HTTP Status Codes

| Range | Category | Common Codes |
|---|---|---|
| 1xx | Informational | 100 Continue, 101 Switching Protocols |
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| 5xx | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout |

### HTTP/1.1 vs HTTP/2 vs HTTP/3

| Feature | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Transport | TCP | TCP | **QUIC (over UDP)** |
| Multiplexing | No (one request per connection or pipelining with HOL blocking) | Yes (multiple streams over single connection) | Yes (no HOL blocking at transport level) |
| Header compression | No | HPACK | QPACK |
| Server push | No | Yes | Yes |
| Connection setup | TCP handshake + TLS handshake | Same as HTTP/1.1 | 0-RTT or 1-RTT (QUIC combines transport + TLS) |

### Cookies and Sessions

- **Cookie:** Small piece of data stored by the browser, sent with every subsequent request to the same domain. Used for session management, personalization, and tracking.
- **Session:** Server-side data store identified by a session ID (typically stored in a cookie). Stores user state across stateless HTTP requests.

---

## 2.4 DNS (Domain Name System)

DNS translates human-readable domain names (e.g., `www.example.com`) into IP addresses (e.g., `93.184.216.34`).

### DNS Resolution Process

```
User types www.example.com
        │
        ▼
1. Browser Cache → found? → done
        │ miss
        ▼
2. OS Cache (hosts file) → found? → done
        │ miss
        ▼
3. Recursive Resolver (ISP) → found in cache? → done
        │ miss
        ▼
4. Root Name Server → "Go ask .com TLD server"
        │
        ▼
5. TLD Name Server (.com) → "Go ask ns1.example.com"
        │
        ▼
6. Authoritative Name Server → "93.184.216.34" (with TTL)
        │
        ▼
7. Resolver caches the result and returns to client
```

### DNS Record Types

| Type | Purpose | Example |
|---|---|---|
| **A** | Maps domain to IPv4 address | `example.com → 93.184.216.34` |
| **AAAA** | Maps domain to IPv6 address | `example.com → 2606:2800:220:1:...` |
| **CNAME** | Alias for another domain name | `www.example.com → example.com` |
| **MX** | Mail exchange server | `example.com → mail.example.com (priority 10)` |
| **NS** | Authoritative name server for the zone | `example.com → ns1.example.com` |
| **TXT** | Arbitrary text (SPF, DKIM, domain verification) | `example.com → "v=spf1 include:_spf.google.com"` |
| **SOA** | Start of Authority; zone metadata | Serial number, refresh/retry timers |
| **PTR** | Reverse DNS (IP → domain) | `34.216.184.93.in-addr.arpa → example.com` |

---

## 2.5 IP Addressing

### IPv4 vs IPv6

| Feature | IPv4 | IPv6 |
|---|---|---|
| Address size | 32 bits (4 bytes) | 128 bits (16 bytes) |
| Notation | Dotted decimal: `192.168.1.1` | Hex colon: `2001:0db8::1` |
| Address space | ~4.3 billion | ~3.4 × 10^38 |
| Header size | 20-60 bytes | Fixed 40 bytes |
| NAT required | Commonly | No (enough addresses) |
| IPSec | Optional | Built-in |

### Subnetting and CIDR

**CIDR notation:** `192.168.1.0/24` means the first 24 bits are the network portion.

| CIDR | Subnet Mask | Hosts per Subnet |
|---|---|---|
| /8 | 255.0.0.0 | 16,777,214 |
| /16 | 255.255.0.0 | 65,534 |
| /24 | 255.255.255.0 | 254 |
| /32 | 255.255.255.255 | 1 (single host) |

Number of usable hosts = 2^(32 - prefix) - 2 (subtract network address and broadcast address).

### Private IP Ranges

| Class | Range | CIDR |
|---|---|---|
| A | 10.0.0.0 -- 10.255.255.255 | 10.0.0.0/8 |
| B | 172.16.0.0 -- 172.31.255.255 | 172.16.0.0/12 |
| C | 192.168.0.0 -- 192.168.255.255 | 192.168.0.0/16 |

### NAT (Network Address Translation)

NAT translates private IPs to a public IP (and vice versa) at the router. It conserves IPv4 addresses and provides a layer of security by hiding internal network structure. The router maintains a **NAT table** mapping (internal IP:port) → (external IP:port).

---

## 2.6 Routing

### Distance-Vector vs Link-State

| Aspect | Distance-Vector | Link-State |
|---|---|---|
| Algorithm | Bellman-Ford | Dijkstra's |
| Knowledge | Each router knows only its neighbors' distances | Each router has complete topology of the network |
| Updates | Periodic, share full routing table with neighbors | Event-driven, flood link-state advertisements to all |
| Convergence | Slow; suffers from count-to-infinity problem | Fast |
| Protocols | RIP, BGP (path-vector variant) | OSPF, IS-IS |
| Scalability | Better for small networks | Better for large networks |

### Key Routing Protocols

| Protocol | Type | Scope | Notes |
|---|---|---|---|
| **OSPF** | Link-state | Interior (within an AS) | Uses areas for hierarchy; fast convergence |
| **BGP** | Path-vector | Exterior (between ASes) | The protocol that routes the internet; uses policies and path attributes |
| **RIP** | Distance-vector | Interior | Max 15 hops; mostly legacy |

---

## 2.7 Application Layer Protocols

### Sockets

A **socket** is an endpoint for bidirectional communication. Identified by (IP address, port number, protocol).

**Socket types:**
- **Stream socket (SOCK_STREAM):** TCP -- reliable, ordered byte stream
- **Datagram socket (SOCK_DGRAM):** UDP -- unreliable, message-oriented

**Socket lifecycle (TCP server):**

```
socket() → bind() → listen() → accept() → read()/write() → close()
```

**Socket lifecycle (TCP client):**

```
socket() → connect() → read()/write() → close()
```

### REST API Principles

| Principle | Description |
|---|---|
| **Stateless** | Each request contains all information needed; server stores no client state |
| **Resource-based** | URLs represent resources (`/users/123`), not actions |
| **HTTP methods as verbs** | GET = read, POST = create, PUT = update, DELETE = remove |
| **Representations** | Resources can have multiple representations (JSON, XML) |
| **HATEOAS** | Responses include links to related resources |

### WebSockets vs HTTP

| Feature | HTTP | WebSocket |
|---|---|---|
| Communication | Request-response (half-duplex) | Full-duplex, persistent |
| Connection | New connection per request (HTTP/1.1 keep-alive reuses) | Single long-lived connection |
| Overhead | Headers on every request | Minimal frame overhead after handshake |
| Use case | Standard web requests | Real-time: chat, live feeds, gaming |

### gRPC and GraphQL

| Feature | REST | gRPC | GraphQL |
|---|---|---|---|
| Protocol | HTTP/1.1 or HTTP/2 | HTTP/2 | HTTP |
| Data format | JSON (text) | Protocol Buffers (binary) | JSON |
| Schema | OpenAPI/Swagger (optional) | `.proto` files (required) | Schema Definition Language (required) |
| Streaming | No native | Unary, server, client, bidirectional streaming | Subscriptions |
| Best for | Public APIs, web | Microservice-to-microservice, low latency | Flexible client queries, mobile apps |

---

## 2.8 TLS/SSL Handshake

TLS (Transport Layer Security) provides encryption, authentication, and integrity for communication over a network.

**TLS 1.2 Handshake (simplified):**

```
Client                                   Server
  │                                        │
  │──── ClientHello ──────────────────────▶│  (supported cipher suites, random)
  │                                        │
  │◀──── ServerHello ──────────────────────│  (chosen cipher suite, random)
  │◀──── Certificate ──────────────────────│  (server's public key certificate)
  │◀──── ServerHelloDone ─────────────────│
  │                                        │
  │──── ClientKeyExchange ────────────────▶│  (pre-master secret encrypted with server's public key)
  │──── ChangeCipherSpec ─────────────────▶│  (switching to encrypted communication)
  │──── Finished ─────────────────────────▶│  (encrypted verification)
  │                                        │
  │◀──── ChangeCipherSpec ─────────────────│
  │◀──── Finished ─────────────────────────│
  │                                        │
  │        Encrypted Data Exchange         │
```

**TLS 1.3 improvements:** 1-RTT handshake (vs 2-RTT in TLS 1.2), 0-RTT resumption, removed insecure cipher suites, simplified handshake.

---

## 2.9 Computer Networks -- Interview Questions

**Q1: What happens when you type `https://www.google.com` in a browser?**

1. **URL parsing:** The browser parses the URL into protocol (HTTPS), host (www.google.com), and path (/).
2. **DNS resolution:** The browser checks its cache, then the OS cache, then queries the recursive DNS resolver. The resolver contacts root servers → .com TLD → google.com's authoritative DNS server to get the IP address.
3. **TCP connection:** The browser establishes a TCP connection to the server's IP on port 443 using the 3-way handshake (SYN, SYN-ACK, ACK).
4. **TLS handshake:** Since it's HTTPS, a TLS handshake occurs. The server presents its certificate, the browser verifies it against trusted CAs, and they negotiate a symmetric session key.
5. **HTTP request:** The browser sends an HTTP GET request for `/` with headers (Host, User-Agent, Accept, cookies, etc.).
6. **Server processing:** Google's load balancer routes the request to a web server, which generates the HTML response.
7. **HTTP response:** The server sends back a response (status 200 OK, headers, HTML body).
8. **Rendering:** The browser parses the HTML, builds the DOM tree, requests additional resources (CSS, JS, images), constructs the CSSOM, creates the render tree, performs layout, and paints pixels to the screen.
9. **Connection management:** The connection may be kept alive for subsequent requests (HTTP/2 multiplexing).

**Q2: Explain the difference between TCP and UDP. When would you use each?**

TCP is connection-oriented, providing reliable, ordered delivery with flow and congestion control, at the cost of higher latency and overhead. UDP is connectionless and provides best-effort delivery with minimal overhead. Use TCP when data integrity is critical (web browsing, file transfer, email, database queries). Use UDP when speed matters more than reliability and the application can tolerate or handle packet loss (live video/audio streaming, online gaming, DNS lookups, IoT sensor data). Many modern protocols like QUIC (used by HTTP/3) build reliability on top of UDP to get the best of both worlds.

**Q3: What is the difference between HTTP and HTTPS?**

HTTP transmits data in plaintext, making it vulnerable to eavesdropping and man-in-the-middle attacks. HTTPS is HTTP over TLS -- it encrypts all communication between client and server, authenticates the server's identity via certificates, and ensures data integrity. HTTPS uses port 443 by default (vs 80 for HTTP). The TLS handshake adds latency to the initial connection but provides confidentiality and trust. Modern best practice is to use HTTPS for all web traffic.

**Q4: How does DNS work? What could cause DNS resolution to be slow?**

DNS is a hierarchical distributed naming system that maps domain names to IP addresses. Resolution starts with local caches (browser, OS), then queries a recursive resolver, which contacts root, TLD, and authoritative name servers as needed. DNS can be slow due to: (1) cache misses requiring multiple round trips, (2) high TTL misses after DNS record changes, (3) slow or overloaded DNS resolvers, (4) network latency to geographically distant DNS servers, (5) DNSSEC validation overhead. Mitigation includes using fast public DNS (Google 8.8.8.8, Cloudflare 1.1.1.1), DNS prefetching in browsers, and appropriate TTL values.

**Q5: What is a CDN and how does it work?**

A Content Delivery Network (CDN) is a geographically distributed network of proxy servers that cache content close to end users. When a user requests a resource, DNS routes them to the nearest CDN edge server (using anycast or geo-DNS). If the edge has the content cached, it serves it directly (cache hit). If not (cache miss), it fetches from the origin server, caches it, and serves it. CDNs reduce latency, decrease load on origin servers, absorb traffic spikes (DDoS protection), and improve availability. Push CDNs receive content proactively from the origin; pull CDNs fetch content lazily on first request.

**Q6: Explain the TCP 3-way handshake. Why is it necessary?**

The 3-way handshake (SYN → SYN-ACK → ACK) establishes a TCP connection. The client sends a SYN with its initial sequence number (ISN). The server responds with SYN-ACK, acknowledging the client's ISN and sending its own. The client sends ACK confirming the server's ISN. This is necessary to: (1) synchronize sequence numbers for reliable ordered delivery, (2) confirm both sides can send and receive, (3) prevent old duplicate connection requests from being accepted (the sequence numbers and timestamps guard against this).

**Q7: What is NAT? What problems does it solve and create?**

NAT (Network Address Translation) modifies IP addresses in packet headers as they pass through a router, allowing multiple devices on a private network to share a single public IP. It solves IPv4 address exhaustion and provides a basic layer of security (external hosts cannot initiate connections to internal hosts). Problems: (1) breaks end-to-end connectivity, (2) complicates protocols that embed IP addresses in payloads (FTP, SIP), (3) makes peer-to-peer connections difficult (requires techniques like STUN/TURN/ICE), (4) adds state to the router (NAT table), making it a potential bottleneck.

**Q8: Compare REST, gRPC, and GraphQL.**

REST is resource-oriented, uses standard HTTP methods and JSON, and is best for public APIs due to simplicity and broad tooling. gRPC uses Protocol Buffers (binary serialization) over HTTP/2, providing strongly-typed contracts, streaming support, and lower latency -- ideal for internal microservice communication. GraphQL gives clients a query language to request exactly the data they need, solving over-fetching and under-fetching problems common with REST. REST is the most ubiquitous, gRPC is the fastest, and GraphQL is the most flexible for complex client data requirements.

---

# 3. Database Systems

---

## 3.1 Relational Database Concepts

### Core Terminology

| Term | Definition |
|---|---|
| **Relation (Table)** | A set of tuples (rows) with a common schema |
| **Tuple (Row)** | A single record in a table |
| **Attribute (Column)** | A named field with a defined data type |
| **Schema** | The structure definition of a table (column names, types, constraints) |
| **Primary Key** | A column (or set of columns) that uniquely identifies each row |
| **Foreign Key** | A column that references the primary key of another table, enforcing referential integrity |
| **Candidate Key** | Any column(s) that could serve as a primary key (unique + not null) |
| **Composite Key** | A primary key consisting of two or more columns |

### Types of Relationships

| Relationship | Example | Implementation |
|---|---|---|
| **One-to-One** | User ↔ Profile | Foreign key in either table (with UNIQUE constraint) |
| **One-to-Many** | Author → Books | Foreign key in the "many" table references the "one" table |
| **Many-to-Many** | Students ↔ Courses | Junction/bridge table with foreign keys to both tables |

---

## 3.2 SQL Essentials

### Types of SQL Statements

| Category | Commands | Purpose |
|---|---|---|
| **DDL** (Data Definition Language) | CREATE, ALTER, DROP, TRUNCATE | Define/modify schema |
| **DML** (Data Manipulation Language) | SELECT, INSERT, UPDATE, DELETE | Manipulate data |
| **DCL** (Data Control Language) | GRANT, REVOKE | Control access |
| **TCL** (Transaction Control Language) | COMMIT, ROLLBACK, SAVEPOINT | Manage transactions |

### JOIN Types

| Join | Returns | Venn Diagram |
|---|---|---|
| **INNER JOIN** | Rows with matching keys in both tables | Intersection |
| **LEFT JOIN** | All rows from left table + matching rows from right (NULLs for no match) | Left circle + intersection |
| **RIGHT JOIN** | All rows from right table + matching rows from left | Right circle + intersection |
| **FULL OUTER JOIN** | All rows from both tables (NULLs where no match) | Both circles |
| **CROSS JOIN** | Cartesian product of both tables | Every combination |
| **SELF JOIN** | Table joined with itself | Hierarchical data (employees → manager) |

```sql
-- INNER JOIN
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- LEFT JOIN
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;
```

### Aggregations and GROUP BY

```sql
SELECT dept_id, COUNT(*) as emp_count, AVG(salary) as avg_salary
FROM employees
WHERE status = 'active'
GROUP BY dept_id
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;
```

**Execution order:** FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

### Window Functions

Window functions perform calculations across a set of rows related to the current row without collapsing them (unlike GROUP BY).

```sql
SELECT name, department, salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    SUM(salary) OVER (PARTITION BY department) as dept_total,
    LAG(salary) OVER (ORDER BY salary) as prev_salary,
    salary - LAG(salary) OVER (ORDER BY salary) as salary_diff
FROM employees;
```

| Function | Description |
|---|---|
| `ROW_NUMBER()` | Unique sequential number for each row in the partition |
| `RANK()` | Rank with gaps (ties get same rank, next rank skips) |
| `DENSE_RANK()` | Rank without gaps |
| `NTILE(n)` | Divide rows into n roughly equal buckets |
| `LAG(col, n)` | Value of col from n rows before |
| `LEAD(col, n)` | Value of col from n rows after |
| `SUM/AVG/MIN/MAX() OVER(...)` | Running aggregates |

### Common Table Expressions (CTEs)

```sql
WITH high_earners AS (
    SELECT id, name, salary, dept_id
    FROM employees
    WHERE salary > 100000
),
dept_stats AS (
    SELECT dept_id, COUNT(*) as count, AVG(salary) as avg_sal
    FROM high_earners
    GROUP BY dept_id
)
SELECT d.dept_name, ds.count, ds.avg_sal
FROM dept_stats ds
JOIN departments d ON ds.dept_id = d.id;
```

**Recursive CTE** (for hierarchical data like org charts):

```sql
WITH RECURSIVE org_chart AS (
    SELECT id, name, manager_id, 0 AS level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level;
```

---

## 3.3 Normalization

Normalization reduces data redundancy and prevents update anomalies by organizing tables according to functional dependencies.

| Normal Form | Rule | Violation Example | Fix |
|---|---|---|---|
| **1NF** | All columns contain atomic (indivisible) values; each row is unique | `phone_numbers = "555-1234, 555-5678"` | Separate into rows or a new table |
| **2NF** | 1NF + no partial dependency (non-key attribute depends on part of composite key) | In (StudentID, CourseID) → StudentName depends only on StudentID | Move StudentName to a Students table |
| **3NF** | 2NF + no transitive dependency (non-key attribute depends on another non-key attribute) | Employee → DeptID → DeptName (DeptName depends on DeptID, not Employee) | Move DeptName to a Departments table |
| **BCNF** | Every determinant is a candidate key | When a non-candidate-key column determines another column | Decompose the table |

### Denormalization

Intentionally introducing redundancy to improve read performance. Common in analytics/OLAP systems and when joining normalized tables is too expensive. Tradeoff: faster reads but slower writes, risk of data inconsistency, and more storage.

---

## 3.4 Indexing

An **index** is a data structure that improves query speed at the cost of additional storage and slower writes.

### Index Types

| Index Type | Data Structure | Best For | Notes |
|---|---|---|---|
| **B-Tree** | Balanced tree | Range queries, equality, sorting | Default in most RDBMS; O(log n) search |
| **B+ Tree** | B-Tree variant with data only in leaves | Range scans | Leaves are linked for efficient sequential access; used by InnoDB |
| **Hash** | Hash table | Exact equality lookups | O(1) average; cannot support range queries or ordering |
| **Bitmap** | Bit arrays per distinct value | Low-cardinality columns (gender, status) | Efficient for AND/OR/NOT operations; common in data warehouses |
| **GiST / GIN** | Generalized trees | Full-text search, geometric data | PostgreSQL extensions |

### Index Categories

| Category | Description |
|---|---|
| **Clustered Index** | Determines the physical order of data on disk. Only one per table (usually the primary key). Accessing rows by clustered index is very fast. |
| **Non-Clustered Index** | Separate structure with pointers to data rows. Multiple allowed per table. Requires a "bookmark lookup" to get full row data. |
| **Composite Index** | Index on multiple columns. Follows the **leftmost prefix rule**: an index on (A, B, C) can serve queries on (A), (A, B), or (A, B, C), but NOT (B) or (C) alone. |
| **Covering Index** | A composite index that includes all columns needed by a query, eliminating the need to access the base table (index-only scan). |
| **Unique Index** | Enforces uniqueness constraint on indexed columns. |

### When NOT to Index

- Tables with very few rows (full scan is faster)
- Columns with very low selectivity (e.g., boolean flags -- unless using bitmap index)
- Write-heavy tables where index maintenance outweighs read benefits
- Columns rarely used in WHERE, JOIN, or ORDER BY clauses

---

## 3.5 Transactions and ACID

A **transaction** is a sequence of database operations that are treated as a single logical unit of work.

### ACID Properties

| Property | Description | Mechanism |
|---|---|---|
| **Atomicity** | All operations in a transaction succeed or all fail (all-or-nothing) | Undo log (rollback on failure) |
| **Consistency** | A transaction brings the database from one valid state to another, respecting all constraints | Constraint checks, triggers |
| **Isolation** | Concurrent transactions do not interfere with each other | Locks, MVCC |
| **Durability** | Once committed, changes survive system failures | Write-ahead log (WAL), fsync |

### Isolation Levels

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Performance |
|---|---|---|---|---|
| **Read Uncommitted** | Possible | Possible | Possible | Fastest |
| **Read Committed** | Prevented | Possible | Possible | Good |
| **Repeatable Read** | Prevented | Prevented | Possible | Moderate |
| **Serializable** | Prevented | Prevented | Prevented | Slowest |

**Definitions:**
- **Dirty Read:** Reading data written by an uncommitted transaction
- **Non-Repeatable Read:** Reading the same row twice yields different values (another transaction modified it)
- **Phantom Read:** A query returns different sets of rows when executed twice (another transaction inserted/deleted rows)

### MVCC (Multi-Version Concurrency Control)

Instead of locking, MVCC keeps multiple versions of each row. Readers see a snapshot consistent with their transaction's start time, while writers create new versions. This allows readers and writers to not block each other, greatly improving concurrency. Used by PostgreSQL, MySQL InnoDB, and Oracle.

---

## 3.6 NoSQL Databases

| Type | Data Model | Examples | Best For | Limitations |
|---|---|---|---|---|
| **Key-Value** | Simple key → value pairs | Redis, Memcached, DynamoDB | Caching, session stores, simple lookups | No complex queries or relationships |
| **Document** | JSON/BSON documents (schema-flexible) | MongoDB, CouchDB, Firestore | Content management, catalogs, user profiles | Joins are expensive; denormalization needed |
| **Column-Family** | Rows with dynamic columns grouped into families | Cassandra, HBase, Bigtable | Time-series, IoT, write-heavy analytics | Limited query flexibility; no joins |
| **Graph** | Nodes + edges with properties | Neo4j, Amazon Neptune, JanusGraph | Social networks, recommendations, fraud detection | Not efficient for bulk analytics |

### SQL vs NoSQL Decision Guide

| Factor | Choose SQL | Choose NoSQL |
|---|---|---|
| Data structure | Well-defined, relational | Flexible, evolving schema |
| Consistency | Strong consistency required (financial) | Eventual consistency acceptable |
| Query complexity | Complex joins, aggregations, transactions | Simple lookups, denormalized reads |
| Scale | Vertical (scale up) | Horizontal (scale out) |
| Examples | Banking, ERP, inventory | Social media feeds, real-time analytics, caching |

---

## 3.7 CAP Theorem and PACELC

### CAP Theorem

In a distributed system, you can only guarantee two of three properties simultaneously:

| Property | Description |
|---|---|
| **Consistency** | Every read receives the most recent write (all nodes see the same data at the same time) |
| **Availability** | Every request receives a response (not necessarily the most recent data) |
| **Partition Tolerance** | The system continues to operate despite network partitions between nodes |

Since network partitions are inevitable in distributed systems, the real choice is between **CP** (consistent but may be unavailable during partitions) and **AP** (available but may return stale data during partitions).

| System | CAP Choice | Behavior During Partition |
|---|---|---|
| Traditional RDBMS | CA (single node) | N/A (not distributed) |
| HBase, MongoDB (default), Redis Cluster | CP | Rejects requests to maintain consistency |
| Cassandra, DynamoDB, CouchDB | AP | Serves potentially stale data; resolves conflicts later |

### PACELC Theorem

Extends CAP: if there is a **P**artition, choose **A**vailability or **C**onsistency; **E**lse (normal operation), choose **L**atency or **C**onsistency.

| System | During Partition (PAC) | Normal Operation (ELC) |
|---|---|---|
| Cassandra | PA | EL (low latency) |
| MongoDB | PC | EC (consistency) |
| DynamoDB | PA | EL (tunable) |

---

## 3.8 Sharding, Replication, and Partitioning

### Replication

| Strategy | Description | Pros | Cons |
|---|---|---|---|
| **Leader-Follower** | One leader handles writes; followers replicate and handle reads | Simple, scales reads | Leader is SPOF; replication lag |
| **Leader-Leader** | Multiple nodes accept writes | No single write bottleneck | Conflict resolution needed |
| **Quorum** | W + R > N ensures consistency (write to W nodes, read from R nodes) | Tunable consistency/availability | Higher latency per operation |

### Partitioning Strategies

| Strategy | Method | Pros | Cons |
|---|---|---|---|
| **Range-based** | Partition by key ranges (A-M, N-Z) | Good for range queries | Hotspots if keys are not uniformly distributed |
| **Hash-based** | Hash(key) mod N determines partition | Uniform distribution | Range queries become scatter-gather |
| **Directory-based** | Lookup table maps keys to partitions | Flexible | Lookup table is a bottleneck/SPOF |

### Query Optimization

| Technique | Description |
|---|---|
| **EXPLAIN / EXPLAIN ANALYZE** | Shows the execution plan (seq scan vs index scan, join strategy, estimated cost) |
| **Index selection** | Ensure WHERE/JOIN/ORDER BY columns are indexed |
| **Avoid SELECT \*** | Select only needed columns to reduce I/O |
| **Use covering indexes** | Include all queried columns in the index |
| **Batch operations** | Use bulk INSERT/UPDATE instead of row-by-row |
| **Parameterized queries** | Allow plan caching; prevent SQL injection |
| **Partitioning** | Split large tables to scan fewer rows |
| **Materialized views** | Precompute expensive aggregations |

---

## 3.9 Database Systems -- Interview Questions

**Q1: What are the ACID properties? Explain each one.**

ACID ensures reliable transaction processing. **Atomicity** guarantees all-or-nothing execution -- if any operation in a transaction fails, the entire transaction is rolled back. **Consistency** ensures the database transitions only between valid states, respecting all defined constraints (unique keys, foreign keys, check constraints). **Isolation** ensures concurrent transactions do not see each other's intermediate states -- the level of isolation is configurable (from Read Uncommitted to Serializable). **Durability** guarantees that once a transaction commits, its changes are permanent even if the system crashes, typically enforced by writing to a write-ahead log (WAL) before acknowledging the commit.

**Q2: What is the difference between a clustered and a non-clustered index?**

A clustered index determines the physical storage order of data in the table. Since data can only be sorted one way, a table can have only one clustered index (typically on the primary key). Accessing rows via a clustered index is fast because the data is co-located. A non-clustered index is a separate structure containing the indexed columns and a pointer (row locator) back to the actual data row. A table can have many non-clustered indexes. Queries using a non-clustered index may require a "bookmark lookup" to retrieve columns not in the index, unless it is a covering index.

**Q3: Explain normalization. What is 3NF?**

Normalization is the process of organizing a relational database to reduce redundancy and prevent update anomalies (insertion, deletion, and modification anomalies). A table is in Third Normal Form (3NF) if: (1) it is in 2NF (no partial dependencies on a composite key), and (2) it has no transitive dependencies -- every non-key attribute depends directly on the primary key, not through another non-key attribute. For example, if an employee table stores dept_id and dept_name, dept_name depends on dept_id (a non-key column), creating a transitive dependency. The fix is to create a separate departments table.

**Q4: When would you denormalize a database?**

Denormalization is appropriate when read performance is critical and the cost of joins becomes prohibitive. Common scenarios include: (1) OLAP/analytics systems where complex aggregation queries run on large datasets, (2) read-heavy applications with infrequent writes, (3) caching precomputed values to avoid repeated expensive calculations, (4) NoSQL databases where joins are not natively supported. The tradeoffs are increased storage, data redundancy, risk of inconsistency on updates, and slower writes. A common pattern is to keep the normalized source of truth and denormalize into materialized views or read replicas.

**Q5: Explain the CAP theorem. Give examples of CP and AP systems.**

The CAP theorem states that a distributed system can provide at most two of three guarantees: Consistency (every read sees the most recent write), Availability (every request gets a response), and Partition Tolerance (the system operates despite network failures). Since partitions are unavoidable, the real choice is CP vs AP. CP systems (e.g., HBase, ZooKeeper) sacrifice availability during partitions to maintain consistency -- they may reject requests rather than return stale data. AP systems (e.g., Cassandra, DynamoDB) sacrifice consistency during partitions to remain available -- they may return stale data and resolve conflicts later using techniques like last-write-wins or vector clocks.

**Q6: What is an execution plan? How do you optimize a slow query?**

An execution plan (obtained via EXPLAIN or EXPLAIN ANALYZE) shows how the database engine will execute a query: which indexes it uses, the join strategy (nested loop, hash join, merge join), estimated row counts, and cost. To optimize a slow query: (1) Check for full table scans and add appropriate indexes. (2) Ensure composite indexes follow the leftmost prefix rule for the query's WHERE clause. (3) Avoid SELECT * -- select only needed columns. (4) Rewrite correlated subqueries as JOINs. (5) Use covering indexes to avoid bookmark lookups. (6) Partition large tables. (7) Analyze table statistics so the query planner has accurate information. (8) Consider materialized views for expensive recurring aggregations.

**Q7: Explain the different types of SQL JOINs with examples.**

INNER JOIN returns only rows with matching keys in both tables (intersection). LEFT JOIN returns all rows from the left table and matching rows from the right table (NULLs for unmatched). RIGHT JOIN is the mirror of LEFT JOIN. FULL OUTER JOIN returns all rows from both tables (NULLs for unmatched on either side). CROSS JOIN returns the Cartesian product (every combination). SELF JOIN joins a table with itself, useful for hierarchical relationships (e.g., finding each employee's manager when both are in the employees table). In practice, INNER JOIN and LEFT JOIN cover 90%+ of use cases.

**Q8: What is database sharding? What are its challenges?**

Sharding horizontally partitions data across multiple database servers (shards), each holding a subset of the data. It enables horizontal scaling beyond the capacity of a single server. Challenges include: (1) choosing a good shard key to avoid hotspots, (2) cross-shard queries and joins become complex and slow, (3) maintaining referential integrity across shards, (4) rebalancing data when adding or removing shards, (5) distributed transactions require coordination (2PC). Consistent hashing can help with rebalancing. An alternative is to use a distributed database that handles sharding transparently (e.g., CockroachDB, Google Spanner).

**Q9: Compare SQL and NoSQL databases. When would you choose each?**

SQL databases (PostgreSQL, MySQL) provide a fixed schema, ACID transactions, powerful query language with JOINs, and are ideal for structured, relational data with complex query needs (financial systems, ERP, inventory). NoSQL databases provide flexible schemas, horizontal scalability, and are optimized for specific access patterns: key-value stores (Redis) for caching, document stores (MongoDB) for semi-structured data, column-family stores (Cassandra) for write-heavy time-series, and graph databases (Neo4j) for relationship-heavy data. Choose SQL when you need strong consistency, complex queries, and well-defined relationships. Choose NoSQL when you need horizontal scale, flexible schema, and your access patterns are well-known and simple.

**Q10: What is MVCC and why is it important?**

Multi-Version Concurrency Control keeps multiple versions of each data row, tagged with transaction timestamps. When a transaction reads data, it sees a consistent snapshot from the transaction's start time, even if other transactions have since modified the data. Writers create new versions instead of overwriting. This means readers never block writers and writers never block readers, dramatically improving concurrency compared to lock-based approaches. MVCC is used by PostgreSQL, MySQL InnoDB, and Oracle. The tradeoff is that old versions must be garbage-collected (PostgreSQL's VACUUM process), and write-write conflicts still require coordination.

---

# 4. Object-Oriented Programming and Design Patterns

---

## 4.1 Four Pillars of OOP

### Encapsulation

Bundling data (attributes) and the methods that operate on that data into a single unit (class), while restricting direct access to some of the object's internals. Access modifiers control visibility:

| Modifier | Class | Subclass | Package | World |
|---|---|---|---|---|
| `private` | Yes | No | No | No |
| `protected` | Yes | Yes | Yes (Java) | No |
| `public` | Yes | Yes | Yes | Yes |
| (default/package) | Yes | No | Yes | No |

**Why it matters:** Encapsulation allows the internal representation to change without affecting external code. It enforces invariants (e.g., a `BankAccount` class can ensure balance never goes negative).

### Abstraction

Hiding complex implementation details and exposing only the essential interface. Achieved through abstract classes and interfaces. The user of a class interacts with its public API without needing to know how it works internally.

**Example:** A `Database` interface exposes `query()`, `insert()`, `delete()`. The caller does not need to know whether the implementation uses PostgreSQL, MongoDB, or an in-memory store.

### Inheritance

A mechanism where a new class (subclass) derives properties and behaviors from an existing class (superclass). Supports code reuse and establishes an "is-a" relationship.

| Type | Description | Supported In |
|---|---|---|
| **Single** | One parent class | Java, C++, Python |
| **Multiple** | Multiple parent classes | C++, Python (via MRO) |
| **Multilevel** | Chain: A → B → C | All OOP languages |
| **Hierarchical** | One parent, multiple children | All OOP languages |

**The Diamond Problem:** In multiple inheritance, if class D inherits from B and C, both of which inherit from A, ambiguity arises about which path to follow. C++ resolves this with virtual inheritance. Python uses the C3 Linearization (MRO -- Method Resolution Order).

### Polymorphism

The ability to treat objects of different classes through a common interface. Comes in two forms:

| Type | Mechanism | Binding Time | Example |
|---|---|---|---|
| **Compile-time (Static)** | Method overloading, operator overloading | Compile time | `add(int, int)` vs `add(double, double)` |
| **Runtime (Dynamic)** | Method overriding, virtual functions | Runtime (vtable lookup) | `Shape* s = new Circle(); s->draw();` |

---

## 4.2 SOLID Principles

| Principle | Definition | Violation Symptom | Example |
|---|---|---|---|
| **S** -- Single Responsibility | A class should have only one reason to change | God classes that do everything | Separate `UserAuth` from `UserProfile` from `UserNotification` |
| **O** -- Open/Closed | Open for extension, closed for modification | Adding features requires changing existing code | Use strategy pattern or inheritance to add new behaviors |
| **L** -- Liskov Substitution | Subtypes must be substitutable for their base types without breaking correctness | Subclass overrides violate parent's contract | A `Square` class that inherits from `Rectangle` but breaks `setWidth/setHeight` behavior |
| **I** -- Interface Segregation | Clients should not be forced to depend on interfaces they do not use | Fat interfaces with many unrelated methods | Split `IWorker` into `IWorkable` and `IFeedable` |
| **D** -- Dependency Inversion | High-level modules should not depend on low-level modules; both should depend on abstractions | Direct instantiation of concrete classes in business logic | Inject a `PaymentProcessor` interface rather than depending on `StripeProcessor` directly |

### Liskov Substitution Principle -- Classic Example

The Square-Rectangle problem: A `Square` inheriting from `Rectangle` violates LSP because `setWidth()` on a Rectangle should not affect height, but on a Square it must. Any code expecting Rectangle behavior will break with a Square.

**Fix:** Use composition or separate interfaces rather than forcing an "is-a" relationship.

---

## 4.3 Creational Design Patterns

These patterns abstract the instantiation process, making a system independent of how its objects are created.

### Singleton

Ensures a class has only one instance and provides a global point of access to it.

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

```cpp
class Singleton {
    static Singleton* instance;
    Singleton() = default;
public:
    static Singleton* getInstance() {
        if (!instance)
            instance = new Singleton();
        return instance;
    }
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
};
```

**Use:** Configuration managers, connection pools, loggers.
**Caution:** Often considered an anti-pattern because it introduces global state, makes testing difficult (hard to mock), and hides dependencies. Thread safety requires care (double-checked locking or static initialization).

### Factory Method

Defines an interface for creating objects but lets subclasses decide which class to instantiate.

```python
from abc import ABC, abstractmethod

class Transport(ABC):
    @abstractmethod
    def deliver(self): pass

class Truck(Transport):
    def deliver(self): return "Deliver by road"

class Ship(Transport):
    def deliver(self): return "Deliver by sea"

class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport: pass

    def plan_delivery(self):
        transport = self.create_transport()
        return transport.deliver()

class RoadLogistics(Logistics):
    def create_transport(self): return Truck()

class SeaLogistics(Logistics):
    def create_transport(self): return Ship()
```

**Use:** When the exact type of object to create is determined by subclasses or configuration.

### Abstract Factory

Provides an interface for creating families of related objects without specifying concrete classes.

**Use:** Creating UI widgets that must be consistent across platforms (WindowsButton + WindowsCheckbox vs MacButton + MacCheckbox).

### Builder

Separates construction of a complex object from its representation, allowing the same construction process to create different representations.

```python
class QueryBuilder:
    def __init__(self):
        self._table = ""
        self._conditions = []
        self._order = ""
        self._limit = None

    def from_table(self, table):
        self._table = table
        return self

    def where(self, condition):
        self._conditions.append(condition)
        return self

    def order_by(self, column):
        self._order = column
        return self

    def limit(self, n):
        self._limit = n
        return self

    def build(self):
        query = f"SELECT * FROM {self._table}"
        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)
        if self._order:
            query += f" ORDER BY {self._order}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

query = (QueryBuilder()
    .from_table("users")
    .where("age > 18")
    .where("status = 'active'")
    .order_by("name")
    .limit(10)
    .build())
```

**Use:** Objects with many optional parameters (avoids telescoping constructors).

### Prototype

Creates new objects by cloning an existing object (prototype) rather than constructing from scratch.

**Use:** When object creation is expensive (e.g., objects loaded from database or requiring complex initialization). Python's `copy.deepcopy()` and C++'s copy constructors support this.

---

## 4.4 Structural Design Patterns

These patterns deal with object composition, creating relationships between objects to form larger structures.

### Adapter

Converts the interface of a class into another interface clients expect. Allows incompatible interfaces to work together.

```python
class EuropeanSocket:
    def provide_220v(self):
        return 220

class USAdapter:
    def __init__(self, european_socket):
        self._socket = european_socket

    def provide_120v(self):
        return self._socket.provide_220v() * 120 // 220
```

**Use:** Integrating third-party libraries, legacy system interfaces, or APIs with different conventions.

### Decorator

Dynamically adds responsibilities to an object without modifying its class. Wraps the original object.

```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: pass
    @abstractmethod
    def description(self) -> str: pass

class SimpleCoffee(Coffee):
    def cost(self): return 2.0
    def description(self): return "Simple coffee"

class MilkDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    def cost(self): return self._coffee.cost() + 0.5
    def description(self): return self._coffee.description() + ", milk"

class SugarDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    def cost(self): return self._coffee.cost() + 0.25
    def description(self): return self._coffee.description() + ", sugar"

coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))
# "Simple coffee, milk, sugar" -> $2.75
```

**Use:** Python decorators (`@staticmethod`, `@login_required`), Java I/O streams (`BufferedReader(FileReader(...))`).

### Facade

Provides a simplified interface to a complex subsystem.

**Use:** A `HomeTheaterFacade` with a `watchMovie()` method that coordinates the projector, sound system, lights, and Blu-ray player. Simplifies client interaction with complex APIs.

### Proxy

Provides a surrogate or placeholder for another object to control access to it.

| Type | Purpose | Example |
|---|---|---|
| **Virtual Proxy** | Lazy initialization | Load heavy image only when displayed |
| **Protection Proxy** | Access control | Check permissions before allowing operations |
| **Remote Proxy** | Represent remote object locally | RPC stub |
| **Caching Proxy** | Cache results of expensive operations | Cache API responses |

### Composite

Composes objects into tree structures to represent part-whole hierarchies. Lets clients treat individual objects and compositions uniformly.

**Use:** File system (files and directories both implement `getSize()`), UI component trees, organizational hierarchies.

### Bridge

Separates an abstraction from its implementation so that the two can vary independently.

**Use:** Shape (Circle, Square) × Renderer (Vector, Raster). Without Bridge, you need CircleVector, CircleRaster, SquareVector, SquareRaster. With Bridge, shapes hold a reference to a renderer.

---

## 4.5 Behavioral Design Patterns

These patterns define how objects interact and distribute responsibility.

### Observer (Pub/Sub)

Defines a one-to-many dependency so that when one object (subject) changes state, all its dependents (observers) are notified and updated automatically.

```python
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args):
        for callback in self._listeners.get(event, []):
            callback(*args)

emitter = EventEmitter()
emitter.on("user_created", lambda user: print(f"Welcome {user}"))
emitter.on("user_created", lambda user: print(f"Sending email to {user}"))
emitter.emit("user_created", "Alice")
```

**Use:** Event systems, GUI frameworks, message brokers, reactive programming.

### Strategy

Defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime.

```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: pass

class QuickSort(SortStrategy):
    def sort(self, data): return sorted(data)  # simplified

class BubbleSort(SortStrategy):
    def sort(self, data):
        arr = data[:]
        for i in range(len(arr)):
            for j in range(len(arr) - 1 - i):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data):
        return self._strategy.sort(data)
```

**Use:** Payment methods, compression algorithms, routing strategies, validation rules.

### Command

Encapsulates a request as an object, allowing parameterization, queuing, logging, and undo operations.

**Use:** Undo/redo functionality, task queues, macro recording, transactional systems.

### Template Method

Defines the skeleton of an algorithm in a base class, letting subclasses override specific steps without changing the algorithm's structure.

```python
from abc import ABC, abstractmethod

class DataMiner(ABC):
    def mine(self, path):        # template method
        data = self.extract(path)
        data = self.transform(data)
        self.load(data)

    @abstractmethod
    def extract(self, path): pass
    @abstractmethod
    def transform(self, data): pass

    def load(self, data):
        print(f"Loading {len(data)} records into database")

class CSVMiner(DataMiner):
    def extract(self, path): return ["csv_row1", "csv_row2"]
    def transform(self, data): return [row.upper() for row in data]

class JSONMiner(DataMiner):
    def extract(self, path): return ["json_obj1", "json_obj2"]
    def transform(self, data): return [obj.upper() for obj in data]
```

### State

Allows an object to alter its behavior when its internal state changes. The object appears to change its class.

**Use:** Vending machines, document workflow (Draft → Review → Published), TCP connection states.

### Chain of Responsibility

Passes a request along a chain of handlers. Each handler decides either to process the request or pass it to the next handler.

**Use:** Middleware pipelines (Express.js, Django), logging level filters, approval workflows.

### Iterator

Provides a way to access elements of a collection sequentially without exposing its underlying representation.

**Use:** Python's `__iter__`/`__next__`, Java's `Iterator` interface, C++'s iterators.

---

## 4.6 Composition vs Inheritance

| Aspect | Inheritance | Composition |
|---|---|---|
| Relationship | "is-a" (Dog is an Animal) | "has-a" (Car has an Engine) |
| Coupling | Tight (changes to parent affect children) | Loose (components are interchangeable) |
| Flexibility | Static (fixed at compile time) | Dynamic (swap components at runtime) |
| Code reuse | Through class hierarchy | Through delegation to components |
| Testing | Harder to test in isolation | Easier to test and mock |

**Rule of thumb:** "Favor composition over inheritance" (Gang of Four). Use inheritance only for genuine "is-a" relationships where LSP holds. Use composition for "has-a" or "can-do" relationships.

---

## 4.7 Coupling and Cohesion

| Concept | Good | Bad |
|---|---|---|
| **Coupling** | Low/Loose (modules are independent) | High/Tight (modules depend heavily on each other) |
| **Cohesion** | High (elements within a module are related and focused) | Low (module handles unrelated responsibilities) |

**Goal:** High cohesion within modules, low coupling between modules.

| Coupling Type | Description | Level |
|---|---|---|
| Content | One module modifies another's internal data | Worst |
| Common | Modules share global data | Bad |
| Control | One module controls the flow of another via flags | Moderate |
| Stamp | Modules share a composite data structure but use different parts | Moderate |
| Data | Modules communicate through simple parameters | Good |
| Message | Modules communicate through a defined interface/messages | Best |

---

## 4.8 OOP & Design Patterns -- Interview Questions

**Q1: Explain the four pillars of OOP.**

The four pillars are: (1) **Encapsulation** -- bundling data and methods together and restricting access to internal details through access modifiers, protecting object invariants. (2) **Abstraction** -- hiding complex implementation behind a simple interface, so users interact with what an object does rather than how it does it. (3) **Inheritance** -- creating new classes from existing ones to reuse code and establish hierarchical relationships. (4) **Polymorphism** -- allowing objects of different types to be treated through a common interface, with behavior determined at compile time (overloading) or runtime (overriding via virtual dispatch).

**Q2: Explain SOLID principles with examples.**

**S (Single Responsibility):** A `User` class should only manage user data, not send emails -- email sending belongs in a separate `NotificationService`. **O (Open/Closed):** Adding a new payment method should not require modifying the existing payment processing code -- use a `PaymentStrategy` interface. **L (Liskov Substitution):** Any code using a `Bird` reference should work correctly whether it receives a `Sparrow` or a `Penguin` -- if `Bird` has `fly()`, then `Penguin` violates LSP. **I (Interface Segregation):** A `Printer` interface should not force a simple printer to implement `fax()` and `scan()` -- split into `IPrinter`, `IFaxer`, `IScanner`. **D (Dependency Inversion):** A `NotificationService` should depend on a `MessageSender` interface, not directly on `EmailSender` or `SMSSender`.

**Q3: What is the difference between an abstract class and an interface?**

An abstract class can have both implemented and abstract methods, instance variables, and constructors. A class can inherit from only one abstract class (in Java/C#). It represents an "is-a" relationship with shared behavior. An interface (in Java/C#) defines a contract of method signatures without implementation (though Java 8+ allows default methods). A class can implement multiple interfaces. Interfaces represent a "can-do" relationship (capabilities). Use an abstract class when subclasses share common behavior and state. Use an interface to define a capability that unrelated classes can implement.

**Q4: Explain the Observer pattern. Where is it used?**

The Observer pattern defines a one-to-many dependency where a subject maintains a list of observers and notifies them when its state changes. Observers register/deregister dynamically. It decouples the subject from the specific observers. Used in: GUI event handling (button click listeners), pub/sub messaging systems, MVC architecture (model notifies views), reactive programming (RxJS Observables), and distributed event systems.

**Q5: When would you use the Factory pattern vs the Builder pattern?**

Use the Factory pattern when you need to create objects of related types based on some condition, and construction is straightforward (few parameters). The factory hides the creation logic and returns an object matching an interface. Use the Builder pattern when constructing complex objects with many optional parameters. The builder provides a fluent API to set parameters step-by-step and validates the result at `build()` time. Factory answers "what type to create?" while Builder answers "how to configure a complex object?"

**Q6: What is the difference between the Adapter and Decorator patterns?**

Both are structural patterns involving wrapping. The Adapter converts one interface to another expected by the client -- it solves interface incompatibility without adding new behavior. The Decorator adds new responsibilities to an object dynamically while preserving its interface -- the wrapped object and the decorator share the same interface. Adapter is about compatibility; Decorator is about enhancement.

**Q7: Explain composition over inheritance. Why is it preferred?**

Inheritance creates a tight coupling between parent and child classes. Changes to the parent can break children (the fragile base class problem). Composition, where a class contains references to other objects and delegates work to them, is more flexible: components can be swapped at runtime, classes are easier to test in isolation, and you avoid the problems of deep inheritance hierarchies. For example, instead of `FlyingFish extends Fish` with a conflicting `Bird.fly()`, use `Fish` with a `FlyBehavior` component.

**Q8: What are the disadvantages of the Singleton pattern?**

(1) Global state makes the code harder to reason about and test (can't easily substitute a mock). (2) Hidden dependencies: classes using the singleton do not declare it as a dependency. (3) Violates Single Responsibility Principle (manages its own lifecycle + business logic). (4) Thread safety requires extra synchronization. (5) Makes parallel testing difficult since state persists across tests. (6) Tight coupling to the concrete singleton class. Alternatives: dependency injection with a single instance scope.

---

# 5. System Design

---

## 5.1 Scalability

### Vertical vs Horizontal Scaling

| Aspect | Vertical Scaling (Scale Up) | Horizontal Scaling (Scale Out) |
|---|---|---|
| Method | Add more CPU, RAM, disk to a single machine | Add more machines to the pool |
| Limit | Hardware ceiling (finite CPU/RAM per machine) | Virtually unlimited |
| Complexity | Simple (no code changes) | Complex (distributed systems challenges) |
| Cost | Expensive high-end hardware | Commodity hardware |
| Availability | Single point of failure | Redundancy built-in |
| Example | Upgrading a 32GB server to 256GB | Adding 10 more servers behind a load balancer |

### Key Scalability Concepts

| Concept | Description |
|---|---|
| **Stateless services** | Servers hold no client state; any server can handle any request. State is stored externally (database, cache, session store). |
| **Idempotency** | An operation can be applied multiple times without changing the result beyond the first application. Critical for retry-safe APIs. |
| **Partitioning** | Splitting data or workload across multiple nodes |
| **Replication** | Copying data across nodes for availability and read scaling |
| **Asynchronous processing** | Offload non-critical work to background queues |

---

## 5.2 Load Balancing

A **load balancer** distributes incoming requests across multiple backend servers to ensure no single server is overwhelmed.

### Load Balancing Algorithms

| Algorithm | Description | Best For |
|---|---|---|
| **Round Robin** | Rotate through servers sequentially | Servers with equal capacity |
| **Weighted Round Robin** | Like RR, but servers with higher weights get more requests | Heterogeneous server capacities |
| **Least Connections** | Route to the server with fewest active connections | Varying request durations |
| **Least Response Time** | Route to the server with lowest latency | Latency-sensitive applications |
| **IP Hash** | Hash client IP to determine server (sticky sessions) | Session affinity without external session store |
| **Consistent Hashing** | Hash-ring based distribution; minimal remapping on server add/remove | Distributed caches, stateful services |

### Load Balancer Types

| Layer | Type | Examines | Example |
|---|---|---|---|
| **Layer 4 (Transport)** | TCP/UDP level | IP + port, connection-level | AWS NLB, HAProxy (TCP mode) |
| **Layer 7 (Application)** | HTTP level | URL, headers, cookies, content | AWS ALB, Nginx, HAProxy (HTTP mode) |

Layer 7 load balancers can make smarter routing decisions (route `/api` to API servers, `/static` to CDN) but have more overhead.

### Health Checks

Load balancers periodically probe backend servers (HTTP GET to `/health`). Unhealthy servers are removed from the pool until they recover.

---

## 5.3 Caching

Caching stores frequently accessed data in a faster storage layer to reduce latency and backend load.

### Caching Strategies

| Strategy | Read | Write | Consistency | Use Case |
|---|---|---|---|---|
| **Cache-Aside (Lazy Loading)** | App checks cache first; on miss, reads from DB and populates cache | App writes to DB only; cache is populated on read miss | Eventually consistent | General purpose; most common |
| **Read-Through** | Cache itself fetches from DB on miss | Same as cache-aside but transparent to app | Eventually consistent | When cache library supports it |
| **Write-Through** | Same as cache-aside | App writes to cache, cache synchronously writes to DB | Strong (but write latency) | When consistency is critical |
| **Write-Behind (Write-Back)** | Same as cache-aside | App writes to cache, cache asynchronously writes to DB | Eventually consistent | Write-heavy workloads |
| **Write-Around** | Same as cache-aside | App writes to DB only, bypassing cache | Eventually consistent | Data rarely re-read after write |

### Cache Eviction Policies

| Policy | Description | Use Case |
|---|---|---|
| **LRU** (Least Recently Used) | Evicts the item not accessed for the longest time | General purpose (most common) |
| **LFU** (Least Frequently Used) | Evicts the item with the fewest accesses | Access frequency matters |
| **FIFO** (First In, First Out) | Evicts the oldest item | Simple, predictable |
| **TTL** (Time To Live) | Items expire after a set duration | Time-sensitive data (stock prices) |
| **Random** | Evicts a random item | Low-overhead option |

### Redis vs Memcached

| Feature | Redis | Memcached |
|---|---|---|
| Data structures | Strings, Lists, Sets, Hashes, Sorted Sets, Streams | Strings only |
| Persistence | RDB snapshots + AOF append-only file | None (pure cache) |
| Replication | Built-in (leader-follower) | None natively |
| Clustering | Redis Cluster (hash slots) | Client-side sharding |
| Pub/Sub | Yes | No |
| Lua scripting | Yes | No |
| Use case | Cache + data store + message broker | Pure high-speed caching |

### Cache Invalidation

"There are only two hard things in Computer Science: cache invalidation and naming things." -- Phil Karlton

| Approach | Description |
|---|---|
| **TTL-based** | Set expiry time; accept staleness within TTL |
| **Event-based** | Invalidate cache on write events (DB triggers, message queue) |
| **Versioning** | Append version to cache key; increment on update |

---

## 5.4 Content Delivery Network (CDN)

| Feature | Push CDN | Pull CDN |
|---|---|---|
| Content upload | Origin proactively pushes to edge servers | Edge servers fetch from origin on first request |
| Freshness | Content explicitly updated | Cache headers (TTL, ETag, Last-Modified) |
| Traffic | Low-traffic sites (upload everything once) | High-traffic sites (popular content cached automatically) |
| Storage cost | Higher (all content replicated) | Lower (only popular content cached) |

---

## 5.5 Message Queues

Message queues decouple producers from consumers, enabling asynchronous processing, load leveling, and fault tolerance.

### Point-to-Point vs Pub/Sub

| Model | Description | Example |
|---|---|---|
| **Point-to-Point (Queue)** | Each message is consumed by exactly one consumer | Task queues (job processing) |
| **Pub/Sub (Topics)** | Each message is broadcast to all subscribers | Notifications, event streaming |

### Kafka vs RabbitMQ

| Feature | Apache Kafka | RabbitMQ |
|---|---|---|
| Model | Distributed commit log | Traditional message broker |
| Ordering | Per-partition ordering | Per-queue FIFO |
| Delivery | Pull-based (consumers poll) | Push-based (broker pushes to consumers) |
| Retention | Configurable (time/size-based); messages persist | Messages deleted after consumption |
| Throughput | Very high (millions of messages/sec) | Moderate (tens of thousands/sec) |
| Use case | Event streaming, log aggregation, real-time pipelines | Task queues, RPC, request-reply patterns |

### Delivery Guarantees

| Guarantee | Description | Mechanism |
|---|---|---|
| **At-most-once** | Message may be lost, never duplicated | Fire and forget |
| **At-least-once** | Message is never lost but may be duplicated | Acknowledgments + retries; consumer must be idempotent |
| **Exactly-once** | Message is delivered exactly once | Transactional messaging + idempotent consumers (hard to achieve) |

---

## 5.6 Microservices vs Monolith

| Aspect | Monolith | Microservices |
|---|---|---|
| Deployment | Single deployable unit | Independent services deployed separately |
| Scaling | Scale the entire application | Scale individual services independently |
| Technology | Single tech stack | Polyglot (different languages/databases per service) |
| Complexity | Simpler initially | Distributed systems complexity (networking, consistency, observability) |
| Development | Easy to start; hard to maintain at scale | Hard to start; easier to maintain individual services |
| Data management | Single database | Database per service (data ownership) |
| Communication | In-process function calls | Network calls (HTTP/gRPC, message queues) |
| Testing | Easier end-to-end testing | Requires contract testing, integration testing |
| Failure handling | One bug can crash everything | Failures are isolated; need circuit breakers |

### Key Microservices Concepts

| Concept | Description |
|---|---|
| **API Gateway** | Single entry point that routes requests to appropriate services, handles auth, rate limiting, request aggregation |
| **Service Discovery** | Mechanism for services to find each other (Consul, Eureka, Kubernetes DNS) |
| **Circuit Breaker** | Prevents cascading failures by stopping requests to a failing service after a threshold |
| **Saga Pattern** | Manages distributed transactions as a sequence of local transactions with compensating actions |
| **Sidecar Pattern** | Attach utility processes (logging, monitoring, proxy) alongside each service container |
| **Strangler Fig** | Migrate from monolith to microservices incrementally by routing traffic to new services |

---

## 5.7 API Design

### REST Best Practices

| Practice | Description | Example |
|---|---|---|
| Use nouns for resources | URLs represent resources, not actions | `/users/123` not `/getUser?id=123` |
| Use HTTP methods as verbs | GET = read, POST = create, PUT = replace, PATCH = update, DELETE = remove | `DELETE /users/123` |
| Use plural nouns | Consistency | `/users` not `/user` |
| Nest for relationships | Sub-resources | `/users/123/orders` |
| Version the API | Backward compatibility | `/v1/users` or `Accept: application/vnd.api.v1+json` |
| Pagination | Limit response size | `?page=2&per_page=20` or cursor-based `?cursor=abc123` |
| Filtering/Sorting | Query parameters | `?status=active&sort=created_at:desc` |
| Idempotency keys | Safe retries for POST | `Idempotency-Key: abc-123` header |

### Rate Limiting Algorithms

| Algorithm | Description | Pros | Cons |
|---|---|---|---|
| **Token Bucket** | Tokens added at fixed rate; each request consumes a token | Allows bursts; smooth rate over time | Complexity in distributed setting |
| **Leaky Bucket** | Requests enter a queue processed at fixed rate | Smooth, consistent output rate | No burst handling |
| **Fixed Window** | Count requests in fixed time windows | Simple to implement | Burst at window boundaries (2x rate) |
| **Sliding Window Log** | Track timestamp of each request; count in sliding window | Accurate | Memory-intensive |
| **Sliding Window Counter** | Combine current + previous window counts weighted by overlap | Good accuracy with low memory | Slight approximation |

---

## 5.8 Consistent Hashing

Traditional hashing (`hash(key) % N`) requires remapping all keys when N changes. Consistent hashing maps both keys and nodes to a ring (0 to 2^32 - 1). Each key is assigned to the first node clockwise from its position.

**Benefits:**
- Adding/removing a node only affects K/N keys on average (K = total keys, N = nodes)
- Virtual nodes (multiple positions per physical node) ensure even distribution

```
        Node A
       /      \
  Key3          Key1
  |                |
  Node D      Node B
       \      /
        Key2
       Node C
```

**Used by:** Cassandra, DynamoDB, Memcached, CDN routing.

---

## 5.9 Back-of-the-Envelope Estimation

### Key Latency Numbers

| Operation | Latency |
|---|---|
| L1 cache reference | ~1 ns |
| L2 cache reference | ~4 ns |
| Main memory reference | ~100 ns |
| SSD random read | ~16 μs |
| HDD random read | ~2-10 ms |
| Round trip within datacenter | ~500 μs |
| Round trip cross-continent | ~150 ms |
| Read 1 MB sequentially from memory | ~3 μs |
| Read 1 MB sequentially from SSD | ~50 μs |
| Read 1 MB sequentially from HDD | ~825 μs |

### Power of Two Approximations

| Power | Exact | Approx | Name |
|---|---|---|---|
| 2^10 | 1,024 | ~1 thousand | 1 KB |
| 2^20 | 1,048,576 | ~1 million | 1 MB |
| 2^30 | 1,073,741,824 | ~1 billion | 1 GB |
| 2^40 | ~1.1 × 10^12 | ~1 trillion | 1 TB |

### Common Estimations

| Metric | Estimate |
|---|---|
| QPS for a web server | ~1,000-10,000 (single server) |
| Daily active users × avg requests | Total daily requests |
| 1 day = 86,400 seconds | ~100,000 seconds (for easy math) |
| 1 million requests/day | ~12 QPS |
| 100 million requests/day | ~1,200 QPS |
| Average tweet/post size | ~250 bytes text + metadata ≈ 1 KB |
| Image | 200 KB - 2 MB |
| Video (1 min, 720p) | ~50 MB |

---

## 5.10 System Design -- Interview Questions

**Q1: Design a URL shortening service (like bit.ly).**

**Requirements:** Given a long URL, generate a short URL. Given a short URL, redirect to the original. Handle high read volume.

**Design:** Use a hash/counter to generate a unique 7-character base62 key (62^7 ≈ 3.5 trillion URLs). Store the mapping (shortKey → longURL) in a database. On read, look up the key and return a 301/302 redirect. Use a distributed key-value store (DynamoDB) or relational DB with the short key as primary key. Add a cache layer (Redis) for hot URLs. For ID generation, use a distributed ID generator (Twitter Snowflake) or a counter with a coordination service. Rate limit the creation endpoint. Analytics: log access with timestamps for click tracking.

**Scale:** Read-heavy (100:1 read-to-write). Cache absorbs most reads. Shard by short key hash. Replicate database for availability.

**Q2: Design a rate limiter.**

**Requirements:** Limit API requests per user/IP to N requests per time window. Return 429 Too Many Requests when exceeded.

**Design:** For a single server, use a token bucket per client (stored in a hash map). For distributed rate limiting, use Redis with atomic operations: store a counter per client with TTL matching the time window. `INCR client:{id}` and `EXPIRE client:{id} window_seconds`. If count exceeds limit, reject. For sliding window accuracy, use a sorted set of timestamps per client, removing entries older than the window before counting. Place the rate limiter as middleware before the application logic.

**Q3: How would you design a chat system like WhatsApp?**

**Core components:** (1) Chat servers handling WebSocket connections for real-time messaging. (2) User presence service tracking online/offline status. (3) Message store (Cassandra -- write-heavy, partitioned by conversation ID) for persistence. (4) Push notification service for offline users. (5) Media storage (S3 + CDN) for images/videos. (6) Group service managing group membership. **Flow:** Client opens WebSocket to a chat server. On send, the server stores the message and forwards it to the recipient's chat server (or queues it if offline). Delivery receipts and read receipts use the same channel. End-to-end encryption: use Signal Protocol (key exchange per conversation, message-level encryption).

**Q4: Explain caching strategies. When would you use write-through vs cache-aside?**

Cache-aside (lazy loading) is the most common: the application checks the cache, on miss reads from DB and populates the cache. The cache only contains data that has been requested. Use for read-heavy workloads where not all data needs to be cached. Write-through writes to cache and DB simultaneously, ensuring the cache is always consistent. Use when you cannot tolerate serving stale data (e.g., shopping cart, inventory counts). The tradeoff is higher write latency. Write-behind (write-back) writes to cache immediately and asynchronously flushes to DB, providing low write latency but risking data loss if the cache fails before flushing.

**Q5: What is consistent hashing and why is it useful?**

Consistent hashing maps both data keys and server nodes onto a circular hash ring. Each key is assigned to the first server encountered clockwise on the ring. When a server is added or removed, only the keys between the affected server and its predecessor need to be remapped -- approximately K/N keys (where K is total keys and N is nodes), compared to rehashing all keys with simple modular hashing. Virtual nodes (multiple positions per physical server) improve load balance. Used in distributed caches (Memcached), databases (Cassandra, DynamoDB), CDNs, and load balancers.

**Q6: Compare monolith vs microservices architectures.**

A monolith packages all functionality into a single deployable unit. It is simpler to develop, test, and deploy initially, but becomes hard to scale and maintain as it grows -- a change in one module requires redeploying everything. Microservices decompose the application into independently deployable services, each owning its data. Benefits: independent scaling, technology diversity, fault isolation, team autonomy. Costs: distributed systems complexity (network latency, partial failures), data consistency challenges, operational overhead (monitoring, tracing, service discovery). Start with a monolith; extract microservices when specific scaling or organizational needs arise (the "monolith-first" approach).

**Q7: How do you handle distributed transactions across microservices?**

The Saga pattern replaces a single distributed transaction with a sequence of local transactions, each with a compensating action for rollback. Two coordination approaches: (1) **Choreography** -- each service publishes events that trigger the next step; decentralized but hard to track. (2) **Orchestration** -- a central coordinator directs the saga steps; easier to manage but introduces a single point of coordination. For example, an order saga: Create Order → Reserve Inventory → Process Payment → Ship. If payment fails, compensate: Release Inventory → Cancel Order. Sagas provide eventual consistency rather than ACID guarantees.

---

# 6. Concurrency and Multithreading

---

## 6.1 Threads vs Processes

| Aspect | Process | Thread |
|---|---|---|
| Address space | Separate | Shared within process |
| Creation overhead | High (new address space, page tables) | Low (shared address space, new stack + registers) |
| Communication | IPC (pipes, sockets, shared memory) | Direct shared memory |
| Context switch | Expensive (TLB flush, cache pollution) | Cheap (same address space) |
| Fault isolation | High (process crash is isolated) | Low (thread crash affects all threads) |

**Thread memory model:**

```
┌─────────────────────────────────────────┐
│              Process                     │
│  ┌──────────────────────────────────┐   │
│  │         Shared Memory             │   │
│  │  Code | Global Data | Heap        │   │
│  │  Open Files | Signal Handlers     │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Thread 1 │  │ Thread 2 │  │Thread 3││
│  │ Stack    │  │ Stack    │  │Stack   ││
│  │ Registers│  │ Registers│  │Registers││
│  │ PC       │  │ PC       │  │PC      ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
```

---

## 6.2 Synchronization Primitives

### Mutex (Mutual Exclusion Lock)

A binary lock that provides exclusive access to a critical section. Only the thread that acquired the lock can release it (ownership semantics).

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:          # acquire and auto-release
        counter += 1    # critical section
```

```cpp
#include <mutex>
std::mutex mtx;
int counter = 0;

void increment() {
    std::lock_guard<std::mutex> guard(mtx);
    counter++;          // critical section
}
```

### Semaphore

A counter-based synchronization primitive. `wait()` (P) decrements the counter; if it would go below 0, the thread blocks. `signal()` (V) increments the counter, potentially unblocking a waiting thread.

| Type | Counter Range | Use Case |
|---|---|---|
| Binary Semaphore | 0 or 1 | Similar to mutex (but no ownership) |
| Counting Semaphore | 0 to N | Limit concurrent access (e.g., connection pool of size N) |

```python
import threading

pool = threading.Semaphore(5)  # max 5 concurrent connections

def use_connection():
    with pool:
        # at most 5 threads here concurrently
        access_database()
```

### Condition Variable

Allows threads to wait for a specific condition to become true. Always used with a mutex. A waiting thread releases the mutex and sleeps until signaled.

```python
import threading

queue = []
cond = threading.Condition()

def producer():
    with cond:
        queue.append(item)
        cond.notify()       # wake one waiting consumer

def consumer():
    with cond:
        while not queue:    # always use while, not if (spurious wakeups)
            cond.wait()     # release lock and sleep
        item = queue.pop(0)
```

### Read-Write Lock (RWLock)

Allows concurrent reads but exclusive writes. Multiple readers can hold the lock simultaneously, but a writer must have exclusive access.

| Scenario | Allowed |
|---|---|
| Multiple readers, no writer | Yes |
| One writer, no readers | Yes |
| Reader + writer simultaneously | No |
| Multiple writers simultaneously | No |

**Use:** Read-heavy data structures (caches, configuration stores).

### Monitor

A high-level synchronization construct that encapsulates a mutex, condition variables, and the shared data they protect into a single unit. Java's `synchronized` keyword implements monitors.

---

## 6.3 Race Conditions and Critical Sections

A **race condition** occurs when the behavior of a program depends on the relative timing of events (e.g., thread scheduling), and the outcome is incorrect for some interleavings.

A **critical section** is a code segment that accesses shared resources and must not be executed by more than one thread at a time.

**Classic race condition example:**

```
Thread A: read counter (0)
Thread B: read counter (0)
Thread A: counter = 0 + 1 = 1, write counter
Thread B: counter = 0 + 1 = 1, write counter
Result: counter = 1 (expected 2)
```

**Prevention:** Use mutexes, atomic operations, or lock-free algorithms to protect critical sections.

### Atomic Operations

Operations that complete entirely or not at all, with no visible intermediate state. Hardware-supported (e.g., compare-and-swap, fetch-and-add).

```python
# Python: no built-in atomics, use threading.Lock
# or use queue.Queue (thread-safe)
```

```cpp
#include <atomic>
std::atomic<int> counter{0};

void increment() {
    counter.fetch_add(1, std::memory_order_relaxed);
}
```

---

## 6.4 Deadlock, Livelock, and Starvation

| Problem | Description | Example |
|---|---|---|
| **Deadlock** | Two or more threads are blocked forever, each waiting for a resource held by another | Thread A holds Lock1, waits for Lock2; Thread B holds Lock2, waits for Lock1 |
| **Livelock** | Threads are not blocked but continuously change state in response to each other, making no progress | Two people in a hallway, each stepping aside in the same direction repeatedly |
| **Starvation** | A thread is perpetually denied access to a resource because other threads are always preferred | Low-priority thread never gets CPU time due to continuous high-priority arrivals |

### Deadlock Prevention Strategies

| Strategy | Approach |
|---|---|
| **Lock ordering** | Always acquire locks in the same global order (prevents circular wait) |
| **Lock timeout** | Attempt to acquire lock with timeout; back off and retry if failed |
| **Try-lock** | Use non-blocking lock attempts (`tryLock()`); release all and retry if any fails |
| **Single lock** | Use one coarse-grained lock (trades parallelism for simplicity) |
| **Lock-free algorithms** | Use atomic compare-and-swap instead of locks |

---

## 6.5 Classic Concurrency Problems

### Producer-Consumer (Bounded Buffer)

Producers add items to a shared buffer; consumers remove them. The buffer has a fixed capacity.

```python
import threading, queue

buffer = queue.Queue(maxsize=10)

def producer():
    while True:
        item = produce_item()
        buffer.put(item)      # blocks if full

def consumer():
    while True:
        item = buffer.get()   # blocks if empty
        process(item)
```

**Synchronization needs:** Mutex (protect buffer), empty semaphore (count empty slots), full semaphore (count filled slots). Python's `queue.Queue` handles all of this internally.

### Readers-Writers Problem

Multiple readers can read simultaneously, but writers need exclusive access.

| Variant | Priority | Risk |
|---|---|---|
| **First readers-writers** | Readers have priority | Writers may starve |
| **Second readers-writers** | Writers have priority | Readers may starve |
| **Third (fair)** | FIFO ordering | No starvation; moderate throughput |

### Dining Philosophers

Five philosophers sit at a table with five forks. Each needs two forks to eat. A naive solution can deadlock (everyone picks up their left fork).

**Solutions:**
1. **Resource ordering:** Number the forks; always pick up the lower-numbered fork first
2. **Arbitrator:** A waiter/mutex permits only 4 philosophers to attempt eating at once
3. **Chandy-Misra:** Request-based solution using message passing (tokens on forks)

---

## 6.6 Thread Pools and Executors

A **thread pool** maintains a fixed number of worker threads that process tasks from a shared queue. Avoids the overhead of creating/destroying threads per task.

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process, item) for item in items]
    results = [f.result() for f in futures]
```

```cpp
// C++17: no standard thread pool, but common pattern:
// Use a queue of std::function + N worker threads
// or use std::async with a custom executor
```

**Sizing the thread pool:**
- **CPU-bound tasks:** Number of threads ≈ number of CPU cores
- **I/O-bound tasks:** Number of threads ≈ cores × (1 + wait_time/compute_time). Can be much larger since threads spend most time blocked on I/O.

---

## 6.7 Async/Await and Event Loops

### Event-Driven (Single-Threaded) Concurrency

An **event loop** runs on a single thread, processing events from a queue. When an I/O operation is needed, it is dispatched non-blocking, and a callback (or coroutine resumption) is registered for completion.

```python
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    results = await asyncio.gather(
        fetch_data("https://api.example.com/a"),
        fetch_data("https://api.example.com/b"),
        fetch_data("https://api.example.com/c"),
    )

asyncio.run(main())
```

### Threads vs Async

| Aspect | Threads | Async/Await |
|---|---|---|
| Concurrency model | Preemptive (OS schedules) | Cooperative (coroutines yield explicitly) |
| Overhead per task | ~1 MB stack per thread | ~KB per coroutine |
| Scalability | Hundreds to low thousands of threads | Tens of thousands of coroutines |
| CPU-bound work | Can utilize multiple cores | Single-threaded; blocks the event loop |
| I/O-bound work | Works but overhead per thread | Ideal; low overhead |
| Synchronization | Mutexes, locks needed | Generally not needed (single-threaded) |
| Debugging | Hard (non-deterministic scheduling) | Easier (deterministic coroutine switching) |

---

## 6.8 Lock-Free and Wait-Free Data Structures

### Compare-And-Swap (CAS)

An atomic hardware instruction that updates a value only if it matches the expected value:

```
CAS(address, expected, new_value):
    atomically:
        if *address == expected:
            *address = new_value
            return true
        else:
            return false
```

**Lock-free:** At least one thread makes progress in a finite number of steps (other threads may starve temporarily).

**Wait-free:** Every thread makes progress in a bounded number of steps (strongest guarantee, hardest to implement).

**Example: Lock-free stack (Treiber Stack):**

```cpp
struct Node { int val; Node* next; };
std::atomic<Node*> head{nullptr};

void push(int val) {
    Node* new_node = new Node{val, nullptr};
    do {
        new_node->next = head.load();
    } while (!head.compare_exchange_weak(new_node->next, new_node));
}
```

### The ABA Problem

CAS can be fooled if a value changes from A→B→A. The thread sees "A" and thinks nothing changed, but the underlying data structure may have been modified. Solution: add a version counter to the pointer (tagged pointers).

---

## 6.9 Memory Models and Visibility

### Java/C++ Memory Model Concepts

| Concept | Description |
|---|---|
| **Happens-before** | If action A happens-before action B, then the effects of A are visible to B. Establishes ordering guarantees. |
| **Volatile (Java) / atomic (C++)** | Variables marked volatile/atomic are always read from/written to main memory, not cached in CPU registers. Provides visibility guarantees. |
| **Memory ordering** | `memory_order_relaxed` (no ordering), `memory_order_acquire/release` (synchronize-with), `memory_order_seq_cst` (total order -- default and safest) |
| **Memory barrier / fence** | Hardware instruction that prevents the CPU from reordering reads/writes across the barrier |

### Python's GIL (Global Interpreter Lock)

The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time, even on multi-core machines.

| Aspect | Detail |
|---|---|
| **What it protects** | CPython's reference counting memory management |
| **Impact on CPU-bound** | Only one core utilized; threading provides no speedup |
| **Impact on I/O-bound** | Threads still useful (GIL released during I/O waits) |
| **Workaround for CPU-bound** | Use `multiprocessing` (separate processes), C extensions (release GIL), `concurrent.futures.ProcessPoolExecutor` |
| **Alternative interpreters** | PyPy, Jython, GraalPy (different GIL strategies) |
| **Python 3.13+** | Free-threaded CPython build available (experimental, no GIL) |

---

## 6.10 Concurrency and Multithreading -- Interview Questions

**Q1: What is a race condition? How do you prevent it?**

A race condition occurs when multiple threads access shared data concurrently and the outcome depends on the non-deterministic order of execution. For example, two threads incrementing a counter without synchronization can read the same value and write back the same incremented value, losing one update. Prevention methods: (1) Mutexes/locks to serialize access to critical sections. (2) Atomic operations for simple read-modify-write operations. (3) Thread-safe data structures (concurrent hash maps, lock-free queues). (4) Immutable data (if data never changes, no synchronization needed). (5) Thread confinement (each thread owns its data).

**Q2: Explain the difference between a mutex and a semaphore.**

A mutex is a binary lock with ownership -- only the thread that locked it can unlock it. It is used for mutual exclusion (protecting a critical section). A semaphore is a counter that can be incremented (signal/V) and decremented (wait/P) by any thread. A counting semaphore initialized to N allows up to N threads to enter the critical section concurrently (e.g., connection pool). A binary semaphore (N=1) behaves similarly to a mutex but lacks ownership semantics -- any thread can signal it, making it suitable for signaling between threads rather than mutual exclusion.

**Q3: What is a deadlock? Give an example and how to avoid it.**

A deadlock occurs when two or more threads are permanently blocked, each waiting for a resource held by another, forming a circular dependency. Example: Thread A acquires Lock1 and waits for Lock2; Thread B acquires Lock2 and waits for Lock1. Avoidance: (1) Lock ordering -- always acquire locks in the same predefined order. (2) Lock timeout -- use `tryLock()` with a timeout and retry. (3) Minimize locking scope -- hold locks for the shortest time possible. (4) Use lock-free algorithms where applicable.

**Q4: What is the Python GIL and how does it affect multithreading?**

The GIL (Global Interpreter Lock) is a mutex in CPython that ensures only one thread executes Python bytecode at a time. For CPU-bound tasks, Python threads cannot achieve true parallelism on multiple cores -- the GIL serializes execution, and multithreading may even be slower due to context-switching overhead. For I/O-bound tasks, threads are still effective because the GIL is released while waiting for I/O operations (network, disk). For CPU-bound parallelism, use `multiprocessing` (spawns separate processes each with their own GIL), or write performance-critical code in C/C++ extensions that release the GIL.

**Q5: Explain async/await. How is it different from multithreading?**

Async/await provides cooperative concurrency on a single thread using coroutines and an event loop. When a coroutine hits an `await` (typically an I/O operation), it yields control to the event loop, which can run other coroutines. This is different from threads in several ways: (1) No preemption -- coroutines yield voluntarily, eliminating race conditions on shared state. (2) Lower overhead -- coroutines use kilobytes of memory vs megabytes for thread stacks. (3) Higher scalability -- can handle tens of thousands of concurrent I/O operations. (4) Not suitable for CPU-bound work -- a CPU-intensive coroutine blocks the entire event loop. Use async for I/O-bound servers (web servers, API clients); use threads/processes for CPU-bound work.

**Q6: What is the Producer-Consumer problem? How do you solve it?**

The Producer-Consumer problem involves producers creating data items and placing them into a shared bounded buffer, while consumers remove and process them. Synchronization challenges: producers must wait if the buffer is full; consumers must wait if it is empty; access to the buffer must be mutually exclusive. Solution: Use a mutex to protect the buffer, a "not full" condition/semaphore for producers, and a "not empty" condition/semaphore for consumers. In Python, `queue.Queue` provides a thread-safe bounded queue with blocking `put()` and `get()`. In Java, `BlockingQueue` implementations handle all synchronization.

**Q7: What are lock-free data structures? When would you use them?**

Lock-free data structures use atomic operations (primarily compare-and-swap) instead of locks to manage concurrent access. They guarantee that at least one thread always makes progress, even if other threads are delayed or preempted -- unlike locks, where a thread holding a lock can block everyone. Use them when: (1) Lock contention is high and you need maximum throughput. (2) You need to avoid priority inversion and deadlocks. (3) You cannot tolerate the latency spikes caused by lock contention. Examples: lock-free queues, stacks (Treiber Stack), and hash maps. Tradeoffs: much harder to implement correctly, prone to subtle bugs (ABA problem), and may not be faster than well-tuned locks under low contention.

**Q8: How do you choose the size of a thread pool?**

For CPU-bound tasks, the optimal thread count is approximately equal to the number of CPU cores (more threads cause excessive context switching without benefit). For I/O-bound tasks, use more threads since they spend most time blocked: threads ≈ cores × (1 + wait_time/compute_time). If threads spend 90% of time waiting on I/O, you could use 10× the core count. For mixed workloads, separate CPU-bound and I/O-bound work into different thread pools. Always measure and tune based on actual performance under realistic load -- theoretical formulas are starting points, not final answers.

---

# 7. Computer Architecture

---

## 7.1 CPU Basics

### Components of a CPU

| Component | Function |
|---|---|
| **ALU (Arithmetic Logic Unit)** | Performs arithmetic (+, -, ×, ÷) and logical (AND, OR, NOT, XOR, shift) operations |
| **Control Unit (CU)** | Fetches instructions, decodes them, coordinates execution by generating control signals |
| **Registers** | Small, ultra-fast storage locations inside the CPU (e.g., PC, IR, MAR, MDR, general-purpose registers) |
| **Cache** | Small, fast memory (SRAM) close to the CPU to reduce main memory access latency |
| **Bus Interface** | Connects CPU to external memory and I/O via data bus, address bus, and control bus |

### Key Registers

| Register | Purpose |
|---|---|
| **PC (Program Counter)** | Address of the next instruction to fetch |
| **IR (Instruction Register)** | Holds the currently executing instruction |
| **MAR (Memory Address Register)** | Holds the memory address to read from or write to |
| **MDR (Memory Data Register)** | Holds data fetched from or to be written to memory |
| **SP (Stack Pointer)** | Points to the top of the current stack frame |
| **PSW / Flags Register** | Status flags: Zero, Carry, Overflow, Sign, Parity |
| **General Purpose (GPRs)** | Operand storage for computations (e.g., x86: EAX, EBX, ECX, EDX; ARM: R0-R15) |

### Instruction Cycle (Fetch-Decode-Execute)

```
┌─────────┐     ┌──────────┐     ┌──────────┐
│  Fetch   │────▶│  Decode  │────▶│ Execute  │
│          │     │          │     │          │
│ PC → MAR │     │ IR → CU  │     │ ALU ops  │
│ Memory → │     │ Identify │     │ Memory   │
│ IR       │     │ operands │     │ access   │
│ PC++     │     │          │     │ Write    │
└─────────┘     └──────────┘     │ back     │
     ▲                            └──────────┘
     │                                 │
     └─────────────────────────────────┘
```

---

## 7.2 Instruction Set Architecture (ISA)

The ISA defines the interface between software and hardware: the set of instructions the CPU can execute, data types, registers, addressing modes, and memory architecture.

### RISC vs CISC

| Aspect | RISC (Reduced Instruction Set Computer) | CISC (Complex Instruction Set Computer) |
|---|---|---|
| Philosophy | Simple instructions, each executes in one clock cycle | Complex instructions that can do multi-step operations |
| Instructions | Fixed length, few formats | Variable length, many formats |
| Registers | Many general-purpose registers (32+) | Fewer registers |
| Memory access | Load/store architecture (only load/store access memory) | Any instruction can access memory |
| Pipelining | Easy to pipeline (uniform instruction format) | Harder to pipeline (variable-length instructions) |
| Compiler role | Compiler does more optimization | Hardware does more work |
| Examples | ARM, RISC-V, MIPS, SPARC | x86, x86-64 (internally translates to micro-ops, which are RISC-like) |
| Power efficiency | Lower power consumption | Higher power consumption |
| Dominance | Mobile, embedded, servers (ARM) | Desktop, laptop, servers (x86) |

### x86 vs ARM

| Feature | x86/x86-64 | ARM |
|---|---|---|
| ISA type | CISC (with RISC-like internals) | RISC |
| Dominant market | Desktop, laptop, servers | Mobile, embedded, increasingly servers/laptops |
| Power efficiency | Higher power draw | Very power-efficient |
| Notable products | Intel Core, AMD Ryzen/EPYC | Apple M-series, Qualcomm Snapdragon, AWS Graviton |
| Backward compatibility | Extensive (decades of x86 code) | Less legacy burden |

---

## 7.3 Pipelining

Pipelining overlaps the execution of multiple instructions, like an assembly line. While one instruction is being executed, the next is being decoded, and the one after that is being fetched.

### Classic 5-Stage Pipeline

| Stage | Abbreviation | Function |
|---|---|---|
| 1. Instruction Fetch | IF | Read instruction from memory at address in PC |
| 2. Instruction Decode | ID | Decode instruction, read register operands |
| 3. Execute | EX | ALU operation, address calculation |
| 4. Memory Access | MEM | Read from or write to data memory |
| 5. Write Back | WB | Write result back to register file |

```
Time →       1    2    3    4    5    6    7    8
Instr 1:    IF   ID   EX  MEM   WB
Instr 2:         IF   ID   EX  MEM   WB
Instr 3:              IF   ID   EX  MEM   WB
Instr 4:                   IF   ID   EX  MEM   WB
```

**Throughput:** In steady state, one instruction completes per clock cycle (though each instruction still takes 5 cycles of latency).

### Pipeline Hazards

| Hazard Type | Cause | Solution |
|---|---|---|
| **Data Hazard** | An instruction depends on the result of a previous instruction that hasn't completed | **Forwarding/Bypassing:** route results directly from EX/MEM to the next instruction's inputs. **Stalling:** insert a pipeline bubble (NOP) until data is available. |
| **Control Hazard** | Branch instructions change the PC; subsequent instructions may be wrong | **Branch prediction:** guess whether branch is taken (static or dynamic). **Branch delay slot:** always execute the instruction after the branch (MIPS). **Speculative execution:** execute predicted path, roll back if wrong. |
| **Structural Hazard** | Two instructions need the same hardware resource simultaneously | **Resource duplication:** separate instruction and data memories/caches. **Stalling.** |

### Branch Prediction

| Type | Method | Accuracy |
|---|---|---|
| **Static** | Predict always taken or always not-taken | ~60-70% |
| **1-bit predictor** | Remember last outcome | Poor for alternating branches |
| **2-bit predictor** | State machine: must mispredict twice to change direction | ~85-90% |
| **Tournament predictor** | Multiple predictors vote (local + global history) | ~95%+ |
| **Neural (perceptron)** | ML-based branch prediction | ~97%+ (modern CPUs) |

**Misprediction penalty:** The pipeline must be flushed and restarted from the correct path. Deeper pipelines have higher penalties (10-20+ cycles on modern CPUs).

---

## 7.4 Memory Hierarchy

```
            ┌──────────────┐
            │  Registers   │  ~1 ns,    bytes,     most expensive
            ├──────────────┤
            │   L1 Cache   │  ~1 ns,    32-64 KB
            ├──────────────┤
            │   L2 Cache   │  ~4 ns,    256 KB-1 MB
            ├──────────────┤
            │   L3 Cache   │  ~10 ns,   2-64 MB
            ├──────────────┤
            │  Main Memory │  ~100 ns,  8-256 GB
            │   (DRAM)     │
            ├──────────────┤
            │     SSD      │  ~16 μs,   256 GB-4 TB
            ├──────────────┤
            │     HDD      │  ~2-10 ms, 1-20 TB,   least expensive
            └──────────────┘
```

**Key insight:** Each level is larger but slower. The hierarchy exploits **locality of reference** to keep frequently accessed data close to the CPU.

---

## 7.5 Cache

### Locality of Reference

| Type | Description | Example |
|---|---|---|
| **Temporal locality** | Recently accessed data will likely be accessed again soon | Loop variables, hot code paths |
| **Spatial locality** | Data near recently accessed addresses will likely be accessed soon | Array traversal, sequential instruction execution |

### Cache Organization

| Term | Description |
|---|---|
| **Cache line (block)** | Unit of data transfer between cache and memory (typically 64 bytes) |
| **Tag** | Identifies which memory block is stored in a cache line |
| **Set** | A group of cache lines that a memory address can map to |
| **Way** | Number of cache lines per set (associativity) |

### Cache Associativity

| Type | Description | Tradeoff |
|---|---|---|
| **Direct-mapped** | Each memory block maps to exactly one cache line | Fast lookup; high conflict misses |
| **N-way set-associative** | Each block maps to one of N lines in a set | Balanced (most common: 8-way, 16-way) |
| **Fully associative** | A block can go in any cache line | Fewest misses; expensive to search |

### Cache Write Policies

| Policy | On Write Hit | On Write Miss |
|---|---|---|
| **Write-through** | Write to cache and memory simultaneously | Write-allocate or write-no-allocate |
| **Write-back** | Write to cache only; mark line as "dirty"; write to memory on eviction | Write-allocate (fetch block into cache, then write) |

Write-back is more common because it reduces memory bus traffic.

### Cache Misses (3 C's)

| Type | Cause | Mitigation |
|---|---|---|
| **Compulsory (cold)** | First access to a block | Prefetching |
| **Capacity** | Cache too small to hold the working set | Larger cache |
| **Conflict** | Multiple blocks map to the same set (associativity limit) | Higher associativity |

### Cache Coherence (MESI Protocol)

In multi-core systems, each core has its own cache. If core A modifies a cache line that core B also has cached, the caches become inconsistent. The MESI protocol maintains coherence:

| State | Meaning |
|---|---|
| **Modified** | Cache line has been modified; only this cache has the valid copy; memory is stale |
| **Exclusive** | Cache line matches memory; only this cache has a copy |
| **Shared** | Cache line matches memory; other caches may also have copies |
| **Invalid** | Cache line is not valid; must be fetched from memory or another cache |

**False sharing:** Two cores modify different variables that happen to share the same cache line. This causes the cache line to bounce between cores (invalidation traffic) even though there is no logical data sharing. Solution: pad data structures so unrelated fields are on different cache lines.

---

## 7.6 Virtual Memory

### Page Tables

Virtual memory maps virtual addresses to physical addresses using **page tables**. Each process has its own page table.

```
Virtual Address: [ Virtual Page Number (VPN) | Page Offset ]
                         │
                    Page Table
                         │
                         ▼
Physical Address: [ Physical Frame Number (PFN) | Page Offset ]
```

**Multi-level page tables** reduce memory overhead by only allocating page table entries for address ranges actually in use. x86-64 uses a 4-level page table (PML4 → PDPT → PD → PT).

### TLB (Translation Lookaside Buffer)

A hardware cache of recent virtual-to-physical translations. A TLB miss requires a page table walk (multiple memory accesses). TLB is typically:

- L1 TLB: 64-128 entries, 1-cycle access
- L2 TLB: 512-2048 entries, ~10-cycle access

**Context switches flush the TLB** (or use ASID -- Address Space Identifier -- to tag entries per process, avoiding flushes).

### Page Faults

| Type | Cause | Action |
|---|---|---|
| **Minor (soft)** | Page is in memory but not mapped in page table | Update page table entry (no disk I/O) |
| **Major (hard)** | Page is not in memory (on disk/swap) | Load page from disk; very expensive (~ms) |
| **Invalid** | Access to unmapped address | Segmentation fault (SIGSEGV) |

---

## 7.7 Storage

### HDD vs SSD

| Feature | HDD (Hard Disk Drive) | SSD (Solid State Drive) |
|---|---|---|
| Technology | Spinning magnetic platters + read/write head | NAND flash memory (no moving parts) |
| Random read latency | 2-10 ms (seek time + rotational delay) | ~16 μs |
| Sequential throughput | 100-200 MB/s | 500-7000 MB/s (NVMe) |
| IOPS (random) | ~100-200 | 10,000-1,000,000 |
| Durability | Susceptible to shock/vibration | Shock-resistant; limited write endurance (TBW) |
| Power | Higher | Lower |
| Cost per GB | Lower | Higher (decreasing) |
| Use case | Bulk storage, backups, archives | OS drives, databases, hot data |

### Storage Interfaces

| Interface | Max Bandwidth | Protocol |
|---|---|---|
| SATA III | 600 MB/s | AHCI |
| NVMe (PCIe 4.0 x4) | ~7,000 MB/s | NVMe |
| NVMe (PCIe 5.0 x4) | ~14,000 MB/s | NVMe |

---

## 7.8 Parallelism

| Level | Description | Example |
|---|---|---|
| **Bit-level** | Increasing word size reduces the number of instructions | 64-bit arithmetic vs 32-bit |
| **ILP (Instruction-Level)** | Execute multiple independent instructions simultaneously | Pipelining, superscalar execution, out-of-order execution |
| **Data-level (SIMD)** | Same operation on multiple data elements simultaneously | SSE/AVX vector instructions processing 8 floats at once |
| **Thread-level** | Multiple threads on multiple cores | Multi-core CPUs, SMT (Hyper-Threading) |
| **Task-level** | Distribute independent tasks across machines | MapReduce, distributed computing |

### GPU Computing

GPUs have thousands of simple cores optimized for data-parallel workloads. A GPU excels when the same operation must be applied to millions of data elements independently.

| Aspect | CPU | GPU |
|---|---|---|
| Cores | Few, powerful (4-64) | Many, simple (thousands) |
| Optimized for | Low-latency, serial/complex tasks | High-throughput, data-parallel tasks |
| Use cases | OS, applications, control flow | Graphics, ML training, scientific computing |

---

## 7.9 Endianness and Floating Point

### Endianness

| Format | Byte Order | Used By |
|---|---|---|
| **Big-endian** | Most significant byte at lowest address | Network protocols (network byte order), SPARC, some ARM modes |
| **Little-endian** | Least significant byte at lowest address | x86, x86-64, ARM (default), RISC-V |

**Example:** The 32-bit integer `0x12345678` stored at address 0x00:

```
Big-endian:    [0x00]=12  [0x01]=34  [0x02]=56  [0x03]=78
Little-endian: [0x00]=78  [0x01]=56  [0x02]=34  [0x03]=12
```

**Matters when:** Parsing binary file formats, network protocols, cross-platform data exchange.

### IEEE 754 Floating Point

| Format | Total Bits | Sign | Exponent | Mantissa | Range |
|---|---|---|---|---|---|
| **Single (float)** | 32 | 1 | 8 | 23 | ±3.4 × 10^38, ~7 decimal digits |
| **Double** | 64 | 1 | 11 | 52 | ±1.8 × 10^308, ~15 decimal digits |

**Value:** (-1)^sign × 1.mantissa × 2^(exponent - bias)

**Key pitfalls:**
- `0.1 + 0.2 ≠ 0.3` (representation error)
- Comparing floats with `==` is unreliable; use epsilon-based comparison
- Special values: +0, -0, +∞, -∞, NaN (Not a Number)
- NaN ≠ NaN (by IEEE 754 definition)
- Catastrophic cancellation: subtracting nearly equal numbers loses significant digits

---

## 7.10 Computer Architecture -- Interview Questions

**Q1: Explain the memory hierarchy. Why does it exist?**

The memory hierarchy arranges storage in tiers from small/fast/expensive (registers) to large/slow/cheap (disk). It exists because there is a fundamental tradeoff between speed, size, and cost in memory technology. Registers are fastest but hold only bytes. SRAM (cache) is fast but expensive per bit. DRAM (main memory) is slower but cheaper and denser. Disk storage is cheapest but orders of magnitude slower. The hierarchy exploits locality of reference -- programs tend to access the same data (temporal locality) and nearby data (spatial locality) repeatedly. By keeping recently and frequently accessed data in faster tiers, the system achieves average access times close to the fastest tier while providing the capacity of the largest tier.

**Q2: What is a cache miss? Explain the 3 C's.**

A cache miss occurs when the CPU requests data that is not present in the cache, requiring a slower access to the next level of the hierarchy. The three C's categorize miss causes: (1) **Compulsory** (cold) misses occur on the first access to a block -- unavoidable but reduced by prefetching. (2) **Capacity** misses occur when the working set exceeds the cache size -- the cache cannot hold all needed data. (3) **Conflict** misses occur in set-associative or direct-mapped caches when multiple blocks compete for the same set -- increased associativity reduces these.

**Q3: What is pipelining? What are pipeline hazards?**

Pipelining overlaps the execution of multiple instructions by dividing the instruction cycle into stages (fetch, decode, execute, memory, writeback). In steady state, one instruction completes per clock cycle, increasing throughput (though individual instruction latency remains the same). Hazards are situations that prevent the next instruction from executing: Data hazards occur when an instruction depends on the result of a prior instruction still in the pipeline (solved by forwarding or stalling). Control hazards arise from branches that change the PC (solved by branch prediction and speculative execution). Structural hazards occur when two instructions need the same hardware resource (solved by resource duplication).

**Q4: Explain RISC vs CISC. Why do modern x86 CPUs blur the line?**

RISC uses simple, fixed-length instructions executed in one cycle, with a load/store memory model and many registers -- this makes pipelining efficient. CISC uses complex, variable-length instructions that can perform multi-step operations including direct memory access. Modern x86 CPUs blur this distinction because internally they decode complex CISC instructions into simpler micro-ops (essentially RISC operations) that flow through a wide, out-of-order, superscalar pipeline. This gives x86 backward compatibility with its vast software ecosystem while achieving RISC-like execution efficiency. ARM has also added some complexity over time but remains fundamentally RISC.

**Q5: What is cache coherence? Explain the MESI protocol.**

In multi-core systems, each core has private caches. Cache coherence ensures all cores see a consistent view of memory. The MESI protocol assigns each cache line one of four states: Modified (dirty, only valid copy), Exclusive (clean, only copy), Shared (clean, possibly in other caches), or Invalid (stale). When a core writes to a Shared line, it sends an invalidation message to other cores, transitioning their copies to Invalid. When a core reads a Modified line from another core, the modified data is supplied (snooping) and the line transitions to Shared in both caches. This protocol prevents one core from reading stale data written by another.

**Q6: What is false sharing and how do you avoid it?**

False sharing occurs when two threads on different cores modify independent variables that reside on the same cache line. Even though there is no logical data sharing, the hardware coherence protocol treats it as a conflict -- the cache line bounces between cores as each write invalidates the other core's copy. This dramatically reduces performance. Avoidance: pad data structures so each thread's data occupies its own cache line (typically 64 bytes), use compiler attributes like `alignas(64)` in C++, or restructure data to separate hot fields used by different threads.

**Q7: Explain virtual memory and the TLB.**

Virtual memory gives each process the illusion of a large, private address space. The MMU translates virtual addresses to physical addresses using page tables. The TLB (Translation Lookaside Buffer) is a small, fast cache of recent page table translations. Without the TLB, every memory access would require multiple additional memory accesses to walk the page table. TLB hit rates above 99% are typical, making the effective translation cost negligible. On a TLB miss, the hardware (or software on some architectures) performs a page table walk. On a context switch, the TLB is flushed (or entries are tagged with ASIDs to avoid flushing).

**Q8: Why is `0.1 + 0.2 != 0.3` in floating point?**

IEEE 754 floating-point numbers are represented in binary. The decimal value 0.1 has no exact finite binary representation (just as 1/3 has no exact finite decimal representation). It is stored as the closest representable value, approximately 0.100000000000000005551. Similarly, 0.2 is approximated. When added, the rounding errors accumulate, producing a result like 0.30000000000000004, which is not exactly 0.3. To compare floating-point numbers, use an epsilon tolerance: `abs(a - b) < epsilon`. For financial calculations requiring exact decimal arithmetic, use decimal types (Python's `decimal.Decimal`, Java's `BigDecimal`).

---

# 8. Distributed Systems

---

## 8.1 Consistency Models

| Model | Guarantee | Performance | Example Systems |
|---|---|---|---|
| **Linearizability (Strong)** | Reads always return the most recent write; operations appear instantaneous | Slowest | Google Spanner, ZooKeeper |
| **Sequential Consistency** | All operations appear in some sequential order consistent with each process's program order | Slower | Theoretical (hard to implement efficiently) |
| **Causal Consistency** | Causally related operations are seen in order; concurrent operations may be seen in any order | Moderate | MongoDB (with causal sessions) |
| **Eventual Consistency** | All replicas eventually converge to the same value (given no new writes) | Fastest | Cassandra, DynamoDB, DNS |

### Strong vs Eventual Consistency Tradeoff

| Aspect | Strong Consistency | Eventual Consistency |
|---|---|---|
| Read guarantee | Always returns the latest write | May return stale data |
| Availability during partition | Reduced (must coordinate with leader/quorum) | High (any replica can serve reads) |
| Latency | Higher (coordination overhead) | Lower (local reads) |
| Use case | Banking, inventory, leader election | Social media feeds, analytics, caching |

---

## 8.2 Consensus Algorithms

Consensus algorithms allow a group of nodes to agree on a single value, even in the presence of failures. They are the foundation of replicated state machines.

### Paxos (Lamport, 1989)

Three roles: **Proposer** (proposes values), **Acceptor** (votes), **Learner** (learns decided value).

**Two phases:**
1. **Prepare:** Proposer sends Prepare(n) with a unique proposal number n. Acceptors respond with the highest-numbered proposal they have already accepted (if any).
2. **Accept:** If a majority responds, the proposer sends Accept(n, value). Acceptors accept if they haven't promised to a higher-numbered proposal.

Value is chosen when a majority of acceptors accept it.

**Limitations:** Complex to implement, hard to reason about, poor performance in practice. Multi-Paxos optimizes for a stable leader.

### Raft (Ongaro & Ousterhout, 2014)

Designed as an understandable alternative to Paxos. Three roles: **Leader**, **Follower**, **Candidate**.

**Key mechanisms:**

| Mechanism | Description |
|---|---|
| **Leader Election** | Followers become candidates after an election timeout. Candidate requests votes from peers. First to get majority becomes leader. Term numbers prevent stale leaders. |
| **Log Replication** | Leader receives client requests, appends to its log, replicates to followers. Entry is committed when stored on a majority of servers. |
| **Safety** | Election restriction: a candidate must have all committed entries to win. Leader completeness: committed entries are never lost. |

**Raft guarantees:**
- Election Safety: at most one leader per term
- Leader Append-Only: leader never overwrites or deletes log entries
- Log Matching: if two logs have an entry with the same index and term, the logs are identical up to that point
- Leader Completeness: a committed entry is present in the logs of all future leaders

**Used by:** etcd, CockroachDB, TiKV, Consul.

---

## 8.3 Replication Strategies

| Strategy | Write Path | Read Path | Consistency | Availability |
|---|---|---|---|---|
| **Leader-Follower (Primary-Backup)** | Only leader accepts writes; replicates to followers | Leader for strong reads; followers for eventual reads | Configurable | Leader is SPOF (failover via leader election) |
| **Leader-Leader (Multi-Master)** | Any node accepts writes | Any node | Eventually consistent (conflict resolution needed) | High (no single write bottleneck) |
| **Leaderless (Quorum)** | Write to W nodes | Read from R nodes; W + R > N ensures overlap | Configurable via W, R, N | High |

### Quorum Reads and Writes

Given N replicas:
- **W** = number of nodes that must acknowledge a write
- **R** = number of nodes that must respond to a read
- If **W + R > N**, at least one node in the read set has the latest write

| Configuration | W | R | Tradeoff |
|---|---|---|---|
| Strong consistency | N | 1 | Slow writes, fast reads |
| Strong consistency | majority | majority | Balanced |
| High availability writes | 1 | N | Fast writes, slow reads |

### Conflict Resolution

For multi-leader and leaderless replication, concurrent writes to the same key can conflict:

| Strategy | Description |
|---|---|
| **Last-Write-Wins (LWW)** | Use timestamps; latest write wins. Simple but loses data. |
| **Vector Clocks** | Track causal history; detect conflicts for application-level resolution |
| **CRDTs** | Conflict-free Replicated Data Types: data structures designed to merge automatically (e.g., counters, sets) |
| **Application-level** | Present conflicts to the user (e.g., Google Docs collaborative editing) |

---

## 8.4 Partitioning / Sharding

| Strategy | Method | Pros | Cons |
|---|---|---|---|
| **Hash partitioning** | Hash(key) determines partition | Uniform distribution | Loses key ordering; range queries scatter across partitions |
| **Range partitioning** | Key ranges assigned to partitions | Efficient range scans | Hotspots if keys are not uniformly distributed |
| **Directory-based** | Lookup service maps keys to partitions | Flexible remapping | Lookup service is a bottleneck/SPOF |
| **Consistent hashing** | Hash ring with virtual nodes | Minimal redistribution on rebalancing | More complex implementation |

### Rebalancing

When adding or removing nodes, data must be redistributed:

| Approach | Description |
|---|---|
| **Fixed number of partitions** | Create many more partitions than nodes; assign partitions to nodes. Adding a node reassigns partitions. (Used by Elasticsearch, Couchbase) |
| **Dynamic partitioning** | Split partitions that grow too large; merge small partitions. (Used by HBase, MongoDB) |
| **Consistent hashing** | Add virtual nodes; only K/N keys need to move |

---

## 8.5 Distributed Transactions

### Two-Phase Commit (2PC)

A protocol for atomic commits across multiple nodes:

```
Coordinator                    Participants
    │                              │
    │──── Prepare ────────────────▶│  Phase 1: Vote
    │◀── Vote Yes/No ─────────────│
    │                              │
    │  (if all Yes)                │
    │──── Commit ─────────────────▶│  Phase 2: Commit
    │◀── Acknowledgment ──────────│
    │                              │
    │  (if any No)                 │
    │──── Abort ──────────────────▶│
```

**Problem:** If the coordinator crashes after sending Prepare but before sending Commit/Abort, participants are blocked (holding locks) indefinitely. The coordinator is a single point of failure.

### Three-Phase Commit (3PC)

Adds a pre-commit phase to reduce blocking. After receiving all "Yes" votes, the coordinator sends a pre-commit message. This allows participants to recover from coordinator failure (if they received pre-commit, they know everyone voted Yes). Not widely used in practice due to complexity and assumptions about timing.

### Saga Pattern

Replaces a distributed transaction with a sequence of local transactions, each with a **compensating transaction** for rollback:

```
T1 → T2 → T3 → T4        (forward path)
C1 ← C2 ← C3              (compensation on failure)
```

**Example:** Order processing:
1. Create order (compensate: cancel order)
2. Reserve inventory (compensate: release inventory)
3. Charge payment (compensate: refund payment)
4. Ship order

If step 3 fails, execute C2 (release inventory) then C1 (cancel order).

| Coordination | Description |
|---|---|
| **Choreography** | Each service publishes events; the next service reacts. Decentralized but hard to monitor. |
| **Orchestration** | A central saga coordinator directs the sequence. Easier to manage and monitor. |

---

## 8.6 Clock Synchronization and Ordering

In distributed systems, there is no global clock. Events on different nodes cannot be perfectly ordered by wall-clock time.

### Lamport Timestamps (Logical Clocks)

Each process maintains a counter C:
1. Before each event, increment C
2. When sending a message, attach C
3. When receiving a message with timestamp T, set C = max(C, T) + 1

**Guarantee:** If event A causally precedes event B, then C(A) < C(B). But the converse is NOT true: C(A) < C(B) does not mean A caused B (concurrent events can have any ordering).

### Vector Clocks

Each process maintains a vector of N counters (one per process):
1. Before each event, increment own counter
2. When sending, attach the full vector
3. When receiving vector V, merge: set each element to max of own and received

**Guarantee:** Can detect both causality AND concurrency. V(A) < V(B) (all elements ≤, at least one <) means A causally precedes B. If neither V(A) < V(B) nor V(B) < V(A), the events are concurrent.

**Tradeoff:** Vector size grows with the number of processes. Impractical for very large systems.

### Hybrid Logical Clocks (HLC)

Combine physical timestamps with logical counters. Provide ordering guarantees similar to Lamport timestamps while staying close to wall-clock time. Used by CockroachDB and MongoDB.

### Google TrueTime

Uses GPS receivers and atomic clocks in data centers to provide a bounded-uncertainty time interval [earliest, latest]. Spanner uses TrueTime to implement linearizable transactions by waiting out uncertainty intervals.

---

## 8.7 Failure Detection

| Method | Description | Tradeoff |
|---|---|---|
| **Heartbeats** | Nodes periodically send "I'm alive" messages. If no heartbeat for T seconds, declare dead. | Simple but slow detection and false positives on network delay |
| **Phi Accrual Failure Detector** | Continuously monitors heartbeat inter-arrival times and computes a "suspicion level" (phi). Higher phi = more likely failed. | Adaptive to network conditions; configurable sensitivity. Used by Cassandra and Akka. |
| **SWIM (Scalable Weakly-consistent Infection-style Membership)** | Combines direct probing and indirect probing (ask another node to probe on your behalf) with gossip-based dissemination | Scalable, robust, fast detection. Used by HashiCorp Memberlist. |

---

## 8.8 MapReduce

A programming model for processing large datasets in parallel across a cluster.

**Two phases:**
1. **Map:** Process each input record independently and emit (key, value) pairs
2. **Reduce:** Group all values by key and aggregate them

```
Input Data → Map → Shuffle/Sort → Reduce → Output

Example: Word Count
Map("hello world hello") → [("hello", 1), ("world", 1), ("hello", 1)]
Shuffle → {"hello": [1, 1], "world": [1]}
Reduce → [("hello", 2), ("world", 1)]
```

**Characteristics:**
- Scales horizontally across commodity machines
- Fault-tolerant (re-execute failed tasks)
- High latency (disk-based, batch processing)
- Superseded by in-memory frameworks (Apache Spark) for iterative workloads

---

## 8.9 Gossip Protocol

A peer-to-peer communication protocol where each node periodically selects a random peer and exchanges state information. Information spreads epidemically through the network.

**Properties:**
- **Scalable:** O(log N) rounds to reach all N nodes
- **Fault-tolerant:** No single point of failure; works with node churn
- **Eventually consistent:** All nodes converge to the same state

**Used for:** Membership protocols (which nodes are alive), failure detection, state dissemination (Cassandra uses gossip for cluster metadata).

---

## 8.10 Resilience Patterns

| Pattern | Description | Use Case |
|---|---|---|
| **Circuit Breaker** | Track failures to a downstream service. After a threshold, "open" the circuit (fail fast without calling the service). Periodically try again ("half-open"). Close circuit when service recovers. | Preventing cascading failures in microservices |
| **Bulkhead** | Isolate components so that failure in one does not consume all resources (e.g., separate thread pools per dependency) | Resource isolation |
| **Retry with Backoff** | On transient failure, retry with exponentially increasing delays (+ jitter to avoid thundering herd) | Handling transient failures |
| **Timeout** | Set upper bounds on how long to wait for responses | Preventing indefinite blocking |
| **Fallback** | When a service fails, provide a degraded response (cached data, default value) | Graceful degradation |

---

## 8.11 Key Distributed Systems

| System | Type | Key Feature |
|---|---|---|
| **ZooKeeper** | Coordination service | Linearizable reads/writes, leader election, distributed locks, configuration management |
| **etcd** | Distributed key-value store | Raft consensus, used as Kubernetes' backing store |
| **Cassandra** | Wide-column store | AP system, tunable consistency, gossip-based, consistent hashing |
| **DynamoDB** | Key-value / document store | Managed, single-digit ms latency, DAX caching, global tables |
| **Kafka** | Distributed log / streaming | Ordered per-partition, persistent, high throughput, consumer groups |
| **Redis** | In-memory data store | Sub-ms latency, data structures, pub/sub, Lua scripting, clustering |

---

## 8.12 Distributed Systems -- Interview Questions

**Q1: Explain the CAP theorem. Is it a strict tradeoff?**

The CAP theorem states that a distributed system can provide at most two of three properties: Consistency (every read returns the latest write), Availability (every request gets a response), and Partition Tolerance (the system works despite network partitions). Since partitions are inevitable in any distributed system, the practical choice is between CP (sacrifice availability during partitions to maintain consistency) and AP (sacrifice consistency during partitions to remain available). However, CAP is not as binary as often presented: systems can be tuned along a spectrum. PACELC extends it -- even without partitions, there is a latency vs consistency tradeoff. Real systems like DynamoDB allow per-request consistency choices.

**Q2: What is the Raft consensus algorithm? How does leader election work?**

Raft ensures a cluster of nodes agrees on a sequence of values (log entries). Each node is a Leader, Follower, or Candidate. Time is divided into terms. Followers expect heartbeats from the leader; if no heartbeat arrives within a random election timeout, a follower becomes a candidate, increments the term, votes for itself, and requests votes from peers. A candidate wins if it receives votes from a majority. The randomized timeout prevents split votes. Once elected, the leader handles all client requests, appending entries to its log and replicating them to followers. An entry is committed when stored on a majority. Raft guarantees at most one leader per term and that committed entries are never lost.

**Q3: Explain eventual consistency. When is it acceptable?**

Eventual consistency guarantees that if no new writes occur, all replicas will eventually converge to the same value. There is no guarantee about how long this takes or what intermediate states a reader might see. It is acceptable when: (1) The application can tolerate temporarily stale data (social media feeds, likes/view counts). (2) Availability and low latency are more important than immediate consistency. (3) The data is not safety-critical (analytics, recommendations). It is NOT acceptable for bank balances, inventory counts, or leader election, where reading stale data leads to incorrect behavior.

**Q4: What is Two-Phase Commit? What are its problems?**

Two-Phase Commit (2PC) coordinates atomic commits across distributed nodes. In Phase 1 (Prepare), the coordinator asks all participants to vote Yes/No. In Phase 2, if all voted Yes, the coordinator sends Commit; otherwise, Abort. Problems: (1) **Blocking:** If the coordinator fails after Prepare but before Commit/Abort, participants hold locks indefinitely, unable to decide. (2) **Single point of failure:** The coordinator is critical. (3) **Latency:** Two round trips of network communication. (4) **Not partition-tolerant:** Participants cannot proceed if they cannot reach the coordinator. Alternatives: Saga pattern (eventual consistency with compensation), or consensus-based approaches (Paxos/Raft commit).

**Q5: What are vector clocks? How do they differ from Lamport timestamps?**

Both are logical clock mechanisms for ordering events in distributed systems without a global clock. Lamport timestamps use a single counter and guarantee that if A causally precedes B, then timestamp(A) < timestamp(B). However, the converse is not true -- two concurrent events can have ordered timestamps. Vector clocks use a vector of N counters (one per process). They can detect both causality AND concurrency: if VC(A) < VC(B) element-wise, then A causally precedes B; if neither is strictly less, the events are concurrent. This makes vector clocks more powerful for conflict detection (used by DynamoDB, Riak) but more expensive (O(N) space per event).

**Q6: Explain the Saga pattern for distributed transactions.**

The Saga pattern breaks a distributed transaction into a sequence of local transactions, each with a compensating action. If all steps succeed, the transaction completes. If any step fails, the completed steps are undone by executing their compensating actions in reverse order. Two coordination approaches: (1) Choreography -- each service publishes domain events that trigger the next step; decentralized but complex to debug. (2) Orchestration -- a central saga coordinator directs the flow; easier to understand and monitor. Sagas provide eventual consistency rather than ACID guarantees. Compensating actions must be idempotent because they might be executed multiple times due to retries.

**Q7: What is a gossip protocol? Where is it used?**

A gossip protocol is a peer-to-peer communication approach where each node periodically selects a random peer and exchanges state information. Like an epidemic, information spreads through the network and eventually reaches all nodes -- typically in O(log N) communication rounds. It is decentralized (no leader), fault-tolerant (works with node failures), and scalable. Used for: membership/failure detection (which nodes are alive/dead), metadata dissemination (Cassandra's cluster topology), aggregate computation (distributed averages/counts), and data reconciliation.

**Q8: What is the circuit breaker pattern?**

The circuit breaker monitors calls to a downstream service and tracks failures. In the **Closed** state, requests pass through normally. If failures exceed a threshold, the circuit **Opens** -- subsequent requests fail immediately without calling the service (fail fast). After a timeout, the circuit enters **Half-Open** -- a limited number of test requests are allowed through. If they succeed, the circuit closes; if they fail, it opens again. This prevents cascading failures (one failing service consuming all threads/connections in the caller), reduces load on a struggling service, and provides fast failure feedback to clients.

---

# 9. Security

---

## 9.1 Symmetric vs Asymmetric Encryption

### Symmetric Encryption

Uses the same key for encryption and decryption.

| Algorithm | Key Size | Block Size | Notes |
|---|---|---|---|
| **AES** (Advanced Encryption Standard) | 128, 192, or 256 bits | 128 bits | Standard; fast in hardware (AES-NI); used everywhere |
| **ChaCha20** | 256 bits | Stream cipher | Software-friendly; used in TLS 1.3 (when no AES-NI hardware) |
| **3DES** | 168 bits (effective 112) | 64 bits | Legacy; slow; being deprecated |

**Block cipher modes:**

| Mode | Description | Use Case |
|---|---|---|
| **ECB** (Electronic Codebook) | Each block encrypted independently | NEVER use (identical plaintext blocks produce identical ciphertext) |
| **CBC** (Cipher Block Chaining) | Each block XORed with previous ciphertext block | Legacy; requires padding; vulnerable to padding oracle |
| **CTR** (Counter) | Encrypts a counter; XOR with plaintext (stream cipher mode) | Parallelizable; no padding needed |
| **GCM** (Galois/Counter Mode) | CTR + authentication tag | Standard for TLS; provides both confidentiality and integrity |

### Asymmetric Encryption

Uses a key pair: public key (shared openly) encrypts, private key (kept secret) decrypts.

| Algorithm | Key Size | Based On | Use Case |
|---|---|---|---|
| **RSA** | 2048-4096 bits | Integer factorization | Encryption, digital signatures, key exchange |
| **ECC** (Elliptic Curve) | 256-384 bits | Elliptic curve discrete log | Same as RSA but smaller keys, faster |
| **Diffie-Hellman** | 2048+ bits | Discrete logarithm | Key exchange only (not encryption) |
| **ECDH** (Elliptic Curve DH) | 256 bits | Elliptic curve discrete log | Key exchange (used in TLS) |

### Symmetric vs Asymmetric Comparison

| Aspect | Symmetric | Asymmetric |
|---|---|---|
| Keys | One shared key | Key pair (public + private) |
| Speed | Very fast (100-1000x faster) | Slow |
| Key distribution | Problem: how to share the key securely? | Public key can be shared openly |
| Use case | Bulk data encryption | Key exchange, digital signatures, authentication |
| Key sizes | 128-256 bits | 2048-4096 bits (RSA) or 256 bits (ECC) |

**In practice, both are used together:** Asymmetric encryption exchanges a symmetric session key (key exchange), then symmetric encryption handles the bulk data (hybrid encryption). This is exactly how TLS works.

---

## 9.2 Hashing

A hash function maps arbitrary-length input to a fixed-length output (digest). Cryptographic hash functions have additional properties:

| Property | Description |
|---|---|
| **Deterministic** | Same input always produces the same hash |
| **Pre-image resistance** | Given hash H, infeasible to find input M such that hash(M) = H |
| **Second pre-image resistance** | Given input M1, infeasible to find M2 ≠ M1 such that hash(M1) = hash(M2) |
| **Collision resistance** | Infeasible to find any two inputs M1 ≠ M2 such that hash(M1) = hash(M2) |
| **Avalanche effect** | A small change in input drastically changes the output |

### Common Hash Functions

| Algorithm | Output Size | Status | Use Case |
|---|---|---|---|
| **MD5** | 128 bits | Broken (collisions found) | Checksums only; NOT for security |
| **SHA-1** | 160 bits | Deprecated (collisions demonstrated) | Legacy; being phased out |
| **SHA-256** | 256 bits | Secure | Digital signatures, TLS, blockchain |
| **SHA-3** | 256/512 bits | Secure | Alternative to SHA-2 (different design: Keccak) |
| **BLAKE2/BLAKE3** | Variable | Secure | Fast hashing for general use |

### Password Hashing

Regular hash functions (SHA-256) are too fast for password hashing -- an attacker can try billions of hashes per second. Password hashing algorithms are deliberately slow:

| Algorithm | Mechanism | Notes |
|---|---|---|
| **bcrypt** | Blowfish-based; configurable cost factor | Widely used; cost factor = 10-12 recommended |
| **scrypt** | Memory-hard (requires large amounts of RAM) | Resistant to GPU/ASIC attacks |
| **Argon2** | Winner of the Password Hashing Competition (2015) | Memory-hard, parallelizable; recommended for new applications |
| **PBKDF2** | Iterative HMAC-SHA | Legacy but still acceptable with high iterations |

### Salt and Rainbow Tables

A **salt** is a random value added to the password before hashing: `hash(salt + password)`. Each user gets a unique salt.

Without salt: Attackers precompute hash tables (**rainbow tables**) mapping common passwords to their hashes. One lookup reveals the password.

With salt: Each password has a unique hash (even identical passwords), making rainbow tables useless. The attacker must brute-force each password individually.

---

## 9.3 TLS/SSL

### TLS 1.2 Handshake (detailed)

```
Client                                    Server
  │                                         │
  │──── ClientHello ───────────────────────▶│
  │    (TLS version, cipher suites,         │
  │     client random, extensions)          │
  │                                         │
  │◀──── ServerHello ───────────────────────│
  │    (chosen cipher suite, server random) │
  │◀──── Certificate ───────────────────────│
  │    (X.509 certificate chain)            │
  │◀──── ServerKeyExchange (if needed) ─────│
  │    (DH parameters / ECDH public key)    │
  │◀──── ServerHelloDone ──────────────────│
  │                                         │
  │──── ClientKeyExchange ─────────────────▶│
  │    (pre-master secret / DH public key)  │
  │──── ChangeCipherSpec ──────────────────▶│
  │──── Finished (encrypted) ──────────────▶│
  │                                         │
  │◀──── ChangeCipherSpec ──────────────────│
  │◀──── Finished (encrypted) ─────────────│
  │                                         │
  │◀═══ Encrypted Application Data ═══════▶│
```

Both sides compute the **master secret** from pre-master secret + client random + server random, then derive symmetric encryption keys.

### TLS 1.3 Improvements

| Feature | TLS 1.2 | TLS 1.3 |
|---|---|---|
| Handshake RTTs | 2 RTTs | 1 RTT (0-RTT resumption possible) |
| Cipher suites | Many (some insecure) | Only AEAD ciphers (AES-GCM, ChaCha20-Poly1305) |
| Key exchange | RSA or DHE | DHE or ECDHE only (forward secrecy mandatory) |
| Forward secrecy | Optional | Mandatory |
| 0-RTT | No | Yes (with replay risk) |

### Certificate Chain and Verification

```
Root CA (self-signed, pre-installed in OS/browser trust store)
  └── Intermediate CA (signed by Root CA)
       └── Server Certificate (signed by Intermediate CA)
```

The browser verifies the chain from server certificate up to a trusted root CA, checking signatures, validity dates, and revocation status (OCSP or CRL).

---

## 9.4 Authentication

### Session-Based Authentication

```
1. Client sends credentials (username + password)
2. Server verifies, creates a session (stored in memory/DB)
3. Server sends back a session ID in a cookie
4. Client sends cookie with every subsequent request
5. Server looks up session ID to identify the user
```

**Pros:** Simple, easy to revoke (delete session). **Cons:** Server must store sessions (stateful), hard to scale across multiple servers (need sticky sessions or shared session store like Redis).

### Token-Based Authentication (JWT)

```
1. Client sends credentials
2. Server verifies, generates a signed JWT
3. Client stores JWT (localStorage or httpOnly cookie)
4. Client sends JWT in Authorization header: "Bearer <token>"
5. Server verifies JWT signature (no database lookup needed)
```

**JWT structure:** `header.payload.signature` (base64url encoded)

```
Header:  {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "user123", "name": "Alice", "exp": 1700000000, "iat": 1699990000}
Signature: HMAC-SHA256(base64(header) + "." + base64(payload), secret_key)
```

**Pros:** Stateless (no server-side session storage), scales easily, works across domains. **Cons:** Cannot be revoked before expiry (use short-lived tokens + refresh tokens), payload is not encrypted (just signed), token size can be large.

### OAuth 2.0

An authorization framework that allows third-party applications to access a user's resources without exposing credentials.

**Roles:**
- **Resource Owner:** The user
- **Client:** The third-party app
- **Authorization Server:** Issues tokens (e.g., Google, GitHub)
- **Resource Server:** Hosts the protected resources (API)

**Authorization Code Flow (most common):**

```
1. Client redirects user to Authorization Server
2. User authenticates and grants permission
3. Authorization Server redirects back with an authorization code
4. Client exchanges code for an access token (server-to-server)
5. Client uses access token to call Resource Server API
```

### OpenID Connect (OIDC)

An identity layer on top of OAuth 2.0. While OAuth 2.0 is for authorization (what can you access?), OIDC adds authentication (who are you?). It provides an **ID token** (JWT) containing user identity claims (name, email, etc.).

---

## 9.5 Authorization

| Model | Description | Use Case |
|---|---|---|
| **RBAC (Role-Based Access Control)** | Permissions assigned to roles; users assigned to roles | Most common: admin, editor, viewer roles |
| **ABAC (Attribute-Based Access Control)** | Permissions based on attributes of user, resource, action, and environment | Fine-grained: "Doctors can view patient records in their department during business hours" |
| **ACL (Access Control List)** | Per-resource list specifying which users/groups have which permissions | File system permissions, network firewalls |
| **ReBAC (Relationship-Based)** | Permissions based on relationships between entities | Social networks: "Can view if friend of friend" (Google Zanzibar) |

---

## 9.6 Common Vulnerabilities (OWASP Top 10)

| Vulnerability | Description | Prevention |
|---|---|---|
| **SQL Injection** | Malicious SQL in user input: `' OR 1=1 --` | Parameterized queries / prepared statements; NEVER concatenate user input into SQL |
| **XSS (Cross-Site Scripting)** | Inject malicious scripts into web pages viewed by others | Output encoding/escaping; Content Security Policy (CSP); sanitize HTML input |
| **CSRF (Cross-Site Request Forgery)** | Trick authenticated user into making unintended requests | CSRF tokens; SameSite cookie attribute; verify Origin/Referer headers |
| **Broken Authentication** | Weak passwords, credential stuffing, session fixation | MFA, rate limiting, secure session management, bcrypt/Argon2 for passwords |
| **Broken Access Control** | Users access resources or actions beyond their permissions | Server-side authorization checks on every request; deny by default |
| **Security Misconfiguration** | Default credentials, unnecessary features enabled, verbose errors | Hardened configs, remove defaults, disable directory listing, custom error pages |
| **SSRF (Server-Side Request Forgery)** | Trick server into making requests to internal resources | Allowlist of permitted URLs/IPs; block internal network ranges |
| **Insecure Deserialization** | Malicious serialized objects execute code on deserialization | Avoid deserializing untrusted data; use JSON instead of native serialization |
| **Injection (general)** | OS command injection, LDAP injection, etc. | Input validation, parameterized interfaces, principle of least privilege |
| **Insufficient Logging & Monitoring** | Attacks go undetected | Log security events, set up alerts, regular log review |

### SQL Injection Example

```sql
-- Vulnerable (string concatenation)
query = "SELECT * FROM users WHERE username = '" + input + "'"
-- Input: ' OR 1=1 --
-- Resulting query: SELECT * FROM users WHERE username = '' OR 1=1 --'
-- Returns all users!

-- Safe (parameterized query)
cursor.execute("SELECT * FROM users WHERE username = %s", (input,))
```

### XSS Types

| Type | Description | Example |
|---|---|---|
| **Stored (Persistent)** | Malicious script stored on server (e.g., in a database) and served to all users | Comment containing `<script>steal_cookies()</script>` |
| **Reflected** | Malicious script in the URL, reflected back in the response | `https://site.com/search?q=<script>alert(1)</script>` |
| **DOM-based** | Client-side JavaScript reads malicious input from the DOM | `document.write(location.hash)` |

---

## 9.7 CORS (Cross-Origin Resource Sharing)

Browsers enforce the **Same-Origin Policy**: scripts on `https://a.com` cannot make requests to `https://b.com`. CORS relaxes this by allowing servers to specify which origins can access their resources.

**CORS headers:**

| Header | Description |
|---|---|
| `Access-Control-Allow-Origin` | Allowed origins (e.g., `https://a.com` or `*`) |
| `Access-Control-Allow-Methods` | Allowed HTTP methods (GET, POST, PUT, etc.) |
| `Access-Control-Allow-Headers` | Allowed custom headers |
| `Access-Control-Allow-Credentials` | Whether to include cookies |
| `Access-Control-Max-Age` | How long to cache preflight response |

**Preflight request:** For "non-simple" requests (PUT, DELETE, custom headers), the browser first sends an OPTIONS request to check if the actual request is permitted. If the server responds with appropriate CORS headers, the browser proceeds with the actual request.

```
Browser                             Server
  │                                   │
  │──── OPTIONS /api/data ───────────▶│  (preflight)
  │     Origin: https://a.com         │
  │     Access-Control-Request-Method: PUT
  │                                   │
  │◀── 204 No Content ───────────────│
  │    Access-Control-Allow-Origin: https://a.com
  │    Access-Control-Allow-Methods: PUT
  │                                   │
  │──── PUT /api/data ───────────────▶│  (actual request)
  │◀── 200 OK ───────────────────────│
```

---

## 9.8 Public Key Infrastructure (PKI)

PKI provides a framework for managing digital certificates and public-key encryption.

### Components

| Component | Role |
|---|---|
| **Certificate Authority (CA)** | Trusted entity that issues and signs digital certificates |
| **Registration Authority (RA)** | Verifies identity before CA issues a certificate |
| **Digital Certificate (X.509)** | Binds a public key to an identity (domain name, organization) |
| **Certificate Revocation List (CRL)** | List of revoked certificates |
| **OCSP (Online Certificate Status Protocol)** | Real-time certificate validity checking |

### Digital Signatures

```
Signing:    hash(message) → digest → encrypt(digest, private_key) → signature
Verifying:  decrypt(signature, public_key) → digest1
            hash(message) → digest2
            compare digest1 == digest2
```

Digital signatures provide:
- **Authentication:** The message came from the private key owner
- **Integrity:** The message has not been tampered with
- **Non-repudiation:** The signer cannot deny signing

---

## 9.9 API Security

| Practice | Description |
|---|---|
| **HTTPS everywhere** | Encrypt all API communication |
| **Authentication** | API keys (simple), OAuth 2.0 (delegation), JWT (stateless) |
| **Rate limiting** | Prevent abuse; return 429 Too Many Requests |
| **Input validation** | Validate type, length, format, range of all inputs |
| **Output encoding** | Prevent injection in responses |
| **Least privilege** | Grant minimum necessary permissions |
| **Parameterized queries** | Prevent SQL injection |
| **CORS configuration** | Restrict allowed origins |
| **Security headers** | `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security` |
| **Logging and monitoring** | Log all access for audit and anomaly detection |
| **Secrets management** | Use environment variables or vaults (HashiCorp Vault, AWS Secrets Manager); never hardcode secrets |

### API Keys vs OAuth

| Aspect | API Key | OAuth 2.0 |
|---|---|---|
| What it identifies | Application | User (with scoped permissions) |
| Complexity | Simple | Complex (flows, tokens, scopes) |
| Revocation | Regenerate key | Revoke token; fine-grained |
| Use case | Server-to-server, simple APIs | User-delegated access, third-party apps |
| Security | Weaker (static, no expiry unless managed) | Stronger (short-lived tokens, scopes, refresh) |

---

## 9.10 Secure Coding Practices

| Practice | Description |
|---|---|
| **Input validation** | Validate all input on the server side (whitelist approach: reject anything not explicitly allowed) |
| **Principle of least privilege** | Code, users, and services should have only the minimum permissions needed |
| **Defense in depth** | Multiple layers of security controls |
| **Fail securely** | Error handling should not reveal sensitive information; default to deny |
| **Keep dependencies updated** | Regularly update libraries to patch known vulnerabilities (CVEs) |
| **Use established libraries** | Do not implement your own cryptography or authentication |
| **Secure defaults** | Ship with secure configurations; require opt-in for less secure modes |
| **Code review** | Security-focused reviews for sensitive code paths |
| **Static analysis** | Use SAST tools (SonarQube, Semgrep) to catch vulnerabilities early |
| **Secrets management** | Never commit secrets to version control; use .env files (gitignored) and vault solutions |

---

## 9.11 Security -- Interview Questions

**Q1: Explain the difference between symmetric and asymmetric encryption. How are they used together?**

Symmetric encryption uses the same key for encryption and decryption (e.g., AES-256). It is very fast and suitable for bulk data encryption, but requires both parties to share the key securely. Asymmetric encryption uses a key pair: the public key encrypts and the private key decrypts (e.g., RSA, ECC). It is much slower but solves the key distribution problem -- the public key can be shared openly. In practice, they are combined in a hybrid approach: asymmetric encryption is used to securely exchange a symmetric session key, and then symmetric encryption handles the actual data. This is exactly how TLS works: the handshake uses asymmetric key exchange (ECDHE), and the application data is encrypted with symmetric AES-GCM.

**Q2: How should you store passwords in a database?**

Never store passwords in plaintext or with reversible encryption. Use a slow, salted, password-hashing algorithm: (1) Generate a unique random salt per user. (2) Hash the password with the salt using bcrypt, scrypt, or Argon2 (with appropriate cost parameters). (3) Store the salt and hash together (bcrypt includes the salt in its output format). When verifying a login, hash the submitted password with the stored salt and compare. The slow hash function (tuned to take ~100-250ms) makes brute-force attacks impractical, and per-user salts prevent rainbow table attacks and ensure identical passwords produce different hashes.

**Q3: What is a JWT? What are its security considerations?**

A JSON Web Token (JWT) is a compact, self-contained token with three base64url-encoded parts: header (algorithm), payload (claims like user ID, expiry), and signature. The server signs the token with a secret (HMAC) or private key (RSA/ECDSA). Clients include it in the Authorization header. Security considerations: (1) The payload is only encoded, not encrypted -- do not include sensitive data unless using JWE (encrypted JWT). (2) Tokens cannot be revoked before expiry -- use short expiration times with refresh tokens. (3) Use strong secrets and RS256 over HS256 in distributed systems. (4) Validate all claims (expiry, issuer, audience). (5) Store tokens in httpOnly, Secure, SameSite cookies (not localStorage, which is vulnerable to XSS).

**Q4: Explain SQL injection. How do you prevent it?**

SQL injection occurs when user-supplied input is inserted directly into a SQL query, allowing the attacker to modify the query's logic. For example, an input of `' OR 1=1 --` can bypass authentication or dump the entire database. Prevention: (1) Always use parameterized queries / prepared statements -- the database treats input as data, never as SQL code. (2) Use ORM frameworks that parameterize by default. (3) Apply input validation (whitelist expected patterns). (4) Use least-privilege database accounts (read-only for read operations). (5) Escape special characters as a secondary defense. Parameterized queries are the primary and most effective defense.

**Q5: What is CSRF? How do you prevent it?**

Cross-Site Request Forgery tricks an authenticated user's browser into making an unintended request to a target site. For example, if a user is logged into their bank, a malicious site could include `<img src="https://bank.com/transfer?to=attacker&amount=10000">`, and the browser would send the request with the bank's session cookies. Prevention: (1) CSRF tokens: include a unique, unpredictable token in forms that the server validates on submission. (2) SameSite cookie attribute: set cookies to `SameSite=Strict` or `SameSite=Lax` so they are not sent with cross-origin requests. (3) Check Origin and Referer headers. (4) Require re-authentication for sensitive actions.

**Q6: Explain the TLS handshake. What is forward secrecy?**

The TLS handshake establishes an encrypted connection. The client sends supported cipher suites and a random value. The server responds with the chosen suite, its certificate, and its random value. They perform a key exchange (ECDHE) to derive a shared secret, from which symmetric encryption keys are derived. Both sides send encrypted "Finished" messages to verify the handshake succeeded. Forward secrecy (achieved with ephemeral Diffie-Hellman: DHE or ECDHE) means each session uses a unique key pair. Even if the server's long-term private key is later compromised, past session keys cannot be recovered, so recorded traffic remains safe. TLS 1.3 mandates forward secrecy.

**Q7: What are the differences between authentication and authorization?**

Authentication verifies identity -- "Who are you?" (login with credentials, MFA). Authorization determines permissions -- "What are you allowed to do?" (access control rules). Authentication happens first; authorization builds on the authenticated identity. For example, a user authenticates with their credentials, then the system checks their role (RBAC) to determine if they can access a specific resource. Technologies: Authentication uses passwords, tokens (JWT), biometrics, OAuth/OIDC. Authorization uses RBAC, ABAC, ACLs, policies.

**Q8: What is XSS? Explain the different types and how to prevent them.**

Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages viewed by other users. Stored XSS: the script is saved on the server (e.g., in a comment) and served to all users who view that page. Reflected XSS: the script is part of the URL/request and reflected in the response. DOM-based XSS: the script is executed client-side by JavaScript that reads untrusted data from the DOM. Prevention: (1) Output encoding: escape HTML entities when inserting user data into HTML. (2) Content Security Policy (CSP): restrict which scripts can execute. (3) Sanitize HTML input (use a library like DOMPurify). (4) Use httpOnly cookies to prevent cookie theft. (5) Use modern frameworks (React, Angular) that auto-escape by default.

**Q9: What is OAuth 2.0? How does the Authorization Code flow work?**

OAuth 2.0 is an authorization framework that lets a third-party application access a user's resources on another service without sharing credentials. In the Authorization Code flow: (1) The client redirects the user to the authorization server's login page. (2) The user authenticates and grants permission. (3) The authorization server redirects back with a short-lived authorization code. (4) The client exchanges the code for an access token (server-to-server, so the client secret is not exposed to the browser). (5) The client uses the access token to call the resource server API. The code-for-token exchange happens server-side, preventing the access token from being exposed in the browser. PKCE (Proof Key for Code Exchange) adds protection for public clients (mobile/SPA) that cannot keep a client secret.

**Q10: What is the difference between hashing and encryption?**

Hashing is a one-way function: given an input, it produces a fixed-size digest from which the original input cannot be recovered. It is used for data integrity verification and password storage. Encryption is a two-way function: data is encrypted with a key and can be decrypted with the same (symmetric) or corresponding (asymmetric) key to recover the original data. Hashing is irreversible by design; encryption is reversible by design. Use hashing for passwords (bcrypt/Argon2), data integrity (SHA-256 checksums), and digital signatures. Use encryption for protecting data in transit (TLS) and at rest (AES-encrypted storage).

---

*End of CS Fundamentals Reference*
