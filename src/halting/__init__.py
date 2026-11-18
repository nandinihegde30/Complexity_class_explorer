"""Halting problem and computability theory demonstrations."""

from src.halting.turing_machine import (
    TuringMachine,
    TuringMachineResult,
    create_halting_machine,
    create_infinite_loop_machine,
    create_busy_beaver_or_counter_machine,
)
from src.halting.diagonalization import (
    HypotheticalHaltingDecider,
    DiagonalProgram,
    demonstrate_diagonalization_paradox,
)

__all__ = [
    "TuringMachine",
    "TuringMachineResult",
    "create_halting_machine",
    "create_infinite_loop_machine",
    "create_busy_beaver_or_counter_machine",
    "HypotheticalHaltingDecider",
    "DiagonalProgram",
    "demonstrate_diagonalization_paradox",
]
