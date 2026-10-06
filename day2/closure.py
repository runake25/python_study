"""Week 1 Day 2 — closures.

Target path: runake25/python_study/day2/closures.py

Stateful callables with no class, no module globals, and no shared mutable
default. Binding is by cell, not by value snapshot.
"""

from __future__ import annotations

import math
import time
from collections import deque
from collections.abc import Callable
from typing import TypeAlias


class ClockFault(ValueError):
    """Clock is non-finite or moved backwards; this is not a rate-limit reject."""


Clock: TypeAlias = Callable[[], float]
FillCounter: TypeAlias = Callable[[], int]
OnFill: TypeAlias = Callable[[str, int], None]
GetPosition: TypeAlias = Callable[[str], int]
RateGate: TypeAlias = Callable[[], bool]


def make_counter(start: int = 0) -> Callable[[], int]:
    """Return a counter. Each call rebinds the cell and returns the new count.

    start=0 means the cell begins at 0; the first call returns 1.
    """
    if isinstance(start, bool) or not isinstance(start, int):
        raise TypeError(f"start must be int, got {type(start).__name__}")

    count = start

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def make_fill_counter() -> FillCounter:
    """Per-session fill ack counter. First ack returns 1.

    Zero is the cell value before any call, not a return value of on_fill.
    Calling on_fill *is* the fill.
    """
    return make_counter(0)


def make_position_book() -> tuple[OnFill, GetPosition]:
    """Per-session net position book. State is a dict captured by cell.

    In-place mutation does not rebind the name, so nonlocal is not required.
    get_position must not insert missing symbols.
    """
    positions: dict[str, int] = {}

    def on_fill(symbol: str, qty: int) -> None:
        if not isinstance(symbol, str) or not symbol.strip():
            raise ValueError("symbol must be a non-empty string")
        if isinstance(qty, bool) or not isinstance(qty, int):
            raise TypeError(f"qty must be int, got {type(qty).__name__}")
        positions[symbol] = positions.get(symbol, 0) + qty

    def get_position(symbol: str) -> int:
        if not isinstance(symbol, str) or not symbol.strip():
            raise ValueError("symbol must be a non-empty string")
        return positions.get(symbol, 0)

    return on_fill, get_position


def make_rate_gate(
    max_trades: int,
    window_sec: float,
    clock: Clock | None = None,
) -> RateGate:
    """Allow a trade iff fewer than max_trades allowed fills sit in the window.

    True records the timestamp. False does not. Rejects must not pollute the
    window.

    Expiry policy: drop timestamps strictly older than now - window_sec.
    A timestamp exactly at the boundary still counts. That is the conservative
    risk choice and the off-by-one this gate is explicit about.

    clock defaults to time.monotonic when the factory is called. Pass a fake
    clock in tests. A backwards or non-finite clock raises ClockFault and
    records nothing. That is not a rate-limit False.
    """
    if isinstance(max_trades, bool) or not isinstance(max_trades, int):
        raise TypeError(f"max_trades must be int, got {type(max_trades).__name__}")
    if isinstance(window_sec, bool) or not isinstance(window_sec, (int, float)):
        raise TypeError(f"window_sec must be real, got {type(window_sec).__name__}")
    if max_trades < 0:
        raise ValueError("max_trades must be >= 0")
    if window_sec < 0 or not math.isfinite(window_sec):
        raise ValueError("window_sec must be finite and >= 0")
    if clock is not None and not callable(clock):
        raise TypeError("clock must be callable")

    clock_fn: Clock = time.monotonic if clock is None else clock

    # Allowed-trade timestamps only, oldest at the left. Never exceeds max_trades.
    stamps: deque[float] = deque()

    def allow() -> bool:
        now = clock_fn()
        if (
            isinstance(now, bool)
            or not isinstance(now, (int, float))
            or not math.isfinite(now)
        ):
            raise ClockFault(f"clock returned non-finite value: {now!r}")
        # Appending a backwards stamp would break oldest-at-left. Do not record.
        if stamps and now < stamps[-1]:
            raise ClockFault(f"clock moved backwards: now={now} last={stamps[-1]}")
        cutoff = now - float(window_sec)
        while stamps and stamps[0] < cutoff:
            stamps.popleft()
        if len(stamps) >= max_trades:
            return False
        stamps.append(float(now))
        return True

    return allow


def closure_cells(fn: Callable[..., object]) -> dict[str, object]:
    """Zip free-var names to cell contents. Do not index __closure__ by guess."""
    cells = fn.__closure__
    if not cells:
        return {}
    return {
        name: cell.cell_contents
        for name, cell in zip(fn.__code__.co_freevars, cells, strict=True)
    }


def _late_binding_broken(symbols: list[str]) -> list[Callable[[], str]]:
    """Every callback reads the same cell. After the loop that cell is the last symbol."""
    hooks: list[Callable[[], str]] = []
    for symbol in symbols:
        hooks.append(lambda: symbol)  # noqa: B023 — deliberate trap
    return hooks


