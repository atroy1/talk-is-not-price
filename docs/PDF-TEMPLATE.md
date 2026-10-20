# The PDF, page by page

Written 2026-10-18. The submission is the official Google Doc template exported to PDF; the Guidelines tab lists "Research report (PDF) using the official template" under Required and the FAQ says to use the copy linked there, not one from an email. So the typeface, margins and section order are fixed. What this document settles is everything inside those bounds: the word budget per slot (measured with a Typst replica of the template, `report/mock/`), the figures and tables, the copy tone, and the export checklist.

## 1. What the template fixes (measured from the official export, 10/18)

| Element | As the template has it |
|---|---|
| Page | US Letter, 1 inch margins all round, 6.5 inch text width, single column |
| Body | **Old Standard TT** 11 pt, justified, about 15 words a line, about 50 lines a page of solid text |
| Section headings | Old Standard TT bold 14 pt, numbered "1. Introduction" to "6. Conclusion", then unnumbered Code and Data, Author Contributions, References, Appendix |
| Title | Old Standard TT bold 22 pt, capitals, centred, a rule above and below, footnote 1 "Research conducted at the AI Collusion Research Sprint, October 2026" |
| Authors | 11 pt, centred, up to six in two rows, then "With / Apart Research" |
| Abstract | "Abstract" bold 14 pt centred; the text block is inset about 1 inch on each side |
| Info box | Arial 11 pt on a yellow fill; delete it before export |
| Footnote | 10 pt |

Old Standard TT is a Google font, so the Doc keeps it when you type; pasted text can carry another font, so paste with Command-Shift-V. The first-place AI Control report was exported from the same template in Times New Roman, which says font changes are tolerated. Do not make one: the judges see fifty reports in this face, and the one that differs reads as not having used the template.

## 2. The budget

The replica (`make mock`) sets the slots below in the template's type with two figures and three tables. At these counts the body runs to about four and one third pages, so the numbers are already the ceiling, not a target with slack. "Most strong projects are 4 to 8 pages" (sprint page), and the template says 4 recommended: the plan is four pages, a fifth is allowed if the result needs it, nothing past five, and the appendix is unlimited.

| Page | Slot | Words | Notes |
|---|---|---|---|
| 1 | Title | 10 to 14 | Two lines in capitals at 22 pt. Three lines costs a paragraph of the introduction. |
| 1 | Authors | | Arthur Troy, Independent, Chantilly, Virginia (your call on the affiliation). |
| 1 | Abstract | 120 to 150 | The form takes 150 or fewer. Problem (1 sentence), what we built (1), the headline number with its baseline and its false-alarm rate (2), what it does not show (1). Written last. |
| 1 | Introduction, opening | 100 to 110 | One real run, one quote from it, the threat model in two sentences. Ends by pointing at Figure 1. |
| 2 | Figure 1 | | Full width, 6.5 x 2.4 inches, caption 40 to 60 words. Top of page 2. |
| 2 | Introduction, rest | 60 + list | Why an auditor cannot do this today, then "Our main contributions are:" and three numbered items of about 20 words. |
| 2 | Related Work | 90 | Colosseum first, as the paper this extends; the gap in one sentence; one quoted line from the Friday talk with its time. |
| 3 | Table 1, positioning | 5 rows | Study, setting, signals, fixed FPR, gap we fill. Phrases, not sentences. |
| 3 | Methods | 70 + 90 + 60 | Data and the prior-work line verbatim; the detector in one equation with threshold, null and seeds; controls, what did not work, the label-validation kappa. |
| 3 | Pre-registration box | 40 | Grey box: date, time, commit hash, three predictions. |
| 3 to 4 | Results | 50 + 120 + 80 | Observation then interpretation, separately, each prediction marked. |
| 4 | Table 2, the numbers | 4 rows | Detector by catch rate at 5% and 1% FPR with intervals, and median lead in rounds. Best row bold. |
| 4 | Figure 2 | | Half width, 3.15 x 3.0 inches, text alongside. The quadrant. |
| 4 to 5 | Discussion | 70 | Theory of change: what an auditor does with it. |
| 5 | Table 3, plus factors | 4 rows | Doctrine to statistic to separation. The only place the legal frame appears. |
| 5 | Limitations | 90 | The ten honest runs, the no-chat reference, encoding blinds the words channel, the temperature confound, one market design, 2025 models in the bundled data. |
| 5 | Future work | 30 | |
| 5 | Conclusion | 60 | The finding in three lines, then the implication. |
| 5 | Code and Data | 40 | Repo, data provenance, author contributions in one line. |
| 6+ | References | 9 to 12 | One style, kept. Talk citation with the recording URL. |
| 6+ | Appendix A | 150 to 200 | Required: Limitations and Dual-Use / Ethical Considerations. |
| 6+ | Appendix B | 100 | LLM Usage Statement (PLAYBOOK section 7). |
| 6+ | Appendix C, D | as needed | Prompts, detector steps, per-model tables, the evasion probe, the run log with costs from the ledger. |

