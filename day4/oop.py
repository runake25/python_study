from collections import deque
from collections.abc import Callable


class BoundedCache:
    """FIFO-bounded cache for a pure function f: int -> int."""

    def __init__(self, f: Callable[[int], int], capacity: int) -> None:
        self._f: Callable[[int], int] = f
        self._capacity: int = capacity
        self._results: dict[int, int] = {}
        self._insertion_order: deque[int] = deque()

    def get(self, key: int) -> int:
        # If capacity is zero or negative, never cache; just compute.
        if self._capacity <= 0:
            return self._f(key)

        if key not in self._results:
            result = self._f(key)
            if len(self._insertion_order) >= self._capacity:
                self._evict_oldest()
            self._add_key(key, result)

        return self._results[key]

    def _evict_oldest(self) -> None:
        oldest_key = self._insertion_order.popleft()
        del self._results[oldest_key]

    def _add_key(self, key: int, result: int) -> None:
        self._results[key] = result
        self._insertion_order.append(key)
