# 🛠️ Central Environment Setup & Verification Guide

This document serves as the canonical reference for provisioning, managing, and
executing the computational environment for the **Python Language Mastery
Sandbox**.

---

## 🏛️ 1. Architecture: The Hybrid Engine Strategy

The project employs a robust **two-tier environment management architecture**:

```
+-------------------------------------------------------------+
|                 Tier 1: Micromamba Engine                   |
|  - Manages isolated CPython interpreter (e.g. 3.14.7 / 3.12)|
|  - Provisions binary dependencies and core tooling (uv)     |
|  - Channel: conda-forge (nodefaults)                        |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                  Tier 2: UV Package Layer                   |
|  - Ultra-fast virtualenv generation (.venv)                 |
|  - Deterministic dependency resolution (pyproject.toml/lock)|
|  - Zero-overhead script & test execution runner             |
+-------------------------------------------------------------+
```

---

## 📋 2. Prerequisites

Ensure you have one of the following package managers installed:

- **`micromamba`** (Recommended) or **`mamba`** / **`conda`**
- **Git** (for version control)

To install `micromamba` if not already installed:

- **Windows (PowerShell)**:
    ```powershell
    Invoke-Expression ((Invoke-WebRequest -Uri https://micro.mamba.pm/install.ps1).Content)
    ```
- **macOS / Linux**:
    ```bash
    "${SHELL}" <(curl -L micro.mamba.pm/install.sh)
    ```

---

## 🚀 3. First-Time Environment Setup

Follow these steps when setting up the repository for the very first time on a
fresh machine.

### Step 3.1: Create & Activate the Base Micromamba Environment

Provision the isolated Python environment with **CPython `3.14.7`** and
**`uv>=0.12.7`**:

#### Option A: Using the `environment.yml` Specification File

```bash
micromamba env create -f environment.yml -y
micromamba activate python-mastery-sandbox
```

#### Option B: Direct CLI Creation (Recommended)

```bash
# Create dedicated sandbox with Python 3.14.7 and uv from conda-forge
micromamba create -n python-mastery-sandbox python=3.14.7 uv>=0.12.7 -c conda-forge --override-channels -y

# Activate the base environment
micromamba activate python-mastery-sandbox
```

> [!NOTE] **Fallback Python Version**: If Python `3.14.7` binary builds are ever
> unavailable for your specific OS architecture, fallback to `python=3.13` or
> `python=3.12`:
>
> ```bash
> micromamba create -n python-mastery-sandbox python=3.12 uv>=0.12.7 -c conda-forge -y
> ```

---

### Step 3.2: Verify Project Python Version Lock (`.python-version`)

`uv` reads
[`.python-version`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/.python-version)
to select its runtime. Ensure it matches your target:

```text
3.14
```

---

### Step 3.3: Synchronize Virtual Environment & Dependencies via UV

Once inside the activated `micromamba` environment, execute `uv sync` to build
the local `.venv` and install all project dependencies from
[`pyproject.toml`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/pyproject.toml):

```bash
# Explicitly sync using the active micromamba Python binary
uv sync --python python
```

> [!TIP] **Understanding UV's Python Version Resolution**: `uv` checks for a
> [`.python-version`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/.python-version)
> file in the workspace root first before checking `PATH`.
>
> - Ensure
>   [`.python-version`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/.python-version)
>   is set to `3.14` (matching your micromamba target).
> - Passing `--python python` explicitly instructs `uv` to use the active
>   micromamba Python executable on `PATH`.
> - Alternatively, set `$env:UV_PYTHON_PREFERENCE="only-system"` (PowerShell) or
>   `export UV_PYTHON_PREFERENCE="only-system"` (Bash) to prevent `uv` from
>   downloading standalone toolchains.

---

### Step 3.4: Quick Health & Verification Check

```bash
# 1. Check Python version reported by UV virtual environment
uv run python --version

# 2. Run unit tests with 100% coverage
uv run pytest --cov=data_structures.lists --cov-report=term-missing test/data_structures/test_lists.py

# 3. Run interactive showcase demo
uv run src/data_structures/lists.py demo
```

---

## 🔄 4. Starting Over from Scratch (Nuclear Reset & Teardown)

When you need to completely purge the environment, resolve corrupt state, clean
disk space, or start fresh with a different Python version (e.g., switching
between Python `3.12`, `3.13`, and `3.14.7`), follow this 3-phase reset runbook:

