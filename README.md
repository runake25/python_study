# python_study

Private daily solutions for **python-track**. The bot reviews whatever you push under today's folder — you do not need to paste code in chat.

## Layout

```
day1/
day2/
...
day28/
```

- One folder per curriculum day: `dayN` where N matches Week/Day progress in `runake25/life/python/state.json` (W1D1 = `day1`, …).
- Put all code, tests, and short notes for that day inside the folder.
- Prefer a short `NOTES.md` (what you finished, blockers, recall-check answer) so the evening log can stay thin in chat.

## Evening flow

1. Commit + push before ~19:00 HKT when you can.
2. python-track reads `dayN/` via `gh`, grades against that day's task, updates `life/python/logs/`.
3. If the folder is missing or empty, the bot asks once in chat.

Existing top-level folders (e.g. `gc/`) are fine to keep; new track work goes under `dayN/`.
