# Talk Is Not Price: What a Chat Monitor Sees and Misses in LLM Seller Markets

Research conducted at the Apart Research AI Collusion Research Sprint, October 23 to 25, 2026 (Track 2, Detection and
Audit). Author: Arthur Troy.

**The claim.** When LLM sellers can message each other they fix prices and say so. A chat monitor calibrated on honest
chat flags every talking cartel at a certified false-alarm rate (35 of 35 GPT-4.1 and Claude 3.x markets from 2025,
29 of 30 under oversight or CEO pressure, 28 of 28 new markets across four families, 4.8%). But the honest chat had to
be manufactured: no model family we tested talks honestly under a neutral instruction, and the one sentence that
produces honest talk ("coordinating prices is illegal") does so for Claude Haiku 5.5, silences Sonnet and Opus 5.5
and does not reach Qwen3.5. What the flag reports is talk, not harm: 16 of the 35 cartels it flags left buyers no
worse off than the competitive price, the honest market that sets the price screen's bar cost buyers more than any
cartel, and a flag says nothing about silent high pricing or about the strategy that outlived the overseer's gag.

**The report** is `report/final/report.pdf`, built from `report/draft/report-draft.md` by `make final`.

## Reproduce

```bash
make freeze
```

regenerates every table and draft figure from the recorded markets and the cached labels and writes
`notes/results-frozen.md`, the file every number in the report comes from. `make final` builds the PDF. Python 3.12,
`uv`, and the pinned requirements in `config/starter-requirements.lock`; `typst` and the Old Standard TT fonts in
`report/fonts/` for the PDF. No API key is needed to reproduce: the labels are cached in `runs/derived/`.

To rerun the labelling or new markets you need keys in `.env` (never committed): `ANTHROPIC_API_KEY`,
`OPENROUTER_API_KEY`. `make labels` relabels messages; `tools/run_queue.py` runs a queue of markets from a TOML file.

## Data

- The 75 prior markets are those released by Agrawal et al. (2025) with their starter code
  (`vendor/llm-agent-collusion`, their licence applies). Before the sprint we updated the starter for current models
  and wrote a loader; the detector, its calibration, all new markets and all analysis were done during the sprint
  (`notes/PRIOR-WORK.md`).
- The 136 new markets are under `runs/live/<tag>/` with their configs (`config/*.toml`) and per-call usage logs.
- Labels: `runs/derived/labels.csv` (DeepSeek V4.1 Flash, first-token probabilities), `labels-alt.csv` (GPT-4.1-mini,
  the second labeller family), `labels-reference.csv` (Claude Sonnet 5.5 on 396 messages), the blind 40-message
  readings under `notes/handlabel/`.

## Pre-registration

Locked Fri Oct 23, 10:37 AM ET, commit `824c801`, before any detector result was read: `notes/preregistration.md`,
with every declared deviation beneath the locked text. `notes/log.md` is the full run and decision log.

## Layout

`analysis/` scores, detector, labeller and every table; `report/` figure scripts, the template replica and the build;
`tools/` the queue runner, check-ins and the LLM router; `config/` prompts and queues; `notes/` the pre-registration,
log, frozen results and working notes; `docs/` the plans and runbooks.

## Spend

About $56 of Claude API credit (Haiku, Sonnet and Opus markets), about $27 of OpenRouter credit (the starter's
per-run judge, DeepSeek and Luna markets, labelling), and local Qwen3.5 35B-A3B markets on a Mac Studio at no cost.
