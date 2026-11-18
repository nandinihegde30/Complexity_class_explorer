"""Brute-force implementation and analysis of the Subset Sum decision problem.

Complexity Class: NP-Complete (NP and NP-Hard)
Exhaustive Search Time Complexity: O(n * 2^n)
Verification Time Complexity: O(n) (Polynomial Time)

Theoretical Analysis:
1. Problem Definition:
   Given a multiset of integers S and an integer target T, does there exist
   a subset S' subset_of S such that sum(S') == T?
2. Exhaustive Search Strategy:
   Every element has two choices: include (1) or exclude (0). For a set of
   size n, there are 2^n possible subsets. Each subset can be represented
   by a binary mask from 0 to 2^n - 1. Computing the sum of an arbitrary
   subset takes up to n additions, yielding a worst-case time complexity of O(n * 2^n).
3. Polynomial-Time Verification:
   Although finding whether a valid subset exists is computationally hard
   (exponential worst-case for brute force), given a proposed subset certificate,
   verifying whether its elements belong to S and sum to T takes only linear time O(n).
   This property defines the complexity class NP (Nondeterministic Polynomial Time).
4. NP vs NP-Hard vs NP-Complete:
   - P: Problems solvable in polynomial time deterministically.
   - NP: Problems verifiable in polynomial time given a certificate.
   - NP-Hard: Problems at least as hard as any problem in NP (every problem in NP
     reduces to it in polynomial time). An NP-hard problem need not be in NP.
   - NP-Complete: Problems that are both in NP and NP-Hard. Subset Sum was proven
     NP-complete by Richard Karp (1972) via reduction from 3-SAT.
"""

from __future__ import annotations

from collections import Counter
from random import Random
from time import perf_counter


DEFAULT_SUBSET_SUM_SIZES = (5, 8, 10, 12, 15, 18, 20, 22, 24, 26)


def subset_sum_bruteforce(
    numbers: list[int] | tuple[int, ...],
    target: int,
) -> bool:
    """Return True if any subset sums to target, otherwise False.

    Algorithm: Exhaustive binary mask enumeration across all 2^n candidate subsets.

    Time Complexity: O(n * 2^n)
    Space Complexity: O(1) auxiliary space (excluding input storage).
    """
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("numbers must be a list or tuple")

    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError("target must be an integer")

    if any(not isinstance(n, int) or isinstance(n, bool) for n in numbers):
        raise TypeError("all numbers must be integers")

    n = len(numbers)

    # Each bit in mask indicates whether the i-th element is included
    for mask in range(1 << n):
        current_sum = 0
        for i in range(n):
            if mask & (1 << i):
                current_sum += numbers[i]

        if current_sum == target:
            return True

    return False


def find_subset_sum_bruteforce(
    numbers: list[int] | tuple[int, ...],
    target: int,
    timeout_seconds: float | None = None,
) -> tuple[list[int] | None, bool]:
    """Find and return a subset whose elements sum to target.

    Algorithm: Exhaustive binary mask enumeration across all 2^n subsets.

    Args:
        numbers: Sequence of input integers.
        target: Target sum to find.
        timeout_seconds: Optional timeout in seconds to prevent UI hangs.

    Returns:
        tuple (subset, timed_out):
            - subset: list of numbers summing to target, or None if no subset exists.
            - timed_out: True if execution exceeded timeout_seconds before completing search.
    """
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("numbers must be a list or tuple")

    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError("target must be an integer")

    if any(not isinstance(n, int) or isinstance(n, bool) for n in numbers):
        raise TypeError("all numbers must be integers")

    n = len(numbers)
    start_time = perf_counter()

    for mask in range(1 << n):
        if timeout_seconds is not None and (mask & 0x7FFF) == 0:
            if (perf_counter() - start_time) > timeout_seconds:
                return None, True

        current_sum = 0
        subset = []
        for i in range(n):
            if mask & (1 << i):
                current_sum += numbers[i]
                subset.append(numbers[i])

        if current_sum == target:
            return subset, False

    return None, False


def verify_subset_sum(
    numbers: list[int] | tuple[int, ...],
    subset_candidate: list[int] | tuple[int, ...],
    target: int,
) -> bool:
    """Verify in polynomial time O(n) whether a proposed subset is a valid certificate.

    This function proves membership in NP:
    Checking a candidate solution takes deterministic linear time O(n),
    even though finding it took exponential search time O(n * 2^n).
    """
    if not isinstance(numbers, (list, tuple)) or not isinstance(subset_candidate, (list, tuple)):
        raise TypeError("numbers and subset_candidate must be lists or tuples")

    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError("target must be an integer")

    if any(not isinstance(x, int) or isinstance(x, bool) for x in subset_candidate):
        raise TypeError("all candidate elements must be integers")

    # Check 1: Subset sum equals target
    if sum(subset_candidate) != target:
        return False

    # Check 2: Every element in subset_candidate exists in numbers with sufficient frequency
    available_counts = Counter(numbers)
    candidate_counts = Counter(subset_candidate)

    for val, count in candidate_counts.items():
        if available_counts[val] < count:
            return False

    return True


def benchmark_subset_sum(
    sizes: tuple[int, ...] | list[int] = DEFAULT_SUBSET_SUM_SIZES,
    trials: int = 3,
    seed: int = 42,
    timeout_seconds: float = 3.0,
) -> list[dict]:
    """Measure brute-force Subset Sum runtime in milliseconds.

    To observe true worst-case exponential growth, the target is set to
    sum(numbers) + 1 (an impossible target for positive integers), forcing
    the algorithm to explore all 2^n possible subsets.

    A safe timeout limit prevents the execution from freezing on large inputs.
    If a size exceeds timeout_seconds or was skipped due to previous timeout,
    runtime_ms is set to None.
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
    timed_out_previously = False

    for size in sizes:
        if timed_out_previously or (size > 22 and timeout_seconds <= 2.5):
            results.append({
                "n": size,
                "runtime_ms": None,
                "target": None,
                "found": False,
            })
            continue

        numbers = [rng.randint(1, 100) for _ in range(size)]
        # Impossible target forces exhaustive examination of all 2^n subsets
        target = sum(numbers) + 1

        start = perf_counter()
        found = False
        aborted = False

        for _ in range(trials):
            t_single_start = perf_counter()
            found = subset_sum_bruteforce(numbers, target)
            t_single_elapsed = perf_counter() - t_single_start
            if t_single_elapsed > timeout_seconds:
                aborted = True
                break

        total_elapsed = perf_counter() - start

        if aborted or total_elapsed > (timeout_seconds * trials):
            timed_out_previously = True
            results.append({
                "n": size,
                "runtime_ms": None,
                "target": target,
                "found": found,
            })
        else:
            elapsed_ms = (total_elapsed * 1000) / trials
            if (elapsed_ms / 1000) > timeout_seconds:
                timed_out_previously = True
            results.append({
                "n": size,
                "runtime_ms": elapsed_ms,
                "target": target,
                "found": found,
            })

    return results
