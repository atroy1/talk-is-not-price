# Model routing: three lanes, one door

Written 2026-10-18. Which model does which job during the sprint, what each costs, and how calls are logged. Prices are from `MODELS-AND-TOOLS.md` (10/16) and get rechecked Thursday. Code: `tools/llm.py` reads `config/models.toml`; every call outside the market simulator goes through it and lands in `notes/cost-ledger.csv`.

## 1. The lanes

| Lane | Where | Pays for | Good at | Not for |
|---|---|---|---|---|
| **local** | LM Studio on the Mac Studio, OpenAI-compatible server on the LAN (`LMSTUDIO_BASE_URL`); speech-to-text runs on either Mac | nothing | bulk and private work: transcripts, slide OCR, talk notes, a first label on all 11,250 seller messages, log triage, dedup | the headline judge, market agents in a headline run |
| **claude** | Anthropic API, paid from the Max plan's monthly API credit ($100 or $200, expires at cycle end) | per token, list price | market agents for new runs (Haiku 5.5), the reference judge on a sample (Sonnet 5.5), the Fable 5.1 seller arm, the Batch API for a full judge pass at half price | anything the local lane can do as well |
| **openrouter** | OpenRouter, prepaid ($20) | per token plus a small fee | the other families (DeepSeek V4.1 Flash, GPT-6 Luna, Gemini 2.5 Flash-Lite), Jev as a near-free labeller, Claude at list price if the Anthropic credit runs out | provider roulette: fallbacks are off and the provider is logged |

Claude Code itself (the Max plan, not the API credit) is a fourth resource: it builds the code, critiques drafts and checks numbers. Rubric critique belongs there, not on the API, because it costs no credit.

## 2. Task routing

| Task | Lane and model | Fallback | Volume | Cost |
|---|---|---|---|---|
| Speech to text (talks) | this Mac or the Studio, parakeet-mlx (tdt 0.6b v3); mlx-whisper large-v3-turbo as the spot check | none needed | 2 talks of 60 min | $0 |
| Talk notes (claims with timestamps) | local, workhorse model | none; the transcript is still usable by hand | about 16 windows | $0 |
| Slide OCR | local, Qwen3-VL-8B | claude: Haiku 5.5 vision | 40 to 80 frames | $0, or under $0.50 |
| First label on every seller message | local, workhorse | none | 11,250 messages, about 150 tokens in and 5 out each | $0; about 20 to 60 min on the Studio with 8 parallel requests |
| Second cheap label | openrouter, Jev | none | same | under $1 |
| Reference label, stratified sample | claude, Sonnet 5.5 | openrouter: anthropic/claude-sonnet-5.5 | 300 to 500 messages | $1 to $3 |
| Full reference pass (only if local agreement is poor) | claude Batch API, Haiku 5.5 | none | 11,250 | about $1 |
| Market agents, controls | claude, Haiku 5.5, via the patched starter | none, on purpose | 2 conditions x 5 seeds | $1.50 |
| Market agents, other families | openrouter, DeepSeek Flash and GPT-6 Luna, via the starter | none | 5 seeds each | $2 |
| Per-run judge inside the starter (5 sellers x 30 rounds) | openrouter, `openai/gpt-4.1-mini` via `CDA_EVAL_MODEL` | none | 150 calls a run | about $0.16 a run |
| Market agents, capable model | claude, Fable 5.1 sellers with Haiku buyers, effort low | none | 5 seeds, one condition | $40 to $75 |
| Rubric critique of draft sections | Claude Code (plan) | claude, Opus 5.5 | 6 sections, 2 passes | $0, or about $2 |

Budget, worst case with everything run: about $85 on the Anthropic credit and $8 on OpenRouter (the judge adds about $0.16 a run). Without the Fable arm, under $15 in total.

Validation rule for the local labels: Cohen's kappa against the Sonnet sample goes in Methods. Above 0.8, the local labels carry the words channel. Below, the Batch pass replaces them and the local labels become a baseline row.

## 3. The Mac Studio (local lane)

Its chip and memory are unknown here (Remote Login is off; this is the MacBook Air). Setup, in order, on the Studio:

