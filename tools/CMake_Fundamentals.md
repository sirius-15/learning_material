# CMake Fundamentals -- Comprehensive Reference

> A deep-dive reference for modern target-based CMake (3.x) plus the surrounding ecosystem: Ninja, CTest, CPack, ccache, vcpkg, Conan, sanitizers, cross-compilation, and IDE integration. Each section includes conceptual explanations, comparison tables, code examples, common pitfalls, and interview questions with detailed answers. Complements the *C++ Fundamentals*, *C++ Testing*, and *Parallel GPU Programming* guides.

---

## Table of Contents

### Part 1: Foundations

1. [Why CMake? Build Systems and Meta-Build Systems](#1-why-cmake-build-systems-and-meta-build-systems)
2. [The CMake Pipeline: Configure, Generate, Build, Install](#2-the-cmake-pipeline-configure-generate-build-install)
3. [Installing CMake and the Tooling Family](#3-installing-cmake-and-the-tooling-family)

### Part 2: Project Anatomy

4. [The Minimal CMakeLists](#4-the-minimal-cmakelists)
5. [In-Source vs Out-of-Source Builds](#5-in-source-vs-out-of-source-builds)
6. [Policies and Backwards Compatibility](#6-policies-and-backwards-compatibility)

### Part 3: Targets, the Modern Core

7. [add_executable, add_library, and Library Types](#7-add_executable-add_library-and-library-types)
8. [Target Properties and the PUBLIC/PRIVATE/INTERFACE Model](#8-target-properties-and-the-publicprivateinterface-model)
9. [The target_* Command Family](#9-the-target_-command-family)
10. [Object, Interface, and Imported Libraries](#10-object-interface-and-imported-libraries)
11. [Alias Targets and Namespace Conventions](#11-alias-targets-and-namespace-conventions)

### Part 4: Variables, Scopes, and the Cache

12. [Variable Scopes](#12-variable-scopes)
13. [The Cache, option, and FORCE](#13-the-cache-option-and-force)
14. [Lists, Strings, Files, and Paths](#14-lists-strings-files-and-paths)
15. [Control Flow, Functions, and Macros](#15-control-flow-functions-and-macros)

### Part 5: Generator Expressions

16. [Anatomy of Generator Expressions](#16-anatomy-of-generator-expressions)
17. [Common Generator Expressions](#17-common-generator-expressions)
18. [Conditional Linking and Per-Config Flags](#18-conditional-linking-and-per-config-flags)
19. [BUILD_INTERFACE vs INSTALL_INTERFACE](#19-build_interface-vs-install_interface)

### Part 6: Configurations, Toolchains, and Presets

20. [Build Configurations and Multi-Config Generators](#20-build-configurations-and-multi-config-generators)
21. [The C++ Standard](#21-the-c-standard)
22. [Toolchain Files and Cross-Compilation](#22-toolchain-files-and-cross-compilation)
23. [CMake Presets](#23-cmake-presets)

### Part 7: Generators and Build Drivers

24. [Generators: Ninja, Make, Visual Studio, Xcode](#24-generators-ninja-make-visual-studio-xcode)
25. [Ninja Deep Dive](#25-ninja-deep-dive)
26. [Compiler Caches: ccache and sccache](#26-compiler-caches-ccache-and-sccache)
27. [Distributed Builds](#27-distributed-builds)

### Part 8: Dependency Management

28. [find_package: Module Mode vs Config Mode](#28-find_package-module-mode-vs-config-mode)
29. [Writing FindXxx Modules](#29-writing-findxxx-modules)
30. [Writing XxxConfig Files](#30-writing-xxxconfig-files)
31. [FetchContent Deep Dive](#31-fetchcontent-deep-dive)
32. [ExternalProject_Add](#32-externalproject_add)
33. [vcpkg Integration](#33-vcpkg-integration)
34. [Conan Integration](#34-conan-integration)
35. [CPM.cmake and Hybrid Approaches](#35-cpmcmake-and-hybrid-approaches)

### Part 9: Installation and Packaging

36. [The install Command](#36-the-install-command)
37. [GNUInstallDirs and FHS Layout](#37-gnuinstalldirs-and-fhs-layout)
38. [Exporting Targets and Generating Config Files](#38-exporting-targets-and-generating-config-files)
39. [ABI and SOVERSION](#39-abi-and-soversion)
40. [CPack: TGZ, DEB, RPM, NSIS, WIX](#40-cpack-tgz-deb-rpm-nsis-wix)
41. [Generating pkg-config Files](#41-generating-pkg-config-files)

### Part 10: Testing with CTest

42. [enable_testing and add_test](#42-enable_testing-and-add_test)
43. [Test Properties](#43-test-properties)
44. [Parallel Test Execution](#44-parallel-test-execution)
45. [gtest_discover_tests and catch_discover_tests](#45-gtest_discover_tests-and-catch_discover_tests)
46. [CTest Dashboards and CDash](#46-ctest-dashboards-and-cdash)
47. [Code Coverage Integration](#47-code-coverage-integration)

### Part 11: Custom Commands and Code Generation

48. [add_custom_command vs add_custom_target](#48-add_custom_command-vs-add_custom_target)
49. [Code Generation: Protobuf, Qt, Flatbuffers](#49-code-generation-protobuf-qt-flatbuffers)
50. [configure_file and Header Generation](#50-configure_file-and-header-generation)
51. [CMake Script Mode](#51-cmake-script-mode)

### Part 12: Compiler Flags, Sanitizers, and Hardening

52. [Per-Target vs Global Flags](#52-per-target-vs-global-flags)
53. [Sanitizers](#53-sanitizers)
54. [Hardening and Security Flags](#54-hardening-and-security-flags)
55. [LTO and IPO](#55-lto-and-ipo)
56. [Warning Levels and Warnings-as-Errors](#56-warning-levels-and-warnings-as-errors)

### Part 13: IDE and Static-Analysis Integration

57. [compile_commands.json for clangd](#57-compile_commandsjson-for-clangd)
58. [clang-tidy, clang-format, and Friends](#58-clang-tidy-clang-format-and-friends)
59. [IDE Support](#59-ide-support)

### Part 14: Performance and Modern Features

60. [Reducing Configure Time](#60-reducing-configure-time)
61. [Unity Builds and Precompiled Headers](#61-unity-builds-and-precompiled-headers)
62. [C++20 Modules Support](#62-c20-modules-support)
63. [Refactoring Legacy CMake](#63-refactoring-legacy-cmake)

### Part 15: Best Practices and Interview Questions

64. [Project Layout and Conventions](#64-project-layout-and-conventions)
65. [Cheatsheet](#65-cheatsheet)
66. [Common Pitfalls](#66-common-pitfalls)
67. [Interview Questions and Answers](#67-interview-questions-and-answers)

---

# Part 1: Foundations

---

# 1. Why CMake? Build Systems and Meta-Build Systems

---

## 1.1 What Problem Does CMake Solve?

A C or C++ source tree is **not** a buildable thing on its own. To produce an executable or library you need to know:

- Which source files to compile, in which order, with which compiler.
- Which include directories, preprocessor definitions, and compiler flags to use, **per file or per target**.
- How to link those object files into a final binary, with which libraries and link flags.
- How that binary changes per platform (Windows vs Linux vs macOS), per architecture (x86_64 vs aarch64), per configuration (Debug vs Release), and per toolchain (GCC vs Clang vs MSVC).
- How to expose the resulting artifacts to downstream consumers (headers, libraries, version metadata).

There are roughly three layers of build tooling that try to solve this:

```
        +-------------------------------------------------+
        |   Meta-build / project-description layer        |   CMake, Meson, Premake
        |   "describe the project once, generate native"  |
        +------------------------+------------------------+
                                 |
                                 v generates
        +-------------------------------------------------+
        |   Build driver / dependency graph executor      |   Ninja, GNU Make, MSBuild
        |   "given a DAG, run actions in parallel"        |
        +------------------------+------------------------+
                                 |
                                 v invokes
        +-------------------------------------------------+
        |   Compiler + linker toolchain                   |   gcc/g++, clang/clang++, cl.exe, link.exe
        |   "turn .cpp into .o, .o into .so/.exe"         |
        +-------------------------------------------------+
```

**CMake is a meta-build system.** It does **not** compile or link directly. Instead, it reads `CMakeLists.txt` files and emits **native build files** (Ninja, Makefiles, Visual Studio `.sln`/`.vcxproj`, Xcode `.xcodeproj`) that an underlying build driver then executes.

## 1.2 Build Systems Compared

| Tool | Layer | Language | Notes |
|---|---|---|---|
| `make` | Build driver | Makefile DSL | Ubiquitous, slow incremental, hard to parallelise correctly |
| `ninja` | Build driver | `.ninja` DSL | Designed for speed; meant to be generated, not hand-written |
| MSBuild | Build driver | XML (`.vcxproj`) | Native Visual Studio driver |
| **CMake** | Meta-build | Domain-specific scripting | Generates Make / Ninja / Visual Studio / Xcode |
| Meson | Meta-build | Python-like DSL | Generates Ninja almost exclusively; faster, stricter |
| Premake | Meta-build | Lua | Generates Make, VS, Xcode, etc. |
| Bazel / Buck | Build system | Starlark | Hermetic, scalable, monorepo-friendly; not a generator |
| xmake | Build system | Lua | Native build engine plus package manager |
| Autotools | Meta-build | M4 + shell | Predates CMake; mostly legacy GNU world |

CMake won because it is portable, mature, and **every IDE and dependency manager understands it**. vcpkg, Conan, CLion, Visual Studio, VS Code, Qt Creator, and almost every modern C++ library all speak CMake.

## 1.3 What "Modern CMake" Means

The term **Modern CMake** (popularised by Daniel Pfeifer's 2017 talk "Effective CMake" and Craig Scott's book *Professional CMake*) refers to a target-based, scope-respecting style introduced gradually from CMake 2.8.12 (2013) and consolidated by 3.0 / 3.12 / 3.21.

| Old-style ("Modern CMake" replaces) | Modern CMake |
|---|---|
| `include_directories(...)` (directory-scoped, leaks to children) | `target_include_directories(my_lib PUBLIC ...)` |
| `add_definitions(-DFOO)` (global) | `target_compile_definitions(my_lib PRIVATE FOO)` |
| `link_libraries(...)` (everything links to everything) | `target_link_libraries(my_app PRIVATE my_lib)` |
| Variables (`MY_LIB_INCLUDE_DIRS`, `MY_LIB_LIBRARIES`) | Imported targets (`MyLib::MyLib`) |
| `set(CMAKE_CXX_FLAGS ...)` (global) | `target_compile_options(my_lib PRIVATE ...)` |
| `file(GLOB SOURCES *.cpp)` (no dependency tracking) | Explicit `add_library(my_lib src/a.cpp src/b.cpp)` |

This guide teaches Modern CMake exclusively. Legacy patterns are referenced only as anti-patterns (Section 63).

## 1.4 A Minimal Mental Model

A CMake project is, conceptually, a graph of **targets** and **usage requirements** on those targets.

```
        +-------------+        target_link_libraries
        |    app      |---PRIVATE---------------+
        +-------------+                          |
              ^                                  v
              |                            +-----+-----+
              |                            |  liba    |--PUBLIC---> Boost::system
              |                            +-----+-----+
              |                                  |
              | target_link_libraries             | INTERFACE
              | PRIVATE: app gets it,            v
              | PUBLIC : app + its dependents,   <header-only requirement>
              | INTERFACE: dependents only
```

A target is more than a list of source files; it carries:

- Include directories that propagate to anything linking it (`INTERFACE_INCLUDE_DIRECTORIES`)
- Compile flags it requires of itself (`COMPILE_OPTIONS`) and of consumers (`INTERFACE_COMPILE_OPTIONS`)
- Linked libraries, both private and propagated
- A language standard (`CXX_STANDARD`, `CXX_STANDARD_REQUIRED`)
- A position-independent-code requirement, an LTO flag, a name suffix, a visibility, an SOVERSION, and dozens of others.

Everything you do in modern CMake is "configure a target" or "compose targets".

## 1.5 What CMake Is Not

| Misconception | Reality |
|---|---|
| "CMake is a build system" | No -- it generates native build files; the build system is Ninja/Make/MSBuild |
| "CMake compiles code" | No -- it invokes the compiler **during configure** only for feature detection (`try_compile`); building is done by the generator |
| "CMake is a package manager" | No -- it can fetch sources (`FetchContent`) and find installed packages (`find_package`), but binary distribution is vcpkg/Conan/system |
| "`CMakeLists.txt` is declarative" | Partially -- it is an imperative scripting language that **describes** a build graph. Side effects matter |
| "`set(VAR ...)` in a function changes the caller's variable" | No -- it is function-local unless you use `PARENT_SCOPE` |

---

# 2. The CMake Pipeline: Configure, Generate, Build, Install

---

A CMake build runs in four distinct phases. Understanding which phase does what is the single most common stumbling block for newcomers.

## 2.1 The Four Phases

```
   Source tree            Build tree
   -----------            ----------
   CMakeLists.txt   --->  [1. Configure] reads CMakeLists.txt, runs CMake script,
   src/*.cpp              detects compilers, runs try_compile/find_package
   include/*.h            writes CMakeCache.txt
                          
                          [2. Generate]  writes build.ninja / Makefile /
                                         *.vcxproj / *.xcodeproj
                          
                          [3. Build]     native tool (ninja/make/msbuild) compiles
                                         and links, producing libs/binaries
                          
                          [4. Install]   copies headers, binaries, config files,
                                         export sets into CMAKE_INSTALL_PREFIX
```

| Phase | Driven by | Inputs | Outputs |
|---|---|---|---|
| **Configure** | `cmake -S <src> -B <build>` | `CMakeLists.txt`, cache vars, env, toolchain | `CMakeCache.txt`, in-memory build graph |
| **Generate** | Same command (immediately follows configure) | In-memory build graph | `build.ninja`, `Makefile`, `*.vcxproj`, etc. |
| **Build** | `cmake --build <build>` (or `ninja`/`make`/`msbuild` directly) | Generated files plus source | Object files, libraries, executables |
| **Install** | `cmake --install <build>` (or `ninja install`) | Built artifacts plus `install()` rules | Files copied to `CMAKE_INSTALL_PREFIX` |

## 2.2 Walkthrough

```bash
# 1+2. Configure and generate
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release

# 3. Build (uses the generator that 'build' was configured for)
cmake --build build --parallel

# 4. Install
cmake --install build --prefix /opt/myproject
```

The four phases are independent: you can rerun configure without re-running build, rerun build without re-running configure (unless `CMakeLists.txt` changed), and so on. CMake detects when reconfiguration is needed and does it automatically at build time if so.

## 2.3 Configure vs Build Time

This is the most important distinction in CMake. Everything happens at either **configure time** or **build time**, and the two phases see very different things.

| Configure time | Build time |
|---|---|
| Runs the CMake interpreter | Runs the generator (`ninja`, `make`, `cl.exe`, `link.exe`) |
| Reads `CMakeLists.txt`, `*.cmake` files | Reads `build.ninja` / `Makefile` / `*.vcxproj` |
| All `set()`, `if()`, `foreach()`, `function()`, `message()` execute now | Generator expressions `$<...>` evaluate now |
| `find_package`, `try_compile`, `try_run`, `execute_process` | Custom commands (`add_custom_command`) run now |
| `FetchContent_MakeAvailable` downloads dependencies now | Compiler/linker run now |
| Multi-config generators see one set of values | Multi-config generators see per-config values |

A common bug: trying to use the value of a generator expression in a `message()` or `if()` at configure time. They are strings until generate time.

```cmake
# BAD -- this does not "evaluate" CONFIG; it sets a literal string
set(flags $<$<CONFIG:Debug>:-O0>)
message(STATUS "flags = ${flags}")   # prints  flags = $<$<CONFIG:Debug>:-O0>
```

## 2.4 The Build Tree (CMakeCache.txt)

The build tree is an opaque directory containing:

- `CMakeCache.txt` -- the cache file, holding every cached variable, the detected compilers, system info, and option() values.
- `CMakeFiles/` -- internal CMake bookkeeping, generated `compile_commands.json`, dependency files, etc.
- The native build files (`build.ninja`, `Makefile`, `*.vcxproj`, `*.xcodeproj`).
- Built artifacts (`.o`, `.a`, `.so`, `.exe`).

The build tree is **disposable**: delete it and rerun configure, you get the same result. The cache file is the contract between configure and build; it is the reason `cmake -DFOO=bar` from a second run is remembered.

## 2.5 Reconfiguring

| Trigger | What CMake does |
|---|---|
| `CMakeLists.txt` newer than `CMakeCache.txt` | Re-runs configure + generate automatically before next build |
| `cmake -DFOO=bar build` | Re-runs configure + generate with `FOO=bar` set in the cache |
| `cmake --fresh -S . -B build` | Deletes the cache and re-configures from scratch (CMake 3.24+) |
| `rm -rf build && cmake ...` | Same effect, lower-tech |

Forcing a clean reconfigure is sometimes necessary when toolchain or environment variables change in ways CMake cannot detect.

## 2.6 Pitfall: Mixing Source and Build Tree

```bash
# DON'T do this
cd src/
cmake .
```

This runs CMake **in the source tree**, polluting it with `CMakeCache.txt`, `CMakeFiles/`, generated build files, and built objects. It is the single biggest hygiene mistake in CMake projects. Always use a separate build directory (Section 5).

---

# 3. Installing CMake and the Tooling Family

---

## 3.1 The Tools

CMake ships with a family of executables, each with a distinct role:

| Tool | Role |
|---|---|
| `cmake` | The main executable: configure, generate, build, install, script mode |
| `ctest` | Test runner that consumes the `CTestTestfile.cmake` produced by `enable_testing()` |
| `cpack` | Package generator (TGZ, DEB, RPM, NSIS, WIX, productbuild, ...) |
| `cmake-gui` | Cross-platform Qt GUI front-end |
| `ccmake` | Curses-based TUI for setting cache variables interactively |

## 3.2 Installing

| Platform | Recommended source | Notes |
|---|---|---|
| Linux | Distro package (`apt install cmake`, `dnf install cmake`) **then** override with [Kitware APT repo](https://apt.kitware.com/) or `pip install cmake` for newer versions | Distro versions are often 1-2 years behind |
| macOS | `brew install cmake` or the official `.dmg` from cmake.org | Homebrew is current |
| Windows | Official installer from cmake.org, or `winget install Kitware.CMake`, or via Visual Studio's installer | Visual Studio bundles a `CMake` executable too |
| All (Python) | `pip install cmake` (uses official binaries under the hood) | Handy in CI, no admin needed |
| All (manual) | Download from <https://cmake.org/download/> | Standalone, no system changes |

**Recommended minimum version:** 3.21 (introduced presets v3, robust `--install`, modern `find_package` improvements). Some features in this guide require 3.24 (`--fresh`, `OVERRIDE_FIND_PACKAGE`) or 3.28 (C++20 modules support).

## 3.3 Verifying the Installation

```bash
$ cmake --version
cmake version 3.28.3

CMake suite maintained and supported by Kitware (kitware.com/cmake).

$ ctest --version
ctest version 3.28.3

$ cpack --version
cpack version 3.28.3
```

## 3.4 Common Command-Line Invocations

```bash
# Configure and generate (the "S/B" form is preferred since 3.13)
cmake -S . -B build -G Ninja

# Configure with cache variables
cmake -S . -B build -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/opt/myproject \
      -DBUILD_TESTING=ON

# Build (generator-agnostic)
cmake --build build --parallel
cmake --build build --target my_lib --parallel
cmake --build build --config Release    # multi-config only

# Install
cmake --install build --prefix /opt/myproject

# Test
ctest --test-dir build --output-on-failure --parallel

# Package
cpack --config build/CPackConfig.cmake

# Script mode (run a *.cmake file with no project)
cmake -P script.cmake

# Tooling
cmake -E make_directory foo bar       # cross-platform mkdir -p
cmake -E remove_directory build       # cross-platform rm -rf
cmake -E copy_if_different a b        # the "cp -u" portable equivalent
cmake -E tar cjf out.tar.bz2 dir/     # portable tar
```

`cmake -E --help` lists every cross-platform helper command -- a small portable shell-toolbox shipped with CMake.

---

# Part 2: Project Anatomy

---

# 4. The Minimal CMakeLists

---

## 4.1 The Three Required Lines

Every CMake project of any size starts with the same three constructs.

```cmake
cmake_minimum_required(VERSION 3.21)
project(hello LANGUAGES CXX)

add_executable(hello src/main.cpp)
```

That's it. From this, `cmake -S . -B build && cmake --build build` produces a working `hello` executable.

## 4.2 cmake_minimum_required

```cmake
cmake_minimum_required(VERSION 3.21)
cmake_minimum_required(VERSION 3.21...3.30)   # range form, recommended
```

This command does **two** things:

1. **Fails configure** if the running CMake is older than the minimum.
2. **Sets policies** to the new (post-`VERSION`) behaviour up to either the running version or the upper bound of the range.

The **range form** (CMake 3.12+) is preferred because it pins policies to a specific upper bound regardless of how new the user's CMake is. This protects you from future-CMake behaviour changes you have not tested against.

| Form | Policy behaviour |
|---|---|
| `VERSION 3.21` | Policies set to 3.21 behaviour; newer policies unset |
| `VERSION 3.21...3.30` | Policies set up to 3.30 behaviour, even on CMake 3.31+ |
| `VERSION 3.21 FATAL_ERROR` | Same as `3.21` (FATAL_ERROR is the default since 3.12 anyway) |

## 4.3 The project Command

```cmake
project(name
        VERSION   1.2.3
        DESCRIPTION "Short blurb"
        HOMEPAGE_URL "https://example.com"
        LANGUAGES CXX C)
```

`project()` does a remarkable amount of work:

- Sets `PROJECT_NAME`, `PROJECT_VERSION` (and `_MAJOR`, `_MINOR`, `_PATCH`, `_TWEAK`).
- Sets `<name>_SOURCE_DIR`, `<name>_BINARY_DIR` for top-level project access.
- Triggers compiler detection for each `LANGUAGES` entry (the `try_compile` of `int main(){}` you see early in configure logs).
- Sets `CMAKE_PROJECT_*` variables when called at top level.
- Loads any toolchain file (`-DCMAKE_TOOLCHAIN_FILE=...`).

The `LANGUAGES` argument is important. If you omit it, CMake defaults to `C CXX`, which probes both compilers. If your project is pure C++, write `LANGUAGES CXX` to skip the C compiler probe.

| Language token | Triggers |
|---|---|
| `C` | C compiler detection (`CMAKE_C_COMPILER`) |
| `CXX` | C++ compiler detection (`CMAKE_CXX_COMPILER`) |
| `ASM` | Assembler |
| `Fortran` | Fortran compiler |
| `CUDA` | CUDA compiler (`nvcc`) |
| `HIP` | AMD HIP compiler |
| `OBJC` / `OBJCXX` | Objective-C/C++ |
| `Swift` | Swift compiler |
| `NONE` | Disable any language detection (useful for script-only projects) |

## 4.4 Project Layout

The conventional layout matches what most users, IDEs, and packagers expect:

```
my_project/
|-- CMakeLists.txt              <- top-level project()
|-- CMakePresets.json           <- optional, but increasingly standard
|-- include/                    <- public headers (installed)
|   `-- my_project/
|       `-- foo.hpp
|-- src/                        <- private sources and private headers
|   |-- CMakeLists.txt          <- src/ subdir, defines my_project library
|   |-- foo.cpp
|   `-- bar.cpp
|-- apps/                       <- executables
|   |-- CMakeLists.txt
|   `-- main.cpp
|-- tests/
|   |-- CMakeLists.txt
|   `-- foo_test.cpp
|-- third_party/                <- vendored deps (if any)
|-- cmake/                      <- custom modules, Find scripts, helpers
|   `-- FindFooDep.cmake
`-- README.md
```

The principle: **one `CMakeLists.txt` per directory that owns build artifacts**. Sub-`CMakeLists.txt` files are pulled in by `add_subdirectory()` from the parent.

## 4.5 A Realistic Top-Level CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.21...3.30)
project(my_project
        VERSION 1.0.0
        DESCRIPTION "Example library and CLI"
        LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Generate compile_commands.json for clangd / editors.
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Only enable testing when building this project as the top level,
# so consumers using add_subdirectory don't pull in our tests.
include(CTest)
if(BUILD_TESTING AND PROJECT_IS_TOP_LEVEL)
    enable_testing()
endif()

add_subdirectory(src)
add_subdirectory(apps)

if(BUILD_TESTING AND PROJECT_IS_TOP_LEVEL)
    add_subdirectory(tests)
endif()
```

`PROJECT_IS_TOP_LEVEL` (CMake 3.21+) is true when the current project is the outermost one being built, and false when the project is consumed via `add_subdirectory()` from a parent. Use it to gate optional behaviour like testing, install rules, or packaging.

## 4.6 Pitfall: Multiple project() Calls

CMake allows multiple `project()` calls (nested projects), but each subsequent call **resets** `PROJECT_NAME`, `PROJECT_VERSION`, `PROJECT_SOURCE_DIR`. The variables `CMAKE_PROJECT_*` retain the outermost (first) project's values.

```cmake
# In top-level CMakeLists.txt
project(top VERSION 1.0)
add_subdirectory(third_party/foo)
# After add_subdirectory, PROJECT_NAME still equals "top" here,
# but inside third_party/foo/CMakeLists.txt during its execution,
# PROJECT_NAME was "foo".
```

---

# 5. In-Source vs Out-of-Source Builds

---

## 5.1 The Two Layouts

| In-source (avoid) | Out-of-source (always) |
|---|---|
| `cmake .` from the repo root | `cmake -S . -B build` |
| Build artifacts mixed with sources | Clean separation: source tree is read-only at build time |
| `.gitignore` becomes a nightmare | Single `build/` entry suffices |
| Cannot try multiple configurations side-by-side | `build-release/`, `build-debug/`, `build-asan/`, etc. |

## 5.2 Forbidding In-Source Builds

Many projects refuse to configure if invoked in-source:

```cmake
if(CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR)
    message(FATAL_ERROR
        "In-source builds are not allowed. "
        "Use a separate build directory: cmake -S . -B build")
endif()
```

`CMAKE_SOURCE_DIR` is the top of the source tree; `CMAKE_BINARY_DIR` is the top of the build tree. Equal means in-source.

## 5.3 The S/B Form vs the Old Form

```bash
# Modern (3.13+): "the source is here, put the build here"
cmake -S . -B build

# Old: "I am currently in the build dir, look one up for the source"
mkdir build && cd build && cmake ..
```

Both work; the `-S/-B` form is more script-friendly, lets you configure without being in the build directory, and is the form used by IDEs and CI.

## 5.4 Useful Source/Binary Variables

| Variable | Meaning |
|---|---|
| `CMAKE_SOURCE_DIR` | Top-level source directory (the one with the outermost `CMakeLists.txt`) |
| `CMAKE_BINARY_DIR` | Top-level build directory |
| `CMAKE_CURRENT_SOURCE_DIR` | Source directory of the current `CMakeLists.txt` |
| `CMAKE_CURRENT_BINARY_DIR` | Build directory for the current `CMakeLists.txt` |
| `PROJECT_SOURCE_DIR` | Top of the source tree of the nearest enclosing `project()` |
| `PROJECT_BINARY_DIR` | Top of the build tree of the nearest enclosing `project()` |
| `<name>_SOURCE_DIR` | Per-project: where `project(<name>)` lives |
| `<name>_BINARY_DIR` | Per-project binary dir |
| `CMAKE_CURRENT_LIST_DIR` | Directory of the currently-executing `*.cmake` file (works inside `include()`) |

The distinction between `CMAKE_CURRENT_SOURCE_DIR` and `CMAKE_CURRENT_LIST_DIR` matters inside modules: the former is the directory of the `CMakeLists.txt` that triggered the include; the latter is the directory of the `.cmake` file itself.

---

# 6. Policies and Backwards Compatibility

---

## 6.1 Why Policies Exist

CMake has been around since 2000. Every release introduces fixes whose new behaviour would silently break old projects. **Policies** let CMake change behaviour without breaking old projects: each behaviour change is gated by a policy ID (`CMP0000`, `CMP0001`, ...) that defaults to OLD on old `cmake_minimum_required` settings and NEW on new ones.

```cmake
cmake_minimum_required(VERSION 3.21)
# All policies CMP0000-CMP???? introduced up to 3.21 are NEW.
# Policies introduced after 3.21 are unset (warning) on a newer CMake.

cmake_policy(SET CMP0091 NEW)   # explicitly opt in to a specific policy
```

## 6.2 A Few Important Policies

| Policy | Effect (NEW) | Introduced |
|---|---|---|
| `CMP0048` | `project(... VERSION ...)` sets `PROJECT_VERSION` (otherwise warning) | 3.0 |
| `CMP0077` | `option()` respects existing normal variables (no override) | 3.13 |
| `CMP0091` | MSVC runtime library selected via `CMAKE_MSVC_RUNTIME_LIBRARY`, not `/MT`/`/MD` flags | 3.15 |
| `CMP0144` | `<PackageName>_ROOT` (capitalised) variables honoured by `find_package` | 3.27 |
| `CMP0167` | FindBoost module removed in favour of upstream `BoostConfig` | 3.30 |

You almost never set individual policies; you set the **bundle** by setting `cmake_minimum_required(VERSION X.Y)`. The exceptions are when:

- You need a single new policy on an otherwise old project.
- You need to keep one old policy on an otherwise modern project (commonly to support a slow-moving consumer).

## 6.3 Policy Push/Pop

```cmake
cmake_policy(PUSH)
cmake_policy(SET CMP0144 NEW)
find_package(Foo REQUIRED)
cmake_policy(POP)
```

This isolates the policy change to a single block, useful inside reusable modules.

## 6.4 The Two Failure Modes

```
Behaviour: OLD          Behaviour: NEW          Behaviour: unset
+----------+            +----------+            +---------------------+
| works as |            | works as |            | Warning: "policy    |
| in CMake |            | in CMake |            | not set, defaulting |
| pre-X.Y  |            | X.Y+     |            | to OLD which may    |
+----------+            +----------+            | be removed"         |
                                                 +---------------------+
```

The "unset" warning is your hint that you should bump `cmake_minimum_required` or explicitly `cmake_policy(SET ...)`.

---

# Part 3: Targets, the Modern Core

---

# 7. add_executable, add_library, and Library Types

---

## 7.1 The Two Target-Creating Commands

CMake creates **build targets** with exactly two commands:

```cmake
add_executable(<name> [WIN32] [MACOSX_BUNDLE] [EXCLUDE_FROM_ALL] [source...])
add_library(<name>    [STATIC | SHARED | MODULE | OBJECT | INTERFACE] [EXCLUDE_FROM_ALL] [source...])
```

Everything else -- include directories, link libraries, compile flags, definitions -- is added **to** an existing target via the `target_*` family (Section 9).

## 7.2 Library Types Compared

| Type | File on disk | Linked into consumer | When to use |
|---|---|---|---|
| `STATIC` | `libfoo.a` (`foo.lib` on Windows) | Yes, at link time | Default; small libs; libs with no ABI concerns |
| `SHARED` | `libfoo.so` / `libfoo.dylib` / `foo.dll`+`foo.lib` | No -- loaded at runtime | Plugins, large libs, ABI boundaries |
| `MODULE` | Same on-disk as SHARED but **not** linkable | Loaded via `dlopen`/`LoadLibrary` | Plugins that must be loaded manually |
| `OBJECT` | `*.o` files only, no archive | Yes -- objects merged into consumer | Avoid duplicate compilation across multiple final libs |
| `INTERFACE` | No file at all | Only usage requirements | Header-only libraries |

### STATIC vs SHARED at the Build Level

```
   add_library(foo STATIC ...)        add_library(foo SHARED ...)

   foo.cpp ----> foo.cpp.o ----+     foo.cpp ----> foo.cpp.o ----+
                                |                                 |
                                v                                 v
                            libfoo.a                          libfoo.so
                                |                                 |
   add_executable(app ...)      |     add_executable(app ...)     |
   target_link_libraries(       |     target_link_libraries(      |
       app PRIVATE foo)         |         app PRIVATE foo)        |
                                v                                 v
                            app    (libfoo.a content       app    (libfoo.so loaded
                                    embedded in app)              at runtime via RPATH/PATH)
```

### Picking a Default

```cmake
option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
add_library(foo ...)   # honours BUILD_SHARED_LIBS: STATIC if OFF, SHARED if ON
```

When `add_library` omits the type, it defaults to STATIC unless `BUILD_SHARED_LIBS=ON` is in the cache. This is the conventional way to let consumers choose.

## 7.3 OBJECT Libraries

Object libraries solve the "build once, link into many" problem.

```cmake
add_library(foo_obj OBJECT a.cpp b.cpp)
target_include_directories(foo_obj PUBLIC include)

add_library(foo_static STATIC $<TARGET_OBJECTS:foo_obj>)
add_library(foo_shared SHARED $<TARGET_OBJECTS:foo_obj>)
```

Both `foo_static` and `foo_shared` contain the same object code without recompiling `a.cpp`/`b.cpp` twice. On modern CMake (3.12+) you can also just link to the object library directly:

```cmake
add_library(foo_static STATIC)
target_link_libraries(foo_static PUBLIC foo_obj)
```

## 7.4 INTERFACE Libraries

For header-only libraries, an `INTERFACE` target carries only usage requirements -- no sources, no compiled output.

```cmake
add_library(span_lite INTERFACE)
target_include_directories(span_lite INTERFACE include)
target_compile_features(span_lite INTERFACE cxx_std_17)

# Consumers:
target_link_libraries(my_app PRIVATE span_lite)
```

Header-only libraries with INTERFACE expose their requirements (include dirs, C++ standard, compile definitions) without producing any artifact. CMake 3.19 added the ability to attach sources to INTERFACE libraries (useful for "no separate compilation needed but I still want them in the IDE").

## 7.5 EXCLUDE_FROM_ALL

```cmake
add_executable(stress_test EXCLUDE_FROM_ALL stress.cpp)
```

`EXCLUDE_FROM_ALL` removes a target from the default `all` build target. Building requires explicitly naming it (`cmake --build build --target stress_test`). Useful for examples, benchmarks, and stress tests that you don't want consuming CI bandwidth by default.

## 7.6 Source File Conventions

```cmake
add_library(foo
    src/foo.cpp
    src/internal.cpp
    src/internal.hpp        # listing headers makes them appear in IDE projects
    include/foo/foo.hpp
)
```

Listing headers in `add_library`/`add_executable` is **optional for compilation** (CMake doesn't compile headers; it picks them up via include directories), but headers listed in the target appear in IDE project views (Visual Studio, Xcode, Qt Creator). Many projects list them for that reason.

## 7.7 file(GLOB) Anti-Pattern

```cmake
# DON'T do this
file(GLOB SRC src/*.cpp)
add_library(foo ${SRC})
```

`file(GLOB)` evaluates at **configure time**. If you add a new `.cpp`, CMake does not detect it -- the build system has no rule to reconfigure -- and you get cryptic link errors. Use either explicit listings (recommended) or `file(GLOB ... CONFIGURE_DEPENDS)` if you absolutely must:

```cmake
file(GLOB SRC CONFIGURE_DEPENDS src/*.cpp)
```

`CONFIGURE_DEPENDS` (3.12+) adds a build-time check that re-globs and reconfigures if files change. It works but is **slower** and **not portable across all generators** (Ninja and Make work; older generators are best-effort). Explicit listing is still preferred.

---

# 8. Target Properties and the PUBLIC/PRIVATE/INTERFACE Model

---

## 8.1 The Most Important Idea in Modern CMake

A target carries two parallel sets of build properties:

- **Build requirements** -- what the target needs to compile itself (its own includes, flags, definitions).
- **Usage requirements** -- what consumers need in order to use the target (the includes/flags they must inherit when linking to it).

Each property has a "private" and an "INTERFACE_" variant:

| Property (private) | INTERFACE_ counterpart (usage requirement) |
|---|---|
| `COMPILE_DEFINITIONS` | `INTERFACE_COMPILE_DEFINITIONS` |
| `COMPILE_OPTIONS` | `INTERFACE_COMPILE_OPTIONS` |
| `COMPILE_FEATURES` | `INTERFACE_COMPILE_FEATURES` |
| `INCLUDE_DIRECTORIES` | `INTERFACE_INCLUDE_DIRECTORIES` |
| `LINK_LIBRARIES` | `INTERFACE_LINK_LIBRARIES` |
| `LINK_OPTIONS` | `INTERFACE_LINK_OPTIONS` |
| `SOURCES` | `INTERFACE_SOURCES` |

The `target_*` commands set both sets through the **scope keyword**.

## 8.2 PUBLIC, PRIVATE, INTERFACE

```cmake
target_include_directories(foo
    PUBLIC    include             # foo needs it + consumers need it
    PRIVATE   src                 # foo needs it; consumers do not
    INTERFACE include/foo_extra)  # foo does not need it; consumers do
```

| Keyword | Adds to private property? | Adds to INTERFACE_ property? | Meaning |
|---|---|---|---|
| `PRIVATE` | Yes | No | "I need this myself; consumers don't" |
| `INTERFACE` | No | Yes | "I don't need this; consumers do" |
| `PUBLIC` | Yes | Yes | "I need it and so do consumers" |

```
    +---------------+ target_include_directories(foo PUBLIC include)
    |   include/    |--------+
    +---------------+        |
                             v
                       +-----+-----+    PUBLIC: foo compiles with -Iinclude
                       |    foo    |             AND propagates to consumers
                       +-----+-----+
                             ^
                             | target_link_libraries(app PRIVATE foo)
                             |
                       +-----+-----+
                       |    app    |    app compiles with -Iinclude
                       +-----------+    (inherited via foo's INTERFACE_INCLUDE_DIRECTORIES)
```

## 8.3 Concrete Examples

```cmake
add_library(net STATIC src/net.cpp)
target_include_directories(net
    PUBLIC  include            # net's public API headers
    PRIVATE src                # private impl headers
)
target_compile_features(net PUBLIC cxx_std_17)
target_link_libraries(net
    PUBLIC  Threads::Threads   # net.hpp uses std::thread; consumers see it
    PRIVATE OpenSSL::Crypto    # used only in net.cpp; consumers don't see it
)
```

Choose the **smallest scope that is correct**. Over-PUBLIC-ing dependencies leaks them into your consumers' build (longer compile times, larger transitive closure, more name collisions). Under-scoping (declaring PRIVATE what is really PUBLIC) causes consumer build failures.

| Rule of thumb | Scope |
|---|---|
| The type appears in your public header | `PUBLIC` |
| The header is `#include`d only by your `.cpp` files | `PRIVATE` |
| You provide a header but don't compile any of your own code against it | `INTERFACE` (header-only) |

## 8.4 Plain target_link_libraries (Legacy)

Before CMake 2.8.12, `target_link_libraries` did not take a scope:

```cmake
target_link_libraries(foo bar)     # plain signature -- no PUBLIC/PRIVATE/INTERFACE
```

The plain signature still works for backward compatibility but **mixes** the property semantics. New code should always use the keyword form. Mixing the two within the same target is an error.

## 8.5 Setting Properties Directly

The `target_*` family is the high-level API. There is also a low-level `set_target_properties` / `set_property` API:

```cmake
set_target_properties(foo PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    POSITION_INDEPENDENT_CODE ON
    INTERPROCEDURAL_OPTIMIZATION ON
    VERSION 1.2.3
    SOVERSION 1)

set_property(TARGET foo APPEND PROPERTY INTERFACE_INCLUDE_DIRECTORIES include/extra)
```

Use the high-level `target_*` commands for everything they cover; use `set_target_properties` for properties without a `target_*` shortcut (CXX_STANDARD, POSITION_INDEPENDENT_CODE, SOVERSION, etc.).

---

# 9. The target_* Command Family

---

## 9.1 The Full Family

| Command | Property it manipulates | Common use |
|---|---|---|
| `target_include_directories` | `INCLUDE_DIRECTORIES` | Where to find headers |
| `target_link_libraries` | `LINK_LIBRARIES` | What to link |
| `target_link_directories` | `LINK_DIRECTORIES` | Where to find link libs (rarely needed -- use targets instead) |
| `target_link_options` | `LINK_OPTIONS` | Raw linker flags (`-Wl,...`) |
| `target_compile_definitions` | `COMPILE_DEFINITIONS` | `-D` preprocessor macros |
| `target_compile_options` | `COMPILE_OPTIONS` | Raw compiler flags (`-Wall`, `-O2`) |
| `target_compile_features` | `COMPILE_FEATURES` | High-level features (`cxx_std_17`, `cxx_constexpr`) |
| `target_sources` | `SOURCES` | Add files to an existing target |
| `target_precompile_headers` | `PRECOMPILE_HEADERS` | PCH for the target |

All take the `PUBLIC`/`PRIVATE`/`INTERFACE` scope keyword.

## 9.2 target_include_directories

```cmake
target_include_directories(foo
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        src)
```

The `$<BUILD_INTERFACE:...>` and `$<INSTALL_INTERFACE:...>` generator expressions are the canonical way to give different include directories during in-tree builds vs after installation (Section 19).

## 9.3 target_link_libraries

```cmake
target_link_libraries(my_app
    PRIVATE
        my_lib              # another CMake target
        Threads::Threads    # imported target from find_package
        OpenSSL::SSL        # imported target from find_package(OpenSSL)
        ${SOMETHING}        # variable holding a target name -- works
        debug foo_d         # legacy: only when linking Debug config
        optimized foo)
```

`target_link_libraries` accepts:

- Other CMake target names (`my_lib`, `foo_obj`).
- Imported targets (`OpenSSL::SSL`).
- Bare library names (`m`, `dl`, `pthread`) -- CMake passes them as-is to the linker.
- Absolute paths to library files.
- Special prefixed names (`debug`/`optimized`/`general`) for config-specific linking (use generator expressions instead, Section 18).

## 9.4 target_compile_definitions

```cmake
target_compile_definitions(foo
    PRIVATE
        FOO_BUILDING_DLL
        FOO_VERSION_MAJOR=${PROJECT_VERSION_MAJOR}
    PUBLIC
        $<$<CONFIG:Debug>:FOO_DEBUG=1>)
```

Definitions are added as `-DFOO=...` on GCC/Clang and `/DFOO=...` on MSVC. Leading `-D` is stripped if present (`-DFOO_BUILDING_DLL` is equivalent to `FOO_BUILDING_DLL`).

## 9.5 target_compile_options vs target_compile_features

```cmake
# Raw flags -- you own the portability problem
target_compile_options(foo PRIVATE -Wall -Wextra -Wpedantic)

# Feature requests -- CMake picks the right flag per compiler
target_compile_features(foo PUBLIC cxx_std_17)
```

| Approach | Pros | Cons |
|---|---|---|
| `target_compile_options` | Maximum control | You hard-code GCC/Clang/MSVC syntax (`-Wall` vs `/W4`) |
| `target_compile_features` | Portable | Limited vocabulary (`cxx_std_*`, `cxx_constexpr`, ...) |

Use features for "what C++ version do I require"; use options for "warnings, optimisation, debug symbols, etc." with explicit per-compiler guards via generator expressions (Section 17).

## 9.6 target_sources

`target_sources` is the underappreciated workhorse for incremental target construction:

```cmake
add_library(foo)                      # no sources yet -- CMake 3.11+ allows this
target_sources(foo PRIVATE src/foo.cpp src/bar.cpp)

# In a subdirectory's CMakeLists.txt, after add_subdirectory(submod):
target_sources(foo PRIVATE src/submod/extra.cpp)
```

This pattern lets a parent target accumulate sources from multiple `CMakeLists.txt` files without passing variables around. Combined with `target_sources(... PUBLIC FILE_SET HEADERS ...)` (3.23+), you can also express "these headers are part of this library's public interface" in a way that interacts cleanly with `install`.

## 9.7 FILE_SET (CMake 3.23+)

```cmake
target_sources(foo
    PUBLIC
        FILE_SET HEADERS
            BASE_DIRS include
            FILES include/foo/foo.hpp
                  include/foo/util.hpp)

install(TARGETS foo
    EXPORT FooTargets
    FILE_SET HEADERS)
```

`FILE_SET HEADERS` describes the public-header surface explicitly; `install(... FILE_SET HEADERS ...)` then knows what to copy without a separate `install(DIRECTORY include/)` step. Section 36 covers installs.

---

# 10. Object, Interface, and Imported Libraries

---

## 10.1 OBJECT Libraries Recap

```cmake
add_library(foo_obj OBJECT a.cpp b.cpp)
target_include_directories(foo_obj PUBLIC include)

add_executable(app main.cpp)
target_link_libraries(app PRIVATE foo_obj)   # CMake 3.12+: object library as link dep
```

Object libraries are useful when:

- You want the same compiled objects in both a STATIC and a SHARED variant of the same library.
- You want to expose a single set of objects to multiple executables without duplicating compilation.
- You need to bundle object files into a "convenience library" without producing a `.a`/`.lib`.

Limitations: object libraries cannot themselves be linked against other libraries at the object-library level (their consumers do the linking).

## 10.2 INTERFACE Libraries for Header-Only

```cmake
# fmt-style header-only library
add_library(my_hdr_only INTERFACE)
target_include_directories(my_hdr_only INTERFACE include)
target_compile_features(my_hdr_only INTERFACE cxx_std_17)
```

INTERFACE libraries also serve as "tagging" targets to carry shared compile options:

```cmake
# A "warning policy" target every internal library links to
add_library(project_warnings INTERFACE)
target_compile_options(project_warnings INTERFACE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic -Werror>
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX /permissive->)

# Every internal library opts in:
target_link_libraries(libfoo PRIVATE project_warnings)
target_link_libraries(libbar PRIVATE project_warnings)
```

## 10.3 IMPORTED Targets

Imported targets represent **pre-built** libraries (system libraries, libraries delivered by `find_package`, libraries shipped with a vendored binary):

```cmake
add_library(myvendor::libfoo SHARED IMPORTED)
set_target_properties(myvendor::libfoo PROPERTIES
    IMPORTED_LOCATION             "${VENDOR_DIR}/lib/libfoo.so.1"
    IMPORTED_SONAME               "libfoo.so.1"
    INTERFACE_INCLUDE_DIRECTORIES "${VENDOR_DIR}/include"
    INTERFACE_COMPILE_DEFINITIONS "FOO_VERSION=1")

target_link_libraries(my_app PRIVATE myvendor::libfoo)
```

The `IMPORTED` keyword tells CMake "I'm not building this; it already exists." Imported targets carry the same usage requirements (INTERFACE_*) as regular targets, which is how `find_package(OpenSSL)` exposes `OpenSSL::SSL` with the right include paths and link libraries.

| Imported target kinds | Notes |
|---|---|
| `IMPORTED` | Local to the directory it was defined in |
| `GLOBAL IMPORTED` | Visible everywhere -- usually preferred |
| `INTERFACE IMPORTED` | Header-only imported (no binary file) |
| Per-config: `IMPORTED_LOCATION_DEBUG`, `IMPORTED_LOCATION_RELEASE` | Multi-config support |

## 10.4 Promoting Imported Targets to GLOBAL

When `find_package` creates a directory-scoped IMPORTED target and you need it deeper in the tree:

```cmake
set_property(TARGET OpenSSL::SSL PROPERTY IMPORTED_GLOBAL TRUE)
```

This is rarely needed in modern code -- modern config modules export targets as GLOBAL already.

---

# 11. Alias Targets and Namespace Conventions

---

## 11.1 The Namespace Convention

Every library distributed for consumption via CMake should expose its targets under a **namespace**: `Boost::system`, `OpenSSL::SSL`, `fmt::fmt`, `nlohmann_json::nlohmann_json`. The double colon does two things:

1. It signals "this is an imported or namespaced target," not a bare library name.
2. CMake will produce a **hard error** if such a target is missing, rather than treating it as a bare library name and passing `-lOpenSSL::SSL` to the linker (which would fail much later with a confusing message).

```cmake
target_link_libraries(my_app PRIVATE OpenSSL::SSL)  # error at configure time if missing
target_link_libraries(my_app PRIVATE OpenSSL_SSL)   # silently passes -lOpenSSL_SSL, fails at link
```

## 11.2 add_library ALIAS

```cmake
add_library(my_project_foo STATIC src/foo.cpp)
target_include_directories(my_project_foo PUBLIC include)

add_library(MyProject::foo ALIAS my_project_foo)
```

Alias targets:

- Are read-only -- you cannot `target_*` an alias, you must use the real name.
- Can be linked against just like the real target.
- Make in-tree usage and post-install usage symmetric: consumers always write `MyProject::foo`, whether using your project via `add_subdirectory`, `FetchContent`, or `find_package`.

## 11.3 Why This Matters

```cmake
# Without alias:
if(MY_PROJECT_BUILT_IN_TREE)
    target_link_libraries(consumer PRIVATE my_project_foo)
else()
    target_link_libraries(consumer PRIVATE MyProject::foo)
endif()

# With alias (recommended):
target_link_libraries(consumer PRIVATE MyProject::foo)
```

The alias removes the conditional. Whether your project is consumed via `find_package`, `add_subdirectory`, or `FetchContent`, the target name is the same.

## 11.4 Executable Aliases (3.11+)

```cmake
add_executable(my_tool src/tool.cpp)
add_executable(MyProject::tool ALIAS my_tool)
```

This is occasionally useful when one CMake project consumes another's executable target (for example, to use it in an `add_custom_command`).

## 11.5 Alias of Alias (Forbidden)

CMake does **not** allow chaining aliases. `add_library(A ALIAS B)` where `B` is itself an alias is an error. Always alias the real target.

---

# Part 4: Variables, Scopes, and the Cache

---

# 12. Variable Scopes

---

## 12.1 The Four Scopes

CMake has **four** distinct variable scopes. Confusing them is the second most common source of bugs (after configure-vs-build-time confusion).

| Scope | Lifetime | Set by | Read by |
|---|---|---|---|
| **Function** | The function call | `set(VAR ...)` inside a `function()` | Inside the function and (with care) `PARENT_SCOPE` |
| **Directory** | The current `CMakeLists.txt` and its subdirectories | `set(VAR ...)` at directory level | Anywhere in this dir and below |
| **Cache** | Across runs, persisted to `CMakeCache.txt` | `set(VAR ... CACHE TYPE "doc")`, `option()`, `-DVAR=...` | Anywhere |
| **Environment** | The OS environment | `set(ENV{VAR} ...)`, exported in shell | `$ENV{VAR}` |

Plus a fifth "pseudo-scope": **global properties** (rarely needed).

## 12.2 Function Scope

```cmake
function(my_func)
    set(LOCAL_VAR "hello")              # function-scoped
    message(STATUS "inside: ${LOCAL_VAR}")
endfunction()

my_func()
message(STATUS "outside: ${LOCAL_VAR}") # prints empty!
```

A function gets a fresh scope. Variables `set()` inside are invisible outside. To export a value:

```cmake
function(make_greeting input output_var)
    set(${output_var} "Hello, ${input}" PARENT_SCOPE)
endfunction()

make_greeting("world" greeting)
message(STATUS "${greeting}")           # Hello, world
```

The `PARENT_SCOPE` keyword writes the variable in the **caller's** scope, not the function's. By convention, the output variable name is passed as an argument so the caller controls naming.

## 12.3 Directory Scope

`add_subdirectory()` creates a new directory scope that **inherits a copy** of all variables from the parent:

```cmake
# Top-level CMakeLists.txt
set(MY_VAR "top")
add_subdirectory(sub)
message(STATUS "after: ${MY_VAR}")     # "top" -- unchanged
```

```cmake
# sub/CMakeLists.txt
message(STATUS "in sub: ${MY_VAR}")    # "top"
set(MY_VAR "sub")                       # local to the sub directory
```

The subdirectory's modifications are isolated unless `PARENT_SCOPE` is used (rare for directories -- usually solved by promoting to the cache or restructuring with targets).

## 12.4 Macros Differ From Functions

```cmake
macro(my_macro)
    set(LOCAL_VAR "hello")              # NOT macro-scoped -- leaks to caller!
endmacro()

my_macro()
message(STATUS "after macro: ${LOCAL_VAR}")   # "hello"
```

Macros do **text substitution** in the caller's scope. Their variables leak. `function` is almost always the better choice; reserve `macro` for cases where you specifically need the call-site behaviour (e.g., setting variables in the caller). See Section 15.

## 12.5 Reading and Writing Cache Variables

```cmake
set(MY_OPTION "default" CACHE STRING "Doc string")
option(ENABLE_FOO "Whether to build foo" ON)        # bool option

# Override on command line:
#   cmake -S . -B build -DMY_OPTION=other -DENABLE_FOO=OFF

# Cache variables can be read directly:
if(ENABLE_FOO)
    message(STATUS "Foo enabled")
endif()
```

A `set(VAR ... CACHE ...)` only writes the cache if the variable is **not already** in the cache. To force overwrite, add `FORCE`:

```cmake
set(MY_OPTION "newdefault" CACHE STRING "Doc" FORCE)
```

## 12.6 Cache Variable Types

| Type | Effect in cmake-gui | Notes |
|---|---|---|
| `BOOL` | Checkbox | Accepts `ON/OFF`, `TRUE/FALSE`, `1/0`, `YES/NO`. Use with `option()` |
| `STRING` | Text field | Free text |
| `PATH` | Directory picker | Must be a directory |
| `FILEPATH` | File picker | Must be a file |
| `INTERNAL` | Hidden | For variables CMake should remember but the user shouldn't edit |

The `INTERNAL` type is useful for "remember the result of this expensive check":

```cmake
if(NOT DEFINED MY_DETECTED_FOO)
    # expensive detection...
    set(MY_DETECTED_FOO "/usr/local" CACHE INTERNAL "detected foo prefix")
endif()
```

## 12.7 Variable Lookup Order

When CMake encounters `${VAR}`, the resolution order is:

1. The current function's scope (if inside a function).
2. The current directory's scope (and ancestors via inheritance).
3. The cache.

There is **no** environment lookup unless you explicitly write `$ENV{VAR}`. Conversely, environment variables can be set with `set(ENV{VAR} value)` and read with `$ENV{VAR}`, but they are not pulled into normal variables automatically.

## 12.8 Pitfall: Cache vs Normal Variables

```cmake
option(ENABLE_FOO "..." ON)             # sets ENABLE_FOO=ON in cache

set(ENABLE_FOO OFF)                     # creates a NORMAL variable that shadows the cache
                                        # ${ENABLE_FOO} now reads "OFF"
                                        # but the cache entry is still ON
```

This is policy `CMP0077` (NEW = `option()` respects existing normal variables, OLD = `option()` always overwrites). With CMake >= 3.13 and `cmake_minimum_required(VERSION 3.13)`, `option()` becomes a no-op if a normal variable of the same name exists, which is the modern, predictable behaviour.

## 12.9 Listing What's in Scope

When debugging, dump every variable:

```cmake
get_cmake_property(_vars VARIABLES)
foreach(_v IN LISTS _vars)
    message(STATUS "${_v} = ${${_v}}")
endforeach()
```

For just the cache:

```bash
cmake -L -N build           # list cache vars (no help)
cmake -LH -N build          # with help strings
cmake -LAH -N build         # including advanced + help
```

---

# 13. The Cache, option, and FORCE

---

## 13.1 What the Cache Is

`CMakeCache.txt` is a key-value store in the build directory that persists across `cmake` invocations. Every `set(VAR value CACHE TYPE "doc")` and every `-DVAR=...` on the command line writes here.

```bash
$ cat build/CMakeCache.txt | head -20
# This is the CMakeCache file.
# For build in directory: /home/me/proj/build
# It was generated by CMake: /usr/bin/cmake
# ...
CMAKE_BUILD_TYPE:STRING=Release
CMAKE_CXX_COMPILER:FILEPATH=/usr/bin/g++
CMAKE_CXX_FLAGS:STRING=
CMAKE_CXX_FLAGS_DEBUG:STRING=-g
CMAKE_INSTALL_PREFIX:PATH=/usr/local
ENABLE_FOO:BOOL=ON
//Documentation string for ENABLE_FOO
ENABLE_FOO-ADVANCED:INTERNAL=1
```

Each line is `NAME:TYPE=VALUE`. Documentation is preserved as `//` comments above the entry.

## 13.2 option()

```cmake
option(<name> "<help>" [initial-value])
```

`option` is shorthand for `set(... BOOL CACHE ...)` with a few extras:

```cmake
option(ENABLE_LTO "Enable link-time optimisation" OFF)
option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
option(MY_PROJECT_BUILD_TESTS "Build my_project's tests" ${PROJECT_IS_TOP_LEVEL})
```

Conventions:

- Prefix project-specific options with the project name (`MY_PROJECT_*`) so they don't collide when your library is consumed via `add_subdirectory`.
- Default to `OFF` for features that pull in heavy dependencies.
- Default test/benchmark options to `${PROJECT_IS_TOP_LEVEL}` so consumers don't get them.

## 13.3 set(... CACHE ...) Variants

```cmake
# First-time setting (no overwrite if already in cache)
set(MY_PATH "/opt/default" CACHE PATH "Default install path")

# Force overwrite, e.g. when injecting a dependency's option
set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "" FORCE)

# Mark as advanced (hidden in ccmake/cmake-gui)
mark_as_advanced(BENCHMARK_ENABLE_TESTING)

# Restricted set of allowed values (cmake-gui shows a dropdown)
set(MY_BACKEND "Stub" CACHE STRING "Backend implementation")
set_property(CACHE MY_BACKEND PROPERTY STRINGS "Stub" "Real" "Mock")
```

The "empty doc string + FORCE" idiom is the canonical way to inject an option value into a dependency that you are consuming via `FetchContent` or `add_subdirectory`.

## 13.4 --fresh, -U, and Clean Re-configure

```bash
cmake --fresh -S . -B build              # 3.24+ -- delete cache and re-configure

cmake -U "ENABLE_FOO" -S . -B build      # remove a specific cache entry
cmake -U "ENABLE_*" -S . -B build        # remove by glob

cmake -DENABLE_FOO=ON -S . -B build      # set / overwrite a cache entry
```

`-U` removes entries but keeps the rest of the cache. `--fresh` is equivalent to deleting `CMakeCache.txt` and `CMakeFiles/CMakeConfigureLog.yaml`.

## 13.5 Cache vs Environment

There is no automatic mirroring. Setting `CMAKE_PREFIX_PATH` in the environment and `-DCMAKE_PREFIX_PATH=...` on the command line both work, but for different reasons:

- Environment is consulted by some commands (`find_package` reads `CMAKE_PREFIX_PATH` from both cache and env).
- The cache is consulted by everything via `${VAR}`.

For reproducibility, prefer cache variables and presets over environment.

---

# 14. Lists, Strings, Files, and Paths

---

## 14.1 Lists Are Semicolon-Separated Strings

There is no distinct list type in CMake; a list is a string with semicolons.

```cmake
set(MY_LIST a b c)                       # MY_LIST = "a;b;c"
set(MY_LIST "a;b;c")                     # same thing

list(LENGTH MY_LIST n)                   # n = 3
list(GET MY_LIST 1 x)                    # x = "b"
list(APPEND MY_LIST d)                   # MY_LIST = "a;b;c;d"
list(REMOVE_ITEM MY_LIST b)              # MY_LIST = "a;c;d"
list(REVERSE MY_LIST)
list(SORT MY_LIST)
list(JOIN MY_LIST "," joined)            # joined = "a,c,d"

# Iteration
foreach(item IN LISTS MY_LIST)
    message(STATUS "${item}")
endforeach()
```

The `IN LISTS` form is important: `foreach(item ${MY_LIST})` works only because of variable expansion, and breaks subtly if any list item contains a semicolon or empty element. `IN LISTS` handles it correctly.

## 14.2 List Pitfalls

```cmake
set(A "x;y;z")
set(B "1;2;3")

# Naive concatenation produces nested semicolons:
set(C "${A};${B}")          # "x;y;z;1;2;3"  -- works because CMake flattens

# But quoted, you get a string with a literal semicolon:
set(D "${A}")               # "x;y;z" -- still a list

# Unsetting an item by index requires care; use REMOVE_ITEM or REMOVE_AT
list(REMOVE_AT MY_LIST 0)
```

A common gotcha: passing a list as a single argument quotes it, turning it into one item:

```cmake
function(takes_list)
    list(LENGTH ARGN n)
    message(STATUS "got ${n} args")
endfunction()

set(MY_LIST a b c)
takes_list("${MY_LIST}")     # got 1 args -- the whole list is one string
takes_list(${MY_LIST})       # got 3 args -- unquoted, splits properly
```

## 14.3 string() -- Manipulating Strings

```cmake
string(LENGTH "hello" n)                          # n = 5
string(SUBSTRING "hello" 1 3 s)                   # s = "ell"
string(TOLOWER "Hello" s)                         # s = "hello"
string(REPLACE "world" "earth" out "hello world") # out = "hello earth"
string(STRIP "  hi  " s)                          # s = "hi"
string(REGEX MATCH "[0-9]+" m "abc123def")        # m = "123"
string(REGEX REPLACE "[a-z]" "_" out "abc123")    # out = "___123"
string(JOIN ", " out "one" "two" "three")         # out = "one, two, three"
string(CONFIGURE "@VAR@ is @VAR2@" out @ONLY)     # @VAR@ substitution
```

`string(CONFIGURE ...)` is useful for one-off template expansion inline; the bulkier counterpart is `configure_file()` for files (Section 50).

## 14.4 file() -- Filesystem Operations

```cmake
file(READ path content)
file(WRITE path content)
file(APPEND path content)
file(COPY src DESTINATION dst)
file(REMOVE path)
file(REMOVE_RECURSE dir)
file(MAKE_DIRECTORY dir)
file(GLOB files "*.cpp")                         # configure-time -- beware
file(GLOB_RECURSE files "src/*.cpp")
file(DOWNLOAD url path)
file(SHA256 path output_var)
file(TIMESTAMP path out "%Y-%m-%dT%H:%M:%S")
file(GENERATE OUTPUT path CONTENT "...")         # build-time output
```

`file(GENERATE ...)` is the build-time counterpart to `file(WRITE ...)`. It is essential when content depends on generator expressions:

```cmake
file(GENERATE
    OUTPUT $<TARGET_FILE_DIR:foo>/info.txt
    CONTENT "Built foo at $<TARGET_FILE:foo> for $<CONFIG>\n")
```

`file(WRITE)` would emit `$<...>` literally; `file(GENERATE)` evaluates them per-config.

## 14.5 cmake_path() (3.20+) -- Portable Path Manipulation

```cmake
cmake_path(SET p NORMALIZE "/usr/local/../local/bin")  # p = /usr/local/bin
cmake_path(GET p PARENT_PATH parent)                    # parent = /usr/local
cmake_path(GET p FILENAME fn)                           # fn = bin
cmake_path(APPEND p2 "/usr" "local" "lib")             # p2 = /usr/local/lib
cmake_path(REPLACE_EXTENSION p2 LAST_ONLY ".so")       # p2 = /usr/local/lib.so
```

Before 3.20, you used `get_filename_component()`, which still works but has more confusing keyword names. New code should use `cmake_path`.

## 14.6 String Quoting Cheat Sheet

```cmake
set(A "hello world")        # A is a single string "hello world"
set(B hello world)          # B is a list: "hello;world"

foreach(x IN ITEMS ${A})    # iterates twice ("hello", "world") because A expands and is unquoted
foreach(x IN ITEMS "${A}")  # iterates once ("hello world")
foreach(x IN LISTS A)       # iterates once ("hello world") -- correct treatment of A as a single-element list
```

When in doubt, quote and use `IN LISTS`.

---

# 15. Control Flow, Functions, and Macros

---

## 15.1 Conditions

```cmake
if(<cond>)
    ...
elseif(<cond>)
    ...
else()
    ...
endif()
```

Conditions accept several forms:

| Form | Meaning |
|---|---|
| `if(VAR)` | True if VAR is a non-false constant (`1`, `ON`, `YES`, `TRUE`, `Y`, non-zero number) **or** a defined variable that resolves to such a value |
| `if(NOT VAR)` | Negation |
| `if(A AND B)`, `if(A OR B)` | Boolean operators |
| `if(DEFINED VAR)` | True if VAR has been set (any scope) |
| `if(VAR STREQUAL "foo")` | String equality |
| `if(VAR MATCHES regex)` | Regex match |
| `if(NUM EQUAL 5)`, `LESS`, `GREATER`, `LESS_EQUAL`, `GREATER_EQUAL` | Numeric comparisons |
| `if(VER VERSION_LESS 1.2.3)` | Version comparison (handles `1.10 > 1.9`) |
| `if(EXISTS path)`, `if(IS_DIRECTORY path)`, `if(IS_ABSOLUTE path)` | Filesystem checks |
| `if(TARGET name)` | True if a CMake target with that name exists |
| `if(POLICY CMP0123)` | True if the policy is known to this CMake |
| `if(COMMAND foo)` | True if `foo` is a known command/function |

## 15.2 if() Auto-Dereference Surprise

```cmake
set(A "B")
set(B "hello")

if(A STREQUAL "hello")        # TRUE!  -- A is auto-dereferenced to "B", which is a variable, so dereferenced again
if("A" STREQUAL "hello")      # FALSE  -- literal "A"
```

The historical `if()` auto-dereferences unquoted operands. The result is that `if(A STREQUAL B)` compares the **values** of A and B. Policy `CMP0054` (NEW since 3.1) changed quoted arguments to no longer be auto-dereferenced; modern code should quote string literals.

## 15.3 foreach Variants

```cmake
foreach(i RANGE 5)                       # 0,1,2,3,4,5
foreach(i RANGE 1 10 2)                  # 1,3,5,7,9
foreach(item IN LISTS my_list)
foreach(item IN ITEMS a b c)
foreach(item IN LISTS list1 list2 ITEMS x y)
foreach(item IN ZIP_LISTS xs ys)         # 3.17+: parallel iteration
    # ${item_0}, ${item_1} hold the i-th elements
endforeach()
```

`foreach(... IN ZIP_LISTS ...)` is the modern way to iterate two lists in parallel; the variables `${var_0}`, `${var_1}` hold the items at the same index.

## 15.4 while

```cmake
set(i 0)
while(i LESS 10)
    math(EXPR i "${i} + 1")
endwhile()
```

`math(EXPR ...)` is the calculator. Rarely needed in CMake code -- if you find yourself doing arithmetic, you may be on the wrong track.

## 15.5 function vs macro

```cmake
function(my_func arg1 arg2)
    # arg1 and arg2 are arguments; ARGN holds extra args
    # ARGC = total count; ARGV0, ARGV1, ... are positional
    # Variables set here are LOCAL to the function
    set(${arg2} "result" PARENT_SCOPE)
endfunction()

macro(my_macro arg1 arg2)
    # arg1, arg2, ARGN are text-substituted; no real scope
    # Variables set here leak to the caller
    set(${arg2} "result")               # no PARENT_SCOPE needed -- already in caller
endmacro()
```

| Feature | `function` | `macro` |
|---|---|---|
| Variable scope | New, local | Caller's |
| `return()` exits | The function | The caller (!) |
| `ARGN`, `ARGV`, `ARGC` | Real lists | Text substitution -- subtly different |
| Performance | Slightly slower (scope push) | Slightly faster |
| When to use | Almost always | Only when you need text-substitution semantics |

The classic macro use case is "wrap a built-in to set things in the caller's scope":

```cmake
macro(set_if_not_defined var value)
    if(NOT DEFINED ${var})
        set(${var} "${value}")
    endif()
endmacro()
```

A function version would need `PARENT_SCOPE`.

## 15.6 cmake_parse_arguments

For functions taking named arguments:

```cmake
function(add_my_test)
    set(options FAST)
    set(one_value_args NAME WORKING_DIR)
    set(multi_value_args ARGS DEPENDS)
    cmake_parse_arguments(MT
        "${options}" "${one_value_args}" "${multi_value_args}"
        ${ARGN})

    # Now MT_FAST, MT_NAME, MT_WORKING_DIR, MT_ARGS, MT_DEPENDS are populated.
    # MT_UNPARSED_ARGUMENTS holds anything not recognised.

    if(NOT MT_NAME)
        message(FATAL_ERROR "add_my_test: NAME is required")
    endif()

    add_test(NAME ${MT_NAME}
             COMMAND ${MT_ARGS}
             WORKING_DIRECTORY ${MT_WORKING_DIR})
endfunction()

add_my_test(NAME smoke ARGS smoke_test --verbose FAST)
```

`cmake_parse_arguments` is the bedrock of every modern CMake helper. The convention is:

- Three lists: option flags (booleans), single-value args, multi-value args.
- A prefix (`MT_` above) for the populated variables.

## 15.7 return() and break() and continue()

```cmake
function(check_thing)
    if(NOT EXISTS "/etc/passwd")
        message(WARNING "Skipping; no passwd file")
        return()                  # exits the function
    endif()
    # ...
endfunction()

foreach(x IN LISTS items)
    if(x STREQUAL "stop")
        break()
    endif()
    if(x STREQUAL "skip")
        continue()
    endif()
endforeach()
```

In CMake 3.25+, `return(PROPAGATE var1 var2 ...)` can simultaneously return and propagate variables to the parent scope -- a tidier alternative to manual `set(... PARENT_SCOPE)`.

---

# Part 5: Generator Expressions

---

# 16. Anatomy of Generator Expressions

---

## 16.1 What They Are

Generator expressions are strings of the form `$<...>` that are **left alone at configure time** and **evaluated at generate time**. This lets them produce different values per build configuration, per target, per source file, per generator.

```cmake
target_compile_options(foo PRIVATE
    $<$<CONFIG:Debug>:-O0 -g>
    $<$<CONFIG:Release>:-O3 -DNDEBUG>
    $<$<CXX_COMPILER_ID:MSVC>:/utf-8 /permissive->)
```

At configure time, this is just a list of literal `$<...>` strings stored on the target. At generate time, when CMake writes the actual `build.ninja` (or per-config `.vcxproj`), it evaluates each expression for the current configuration and compiler.

## 16.2 The Two-Stage Model in Action

```
Configure time: foo's COMPILE_OPTIONS property holds:
    $<$<CONFIG:Debug>:-O0 -g>;$<$<CONFIG:Release>:-O3 -DNDEBUG>;$<$<CXX_COMPILER_ID:MSVC>:/utf-8 /permissive->

Generate time (Ninja, Debug, GCC):
    Evaluates to: -O0 -g

Generate time (Ninja, Release, GCC):
    Evaluates to: -O3 -DNDEBUG

Generate time (VS 2022 multi-config, Debug, MSVC):
    Evaluates to: -O0 -g /utf-8 /permissive-
```

This is why `message(STATUS "${target_property}")` shows the raw `$<...>` strings -- you are reading at configure time, when generator expressions are still strings.

## 16.3 Syntax

```
$<expression>                 # single-argument
$<expression:value>           # conditional/transform
$<expression:value,arg2,...>  # multi-arg
```

The grammar is recursive: any value can itself be a generator expression. Nesting is common:

```cmake
$<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:GNU>>:-fsanitize=address>
```

This reads: "if the build configuration is Debug AND the compiler is GNU, emit `-fsanitize=address`".

## 16.4 Where They Can Be Used

| Location | Generator expressions supported? |
|---|---|
| `target_*` commands (include dirs, link libs, compile options, ...) | Yes |
| `add_test`, `set_tests_properties` | Yes |
| `install` (TARGETS, FILES) | Yes |
| `file(GENERATE)` | Yes |
| `add_custom_command`, `add_custom_target` | Yes (for COMMAND and arguments) |
| `set()`, `message()`, `if()` -- regular commands | **No** -- they see raw strings |
| `configure_file()` | **No** -- use `file(GENERATE)` instead for genex content |

This is one of the most common "why doesn't my CMake work?" moments: trying to use a generator expression in a regular variable or `message()` call. They only evaluate inside contexts that survive to generate time.

## 16.5 Reading Generator Expressions

```
$<CONFIG:Debug>                    -> "1" if current config is Debug, else "0"
$<$<CONFIG:Debug>:-O0>             -> "-O0" if current config is Debug, else ""
$<$<CONFIG:Debug>:flag,otherflag>  -> "flag" if Debug, "otherflag" otherwise (3-arg form: $<IF:...>)
$<IF:$<CONFIG:Debug>,a,b>          -> "a" if Debug, "b" otherwise
```

The two most-used forms are:

1. `$<COND:value>` -- emit `value` if `COND` is truthy, otherwise empty.
2. `$<IF:COND,then,else>` -- emit `then` or `else`.

---

# 17. Common Generator Expressions

---

## 17.1 Configuration

```cmake
$<CONFIG>                            # current config: Debug, Release, RelWithDebInfo, MinSizeRel
$<CONFIG:Debug>                      # "1" if Debug, "0" otherwise
$<CONFIG:Debug,RelWithDebInfo>       # "1" if either Debug or RelWithDebInfo
```

## 17.2 Compiler and Platform

```cmake
$<CXX_COMPILER_ID>                   # GNU, Clang, AppleClang, MSVC, Intel, IntelLLVM, ...
$<CXX_COMPILER_ID:GNU>               # 1/0
$<CXX_COMPILER_ID:GNU,Clang>         # 1 if either
$<CXX_COMPILER_VERSION>              # e.g. "13.2.0"
$<CXX_COMPILER_VERSION:13.2.0>       # exact-version test (rare; prefer VERSION_GREATER_EQUAL)
$<COMPILE_LANG_AND_ID:CXX,GNU>       # 1 if compiling C++ with GNU
$<PLATFORM_ID>                       # Linux, Darwin, Windows, FreeBSD, ...
$<PLATFORM_ID:Linux>
```

`COMPILE_LANG_AND_ID` is essential when a target mixes C and C++ -- it lets you apply C++-only flags without breaking the C compile.

## 17.3 Target Queries

```cmake
$<TARGET_FILE:foo>                   # full path to foo's output (lib.so, exe, ...)
$<TARGET_FILE_NAME:foo>              # just the filename
$<TARGET_FILE_DIR:foo>               # the directory containing the output
$<TARGET_OBJECTS:foo_obj>            # list of object files in an OBJECT library
$<TARGET_PROPERTY:foo,LINK_LIBRARIES>
$<TARGET_EXISTS:foo>                 # 3.12+
$<TARGET_GENEX_EVAL:foo,$<...>>      # evaluate a genex in foo's context (3.12+)
```

`$<TARGET_FILE:foo>` is the canonical way to refer to "wherever the build system actually placed foo's output", including per-config subdirectories on multi-config generators.

## 17.4 String/Logic Operations

```cmake
$<NOT:cond>
$<AND:c1,c2,...>
$<OR:c1,c2,...>
$<BOOL:value>                        # convert to 0/1 by CMake truthiness
$<STREQUAL:a,b>
$<EQUAL:1,2>
$<IN_LIST:item,list>                 # 3.12+
$<VERSION_LESS:1.2,1.3>
$<VERSION_GREATER_EQUAL:13,12>
$<LOWER_CASE:Hello>                  # "hello"
$<JOIN:list,,>                       # join with delimiter
```

## 17.5 List/Filter Operations (3.15+)

```cmake
$<FILTER:list,INCLUDE,regex>         # keep matching items
$<FILTER:list,EXCLUDE,regex>         # drop matching items
$<GENEX_EVAL:expr>                   # re-evaluate the result of expr
$<REMOVE_DUPLICATES:list>
$<TARGET_PROPERTY:foo,SOURCES>       # often combined with FILTER
```

## 17.6 Common Patterns

### Per-compiler warning flags

```cmake
target_compile_options(foo PRIVATE
    $<$<COMPILE_LANG_AND_ID:CXX,GNU,Clang,AppleClang>:-Wall -Wextra -Wpedantic>
    $<$<COMPILE_LANG_AND_ID:CXX,MSVC>:/W4 /permissive- /utf-8>)
```

### Sanitiser flag, only on supported compilers + debug

```cmake
target_compile_options(foo PRIVATE
    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:GNU,Clang>>:-fsanitize=address -fno-omit-frame-pointer>)
target_link_options(foo PRIVATE
    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:GNU,Clang>>:-fsanitize=address>)
```

### Per-platform include directory

```cmake
target_include_directories(foo PRIVATE
    $<$<PLATFORM_ID:Linux>:linux>
    $<$<PLATFORM_ID:Darwin>:macos>
    $<$<PLATFORM_ID:Windows>:win>)
```

### Compile-time symbol with version

```cmake
target_compile_definitions(foo PUBLIC
    FOO_VERSION="${PROJECT_VERSION}"
    FOO_VERSION_MAJOR=${PROJECT_VERSION_MAJOR})
```

(No genex needed -- these are configure-time constants.)

---

# 18. Conditional Linking and Per-Config Flags

---

## 18.1 Linking Against a Library Only in Debug

```cmake
target_link_libraries(my_app
    PRIVATE
        $<$<CONFIG:Debug>:my_debug_helper>)
```

The naive `if(CMAKE_BUILD_TYPE STREQUAL Debug)` does **not** work on multi-config generators (Visual Studio, Xcode), because configure-time has no fixed `CMAKE_BUILD_TYPE`. Always use generator expressions for config-dependent linking.

## 18.2 Per-Config Compile Flags

```cmake
target_compile_options(my_lib PRIVATE
    $<$<CONFIG:Debug>:-O0 -g3 -DDEBUG_FOO>
    $<$<CONFIG:Release>:-O3 -DNDEBUG -DRELEASE_FOO>
    $<$<CONFIG:RelWithDebInfo>:-O2 -g -DNDEBUG>
    $<$<CONFIG:MinSizeRel>:-Os -DNDEBUG>)
```

Equivalent using config-specific properties (older style):

```cmake
target_compile_options(my_lib PRIVATE
    "$<$<CONFIG:Debug>:-O0;-g3>"
    "$<$<CONFIG:Release>:-O3>")
```

The semicolons inside genex strings are how multi-value arguments are passed; quote the entire genex to keep CMake from splitting.

## 18.3 Per-Compiler Linker Flags

```cmake
target_link_options(my_app PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wl,--as-needed>
    $<$<CXX_COMPILER_ID:MSVC>:/INCREMENTAL:NO>)
```

## 18.4 Optional Link Libraries

```cmake
find_package(OpenSSL QUIET)

target_link_libraries(my_app
    PRIVATE
        $<$<TARGET_EXISTS:OpenSSL::SSL>:OpenSSL::SSL>)
target_compile_definitions(my_app
    PRIVATE
        $<$<TARGET_EXISTS:OpenSSL::SSL>:HAS_OPENSSL>)
```

If OpenSSL is found, link it and define `HAS_OPENSSL`. Otherwise, do neither. The conditional flows naturally without nested `if()` blocks.

## 18.5 The "Don't Repeat Yourself" Trick

```cmake
# Define a per-config flag set once
set(_debug_flags -O0 -g -fno-omit-frame-pointer -DDEBUG_LOGGING)
set(_release_flags -O3 -DNDEBUG -ffunction-sections -fdata-sections)

target_compile_options(foo PRIVATE
    $<$<CONFIG:Debug>:${_debug_flags}>
    $<$<CONFIG:Release,RelWithDebInfo>:${_release_flags}>)
```

The variable expands at configure time (so the list contents are textually inserted), but the `$<CONFIG:...>` test runs at generate time.

---

# 19. BUILD_INTERFACE vs INSTALL_INTERFACE

---

## 19.1 The Two Lives of a Target

A target lives in two worlds:

1. **In-tree (BUILD)** -- inside the build directory, in your project. Headers live next to sources in the source tree.
2. **Installed (INSTALL)** -- on the consumer's machine. Headers live under `${CMAKE_INSTALL_PREFIX}/include`. The original source tree is gone.

These two worlds need **different paths** for include directories. The dance is solved with two generator expressions:

```cmake
target_include_directories(foo
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>)
```

- `$<BUILD_INTERFACE:...>` -- emits the value when the target is being consumed **inside** the build tree (e.g. via `add_subdirectory` or `FetchContent`).
- `$<INSTALL_INTERFACE:...>` -- emits the value when the target is being consumed **after install** (via `find_package` and the generated `FooConfig.cmake`).

## 19.2 Why Both?

```
BUILD context  (during build, or downstream via add_subdirectory):
    target_include_directories: /home/me/foo/include
    Consumer's compile:  -I/home/me/foo/include

INSTALL context (after `cmake --install`, downstream via find_package):
    target_include_directories: ${CMAKE_INSTALL_PREFIX}/include
    Consumer's compile:  -I/opt/foo/include
```

Without the two interface generator expressions:

- Using only `BUILD_INTERFACE` -- the installed package would have **no** include path, causing consumer build failures.
- Using only `INSTALL_INTERFACE` -- in-tree consumers (subdirectory/FetchContent) would have no include path, causing the same failure inside your own monorepo.
- Using a plain path (no genex) -- the build tree's absolute path would leak into the installed config file. Consumers on a different machine would get broken `-I/home/me/foo/include` lines.

## 19.3 The Same Pattern for Sources and Definitions

```cmake
target_compile_definitions(foo
    PUBLIC
        $<BUILD_INTERFACE:FOO_BUILDING>
        $<INSTALL_INTERFACE:FOO_INSTALLED>)
```

In practice, most projects only need `BUILD_INTERFACE`/`INSTALL_INTERFACE` for include directories; flags and definitions tend to be the same in both contexts.

## 19.4 The Full Install Recipe Preview

```cmake
include(GNUInstallDirs)

target_include_directories(foo
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

install(TARGETS foo
    EXPORT FooTargets
    LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR})

install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT FooTargets
    FILE FooTargets.cmake
    NAMESPACE Foo::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/Foo)
```

The `install(EXPORT)` produces a `FooTargets.cmake` consumed via `find_package(Foo)`. The `INSTALL_INTERFACE` paths from above are baked into this file. Section 38 has the full install dance.

---

# Part 6: Configurations, Toolchains, and Presets

---

# 20. Build Configurations and Multi-Config Generators

---

## 20.1 The Four Standard Configurations

CMake defines four canonical build configurations:

| Configuration | Optimisation | Debug info | NDEBUG | Typical flags (GCC/Clang) |
|---|---|---|---|---|
| `Debug` | `-O0` | `-g` | not defined | `-O0 -g` |
| `Release` | `-O3` | none | defined | `-O3 -DNDEBUG` |
| `RelWithDebInfo` | `-O2` | `-g` | defined | `-O2 -g -DNDEBUG` |
| `MinSizeRel` | `-Os` | none | defined | `-Os -DNDEBUG` |

These map to per-config `CMAKE_<LANG>_FLAGS_<CONFIG>` variables (`CMAKE_CXX_FLAGS_DEBUG`, `CMAKE_CXX_FLAGS_RELEASE`, ...). Custom configurations are possible but rarely needed.

## 20.2 Single-Config vs Multi-Config Generators

This is one of the most important practical distinctions in CMake.

| Aspect | Single-config generator | Multi-config generator |
|---|---|---|
| Examples | Ninja, Make, Ninja Multi-Config (3.17+) | Visual Studio, Xcode |
| When configuration is chosen | Configure time, via `-DCMAKE_BUILD_TYPE=Release` | Build time, via `--config Release` |
| Build directory layout | Single set of artifacts | Per-config subdirectories (`Debug/`, `Release/`) |
| To get multiple configs | Configure multiple build dirs | Build all configs in one dir |
| `CMAKE_BUILD_TYPE` at configure | Set by user; CMake honours it | Empty -- CMake ignores it |
| `$<CONFIG>` at generate | Evaluates to the configured type | Evaluates per build action |

```bash
# Single-config (Ninja): one config per build dir
cmake -S . -B build-debug   -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake -S . -B build-release -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build-debug
cmake --build build-release

# Multi-config (Visual Studio): one build dir, build each config separately
cmake -S . -B build -G "Visual Studio 17 2022"
cmake --build build --config Debug
cmake --build build --config Release
```

## 20.3 Always Use $<CONFIG> for Config Logic

Because `CMAKE_BUILD_TYPE` is empty on multi-config generators, this is **wrong** for cross-generator code:

```cmake
# WRONG -- breaks on Visual Studio / Xcode
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_definitions(foo PRIVATE MY_DEBUG)
endif()
```

The right pattern uses a generator expression:

```cmake
target_compile_definitions(foo PRIVATE $<$<CONFIG:Debug>:MY_DEBUG>)
```

## 20.4 Setting a Default CMAKE_BUILD_TYPE

A common idiom for single-config generators:

```cmake
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
        Debug Release RelWithDebInfo MinSizeRel)
endif()
```

`CMAKE_CONFIGURATION_TYPES` is the multi-config equivalent: the list of configurations a multi-config generator should produce. If neither is set, you default to Release (a defensible choice for a library; for an application some prefer Debug).

## 20.5 Ninja Multi-Config

CMake 3.17 added `Ninja Multi-Config`, a generator that gives you Ninja's speed with multi-config's ergonomics:

```bash
cmake -S . -B build -G "Ninja Multi-Config" \
      -DCMAKE_CONFIGURATION_TYPES="Debug;Release;RelWithDebInfo"
cmake --build build --config Debug
cmake --build build --config Release
```

Output ends up in `build/Debug/`, `build/Release/`, etc. Targets are reusable between configs without reconfigure.

---

# 21. The C++ Standard

---

## 21.1 Two Ways to Say "C++20"

```cmake
# Approach 1: target property (recommended)
set_target_properties(foo PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF)

# Approach 2: feature requirement (also recommended)
target_compile_features(foo PUBLIC cxx_std_20)
```

| Aspect | `CXX_STANDARD` | `target_compile_features(... cxx_std_NN)` |
|---|---|---|
| Scope | Target-only | Honours PUBLIC/PRIVATE/INTERFACE |
| Propagates to consumers? | No | Yes (if PUBLIC or INTERFACE) |
| What it means | "Compile this target with at least C++NN" | "This target and possibly its consumers need at least C++NN" |
| Strictness | With `CXX_STANDARD_REQUIRED ON`, CMake errors if compiler can't | Always requires |
| Per-language | Set per language (`CXX_`, `C_`) | Per language token |

The `target_compile_features` form is preferred for libraries because it carries through to consumers.

## 21.2 The Global Default

```cmake
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```

These cache-like variables set the **defaults** for every subsequently-created target. They don't override per-target settings, so they are a fine "one line for the whole project" approach.

| Variable | Default | Effect |
|---|---|---|
| `CMAKE_CXX_STANDARD` | (none) | Minimum C++ standard (`11`, `14`, `17`, `20`, `23`) |
| `CMAKE_CXX_STANDARD_REQUIRED` | `OFF` | If ON, fail when compiler can't reach the standard; if OFF, fall back |
| `CMAKE_CXX_EXTENSIONS` | `ON` | If OFF, use `-std=c++NN` instead of `-std=gnu++NN` (strict ISO mode) |

Most projects want `STANDARD_REQUIRED ON` and `EXTENSIONS OFF` to avoid silent fallback to older standards and accidental GNU-only extension usage.

## 21.3 Per-Target Overrides

```cmake
add_library(legacy_lib src/legacy.cpp)
set_target_properties(legacy_lib PROPERTIES
    CXX_STANDARD 11)               # this one library still C++11

add_library(modern_lib src/modern.cpp)
target_compile_features(modern_lib PUBLIC cxx_std_23)
```

Mixing standards is allowed -- each translation unit compiles with its target's setting.

## 21.4 Feature Flags vs Standard

CMake also exposes individual C++ feature flags (`cxx_constexpr`, `cxx_lambdas`, `cxx_variadic_templates`, ...):

```cmake
target_compile_features(foo PRIVATE cxx_constexpr cxx_lambdas)
```

In practice, almost everyone uses `cxx_std_NN`. Individual feature flags are legacy from CMake 3.1-3.7 era.

## 21.5 Detecting the Standard at Compile Time

CMake doesn't expose the chosen standard to source code; you check the standard's predefined macros:

```cpp
#if __cplusplus >= 202002L
    // C++20 or newer
#endif
```

On MSVC the `__cplusplus` value is by default `199711L` unless you pass `/Zc:__cplusplus`. The standard preset for new projects adds `/Zc:__cplusplus /permissive- /utf-8` to MSVC builds:

```cmake
target_compile_options(foo PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/Zc:__cplusplus /permissive- /utf-8>)
```

---

# 22. Toolchain Files and Cross-Compilation

---

## 22.1 What a Toolchain File Does

A toolchain file is a `.cmake` file that tells CMake "you are building **for** a different platform than you are running **on**". It typically sets:

- `CMAKE_SYSTEM_NAME`, `CMAKE_SYSTEM_PROCESSOR` -- the target system.
- `CMAKE_C_COMPILER`, `CMAKE_CXX_COMPILER` -- the cross-compiler binaries.
- `CMAKE_SYSROOT`, `CMAKE_FIND_ROOT_PATH` -- where to find target headers and libraries.
- `CMAKE_FIND_ROOT_PATH_MODE_*` -- how `find_*` commands should behave (search target sysroot vs host).

The file is passed via `-DCMAKE_TOOLCHAIN_FILE=path/to/toolchain.cmake` at configure time.

## 22.2 Minimal Cross-Compile Toolchain (ARM Linux on x86_64 Host)

```cmake
# aarch64-linux.cmake
set(CMAKE_SYSTEM_NAME      Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

set(CMAKE_C_COMPILER   aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)

set(CMAKE_SYSROOT       /usr/aarch64-linux-gnu)
set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})

# Don't look on the host for programs by default; do look on the host for tools
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
```

Usage:

```bash
cmake -S . -B build-arm \
      -DCMAKE_TOOLCHAIN_FILE=cmake/aarch64-linux.cmake \
      -DCMAKE_BUILD_TYPE=Release
cmake --build build-arm
```

## 22.3 The FIND_ROOT_PATH_MODE Matrix

| Variable | What it controls | Typical value for cross |
|---|---|---|
| `CMAKE_FIND_ROOT_PATH_MODE_PROGRAM` | `find_program` (compilers, code generators) | `NEVER` (use host tools) |
| `CMAKE_FIND_ROOT_PATH_MODE_LIBRARY` | `find_library` | `ONLY` (target sysroot only) |
| `CMAKE_FIND_ROOT_PATH_MODE_INCLUDE` | `find_path` | `ONLY` |
| `CMAKE_FIND_ROOT_PATH_MODE_PACKAGE` | `find_package` config files | `ONLY` |

| Value | Meaning |
|---|---|
| `NEVER` | Don't use the root path -- look on the host |
| `ONLY` | Only look under the root path -- not on the host |
| `BOTH` | Look both places (default) |

`NEVER` for programs is the key cross-compile setting: you want `protoc` and `python` from the host, but `libssl.a` from the target sysroot.

## 22.4 Embedded / Bare-Metal Cross

```cmake
# arm-none-eabi.cmake
set(CMAKE_SYSTEM_NAME      Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)   # no linker yet -> static only

set(CMAKE_C_COMPILER   arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)
set(CMAKE_ASM_COMPILER arm-none-eabi-as)

set(CMAKE_C_FLAGS_INIT   "-mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16")
set(CMAKE_CXX_FLAGS_INIT "${CMAKE_C_FLAGS_INIT}")
```

`CMAKE_SYSTEM_NAME Generic` tells CMake "no operating system" -- standard libraries that depend on syscalls (e.g., `pthreads`) don't apply. `CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY` avoids requiring a working linker during compiler detection, which matters in bare-metal where linking needs a custom linker script.

## 22.5 Pre-Made Toolchain Files

| Toolchain | Source |
|---|---|
| **Android NDK** | `$NDK/build/cmake/android.toolchain.cmake` |
| **iOS** | Use Xcode generator with `CMAKE_SYSTEM_NAME=iOS`, `CMAKE_OSX_DEPLOYMENT_TARGET`, `CMAKE_OSX_ARCHITECTURES` |
| **Emscripten** | `$EMSDK/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake` (use `emcmake cmake ...`) |
| **vcpkg** | `$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake` (wraps your toolchain) |
| **Conan 2** | Generated `conan_toolchain.cmake` |

These are battle-tested and almost always preferable to rolling your own.

## 22.6 Detecting Cross-Compile in CMakeLists.txt

```cmake
if(CMAKE_CROSSCOMPILING)
    # we're cross-compiling; skip running tests on the host
endif()

if(NOT CMAKE_CROSSCOMPILING)
    add_subdirectory(host_tools)
endif()
```

`CMAKE_CROSSCOMPILING` is set automatically when a toolchain file declares a target system different from the host.

---

# 23. CMake Presets

---

## 23.1 Why Presets

Hand-rolling `cmake -S . -B build-debug-asan -G Ninja -DCMAKE_BUILD_TYPE=Debug -DENABLE_ASAN=ON -DCMAKE_CXX_COMPILER=clang++ ...` every time gets old. CMake Presets (3.19+, mature in 3.23+) move this configuration into a checked-in JSON file:

```json
{
    "version": 6,
    "cmakeMinimumRequired": { "major": 3, "minor": 23, "patch": 0 },
    "configurePresets": [
        {
            "name": "default",
            "displayName": "Default Release",
            "generator": "Ninja",
            "binaryDir": "${sourceDir}/build/${presetName}",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Release",
                "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
            }
        }
    ],
    "buildPresets": [
        { "name": "default", "configurePreset": "default" }
    ],
    "testPresets": [
        { "name": "default", "configurePreset": "default",
          "output": { "outputOnFailure": true } }
    ]
}
```

Usage:

```bash
cmake --preset default
cmake --build --preset default
ctest --preset default
```

## 23.2 The File Layout

| File | Tracked in VCS? | Purpose |
|---|---|---|
| `CMakePresets.json` | Yes | Shared project presets |
| `CMakeUserPresets.json` | No (gitignored) | Personal/local overrides |

`CMakeUserPresets.json` can `inheritFrom` presets in `CMakePresets.json`, override one or two settings, and add user-only presets without touching the project file.

## 23.3 Inheritance

```json
{
    "version": 6,
    "configurePresets": [
        {
            "name": "base",
            "hidden": true,
            "generator": "Ninja Multi-Config",
            "binaryDir": "${sourceDir}/build/${presetName}",
            "cacheVariables": {
                "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
            }
        },
        {
            "name": "gcc-release",
            "inherits": "base",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Release",
                "CMAKE_C_COMPILER": "gcc",
                "CMAKE_CXX_COMPILER": "g++"
            }
        },
        {
            "name": "clang-asan",
            "inherits": "base",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Debug",
                "CMAKE_C_COMPILER": "clang",
                "CMAKE_CXX_COMPILER": "clang++",
                "ENABLE_ASAN": "ON"
            }
        }
    ]
}
```

`hidden: true` means the preset can be inherited but not used directly. Single-inheritance is most common; multiple inheritance is supported but tricky.

## 23.4 Conditions

```json
{
    "name": "msvc-release",
    "condition": {
        "type": "equals",
        "lhs": "${hostSystemName}",
        "rhs": "Windows"
    },
    "generator": "Visual Studio 17 2022"
}
```

Presets can be conditioned on host system, environment variables, or arbitrary boolean expressions. `cmake --list-presets` only shows presets whose conditions evaluate true on this machine.

## 23.5 Macros in Presets

| Macro | Expands to |
|---|---|
| `${sourceDir}` | The top-level source directory |
| `${sourceParentDir}` | Parent of source dir |
| `${sourceDirName}` | Basename of source dir |
| `${presetName}` | The current preset's name |
| `${generator}` | The chosen generator |
| `${hostSystemName}` | Windows/Linux/Darwin |
| `${dollar}` | A literal `$` |
| `$env{VAR}` | An environment variable |
| `$penv{VAR}` | An environment variable as seen by the preset launcher (before any preset-set env) |

## 23.6 The Full Lifecycle

```bash
cmake --list-presets                     # list configure presets
cmake --preset clang-asan                # configure using preset
cmake --build --preset clang-asan-build  # build using build preset
ctest --preset clang-asan-test           # run tests using test preset
cpack --preset clang-asan-package        # build packages using package preset
```

Presets v6 (CMake 3.25+) introduced **package presets** (for `cpack`) and **workflow presets** that chain configure -> build -> test -> package in one command:

```json
{
    "workflowPresets": [
        {
            "name": "release-workflow",
            "steps": [
                { "type": "configure", "name": "gcc-release" },
                { "type": "build",     "name": "gcc-release-build" },
                { "type": "test",      "name": "gcc-release-test" },
                { "type": "package",   "name": "gcc-release-package" }
            ]
        }
    ]
}
```

```bash
cmake --workflow --preset release-workflow
```

This is the cleanest cross-platform CI entry point a modern CMake project can offer.

## 23.7 Presets vs Toolchain Files

| Preset | Toolchain |
|---|---|
| Set generator, cache vars, env | Set compilers, sysroot, find rules |
| Pre-build user-facing UX | CMake-internal cross-compile mechanism |
| Can specify a toolchain (`toolchainFile`) | Used by a preset to wire things up |

The two are complementary, not competing. A preset usually points to a toolchain file plus the per-build choices on top.

---

# Part 7: Generators and Build Drivers

---

# 24. Generators: Ninja, Make, Visual Studio, Xcode

---

## 24.1 The Generator List

A **generator** is the CMake plugin that emits native build files. `cmake -G "Generator Name"` selects one; `cmake --help` lists all generators on your platform.

| Generator | Output | Platforms | Single/Multi-config |
|---|---|---|---|
| `Ninja` | `build.ninja` | All | Single |
| `Ninja Multi-Config` | `build.ninja` per config | All (3.17+) | Multi |
| `Unix Makefiles` | `Makefile` | Unix, macOS, MinGW | Single |
| `MinGW Makefiles` | `Makefile` (MinGW-flavoured) | Windows + MinGW | Single |
| `NMake Makefiles` | `Makefile` (MS NMake) | Windows + MSVC | Single |
| `Visual Studio 17 2022` | `.sln` + `.vcxproj` | Windows | Multi |
| `Visual Studio 16 2019` | `.sln` + `.vcxproj` | Windows | Multi |
| `Xcode` | `.xcodeproj` | macOS | Multi |
| `CodeBlocks - <native>` | CodeBlocks project | All (deprecated by most IDEs) | Per-native |
| `Eclipse CDT4 - <native>` | Eclipse project | All (largely abandoned) | Per-native |

## 24.2 Picking a Generator

```
        +-----------------------------+
        | Are you on Windows + VS?    |---no---+
        +-------------+---------------+        |
                      yes                      |
                      |                        v
        +-------------v---------------+    +---+---+
        | Want IDE integration?       |    | Ninja |  <-- default for new code
        +--+----------------------+---+    +-------+
           |                      |
           |  yes                 | no
           v                      v
    +------+------+         +-----+-----+
    | Visual      |         |   Ninja   |
    | Studio 17   |         | (faster   |
    | 2022        |         |  than NMake)|
    +-------------+         +-----------+
```

**Ninja** is the recommended generator for almost every project on every platform. It is the fastest, has the cleanest dependency graph, and is what every CI system, IDE (via `cmake --build`), and tooling expects to find a `compile_commands.json` from.

## 24.3 Generator-Specific Quirks

| Generator | Quirk |
|---|---|
| Ninja | `CMAKE_BUILD_TYPE` mandatory if you want optimisation. No `make clean` -- use `ninja -t clean`. |
| Make | Slow incremental builds on large trees; `make -j` doesn't respect modules |
| Visual Studio | Multi-config -- `CMAKE_BUILD_TYPE` ignored. Use `--config Release` |
| Xcode | Multi-config. `CMAKE_OSX_DEPLOYMENT_TARGET`, `CMAKE_OSX_ARCHITECTURES` matter |
| NMake | Single-threaded by default -- almost always inferior to Ninja |
| MinGW | `sh.exe` from MSYS must not be on PATH or generation fails |

## 24.4 Switching Generators

You **cannot** switch generators in an existing build directory. CMake will refuse:

```
You have changed variables that require your cache to be deleted.
Configure will be re-run and you may have to reset some variables.
```

The remedy is to delete the build directory or use `--fresh`:

```bash
rm -rf build && cmake -S . -B build -G Ninja
# or
cmake --fresh -S . -B build -G Ninja
```

## 24.5 -G Aliases

For Visual Studio specifically, CMake also accepts an architecture in `-A`:

```bash
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake -S . -B build -G "Visual Studio 17 2022" -A ARM64
cmake -S . -B build -G "Visual Studio 17 2022" -A Win32   # explicit 32-bit
```

The toolset is `-T`:

```bash
cmake -S . -B build -G "Visual Studio 17 2022" -A x64 -T ClangCL
```

This builds VS solution files but uses Clang/LLVM as the compiler -- a common request from teams who want VS IDE integration but a different compiler.

---

# 25. Ninja Deep Dive

---

## 25.1 Why Ninja Won

Ninja was created (2010) explicitly as a target for higher-level meta-build systems. Its goals: be fast, do one thing well (run a dependency graph), and be **human-unfriendly** to write -- the syntax is intentionally austere so people don't try to write it by hand.

| Property | Ninja | GNU Make |
|---|---|---|
| Designed to be hand-written? | No | Yes |
| Implicit rules | None | Many built-in (`%.o: %.c`, etc.) |
| Variable expansion | One pass, lazy | Multiple passes, eager |
| Header dependency files (`.d`) | First-class via `depfile = ...` | Add-on (`-MMD`) |
| Parallel job launching | Optimised, fork+exec | `make -j` is correct but slower at scale |
| Build time on identical large tree | Baseline | Often 2-5x slower |

## 25.2 Inspecting What Ninja Will Do

```bash
ninja -n build_target            # dry run: print commands but don't execute
ninja -t targets all             # list all targets
ninja -t deps                    # show header-dep info that Ninja has cached
ninja -t commands                # show full command for each target
ninja -t graph foo               # graphviz dot output for foo's deps
ninja -t recompact               # recompact .ninja_deps
ninja -t cleandead               # remove output files no longer mentioned
```

`ninja -t graph foo | dot -Tpng > foo.png` gives a visual dependency graph -- invaluable when wondering why something is rebuilding.

## 25.3 Useful Flags

```bash
ninja -j 1                       # serial
ninja -j 16                      # 16 parallel jobs
ninja -k 0                       # keep going even after errors (build everything possible)
ninja -v                         # show full commands
ninja -d explain                 # print why each target is being rebuilt
ninja -d keepdepfile             # keep .d files for inspection
ninja -t clean                   # clean
ninja -t clean -g                # also clean generated headers
```

`ninja -d explain` is the single best debugging tool for unexpected rebuilds.

## 25.4 Configuration via cmake --build

Generator-agnostic build invocations should use `cmake --build`:

```bash
cmake --build build                       # default, all targets
cmake --build build --target foo          # one target
cmake --build build --parallel 8          # explicit parallelism
cmake --build build --config Release      # multi-config only
cmake --build build -- -d explain         # pass-through to underlying generator (Ninja here)
```

The double-dash separates CMake's options from generator-native options.

## 25.5 Ninja vs Make in Practice

For a 1000-file C++ project:

```
Full build:           Ninja 60s vs Make 90s
Incremental no-op:    Ninja 0.2s vs Make 5-15s
Incremental 1 file:   Ninja 2s vs Make 8s
Parallelism:          Ninja saturates CPUs; Make often has stragglers
```

The no-op case is the killer: Make re-stats every file every time; Ninja keeps a deps database and does it in one pass.

---

# 26. Compiler Caches: ccache and sccache

---

## 26.1 What a Compiler Cache Does

A compiler cache wraps the compiler invocation:

```
Without cache: g++ -c -O2 foo.cpp -o foo.o          (10 seconds)

With cache, first run: 
  ccache g++ -c -O2 foo.cpp -o foo.o                 (10 + 0.1 seconds, cache populated)

With cache, second run (no source changes):
  ccache g++ -c -O2 foo.cpp -o foo.o                 (0.1 seconds, cache hit)
```

The cache key is roughly hash(source + headers + flags + compiler version). When the inputs are identical, the cached `.o` is reused.

## 26.2 The Two Main Caches

| Tool | Origin | Notes |
|---|---|---|
| `ccache` | C/C++ classic | Mature, ubiquitous, supports many compilers |
| `sccache` | Mozilla (Rust-rewritten ccache) | Supports remote caches (S3, Redis, GCS), distributed teams |

`ccache` is local-only by default; `sccache` is designed for shared/cloud caches and is the default in many CI rigs.

## 26.3 Plugging a Cache Into CMake

The clean way is **launchers**:

```cmake
find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
    set(CMAKE_C_COMPILER_LAUNCHER   "${CCACHE_PROGRAM}")
    set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
endif()
```

This prefixes every compile with `ccache`. The launcher mechanism is preferred over `CMAKE_CXX_COMPILER=ccache;g++` because it works correctly across generators.

For per-target launchers (rare):

```cmake
set_target_properties(foo PROPERTIES CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
```

## 26.4 CMake Variables and Cache Hits

To maximise cache hits, the **compiler invocation** must be byte-stable across machines and runs. Common cache-busters:

| Cause | Fix |
|---|---|
| `__DATE__` / `__TIME__` in code | `-Wno-builtin-macro-redefined -D__DATE__= -D__TIME__=` or remove |
| Absolute paths in include flags | `-fdebug-prefix-map=/abs/build/path=.` (GCC/Clang) |
| Different temp filenames | Set `CCACHE_NOHASHDIR=1` |
| ccache reads `__FILE__` | `CCACHE_BASEDIR=/path/to/source` makes paths relative |

Modern ccache (4.x+) handles most of these automatically with `hash_dir=false` and `base_dir`.

## 26.5 sccache Cache Backends

```bash
# Local disk (default)
sccache --stats

# S3
SCCACHE_BUCKET=my-build-cache \
SCCACHE_S3_USE_SSL=true \
sccache cmake --build build

# Redis
SCCACHE_REDIS=redis://cache.local:6379 sccache ...

# GCS
SCCACHE_GCS_BUCKET=my-cache SCCACHE_GCS_RW_MODE=READ_WRITE sccache ...
```

Distributed caches are transformative for big teams: a colleague's CI run populates the cache, and your local build is instant.

## 26.6 Reading ccache Statistics

```bash
$ ccache -s
cache directory                     /home/me/.ccache
cache hit (direct)                  31204
cache hit (preprocessed)               203
cache miss                            8421
called for link                       2104
called for preprocessing              1287
cache size                           14.2 GB
max cache size                       20.0 GB
```

Hit rates above 80% on incremental builds are typical for a well-configured project. Sub-50% suggests a cache-buster (absolute paths, embedded timestamps, or mismatched flags between users).

---

# 27. Distributed Builds

---

## 27.1 Why Distribute

Even with Ninja and ccache, a from-scratch build of a large project (Chromium, LLVM, big game engines) takes 30-60 minutes on a single workstation. Distributed builds dispatch compile jobs across a build farm or peer machines.

| Tool | Mechanism | Best for |
|---|---|---|
| `distcc` | Plain TCP, plain compiler invocation | Small homogeneous LAN clusters |
| **IceCC** (Icecream) | Scheduler + nodes, sandboxed via `chroot` | Larger LANs, mixed configs |
| `sccache` (dist mode) | Remote build server (gRPC) | Cloud-distributed teams |
| FastBuild | Built-in BFF compiler, own scheduler | Windows game studios |
| Bazel remote | Bazel-only, remote execution API | Bazel monorepos |
| Buildbarn / Buildbuddy / Bazel REv2 | Standardised remote execution | Multi-tool, large orgs |

## 27.2 distcc

Conceptually the simplest: replace the compiler invocation with `distcc <compiler>`.

```bash
# /etc/distcc/hosts on each machine:
localhost
build1.local
build2.local
build3.local
```

CMake-side: `CMAKE_CXX_COMPILER_LAUNCHER=distcc`. distcc ships preprocessed source to peers; peers compile and ship `.o` back.

## 27.3 IceCream (IceCC)

A modern successor to distcc. Central scheduler hands out jobs; nodes register and report capabilities. The compiler binary itself is shipped to nodes via a tarball ("env"), so nodes can compile for **any** compiler version without preinstalling.

```bash
# Wire CMake to IceCC
set(CMAKE_CXX_COMPILER_LAUNCHER icecc)
```

## 27.4 sccache Dist Mode

```bash
# Build server side
sccache-dist server --conf server.conf

# Client side
SCCACHE_DIST_URL=https://build.internal:10500 sccache cmake --build build
```

sccache distinguishes itself by combining caching and distribution: a cached hit is served from the cache; a miss is dispatched to a remote builder, and the result is cached for next time.

## 27.5 Practical Notes

- Distributed builds only help **compile-bound** work. Linking is still local and serial.
- Different versions of headers, compilers, or sysroots between scheduler and node will cause subtle differences in `.o` files (and cache misses).
- Most distributed systems require an **identical** compiler version across all nodes -- managed via Docker images or IceCC's env-shipping mechanism.
- Combine ccache **and** a distributed builder: ccache locally, distributed cache as fallback.

---

# Part 8: Dependency Management

---

# 28. find_package: Module Mode vs Config Mode

---

## 28.1 The One Command, Two Modes Reality

`find_package(Foo)` is the canonical way to consume a dependency. Under the hood, it operates in one of two modes:

| Mode | What it looks for | Who provides it |
|---|---|---|
| **Module mode** | `FindFoo.cmake` on `CMAKE_MODULE_PATH` or in CMake's own `Modules/` directory | The consumer (you) or CMake's standard distribution |
| **Config mode** | `FooConfig.cmake` or `foo-config.cmake` installed alongside Foo | The dependency itself (when installed via its own `cmake --install`) |

```cmake
# 1. Tries module mode first (FindFoo.cmake), then config mode (FooConfig.cmake)
find_package(Foo REQUIRED)

# 2. Forces config mode -- error if FooConfig.cmake is missing
find_package(Foo REQUIRED CONFIG)

# 3. Forces module mode
find_package(Foo REQUIRED MODULE)
```

## 28.2 Why Two Modes Exist (Historical)

When CMake was new, no library shipped its own CMake support. CMake's authors wrote `Find<X>.cmake` modules for popular libraries (Boost, OpenSSL, ZLIB, Threads, ...) as part of CMake itself. This is **module mode** -- the consumer's CMake distribution knows how to find the dependency by running ad-hoc detection scripts.

As libraries grew CMake-aware, they began shipping their own `FooConfig.cmake` describing themselves with imported targets. This is **config mode** -- the canonical modern approach.

| Aspect | Module mode | Config mode |
|---|---|---|
| Who maintains the detection | CMake project / you | The library itself |
| Imported targets exposed? | Sometimes (newer modules) | Always |
| Version handling | Often imprecise | Built-in via `FooConfigVersion.cmake` |
| Component support | Some modules | Always |
| Transitive deps | Often missing | Always (config files call `find_dependency`) |
| When to prefer | Legacy libs without CMake support | Anything with a `cmake/` install dir |

## 28.3 What find_package Does Internally

```
find_package(OpenSSL 3.0 REQUIRED COMPONENTS SSL Crypto CONFIG)

         |
         v
    +-------------+
    | Search for  |     CMAKE_PREFIX_PATH, vcpkg toolchain prefix, /usr, /usr/local,
    | OpenSSLConfig.cmake|  /opt, env(<Pkg>_ROOT), CMAKE_FRAMEWORK_PATH, ...
    +------+------+
           |
           v found at <prefix>/lib/cmake/OpenSSL/OpenSSLConfig.cmake
           v
    +------+------+
    | Include the |     Brings in OpenSSL::SSL, OpenSSL::Crypto as imported targets
    | config file |
    +------+------+
           |
           v
    +------+------+
    | Verify      |     OpenSSLConfigVersion.cmake checks 3.0 compatibility
    | version &   |     Components check internal state
    | components  |
    +-------------+
```

## 28.4 The Search Path Variables

In order of consultation:

| Variable | Notes |
|---|---|
| `<Pkg>_ROOT` (3.12+; case-sensitive 3.27+ via CMP0144) | Per-package override |
| `CMAKE_PREFIX_PATH` | The main list of prefixes to search |
| `<Pkg>_DIR` | Direct path to the directory containing `FooConfig.cmake` |
| `CMAKE_FRAMEWORK_PATH` | macOS frameworks |
| `CMAKE_APPBUNDLE_PATH` | macOS .app bundles |
| `PATH`-derived | `lib/cmake/<Pkg>` on the path |
| System | `/usr`, `/usr/local`, `/opt/<pkg>/...` |

```bash
cmake -S . -B build \
      -DCMAKE_PREFIX_PATH="/opt/openssl;/opt/zlib" \
      -DBoost_ROOT=/opt/boost
```

## 28.5 Components and Versions

```cmake
find_package(Qt6 6.5 REQUIRED COMPONENTS Core Widgets Network)
find_package(Boost 1.74 REQUIRED COMPONENTS system filesystem)
```

Each library decides what its components mean. Qt's components map to Qt sub-modules; Boost's components map to compiled Boost libraries. The version is interpreted by the library's `<Pkg>ConfigVersion.cmake` file (compat policies vary: `AnyNewerVersion`, `SameMajorVersion`, `SameMinorVersion`, `ExactVersion`).

## 28.6 REQUIRED vs QUIET vs Optional

```cmake
find_package(Foo)                # search, set Foo_FOUND, no failure
find_package(Foo REQUIRED)       # FATAL_ERROR if not found
find_package(Foo QUIET)          # search silently, no status messages
find_package(Foo QUIET OPTIONAL_COMPONENTS Bar Baz)  # try to find some components
```

After the call:

```cmake
if(Foo_FOUND)
    target_link_libraries(my_app PRIVATE Foo::Foo)
endif()
```

`Foo_FOUND` is always set; `Foo_VERSION`, `Foo_<COMPONENT>_FOUND` may be set depending on the module.

## 28.7 Pitfall: Plain Bare Libraries Found

Old Find modules set variables (`OPENSSL_LIBRARIES`, `OPENSSL_INCLUDE_DIRS`) instead of imported targets. Linking against those variables loses propagation:

```cmake
# OLD STYLE -- avoid in new code:
find_package(OpenSSL REQUIRED)
target_include_directories(my_app PRIVATE ${OPENSSL_INCLUDE_DIRS})
target_link_libraries(my_app PRIVATE ${OPENSSL_LIBRARIES})

# MODERN -- prefer (all of CMake's bundled Find modules now provide imported targets):
find_package(OpenSSL REQUIRED)
target_link_libraries(my_app PRIVATE OpenSSL::SSL OpenSSL::Crypto)
```

---

# 29. Writing FindXxx Modules

---

## 29.1 When to Write One

You need a `FindMyLib.cmake` when:

- The library does **not** ship its own `MyLibConfig.cmake`.
- It is not already in CMake's bundled Find modules (`cmake --find-modules-help`).
- You can't fix the upstream library to ship config files.

If you can fix upstream, do that instead -- a config file is always preferable.

## 29.2 Minimal FindMyLib.cmake

```cmake
# FindMyLib.cmake -- locate MyLib

find_path(MYLIB_INCLUDE_DIR
    NAMES mylib/mylib.h
    HINTS ENV MYLIB_ROOT
    PATH_SUFFIXES include)

find_library(MYLIB_LIBRARY
    NAMES mylib libmylib
    HINTS ENV MYLIB_ROOT
    PATH_SUFFIXES lib lib64)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(MyLib
    REQUIRED_VARS MYLIB_LIBRARY MYLIB_INCLUDE_DIR)

if(MyLib_FOUND AND NOT TARGET MyLib::MyLib)
    add_library(MyLib::MyLib UNKNOWN IMPORTED)
    set_target_properties(MyLib::MyLib PROPERTIES
        IMPORTED_LOCATION             "${MYLIB_LIBRARY}"
        INTERFACE_INCLUDE_DIRECTORIES "${MYLIB_INCLUDE_DIR}")
endif()

mark_as_advanced(MYLIB_INCLUDE_DIR MYLIB_LIBRARY)
```

`FindPackageHandleStandardArgs` is a CMake-provided helper that uniformly handles `REQUIRED`, `QUIET`, `VERSION`, and sets `MyLib_FOUND`. Every Find module should use it.

## 29.3 Discovery: Use HINTS, Not PATHS

```cmake
find_path(MYLIB_INCLUDE_DIR mylib.h
    HINTS ${MYLIB_ROOT}/include             # checked BEFORE system paths
    PATHS /opt/local/include /usr/local/include /usr/include  # AFTER system
    NO_DEFAULT_PATH                          # skip the default search list (rare)
)
```

| Keyword | Search order |
|---|---|
| `HINTS` | Tried **before** standard system paths |
| `PATHS` | Tried **after** standard system paths |
| `NO_DEFAULT_PATH` | Skip system paths entirely |

## 29.4 Version Detection

```cmake
if(MYLIB_INCLUDE_DIR AND EXISTS "${MYLIB_INCLUDE_DIR}/mylib/version.h")
    file(STRINGS "${MYLIB_INCLUDE_DIR}/mylib/version.h" _ver REGEX
        "#define MYLIB_VERSION_STRING \"[^\"]+\"")
    string(REGEX REPLACE
        "#define MYLIB_VERSION_STRING \"([^\"]+)\".*" "\\1"
        MyLib_VERSION "${_ver}")
endif()

find_package_handle_standard_args(MyLib
    REQUIRED_VARS MYLIB_LIBRARY MYLIB_INCLUDE_DIR
    VERSION_VAR   MyLib_VERSION)
```

`VERSION_VAR` then enables `find_package(MyLib 1.2.3 REQUIRED)`.

## 29.5 pkg-config Fallback

If the library has a `.pc` file, lean on `pkg-config` for the heavy lifting:

```cmake
find_package(PkgConfig)
if(PkgConfig_FOUND)
    pkg_check_modules(PC_MYLIB QUIET mylib)
endif()

find_path(MYLIB_INCLUDE_DIR mylib.h
    HINTS ${PC_MYLIB_INCLUDE_DIRS})
find_library(MYLIB_LIBRARY mylib
    HINTS ${PC_MYLIB_LIBRARY_DIRS})
```

`pkg-config` parses `.pc` files for include flags, libs, and compile/link options; we extract the directories and find the actual files.

---

# 30. Writing XxxConfig Files

---

## 30.1 What You Want to Produce

When your library installs, you want consumers to be able to do:

```cmake
find_package(MyLib 1.0 REQUIRED)
target_link_libraries(consumer PRIVATE MyLib::Core MyLib::Extras)
```

That requires installing two files alongside the library:

- `<prefix>/lib/cmake/MyLib/MyLibConfig.cmake` -- the entry point.
- `<prefix>/lib/cmake/MyLib/MyLibConfigVersion.cmake` -- version compatibility.

Plus a third generated file with the actual targets:

- `<prefix>/lib/cmake/MyLib/MyLibTargets.cmake` -- generated by `install(EXPORT)`.

## 30.2 The Generated Targets File

```cmake
install(TARGETS my_core my_extras
    EXPORT MyLibTargets
    LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT MyLibTargets
    FILE       MyLibTargets.cmake
    NAMESPACE  MyLib::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
```

This produces a `MyLibTargets.cmake` that recreates `MyLib::my_core` and `MyLib::my_extras` as imported targets on the consumer's machine.

## 30.3 The Config File (Template)

`cmake/MyLibConfig.cmake.in`:

```cmake
@PACKAGE_INIT@

include(CMakeFindDependencyMacro)

# Re-find our own dependencies so consumers transitively get them
find_dependency(Threads)
find_dependency(OpenSSL 3.0)

# Pull in the targets file produced by install(EXPORT)
include("${CMAKE_CURRENT_LIST_DIR}/MyLibTargets.cmake")

check_required_components(MyLib)
```

`@PACKAGE_INIT@` is replaced by `configure_package_config_file()` with boilerplate that sets `PACKAGE_PREFIX_DIR` correctly regardless of where the user installs the package.

`find_dependency` is the imports-correct equivalent of `find_package` for use inside Config files -- it forwards `QUIET`/`REQUIRED` and sets up `<Pkg>_FOUND` consistently.

## 30.4 Generating the Real Config File

```cmake
include(CMakePackageConfigHelpers)

configure_package_config_file(
    cmake/MyLibConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    VERSION   ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
```

| Compatibility | Match policy |
|---|---|
| `AnyNewerVersion` | Any newer or equal version is fine (rare) |
| `SameMajorVersion` | Same major; minor/patch may differ (semver) |
| `SameMinorVersion` | Same major.minor (strict semver) |
| `ExactVersion` | Exact match only |

`SameMajorVersion` is the right default for libraries that follow semver.

## 30.5 The Result on the Consumer Side

```bash
# Producer
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/opt/mylib
cmake --build build && cmake --install build

# Consumer
cmake -S . -B build -DCMAKE_PREFIX_PATH=/opt/mylib
```

```cmake
find_package(MyLib 1.0 REQUIRED)
target_link_libraries(my_app PRIVATE MyLib::Core)
```

The full circle: producer exports, installs to a prefix; consumer adds the prefix to `CMAKE_PREFIX_PATH` and uses normal `find_package` + namespaced targets.

---

# 31. FetchContent Deep Dive

---

## 31.1 What FetchContent Solves

`FetchContent` (3.11+, mature since 3.14) downloads and adds source-level dependencies **at configure time**, integrating them via `add_subdirectory`. The result is a self-contained build: no system install, no external package manager.

```cmake
include(FetchContent)

FetchContent_Declare(fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG        10.2.1
    GIT_SHALLOW    TRUE)

FetchContent_MakeAvailable(fmt)

target_link_libraries(my_app PRIVATE fmt::fmt)
```

That's it. On first configure, CMake clones fmt into `build/_deps/fmt-src/`, calls `add_subdirectory` on it, and exposes its targets. On subsequent configures, the clone is cached.

## 31.2 FetchContent vs ExternalProject

| | `FetchContent` | `ExternalProject_Add` |
|---|---|---|
| When dep is built | **Configure time**, in the main build | **Build time**, isolated sub-project |
| Targets available in main project | Yes (real CMake targets) | No (isolated build tree) |
| Can `target_link_libraries(my_app dep::dep)` | Yes | Not directly |
| Cross-config compatibility | Native | Yes |
| Use case | Most modern dependencies | Pre-CMake projects, autotools, etc. |

`FetchContent` is built on top of `ExternalProject`, but it does the download + `add_subdirectory` at configure time, which is what makes `target_link_libraries(my_app fmt::fmt)` "just work".

## 31.3 Declare Sources

```cmake
FetchContent_Declare(fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG        10.2.1)              # tag, branch, or full SHA

FetchContent_Declare(json
    URL      https://github.com/nlohmann/json/archive/v3.11.3.tar.gz
    URL_HASH SHA256=a22461d13119ac5c78f205d3df1db13403e58ce1bb1794edc9313677313f4a9d)

FetchContent_Declare(local_lib
    SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/third_party/local_lib)

FetchContent_Declare(catch
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
    GIT_SHALLOW    TRUE                   # shallow clone -- faster
    SYSTEM)                                # treat headers as -isystem (3.25+)
```

| Source | Notes |
|---|---|
| `GIT_REPOSITORY` + `GIT_TAG` | Most flexible; supports SHA, tag, branch |
| `URL` (+ `URL_HASH`) | Tarball/zip; hash for integrity |
| `SOURCE_DIR` | Already-on-disk path; useful for vendoring during transition |
| `SVN_*`, `HG_*` | Other VCS |

## 31.4 Making the Dependency Available

```cmake
FetchContent_MakeAvailable(fmt json catch)
```

This pulls the source down if needed and calls `add_subdirectory` on each. It's a one-liner that replaced the longer pattern:

```cmake
FetchContent_GetProperties(fmt)
if(NOT fmt_POPULATED)
    FetchContent_Populate(fmt)
    add_subdirectory(${fmt_SOURCE_DIR} ${fmt_BINARY_DIR})
endif()
```

Use the longer form only when you need custom subdir args (`EXCLUDE_FROM_ALL`, `SYSTEM`).

## 31.5 Suppressing the Dependency's Tests and Examples

```cmake
set(FMT_TEST     OFF CACHE BOOL "" FORCE)
set(FMT_DOC      OFF CACHE BOOL "" FORCE)
set(FMT_INSTALL  OFF CACHE BOOL "" FORCE)

FetchContent_Declare(fmt ...)
FetchContent_MakeAvailable(fmt)
```

You must set the dep's cache options **before** `FetchContent_MakeAvailable`. Forcing the value with `FORCE` is correct here because you are intentionally overriding the dep's default.

## 31.6 EXCLUDE_FROM_ALL and SYSTEM

```cmake
FetchContent_Declare(fmt
    GIT_REPOSITORY ...
    GIT_TAG        ...
    OVERRIDE_FIND_PACKAGE             # 3.24+: redirect find_package(fmt) to this
    EXCLUDE_FROM_ALL                  # 3.28+: don't build dep's targets unless used
    SYSTEM)                            # 3.25+: treat its includes as system
```

`SYSTEM` is invaluable: it suppresses warnings inside the dependency's headers (no more 50 warnings from inside `fmt/format.h`).

`OVERRIDE_FIND_PACKAGE` lets you write:

```cmake
find_package(fmt REQUIRED)            # if fmt is system-installed, uses it;
                                       # otherwise falls back to FetchContent
```

so the same code works whether the consumer has fmt installed or wants the project to fetch it.

## 31.7 FetchContent and CMake Cache

The downloaded sources live in `build/_deps/<name>-src/`. The download stamp is in `build/_deps/<name>-subbuild/`. `--fresh` re-downloads. To force a re-fetch without nuking the whole build:

```bash
rm -rf build/_deps && cmake -S . -B build
```

## 31.8 Pitfalls

- **Don't pin to a branch (`GIT_TAG main`).** Builds become non-reproducible. Always pin to a tag or SHA.
- **Use `GIT_SHALLOW TRUE`** to avoid downloading years of history -- but only with a real tag/SHA, not a branch.
- **Beware of conflicting options** between the dep's CMakeLists and yours. The dep might `add_subdirectory` your sources or vice versa with conflicting policies.
- **`FetchContent_MakeAvailable` calls `enable_testing()`** indirectly through some deps. Gate testing with `BUILD_TESTING AND PROJECT_IS_TOP_LEVEL` to keep their tests out of yours.

---

# 32. ExternalProject_Add

---

## 32.1 The "Build-Time" Sibling of FetchContent

`ExternalProject_Add` is the original mechanism (CMake 2.8+) for integrating non-CMake projects. Unlike `FetchContent`, the dependency is built as part of `cmake --build`, not added to the main CMake project tree.

```cmake
include(ExternalProject)

ExternalProject_Add(myextlib
    URL https://example.com/myextlib-1.0.tar.gz
    URL_HASH SHA256=...
    CONFIGURE_COMMAND <SOURCE_DIR>/configure --prefix=<INSTALL_DIR>
    BUILD_COMMAND     make -j8
    INSTALL_COMMAND   make install
    BUILD_BYPRODUCTS  <INSTALL_DIR>/lib/libmyextlib.a)
```

The build-time isolation is the point: the dep can be built with autotools, Meson, Make, custom scripts -- anything that produces files.

## 32.2 When to Prefer ExternalProject

| Situation | Choice |
|---|---|
| Pure CMake dependency | `FetchContent` (cleaner integration) |
| Autotools / Meson / SCons / GNU Make project | `ExternalProject_Add` |
| Need different compiler/toolchain for dep | `ExternalProject_Add` (sub-build is isolated) |
| Dep cross-builds for different target | `ExternalProject_Add` |
| Don't want dep's targets to clutter your build | `ExternalProject_Add` |

## 32.3 Connecting ExternalProject Outputs to Your Targets

Because the ExternalProject's targets don't exist in your CMake project, you need to **manually wrap** them:

```cmake
ExternalProject_Add(zlib_ext
    URL https://zlib.net/zlib-1.3.1.tar.gz
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
    BUILD_BYPRODUCTS <INSTALL_DIR>/lib/libz.a)

ExternalProject_Get_Property(zlib_ext INSTALL_DIR)
file(MAKE_DIRECTORY ${INSTALL_DIR}/include)   # avoid "include dir doesn't exist" error

add_library(zlib::zlib STATIC IMPORTED)
set_target_properties(zlib::zlib PROPERTIES
    IMPORTED_LOCATION             ${INSTALL_DIR}/lib/libz.a
    INTERFACE_INCLUDE_DIRECTORIES ${INSTALL_DIR}/include)
add_dependencies(zlib::zlib zlib_ext)         # so our build waits for ext build

target_link_libraries(my_app PRIVATE zlib::zlib)
```

`BUILD_BYPRODUCTS` tells Ninja what files the external project produces; without it, Ninja can't track the dependency correctly and will complain about missing inputs.

## 32.4 Useful ExternalProject Steps

`ExternalProject_Add` decomposes the build into named steps you can hook:

```
download -> update -> patch -> configure -> build -> install -> test
```

```cmake
ExternalProject_Add(thing
    ...
    PATCH_COMMAND  patch -p1 < ${CMAKE_CURRENT_SOURCE_DIR}/thing-fix.patch
    TEST_COMMAND   make check
    LOG_DOWNLOAD   1
    LOG_BUILD      1
    LOG_INSTALL    1)
```

`LOG_*` flags redirect that step's stdout to a log file (`<build>/thing-prefix/src/thing-stamp/thing-build.log`), useful when verbose output is overwhelming.

## 32.5 FetchContent + ExternalProject Hybrid

```cmake
FetchContent_Declare(autotools_lib
    URL https://example.com/foo.tar.gz)
FetchContent_GetProperties(autotools_lib)
if(NOT autotools_lib_POPULATED)
    FetchContent_Populate(autotools_lib)
    # Now we have the source but won't add_subdirectory it (it's not CMake)
    ExternalProject_Add(autotools_lib_build
        SOURCE_DIR ${autotools_lib_SOURCE_DIR}
        CONFIGURE_COMMAND <SOURCE_DIR>/configure --prefix=<INSTALL_DIR>
        BUILD_COMMAND     make
        INSTALL_COMMAND   make install)
endif()
```

This pattern -- FetchContent for download, ExternalProject for build -- handles autotools deps cleanly inside a modern CMake workflow.

---

# 33. vcpkg Integration

---

## 33.1 What vcpkg Is

vcpkg is Microsoft's open-source C/C++ package manager. It provides a curated repository of build recipes ("ports") for thousands of libraries, all building from source against your toolchain. The output is installed to a vcpkg-managed directory that you point CMake to.

## 33.2 Two Modes: Classic vs Manifest

| Mode | Definition | Workflow |
|---|---|---|
| **Classic** | Global install: `vcpkg install fmt zlib openssl` | One vcpkg root, shared across projects |
| **Manifest** | Per-project `vcpkg.json` lists dependencies | Reproducible per-project; recommended |

## 33.3 Manifest Mode Walkthrough

`vcpkg.json` in your project root:

```json
{
    "name": "my-project",
    "version": "1.0.0",
    "dependencies": [
        "fmt",
        "nlohmann-json",
        {
            "name": "boost",
            "features": ["system", "filesystem"]
        }
    ],
    "builtin-baseline": "2024-01-08"
}
```

Then configure with the vcpkg toolchain:

```bash
cmake -S . -B build \
      -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

The vcpkg toolchain wraps your real toolchain (or supplies one if absent), installs the manifest's deps to `build/vcpkg_installed/`, and prepends that prefix to `CMAKE_PREFIX_PATH`. Your `find_package(fmt)` then "just works".

## 33.4 In CMakeLists.txt -- No vcpkg-Specific Code

```cmake
find_package(fmt CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

target_link_libraries(my_app PRIVATE fmt::fmt nlohmann_json::nlohmann_json)
```

vcpkg's value proposition is that no `CMakeLists.txt` code is vcpkg-specific. Your project speaks plain `find_package`; vcpkg arranges for those packages to be present.

## 33.5 Triplets

vcpkg uses **triplets** to describe target platform + ABI:

| Triplet | Meaning |
|---|---|
| `x64-linux` | 64-bit Linux, default GCC |
| `x64-windows` | Dynamic CRT, Visual Studio |
| `x64-windows-static` | Static CRT, statically linked deps |
| `arm64-osx` | Apple Silicon |
| `wasm32-emscripten` | WebAssembly |

```bash
cmake -S . -B build \
      -DCMAKE_TOOLCHAIN_FILE=... \
      -DVCPKG_TARGET_TRIPLET=x64-windows-static
```

Triplet choice affects which CRT, whether deps are static or shared, and which compiler/sysroot is used.

## 33.6 Baseline and Reproducibility

`builtin-baseline` in `vcpkg.json` pins to a specific commit of the vcpkg repository, so the same `vcpkg.json` produces the same dep versions across machines and over time. Without a baseline, your team gets non-deterministic versions.

```bash
cd $VCPKG_ROOT && git rev-parse HEAD     # what to put in builtin-baseline
```

## 33.7 Custom Ports

A "port" is the build recipe for a single library. You can write your own for in-house libraries and point vcpkg at them via `vcpkg-configuration.json`:

```json
{
    "default-registry": {
        "kind": "git",
        "repository": "https://github.com/microsoft/vcpkg",
        "baseline": "abc123..."
    },
    "registries": [
        {
            "kind": "git",
            "repository": "https://internal/our-vcpkg-ports",
            "baseline": "def456...",
            "packages": ["mycorp-internal-lib"]
        }
    ]
}
```

This is how enterprises layer internal libraries on top of vcpkg without forking.

---

# 34. Conan Integration

---

## 34.1 Conan vs vcpkg

| | vcpkg | Conan |
|---|---|---|
| Style | Built from source, install-and-link | Binaries + recipes, more configurable |
| Per-project file | `vcpkg.json` | `conanfile.txt` / `conanfile.py` |
| Build profile | Implicit via triplet | Explicit profile file (`debug`, `release`, ABI) |
| Custom recipes | Ports | Conan recipes (Python) |
| Native CMake integration | Toolchain file | Generators (`CMakeDeps`, `CMakeToolchain`) |
| Binary cache | None public | Public (ConanCenter) + private remotes |

Both ship 1000+ libraries; both are widely used. Pick by team preference; their CMake-side integration is similarly clean once set up.

## 34.2 Conan 2 Workflow

`conanfile.txt`:

```ini
[requires]
fmt/10.2.1
nlohmann_json/3.11.3
boost/1.84.0

[generators]
CMakeDeps
CMakeToolchain

[options]
boost/*:shared=False
```

Build profile (`~/.conan2/profiles/default`):

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.cppstd=20
compiler.libcxx=libstdc++11
build_type=Release
```

Install dependencies:

```bash
conan install . --output-folder=build --build=missing
```

This downloads (or builds) deps into a Conan cache and writes `conan_toolchain.cmake` and per-package `*-config.cmake` files into `build/`.

## 34.3 Configure With CMake

```bash
cmake -S . -B build \
      -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake \
      -DCMAKE_BUILD_TYPE=Release

cmake --build build
```

The Conan toolchain sets up the compiler, build type, CRT, and `CMAKE_PREFIX_PATH` so that subsequent `find_package` calls find the Conan-installed deps.

## 34.4 In CMakeLists.txt -- Again, No Conan-Specific Code

```cmake
find_package(fmt REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(Boost REQUIRED COMPONENTS system filesystem)

target_link_libraries(my_app PRIVATE
    fmt::fmt
    nlohmann_json::nlohmann_json
    Boost::system Boost::filesystem)
```

## 34.5 conanfile.py for Complex Cases

When you need conditional dependencies, build options, or to publish your own library, switch to a Python recipe:

```python
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake

class MyProject(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = ("fmt/10.2.1", "boost/1.84.0")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["MY_PROJECT_WITH_OPENSSL"] = "ON"
        tc.generate()
        CMakeDeps(self).generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
```

## 34.6 Profiles for Cross-Building

```bash
conan install . -pr:h=android-arm64 -pr:b=default --build=missing
```

`-pr:h` is the **host** profile (target); `-pr:b` is the **build** profile (where you're running Conan). This is Conan's clean cross-compile story: deps for the host platform, build deps (CMake, protoc) for the build platform.

---

# 35. CPM.cmake and Hybrid Approaches

---

## 35.1 What CPM.cmake Is

CPM.cmake is a single `.cmake` file wrapper around `FetchContent` that adds:

- Version-as-string syntax (`CPMAddPackage("gh:fmtlib/fmt#10.2.1")`).
- Local caching across projects (one fmt download for your whole machine).
- "find_package or download" semantics (use system if available, else fetch).
- A shorter API for the common case.

```cmake
include(cmake/CPM.cmake)

CPMAddPackage("gh:fmtlib/fmt#10.2.1")
CPMAddPackage("gh:nlohmann/json@3.11.3")
CPMAddPackage(
    NAME       Catch2
    GIT_TAG    v3.5.2
    GITHUB_REPOSITORY catchorg/Catch2
    OPTIONS "CATCH_INSTALL_DOCS OFF")

target_link_libraries(my_app PRIVATE fmt::fmt nlohmann_json::nlohmann_json)
```

CPM is "FetchContent with sugar". You can adopt it or stick with raw FetchContent -- both produce identical builds.

## 35.2 The Hybrid Approach

A common modern pattern for libraries that want to support multiple consumption modes:

```cmake
find_package(fmt 10 QUIET)

if(NOT fmt_FOUND)
    include(FetchContent)
    FetchContent_Declare(fmt
        GIT_REPOSITORY https://github.com/fmtlib/fmt.git
        GIT_TAG        10.2.1
        GIT_SHALLOW    TRUE)
    FetchContent_MakeAvailable(fmt)
endif()

target_link_libraries(my_app PRIVATE fmt::fmt)
```

Or with `OVERRIDE_FIND_PACKAGE` (3.24+):

```cmake
FetchContent_Declare(fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG        10.2.1
    OVERRIDE_FIND_PACKAGE)

find_package(fmt 10 REQUIRED)             # uses system fmt if found, else FetchContent
target_link_libraries(my_app PRIVATE fmt::fmt)
```

This "find_package or FetchContent" pattern is the gold standard: distributors get system libraries; developers and CI get reproducible source builds.

## 35.3 Choosing a Dependency Strategy

| Strategy | Best for |
|---|---|
| **`find_package` only** | Libraries deployed via system packages (Linux distros) |
| **`FetchContent` / `CPM`** | Self-contained projects, CI builds, no dep on system state |
| **vcpkg manifest** | Cross-platform projects wanting binaries + reproducibility |
| **Conan** | Teams needing fine-grained build profiles and ABI control |
| **Hybrid (`find_package` + `FetchContent`)** | Libraries that want "build anywhere" without forcing a package manager |

There is no single right answer. Most modern projects converge on `FetchContent` + `find_package` hybrid for top-of-tree open-source projects, vcpkg or Conan for enterprise / closed-source.

---

# Part 9: Installation and Packaging

---

# 36. The install Command

---

## 36.1 What install Does

`install()` records rules that are executed by `cmake --install <build>` (or `make install`, `ninja install`). These rules copy files from the source tree and build tree into `CMAKE_INSTALL_PREFIX`.

```cmake
install(TARGETS foo
    LIBRARY  DESTINATION lib
    ARCHIVE  DESTINATION lib
    RUNTIME  DESTINATION bin
    INCLUDES DESTINATION include)
```

That single rule handles the four artifact types a library can produce:

| Argument | What it covers | Typical destination |
|---|---|---|
| `LIBRARY` | Shared libraries (`.so`, `.dylib`) | `lib/` |
| `ARCHIVE` | Static libraries (`.a`, `.lib`) and import libraries (`foo.lib` on Windows for DLLs) | `lib/` |
| `RUNTIME` | Executables (`foo`, `foo.exe`) and DLLs (`foo.dll`) | `bin/` |
| `INCLUDES` | Public include directory for use in `INSTALL_INTERFACE` | `include/` |
| `OBJECTS` | Object files (rare) | `lib/objects/` |
| `FRAMEWORK` | macOS frameworks | `Library/Frameworks/` |
| `BUNDLE` | macOS app bundles | `Applications/` |

## 36.2 The Multiple Forms of install()

```cmake
# Install targets (the most common form)
install(TARGETS foo bar ...)

# Install raw files
install(FILES include/foo.h DESTINATION include)
install(FILES doc/man/foo.1 DESTINATION share/man/man1)

# Install a whole directory tree
install(DIRECTORY include/ DESTINATION include
        FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp"
        PATTERN "internal" EXCLUDE)

# Install a generated script with execute permission
install(PROGRAMS scripts/my_tool.sh DESTINATION bin)

# Run CMake code at install time (per-file inspection, fixup_bundle, etc.)
install(CODE "message(STATUS \"Installing into ${CMAKE_INSTALL_PREFIX}\")")
install(SCRIPT post_install.cmake)

# Export the imported-target dump
install(EXPORT FooTargets ...)
```

## 36.3 install(TARGETS) Detail

The full signature is dense:

```cmake
install(TARGETS foo bar
    EXPORT       FooTargets                       # add to an export set
    LIBRARY
        DESTINATION ${CMAKE_INSTALL_LIBDIR}
        COMPONENT   Runtime
        NAMELINK_COMPONENT Development            # split .so vs .so.1.0
    ARCHIVE
        DESTINATION ${CMAKE_INSTALL_LIBDIR}
        COMPONENT   Development
    RUNTIME
        DESTINATION ${CMAKE_INSTALL_BINDIR}
        COMPONENT   Runtime
    INCLUDES
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILE_SET HEADERS
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
```

**Component groups** (`COMPONENT Runtime`, `COMPONENT Development`) let downstream tools (CPack, Linux package builders) split artifacts into separate packages: a runtime package (just the `.so`), a development package (the `.a`, headers, symlinks).

## 36.4 install(DIRECTORY)

```cmake
install(DIRECTORY include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING
        PATTERN "*.h"
        PATTERN "*.hpp"
        PATTERN "*.inl"
    PATTERN "internal" EXCLUDE
    PATTERN ".git*"    EXCLUDE)
```

The trailing slash on `include/` matters: with slash, the **contents** of `include/` are installed at the destination; without slash, the directory itself is installed (creating `${prefix}/include/include/`).

| Option | Meaning |
|---|---|
| `FILES_MATCHING PATTERN ...` | Whitelist mode -- only matched files installed |
| `PATTERN ... EXCLUDE` | Blacklist mode -- exclude matched paths |
| `REGEX ...` / `EXCLUDE` | Same but with regular expressions |
| `USE_SOURCE_PERMISSIONS` | Copy file permissions from source |

## 36.5 install(EXPORT) and the Targets File

The `EXPORT FooTargets` argument to `install(TARGETS)` adds those targets to a named export set. The actual file is emitted by `install(EXPORT)`:

```cmake
install(EXPORT FooTargets
    FILE       FooTargets.cmake
    NAMESPACE  Foo::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/Foo)
```

The file `FooTargets.cmake` at install time recreates `Foo::foo`, `Foo::bar` as `IMPORTED` targets with the right install-side include paths and library locations.

## 36.6 CMAKE_INSTALL_PREFIX and DESTDIR

```bash
# Set at configure
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/opt/myproject

# Build
cmake --build build

# Install
cmake --install build                              # to /opt/myproject
cmake --install build --prefix /tmp/staging        # override at install time
DESTDIR=/tmp/staging cmake --install build         # POSIX DESTDIR-style staging
```

`CMAKE_INSTALL_PREFIX` is baked into config files at configure/build time. `DESTDIR` is honoured at install time only, prepending a path to every destination -- the canonical way to build a Linux distribution package.

## 36.7 The install RUNTIME_DEPENDENCIES Helper (3.21+)

```cmake
install(TARGETS my_app
    RUNTIME_DEPENDENCIES
        PRE_EXCLUDE_REGEXES "api-ms-" "ext-ms-" "^/lib" "^/usr/lib"
        POST_EXCLUDE_REGEXES ".*system32/.*\\.dll"
        DIRECTORIES $<TARGET_FILE_DIR:my_app>)
```

This bundles the app's dynamic-library dependencies into the install tree, so the result is a self-contained directory of executables + their needed DLLs/`.so` files. On Linux it analyses `RPATH`; on macOS it uses `otool`; on Windows it walks DLL imports.

---

# 37. GNUInstallDirs and FHS Layout

---

## 37.1 What FHS Is

The Filesystem Hierarchy Standard codifies the conventional Unix layout:

```
/usr/local/
|-- bin/                          # executables
|-- sbin/                         # system binaries
|-- lib/                          # libraries (lib64/ on biarch)
|-- libexec/                      # internal helpers, not in PATH
|-- include/                      # headers
|-- share/                        # data, docs, locale
|   |-- doc/<project>/
|   |-- locale/<lang>/LC_MESSAGES/
|   `-- man/man1/
`-- etc/                          # configuration
```

Linux distributions follow this layout. Packages that hard-code `lib/` instead of `lib64/`, or `bin/` instead of `libexec/`, fail to integrate cleanly.

## 37.2 The GNUInstallDirs Module

CMake's `GNUInstallDirs` module exposes platform-correct variables:

```cmake
include(GNUInstallDirs)

install(TARGETS my_lib
    LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(FILES doc/my_lib.1 DESTINATION ${CMAKE_INSTALL_MANDIR}/man1)
install(FILES my_lib.pc    DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig)
```

| Variable | Default | Notes |
|---|---|---|
| `CMAKE_INSTALL_BINDIR` | `bin` | Executables |
| `CMAKE_INSTALL_SBINDIR` | `sbin` | System binaries |
| `CMAKE_INSTALL_LIBEXECDIR` | `libexec` | Internal binaries (debian: `lib/<project>`) |
| `CMAKE_INSTALL_LIBDIR` | `lib` (or `lib64` on 64-bit Linux) | Libraries |
| `CMAKE_INSTALL_INCLUDEDIR` | `include` | Headers |
| `CMAKE_INSTALL_SYSCONFDIR` | `etc` | Config |
| `CMAKE_INSTALL_DATAROOTDIR` | `share` | Data root |
| `CMAKE_INSTALL_DATADIR` | `share` | App-specific data |
| `CMAKE_INSTALL_DOCDIR` | `share/doc/<project>` | Docs |
| `CMAKE_INSTALL_MANDIR` | `share/man` | Man pages |
| `CMAKE_INSTALL_INFODIR` | `share/info` | GNU info pages |
| `CMAKE_INSTALL_LOCALEDIR` | `share/locale` | Translations |

The defaults are overridable on the command line (`-DCMAKE_INSTALL_LIBDIR=lib64`), which is how distros customise.

## 37.3 Pitfall: Hard-Coding lib

```cmake
install(TARGETS foo DESTINATION lib)              # wrong on Fedora x86_64 (lib64)
install(TARGETS foo DESTINATION ${CMAKE_INSTALL_LIBDIR})   # portable
```

If you ever ship to Linux distributions, always go through `GNUInstallDirs`.

## 37.4 Project-Specific Layouts

```cmake
include(GNUInstallDirs)

set(MY_PROJECT_INSTALL_CMAKEDIR ${CMAKE_INSTALL_LIBDIR}/cmake/MyProject)
set(MY_PROJECT_INSTALL_INCLUDEDIR ${CMAKE_INSTALL_INCLUDEDIR}/my_project)
```

It is conventional to nest your project's headers in a subdirectory (`include/my_project/foo.h`) so they don't pollute the global include namespace.

---

# 38. Exporting Targets and Generating Config Files

---

## 38.1 The Full Export Recipe

```cmake
cmake_minimum_required(VERSION 3.21)
project(MyLib VERSION 1.0.0 LANGUAGES CXX)

include(GNUInstallDirs)

add_library(my_lib src/my_lib.cpp)
target_include_directories(my_lib
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
target_compile_features(my_lib PUBLIC cxx_std_17)
add_library(MyLib::my_lib ALIAS my_lib)

install(TARGETS my_lib
    EXPORT  MyLibTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT MyLibTargets
    FILE       MyLibTargets.cmake
    NAMESPACE  MyLib::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)

include(CMakePackageConfigHelpers)
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/MyLibConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    VERSION       ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
```

## 38.2 The Resulting Install Tree

```
/opt/mylib/
|-- include/
|   `-- my_lib/
|       `-- my_lib.h
|-- lib/
|   |-- libmy_lib.so.1.0.0
|   |-- libmy_lib.so.1
|   |-- libmy_lib.so
|   `-- cmake/
|       `-- MyLib/
|           |-- MyLibConfig.cmake             <- the entry point
|           |-- MyLibConfigVersion.cmake      <- version compatibility
|           `-- MyLibTargets.cmake            <- the target definitions
```

A consumer then does:

```cmake
cmake -DCMAKE_PREFIX_PATH=/opt/mylib -S . -B build
```

```cmake
find_package(MyLib 1.0 REQUIRED)
target_link_libraries(consumer PRIVATE MyLib::my_lib)
```

## 38.3 Export for Build Tree (No Install)

For developer-oriented "find me from the build directory" use cases:

```cmake
export(EXPORT MyLibTargets
    FILE      ${CMAKE_CURRENT_BINARY_DIR}/MyLibTargets.cmake
    NAMESPACE MyLib::)
```

This writes the targets file directly into the build dir, useful for super-builds that consume your project before install. The CMake user registry (`~/.cmake/packages/`) plus `export(PACKAGE)` can let `find_package` find a build tree without explicitly adding it to `CMAKE_PREFIX_PATH` -- though the registry is disabled by default in modern CMake for hygiene reasons.

## 38.4 configure_package_config_file Internals

`configure_package_config_file` differs from `configure_file` in that it:

1. Replaces `@PACKAGE_INIT@` with boilerplate that computes `PACKAGE_PREFIX_DIR` based on the location of the actual installed config file (not the configure-time prefix).
2. Uses `set_and_check()` for path variables, which gives clearer errors if the install was moved.
3. Adds `check_required_components()` support.

```cmake
# MyLibConfig.cmake.in
@PACKAGE_INIT@

include(CMakeFindDependencyMacro)
find_dependency(Threads)
find_dependency(OpenSSL 3.0)

set_and_check(MyLib_INCLUDE_DIR "@PACKAGE_CMAKE_INSTALL_INCLUDEDIR@")
include("${CMAKE_CURRENT_LIST_DIR}/MyLibTargets.cmake")
check_required_components(MyLib)
```

`@PACKAGE_<var>@` is the trick for path variables. Inside `configure_package_config_file`, `@PACKAGE_CMAKE_INSTALL_INCLUDEDIR@` becomes the path relative to the install location, which is then resolved by the boilerplate at consumption time.

---

# 39. ABI and SOVERSION

---

## 39.1 The Linux Shared-Library Naming Convention

```
libfoo.so.1.2.3   <- the actual file (real name)
libfoo.so.1       <- soname symlink (compat name)
libfoo.so         <- linker name symlink (development)
```

| Name | Used by |
|---|---|
| Real name | Nobody directly; identity for the file system |
| Soname | The dynamic linker at runtime |
| Linker name | The static linker (`-lfoo`) at link time |

A binary linked against `libfoo.so.1` (via `-lfoo` resolving to `libfoo.so` -> `libfoo.so.1` -> `libfoo.so.1.2.3`) continues to work after `libfoo.so.1` is upgraded to point to `libfoo.so.1.2.4` -- because the soname encoded in the binary is "1", and any `libfoo.so.1.*` satisfies it.

## 39.2 CMake Properties

```cmake
set_target_properties(my_lib PROPERTIES
    VERSION   ${PROJECT_VERSION}       # 1.2.3
    SOVERSION ${PROJECT_VERSION_MAJOR})  # 1
```

`VERSION` becomes the real-name suffix; `SOVERSION` becomes the soname. CMake creates the appropriate symlinks at install time.

## 39.3 Semver Mapping

| API change | Bump |
|---|---|
| Bug fix, no ABI change | PATCH (`1.0.0 -> 1.0.1`) |
| Add functionality, no break | MINOR (`1.0.0 -> 1.1.0`) |
| Break ABI | MAJOR + SOVERSION (`1.x.x -> 2.0.0`, `SOVERSION 1 -> 2`) |

When `SOVERSION` changes, every consumer must be relinked. When `VERSION` changes within the same `SOVERSION`, existing consumers continue to work.

## 39.4 Windows Considerations

DLL versioning on Windows is different: there is no soname/symlink scheme. Versions are encoded in the DLL filename or, more often, communicated externally (manifests, side-by-side assemblies, or simple `foo-1.dll` / `foo-2.dll` naming). CMake's `VERSION`/`SOVERSION` are Unix concepts; on Windows they are largely ignored.

```cmake
set_target_properties(my_lib PROPERTIES
    VERSION   ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    WINDOWS_EXPORT_ALL_SYMBOLS YES)
```

`WINDOWS_EXPORT_ALL_SYMBOLS` (3.4+) makes a DLL on Windows behave roughly like a `.so` on Linux by auto-generating the `.def` export list. Cleaner is to use `__declspec(dllexport)`/`__declspec(dllimport)` macros driven by a generated header from `GenerateExportHeader`:

```cmake
include(GenerateExportHeader)
generate_export_header(my_lib EXPORT_FILE_NAME my_lib_export.h)
```

This produces `my_lib_export.h` with a `MY_LIB_EXPORT` macro that expands to `__declspec(dllexport)` when building the library and `__declspec(dllimport)` when consuming it.

---

# 40. CPack: TGZ, DEB, RPM, NSIS, WIX

---

## 40.1 What CPack Does

CPack reuses your `install()` rules to produce platform-native installer/package files: tarballs, DEBs, RPMs, NSIS installers, WIX MSIs, macOS DMGs, and more.

```cmake
include(CPack)
```

This is the minimal incantation. The default produces a TGZ matching your install tree. Variables before `include(CPack)` configure it:

```cmake
set(CPACK_PACKAGE_NAME              "MyProject")
set(CPACK_PACKAGE_VERSION           "${PROJECT_VERSION}")
set(CPACK_PACKAGE_DESCRIPTION       "A short description")
set(CPACK_PACKAGE_VENDOR            "MyCompany")
set(CPACK_RESOURCE_FILE_LICENSE     "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_PACKAGE_INSTALL_DIRECTORY "${CPACK_PACKAGE_NAME}")

set(CPACK_GENERATOR "TGZ;DEB;RPM")        # what to produce
include(CPack)
```

## 40.2 Producing Packages

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
cd build
cpack                          # produces packages per CPACK_GENERATOR
cpack -G DEB                   # override: produce only DEB
cpack -G NSIS;ZIP              # multiple generators
```

## 40.3 The Generator Matrix

| Generator | Platform | Notes |
|---|---|---|
| `TGZ` / `TXZ` / `TBZ2` / `ZIP` | All | Plain archives -- no installer logic |
| `STGZ` | Unix | Self-extracting shell tarball |
| `DEB` | Debian/Ubuntu | `.deb` files; uses `dpkg` |
| `RPM` | Fedora/RHEL/SUSE | `.rpm` files; uses `rpmbuild` |
| `NSIS` / `NSIS64` | Windows | Nullsoft installer (free, scriptable) |
| `WIX` | Windows | MSI installer (requires WiX toolset) |
| `productbuild` | macOS | `.pkg` installer |
| `DragNDrop` | macOS | `.dmg` disk image |
| `Bundle` | macOS | `.app` bundle |
| `IFW` | All | Qt Installer Framework |

## 40.4 DEB Specifics

```cmake
set(CPACK_DEB_COMPONENT_INSTALL ON)
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "you <you@example.com>")
set(CPACK_DEBIAN_PACKAGE_DEPENDS    "libc6 (>= 2.31), libssl3")
set(CPACK_DEBIAN_PACKAGE_SECTION    "libs")
set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "amd64")
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS  ON)    # auto-derive deps from binaries
```

`CPACK_DEBIAN_PACKAGE_SHLIBDEPS` runs `dpkg-shlibdeps` on each binary to compute the real dependency list -- much more reliable than hand-maintaining `PACKAGE_DEPENDS`.

## 40.5 RPM Specifics

```cmake
set(CPACK_RPM_COMPONENT_INSTALL  ON)
set(CPACK_RPM_PACKAGE_LICENSE    "Apache-2.0")
set(CPACK_RPM_PACKAGE_GROUP      "Development/Libraries")
set(CPACK_RPM_PACKAGE_REQUIRES   "openssl-libs >= 3.0")
set(CPACK_RPM_PACKAGE_AUTOREQ    YES)
```

`CPACK_RPM_PACKAGE_AUTOREQ` is the RPM equivalent of `SHLIBDEPS` -- the RPM builder computes shared-library deps automatically.

## 40.6 Component Packaging

```cmake
install(TARGETS my_app
    RUNTIME DESTINATION bin COMPONENT runtime)

install(TARGETS my_lib
    LIBRARY DESTINATION lib COMPONENT runtime
    ARCHIVE DESTINATION lib COMPONENT development
    INCLUDES DESTINATION include)

install(DIRECTORY include/ DESTINATION include COMPONENT development)

set(CPACK_COMPONENTS_ALL runtime development)
set(CPACK_DEB_COMPONENT_INSTALL ON)
set(CPACK_RPM_COMPONENT_INSTALL ON)

set(CPACK_COMPONENT_RUNTIME_DESCRIPTION     "Runtime libraries")
set(CPACK_COMPONENT_DEVELOPMENT_DESCRIPTION "Headers and static libs")
set(CPACK_COMPONENT_DEVELOPMENT_DEPENDS     runtime)
```

CPack then emits separate `.deb`/`.rpm` files per component, with the right inter-package dependencies. This is the modern Linux distro convention: `libfoo` (runtime) and `libfoo-dev` (development).

## 40.7 Windows NSIS

```cmake
set(CPACK_NSIS_DISPLAY_NAME      "My Project ${PROJECT_VERSION}")
set(CPACK_NSIS_HELP_LINK         "https://example.com/help")
set(CPACK_NSIS_URL_INFO_ABOUT    "https://example.com/")
set(CPACK_NSIS_CONTACT           "support@example.com")
set(CPACK_NSIS_MUI_ICON          "${CMAKE_CURRENT_SOURCE_DIR}/installer.ico")
set(CPACK_NSIS_MODIFY_PATH       ON)
set(CPACK_NSIS_ENABLE_UNINSTALL_BEFORE_INSTALL ON)
```

NSIS is free (BSD-ish), scriptable, and produces tidy `*.exe` installers with uninstall support. WiX MSI is more enterprise-friendly but requires the WiX toolset.

---

# 41. Generating pkg-config Files

---

## 41.1 What pkg-config Is

`pkg-config` is the historical predecessor to CMake config files. A library installs a `.pc` file containing the include flags and link flags needed; consumers query it:

```bash
$ pkg-config --cflags --libs openssl
-I/usr/include/openssl -lssl -lcrypto

$ pkg-config --modversion openssl
3.0.13
```

It is still ubiquitous on Linux, used by Make-based, autotools-based, and non-CMake C++ projects. Modern CMake projects should produce both a `.pc` file and a `<Pkg>Config.cmake`.

## 41.2 A pkg-config Template

`mylib.pc.in`:

```
prefix=@CMAKE_INSTALL_PREFIX@
exec_prefix=${prefix}
libdir=${prefix}/@CMAKE_INSTALL_LIBDIR@
includedir=${prefix}/@CMAKE_INSTALL_INCLUDEDIR@

Name: MyLib
Description: A short description
Version: @PROJECT_VERSION@
Requires: openssl >= 3.0
Libs: -L${libdir} -lmy_lib
Cflags: -I${includedir}
```

## 41.3 Generating It

```cmake
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/mylib.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/mylib.pc
    @ONLY)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/mylib.pc
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig)
```

`@ONLY` restricts substitution to `@VAR@` form (not `${VAR}`), which prevents shell-like variables in the template from being substituted accidentally.

## 41.4 Two Wire Formats Side by Side

| Consumer | Lookup |
|---|---|
| CMake project | `find_package(MyLib)` -> `MyLibConfig.cmake` |
| `pkg-config` | `pkg-config --cflags --libs mylib` -> `mylib.pc` |
| Meson | Either: `dependency('mylib')` tries both |
| autotools | `PKG_CHECK_MODULES(MYLIB, [mylib])` -> `mylib.pc` |

Ship both -- the burden is minimal and the audience reach is much larger.

---

# Part 10: Testing with CTest

---

# 42. enable_testing and add_test

---

## 42.1 The Two-Line Setup

```cmake
include(CTest)                     # provides BUILD_TESTING option and CDash hooks
                                    # also calls enable_testing() internally

if(BUILD_TESTING)
    add_executable(my_test tests/my_test.cpp)
    target_link_libraries(my_test PRIVATE my_lib)
    add_test(NAME my_test COMMAND my_test)
endif()
```

| Command | What it does |
|---|---|
| `enable_testing()` | Turn on CTest support in this and all sub-directories |
| `include(CTest)` | Same plus: defines `BUILD_TESTING` option (default ON), sets up CDash dashboard variables |
| `add_test(NAME ... COMMAND ...)` | Register a test with CTest |

`include(CTest)` is the usual entry point. Wrap your test infrastructure in `if(BUILD_TESTING)` so consumers can turn it off via `-DBUILD_TESTING=OFF`.

## 42.2 add_test Signatures

```cmake
# Old form (still works, less flexible)
add_test(simple_test ./my_test)

# Modern form
add_test(NAME my_test
    COMMAND my_test --verbose
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    CONFIGURATIONS Debug Release
    COMMAND_EXPAND_LISTS)
```

The `COMMAND` value can reference a CMake target by name -- CTest resolves it to the actual executable path at test time. This is preferred over hard-coding paths.

```cmake
add_test(NAME smoke_test COMMAND $<TARGET_FILE:my_test> --quick)
```

`$<TARGET_FILE:my_test>` is a generator expression -- always valid, always resolves to the right per-config path.

## 42.3 Running Tests

```bash
ctest --test-dir build                         # run all tests
ctest --test-dir build -V                      # verbose (show output)
ctest --test-dir build --output-on-failure     # output for failed tests only
ctest --test-dir build -j 8                    # parallel
ctest --test-dir build -R 'smoke|fast'         # regex include filter
ctest --test-dir build -E 'slow|brittle'       # regex exclude filter
ctest --test-dir build -L unit                 # label include filter
ctest --test-dir build -LE integration         # label exclude filter
ctest --test-dir build -C Debug                # config (multi-config only)
ctest --test-dir build --rerun-failed          # re-run only last-run failures
ctest --test-dir build --repeat until-fail:10  # repeat each test until failure (flaky-test hunting)
ctest --test-dir build --schedule-random       # random order (catches ordering bugs)
```

`--output-on-failure` is the option you want in CI -- silent on success, verbose on failure, the right balance.

---

# 43. Test Properties

---

## 43.1 The set_tests_properties Command

```cmake
add_test(NAME big_test COMMAND big_test)

set_tests_properties(big_test PROPERTIES
    TIMEOUT                  300
    LABELS                   "slow;integration"
    ENVIRONMENT              "TMPDIR=/tmp/big_test"
    WORKING_DIRECTORY        ${CMAKE_BINARY_DIR}/test_workdir
    PASS_REGULAR_EXPRESSION  "All tests passed"
    FAIL_REGULAR_EXPRESSION  "(ERROR|FATAL)"
    SKIP_REGULAR_EXPRESSION  "SKIPPED"
    WILL_FAIL                FALSE
    DISABLED                 FALSE
    RUN_SERIAL               TRUE
    PROCESSORS               4
    RESOURCE_LOCK            "gpu0"
    DEPENDS                  "setup_test"
    FIXTURES_SETUP           "shared_data"
    FIXTURES_CLEANUP         "shared_data"
    FIXTURES_REQUIRED        "shared_data")
```

## 43.2 Common Properties

| Property | Effect |
|---|---|
| `TIMEOUT` | Kill the test after N seconds and mark failed |
| `LABELS` | Tag tests for `-L` filtering |
| `WORKING_DIRECTORY` | `chdir` before running |
| `ENVIRONMENT` | Set env vars (list of `KEY=VALUE`) |
| `WILL_FAIL` | Inverts pass/fail -- test should exit non-zero |
| `DISABLED` | Skip entirely; still shown in reports |
| `RUN_SERIAL` | Cannot run in parallel with anything else |
| `PROCESSORS` | Count as N CPUs for scheduling (when test is multi-threaded) |
| `RESOURCE_LOCK` | Mutual-exclusion lock with other tests holding the same lock |
| `DEPENDS` | This test runs after named test(s) succeed |

## 43.3 Pass/Fail Regular Expressions

```cmake
set_tests_properties(my_test PROPERTIES
    PASS_REGULAR_EXPRESSION  "PASSED"
    FAIL_REGULAR_EXPRESSION  "FAILED|Error"
    SKIP_REGULAR_EXPRESSION  "skipped due to")
```

| Pattern | Meaning |
|---|---|
| `PASS_REGULAR_EXPRESSION` | Output must match to be considered passing (overrides exit code) |
| `FAIL_REGULAR_EXPRESSION` | Output matching this fails the test |
| `SKIP_REGULAR_EXPRESSION` | Output matching this marks the test SKIPPED |
| `SKIP_RETURN_CODE` | A specific exit code maps to SKIPPED (e.g., `77` is GNU convention) |

Modern frameworks (GoogleTest, Catch2, Boost.Test) report via exit code, so regex matching is largely a legacy mechanism. Still useful for legacy binaries.

## 43.4 Test Fixtures

```cmake
add_test(NAME setup    COMMAND db_setup)
add_test(NAME teardown COMMAND db_teardown)

add_test(NAME db_test_1 COMMAND db_test_1)
add_test(NAME db_test_2 COMMAND db_test_2)

set_tests_properties(setup    PROPERTIES FIXTURES_SETUP    db)
set_tests_properties(teardown PROPERTIES FIXTURES_CLEANUP  db)
set_tests_properties(db_test_1 db_test_2 PROPERTIES
    FIXTURES_REQUIRED db)
```

CTest figures out the dependency order: `setup` runs first, then `db_test_1` and `db_test_2` (potentially in parallel), then `teardown` last. If `setup` fails, the dependent tests are skipped.

## 43.5 Disabling vs Skipping

| State | What it means |
|---|---|
| Test runs and passes | `Passed` |
| Test runs and fails | `Failed` |
| Test would run but you said `DISABLED TRUE` | `Not Run` |
| Test's `SKIP_REGULAR_EXPRESSION` matched output | `Skipped` |
| Test returned `SKIP_RETURN_CODE` | `Skipped` |
| Test's fixture failed | `Not Run` |

Skipped and Not Run are reported separately from failed -- CI dashboards distinguish them.

---

# 44. Parallel Test Execution

---

## 44.1 The Default

`ctest -j N` runs up to N tests concurrently. The default is serial. Most tests should be parallel-safe by design: independent fixtures, no shared state in `/tmp`, no fixed network ports.

## 44.2 Tests That Cannot Parallelise

```cmake
set_tests_properties(uses_gpu0 PROPERTIES
    RESOURCE_LOCK "gpu0")
set_tests_properties(uses_gpu0_again PROPERTIES
    RESOURCE_LOCK "gpu0")

set_tests_properties(uses_port_8080 PROPERTIES
    RESOURCE_LOCK "port_8080")
```

`RESOURCE_LOCK` is a string-keyed mutex. CTest schedules so no two tests holding the same lock run concurrently. A test can hold multiple locks (space-separated).

`RUN_SERIAL TRUE` is stronger: such a test runs **alone**, blocking everyone else for its duration. Use for tests that hammer the whole machine.

## 44.3 Reporting CPU Cost

```cmake
set_tests_properties(multithreaded_stress PROPERTIES
    PROCESSORS 8)
```

CTest's scheduler treats this test as using 8 CPU slots. With `-j 16`, it leaves only 8 slots for other tests, preventing oversubscription.

## 44.4 Hardware Resources (3.16+)

For finer-grained scheduling (multiple GPUs, NICs, etc.):

```cmake
set_tests_properties(gpu_test_1 PROPERTIES
    RESOURCE_GROUPS "gpus:1")
set_tests_properties(big_gpu_test PROPERTIES
    RESOURCE_GROUPS "gpus:2")
```

```bash
ctest -j 8 --resource-spec-file resources.json
```

`resources.json`:

```json
{
    "version": { "major": 1, "minor": 0 },
    "local": [
        {
            "gpus": [
                { "id": "0", "slots": 1 },
                { "id": "1", "slots": 1 },
                { "id": "2", "slots": 1 }
            ]
        }
    ]
}
```

CTest sets environment variables (`CTEST_RESOURCE_GROUP_COUNT`, `CTEST_RESOURCE_GROUP_<n>`) for each test, listing which resource IDs it received. The test reads them and pins itself accordingly (`CUDA_VISIBLE_DEVICES=...`).

## 44.5 Scheduling Order

`ctest --schedule-random` runs in random order each invocation. This catches tests with ordering bugs (test A leaves shared state that test B depends on, but only when A happens to run first). It is excellent hygiene to enable this in CI periodically.

`ctest --rerun-failed` re-runs only tests that failed last time, useful for iterative debugging.

`ctest --repeat until-fail:50` is the flaky-test hunter: each test runs up to 50 times; first failure is reported. The opposite, `--repeat until-pass:5`, gives a test 5 attempts before declaring failure, useful in inherently flaky integration tests.

---

# 45. gtest_discover_tests and catch_discover_tests

---

## 45.1 The Problem

`add_test(NAME my_test COMMAND my_test)` registers one CTest test that runs the entire `my_test` binary. If `my_test` contains 100 GoogleTest cases, CTest sees one test that passes or fails as a unit. CTest can't filter, parallelise, or report at the case level.

## 45.2 GoogleTest Discovery

CMake's `GoogleTest` module provides `gtest_discover_tests`:

```cmake
include(GoogleTest)

add_executable(my_test tests/my_test.cpp)
target_link_libraries(my_test PRIVATE my_lib GTest::gtest_main)

gtest_discover_tests(my_test
    DISCOVERY_TIMEOUT 60
    PROPERTIES LABELS "unit;fast")
```

At post-build time, CMake runs `./my_test --gtest_list_tests`, parses the output, and registers each case as a separate CTest entry (`WidgetTest.AddsTwoNumbers`, `WidgetTest.HandlesNegatives`, ...). CTest can then parallelise across cases and filter precisely.

This is the modern replacement for the older `gtest_add_tests` (which parsed source code at configure time and was prone to errors with macros).

(See [languages/CPP_Testing.md](../languages/CPP_Testing.md) Section 27 for the deeper GoogleTest+CMake integration, and Section 29 for `gtest_discover_tests` vs `gtest_add_tests` details. This Section gives the CMake-side view; the C++ Testing guide gives the GoogleTest-side view.)

## 45.3 Catch2 Discovery

Catch2 (v3+) provides `catch_discover_tests`:

```cmake
find_package(Catch2 3 REQUIRED)
include(Catch)

add_executable(my_test tests/my_test.cpp)
target_link_libraries(my_test PRIVATE my_lib Catch2::Catch2WithMain)

catch_discover_tests(my_test
    REPORTER junit
    OUTPUT_DIR ${CMAKE_BINARY_DIR}/test_results
    OUTPUT_SUFFIX .xml
    PROPERTIES LABELS "unit")
```

Catch2's discovery works the same way: invoke the binary with a list-tests flag, parse, register each case.

## 45.4 Doctest, Boost.Test, etc.

Other frameworks have similar discovery helpers:

| Framework | Helper module |
|---|---|
| GoogleTest | `gtest_discover_tests` from CMake's `GoogleTest` |
| Catch2 v3 | `catch_discover_tests` from Catch2's CMake config |
| doctest | `doctest_discover_tests` shipped with doctest |
| Boost.Test | Ad-hoc -- usually `add_test(NAME ... COMMAND ... --run_test=...)` per case |

## 45.5 Discovery vs add_test Trade-Off

| | Discovery | Manual `add_test` |
|---|---|---|
| Per-case CTest reports | Yes | No |
| Filter individual cases via `ctest -R` | Yes | No (only by binary) |
| Parallelise cases of one binary | Yes | No |
| Build-time overhead | Small (one extra run per binary) | None |
| Reliability with parameterised/typed tests | Excellent (uses runtime listing) | Manual maintenance |

For new code, use discovery unconditionally.

---

# 46. CTest Dashboards and CDash

---

## 46.1 CDash

CDash is a web dashboard hosted at <https://my.cdash.org/> (community) or self-hosted. It aggregates results from many builds (different platforms, compilers, configurations) and presents trends over time.

## 46.2 CTestConfig.cmake

Drop a `CTestConfig.cmake` at the project root:

```cmake
set(CTEST_PROJECT_NAME       "MyProject")
set(CTEST_NIGHTLY_START_TIME "00:00:00 UTC")
set(CTEST_DROP_METHOD     "https")
set(CTEST_DROP_SITE       "my.cdash.org")
set(CTEST_DROP_LOCATION   "/submit.php?project=MyProject")
set(CTEST_DROP_SITE_CDASH TRUE)
```

`include(CTest)` reads this automatically.

## 46.3 Dashboard Submissions

```bash
ctest --test-dir build -D Experimental    # one-off submission to "Experimental" track
ctest --test-dir build -D Nightly         # nightly build track
ctest --test-dir build -D Continuous      # short-cycle CI submission
```

Each command runs configure (Update phase), build (Build phase), test (Test phase), and uploads results. The dashboard shows pass/fail counts, build warnings, and test trends.

## 46.4 Custom Dashboard Scripts

For complex submissions, write a CTest script:

```cmake
# dashboard.cmake -- run with: ctest -S dashboard.cmake
set(CTEST_SOURCE_DIRECTORY "/src/myproject")
set(CTEST_BINARY_DIRECTORY "/tmp/build")
set(CTEST_CMAKE_GENERATOR "Ninja")

set(CTEST_BUILD_CONFIGURATION "Release")
set(CTEST_SITE     "$ENV{HOSTNAME}")
set(CTEST_BUILD_NAME "Linux-GCC13-Release")

ctest_start(Nightly)
ctest_update()
ctest_configure(OPTIONS "-DBUILD_TESTING=ON")
ctest_build()
ctest_test()
ctest_coverage()
ctest_memcheck()
ctest_submit()
```

`ctest -S dashboard.cmake` runs this end-to-end as part of nightly CI.

## 46.5 JUnit XML for Other CIs

GitHub Actions, GitLab CI, Jenkins, and Azure DevOps prefer JUnit XML test reports over CDash. CTest 3.21+ can produce them directly:

```bash
ctest --test-dir build --output-junit results.xml
```

GoogleTest and Catch2 can also emit JUnit XML themselves (via `--gtest_output=xml:foo.xml`), which CI picks up directly.

---

# 47. Code Coverage Integration

---

## 47.1 The Toolchains

| Toolchain | Mechanism | Tool to process |
|---|---|---|
| GCC | `-coverage` (`-fprofile-arcs -ftest-coverage`) | `gcov`, `lcov`, `gcovr` |
| Clang | `-fprofile-instr-generate -fcoverage-mapping` | `llvm-profdata`, `llvm-cov` |
| MSVC | `/Qspectre /experimental:coverage` (experimental); OpenCppCoverage | OpenCppCoverage |

The flags must be applied to **both** compile and link. CMake-side:

```cmake
add_library(coverage_flags INTERFACE)
target_compile_options(coverage_flags INTERFACE
    $<$<CONFIG:Debug>:--coverage>)
target_link_options(coverage_flags INTERFACE
    $<$<CONFIG:Debug>:--coverage>)

target_link_libraries(my_lib PRIVATE coverage_flags)
target_link_libraries(my_test PRIVATE coverage_flags)
```

## 47.2 GCC + lcov Workflow

```bash
# 1. Build with coverage flags
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DENABLE_COVERAGE=ON
cmake --build build

# 2. Run the tests (this generates .gcda files alongside .gcno)
ctest --test-dir build

# 3. Capture coverage
lcov --capture --directory build --output-file coverage.info

# 4. Strip system / third-party
lcov --remove coverage.info '/usr/*' '*/third_party/*' --output-file coverage.info

# 5. Generate HTML
genhtml coverage.info --output-directory coverage_html
```

`gcovr` is a Python alternative that produces HTML directly:

```bash
gcovr --root . --html --html-details -o coverage.html --exclude '.*/third_party/.*'
```

## 47.3 Clang Source-Based Coverage

```bash
# 1. Flags
cmake -DCMAKE_CXX_FLAGS='-fprofile-instr-generate -fcoverage-mapping' \
      -DCMAKE_EXE_LINKER_FLAGS='-fprofile-instr-generate' \
      -S . -B build
cmake --build build

# 2. Run tests; LLVM_PROFILE_FILE points to per-process .profraw
LLVM_PROFILE_FILE='build/test-%p.profraw' ctest --test-dir build

# 3. Merge profile data
llvm-profdata merge -sparse build/*.profraw -o coverage.profdata

# 4. Report
llvm-cov report  ./build/my_test -instr-profile=coverage.profdata
llvm-cov show    ./build/my_test -instr-profile=coverage.profdata -format=html > coverage.html
```

Clang's source-based coverage is more precise than GCC's: it tracks code coverage at the AST level, which gives accurate function and region counts, including for code with `inline` functions and templates.

## 47.4 Windows (OpenCppCoverage)

```bash
OpenCppCoverage --sources src --export_type html:coverage_html \
                -- build\Release\my_test.exe
```

OpenCppCoverage runs the binary under a debugger, intercepting line executions. No special compile flags needed -- it works on any PDB-built binary.

## 47.5 CI Integration

| Service | Coverage upload |
|---|---|
| Codecov | `bash <(curl -s https://codecov.io/bash)` after `lcov` |
| Coveralls | `coveralls-lcov coverage.info` |
| SonarQube | `sonar.cfamily.gcov.reportsPath`, or via `sonar-scanner` |
| GitHub Actions | Many actions wrap the above |

Either ship `coverage.info` (lcov format) or `coverage.xml` (Cobertura format) as the CI artifact; most services accept both.

---

# Part 11: Custom Commands and Code Generation

---

# 48. add_custom_command vs add_custom_target

---

## 48.1 The Two Commands

| Command | Semantics | Re-runs |
|---|---|---|
| `add_custom_command(OUTPUT ...)` | Defines a build rule: "to produce X, run Y" | When inputs are newer than outputs |
| `add_custom_command(TARGET ...)` | Hooks into an existing target's pre/post build steps | Every time that target is built |
| `add_custom_target(name COMMAND ...)` | Defines a target that always runs | Every build (target has no outputs to compare) |

The mental model: **`OUTPUT` is for files; `TARGET` is for steps tied to a target; `add_custom_target` is for pseudo-actions like `make doc` or `make format`**.

## 48.2 add_custom_command(OUTPUT)

```cmake
add_custom_command(
    OUTPUT  ${CMAKE_CURRENT_BINARY_DIR}/generated.cpp
    COMMAND ${Python_EXECUTABLE}
            ${CMAKE_CURRENT_SOURCE_DIR}/scripts/gen.py
            -o ${CMAKE_CURRENT_BINARY_DIR}/generated.cpp
            -i ${CMAKE_CURRENT_SOURCE_DIR}/schema.json
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/scripts/gen.py
            ${CMAKE_CURRENT_SOURCE_DIR}/schema.json
    COMMENT "Generating generated.cpp from schema.json")

add_executable(my_app main.cpp ${CMAKE_CURRENT_BINARY_DIR}/generated.cpp)
```

CMake sees that `my_app` depends on `generated.cpp`; `generated.cpp` is the output of the custom command; thus the build system runs the custom command when `gen.py` or `schema.json` changes. This is the canonical code-generation pattern.

## 48.3 add_custom_command(TARGET)

```cmake
add_executable(my_app main.cpp)

add_custom_command(TARGET my_app POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_SOURCE_DIR}/config.json
            $<TARGET_FILE_DIR:my_app>/config.json
    COMMENT "Copying config.json next to my_app")
```

| `TARGET` step | When it runs |
|---|---|
| `PRE_BUILD` | Before the target's own actions (Visual Studio only -- silently downgrades on others) |
| `PRE_LINK` | After compile, before link |
| `POST_BUILD` | After link |

`POST_BUILD` is by far the most useful: copy data files next to the executable, sign the binary, strip debug info, run a smoke test, etc.

## 48.4 add_custom_target

```cmake
add_custom_target(format
    COMMAND clang-format -i ${ALL_SOURCES}
    COMMENT "Running clang-format")

add_custom_target(docs
    COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Building Doxygen docs")
```

`add_custom_target` always runs when invoked (`cmake --build build --target format`). It has no output dependencies. If you want incremental behaviour, use `add_custom_command(OUTPUT ...)` and have a custom target depend on the outputs.

## 48.5 Combining Them

The robust pattern is custom-target wrapping custom-command outputs:

```cmake
set(GENERATED_FILES
    ${CMAKE_CURRENT_BINARY_DIR}/foo.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/foo.h)

add_custom_command(
    OUTPUT  ${GENERATED_FILES}
    COMMAND ${CODE_GEN} -o ${CMAKE_CURRENT_BINARY_DIR}
    DEPENDS schema.json)

add_custom_target(generate_foo DEPENDS ${GENERATED_FILES})

add_library(my_lib ${GENERATED_FILES} other_sources.cpp)
add_dependencies(my_lib generate_foo)
```

`add_custom_target` makes `generate_foo` always available to depend on, while `add_custom_command` provides the actual incremental rule.

## 48.6 Pitfall: Using configure_file for Generated Code

```cmake
# CONFIGURE TIME -- only re-runs when CMake re-configures
configure_file(template.cpp.in ${CMAKE_CURRENT_BINARY_DIR}/generated.cpp @ONLY)
```

`configure_file` works at configure time. If your template depends only on CMake variables, this is correct. If it depends on **external files** or build-time data, use `add_custom_command(OUTPUT ...)` instead.

---

# 49. Code Generation: Protobuf, Qt, Flatbuffers

---

## 49.1 Protocol Buffers

`find_package(Protobuf)` provides `protobuf_generate`:

```cmake
find_package(Protobuf REQUIRED)

add_library(my_proto OBJECT)

protobuf_generate(
    TARGET   my_proto
    PROTOS   proto/foo.proto proto/bar.proto
    LANGUAGE cpp
    IMPORT_DIRS proto)

target_link_libraries(my_proto PUBLIC protobuf::libprotobuf)
target_include_directories(my_proto PUBLIC ${CMAKE_CURRENT_BINARY_DIR})

add_executable(my_app main.cpp)
target_link_libraries(my_app PRIVATE my_proto)
```

`protobuf_generate` invokes `protoc` to produce `foo.pb.cc`/`foo.pb.h` for each `.proto` and attaches them to `my_proto` as sources. Section 48's `add_custom_command` machinery is hidden inside.

## 49.2 gRPC

```cmake
find_package(gRPC CONFIG REQUIRED)

protobuf_generate(
    TARGET   service_proto
    PROTOS   proto/service.proto
    LANGUAGE cpp)
protobuf_generate(
    TARGET   service_proto
    PROTOS   proto/service.proto
    LANGUAGE grpc
    GENERATE_EXTENSIONS .grpc.pb.h .grpc.pb.cc
    PLUGIN "protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>")
```

The second `protobuf_generate` call runs `protoc` with the gRPC plugin, producing service stubs.

## 49.3 Qt's moc, uic, rcc

Qt's metaobject compiler (`moc`), UI compiler (`uic`), and resource compiler (`rcc`) are integrated automatically when you opt in:

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
qt_standard_project_setup()                # 6.3+

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

qt_add_executable(my_app
    main.cpp
    mainwindow.cpp mainwindow.h mainwindow.ui
    resources.qrc)

target_link_libraries(my_app PRIVATE Qt6::Widgets)
```

`CMAKE_AUTOMOC ON` makes CMake scan every source for `Q_OBJECT`, run `moc` on matching headers, and add the generated code. The same logic for `.ui` files (`AUTOUIC`) and `.qrc` files (`AUTORCC`).

## 49.4 Flatbuffers

```cmake
find_package(flatbuffers CONFIG REQUIRED)

flatbuffers_generate_headers(
    TARGET schema_headers
    SCHEMAS schema/foo.fbs schema/bar.fbs
    BINARY_SCHEMAS_DIR ${CMAKE_BINARY_DIR}/bfbs)

target_link_libraries(my_app PRIVATE flatbuffers::flatbuffers schema_headers)
```

Flatbuffers produces only headers (`*_generated.h`), so the integration is lighter than Protobuf.

## 49.5 Bison / Flex

```cmake
find_package(BISON REQUIRED)
find_package(FLEX  REQUIRED)

bison_target(my_parser parser.y ${CMAKE_CURRENT_BINARY_DIR}/parser.cpp
             DEFINES_FILE ${CMAKE_CURRENT_BINARY_DIR}/parser.h)
flex_target(my_lexer lexer.l ${CMAKE_CURRENT_BINARY_DIR}/lexer.cpp)

add_flex_bison_dependency(my_lexer my_parser)

add_library(my_parser_lib
    ${BISON_my_parser_OUTPUTS}
    ${FLEX_my_lexer_OUTPUTS})

target_include_directories(my_parser_lib PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
```

`bison_target` and `flex_target` define the generation steps and populate variables (`BISON_my_parser_OUTPUTS`) with the produced files for use as sources.

---

# 50. configure_file and Header Generation

---

## 50.1 The Configure-Time Template

```cmake
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/include/version.h.in
    ${CMAKE_CURRENT_BINARY_DIR}/include/version.h
    @ONLY)

target_include_directories(my_lib PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/include)
```

`include/version.h.in`:

```cpp
#pragma once

#define MY_PROJECT_VERSION_MAJOR @PROJECT_VERSION_MAJOR@
#define MY_PROJECT_VERSION_MINOR @PROJECT_VERSION_MINOR@
#define MY_PROJECT_VERSION_PATCH @PROJECT_VERSION_PATCH@
#define MY_PROJECT_VERSION       "@PROJECT_VERSION@"
#define MY_PROJECT_GIT_HASH      "@MY_PROJECT_GIT_HASH@"

#cmakedefine MY_PROJECT_WITH_SSL
#cmakedefine01 MY_PROJECT_WITH_LOGGING
```

CMake substitutes `@VAR@` with `${VAR}`. `#cmakedefine` becomes `#define` if the variable is truthy, otherwise a comment. `#cmakedefine01` produces `#define X 0` or `#define X 1`.

| Form | Effect when truthy | Effect when falsy/undef |
|---|---|---|
| `#cmakedefine VAR` | `#define VAR` | `/* #undef VAR */` |
| `#cmakedefine VAR @VAR@` | `#define VAR <value>` | `/* #undef VAR */` |
| `#cmakedefine01 VAR` | `#define VAR 1` | `#define VAR 0` |

## 50.2 Embedding Git Hash

```cmake
find_package(Git)
if(Git_FOUND)
    execute_process(
        COMMAND ${GIT_EXECUTABLE} rev-parse --short HEAD
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        OUTPUT_VARIABLE MY_PROJECT_GIT_HASH
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET)
endif()

configure_file(version.h.in version.h @ONLY)
```

The hash is captured at configure time. If you want it to refresh every build, use `add_custom_command` to regenerate `version.h` from the latest hash.

## 50.3 file(GENERATE) for Build-Time Templates

```cmake
file(GENERATE
    OUTPUT $<TARGET_FILE_DIR:my_lib>/my_lib_info.json
    CONTENT
"{
    \"name\": \"my_lib\",
    \"version\": \"${PROJECT_VERSION}\",
    \"binary\": \"$<TARGET_FILE:my_lib>\",
    \"config\": \"$<CONFIG>\"
}\n")
```

Because `$<...>` is involved, `configure_file` cannot be used here -- the genexs would appear literally in the output. `file(GENERATE)` is the build-time evaluator.

## 50.4 @ONLY vs Plain configure_file

```cmake
configure_file(in.txt out.txt @ONLY)    # only @VAR@ substitution
configure_file(in.txt out.txt)          # @VAR@ AND ${VAR} substitution
```

`@ONLY` is the safer choice -- shell-style `${VAR}` in your template stays literal, avoiding accidental substitution of shell variables.

---

# 51. CMake Script Mode

---

## 51.1 Running a CMake Script

`cmake -P script.cmake` runs a `.cmake` file in **script mode**: no project, no build tree, just the CMake language as a portable scripting environment.

```cmake
# script.cmake
message(STATUS "Args: ${CMAKE_ARGV0} ${CMAKE_ARGV1} ${CMAKE_ARGV2}")

file(GLOB sources CONFIGURE_DEPENDS "src/*.cpp")
foreach(src IN LISTS sources)
    file(SIZE ${src} sz)
    message(STATUS "${src}: ${sz} bytes")
endforeach()

execute_process(COMMAND ${CMAKE_COMMAND} -E sha256sum src/main.cpp
                OUTPUT_VARIABLE hash)
message(STATUS "${hash}")
```

```bash
cmake -P script.cmake arg1 arg2 arg3
```

Script mode is useful for:

- Cross-platform shell-like utilities (mkdir, copy, hash, tar) that work the same on Windows and Unix.
- Build-step glue: pre-process a file, regenerate a header, modify a config.
- Test helpers: `add_test(NAME ... COMMAND ${CMAKE_COMMAND} -P run_test.cmake)`.

## 51.2 cmake -E -- Built-In Commands

`cmake -E` exposes a portable command palette:

```bash
cmake -E make_directory dir
cmake -E remove_directory dir
cmake -E copy_if_different a b
cmake -E rename a b
cmake -E touch foo
cmake -E sleep 5
cmake -E sha256sum file
cmake -E tar cf out.tar dir/
cmake -E tar xzf in.tar.gz
cmake -E env VAR=val cmd args...      # set env vars for the wrapped command
cmake -E echo "hello"                  # cross-platform echo
cmake -E time cmd args...              # like /usr/bin/time but portable
```

In CMake scripts and `add_custom_command`s, prefer `${CMAKE_COMMAND} -E <cmd>` over native shell commands to keep your build portable across Linux/macOS/Windows.

## 51.3 Custom Cross-Platform Helpers

```cmake
# helper.cmake -- portable rmrf

if(NOT DEFINED TARGET_DIR)
    message(FATAL_ERROR "Usage: cmake -DTARGET_DIR=<path> -P helper.cmake")
endif()

if(EXISTS "${TARGET_DIR}")
    file(REMOVE_RECURSE "${TARGET_DIR}")
    message(STATUS "Removed ${TARGET_DIR}")
endif()
```

Invoke:

```bash
cmake -DTARGET_DIR=build/foo -P helper.cmake
```

Cache variables (`-D`) become normal variables in script mode.

---

# Part 12: Compiler Flags, Sanitizers, and Hardening

---

# 52. Per-Target vs Global Flags

---

## 52.1 Why Global Flags Are a Smell

```cmake
# DON'T do this in libraries
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror")
add_compile_options(-Wall -Wextra -Werror)
```

These set flags **globally**: every target in this directory and below gets them. Problems:

- Vendored or `add_subdirectory()`d third-party code inherits your strict flags and breaks.
- Consumers `add_subdirectory()`ing your project get them too, which they did not opt into.
- They are sticky: a `set(CMAKE_CXX_FLAGS ...)` in a subdirectory leaks back up via cache pollution if mis-done.

## 52.2 Per-Target via target_compile_options

```cmake
target_compile_options(my_lib PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /utf-8 /permissive->)
```

Now only `my_lib` is affected. Vendored code in `third_party/` is untouched.

## 52.3 The "Warning Policy" Interface Library Pattern

```cmake
add_library(project_warnings INTERFACE)
target_compile_options(project_warnings INTERFACE
    $<$<CXX_COMPILER_ID:GNU>:
        -Wall -Wextra -Wpedantic
        -Wshadow -Wnon-virtual-dtor -Wold-style-cast
        -Wcast-align -Wunused -Woverloaded-virtual -Wconversion
        -Wsign-conversion -Wnull-dereference -Wdouble-promotion
        -Wformat=2 -Wimplicit-fallthrough>
    $<$<CXX_COMPILER_ID:Clang,AppleClang>:
        -Wall -Wextra -Wpedantic
        -Wshadow -Wnon-virtual-dtor -Wold-style-cast
        -Wcast-align -Wunused -Woverloaded-virtual -Wconversion
        -Wsign-conversion -Wnull-dereference -Wdouble-promotion
        -Wformat=2 -Wimplicit-fallthrough>
    $<$<CXX_COMPILER_ID:MSVC>:
        /W4 /utf-8 /permissive-
        /w14640 /w14826>)

# Every internal lib opts in:
target_link_libraries(libfoo PRIVATE project_warnings)
target_link_libraries(libbar PRIVATE project_warnings)

# Vendored libs do NOT opt in:
add_subdirectory(third_party/somedep)   # builds with its own flags
```

This pattern, popularised by Jason Turner's `cmake_template` and others, is the cleanest "warnings everywhere we own, leave everyone else alone" approach.

## 52.4 When Global Is OK

```cmake
# Top-level project, after add_subdirectory(third_party/...), before our own subdirs
add_compile_options($<$<CXX_COMPILER_ID:MSVC>:/utf-8>)
```

Trivial, compiler-agnostic options that should affect everything (`/utf-8` for UTF-8 source files on MSVC, `-fdiagnostics-color=always`) can be set globally. Anything that might break third-party code shouldn't.

---

# 53. Sanitizers

---

## 53.1 The Sanitizer Family

| Sanitizer | Detects | Slowdown | Memory overhead |
|---|---|---|---|
| **AddressSanitizer** (ASan) | Out-of-bounds, use-after-free, double-free, leaks | 2-3x | ~3x |
| **UndefinedBehaviorSanitizer** (UBSan) | Signed overflow, null deref, alignment violations, etc. | ~1.2x | Low |
| **ThreadSanitizer** (TSan) | Data races, deadlocks | 5-15x | 5-10x |
| **MemorySanitizer** (MSan) | Uninitialised reads | 3x | 2-3x; requires instrumented libc |
| **LeakSanitizer** (LSan) | Memory leaks | Minimal | Same as ASan (bundled) |

Sanitizers are compile-and-link flags supported by GCC and Clang (MSVC supports ASan since VS 2019 16.9).

## 53.2 Wiring Sanitizers via INTERFACE Library

```cmake
option(ENABLE_ASAN  "Enable AddressSanitizer"          OFF)
option(ENABLE_UBSAN "Enable UndefinedBehaviorSanitizer" OFF)
option(ENABLE_TSAN  "Enable ThreadSanitizer"           OFF)

add_library(project_sanitizers INTERFACE)

if(ENABLE_ASAN AND NOT MSVC)
    target_compile_options(project_sanitizers INTERFACE
        -fsanitize=address -fno-omit-frame-pointer)
    target_link_options(project_sanitizers INTERFACE
        -fsanitize=address)
endif()

if(ENABLE_UBSAN)
    target_compile_options(project_sanitizers INTERFACE
        -fsanitize=undefined -fno-omit-frame-pointer)
    target_link_options(project_sanitizers INTERFACE
        -fsanitize=undefined)
endif()

if(ENABLE_TSAN)
    if(ENABLE_ASAN)
        message(FATAL_ERROR "TSan and ASan are incompatible")
    endif()
    target_compile_options(project_sanitizers INTERFACE -fsanitize=thread)
    target_link_options(project_sanitizers INTERFACE -fsanitize=thread)
endif()

target_link_libraries(my_lib PRIVATE project_sanitizers)
```

The flags must be on **both** compile and link, which is why `target_link_options` mirrors `target_compile_options`.

## 53.3 Important Incompatibilities

| Combination | Status |
|---|---|
| ASan + TSan | Incompatible -- cannot use both at once |
| ASan + MSan | Incompatible |
| MSan + uninstrumented libc | False positives; need MSan-instrumented stdlib |
| UBSan + anything | Combines freely |
| TSan + UBSan | Works |

ASan and UBSan together is the standard CI combo for unit tests; TSan is run separately on tests known to be concurrent.

## 53.4 Common Runtime Options

```bash
ASAN_OPTIONS=detect_leaks=1:halt_on_error=1:abort_on_error=1 ./my_test
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 ./my_test
TSAN_OPTIONS=halt_on_error=1:second_deadlock_stack=1 ./my_test
```

| Option | Notes |
|---|---|
| `halt_on_error` | Abort on first error (default for some sanitizers, not all) |
| `abort_on_error` | Use `abort()` not `_exit()`, so coredumps work |
| `detect_leaks` | LSan-on-by-default with ASan on Linux |
| `print_stacktrace` | Each report includes a stack |
| `suppressions=<file>` | Path to a list of known-issue rules |

## 53.5 ctest Integration

```cmake
add_test(NAME my_test COMMAND my_test)
set_tests_properties(my_test PROPERTIES
    ENVIRONMENT "ASAN_OPTIONS=halt_on_error=1:abort_on_error=1;UBSAN_OPTIONS=halt_on_error=1")
```

Standard CI practice: ASan+UBSan build runs the entire test suite; any sanitizer error fails the build.

---

# 54. Hardening and Security Flags

---

## 54.1 The Standard Hardening Flag Set

For GCC/Clang on Linux:

| Flag | Effect |
|---|---|
| `-fstack-protector-strong` | Stack canaries on functions with vulnerable stack frames |
| `-fstack-clash-protection` | Probe pages of the stack to prevent stack-clash attacks |
| `-D_FORTIFY_SOURCE=2` (`=3` if available) | Compile-time and runtime checks of stdlib calls (`strcpy` etc.) |
| `-D_GLIBCXX_ASSERTIONS` | Enable libstdc++ assertion checks |
| `-fPIE -pie` (link) | Position-Independent Executable; ASLR for executables |
| `-Wl,-z,relro,-z,now` | Read-Only Relocations; resolve all symbols at startup |
| `-Wl,-z,noexecstack` | Mark the stack non-executable |
| `-fcf-protection=full` | Control-Flow Integrity (Intel CET, modern CPUs) |
| `-fstack-clash-protection` | Defend against stack-clash exploits |

```cmake
add_library(project_hardening INTERFACE)
target_compile_options(project_hardening INTERFACE
    $<$<COMPILE_LANGUAGE:CXX>:
        $<$<CXX_COMPILER_ID:GNU,Clang>:
            -fstack-protector-strong
            -fstack-clash-protection
            -fcf-protection=full
            -D_FORTIFY_SOURCE=2
            -D_GLIBCXX_ASSERTIONS>>)

target_link_options(project_hardening INTERFACE
    $<$<CXX_COMPILER_ID:GNU,Clang>:
        -Wl,-z,relro
        -Wl,-z,now
        -Wl,-z,noexecstack>)
```

`_FORTIFY_SOURCE` requires `-O1` or higher; combining it with `-O0` produces a warning and no effect. Apply hardening to Release builds, not Debug.

## 54.2 POSITION_INDEPENDENT_CODE

```cmake
set_target_properties(my_lib PROPERTIES POSITION_INDEPENDENT_CODE ON)

# or globally:
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
```

SHARED libraries need PIC always; STATIC libraries need it only if they will be linked into shared libraries. On modern Linux distributions, PIE executables (also using PIC) are standard.

## 54.3 MSVC Hardening

| MSVC flag | Linux/Clang equivalent |
|---|---|
| `/GS` | `-fstack-protector` (on by default) |
| `/sdl` | `/GS` plus extra checks |
| `/DYNAMICBASE` | ASLR (on by default) |
| `/NXCOMPAT` | DEP/NX |
| `/guard:cf` | CFG (Control Flow Guard) |
| `/Qspectre` | Spectre mitigations |

```cmake
target_compile_options(my_lib PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/sdl /guard:cf /Qspectre>)
target_link_options(my_lib PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/DYNAMICBASE /NXCOMPAT /guard:cf>)
```

## 54.4 The MSVC CRT (CMP0091)

```cmake
cmake_minimum_required(VERSION 3.15)        # for CMP0091 NEW
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
```

Values: `MultiThreaded`, `MultiThreadedDLL`, `MultiThreadedDebug`, `MultiThreadedDebugDLL`. The DLL variants use the shared CRT (`/MD`); the non-DLL variants use the static CRT (`/MT`).

With `CMP0091 NEW`, this property is the single source of truth; without it, you'd be setting `/MT`/`/MD` flags via `CMAKE_CXX_FLAGS_<CONFIG>` and battling override propagation.

---

# 55. LTO and IPO

---

## 55.1 What LTO/IPO Does

Link-Time Optimization (also called Interprocedural Optimization on MSVC) defers code generation to link time, allowing the linker to see across translation-unit boundaries: inlining, devirtualisation, dead-code elimination, and constant propagation across `.o` files.

Typical effect: 5-15% performance improvement, 10-50% binary-size reduction, 2-5x longer link time.

## 55.2 CheckIPOSupported

```cmake
include(CheckIPOSupported)
check_ipo_supported(RESULT ipo_supported OUTPUT ipo_error)

if(ipo_supported)
    set_property(TARGET my_lib PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
else()
    message(STATUS "IPO not supported: ${ipo_error}")
endif()
```

`check_ipo_supported` does a `try_compile` to verify the toolchain supports IPO, then you set `INTERPROCEDURAL_OPTIMIZATION` on individual targets.

## 55.3 Per-Config IPO

```cmake
set_target_properties(my_app PROPERTIES
    INTERPROCEDURAL_OPTIMIZATION_RELEASE        TRUE
    INTERPROCEDURAL_OPTIMIZATION_RELWITHDEBINFO TRUE)
```

LTO in Debug is rarely useful (link times explode); enable per-config.

## 55.4 ThinLTO vs Full LTO

Clang and modern GCC support ThinLTO (`-flto=thin`), which parallelises LTO across linker threads, dramatically reducing link time while keeping most of the optimisation benefit.

```cmake
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(my_app PRIVATE $<$<CONFIG:Release>:-flto=thin>)
    target_link_options(my_app PRIVATE    $<$<CONFIG:Release>:-flto=thin>)
endif()
```

When using ThinLTO, you typically also want `lld` as the linker (`-fuse-ld=lld`); the default GNU `ld` is much slower at LTO link.

## 55.5 Static Library Considerations

A static library with LTO emits LLVM IR (`.o` bitcode) instead of native object code. Consumers must also use LTO -- or at least use a recent linker that can mix LTO and non-LTO inputs. Be conservative: distributed static libraries should be non-LTO; LTO is more reliably an executable-side concern.

---

# 56. Warning Levels and Warnings-as-Errors

---

## 56.1 The Reasonable Defaults

```cmake
target_compile_options(my_lib PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:
        -Wall -Wextra -Wpedantic
        -Wshadow -Wnon-virtual-dtor -Wcast-align
        -Wunused -Woverloaded-virtual -Wmisleading-indentation
        -Wduplicated-cond -Wduplicated-branches
        -Wlogical-op -Wnull-dereference -Wdouble-promotion
        -Wformat=2>
    $<$<CXX_COMPILER_ID:MSVC>:
        /W4 /permissive- /utf-8>)
```

(Some GCC-specific warnings like `-Wduplicated-branches` are not in Clang, so split if you maintain strict per-compiler lists.)

## 56.2 Warnings As Errors

```cmake
option(MY_PROJECT_WARNINGS_AS_ERRORS "Treat warnings as errors" OFF)

if(MY_PROJECT_WARNINGS_AS_ERRORS)
    target_compile_options(my_lib PRIVATE
        $<$<CXX_COMPILER_ID:GNU,Clang>:-Werror>
        $<$<CXX_COMPILER_ID:MSVC>:/WX>)
endif()
```

The right pattern: **off by default** for casual builds and developer ergonomics, **on in CI** so that no warning ever makes it to main. Distributions then build with warnings-as-errors off (because they pin compiler versions that may introduce new warnings).

`CMAKE_COMPILE_WARNING_AS_ERROR` (3.24+) is a per-target boolean property with the same effect, compiler-agnostic:

```cmake
set_target_properties(my_lib PROPERTIES COMPILE_WARNING_AS_ERROR ON)
```

## 56.3 Suppressing Warnings Locally

Sometimes you must silence one warning in one place:

```cmake
target_compile_options(my_one_file_target PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wno-deprecated-declarations>)
```

Per-source-file:

```cmake
set_source_files_properties(legacy.cpp PROPERTIES
    COMPILE_OPTIONS "-Wno-old-style-cast")
```

Try to avoid this -- usually the warning is right. The right escape hatch is to fix the underlying code or, when truly necessary, use `#pragma GCC diagnostic push/pop` in the source.

## 56.4 Third-Party Headers via SYSTEM

```cmake
target_include_directories(my_lib SYSTEM PRIVATE third_party/somelib/include)
```

`SYSTEM` makes the compiler treat those headers as system headers; most warnings are suppressed inside them. This is the right answer when you control the build but not the third-party code.

`FetchContent_Declare(... SYSTEM)` does the same thing across the dependency's includes (CMake 3.25+).

---

# Part 13: IDE and Static-Analysis Integration

---

# 57. compile_commands.json for clangd

---

## 57.1 What compile_commands.json Is

`compile_commands.json` is a JSON file listing every translation unit and the exact command used to compile it. Tools like clangd, ccls, include-what-you-use, clang-tidy, and many IDEs read it to get authoritative build information.

```json
[
    {
        "directory": "/home/me/proj/build",
        "command": "/usr/bin/g++ -DFOO=1 -I/home/me/proj/include -std=c++20 -c /home/me/proj/src/foo.cpp",
        "file": "/home/me/proj/src/foo.cpp"
    },
    ...
]
```

## 57.2 Enabling Generation

```cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```

Set this once near the top of your top-level `CMakeLists.txt`. After configure, `build/compile_commands.json` exists.

`Ninja` and `Make` generators support this natively; **Visual Studio and Xcode generators do not** (they have their own project formats). For VS-based projects, use Ninja-Multi-Config or have a sidecar configure step.

## 57.3 Symlinking to the Repo Root

clangd looks in the source tree by default:

```bash
ln -sf build/compile_commands.json compile_commands.json
```

Or in CMake:

```cmake
if(CMAKE_EXPORT_COMPILE_COMMANDS)
    file(CREATE_LINK
        ${CMAKE_BINARY_DIR}/compile_commands.json
        ${CMAKE_SOURCE_DIR}/compile_commands.json
        SYMBOLIC)
endif()
```

This keeps the file under version control of the source tree's location, where IDEs look for it.

## 57.4 Multiple Compilation DBs

For projects with multiple build dirs (debug, release, asan), point clangd at one via `.clangd`:

```yaml
# .clangd at project root
CompileFlags:
  CompilationDatabase: build-debug
```

Or via CLI:

```bash
clangd --compile-commands-dir=build-debug
```

## 57.5 What clangd Does With It

For each open file, clangd:

1. Finds its compilation entry.
2. Replays the command in a virtual file system.
3. Provides go-to-definition, autocompletion, diagnostics, code actions.

The accuracy of clangd is proportional to the accuracy of `compile_commands.json`. If your build does codegen, ensure the generated files are in `compile_commands.json` (set `CMAKE_EXPORT_COMPILE_COMMANDS ON` after `add_custom_command` declarations).

---

# 58. clang-tidy, clang-format, and Friends

---

## 58.1 Wiring clang-tidy via CMake Property

```cmake
find_program(CLANG_TIDY_EXE clang-tidy REQUIRED)

set(CMAKE_CXX_CLANG_TIDY
    ${CLANG_TIDY_EXE}
    --warnings-as-errors=*
    --header-filter=^${CMAKE_SOURCE_DIR}/include)

add_library(my_lib src/foo.cpp)
```

`CMAKE_CXX_CLANG_TIDY` (and `CMAKE_C_CLANG_TIDY`) is a list whose first element is the executable and remaining elements are extra args. When set, CMake runs `clang-tidy` as part of every compile -- the tool gets the exact same flags as the compiler, so it sees the same definitions and includes.

Per-target:

```cmake
set_target_properties(my_lib PROPERTIES
    CXX_CLANG_TIDY "${CLANG_TIDY_EXE};--config-file=${CMAKE_SOURCE_DIR}/.clang-tidy")
```

## 58.2 .clang-tidy Configuration

Put a `.clang-tidy` file at the project root:

```yaml
Checks: >
  -*,
  bugprone-*,
  cppcoreguidelines-*,
  modernize-*,
  performance-*,
  portability-*,
  readability-*,
  -modernize-use-trailing-return-type,
  -readability-magic-numbers,
  -cppcoreguidelines-pro-bounds-pointer-arithmetic
WarningsAsErrors: ''
HeaderFilterRegex: '^include/my_project/.*\.h(pp)?$'
FormatStyle: file
```

This enables a curated set of checks and turns off the few that produce too much noise.

## 58.3 clang-format Integration

Two common patterns:

**Pattern 1: Custom target for "format all"**:

```cmake
find_program(CLANG_FORMAT_EXE clang-format)

if(CLANG_FORMAT_EXE)
    file(GLOB_RECURSE ALL_SOURCES
        ${CMAKE_SOURCE_DIR}/src/*.cpp
        ${CMAKE_SOURCE_DIR}/src/*.h
        ${CMAKE_SOURCE_DIR}/include/*.hpp
        ${CMAKE_SOURCE_DIR}/tests/*.cpp)

    add_custom_target(format
        COMMAND ${CLANG_FORMAT_EXE} -i ${ALL_SOURCES}
        COMMENT "Running clang-format on ${ALL_SOURCES}")

    add_custom_target(format-check
        COMMAND ${CLANG_FORMAT_EXE} --dry-run --Werror ${ALL_SOURCES}
        COMMENT "Checking formatting")
endif()
```

Now `cmake --build build --target format` rewrites files; `--target format-check` is the CI gate.

**Pattern 2: pre-commit hook** -- managed outside CMake, equally common.

## 58.4 include-what-you-use

```cmake
find_program(IWYU_EXE include-what-you-use)
if(IWYU_EXE)
    set(CMAKE_CXX_INCLUDE_WHAT_YOU_USE
        ${IWYU_EXE}
        -Xiwyu --no_fwd_decls
        -Xiwyu --mapping_file=${CMAKE_SOURCE_DIR}/iwyu.imp)
endif()
```

Same mechanism as `CMAKE_CXX_CLANG_TIDY`. IWYU suggests `#include` cleanups based on what symbols a file actually uses.

## 58.5 cppcheck

```cmake
find_program(CPPCHECK_EXE cppcheck)
if(CPPCHECK_EXE)
    set(CMAKE_CXX_CPPCHECK
        ${CPPCHECK_EXE}
        --enable=warning,style,performance,portability
        --suppress=missingInclude
        --inline-suppr
        --quiet)
endif()
```

`CMAKE_CXX_CPPCHECK` is the analogous property for cppcheck. cppcheck is non-clang-based and catches some classes of bugs (e.g., uninitialised members) that clang-tidy misses; the two are complementary.

## 58.6 Turning Linters Off in CI vs Local

```cmake
option(ENABLE_LINTERS "Run clang-tidy and others as part of build" OFF)

if(ENABLE_LINTERS)
    if(CLANG_TIDY_EXE)
        set(CMAKE_CXX_CLANG_TIDY ${CLANG_TIDY_EXE})
    endif()
    if(IWYU_EXE)
        set(CMAKE_CXX_INCLUDE_WHAT_YOU_USE ${IWYU_EXE})
    endif()
endif()
```

Linters can add 2-3x to compile time. Default off, on in dedicated CI jobs.

---

# 59. IDE Support

---

## 59.1 VS Code (CMake Tools)

CMake Tools (Microsoft, official) is the dominant CMake IDE integration in VS Code:

- Reads `CMakePresets.json` (selects configure preset, build preset, test preset from the UI).
- Auto-generates `compile_commands.json` for clangd.
- Provides "Run CTest" from the test explorer.
- Surface CMake errors in the Problems panel.

Workspace config (`.vscode/settings.json`):

```json
{
    "cmake.useCMakePresets": "auto",
    "cmake.configureOnOpen": true,
    "C_Cpp.intelliSenseEngine": "disabled",
    "clangd.arguments": [
        "--compile-commands-dir=${workspaceFolder}/build",
        "--header-insertion=never"
    ]
}
```

Disabling `C_Cpp.intelliSenseEngine` and using clangd is the modern recommendation -- clangd is faster and more accurate for CMake-driven projects.

## 59.2 CLion

CLion (JetBrains) treats CMake as a first-class project model:

- Reads `CMakeLists.txt` directly; no `.idea` project for CMake projects.
- Supports CMake Presets (since 2022.1).
- Profiles, profilers, run configurations all driven by CMake targets.
- Built-in formatter and analyser are not clangd; CLion's own indexer is comparable but slightly different.

To switch CLion to use clangd-based analysis: Settings -> Languages -> C/C++ -> Clangd. Or use external clangd via `compile_commands.json`.

## 59.3 Visual Studio

Visual Studio (2017+) supports two CMake modes:

| Mode | How |
|---|---|
| **Open Folder** | Visual Studio reads `CMakeLists.txt` directly, generates Ninja under the hood, reads `CMakePresets.json` for configurations |
| **Generated .sln** | Run `cmake -G "Visual Studio 17 2022"` externally, then open the `.sln` in VS |

The Open Folder mode is the modern recommendation for new projects; the generated `.sln` mode is useful when you have many `.props` files and team-wide MSBuild conventions.

```json
// CMakeSettings.json (older Open Folder mode; superseded by CMakePresets)
{
    "configurations": [
        { "name": "x64-Release", "generator": "Ninja",
          "configurationType": "Release", "buildRoot": "${projectDir}/out/build/${name}",
          "installRoot": "${projectDir}/out/install/${name}" }
    ]
}
```

CMakePresets.json supersedes `CMakeSettings.json` for new projects.

## 59.4 Xcode

Xcode is the macOS-native option, generated by `cmake -G Xcode`. Multi-config; `CMAKE_BUILD_TYPE` is ignored; configure with `CMAKE_CONFIGURATION_TYPES=Debug;Release`.

Xcode quirks:

- Requires `CMAKE_OSX_DEPLOYMENT_TARGET` for proper minimum-version targeting.
- `CMAKE_OSX_ARCHITECTURES=arm64;x86_64` produces universal binaries.
- Frameworks: `add_library(foo SHARED FRAMEWORK ...)` plus framework-specific properties.

For day-to-day development on macOS, Ninja-Multi-Config is faster than Xcode; reserve Xcode generator for iOS builds or when you need Instruments and Xcode-specific tools.

## 59.5 Qt Creator

Qt Creator reads `CMakeLists.txt` directly, supports `CMakePresets.json`, and has good built-in Qt-aware features (UI designer, Qt Quick). The Kit system maps to CMake toolchain files.

## 59.6 Folders and Project Views

For large projects, folder organisation matters in IDE project views (Visual Studio and Xcode):

```cmake
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set_target_properties(my_lib       PROPERTIES FOLDER "Core")
set_target_properties(my_tests     PROPERTIES FOLDER "Tests/Unit")
set_target_properties(my_benchmark PROPERTIES FOLDER "Tests/Benchmarks")
```

In Visual Studio, this groups targets into "Core", "Tests/Unit", "Tests/Benchmarks" virtual folders. Source files within a target can be grouped with `source_group(... FILES ...)` or auto-grouped with `source_group(TREE ...)`:

```cmake
source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})
```

This mirrors the on-disk directory layout in the IDE's project view.

---

# Part 14: Performance and Modern Features

---

# 60. Reducing Configure Time

---

## 60.1 The Configure-Time Budget

A clean configure of a large project (1000+ targets, dozens of `find_package` calls) takes 30-120 seconds. Repeated reconfigures (after edits to `CMakeLists.txt`) are usually 5-30 seconds. When this grows beyond a minute, productivity suffers.

## 60.2 Profile the Configure

```bash
cmake -S . -B build --profiling-output=cmake-profile.json --profiling-format=google-trace
```

CMake (3.18+) writes a Chrome-trace JSON. Load it in `chrome://tracing/` or perfetto.dev to see which commands took the time.

```bash
cmake -S . -B build --trace --trace-expand          # ultra-verbose trace
cmake -S . -B build --trace-redirect=trace.log      # to file
cmake -S . -B build --debug-find                    # show find_package details
```

## 60.3 Common Slow Spots

| Slow spot | Mitigation |
|---|---|
| `find_package` doing exhaustive system searches | Set `<Pkg>_ROOT` / `CMAKE_PREFIX_PATH` to point directly |
| `FetchContent_MakeAvailable` redownloading | Use `GIT_SHALLOW` + tag, not branch; ensure cache is hot |
| Many `try_compile` / `try_run` checks | Cache results explicitly; don't re-detect every configure |
| `file(GLOB)` on huge trees | Use explicit listings |
| Recursive `add_subdirectory` chain through many dirs | Flatten; combine sibling dirs |
| C compiler probe when only C++ needed | `project(name LANGUAGES CXX)` (skip C) |

## 60.4 Cache try_compile Results

```cmake
if(NOT DEFINED HAVE_SOMETHING)
    include(CheckCXXSourceCompiles)
    check_cxx_source_compiles("
        #include <chrono>
        int main() { return 0; }
    " HAVE_SOMETHING)
endif()
```

`check_cxx_source_compiles` caches its result by default. The `if(NOT DEFINED)` wrapper isn't strictly necessary, but it makes the intent explicit.

## 60.5 Avoid Recursive add_subdirectory Where Possible

Each `add_subdirectory` opens a fresh directory scope, copies variables, and reads a `CMakeLists.txt`. In huge trees, 1000 subdirs cost real time.

The alternative: a flatter structure, where each library is in a sibling directory and the top-level just does `add_subdirectory(libfoo); add_subdirectory(libbar); ...`.

---

# 61. Unity Builds and Precompiled Headers

---

## 61.1 Unity Builds

A **unity build** concatenates many translation units into one `.cpp` per batch, drastically reducing parser invocations and template instantiations.

```cmake
set_target_properties(my_lib PROPERTIES UNITY_BUILD ON)
set_target_properties(my_lib PROPERTIES UNITY_BUILD_BATCH_SIZE 16)
```

Or globally:

```cmake
set(CMAKE_UNITY_BUILD ON)
```

Typical effect: 2-5x faster full builds. Trade-offs:

- **Anonymous namespaces** in different files now share scope (name collisions).
- **`static` symbols** with the same name in different files collide.
- One compilation error has confusingly-mixed file references.
- Incremental rebuilds are coarser (changing one file rebuilds its whole batch).

For these reasons, unity builds are typically enabled for **CI/full builds** and off for **incremental development**.

## 61.2 Precompiled Headers

```cmake
target_precompile_headers(my_lib PRIVATE
    <vector>
    <string>
    <unordered_map>
    "common.h")
```

CMake compiles the listed headers once into a `.pch` (`.gch` on GCC) and prepends it to every TU of the target. Effect: 1.5-3x faster compilation for translation units that include any of the listed headers.

Pitfalls:

- The same PCH cannot be shared across targets with different flags.
- Adding too many headers can cause memory issues with the PCH binary.
- Including the PCH inadvertently leaks symbols into TUs that didn't `#include` them, hiding missing-include bugs.

For libraries you publish to the world, leave PCH off by default; the consumer can opt in.

## 61.3 REUSE_FROM (3.16+)

```cmake
target_precompile_headers(big_lib PRIVATE
    <vector> <string> <map>)

target_precompile_headers(small_lib REUSE_FROM big_lib)
```

Multiple targets can share one compiled PCH if their flags allow. CMake handles the dependency.

## 61.4 Combining Unity Builds and PCH

Generally complementary. Unity reduces parse cost; PCH reduces preprocess+parse cost of large headers. Best for fastest builds: both on. Best for incremental development: both off (so individual file rebuilds are fast and correct).

```cmake
option(ENABLE_UNITY "Enable unity builds for CI" OFF)
option(ENABLE_PCH   "Enable PCH for select targets" OFF)
```

---

# 62. C++20 Modules Support

---

## 62.1 What Modules Bring

C++20 modules let you replace `#include` with `import`:

```cpp
// math.cppm  (module interface)
export module math;
export int square(int x) { return x * x; }

// main.cpp
import math;
int main() { return square(3); }
```

Build benefit: parse the module's interface once, reuse a compiled BMI (Built Module Interface) across consumers. For large codebases dominated by header parsing, modules can give multi-x speedups.

## 62.2 Build-System Implications

Modules add a new build phase: **dependency scanning**. Before compiling, the build system must scan each TU to determine which modules it imports, then build the producer of those modules first. This is a fundamentally new graph constraint.

## 62.3 CMake Module Support (3.28+)

```cmake
cmake_minimum_required(VERSION 3.28)
project(modules_demo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_SCAN_FOR_MODULES ON)

add_library(math)
target_sources(math
    PUBLIC FILE_SET CXX_MODULES
    FILES math.cppm)

add_executable(app main.cpp)
target_link_libraries(app PRIVATE math)
```

| Element | Meaning |
|---|---|
| `FILE_SET CXX_MODULES` | Declare files in this set as C++ module interface units |
| `CMAKE_CXX_SCAN_FOR_MODULES` | Globally enable scanning |
| Compiler support | GCC 14+, Clang 16+, MSVC 19.35+ |

The full landscape (mixed module-and-header code, header units, named-module installs) is still evolving. CMake 3.28+ marks the first version where pure-modules projects are practical.

## 62.4 Header Units

A header unit treats a regular header as if it were a module:

```cpp
import <vector>;        // header unit form
```

```cmake
target_sources(my_lib PUBLIC
    FILE_SET CXX_MODULE_HEADER_UNITS
    BASE_DIRS include
    FILES include/my_header.h)
```

Header units are less mature in CMake than named modules; expect this to improve.

## 62.5 Recommendation

For new projects targeting only the latest toolchains, modules are usable. For libraries that must support a range of toolchains and consumers, stick with headers for now and adopt modules incrementally over the next few years.

---

# 63. Refactoring Legacy CMake

---

## 63.1 Telltales of Legacy

| Smell | Modern replacement |
|---|---|
| `add_definitions(-DFOO)` | `target_compile_definitions(target PRIVATE FOO)` |
| `include_directories(...)` | `target_include_directories(target PUBLIC|PRIVATE ...)` |
| `link_directories(...)` | Almost never needed -- use imported targets or full paths |
| `link_libraries(...)` | `target_link_libraries(target PRIVATE ...)` |
| `set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")` | `target_compile_options(target PRIVATE -Wall)` |
| `${OPENSSL_LIBRARIES}` and `${OPENSSL_INCLUDE_DIR}` | `OpenSSL::SSL` (imported target) |
| `file(GLOB ...)` for sources | Explicit listing |
| Multiple `if(WIN32 OR MSVC)` blocks for flags | Generator expressions |
| `set_property(TARGET ... APPEND PROPERTY INCLUDE_DIRECTORIES ...)` | `target_include_directories(... PUBLIC ...)` |
| `cmake_minimum_required(VERSION 2.8)` | Bump to at least 3.21 |
| Hand-written `Find<Pkg>.cmake` for things now config-mode | Use the upstream `<Pkg>Config.cmake` |

## 63.2 Strategy for Big Migrations

1. **Bump `cmake_minimum_required`** to a modern version (3.21+) as the first commit.
2. **Add an alias target** for every library you ship: `add_library(Foo::core ALIAS foo_core)`. Consumers use the alias; you can swap the underlying target without breaking them.
3. **Per-library**: convert `include_directories` -> `target_include_directories`. Use PUBLIC/PRIVATE deliberately.
4. **Per-library**: convert global flags -> `target_compile_options`/`target_compile_definitions`.
5. **Per-library**: convert plain `target_link_libraries(foo bar)` -> keyword form `target_link_libraries(foo PRIVATE bar)`.
6. **Replace variable-based finds** (`${BOOST_LIBRARIES}`) with imported targets (`Boost::system`).
7. **Remove `file(GLOB)`** in favour of explicit listings (or `CONFIGURE_DEPENDS` if you must).
8. **Add `install(EXPORT)`** if you ship a library.
9. **Add `CMakePresets.json`** as the user-facing entry point.

This sequence can usually be done incrementally without breaking the build.

## 63.3 The "It Worked Before, Now It Doesn't" Diagnostic

When converting, the most common surprise is that an INCLUDE/define is missing in a consumer. The cause is almost always:

- A `target_include_directories(... PRIVATE ...)` that should have been PUBLIC.
- A `target_link_libraries(... PRIVATE ...)` that should have been PUBLIC.
- A header in `include/` that uses a type from a dependency, but the dependency is PRIVATE.

Run the consumer's compile manually with `-v` to see the actual `-I` and `-D` flags, compare against the source-of-truth (your `target_*` calls), and adjust the scope.

---

# Part 15: Best Practices and Interview Questions

---

# 64. Project Layout and Conventions

---

## 64.1 The Recommended Layout

```
my_project/
|-- CMakeLists.txt                         <- top-level project()
|-- CMakePresets.json                      <- user-facing build entry points
|-- README.md
|-- LICENSE
|-- .clang-format
|-- .clang-tidy
|-- .gitignore                             <- includes build/, build-*/
|-- cmake/                                  <- custom modules and helpers
|   |-- Modules/                            <- FindXxx.cmake files
|   |-- CompilerWarnings.cmake
|   |-- Sanitizers.cmake
|   `-- MyProjectConfig.cmake.in            <- exported config template
|-- include/                                <- public headers (installed)
|   `-- my_project/
|       |-- foo.hpp
|       `-- bar.hpp
|-- src/                                    <- library implementation
|   |-- CMakeLists.txt
|   |-- foo.cpp
|   |-- foo_impl.hpp                        <- private headers next to .cpp
|   `-- bar.cpp
|-- apps/                                   <- executables
|   |-- CMakeLists.txt
|   |-- cli/
|   |   |-- CMakeLists.txt
|   |   `-- main.cpp
|   `-- gui/
|       |-- CMakeLists.txt
|       `-- main.cpp
|-- tests/
|   |-- CMakeLists.txt
|   |-- unit/
|   |   |-- foo_test.cpp
|   |   `-- bar_test.cpp
|   `-- integration/
|       `-- end_to_end_test.cpp
|-- benchmarks/
|   |-- CMakeLists.txt
|   `-- foo_bench.cpp
|-- examples/
|   |-- CMakeLists.txt
|   `-- example1.cpp
|-- docs/
|   `-- Doxyfile.in
`-- third_party/                            <- vendored deps (if any)
    `-- somelib/
```

## 64.2 Top-Level CMakeLists.txt Template

```cmake
cmake_minimum_required(VERSION 3.21...3.30)

project(my_project
        VERSION 0.1.0
        DESCRIPTION "A short blurb"
        LANGUAGES CXX)

# Defaults that apply to every target
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Where to put custom CMake modules
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Reusable INTERFACE libraries
include(cmake/CompilerWarnings.cmake)        # adds project_warnings target
include(cmake/Sanitizers.cmake)              # adds project_sanitizers target

# Options
option(MY_PROJECT_BUILD_TESTS      "Build tests"      ${PROJECT_IS_TOP_LEVEL})
option(MY_PROJECT_BUILD_BENCHMARKS "Build benchmarks" OFF)
option(MY_PROJECT_BUILD_EXAMPLES   "Build examples"   ${PROJECT_IS_TOP_LEVEL})
option(MY_PROJECT_BUILD_DOCS       "Build Doxygen documentation" OFF)
option(MY_PROJECT_WARNINGS_AS_ERRORS "Treat warnings as errors" OFF)

# Sane defaults for single-config generators
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
        Debug Release RelWithDebInfo MinSizeRel)
endif()

include(CTest)

add_subdirectory(src)
add_subdirectory(apps)

if(MY_PROJECT_BUILD_TESTS AND BUILD_TESTING)
    add_subdirectory(tests)
endif()

if(MY_PROJECT_BUILD_BENCHMARKS)
    add_subdirectory(benchmarks)
endif()

if(MY_PROJECT_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

if(MY_PROJECT_BUILD_DOCS)
    add_subdirectory(docs)
endif()
```

## 64.3 src/CMakeLists.txt Template (Library)

```cmake
add_library(my_project_core
    foo.cpp
    bar.cpp
    foo_impl.hpp)

add_library(MyProject::core ALIAS my_project_core)

target_include_directories(my_project_core
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR})

target_compile_features(my_project_core PUBLIC cxx_std_20)
target_link_libraries(my_project_core
    PRIVATE
        project_warnings
        project_sanitizers
    PUBLIC
        Threads::Threads)

set_target_properties(my_project_core PROPERTIES
    VERSION   ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR})

# Install
include(GNUInstallDirs)
install(TARGETS my_project_core
    EXPORT  MyProjectTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

install(DIRECTORY ${CMAKE_SOURCE_DIR}/include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
```

## 64.4 Naming Conventions

| Element | Convention |
|---|---|
| CMake target names | `lower_snake_case` (matches file convention) |
| Alias / public names | `Namespace::SubLib` (`MyProject::core`) |
| CMake function names | `lower_snake_case`, prefixed with project name |
| CMake variables | `UPPER_SNAKE_CASE`, prefixed with project name |
| Cache variables (options) | `UPPER_SNAKE_CASE`, prefixed with project name |
| File names | `CamelCase.cmake` for modules, `lower_snake_case.cmake.in` for templates |

The prefix ensures no collision when consumed via `add_subdirectory` or `FetchContent`.

## 64.5 What Belongs in cmake/

| File | Purpose |
|---|---|
| `cmake/Modules/FindXxx.cmake` | Custom Find modules for legacy deps |
| `cmake/CompilerWarnings.cmake` | Defines `project_warnings` INTERFACE target |
| `cmake/Sanitizers.cmake` | Defines `project_sanitizers` INTERFACE target |
| `cmake/MyProjectConfig.cmake.in` | Template for the exported `*Config.cmake` |
| `cmake/StandardProjectSettings.cmake` | Build-type default, ccache, etc. |
| `cmake/Doxygen.cmake` | Doxygen target wiring |

Each should be < 100 lines and do one thing.

---

# 65. Cheatsheet

---

## 65.1 Commands You Will Run Daily

```bash
# Configure
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --preset gcc-release                              # via preset

# Build
cmake --build build --parallel
cmake --build build --target my_lib --parallel
cmake --build build --config Release                    # multi-config only

# Test
ctest --test-dir build --output-on-failure --parallel
ctest --test-dir build -R 'unit::.*'                    # regex filter
ctest --test-dir build -L fast                          # label filter

# Install
cmake --install build --prefix /opt/my_project
DESTDIR=/tmp/staging cmake --install build              # staging

# Package
cd build && cpack -G "TGZ;DEB"

# Clean
cmake --build build --target clean
rm -rf build && cmake -S . -B build ...                 # full reset
cmake --fresh -S . -B build ...                         # 3.24+ equivalent
```

## 65.2 Commands You Use When Things Go Wrong

```bash
cmake --build build -- -d explain                       # Ninja: why is X rebuilding?
ninja -t graph my_target | dot -Tpng > graph.png        # dependency graph
cmake -LH build                                          # list cache + help
cmake -LA build                                          # list cache + advanced
cmake --debug-find -S . -B build                        # why is find_package failing?
cmake --trace --trace-expand -S . -B build              # full trace (verbose!)
cmake --profiling-output=p.json --profiling-format=google-trace ...
ctest --rerun-failed --output-on-failure                # re-run only failures
ctest --repeat until-fail:10 -R flaky_test              # flaky-test hunt
```

## 65.3 The 30 CMake Commands You Will Use Most

| Command | Notes |
|---|---|
| `cmake_minimum_required` | Always first |
| `project` | Sets name, version, languages |
| `add_executable` / `add_library` | Create targets |
| `target_include_directories` | Headers |
| `target_link_libraries` | Linking + transitive deps |
| `target_compile_features` | C++ standard etc. |
| `target_compile_options` | Raw flags |
| `target_compile_definitions` | `-D` |
| `target_sources` | Add files to a target |
| `set_target_properties` | Catch-all property setter |
| `set` | Variables |
| `option` | Boolean cache var |
| `if` / `else` / `endif` | Conditions |
| `foreach` / `endforeach` | Iteration |
| `function` / `endfunction` | Reusable code |
| `find_package` | Locate dependencies |
| `find_program` / `find_library` / `find_path` | Lower-level lookups |
| `include(CTest)` | Tests |
| `add_test` | Register a test |
| `set_tests_properties` | Test labels, timeouts, etc. |
| `enable_testing` | Inside `include(CTest)` |
| `add_subdirectory` | Bring in a sub-project |
| `add_custom_command` | Build-time rule |
| `add_custom_target` | Always-runs pseudo-target |
| `configure_file` | Template substitution |
| `install` | Install rules |
| `include(GNUInstallDirs)` | Use FHS-correct paths |
| `include(CMakePackageConfigHelpers)` | For exporting libraries |
| `FetchContent_Declare` / `FetchContent_MakeAvailable` | Source-level deps |
| `message` | Logging |

## 65.4 Generator-Expression Cheat Sheet

| Genex | Meaning |
|---|---|
| `$<CONFIG>` | Current build config name |
| `$<CONFIG:Debug>` | `1` if Debug |
| `$<$<CONFIG:Debug>:flag>` | `flag` if Debug |
| `$<IF:cond,a,b>` | `a` if cond else `b` |
| `$<CXX_COMPILER_ID:GNU>` | `1` if GCC |
| `$<CXX_COMPILER_ID:GNU,Clang>` | `1` if either |
| `$<PLATFORM_ID:Linux>` | `1` if Linux |
| `$<COMPILE_LANG_AND_ID:CXX,GNU>` | `1` if compiling C++ with GCC |
| `$<TARGET_FILE:foo>` | Absolute path to foo's binary |
| `$<TARGET_FILE_DIR:foo>` | Directory of foo's binary |
| `$<BUILD_INTERFACE:value>` | `value` in build tree |
| `$<INSTALL_INTERFACE:value>` | `value` after install |
| `$<AND:c1,c2>`, `$<OR:c1,c2>`, `$<NOT:c>` | Boolean |

## 65.5 Useful Variables

| Variable | Meaning |
|---|---|
| `CMAKE_SOURCE_DIR` | Top-level source dir |
| `CMAKE_BINARY_DIR` | Top-level build dir |
| `CMAKE_CURRENT_SOURCE_DIR` | This file's source dir |
| `CMAKE_CURRENT_BINARY_DIR` | This file's build dir |
| `PROJECT_NAME` | Closest enclosing `project()` |
| `PROJECT_VERSION`, `_MAJOR`, `_MINOR`, `_PATCH` | Version components |
| `PROJECT_IS_TOP_LEVEL` | True when this `project()` is outermost (3.21+) |
| `CMAKE_BUILD_TYPE` | Single-config generators only |
| `CMAKE_CONFIGURATION_TYPES` | Multi-config generators |
| `CMAKE_CXX_COMPILER_ID` | GNU/Clang/AppleClang/MSVC/Intel/... |
| `CMAKE_SYSTEM_NAME` | Linux/Windows/Darwin/... |
| `CMAKE_SYSTEM_PROCESSOR` | x86_64/aarch64/... |
| `CMAKE_INSTALL_PREFIX` | Install destination |
| `CMAKE_PREFIX_PATH` | Where `find_package` searches |
| `CMAKE_MODULE_PATH` | Where `include()`/`find_package` find modules |

---

# 66. Common Pitfalls

---

## 66.1 The "I Lost an Afternoon To This" List

### Pitfall 1: file(GLOB) for sources

```cmake
file(GLOB SRC src/*.cpp)        # silently fails to detect new files
add_library(foo ${SRC})
```

**Fix:** explicit listing, or `CONFIGURE_DEPENDS` if you must.

### Pitfall 2: Modifying CMAKE_CXX_FLAGS After project()

```cmake
project(foo)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")   # global, leaks to deps
```

**Fix:** `target_compile_options(foo PRIVATE -Wall)`.

### Pitfall 3: Using CMAKE_BUILD_TYPE in if() for Per-Config Logic

```cmake
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    # broken on Visual Studio / Xcode
endif()
```

**Fix:** generator expression `$<$<CONFIG:Debug>:...>`.

### Pitfall 4: Linking Against Variable Instead of Target

```cmake
find_package(OpenSSL REQUIRED)
target_link_libraries(my_app PRIVATE ${OPENSSL_LIBRARIES})   # misses includes/defs
```

**Fix:** `target_link_libraries(my_app PRIVATE OpenSSL::SSL OpenSSL::Crypto)`.

### Pitfall 5: PRIVATE Linking a Library Whose Types Appear in Your Header

```cmake
target_link_libraries(my_lib PRIVATE Boost::system)   # but my_lib.hpp uses boost::system::error_code
```

Consumers of `my_lib` get a header that mentions Boost::system but don't get its include path.

**Fix:** PUBLIC.

### Pitfall 6: Hard-Coded Paths in INSTALL_INTERFACE

```cmake
target_include_directories(my_lib
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)   # works in build, breaks after install
```

**Fix:**

```cmake
target_include_directories(my_lib
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
```

### Pitfall 7: Forgetting include(GNUInstallDirs)

```cmake
install(TARGETS foo LIBRARY DESTINATION lib)   # wrong on Fedora x86_64 (lib64)
```

**Fix:** `install(... DESTINATION ${CMAKE_INSTALL_LIBDIR})` plus `include(GNUInstallDirs)`.

### Pitfall 8: target_link_libraries Without Scope Keyword

```cmake
target_link_libraries(foo bar)                       # legacy plain form
target_link_libraries(foo PRIVATE bar)               # modern keyword form
```

Mixing the two within the same target is an error.

### Pitfall 9: option() After set() of Same Name

```cmake
set(ENABLE_FOO ON)
option(ENABLE_FOO "..." OFF)              # depends on policy CMP0077
```

**Fix:** `cmake_minimum_required(VERSION 3.13)` or higher so `option()` respects existing normal vars.

### Pitfall 10: Quotes in foreach

```cmake
set(items a b c)
foreach(x ${items})         # 3 iterations -- usually OK
foreach(x "${items}")       # 1 iteration with the whole list as one item -- usually wrong
foreach(x IN LISTS items)   # 3 iterations -- correct for any list (including empty/with-semicolons)
```

### Pitfall 11: Configure-Time Variables That Should Be Build-Time

```cmake
configure_file(version.h.in version.h)
# Now bake-in the current git hash at CONFIGURE time -- doesn't refresh on commits
```

**Fix:** `add_custom_command(OUTPUT version.h COMMAND ...)` if you want it to refresh per build.

### Pitfall 12: Inheritance Bug with PARENT_SCOPE

```cmake
function(do_thing)
    set(OUT "result")                  # function-local
endfunction()
do_thing()
message(${OUT})                         # empty!
```

**Fix:** `set(OUT "result" PARENT_SCOPE)` in the function, and pass the output var name as an argument.

### Pitfall 13: macro vs function

```cmake
macro(make_a)
    set(LOCAL "in macro")              # leaks to caller!
endmacro()
make_a()
message(${LOCAL})                       # "in macro"
```

Use `function` unless you specifically need text-substitution.

### Pitfall 14: Cache Variable Type Mismatch

```cmake
option(ENABLE_FOO "..." ON)           # BOOL
# elsewhere:
set(ENABLE_FOO "yes" CACHE STRING "..." FORCE)   # type now STRING
# Now if(ENABLE_FOO) and consumers' BOOL expectations differ
```

**Fix:** keep the type consistent through the whole project.

### Pitfall 15: cmake_minimum_required Inside a Subdirectory

```cmake
# top/CMakeLists.txt
cmake_minimum_required(VERSION 3.21)
add_subdirectory(sub)

# sub/CMakeLists.txt
cmake_minimum_required(VERSION 2.8)   # resets policies!
```

**Fix:** only set it once at the top, or use the range form `VERSION X...Y` everywhere to be explicit.

---

# 67. Interview Questions and Answers

---

## 67.1 Fundamentals

**Q1. What problem does CMake solve, and how is it different from Make?**

CMake is a **meta-build system**: it does not compile or link code; it reads `CMakeLists.txt` files describing the project and generates native build files (Makefiles, Ninja build files, Visual Studio `.vcxproj`, Xcode `.xcodeproj`) that an underlying build tool then executes. Make is a build tool: it consumes a Makefile and runs the commands described.

This means CMake is portable across build environments (the same `CMakeLists.txt` produces a working build on Linux+Make, Windows+VS, macOS+Xcode), and it lets you describe the project in a higher-level, declarative-ish language with concepts like targets, usage requirements, and configurations -- rather than the rule/recipe model of Make.

**Q2. Explain the configure / generate / build / install phases.**

CMake operates in four phases:

1. **Configure** (`cmake -S . -B build`): CMake reads `CMakeLists.txt`, runs the embedded script, probes the toolchain (running small `try_compile` programs to detect compiler features), and builds an in-memory project model.
2. **Generate**: CMake writes the native build files (build.ninja, Makefile, *.vcxproj, etc.) based on the in-memory model.
3. **Build** (`cmake --build build`): the native build tool reads the generated files, compiles sources to objects, links them into binaries.
4. **Install** (`cmake --install build`): the install rules emitted at configure time are executed to copy artifacts into `CMAKE_INSTALL_PREFIX`.

The key idea is that most of the project description (`if`, `foreach`, `find_package`, `set`) runs at configure time. Build-time semantics is expressed via generator expressions and custom commands. Mixing the two up is the most common source of CMake bugs.

**Q3. What are "modern CMake" idioms and how do they differ from legacy?**

Modern CMake (post-3.0, mature post-3.12) is **target-based**. Everything is a target -- executables, libraries, even header-only collections -- and you configure them with `target_*` commands that carry **usage requirements** via PUBLIC / PRIVATE / INTERFACE scope keywords.

Legacy CMake was **directory-based**. You set `include_directories()`, `add_definitions()`, `link_libraries()` at the directory level, which leaked into every target in the directory and its subdirectories. Modern equivalents (`target_include_directories`, `target_compile_definitions`, `target_link_libraries`) are scoped to targets.

The other big shift is **imported targets** instead of variables: `find_package(OpenSSL)` exposes `OpenSSL::SSL` (with its includes, defs, and link libs encoded as the target's `INTERFACE_*` properties) instead of `OPENSSL_LIBRARIES` and `OPENSSL_INCLUDE_DIR` strings.

## 67.2 Targets and Properties

**Q4. Explain PUBLIC, PRIVATE, and INTERFACE in target_link_libraries.**

Targets carry two parallel property sets:

- **Build requirements** -- what the target needs to compile itself.
- **Usage requirements** -- what consumers of the target need to use it.

The scope keyword determines which set the value joins:

- **PRIVATE**: build-only. Adds to the target's own build but not propagated to consumers.
- **INTERFACE**: usage-only. Does **not** affect the target itself; only propagated to consumers.
- **PUBLIC**: both. Affects the target's own build and propagated to consumers.

Example: if `libfoo.hpp` (your public header) `#include <openssl/ssl.h>`, then consumers of libfoo need `-I` for OpenSSL too -- that means `target_link_libraries(libfoo PUBLIC OpenSSL::SSL)`. If `openssl/ssl.h` appears only in `libfoo.cpp`, then `PRIVATE` is right.

The rule of thumb: choose the **smallest scope that is correct**. Over-PUBLIC-ing slows consumer builds and pollutes their symbol space; under-scoping breaks consumer builds.

**Q5. When would you use an INTERFACE library, OBJECT library, or alias target?**

**INTERFACE library**: carries only usage requirements -- no sources, no compiled output. Three uses:

1. Header-only libraries.
2. "Policy" targets like `project_warnings` that bundle a set of compile options for opt-in.
3. Wrapping pre-built things that don't fit `IMPORTED`.

**OBJECT library**: compiles sources into `.o` files without producing an archive or shared lib. Used when:

1. The same compiled objects should be embedded into both a STATIC and a SHARED variant without recompiling.
2. You want a "convenience library" without producing a deliverable.

**Alias target** (`add_library(Foo::core ALIAS foo_core)`): a read-only second name for an existing target. Crucial for making your project consumable identically whether via `add_subdirectory`, `FetchContent`, or `find_package`. Consumers always write `Foo::core`, regardless of which mechanism brought the library in.

**Q6. What is the difference between an IMPORTED target and a regular target?**

A regular target is built from sources by this CMake project. An IMPORTED target represents a pre-built artifact -- a library that already exists on disk. It carries the same `INTERFACE_*` usage requirements as a regular target (include paths, link libs, compile defs), but has `IMPORTED_LOCATION` pointing at the binary instead of being built from sources.

Imported targets are how `find_package(OpenSSL)` exposes `OpenSSL::SSL`: under the hood, CMake creates an IMPORTED library, sets its `IMPORTED_LOCATION` to `/usr/lib/libssl.so`, its `INTERFACE_INCLUDE_DIRECTORIES` to `/usr/include`, and you link against it with the same `target_link_libraries` you'd use for a local target.

## 67.3 Configurations, Generators, Generator Expressions

**Q7. Why doesn't `if(CMAKE_BUILD_TYPE STREQUAL "Debug")` work everywhere?**

Multi-config generators (Visual Studio, Xcode, Ninja-Multi-Config) don't fix the configuration at configure time. They produce build files that contain all four configurations (Debug / Release / RelWithDebInfo / MinSizeRel), and the user picks at build time via `cmake --build build --config Release`. At configure time, `CMAKE_BUILD_TYPE` is empty.

Single-config generators (Ninja, Make) fix the configuration at configure time via `-DCMAKE_BUILD_TYPE=Release`, so `CMAKE_BUILD_TYPE` has a value.

The portable solution is a **generator expression**: `$<$<CONFIG:Debug>:flag>` is evaluated at generate time, when CMake knows the current config -- it works correctly on both single- and multi-config generators.

**Q8. What is a generator expression and when are they evaluated?**

A generator expression is a string of the form `$<...>` that survives configure time as a literal and is **evaluated at generate time** by the native-build-file writer. They are how CMake expresses "the value depends on configuration, target, source file, or generator".

Common forms:

- `$<CONFIG:Debug>` -- 1 if current config is Debug, else 0.
- `$<$<CONFIG:Debug>:value>` -- emit `value` if Debug, else empty.
- `$<IF:c,a,b>` -- emit a or b based on c.
- `$<TARGET_FILE:foo>` -- the absolute path to foo's binary.

They work inside `target_*`, `add_test`, `install`, `add_custom_command`, and `file(GENERATE)` -- contexts that survive to generate time. They do **not** work in regular `set()`, `message()`, `if()`, or `configure_file()`, which are pure configure-time commands.

**Q9. Why use Ninja over Make?**

Ninja was designed explicitly to be the back-end of meta-build systems (CMake, GN, Meson). It's faster than Make on every measurable axis:

- **Full builds**: 1.5-2x faster due to better parallelism (efficient process spawning, no `make -j` straggler problem).
- **No-op (everything up to date) builds**: Ninja often 10-50x faster because it keeps a dependency database and doesn't re-stat the entire tree on every invocation.
- **Header dependency tracking**: first-class in Ninja (`depfile`), more reliable across edge cases than Make's `-MMD` approach.

The only real disadvantage of Ninja is that it's not human-readable -- by design, you don't hand-edit `build.ninja`. But you weren't going to hand-edit `Makefile` either, with a CMake project.

## 67.4 Dependencies

**Q10. find_package: module mode vs config mode -- explain.**

`find_package(Foo)` operates in one of two modes:

- **Module mode**: CMake looks for `FindFoo.cmake` on `CMAKE_MODULE_PATH` or in CMake's bundled `Modules/`. The `FindFoo.cmake` is a detection script (often written by the CMake project itself or shipped with CMake) that probes the system, sets variables like `FOO_INCLUDE_DIR` and `FOO_LIBRARIES`, and ideally creates imported targets.
- **Config mode**: CMake looks for `FooConfig.cmake` (or `foo-config.cmake`) **installed by Foo itself**, typically under `${CMAKE_INSTALL_LIBDIR}/cmake/Foo/`. The config file is written by Foo's authors; it brings in imported targets with all their usage requirements.

`find_package(Foo)` tries module mode first, then config mode. Add `MODULE` or `CONFIG` to force one.

Config mode is the modern standard -- the library owns its own description, transitive deps work automatically (via `find_dependency`), and imported targets are guaranteed. Module mode survives for legacy libraries.

**Q11. When would you use FetchContent versus find_package? Versus ExternalProject?**

- **`find_package`** when the dependency is **installed on the system** or by a package manager (vcpkg, Conan). The dependency exists as artifacts; CMake locates them. Fast incremental builds, but requires the user to have installed the dep.
- **`FetchContent`** when you want a **source-level, self-contained** build. The dependency is downloaded at configure time and added via `add_subdirectory`. Hermetic, reproducible, no external requirements -- at the cost of building the dep yourself.
- **`ExternalProject_Add`** when the dependency is **not a CMake project** (autotools, plain Make, Meson) or needs its own isolated sub-build (e.g., different toolchain). The dep is built at build time, not added to the main project graph; you wrap its outputs in IMPORTED targets manually.

The modern hybrid is `find_package(... CONFIG)` plus `FetchContent` with `OVERRIDE_FIND_PACKAGE`: the consumer can supply a system-installed version if available, and FetchContent picks up the slack otherwise.

**Q12. How does FetchContent handle reproducibility?**

To get reproducible builds, you must pin to a specific commit (a Git tag like `v1.2.3` or a SHA1), not a branch:

```cmake
FetchContent_Declare(fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG        10.2.1)
```

For tarballs, use `URL_HASH SHA256=...` to lock the content:

```cmake
FetchContent_Declare(json
    URL      https://github.com/nlohmann/json/archive/v3.11.3.tar.gz
    URL_HASH SHA256=a22461d13119ac5c78f205d3df1db13403e58ce1bb1794edc9313677313f4a9d)
```

Combined with `GIT_SHALLOW TRUE`, downloads are also faster. Without pinning, your team gets nondeterministic builds when upstream moves.

## 67.5 Installation and Packaging

**Q13. Walk through the steps to make your library consumable via `find_package`.**

Five steps:

1. **Export public usage requirements correctly**:

```cmake
target_include_directories(my_lib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
```

2. **Install the target and add it to an export set**:

```cmake
install(TARGETS my_lib EXPORT MyLibTargets ...)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
```

3. **Generate the targets file**:

```cmake
install(EXPORT MyLibTargets
    NAMESPACE MyLib::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
```

4. **Generate the config and version files**:

```cmake
include(CMakePackageConfigHelpers)
configure_package_config_file(cmake/MyLibConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
write_basic_package_version_file(...)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake ... DESTINATION ...)
```

5. **The template `MyLibConfig.cmake.in`** must call `find_dependency` for transitive deps and include the targets file.

Consumer side:

```cmake
find_package(MyLib 1.0 REQUIRED)
target_link_libraries(my_app PRIVATE MyLib::my_lib)
```

**Q14. Explain BUILD_INTERFACE vs INSTALL_INTERFACE.**

A target's include directories (and other usage requirements) need different values when consumed from inside the build tree versus after installation:

- **`$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>`** -- when the target is consumed via `add_subdirectory` or `FetchContent` (build tree), use the path to the headers in the source tree.
- **`$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>`** -- when the target is consumed via `find_package` (installed), use the install-side path.

Without this split, the installed `FooTargets.cmake` would either embed absolute paths from your build machine (breaking consumers) or have no include path at all (causing compile errors).

**Q15. What does `install(EXPORT ...)` do, and why do we need it?**

`install(EXPORT MyLibTargets)` generates a file (`MyLibTargets.cmake`) at install time that **recreates** the targets you installed as `IMPORTED` targets in the consumer's CMake. Combined with `install(TARGETS my_lib EXPORT MyLibTargets ...)`, every target you added to the export set ends up in the file.

The consumer's `find_package(MyLib)` includes this file (transitively via your `MyLibConfig.cmake`), giving them imported targets `MyLib::my_lib` with the right install-tree paths, the right transitive dependencies, the right compile features, and the right link libraries -- all derived from your in-tree target definition.

This is the mechanism that makes `target_link_libraries(consumer PRIVATE MyLib::my_lib)` "just work" without the consumer needing to know anything about MyLib's internal layout.

## 67.6 Testing and Tooling

**Q16. What does `gtest_discover_tests` do better than `add_test`?**

`add_test(NAME my_test COMMAND my_test)` registers **one** CTest entry that runs the whole `my_test` binary. If the binary has 100 GoogleTest cases, CTest sees a single pass/fail; you cannot filter, parallelise, or report at the case level.

`gtest_discover_tests(my_test)` does the following at **post-build** time:

1. Runs `my_test --gtest_list_tests` to enumerate the cases.
2. Registers each case (`SuiteName.CaseName`) as a separate CTest entry.

Now `ctest -j 8` can parallelise across cases (per binary), `ctest -R 'WidgetTest.*'` filters precisely, and reporting (CDash, JUnit XML, GitHub Actions) is per-case rather than per-binary.

The earlier helper `gtest_add_tests` parsed source code at **configure** time to find cases, which was fragile with macros and parameterised tests. `gtest_discover_tests` is reliable because it asks the runtime binary itself.

**Q17. How do you wire ccache into a CMake build?**

The cleanest way is via the **compiler launcher** variables:

```cmake
find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
    set(CMAKE_C_COMPILER_LAUNCHER   ${CCACHE_PROGRAM})
    set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
endif()
```

This prepends `ccache` to every compile invocation -- across all generators and CMake versions. The older alternative (`CMAKE_CXX_COMPILER=ccache;g++`) is fragile.

For cache hits, ensure compilation is byte-stable: no `__DATE__`/`__TIME__` in code, no absolute paths in flags (use `-fdebug-prefix-map=/abs/path=.`), and set `CCACHE_BASEDIR` to the project root so relative paths are normalised.

**Q18. How do you enable sanitizers cleanly?**

Use an INTERFACE library that targets opt into:

```cmake
add_library(project_sanitizers INTERFACE)

option(ENABLE_ASAN "Enable AddressSanitizer" OFF)
if(ENABLE_ASAN)
    target_compile_options(project_sanitizers INTERFACE
        -fsanitize=address -fno-omit-frame-pointer)
    target_link_options(project_sanitizers INTERFACE
        -fsanitize=address)
endif()

# Internal libs and tests opt in:
target_link_libraries(my_lib   PRIVATE project_sanitizers)
target_link_libraries(my_tests PRIVATE project_sanitizers)
```

The key points:

- Flags must be on **both** compile and link (sanitizer runtime must be linked in).
- Apply to your code but not to vendored / FetchContent deps (false positives can derail CI).
- Some sanitizers are mutually exclusive: ASan and TSan cannot be combined.

Standard CI rig: one job builds with ASan+UBSan, one job with TSan; each runs the entire test suite.

## 67.7 Advanced

**Q19. Why might `target_include_directories(... PUBLIC ...)` create a problem for installed consumers?**

If you write:

```cmake
target_include_directories(my_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
```

The literal path `/home/me/build/proj/include` is baked into your generated `MyLibTargets.cmake` at install time. When a consumer on a different machine does `find_package(MyLib)`, their compile fails because that directory doesn't exist on their machine.

The fix is the BUILD_INTERFACE / INSTALL_INTERFACE genex split:

```cmake
target_include_directories(my_lib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
```

Now the in-tree usage gets the source-tree path; the installed-targets file gets the install-tree path; consumers in both contexts work.

**Q20. Describe the CMake variable scope rules.**

CMake has four scopes:

1. **Function scope**: `function()` creates a new scope. Variables `set()` inside are local. To propagate to the caller, use `set(VAR value PARENT_SCOPE)`.
2. **Directory scope**: each `CMakeLists.txt` has its own scope. Variables set at this level are visible in this directory and all subdirectories (`add_subdirectory`) -- but modifications in a subdirectory don't propagate back unless explicit.
3. **Cache scope**: persistent across CMake runs, stored in `CMakeCache.txt`. Set by `set(... CACHE TYPE "doc")`, `option()`, or `-DVAR=...`. Visible everywhere.
4. **Environment**: not really a CMake scope -- access with `$ENV{VAR}` and `set(ENV{VAR} value)`.

Macros (`macro()`) do **not** create a new scope -- they are text substitution in the caller's scope. This is the main reason to prefer `function()` over `macro()` unless you specifically need the macro's caller-affecting semantics.

**Q21. What is `cmake_minimum_required` actually doing besides version checking?**

It does **two** things:

1. **Version check**: errors if the CMake running this file is older than the minimum.
2. **Policy activation**: sets every CMake policy introduced up to and including that version to its **NEW** behaviour. Older policies stay at NEW; newer ones (introduced after this version, on a newer CMake) stay unset, which produces warnings.

CMake's policy system is how the project author opts into modern behaviour and avoids breakage from CMake's own evolution. Each behavioural change is gated by a numbered policy (`CMP0048`, `CMP0091`, etc.). Old projects (with low `cmake_minimum_required`) see old behaviour; modern projects see modern behaviour.

The range form -- `cmake_minimum_required(VERSION 3.21...3.30)` -- is preferred because it pins policies up to 3.30 regardless of how new CMake gets, protecting you from future policy changes you have not tested against.

**Q22. You inherit a 10-year-old CMake project with `cmake_minimum_required(VERSION 2.6)`, `file(GLOB)` everywhere, and global `include_directories`. How do you modernise it?**

Stepwise, in commits that don't break the build at any point:

1. **Bump the minimum**: `cmake_minimum_required(VERSION 3.21...3.30)`. This activates modern policy defaults.
2. **Per library, introduce a `target_*` block**: replace `include_directories(...)` with `target_include_directories(name PUBLIC ...)`; replace `add_definitions(-DFOO)` with `target_compile_definitions(name PUBLIC FOO)`.
3. **Per library, introduce an alias**: `add_library(MyProj::core ALIAS proj_core)`. Update internal `target_link_libraries` calls to use the alias.
4. **Replace variable-based finds with imported targets**: where `${OPENSSL_LIBRARIES}` appears, switch to `OpenSSL::SSL OpenSSL::Crypto`.
5. **Replace `file(GLOB)` with explicit listings**. This is mechanical but tedious.
6. **Add a `CMakePresets.json`** for user-facing entry points.
7. **Add `install(EXPORT)` and `MyProjConfig.cmake.in`** to make the project consumable by `find_package`.
8. **Add CI jobs** for ASan+UBSan and warnings-as-errors with the new INTERFACE-library "policy targets".

Each step can be reviewed and committed independently, and the build keeps working after every commit.

**Q23. Explain a real-world scenario where you'd use `add_custom_command` with `OUTPUT` versus `TARGET POST_BUILD`.**

**OUTPUT**: when you have a real file that depends on real input files, and that real file is itself an input to a target. Classic case: code generation.

```cmake
add_custom_command(
    OUTPUT  ${CMAKE_CURRENT_BINARY_DIR}/parser.cpp
    COMMAND ${BISON_EXE} -o ${CMAKE_CURRENT_BINARY_DIR}/parser.cpp ${CMAKE_CURRENT_SOURCE_DIR}/parser.y
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/parser.y)

add_library(my_parser ${CMAKE_CURRENT_BINARY_DIR}/parser.cpp)
```

The build system runs Bison only when `parser.y` changes; otherwise the cached `parser.cpp` is reused.

**TARGET POST_BUILD**: when you want a side effect tied to a target's build, not a file dependency. Classic case: copying data files next to an executable.

```cmake
add_custom_command(TARGET my_app POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_SOURCE_DIR}/data/config.json
            $<TARGET_FILE_DIR:my_app>/config.json)
```

Every time `my_app` is linked, the config is refreshed alongside it. There's no "output file as build artifact" in the dependency graph -- it's a build-attached side effect.

**Q24. What's `CMakePresets.json` and why prefer it over a wiki page of `cmake -G ... -DFOO=...` invocations?**

`CMakePresets.json` is a versioned JSON file at the project root that captures **named configurations**: generator, build directory, cache variables, environment, build/test/package settings. Users invoke them with `cmake --preset gcc-release`, `cmake --build --preset gcc-release`, `ctest --preset gcc-release`.

Benefits over wiki/Makefile/script wrappers:

1. **Discoverable**: `cmake --list-presets` shows the catalog.
2. **IDE-native**: VS Code CMake Tools, CLion, and Visual Studio all read presets directly, surfacing them in dropdowns.
3. **Inheritable**: a `base` preset can carry common settings; specific presets override one or two things.
4. **Conditioned**: a preset can be gated on host OS, env vars, or arbitrary booleans -- the preset list adapts to the user's environment.
5. **Workflow presets** (3.25+): chain configure -> build -> test -> package in one command.

Wiki pages drift. `CMakePresets.json` lives next to the code and is updated atomically with the rest of the project.

**Q25. How do you debug "find_package isn't finding the library I just installed"?**

Several debugging tools:

1. `cmake --debug-find -S . -B build` -- CMake logs every directory it searches in `find_package` / `find_library` / `find_path` / `find_program`.
2. Check `CMAKE_PREFIX_PATH` -- is the install prefix on it? Set with `-DCMAKE_PREFIX_PATH=/opt/mylib`.
3. Check `<Pkg>_ROOT` -- per-package override. Set with `-DBoost_ROOT=/opt/boost`.
4. Check for `<Pkg>Config.cmake` at the expected location: `<prefix>/lib/cmake/<Pkg>/`, `<prefix>/lib/cmake/<lowercase>/`, etc. The naming is case-sensitive; modern CMake is more forgiving but old versions weren't.
5. Look at the library's documentation -- some require `CMAKE_PREFIX_PATH`, some require `find_package(... CONFIG REQUIRED)` to skip module mode entirely.
6. If module mode is finding the wrong version, force config mode with `find_package(Foo REQUIRED CONFIG)`.
7. Examine the file: `cat /opt/mylib/lib/cmake/MyLib/MyLibConfig.cmake` -- does it look sane? Are the `find_dependency` calls failing transitively?
8. Try a minimal repro: a fresh project with one `find_package(MyLib REQUIRED)` and a `message(STATUS "Found at ${MyLib_DIR}")` -- isolates the problem from the rest of your project.

---

> End of *CMake Fundamentals* -- comprehensive reference.

> For tighter focus on related topics, see the companion guides:
>
> - [C++ Fundamentals](../languages/Cpp_Fundamentals.md) -- the language this build system is most often used with.
> - [C++ Testing](../languages/CPP_Testing.md) -- GoogleTest, GoogleMock, and the CMake recipes for integrating them. Section 27 of that guide overlaps with this guide's Part 10.
> - [Parallel and GPU Programming](../ml-gpu/Parallel_GPU_Programming.md) -- the CUDA, HIP, OpenMP, and other backends commonly orchestrated through CMake.

