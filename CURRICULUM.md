# 4-Week Curriculum (21 Nov – 20 Dec 2026)

**One rule: this is the whole list.** If it isn't on today's line, it isn't today's job. You are not missing anything. Interviewers for Python quant dev / data / reliability roles test exactly four things, and every day below hits them:

1. **Can you code under pressure?** → LeetCode, 2 problems a day
2. **Do you really know Python?** → build the classic pieces from a blank file
3. **Do you understand the machine?** → systems, twice a week
4. **Can you talk about your work?** → stories, mocks

## Every study day

| Time | Block |
|---|---|
| 08:00 – 08:30 | Redo yesterday's failed LeetCode from a blank file |
| 08:30 – 10:30 | **NN1 – LeetCode**: 2 problems, max 30 min each, then read the best solution |
| 10:45 – 12:30 | **NN2 – Python build** (code + tests) |
| 13:30 – 15:00 | **NN3 – Systems / Story / Mock** |
| 15:00 – 17:00 | Data business. Hard stop. |
| Evening | Off. 21:40 scorecard. |

**Proof = pushed to `dayN/`.** LeetCode: `lc_<number>.py` with time taken in a top comment. Build: module + `test_*.py` (pytest) passing. Story: STAR write-up in `stories.md`, ≤ 2 min out loud. Systems: runnable experiment + `systems.md` answering the 3 questions in your own words with your measured numbers.

**Resources, used only like this:** Fluent Python = the one chapter listed, only *after* you've tried the build. Get Cracked = 1–2 extra questions on the same topic only *after* all 3 NNs are green. Nothing else. No new courses, books or videos for 4 weeks.

**Sundays:** no folder. 1 hour: redo the week's worst problem and worst build from a blank file. Rest of the day off.

---

## Week 1 — Python fundamentals that trip you up
LeetCode: arrays & hashing, two pointers

| Day | Date | NN1 LeetCode | NN2 Python build | NN3 |
|---|---|---|---|---|
| 1 | Sat 21 Nov | 217 Contains Duplicate, 242 Valid Anagram | `@timer` decorator (any signature, keeps metadata via `wraps`, returns the result), then `@timer(unit="ms")` with arguments, then `@retry(times, exceptions, backoff)`. *FP ch. 9* | Story 1: the options risk engine |
| — | Sun 22 Nov | Review | | |
| 2 | Mon 23 Nov | 1 Two Sum, 49 Group Anagrams | Closures: counter factory with `nonlocal`; reproduce + fix the late-binding lambda-in-a-loop bug; `@memoize` with `cache_info()`; compare with `functools.lru_cache`. *FP ch. 9* | Story 2: backfill from hours to < 30 s |
| 3 | Tue 24 Nov | 347 Top K Frequent, 238 Product Except Self | Generators: lazy file reader, a parse → filter → aggregate pipeline, `chunked(it, n)`, `sliding_window(it, n)`, `yield from`. Show memory stays flat on a 1 GB file. *FP ch. 17* | **Systems 1:** processes vs threads & the GIL |
| 4 | Wed 25 Nov | 128 Longest Consecutive, 36 Valid Sudoku | Context managers: class-based `Timer`, the same with `@contextmanager`, and a `transaction()` that rolls back on exception. Know what `__exit__` returning True does. *FP ch. 18* | Story 3: escalation point for 25+ clients |
| 5 | Thu 26 Nov | 125 Valid Palindrome, 167 Two Sum II | Data model: a `Money`/`Price` class with `__repr__`, `__eq__`, `__hash__`, `__add__`, ordering, `__iter__`; then a frozen `@dataclass` version. Explain why mutable + hashable is a bug. *FP ch. 1, 11* | **Systems 2:** memory |
| 6 | Fri 27 Nov | 15 3Sum, 11 Container With Most Water | **LRU cache from scratch**, O(1) get/put: first with `OrderedDict`, then dict + your own doubly linked list. Capacity 0 and 1, updating an existing key. | Story 4: Hospital Authority platform |
| 7 | Sat 28 Nov | 42 Trapping Rain Water + redo week's worst | **Week build:** log analyser CLI. Streams a big log with generators, counts per level, p50/p99 latency, `@timer` on the hot path, context manager for the output file. | Story 5: JPMorgan hackathon |
| — | Sun 29 Nov | Review | | |

