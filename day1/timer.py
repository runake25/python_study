import time
from functools import wraps


def timer(unit):

    match unit:
        case "ns":
            divisor = 1
        case "ms":
            divisor = 1_000_000

        case "s":
            divisor = 1_000_000_000

        case _:
            raise ValueError(f"Unknown unit {unit!r}")

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter_ns()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter_ns() - start
                print(f"time taken : {elapsed / divisor:.6f} {unit}")

        return wrapper

    return decorate


@timer(unit="s")
def add10(int1, int2):
    """Return the sum of two numbers"""
    return print(int1 + int2)


def main():
    add10(3, 5)

    print(add10.__name__, add10.__doc__)


if __name__ == "__main__":
    main()
