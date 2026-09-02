"""
Python List Data Structure: Deep Mechanics, Operations & CLI Showcase
======================================================================
This module provides a comprehensive, production-grade implementation of Python list
manipulations, algorithmic transformations, statistical calculations, memory growth
diagnostics, and operational benchmarking.

Every public method is exposed via a full-featured CLI interface.

Author: Python Language Mastery Sandbox
License: MIT
"""

from __future__ import annotations

import argparse
import ast
from collections import deque
from dataclasses import asdict, dataclass
import json
import math
import shlex
import sys
import time
from typing import Any, Callable, Sequence


# ============================================================================
# Core Data Models
# ============================================================================


@dataclass(frozen=True, slots=True)
class MemoryAllocationStep:
    """Snapshot of list capacity and memory footprint during dynamic resizing."""

    length: int
    size_bytes: int
    over_allocated_slots: int
    bytes_per_element: float


@dataclass(frozen=True, slots=True)
class ListStatistics:
    """Descriptive statistics for a numeric list."""

    count: int
    sum: float
    min: float
    max: float
    mean: float
    median: float
    variance: float
    std_dev: float

    def to_dict(self) -> dict[str, float | int]:
        """Convert statistics to a dictionary."""
        return asdict(self)


# ============================================================================
# List Operations Manager
# ============================================================================


