to prevent float drifting. float can’t represent many decimals exactly (0.1 isn’t exact in binary), so 0.1 + 0.2 and tick math can round wrong; money/prices need exact base-10, so parse with Decimal("0.1") from the string, never float then Decimal

we use lazy reading by using generator, which pull ocnstant memory each iter, list will force to pull all the result at once 

os.replace is atomic only when source and dest are on the same filesystem.   with plain open write mode and json dump, it will immediately trucate existing file to 0 bytes upon opening, if something crashes in the moddle of the operation the reader will observe inconsistant information

Recipe, in order:

Same-dir temp — create something like report.json.tmp next to report.json (same folder → same disk).
Write — dump the full JSON into the temp.
flush — push Python’s buffer out to the OS.
fsync — force the OS to finish writing to disk before you continue.
os.replace(temp, report.json) — rename/swap so the target name flips to the finished file in one step.



On a bad row, ingest_day logs the event and continues. The scan does not stop. That continue is the policy. fail_fast was the switch for the other choice: raise on the first bad row so the report is not written. Nothing reads the parameter, so fail_fast=True and fail_fast=False both take the continue.