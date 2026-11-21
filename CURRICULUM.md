# Curriculum (21 Nov – 20 Dec 2026)

**One rule: this is the whole list.** If it isn't on today's line, it isn't today's job. You are not missing anything.

Two phases:
- **Phase 1 – Sprint (21–30 Nov).** Hard deadline Mon 30 Nov. Get `feed-recovery` to a state worth talking about (M0–M5), keep LeetCode and Python drills ticking daily, get Shizuku recording. Resume is rewritten in one go on Sun 29 Nov.
- **Phase 2 – Interview-ready (1–19 Dec).** Finish feed-recovery (M6–M10) alongside full interview prep.

Interviews for Python quant dev / data / reliability roles test four things: **code under pressure** (LeetCode), **real Python** (build from a blank file), **the machine** (systems), **talking about your work** (stories, resume, mocks). Every day hits them.

## Where things live

| What | Where | Proof |
|---|---|---|
| LeetCode + Python drills, systems, stories | `python_study/dayN/` | `lc_<n>.py` (time taken in a top comment), drill + `test_*.py`, `systems.md` + experiment, `stories.md` |
| Showcase project | `runake25/feed-recovery` | Commits that meet the milestone's "Done when" in **`GUIDE.md`** (the spec), with pytest / hypothesis / ruff / mypy green |
| Resume | Private doc "Resume Draft" | Rewritten on Sun 29 Nov; paste it to the coach for review |
| Daily tasks and scorecards | Your 07:55 and 21:40 messages | Graded from what is pushed |
| Data business | `runake25/shizuku` | Commits + recorder running |

Unpushed work doesn't count.

**Resources, used only like this:** Fluent Python = the one chapter listed, only after you've tried. Get Cracked = 1–2 extra questions on the day's topic, only after all 3 NNs are green. feed-recovery: `GUIDE.md` is the scope. Anything on its out-of-scope list is out. No new courses, books or videos.

**Sundays:** no folder. 1 hour redoing the week's worst problem and worst drill from a blank file. Rest. (Exception: Sun 29 Nov is resume day.)

---

## Phase 1 — Sprint (21–30 Nov)

| Time | Block |
|---|---|
| 08:00 – 09:30 | **NN1 – Interview drill**: 1 LeetCode (max 30 min) + 1 Python from-scratch drill (max 30 min) |
| 09:45 – 13:00 | **NN2 – feed-recovery** milestone (per `GUIDE.md` §9) |
| 14:00 – 15:00 | **NN3 – Systems or story.** A story takes 30 min; the rest of the hour goes back to feed-recovery |
| 15:00 – 17:00 | **Shizuku** (tracked, not scored) |
| Evening | Off. 21:40 scorecard. |

**Target by 30 Nov:** M0–M4 done for certain (book + hash, codecs, publisher/subscriber, checker at 100 subs, loss recovery via retransmit with no snapshot). M5 is the stretch. That's already a strong story: lossy UDP fan-out with retransmit, 100 subscribers, proven consistent by hash, with real numbers. The guide's own pace is 4–5 weeks part-time, so finishing everything by 30 Nov isn't the goal. Shipping clean, measured milestones is.

