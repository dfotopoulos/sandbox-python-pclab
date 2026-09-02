---
name: python-mastery-architecture
description: >-
    Standard directory layout, Python Language Mastery domain taxonomy, 3-part
    learning triad, CLI interface standards, and test execution runbook for the
    Python Language Mastery Sandbox project.
---

# Python Language Mastery Architecture

This skill defines the repository structure, Python domain taxonomy, 3-part
learning triad, and development conventions for the `python-mastery-sandbox`
project.

## 3-Pillar Layout Architecture

Every Python language concept is developed across three mirrored pillars:

1. **Production CLI Script (`src/<domain>/<feature>.py`)**:
    - PEP 8 and PEP 257 compliant Python code with complete type annotations.
    - Comprehensive docstrings explaining computational algorithms and internal
      mechanics.
    - Dedicated CLI subcommands and arguments for **every public method**.
    - Built-in interactive demonstration when run with `demo` or without
      arguments.

2. **Unit Test Suite (`test/<domain>/test_<feature>.py`)**:
    - Pytest suite requiring **100% line and branch code coverage**.
    - Tests all algorithm paths, boundary conditions, edge cases, exceptions,
      and every CLI subcommand and flag.

3. **Instructional Teaching Guide (`doc/notes/<domain>/<feature>.md`)**:
    - University-textbook style guide covering CPython internals, memory layout,
      Big-O complexity, algebra, diagrams, CLI walkthroughs, and pitfalls.

---

## Domain Taxonomy

- `data_structures/`: Lists, Dictionaries, Tuples, Sets, Deques, Heaps, Trees.
- `control_flow/`: Structural Pattern Matching, Generators, Iterators, Context
  Managers, Comprehensions.
- `functional_programming/`: Closures, Decorators, Higher-Order Functions,
  Lambdas, `itertools`, `functools`.
- `object_oriented/`: Classes, MRO, Dunder Methods, Descriptors, Metaclasses,
  ABCs, `__slots__`.
- `concurrency_and_async/`: Asyncio, Coroutines, Threading, Multiprocessing,
  Futures.
- `metaprogramming/`: AST, Bytecode (`dis`), Frame Evaluation (`inspect`),
  Import Hooks.
- `typing_and_protocols/`: Generics, Protocols, Overloads, Type Narrowing.
- `io_and_serialization/`: Pathlib, Streams, Struct, Buffer Protocol,
  `memoryview`, SQLite.

---

## Verification & Execution Runbook

- **Environment Setup Guide**: See `doc/environment_setup.md`
- **Run Module Demo**: `uv run src/<domain>/<feature>.py demo`
- **Run Subcommand**: `uv run src/<domain>/<feature>.py <command> [flags]`
- **Run Unit Tests with 100% Coverage**:
  `uv run pytest --cov=<domain>.<feature> --cov-report=term-missing test/<domain>/test_<feature>.py`
- **Run All Tests**: `uv run pytest`
