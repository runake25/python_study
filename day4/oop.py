from collections import OrderedDict
from collections.abc import Callable


class LRUBoundedCache:
    """LRU-bounded cache for a pure function f: int -> int."""

    def __init__(self, f: Callable[[int], int], capacity: int) -> None:
        self._f: Callable[[int], int] = f
        self._capacity: int = capacity
        self._results: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if self._capacity <= 0:
            return self._f(key)

        # Cache Hit: Move key to the end (mark as most recently used)
        if key in self._results:
            self._results.move_to_end(key)
            return self._results[key]
        result = self._f(key)
        # Cache Miss: Evict least recently used (first item) if full
        if len(self._results) >= self._capacity:
            _ = self._results.popitem(last=False)

        self._results[key] = result
        return result
