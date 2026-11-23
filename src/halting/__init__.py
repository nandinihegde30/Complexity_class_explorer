"""Halting problem and computability theory demonstrations."""

from src.halting.turing_machine import (
    TuringMachine,
    TuringMachineResult,
    create_halting_machine,
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
    "HypotheticalHaltingDecider",
    "DiagonalProgram",
    "demonstrate_diagonalization_paradox",
]