class ListOperationsManager:
    """
    Comprehensive manager providing algorithmic operations, transformations,
    and diagnostics on Python lists.
    """

    @staticmethod
    def create_list(
        elements: Sequence[Any] | None = None,
        fill_value: Any | None = None,
        count: int = 0,
        pattern: str = "none",
    ) -> list[Any]:
        """
        Create a new list from an existing sequence, repeated fill value, or pattern.

        :param elements: Optional initial sequence.
        :param fill_value: Value to repeat `count` times.
        :param count: Repetition count for fill_value or pattern length.
        :param pattern: Generation pattern ('none', 'range', 'evens', 'squares', 'fibonacci', 'powers_of_two').
        :return: Newly created list.
        :raises ValueError: If count is negative or pattern is unrecognized.
        """
        if count < 0:
            raise ValueError("Count must be non-negative.")

        if elements is not None:
            return list(elements)

        pattern_normalized = pattern.strip().lower()
        if pattern_normalized == "none":
            if fill_value is not None:
                return [fill_value] * count
            return []

        if pattern_normalized == "range":
            return list(range(count))
        if pattern_normalized == "evens":
            return [i * 2 for i in range(count)]
        if pattern_normalized == "squares":
            return [i * i for i in range(count)]
        if pattern_normalized == "powers_of_two":
            return [2**i for i in range(count)]
        if pattern_normalized == "fibonacci":
            if count == 0:
                return []
            if count == 1:
                return [0]
            fib = [0, 1]
            while len(fib) < count:
                fib.append(fib[-1] + fib[-2])
            return fib

        raise ValueError(
            f"Unrecognized pattern '{pattern}'. Allowed: none, range, evens, squares, fibonacci, powers_of_two."
        )

    @staticmethod
    def slice_list(
        data: Sequence[Any],
        start: int | None = None,
        stop: int | None = None,
        step: int | None = None,
    ) -> list[Any]:
        """
        Extract a slice from the sequence using standard Python indexing algebra.

        :param data: Input sequence.
        :param start: Starting index (inclusive).
        :param stop: Stopping index (exclusive).
        :param step: Stride/step size (must not be 0).
        :return: Extracted slice as a list.
        :raises ValueError: If step is 0.
        """
        if step == 0:
            raise ValueError("Slice step cannot be zero.")
        return list(data[start:stop:step])

    @staticmethod
    def insert_element(data: Sequence[Any], index: int, value: Any) -> list[Any]:
        """
        Insert an element at a specific index, returning a new list.

        :param data: Source sequence.
        :param index: Target insertion position.
        :param value: Value to insert.
        :return: New list with inserted element.
        """
        result = list(data)
        result.insert(index, value)
        return result

    @staticmethod
    def delete_element(
        data: Sequence[Any],
        index: int | None = None,
        value: Any | None = None,
        all_occurrences: bool = False,
    ) -> tuple[list[Any], Any]:
        """
        Delete an element by index or value.

        :param data: Source sequence.
        :param index: Index to pop.
        :param value: Value to remove.
        :param all_occurrences: If True, removes all instances of `value`.
        :return: Tuple of (modified list, deleted element(s)).
        :raises ValueError: If neither index nor value is provided, or if value not found.
        :raises IndexError: If index is out of bounds.
        """
        result = list(data)
        if index is not None:
            if not (-len(result) <= index < len(result)) or len(result) == 0:
                raise IndexError(f"Index {index} out of range for list of length {len(result)}.")
            removed = result.pop(index)
            return result, removed

        if value is not None:
            if value not in result:
                raise ValueError(f"Value '{value}' not found in list.")
            if all_occurrences:
                removed_count = result.count(value)
                result = [x for x in result if x != value]
                return result, [value] * removed_count
            result.remove(value)
            return result, value

        raise ValueError("Must provide either 'index' or 'value' for deletion.")

    @staticmethod
    def search_element(data: Sequence[Any], value: Any, return_all: bool = False) -> list[int]:
        """
        Search for indices of a target value within the sequence.

        :param data: Source sequence.
        :param value: Target value to find.
        :param return_all: If True, returns all matched indices; otherwise only the first.
        :return: List of 0-based indices where `value` appears.
        :raises ValueError: If value is not present in data.
        """
        indices: list[int] = []
        for i, item in enumerate(data):
            if item == value:
                indices.append(i)
                if not return_all:
                    break

        if not indices:
            raise ValueError(f"Value '{value}' not found in list.")

        return indices

    @staticmethod
    def sort_list(
        data: Sequence[Any],
        reverse: bool = False,
        key_strategy: str = "natural",
    ) -> list[Any]:
        """
        Sort elements using Timsort with selectable key strategies.

        :param data: Input sequence.
        :param reverse: If True, sort in descending order.
        :param key_strategy: Strategy: 'natural', 'length', 'numeric', 'abs', 'lowercase'.
        :return: Sorted list.
        :raises ValueError: If key_strategy is invalid or types are incompatible.
        """
        result = list(data)
        strategy = key_strategy.strip().lower()

        key_fn: Callable[[Any], Any] | None = None
        if strategy == "natural":
            key_fn = None
        elif strategy == "length":
            key_fn = lambda x: len(str(x))
        elif strategy == "numeric":
            key_fn = lambda x: float(x)
        elif strategy == "abs":
            key_fn = lambda x: abs(float(x))
        elif strategy == "lowercase":
            key_fn = lambda x: str(x).lower()
        else:
            raise ValueError(
                f"Unknown key_strategy '{key_strategy}'. Allowed: natural, length, numeric, abs, lowercase."
            )

        try:
            if key_fn is not None:
                result.sort(key=key_fn, reverse=reverse)
            else:
                result.sort(reverse=reverse)
        except TypeError as exc:
            raise ValueError(f"Cannot sort elements with strategy '{key_strategy}': {exc}") from exc

        return result

    @staticmethod
    def reverse_list(data: Sequence[Any], in_place: bool = False) -> list[Any]:
        """
        Reverse elements of a sequence.

        :param data: Source sequence.
        :param in_place: If True and data is a list, mutates in place; otherwise returns a new reversed list.
        :return: Reversed list.
        """
        if in_place and isinstance(data, list):
            data.reverse()
            return data
        return list(reversed(data))

    @staticmethod
    def filter_and_transform(
        data: Sequence[Any],
        filter_strategy: str = "none",
        transform_strategy: str = "none",
    ) -> list[Any]:
        """
        Filter and transform elements using list comprehensions.

        :param data: Input sequence.
        :param filter_strategy: 'none', 'evens', 'odds', 'positives', 'negatives', 'non_empty'.
        :param transform_strategy: 'none', 'square', 'cube', 'abs', 'upper', 'lower', 'stringify'.
        :return: Transformed and filtered list.
        :raises ValueError: If strategy names are invalid or element types do not match strategy.
        """
        f_strat = filter_strategy.strip().lower()
        t_strat = transform_strategy.strip().lower()

        # Build filter predicate
        pred: Callable[[Any], bool]
        if f_strat == "none":
            pred = lambda _: True
        elif f_strat == "evens":
            pred = lambda x: int(x) % 2 == 0
        elif f_strat == "odds":
            pred = lambda x: int(x) % 2 != 0
        elif f_strat == "positives":
            pred = lambda x: float(x) > 0
        elif f_strat == "negatives":
            pred = lambda x: float(x) < 0
        elif f_strat == "non_empty":
            pred = lambda x: bool(x)
        else:
            raise ValueError(
                f"Unknown filter_strategy '{filter_strategy}'. Allowed: none, evens, odds, positives, negatives, non_empty."
            )

        # Build transform function
        trans: Callable[[Any], Any]
        if t_strat == "none":
            trans = lambda x: x
        elif t_strat == "square":
            trans = lambda x: float(x) ** 2 if isinstance(x, float) or "." in str(x) else int(x) ** 2
        elif t_strat == "cube":
            trans = lambda x: float(x) ** 3 if isinstance(x, float) or "." in str(x) else int(x) ** 3
        elif t_strat == "abs":
            trans = lambda x: abs(float(x)) if isinstance(x, float) or "." in str(x) else abs(int(x))
        elif t_strat == "upper":
            trans = lambda x: str(x).upper()
        elif t_strat == "lower":
            trans = lambda x: str(x).lower()
        elif t_strat == "stringify":
            trans = lambda x: str(x)
        else:
            raise ValueError(
                f"Unknown transform_strategy '{transform_strategy}'. Allowed: none, square, cube, abs, upper, lower, stringify."
            )

        try:
            return [trans(x) for x in data if pred(x)]
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Error applying filter/transform strategies: {exc}") from exc

    @staticmethod
    def rotate_list(data: Sequence[Any], shift: int) -> list[Any]:
        """
        Cyclically rotate the list elements by `shift` positions.

        :param data: Source sequence.
        :param shift: Number of places to rotate (positive = right, negative = left).
        :return: Rotated list.
        """
        if not data:
            return []
        n = len(data)
        effective_shift = shift % n
        if effective_shift == 0:
            return list(data)
        return list(data[-effective_shift:]) + list(data[:-effective_shift])

    @staticmethod
    def chunk_list(data: Sequence[Any], chunk_size: int) -> list[list[Any]]:
        """
        Partition a sequence into consecutive chunks of fixed size.

        :param data: Source sequence.
        :param chunk_size: Positive integer size of each chunk.
        :return: List of chunk sublists.
        :raises ValueError: If chunk_size <= 0.
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be strictly positive (>= 1).")
        return [list(data[i : i + chunk_size]) for i in range(0, len(data), chunk_size)]

    @staticmethod
    def flatten_list(data: Sequence[Any], depth: int = -1) -> list[Any]:
        """
        Flatten nested lists up to a specified depth.

        :param data: Nested sequence.
        :param depth: Recursion depth limit (-1 for unbounded flattening).
        :return: Flattened list.
        :raises ValueError: If depth is less than -1.
        """
        if depth < -1:
            raise ValueError("Depth must be -1 (unbounded) or >= 0.")

        result: list[Any] = []

        def _flatten_helper(items: Sequence[Any], current_depth: int) -> None:
            for item in items:
                if isinstance(item, (list, tuple)) and (depth == -1 or current_depth < depth):
                    _flatten_helper(item, current_depth + 1)
                else:
                    result.append(item)

        _flatten_helper(data, 0)
        return result

    @staticmethod
    def deduplicate_list(data: Sequence[Any], preserve_order: bool = True) -> list[Any]:
        """
        Remove duplicate items from a sequence.

        :param data: Source sequence.
        :param preserve_order: If True, preserves the original relative order (O(n)).
        :return: Deduplicated list.
        """
        if preserve_order:
            seen: set[Any] = set()
            result: list[Any] = []
            for item in data:
                # Handle unhashable items safely (like nested lists)
                try:
                    if item not in seen:
                        seen.add(item)
                        result.append(item)
                except TypeError:
                    if item not in result:
                        result.append(item)
            return result
        # Fast set conversion when order doesn't matter
        try:
            return list(set(data))
        except TypeError:
            # Fallback for unhashable items
            return ListOperationsManager.deduplicate_list(data, preserve_order=True)

    @staticmethod
    def calculate_statistics(data: Sequence[int | float]) -> ListStatistics:
        """
        Compute descriptive statistics on a numeric sequence.

        :param data: Sequence of numeric values.
        :return: ListStatistics dataclass instance.
        :raises ValueError: If data is empty or contains non-numeric values.
        """
        if not data:
            raise ValueError("Cannot calculate statistics on an empty list.")

        try:
            numeric_vals = [float(x) for x in data]
        except (ValueError, TypeError) as exc:
            raise ValueError(f"All elements must be numeric: {exc}") from exc

        count = len(numeric_vals)
        total_sum = sum(numeric_vals)
        min_val = min(numeric_vals)
        max_val = max(numeric_vals)
        mean_val = total_sum / count

        sorted_vals = sorted(numeric_vals)
        mid = count // 2
        if count % 2 == 1:
            median_val = sorted_vals[mid]
        else:
            median_val = (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0

        if count > 1:
            variance_val = sum((x - mean_val) ** 2 for x in numeric_vals) / (count - 1)
        else:
            variance_val = 0.0
        std_dev_val = math.sqrt(variance_val)

        return ListStatistics(
            count=count,
            sum=total_sum,
            min=min_val,
            max=max_val,
            mean=mean_val,
            median=median_val,
            variance=variance_val,
            std_dev=std_dev_val,
        )

    @staticmethod
    def analyze_memory_growth(max_elements: int = 64) -> list[MemoryAllocationStep]:
        """
        Empirically track CPython dynamic list capacity expansion and memory usage.

        :param max_elements: Number of elements to progressively append.
        :return: List of MemoryAllocationStep records when reallocations occur.
        :raises ValueError: If max_elements <= 0.
        """
        if max_elements <= 0:
            raise ValueError("max_elements must be strictly positive (>= 1).")

        steps: list[MemoryAllocationStep] = []
        lst: list[int] = []
        prev_size = sys.getsizeof(lst)

        # Baseline empty list record
        steps.append(
            MemoryAllocationStep(
                length=0,
                size_bytes=prev_size,
                over_allocated_slots=0,
                bytes_per_element=0.0,
            )
        )

        for i in range(1, max_elements + 1):
            lst.append(i)
            current_size = sys.getsizeof(lst)
            if current_size != prev_size:
                # Reallocation / expansion detected
                bytes_per_item = (current_size - steps[0].size_bytes) / i if i > 0 else 0.0
                steps.append(
                    MemoryAllocationStep(
                        length=i,
                        size_bytes=current_size,
                        over_allocated_slots=int((current_size - prev_size) / 8),
                        bytes_per_element=round(bytes_per_item, 2),
                    )
                )
                prev_size = current_size

        return steps

    @staticmethod
    def benchmark_operations(size: int = 10000, iterations: int = 5) -> dict[str, float]:
        """
        Benchmark core list and deque operations in microseconds.

        :param size: Number of elements for benchmark workloads.
        :param iterations: Number of trials for averaging.
        :return: Dictionary of operation name to average execution time in microseconds.
        :raises ValueError: If size <= 0 or iterations <= 0.
        """
        if size <= 0 or iterations <= 0:
            raise ValueError("size and iterations must be strictly positive.")

        timings: dict[str, float] = {}

        # 1. Append to end O(1) amortized
        times: list[float] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            test_lst: list[int] = []
            for i in range(size):
                test_lst.append(i)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1e6)
        timings["append_end_us"] = round(sum(times) / iterations, 2)

        # 2. List comprehension O(n)
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            _ = [i for i in range(size)]
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1e6)
        timings["list_comprehension_us"] = round(sum(times) / iterations, 2)

        # 3. Insert at index 0 O(n)
        scale_down = min(size, 2000)
        times = []
        for _ in range(iterations):
            test_lst = []
            t0 = time.perf_counter()
            for i in range(scale_down):
                test_lst.insert(0, i)
            t1 = time.perf_counter()
            times.append(((t1 - t0) * 1e6) * (size / scale_down))
        timings["insert_front_scaled_us"] = round(sum(times) / iterations, 2)

        # 4. Deque appendleft O(1)
        times = []
        for _ in range(iterations):
            dq: deque[int] = deque()
            t0 = time.perf_counter()
            for i in range(size):
                dq.appendleft(i)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1e6)
        timings["deque_appendleft_us"] = round(sum(times) / iterations, 2)

        # 5. Slicing copy O(k)
        sample = list(range(size))
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            _ = sample[:]
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1e6)
        timings["shallow_slice_copy_us"] = round(sum(times) / iterations, 2)

        return timings


# ============================================================================
# CLI Helper Parsers and Formatters
# ============================================================================


def parse_elements_input(raw: str | None) -> list[Any]:
    """
    Parse a raw string input into a typed Python list.
    Supports JSON literals, Python literal structures, or comma-separated tokens.
    """
    if raw is None:
        return []

    raw = raw.strip()
    if not raw:
        return []

    # Attempt ast.literal_eval for structures like "[1, 2, [3, 4]]" or "(1, 2)"
    if raw.startswith(("[", "{", "(")):
        try:
            evaluated = ast.literal_eval(raw)
            if isinstance(evaluated, (list, tuple)):
                return list(evaluated)
        except (ValueError, SyntaxError):
            pass

    # Fallback to comma-separated tokenization with auto-type casting
    tokens = [tok.strip() for tok in raw.split(",")]
    result: list[Any] = []
    for token in tokens:
        if token.isdigit():
            result.append(int(token))
        elif token.startswith("-") and token[1:].isdigit():
            result.append(int(token))
        else:
            try:
                result.append(float(token))
            except ValueError:
                result.append(token)
    return result


def parse_single_value(raw: str | None) -> Any:
    """Parse a single value token into an int, float, or string."""
    if raw is None:
        return None
    raw = raw.strip()
    if raw.isdigit():
        return int(raw)
    if raw.startswith("-") and raw[1:].isdigit():
        return int(raw)
    try:
        return float(raw)
    except ValueError:
        return raw


# ============================================================================
# Interactive Demonstration Function
# ============================================================================


def run_interactive_showcase() -> None:
    """Run an end-to-end pedagogical demonstration of all list operations."""
    mgr = ListOperationsManager
    print("=" * 70)
    print("PYTHON LIST DATA STRUCTURE: DEEP OPERATIONAL SHOWCASE")
    print("=" * 70)

    # 1. Creation
    fibs = mgr.create_list(pattern="fibonacci", count=8)
    print(f"\n[1] Generated Fibonacci List (count=8): {fibs}")

    # 2. Slicing
    sliced = mgr.slice_list(fibs, start=1, stop=7, step=2)
    print(f"[2] Sliced fibs[1:7:2]: {sliced}")

    # 3. Insertion
    inserted = mgr.insert_element(fibs, index=2, value=999)
    print(f"[3] Inserted 999 at index 2: {inserted}")

    # 4. Deletion
    deleted, val = mgr.delete_element(inserted, index=2)
    print(f"[4] Deleted element at index 2 (removed {val}): {deleted}")

    # 5. Search
    indices = mgr.search_element(fibs, value=1, return_all=True)
    print(f"[5] Searched for value 1 in {fibs}: indices = {indices}")

    # 6. Sorting
    words = ["banana", "fig", "apple", "elderberry", "date"]
    sorted_words = mgr.sort_list(words, key_strategy="length")
    print(f"[6] Sorted words by length: {sorted_words}")

    # 7. Rotation
    rotated = mgr.rotate_list(fibs, shift=3)
    print(f"[7] Rotated {fibs} right by 3 places: {rotated}")

    # 8. Chunking
    chunks = mgr.chunk_list(fibs, chunk_size=3)
    print(f"[8] Chunked {fibs} into size 3 batches: {chunks}")

    # 9. Flattening
    nested = [1, [2, [3, 4], 5], [6, 7]]
    flat = mgr.flatten_list(nested)
    print(f"[9] Flattened {nested} (all levels): {flat}")

    # 10. Deduplication
    dupes = [1, 2, 2, 3, 1, 4, 2, 5]
    deduped = mgr.deduplicate_list(dupes, preserve_order=True)
    print(f"[10] Deduplicated {dupes} (order preserved): {deduped}")

    # 11. Statistics
    stats = mgr.calculate_statistics(fibs)
    print(f"[11] Descriptive Stats for {fibs}:")
    print(f"     Sum={stats.sum}, Mean={stats.mean:.2f}, Median={stats.median}, StdDev={stats.std_dev:.2f}")

    # 12. Memory Growth
    steps = mgr.analyze_memory_growth(max_elements=32)
    print("\n[12] CPython Dynamic List Resizing Transitions:")
    print(f"{'Length':<10} {'Size (Bytes)':<15} {'Overallocated Slots':<20}")
    print("-" * 48)
    for s in steps[:8]:
        print(f"{s.length:<10} {s.size_bytes:<15} {s.over_allocated_slots:<20}")

    # 13. Benchmarking
    bench = mgr.benchmark_operations(size=5000, iterations=3)
    print("\n[13] Microsecond Benchmark Timings (5000 items):")
    for k, v in bench.items():
        print(f"     - {k:<25}: {v:.2f} us")

    print("\n" + "=" * 70)
    print("[SUCCESS] Showcase execution completed successfully.")
    print("=" * 70)


# ============================================================================
# CLI Entrypoint & Subparsers
# ============================================================================


def build_cli_parser() -> argparse.ArgumentParser:
    """Construct the comprehensive argparse command-line parser."""
    parser = argparse.ArgumentParser(
        prog="lists.py",
        description="Production CLI & Pedagogical Toolkit for Python Lists.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: demo
    subparsers.add_parser("demo", help="Run the full interactive showcase.")

    # Command: create
    p_create = subparsers.add_parser("create", help="Create a list with specified patterns or values.")
    p_create.add_argument("--elements", type=str, default=None, help="Initial comma-separated elements or JSON.")
    p_create.add_argument("--fill", type=str, default=None, help="Fill value to repeat.")
    p_create.add_argument("--count", type=int, default=0, help="Number of repetitions or pattern size.")
    p_create.add_argument(
        "--pattern",
        type=str,
        default="none",
        choices=["none", "range", "evens", "squares", "fibonacci", "powers_of_two"],
        help="Generation pattern.",
    )
    p_create.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: slice
    p_slice = subparsers.add_parser("slice", help="Slice a list with start, stop, step indices.")
    p_slice.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_slice.add_argument("--start", type=int, default=None, help="Start index (inclusive).")
    p_slice.add_argument("--stop", type=int, default=None, help="Stop index (exclusive).")
    p_slice.add_argument("--step", type=int, default=None, help="Stride/step (cannot be 0).")
    p_slice.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: insert
    p_insert = subparsers.add_parser("insert", help="Insert an element at a given index.")
    p_insert.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_insert.add_argument("--index", type=int, required=True, help="Target index for insertion.")
    p_insert.add_argument("--value", type=str, required=True, help="Value to insert.")
    p_insert.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: delete
    p_delete = subparsers.add_parser("delete", help="Delete an element by index or value.")
    p_delete.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_delete.add_argument("--index", type=int, default=None, help="Index to delete (pop).")
    p_delete.add_argument("--value", type=str, default=None, help="Value to remove.")
    p_delete.add_argument("--all", action="store_true", help="Remove all occurrences of value.")
    p_delete.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: search
    p_search = subparsers.add_parser("search", help="Find 0-based indices of a target value.")
    p_search.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_search.add_argument("--value", type=str, required=True, help="Target value to search for.")
    p_search.add_argument("--all", action="store_true", help="Return all matched indices.")
    p_search.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: sort
    p_sort = subparsers.add_parser("sort", help="Sort elements using Timsort.")
    p_sort.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_sort.add_argument("--reverse", action="store_true", help="Sort in descending order.")
    p_sort.add_argument(
        "--key",
        type=str,
        default="natural",
        choices=["natural", "length", "numeric", "abs", "lowercase"],
        help="Sorting key strategy.",
    )
    p_sort.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: reverse
    p_reverse = subparsers.add_parser("reverse", help="Reverse a sequence.")
    p_reverse.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_reverse.add_argument("--in-place", action="store_true", help="Perform in-place reversal.")
    p_reverse.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: filter
    p_filter = subparsers.add_parser("filter", help="Filter and transform elements via comprehensions.")
    p_filter.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_filter.add_argument(
        "--filter-strategy",
        type=str,
        default="none",
        choices=["none", "evens", "odds", "positives", "negatives", "non_empty"],
        help="Filter predicate.",
    )
    p_filter.add_argument(
        "--transform-strategy",
        type=str,
        default="none",
        choices=["none", "square", "cube", "abs", "upper", "lower", "stringify"],
        help="Transformation mapping.",
    )
    p_filter.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: rotate
    p_rotate = subparsers.add_parser("rotate", help="Rotate elements cyclically.")
    p_rotate.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_rotate.add_argument("--shift", type=int, required=True, help="Shift count (+ right, - left).")
    p_rotate.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: chunk
    p_chunk = subparsers.add_parser("chunk", help="Partition sequence into fixed-size batches.")
    p_chunk.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_chunk.add_argument("--chunk-size", type=int, required=True, help="Batch size (>= 1).")
    p_chunk.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: flatten
    p_flatten = subparsers.add_parser("flatten", help="Flatten nested lists.")
    p_flatten.add_argument("--elements", type=str, required=True, help="Nested sequence (e.g. '[[1,2],[3,[4]]]').")
    p_flatten.add_argument("--depth", type=int, default=-1, help="Recursion depth limit (-1 for unbounded).")
    p_flatten.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: deduplicate
    p_dedup = subparsers.add_parser("deduplicate", help="Remove duplicate values.")
    p_dedup.add_argument("--elements", type=str, required=True, help="Input sequence.")
    p_dedup.add_argument("--preserve-order", action="store_true", default=True, help="Preserve initial order.")
    p_dedup.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: stats
    p_stats = subparsers.add_parser("stats", help="Compute summary statistics for numeric list.")
    p_stats.add_argument("--elements", type=str, required=True, help="Numeric sequence.")
    p_stats.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: growth
    p_growth = subparsers.add_parser("growth", help="Analyze CPython list dynamic reallocation growth.")
    p_growth.add_argument("--max-elements", type=int, default=64, help="Maximum elements to append.")
    p_growth.add_argument("--json", action="store_true", help="Output result as JSON.")

    # Command: benchmark
    p_bench = subparsers.add_parser("benchmark", help="Benchmark list vs deque operations.")
    p_bench.add_argument("--size", type=int, default=10000, help="Element count per trial.")
    p_bench.add_argument("--iterations", type=int, default=5, help="Number of benchmark iterations.")
    p_bench.add_argument("--json", action="store_true", help="Output result as JSON.")

    return parser


def handle_cli_dispatch(args: argparse.Namespace) -> int:
    """Execute the appropriate ListOperationsManager method based on parsed arguments."""
    mgr = ListOperationsManager

    if args.command is None or args.command == "demo":
        run_interactive_showcase()
        return 0

    as_json = getattr(args, "json", False)

    try:
        if args.command == "create":
            elems = parse_elements_input(args.elements) if args.elements else None
            fill = parse_single_value(args.fill)
            res = mgr.create_list(elements=elems, fill_value=fill, count=args.count, pattern=args.pattern)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Created List: {res}")

        elif args.command == "slice":
            data = parse_elements_input(args.elements)
            res = mgr.slice_list(data, start=args.start, stop=args.stop, step=args.step)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Sliced List: {res}")

        elif args.command == "insert":
            data = parse_elements_input(args.elements)
            val = parse_single_value(args.value)
            res = mgr.insert_element(data, index=args.index, value=val)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Result List: {res}")

        elif args.command == "delete":
            data = parse_elements_input(args.elements)
            val = parse_single_value(args.value)
            res_list, deleted = mgr.delete_element(
                data, index=args.index, value=val, all_occurrences=getattr(args, "all", False)
            )
            if as_json:
                print(json.dumps({"result": res_list, "deleted": deleted}))
            else:
                print(f"Result List: {res_list}\nDeleted Element(s): {deleted}")

        elif args.command == "search":
            data = parse_elements_input(args.elements)
            val = parse_single_value(args.value)
            res = mgr.search_element(data, value=val, return_all=getattr(args, "all", False))
            if as_json:
                print(json.dumps({"indices": res}))
            else:
                print(f"Found at Index/Indices: {res}")

        elif args.command == "sort":
            data = parse_elements_input(args.elements)
            res = mgr.sort_list(data, reverse=args.reverse, key_strategy=args.key)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Sorted List: {res}")

        elif args.command == "reverse":
            data = parse_elements_input(args.elements)
            res = mgr.reverse_list(data, in_place=args.in_place)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Reversed List: {res}")

        elif args.command == "filter":
            data = parse_elements_input(args.elements)
            res = mgr.filter_and_transform(
                data, filter_strategy=args.filter_strategy, transform_strategy=args.transform_strategy
            )
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Filtered & Transformed List: {res}")

        elif args.command == "rotate":
            data = parse_elements_input(args.elements)
            res = mgr.rotate_list(data, shift=args.shift)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Rotated List: {res}")

        elif args.command == "chunk":
            data = parse_elements_input(args.elements)
            res = mgr.chunk_list(data, chunk_size=args.chunk_size)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Chunked Batches: {res}")

        elif args.command == "flatten":
            data = parse_elements_input(args.elements)
            res = mgr.flatten_list(data, depth=args.depth)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Flattened List: {res}")

        elif args.command == "deduplicate":
            data = parse_elements_input(args.elements)
            res = mgr.deduplicate_list(data, preserve_order=args.preserve_order)
            if as_json:
                print(json.dumps({"result": res}))
            else:
                print(f"Deduplicated List: {res}")

        elif args.command == "stats":
            data = parse_elements_input(args.elements)
            stats = mgr.calculate_statistics(data)
            if as_json:
                print(json.dumps(stats.to_dict(), indent=2))
            else:
                print("List Summary Statistics:")
                for k, v in stats.to_dict().items():
                    print(f"  {k:<12}: {v}")

        elif args.command == "growth":
            steps = mgr.analyze_memory_growth(max_elements=args.max_elements)
            if as_json:
                print(json.dumps([asdict(s) for s in steps], indent=2))
            else:
                print(f"CPython List Dynamic Resizing Analysis (1..{args.max_elements}):")
                print(f"{'Length':<8} {'Size (Bytes)':<14} {'Overallocated Slots':<20} {'Bytes/Elem':<12}")
                print("-" * 56)
                for s in steps:
                    print(f"{s.length:<8} {s.size_bytes:<14} {s.over_allocated_slots:<20} {s.bytes_per_element:<12}")

        elif args.command == "benchmark":
            results = mgr.benchmark_operations(size=args.size, iterations=args.iterations)
            if as_json:
                print(json.dumps(results, indent=2))
            else:
                print(f"Benchmark Results (size={args.size}, iterations={args.iterations}):")
                for k, v in results.items():
                    print(f"  {k:<28}: {v:.2f} us")

        return 0

    except (ValueError, IndexError, TypeError) as err:
        if as_json:
            print(json.dumps({"error": str(err)}))
        else:
            print(f"Error: {err}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    """Main program entrypoint."""
    if argv is None and len(sys.argv) == 2 and " " in sys.argv[1]:
        argv = shlex.split(sys.argv[1])
    elif argv is not None and len(argv) == 1 and " " in argv[0]:
        argv = shlex.split(argv[0])

    parser = build_cli_parser()
    args = parser.parse_args(argv)
    return handle_cli_dispatch(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
