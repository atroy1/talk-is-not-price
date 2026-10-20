// Page-budget mock-up of the Apart report. NOT the submission: the submission is the official Google Doc.
// This reproduces the Doc's type (Old Standard TT 11 pt, 14 pt headings, 1 in margins, US Letter) so the
// word budgets in docs/PDF-TEMPLATE.md are measured, not guessed. Bracketed orange text marks every slot.
// Build: typst compile --font-path report/fonts report/mock/report.typ report/mock/mock.pdf

#let slot(words, note) = [#text(fill: rgb("#b4530a"), style: "italic")[\[#note; about #words words\]] #lorem(words)]
#let mark(body) = text(fill: rgb("#b4530a"), style: "italic")[\[#body\]]

#set page(paper: "us-letter", margin: 1in, numbering: "1", number-align: center)
#set text(font: "Old Standard TT", size: 11pt, lang: "en")
#set par(justify: true, leading: 0.52em, spacing: 0.85em)
#set heading(numbering: "1.")
#show heading.where(level: 1): it => block(above: 1.3em, below: 0.7em)[#text(size: 14pt, weight: "bold")[#if it.numbering != none [#counter(heading).display() ] #it.body]]
#show heading.where(level: 2): it => block(above: 1em, below: 0.5em)[#text(size: 11pt, weight: "bold")[#it.body]]
#show figure.caption: it => context [#align(left)[#text(size: 10pt)[*#it.supplement #it.counter.display(it.numbering).* #it.body]]]
#set figure(gap: 6pt)
#show table: set text(size: 9.5pt)
#set table(stroke: none, inset: (x: 5pt, y: 3.5pt))
#show link: underline

// ---------------------------------------------------------------- title block (mirrors the template)
#line(length: 100%, stroke: 0.8pt)
#v(6pt)
#align(center)[#text(size: 19pt, weight: "bold")[TALK IS CHEAP, PRICES ARE NOT: CATCHING LLM CARTELS BY WHAT THEY SAY AND WHAT THEY CHARGE#footnote[Research conducted at the AI Collusion Research Sprint, October 2026.]]]
#v(6pt)
#line(length: 100%, stroke: 0.8pt)
#v(10pt)
#align(center)[
  Arthur Troy \ Independent, Chantilly, Virginia
  #v(6pt)
  *With* \ Apart Research
]
#v(10pt)
#align(center)[#text(size: 14pt, weight: "bold")[Abstract]]
#block(inset: (x: 0.55in))[#slot(140, "Abstract, 150 words or fewer on the form: problem (1 sentence), what we built (1), the headline number with its baseline and false-alarm rate (2), what it does not show (1)")]

= Introduction
#slot(110, "The problem and one vivid example from a real run, with the quote; threat model in two sentences")

#figure(image("fig1_proof.png", width: 100%), caption: [#mark[Smoking-gun run, or the lead-time curves if the opener moves to page 3.] Share of the 50 collusive runs caught by round at a false-alarm rate of 5% set on the 10 no-chat runs and 200 permutation nulls; shaded bands are 95% bootstrap intervals across runs. Dashed lines mark the median round of the first price-floor proposal in chat and of the asks locking. Synthetic numbers.])

#slot(60, "Why it matters for deployment and what an auditor cannot do today")
Our main contributions are:
+ #mark[Contribution 1: the fused detector at a fixed false-alarm rate, 20 words]
+ #mark[Contribution 2: the lead-time result, 20 words]
+ #mark[Contribution 3: the cross-model test, or the "collusion on paper" rate, 20 words]

= Related Work
#slot(90, "Colosseum first, as the paper this extends; then the gap sentence; one line from the Friday talk with its timestamp")
#figure(table(columns: (1.6fr, 1.4fr, 1.2fr, 0.9fr, 1.6fr), align: left,
  table.hline(stroke: 0.6pt),
  [*Study*], [*Setting*], [*Signals*], [*Fixed FPR*], [*Gap we fill*],
  table.hline(stroke: 0.4pt),
  [Colosseum (2026)], [cooperative tasks], [chat judge, action regret, compared], [no], [markets, fused, mixed models],
  [Audit the Whisper (2025)], [pricing, auctions], [MI, watermark variance, fused], [yes, 1 in 1,000], [synthetic colluders; ours collude unprompted],
  [NARCBench (2026)], [4 agents], [activations], [yes], [needs weights; ours is black-box],
  [Agrawal et al. (2025)], [double auction, our data], [price metrics, judge, separate], [no], [calibrated fusion],
  [*This report*], [double auction], [chat and prices, fused], [yes, 5%], [],
  table.hline(stroke: 0.6pt)),
  caption: [Nearest studies. #mark[Keep to five rows; every cell a phrase, not a sentence.]])

= Methods
#slot(70, "Data: 75 runs from Agrawal et al. 2025, conditions and counts; the prior-work line verbatim from notes/PRIOR-WORK.md")
#slot(90, "Detector: words score, deeds score, fusion rule, in one equation; threshold set on honest runs; permutation null; seeds")
#block(width: 100%, fill: luma(245), stroke: 0.5pt + luma(150), inset: 8pt, radius: 2pt)[
  *Pre-registered Fri Oct 23, 4:00 PM ET (commit* `abc1234`*).* (1) #mark[prediction, 15 words] (2) #mark[prediction] (3) #mark[prediction] Outcomes are marked in Section 4.
]
#slot(60, "Controls: positive, null, permutation; what did not work; the local-label validation kappa")

