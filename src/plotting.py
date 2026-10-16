
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def plot_runtime_curves(
    results: list[dict],
    output_path: str = "outputs/runtime_growth.png",
) -> Path:
    """Plot runtime curves for algorithms and save the graph."""
    if not results:
        raise ValueError("Results cannot be empty.")

    # Validate all data before creating the plot.
    for result in results:
        if len(result["input_sizes"]) != len(result["runtime_ms"]):
            raise ValueError(
                f"Input sizes and runtimes must match for "
                f"{result['algorithm']}."
            )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    try:
        for result in results:
            ax.plot(
                result["input_sizes"],
                result["runtime_ms"],
                marker="o",
                label=result["algorithm"],
            )

        ax.set_xlabel("Input Size")
        ax.set_ylabel("Runtime (milliseconds)")
        ax.set_title("Algorithm Runtime Growth")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()
        fig.savefig(output_file)
    finally:
        plt.close(fig)
    return output_file