# 🚀 Python Lists: CLI Execution Best Practices & Command Cookbook

This document provides the definitive, production-grade guide to executing,
benchmarking, and automating the
[`src/data_structures/lists.py`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/src/data_structures/lists.py)
module across Windows, macOS, and Linux environments.

---

## 🏛️ 1. Environment Activation: The Two Execution Paradigms

When running production Python CLI tools in this repository, you have **two
primary execution paradigms**:

### Paradigm A: The Idiomatic `uv run` Approach (⭐ Recommended)

The modern, industry-standard approach uses `uv run`. It eliminates manual
virtual environment activation, resolves shell script execution policies, and
automatically ensures dependencies are up to date:

```powershell
# 1. Activate base Micromamba engine (once per terminal session)
micromamba activate python-mastery-sandbox

# 2. Execute any CLI command directly (uv handles the .venv transparently)
uv run src/data_structures/lists.py demo
uv run src/data_structures/lists.py stats --elements 10,20,30,40 --json
```

#### Why `uv run` is the Recommended Best Practice:

- **No PowerShell Execution Policy Blockers**: Bypasses Windows `Restricted`
  script execution policies that often block `.venv\Scripts\Activate.ps1`.
- **Zero Shell State Mutation**: You do not have to remember to `deactivate` or
  switch subshells.
- **Cross-Platform Consistency**: The exact same command runs on Windows
  (PowerShell/CMD), Linux, macOS, and CI/CD pipelines.

---

### Paradigm B: The Interactive Shell Activation Approach

If you prefer activating the virtual environment interactively so that `python`
points directly to the `.venv` interpreter:

#### Windows (PowerShell):

```powershell
# 1. Activate Micromamba
micromamba activate python-mastery-sandbox

# 2. Allow local script execution (if not already enabled)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force

# 3. Activate the project .venv
.\.venv\Scripts\Activate.ps1

# 4. Execute with standard python command
python src/data_structures/lists.py demo
```

#### Windows (Command Prompt `cmd.exe`):

```cmd
micromamba activate python-mastery-sandbox
.venv\Scripts\activate.bat
python src/data_structures/lists.py demo
```

#### Linux / macOS (`bash` / `zsh`):

```bash
micromamba activate python-mastery-sandbox
source .venv/bin/activate
python src/data_structures/lists.py demo
```

---

## 📖 2. Exhaustive CLI Subcommand Cookbook

