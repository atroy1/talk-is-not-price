# Apart AI Collusion Research Sprint, Oct 23 to 25, 2026

Prep workspace. Read in this order:

1. `docs/BASELINE.md` the event, the schedule in Eastern time, the rubric, past-sprint numbers, what a winning report looks like, where this machine stands.
2. `docs/PLAYBOOK.md` (v2, 10/18) roles, the pre-sprint checklist, gates G0 to G7 around the real calendar, scope cuts, the submission fields. Its companions: `docs/MODEL-ROUTING.md` (local Mac Studio models, Claude API, OpenRouter: which does what, costs, keys), `docs/TALKS-PIPELINE.md` (live capture of the Friday talks to a cited note), `docs/PDF-TEMPLATE.md` (the report page by page: measured word budgets, figures, tables, tone, export checklist).
3. `docs/TRACK-PICKS.md` the twelve questions ranked for fit, with a recommendation.
4. `docs/RESEARCH-BRIEF.md` speakers, nearest studies and novelty check, past winners. `docs/END-PRODUCT.md` the 4-page PDF plan, creative options, and the five alternative framings with a recommendation (choice pending).
5. `docs/MODELS-AND-TOOLS.md` API access, cost per run by model, starter-code fixes, efficiency tools.
6. `papers/README.md` reading order; `papers/abstracts.md` every cited arXiv abstract.
7. `notes/report-skeleton.md` paste into the template copy; `notes/log.md` the running log.

Reference copies: `docs/apart-report-template.txt` (official template text), `docs/reference-winning-report-ai-control-2026.pdf` (first place, March 2026).

Environment: `.venv` is Python 3.12 with the double-auction starter installed; `.venv-tools` holds the speech-to-text and API clients for `tools/`. `make help` lists the shortcuts (ping, self-test, ledger, talk, notes, figs, mock). Starter repos live in `vendor/` (gitignored, third-party). Keys go in `.env` (copy `.env.example`).

Tools (plumbing, 10/18): `tools/llm.py` + `config/models.toml` route every non-simulator LLM call and keep `notes/cost-ledger.csv`; `tools/talks.sh` + `tools/talk_notes.py` turn a talk recording into `notes/talks/<slug>.md`; `tools/studio-probe.sh` runs on the Mac Studio; `report/` holds the figure style, layout proofs and the Typst page-budget replica of the template.

Code: `analysis/load_runs.py` loads the 75 bundled runs into tables (`python -m analysis.load_runs`); `patches/llm-agent-collusion.patch` updates the starter for current models; `scripts/replay_run.py` replays a recorded run. Everything built before Friday is listed in `notes/PRIOR-WORK.md`.