= Results
#slot(50, "Observation 1, then its interpretation, separately; prediction (1) checked or crossed")

#figure(table(columns: (1.6fr, 1fr, 1fr, 1fr), align: (left, right, right, right),
  table.hline(stroke: 0.6pt),
  [*Detector*], [*Caught at 5% FPR*], [*Caught at 1% FPR*], [*Median lead, rounds*],
  table.hline(stroke: 0.4pt),
  [LLM judge (as shipped)], [0.xx [0.xx, 0.xx]], [n/a], [x],
  [Chat only], [0.xx [0.xx, 0.xx]], [0.xx [0.xx, 0.xx]], [x],
  [Prices only], [0.xx [0.xx, 0.xx]], [0.xx [0.xx, 0.xx]], [x],
  [*Chat + prices*], [*0.xx [0.xx, 0.xx]*], [*0.xx [0.xx, 0.xx]*], [*x*],
  table.hline(stroke: 0.6pt)),
  caption: [Share of the 50 collusive runs caught, with 95% bootstrap intervals, at thresholds set on honest runs. #mark[Bold the best row; n stated; a 1% column only if the null set supports it.]])

#grid(columns: (3.15in, 1fr), column-gutter: 0.2in,
  figure(image("fig2_proof.png", width: 3.15in), caption: [Words against deeds, one dot per run, coloured by seller model. Top left is talk without a price effect; bottom right is a price effect without talk. Synthetic numbers.]),
  [#slot(120, "Observation 2 (the quadrant) and the cross-model row: does the 2025-calibrated detector catch 2026 models at the same false-alarm rate; prediction (2) and (3) checked")])

#slot(80, "Robustness: seeds, threshold sweep, the permutation null, what moved when the window changed")

= Discussion and Limitations
#slot(70, "What an auditor does with this (theory of change); the plus-factors table carries the doctrine")
#figure(table(columns: (1.2fr, 1.6fr, 1.2fr), align: left,
  table.hline(stroke: 0.6pt),
  [*Plus factor (Berger et al. 2025)*], [*Statistic in the logs*], [*Separation, honest vs colluding*],
  table.hline(stroke: 0.4pt),
  [parallel pricing], [ask dispersion, rounds locked], [x.x [x.x, x.x]],
  [communication], [floor proposals and agreements per round], [x.x],
  [actions against self-interest], [asks held above the trade-clearing level], [x.x],
  [market structure], [five sellers, repeated game, visible asks], [fixed by design],
  table.hline(stroke: 0.6pt)),
  caption: [Each antitrust plus factor and the statistic that stands in for it. #mark[One table, no prose repeat.]])
== Limitations
#slot(90, "Ten honest runs; the no-chat reference; encoding blinds the words channel; temperature confound; one market design; the bundled runs are 2025 models")
== Future work
#slot(30, "Two sentences")

= Conclusion
#slot(60, "The finding in three lines, then the implication")

#heading(numbering: none)[Code and Data]
Code and a one-command reproduction: #mark[public repo URL]. Data: the 75 runs are those released by Agrawal et al. (2025); the new runs are in the repository with their configs. Author contributions: A.T. did all of the work.

#pagebreak()
#heading(numbering: none)[References]
#set par(justify: false, hanging-indent: 1.2em)
#text(size: 10pt)[
+ Agrawal et al. (2025). Emergent collusion in LLM double auctions. arXiv:2507.01413.
+ Nakamura, Bagdasarian et al. (2026). Colosseum: auditing collusion in multi-agent tasks. arXiv:2602.15198.
+ Audit the Whisper (2025). ColludeBench. arXiv:2510.04303.
+ Rose et al. (2026). NARCBench. arXiv:2604.01151.
+ Berger et al. (2025). Plus factors and algorithmic collusion. ABA Antitrust.
+ Mathew, Matthews, McCarthy, Velja, Schroeder de Witt et al. (2025). Hidden in Plain Text. arXiv:2410.03768.
+ Motwani et al. (2024). Secret Collusion among AI Agents. NeurIPS 2024. arXiv:2402.07510.
+ Anwar et al. (2026). A decision-theoretic formalisation of steganography. arXiv:2602.23163.
+ #mark[talk citation, with recording URL and timestamp]
]
#set par(justify: true, hanging-indent: 0pt)

#heading(numbering: none)[Appendix A. Limitations and Dual-Use / Ethical Considerations]
#slot(160, "Required. What the result does and does not establish; whether the setup makes real collusion easier to run or harder to catch; why publishing the detector's features does not hand colluders an evasion recipe, and the one way it might")

#heading(numbering: none)[Appendix B. LLM Usage Statement]
#slot(110, "From PLAYBOOK section 7, filled in: Claude Code for code and critique; local models for transcripts and first-pass labels, validated against Sonnet on N messages at kappa x; market agents by model; all prose by the author; quotes checked against the recording")

#heading(numbering: none)[Appendix C. Prompts and detector details]
#slot(120, "Seller and buyer prompts as run; the words scorer prompt; the labelling prompt; threshold procedure step by step")

#heading(numbering: none)[Appendix D. Extended results]
#slot(80, "Per-model and per-condition tables; the evasion probe (sellers told they are watched); private reasoning against public message counts; the run log summary with costs from the ledger")
