# 🖥️ VSCodium: Complete Execution & Debugging Guide

This guide provides a comprehensive manual on how to execute Python scripts, CLI
tools, and test suites in **VSCodium / VS Code**, contrasting **Interactive
Debugging (Debug Mode)** with **Task & Direct Execution (No Debug Mode)**.

---

## ⚖️ 1. Execution Modalities: Debug Mode vs. No Debug Mode

In VSCodium, you have two complementary execution workflows configured in the
[`.vscode/`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/.vscode)
directory:

```
                            ┌────────────────────────────────────────────────────────┐
                            │                    VSCodium Workspace                  │
                            └──────────────────────────┬─────────────────────────────┘
                                                       │
                           ┌───────────────────────────┴───────────────────────────┐
                           ▼                                                       ▼
        ┌──────────────────────────────────────┐                ┌──────────────────────────────────────-┐
        │   🐞 DEBUG MODE (launch.json)        │                │   ⚡ NO DEBUG MODE (tasks.json / CLI) │
        ├──────────────────────────────────────┤                ├──────────────────────────────────────-┤
        │ • Attaches Python debug adapter      │                │ • Zero debugger overhead              │
        │ • Pauses execution on breakpoints    │                │ • Executes shell commands directly    │
        │ • Inspects live variables & callstack│                │ • High-speed execution                │
        │ • Step-by-step execution (F10 / F11) │                │ • Ideal for tests, formatting, builds │
        │ • Trigger: F5 / Ctrl+Shift+D         │                │ • Trigger: Ctrl+Shift+B / Run Task    │
        └──────────────────────────────────────┘                └──────────────────────────────────────-┘
```

### Summary Comparison Table

| Dimension            | 🐞 Debug Mode (`launch.json`)                       | ⚡ No Debug Mode (`tasks.json` / Terminal)              |
| :------------------- | :-------------------------------------------------- | :------------------------------------------------------ |
| **Primary Goal**     | Deep investigation, bug fixing, variable inspection | Running scripts, automated testing, formatting          |
| **Debug Engine**     | Starts `debugpy` adapter                            | Pure shell process (`pwsh` / `bash` via `uv run`)       |
| **Breakpoints**      | ✅ **Active** (Pauses execution at red dots)        | ❌ **Ignored** (Executes straight through)              |
| **Variable Watch**   | ✅ Live Memory & Variable Inspector panels          | ❌ Standard terminal stdout/stderr only                 |
| **Step-Through**     | ✅ Step Over (`F10`), Step Into (`F11`)             | ❌ Runs uninterrupted from start to finish              |
| **Startup Latency**  | ~300ms (Debugger initialization)                    | Instant (0ms overhead)                                  |
| **Primary Shortcut** | **`F5`** or `Ctrl+Shift+D`                          | **`Ctrl+Shift+B`** or `Ctrl+Shift+P -> Tasks: Run Task` |

---

## 🐞 Part 1: How to Run with Full Debugging (Debug Mode)

Debug mode connects VSCodium to Python's debugging engine (`debugpy`), giving
you complete control over line-by-line code execution and memory inspection.

### 1.1 Setting Breakpoints

1. Open any Python file (e.g.
   [`src/tutorial/list/example_list_001/example_list_001.py`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/src/tutorial/list/example_list_001/example_list_001.py)).
2. Click in the margin to the left of any line number (or press **`F9`** on that
   line).
3. A **solid red dot (🔴)** will appear, marking the breakpoint.

```python
45:     manager = ListManager(args.data)
46: 🔴  if args.add is not None:           # <-- Execution will pause here
47:         print(f"Result: {manager.add(args.add)}")
```

---

### 1.2 Launching the Debugger (`F5`)

1. Open the **Run & Debug Sidebar** by pressing **`Ctrl+Shift+D`** (or clicking
   the Play/Bug icon in the left activity bar).
