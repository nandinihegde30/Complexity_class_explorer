"""Educational demonstration of Turing's Diagonalization Proof for the Halting Problem.

This module models the classic proof by contradiction:
1. Assume there exists a hypothetical decider H(P, I) that correctly determines
   whether any program P halts on input I.
2. Construct a diagonal program D(P):
   - Query H(P, P).
   - If H predicts that P(P) halts, D enters an infinite loop.
   - If H predicts that P(P) loops forever, D halts immediately.
3. Consider the self-referential case D(D):
   - If H predicts D(D) halts -> D(D) loops forever (Contradiction).
   - If H predicts D(D) loops -> D(D) halts (Contradiction).
4. Conclusion: Such an algorithm H cannot exist. The Halting Problem is undecidable.
"""

from __future__ import annotations

from typing import Literal


Prediction = Literal["HALTS", "LOOPS_FOREVER"]


class HypotheticalHaltingDecider:
    """Represents the hypothetical machine H assumed in the proof by contradiction.

    This class serves as an educational model. It does not attempt to solve the
    halting problem, but illustrates the theoretical oracle whose existence is refuted.
    """

    def __init__(self, mode: Prediction = "HALTS") -> None:
        """Initialize with an assumed prediction mode for D(D).

        Args:
            mode: Assumed verdict ("HALTS" or "LOOPS_FOREVER") for self-reference.
        """
        if mode not in ("HALTS", "LOOPS_FOREVER"):
            raise ValueError("Mode must be 'HALTS' or 'LOOPS_FOREVER'.")
        self.assumed_prediction = mode

    def predict(self, program_name: str, input_data: str) -> Prediction:
        """Hypothetical prediction of whether program_name halts on input_data."""
        # For the self-referential paradox D(D), return the assumed hypothesis
        if program_name == "D" and input_data == "D":
            return self.assumed_prediction
        # Other arbitrary programs (for illustration)
        return "HALTS"


class DiagonalProgram:
    """The diagonal program D constructed specifically to invert H's prediction."""

    def __init__(self, decider: HypotheticalHaltingDecider) -> None:
        self.decider = decider

    def evaluate_behavior(self, program_name: str) -> dict:
        """Simulate the behavioral logic of D on program_name.

        Educational simulation: does NOT run real infinite loops.
        """
        # Step 1: D asks H what P(P) does
        prediction = self.decider.predict(program_name, program_name)

        # Step 2: D does the exact opposite of H's prediction
        if prediction == "HALTS":
            actual_action = "LOOPS_FOREVER"
            contradiction_note = (
                "H predicted HALTS, so D intentionally loops forever. "
                "Prediction was WRONG."
            )
        else:
            actual_action = "HALTS"
            contradiction_note = (
                "H predicted LOOPS_FOREVER, so D intentionally halts immediately. "
                "Prediction was WRONG."
            )

        return {
            "program_analyzed": program_name,
            "h_prediction": prediction,
            "d_actual_action": actual_action,
            "contradiction_found": prediction != actual_action,
            "note": contradiction_note,
        }


def demonstrate_diagonalization_paradox() -> dict:
    """Systematically evaluate both hypothetical cases to demonstrate the proof.

    Returns:
        Structured dictionary explaining the proof steps and contradictions.
    """
    results = {}

    # Case 1: Assume H predicts D(D) HALTS
    h_case1 = HypotheticalHaltingDecider(mode="HALTS")
    d_case1 = DiagonalProgram(h_case1)
    res_case1 = d_case1.evaluate_behavior("D")
    results["hypothesis_halts"] = {
        "assumption": "Suppose H(D, D) returns 'HALTS'.",
        "d_behavior": "By definition, D reads 'HALTS' and enters an infinite loop.",
        "actual_result": res_case1["d_actual_action"],
        "contradiction": (
            "Contradiction: H claimed D(D) halts, but D(D) runs forever! "
            "Therefore H failed."
        ),
    }

    # Case 2: Assume H predicts D(D) LOOPS_FOREVER
    h_case2 = HypotheticalHaltingDecider(mode="LOOPS_FOREVER")
    d_case2 = DiagonalProgram(h_case2)
    res_case2 = d_case2.evaluate_behavior("D")
    results["hypothesis_loops"] = {
        "assumption": "Suppose H(D, D) returns 'LOOPS_FOREVER'.",
        "d_behavior": "By definition, D reads 'LOOPS_FOREVER' and terminates immediately.",
        "actual_result": res_case2["d_actual_action"],
        "contradiction": (
            "Contradiction: H claimed D(D) loops forever, but D(D) halted! "
            "Therefore H failed."
        ),
    }

    results["mathematical_conclusion"] = (
        "In both logically possible cases, H is proven wrong about D(D). "
        "Because H was defined as a general decider that is always correct on any input, "
        "the initial premise that such an algorithm H can exist must be false. "
        "Hence, the Halting Problem is UNDECIDABLE."
    )

    return results


if __name__ == "__main__":
    demo = demonstrate_diagonalization_paradox()
    print("===== TURING'S DIAGONALIZATION PROOF =====")
    print("\nCase 1:")
    print("  Assumption:", demo["hypothesis_halts"]["assumption"])
    print("  Behavior:  ", demo["hypothesis_halts"]["d_behavior"])
    print("  Paradox:   ", demo["hypothesis_halts"]["contradiction"])
    print("\nCase 2:")
    print("  Assumption:", demo["hypothesis_loops"]["assumption"])
    print("  Behavior:  ", demo["hypothesis_loops"]["d_behavior"])
    print("  Paradox:   ", demo["hypothesis_loops"]["contradiction"])
    print("\nConclusion:")
    print(" ", demo["mathematical_conclusion"])
