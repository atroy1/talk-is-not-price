# Talk Is Not Price: What a Chat Monitor Sees and Misses in LLM Seller Markets

Research conducted at the Apart Research AI Collusion Research Sprint, October 23 to 25, 2026 (Track 2, Detection and
Audit). Author: Arthur Troy.

**The claim.** When five LLM sellers in a market can message each other, they agree on prices and say so in plain
words. No monitor that reads their chat had been calibrated on honest LLM markets, because none existed. We found
that no model we tested talks honestly on its own: one added sentence, "coordinating prices is illegal", makes one
model talk honestly, silences three and is ignored by two. Calibrated on 20 of those honest markets (4.8% certified
false-alarm rate), the monitor flags 105 of the 112 markets whose sellers were free to coordinate, with one false
alarm among 34 honest markets that talked. It measures agreement rather than harm: 16 of the 35 cartels in the prior
data left buyers no worse off than the competitive benchmark, the most expensive market in the study was honest and
silent, and gagged sellers under profit pressure kept their plan in private notes and their prices high.
Pre-registered; the headline is exploratory and every change is declared.

**The report** is `report/final/report.pdf` (four-page body, appendix A to J), built from
`report/draft/report-draft.md` by `make final`. The 150-word abstract for the submission form is
`report/final/abstract-150.txt`.

## Reproduce

```bash
make freeze
```

regenerates every table and figure from the recorded markets and the cached labels and writes
`notes/results-frozen.md`, the file every number in the report comes from. `make final` builds the PDF. Needs Python
3.12 with the pinned requirements in `config/starter-requirements.lock` (a `.venv` at the repository root), and for
the PDF `typst` plus the Old Standard TT fonts in `report/fonts/`. No API key is needed to reproduce: the labels are
cached in `runs/derived/`.

The market simulator is the starter code of Agrawal et al. (2025), which is not vendored here. Clone it to
`vendor/llm-agent-collusion` from https://github.com/andyjliu/llm-agent-collusion and apply
`patches/llm-agent-collusion.patch` (current model names, a reasoning switch, an empty-reply retry, a per-call usage
log). Their licence applies to their code and to the 75 prior markets, which `analysis/load_runs.py` reads from that
checkout.

To rerun the labelling or new markets you need keys in `.env` (never committed): `ANTHROPIC_API_KEY`,
`OPENROUTER_API_KEY`. `make labels` relabels messages; `tools/run_queue.py` runs a queue of markets from a TOML file
in `config/`.

## Data

- The 160 new markets are under `runs/live/<tag>/` as the simulator wrote them (asks, bids, trades, every seller
  message, and the per-call usage log), with their queue configs in `config/*.toml`. The one timed-out planted
  market the report keeps is `runs/live/_planted-s3b-attempt1`.
- Labels: `runs/derived/labels.csv` (DeepSeek V4.1 Flash, first-token probabilities), `labels-alt.csv` (GPT-4.1-mini,
  the second labeller family), `labels-reference.csv` (Claude Sonnet 5.5 on 396 messages), and the 40-message
  readings under `notes/handlabel/`.
- Every table the report cites is a CSV in `runs/derived/`; `runs/derived/accounting.md` places all 235 markets once.

## Pre-registration

Locked Fri Oct 23, 10:37 AM ET, commit `824c801`, before any detector result was read: `notes/preregistration.md`,
with every declared deviation beneath the locked text. `notes/log.md` is the full run and decision log. Before the
sprint the only work was updating the starter for current models and writing a loader (`notes/PRIOR-WORK.md`); the
detector, its calibration, all new markets and all analysis were done during the sprint.

## Layout

`analysis/` scores, detector, labeller, the accounting and every table; `report/` figure scripts, the template
replica and the build; `tools/` the queue runner, check-ins and the LLM router; `config/` prompts and queues;
`notes/` the pre-registration, log, frozen results and working notes; `docs/` the plans and runbooks.
