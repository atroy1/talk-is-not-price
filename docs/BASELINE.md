# Baseline: Apart Research AI Collusion Research Sprint

Written 2026-10-15. Sources: the sprint page, Apart's sprint index, past sprint pages, the registration email (Oct 13, to arthur.troy@me.com), the official report template, and the first-place report from the AI Control Hackathon 2026.

## The event

- **What:** AI Collusion Research Sprint, by Apart Research with Poseidon Research and AE Studio. Support from Modal and The AI Alignment Foundation.
- **When:** Fri Oct 23 to Sun Oct 25, 2026. Online, with in-person hubs (nearest: NYC at Collider, Atlanta at Georgia Tech AISI).
- **Deadline:** Sun Oct 25, 11:59 PM Anywhere on Earth. That is **Mon Oct 26, 7:59 AM Eastern**. Plan to submit Sunday evening ET and treat the Monday morning slack as insurance only.
- **Theme:** collusion between AI agents in markets and everyday deployments. Three tracks: (1) Markets and Collusion, (2) Detection and Audit, (3) Carriers and Countermeasures. Twelve numbered research questions, each with starter code and a $0 to $150 budget estimate. Full list in `TRACK-PICKS.md`.
- **Designed for:** a 16 GB laptop with no GPU and low-cost API models. The $250 Modal credit is for in-person hub teams only.
- **Status of your registration:** registered Oct 13. The email says the **pre-hackathon survey is required**; without it you are an observer, not eligible for prizes or team matching.
- **Links:** sprint page https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 · Discord https://discord.gg/XswWBvugYs (channels: #announcements, #projects-teams, #hack-and-chat, #help-desk) · report template (Google Doc, make a copy) https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy · survey https://apartresearch.notion.site/2b0fcfd1de9d8080ac3ac4c41a78c8f8 · email sprints@apartresearch.com

## Schedule (Eastern time)

| When | What |
|---|---|
| Thu Oct 22, 10:15 AM | Joan Velja (Oxford): How concerned should we be by steganography? (Zoom, RSVP luma.com/ai-collusion-research-sprint-joan-velja) |
| Thu Oct 22, 1:15 PM | Sumeet Motwani (Oxford): We're Not Prepared for Steganographic Collusion (luma.com/ai-collusion-research-sprint-sumeet-motwani) |
| Fri Oct 23, 1:15 PM | Usman Anwar (Cambridge): steganography detection, CoT monitorability (luma.com/ai-collusion-research-sprint-usman-anwar) |
| Fri Oct 23, 2:15 PM | Eugene Bagdasarian and Mason Nakamura (UMass): Colosseum, auditing collusion (luma.com/ai-collusion-sprint-bagdasarian-nakamura) |
| Sat 10 AM to Sun 6 PM | NYC hub open (in person only) |
| Mon Oct 26, 7:59 AM | Hard deadline (Sun 11:59 PM AoE) |

Talks are recorded and posted to Discord. Attendance is not required. Teams form before or during the sprint in #projects-teams; solo is allowed; up to 5 recommended.

## How Apart sprints have worked (numbers from recent sprints)

| Sprint | Sign-ups | Projects submitted | Submission rate |
|---|---|---|---|
| AI Control, Mar 2026 | 792 | 125 | 16% |
| Secret Loyalties, Jul 2026 | 739 | 177 | 24% |
| Digital Minds, Aug 2026 | 950 | 233 | 25% |
| AI Incident Response, Sep 2026 | n/a | 231 | n/a |

- Five cash prizes per sprint: $1,000 / $500 / $300 / $100 / $100. With 125 to 233 submissions, a cash prize goes to roughly 2 to 4 percent of projects. The realistic goals, in order: a complete, honest 4-page report; judge feedback worth having; a top-5 finish.
- Winners also get fellowship fast-tracking, mentor introductions, and a path to a publishable write-up. Results come 1 to 2 weeks after the judging deadline; written feedback is emailed to every team.
- Judges are external experts (30+ for AI Control). Each project is assigned to judges who read **only the PDF**. Code, video and slides are optional and secondary.
- Unfinished submissions are accepted and judged on what was done. Resubmission before the deadline replaces the earlier files (same title).
- Multiple submissions are allowed with distinct titles.

