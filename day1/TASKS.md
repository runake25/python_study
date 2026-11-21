# Day 1 — Sat 21 Nov 2026

Phase 1 sprint. Milestone: **M0**.

You lost the morning, so the order is NN2 first (it's the one with a deadline), then NN1, then NN3. Shizuku only if the three are green.

---

## NN2 — feed-recovery M0: `book.py` (do this first, ~3 h)

**Where:** `runake25/feed-recovery` → `feed/__init__.py`, `feed/book.py`, `tests/test_book.py`.

**Read first:** GUIDE.md §2 (feed source), §5 (fixed design choices: book, diffs, incremental hash, one choke point, self-check), §12 traps 1, 7, 14.

**Build:**
- Integer prices (ticks) and integer quantities. **No floats.**
- A book with two sides (bid, ask). One method, `set_level(side, price, qty)`, updates the stored level **and** the running hash together. `qty == 0` deletes the level. Nothing else writes level storage. No `await` inside it.
- Incremental hash: `H = Σ h(side, price, qty) mod 2**64`, where `h` = 8-byte `blake2b` of the packed level (`struct`, little-endian). On a change: subtract the old level's `h` (if it existed), add the new one (if qty > 0).
- `full_hash()`: recompute from scratch over all levels.
- Seeded generator: fixed mid price, 1,000 price levels per side created at startup; each tick yields a diff of 1–10 `(side, price, new_qty)` entries, **only within the top 20 levels per side**. Same seed → same sequence.
- `apply(diff)` goes through `set_level` only.

**Done when (GUIDE M0, word for word):** After 100k diffs, the incremental hash equals a full recompute at every step.

**Tests that must exist and pass:**
1. 100k diffs from a seeded generator: `book.hash == book.full_hash()` after every diff.
2. Same seed twice → identical final hash. Different seed → different hash.
3. Applying the same diff twice is harmless (absolute values).
4. Deep levels (beyond top 20) never change after startup.
5. A test that fails if anything other than `set_level` writes level storage (e.g. write a level directly, then assert the hash no longer matches `full_hash()`, proving the self-check would catch it).
6. Uses `blake2b`, never built-in `hash()` (trap 1): the hash of a fixed book is a hard-coded constant in the test, so it's stable across processes.

**Proof:** pushed to feed-recovery; `pytest`, `ruff check .`, `mypy --strict feed/` all green. Put the 100k-diff test's runtime in your commit message.

**Out of scope today:** wire format, sockets, anything async. Just the book.

---

## NN1 — Interview drill (~1 h)

**Where:** `python_study/day1/`

**a) LeetCode 217 Contains Duplicate** → `lc_217.py`. 30 min max, no hints. Top comment: time taken, and the time and space complexity of your solution. Then write a second version with a different trade-off (e.g. O(1) extra space) and state its cost.

**b) `@timer` decorator** → `timer.py` + `test_timer.py`. 30 min max.
- Works on a function with any signature (positional, keyword, defaults).
- Returns the wrapped function's result unchanged.
- Keeps `__name__` and `__doc__` (`functools.wraps`).
- Uses `time.perf_counter_ns()`, and reports the elapsed time even when the function raises (then re-raises the same exception).
- Then a second form, `@timer(unit="ms")`, that accepts arguments. Reject an unknown unit with a clear `ValueError` at decoration time.
- Tests: result passthrough, metadata kept, exception path still timed and re-raised, bad unit raises. Inject the clock or capture output so tests don't depend on real timing.

**Only after you've tried:** Fluent Python ch. 9.

---

## NN3 — Story 1: the options risk engine (~30 min)

**Where:** `python_study/day1/stories.md`

STAR, ≤ 2 minutes out loud, real numbers:
- **S:** What did Premialab's clients need, and what was missing before?
- **T:** What were you personally responsible for?
- **A:** What you built: MSCI methodology, Greeks, PnL, VaR / CVaR, 200K+ securities a day. One hard technical decision and why you made it.
- **R:** Who used it (25+ institutional funds) and what changed for them. A number.

Then say it out loud once, timed, and write the time at the bottom.

---

## Shizuku (15:00–17:00, tracked, not scored)

Pick the first source. Write `docs/PROBE_NOTES.md` in shizuku: endpoint, rate limit, auth (must be public and unauthenticated), the immutable primary key, and what `event_time` is for this source.

---

Push as you go. Unpushed work doesn't count.
