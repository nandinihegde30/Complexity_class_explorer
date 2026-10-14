
# Member 3 - Halting Problem demo

START_NUMBER = 27


def halting_problem_explanation():
    """Explain why the Halting Problem is undecidable."""

    text = (
        "The Halting Problem asks whether a program will stop "
        "or run forever for a given input. Alan Turing proved "
        "that no algorithm can correctly answer this for every "
        "possible program and input. Therefore, the Halting "
        "Problem is undecidable. If a program does not stop "
        "within a fixed step limit, we cannot conclude that "
        "it will run forever."
    )

    return text


def run_bounded_demo(max_steps=10):
    """Run the Collatz process for a limited number of steps."""

    if type(max_steps) is not int:
        raise TypeError("max_steps must be an integer")

    if max_steps < 1:
        raise ValueError("max_steps must be at least 1")

    n = START_NUMBER
    steps = 0

    while n != 1 and steps < max_steps:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1

        steps += 1

    if n == 1:
        status = "stopped_within_bound"
    else:
        status = "bound_exhausted"

    return {"status": status, "steps": steps}