2. Click the dropdown menu at the top of the sidebar and select a target:
    - **`🎓 Example List 001 (Interactive Input Prompt)`**: Prompts for custom
      arguments before debugging.
    - **`🎓 Example List 001 (Sort Nick, Filippos, Dimitra)`**: 1-click debug
      with pre-set arguments.
    - **`🐍 Lists CLI Demo (Showcase)`**: Debugs the production lists showcase.
    - **`🧪 Pytest: Test Example List 001`**: Debugs the unit test suite.
3. Press **`F5`** (or click the green **Play ▶️** button).
4. If an input prompt appears at the top of the screen:
    - Type your arguments (or press **`Enter`** to accept the default
      `--data Nick Filippos Dimitra --sort`).

---

### 1.3 Navigating the Debug Toolbar

When execution hits a breakpoint, the line highlights in yellow and the floating
Debug Toolbar appears:

```
┌─────────────────────────────────────────────────────────────┐
│   ▶️ Continue   ↷ Step Over   ⬇️ Step Into   ⬆️ Step Out   🔄 Restart   ⏹️ Stop   │
│      (F5)          (F10)         (F11)       (Shift+F11) (Ctrl+Shift+F5) (Shift+F5)│
└─────────────────────────────────────────────────────────────┘
```

- **▶️ Continue (`F5`)**: Resume execution until the next breakpoint or program
  completion.
- **↷ Step Over (`F10`)**: Execute the current line and advance to the next line
  in the current function.
- **⬇️ Step Into (`F11`)**: Step inside the function called on the current line
  (e.g. step into `ListManager.sort()`).
- **⬆️ Step Out (`Shift+F11`)**: Finish executing the current function and
  return to the caller.
- **🔄 Restart (`Ctrl+Shift+F5`)**: Rerun the debug session from the beginning.
- **⏹️ Stop (`Shift+F5`)**: Immediately terminate the debug session.

---

### 1.4 Inspecting State & Memory During Debugging

While paused on a breakpoint, look at the panels in the left sidebar:

1. **Variables Panel**:
    - **Locals**: Shows all local variables (e.g. `args`, `manager`,
      `self.data`).
    - **Globals**: Shows module-level constants and imported packages.
2. **Watch Panel**:
    - Click **`+`** to evaluate custom expressions dynamically (e.g.
      `len(manager.data)` or `type(args)`).
3. **Call Stack Panel**:
    - Shows the active stack frames from `main()` down to the current method.
4. **Debug Console Tab** (`Ctrl+Shift+Y`):
    - An interactive Python REPL connected to the live paused execution state.
      You can type any Python statement (e.g. `manager.data.append("extra")`) to
      test behavior on the fly.

---

## ⚡ Part 2: How to Run with No Debug (Task & Direct Execution)

No Debug mode executes scripts and commands directly through the system shell
via `uv run`. It bypasses the debugger completely, providing instant execution
and standard terminal output.

### 2.1 Method A: Using VSCodium Tasks Menu

1. Press **`Ctrl+Shift+P`** (or `F1`).
2. Type **`Tasks: Run Task`** and press **`Enter`**.
3. Select any task from the menu:
    - `🎓 Example List 001 (Interactive Input Prompt)`
    - `🎓 Example List 001 (Sort Nick, Filippos, Dimitra)`
    - `🎓 Example List 001 (Help)`
    - `🐍 Lists CLI (Interactive Subcommand Prompt)`
    - `🐍 Lists CLI Demo (Showcase)`
    - `🧪 Pytest: Test Example List 001`
    - `📊 Pytest: Full Suite with 100% Coverage`
    - `✨ Format Code & Docs (Prettier)`
    - `🔍 Lint Code (Ruff)`
    - `🛡️ Static Type Check (Mypy)`
4. The task opens in the **Terminal** tab and prints the output immediately.

---

### 2.2 Method B: Default Build Shortcut (`Ctrl+Shift+B`)

Pressing **`Ctrl+Shift+B`** triggers the default build task
(`🐍 Lists CLI Demo (Showcase)`), running the complete 15-operation lists
showcase instantly.

---

### 2.3 Method C: Running Directly in the Terminal (CLI)

