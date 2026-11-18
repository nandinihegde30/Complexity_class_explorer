"""Educational Turing Machine simulator for computability theory demonstrations.

This module models a deterministic Turing Machine with a two-way infinite tape,
a read/write tape head, discrete states, and explicit transition rules.
It illustrates why finite step-bounded simulations cannot solve the general
Halting Problem: reaching a step limit merely yields UNKNOWN (STEP_LIMIT_REACHED).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


MoveDirection = Literal["L", "R", "N"]


@dataclass
class TuringMachineResult:
    """Outcome of a Turing Machine simulation run."""

    status: str  # "HALTED", "STEP_LIMIT_REACHED", or "CYCLE_DETECTED"
    steps: int
    final_state: str
    head_position: int
    tape_content: str
    is_halted: bool
    explanation: str
    trace: list[dict] = field(default_factory=list)

    @property
    def result_category(self) -> str:
        """Return standard three-state category: HALTED, CYCLE DETECTED, or UNKNOWN (STEP LIMIT REACHED)."""
        if self.status == "HALTED":
            return "HALTED"
        elif self.status == "CYCLE_DETECTED":
            return "CYCLE DETECTED"
        elif self.status == "STEP_LIMIT_REACHED":
            return "UNKNOWN (STEP LIMIT REACHED)"
        return self.status

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "result_category": self.result_category,
            "steps": self.steps,
            "final_state": self.final_state,
            "head_position": self.head_position,
            "tape_content": self.tape_content,
            "is_halted": self.is_halted,
            "explanation": self.explanation,
        }


class TuringMachine:
    """Deterministic Turing Machine with a discrete tape and state transitions."""

    def __init__(
        self,
        initial_tape: str | list[str] | None = None,
        blank_symbol: str = "B",
        initial_state: str = "q0",
        halt_states: set[str] | list[str] | None = None,
        transitions: dict[tuple[str, str], tuple[str, str, MoveDirection]] | None = None,
    ) -> None:
        """Initialize the Turing Machine.

        Args:
            initial_tape: Initial contents of the tape starting at index 0.
            blank_symbol: Symbol representing an empty tape cell.
            initial_state: Starting state of the finite control.
            halt_states: Set of states in which the machine halts.
            transitions: Mapping (state, read_symbol) -> (next_state, write_symbol, direction).
        """
        self.blank_symbol = blank_symbol
        self.initial_state = initial_state
        self.state = initial_state
        self.head_position = 0
        self.halt_states = set(halt_states) if halt_states is not None else {"q_halt"}
        self.transitions = transitions or {}

        # Two-way infinite tape represented as a dictionary mapping index -> symbol
        self.tape: dict[int, str] = {}
        if initial_tape is not None:
            for idx, symbol in enumerate(initial_tape):
                self.tape[idx] = str(symbol)

    def read_tape(self, position: int | None = None) -> str:
        """Read the symbol at the specified position or the current head position."""
        pos = self.head_position if position is None else position
        return self.tape.get(pos, self.blank_symbol)

    def write_tape(self, symbol: str, position: int | None = None) -> None:
        """Write a symbol to the specified position or the current head position."""
        pos = self.head_position if position is None else position
        if symbol == self.blank_symbol:
            self.tape.pop(pos, None)
        else:
            self.tape[pos] = symbol

    def step(self) -> bool:
        """Execute one computational step.

        Returns:
            True if a transition was executed, False if the machine halted.
        """
        if self.state in self.halt_states:
            return False

        current_symbol = self.read_tape()
        rule = self.transitions.get((self.state, current_symbol))

        if rule is None:
            # Undefined transition: machine halts
            return False

        next_state, write_symbol, direction = rule

        # Write symbol to current cell
        self.write_tape(write_symbol)

        # Update state
        self.state = next_state

        # Move tape head
        if direction == "R":
            self.head_position += 1
        elif direction == "L":
            self.head_position -= 1
        elif direction == "N":
            pass
        else:
            raise ValueError(f"Invalid direction '{direction}'. Expected 'L', 'R', or 'N'.")

        return True

    def get_tape_window(self, padding: int = 2) -> str:
        """Return a string view of the tape around visited cells."""
        if not self.tape:
            indices = [self.head_position]
        else:
            indices = list(self.tape.keys()) + [self.head_position]

        min_idx = min(indices) - padding
        max_idx = max(indices) + padding
        symbols = [self.read_tape(i) for i in range(min_idx, max_idx + 1)]
        return "".join(symbols)

    def run(
        self,
        max_steps: int = 1000,
        detect_cycles: bool = False,
        record_trace: bool = False,
    ) -> TuringMachineResult:
        """Simulate execution up to max_steps.

        Args:
            max_steps: Maximum allowable computational steps.
            detect_cycles: If True, tracks visited configurations to detect strict cycles.
            record_trace: If True, stores step configurations for debugging.

        Returns:
            TuringMachineResult with execution status and details.
        """
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")

        seen_configurations = set()
        trace = []
        step_count = 0

        while step_count < max_steps:
            if self.state in self.halt_states:
                return TuringMachineResult(
                    status="HALTED",
                    steps=step_count,
                    final_state=self.state,
                    head_position=self.head_position,
                    tape_content=self.get_tape_window(),
                    is_halted=True,
                    explanation=f"Machine reached halting state '{self.state}' after {step_count} step(s).",
                    trace=trace,
                )

            current_symbol = self.read_tape()
            rule = self.transitions.get((self.state, current_symbol))
            if rule is None:
                return TuringMachineResult(
                    status="HALTED",
                    steps=step_count,
                    final_state=self.state,
                    head_position=self.head_position,
                    tape_content=self.get_tape_window(),
                    is_halted=True,
                    explanation=(
                        f"Machine halted at state '{self.state}' because no transition rule was defined "
                        f"for symbol '{current_symbol}'."
                    ),
                    trace=trace,
                )

            if detect_cycles:
                # Configuration is (state, head_position, frozenset of tape)
                config = (self.state, self.head_position, tuple(sorted(self.tape.items())))
                if config in seen_configurations:
                    return TuringMachineResult(
                        status="CYCLE_DETECTED",
                        steps=step_count,
                        final_state=self.state,
                        head_position=self.head_position,
                        tape_content=self.get_tape_window(),
                        is_halted=False,
                        explanation=(
                            f"Periodic repeating configuration detected at step {step_count}. "
                            f"The machine will repeat this cycle indefinitely without halting."
                        ),
                        trace=trace,
                    )
                seen_configurations.add(config)

            if record_trace:
                trace.append({
                    "step": step_count,
                    "state": self.state,
                    "head": self.head_position,
                    "symbol": current_symbol,
                })

            self.step()
            step_count += 1

        # Check if the step just taken landed in a halt state
        if self.state in self.halt_states:
            return TuringMachineResult(
                status="HALTED",
                steps=step_count,
                final_state=self.state,
                head_position=self.head_position,
                tape_content=self.get_tape_window(),
                is_halted=True,
                explanation=f"Machine reached halting state '{self.state}' exactly at step limit ({step_count}).",
                trace=trace,
            )

        # Crucial academic requirement: DO NOT claim it will never halt.
        return TuringMachineResult(
            status="STEP_LIMIT_REACHED",
            steps=step_count,
            final_state=self.state,
            head_position=self.head_position,
            tape_content=self.get_tape_window(),
            is_halted=False,
            explanation=(
                f"Simulation step limit ({max_steps}) was reached while in state '{self.state}'. "
                "The halting status is UNKNOWN: finite simulation alone cannot determine whether "
                "the machine would halt on a subsequent step or loop forever."
            ),
            trace=trace,
        )


def create_halting_machine(input_string: str = "110") -> TuringMachine:
    """Create a machine that inverts bits and halts when encountering a blank symbol.

    Example demonstration 1: A machine that halts successfully.
    """
    transitions = {
        ("q0", "1"): ("q0", "0", "R"),
        ("q0", "0"): ("q0", "1", "R"),
        ("q0", "B"): ("q_halt", "B", "N"),
    }
    return TuringMachine(
        initial_tape=input_string,
        blank_symbol="B",
        initial_state="q0",
        halt_states={"q_halt"},
        transitions=transitions,
    )


def create_infinite_loop_machine() -> TuringMachine:
    """Create a machine that oscillates endlessly between two states.

    Example demonstration 2: A machine that enters a non-halting cycle.
    q0 at position 0 writes 'X', moves Right to position 1 -> state q1.
    q1 at position 1 writes 'Y', moves Left to position 0 -> state q0.
    """
    transitions = {
        ("q0", "B"): ("q1", "X", "R"),
        ("q0", "X"): ("q1", "X", "R"),
        ("q0", "Y"): ("q1", "X", "R"),
        ("q1", "B"): ("q0", "Y", "L"),
        ("q1", "X"): ("q0", "Y", "L"),
        ("q1", "Y"): ("q0", "Y", "L"),
    }
    return TuringMachine(
        initial_tape=None,
        blank_symbol="B",
        initial_state="q0",
        halt_states={"q_halt"},
        transitions=transitions,
    )


def create_busy_beaver_or_counter_machine() -> TuringMachine:
    """Create a machine that increments a tape counter and continues moving right.

    Example demonstration 3: Reaches step limit and yields UNKNOWN / STEP_LIMIT_REACHED.
    """
    transitions = {
        ("q0", "B"): ("q0", "1", "R"),
        ("q0", "1"): ("q0", "1", "R"),
    }
    return TuringMachine(
        initial_tape=None,
        blank_symbol="B",
        initial_state="q0",
        halt_states={"q_halt"},
        transitions=transitions,
    )
