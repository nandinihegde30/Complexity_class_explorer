"""Interactive Explore Mode for Complexity Class Explorer.

Provides a terminal menu-driven interface allowing users to experiment with:
1. P Class (Merge Sort)
2. NP Class (Subset Sum)
3. Undecidable (Turing Machine Halting & Diagonalization)
4. Cryptography (RSA & Password Hashing)
5. Automated Benchmarking
6. Complexity Concepts Overview
"""

from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from RSAdemo import generate_keys, encrypt, decrypt
from src.crypto_context import crypto_context
from src.halting.diagonalization import demonstrate_diagonalization_paradox
from src.halting.turing_machine import (
    create_halting_machine,
    create_infinite_loop_machine,
    create_busy_beaver_or_counter_machine,
)
from src.merge_sort import merge_sort
from src.password_hashing import (
    hash_password,
    verify_password,
    benchmark_work_factors,
)
from src.run_benchmarks import run_all_benchmarks
from src.subset_sum import find_subset_sum_bruteforce, verify_subset_sum


def print_header(title: str) -> None:
    print(f"\n{'=' * 50}")
    print(f" {title}")
    print(f"{'=' * 50}\n")


def prompt_integers(prompt_text: str) -> list[int] | None:
    """Prompt the user for space-separated integers with thorough validation."""
    raw = input(prompt_text).strip()
    if not raw:
        print("Error: Input cannot be empty. Please enter integers.")
        return None

    tokens = raw.split()
    numbers = []
    for token in tokens:
        try:
            numbers.append(int(token))
        except ValueError:
            print(f"Error: '{token}' is not a valid integer.")
            return None
    return numbers


def run_merge_sort_interactive() -> None:
    """Mode 1A: Interactive Merge Sort (P)."""
    print_header("MERGE SORT – P CLASS")

    print("Enter array elements separated by spaces (e.g. 45 12 89 3 21 7):")
    numbers = prompt_integers("> ")
    if numbers is None:
        return

    print(f"\nOriginal Array: {numbers}")

    # Measure real execution time
    t0 = perf_counter()
    sorted_array = merge_sort(numbers)
    elapsed_ms = (perf_counter() - t0) * 1000

    print(f"\nSorted Array:   {sorted_array}")
    print(f"\nExecution Time: {elapsed_ms:.4f} ms")
    print("\nTime Complexity:  O(n log n)")
    print("Space Complexity: O(n)")
    print("\nExplanation:")
    print("Merge Sort repeatedly divides the array into smaller")
    print("subarrays, sorts them recursively, and merges them in linear time.")
    print("\nClassification: P (Polynomial Time)")


def run_subset_sum_interactive() -> None:
    """Mode 1B: Interactive Subset Sum (NP-Complete)."""
    print_header("SUBSET SUM – NP CLASS")

    print("Enter array elements separated by spaces (e.g. 2 3 7 8 10):")
    numbers = prompt_integers("> ")
    if numbers is None:
        return

    target_raw = input("\nEnter target sum: ").strip()
    try:
        target = int(target_raw)
    except ValueError:
        print(f"Error: '{target_raw}' is not a valid integer.")
        return

    # Warning for large input size to prevent freezing
    n = len(numbers)
    if n > 22:
        print(f"\nWarning: Input size n={n} requires searching up to {2**n:,} subsets.")
        print("Brute-force exploration may take a long time on your machine.")
        confirm = input("Do you wish to proceed? (y/n, default n): ").strip().lower()
        if confirm != "y":
            print("Subset Sum search aborted by user.")
            return

    print("\nSearching for a subset...")
    t0 = perf_counter()
    # Apply a safe 5.0 second timeout
    subset, timed_out = find_subset_sum_bruteforce(numbers, target, timeout_seconds=5.0)
    elapsed_ms = (perf_counter() - t0) * 1000

    if timed_out:
        print(f"\nSearch TIMED OUT after {elapsed_ms:.2f} ms (safe 5.0s limit reached).")
        print("The search was halted to prevent freezing the application.")
    elif subset is not None:
        print(f"\nSubset Found: {subset}")
        print(f"Subset Sum:   {sum(subset)}")
        print(f"\nExecution Time: {elapsed_ms:.4f} ms")

        # Demonstrate polynomial-time verification
        t_verify = perf_counter()
        is_verified = verify_subset_sum(numbers, subset, target)
        verify_ms = (perf_counter() - t_verify) * 1000
        print(f"\nPolynomial-time Certificate Verification: {is_verified} ({verify_ms:.4f} ms)")
    else:
        print(f"\nNo subset found summing to target {target}.")
        print(f"Subsets Explored: {2**n:,}")
        print(f"Execution Time:   {elapsed_ms:.4f} ms")

    print("\nTime Complexity:  O(n * 2^n) for the current brute-force implementation.")
    print("Verification:     O(n) linear polynomial time given a candidate certificate.")
    print("\nExplanation:")
    print("The algorithm explores possible subsets to determine")
    print("whether any subset has the required target sum.")
    print("\nClassification:")
    print("Subset Sum Decision Problem – NP-Complete")


