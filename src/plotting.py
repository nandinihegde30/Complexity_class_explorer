"""Matplotlib plotting utilities for runtime complexity comparison.

This module visualizes:
1. Polynomial growth of Merge Sort (O(n log n)).
2. Exponential growth of brute-force Subset Sum (O(n * 2^n)).
3. Combined comparison highlighting the dramatic divergence between P and NP-complete problems.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib
import matplotlib.pyplot as plt


def _filter_valid_points(
    input_sizes: Sequence[int],
    runtimes_ms: Sequence[float | None],
) -> tuple[list[int], list[float], list[int]]:
    """Filter out timed-out (None) data points while tracking timed-out sizes."""
    valid_x = []
    valid_y = []
    timed_out_x = []

    for x, y in zip(input_sizes, runtimes_ms):
        if y is not None:
            valid_x.append(x)
            valid_y.append(float(y))
        else:
            timed_out_x.append(x)

    return valid_x, valid_y, timed_out_x


def plot_runtime_curves(
    results: list[dict],
    output_path: str = "outputs/runtime_growth.png",
    log_scale: bool = False,
    show: bool = False,
) -> Path:
    """Plot runtime curves for one or more algorithms and save the figure.

    Handles timeouts/None values gracefully and supports logarithmic y-scaling.

    Args:
        results: List of dicts, each with 'algorithm', 'input_sizes', and 'runtime_ms'.
        output_path: Destination image path.
        log_scale: If True, uses logarithmic scale on the y-axis.
        show: If True, displays the plot interactively.

    Returns:
        Path object to the saved plot image.
    """
    if not results:
        raise ValueError("Results cannot be empty.")

    for result in results:
        if len(result["input_sizes"]) != len(result["runtime_ms"]):
            raise ValueError(
                f"Input sizes and runtimes must match for {result['algorithm']}."
            )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    try:
        colors = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e"]

        for idx, result in enumerate(results):
            color = colors[idx % len(colors)]
            x_vals, y_vals, timed_out = _filter_valid_points(
                result["input_sizes"], result["runtime_ms"]
            )

            if x_vals:
                ax.plot(
                    x_vals,
                    y_vals,
                    marker="o",
                    linewidth=2,
                    markersize=6,
                    color=color,
                    label=result["algorithm"],
                )

            # Indicate timed-out points if present
            if timed_out:
                ax.scatter(
                    timed_out,
                    [max(y_vals) if y_vals else 1.0] * len(timed_out),
                    marker="x",
                    s=80,
                    color=color,
                    label=f"{result['algorithm']} (Timed Out)",
                )

        ax.set_xlabel("Input Size (n)", fontsize=11, fontweight="bold")
        ax.set_ylabel(
            "Execution Time (milliseconds)" + (" [Log Scale]" if log_scale else ""),
            fontsize=11,
            fontweight="bold",
        )
        ax.set_title("Algorithm Runtime Growth Comparison", fontsize=13, fontweight="bold")

        if log_scale:
            ax.set_yscale("log")

        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend(loc="best", fontsize=10)
        fig.tight_layout()
        fig.savefig(output_file, dpi=150)

        if show:
            plt.show()
    finally:
        plt.close(fig)

    return output_file


def plot_merge_sort_growth(
    input_sizes: Sequence[int],
    runtimes_ms: Sequence[float],
    output_path: str = "outputs/merge_sort_growth.png",
    show: bool = False,
) -> Path:
    """Plot Merge Sort's polynomial O(n log n) scaling curve."""
    data = [{
        "algorithm": "Merge Sort (P: O(n log n))",
        "input_sizes": list(input_sizes),
        "runtime_ms": list(runtimes_ms),
    }]
    return plot_runtime_curves(data, output_path=output_path, log_scale=False, show=show)


def plot_subset_sum_growth(
    input_sizes: Sequence[int],
    runtimes_ms: Sequence[float | None],
    output_path: str = "outputs/subset_sum_growth.png",
    log_scale: bool = False,
    show: bool = False,
) -> Path:
    """Plot brute-force Subset Sum's exponential O(n * 2^n) scaling curve."""
    data = [{
        "algorithm": "Brute-force Subset Sum (NP-Complete: O(n * 2^n))",
        "input_sizes": list(input_sizes),
        "runtime_ms": list(runtimes_ms),
    }]
    return plot_runtime_curves(data, output_path=output_path, log_scale=log_scale, show=show)


def plot_combined_comparison(
    merge_results: dict | list[dict],
    subset_results: dict | list[dict],
    output_path: str = "outputs/combined_growth.png",
    log_scale: bool = True,
    show: bool = False,
) -> Path:
    """Plot combined comparison graph comparing Merge Sort and Subset Sum on a log scale."""
    if isinstance(merge_results, list):
        merge_dict = {
            "algorithm": "Merge Sort (Polynomial O(n log n))",
            "input_sizes": [r["n"] for r in merge_results],
            "runtime_ms": [r["runtime_ms"] for r in merge_results],
        }
    else:
        merge_dict = merge_results

    if isinstance(subset_results, list):
        subset_dict = {
            "algorithm": "Subset Sum (Exponential O(n * 2^n))",
            "input_sizes": [r["n"] for r in subset_results],
            "runtime_ms": [r["runtime_ms"] for r in subset_results],
        }
    else:
        subset_dict = subset_results

    # Save to both combined_growth.png and runtime_growth.png for backward compatibility
    plot_runtime_curves([merge_dict, subset_dict], output_path=output_path, log_scale=log_scale, show=show)
    compat_path = Path(output_path).parent / "runtime_growth.png"
    if str(compat_path) != str(output_path):
        plot_runtime_curves([merge_dict, subset_dict], output_path=str(compat_path), log_scale=log_scale, show=False)

    return Path(output_path)
