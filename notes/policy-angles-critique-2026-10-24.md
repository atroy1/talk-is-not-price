# Adversarial critique of the two policy angles (Oct 24)

Figures checked against `notes/results-frozen.md`; "report only" means found only in the report draft.

## Angle 1. What an agent log proves

### 1. Strongest objections

1. "The harm evidence is absent from the same log." Opponent: your own report says the median cartel cost buyers
   about $221 more than the honest no-chat median (+$36 against -$185, frozen table 5), and Haiku with chat sits at
   -$8 against -$126 and -$166 for honest Haiku. Part B, your own honest-median baseline, finds the harm that fact 2 denies.
2. "The invitation is accepted by conforming: in 94% of 3,377 proposals..." Opponent: every market opens near $97
   and asks are sticky; next-round asks at or above a named price are what inertia produces. Without the same measure on no-chat markets, 94% in five-seller toy
   markets proves nothing.
3. "Honest markets reproduce the price pattern without the communications." Opponent: one market in ten did (base-4);
   only 1 of 10 honest 2025 markets was above zero. A bar set by the single worst of 10 honest markets says the
   screen has n = 10, not that honest agents price like cartels.

### 2. Legal and institutional errors

1. Wrong: calling the messages a "plus factor". An exchange proposing and agreeing to a common price is direct
   evidence of agreement; plus factors are the circumstantial route when that is missing (Flat Glass, 3d Cir. 2004,
   ranks such evidence above the economic factors). Part A answers a question the log already answers.
2. Missing: per se illegality. Price fixing, floors at cost and horizontal maximum prices included (Socony-Vacuum
   1940; Maricopa 1982), needs no proof of effect. Harm goes to damages and sentencing, not liability; Luna's downward
   coordination is still price fixing. Fact 2 implies the opposite.
3. Missing: attribution and intent. The first defence is that no human at either firm agreed. The deployer's prompt
   is "not evidence of what the agents did", but it is central evidence of the principal's intent, which criminal
   liability requires (Gypsum 1978).
4. Overstated: Interstate Circuit. Acceptance by conformity needs knowledge that rivals were invited and conduct that
   pays only if they comply. "Asks at or above" drops the against-interest element.
5. Wrong: Twombly is a pleading case; the evidentiary bar is Matsushita and Monsanto.
6. Missing: live US cases are hub-and-spoke through a shared vendor (RealPage; Duffy v. Yardi; to verify), not
   seller-to-seller chat. Internal audit does not "already hold the honest baseline": a firm cannot run its rivals'
   agents.

### 3. Numbers

- 94% of 3,377 and 96% of 2,653: not in the frozen file.
- $96.5 held: report only. +$149 a market: nowhere.
- Qwen "fixed a floor at their own cost": report only; the frozen file shows negative overcharge, nothing more.
- "A tenth of a cent per message": $0.30 / 22,505 is about 0.0013 cents, off by roughly 75 times. The $0.30 is not in
  the frozen file; 22,505 is report only.
- "A keyword rule finds the same markets": it misses 1 of 8 Qwen markets and flags 1 of 9 (+$6) and 1 of 6
  (Sonnet and Opus) honest markets (table 8).

### 4. What would make it survive

Cut fact 2 and the "harm is absent" framing. Replace it with the $221 median gap and the point that harm goes to
damages, not liability.

Add one paragraph recasting Part A as direct evidence and Part B as a yardstick damages benchmark. Give the acceptance
measure an honest no-chat rate, and name attribution to the principals as the open question.

## Angle 2. Certify the monitor

### 1. Strongest objections

1. "The honest traffic does not exist: every LLM seller family we tested coordinates when it can talk." Opponent: the
   design hands rivals a chat room and a profit goal, not nature. Opus under "set your ask
   independently" could talk and sent nothing (table 2: 0 chat flags), so the claim fails for one family even here.
2. "The certified false-alarm rate is k/(n+1) on that set and nothing more." Opponent: then it is worth little. At n = 20 the floor is 4.8% per market: about 48 false alarms per 1,000 markets at the bound. It holds only if
   deployed traffic is exchangeable with traffic made under a sanitising "it is illegal" instruction. At a chat
   threshold of 0.0, it says only that the labeller flagged no message in bland traffic, which any vendor can arrange.
3. "Silence is not compliance and must be reported as the monitor's blind spot." Opponent (the litigator): agents that
   do not talk to rivals are the compliant outcome; tacit parallel pricing is lawful. The silent Opus market at $95.28
   is matched by honest no-chat markets.

### 2. Legal and institutional errors

1. Wrong: the AI Act line. Logging (Art. 12) and human oversight (Art. 14) bind high-risk systems. Annex III reaches
   credit scoring and life and health insurance pricing, not retail pricing agents.
2. Missing: a home and an enforcer. Nobody certifies monitors. Plausible homes: DOJ Antitrust Division
   compliance-programme evaluation, procurement terms, marketplace rules. The likeliest enforcer
   is FTC substantiation doctrine against vendors selling accuracy claims they cannot support (to verify against
   Operation AI Comply, 2024).
3. Overstated: requirement 4 as a "miss rate". The pair split 48 of 50 against 1 of 42 messages, but the zero-threshold
   monitor still fired on that one message (report 4.4).

### 3. Numbers

- "7 of 7 families": not in the frozen file; Opus under the neutral instruction is a counterexample.
- "8 of 12 markets sent nothing", attributed to the illegal sentence: only 4 of the 8 were under it (table 11).
- "First alarm in round 1": Luna's is round 2 (table 1).
- Gag by round 7, $88, $96.5, "held in half": report only. "Half" is the design split (CEO pressure in 10 of 20),
  not an outcome rate.
- One-in-twenty sampling, round 4, 55%: not in the frozen file.
- $0.30 a market, $56, $26: not in the frozen file.

### 4. What would make it survive

Cut the AI Act and "regulator" framing, and the general claim that honest traffic does not exist.

Add a recast: a disclosure and substantiation standard for anyone selling a monitor's accuracy. It should state n,
the instruction, the exchangeability assumption and the resolution floor k/(n+1), with the FTC as enforcer.

## 5. Verdict

- Angle 1: keep with the stated edits; as written, fact 2 contradicts the report and the legal frame is mislabelled.
- Angle 2: keep with the stated edits; closest to the paper's first result, but "certify" should become "substantiate".
