
import pytest

from src.subset_sum import subset_sum_bruteforce, benchmark_subset_sum


def test_subset_exists():
    assert subset_sum_bruteforce([3, 5, 7], 8) is True


def test_subset_does_not_exist():
    assert subset_sum_bruteforce([2, 4, 6], 5) is False


def test_empty_list_target_zero():
    assert subset_sum_bruteforce([], 0) is True


def test_empty_list_nonzero_target():
    assert subset_sum_bruteforce([], 4) is False


def test_entire_list_is_solution():
    assert subset_sum_bruteforce([1, 2, 3], 6) is True


def test_negative_numbers():
    assert subset_sum_bruteforce([-4, 7, 2], 3) is True


def test_duplicate_numbers():
    assert subset_sum_bruteforce([3, 3, 3], 6) is True


def test_target_must_be_integer():
    with pytest.raises(TypeError):
        subset_sum_bruteforce([1, 2, 3], 2.5)


def test_numbers_must_be_list_or_tuple():
    with pytest.raises(TypeError):
        subset_sum_bruteforce("123", 3)


def test_elements_must_be_integers():
    with pytest.raises(TypeError):
        subset_sum_bruteforce([1, "2", 3], 3)


def test_benchmark_returns_expected_fields():
    results = benchmark_subset_sum(
        sizes=(2, 3),
        trials=1,
        seed=42,
    )

    assert len(results) == 2

    for result in results:
        assert set(result) == {
            "n",
            "runtime_ms",
            "target",
            "found",
        }
        assert result["runtime_ms"] >= 0
        assert result["found"] is False


def test_benchmark_rejects_zero_trials():
    with pytest.raises(ValueError):
        benchmark_subset_sum(sizes=(2,), trials=0)
