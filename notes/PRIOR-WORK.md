# Work done before the sprint (disclose in the report)

The sprint page: "you must clearly identify what is new work done during the sprint. Undisclosed prior work can lead to disqualification." Everything below was done before Fri Oct 23 and is plumbing, not results. Paste a one-line version into the report's Methods or Code and Data section.

| Date | Item | What it is | What it is not |
|---|---|---|---|
| 2026-10-15 | Prep docs (`docs/`) | Reading, rules, schedule, track ranking | No research results |
| 2026-10-16 | `patches/llm-agent-collusion.patch` | Starter code updated for current model IDs: temperature dropped for current Claude models, answer read from text blocks, refusals logged, DeepSeek and OpenRouter routing, `--effort` and `--overseer_model` flags | No change to the market, prompts or metrics |
| 2026-10-16 | `analysis/load_runs.py` | Reads the 75 Agrawal et al. 2025 runs into tables as recorded | No new statistic, score or detector |
| 2026-10-16 | `scripts/replay_run.py` | Prints a recorded run round by round with a cost estimate | Demo only, not used in results |

Suggested line: "The 75 market runs are from Agrawal et al. (2025). Before the sprint we updated their starter code for current models and wrote a loader for their data; the detector, its calibration, all new runs and all analysis were done during the sprint."
