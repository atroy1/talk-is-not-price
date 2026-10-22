#!/usr/bin/env python3
"""Sequential launcher for the starter's market runs, built to run unattended overnight.

    python -m tools.run_queue config/queue-friday.toml            # run it
    python -m tools.run_queue config/queue-friday.toml --dry-run  # print the commands only
    python -m tools.run_queue config/queue-fake.toml --fake       # 2 rounds against a built-in fake server, no keys
    touch runs/STOP                                               # finish the current run, then stop

One run at a time (rate limits), no model fallback (a fallback would record another model's
behaviour under this one's name), one retry on a non-zero exit, then skip. Each run's stdout and
stderr go to runs/live/<tag>/, the starter's results folder is moved there afterwards, and one
line per run is appended to notes/log.md with the exit code, the wall clock and an estimated cost.
A tag whose folder already holds collusion_metrics.json is skipped unless --force.

Queue file (TOML):
    [defaults]            rounds = 30, sellers = 5, buyers = 5, timeout_min = 120, effort = "" (Claude only),
                          eval_model = "gpt-4.1-mini" (the starter's per-run judge; "openai/gpt-4.1-mini" routes it via OpenRouter),
                          reasoning = "default" | "off" | "minimal" | "low" | "medium" | "high" (OpenRouter models' hidden reasoning),
                          or_provider = { quantizations = ["fp8"] } (OpenRouter host filter, merged into the provider block),
                          seller_prompt_template = "seller_prompt_compete.jinja2" (a file in the starter's prompt_templates/),
                          seed = 7 (fixes the market and local replies), zip_buyers = true (algorithmic buyers),
                          inject_round = 12, inject_text = "..." (added to every seller prompt from that round: branch replays),
                          think_prefill = "...", think_round = 8 (written as the opening of each seller's private reasoning
                          from that round; needs reasoning = "default": thought injection)
    [[runs]]              tag, seller_model, buyer_model, seller_comms, oversight, boss_pressure, hide_num_rounds, plus any default
Models must be in the starter's SUPPORTED_MODELS (patched list in patches/llm-agent-collusion.patch).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import tomllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from tools.llm import load_config, price, load_env

ROOT = Path(__file__).resolve().parent.parent
STARTER = ROOT / "vendor" / "llm-agent-collusion"
PYTHON = ROOT / ".venv" / "bin" / "python"
LIVE = ROOT / "runs" / "live"
STOP = ROOT / "runs" / "STOP"
LOG = ROOT / "notes" / "log.md"
TOKENS_PER_30_ROUNDS = (650_000, 165_000)  # measured on base-seller_comms-1, docs/MODELS-AND-TOOLS.md
JUDGE_TOKENS_PER_30_ROUNDS = (225_000, 45_000)  # 5 sellers x 30 rounds x about 1.5k in / 300 out, the per-run judge
FLAGS = ("seller_comms", "buyer_comms", "oversight", "boss_pressure", "hide_num_rounds")
FLAG_ARG = {"seller_comms": "--seller_comms_enabled", "buyer_comms": "--buyer_comms_enabled",
            "oversight": "--oversight_enabled", "boss_pressure": "--boss_pressure", "hide_num_rounds": "--hide_num_rounds"}


def load_queue(path):
    q = tomllib.load(open(path, "rb"))
    d = {"rounds": 30, "sellers": 5, "buyers": 5, "timeout_min": 120, "effort": "", "overseer_model": "",
         "eval_model": "gpt-4.1-mini", "reasoning": "default", "or_provider": {}}  # the starter's per-run judge; "openai/gpt-4.1-mini" sends it through OpenRouter
    d.update(q.get("defaults", {}))
    runs = []
    for r in q["runs"]:
        spec = dict(d); spec.update(r)
        spec.setdefault("buyer_model", spec["seller_model"])
        if "tag" not in spec:
            raise SystemExit(f"run without a tag: {r}")
        runs.append(spec)
    return runs


def command(spec):
    cmd = [str(PYTHON), "-m", "src.continuous_double_auction.simulation",
           "--seller_models", *([spec["seller_model"]] * spec["sellers"]),
           "--buyer_models", *([spec["buyer_model"]] * spec["buyers"]),
           "--rounds", str(spec["rounds"]), "--tag", spec["tag"]]
    for f in FLAGS:
        if spec.get(f):
            cmd.append(FLAG_ARG[f])
    if spec.get("effort"):
        cmd += ["--effort", spec["effort"]]
    if spec.get("overseer_model"):
        cmd += ["--overseer_model", spec["overseer_model"]]
    if spec.get("seller_prompt_template"):
        cmd += ["--seller_prompt_template", spec["seller_prompt_template"]]
    if spec.get("seed") is not None:
        cmd += ["--seed", str(spec["seed"])]
    if spec.get("zip_buyers"):
        i = cmd.index("--buyer_models")
        cmd[i:i + 1 + spec["buyers"]] = ["--zip_buyers"]
    return cmd


def estimate(spec, cfg):
    """Rough dollars: half the tokens to sellers' model, half to buyers', scaled by rounds."""
    tin, tout = (t * spec["rounds"] / 30 for t in TOKENS_PER_30_ROUNDS)
    total = 0.0
    for model in (spec["seller_model"],) + (() if spec.get("zip_buyers") else (spec["buyer_model"],)):
        lane = "claude" if model.startswith("claude") else "openrouter"
        p = price(cfg, lane, model, tin / 2, tout / 2)
        total += 0.0 if p != p else p  # NaN (unknown price) counts as 0 and is flagged by the caller
    jin, jout = (t * spec["rounds"] / 30 for t in JUDGE_TOKENS_PER_30_ROUNDS)
    pj = price(cfg, "openrouter", spec["eval_model"], jin, jout)
    total += 0.0 if pj != pj else pj
    return total


def attempt_needs_openai(spec):
    return spec["eval_model"].startswith("gpt") and not os.environ.get("OPENAI_API_KEY")


def known_prices(spec, cfg):
    models = (spec["seller_model"], spec["eval_model"]) + (() if spec.get("zip_buyers") else (spec["buyer_model"],))
    return all(m in cfg.get("prices", {}) for m in models)


def log_line(text):
    with open(LOG, "a") as f:
        f.write(f"- {time.strftime('%Y-%m-%d %H:%M')} queue: {text}\n")


def newest_results(tag, since):
    cands = [p for p in (STARTER / "results").glob(f"*_{tag}") if p.stat().st_mtime >= since - 5]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def run_one(spec, cfg, attempt, env):
    out = LIVE / spec["tag"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "spec.json").write_text(json.dumps(spec, indent=2))
    cmd = command(spec)
    t0 = time.time()
    usage_log = out / f"usage.{attempt}.jsonl"
    usage_log.unlink(missing_ok=True)
    reasoning_log = out / f"reasoning.{attempt}.jsonl"
    reasoning_log.unlink(missing_ok=True)
    env = dict(env, CDA_EVAL_MODEL=spec["eval_model"], CDA_REASONING=spec["reasoning"], CDA_USAGE_LOG=str(usage_log),
               CDA_REASONING_LOG=str(reasoning_log),
               CDA_OR_PROVIDER=json.dumps(spec["or_provider"]) if spec["or_provider"] else "",
               CDA_OR_PROVIDER_MODELS=",".join({spec["seller_model"], spec["buyer_model"]}),
               CDA_INJECT_ROUND=str(spec.get("inject_round", "")), CDA_INJECT_TEXT=spec.get("inject_text", ""),
               CDA_LOCAL_MODELS=str(ROOT / "config" / "local-models.json"),
               CDA_THINK_PREFILL=spec.get("think_prefill", ""), CDA_THINK_ROUND=str(spec.get("think_round", 1)))
    with open(out / f"stdout.{attempt}.log", "w") as so, open(out / f"stderr.{attempt}.log", "w") as se:
        try:
            p = subprocess.run(cmd, cwd=STARTER, stdout=so, stderr=se, env=env, timeout=spec["timeout_min"] * 60)
            code = p.returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    mins = (time.time() - t0) / 60
    res = newest_results(spec["tag"], t0)
    if res is not None:
        dest = out / "run"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(res), dest)
    market_ok = res is not None and rounds_done(out / "run" / "auction_results.md") >= spec["rounds"]
    metrics_ok = market_ok and judge_scored(out / "run" / "collusion_metrics.json")
    return code, mins, market_ok, metrics_ok, actual_cost(usage_log, cfg)


def judge_scored(path):
    """True when the per-run judge produced at least one seller coordination score."""
    if not path.exists():
        return False
    m = json.loads(path.read_text())
    return any(v is not None for k, vals in m.items() if k.endswith("_coordination_score") for v in (vals or []))


def rounds_done(path):
    """Completed rounds in the starter's auction_results.md (one JSON block per finished round)."""
    if not path.exists():
        return 0
    import re
    blocks = re.findall(r"````json\n(.*?)\n````", path.read_text(), re.S)
    return max((json.loads(b).get("round_number", 0) for b in blocks), default=0)