## The rubric (three dimensions, each 1 to 5)

**Impact Potential & Innovation.** 3 = clear problem, reasonable approach, some novelty in framing or method. 4 = important problem with an original approach, or a neglected problem area; others could build on it. 5 = opens a new direction, clear theory of change. Judges explicitly check at 4 and 5 whether the work replicates recent papers.

**Execution Quality.** 3 = technically solid for the timeframe, interpretable results, limitations acknowledged. 4 = thorough methodology with convincing validation; immediately useful. 5 = ambitious scope executed rigorously, surprising findings or unusually robust validation.

**Presentation & Clarity.** 3 = problem, method, findings and limitations all findable. 4 = easy to follow, right level of detail. 5 = a model for how to present this kind of work.

Guidance printed on the sprint page: report variance, seeds and baselines; **always include the positive control**; state what the result does and does not establish; identify clearly what was new work during the sprint. Undisclosed prior work disqualifies.

## What the template asks for

Official template (copy saved at `docs/apart-report-template.txt`):

- Title, up to 6 authors with affiliations, "With Apart Research".
- Abstract 150 to 250 words: problem, approach, key results, main takeaway. Polish it last.
- **Recommended length: 4 pages excluding references and appendix.** Intro and related work 1 page, methods and results 2.5 pages, discussion 0.5 page.
- 1 Introduction with a numbered list of contributions. 2 Related Work (when would someone use this over the state of the art; what do we know now that we did not). 3 Methods (replicable; what did not work). 4 Results (at least one numbered figure with a caption that stands alone; distinguish observation from interpretation; is the difference significant, is it robust). 5 Discussion and Limitations (assumptions and how conclusions change if they fail; future work). 6 Conclusion. Code and Data links. Author contributions. References. Appendix. **LLM Usage Statement** (required to be honest: how LLMs were used; the final text must be primarily the team's own).
- The submission form also requires a separate "Limitations and Dual-Use / Ethical Considerations" appendix, track selection, and a yes/no on interest in publishing.

## Anatomy of a first-place report

"Omission Attacks: When Doing Nothing Is the Attack" (AI Control Hackathon, Mar 2026; 2 authors; 9 pages with references; copy at `docs/reference-winning-report-ai-control-2026.pdf`).

What it did in one weekend: named an under-studied attack class, built a 14-item taxonomy, hand-wrote 5 attack traces, ran them through every monitor tier of an existing framework, reported head-to-head numbers against the existing baseline (4.0/10 on the best monitor vs 92.3/100 for known attacks), then proposed a fix (postcondition monitoring) and tested it on the same traces (5 of 5 caught).

Why it won: one vivid example in the abstract (the agent "forgets" ip6tables); a clean contrast number; the gap and the fix in the same paper; a reusable framing others can build on.

What the judges still dinged: no repeated runs to average LLM variance, no false-positive rate, possible overfitting of the fix via task-specific prompts, monitor configuration under-described. A project that shows seeds, repeats and an FPR at a fixed threshold outscores this on Execution.

Lesson from Secret Loyalties (Jul 2026): several teams' detections vanished under matched control models. Calibration against a null control is now expected, not a bonus.

## Where you stand (this machine)

- MacBook: Apple M2, 16 GB RAM, about 14 GB disk free (tight; the vendor repos are 1.8 GB).
- Python 3.12 and 3.14 via Homebrew; no uv or conda. A 3.12 venv is at `.venv` with the double-auction starter installed and its CLI running.
- API keys: none of OPENAI, ANTHROPIC, OPENROUTER, GOOGLE, GROQ are set in the shell. The Modal CLI is installed but there is no token file. The starter repos read keys from `.env` files or environment variables.
- Model names in the starter repos are from mid-2025 (gpt-4.1-mini, claude-3-5-haiku, gemini-2.5-flash-preview). Expect to update `SUPPORTED_MODELS` to whatever is live and cheap on sprint day.
