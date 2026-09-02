"""
Unit tests for data_structures.lists module achieving 100% line and branch coverage.
"""

from __future__ import annotations

import json
from typing import Any
import pytest

from data_structures.lists import (
    ListOperationsManager,
    ListStatistics,
    MemoryAllocationStep,
    build_cli_parser,
    handle_cli_dispatch,
    main,
    parse_elements_input,
    parse_single_value,
    run_interactive_showcase,
)


# ============================================================================
# Core ListOperationsManager Tests
# ============================================================================


class TestListCreation:
    """Test suite for ListOperationsManager.create_list."""

    def test_create_from_sequence(self):
        result = ListOperationsManager.create_list(elements=[1, 2, 3])
        assert result == [1, 2, 3]

    def test_create_fill_value(self):
        result = ListOperationsManager.create_list(fill_value="x", count=4)
        assert result == ["x", "x", "x", "x"]

    def test_create_empty_default(self):
        result = ListOperationsManager.create_list()
        assert result == []

    def test_create_negative_count_raises(self):
        with pytest.raises(ValueError, match="Count must be non-negative"):
            ListOperationsManager.create_list(count=-1)

    def test_create_pattern_range(self):
        result = ListOperationsManager.create_list(pattern="range", count=5)
        assert result == [0, 1, 2, 3, 4]

    def test_create_pattern_evens(self):
        result = ListOperationsManager.create_list(pattern="evens", count=4)
        assert result == [0, 2, 4, 6]

    def test_create_pattern_squares(self):
        result = ListOperationsManager.create_list(pattern="squares", count=4)
        assert result == [0, 1, 4, 9]

    def test_create_pattern_powers_of_two(self):
        result = ListOperationsManager.create_list(pattern="powers_of_two", count=5)
        assert result == [1, 2, 4, 8, 16]

    def test_create_pattern_fibonacci(self):
        assert ListOperationsManager.create_list(pattern="fibonacci", count=0) == []
        assert ListOperationsManager.create_list(pattern="fibonacci", count=1) == [0]
        assert ListOperationsManager.create_list(pattern="fibonacci", count=6) == [0, 1, 1, 2, 3, 5]

    def test_create_pattern_invalid_raises(self):
        with pytest.raises(ValueError, match="Unrecognized pattern"):
            ListOperationsManager.create_list(pattern="unknown_pattern", count=5)


class TestListSlicing:
    """Test suite for ListOperationsManager.slice_list."""

    def test_slice_standard(self):
        data = [10, 20, 30, 40, 50]
        assert ListOperationsManager.slice_list(data, 1, 4) == [20, 30, 40]

    def test_slice_with_step(self):
        data = [0, 1, 2, 3, 4, 5, 6, 7]
        assert ListOperationsManager.slice_list(data, 0, 8, 2) == [0, 2, 4, 6]

    def test_slice_reverse(self):
        data = [1, 2, 3, 4, 5]
        assert ListOperationsManager.slice_list(data, step=-1) == [5, 4, 3, 2, 1]

    def test_slice_step_zero_raises(self):
        with pytest.raises(ValueError, match="Slice step cannot be zero"):
            ListOperationsManager.slice_list([1, 2, 3], step=0)


class TestListInsertion:
    """Test suite for ListOperationsManager.insert_element."""

    def test_insert_at_beginning(self):
        assert ListOperationsManager.insert_element([2, 3], 0, 1) == [1, 2, 3]

    def test_insert_in_middle(self):
        assert ListOperationsManager.insert_element([1, 3], 1, 2) == [1, 2, 3]

    def test_insert_at_end(self):
        assert ListOperationsManager.insert_element([1, 2], 5, 3) == [1, 2, 3]


