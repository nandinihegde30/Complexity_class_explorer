
import pytest

from src.merge_sort import merge_sort, benchmark_merge_sort


def test_sort_random_numbers():
    assert merge_sort([5, 2, 8, 1, 3]) == [1, 2, 3, 5, 8]


def test_empty_list():
    assert merge_sort([]) == []


def test_single_element():
    assert merge_sort([7]) == [7]


def test_already_sorted():
    assert merge_sort([1, 2, 3, 4]) == [1, 2, 3, 4]


def test_reverse_sorted():
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_duplicate_elements():
    assert merge_sort([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]


def test_negative_numbers():
    assert merge_sort([-5, 3, -1, 0]) == [-5, -1, 0, 3]


def test_float_numbers():
    assert merge_sort([2.5, 1.1, 3.7]) == [1.1, 2.5, 3.7]


def test_input_is_not_modified():
    numbers = [4, 2, 3, 1]
    original = numbers.copy()

    merge_sort(numbers)

    assert numbers == original


def test_invalid_input_type():
    with pytest.raises(TypeError):
        merge_sort("123")


def test_invalid_element_type():
    with pytest.raises(TypeError):
        merge_sort([1, "two", 3])


def test_benchmark_returns_expected_fields():
    results = benchmark_merge_sort(
        sizes=(10, 20),
        trials=1,
        seed=42,
    )

    assert len(results) == 2

    for result in results:
        assert set(result) == {"n", "runtime_ms"}
        assert result["runtime_ms"] >= 0


def test_benchmark_rejects_zero_trials():
    with pytest.raises(ValueError):
        benchmark_merge_sort(sizes=(10,), trials=0)
