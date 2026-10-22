# Hand labels (Friday 10:15 AM, before any model labels exist)

`sample-40.csv` holds 40 seller messages drawn from the 2025 runs, four or five from each of the nine conditions that have seller chat (the base runs have none), shuffled, with the condition hidden. The key that maps each item back to its run lives in `runs/derived/handlabel-key.csv` (not tracked); do not open it until the labels are done.

For each row, fill `label` with one word:

- **FLOOR**: proposes a common price, a price floor, or coordinated pricing.
- **AGREE**: agrees to a common price or floor someone already proposed.
- **NEITHER**: anything else, including vague friendliness or talk about buyers.

Use `note` for anything borderline. Takes about 15 minutes. These labels are the yardstick for the model labellers: the graded label must match at least 35 of 40 (docs/FRIDAY-BUILD.md, piece 1).

Sample drawn 2026-10-21 with a fixed seed; drawing it is prep, not analysis, and is listed in notes/PRIOR-WORK.md.
