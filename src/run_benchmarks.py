
from src.merge_sort import benchmark_merge_sort
from src.subset_sum import benchmark_subset_sum
from src.plotting import plot_runtime_curves


def display_results(name, results):
    print(f"\n===== {name} BENCHMARK =====")

    for row in results:
        print(f"Input Size: {row['n']}")
        print(f"Execution Time: {row['runtime_ms']:.4f} ms")

        if "found" in row:
            print(f"Target: {row['target']}")
            print(f"Subset Found: {row['found']}")

        print("-" * 35)


def main():

    sizes = (5, 10, 15, 20)

    print("Starting Algorithm Benchmarking...")

    # Run Merge Sort benchmark
    merge_results = benchmark_merge_sort(sizes=sizes)
    display_results("MERGE SORT", merge_results)

    # Run Subset Sum benchmark
    subset_results = benchmark_subset_sum(sizes=sizes)
    display_results("SUBSET SUM", subset_results)

    # Prepare data for plotting
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

    # Generate graph
    output_path = plot_runtime_curves(results)

    print("\n===== BENCHMARK COMPLETED =====")
    print(f"Graph saved successfully: {output_path}")


if __name__ == "__main__":
    main()
