
"""Brute-force implementation of the Subset Sum decision problem."""

from random import Random
from time import perf_counter


def subset_sum_bruteforce(numbers, target):
    """Return True if any subset sums to target, otherwise False.

    Time complexity: O(n * 2**n)
    Space complexity: O(1) auxiliary space, excluding the input.
    """
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("numbers must be a list or tuple")

    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError("target must be an integer")

    if any(not isinstance(n, int) or isinstance(n, bool) for n in numbers):
        raise TypeError("all numbers must be integers")

    n = len(numbers)

    # Each bit represents whether an element is included in a subset.
    for mask in range(1 << n):
        current_sum = 0

        for i in range(n):
            if mask & (1 << i):
                current_sum += numbers[i]

        if current_sum == target:
            return True

    return False



def benchmark_subset_sum(
    sizes=(5, 10, 15, 20, 25, 30),
    trials=3,
    seed=42,
):
    """Measure brute-force Subset Sum runtime in milliseconds.

    The generated target is impossible to reach, forcing the algorithm
    to examine every subset. Large input sizes may take a long time.
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
        numbers = [rng.randint(1, 100) for _ in range(size)]

        # Impossible target forces examination of all 2**n subsets.
        target = sum(numbers) + 1

        start = perf_counter()

        for _ in range(trials):
            found = subset_sum_bruteforce(numbers, target)

        elapsed_ms = (perf_counter() - start) * 1000 / trials

        results.append({
            "n": size,
            "runtime_ms": elapsed_ms,
            "target": target,
            "found": found,
        })

    return results
