"""Collatz conjecture bounded execution demo (optional mathematical illustration).

Note on Computability Theory:
The Collatz (3n + 1) process is an unsolved mathematical conjecture.
While observing that a sequence has not reached 1 within a finite step limit
illustrates bounded execution, it is an empirical heuristic and NOT a formal
demonstration of the Halting Problem or undecidability.

For the formal computability theory demonstrations, see:
- src.halting.turing_machine: Turing Machine simulation and step-limit UNKNOWN behavior.
- src.halting.diagonalization: Turing's Diagonalization Proof by contradiction.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Retained for backwards compatibility and educational comparison
from src.halting.turing_machine import (
    TuringMachine,
    create_halting_machine,
    create_infinite_loop_machine,
    create_busy_beaver_or_counter_machine,
)
from src.halting.diagonalization import (
    demonstrate_diagonalization_paradox,
)

START_NUMBER = 27


def halting_problem_explanation() -> str:
    """Explain why the Halting Problem is undecidable."""
    return (
        "The Halting Problem asks whether a program will stop "
        "or run forever for a given input. Alan Turing proved "
        "that no algorithm can correctly answer this for every "
        "possible program and input. Therefore, the Halting "
        "Problem is undecidable. If a program does not stop "
        "within a fixed step limit, we cannot conclude that "
        "it will run forever."
    )


def run_bounded_demo(max_steps=10, start_number=START_NUMBER):
    """Run the Collatz process for a limited number of steps.

    Note: This is an empirical illustration of bounded execution on a mathematical sequence,
    not a proof of undecidability.
    """
    if type(start_number) is not int:
        raise TypeError("Starting number must be an integer")

    if start_number < 1:
        raise ValueError("Starting number must be positive")

    if type(max_steps) is not int:
        raise TypeError("max_steps must be an integer")

    if max_steps < 1:
        raise ValueError("max_steps must be at least 1")

    n = start_number
    steps = 0

    while n != 1 and steps < max_steps:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1

        steps += 1
        print(f"Step {steps}: {n}")

    if n == 1:
        status = "stopped_within_bound"
    else:
        status = "bound_exhausted"

    print(f"\nStatus: {status}")
    print(f"Total steps: {steps}")

    return {"status": status, "steps": steps}


if __name__ == "__main__":
    print(halting_problem_explanation())
    number = int(input("\nEnter starting number: "))
    limit = int(input("Enter maximum steps: "))
    run_bounded_demo(max_steps=limit, start_number=number)