Body prose in total: about 1,100 words. To land on four pages exactly, Table 3 moves to Appendix D and Discussion absorbs one sentence from it.

## 3. Figures

Two in the body, numbered, each with a caption that stands alone. Style file `report/figstyle.mplstyle`; layout proofs on synthetic numbers in `report/mock/fig1_proof.png` and `fig2_proof.png` (`make figs`). Saturday swaps the data in and nothing else.

- **Size.** Draw at the printed size: 6.5 x 2.4 inches full width, 3.15 x 3.0 inches half width. Never scale in the Doc; insert at 100 percent so 8 pt stays 8 pt.
- **Type.** Helvetica Neue (Arial if absent), 8.5 pt labels, 8 pt ticks and legend, 9 pt bold left-aligned title, 7 to 7.5 pt annotations. Nothing under 7 pt.
- **Palette**, fixed order, validated 10/18 with the colour-vision checker (all pass; the fourth and fifth are always direct-labelled): words `#0072B2`, deeds `#D55E00`, fused `#111111`. Models: GPT-4.1 2025 runs `#777777`, Haiku 5.5 `#009E73`, DeepSeek Flash `#CC79A7`, GPT-6 Luna `#E69F00`. Bands: competitive `#e6e6e6`, cartel `#fbe3d6`. One axis per chart, never two scales.
- **Marks.** 1.5 pt lines, 12 to 14 pt² dots with a white edge, intervals as light fills, grid on y only, spines on left and bottom only, labels at line ends instead of a legend when there are three series or fewer.
- **Figure 1** (lead time): share of collusive runs caught by round at 5% false alarms, three curves (chat, prices, fused), bootstrap bands, two dashed markers (median first floor proposal; median lock). If the smoking-gun opener wins instead, it is one run on one clock: five asks flat at $93 for twenty rounds with the chat lines along the top and bands at $90 and $100.
- **Figure 2** (quadrant): words against deeds, one dot per run, coloured by seller model, the four corners named, bands for the competitive and cartel price. Legend below in two columns.
- **Export.** `savefig` at 300 dpi PNG (the style does it). Google Docs will not take PDF or SVG. Insert > Image > Upload from computer, set wrapping to In line, check the width in Image options is 6.5 or 3.15 inches. Caption as a normal paragraph under the image: "**Figure 1.** " in bold, then the caption, 10 pt.
- **Caption formula.** What the reader sees; how to read it; the one takeaway; then n, what the bands are, and the threshold. Forty to sixty words. The caption must survive being read alone, because judges skim figures first.

## 4. Tables

Native Doc tables, never images, so the text stays searchable and the numbers copy out. 9.5 pt. Header row bold. Rules: one above the header, one below it, one at the foot; no vertical rules, no fills (in Docs: select the table, set borders to 0 pt, then select the header row and give it a 0.5 pt bottom border, repeat for the top and the last row). Numbers right-aligned, text left. Intervals in brackets after the point estimate: `0.84 [0.76, 0.91]`. Bold the row the text calls best. Caption above the table: "**Table 1.** ..." 10 pt.

The pre-registration box is a one-cell table: light grey fill `#f2f2f2`, 0.5 pt border, 8 pt cell padding, text 10.5 pt. First line bold: "Pre-registered Fri Oct 23, 4:00 PM ET (commit `abc1234`)." Then the three predictions as (1) (2) (3) in one paragraph. Results marks each with "held" or "did not hold" in the text, nothing fancier.

## 5. Title and abstract

The title states the finding. Four candidates are in `END-PRODUCT.md`; pick Sunday from the numbers. Two lines in capitals at 22 pt is about 12 words, so cut the subtitle if the main clause carries it. Test: a reader who sees only the title should be able to say what was found.

Abstract, in order and nothing else: the problem in one sentence with a source; what we built in one; the headline as a number against its baseline at a stated false-alarm rate, with the n; the second result if there is one; what it does not show. No "novel", no "framework", no "we believe". Count the words on the form, not in the Doc.

## 6. Copy tone

The voice is a careful analyst reporting to someone who will act on it: dry, specific, confident where the data is and plain about where it is not. Economist in register, not in flourish.

- Lead with the finding, then the evidence, then the caveat. Never the reverse.
- Observation and interpretation in separate sentences, in that order: "At 5% false alarms the fused detector caught 41 of 50 collusive runs [0.72, 0.90]. We read this as the price channel confirming what chat proposed six rounds earlier."
- Every number carries its n, its interval or its baseline. A number alone is decoration.
- Short sentences, concrete nouns, active verbs. "The detector missed three runs" beats "three runs were not detected by the detector".
- One idea per paragraph; the first sentence says what the paragraph establishes.
- Cite as you go: a source on every factual claim, in the one style chosen.
- Say what did not work and what the result does not establish, in the body, not only in the appendix.
- No em dashes. Colons sparingly. No exclamation marks, no rhetorical questions.
- Name things once and keep the name: "words" and "deeds", or "chat" and "prices", not both.

