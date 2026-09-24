import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def normal_function(x: int) -> int:
    print(f"Normal function called with {x}")
    return x + 1


def time_wrapper(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time: float = time.perf_counter()
        result: R = func(*args, **kwargs)
        end_time: float = time.perf_counter()
        print(f"Time taken: {end_time - start_time} seconds")
        return result

    return wrapper


if __name__ == "__main__":
    f: Callable[[int], int] = time_wrapper(normal_function)

    wrap = f(1)

    direct = normal_function(1)

    print(wrap, direct)
    assert wrap == direct == 2