class TestListDeletion:
    """Test suite for ListOperationsManager.delete_element."""

    def test_delete_by_index(self):
        res, val = ListOperationsManager.delete_element([10, 20, 30], index=1)
        assert res == [10, 30]
        assert val == 20

    def test_delete_by_negative_index(self):
        res, val = ListOperationsManager.delete_element([10, 20, 30], index=-1)
        assert res == [10, 20]
        assert val == 30

    def test_delete_by_index_out_of_bounds_raises(self):
        with pytest.raises(IndexError, match="out of range"):
            ListOperationsManager.delete_element([10, 20], index=5)
        with pytest.raises(IndexError, match="out of range"):
            ListOperationsManager.delete_element([], index=0)

    def test_delete_by_value(self):
        res, val = ListOperationsManager.delete_element([1, 2, 3, 2], value=2)
        assert res == [1, 3, 2]
        assert val == 2

    def test_delete_all_occurrences_by_value(self):
        res, val = ListOperationsManager.delete_element([1, 2, 3, 2, 4, 2], value=2, all_occurrences=True)
        assert res == [1, 3, 4]
        assert val == [2, 2, 2]

    def test_delete_value_not_found_raises(self):
        with pytest.raises(ValueError, match="not found in list"):
            ListOperationsManager.delete_element([1, 2, 3], value=99)

    def test_delete_no_args_raises(self):
        with pytest.raises(ValueError, match="Must provide either 'index' or 'value'"):
            ListOperationsManager.delete_element([1, 2, 3])


class TestListSearching:
    """Test suite for ListOperationsManager.search_element."""

    def test_search_first_match(self):
        assert ListOperationsManager.search_element(["a", "b", "c", "b"], "b") == [1]

    def test_search_all_matches(self):
        assert ListOperationsManager.search_element(["a", "b", "c", "b"], "b", return_all=True) == [1, 3]

    def test_search_not_found_raises(self):
        with pytest.raises(ValueError, match="not found in list"):
            ListOperationsManager.search_element([1, 2, 3], 99)


class TestListSorting:
    """Test suite for ListOperationsManager.sort_list."""

    def test_sort_natural(self):
        assert ListOperationsManager.sort_list([3, 1, 4, 2]) == [1, 2, 3, 4]

    def test_sort_reverse(self):
        assert ListOperationsManager.sort_list([1, 2, 3], reverse=True) == [3, 2, 1]

    def test_sort_by_length(self):
        assert ListOperationsManager.sort_list(["banana", "apple", "fig"], key_strategy="length") == ["fig", "apple", "banana"]

    def test_sort_by_numeric(self):
        assert ListOperationsManager.sort_list(["10", "2", "300"], key_strategy="numeric") == ["2", "10", "300"]

    def test_sort_by_abs(self):
        assert ListOperationsManager.sort_list([-5, 2, -1, 4], key_strategy="abs") == [-1, 2, 4, -5]

    def test_sort_by_lowercase(self):
        assert ListOperationsManager.sort_list(["Banana", "apple", "Cherry"], key_strategy="lowercase") == ["apple", "Banana", "Cherry"]

    def test_sort_invalid_strategy_raises(self):
        with pytest.raises(ValueError, match="Unknown key_strategy"):
            ListOperationsManager.sort_list([1, 2, 3], key_strategy="invalid")

    def test_sort_incompatible_types_raises(self):
        with pytest.raises(ValueError, match="Cannot sort elements"):
            ListOperationsManager.sort_list([1, "two", 3], key_strategy="natural")


class TestListReversal:
    """Test suite for ListOperationsManager.reverse_list."""

    def test_reverse_new_list(self):
        data = [1, 2, 3]
        res = ListOperationsManager.reverse_list(data, in_place=False)
        assert res == [3, 2, 1]
        assert data == [1, 2, 3]

    def test_reverse_in_place(self):
        data = [1, 2, 3]
        res = ListOperationsManager.reverse_list(data, in_place=True)
        assert res == [3, 2, 1]
        assert data == [3, 2, 1]

    def test_reverse_tuple_in_place_fallback(self):
        data = (1, 2, 3)
        res = ListOperationsManager.reverse_list(data, in_place=True)
        assert res == [3, 2, 1]


