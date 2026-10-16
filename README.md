# Apart AI Collusion Research Sprint, Oct 23 to 25, 2026

Prep workspace. Read in this order:

1. `docs/BASELINE.md` the event, the schedule in Eastern time, the rubric, past-sprint numbers, what a winning report looks like, where this machine stands.
2. `docs/PLAYBOOK.md` the pre-sprint checklist and the hour-by-hour weekend plan with scope-cut rules.
3. `docs/TRACK-PICKS.md` the twelve questions ranked for fit, with a recommendation.
4. `docs/MODELS-AND-TOOLS.md` API access, cost per run by model, starter-code fixes, efficiency tools.
5. `papers/README.md` reading order; `papers/abstracts.md` every cited arXiv abstract.
6. `notes/report-skeleton.md` paste into the template copy; `notes/log.md` the running log.

Reference copies: `docs/apart-report-template.txt` (official template text), `docs/reference-winning-report-ai-control-2026.pdf` (first place, March 2026).

Environment: `.venv` is Python 3.12 with the double-auction starter installed. Starter repos live in `vendor/` (gitignored, third-party). Keys go in `.env` (copy `.env.example`).

Code: `analysis/load_runs.py` loads the 75 bundled runs into tables (`python -m analysis.load_runs`); `patches/llm-agent-collusion.patch` updates the starter for current models; `scripts/replay_run.py` replays a recorded run. Everything built before Friday is listed in `notes/PRIOR-WORK.md`.
