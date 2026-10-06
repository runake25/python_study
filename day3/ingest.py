import csv
import json
import os
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


def iter_csv(path: Path) -> Iterator[tuple[int, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        yield from enumerate(reader, start=2)


def scan_quotes(path: Path, error_log: Path) -> tuple[int, int, dict]:
    ok_count = 0
    err_count = 0
    buckets: dict[str, dict] = {}

    with error_log.open("a", encoding="utf-8") as log:
        for line_number, row in iter_csv(path):
            reason, bid, ask, size = check_csv(row)
            if reason is not None:
                err_count += 1
                event = {
                    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "source": path.name,
                    "row_num": line_number,
                    "reason": reason,
                    "raw": ",".join(
                        row.get(key, "")
                        for key in ("symbol", "ts", "bid", "ask", "size")
                    ),
                }
                log.write(json.dumps(event) + "\n")
                continue

            ok_count += 1
            update_bucket(buckets, row["symbol"], bid, ask, size)

    summary = {
        symbol: {
            "count": bucket["count"],
            "last_mid": str(bucket["last_mid"]),
            "vwap": str(bucket["notional"] / bucket["volume"]),
        }
        for symbol, bucket in buckets.items()
    }
    return ok_count, err_count, summary


def check_csv(row: dict[str, str]):
    try:
        bid = Decimal(row["bid"])
        ask = Decimal(row["ask"])
        size = Decimal(row["size"])
    except KeyError:
        return "bad_field_count", None, None, None
    except InvalidOperation:
        return "bad_price", None, None, None
    except TypeError:
        return "wrong_type", None, None, None
    if size <= 0:
        return "bad_qty", None, None, None
    if bid > ask:
        return "inverted_book", None, None, None
    return None, bid, ask, size


def update_bucket(
    buckets: dict[str, dict], symbol: str, bid: Decimal, ask: Decimal, size: Decimal
) -> None:
    mid = (bid + ask) / 2
    bucket = buckets.setdefault(
        symbol,
        {
            "count": 0,
            "notional": Decimal(0),
            "volume": Decimal(0),
        },
    )
    bucket["count"] += 1
    bucket["notional"] += mid * size
    bucket["volume"] += size
    bucket["last_mid"] = mid


def write_json_atomic(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def ingest_day(day_dir, *, fail_fast=False):
    meta = Path(day_dir) / "meta.json"
    data = Path(day_dir) / "fills"
    error_log = day_dir / "errors.jsonl"
    report_path = day_dir / "report.json"
    err_count = 0
    ok_count = 0
    buckets: dict[str, dict] = {}
    with error_log.open("a", encoding="utf-8") as log:
        for item in sorted(data.glob("*.csv")):
            for line_number, row in iter_csv(item):
                reason, bid, ask, size = check_csv(row)
                if reason is not None:
                    err_count += 1
                    event = {
                        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "source": item.name,
                        "row_num": line_number,
                        "reason": reason,
                        "raw": ",".join(
                            str(val)
                            for key in ("symbol", "ts", "bid", "ask", "size")
                            if (val := row.get(key)) is not None and val != ""
                        ),
                    }
                    log.write(json.dumps(event) + "\n")
                    continue

                ok_count += 1
                update_bucket(buckets, row["symbol"], bid, ask, size)

    summary = {
        symbol: {
            "count": bucket["count"],
            "last_mid": str(bucket["last_mid"]),
            "vwap": str(bucket["notional"] / bucket["volume"]),
        }
        for symbol, bucket in buckets.items()
    }
    report = {
        "ok_count": ok_count,
        "bad_row_count": err_count,
        "symbols": summary,
    }
    write_json_atomic(report_path, report)
    return ok_count, err_count, summary


fillday_log = Path(__file__).resolve().parent / "data" / "day"
errorday_log = Path(__file__).resolve().parent / "data" / "day" / "errors.jsonl"


print(ingest_day(fillday_log))
