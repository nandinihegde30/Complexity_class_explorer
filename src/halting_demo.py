
# Member 3 - Halting Problem demo

START_NUMBER = 27


def run_bounded_demo(start_number, max_steps=10):
    """Run the Collatz process for a limited number of steps."""

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
    number = int(input("Enter starting number: "))
    limit = int(input("Enter maximum steps: "))

    run_bounded_demo(number, limit)
