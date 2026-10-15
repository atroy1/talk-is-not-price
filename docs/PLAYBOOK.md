# Playbook: how to run the weekend

The judges read a 4-page PDF. Everything below exists to make that PDF true, clear and done by Sunday evening.

## Before the sprint (Oct 15 to Oct 22)

Your actions (I cannot do these for you):

- [ ] Fill the pre-hackathon survey (required for prize eligibility and team matching): https://apartresearch.notion.site/2b0fcfd1de9d8080ac3ac4c41a78c8f8
- [ ] Join the Discord https://discord.gg/XswWBvugYs and read the pinned FAQ in #help-desk. Post a one-paragraph project idea in #projects-teams by Wed Oct 21 if you want teammates.
- [ ] RSVP on Luma for the Fri Oct 23 talks (Anwar 1:15 PM ET; Bagdasarian and Nakamura 2:15 PM ET). The Thursday steganography talks matter only for Track 3 picks.
- [ ] Load API keys: an OpenAI key and an OpenRouter key cover every starter repo. Budget $30 to $60. Put them in `.env` at the project root (gitignored); never in the vendor folders.
- [ ] Decide solo or team. Solo is fine; the first-place AI Control report was two people.
- [ ] Make a copy of the Google Doc template now and paste the skeleton from `notes/report-skeleton.md` into it, so Sunday is editing, not formatting.

Prep work (can be done here, in this folder, before Friday):

1. Read the six papers marked "read first" in `papers/README.md`. Two hours.
2. Run the double-auction starter once end to end with cheap models and 5 rounds. Confirm cost per run. Fix model names.
3. Build the analysis notebook on the **bundled 75 runs** in `vendor/llm-agent-collusion/data` (base, seller_comms, oversight, boss_pressure, and mixed-model conditions, each with per-agent transcripts, `collusion_metrics.json`, and an LLM-judge file). This is free, offline, and gives Figure 1 before the sprint starts. Disclose it as prior data in the report.
4. Write the one-sentence claim and the positive control before writing any new code.

## The weekend (Eastern time)

**Friday Oct 23**
- 1:15 to 3:15 PM: the two talks. Take notes on what the speakers say is unsolved; that is the Related Work paragraph.
- 4 PM: lock the research question. Write the claim sentence: "We show that X, measured by Y, under conditions Z, compared with baseline B." If the sentence cannot be written, the project is not ready.
- Evening: run the positive control (a setup where collusion is known to occur) and the null control (a setup where it cannot). Both must register correctly before anything else runs.

**Saturday Oct 24**
- Morning: main experiments, 3 seeds minimum per condition. Log every run with its config.
- 2 PM gate: is there a draft Figure 1? If not, cut conditions, not seeds.
- 6 PM gate: results frozen for the main claim. Anything after this is an ablation or goes to the appendix.
- Evening: write Methods while the setup is fresh. Write Limitations as you notice them, in a running list.

**Sunday Oct 25**
- 10 AM: write Results and Discussion from the frozen numbers. Figures numbered, captions stand alone.
- 1 PM: submit a complete early version through the form (same title later replaces it). This removes deadline risk.
- 3 PM: Introduction with the three contributions, Related Work, Conclusion.
- 5 PM: Abstract last, with the actual numbers. Dual-use appendix. LLM usage statement. References checked.
- 7 PM: final PDF, resubmit, confirm the form acknowledges it. Stop.

## Rules that decide the score

- One claim, defended, beats three claims gestured at.
- Seeds, variance and a baseline on every number. A positive control and a null control, always.
- Report a false-positive rate at a fixed threshold for any detector. The first-place AI Control report lost points for not having one.
- Honest limitations are rewarded; the rubric says so. Say what the result does not establish.
- Disclose prior work precisely: "the 75 runs are from Agrawal et al. 2025; the detector, the fusion and all analysis are new."
- The report must be primarily your own writing. Use Claude for drafts, critique and checking; rewrite in your voice; state that in the LLM Usage Statement.
- Four pages. The reader is an expert with 15 minutes. Cut.
- At least one figure that makes the result obvious without the text (your strength; use it).
- No em dashes.

## Scope cuts, in order, if time runs out

1. Drop the second dataset; keep one.
2. Drop model diversity; keep one cheap model.
3. Drop the fresh API runs entirely; the bundled data alone supports a detection paper.
4. Keep the controls and the FPR. Never cut those.

## Working with Claude during the sprint

- One session for the experiment code, one for the write-up. Keep this folder as the single source of truth; `notes/log.md` records every run and every decision with the time.
- Ask for critique in the judges' terms: "score this draft 1 to 5 on each rubric dimension and say what would move each score by one."
- Do not let an agent fan out; each API run costs money and the budget is small.
