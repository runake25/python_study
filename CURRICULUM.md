# Curriculum (21 Nov – 20 Dec 2026)

**One rule: this is the whole list.** If it isn't on today's line, it isn't today's job. You are not missing anything.

Two phases:
- **Phase 1 – Sprint to the recruiter call (21–30 Nov).** Ship `feed-recovery`, rewrite the resume, get Shizuku recording. Keep LeetCode and Python drills ticking daily.
- **Phase 2 – Interview-ready (1–19 Dec).** Full study days for the Jump / Jane Street loops.

Interviews for Python quant dev / data / reliability roles test four things: **code under pressure** (LeetCode), **real Python** (build from a blank file), **the machine** (systems), **talking about your work** (stories, resume, mocks). Every day hits them.

## Where things live

| What | Where | Proof |
|---|---|---|
| LeetCode + Python drills, systems, stories | `python_study/dayN/` | `lc_<n>.py` (time taken in a top comment), drill + `test_*.py`, `systems.md` + experiment, `stories.md` |
| Resume | `python_study/resume/RESUME.md` | Commits. The coach reviews the diff. |
| Showcase project | `runake25/feed-recovery` | Commits + passing `pytest`, `ruff`, `mypy` |
| Data business | `runake25/shizuku` | Commits + recorder running |

Unpushed work doesn't count.

**Resources, used only like this:** Fluent Python = the one chapter listed, only after you've tried. Get Cracked = 1–2 extra questions on the day's topic, only after all 3 NNs are green. No new courses, books or videos.

**Sundays:** no folder. 1 hour redoing the week's worst problem and worst drill from a blank file. Rest.

---

## Phase 1 — Sprint (21–30 Nov)

| Time | Block |
|---|---|
| 08:00 – 09:30 | **NN1 – Interview drill**: 1 LeetCode (max 30 min) + 1 Python from-scratch drill (max 30 min) |
| 09:45 – 13:00 | **NN2 – feed-recovery** milestone |
| 14:00 – 15:00 | **NN3 – Resume / systems / story** |
| 15:00 – 17:00 | **Shizuku** (tracked, not scored) |
| Evening | Off. 21:40 scorecard. |

### feed-recovery: what it is

A market-data feed handler that **survives packet loss**. Exchanges publish sequenced market data over UDP multicast. Packets get dropped, duplicated and reordered, and a handler that misses one has a wrong order book. This project:

- simulates an exchange publishing sequenced messages over UDP, with configurable drop / duplicate / reorder (chaos)
- detects gaps by sequence number, buffers out-of-order messages, and recovers missed ones over a TCP retransmit channel, falling back to snapshot + replay
- runs A/B line arbitration (two redundant feeds, take whichever arrives first)
- proves correctness with property-based tests: **the book rebuilt from a lossy feed equals the book from a lossless feed**
- measures it: gap count, recovery latency p50/p99, throughput

It is the market-data version of what you did at Premialab (vendor outages, refetch alerts), and it's the kind of problem Jump and Jane Street actually deal with. Stack is already in the repo: Python 3.14, pytest, hypothesis, mypy, ruff.

### Sprint days