You can always open the integrated terminal (`Ctrl+` `) and execute commands
directly:

```bash
# Run Example List 001 with custom elements and sort
uv run src/tutorial/list/example_list_001/example_list_001.py --data delta alpha charlie beta --sort

# Run production lists statistics with JSON output
uv run src/data_structures/lists.py stats --elements 10,20,30,40,50 --json

# Run unit tests with 100% coverage verification
uv run pytest --cov=src --cov-report=term-missing test/
```

---

## 🗺️ 3. Complete Project Target Reference

All targets are synchronized across both
[`.vscode/launch.json`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/.vscode/launch.json)
and
[`.vscode/tasks.json`](file:///C:/usr/src/ntua/chemeng/sandbox-python-pclab/.vscode/tasks.json):

| Target Name                                         | 🐞 Debugger (`F5`) | ⚡ Task Runner (`Tasks: Run Task`) | Underlying Command / Script                               |
| :-------------------------------------------------- | :----------------: | :--------------------------------: | :-------------------------------------------------------- |
| **Example List 001 (Input Prompt)**                 |         ✅         |                 ✅                 | `example_list_001.py ${input:exampleList001Args}`         |
| **Example List 001 (Sort Nick, Filippos, Dimitra)** |         ✅         |                 ✅                 | `example_list_001.py --data Nick Filippos Dimitra --sort` |
| **Example List 001 (Sort Dimitrios, James, John)**  |         ✅         |                 ✅                 | `example_list_001.py --data Dimitrios James John --sort`  |
| **Example List 001 (Help)**                         |         —          |                 ✅                 | `example_list_001.py --help`                              |
| **Lists CLI (Subcommand Prompt)**                   |         ✅         |                 ✅                 | `lists.py ${input:listsCliArgs}`                          |
| **Lists CLI Demo (Showcase)**                       |         ✅         |        ✅ (`Ctrl+Shift+B`)         | `lists.py demo`                                           |
| **Pytest: Test Example List 001**                   |         ✅         |                 ✅                 | `pytest test/.../test_example_list_001.py -v`             |
| **Pytest: Test Lists Manager**                      |         ✅         |                 ✅                 | `pytest test/data_structures/test_lists.py -v`            |
| **Pytest: Full Suite (100% Coverage)**              |         ✅         |                 ✅                 | `pytest --cov=src --cov-report=term-missing test/`        |
| **UV: Sync Dependencies**                           |         —          |                 ✅                 | `uv sync --python python`                                 |
| **Format Code & Docs**                              |         —          |                 ✅                 | `pnpm run format`                                         |
| **Lint Code**                                       |         —          |                 ✅                 | `uv run ruff check src/ test/`                            |
| **Static Type Check**                               |         —          |                 ✅                 | `uv run mypy src/`                                        |

---

## 🛡️ 4. Engineering Traps & Best Practices

### Trap 1: The `${file}` Dynamic Macro Pitfall

- **Problem**: When a launch configuration uses `"program": "${file}"`, pressing
  `F5` while viewing `launch.json` or `settings.json` attempts to execute the
  JSON file as Python code, throwing `NameError: name 'true' is not defined`.
- **Solution**: All project launch targets use explicit script paths
  (`"${workspaceFolder}/src/..."`), preventing this error entirely.

### Trap 2: Single-String IDE Argument Passing

- **Problem**: When VSCodium evaluates an input prompt `${input:scriptArgs}`, it
  passes the entire input string (e.g. `--data Nick John --sort`) as a single
  string token in `sys.argv[1]`, causing `argparse` to raise `SystemExit: 2`.
- **Solution**: Both `lists.py` and `example_list_001.py` automatically detect
  single-string inputs and tokenize them safely via `shlex.split()`.

### Trap 3: PowerShell Profile Working Directory Drift

- **Problem**: PowerShell profiles that switch directories on launch
  (`cd C:\Users\...`) cause relative file paths to fail
  (`os error 3: path not found`).
- **Solution**: All tasks in `tasks.json` enforce
  `Set-Location '${workspaceFolder}'` and pass
  `--directory '${workspaceFolder}'` to `uv`.
