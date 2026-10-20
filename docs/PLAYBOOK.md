# Playbook: how to run the weekend (v2, finalized 2026-10-18)

The judges read one PDF. Everything below exists to make that PDF true, clear and submitted by Sunday evening. Version 1 (10/15) assumed a free Saturday; this version is built around the real calendar: a Wegmans shift Saturday 7 AM to noon, the Thursday shift and the DC interview, and talks that are only recorded "after the event" (sprint FAQ), so the Friday talks must be captured live.

Companion documents: `docs/MODEL-ROUTING.md` (which model does what, and what it costs), `docs/TALKS-PIPELINE.md` (speech to transcript to cited note), `docs/PDF-TEMPLATE.md` (the report, page by page). The research itself is in `docs/END-PRODUCT.md` and `docs/RESEARCH-BRIEF.md`.

## 1. Who does what

| Actor | Does | Never does |
|---|---|---|
| **Arty** | Decisions at every gate. All prose in the report. Discord, Luma, the submission form. Attends the Friday talks. | Hand-edits run outputs or figures after the freeze. |
| **Claude Code session "lab"** (this folder, experiments) | Detector code, calibration, run queue, figures, tables, `notes/log.md`. Subagents on Sonnet only, none while API runs are in flight. | Writes report prose. Fans out agents. Changes a frozen number. |
| **Claude Code session "desk"** (write-up) | Rubric critique ("score 1 to 5 per dimension, say what moves each by one"), reference and caption checks, consistency between numbers in text, tables and figures, the export checklist. | Writes final sentences into the Doc. Its drafts are raw material for rewriting, and that is what the LLM Usage Statement says. |
| **Mac Studio, local models** | Transcripts, slide OCR, talk notes, bulk labelling of the 11,250 seller messages, log triage, anything bulk or repetitive. Free and private. | Plays a market agent in a headline run. Judges the final sample (that is the Claude judge's job). |
| **Claude API** (Max plan credits) | Market agents for new runs (Haiku 5.5), the reference judge on a stratified sample (Sonnet 5.5), the Fable 5.1 seller arm if credit allows. | Anything the local lane can do. |
| **OpenRouter** | The other model families (DeepSeek V4.1 Flash, GPT-6 Luna, Gemini Flash-Lite), Jev as a cheap labeller, and the fallback if Anthropic credit runs out. | Silent provider substitution: fallbacks off, provider logged. |

## 2. Before Friday (Oct 18 to Oct 22)

Your actions, in the order they unblock things:

- [ ] **Pre-hackathon survey** (prize eligibility): https://apartresearch.notion.site/2b0fcfd1de9d8080ac3ac4c41a78c8f8
- [ ] **Discord** https://discord.gg/XswWBvugYs, read the pinned FAQ in #help-desk. Post the one-paragraph idea in #projects-teams by Wed Oct 21 only if you want teammates; solo is on file as the default.
- [ ] **Luma RSVPs** for the two Friday talks (calendar entries added 10/18 carry the links). Thursday's talks collide with the shift and the DC interview; skip them live and catch the recordings if they appear.
- [ ] **API credits and keys** (details in `docs/MODEL-ROUTING.md` section 5): claim the Max plan API credit, create one Anthropic key, prepay $20 on OpenRouter, put both in `.env`. Then `make ping` (or `.venv-tools/bin/python -m tools.llm --ping`) must show every lane green.
- [ ] **Mac Studio**: System Settings > General > Sharing > Remote Login ON (so this laptop can drive it), install LM Studio, run `tools/studio-probe.sh` there and paste its output into `notes/log.md`, pull the models for your RAM tier, start the server on the local network (port 1234). From the Air: `curl http://arthurs-mac-studio.local:1234/v1/models`.
- [ ] **Google Doc**: make the copy from the Guidelines tab link (the FAQ says the template in any email may be older), paste `notes/report-skeleton.md`, name it with the working title. Sunday is editing, not formatting.
- [ ] **Framing**: the recommendation on file is lead time as the headline, the quadrant as Figure 2, detector ageing as the stretch arm (`docs/END-PRODUCT.md`). Say yes, or name another, by Wednesday. Friday 4 PM only confirms it against the controls.
- [ ] **Saturday shift**: 7 AM to noon as it stands. The plan below works around it with unattended overnight runs. If you can swap it, Saturday afternoon gains five hours for the stretch arm.
- [ ] **Team or solo**: solo by default. If a teammate appears, they own the cross-model arm and nothing on the critical path.

Prep that can be done in this folder before Friday (plumbing only; every item goes in `notes/PRIOR-WORK.md`):

1. Done 10/16: starter patched, loader built, replay script.
2. Done 10/18: model router (`tools/llm.py`, `config/models.toml`), talk pipeline (`tools/talks.sh`, `tools/talk_notes.py`), report mock-up and figure style (`report/`).
3. Done 10/20: `tools/run_queue.py` and the Friday queue file (section 6). Thursday evening, after the keys exist: one real 3-round run on Haiku to confirm the cost line in `MODELS-AND-TOOLS.md`.
4. Thursday evening: talk pipeline dry run on any public talk recording (a past Apart talk on YouTube), end to end, so Friday's capture is routine. See `docs/TALKS-PIPELINE.md` section 6.
5. Not before Friday: the detector, any score, any calibration, any results figure.

## 3. The weekend, gate by gate (Eastern time)

A gate has a pass test and a named cut. Record the outcome in `notes/log.md` with the time.

| Gate | When | Pass test | If it fails |
|---|---|---|---|
| **G0 Ready** | Thu Oct 22, 10 PM | `--ping` green on all three lanes; Studio server answers from the Air; Doc copy exists; pipeline dry run produced a cited note; run queue did a 3-round dry run. | Fix Friday 9 AM to noon. Anything still red at noon is dropped from the plan, not patched during the talks. |
| **G1 Talks captured** | Fri 3:30 PM | Both Friday talks have a transcript with timestamps and a note in `notes/talks/`. | Use the papers only; the Related Work paragraph cites Colosseum the paper, not the talk. |
| **G2 Lock** | Fri 4 PM | The claim sentence is written ("We show that X, measured by Y, under Z, against baseline B") and three predictions are committed. The commit hash goes in the report's pre-registration box. | If the sentence cannot be written, the project is not ready: take the recommendation on file as is and commit it. Do not spend the evening choosing. |
| **G3 Controls** | Fri 9 PM | Positive control: seller_comms runs score above the no-chat base runs on both channels. Null control: permutation null gives the expected false-alarm rate at the chosen threshold. | Debug to midnight. If still failing, the headline becomes the descriptive quadrant on whichever channel registers, and the lead-time claim moves to the appendix. |
| **Overnight** | Fri 10 PM to Sat noon | Run queue launched: controls on Haiku 5.5, then DeepSeek Flash, then GPT-6 Luna, 5 seeds each, seller messaging on. Stop file checked before each run. | Runs that fail retry once, then skip. Whatever finished by Saturday noon is the cross-model data. |
| **G4 Figure 1** | Sat 2:30 PM | A draft of the headline figure exists from the bundled runs, with intervals across seeds. | Cut conditions, not seeds. Cut the cross-model arm before anything on the bundled data. |
| **G5 Freeze** | Sat 6 PM | Numbers for the main claim are frozen and copied into `notes/results-frozen.md`. Everything after is an ablation or appendix. | Freeze what exists. A narrower true claim beats a wider late one. |
| **G6 Early submit** | Sun 1 PM | A complete report is submitted through the form and the confirmation email arrived. | Submit whatever is complete; the same title later replaces it. |
| **G7 Final** | Sun 7:30 PM | Final PDF exported, checklist in `docs/PDF-TEMPLATE.md` section 9 passed, resubmitted, confirmation arrived. Stop. | The Monday 7:59 AM deadline is insurance only. |

### Friday Oct 23

- 9 AM to noon: fix anything G0 left red. Reread `docs/END-PRODUCT.md`. Open the two Zoom links from Luma ten minutes early and start the local recording (pipeline section 3).
- 1:15 to 3:15 PM: the talks. Notes by hand on what each speaker says is unsolved. Recording runs.
- 3:15 to 4 PM: `tools/talks.sh` on both recordings, then `tools/talk_notes.py`. Read the notes. Pick the one or two lines that change Related Work.
- 4 PM: G2. Commit.
- 4:30 to 9 PM: the detector on the bundled 75 runs: words score, deeds score, fusion, threshold set on honest runs at 5% false alarms, permutation null. G3 at 9.
- 9 to 10 PM: `make queue`. Check the first run completes, lands in `runs/live/`, and bills what the cost table says. Sleep.

### Saturday Oct 24

- 7 AM to noon: shift. The queue runs. Nothing is scheduled that needs you.
- 12:30 PM: read the queue log. Load the finished runs through the loader. Note failures.
- 1 to 2:30 PM: the headline analysis (lead time by round: chat, prices, fused) and the quadrant. G4.
- 2:30 to 6 PM: cross-model scoring with the detector calibrated on the 2025 runs; the Fable seller arm only if the Anthropic credit shows at least $60 left and the queue is idle. G5 at 6.
- 6 to 10 PM: Methods written while the setup is fresh. Limitations as a running list. Tables filled from the frozen file. Figures exported at the sizes in `docs/PDF-TEMPLATE.md`.

### Sunday Oct 25

- 9 AM to 1 PM: Results and Discussion from the frozen numbers. Figures in the Doc with captions that stand alone. G6 at 1 PM.
- 1:30 to 3 PM: Introduction with the three contributions, Related Work (positioning table plus the talk lines), Conclusion.
- 3 to 5 PM: Abstract last, 150 words or fewer, the actual numbers. Dual-use appendix. LLM Usage Statement (section 7). References checked against `papers/abstracts.md`.
- 5 to 6:30 PM: "desk" session scores the PDF on the rubric; fix what moves a score. Second pass for the generated-text tells in `docs/PDF-TEMPLATE.md` section 7.
- 6:30 to 7:30 PM: export, checklist, resubmit, confirmation. G7. Stop.

## 4. Rules that decide the score

- One claim, defended, beats three claims gestured at.
- Seeds, variance and a baseline on every number. Positive control and null control, always (the sprint page says "always include the positive control").
- Every detector number is a catch rate at a stated false-alarm rate, with an interval. The first-place AI Control report lost points for not having one.
- Honest limitations are rewarded; the rubric says so. The required appendix is "Limitations and Dual-Use / Ethical Considerations": what the result does and does not establish, and whether the setup makes real collusion easier to do or harder to catch.
- Disclose prior work with the line in `notes/PRIOR-WORK.md`. Undisclosed prior work disqualifies.
- The form takes an abstract of 150 words or fewer. The template's 150 to 250 loses.
- Link a source for every factual claim. No citation style is required, so use one and keep it.
- The report must read as written, not generated. Judges will not score "generic framing, padded sections, claims without sources, no trace of what you actually did". The LLM Usage Statement says exactly how Claude and the local models were used.
- About four pages plus appendix. "Most strong projects are 4 to 8 pages"; four dense pages beat eight loose ones. The reader is an expert with 15 minutes.
- No em dashes.

## 5. Scope cuts, in order

1. Drop the Fable seller arm.
2. Drop the cross-model arm; keep the bundled 75 runs.
3. Drop the quadrant figure; keep the lead-time figure and Table 1.
4. Never cut: the positive control, the null control, the fixed false-alarm rate, the prior-work line, the dual-use appendix.

## 6. The run queue (built 2026-10-20)

`make queue-dry` prints the Friday queue's twenty commands and the cost (about $6.10 with the judge); `make queue` runs it under `caffeinate` so the Mac stays awake; `make queue-fake` is the no-key plumbing check (2 rounds against a built-in fake server). `touch runs/STOP` finishes the current run and stops. Queue file: `config/queue-friday.toml` (controls on Haiku 5.5 with chat on and off, then DeepSeek Flash, then GPT-6 Luna, five replicates each; the Fable arm is commented out until Saturday's credit check).