| Day | Date | NN1 Drill (LeetCode + Python) | NN2 feed-recovery | NN3 | Shizuku (15–17) |
|---|---|---|---|---|---|
| 1 | Sat 21 Nov | 217 Contains Duplicate + `@timer` decorator (any signature, `wraps`, returns result, then `@timer(unit="ms")`). *FP ch. 9* | README design doc: problem, architecture, message format, invariants, what you'll measure. Message model as frozen dataclasses + binary encode/decode with `struct`, round-trip tests (hypothesis). | **Resume v1**: rewrite every Premialab bullet for a Python quant dev role (what you built, scale, measured impact). | Pick the first source; write `docs/PROBE_NOTES.md` (endpoint, rate limit, primary key). |
| 2 | Mon 23 Nov | 1 Two Sum + closure drill: counter with `nonlocal`, fix the late-binding lambda bug, `@memoize`. | Exchange simulator: publishes sequenced messages over UDP on localhost, with drop / duplicate / reorder rates. | Story 1: options risk engine (STAR, ≤ 2 min) | Minimal recorder: fetch → SHA-256 → append-only Bronze write with `event_time` + `ingestion_time`. |
| 3 | Tue 24 Nov | 49 Group Anagrams + generator pipeline drill (`chunked`, `sliding_window`, `yield from`). *FP ch. 17* | Receiver: asyncio UDP consumer, gap detection, duplicate and out-of-order handling with a bounded buffer. Property tests over random loss patterns. | **Systems 5: TCP, UDP & multicast** (you're using it today) | Recorder running 24/7 (cron / systemd / Docker), backoff + jitter on errors. |
| 4 | Wed 25 Nov | 347 Top K Frequent + context manager drill (class `Timer`, `@contextmanager`, rollback `transaction()`). *FP ch. 18* | Recovery: TCP retransmit request for missing ranges, timeout + retry with backoff, snapshot + replay fallback. | **Resume v2** after the coach's critique. Projects section: option dashboard + feed-recovery. | Gap / health check: alert if no new data for N minutes. |
| 5 | Thu 26 Nov | 238 Product Except Self + data model drill (`Price` class: `__repr__`, `__eq__`, `__hash__`, ordering; then frozen dataclass). *FP ch. 1* | Order book built from the feed. **Key test:** lossy feed + recovery gives the same book as a lossless feed (hypothesis). | **Systems 1: processes, threads & the GIL** (why your receiver is asyncio) | Leave it running. Check the Bronze data is complete. |
| 6 | Fri 27 Nov | 128 Longest Consecutive + **LRU cache from scratch** (dict + doubly linked list, O(1)). | A/B line arbitration + metrics (gaps, recovery latency p50/p99, msgs/sec). Benchmark and profile one hot path. | Story 6: why you left Premialab, why Jump / Jane Street + 90-sec "tell me about yourself" | Write the Silver-layer plan only (schema, dedupe key). Build it in December. |
| 7 | Sat 28 Nov | 15 3Sum + `@retry(times, exceptions, backoff)` drill | Ship it: README with real numbers, a CLI demo command, GitHub Actions running ruff + mypy + pytest, graceful shutdown on SIGTERM. | **Resume final**: feed-recovery bullets with your measured numbers. Export to PDF. | Check it's still recording. |
| — | Sun 29 Nov | Review: redo the week's worst problem + drill | — | — | — |
| 8 | Mon 30 Nov | 11 Container With Most Water + rate limiter drill (token bucket, fake clock) | Buffer day: fix whatever the reviews flagged. Record a 2-min walkthrough of the project. | **Recruiter call prep**: 60-sec pitch, why these firms, your questions, timeline, compensation range. Mock call in chat. | — |

If the recruiter call is earlier than 30 Nov, the resume final moves to the day before the call.

---

## Phase 2 — Interview-ready (1–19 Dec)

| Time | Block |
|---|---|
| 08:00 – 08:30 | Redo yesterday's failed LeetCode from a blank file |
| 08:30 – 10:30 | **NN1 – LeetCode**: 2 problems, max 30 min each |
| 10:45 – 12:30 | **NN2 – Python build** (code + tests) |
| 13:30 – 15:00 | **NN3 – Systems / story / mock** |
| 15:00 – 17:00 | Shizuku (tracked, not scored) |

If a real interview gets scheduled, the coach switches to prep for that firm and its format, then resumes here.

| Day | Date | NN1 LeetCode | NN2 Python build | NN3 |
|---|---|---|---|---|
| 9 | Tue 1 Dec | 242 Valid Anagram, 36 Valid Sudoku | Min-heap from scratch + streaming top-k with `heapq` | **Systems 2: memory** |
| 10 | Wed 2 Dec | 125 Valid Palindrome, 167 Two Sum II | Rate limiter v2: sliding-window log, thread-safe with a `Lock`, concurrency test | Story 2: backfill from hours to < 30 s |
| 11 | Thu 3 Dec | 42 Trapping Rain Water, 121 Best Time to Buy/Sell | Concurrency: producer–consumer with threads vs `asyncio.gather` + `Semaphore` + timeouts, timed. *FP ch. 19, 21* | **Systems 3: CPU & caches** |
| 12 | Fri 4 Dec | 3 Longest Substring, 424 Longest Repeating Char Replacement | Performance: `cProfile` a slow risk calc and fix the hotspot; pure Python vs NumPy returns/VaR, measured | Story 3: escalation point for 25+ clients |
| 13 | Sat 5 Dec | 567 Permutation in String, 20 Valid Parentheses | Limit order book matching engine: add, cancel, match, price-time priority | 30-min Python internals mock (in chat) |
| — | Sun 6 Dec | Review | | |
| 14 | Mon 7 Dec | 76 Min Window Substring, 155 Min Stack | Ingest pipeline in pandas: schema checks, dedupe, missing-data report, vectorised returns | Story 4: Hospital Authority |
| 15 | Tue 8 Dec | 150 Evaluate RPN, 739 Daily Temperatures | As-of join by hand for two price feeds, checked against `pandas.merge_asof`; pytest parametrize | **Systems 4: syscalls & files** |
| 16 | Wed 9 Dec | 853 Car Fleet, 704 Binary Search | Cache service: TTL + LRU eviction + hit/miss stats, thread-safe | Behavioural mock: 4 random questions |
| 17 | Thu 10 Dec | 74 Search 2D Matrix, 875 Koko Eating Bananas | Metrics collector: counters, gauges, histogram with p50/p99 | **Systems 6: curl a URL end to end** |
| 18 | Fri 11 Dec | 153 Min in Rotated Array, 33 Search Rotated Array | **Speed round**, 25 min each from blank files: `@timer`, LRU cache, context manager | Story 5: JPMorgan hackathon |
| 19 | Sat 12 Dec | **Mock day**: 2 unseen problems, 45 min, in chat | Rebuild the rate limiter, 25 min | Mock: Python internals + systems Q&A |
| — | Sun 13 Dec | Review | | |
| 20 | Mon 14 Dec | 206 Reverse List, 21 Merge Two Lists | Multiprocessing: parallelise a CPU-bound risk calc with a process pool; measure speed-up vs threads | Story 7: a mistake or production failure |
| 21 | Tue 15 Dec | 141 Linked List Cycle, 143 Reorder List | Typing: `Protocol`, generics, `TypedDict`; make one module pass `mypy --strict` | **Systems 7: latency numbers** |
| 22 | Wed 16 Dec | 19 Remove Nth From End, 981 Time Based Key-Value Store | **Speed round 2**: `@retry`, ring buffer, min-heap | Story 8: a disagreement + behavioural mock 2 |
| 23 | Thu 17 Dec | 23 Merge k Lists, 226 Invert Tree | Debugging: the coach gives you a buggy service; find and fix the bugs, write a test for each | **Systems 8: Linux debugging & signals** |
| 24 | Fri 18 Dec | 104 Max Depth, 102 Level Order | **Full mock**: coding 45 min, then Python internals + systems 20 min | Behavioural 15 min (same mock) |
| 25 | Sat 19 Dec | 98 Validate BST, 200 Number of Islands | Rebuild your weakest build from scratch | Retro: score trend, top 3 gaps, plan for month 2 |
| — | Sun 20 Dec | Review | | |

Month 2 (set at the retro): trees, heaps, graphs, backtracking, 1-D DP, more mocks, and whatever the scorecards say you're weakest at.

---

## Systems track — answer these in `systems.md`, with an experiment you ran

1. **Processes vs threads & the GIL** — Demo: CPU-bound and I/O-bound work with threads vs processes, timed. Q: Why didn't threads speed up the CPU job? When do they help? What does the GIL actually protect?
2. **Memory** — Demo: `sys.getsizeof` and `tracemalloc` on a list of floats vs `array` vs NumPy. Q: Stack vs heap? Virtual memory and page faults? Why is a list of floats so big?
3. **CPU & caches** — Demo: row- vs column-wise traversal of a big NumPy array; loop vs vectorised. Q: What's a cache line? Why does locality matter? Why is NumPy fast?
4. **Syscalls & files** — Demo: `strace -c` a script; read a large file line-by-line vs in big chunks vs `mmap`. Q: What's a syscall and why is it expensive? File descriptors? The page cache?
5. **TCP, UDP & multicast** — Demo: a UDP sender/receiver and a TCP echo pair, measure round trips and loss. Q: TCP vs UDP and when each? The handshake? Nagle / `TCP_NODELAY`? Why do exchanges publish market data over UDP multicast, and how do you recover a lost packet?
6. **curl a URL, end to end** — Demo: `curl -v` with phase timings. Q: DNS → TCP → TLS → HTTP. Where does the time go? What do you check if it's slow?
7. **Latency numbers** — Demo: time a dict lookup, a function call, a file read, a local socket round trip. Q: L1 vs RAM vs SSD vs network? Where do you look first in a slow service?
8. **Linux debugging & signals** — Demo: inspect your feed-recovery receiver with `ps`, `top`, `ss`, `lsof`, `strace`. Q: SIGTERM vs SIGKILL? How do you debug a hung process? One at 100% CPU?

## Story bank (STAR, ≤ 2 min, real numbers)

1. Options risk engine (200K+ securities/day, 25+ funds)
2. Backfill from several hours to < 30 s
3. Escalation point under pressure (vendor outage, client impact)
4. Hospital Authority: building for non-technical users (20+ min to 5 min)
5. JPMorgan Code for Good: leading a team, 1st of 70+
6. Why you left Premialab, why this firm, why quant dev
7. A mistake or failure, and what you changed
8. A disagreement, and how it got resolved

## If you fall behind

Don't skip ahead and don't double up. If a day scores 0–1/3, repeat it. If it scores 2/3, move on and the missed item replaces tomorrow's NN3. In Phase 1, feed-recovery and the resume have a hard deadline (the recruiter call), so if they slip, they take the NN3 slot until they're back on track. The coach handles this. You just open the folder.
