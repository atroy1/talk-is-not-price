# Work done before the sprint (disclose in the report)

The sprint page: "you must clearly identify what is new work done during the sprint. Undisclosed prior work can lead to disqualification." Everything below was done before Fri Oct 23 and is plumbing, not results. Paste a one-line version into the report's Methods or Code and Data section.

| Date | Item | What it is | What it is not |
|---|---|---|---|
| 2026-10-15 | Prep docs (`docs/`) | Reading, rules, schedule, track ranking | No research results |
| 2026-10-16 | `patches/llm-agent-collusion.patch` | Starter code updated for current model IDs: temperature dropped for current Claude models, answer read from text blocks, refusals logged, DeepSeek and OpenRouter routing, `--effort` and `--overseer_model` flags | No change to the market, prompts or metrics |
| 2026-10-16 | `analysis/load_runs.py` | Reads the 75 Agrawal et al. 2025 runs into tables as recorded | No new statistic, score or detector |
| 2026-10-16 | `scripts/replay_run.py` | Prints a recorded run round by round with a cost estimate | Demo only, not used in results |
| 2026-10-18 | `tools/llm.py`, `config/models.toml` | One client for every non-simulator LLM call (local LM Studio, Claude API, OpenRouter), a cost ledger, a self-test against a fake server | No prompt that scores a market; no result |
| 2026-10-18 | `tools/talks.sh`, `tools/srt_to_md.py`, `tools/talk_notes.py` | Speech-to-text and note-taking for the sprint talks (parakeet-mlx, mlx-whisper, ffmpeg scene frames, local-model claim finder with verbatim check) | Reads talks only; computes nothing about the data |
| 2026-10-18 | `report/` (figstyle, fig_proof.py, mock/report.typ, fonts) | Figure style, two layout-proof figures on synthetic numbers, a Typst page-budget mock of the template | No real number anywhere; the submission is the official Google Doc |
| 2026-10-20 | `tools/run_queue.py`, `config/queue-friday.toml`, `config/queue-fake.toml` | Sequential launcher for the starter's market runs: one at a time, one retry only when no market output exists, STOP file, stdout/stderr and the results folder under `runs/live/<tag>/`, one log line per run with an estimated cost; a 2-round check against a built-in fake server | Runs the starter as is; no new statistic or detector |
| 2026-10-20 | patch addition (`evaluate.py`) | The starter's per-run judge model (gpt-4.1-mini) now reads `CDA_EVAL_MODEL`, so it can route through OpenRouter without an OpenAI key | Same judge model and prompt as the 2025 data |

Suggested line: "The 75 market runs are from Agrawal et al. (2025). Before the sprint we updated their starter code for current models and wrote a loader for their data; the detector, its calibration, all new runs and all analysis were done during the sprint."
