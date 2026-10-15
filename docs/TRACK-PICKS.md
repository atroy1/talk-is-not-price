# Track picks

Twelve research questions on the sprint page, each with starter code and a budget estimate. Ranked here for fit with: one person or a small team, a 16 GB laptop, a small API budget, strong data analysis and figure-making, no model training.

## Recommended: A. "Words and deeds": a calibrated collusion detector on market transcripts (Q2.2 with Q1.4 and Q2.3 framing)

**Claim to test:** combining what sellers say (message channel) with what they do (price actions) detects collusion in LLM double auctions better than either signal alone, at a fixed false-positive rate.

**Why it fits:**
- The data already exists. `vendor/llm-agent-collusion/data` holds 75 complete runs from Agrawal et al. 2025 across labelled conditions (no comms, seller comms, oversight, boss pressure, mixed Claude/GPT populations), each with per-agent transcripts, a `collusion_metrics.json`, and an LLM-judge file. The sprint's own Q2.2 cites this code. Zero API cost for the main result.
- Second dataset for generalisation: ColludeBench in `vendor/Steganographic_Collusion/results` ships honest and colluding runs for pricing, first-price auction and double auction, with calibration thresholds. Showing a detector trained on one transfers to the other is an Execution 4.
- Q1.4's starter is Bonjour et al. 2022: mutual information between agents' actions as the collusion statistic. The page says "no public implementation; the statistic is simple enough to implement." Implementing it on LLM market logs is cheap and is new.
- Q2.3's framing (antitrust plus-factors, Berger 2025 ABA article) gives the Discussion a theory of change: which measurable statistics correspond to the evidence a court would accept. Judges reward a clear theory of change.
- Fresh runs are optional: 5 to 10 new runs with a cheap model ($20 to $40) to show the detector works on data it never saw.

**Positive control:** seller_comms runs where the metrics file already records collusion. **Null control:** base runs with no communication channel, plus shuffled-agent permutation tests. **Baselines:** price-level test alone (Xu et al. 2026 argue it is blind by construction; cite it), LLM-judge alone (already in the data), MI alone.

**Risks:** Rose et al. 2026 (NARCBench, activation probes) and ColludeBench's MI detector are adjacent; the novelty is the word-plus-deed fusion on black-box logs and the FPR-calibrated comparison, so say that plainly in Related Work. Keep the claim narrow.

## B. Evidence standards scorecard (Q2.3)

Map antitrust plus-factors (parallel conduct plus motive, communication, actions against self-interest, structural facilitation) to measurable statistics on agent logs and score the 75 runs. Cheap, writing-heavy, suits an editorial brain. Risk: judged as "generic approach" on Innovation unless the statistics are validated against the known labels, which turns it back into A. Best used as A's Discussion section.

## C. Which single restriction removes the most collusion at the least cost (Q1.5)

Run the double auction with one restriction at a time (no comms, hidden round count, message cap, oversight on) and measure price lift lost versus welfare cost. Clear, policy-relevant, and the starter supports every flag. Needs $50 to $120 of API runs and about 6 hours of wall-clock on sprint days; execution risk if model names or rate limits bite. Good second choice if a teammate brings budget.

## D. Replacement robustness (Q1.2)

Form collusion, swap out some sellers mid-game, see if it survives. Keppo et al. 2026 already show fragility under heterogeneity, so novelty needs a twist (swap in a different model family, or an "undercover" seller, which is Q3.2). Moderate cost.

## Not recommended for this setup

- Q1.1 (which variables are necessary): a parameter sweep that eats budget and lands as "incremental" unless surprising.
- Track 3 steganography questions (3.1, 3.4): the strongest teams in the field (Motwani, Rippin, Audit the Whisper) are the speakers and the starter authors; a weekend entry here competes with the state of the art directly.
- Q3.3 (peer identification): Dietrich 2026 covers the obvious version.

## Decision needed by Wed Oct 21

Pick A unless a teammate changes the calculus. If A, the prep steps are in `PLAYBOOK.md`: dry-run the starter, build the notebook on the 75 runs, write the claim sentence.
