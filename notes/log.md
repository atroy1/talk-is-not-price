# Sprint log

One line per run or decision, with the time. Started 2026-10-15.

- 2026-10-15 prep: folder created, 10 starter repos cloned to vendor/, .venv (3.12) with the double-auction starter installed. Docs written: BASELINE, PLAYBOOK, TRACK-PICKS.
- 2026-10-16 research: docs/MODELS-AND-TOOLS.md (Max plan API credits, cost per run ~650k in / 165k out tokens, Claude wrapper temperature 400, Jev as cheap message scorer, Context Mode for transcripts).
- 2026-10-16 scripts/replay_run.py: replays a recorded run as if live, prices the bill per model (base-seller_comms-1: 299 calls, ~7.5 min wall clock in 2025, $0.15 on Haiku 5.5).
- 2026-10-16 prep: starter patched (patches/llm-agent-collusion.patch, fake-server check passed), analysis/load_runs.py built (75 runs, 0 unparsed replies, 3 of 11,250 judge rows failed), PLAYBOOK step 3 narrowed to plumbing, notes/PRIOR-WORK.md started. Data fact: only the 10 'base' runs have no seller channel; boss_pressure runs have it on.
- 2026-10-17 research: docs/RESEARCH-BRIEF.md (Colosseum says neither chat nor actions alone catch all collusion; novelty slot = both, in a market, at fixed FPR, across model families) and docs/END-PRODUCT.md (quadrant figure, smoking-gun opener, pre-registration box, page plan).
- 2026-10-17 framing options recorded in docs/END-PRODUCT.md (quadrant, lead time, detector ageing, evidence standard, on paper in markets, lying to the watchdog). Recommendation: lead time headline + quadrant Fig 2 + ageing stretch. His pick pending; decide by Fri 4 PM after controls.
- 2026-10-18 framework finalized: docs/PLAYBOOK.md v2 (gates G0 to G7 around the real calendar: Sat shift 7 AM to noon, Thu shift + DC interview, Friday talks captured live because recordings post after the event), docs/MODEL-ROUTING.md (three lanes, one door: tools/llm.py + config/models.toml, self-test passes, --ping skips all three lanes until keys exist), docs/TALKS-PIPELINE.md (tools/talks.sh + talk_notes.py tested on a synthetic clip: parakeet-mlx 16 s clip verbatim, 2 scene frames, prompts written), docs/PDF-TEMPLATE.md + report/ (template is REQUIRED per the Guidelines tab; its type is Old Standard TT 11/14/22 pt on Letter with 1 in margins; Typst mock measures the page budget). Calendar: Fri talks, Fri 4 PM lock, Sun 1 PM early submit, Mon 7:59 AM deadline added to Work. Mac Studio: Remote Login off, specs unknown; tools/studio-probe.sh to run there.
- 2026-10-20 09:51 queue: start config/queue-fake.toml, 1 runs, est $0.00
- 2026-10-20 09:51 queue: fake-check attempt 1: ok, 0.1 min, runs/live/fake-check, est $0.00 (gpt-4.1-mini sellers, gpt-4.1-mini buyers, 2 rounds)
- 2026-10-20 09:51 queue: end config/queue-fake.toml
- 2026-10-20 09:52 queue: start config/queue-fake.toml, 1 runs, est $0.00
- 2026-10-20 09:52 queue: fake-check attempt 1: ok, 0.0 min, runs/live/fake-check, est $0.00 (gpt-4.1-mini sellers, gpt-4.1-mini buyers, 2 rounds, judge gpt-4.1-mini)
- 2026-10-20 09:52 queue: end config/queue-fake.toml
- 2026-10-20 plumbing: tools/run_queue.py built and checked (queue-fake: 2 rounds, 10 agents, metrics written, logged above). Finding: the starter judges every seller every round with gpt-4.1-mini on the OpenAI API after each market; patched so CDA_EVAL_MODEL can point it at openai/gpt-4.1-mini on OpenRouter (queue-friday.toml sets this). Friday queue: 20 runs, about $6.10 with the judge included. `make queue` runs it under caffeinate.