Every public method in
[`ListOperationsManager`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/src/data_structures/lists.py#L51)
is exposed via dedicated CLI subcommands.

### 2.1 Interactive Showcase Demo

Runs the end-to-end pedagogical showcase demonstrating all 15 core operations:

```bash
uv run src/data_structures/lists.py demo
```

---

### 2.2 List Creation & Mathematical Patterns

Generate lists from raw values, repeated fills, or mathematical sequences
(`range`, `evens`, `squares`, `fibonacci`, `powers_of_two`):

```bash
# Generate first 8 terms of the Fibonacci sequence
uv run src/data_structures/lists.py create --pattern fibonacci --count 8

# Generate powers of two
uv run src/data_structures/lists.py create --pattern powers_of_two --count 6

# Generate repeated fill value
uv run src/data_structures/lists.py create --fill "sandbox" --count 4

# Output structured JSON
uv run src/data_structures/lists.py create --pattern squares --count 5 --json
```

---

### 2.3 Extended Slicing & Striding

Execute Python indexing algebra with optional `start`, `stop`, and `step`
(including negative strides):

```bash
# Slice with start, stop, and step (indices 1 to 5 with step 2)
uv run src/data_structures/lists.py slice --elements 10,20,30,40,50,60 --start 1 --stop 5 --step 2

# Reverse a sequence using negative step (-1)
uv run src/data_structures/lists.py slice --elements 1,2,3,4,5 --step -1

# Slice with JSON output
uv run src/data_structures/lists.py slice --elements alpha,beta,gamma,delta --start 1 --stop 3 --json
```

---

### 2.4 Positional Insertion & Deletion

Insert at arbitrary indices, pop by index, or remove by value (single or all
occurrences):

```bash
# Insert 'beta' at index 1
uv run src/data_structures/lists.py insert --elements alpha,gamma --index 1 --value beta

# Delete element by 0-based index (pop)
uv run src/data_structures/lists.py delete --elements 10,20,30,40 --index 2

# Delete single occurrence of value
uv run src/data_structures/lists.py delete --elements apple,banana,apple,orange --value apple

# Delete ALL occurrences of value
uv run src/data_structures/lists.py delete --elements apple,banana,apple,orange --value apple --all --json
```

---

### 2.5 Element Search & Index Resolution

Search for value indices (first match or all matching positions):

```bash
# Return first index of target
uv run src/data_structures/lists.py search --elements a,b,c,d,b --value b

# Return all indices where target appears
uv run src/data_structures/lists.py search --elements a,b,c,d,b --value b --all --json
```

---

### 2.6 Advanced Timsort Strategies

Sort sequences using natural ordering, string length, numeric magnitude,
absolute value, or case-insensitive:

```bash
# Sort strings by length
uv run src/data_structures/lists.py sort --elements "banana,apple,fig,elderberry,date" --key length

# Sort by absolute numeric magnitude in descending order
uv run src/data_structures/lists.py sort --elements "-10,3,-2,8,1,-15" --key abs --reverse --json

# Case-insensitive alphabetical sorting
uv run src/data_structures/lists.py sort --elements "Banana,apple,Cherry,date" --key lowercase
```

---

### 2.7 Sequence Inversion & Reversal

Demonstrate in-place mutation vs newly allocated reversed sequences:

```bash
# Reversed copy
uv run src/data_structures/lists.py reverse --elements 1,2,3,4,5

# In-place reversal
uv run src/data_structures/lists.py reverse --elements 1,2,3,4,5 --in-place --json
```

---

### 2.8 Comprehension Filtering & Mapping Transformations

Combine predicates (`evens`, `odds`, `positives`, `negatives`, `non_empty`) and
mappings (`square`, `cube`, `abs`, `upper`, `lower`, `stringify`):

```bash
# Filter even numbers and compute their squares
uv run src/data_structures/lists.py filter --elements 1,2,3,4,5,6,7,8 --filter-strategy evens --transform-strategy square

# Filter non-empty strings and convert to uppercase
uv run src/data_structures/lists.py filter --elements "apple,,banana,,cherry" --filter-strategy non_empty --transform-strategy upper --json
```

---

### 2.9 Cyclic Rotation & Batch Chunking

Perform cyclic shifts (+ right, - left) and partition arrays into fixed-size
batches:

```bash
# Rotate list right by 2 positions
uv run src/data_structures/lists.py rotate --elements 1,2,3,4,5 --shift 2

# Rotate list left by 1 position
uv run src/data_structures/lists.py rotate --elements 1,2,3,4,5 --shift -1

# Partition elements into chunks of size 3
uv run src/data_structures/lists.py chunk --elements a,b,c,d,e,f,g,h --chunk-size 3 --json
```

---

### 2.10 Nested List Flattening

Flatten arbitrary nested list structures to a bounded depth or unbounded
recursive depth:

```bash
# Unbounded flattening of deeply nested structure
uv run src/data_structures/lists.py flatten --elements "[[1, 2], [3, [4, [5, 6]]], 7]"

# Flatten with maximum depth limit of 1
uv run src/data_structures/lists.py flatten --elements "[[1, 2], [3, [4, 5]]]" --depth 1 --json
```

---

### 2.11 Deduplication (Order-Preserving vs Set Hashing)

Remove duplicates with $O(N)$ order preservation:

```bash
# Order-preserving deduplication
uv run src/data_structures/lists.py deduplicate --elements 3,1,2,3,2,4,1,5 --preserve-order --json
```

---

### 2.12 Summary Descriptive Statistics

Calculate count, sum, min, max, mean, median, sample variance, and standard
deviation on numeric sequences:

```bash
# Output formatted table
uv run src/data_structures/lists.py stats --elements 12.5,45.0,23.1,89.4,3.2

# Output machine-readable JSON
uv run src/data_structures/lists.py stats --elements 10,20,30,40,50 --json
```

---

### 2.13 Dynamic CPython Memory Growth Analysis

Empirically measure CPython's list capacity reallocation schedule, unused slot
headroom, and byte consumption:

```bash
# Track dynamic reallocations up to 64 appended elements
uv run src/data_structures/lists.py growth --max-elements 64

# JSON export for plotting or data pipelines
uv run src/data_structures/lists.py growth --max-elements 32 --json
```

---

### 2.14 Microsecond Operation Benchmarking

Benchmark performance timings for `append()`, `insert(0)`, `comprehensions`,
`deque.appendleft()`, and `slicing`:

```bash
uv run src/data_structures/lists.py benchmark --size 10000 --iterations 5 --json
```

---

## 🔄 3. Shell Pipelines & Data Integration Recipes

Because every command supports `--json`, you can seamlessly integrate `lists.py`
into CLI data pipelines.

### PowerShell Pipeline Integration

```powershell
# Parse stats output directly into PowerShell objects
$stats = uv run src/data_structures/lists.py stats --elements 10,25,30,45,90 --json | ConvertFrom-Json
Write-Host "Calculated Mean: $($stats.mean)"
Write-Host "Calculated StdDev: $($stats.std_dev)"

# Filter numbers and sort using chained PowerShell commands
$sorted = uv run src/data_structures/lists.py filter --elements 9,4,7,2,8,1,6 --filter-strategy evens --json | ConvertFrom-Json
$sorted.result
```

### Unix / Bash (`jq`) Pipeline Integration

```bash
# Extract only the median from stats calculation
uv run src/data_structures/lists.py stats --elements 10,20,30,40,50 --json | jq '.median'

# Extract memory allocation transitions
uv run src/data_structures/lists.py growth --max-elements 64 --json | jq '.[] | {length, size_bytes, overallocated: .over_allocated_slots}'
```

---

## 🧪 4. Automated Testing & 100% Coverage Verification

Run the test suite verifying all 100 unit tests and ensuring strict 100% line
and branch coverage:

```bash
# Run pytest with missing line coverage reporting
uv run pytest --cov=data_structures.lists --cov-report=term-missing test/data_structures/test_lists.py

# Enforce strict 100% coverage gate (fails build if <100%)
uv run pytest --cov=data_structures.lists --cov-fail-under=100 test/data_structures/test_lists.py
```

---

## 🎯 5. Summary Best Practices Cheat Sheet

| Task                               | Recommended Best Practice Command                                     |
| :--------------------------------- | :-------------------------------------------------------------------- |
| **Run Interactive Showcase**       | `uv run src/data_structures/lists.py demo`                            |
| **Run Any Subcommand**             | `uv run src/data_structures/lists.py <subcommand> [flags]`            |
| **Machine-Readable Output**        | Add `--json` flag to any subcommand                                   |
| **Run Unit Tests (100% Coverage)** | `uv run pytest --cov=data_structures.lists --cov-report=term-missing` |
| **VSCodium 1-Click Task**          | Press `Ctrl+Shift+B` in VSCodium                                      |
| **VSCodium Run & Debug**           | Select `🐍 Python: Lists CLI Demo` and press `F5`                     |
