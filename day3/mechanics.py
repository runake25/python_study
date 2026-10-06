from ast import expr_context
from difflib import restore
from pathlib import Path
from decimal import *
import json
BASE_DIR = Path(__file__).resolve().parent

fill_log = BASE_DIR / "data" / "fills.log"

try:
    with open(fill_log, encoding="utf-8") as file:
        for line in file:
            print(line, end="")
        raise RuntimeError("boom")
    
except RuntimeError as exc:
    print(exc)
    print(file.closed)
    
print(repr(0.10 + 0.20))

print(repr(Decimal("0.10") + Decimal("0.20")))

price = Decimal("189.25")
tick = Decimal("0.01")
ticks = int(price/tick)
restore = Decimal(ticks) * tick

print(ticks)
print(restore)

print(int(0.29 / 0.01))
print(int(Decimal("0.29") / Decimal("0.01")))

try:
    print(json.dumps({"last_mid": Decimal("189.25")}))
except TypeError as exc:
    print(type(exc).__name__)

print(json.dumps({"last_mid": "189.25"}))

meta_path = Path(__file__).resolve().parent / "data" / "meta.json"
with meta_path.open(encoding="utf-8") as f:
    meta = json.load(f)
print(meta["venue"])

truncated_path = Path(__file__).resolve().parent / "data" / "truncated.json"
try:
    with truncated_path.open(encoding="utf-8") as f:
        json.load(f)
except json.JSONDecodeError as exc:
    print(type(exc).__name__)