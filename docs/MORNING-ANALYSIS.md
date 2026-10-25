# The morning analysis session (Sunday Oct 25, 8:30 AM)

Runbook for the scheduled session that reads the overnight results and folds them into the paper. The 6 AM check-in
(sprint-sunday-6am) has already pulled, labelled with both labellers, run `make freeze` and logged. Written Sat Oct 24,
10:30 PM.

## 1. What ran overnight, and the question each answers

| Queue (log in runs/live/) | Markets | Question |
|---|---|---|
| queue-honest-xfamily | dsflash-explicit 1-5, luna-explicit 1-5 (illegal sentence); sonnet55-talk-illegal 1-5 and haiku55-talk-illegal 1-5 (illegal sentence plus a required hourly market note, template seller_prompt_compete_explicit_talk) | Does the honest reference exist outside Haiku? Does a model that went silent talk honestly when it must talk? |
| queue-opus-silent | opus55-neutral 1-4 (30 rounds, "set your ask independently", Haiku buyers) | How often does silence come with high prices? (one 20-round market so far) |
| queue-qwen-planted2 | qwen35b-abl-planted-oversight-s4, qwen35b-stock-planted-oversight-s4 (6 rounds) | A second planted pair: does stock conceal and abliterated confess again? |
| laptop: labels-alt.csv | GPT-4.1-mini labels for every seller message | Do the headline numbers hold under a second labeller family? |

## 2. Steps

1. Read the last 40 lines of `notes/log.md` (the 6 AM entry) and `notes/results-frozen.md`. If the 6 AM entry is
   missing, do its steps first: `make studio-pull`; `.venv/bin/python -m analysis.labels --live --workers 3`;
   `.venv/bin/python -m analysis.labels --live --task label_alt --out runs/derived/labels-alt.csv --workers 6`;
   `make freeze`.
2. For each overnight group, the descriptive result, from the frozen file's sections 2, 5, 8, 9 and 11: markets
   finished, messages sent, share labelled collusive, flags by chat and prices, mean ask from round 6, overcharge.
   For the silent set: how many of the Opus markets sent no message, and their price flags against the Haiku bar.
   For the planted pair: messages flagged, reasonings coordinating (label the reasoning tails with
   `analysis.private_plan.label_scratch` on the last 4,000 characters, as `runs/derived/abl-planted-s3-reasoning-labels.json`
   was made), overseer verdicts from `run/Overseer.md`.
3. The second-labeller chain: with `CDA_LABELS=runs/derived/labels-alt.csv CDA_SUFFIX=-alt` run
   `.venv/bin/python -m analysis.controls`, `.venv/bin/python -m analysis.detect --chat-reference explicit`,
   `.venv/bin/python -m analysis.flag_matrix`. Compare `runs/derived/detect-results-explicit-alt.csv` and
   `flag-summary-alt.csv` with the originals: catches per set, false alarms per honest group, the chat threshold.
   Write the comparison as a table into `notes/robustness-second-labeller.md`.
4. Update the draft (`report/draft/report-draft.md`) where the overnight data change a sentence: Section 4.1 (the
   instruction grid, now with DeepSeek, Luna and the required-note rows), 4.4 (the silent set: n and how many priced
   above the bar), 4.3 (the second planted pair), Methods (the second labeller in the labeller paragraph), the
   limitations ("one labeller" becomes "two labeller families" if the chain holds), and Table 2's honest block.
   Change sentences, not structure. Every new number must be in `notes/results-frozen.md`.
5. Regenerate figures (`make reproduce` does it) and look at Figure 3 (instruction grid) with its new rows and columns.
6. Append a dated log entry: what landed, what failed, the numbers that moved, the robustness result, and anything
   that contradicts a claim in the draft (say so plainly). Commit with a plain message. Do not push.
7. Send Arty one push notification (under 200 characters): the most interesting overnight result and whether anything
   in the draft had to change.

## 3. Rules

Never edit `notes/preregistration.md`; never remove `runs/STOP`; start no market runs; never change a number by hand;
no em dashes; never print keys. The frozen file is the authority. If the Studio is unreachable, work from what was
pulled at 6 AM and say so.