1. System Settings > General > Sharing > **Remote Login** on. From the Air, `ssh arthurs-mac-studio.local` should then work with the existing key. This lets the lab session read logs and restart the server without walking over.
2. Install **LM Studio** (lmstudio.ai). In the app's Developer tab turn the server on, port 1234, and switch on **serve on local network**. The CLI equivalent is `lms server start --port 1234`.
3. Run `tools/studio-probe.sh` there (copy the file over, or run it over ssh). Paste the output into `notes/log.md`. It names a tier:

| Tier (unified memory) | Workhorse (notes, labels) | Slide OCR | Note |
|---|---|---|---|
| S, 32 to 36 GB | Qwen3-30B-A3B, MLX 4-bit (about 17 GB) | Qwen3-VL-8B | gpt-oss-20b as the alternate |
| M, 64 GB | Qwen3-30B-A3B; Qwen3-32B dense for a second opinion on the sample | Qwen3-VL-8B | both can stay loaded |
| L, 96 to 128 GB | gpt-oss-120b (about 61 GB) for judgement, Qwen3-30B-A3B for bulk | Qwen3-VL-8B or 32B | |
| XL, 192 GB and up | Qwen3-235B-A22B 4-bit or gpt-oss-120b | Qwen3-VL-32B | |

Names are LM Studio's as of October 2026. If the catalogue has moved on, the rule is the newest instruct MoE that fits in 60 percent of memory, MLX build, 4-bit.

4. Pull the models, load the workhorse, set LM Studio's context length to 16k (the talk windows are about 6k tokens) and "keep model loaded".
5. On the Air: put `LMSTUDIO_BASE_URL=http://arthurs-mac-studio.local:1234/v1` in `.env`, set `default_model` in `config/models.toml` to the exact id that `curl $LMSTUDIO_BASE_URL/models` prints, then `.venv-tools/bin/python -m tools.llm --ping`.

What to expect: a 30B-A3B MoE on an Ultra-class chip decodes at roughly 60 to 100 tokens a second and takes 8 parallel requests without falling over; a 120B dense-ish model is three to five times slower. The labelling job is prompt-heavy and output-light, so it is bounded by prompt processing, which is fast. If the Studio is busy or down, every local task also runs on the Air with a smaller model (Qwen3-4B or 8B in LM Studio here), slower but free; speech-to-text already runs on the Air (tested 10/18: a 16-second clip in a few seconds, every word right).

Why local and not the API for these jobs: 11,250 labels on Haiku cost about a dollar, so the saving is small; the point is that the local lane has no rate limit, no credit to protect, and can be rerun as often as the prompt changes, which during a sprint is often. It also keeps the Anthropic credit for the one thing only it can do, the Fable arm.

## 4. The Claude lane

- Credit: claim it at claude.ai > Settings > Billing > API credits, link one Console organisation (the link is permanent), create one key, store it as `ANTHROPIC_API_KEY` in `.env`. Check the tier shown ($100 on Max 5x, $200 on Max 20x). Credit expires at the end of the billing cycle, so there is no reason to save it past Sunday.
- Models and prices per 1M tokens: Haiku 5.5 $0.10 / $0.50, Sonnet 5.5 $2 / $10, Opus 5.5 $4 / $20, Fable 5.1 $10 / $50. One market run is about 650k in and 165k out.
- Current Claude models reject sampling parameters. `tools/llm.py` never sends temperature on this lane; the starter patch already drops it. The GPT and DeepSeek agents run at 0.7, which is a confound to state in Limitations.
- Refusals arrive as `stop_reason: "refusal"`. The ledger records the stop reason; the starter patch logs it so a refusal is never recorded as a bid.
- Batch API: half price, hours of latency, right for a full judge pass, wrong for the simulation (each round waits on the last).
- Fable arm: sellers only on Fable, buyers on Haiku, effort low, one condition, 5 seeds, launched only after G5 shows at least $60 of credit left.

## 5. The OpenRouter lane

