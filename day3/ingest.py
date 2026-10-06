import json
import csv
from collections.abc import Iterator
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


def iter_fills(path: Path) -> Iterator[tuple[int, str]]:
    with path.open(encoding="utf-8") as handle:
        yield from enumerate(handle, start=1)


def ingest_fills(path: Path, error_log: Path) -> tuple[int, int]:
    ok_count = 0
    err_count = 0

    with error_log.open("a", encoding="utf-8") as log:
        for line_number, line in iter_fills(path):
            reason = check_fill(line)
            if reason is None:
                ok_count += 1
                continue

            err_count += 1
            event = {
                "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "source": path.name,
                "row_num": line_number,
                "reason": reason,
                "raw": line.rstrip("\n")[:500],
            }
            log.write(json.dumps(event) + "\n")

    return ok_count, err_count


def check_fill(line: str) -> str | None:
    parts = line.split()
    if len(parts) != 5:
        return "bad_field_count"

    _ts, _symbol, side, qty_token, px_token = parts
    if side not in ("B", "S"):
        return "bad_side"
    try:
        qty = int(qty_token)
    except ValueError:
        return "bad_qty"
    if qty <= 0:
        return "bad_qty"
    try:
        Decimal(px_token)
    except InvalidOperation:
        return "bad_price"
    return None

fill_log = Path(__file__).resolve().parent / "data" / "fills.log"
error_log = Path(__file__).resolve().parent / "data" / "errors.jsonl"
print(ingest_fills(fill_log, error_log))



def iter_csv(path: Path) -> Iterator[tuple[int, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        yield from enumerate(reader, start=2)


def scan_quotes(path: Path, error_log: Path) -> tuple[int, int]:
    ok_count = 0
    err_count = 0

    with error_log.open("a", encoding="utf-8") as log:
        for line_number, line in iter_csv(path):
            reason = check_csv(line)
            print(line)
            if reason is None:
                ok_count += 1
                continue

            err_count += 1
            event = {
                "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "source": path.name,
                "row_num": line_number,
                "reason": reason,
                "raw": line.rstrip("\n")[:500],
            }
            log.write(json.dumps(event) + "\n")

    return ok_count, err_count


def check_csv(line: str) -> str | None:
    parts = line.split(",")
    print(parts)
    if len(parts) != 5:
        return "bad_field_count"

    symbol, ts, bid, ask, size = parts

    try:
        size = int(size)
    except ValueError:
        return "bad_qty"
    if size <= 0:
        return "bad_qty"
    try:
        bid = Decimal(bid)
        ask = Decimal(ask)
        Decimal(bid-ask)
    except InvalidOperation:
        return "bad_price"
    return None



fill_log = Path(__file__).resolve().parent / "data" / "quotes.csv"
error_log = Path(__file__).resolve().parent / "data" / "errors.jsonl"
print(scan_quotes(fill_log, error_log))