## Week 2 — Data structures & concurrency
LeetCode: sliding window, stack, binary search

| Day | Date | NN1 LeetCode | NN2 Python build | NN3 |
|---|---|---|---|---|
| 8 | Mon 30 Nov | 121 Best Time to Buy/Sell, 3 Longest Substring | Min-heap from scratch (`push`, `pop`, `heapify`), then streaming top-k with `heapq`. | Story 6: why you left Premialab, why this firm |
| 9 | Tue 1 Dec | 424 Longest Repeating Char Replacement, 567 Permutation in String | Rate limiter: token bucket + sliding-window log, thread-safe with a `Lock`, tested with an injected fake clock. | **Systems 3:** CPU & caches |
| 10 | Wed 2 Dec | 20 Valid Parentheses, 76 Min Window Substring | Ring buffer (fixed capacity) + O(1) rolling mean & variance (Welford) over a price stream. | Story 7: a mistake or production failure |
| 11 | Thu 3 Dec | 155 Min Stack, 150 Evaluate RPN | Concurrency: producer–consumer with `queue.Queue` and threads; then fetch 50 fake vendor calls with `asyncio.gather`, a `Semaphore` limit and timeouts. Time both. *FP ch. 19, 21* | **Systems 4:** syscalls & files |
| 12 | Fri 4 Dec | 739 Daily Temperatures, 853 Car Fleet | Performance: `cProfile` a deliberately slow risk calc, fix the hotspot; pure-Python vs NumPy-vectorised returns/VaR, with measured speed-up. | Story 8: disagreement with a teammate or manager |
| 13 | Sat 5 Dec | 704 Binary Search, 74 Search a 2D Matrix | **Week build:** limit order book: add, cancel, match, best bid/ask, price-time priority, full tests. | 30-min Python internals mock (oral, in chat) |
| — | Sun 6 Dec | Review | | |

## Week 3 — Reliability & data builds (your edge)
LeetCode: binary search, linked lists

| Day | Date | NN1 LeetCode | NN2 Python build | NN3 |
|---|---|---|---|---|
| 14 | Mon 7 Dec | 875 Koko Eating Bananas, 153 Min in Rotated Array | Flaky vendor client: retry with exponential backoff + jitter, plus a circuit breaker (closed / open / half-open). Tested with a fake vendor. | 90-sec "tell me about yourself" |
| 15 | Tue 8 Dec | 33 Search Rotated Array, 206 Reverse Linked List | Market data stream processor: tick generator in, per-symbol 1-min VWAP out, plus stale-data and gap alerts. | **Systems 5:** TCP, UDP & sockets |
| 16 | Wed 9 Dec | 21 Merge Two Lists, 141 Linked List Cycle | Ingest pipeline in pandas: schema checks, dedupe, missing-data report, daily returns, all vectorised. | Behavioural mock: 4 random questions in chat |
| 17 | Thu 10 Dec | 143 Reorder List, 19 Remove Nth From End | asyncio consumer with backpressure (bounded queue), a slow downstream, and graceful shutdown. | **Systems 6:** what happens when you curl a URL |
| 18 | Fri 11 Dec | 981 Time Based Key-Value Store, 23 Merge k Lists | As-of join: implement it by hand for two price feeds, then check against `pandas.merge_asof`. pytest fixtures + parametrize. | Resume drill: defend every bullet |
| 19 | Sat 12 Dec | **Mock day**: 2 unseen problems, 45 min, in chat | Rebuild the LRU cache from a blank file, 25 min | Mock: Python internals + systems Q&A |
| — | Sun 13 Dec | Review | | |

## Week 4 — Trees, heaps & interview-ready
LeetCode: trees, heaps, first graphs

