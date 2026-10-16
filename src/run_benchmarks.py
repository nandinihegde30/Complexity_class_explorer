
from src.merge_sort import benchmark_merge_sort
from src.subset_sum import benchmark_subset_sum
from src.plotting import plot_runtime_curves


def main():
    # Use identical input sizes for both algorithms.
    sizes = (5, 10, 15, 20)

    merge_results = benchmark_merge_sort(sizes=sizes)
    subset_results = benchmark_subset_sum(sizes=sizes)

    # Convert benchmark outputs into the plotting function's format.
    results = [
        {
            "algorithm": "Merge Sort",
            "input_sizes": [row["n"] for row in merge_results],
            "runtime_ms": [row["runtime_ms"] for row in merge_results],
        },
        {
            "algorithm": "Brute-force Subset Sum",
            "input_sizes": [row["n"] for row in subset_results],
            "runtime_ms": [row["runtime_ms"] for row in subset_results],
        },
    ]

    output_path = plot_runtime_curves(results)
    print(f"Runtime graph saved to: {output_path}")


if __name__ == "__main__":
    main()
