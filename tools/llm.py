#!/usr/bin/env python3
"""One door for every LLM call outside the market simulator.

    from tools.llm import complete
    r = complete("label_message", "Let's remain unified at $93.00 this hour.", system=PROMPT)
    r.text, r.lane, r.model, r.usd

    python -m tools.llm --ping                 # one tiny call per lane whose key is set
    python -m tools.llm --self-test            # fake server; no network, no key
    python -m tools.llm --task talk_notes --prompt "..." [--system "..."]
    python -m tools.llm --ledger               # spend so far by lane and task

Lanes, prices and tasks live in config/models.toml. Every call appends one row to
notes/cost-ledger.csv, which the Methods cost line and the LLM Usage Statement read from.
No silent fallback: a task falls back only when its config names one, and the row says so.
Current Claude models reject sampling parameters, so the Anthropic path never sends temperature.
"""
import argparse
import csv
import json
import os
import sys
import threading
import time
import tomllib
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "models.toml"
LEDGER = ROOT / "notes" / "cost-ledger.csv"
COLUMNS = ["ts", "task", "lane", "model", "provider", "in_tokens", "out_tokens", "usd",
           "latency_s", "ok", "fallback_from", "stop_reason", "note"]


def load_env():
    """Fill os.environ from .env at the project root without overriding the shell."""
    p = ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load_config():
    with open(CONFIG, "rb") as f:
        return tomllib.load(f)


@dataclass
class Reply:
    text: str
    task: str
    lane: str
    model: str
    provider: str
    in_tokens: int
    out_tokens: int
    usd: float
    latency_s: float
    ok: bool = True
    fallback_from: str = ""
    stop_reason: str = ""
    note: str = ""
    top_logprobs: list = None  # first answer token's alternatives as (token, probability), when the task asks for them


def price(cfg, lane, model, in_tokens, out_tokens):
    if lane == "local":
        return 0.0
    p = cfg.get("prices", {}).get(model)
    if not p:
        return float("nan")
    return (in_tokens * p[0] + out_tokens * p[1]) / 1_000_000


def lane_base_url(lane_cfg):
    if "base_url" in lane_cfg:
        return lane_cfg["base_url"]
    return os.environ.get(lane_cfg["base_url_env"], "")


def lane_key(lane_cfg):
    return os.environ.get(lane_cfg.get("key_env", ""), "")


def lane_ready(cfg, lane):
    lc = cfg["lanes"][lane]
    if lc["kind"] == "anthropic":
        return bool(lane_key(lc))
    if "base_url" in lc:
        return bool(lane_key(lc))
    return bool(lane_base_url(lc))


def _call_openai(lc, model, system, user, max_tokens, temperature, logprobs=0, provider=None):
    from openai import OpenAI
    base = lane_base_url(lc)
    client = OpenAI(base_url=base, api_key=lane_key(lc) or "none", max_retries=2, timeout=120)
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    kw = dict(model=model, messages=msgs, max_tokens=max_tokens)
    if temperature is not None:
        kw["temperature"] = temperature
    if lc.get("extra_body"):
        kw["extra_body"] = json.loads(json.dumps(lc["extra_body"]))
    if provider:
        kw.setdefault("extra_body", {}).setdefault("provider", {}).update(provider)
    if logprobs:
        kw.update(logprobs=True, top_logprobs=logprobs)
        # only hosts that really return logprobs may serve the call
        kw.setdefault("extra_body", {}).setdefault("provider", {})["require_parameters"] = True
    r = client.chat.completions.create(**kw)
    text = r.choices[0].message.content or ""
    _call_openai.last_top = None
    lp = getattr(r.choices[0], "logprobs", None)
    if logprobs and lp and lp.content:
        import math
        _call_openai.last_top = [(t.token, round(math.exp(t.logprob), 4)) for t in lp.content[0].top_logprobs]
    u = r.usage
    provider = getattr(r, "provider", None) or urlparse(base).hostname or "openai-compatible"
    return text, int(u.prompt_tokens or 0), int(u.completion_tokens or 0), str(provider), r.model or model, \
        str(r.choices[0].finish_reason or "")


def _call_anthropic(lc, model, system, user, max_tokens, temperature, logprobs=0, provider=None):
    import anthropic
    ws = os.environ.get("ANTHROPIC_WORKSPACE_ID")  # needed when the key is organisation-level, not workspace-scoped
    client = anthropic.Anthropic(api_key=lane_key(lc), max_retries=2, timeout=120,
                                 default_headers={"anthropic-workspace-id": ws} if ws else None)
    kw = dict(model=model, max_tokens=max_tokens, messages=[{"role": "user", "content": user}])
    if system:
        kw["system"] = system
    r = client.messages.create(**kw)  # no temperature on purpose
    text = "".join(getattr(b, "text", "") for b in r.content if getattr(b, "type", "") == "text")
    return text, int(r.usage.input_tokens), int(r.usage.output_tokens), "anthropic", r.model, str(r.stop_reason)


def _once(cfg, task, lane, model, system, user, max_tokens, temperature, note, fallback_from="", logprobs=0, provider=None):
    lc = cfg["lanes"][lane]
    t0 = time.time()
    fn = _call_anthropic if lc["kind"] == "anthropic" else _call_openai
    text, tin, tout, provider, model_used, stop = fn(lc, model, system, user, max_tokens, temperature, logprobs, provider)
    top = getattr(_call_openai, "last_top", None) if fn is _call_openai else None
    return Reply(text=text, task=task, lane=lane, model=model_used, provider=provider, in_tokens=tin,
                 out_tokens=tout, usd=price(cfg, lane, model, tin, tout), latency_s=round(time.time() - t0, 2),
                 fallback_from=fallback_from, stop_reason=stop, note=note, top_logprobs=top)


