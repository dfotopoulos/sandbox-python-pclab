# 🚀 Project Blueprint: Python Language Mastery Sandbox (`python-mastery-sandbox`)

This document defines the architecture, configuration, domain taxonomy, tooling,
and development standards for the **Python Language Mastery Sandbox**.

---

## 🏛️ 1. High-Level Architecture: The 3-Part Learning Triad

For every Python language concept, data structure, or system feature under
study, the repository enforces the **3-Part Learning Triad** across a
**Domain-Mirrored Layout**:

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

## 🗺️ 2. Domain Taxonomy for Python Language Mastery

| Domain Directory          | Scope & Conceptual Coverage                                                                                             | Examples                                                                              |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `data_structures/`        | Built-in & standard collections: Lists, Dicts, Tuples, Sets, Deques, Heaps, Trees, Custom Sequences                     | `lists.py`, `dictionaries.py`, `sets_and_tuples.py`, `custom_collections.py`          |
| `control_flow/`           | Flow mechanisms: Structural Pattern Matching, Generators, Iterators, Context Managers, Advanced Comprehensions          | `pattern_matching.py`, `generators_and_iterators.py`, `context_managers.py`           |
| `functional_programming/` | Functional paradigms: Closures, Parameterized Decorators, Higher-Order Functions, Lambdas, `itertools`, `functools`     | `closures_and_decorators.py`, `functools_itertools.py`, `lambdas_and_higher_order.py` |
| `object_oriented/`        | OOP internals: Classes, MRO/C3 Linearization, Dunder Methods, Descriptors, Metaclasses, ABCs, `__slots__` Memory Tuning | `inheritance_and_mro.py`, `dunder_methods.py`, `descriptors_and_metaclasses.py`       |
| `concurrency_and_async/`  | Concurrency paradigms: Asyncio Event Loops, Tasks, Coroutines, Threading & Synchronization, Multiprocessing, IPC Pools  | `asyncio_fundamentals.py`, `threading_and_locks.py`, `multiprocessing_pools.py`       |
| `metaprogramming/`        | Runtime dynamism & internals: AST Transformation, Bytecode (`dis`), Frame Evaluation (`inspect`), Import Hooks, `eval`  | `ast_and_bytecode.py`, `inspect_and_frame_eval.py`, `custom_import_hooks.py`          |
| `typing_and_protocols/`   | Type system: Generics, TypeVars, Protocols / Structural Subtyping, Overloads, Type Narrowing, Runtime Introspection     | `generics_and_typevars.py`, `structural_protocols.py`, `runtime_type_checkers.py`     |
| `io_and_serialization/`   | I/O & data persistence: Pathlib, Streams, Binary Struct Packing, Buffer Protocol, `memoryview`, SQLite persistence      | `pathlib_and_streams.py`, `binary_struct_serialization.py`, `buffer_memoryview.py`    |

---

## 🏛️ 3. The 3-Part Learning Triad Standard

### Pillar 1: Production CLI Script (`src/<domain>/<feature>.py`)

- **Type Annotations**: Strict PEP 484/585/604 annotations across all functions
  and classes.
- **Deep Algorithmic Implementation**: Clean, performant, idiomatic
  implementation of core mechanics and edge cases.
- **CLI Exposing All Public Methods**: Full `argparse` integration where **every
  single public method has dedicated CLI arguments / subcommands**.
- **Self-Contained Demo**: Includes a rich terminal demo mode when run without
  arguments or with `demo`.

### Pillar 2: Unit Test Suite (`test/<domain>/test_<feature>.py`)

- **100% Coverage Policy**: Line and branch coverage must strictly achieve
  **100%**.
- **Testing Scope**:
    - Analytical benchmark assertions.
    - Comprehensive boundary checks (empty inputs, single items, out-of-bounds
      indices, extreme values).
    - Robust exception validations (`pytest.raises`).
    - Full CLI test coverage: tests all subcommands, flag variations, stdout
      formats (text & JSON), error flags, and `main()`.

### Pillar 3: University-Level Pedagogical Guide (`doc/notes/<domain>/<feature>.md`)

- **CPython Internal Mechanics**: Memory layout (e.g. `PyListObject`,
  `ob_item`), pointer arrays, and growth algorithms.
- **Asymptotic Complexity Table**: Rigorous Big-O time and space analysis for
  every operation.
- **Mathematical Formulations & Visual Diagrams**: Indexing algebra,
  ASCII/Mermaid memory charts.
- **Step-by-Step Numerical Walkthrough**: Exact inputs, state transitions, and
  outputs.
- **Traps, Pitfalls & Anti-Patterns**: Subtle gotchas, mutable defaults,
  iterator invalidation, and recommended idioms.
- **Summary Reference Table**: Comprehensive cheat-sheet.

---

## 🛠️ 4. Quick Execution Runbook

```bash
# Sync dependencies
uv sync

# Run module demo
uv run src/data_structures/lists.py demo

# Run module with specific CLI arguments
uv run src/data_structures/lists.py sort --elements "pear,kiwi,apple,banana" --key length

# Run tests and verify 100% coverage
uv run pytest --cov=data_structures.lists --cov-report=term-missing test/data_structures/test_lists.py

# Format documentation and configs
pnpm run format
```
