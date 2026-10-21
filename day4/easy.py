from dataclasses import dataclass
from enum import Enum
from decimal import Decimal


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(
    frozen=True,
    slots=True,
)
class Fill:
    fill_id: int
    symbol: str
    side: Side
    qty: int
    price: Decimal


class PositionLedger:
    def __init__(self) -> None:
        self._positions: dict[str, int] = {}
        self._avg_cost: dict[str, Decimal] = {}
        self._realized_pnl_total: dict[str, Decimal] = {}
        self._seen: set[int] = set()

    def apply(self, fill: Fill) -> None:
        """Apply one fill using average-cost accounting.

        Positive position = long; negative position = short.
        Duplicate fill IDs are rejected.
        """
        # Validate before changing any ledger state.
        if not isinstance(fill, Fill):
            raise TypeError("fill must be a Fill")
        if type(fill.fill_id) is not int:
            raise TypeError("fill_id must be an integer")
        if fill.fill_id in self._seen:
            raise ValueError(f"duplicate fill_id: {fill.fill_id}")
        if not isinstance(fill.symbol, str) or not fill.symbol.strip():
            raise ValueError("symbol must be a non-empty string")
        if not isinstance(fill.side, Side):
            raise TypeError("side must be a Side")
        if type(fill.qty) is not int:
            raise TypeError("qty must be an integer")
        if fill.qty <= 0:
            raise ValueError("qty must be positive")
        if not isinstance(fill.price, Decimal):
            raise TypeError("price must be a Decimal")
        if not fill.price.is_finite() or fill.price <= 0:
            raise ValueError("price must be finite and positive")

        symbol = fill.symbol
        zero = Decimal("0")

        old_qty = self._positions.get(symbol, 0)
        old_avg = self._avg_cost.get(symbol, zero)
        old_realized = self._realized_pnl_total.get(symbol, zero)

        signed_qty = fill.qty if fill.side is Side.BUY else -fill.qty
        new_qty = old_qty + signed_qty

        new_avg = old_avg
        new_realized = old_realized

        if old_qty == 0:
            # Opening a position.
            new_avg = fill.price

        elif (old_qty > 0) == (signed_qty > 0):
            # Increasing an existing long or short.
            new_avg = (abs(old_qty) * old_avg + fill.qty * fill.price) / abs(new_qty)

        else:
            # Closing some or all of the existing position.
            closed_qty = min(abs(old_qty), fill.qty)
            old_direction = 1 if old_qty > 0 else -1

            new_realized += (fill.price - old_avg) * closed_qty * old_direction

            if new_qty == 0:
                new_avg = zero
            elif (new_qty > 0) != (old_qty > 0):
                # Flipped direction: residual opens at this fill's price.
                new_avg = fill.price
            # Otherwise this was a partial close: retain old_avg.

        # Commit only after validation and calculations succeed.
        self._positions[symbol] = new_qty
        self._avg_cost[symbol] = new_avg
        self._realized_pnl_total[symbol] = new_realized
        self._seen.add(fill.fill_id)

    def get_position(self, symbol: str) -> int:
        """Returns the current position for a given symbol."""
        return self._positions.get(symbol, 0)

    def realized_pnl(self, symbol: str) -> Decimal:
        """Returns the realized PnL for a given symbol."""
        return self._realized_pnl_total.get(symbol, Decimal("0.0"))


if __name__ == "__main__":
    ledger = PositionLedger()

    # Example usage:
    fill1 = Fill(
        fill_id=1, symbol="AAPL", side=Side.BUY, qty=10, price=Decimal("150.00")
    )
    ledger.apply(fill1)

    fill2 = Fill(
        fill_id=2, symbol="AAPL", side=Side.SELL, qty=5, price=Decimal("155.00")
    )
    ledger.apply(fill2)

    print(f"Position for AAPL: {ledger.get_position('AAPL')}")
    print(f"Realized PnL for AAPL: {ledger.realized_pnl('AAPL')}")
