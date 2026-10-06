to prevent float drifting

we use lazy reading by using generator, which pull ocnstant memory each iter, list will force to pull all the result at once 

os.replace is atomic only when source and dest are on the same filesystem.   with plain open write mode and json dump, it will immediately trucate existing file to 0 bytes upon opening, if something crashes in the moddle of the operation the reader will observe inconsistant information


On a bad row, ingest_day logs the event and continues. The scan does not stop. That continue is the policy. fail_fast was the switch for the other choice: raise on the first bad row so the report is not written. Nothing reads the parameter, so fail_fast=True and fail_fast=False both take the continue.