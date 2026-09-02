# Python Language Mastery Sandbox — Agent Instructions & Architecture

This repository is dedicated to deeply studying and mastering the **Python
Programming Language** through production-grade code, interactive CLI tools,
exhaustive 100% unit test coverage, and university-textbook-quality
instructional documentation.

All agent interactions and implementations in this repository **must** follow
the **3-Part Learning Triad** and the **Domain-Mirrored Layout** detailed below.

---

## 🏛️ Directory Layout Architecture

The repository organizes Python language features across three mirrored pillars:

```text
python-mastery-sandbox/
├── .agents/                              # Agent Skills & Customizations
│   └── skills/
│       └── python-mastery-architecture/
│           └── SKILL.md
├── src/                                  # 1. Production CLI Modules
│   └── <domain>/
│       ├── __init__.py
│       └── <feature_name>.py
├── test/                                 # 2. Comprehensive Test Suites (100% Coverage)
│   └── <domain>/
│       ├── __init__.py
│       └── test_<feature_name>.py
├── doc/
│   ├── environment_setup.md              # Central Environment Documentation
│   ├── python_mastery_blueprint.md       # Master Architecture Blueprint
│   └── notes/                            # 3. University-Textbook Quality Notes
│       └── <domain>/
│           └── <feature_name>.md
├── .python-version
├── AGENTS.md
├── GEMINI.md
├── environment.yml
├── pyproject.toml
└── uv.lock
```

---

## 🗺️ Topic Domain Taxonomy

| Domain Directory          | Scope & Concepts Covered                                                                                             | Examples                                                                              |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `data_structures/`        | Lists, Dictionaries, Tuples & Namedtuples, Sets & Frozensets, Queues & Deques, Heaps, Trees, Custom Sequences        | `lists.py`, `dictionaries.py`, `sets_and_tuples.py`, `custom_collections.py`          |
| `control_flow/`           | Structural Pattern Matching, Generators, Iterators, Context Managers, Advanced Comprehensions, Exception Hierarchies | `pattern_matching.py`, `generators_and_iterators.py`, `context_managers.py`           |
| `functional_programming/` | Closures, Parameterized Decorators, Higher-Order Functions, Lambdas, `itertools`, `functools`, Pure Functions        | `closures_and_decorators.py`, `functools_itertools.py`, `lambdas_and_higher_order.py` |
| `object_oriented/`        | Classes, MRO/C3 Linearization, Dunder Methods, Descriptors, Metaclasses, ABCs, `__slots__` Memory Optimization       | `inheritance_and_mro.py`, `dunder_methods.py`, `descriptors_and_metaclasses.py`       |
| `concurrency_and_async/`  | Asyncio Event Loops, Tasks, Coroutines, Threading & Synchronization Locks, Multiprocessing, IPC Pools, Futures       | `asyncio_fundamentals.py`, `threading_and_locks.py`, `multiprocessing_pools.py`       |
| `metaprogramming/`        | AST Transformation, Bytecode Disassembly (`dis`), Frame Evaluation (`inspect`), Import Hooks, Dynamic Code Execution | `ast_and_bytecode.py`, `inspect_and_frame_eval.py`, `custom_import_hooks.py`          |
| `typing_and_protocols/`   | Generics, TypeVars, Protocols / Structural Subtyping, Overloads, Type Narrowing, Runtime Introspection               | `generics_and_typevars.py`, `structural_protocols.py`, `runtime_type_checkers.py`     |
| `io_and_serialization/`   | Pathlib, Stream I/O, Binary Struct Packing, Buffer Protocol, `memoryview`, SQLite persistence                        | `pathlib_and_streams.py`, `binary_struct_serialization.py`, `buffer_memoryview.py`    |

---

## 🏛️ The 3-Part Learning Triad

For every Python feature or concept under study, create and maintain the
following three artifacts:

### 1. Production CLI Script (`src/<domain>/<feature>.py`)

- **Design**: Clean, idiomatic, PEP 8 / PEP 257 compliant Python code with
  strict type annotations.
- **Exhaustive CLI Interface**: Every single public method **must** be
  accessible via dedicated CLI subcommands and arguments (using `argparse`).
- **Structured Output**: Supports clean formatted terminal output as well as
  structured JSON output via `--json` flags.
- **Executable Demo**: Contains an executable `main()` function running a rich
  demonstration when invoked without arguments or via `demo`.
- **Execution**: Executable directly using
  `uv run src/<domain>/<feature>.py [subcommand] [flags]`.

### 2. Unit Test Suite (`test/<domain>/test_<feature>.py`)

- **Coverage**: **Must achieve 100% code coverage** (line and branch coverage).
- **Test Scope**:
    - Deterministic unit tests for every public method and helper function.
    - Comprehensive boundary checks (empty inputs, single items, out-of-bounds
      indices, extreme values, type validation).
    - Exception and error handling tests (`ValueError`, `TypeError`,
      `IndexError`, `pytest.raises`).
    - Full CLI test coverage exercising every subcommand, flag permutation,
      stdout rendering, JSON formatting, and `main()` invocation.
- **Execution & Verification**:
    - Run test suite: `uv run pytest test/<domain>/test_<feature>.py`
    - Verify 100% coverage:
      `uv run pytest --cov=<domain>.<feature> --cov-report=term-missing test/<domain>/test_<feature>.py`

### 3. Instructional Teaching Document (`doc/notes/<domain>/<feature>.md`)

- **Style & Tone**: University-textbook depth, pedagogical rigor, and structured
  for deep physical/mental intuition.
- **Contents**:
    - **Core Concepts & CPython Internals**: Memory layout (`PyObject`, struct
      pointers), garbage collection, reference counting, and internal allocation
      strategies.
    - **Complexity Analysis**: Formal Big-O time and space complexity table with
      amortization mechanics.
    - **Mathematical & Indexing Algebra**: Formal algebraic models and slice
      mappings.
    - **Visuals & Memory Diagrams**: Clear ASCII or Mermaid diagrams visualizing
      memory pointers and buffers.
    - **Step-by-Step Code & CLI Walkthrough**: Concrete execution traces with
      exact outputs.
    - **Traps, Pitfalls & Anti-Patterns**: Subtle bugs (e.g. mutable default
      arguments, concurrent modification during iteration, shallow copy traps)
      with corrected paradigms.
    - **Summary Reference Table**: Comprehensive cheat-sheet.

---

## 🛠️ Tooling & Project Conventions

- **Central Environment Guide**: Full documentation in
  [`doc/environment_setup.md`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/doc/environment_setup.md).
- **Base Environment**: Micromamba environment (`python-mastery-sandbox`)
  defined in `environment.yml` with Python `>=3.12` / `3.14.7` and `uv`.
- **Project & Package Manager**: `uv` managing virtual environments and
  dependencies locked in `pyproject.toml`.
- **Testing Framework**: `pytest` with `pytest-cov`.
- **Formatting & Linting**: `pnpm run format` (Prettier), `uv run ruff`,
  `uv run mypy`.