| Day | Date | NN1 Drill (LeetCode + Python) | NN2 feed-recovery | NN3 | Shizuku (15–17) |
|---|---|---|---|---|---|
| 1 | Sat 21 Nov | 217 Contains Duplicate + `@timer` decorator (any signature, `wraps`, returns result, then `@timer(unit="ms")`). *FP ch. 9* | **M0** `book.py`: seeded generator (1,000 levels per side, ticks touch top 20), `set_level` choke point, incremental blake2b hash. Done when the incremental hash equals a full recompute at every step over 100k diffs. | Story 1: options risk engine (STAR, ≤ 2 min) | Pick the first source; write `docs/PROBE_NOTES.md` (endpoint, rate limit, primary key). |
| — | Sun 22 Nov | Review | | | |
| 2 | Mon 23 Nov | 1 Two Sum + closure drill: counter with `nonlocal`, fix the late-binding lambda bug, `@memoize`. | **M1** `wire.py`: `struct.Struct` codecs for every message in §6. Round-trip + hypothesis tests; truncated, oversized and wrong-count input raise clean errors; encoder rejects datagrams > 1,200 bytes. | Story 2: backfill from hours to < 30 s | Minimal recorder: fetch → SHA-256 → append-only Bronze write with `event_time` + `ingestion_time`. |
| 3 | Tue 24 Nov | 49 Group Anagrams + generator pipeline drill (`chunked`, `sliding_window`, `yield from`). *FP ch. 17* | **M2** publisher + 1 subscriber: control session (TCP Subscribe/Hello) + UDP diff stream, absolute-time tick loop, `config.py` invariant checks. Done when hashes match for a 60 s run. | **Systems 5: TCP, UDP & multicast** (you're wiring both today) | Recorder running 24/7, backoff + jitter on errors. |
| 4 | Wed 25 Nov | 347 Top K Frequent + context manager drill (class `Timer`, `@contextmanager`, rollback `transaction()`). *FP ch. 18* | **M3** checker + per-tick reports, `hist.py` log-linear histogram, scale to 100 subscribers over ~4 subfleet processes. Done when every subscriber is consistent every tick, baseline histogram saved, unplanned gaps = 0. | Story 3: escalation point for 25+ clients | Gap / health check: alert if no new data for N minutes. |
| 5 | Thu 26 Nov | 238 Product Except Self + data model drill (`Price` class: `__repr__`, `__eq__`, `__hash__`, ordering; then `@dataclass(slots=True, frozen=True)`). *FP ch. 1* | **M4 part 1**: `sub.py` as a pure `step(state, event) -> (state, actions)` (§7), `pending` buffer, `advance()`; scripted state-machine tests (gap, dup, reorder that fills a hole). | **Systems 1: processes, threads & the GIL** (why the fleet is split into 4 processes) | Leave it running. Check the Bronze data is complete. |
| 6 | Fri 27 Nov | 128 Longest Consecutive + **LRU cache from scratch** (dict + doubly linked list, O(1)). | **M4 part 2**: dropper (drop / reorder / dup, seeded), publisher ring, TCP retransmit. Done when 1% loss, a 50-burst and reorder-by-one recover with **no snapshot**, plus a test showing a late live datagram filling a hole before its resend lands. Hypothesis property on `step()`. | Story 6: why you left Premialab, why these firms + 90-sec "tell me about yourself" | Write the Silver-layer plan only (schema, dedupe key). Build it in December. |
| 7 | Sat 28 Nov | 15 3Sum + `@retry(times, exceptions, backoff)` drill | **M5 (stretch)**: snapshot, epoch, MaxGap; publisher kill/restart without the cache. Either way, today ends with: README (what it is, how to run, out-of-scope list, the numbers you have so far) and GitHub Actions running ruff + mypy + pytest. | Story 5: JPMorgan hackathon | Check it's still recording. |
| — | **Sun 29 Nov** | **Resume day** (no LeetCode) | | | |
| | | **Rewrite the Resume Draft doc in one go**: every Premialab bullet as built / scale / measured result for a Python quant dev role; feed-recovery as the lead project with the milestones done and your real numbers; option dashboard second. Export a 1-page PDF. Coach reviews it like a top-firm recruiter skimming for 30 s, then like the hiring engineer. | | | |
| 8 | **Mon 30 Nov** | 11 Container With Most Water (light day) | Fix anything the resume review flagged; send the PDF before the call | **Call prep**: 60-sec pitch, a 2-min feed-recovery walkthrough, why these firms, what roles to target (Python dev / data / reliability), your questions, timeline, compensation range. Mock call in chat. **Then the call.** | — |

---

## Phase 2 — Interview-ready (1–19 Dec)

| Time | Block |
|---|---|
| 08:00 – 08:30 | Redo yesterday's failed LeetCode from a blank file |
| 08:30 – 10:30 | **NN1 – LeetCode**: 2 problems, max 30 min each |
| 10:45 – 13:00 | **NN2 – feed-recovery milestone or Python build** |
| 13:30 – 15:00 | **NN3 – Systems / story / mock** |
| 15:00 – 17:00 | Shizuku (tracked, not scored) |

If a real interview gets scheduled, the coach switches to prep for that firm and its format, then resumes here. If M5 didn't land in the sprint, it goes first on Day 9 and everything after shifts by a day.

| Day | Date | NN1 LeetCode | NN2 | NN3 |
|---|---|---|---|---|
| 9 | Tue 1 Dec | 242 Valid Anagram, 36 Valid Sudoku | **M6** `snapcache`: one upstream session, request merging via a shared future, invalidate on session loss, `min_epoch` floor | **Systems 2: memory** |
| 10 | Wed 2 Dec | 125 Valid Palindrome, 167 Two Sum II | **M6 done**: restart storm gives 1 upstream fetch per epoch; test that a dead-epoch snapshot is never served | Story 4: Hospital Authority |
| 11 | Thu 3 Dec | 42 Trapping Rain Water, 121 Best Time to Buy/Sell | Python build: producer–consumer with threads vs `asyncio.gather` + `Semaphore` + timeouts, timed. *FP ch. 19, 21* | **Systems 3: CPU & caches** |
| 12 | Fri 4 Dec | 3 Longest Substring, 424 Longest Repeating Char Replacement | **M7 broken**: serial `await drain()` broadcast, one stuck client in the storm; measure the healthy 99 | Story 7: a mistake or production failure |
| 13 | Sat 5 Dec | 567 Permutation in String, 20 Valid Parentheses | **M7 fixed**: per-client writer tasks + deadline cut; plus the stream slow-reader control | 30-min Python internals mock (in chat) |
| — | Sun 6 Dec | Review | | |
| 14 | Mon 7 Dec | 76 Min Window Substring, 155 Min Stack | **M8** divergence alert: ghost level deep in the book, alert within K reports while liveness stays green | Story 8: a disagreement |
| 15 | Tue 8 Dec | 150 Evaluate RPN, 739 Daily Temperatures | Python build: `cProfile` a slow risk calc and fix the hotspot; pure Python vs NumPy returns/VaR, measured | **Systems 4: syscalls & files** |
| 16 | Wed 9 Dec | 853 Car Fleet, 704 Binary Search | **M9** harness: every scenario × N = 30, raw CSV per run, one command reproduces every number | Behavioural mock: 4 random questions |
| 17 | Thu 10 Dec | 74 Search 2D Matrix, 875 Koko Eating Bananas | Python build: rate limiter (token bucket + sliding window), thread-safe, fake clock | **Systems 6: curl a URL end to end** |
| 18 | Fri 11 Dec | 153 Min in Rotated Array, 33 Search Rotated Array | **M10** `WRITEUP.md`: §13 outline, one plot per scenario, the three sentences from one run | Update the resume project bullets with final numbers |
| 19 | Sat 12 Dec | **Mock day**: 2 unseen problems, 45 min, in chat | **Project deep-dive mock**: defend feed-recovery's design for 30 min, interviewer-style | Mock: Python internals + systems Q&A |
| — | Sun 13 Dec | Review | | |
| 20 | Mon 14 Dec | 206 Reverse List, 21 Merge Two Lists | Python build: process pool for a CPU-bound risk calc; speed-up vs threads | Re-record your 3 weakest stories |
| 21 | Tue 15 Dec | 141 Linked List Cycle, 143 Reorder List | Python build: limit order book matching engine (price-time priority) | **Systems 7: latency numbers** |
| 22 | Wed 16 Dec | 19 Remove Nth From End, 981 Time Based Key-Value Store | **Speed round**, 25 min each from blank files: `@retry`, LRU cache, context manager | Behavioural mock 2 |
| 23 | Thu 17 Dec | 23 Merge k Lists, 226 Invert Tree | Debugging: the coach gives you a buggy service; find and fix the bugs, write a test for each | **Systems 8: Linux debugging & signals** |
| 24 | Fri 18 Dec | 104 Max Depth, 102 Level Order | **Full mock**: coding 45 min, then Python internals + systems 20 min | Behavioural 15 min (same mock) |
| 25 | Sat 19 Dec | 98 Validate BST, 200 Number of Islands | Rebuild your weakest build from scratch | Retro: score trend, top 3 gaps, plan for month 2 |
| — | Sun 20 Dec | Review | | |

Month 2 (set at the retro): trees, heaps, graphs, backtracking, 1-D DP, more mocks, any optional feed-recovery extensions (bucketed hash, real L2 replay), and whatever the scorecards say you're weakest at.

---

## Systems track — answer these in `systems.md`, with an experiment you ran

1. **Processes vs threads & the GIL** — Demo: CPU-bound and I/O-bound work with threads vs processes, timed. Q: Why didn't threads speed up the CPU job? When do they help? What does the GIL actually protect?
2. **Memory** — Demo: `sys.getsizeof` and `tracemalloc` on a list of floats vs `array` vs NumPy. Q: Stack vs heap? Virtual memory and page faults? Why is a list of floats so big?
3. **CPU & caches** — Demo: row- vs column-wise traversal of a big NumPy array; loop vs vectorised. Q: What's a cache line? Why does locality matter? Why is NumPy fast?
4. **Syscalls & files** — Demo: `strace -c` a script; read a large file line-by-line vs in big chunks vs `mmap`. Q: What's a syscall and why is it expensive? File descriptors? The page cache?
5. **TCP, UDP & multicast** — Demo: a UDP sender/receiver and a TCP echo pair, measure round trips; show `sendto` never blocks on a stopped reader. Q: TCP vs UDP and when each? The handshake? Nagle / `TCP_NODELAY`? Why do exchanges publish market data over UDP multicast, and how is a lost packet recovered?
6. **curl a URL, end to end** — Demo: `curl -v` with phase timings. Q: DNS → TCP → TLS → HTTP. Where does the time go? What do you check if it's slow?
7. **Latency numbers** — Demo: time a dict lookup, a function call, a file read, a local socket round trip. Q: L1 vs RAM vs SSD vs network? Where do you look first in a slow service?
8. **Linux debugging & signals** — Demo: inspect the running feed-recovery publisher and a subfleet with `ps`, `top`, `ss`, `lsof`, `strace`. Q: SIGTERM vs SIGKILL? How do you debug a hung process? One at 100% CPU?

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

Don't skip ahead and don't double up. If a day scores 0–1/3, repeat it. If it scores 2/3, move on and the missed item replaces tomorrow's NN3. In Phase 1, a slipped feed-recovery milestone takes the NN3 slot until it's back on track, because 30 Nov doesn't move. Resume day stays Sun 29 Nov no matter what. The coach handles this. You just open the folder.
