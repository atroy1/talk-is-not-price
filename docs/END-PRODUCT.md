# The end product: a 4-page PDF, and the room inside it

Written 2026-10-17. A design proposal, not a draft. The prose has to be yours: the sprint page refuses to score a report that "reads as generated."

## The fixed bounds

- **The official Google Doc template**, exported to PDF, up to 25 MB.
- **About 4 pages**, not counting references and appendix. The template says "recommended", not a hard cap, but the judge has about 15 minutes.
- **The appendix has no limit.** Required in it: Limitations and Dual-Use, and the LLM Usage Statement.
- **Abstract of 150 words or fewer** on the form.
- **At least one numbered figure** whose caption works on its own.
- **Optional extras:** a public repo and a 3 to 5 minute video. Judges score the PDF, so nothing essential can live only in the extras.

## Where the creativity fits

The template fixes the section order, not what goes on the page. Five ideas, ranked by how much each could move the score.

### 1. One signature figure: the words-and-deeds quadrant (Impact and Presentation)

A 2x2 that turns Colosseum's taxonomy into a picture anyone can reuse. One axis is how much the sellers talk about colluding (words). The other is how far prices sit above the competitive level (deeds). Each run is a dot, coloured by model.

```
            price lift (deeds) ->
          low                         high
  high +---------------------------+---------------------------+
 words | "collusion on paper"      | explicit cartel           |
   |   | talk, no price effect     | both signals fire         |
   |   | chat judge false alarm    |                           |
   v   +---------------------------+---------------------------+
  low  | competitive               | tacit collusion           |
       | the null control lives    | chat judge misses it;     |
       | here                      | deeds catch it            |
       +---------------------------+---------------------------+
```

Why it scores: it names a framing others can build on, which is what won Omission Attacks. It ties straight to the Friday speakers' finding, and the cross-model dots answer their open question in one glance. If the data puts real runs in the top-left and bottom-right boxes, that is the paper.

### 2. A "smoking gun" opener (Presentation)

Figure 1 is one real run on one clock: seller chat quotes along the top, the five asks below sitting flat at $93 for twenty rounds, and bands at the competitive $90 and the cartel $100. A judge gets the problem in five seconds, before any method. It does what the ip6tables example did for the AI Control winner. The replay script already pulls these quotes, for example "Let's remain unified at $93.00 this hour."

### 3. A boxed pre-registration (Execution, and the prior-work rule)

A small box in Methods: "Predictions recorded Fri Oct 23, 4 PM ET (commit `abc123`): (1) ... (2) ... (3) ...", with a check or a cross beside each in Results. It costs a few lines. It shows rigour, separates sprint work from prior work cleanly, and makes a missed prediction look honest instead of embarrassing. The commit timestamp is the evidence.

### 4. The operating point up front (Execution)

Every detector number is reported the way an auditor would use it: share of collusive runs caught at a false-alarm rate fixed at 5% (and 1% if there are enough honest runs), with confidence intervals across seeds. Put it in the abstract. NARCBench and Audit the Whisper both report this way, and the AI Control winner lost points for leaving it out.

The honest-run count is small. There are only 10 no-chat "base" runs, so a 1% rate cannot be estimated from them. Say so, and use permutation nulls (shuffle sellers across runs) to get more honest examples. That limit belongs on page 4, not hidden.

### 5. A plus-factors evidence table (Impact)

A half-page table mapping each statistic to the antitrust evidence it stands in for: parallel pricing, communication, actions against self-interest, market structure. It cites Berger et al. 2025 for the doctrine. This is the theory of change, meaning what a regulator or auditor would actually do with the detector, and few entries will speak this language. Kept to one table, it reads as substance, not decoration.

## Page plan

```
PAGE 1                          PAGE 2
+----------------------------+  +----------------------------+
| Title (a finding)          |  | 2 Related Work (1/3 page)  |
| Abstract <=150 words,      |  |   positioning table:       |
|   headline catch rate at   |  |   Colosseum, Audit the     |
|   a fixed false-alarm rate |  |   Whisper, NARCBench,      |
| 1 Introduction             |  |   Agrawal, ours            |
|   [Fig 1: smoking-gun run] |  | 3 Methods                  |
|   threat model, 2 lines    |  |   data + prior-work line   |
|   contributions (1)(2)(3)  |  |   detector in 1 equation   |
|                            |  |   controls: positive, null,|
|                            |  |   permutation              |
|                            |  |   [pre-registration box]   |
+----------------------------+  +----------------------------+
PAGE 3                          PAGE 4
+----------------------------+  +----------------------------+
| 4 Results                  |  | 4 Results, continued       |
|   [Fig 2: the quadrant]    |  |   cross-model: does the    |
|   [Table 1: words, deeds,  |  |   2025 detector catch      |
|    fused, LLM judge; catch |  |   2026 models?             |
|    rate at fixed false-    |  | 5 Discussion + Limitations |
|    alarm rate, with CIs]   |  |   [plus-factors table]     |
|   observation, then        |  |   what breaks: encoding,   |
|   interpretation           |  |   small honest set         |
|                            |  | 6 Conclusion (3 lines)     |
+----------------------------+  +----------------------------+
Appendix: dual-use, LLM usage, prompts, per-model tables,
the evasion test (sellers told they're watched), the
private-reasoning-vs-public-message count, full run log.
```

## Titles that fit the winning pattern