def run_halting_interactive() -> None:
    """Mode 1C: Interactive Turing Machine & Halting Problem (Undecidable)."""
    print_header("HALTING PROBLEM – UNDECIDABLE")

    print("Select a Turing Machine demonstration:")
    print("1. Bit-Inverter Machine (Halting demonstration)")
    print("2. Ping-Pong Oscillating Machine (Cycle demonstration)")
    print("3. Unary Counter Machine (Step-limit demonstration)")
    print("4. Turing's Diagonalization Proof (Contradiction)")

    choice = input("\nEnter your choice (1-4): ").strip()
    if choice not in ("1", "2", "3", "4"):
        print("Invalid choice. Returning to menu.")
        return

    if choice == "4":
        print_header("TURING'S DIAGONALIZATION PROOF")
        demo = demonstrate_diagonalization_paradox()
        print("[Hypothesis A: Assume H(D, D) predicts 'HALTS']")
        print("  Premise:       ", demo["hypothesis_halts"]["assumption"])
        print("  Action of D(D):", demo["hypothesis_halts"]["d_behavior"])
        print("  Contradiction: ", demo["hypothesis_halts"]["contradiction"])
        print("\n[Hypothesis B: Assume H(D, D) predicts 'LOOPS_FOREVER']")
        print("  Premise:       ", demo["hypothesis_loops"]["assumption"])
        print("  Action of D(D):", demo["hypothesis_loops"]["d_behavior"])
        print("  Contradiction: ", demo["hypothesis_loops"]["contradiction"])
        print("\n[Mathematical Conclusion]")
        print(" ", demo["mathematical_conclusion"])
        return

    steps_raw = input("\nEnter maximum execution steps (e.g. 50): ").strip()
    try:
        max_steps = int(steps_raw)
        if max_steps < 1:
            print("Steps must be a positive integer.")
            return
    except ValueError:
        print(f"Error: '{steps_raw}' is not a valid integer.")
        return

    print("\nExecuting Turing Machine...")

    if choice == "1":
        # Halting machine
        tape_in = input("Enter binary string tape (press Enter for default '1101'): ").strip()
        if not tape_in:
            tape_in = "1101"
        tm = create_halting_machine(tape_in)
        res = tm.run(max_steps=max_steps)
        print(f"\nResult:         {res.result_category}")
        print(f"Steps Executed: {res.steps}")
        print(f"Final Tape:     {res.tape_content}")
        print(f"\nExplanation:\n{res.explanation}")

    elif choice == "2":
        # Oscillating cycle
        tm = create_infinite_loop_machine()
        res = tm.run(max_steps=max_steps, detect_cycles=True)
        print(f"\nResult:         {res.result_category}")
        print(f"Steps Executed: {res.steps}")
        print(f"\nExplanation:\n{res.explanation}")

    elif choice == "3":
        # Step limit reached
        tm = create_busy_beaver_or_counter_machine()
        res = tm.run(max_steps=max_steps, detect_cycles=False)
        print(f"\nResult:         {res.result_category}")
        print(f"Steps Executed: {res.steps}")
        print(f"\nExplanation:\n{res.explanation}")