| Day | Date | NN1 LeetCode | NN2 Python build | NN3 |
|---|---|---|---|---|
| 20 | Mon 14 Dec | 226 Invert Tree, 104 Max Depth | In-memory cache service: TTL + LRU eviction + hit/miss stats, thread-safe. | Re-record your 3 weakest stories |
| 21 | Tue 15 Dec | 102 Level Order, 98 Validate BST | Metrics collector: counters, gauges, histogram with p50/p99, and a `/health`-style check. | **Systems 7:** latency numbers |
| 22 | Wed 16 Dec | 230 Kth Smallest in BST, 199 Right Side View | **Speed round** from blank files, 25 min each: `@retry` decorator, rate limiter, ring buffer. | Behavioural mock 2 |
| 23 | Thu 17 Dec | 703 Kth Largest in Stream, 215 Kth Largest | Worker service that handles SIGTERM cleanly: finishes in-flight work, flushes, exits 0. | **Systems 8:** Linux debugging & signals |
| 24 | Fri 18 Dec | 973 K Closest Points, 200 Number of Islands | **Full mock**: coding 45 min, then Python internals + systems 20 min | Behavioural 15 min (same mock) |
| 25 | Sat 19 Dec | 207 Course Schedule, 70 Climbing Stairs | Rebuild the week's weakest build from scratch | Retro: score trend, top 3 gaps, plan for month 2 |
| — | Sun 20 Dec | Review | | |

Month 2 (set at the retro): graphs, backtracking, 1-D DP, more mocks, and whatever the scorecards say you're weakest at.

---

## Systems track — the 3 questions to answer in `systems.md`

1. **Processes vs threads & the GIL** — Demo: CPU-bound and I/O-bound work with threads vs processes, timed. Q: Why didn't threads speed up the CPU job? When do they help? What does the GIL actually protect?
2. **Memory** — Demo: `sys.getsizeof` and `tracemalloc` on a list of floats vs `array` vs NumPy. Q: Stack vs heap? What is virtual memory and a page fault? Why is a Python list of floats so big?
3. **CPU & caches** — Demo: row-wise vs column-wise traversal of a big NumPy array; loop vs vectorised. Q: What's a cache line? Why does locality matter? Why is NumPy fast (contiguous memory, SIMD, no per-element interpreter)?
4. **Syscalls & files** — Demo: `strace -c` a script; read a large file line-by-line vs in big chunks vs `mmap`. Q: What's a syscall and why is it expensive? What's a file descriptor? What is the page cache?
5. **TCP, UDP & sockets** — Demo: a socket echo server + client, and measure round-trip time. Q: TCP vs UDP and when each is used? The 3-way handshake? Nagle / `TCP_NODELAY`? Why do exchanges use UDP multicast for market data?
6. **curl a URL, end to end** — Demo: `curl -v` plus timing for each phase. Q: Walk through DNS → TCP → TLS → HTTP. Where does the time go? What would you check if it's slow?
7. **Latency numbers** — Demo: measure dict lookup, a function call, a file read, a local socket round trip. Q: Rough cost of L1 vs RAM vs SSD vs network? Where would you look first in a slow service?
8. **Linux debugging & signals** — Demo: your SIGTERM worker from Day 23; inspect it with `ps`, `top`, `ss`, `lsof`, `strace`. Q: SIGTERM vs SIGKILL? How do you debug a hung process? A process using 100% CPU?

## Story bank (STAR, ≤ 2 min each, real numbers)

1. Options risk engine (200K+ securities/day, 25+ funds)
2. Backfill from several hours to < 30 s
3. Escalation point under pressure (vendor outage, client impact)
4. Hospital Authority: building for non-technical users (20+ min to 5 min)
5. JPMorgan Code for Good: leading a team, 1st of 70+
6. Why you left Premialab, why this firm, why quant dev
7. A mistake or failure, and what you changed
8. A disagreement, and how it got resolved

## If you fall behind

Don't skip ahead and don't try to catch up by doubling up. If a day scores 0–1/3, repeat that day. If it scores 2/3, move on and the missed item replaces tomorrow's NN3. The coach handles this. You just open the folder.