def _late_binding_fixed(symbols: list[str]) -> list[Callable[[], str]]:
    """Default arg binds the current value into a local at definition time."""
    hooks: list[Callable[[], str]] = []
    for symbol in symbols:
        hooks.append(lambda symbol=symbol: symbol)
    return hooks


def _run_tests() -> None:
    # --- counters: independent cells, increment-then-return ---
    a = make_counter()
    b = make_counter(10)
    assert closure_cells(a) == {"count": 0}
    assert a() == 1 and a() == 2 and a() == 3
    assert b() == 11 and b() == 12
    assert a() == 4  # b's calls did not touch a
    assert closure_cells(a) == {"count": 4}
    assert a.__closure__ is not b.__closure__
    assert a.__closure__[0] is not b.__closure__[0]

    fills_desk_a = make_fill_counter()
    fills_desk_b = make_fill_counter()
    assert closure_cells(fills_desk_a) == {"count": 0}  # before any fill
    assert fills_desk_a() == 1
    assert closure_cells(fills_desk_a) == {"count": 1}
    assert [fills_desk_a() for _ in range(3)] == [2, 3, 4]
    assert fills_desk_b() == 1

    # --- position book ---
    on_fill, get_pos = make_position_book()
    on_fill_b, get_pos_b = make_position_book()
    assert get_pos("AAPL") == 0
    on_fill("AAPL", 10)
    on_fill("AAPL", -4)
    on_fill("MSFT", -3)  # short through zero
    on_fill("MSFT", -2)
    on_fill("ES", 1)
    assert get_pos("AAPL") == 6
    assert get_pos("MSFT") == -5
    assert get_pos("ES") == 1
    assert get_pos("NVDA") == 0  # read must not insert
    on_fill_b("AAPL", 100)
    assert get_pos("AAPL") == 6
    assert get_pos_b("AAPL") == 100
    try:
        on_fill("", 1)
        raise AssertionError("empty symbol must fail")
    except ValueError:
        pass
    try:
        on_fill("AAPL", True)  # type: ignore[arg-type]
        raise AssertionError("bool qty must fail")
    except TypeError:
        pass

    assert "positions" in on_fill.__code__.co_freevars

    # --- rate gate ---
    class FakeClock:
        def __init__(self, t: float = 0.0) -> None:
            self.t = t

        def __call__(self) -> float:
            return self.t

        def advance(self, dt: float) -> None:
            self.t += dt

    clock = FakeClock(0.0)
    gate = make_rate_gate(2, 10.0, clock)
    assert gate() is True  # t=0
    clock.advance(1.0)
    assert gate() is True  # t=1, window holds 2
    clock.advance(1.0)
    assert gate() is False  # t=2 saturated; must not record
    clock.t = 10.0  # boundary: stamp 0 is not strictly older than 0
    assert gate() is False
    clock.t = 10.0 + 1e-9
    assert gate() is True  # stamp 0 expired; stamp 1 remains; record 10+eps
    clock.t = 11.0 + 1e-9
    assert gate() is True  # stamp 1 expired

    # rejects do not extend the window
    clock2 = FakeClock(0.0)
    gate2 = make_rate_gate(1, 5.0, clock2)
    assert gate2() is True
    assert gate2() is False
    assert gate2() is False
    clock2.advance(5.0 + 1e-9)
    assert gate2() is True  # only one stamp was stored, so one expiry frees the slot

    always_deny = make_rate_gate(0, 5.0, FakeClock(0.0))
    assert always_deny() is False and always_deny() is False

    zero_window = make_rate_gate(1, 0.0, clock := FakeClock(0.0))
    assert zero_window() is True
    assert (
        zero_window() is False
    )  # same timestamp still inside a 0-width inclusive edge
    clock.advance(1e-9)
    assert zero_window() is True

    back = FakeClock(5.0)
    gate_back = make_rate_gate(1, 10.0, back)
    assert gate_back() is True
    back.t = 4.0
    try:
        gate_back()
        raise AssertionError("backwards clock must not look like a rate reject")
    except ClockFault:
        pass
    back.t = 5.0
    assert gate_back() is False  # equal to last is not backwards; still saturated
    back.t = 15.0 + 1e-9
    assert gate_back() is True  # rejected tick was not stored

    c1, c2 = FakeClock(0.0), FakeClock(0.0)
    g1, g2 = make_rate_gate(1, 10.0, c1), make_rate_gate(1, 10.0, c2)
    assert g1() is True and g1() is False
    assert g2() is True  # separate stamp deques

    on_a, get_a = make_position_book()

    def _cell(fn: Callable[..., object], name: str) -> object:
        idx = fn.__code__.co_freevars.index(name)
        closure = fn.__closure__
        assert closure is not None
        return closure[idx]

    assert _cell(on_a, "positions") is _cell(get_a, "positions")

    broken = _late_binding_broken(["AAPL", "MSFT", "ES"])
    assert [h() for h in broken] == ["ES", "ES", "ES"]
    fixed = _late_binding_fixed(["AAPL", "MSFT", "ES"])
    assert [h() for h in fixed] == ["AAPL", "MSFT", "ES"]

    print("all assertions passed")


if __name__ == "__main__":
    _run_tests()