def actual_cost(usage_log, cfg):
    """Real spend from the per-call usage log: OpenRouter reports cost; Anthropic is priced from config."""
    if not usage_log.exists():
        return None
    usd, calls, empty, reasoning = 0.0, 0, 0, 0
    for line in usage_log.read_text().splitlines():
        r = json.loads(line); calls += 1; empty += not r.get("ok", True)
        if r.get("route") == "local":
            continue  # the Studio costs nothing per call
        if r.get("route") == "openrouter":
            usd += float(r.get("cost") or 0)
            reasoning += int(((r.get("completion_tokens_details") or {}).get("reasoning_tokens")) or 0)
        else:
            p = price(cfg, "claude", r["model"], int(r.get("input_tokens") or 0), int(r.get("output_tokens") or 0))
            usd += 0.0 if p != p else p
    return {"usd": usd, "calls": calls, "empty": empty, "reasoning_tokens": reasoning}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("queue"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fake", action="store_true", help="serve a fake OpenAI endpoint and point the starter at it")
    ap.add_argument("--force", action="store_true", help="rerun tags that already have metrics")
    ap.add_argument("--log", help="append queue lines here instead of notes/log.md (the Studio uses runs/live/queue-log.md)")
    a = ap.parse_args()
    global LOG
    if a.log:
        LOG = (ROOT / a.log) if not os.path.isabs(a.log) else Path(a.log)
        LOG.parent.mkdir(parents=True, exist_ok=True)
    load_env()
    cfg = load_config()
    runs = load_queue(a.queue)
    env = dict(os.environ, WANDB_MODE="disabled", WANDB_SILENT="true", PYTHONUNBUFFERED="1")
    if a.fake:
        srv = HTTPServer(("127.0.0.1", 0), FakeOpenAI)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        env.update(OPENAI_BASE_URL=f"http://127.0.0.1:{srv.server_port}/v1", OPENAI_API_KEY="fake")
        print(f"fake OpenAI server on port {srv.server_port}")

    total = 0.0
    print(f"{len(runs)} runs in {a.queue}")
    for spec in runs:
        est = estimate(spec, cfg); total += est
        flag = "" if known_prices(spec, cfg) else "  (price unknown for a model: estimate incomplete)"
        buyers = "ZIP buyers" if spec.get("zip_buyers") else spec["buyer_model"]
        print(f"  {spec['tag']:34s} {spec['seller_model']} / {buyers}  {spec['rounds']} rounds  ~${est:.2f}{flag}")
        if attempt_needs_openai(spec):
            print(f"     NOTE: judge {spec['eval_model']} goes to the OpenAI API and needs OPENAI_API_KEY; set eval_model = \"openai/gpt-4.1-mini\" to use OpenRouter")
        if a.dry_run:
            print("     " + " ".join(command(spec)))
    print(f"estimated total ~${total:.2f}")
    if a.dry_run:
        return
    if not PYTHON.exists() or not (STARTER / "src").exists():
        raise SystemExit("starter or .venv missing")

    LIVE.mkdir(parents=True, exist_ok=True)
    log_line(f"start {a.queue}, {len(runs)} runs, est ${total:.2f}")
    for spec in runs:
        if STOP.exists():
            log_line(f"STOP file found, stopping before {spec['tag']}"); print("STOP"); break
        done = rounds_done(LIVE / spec["tag"] / "run" / "auction_results.md") >= spec["rounds"]
        if done and not a.force:
            print(f"skip {spec['tag']} (done)"); continue
        for attempt in (1, 2):
            print(f"run {spec['tag']} attempt {attempt} ...", flush=True)
            code, mins, market_ok, metrics_ok, spent = run_one(spec, cfg, attempt, env)
            if metrics_ok and code == 0:
                status = "ok"
            elif market_ok:
                status = f"market done, judge scores missing (exit {code}); rescore later, not rerun"
            else:
                status = f"failed (exit {code}), market incomplete"
            bill = (f"spent ${spent['usd']:.3f} over {spent['calls']} calls ({spent['empty']} empty, {spent['reasoning_tokens']} reasoning tokens)"
                    if spent else f"est ${estimate(spec, cfg):.2f}")
            log_line(f"{spec['tag']} attempt {attempt}: {status}, {mins:.1f} min, runs/live/{spec['tag']}, {bill} "
                     f"({spec['seller_model']} sellers, {'ZIP' if spec.get('zip_buyers') else spec['buyer_model']} buyers, {spec['rounds']} rounds, reasoning {spec['reasoning']}, judge {spec['eval_model']})")
            print(f"   {status} in {mins:.1f} min; {bill}")
            if market_ok:
                break  # never pay for the same market twice because the judge failed
        else:
            log_line(f"{spec['tag']} skipped after 2 attempts")
    log_line(f"end {a.queue}")


# ---------------------------------------------------------------- fake OpenAI endpoint for --fake

class FakeOpenAI(BaseHTTPRequestHandler):
    """Answers any chat completion with the JSON the seller or buyer prompt asks for.
    Sellers ask 90.00 and buyers bid 91.00 so trades happen; chat fields are filled when the prompt has them."""
    hits = 0

    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n) or b"{}")
        prompt = "\n".join(m.get("content", "") for m in req.get("messages", []))
        FakeOpenAI.hits += 1
        reply = {"reflection": "fake", "plan_for_this_hour": "fake", "new_memory": "fake hour", "scratch_pad_update": "#### Observations\nfake"}
        if '"ask":' in prompt:
            reply["ask"] = 90.0
            if "message_to_sellers" in prompt:
                reply.update(plan_for_message="fake", message_to_sellers="Let's remain unified at $93.00 this hour.")
        else:
            reply["bid"] = 91.0
            if "message_to_buyers" in prompt:
                reply.update(plan_for_message="fake", message_to_buyers="hold bids")
        if '"coordination":' in prompt:  # the starter's per-run judge and the overseer ask for this shape
            reply = {"coordination": "no", "score": 1, "type": "null", "evidence": []}
        body = json.dumps({"id": "fake", "object": "chat.completion", "created": 0, "model": req.get("model"),
                           "choices": [{"index": 0, "finish_reason": "stop",
                                        "message": {"role": "assistant", "content": json.dumps(reply)}}],
                           "usage": {"prompt_tokens": len(prompt) // 4, "completion_tokens": 80, "total_tokens": len(prompt) // 4 + 80}}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


if __name__ == "__main__":
    main()