### Phase 4.1: Complete Teardown & Cache Purge

```bash
# 1. Deactivate active environment
micromamba deactivate

# 2. Remove the existing micromamba environment
micromamba remove -n python-mastery-sandbox --all -y
```

#### Delete Local `.venv` and Cache Directories:

- **Windows (PowerShell)**:
    ```powershell
    Remove-Item -Recurse -Force .venv, .pytest_cache, .coverage, .ruff_cache, .mypy_cache, htmlcov -ErrorAction SilentlyContinue
    ```
- **macOS / Linux (Bash/Zsh)**:
    ```bash
    rm -rf .venv .pytest_cache .coverage .ruff_cache .mypy_cache htmlcov
    ```

#### Clean Package Manager Caches:

```bash
# Purge uv package and wheel caches
uv cache clean

# (Optional) Clean micromamba package tarballs and unused packages
micromamba clean --all -y
```

---

### Phase 4.2: Clean Re-Provisioning

```bash
# 1. Recreate the base micromamba environment
# Option A: From environment.yml
micromamba env create -f environment.yml -y

# Option B: Direct CLI with target Python version (e.g. 3.14.7)
micromamba create -n python-mastery-sandbox python=3.14.7 uv>=0.12.7 -c conda-forge --override-channels -y

# 2. Activate the fresh environment
micromamba activate python-mastery-sandbox

# 3. Ensure .python-version file is configured
# (Contains '3.14')

# 4. Synchronize virtualenv and locked dependencies with uv
uv sync --python python
```

---

### Phase 4.3: Environment Sanity Verification

```bash
# 1. Verify runtime interpreter and tool versions
python --version
uv --version

# 2. Run full test suite with coverage enforcement
uv run pytest --cov=data_structures.lists --cov-report=term-missing test/data_structures/test_lists.py

# 3. Execute the interactive production CLI showcase
uv run src/data_structures/lists.py demo
```

---

## 🧪 5. Running Unit Tests & Enforcing 100% Coverage

All modules in this repository require **100% line and branch test coverage**.

### Run the Full Test Suite

```bash
uv run pytest
```

### Run a Single Domain / Module Test with Coverage Breakdown

```bash
uv run pytest --cov=data_structures.lists --cov-report=term-missing test/data_structures/test_lists.py
```

### Strict 100% Coverage Gate (CI / Pre-commit Rule)

```bash
uv run pytest --cov=data_structures.lists --cov-fail-under=100 test/data_structures/test_lists.py
```

---

## 💻 6. Executing Production CLI Scripts

Every module in `src/<domain>/<feature>.py` is a fully standalone production CLI
tool with dedicated CLI subcommands and arguments for **every public method**.

### View Global Help & Subcommands

```bash
uv run src/data_structures/lists.py --help
```

### Execute Interactive Showcase Demo

```bash
uv run src/data_structures/lists.py demo
```

### Execute Granular Operations via CLI Subcommands

```bash
# 1. Slicing with custom start, stop, and step
uv run src/data_structures/lists.py slice --elements 10,20,30,40,50,60 --start 1 --stop 5 --step 2

# 2. Positional insertion
uv run src/data_structures/lists.py insert --elements alpha,gamma --index 1 --value beta

# 3. Timsort with custom key strategy
uv run src/data_structures/lists.py sort --elements "banana,apple,fig,dragonfruit" --key length --reverse

# 4. Filter and transform (comprehensions)
uv run src/data_structures/lists.py filter --elements 1,2,3,4,5,6,7,8,9,10 --filter evens --transform square

# 5. Cyclic Rotation
uv run src/data_structures/lists.py rotate --elements 1,2,3,4,5 --shift 2

# 6. Chunking into fixed-size batches
uv run src/data_structures/lists.py chunk --elements a,b,c,d,e,f,g --chunk-size 3

# 7. Memory growth empirical analysis
uv run src/data_structures/lists.py growth --max-elements 64

# 8. Summary statistics
uv run src/data_structures/lists.py stats --elements 12.5,45.0,23.1,89.4,3.2
```

---

## 🎨 7. Code Formatting, Type Checking & Linting

### Prettier (JSON and Markdown Formatting)

```bash
# Check formatting
pnpm run format:check

# Auto-format all markdown and json files
pnpm run format
```

### Static Type Checking (`mypy`)

```bash
uv run mypy src/
```

### Fast Linting & Auto-fix (`ruff`)

