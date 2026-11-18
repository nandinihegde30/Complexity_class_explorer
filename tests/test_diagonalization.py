"""Tests for the educational Diagonalization Proof demonstration."""

import pytest

from src.halting.diagonalization import (
    HypotheticalHaltingDecider,
    DiagonalProgram,
    demonstrate_diagonalization_paradox,
)


def test_hypothetical_decider_modes():
    h_halts = HypotheticalHaltingDecider(mode="HALTS")
    assert h_halts.predict("D", "D") == "HALTS"

    h_loops = HypotheticalHaltingDecider(mode="LOOPS_FOREVER")
    assert h_loops.predict("D", "D") == "LOOPS_FOREVER"

    with pytest.raises(ValueError):
        HypotheticalHaltingDecider(mode="INVALID_MODE")  # type: ignore


def test_diagonal_program_inversion():
    """Verify that program D strictly inverts H's prediction."""
    h_halts = HypotheticalHaltingDecider(mode="HALTS")
    d1 = DiagonalProgram(h_halts)
    res1 = d1.evaluate_behavior("D")
    assert res1["h_prediction"] == "HALTS"
    assert res1["d_actual_action"] == "LOOPS_FOREVER"
    assert res1["contradiction_found"] is True

    h_loops = HypotheticalHaltingDecider(mode="LOOPS_FOREVER")
    d2 = DiagonalProgram(h_loops)
    res2 = d2.evaluate_behavior("D")
    assert res2["h_prediction"] == "LOOPS_FOREVER"
    assert res2["d_actual_action"] == "HALTS"
    assert res2["contradiction_found"] is True


def test_demonstrate_diagonalization_paradox():
    """Verify complete paradox structure and conclusion."""
    demo = demonstrate_diagonalization_paradox()

    assert "hypothesis_halts" in demo
    assert "hypothesis_loops" in demo
    assert "mathematical_conclusion" in demo

    assert "contradiction" in demo["hypothesis_halts"]["contradiction"].lower()
    assert "contradiction" in demo["hypothesis_loops"]["contradiction"].lower()
    assert "undecidable" in demo["mathematical_conclusion"].lower()