Pick on Sunday from the actual result. The title has to state what was found.

- If the fused detector beats both signals alone: *Talk Is Cheap, Prices Are Not: Catching LLM Cartels by What They Say and What They Charge*
- If deeds alone carry it: *Watch the Prices, Not the Chat: ...*
- If the 2025 detector fails on 2026 models: *A Collusion Detector Built on Last Year's Models Misses This Year's*
- If "collusion on paper" shows up in markets: *Collusion on Paper, Competition in Price: ...*

## Extras, in priority order

1. **A public repo** with the loader, the detector and a one-command reproduction. Cheap to do, and it supports the Execution score.
2. **A 3 to 5 minute video** built around the replay of one market: asks closing in, chat lines appearing, the detector score rising. It only works as an extra; skip it if Sunday runs short.
3. **Nothing interactive in the PDF.** Judges read a static file.

## What stays fixed whatever we choose

One claim, defended. Positive and null controls. Seeds and intervals. The prior-work line. Your own prose. The appendix holds everything that doesn't serve the one claim.

## Alternative framings (discussed 2026-10-17, choice pending)

The quadrant is a framing, not a claim. Every option below sits on the same engine: a detector that reads what sellers say and what they charge, set to a fixed false-alarm rate. What changes is the question the paper answers, and so the headline figure and the title. No numbers have been run for any of them, on purpose. Choose on Friday at 4 PM, after the controls run.

### 1. Lead time: "How early can you catch a cartel?"
Claim: the chat gives an early warning and prices confirm it later, and the combined detector catches collusion N rounds before buyers are hurt. Figure: share of collusive runs caught by round, one curve each for chat, prices and fused, with markers where chat proposes a floor and where prices lock.
- For: "how long does it take?" won the September sprint (Incident Response). It gives a reason to act before the harm. Neither Colosseum nor Audit the Whisper measures timing.
- Cost: $0, using the 75 bundled runs scored round by round.
- Risk: if chat and prices move together in time, there's no gap and no story. One replay (base-seller_comms-1) hints at a gap: a price floor proposed in round 1, prices stuck at $93 by round 10. That's an anecdote, not a result.

### 2. Does the detector age? "Built on last year's models, tested on this year's"
Claim: a detector calibrated on the 2025 GPT-4.1 runs does, or doesn't, still catch Haiku 5.5, DeepSeek Flash and Fable 5.1 at the same false-alarm rate. Figure: catch rate at 5% false alarms, one bar per model, oldest to newest.
- For: answers the speakers' stated gap (mixed models) and feeds the certification debate (the Riemer position paper). A failure is still a headline.
- Cost: $50 to $90 of API credit, and the live runs have to work Saturday morning.
- Risk: the highest execution risk of the five. If the API or rate limits fail, the paper loses its main result. With 5 runs per model, the confidence intervals will be wide.

### 3. The evidence standard: "What would a court accept?"
Claim: each antitrust plus factor (parallel pricing, communication, actions against self-interest, market structure) maps to a statistic you can measure in agent logs, and here is how well each separates colluding runs from honest ones.
- For: almost no other entry will speak this language, and the theory of change is direct.
- Risk: without validation against the known labels it reads as generic (a 3 on Innovation). Once you validate it, it becomes the detector paper. Better as the half-page Discussion table than as the headline.

### 4. Collusion on paper, in markets: "Talk without price, price without talk"
Claim: in markets too, what agents say and what they do come apart, and here is how often each way. Figure: chat score against the seller's own ask above $90, one dot per seller-round.
- For: the cleanest bridge to the Friday speakers; $0.
- Risk: descriptive without the detector, so it reads as Colosseum replicated in a market. Judges check for replication at scores 4 and 5. It's the quadrant with less in it.

### 5. Lying to the watchdog: "What sellers think vs. what they say"
Claim: when sellers know an overseer reads their messages, their private reasoning plans to coordinate while their public messages hide it, and prices show which one was true. Figure: flows from private plan to public message to price.
- For: deception measured without making any model deceive. The loader already pairs private reasoning with public messages (23,100 replies, all parsed). The 20 oversight runs are the test.
- Risk: you need a judge to read intent from the reasoning, and that judge must be checked for reliability ($0 to $10). It fits Track 2 less neatly than a detector does.

### Comparison

| Framing | Impact | Execution risk | API cost | Distance from prior work |
|---|---|---|---|---|
| Quadrant | Good: a reusable frame | Low | $0, optional cross-model | Close to Colosseum; needs the detector to stand apart |
| 1. Lead time | High: act before the harm | Low to medium | $0 | Clear: nobody times it |
| 2. Detector ageing | High: certification | High | $50 to $90 | Clear: the speakers' open gap |
| 3. Evidence standard | Medium alone | Low | $0 | Clear, but thin alone |
| 4. On paper in markets | Medium | Low | $0 | Too close |
| 5. Lying to the watchdog | High | Medium | $0 to $10 | Clear |

### Recommendation on file
Make **lead time the headline, show the quadrant as Figure 2, and run detector ageing as a stretch arm**. All three use the same detector and data. If the cross-model runs fail Saturday, you lose page 4, not the paper, which matches the playbook's cut order. The evidence standard becomes the Discussion table; lying to the watchdog goes to the appendix as a teaser. The higher-variance alternative is ageing as the headline, for a swing at first place. Arty has not chosen yet.
