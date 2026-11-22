"""Tests for the educational Turing Machine simulator."""

import pytest

from src.halting.turing_machine import (
    TuringMachine,
    TuringMachineResult,
    create_halting_machine,
)


def test_halting_machine_halts_and_inverts():
    """Verify that the halting machine terminates and produces correct output."""
    tm = create_halting_machine("110")
    result = tm.run(max_steps=50)

    assert isinstance(result, TuringMachineResult)
    assert result.status == "HALTED"
    assert result.is_halted is True
    assert result.steps > 0
    # Inverted 110 -> 001
    assert "001" in result.tape_content


def test_step_limit_reached_reports_unknown():
    """Crucial test: hitting max_steps before halting yields STEP_LIMIT_REACHED."""
    tm = create_halting_machine("1101")
    result = tm.run(max_steps=2)

    assert result.status == "STEP_LIMIT_REACHED"
    assert result.is_halted is False
    assert result.steps == 2
    assert "unknown" in result.explanation.lower()


def test_single_step_execution():
    """Verify step-by-step state and head tracking."""
    tm = create_halting_machine("1")
    assert tm.state == "q0"
    assert tm.head_position == 0

    can_continue = tm.step()
    assert can_continue is True
    assert tm.read_tape(0) == "0"
    assert tm.head_position == 1

    can_continue = tm.step()
    assert tm.state == "q_halt"
    # Machine is now halted
    assert tm.step() is False


def test_invalid_max_steps():
    tm = create_halting_machine("1")
    with pytest.raises(ValueError):
        tm.run(max_steps=0)