def log(reply):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    new = not LEDGER.exists()
    row = asdict(reply)
    row["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    row.pop("text"); row.pop("top_logprobs", None)
    with open(LEDGER, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        if new:
            w.writeheader()
        w.writerow(row)


def complete(task, user, system=None, model=None, lane=None, max_tokens=None, temperature=None, note=""):
    load_env()
    cfg = load_config()
    t = cfg["tasks"][task]
    lane = lane or t["lane"]
    model = model or t.get("model") or cfg["lanes"][lane].get("default_model")
    max_tokens = max_tokens or t.get("max_tokens", 256)
    temperature = t.get("temperature") if temperature is None else temperature
    logprobs = int(t.get("top_logprobs", 0))
    provider = t.get("provider")
    try:
        reply = _once(cfg, task, lane, model, system, user, max_tokens, temperature, note, logprobs=logprobs, provider=provider)
    except Exception as e:  # noqa: BLE001
        fb = t.get("fallback")
        failed = Reply(text="", task=task, lane=lane, model=model, provider="", in_tokens=0, out_tokens=0,
                       usd=0.0, latency_s=0.0, ok=False, note=f"{type(e).__name__}: {str(e)[:120]}")
        log(failed)
        if not fb:
            raise
        fl, fm = fb.split(":", 1)
        reply = _once(cfg, task, fl, fm, system, user, max_tokens, temperature, note,
                      fallback_from=f"{lane}:{model}", logprobs=logprobs)
    log(reply)
    return reply


# ---------------------------------------------------------------- fake server for --self-test

class _Fake(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silence
        pass

    def do_GET(self):
        body = json.dumps({"object": "list", "data": [{"id": "fake-model", "object": "model"}]}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n) or b"{}")
        if req.get("model") == "does-not-exist":
            body = json.dumps({"error": {"message": "model not found"}}).encode()
            self.send_response(404)
        else:
            body = json.dumps({"id": "x", "object": "chat.completion", "created": 0, "model": req.get("model"),
                               "choices": [{"index": 0, "finish_reason": "stop",
                                            "message": {"role": "assistant", "content": "FLOOR"}}],
                               "usage": {"prompt_tokens": 42, "completion_tokens": 1, "total_tokens": 43}}).encode()
            self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


def self_test():
    global LEDGER
    real_ledger, LEDGER = LEDGER, ROOT / "runs" / "selftest-ledger.csv"  # never pollute the real ledger
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.unlink(missing_ok=True)
    srv = HTTPServer(("127.0.0.1", 0), _Fake)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    os.environ["LMSTUDIO_BASE_URL"] = f"http://127.0.0.1:{srv.server_port}/v1"
    os.environ["LMSTUDIO_API_KEY"] = "test"
    before = LEDGER.read_text().count("\n") if LEDGER.exists() else 1  # header counts
    r = complete("label_message", "Let's remain unified at $93.00 this hour.", system="Label it.",
                 model="fake-model", note="self-test")
    assert r.text == "FLOOR" and r.usd == 0.0 and r.in_tokens == 42, r
    r2 = complete("_selftest", "x", note="self-test fallback")
    assert r2.fallback_from == "local:does-not-exist" and r2.model == "fake-model", r2
    after = LEDGER.read_text().count("\n")
    assert after - before == 3, (before, after)  # ok row, failed row, fallback row
    srv.shutdown()
    print("self-test ok: direct call, fallback path, ledger rows", LEDGER.relative_to(ROOT))
    LEDGER = real_ledger


def ping():
    load_env()
    cfg = load_config()
    for lane in cfg["lanes"]:
        if not lane_ready(cfg, lane):
            print(f"{lane:11s} SKIP  no key or base url in .env"); continue
        try:
            r = complete("_ping", "Reply with the single word OK.", lane=lane, note="ping")
            print(f"{lane:11s} OK    {r.model} via {r.provider} {r.latency_s}s ${r.usd:.5f} -> {r.text.strip()[:20]!r}")
        except Exception as e:  # noqa: BLE001
            print(f"{lane:11s} FAIL  {type(e).__name__}: {str(e)[:100]}")


def ledger():
    if not LEDGER.exists():
        print("no ledger yet"); return
    tot = {}
    with open(LEDGER) as f:
        for row in csv.DictReader(f):
            if row["ok"] != "True":
                continue
            k = (row["lane"], row["task"])
            t = tot.setdefault(k, [0, 0, 0.0, 0])
            t[0] += int(row["in_tokens"]); t[1] += int(row["out_tokens"])
            t[2] += float(row["usd"] or 0); t[3] += 1
    print(f"{'lane':11s} {'task':16s} {'calls':>6s} {'in':>9s} {'out':>8s} {'usd':>8s}")
    for (lane, task), (i, o, u, n) in sorted(tot.items()):
        print(f"{lane:11s} {task:16s} {n:6d} {i:9d} {o:8d} {u:8.3f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ping", action="store_true"); ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--ledger", action="store_true"); ap.add_argument("--task"); ap.add_argument("--prompt")
    ap.add_argument("--system"); ap.add_argument("--lane"); ap.add_argument("--model")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.ping:
        return ping()
    if a.ledger:
        return ledger()
    if a.task and a.prompt:
        r = complete(a.task, a.prompt, system=a.system, lane=a.lane, model=a.model)
        print(r.text); print(f"[{r.lane} {r.model} in={r.in_tokens} out={r.out_tokens} ${r.usd:.4f} {r.latency_s}s]", file=sys.stderr)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