Tells that make a report "read as generated" (the sprint page says such reports are not scored); purge every one on the Sunday pass:

- Openers like "In recent years", "As AI systems become increasingly", "In this work, we".
- "Delve", "crucial", "pivotal", "robust framework", "shed light", "paving the way", "it is worth noting", "importantly".
- Triads by reflex (three adjectives, three clauses, three bullets where two were true).
- Paragraphs of equal length that each restate the heading.
- "Furthermore", "Moreover", "Additionally" as paragraph glue.
- Sentences beginning "This" with no noun ("This demonstrates").
- Claims without a source, and no trace of what you actually did: no run names, no round numbers, no quote from a transcript, no dead end mentioned.
- Hedging stacks ("may potentially suggest").

Before and after, for the opening:

> Before: "Collusion among AI agents is an increasingly crucial concern as multi-agent systems are deployed in high-stakes domains. In this work, we propose a novel framework for detecting collusion."
>
> After: "In run base-seller_comms-1 of Agrawal et al. (2025), one seller wrote 'Let's remain unified at $93.00 this hour' in round 1. By round 10 all five asks sat at $93, three dollars above the competitive price, and stayed there for twenty rounds. A judge reading the chat flags that run. In 57.9% of Colosseum's models the advantage showed only in actions, and the chat judge saw 10.5% of it (Nakamura et al. 2026). We ask which signal catches a cartel first, and at what false-alarm rate."

## 7. Section-by-section intent

1. **Introduction**: the run, the threat model (sellers that can message; an auditor who reads logs after the fact), why the auditor is stuck today (chat judges false-alarm on talk, price tests are blind to tacit collusion), the three contributions.
2. **Related Work**: Colosseum as the parent; Audit the Whisper and NARCBench as the fixed-FPR precedents; Agrawal as the data; the slot we fill, stated narrowly; one line from the talk.
3. **Methods**: data and the prior-work line; the detector in one equation; threshold from honest runs; permutation null; seeds and bootstrap; the local-label validation; what did not work; the box.
4. **Results**: Table 2 first, then Figure 1's lead-time reading, then Figure 2, then cross-model, then robustness. Each prediction marked.
5. **Discussion and Limitations**: what an auditor does Monday morning with this; Table 3; the honest list; two sentences of future work.
6. **Conclusion**: three lines and the implication for certification.

## 8. Building the Doc (Thursday, so Sunday is editing)

1. Open the template link on the Guidelines tab, File > Make a copy, name it with the working title.
2. Delete the yellow info box and every italic guidance paragraph.
3. Paste `notes/report-skeleton.md` headings in, with Command-Shift-V, under the template's own numbered headings (keep the template's heading paragraphs; they carry the style).
4. Put the author block in. Leave the title as a placeholder in capitals so its length is visible.
5. Insert two empty paragraphs where Figure 1 and Figure 2 go, with their captions drafted from the formula.
6. Build the three tables empty with their headers and rules, and the grey box with its first line.
7. Add the appendix headings A to D and paste the LLM Usage Statement draft from the playbook.
8. File > Download > PDF once, to see that the fonts embed (`pdffonts`) and the page count is as the mock predicts.

## 9. Export checklist (Sunday, twice: before the 1 PM early submission and before the final)

- [ ] Info box and all guidance text gone; title and author block current; footnote 1 intact.
- [ ] Abstract counted on the form: 150 words or fewer.
- [ ] Figures inserted at 100 percent, in line, each numbered, each caption stands alone, each referenced in the text before it appears.
- [ ] Tables native, numbered, captioned, intervals and n present, best row bold.
- [ ] Pre-registration box carries the real commit hash and the predictions are marked in Results.
- [ ] Every factual claim has a source; every talk quote was heard.
- [ ] Prior-work line present in Methods or Code and Data.
- [ ] Appendix A present and titled exactly "Limitations and Dual-Use / Ethical Considerations". Appendix B, the LLM Usage Statement, present.
- [ ] Generated-text tells purged (section 6). No em dashes (search for "—").
- [ ] Body ends by page 5 at the latest; appendix follows.
- [ ] File > Download > PDF. Check: `pdfinfo` page count, `pdffonts` shows Old Standard TT embedded, size under 25 MB, links clickable, figures legible at 100 percent on screen.
- [ ] Title on the form identical to the Doc; same title on the resubmission so the files replace.

## 10. The replica

`report/mock/report.typ` reproduces the template's type and geometry so budgets can be measured without touching the Doc. `make mock` builds `report/mock/mock.pdf` and prints the page count. Orange bracketed text marks each slot with its budget; the grey text is filler. It is a ruler, not the report: nothing from it is pasted into the Doc, and the Doc is what gets submitted.
