Theory of computation- Group 17 - Implementing Complexity class explore


# Complexity Class Explorer

A Python project demonstrating algorithmic complexity using
Merge Sort, brute-force Subset Sum, and a bounded execution
demonstration related to the Halting Problem.

## Features

- Merge Sort: O(n log n) sorting algorithm.
- Subset Sum: brute-force exponential search.
- Halting Problem: bounded execution illustration.
- Runtime plotting to compare measured algorithm performance.
- Cryptography context covering RSA factoring and password hashing.

## Requirements

Python 3.10 or later.

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run tests

```bash
python -m pytest -q
```

## Runtime plots

Benchmark results can be visualized using the plotting utility
in `src/plotting.py`. Generated plots are saved under `outputs/`.

## Limitations

Runtime measurements illustrate observed behaviour and do not
prove complexity classes or cryptographic security.
The bounded execution demo does not solve the general Halting Problem.
