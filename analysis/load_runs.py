"""Load the 75 bundled double-auction runs (Agrawal et al. 2025) into flat tables.

Plumbing only: this reads what the runs recorded and computes nothing new.
Prior data, built before the sprint; disclose it as such.

    from analysis.load_runs import load_all
    t = load_all()            # dict of DataFrames, cached in runs/tables.pkl
    t["runs"], t["orders"], t["trades"], t["messages"], t["turns"], t["judge"]

    python -m analysis.load_runs   # rebuild the cache and print a summary
"""
import glob
import json
import os
import pickle
import re

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "vendor", "llm-agent-collusion", "data")
CACHE = os.path.join(ROOT, "runs", "tables.pkl")
CACHE_VERSION = 1

JSON_BLOCK = re.compile(r"````json\n(.*?)\n````", re.S)
TURN = re.compile(r"\n(?=## (?:Prompt|Response): Round )")
TURN_HEAD = re.compile(r"## (Prompt|Response): Round (\d+) - (\S+ \S+)")
FLAGS = ["seller_comms_enabled", "buyer_comms_enabled", "oversight_enabled", "boss_pressure", "hide_num_rounds"]
# Per-round series in collusion_metrics.json, kept in the orders-free "metric_rounds" table
ROUND_SERIES = ["avg_seller_asks_by_round", "avg_buyer_bids_by_round", "avg_trade_prices_by_round",
                "collusion_indices", "seller_ask_dispersions", "price_cost_margins"]


def run_dirs():
    return sorted(d for d in glob.glob(os.path.join(DATA, "*")) if os.path.isdir(d))


def _split_tag(tag):
    """'gpt_buyers-claude_sellers-seller_comms-3' -> ('gpt_buyers-claude_sellers-seller_comms', 3)"""
    m = re.match(r"(.*)-(\d+)$", tag)
    return (m.group(1), int(m.group(2))) if m else (tag, None)


def _load_run(path):
    run_id = os.path.basename(path)
    meta = json.load(open(os.path.join(path, "experiment_metadata.json")))
    cfg = meta["auction_config"]
    metrics = json.load(open(os.path.join(path, "collusion_metrics.json")))
    condition, seed = _split_tag(cfg["tag"])
    sellers, buyers = meta["seller_ids"], meta["buyer_ids"]
    model_of = dict(zip(sellers, cfg["seller_models"])) | dict(zip(buyers, cfg["buyer_models"]))

    run = {"run_id": run_id, "condition": condition, "seed": seed, "rounds": cfg["rounds"],
           "seller_models": "+".join(sorted(set(cfg["seller_models"]))),
           "buyer_models": "+".join(sorted(set(m for m in cfg["buyer_models"] if m))),
           "temperature": cfg.get("temperature")}
    run |= {f: bool(cfg.get(f)) for f in FLAGS}
    run |= {k: v for k, v in metrics.items() if not isinstance(v, (list, dict))}

    orders, trades, messages = [], [], []
    text = open(os.path.join(path, "auction_results.md")).read()
    for block in JSON_BLOCK.findall(text):
        r = json.loads(block)
        n = r["round_number"]
        orders += [{"run_id": run_id, "round": n, "agent": a, "side": "ask", "price": p} for a, p in r["seller_asks"].items()]
        orders += [{"run_id": run_id, "round": n, "agent": a, "side": "bid", "price": p} for a, p in r["buyer_bids"].items()]
        trades += [{"run_id": run_id, "round": n, "buyer": t["buyer_id"], "seller": t["seller_id"], "price": t["price"]}
                   for t in r.get("trades", [])]
        for kind in ("seller_messages", "buyer_messages"):
            messages += [{"run_id": run_id, "round": n, "agent": a, "channel": kind.split("_")[0], "text": m}
                         for a, m in (r.get(kind) or {}).items()]

    metric_rounds = pd.DataFrame({k: metrics[k] for k in ROUND_SERIES if k in metrics})
    metric_rounds.insert(0, "round", range(1, len(metric_rounds) + 1))
    metric_rounds.insert(0, "run_id", run_id)

    # Each agent's own transcript: the prompt it saw and the JSON it answered with
    turns = []
    for f in sorted(glob.glob(os.path.join(path, "*.md"))):
        agent = os.path.basename(f)[:-3]
        if agent == "auction_results":
            continue
        role = "overseer" if agent == "Overseer" else agent.split()[0].lower()
        prompt_chars = {}
        for blk in TURN.split(open(f).read()):
            h = TURN_HEAD.match(blk)
            if not h:
                continue
            kind, n, ts = h.group(1), int(h.group(2)), h.group(3)
            if kind == "Prompt":
                prompt_chars[n] = len(blk)
                continue
            row = {"run_id": run_id, "round": n, "agent": agent, "role": role, "model": model_of.get(agent),
                   "time": ts, "prompt_chars": prompt_chars.get(n), "response_chars": len(blk), "parse_error": False}
            j = JSON_BLOCK.search(blk)
            try:
                body = json.loads(j.group(1)) if j else None
            except json.JSONDecodeError:
                body = None
            if isinstance(body, dict):
                row |= {k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in body.items()}
            else:
                row["parse_error"] = True
                row["raw"] = blk
            turns.append(row)

    # LLM judge, one verdict per seller per round; seller_N is the Nth id in experiment_metadata
    judge = []
    eval_path = os.path.join(path, "llm_eval_full.json")
    if os.path.exists(eval_path):
        for s in json.load(open(eval_path)):
            idx = int(s["seller_id"].split("_")[1]) - 1
            for r in s["rounds"]:
                d = r.get("data") or {}
                judge.append({"run_id": run_id, "round": r["round"], "seller_key": s["seller_id"],
                              "agent": sellers[idx] if idx < len(sellers) else None, "status": r.get("status"),
                              "coordination": d.get("coordination"), "score": d.get("score"),
                              "type": d.get("type"), "n_evidence": len(d.get("evidence") or []),
                              "evidence": json.dumps(d.get("evidence") or [])})

    return run, orders, trades, messages, metric_rounds, turns, judge