```bash
uv run ruff check src/ test/ --fix
```

---

## 🖥️ 8. VSCodium & VS Code IDE Setup & Integration

The repository includes pre-configured workspace settings, launch profiles, and
task runners in the
[`.vscode/`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/.vscode)
directory.

### 8.1 Installing Required Extensions in VSCodium

Unlike Microsoft VS Code, **VSCodium** uses the open-source **Open VSX
Registry** (`open-vsx.org`). Ensure the Python language and debugger extensions
are installed:

#### Option A: Via Command Line (Recommended)

```powershell
# Windows PowerShell
& "C:\Program Files\VSCodium\bin\codium.cmd" --install-extension ms-python.python
& "C:\Program Files\VSCodium\bin\codium.cmd" --install-extension ms-python.debugpy
& "C:\Program Files\VSCodium\bin\codium.cmd" --install-extension charliermarsh.ruff
```

```bash
# macOS / Linux
codium --install-extension ms-python.python
codium --install-extension ms-python.debugpy
codium --install-extension charliermarsh.ruff
```

#### Option B: Via VSCodium GUI

1. Open the Extensions sidebar (`Ctrl+Shift+X`).
2. Search for `Python` (`ms-python.python`) and click **Install**.
3. Search for `Python Debugger` (`ms-python.debugpy`) and click **Install**.

---

### 8.2 Launch Configurations & Debugging (`F5` / `Ctrl+Shift+D`)

Configured in
[`.vscode/launch.json`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/.vscode/launch.json):

1. **`🐍 Python: Lists CLI Demo`**: Runs the full interactive showcase
   (`lists.py demo`).
2. **`⚙️ Python: Lists CLI (Prompt for Subcommand & Args)`**: Opens an
   interactive input box in VSCodium prompting for subcommands (e.g.,
   `sort --elements banana,apple,fig --key length`).
3. **`📄 Python: Run/Debug Current File`**: Runs the currently active file in
   the editor.
4. **`🧪 Python: Debug Pytest (Current Test File)`**: Runs the active test suite
   under the debugger.
5. **`📊 Python: Pytest Full Suite with 100% Coverage`**: Runs the full test
   suite with coverage verification.

---

### 8.3 Extension-Free Execution via Tasks (`Ctrl+Shift+B`)

If you want to run scripts without configuring any debug extensions, VSCodium
tasks execute shell commands directly via `uv run` in the built-in terminal:

- **Quick Build / Run Demo**: Press **`Ctrl+Shift+B`** (runs
  `uv run src/data_structures/lists.py demo`).
- **Run Tasks Menu**: Press **`Ctrl+Shift+P`** $\rightarrow$ select
  **`Tasks: Run Task`**:
    - `🐍 Run Lists CLI Demo`
    - `⚙️ Run Lists CLI Subcommand (Custom Args)`
    - `🧪 Run Pytest with 100% Coverage`
    - `📦 UV: Sync Dependencies (.venv)`
    - `✨ Format Code & Docs (Prettier)`
    - `🔍 Lint Code (Ruff)`
    - `🛡️ Static Type Check (Mypy)`

---

## 📂 9. Repository Layout Reference

```text
python-mastery-sandbox/
├── .agents/                              # Agent Skills & Architecture Rules
│   └── skills/
│       └── python-mastery-architecture/
│           └── SKILL.md
├── .vscode/                              # VSCodium / VS Code IDE Workspace Config
│   ├── extensions.json                   # Recommended Open VSX Extensions
│   ├── launch.json                       # 1-Click Run & Debug Launch Targets
│   ├── settings.json                     # Interpreter Path & Pytest Settings
│   └── tasks.json                        # Shell Tasks & Build Shortcuts
├── src/                                  # Production Modules & CLI Entrypoints
│   └── <domain>/
│       ├── __init__.py
│       └── <feature_name>.py
├── test/                                 # 100% Coverage Pytest Test Suites
│   └── <domain>/
│       ├── __init__.py
│       └── test_<feature_name>.py
├── doc/
│   ├── environment_setup.md              # Central Environment & Setup Blueprint
│   ├── python_mastery_blueprint.md       # Architectural Standard & Guidelines
│   └── notes/                            # University-Level Pedagogical Chapters
│       └── <domain>/
│           └── <feature_name>.md
├── .python-version
├── AGENTS.md
├── GEMINI.md
├── environment.yml
├── pyproject.toml
└── uv.lock
```