class TestListFilterTransform:
    """Test suite for ListOperationsManager.filter_and_transform."""

    def test_filter_evens_transform_square(self):
        data = [1, 2, 3, 4, 5, 6]
        res = ListOperationsManager.filter_and_transform(data, filter_strategy="evens", transform_strategy="square")
        assert res == [4, 16, 36]

    def test_filter_odds_transform_cube(self):
        data = [1, 2, 3, 4]
        res = ListOperationsManager.filter_and_transform(data, filter_strategy="odds", transform_strategy="cube")
        assert res == [1, 27]

    def test_filter_positives_transform_abs(self):
        data = [-5, 3, -1, 4]
        res = ListOperationsManager.filter_and_transform(data, filter_strategy="positives", transform_strategy="abs")
        assert res == [3, 4]

    def test_filter_negatives_transform_abs_floats(self):
        data = [-5.5, 3.0, -1.2]
        res = ListOperationsManager.filter_and_transform(data, filter_strategy="negatives", transform_strategy="abs")
        assert res == [5.5, 1.2]

    def test_filter_non_empty_transform_upper_lower_stringify(self):
        data = ["", "hello", "world"]
        assert ListOperationsManager.filter_and_transform(data, filter_strategy="non_empty", transform_strategy="upper") == ["HELLO", "WORLD"]
        assert ListOperationsManager.filter_and_transform(data, filter_strategy="non_empty", transform_strategy="lower") == ["hello", "world"]
        assert ListOperationsManager.filter_and_transform([1, 2], transform_strategy="stringify") == ["1", "2"]

    def test_filter_float_powers(self):
        data = [2.5]
        assert ListOperationsManager.filter_and_transform(data, transform_strategy="square") == [6.25]
        assert ListOperationsManager.filter_and_transform(data, transform_strategy="cube") == [15.625]

    def test_filter_none_transform_none(self):
        data = [1, 2, 3]
        assert ListOperationsManager.filter_and_transform(data) == [1, 2, 3]

    def test_invalid_filter_strategy_raises(self):
        with pytest.raises(ValueError, match="Unknown filter_strategy"):
            ListOperationsManager.filter_and_transform([1, 2], filter_strategy="invalid")

    def test_invalid_transform_strategy_raises(self):
        with pytest.raises(ValueError, match="Unknown transform_strategy"):
            ListOperationsManager.filter_and_transform([1, 2], transform_strategy="invalid")

    def test_filter_transform_type_error_raises(self):
        with pytest.raises(ValueError, match="Error applying filter/transform strategies"):
            ListOperationsManager.filter_and_transform(["abc"], filter_strategy="evens")


