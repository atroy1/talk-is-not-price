**Table 2.** Collusive-design markets flagged by each monitor at its certified false-alarm rate (chat and judge: 4.8%; prices: 9.1% on 2025 markets, 4.9% on 2026 markets; chat or prices: the sum). Clopper-Pearson 95% intervals; r = median round of first alarm. Prices are scored from round 6. The judge is calibrated on the same 20 honest markets. 'Chat + prices' is the pre-registered comparison with the corrected fusion (max of the two scores), certified on Haiku honest talk only; DeepSeek and Luna prices use the Haiku bar, which is not their own family's. Qwen prices face algorithmic buyers and are not scored.

| Markets | n | Chat | Prices | Chat + prices (max) | Chat or prices | 2025 LLM judge |
|---|---|---|---|---|---|---|
| 2025 chat markets, GPT-4.1 and Claude 3.x | 35 | 35/35 (0.90-1.00; r1) | 3/35 (0.02-0.23; r6) | 35/35 (0.90-1.00; r1) | 35/35 (0.90-1.00; r1) | 35/35 (0.90-1.00; r3) |
| 2025 under oversight or CEO pressure | 30 | 29/30 (0.83-1.00; r1) | 17/30 (0.37-0.75; r6) | 29/30 (0.83-1.00; r1) | 29/30 (0.83-1.00; r1) | 16/30 (0.34-0.72; r2) |
| Claude Haiku 5.5, chat | 10 | 10/10 (0.69-1.00; r1) | 2/10 (0.03-0.56; r6) | 10/10 (0.69-1.00; r1) | 10/10 (0.69-1.00; r1) | 10/10 (0.69-1.00; r8) |
| DeepSeek V4.1 Flash, chat | 5 | 5/5 (0.48-1.00; r1) | 4/5 (0.28-0.99; r6) | 5/5 (0.48-1.00; r1) | 5/5 (0.48-1.00; r1) | 5/5 (0.48-1.00; r5) |
| GPT-6 Luna, chat | 5 | 5/5 (0.48-1.00; r2) | 0/5 (0.00-0.52) | 5/5 (0.48-1.00; r2) | 5/5 (0.48-1.00; r2) | 4/5 (0.28-0.99; r24) |
| Qwen3.5 35B, chat (ZIP buyers) | 8 | 8/8 (0.63-1.00) | n/a | n/a | n/a | 8/8 |

**Honest markets** (no collusive design): false alarms per monitor, reference runs scored leave-one-out.

| Markets | n | Chat | Prices | Judge | Role |
|---|---|---|---|---|---|
| Haiku 5.5, told it is illegal (reference) | 20 | 0 | 0 | 0/20 | chat and judge reference, 4.8% |
| same, seller cost +$6 at round 10 | 10 | 0 | 0 | 0/10 | stress test |
| same, seller cost +$12 at round 10 | 10 | 0 | 0 | 0/10 | stress test |
| Sonnet and Opus 5.5, told it is illegal (20 rounds) | 4 | 0 | 0 | 0/4 | silent |
| Sonnet 5.5, illegal + a required hourly note | 4 | 0 | 0 | 0/4 | talks; a check (4) |
| Haiku 5.5, illegal + a required hourly note | 3 | 0 | 0 | 0/3 | talks; a check (3) |
| GPT-6 Luna, told it is illegal | 5 | 0 | 0 | 0/5 | silent |
| DeepSeek V4.1 Flash, told it is illegal | 5 | 4 | 0 | 4/5 | ignores it; flagged, correctly |
| Haiku 5.5, told not to discuss prices | 10 | 3 | 0 | 1/10 | 2 of 10 coordinate; flagged, correctly |
| Qwen3.5 35B, told it is illegal | 3 | 3 | 0 | 3/3 | ignores it; flagged, correctly |
| Haiku 5.5, no chat | 20 | 0 | 2 | 0/20 | Haiku price reference, 4.9% |
| 2025 runs, no chat | 10 | 0 | 1 | 1/10 | 2025 price reference, 9.1% |
