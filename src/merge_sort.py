
"""Merge Sort implementation and runtime benchmarking."""

from random import Random
from time import perf_counter


def merge_sort(numbers):
    """Return a sorted copy of numbers using Merge Sort.

    Time complexity:
        Best, average, and worst case: O(n log n)

    Space complexity:
        O(n) auxiliary space.
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

    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])

    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
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
    sizes=(100, 500, 1000, 2000, 5000, 10000),
    trials=3,
    seed=42,
):
    """Benchmark Merge Sort and return runtimes in milliseconds."""
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
