
from pathlib import Path

import pytest

from src.plotting import plot_runtime_curves


def test_plot_runtime_curves_creates_file(tmp_path):
    output_file = tmp_path / "runtime_growth.png"

    results = [
        {
            "algorithm": "Merge Sort",
            "input_sizes": [10, 20, 30],
            "runtime_ms": [1.0, 2.0, 4.0],
        },
        {
            "algorithm": "Subset Sum",
            "input_sizes": [10, 20, 30],
            "runtime_ms": [1.0, 3.0, 8.0],
        },
    ]

    plot_runtime_curves(results, str(output_file))

    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_plot_runtime_curves_rejects_empty_results(tmp_path):
    output_file = tmp_path / "empty.png"

    with pytest.raises(ValueError):
        plot_runtime_curves([], str(output_file))


def test_plot_runtime_curves_rejects_mismatched_lengths(tmp_path):
    results = [
        {
            "algorithm": "Example",
            "input_sizes": [10, 20],
            "runtime_ms": [1.0],
        }
    ]

    with pytest.raises(ValueError):
        plot_runtime_curves(results, str(tmp_path / "bad.png"))