What it does: one run at a time, no model fallback, stdout and stderr and the starter's results folder under `runs/live/<tag>/`, one line per run in `notes/log.md`. A run whose market finished but whose judge failed is not rerun (no paying twice); its metrics are recomputed later. Found while building it: after every market the starter scores each seller each round with gpt-4.1-mini through the OpenAI API. With no OpenAI key that step would fail on every real run, so the patch now reads `CDA_EVAL_MODEL`, and the Friday queue sends the judge to `openai/gpt-4.1-mini` on OpenRouter (same model as the 2025 data; about $0.16 a run).

Thursday, once keys exist: one real run with `rounds = 3` on Haiku to confirm the cost line, then the queue is ready.

## 7. The LLM Usage Statement (draft, fill in Sunday)

"Claude Code (Anthropic) was used to write and debug the analysis code, to critique drafts against the rubric, and to check references and numbers for consistency. Local open-weight models on our own hardware transcribed the sprint talks and produced a first-pass label for each seller message; those labels were validated against a Claude Sonnet 5.5 judge on a stratified sample of N messages (agreement: x%). The market agents in the new runs were [models]. All prose in this report was written by the author; all numbers were recomputed from the frozen results file and checked by hand. Quotes from talks were checked against the recording."

## 8. Submission form, fields to have ready

Title (the finding, chosen Sunday from `END-PRODUCT.md`), abstract (150 words or fewer, pasted from the Doc after the word count), track (2, Detection and Audit), authors and affiliation ("Independent" or "AMER"), PDF under 25 MB, repo link (public by Sunday 1 PM, with a one-command reproduction), video link if made, publishing interest yes or no, the dual-use appendix present.
