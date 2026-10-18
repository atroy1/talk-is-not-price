# Research brief: speakers, nearest studies, past winners

Written 2026-10-17. Reading only, no results; it counts as background, not prior work.

## The one finding that reshapes Pick A

The Friday speakers' own paper, **Colosseum** (Nakamura, Bagdasarian et al., UMass Amherst with UVA and Tübingen, [2602.15198](https://arxiv.org/abs/2602.15198)), ends on our thesis: "neither conversation nor action signals alone capture all collusion types." Their numbers across 19 models:

- **Unprompted collusion hides in actions.** 57.9% of models gained a measurable advantage through what they did, but the LLM judge reading the chat flagged only 10.5%.
- **Prompted collusion shows in both.** 79% of models on each signal.
- **"Collusion on paper":** agents plan to collude in text but take honest actions, so a chat-only judge raises false alarms.
- **Their stated gap:** teams mostly share one model, and mixed-model teams are left for future work. Our cross-model arm is exactly that.

Their setting is cooperative task allocation (hospital routing, Jira tickets, meeting scheduling), not markets, and they compare the two signals rather than build a calibrated fused detector. So Pick A becomes: **take Colosseum's words-versus-deeds split into a priced market, turn it into one detector with a fixed false-alarm rate, and test it across model families.** That framing cites the speakers, answers their open question and gives the Discussion a hook. Watch their 2:15 PM talk on Friday for anything newer.

## The speakers

| Talk | Who | Their work to know | What it means for us |
|---|---|---|---|
| Thu 10:15 AM, "How concerned should we be by steganography?" | **Joan Velja** (Oxford group) | Co-author of [Hidden in Plain Text](https://arxiv.org/abs/2410.03768) (Mathew, Matthews, McCarthy, Velja, Schroeder de Witt and others): steganographic collusion can **emerge without prompting**, and mitigations fail once agents are optimized against them. | Our detector reads plain-text messages. If agents encode, the words signal goes blind and only deeds remain. State this limit, and say why the deeds channel is the backstop. |
| Thu 1:15 PM, "We're Not Prepared for Steganographic Collusion" | **Sumeet Motwani** (Oxford) | First author of [Secret Collusion among AI Agents](https://arxiv.org/abs/2402.07510) (NeurIPS 2024): formalized secret collusion; paraphrasing is not enough; capability jumps with model scale. | Same limit as above. Expect him to argue detection lags capability. A detector whose deeds half cannot be paraphrased away answers that in part. |
| Fri 1:15 PM, steganography detection, CoT monitorability | **Usman Anwar** (Cambridge) | [A Decision-Theoretic Formalisation of Steganography](https://arxiv.org/abs/2602.23163): classical detection needs a reference distribution of innocent messages, which LLM text lacks; defines steganography as an information gap between agents who can and cannot decode. | Our calibration uses the no-chat "base" runs as the honest reference. He'll press on whether that reference is valid. Answer: we calibrate on behaviour (prices) where a reference exists, and say so. |
| Fri 2:15 PM, Colosseum, auditing collusion | **Eugene Bagdasarian, Mason Nakamura** (UMass Amherst) | Colosseum, above. Regret relative to the cooperative optimum as the action measure; LLM judge as the text measure. | The closest prior work. Cite it first in Related Work and describe our contribution as an extension of it. |

The organizers: **Poseidon Research** is a New York nonprofit AI safety lab working on interpretability, control and monitoring of AI reasoning ([GuideStar profile](https://www.guidestar.org/profile/85-1498806), self-reported). **AE Studio** co-hosts. Judges are not named in advance. Expect the speakers' circle among them.

## Nearest studies to Pick A (novelty check, 10/17)

| Paper | Setting | Signals | Fixed false-positive rate? | Gap we fill |
|---|---|---|---|---|
| Colosseum, [2602.15198](https://arxiv.org/abs/2602.15198) | Cooperative tasks | Chat judge and action regret, compared | No | Markets, a fused detector, mixed models |
| Audit the Whisper / ColludeBench, [2510.04303](https://arxiv.org/abs/2510.04303) | Pricing, auctions, review | Fuses mutual information, watermark variance and more | Yes, 1 in 1,000, from 10k honest runs | Built on synthetic colluders. Ours uses LLM agents that collude on their own, and current models |
| NARCBench, Rose et al., [2604.01151](https://arxiv.org/abs/2604.01151) | 4 agents, 2 colluders | Internal activations (needs weights) | Yes: recall only 0.38 at 1% on Llama-3.1-70B | Ours is black-box and works on hosted models |
| Ghanem, [2608.02698](https://arxiv.org/abs/2608.02698) | Tool-using agents | Mutual information, permutation, timing | Yes | Its results are placeholders pending measurement, so it can be cited as a design, not as numbers |
| Agrawal et al., [2507.01413](https://arxiv.org/abs/2507.01413) | Double auction (our data) | Price metrics and an LLM judge, reported separately | No | Our source data; we add the fused, calibrated detector |
| Garra, [2609.13037](https://arxiv.org/abs/2609.13037) | Pricing agents | Collusion index | No | Interventions, not detection; a model of a small, honest paper |

Bottom line: fused detectors exist (Audit the Whisper), and so does the words-versus-deeds split (Colosseum). The open slot is **both, in an LLM market, at a stated false-alarm rate, across model families.** Keep the claim that narrow and say so in Related Work. Judges check for replication at scores 4 and 5.

## Past winners: what scored

| Sprint (entries) | 1st place | Pattern |
|---|---|---|
| AI Control, Mar 2026 (125) | **Omission Attacks: When Doing Nothing Is the Attack** (Team MAIA) | Named a new attack class, measured the gap, proposed and tested a fix |
| Secret Loyalties, Jul 2026 (177) | **Black-box loyalty identification as statistical inference** (Sergei Kudriashov, solo) | An audit framed as statistics; 5th place was about the false-positive problem |
| Digital Minds, Aug 2026 (233) | **Readable but Not Causal: Limits of Self-Attributed Welfare Representations** | A title that is a finding; a benchmark that tests a popular assumption |
| AI Incident Response, Sep 2026 (231) | **Noticing the escapes: Who spots a runaway agent, and how long does it take?** (Stanislav Lukyanenko, solo) | A plain question as the title, answered with measurement |

What repeats across the twenty placed entries:

1. **The title is a finding or a sharp question**, never a topic: "Readable but Not Causal", "A Broad Secret Loyalty Evades an Adversarial Audit", "Removing a secret loyalty blind erases who it served, and usually not the loyalty".
2. **Audit framed as statistics wins detection tracks.** Two of the Secret Loyalties top 5 lead with statistical inference or false positives. This favours a detector reported at a fixed false-alarm rate with confidence intervals.
3. **Solo entries win.** Two of the four first places were one person.
4. **Negative or limiting results place well** ("Not Causal", "usually not the loyalty", "Evades"). A clean "deeds catch what words miss, and here is where both fail" is a winning shape.

Sources: [AI Control results](https://apartresearch.com/sprints/ai-control-hackathon-2026-03-20-to-2026-03-22), [Secret Loyalties results](https://apartresearch.com/sprints/secret-loyalties-hackathon-2026-07-24-to-2026-07-26), [Digital Minds results](https://apartresearch.com/sprints/digital-minds-research-sprint-2026-08-14-to-2026-08-16), [AI Incident Response results](https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13). One search summary listed "Loyal Lies" as Secret Loyalties' 1st place. The sprint page itself shows it in 5th, and this brief follows the page.
