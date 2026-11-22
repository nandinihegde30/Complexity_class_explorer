# Theory of Computation: Complexity Class Explorer (Group 17)

An academic and empirical exploration of computational complexity theory, covering **P**, **NP**, and **Undecidable** problems, with real-world applications in **Modern Cryptography** (RSA integer factorization and salted password hashing).

---

## 1. Project Overview

Computational complexity theory classifies computational problems based on the inherent resources (time and auxiliary space) required to solve them. This project provides:
1. **Interactive Explore Mode (`main.py`):** An intuitive CLI interface allowing users to enter custom inputs, execute algorithms, inspect outputs, and view measured execution times and complexity classifications.
2. **Automated Benchmark Mode (`src/run_benchmarks.py`):** Predefined input sizes measuring empirical runtime scaling, timeout protections, and publication-quality Matplotlib plots.
3. **Formal Computability Demonstrations:** A deterministic **Turing Machine Simulator** demonstrating step-by-step state transitions and clean halting behavior (`HALTED` / `UNKNOWN (STEP LIMIT REACHED)`), accompanied by **Turing's Diagonalization Proof** ($D(D)$).
4. **Master Jupyter Notebook (`Complexity_Class_Explorer.ipynb`):** A complete 16-section interactive deliverable with all explanations, code cells, benchmark tables, and embedded Matplotlib plots.

---

## 2. Project Objectives

- **Bridge Theory and Practice:** Connect abstract computational complexity classes (P, NP, NP-Complete, and Undecidable) with hands-on, runnable Python 3 implementations.
- **Support Dual Execution Modes:** Enable independent interactive experimentation and automated empirical benchmarking.
- **Empirical Complexity Benchmarking:** Measure real-world scaling using `time.perf_counter()` across 10 increasing input sizes.
- **Cryptographic Grounding:** Explain the foundational role of computational asymmetry in RSA public-key cryptography and salted PBKDF2 password hashing.
- **Viva and Presentation Readiness:** Provide rigorous theoretical distinctions, eliminating common misconceptions (e.g. why $P \neq NP$ alone does not guarantee cryptographic security, and why step limits never prove non-halting).

---

## 3. Technologies Used

- **Language:** Python 3 (Tested on Python 3.10, 3.11, and 3.14)
- **Data Visualization:** Matplotlib (Agg backend for headless generation; inline display in Jupyter)
- **Testing Framework:** Pytest (Comprehensive unit test suite with 68 passing tests)
- **Interactive Environment:** Jupyter Notebook (`.ipynb` nbformat v4) and Visual Studio Code

---

## 4. Explanation of Complexity Classes

| Concept | Demonstration Problem | Time Complexity | Verification Complexity | Classification | Halting Guarantee |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P** | Merge Sort | $\Theta(n \log n)$ | $O(n)$ | Tractable (Deterministic) | Guaranteed to halt in polynomial time |
| **NP** | Subset Sum (Decision) | Brute-force $O(n \cdot 2^n)$ | $O(n)$ Linear Time | NP-Complete | Guaranteed to halt in exponential time |
| **Undecidable** | Halting Problem | No general algorithm exists | Unverifiable | Undecidable | No general decider can exist |

### Key Theoretical Distinctions:
1. **Decision vs Sorting:** Formally, P and NP are classes of decision problems (yielding binary YES/NO outputs). Merge Sort is a polynomial-time sorting algorithm representing tractability in P.
2. **NP Asymmetry:** Finding a valid subset among $2^n$ candidates requires exponential brute-force search ($O(n \cdot 2^n)$). However, verifying a given subset certificate takes only linear $O(n)$ time.
3. **Step Limits in Halting:** Reaching a step limit in a Turing Machine simulation results in **UNKNOWN (STEP LIMIT REACHED)**. A finite step bound cannot distinguish slow termination from an infinite loop.
4. **Cryptography and P vs NP:** Modern cryptographic systems rely on the assumed computational hardness of specific mathematical problems. The unresolved P versus NP question alone neither establishes nor guarantees cryptographic security. In particular, integer factorization in its decision formulation is in $NP \cap \text{co-}NP$ (suspected NP-intermediate, not NP-complete).

---

## 5. Features of the Interactive Application (`main.py`)

Run the interactive application using:
```bash
python main.py
```

### Main Menu Options:
1. **P Class – Merge Sort:** Enter custom integer arrays of any size. Displays original array, sorted result, measured execution time, and $O(n \log n)$ complexity analysis.
2. **NP Class – Subset Sum:** Enter custom integer arrays and target sum. Explores subsets, displays found subset or reports no solution, validates solution via $O(n)$ polynomial verification, and warns/protects against large $n > 22$.
3. **Undecidable – Halting Problem:**
   - **Bit-Inverter Machine:** Executes transitions on a binary tape and halts at state `q_halt` -> `HALTED`.
   - **Turing's Diagonalization Proof:** Demonstrates the mathematical contradiction of the adversary machine $D(D)$.
4. **Cryptography Demonstration:**
   - **RSA Public-Key:** Key generation, encryption $c = m^e \pmod n$, decryption $m = c^d \pmod n$, and integer factorization discussion.
   - **Password Hashing:** Random salting (`secrets.token_bytes`), PBKDF2-HMAC-SHA256, constant-time verification, and work factor benchmark.
