"""Merge Sort implementation, theoretical analysis, and runtime benchmarking.

Algorithm Class: Divide and Conquer
Complexity Class: P (Deterministic Polynomial Time)

Theoretical Analysis:
1. Divide: The list of size n is divided at the middle into two sublists
   of size n/2.
2. Conquer: Both sublists are recursively sorted using Merge Sort.
3. Combine: The two sorted sublists are merged into a single sorted list
   in linear time O(n).

Recurrence Relation:
    T(n) = 2 * T(n/2) + O(n) for n > 1
    T(1) = O(1)
By the Master Theorem (Case 2, a=2, b=2, f(n)=O(n^1)), T(n) = O(n log n).

Time Complexity:
- Best Case:    O(n log n) - Even for already sorted arrays, the recursive divisions
                             and merge step comparisons still proceed through all log2(n) levels.
- Average Case: O(n log n) - For random input distributions.
- Worst Case:   O(n log n) - Even with reverse or adversarial inputs, recursion depth is log2(n).

Auxiliary Space Complexity:
- O(n) auxiliary memory for creating temporary merged sublists,
  plus O(log n) call stack space for recursion frames.
"""

from __future__ import annotations

from random import Random
from time import perf_counter


DEFAULT_MERGE_SORT_SIZES = (10, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000)


def merge_sort(numbers: list[int | float] | tuple[int | float, ...]) -> list[int | float]:
    """Return a sorted copy of numbers using Merge Sort.

    Args:
        numbers: Sequence of numbers (integers or floats).

    Returns:
        A new list containing the elements in non-decreasing order.

    Raises:
        TypeError: If input is not a list/tuple or contains non-numeric values.
    """
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("numbers must be a list or tuple")

    if any(
        not isinstance(n, (int, float)) or isinstance(n, bool)
        for n in numbers
    ):
        raise TypeError("all elements must be numbers")

    if len(numbers) <= 1:
        return list(numbers)

    middle = len(numbers) // 2

    # Divide and Conquer
    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])

    # Combine
    return _merge(left, right)


def _merge(left: list[int | float], right: list[int | float]) -> list[int | float]:
    """Merge two sorted lists into one sorted list in linear time O(len(left) + len(right))."""
    result = []
    i = 0
    j = 0
    len_left = len(left)
    len_right = len(right)

    while i < len_left and j < len_right:
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def benchmark_merge_sort(
    sizes: tuple[int, ...] | list[int] = DEFAULT_MERGE_SORT_SIZES,
    trials: int = 3,
    seed: int = 42,
) -> list[dict]:
    """Benchmark Merge Sort and return runtimes in milliseconds.

    Args:
        sizes: Sequence of input sizes to evaluate.
        trials: Repetitions per input size to calculate average runtime.
        seed: Random seed for reproducible input generation.

    Returns:
        List of dicts with 'n' and 'runtime_ms'.
    """
    if (
        not isinstance(trials, int)
        or isinstance(trials, bool)
        or trials < 1
    ):
        raise ValueError("trials must be a positive integer")

    sizes = list(sizes)

    if any(
        not isinstance(n, int) or isinstance(n, bool) or n < 0
        for n in sizes
    ):
        raise ValueError("sizes must contain non-negative integers")

    rng = Random(seed)
    results = []

    for size in sizes:
        numbers = [rng.randint(0, 100000) for _ in range(size)]

        # Warm-up run; excluded from the measurements.
        merge_sort(numbers)

        start = perf_counter()
        for _ in range(trials):
            merge_sort(numbers)
        elapsed_ms = (perf_counter() - start) * 1000 / trials

        results.append({
            "n": size,
            "runtime_ms": elapsed_ms,
        })

    return results