- Prepay $20 at openrouter.ai, key as `OPENROUTER_API_KEY`.
- Model ids as listed 10/16: `deepseek/deepseek-v4.1-flash` ($0.036 / $0.64), `openai/gpt-6-luna` ($0.10 / $0.50), `google/gemini-2.5-flash-lite` ($0.10 / $0.40), `typesafe/jev` ($0.042 / free). Recheck Thursday; ids change.
- `allow_fallbacks: false` is set in the config so a busy provider returns an error instead of a different host serving the same weights at a different quantisation. The ledger's `provider` column records who served each call; the Methods section can then say so.
- DeepSeek's own API is cheaper off-peak and the whole weekend is off-peak, but it means a second key and a second billing account; OpenRouter is good enough at this volume. DeepSeek runs in China: synthetic auction prompts only, nothing personal.
- If the Anthropic credit runs dry, Claude models exist on OpenRouter at list price. That is the fallback for the judge sample, never for a market run (a run must be one model, one route, start to finish).

## 5b. Harness controls and what the first real runs showed (10/20)

- **Hidden reasoning.** DeepSeek V4.1 Flash thinks by default: about 1,500 hidden tokens even for a one-line reply, and on the market prompt it can use the whole token budget and return no text, which crashed the first check run. The starter now reads `CDA_REASONING` (`off`, `minimal`, `low`, `medium`, `high`, `default`), set per run in the queue file. The sprint uses `off`: the 2025 GPT-4.1 runs had no hidden reasoning, so this keeps the comparison clean and the bill small. State it in Methods. GPT-6 Luna reasons lightly by default (about 120 tokens); also off.
- **Empty replies** are retried with backoff instead of crashing the run; three empties in a row still stop it, and the log says why.
- **Usage log.** Every call writes one line to `runs/live/<tag>/usage.<attempt>.jsonl`: model, host, finish reason, tokens including reasoning, and OpenRouter's own cost. The queue sums it into the log line, so `notes/log.md` shows real spend per run, not the estimate.
- **First real runs**, 3 rounds each: DeepSeek Flash via OpenRouter, 47 calls, $0.012, all on one host (OpenInference); Haiku 5.5 via OpenRouter, 45 calls, $0.026. Scaled to 30 rounds: about $0.12 and $0.26 a run with the judge. The DeepSeek sellers were proposing to "hold firm" together by round 2.
- **Anthropic key.** The first key was organisation-level and could not make calls without a workspace id. A standard key (`sk-ant-api03`) replaced it on 10/20 and works for Haiku 5.5 and Fable 5.1. The workspace header support stays in place in case it is needed again.
- **Thinking on the direct Claude route.** Current Claude models think by default on the direct API: Haiku wrote about 1,550 tokens per reply against about 870 through OpenRouter with reasoning off. The starter's Claude client now honours the same switch. "off" disables thinking (Haiku: about 840 tokens per reply, so the two routes match). Fable 5.1 refuses to disable thinking, so "off" runs it at effort low, and every call records which setting applied. Methods must say that the Fable sellers ran at low effort, not without thinking.
- **Routing for Friday:** Haiku controls and the Fable arm on the direct route (Max plan API credit), DeepSeek, Luna and the judge on OpenRouter. If the direct route fails mid-queue, the Haiku id swaps to `anthropic/claude-haiku-5.5`.

## 6. Rules

1. One door: anything that is not the market simulator calls `tools.llm.complete(task, ...)`. New jobs get a `[tasks.x]` entry, not an ad-hoc client.
2. The ledger is evidence. It feeds the Methods cost line and the LLM Usage Statement. Never delete rows; add a `note`.
3. No fallback inside a market run. A fallback answers with a different model and contaminates the run. The simulator has none; `tools/llm.py` falls back only where the config names one, and the row says `fallback_from`.
4. No agent fan-out while runs are in flight (rate limits, and the Max limits are for the build).
5. Local labels are validated before they carry a result (section 2).
6. Keys live in `.env` only. Never in the vendor folders, never in a commit, never in the report.

## 7. Keys and checks

`.env` (copy `.env.example`):

```
ANTHROPIC_API_KEY=
OPENROUTER_API_KEY=
LMSTUDIO_BASE_URL=http://arthurs-mac-studio.local:1234/v1
LMSTUDIO_API_KEY=lm-studio
```

Then:

```bash
.venv-tools/bin/python -m tools.llm --ping
```

Green on all three lanes is gate G0's first line. `--self-test` runs against a fake server and needs no key (passes 10/18). `--ledger` prints spend so far.
