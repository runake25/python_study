from dataclasses import dataclass
from enum import Enum
import pandas


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
    price: float


class PositionLedger:
    def __init__(self):
        self._positions: dict[str, int] = {}
        self._realized_pnl_total: dict[str, float] = {}
        self.avg_prices: dict[str, float] = {}

    def apply(self, fill) -> None:
        """Updates positions and calculates PnL based on an incoming fill."""
        symbol = fill.symbol
        qty = fill.qty
        price = fill.price
        is_buy = fill.side == Side.BUY

        # get current state
        current_qty = self.positions.get(symbol, 0)
        current_avg_price = self.avg_prices.get(symbol, 0.0)
        realized = self.realized_pnl_total.get(symbol, 0.0)

        # update

        # fill/PnL logic here...

    def get_position(self, symbol: str) -> int:
        """Returns the current position for a given symbol."""
        return self._positions.get(symbol, 0)

    def realized_pnl(self, symbol: str) -> float:
        """Returns the realized PnL for a given symbol."""
        return self._realized_pnl_total.get(symbol, 0.0)
