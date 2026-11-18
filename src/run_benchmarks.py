"""Comprehensive benchmarking suite for Complexity Class Explorer.

Benchmarks:
1. Merge Sort (Polynomial O(n log n)) across 10 input sizes.
2. Brute-Force Subset Sum (Exponential O(n * 2^n)) across 10 input sizes with safe timeout.
3. Turing Machine Halting Problem step observation (illustrating undecidability).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is on sys.path for direct script execution
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from typing import Sequence

from src.merge_sort import benchmark_merge_sort, DEFAULT_MERGE_SORT_SIZES
from src.subset_sum import benchmark_subset_sum, DEFAULT_SUBSET_SUM_SIZES
from src.halting.turing_machine import (
    create_halting_machine,
    create_infinite_loop_machine,
    create_busy_beaver_or_counter_machine,
)
from src.plotting import (
    plot_merge_sort_growth,
    plot_subset_sum_growth,
    plot_combined_comparison,
)


def display_results_table(title: str, results: Sequence[dict]) -> None:
    """Print benchmark data in a clean formatted ASCII table."""
    print(f"\n{'=' * 65}")
    print(f" {title}")
    print(f"{'=' * 65}")

    header = f"{'Input Size (n)':<16} | {'Runtime (ms)':<18} | {'Status / Notes':<24}"
    print(header)
    print("-" * 65)

    for row in results:
        n_val = row.get("n", "N/A")
        runtime = row.get("runtime_ms")

        if runtime is not None:
            time_str = f"{runtime:.4f} ms"
            status = "Completed"
        else:
            time_str = "Timed out / Skipped"
            status = "Exceeded safe limit"

        if "found" in row and row["found"] is not None:
            status += f" (Found: {row['found']})"

        print(f"{str(n_val):<16} | {time_str:<18} | {status:<24}")

    print("-" * 65)


def run_turing_machine_observations() -> list[dict]:
    """Execute selected Turing Machine configurations and inspect step counts.

    Academic Note:
    Unlike sorting or subset sum, undecidable problems have NO general runtime complexity.
    Observing finite steps for particular instances cannot establish whether an
    arbitrary machine will halt.
    """
    observations = []

    # Machine 1: Guaranteed to halt
    tm_halt = create_halting_machine("1101")
    res_halt = tm_halt.run(max_steps=100)
    observations.append({
        "machine": "Bit-Inverter Machine (Halting)",
        "input_tape": "1101",
        "max_steps": 100,
        "steps_taken": res_halt.steps,
        "status": res_halt.status,
        "is_halted": res_halt.is_halted,
        "note": "Halted normally upon scanning blank cell.",
    })

    # Machine 2: Infinite oscillating cycle
    tm_loop = create_infinite_loop_machine()
    res_loop = tm_loop.run(max_steps=50, detect_cycles=True)
    observations.append({
        "machine": "Ping-Pong Oscillating Machine (Cycle)",
        "input_tape": "Empty",
        "max_steps": 50,
        "steps_taken": res_loop.steps,
        "status": res_loop.status,
        "is_halted": res_loop.is_halted,
        "note": "Infinite periodic cycle detected via state memory.",
    })

    # Machine 3: Counter reaching step limit
    tm_counter = create_busy_beaver_or_counter_machine()
    res_counter = tm_counter.run(max_steps=25)
    observations.append({
        "machine": "Unary Counter Machine (Step Bound)",
        "input_tape": "Empty",
        "max_steps": 25,
        "steps_taken": res_counter.steps,
        "status": res_counter.status,
        "is_halted": res_counter.is_halted,
        "note": "Step limit reached. Status is UNKNOWN (cannot decide infinite loop).",
    })

    return observations


def display_turing_observations(observations: list[dict]) -> None:
    """Print Turing Machine simulation results with distinct three-category outcomes."""
    print(f"\n{'=' * 80}")
    print(" TURING MACHINE SIMULATOR: HALTING PROBLEM DEMONSTRATIONS")
    print(f"{'=' * 80}")
    print(
        f"{'Machine Name':<35} | {'Steps':<8} | {'Result Category':<32}"
    )
    print("-" * 80)
    for obs in observations:
        # Map to the 3 required categories
        status = obs["status"]
        if status == "HALTED":
            category = "HALTED"
        elif status == "CYCLE_DETECTED":
            category = "CYCLE DETECTED"
        else:
            category = "UNKNOWN (STEP LIMIT REACHED)"

        print(
            f"{obs['machine'][:35]:<35} | {obs['steps_taken']:<8} | {category:<32}"
        )
    print("-" * 80)
    print("Key Theoretical Insight:")
    print("  1. When a machine enters its halting state, we know it HALTED.")
    print("  2. When periodic state cycle is detected, CYCLE DETECTED proves non-halting.")
    print("  3. When step limit is reached, result is UNKNOWN (STEP LIMIT REACHED).")
    print("     A finite step limit NEVER proves that the machine will never halt.")


def run_all_benchmarks(
    merge_sizes: Sequence[int] = DEFAULT_MERGE_SORT_SIZES,
    subset_sizes: Sequence[int] = DEFAULT_SUBSET_SUM_SIZES,
    output_dir: str = "outputs",
    subset_timeout_sec: float = 2.0,
) -> dict:
    """Run all benchmarks, generate plots, and return structured results."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print("Running Merge Sort Benchmark (P)...")
    merge_results = benchmark_merge_sort(sizes=merge_sizes, trials=3, seed=42)
    display_results_table("MERGE SORT BENCHMARK (P: O(n log n))", merge_results)

    print("\nRunning Brute-force Subset Sum Benchmark (NP-Complete)...")
    subset_results = benchmark_subset_sum(
        sizes=subset_sizes,
        trials=1,
        seed=42,
        timeout_seconds=subset_timeout_sec,
    )
    display_results_table("SUBSET SUM BENCHMARK (NP: O(n * 2^n))", subset_results)

    print("\nRunning Turing Machine Halting Observations (Undecidable)...")
    tm_observations = run_turing_machine_observations()
    display_turing_observations(tm_observations)

    # Generate the 3 required plots
    merge_plot = plot_merge_sort_growth(
        input_sizes=[r["n"] for r in merge_results],
        runtimes_ms=[r["runtime_ms"] for r in merge_results],
        output_path=f"{output_dir}/merge_sort_growth.png",
    )

    subset_plot = plot_subset_sum_growth(
        input_sizes=[r["n"] for r in subset_results],
        runtimes_ms=[r["runtime_ms"] for r in subset_results],
        output_path=f"{output_dir}/subset_sum_growth.png",
        log_scale=False,
    )

    combined_plot = plot_combined_comparison(
        merge_results=merge_results,
        subset_results=subset_results,
        output_path=f"{output_dir}/combined_growth.png",
        log_scale=True,
    )

    return {
        "merge_sort": merge_results,
        "subset_sum": subset_results,
        "turing_observations": tm_observations,
        "plot_paths": {
            "merge_sort": str(merge_plot),
            "subset_sum": str(subset_plot),
            "combined": str(combined_plot),
        },
    }


def main():
    print("Starting Complexity Class Explorer Benchmark Suite...")
    benchmark_data = run_all_benchmarks()
    print("\n===== ALL BENCHMARKS COMPLETED SUCCESSFULLY =====")
    for name, path in benchmark_data["plot_paths"].items():
        print(f"Generated Plot [{name}]: {path}")


if __name__ == "__main__":
    main()
