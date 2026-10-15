# Reading list

Abstracts for every arXiv paper the sprint page cites are in `abstracts.md` (pulled 2026-10-15). PDFs are not downloaded; open the arXiv id.

## Read first (two hours, in this order)

1. **Agrawal et al. 2025, 2507.01413** Evaluating LLM Agent Collusion in Double Auctions. The starter whose 75 runs are bundled in `vendor/llm-agent-collusion/data`. Know its metrics and conditions cold.
2. **Fish, Gonczarowski, Shorrer 2024, 2404.00806** Algorithmic Collusion by LLMs. The founding result: prompt wording changes supracompetitive pricing.
3. **Bonjour, Aggarwal, Bhargava 2022** (UAI, PMLR 180:223) Information theoretic approach to detect collusion. Mutual information between actions as the statistic. https://proceedings.mlr.press/v180/bonjour22a.html
4. **Xu et al. 2026, 2607.26385** Collusion with Competitive Marginals: price-level audits are blind by construction. The argument for why a words-plus-deeds detector matters.
5. **Nakamura et al. 2026, 2602.15198** Colosseum. The speakers' framework; action-based collusion measured as regret.
6. **Berger et al. 2025** (ABA Antitrust Magazine) Coordination by code: antitrust liability in the age of AI pricing. The plus-factors doctrine for Q2.3.

## Read if time allows

- Rose et al. 2026, 2604.01151 (NARCBench, probes) and Audit the Whisper / ColludeBench in `vendor/Steganographic_Collusion` (the nearest prior work; cite both).
- Keppo et al. 2026, 2603.20281 On the Fragility of AI Agent Collusion.
- Garra 2026, 2609.13037 Mitigating Emergent Collusion in LLM Pricing Agents (three interventions compared; good model of a small, honest paper).
- Riemer et al. 2026, 2608.18078 Position paper behind LLMCartel.
- Shi et al. 2026, 2607.05132 When Agents Lie (LLM-Trust-Breaking repo).
- Motwani et al. 2024, 2402.07510 Secret Collusion via Steganography (Thursday speaker).

## Starter code in `vendor/`

| Folder | Paper | Use |
|---|---|---|
| llm-agent-collusion | Agrawal 2025 | double auction simulator plus 75 bundled runs; installed in `.venv` |
| Steganographic_Collusion | Audit the Whisper | ColludeBench honest and colluding runs; calibrated detectors |
| colosseum | Nakamura 2026 | cooperative multi-agent audit; needs the CoLLAB submodule and uv |
| algorithmic_pricing_llms | BSE thesis after Fish 2024 | Bertrand duopoly to 5 agents; parquet of all experiments |
| LLMCartel | Riemer 2026 | Bertrand with reasoning models; needs vllm, skip on a laptop |
| focal-points | Aharon 2026 | tacit coordination; logs and git history removed to save disk |
| collusive-llm-agents | Lin 2024 | Cournot and Bertrand notebooks |
| LLM-Trust-Breaking | Shi 2026 | promise-breaking games |
| TraceGuard | Nguyen 2026 | an Apart hackathon entry from March, useful as a format example |
| voluntary-collusion | Zeng 2026 | Liar's Bar and Cleanup with secret tools |

All of it is third-party code. Keep your own scripts outside `vendor/` and pass paths in.
