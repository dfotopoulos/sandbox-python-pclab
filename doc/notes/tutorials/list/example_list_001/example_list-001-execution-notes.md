# 🚀 Execution Notes & Laboratory Manual: `example_list_001.py`

This document provides complete instructions for executing, testing, and
experimenting with
[`src/tutorial/list/example_list_001/example_list_001.py`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/src/tutorial/list/example_list_001/example_list_001.py).

---

## 🏛️ 1. Environment Setup & Execution Modes

### Mode A: Idiomatic Modern Execution with `uv run` (⭐ Recommended)

No manual virtual environment activation required. `uv` automatically executes
the script within the managed `.venv`:

```powershell
# 1. Activate micromamba base environment (once per shell session)
micromamba activate python-mastery-sandbox

# 2. Execute directly with uv
uv run src/tutorial/list/example_list_001/example_list_001.py --help
```

### Mode B: Direct Python Execution with Activated Environment

```powershell
# Windows PowerShell
micromamba activate python-mastery-sandbox
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
.\.venv\Scripts\Activate.ps1

python src/tutorial/list/example_list_001/example_list_001.py --help
```

---

## 📋 2. CLI Switches & Arguments Reference Table

| CLI Switch     | Argument Format | Type        | Description                                                |
| :------------- | :-------------- | :---------- | :--------------------------------------------------------- |
| `-h`, `--help` | None            | Flag        | Display help message and exit                              |
| `--data`       | `[ELEM ...]`    | String List | Space-separated list elements (e.g. `--data a b c`)        |
| `--add`        | `ITEM`          | String      | Append an item to the end of the list                      |
| `--remove`     | `ITEM`          | String      | Remove the first occurrence of item (safe no-op if absent) |
| `--sort`       | None            | Flag        | Sort list elements in ascending lexicographical order      |
| `--reverse`    | None            | Flag        | Invert the order of the list elements                      |
| `--pop`        | None            | Flag        | Pop and display the last element (returns `None` on empty) |
| `--clear`      | None            | Flag        | Remove all elements and return an empty list               |

---

## 🧪 3. Exhaustive Execution Recipes & Expected Outputs

### 3.1 Inspecting & Initializing Data

#### Recipe 1: Default Empty Initialization (No Arguments)

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py
```

**Output:**

```text
Current List: []
```

#### Recipe 2: Initializing with Elements

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data apple banana cherry
```

**Output:**

```text
Current List: ['apple', 'banana', 'cherry']
```

---

### 3.2 Appending Elements (`--add`)

#### Recipe 3: Add an Element to an Existing List

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data apple banana --add cherry
```

**Output:**

```text
Result: ['apple', 'banana', 'cherry']
```

#### Recipe 4: Add an Element to an Initially Empty List

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --add first_item
```

**Output:**

```text
Result: ['first_item']
```

---

### 3.3 Removing Elements (`--remove`)

#### Recipe 5: Remove an Existing Element

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data alpha beta gamma --remove beta
```

**Output:**

```text
Result: ['alpha', 'gamma']
```

#### Recipe 6: Attempt Removal of Non-Existent Element (Safe No-Op)

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data alpha beta gamma --remove delta
```

**Output:**

```text
Result: ['alpha', 'beta', 'gamma']
```

---

### 3.4 Sorting Elements (`--sort`)

#### Recipe 7: Lexicographical Alphabetical Sort

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data delta alpha charlie beta --sort
```

**Output:**

```text
Result: ['alpha', 'beta', 'charlie', 'delta']
```

#### Recipe 8: Lexicographical vs Numerical String Sorting Observation

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data 10 2 100 25 3 --sort
```

**Output:**

```text
Result: ['10', '100', '2', '25', '3']
```

_(Note: Because CLI inputs are treated as strings, `'10'` comes before `'2'`
lexicographically)._

---

### 3.5 Inverting Sequence Order (`--reverse`)

#### Recipe 9: Reverse Elements In-Place

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data 1 2 3 4 5 --reverse
```

**Output:**

```text
Result: ['5', '4', '3', '2', '1']
```

---

### 3.6 LIFO Tail Popping (`--pop`)

#### Recipe 10: Pop from Populated List

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data task1 task2 task3 --pop
```

**Output:**

```text
Popped: task3, Remaining: ['task1', 'task2']
```

#### Recipe 11: Pop from Empty List (Boundary Safety)

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --pop
```

**Output:**

```text
Popped: None, Remaining: []
```

---

### 3.7 Clearing List (`--clear`)

#### Recipe 12: Clear Memory Buffer

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data a b c d e --clear
```

**Output:**

```text
Result: []
```

---

## ⚖️ 4. Evaluation Precedence & Flag Priority

When multiple operation flags are passed in a single command, the CLI evaluates
them based on the `if-elif-else` ladder in `main()`:

$$\text{Priority}: \text{--add} > \text{--remove} > \text{--sort} > \text{--reverse} > \text{--pop} > \text{--clear} > \text{Default View}$$

#### Laboratory Experiment: Passing `--add` and `--sort` Simultaneously

```bash
uv run src/tutorial/list/example_list_001/example_list_001.py --data z a --add m --sort
```

**Output:**

```text
Result: ['z', 'a', 'm']
```

_(Explanation: `--add` has higher precedence in the `if-elif-else` chain, so
`--add` is executed and `--sort` is ignored)._

---

## 💻 5. VSCodium / VS Code Debugging Integration

To run or debug `example_list_001.py` directly in **VSCodium**:

1. Open `src/tutorial/list/example_list_001/example_list_001.py` in the editor.
2. Select **`📄 Python: Run/Debug Current File`** from the Run & Debug dropdown
   (`Ctrl+Shift+D`).
3. Press **`F5`**.
4. Or run directly in the VSCodium terminal with
   `uv run src/tutorial/list/example_list_001/example_list_001.py --data a b c --sort`.