def run_crypto_interactive() -> None:
    """Mode 1D: Interactive Cryptography (RSA & Password Hashing)."""
    print_header("CRYPTOGRAPHY DEMONSTRATION")

    print("1. RSA Public-Key Encryption & Decryption")
    print("2. Password Hashing (PBKDF2-HMAC-SHA256)")
    print("3. Return to Main Menu")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        print_header("RSA PUBLIC-KEY CRYPTOGRAPHY")
        p, q = 61, 53
        pub_key, priv_key, phi = generate_keys(p, q)
        e, n = pub_key
        d, _ = priv_key

        print(f"Educational Key Setup:")
        print(f"Primes:             p = {p}, q = {q}")
        print(f"Modulus:            n = p * q = {n}")
        print(f"Euler's Totient:    phi(n) = (p-1)*(q-1) = {phi}")
        print(f"Public Key (e, n):  ({e}, {n})")
        print(f"Private Key (d, n): ({d}, {n})")

        msg_raw = input(f"\nEnter a numeric message between 0 and {n-1} (e.g. 42): ").strip()
        try:
            message = int(msg_raw)
            if not 0 <= message < n:
                print(f"Error: Message must be between 0 and {n-1}.")
                return
        except ValueError:
            print(f"Error: '{msg_raw}' is not a valid integer.")
            return

        ciphertext = encrypt(message, pub_key)
        decrypted = decrypt(ciphertext, priv_key)

        print(f"\nOriginal Message:   {message}")
        print(f"Encrypted Cipher:   {ciphertext}")
        print(f"Decrypted Message:  {decrypted}")
        print(f"Success:            {message == decrypted}")
        print("\nTheoretical Note:")
        print("Factoring n into p and q is hard for large numbers (sub-exponential GNFS),")
        print("while modular exponentiation requires a polynomial number of bit operations in the size of the modulus under standard arithmetic models.")
        print("Note: Small-prime RSA without OAEP padding is for educational teaching only.")

    elif choice == "2":
        print_header("PASSWORD HASHING (PBKDF2-HMAC-SHA256)")
        pwd = input("Enter sample password (press Enter for 'CorrectHorseBatteryStaple!'): ").strip()
        if not pwd:
            pwd = "CorrectHorseBatteryStaple!"

        # Hash with fresh salt
        hashed = hash_password(pwd, iterations=100_000)
        print(f"\nPassword:              [PROTECTED - length {len(pwd)}]")
        print(f"Salt (Hex):            {hashed['salt_hex']}")
        print(f"Work Factor (Iters):   {hashed['iterations']:,}")
        print(f"Derived Key (Hex):     {hashed['hash_hex'][:32]}... (truncated)")

        # Verify correct password
        ok = verify_password(pwd, hashed["hash_hex"], hashed["salt_hex"], hashed["iterations"])
        print(f"\nVerification with Correct Password: {ok}")

        # Verify wrong password
        wrong_pwd = pwd + "_wrong"
        bad = verify_password(wrong_pwd, hashed["hash_hex"], hashed["salt_hex"], hashed["iterations"])
        print(f"Verification with Wrong Password:   {bad}")

        print("\nWork Factor Benchmark (Cost Scaling):")
        wf_results = benchmark_work_factors(pwd, iteration_counts=(10_000, 50_000, 100_000))
        for r in wf_results:
            print(f"  {r['iterations']:<8,} iterations -> {r['time_ms']:.2f} ms")

        print("\nTheoretical Note:")
        print("Password hashing is a one-way (irreversible) function with a tunable cost.")
        print("Encryption is a two-way (reversible) operation using a key.")


def run_benchmark_mode() -> None:
    """Mode 2: Automated Benchmark Analysis."""
    print_header("AUTOMATED BENCHMARK ANALYSIS")
    print("Running Merge Sort, Subset Sum, and Halting Problem observations...")
    results = run_all_benchmarks()
    print("\nBenchmark completed successfully.")
    print("Generated graphs saved to:")
    for key, path in results["plot_paths"].items():
        print(f"  - {key}: {path}")


def view_complexity_concepts() -> None:
    """Display complexity theory summary table and concepts."""
    print_header("COMPLEXITY CONCEPTS OVERVIEW")
    print(f"{'Concept':<14} | {'Representative Demo':<24} | {'Complexity Model':<20}")
    print("-" * 65)
    print(f"{'P':<14} | {'Merge Sort':<24} | {'O(n log n) [Polynomial]'}")
    print(f"{'NP':<14} | {'Subset Sum':<24} | {'O(n * 2^n) [Brute-force]'}")
    print(f"{'NP Verification':<14} | {'Certificate Check':<24} | {'O(n) [Linear Time]'}")
    print(f"{'Undecidable':<14} | {'Halting Problem':<24} | {'No algorithm exists'}")
    print("-" * 65)
    print("\nKey Theoretical Takeaways:")
    print("1. P contains problems solvable in polynomial time.")
    print("2. NP contains problems verifiable in polynomial time.")
    print("3. P vs NP asks whether every verifiable problem is efficiently solvable.")
    print("4. Undecidable problems cannot be decided by any general Turing Machine.")
    print("5. Modern cryptographic systems rely on the assumed computational hardness of specific mathematical problems.")
    print("   The unresolved P versus NP question alone neither establishes nor guarantees cryptographic security.")
    print("6. Integer factorization in its decision formulation is in NP and co-NP (suspected NP-intermediate, not NP-complete).")


def main_interactive_menu() -> None:
    """Main interactive menu loop."""
    while True:
        print("\n" + "=" * 49)
        print("             COMPLEXITY CLASS EXPLORER           ")
        print("=" * 49)
        print("\nExplore computational complexity through")
        print("interactive algorithm demonstrations.\n")
        print("1. P Class – Merge Sort")
        print("2. NP Class – Subset Sum")
        print("3. Undecidable – Halting Problem")
        print("4. Cryptography Demonstration")
        print("5. Run Benchmark Analysis")
        print("6. View Complexity Concepts")
        print("7. Exit\n")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            run_merge_sort_interactive()
        elif choice == "2":
            run_subset_sum_interactive()
        elif choice == "3":
            run_halting_interactive()
        elif choice == "4":
            run_crypto_interactive()
        elif choice == "5":
            run_benchmark_mode()
        elif choice == "6":
            view_complexity_concepts()
        elif choice == "7":
            print("\nThank you for exploring Complexity Class Explorer. Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please select an option from 1 to 7.")

        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main_interactive_menu()