class TestListRotation:
    """Test suite for ListOperationsManager.rotate_list."""

    def test_rotate_empty(self):
        assert ListOperationsManager.rotate_list([], 3) == []

    def test_rotate_zero_shift(self):
        assert ListOperationsManager.rotate_list([1, 2, 3], 0) == [1, 2, 3]

    def test_rotate_right(self):
        assert ListOperationsManager.rotate_list([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]

    def test_rotate_left(self):
        assert ListOperationsManager.rotate_list([1, 2, 3, 4, 5], -2) == [3, 4, 5, 1, 2]


class TestListChunking:
    """Test suite for ListOperationsManager.chunk_list."""

    def test_chunk_even(self):
        assert ListOperationsManager.chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_chunk_remainder(self):
        assert ListOperationsManager.chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_chunk_invalid_size_raises(self):
        with pytest.raises(ValueError, match="chunk_size must be strictly positive"):
            ListOperationsManager.chunk_list([1, 2, 3], 0)


class TestListFlattening:
    """Test suite for ListOperationsManager.flatten_list."""

    def test_flatten_unbounded(self):
        nested = [1, [2, [3, [4]], 5], 6]
        assert ListOperationsManager.flatten_list(nested) == [1, 2, 3, 4, 5, 6]

    def test_flatten_depth_1(self):
        nested = [1, [2, [3]], 4]
        assert ListOperationsManager.flatten_list(nested, depth=1) == [1, 2, [3], 4]

    def test_flatten_depth_0(self):
        nested = [1, [2, 3]]
        assert ListOperationsManager.flatten_list(nested, depth=0) == [1, [2, 3]]

    def test_flatten_invalid_depth_raises(self):
        with pytest.raises(ValueError, match="Depth must be -1"):
            ListOperationsManager.flatten_list([1, 2], depth=-2)


class TestListDeduplication:
    """Test suite for ListOperationsManager.deduplicate_list."""

    def test_dedup_preserve_order(self):
        data = [3, 1, 2, 3, 2, 4, 1]
        assert ListOperationsManager.deduplicate_list(data, preserve_order=True) == [3, 1, 2, 4]

    def test_dedup_unhashable_preserve_order(self):
        data = [[1, 2], [3], [1, 2], [4]]
        assert ListOperationsManager.deduplicate_list(data, preserve_order=True) == [[1, 2], [3], [4]]

    def test_dedup_set_conversion(self):
        data = [3, 1, 2, 3, 2]
        res = ListOperationsManager.deduplicate_list(data, preserve_order=False)
        assert sorted(res) == [1, 2, 3]

    def test_dedup_unhashable_set_conversion_fallback(self):
        data = [[1], [2], [1]]
        res = ListOperationsManager.deduplicate_list(data, preserve_order=False)
        assert res == [[1], [2]]


class TestListStatistics:
    """Test suite for ListOperationsManager.calculate_statistics."""

    def test_statistics_odd_length(self):
        stats = ListOperationsManager.calculate_statistics([10, 20, 30])
        assert stats.count == 3
        assert stats.sum == 60.0
        assert stats.min == 10.0
        assert stats.max == 30.0
        assert stats.mean == 20.0
        assert stats.median == 20.0
        assert stats.variance == 100.0
        assert round(stats.std_dev, 2) == 10.0

    def test_statistics_even_length(self):
        stats = ListOperationsManager.calculate_statistics([10, 20, 30, 40])
        assert stats.count == 4
        assert stats.median == 25.0

    def test_statistics_single_element(self):
        stats = ListOperationsManager.calculate_statistics([42])
        assert stats.count == 1
        assert stats.variance == 0.0
        assert stats.std_dev == 0.0

    def test_statistics_empty_raises(self):
        with pytest.raises(ValueError, match="Cannot calculate statistics on an empty list"):
            ListOperationsManager.calculate_statistics([])

    def test_statistics_non_numeric_raises(self):
        with pytest.raises(ValueError, match="All elements must be numeric"):
            ListOperationsManager.calculate_statistics(["a", "b"])


class TestMemoryGrowthAndBenchmark:
    """Test suite for memory growth tracking and benchmarks."""

    def test_analyze_memory_growth(self):
        steps = ListOperationsManager.analyze_memory_growth(max_elements=16)
        assert len(steps) >= 2
        assert steps[0].length == 0
        assert steps[0].size_bytes > 0

    def test_analyze_memory_growth_invalid_raises(self):
        with pytest.raises(ValueError, match="max_elements must be strictly positive"):
            ListOperationsManager.analyze_memory_growth(0)

    def test_benchmark_operations(self):
        res = ListOperationsManager.benchmark_operations(size=100, iterations=2)
        assert "append_end_us" in res
        assert "list_comprehension_us" in res
        assert "insert_front_scaled_us" in res
        assert "deque_appendleft_us" in res
        assert "shallow_slice_copy_us" in res

    def test_benchmark_invalid_raises(self):
        with pytest.raises(ValueError, match="size and iterations must be strictly positive"):
            ListOperationsManager.benchmark_operations(size=0)


# ============================================================================
# CLI Helper Parser Tests
# ============================================================================


class TestCLIHelpers:
    """Test suite for CLI input parsers."""

    def test_parse_elements_input_none_or_empty(self):
        assert parse_elements_input(None) == []
        assert parse_elements_input("") == []
        assert parse_elements_input("   ") == []

    def test_parse_elements_input_ast_literal(self):
        assert parse_elements_input("[1, [2, 3], 4]") == [1, [2, 3], 4]
        assert parse_elements_input("(1, 2, 3)") == [1, 2, 3]

    def test_parse_elements_input_ast_syntax_error_fallback(self):
        # Starts with [ but invalid python syntax, falls back to token splitting
        assert parse_elements_input("[invalid python syntax") == ["[invalid python syntax"]

    def test_parse_elements_input_json_non_list(self):
        # Valid json string or dict, should not return list, falls back to token splitting
        assert parse_elements_input('{"key": "value"}') == ['{"key": "value"}']

    def test_parse_elements_input_json(self):
        assert parse_elements_input('["apple", "banana"]') == ["apple", "banana"]

    def test_parse_elements_input_comma_separated(self):
        assert parse_elements_input("1, 2, -3, 4.5, text") == [1, 2, -3, 4.5, "text"]

    def test_parse_single_value(self):
        assert parse_single_value(None) is None
        assert parse_single_value("42") == 42
        assert parse_single_value("-42") == -42
        assert parse_single_value("3.14") == 3.14
        assert parse_single_value("hello") == "hello"


# ============================================================================
# Full CLI Dispatch & Subcommand Integration Tests
# ============================================================================


class TestCLIDispatch:
    """Integration test suite covering all CLI subcommands and options."""

    def test_cli_demo(self, capsys):
        code = main(["demo"])
        assert code == 0
        captured = capsys.readouterr().out
        assert "PYTHON LIST DATA STRUCTURE: DEEP OPERATIONAL SHOWCASE" in captured

    def test_cli_no_args_triggers_demo(self, capsys):
        code = main([])
        assert code == 0
        captured = capsys.readouterr().out
        assert "Showcase execution completed successfully" in captured

    def test_cli_create(self, capsys):
        assert main(["create", "--pattern", "evens", "--count", "4"]) == 0
        assert "Created List: [0, 2, 4, 6]" in capsys.readouterr().out

        assert main(["create", "--pattern", "evens", "--count", "4", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [0, 2, 4, 6]}

        assert main(["create", "--fill", "z", "--count", "3"]) == 0
        assert "Created List: ['z', 'z', 'z']" in capsys.readouterr().out

    def test_cli_slice(self, capsys):
        assert main(["slice", "--elements", "10,20,30,40,50", "--start", "1", "--stop", "4", "--step", "2"]) == 0
        assert "Sliced List: [20, 40]" in capsys.readouterr().out

        assert main(["slice", "--elements", "10,20,30", "--step", "-1", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [30, 20, 10]}

    def test_cli_insert(self, capsys):
        assert main(["insert", "--elements", "1,3", "--index", "1", "--value", "2"]) == 0
        assert "Result List: [1, 2, 3]" in capsys.readouterr().out

        assert main(["insert", "--elements", "1,3", "--index", "1", "--value", "2", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [1, 2, 3]}

    def test_cli_delete(self, capsys):
        assert main(["delete", "--elements", "10,20,30", "--index", "1"]) == 0
        out = capsys.readouterr().out
        assert "Result List: [10, 30]" in out
        assert "Deleted Element(s): 20" in out

        assert main(["delete", "--elements", "1,2,2,3", "--value", "2", "--all", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [1, 3], "deleted": [2, 2]}

    def test_cli_search(self, capsys):
        assert main(["search", "--elements", "a,b,c,b", "--value", "b", "--all"]) == 0
        assert "Found at Index/Indices: [1, 3]" in capsys.readouterr().out

        assert main(["search", "--elements", "a,b,c", "--value", "b", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"indices": [1]}

    def test_cli_sort(self, capsys):
        assert main(["sort", "--elements", "banana,apple,fig", "--key", "length"]) == 0
        assert "Sorted List: ['fig', 'apple', 'banana']" in capsys.readouterr().out

        assert main(["sort", "--elements", "3,1,2", "--reverse", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [3, 2, 1]}

    def test_cli_reverse(self, capsys):
        assert main(["reverse", "--elements", "1,2,3"]) == 0
        assert "Reversed List: [3, 2, 1]" in capsys.readouterr().out

        assert main(["reverse", "--elements", "1,2,3", "--in-place", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [3, 2, 1]}

    def test_cli_filter(self, capsys):
        assert main(["filter", "--elements", "1,2,3,4", "--filter-strategy", "evens", "--transform-strategy", "square"]) == 0
        assert "Filtered & Transformed List: [4, 16]" in capsys.readouterr().out

        assert main(["filter", "--elements", "1,2,3,4", "--filter-strategy", "odds", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [1, 3]}

    def test_cli_rotate(self, capsys):
        assert main(["rotate", "--elements", "1,2,3,4,5", "--shift", "2"]) == 0
        assert "Rotated List: [4, 5, 1, 2, 3]" in capsys.readouterr().out

        assert main(["rotate", "--elements", "1,2,3,4,5", "--shift", "-1", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [2, 3, 4, 5, 1]}

    def test_cli_chunk(self, capsys):
        assert main(["chunk", "--elements", "1,2,3,4,5", "--chunk-size", "2"]) == 0
        assert "Chunked Batches: [[1, 2], [3, 4], [5]]" in capsys.readouterr().out

        assert main(["chunk", "--elements", "1,2,3,4", "--chunk-size", "2", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [[1, 2], [3, 4]]}

    def test_cli_flatten(self, capsys):
        assert main(["flatten", "--elements", "[[1, 2], [3, [4]]]"]) == 0
        assert "Flattened List: [1, 2, 3, 4]" in capsys.readouterr().out

        assert main(["flatten", "--elements", "[[1, 2], [3, [4]]]", "--depth", "1", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [1, 2, 3, [4]]}

    def test_cli_deduplicate(self, capsys):
        assert main(["deduplicate", "--elements", "1,2,2,3,1"]) == 0
        assert "Deduplicated List: [1, 2, 3]" in capsys.readouterr().out

        assert main(["deduplicate", "--elements", "1,2,2,3,1", "--json"]) == 0
        assert json.loads(capsys.readouterr().out) == {"result": [1, 2, 3]}

    def test_cli_stats(self, capsys):
        assert main(["stats", "--elements", "10,20,30"]) == 0
        assert "List Summary Statistics:" in capsys.readouterr().out

        assert main(["stats", "--elements", "10,20,30", "--json"]) == 0
        data = json.loads(capsys.readouterr().out)
        assert data["mean"] == 20.0
        assert data["sum"] == 60.0

    def test_cli_growth(self, capsys):
        assert main(["growth", "--max-elements", "16"]) == 0
        assert "CPython List Dynamic Resizing Analysis" in capsys.readouterr().out

        assert main(["growth", "--max-elements", "8", "--json"]) == 0
        data = json.loads(capsys.readouterr().out)
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_cli_benchmark(self, capsys):
        assert main(["benchmark", "--size", "100", "--iterations", "2"]) == 0
        assert "Benchmark Results" in capsys.readouterr().out

        assert main(["benchmark", "--size", "100", "--iterations", "2", "--json"]) == 0
        data = json.loads(capsys.readouterr().out)
        assert "append_end_us" in data

    def test_cli_error_handling_text_output(self, capsys):
        code = main(["delete", "--elements", "1,2,3", "--index", "99"])
        assert code == 1
        err = capsys.readouterr().err
        assert "Error: Index 99 out of range" in err

    def test_cli_error_handling_json_output(self, capsys):
        code = main(["search", "--elements", "1,2,3", "--value", "99", "--json"])
        assert code == 1
        out = capsys.readouterr().out
        assert json.loads(out) == {"error": "Value '99' not found in list."}

    def test_cli_single_string_arg_split(self, capsys):
        # Emulates IDE debuggers passing a full command string as single argument
        code = main(["stats --elements 10,20,30,40 --json"])
        assert code == 0
        data = json.loads(capsys.readouterr().out)
        assert data["count"] == 4
        assert data["mean"] == 25.0

    def test_cli_sys_argv_single_string_split(self, monkeypatch, capsys):
        import sys
        monkeypatch.setattr(sys, "argv", ["lists.py", "slice --elements 1,2,3,4,5 --step -1 --json"])
        code = main()
        assert code == 0
        data = json.loads(capsys.readouterr().out)
        assert data["result"] == [5, 4, 3, 2, 1]
