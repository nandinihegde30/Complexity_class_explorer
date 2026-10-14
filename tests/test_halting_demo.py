
import pytest

from src.halting_demo import (
    halting_problem_explanation,
    run_bounded_demo,
)


def test_explanation_is_not_empty():
    text = halting_problem_explanation()
    assert isinstance(text, str)
    assert len(text.strip()) > 0
    assert "undecidable" in text.lower()


def test_result_has_correct_keys():
    result = run_bounded_demo()
    assert "status" in result
    assert "steps" in result


def test_default_bound_runs_out():
    result = run_bounded_demo()
    assert result["status"] == "bound_exhausted"
    assert result["steps"] == 10


def test_big_bound_stops():
    result = run_bounded_demo(1000)
    assert result["status"] == "stopped_within_bound"
    assert result["steps"] == 111


def test_boundary_values():
    assert run_bounded_demo(111)["status"] == "stopped_within_bound"
    assert run_bounded_demo(110)["status"] == "bound_exhausted"


def test_status_and_steps_are_valid():
    for bound in [1, 5, 50, 111, 500]:
        result = run_bounded_demo(bound)
        assert result["status"] in [
            "stopped_within_bound",
            "bound_exhausted",
        ]
        assert result["steps"] <= bound


def test_invalid_step_limits():
    with pytest.raises(ValueError):
        run_bounded_demo(0)

    with pytest.raises(ValueError):
        run_bounded_demo(-5)


def test_wrong_type():
    for value in ["10", 2.5, True]:
        with pytest.raises(TypeError):
            run_bounded_demo(value)
