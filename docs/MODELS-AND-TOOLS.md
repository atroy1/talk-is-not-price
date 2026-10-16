# Models, API access and efficiency tools

Written 2026-10-16. Prices change often; recheck the official pages on Thu Oct 22.

## 1. Your Claude API access

- **Today:** none wired up. No API key is set in the shell or in any `.env`. Claude Code is logged in through claude.ai on a **Max** plan (org "arty tee").
- **The Max plan includes monthly API credits** (announced Oct 7, 2026): $100 a month on Max 5x, $200 on Max 20x. They cover the Claude API, the Agent SDK, Managed Agents and the Playground. They do not cover Claude Code. They expire at the end of each billing cycle with no rollover, and requests stop when the credit runs out (nothing is charged to the plan).
- **To claim (your step, about 5 minutes):** claude.ai > Settings > Billing > API credits, then link a Console organization at platform.claude.com. The link is permanent (only support can change it), so pick the org you'll build in. Then create an API key and put it in `.env` as `ANTHROPIC_API_KEY`. Check which Max tier you have on the same page.
- **Not recommended:** driving the simulations through `claude -p` on your plan limits. Each run is about 300 calls, and the plan limits are what you need for Claude Code over the weekend.

Sources: [API credits for Max and Team plans](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers), [Help Center article](https://support.claude.com/en/articles/17154008), [Agent SDK with your plan](https://support.claude.com/en/articles/15036540).

## 2. What one market run costs

Measured on `base-seller_comms-1` (10 agents, 30 rounds): about **650k input tokens and 165k visible output tokens per run**. Models that think bill extra output on top of that, so treat the column as a floor.

| Model | Input / output per 1M | One run (list price) | Source |
|---|---|---|---|
| Gemini 2.5 Flash-Lite | $0.10 / $0.40 | about $0.13 | tracker only, may not be open to new projects |
| Claude Haiku 5.5 | $0.10 / $0.50 | about $0.15 | Anthropic (official) |
| GPT-6 Luna | $0.10 / $0.50 | about $0.15 | OpenRouter listing (`openai/gpt-6-luna`), 10/16 |
| DeepSeek Flash (V4.1), off-peak | $0.15 / $0.60 | about $0.20 | DeepSeek (official) |
| DeepSeek Flash, peak | $0.30 / $1.20 | about $0.39 | DeepSeek (official) |
| DeepSeek Flash via OpenRouter | $0.036 / $0.64 | about $0.13 | OpenRouter listing (`deepseek/deepseek-v4.1-flash`), 10/16 |
| Claude Sonnet 5.5 | $2 / $10 | about $2.95 | Anthropic |
| Claude Opus 5.5 | $4 / $20 | about $5.90 | Anthropic |
| Claude Fable 5.1 | $10 / $50 | about $14.70, more with thinking | Anthropic |

- **DeepSeek peak hours** are 01:00-04:00 and 06:00-10:00 UTC on weekdays (9 PM-midnight and 2-6 AM Eastern). The whole sprint weekend is off-peak. Cache hits are nearly free ($0.003 per 1M off-peak), and the market prompt repeats its rules every call.
- **Fable 5.1 is about 100 times the price of Haiku 5.5 or DeepSeek Flash.** A 15-run design (3 conditions x 5 seeds) costs about $2 to $6 on the cheap models and $220 or more on Fable, which is past a $100 to $200 credit. To make Fable affordable: only the 5 sellers run on Fable while the buyers run on Haiku (about half the cost, and the original data already mixes models), effort set to `low`, and 5 runs on one condition (seller messaging on). That's roughly $40 to $75.
- **Batch API (50% off)** doesn't fit the simulation, because each round waits on the last one. Use it for the scoring pass (judging 11,000 seller messages), not the markets.

Sources: [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing), [benchlm price table](https://benchlm.ai/llm-pricing), [VentureBeat on GPT-6 Luna](https://venturebeat.com/technology/openai-releases-gpt-6-sol-and-luna-models-slashing-api-costs-50-or-more), [Gemini pricing roundup](https://www.morphllm.com/gemini-api-pricing).

## 3. Starter code fixes before any new run

Done 10/16: items 1 to 4 are patched in `vendor/llm-agent-collusion` and saved as `patches/llm-agent-collusion.patch` (reapply with `git -C vendor/llm-agent-collusion apply ../../patches/llm-agent-collusion.patch` after a fresh clone). New flags: `--effort` (Claude only) and `--overseer_model`. New model IDs route by name: `claude-*` to the Claude API, `deepseek-flash` to DeepSeek's API, anything with a slash to OpenRouter. No refusal fallback is set on purpose: a fallback would answer with a different model and contaminate a run.

Checked in `vendor/llm-agent-collusion/src/resources/model_wrappers.py`:

1. **Temperature breaks every current Claude model.** The Anthropic wrapper sends `temperature=0.7`. Fable 5.1 and Opus 5.5 reject any sampling parameter, and Sonnet 5.5 and Haiku 5.5 reject anything but the default. All four return a 400 error. Drop the parameter for Claude. This also means Claude runs at default sampling while the GPT and DeepSeek runs use 0.7. That mismatch is a confound, so put it in Limitations.
2. **`SUPPORTED_MODELS`** in `cda_types.py` lists only mid-2025 models. Add the new IDs: `claude-haiku-5-5`, `claude-fable-5-1`, and the DeepSeek and OpenAI IDs.
3. **DeepSeek needs no new wrapper.** The OpenRouter client already exists (one key covers DeepSeek, OpenAI, Gemini and Jev). DeepSeek's own API is OpenAI-compatible too, so you could point the OpenAI client at DeepSeek's base URL instead.
4. **Refusals.** Current Claude models can stop with `stop_reason: "refusal"`. Price-fixing role-play is unlikely to trip a classifier, but log the stop reason so a refusal doesn't get recorded as a bid.
5. **Data note.** DeepSeek's API runs in China. That's fine for synthetic auction prompts, but don't send anything personal.

## 4. Efficiency tools

| Tool | What it is | Saves | Use here? |
|---|---|---|---|
| **Jev** (TypeSafe AI) | A hosted "decision model": you give it text and a fixed list of options, and it returns a typed choice with a probability. It doesn't write free text. About $0.042 per 1M input tokens, output free, 32K context. Closed weights; available on OpenRouter and Vercel AI Gateway (one source says waitlisted). | Bounded yes/no and pick-one calls that would otherwise go to a full LLM. REFLEX paper: 72.7% fewer strong-model calls on its own 100-task benchmark, little gain where cheap routing is already accurate. | **Yes, as a cheap "words" scorer and a baseline.** Labelling all ~11,000 seller messages in the 75 runs ("proposes a price floor / agrees to one / neither") costs well under $1. Compare it against the run's existing LLM judge and your detector. Never use it to play the agents, because that changes what you're studying. |
| **Ponytail** | A Claude Code plugin that pushes the agent toward the smallest working code (standard library first, no new abstractions). | Its own benchmark: 54% less code, 22% fewer tokens across 12 tasks. | Optional. It keeps the analysis code small; judges only read the PDF. |
| **Caveman** | A skill that makes the agent's replies terse. | Up to 65% fewer output tokens (project's claim). | Optional, for your Claude Code session only. Keep it out of the market agents' prompts: terse agents could collude differently. |
| **RTK** (Rust Token Killer) | Compresses shell output (git, tests, logs) before the agent reads it. | 60-90% of command-output tokens. | Useful during the build. |
| **Context Mode** | An MCP server that keeps big tool output in a local search index and returns only matches. | Example: 315 KB of output down to 5.4 KB. | **The most useful of the four for this sprint.** One run's transcripts are 3.3 MB, and reading a few into Claude Code would burn your weekend limits. |

The coding-agent tools (Ponytail, Caveman, RTK, Context Mode) all stretch your Max plan limits while you build. None of them changes what the experiments cost. The levers that cut experiment cost are, in order: the free main result on the 75 bundled runs, a cheap model for new runs, off-peak DeepSeek, and caching.

Sources: [REFLEX with Jev, arXiv 2609.26532](https://arxiv.org/abs/2609.26532), [requesty on Jev pricing](https://www.requesty.ai/blog/typesafe-jev-explained), [Forbes on decision models](https://www.forbes.com/sites/ronschmelzer/2026/10/12/decisions-decisions-a-guide-to-the-new-wave-of-ai-decision-models-besides-jev/), [DataCamp: four token-saving tools](https://www.datacamp.com/tutorial/how-to-reduce-token-usage-in-ai-coding-agents), [Ponytail write-up](https://manish.sh/writings/ai-tools/ponytail).

## 5. What this adds to Pick A

A cross-model arm fits the remaining budget. Use the cheapest model (Haiku 5.5) for the null and positive controls, DeepSeek Flash as a second family, and a small Fable 5.1 seller arm as the "most capable model" probe. The question: does a detector calibrated on the 2025 GPT-4.1 runs still catch collusion by models it has never seen, at the same false-positive rate? Total about $50 to $90, most of it Fable, which fits inside one month of Max credit.