5. **Run Benchmark Analysis:** Runs full benchmark across 10 input sizes and saves plots to `outputs/`.
6. **View Complexity Concepts:** Formatted summary table for viva preparation.
7. **Exit:** Clean termination.

---

## 6. Benchmarking Functionality

The automated benchmark mode measures runtime across 10 increasing input sizes:
- **Merge Sort Sizes:** `[10, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]`
- **Subset Sum Sizes:** `[5, 8, 10, 12, 15, 18, 20, 22, 24, 26]`
- **Safe Timeout Guards:** A 2.0-second safety limit automatically skips large combinatorial sizes ($n \ge 22$) to prevent application freezes.

### Generated Visualizations (`outputs/`):
- `merge_sort_growth.png`: Polynomial $O(n \log n)$ scaling curve.
- `subset_sum_growth.png`: Exponential $O(n \cdot 2^n)$ scaling curve.
- `combined_growth.png`: Logarithmic y-axis comparison demonstrating the divergence between P and NP-Complete.

---

## 7. Installation Instructions

1. Clone or extract the project repository.
2. Open a terminal in the project root directory:
   ```bash
   cd Complexity_class_explorer-feature-final-project-setup
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 8. Execution Commands

### Launch Interactive Explorer Mode:
```bash
python main.py
```

### Run Automated Benchmark Suite:
```bash
python src/run_benchmarks.py
```

### Run Standalone Password Hashing Demo:
```bash
python src/password_hashing.py
```

### Run Standalone Interactive RSA Demo:
```bash
python RSAdemo.py
```

### Run Pytest Test Suite:
```bash
python -m pytest -v
```

### Regenerate and Re-execute Master Jupyter Notebook:
```bash
python src/generate_notebook.py
```

---

## 9. Jupyter Notebook Instructions

The primary course deliverable is **`Complexity_Class_Explorer.ipynb`**.

### Opening and Executing in VS Code:
1. Open the repository folder in VS Code.
2. Open `Complexity_Class_Explorer.ipynb`.
3. Select your Python 3 environment in the top right kernel selector.
4. Click **Run All** to execute all 16 sections sequentially.
5. All three Matplotlib plots are embedded directly as inline images inside the notebook outputs.

---

## 10. Sample Terminal Outputs

### Sample 1: Interactive Merge Sort
```text
========== MERGE SORT – P CLASS ==========

Enter array elements separated by spaces (e.g. 45 12 89 3 21 7):
> 45 12 89 3 21 7

Original Array: [45, 12, 89, 3, 21, 7]

Sorted Array:   [3, 7, 12, 21, 45, 89]

Execution Time: 0.0210 ms

Time Complexity:  O(n log n)
Space Complexity: O(n)

Explanation:
Merge Sort repeatedly divides the array into smaller
subarrays, sorts them recursively, and merges them in linear time.

Classification: P (Polynomial Time)
```

### Sample 2: Interactive Subset Sum
```text
========== SUBSET SUM – NP CLASS ==========

Enter array elements separated by spaces (e.g. 2 3 7 8 10):
> 2 3 7 8 10

Enter target sum: 11

Searching for a subset...

Subset Found: [3, 8]
Subset Sum:   11

Execution Time: 0.0380 ms

Polynomial-time Certificate Verification: True (0.0020 ms)

Time Complexity:  O(n * 2^n) for the current brute-force implementation.
Verification:     O(n) linear polynomial time given a candidate certificate.

Explanation:
The algorithm explores possible subsets to determine
whether any subset has the required target sum.

Classification:
Subset Sum Decision Problem – NP-Complete
```

### Sample 3: Interactive Halting Problem
```text
==================================================
 HALTING PROBLEM – UNDECIDABLE
==================================================

Select a Halting Problem demonstration:
1. Bit-Inverter Machine (Turing Machine Halting demonstration)
2. Turing's Diagonalization Proof (Contradiction)

Enter your choice (1-2): 1

Enter maximum execution steps (e.g. 50): 50

Executing Turing Machine...
Enter binary string tape (press Enter for default '1101'): 1101

Result:         HALTED
Steps Executed: 5
Final Tape:     BB0010BBB

Explanation:
Machine reached halting state 'q_halt' after 5 step(s).
```

---

## 11. Project Limitations and Academic Scope

1. **Empirical Measurements vs. Complexity Proofs:** Measured runtimes reflect observed execution on hardware; they illustrate theoretical scaling but do not formally prove lower bounds.
2. **Safe Timeout Guards:** For Subset Sum, input sizes $n \ge 22$ exceed practical interactive limits for single-threaded Python ($2^{22} \approx 4.19 \times 10^6$ operations). Safe timeout guards skip excessively long sizes to prevent application freezes.
3. **Educational Cryptography:** The RSA demonstration uses small primes without OAEP padding to facilitate manual inspection and mathematical comprehension during vivas. Production systems require 2048+ bit moduli, OAEP padding, and memory-hard password hashes (e.g., Argon2id).
4. **Quantum Considerations:** While classical factoring is sub-exponential, Shor's quantum algorithm factors in polynomial time $O((\log n)^3)$.