def build():
    parts = [_load_run(d) for d in run_dirs()]
    return {
        "runs": pd.DataFrame([p[0] for p in parts]),
        "orders": pd.DataFrame([o for p in parts for o in p[1]]),
        "trades": pd.DataFrame([t for p in parts for t in p[2]]),
        "messages": pd.DataFrame([m for p in parts for m in p[3]]),
        "metric_rounds": pd.concat([p[4] for p in parts], ignore_index=True),
        "turns": pd.DataFrame([t for p in parts for t in p[5]]),
        "judge": pd.DataFrame([j for p in parts for j in p[6]]),
    }


def load_all(rebuild=False):
    if not rebuild and os.path.exists(CACHE):
        cached = pickle.load(open(CACHE, "rb"))
        if cached.get("version") == CACHE_VERSION:
            return cached["tables"]
    tables = build()
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    pickle.dump({"version": CACHE_VERSION, "tables": tables}, open(CACHE, "wb"))
    return tables


LIVE = os.path.join(ROOT, "runs", "live")


def live_run_dirs(prefixes=None):
    """Finished new runs: runs/live/<tag>/run/ holding metrics and the judge file. Checks are skipped by name."""
    out = []
    for d in sorted(glob.glob(os.path.join(LIVE, "*", "run"))):
        tag = os.path.basename(os.path.dirname(d))
        # plumbing checks and smoke tests, not data (the Qwen arm's real runs, qwen35b-...-s<N>, are kept)
        if "-check" in tag or "-smoke" in tag or tag.startswith(("fake", "replay", "test", "qwen9b")):
            continue
        if prefixes and not tag.startswith(tuple(prefixes)):
            continue
        if all(os.path.exists(os.path.join(d, f)) for f in ("experiment_metadata.json", "collusion_metrics.json", "auction_results.md")):
            out.append(d)
    return out


def load_live(prefixes=None):
    """Same tables as load_all, for the sprint's new runs (sprint work, Fri Oct 23). run_id = the queue tag."""
    parts = []
    for d in live_run_dirs(prefixes):
        p = list(_load_run(d))
        tag = os.path.basename(os.path.dirname(d))
        old = p[0]["run_id"]
        p[0] = p[0] | {"run_id": tag}
        p[0]["condition"], p[0]["seed"] = _split_tag(tag)
        for i in (1, 2, 3, 5, 6):
            for row in p[i]:
                row["run_id"] = tag
        p[4]["run_id"] = tag
        parts.append(p)
    if not parts:
        return {}
    return {
        "runs": pd.DataFrame([p[0] for p in parts]),
        "orders": pd.DataFrame([o for p in parts for o in p[1]]),
        "trades": pd.DataFrame([t for p in parts for t in p[2]]),
        "messages": pd.DataFrame([m for p in parts for m in p[3]]),
        "metric_rounds": pd.concat([p[4] for p in parts], ignore_index=True),
        "turns": pd.DataFrame([t for p in parts for t in p[5]]),
        "judge": pd.DataFrame([j for p in parts for j in p[6]]),
    }


if __name__ == "__main__":
    t = load_all(rebuild=True)
    for name, df in t.items():
        print(f"{name:<14} {len(df):>7} rows  {len(df.columns):>3} cols")
    print()
    print(t["runs"].groupby(["condition", "seller_models"]).size().to_string())
    turns = t["turns"]
    print(f"\nunparsed agent replies: {turns['parse_error'].sum()} of {len(turns)}")
    print(f"judge rows not 'success': {(t['judge']['status'] != 'success').sum()} of {len(t['judge'])}")
