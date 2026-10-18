# Sprint log

One line per run or decision, with the time. Started 2026-10-15.

- 2026-10-15 prep: folder created, 10 starter repos cloned to vendor/, .venv (3.12) with the double-auction starter installed. Docs written: BASELINE, PLAYBOOK, TRACK-PICKS.
- 2026-10-16 research: docs/MODELS-AND-TOOLS.md (Max plan API credits, cost per run ~650k in / 165k out tokens, Claude wrapper temperature 400, Jev as cheap message scorer, Context Mode for transcripts).
- 2026-10-16 scripts/replay_run.py: replays a recorded run as if live, prices the bill per model (base-seller_comms-1: 299 calls, ~7.5 min wall clock in 2025, $0.15 on Haiku 5.5).
- 2026-10-16 prep: starter patched (patches/llm-agent-collusion.patch, fake-server check passed), analysis/load_runs.py built (75 runs, 0 unparsed replies, 3 of 11,250 judge rows failed), PLAYBOOK step 3 narrowed to plumbing, notes/PRIOR-WORK.md started. Data fact: only the 10 'base' runs have no seller channel; boss_pressure runs have it on.
- 2026-10-17 research: docs/RESEARCH-BRIEF.md (Colosseum says neither chat nor actions alone catch all collusion; novelty slot = both, in a market, at fixed FPR, across model families) and docs/END-PRODUCT.md (quadrant figure, smoking-gun opener, pre-registration box, page plan).
- 2026-10-17 framing options recorded in docs/END-PRODUCT.md (quadrant, lead time, detector ageing, evidence standard, on paper in markets, lying to the watchdog). Recommendation: lead time headline + quadrant Fig 2 + ageing stretch. His pick pending; decide by Fri 4 PM after controls.
