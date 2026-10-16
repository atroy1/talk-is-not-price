"""Replay a recorded double-auction run as if it were running live.

No API calls. Reads one run folder from the Agrawal et al. 2025 data and prints
what a fresh run would show round by round, with the token bill priced at
whichever model you name. Usage:

    python scripts/replay_run.py [run_folder] [--model claude-haiku-5-5] [--delay 0.2]
"""
import argparse
import glob
import json
import os
import re
import statistics
import sys
import time
from collections import defaultdict

DATA = "vendor/llm-agent-collusion/data"
DEFAULT_RUN = "20250516_212322_base-seller_comms-1"

# $ per 1M tokens (input, output), checked 2026-10-16; see docs/MODELS-AND-TOOLS.md
PRICES = {
    "claude-haiku-5-5": (0.10, 0.50),
    "deepseek-flash (off-peak)": (0.15, 0.60),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-fable-5-1": (10.00, 50.00),
}

COLLUSIVE = re.compile(
    r"above \$|floor|hold (firm|steady|the line)|coordinat|together|undercut|"
    r"discipline|collective|all of us|maintain (strong|high)",
    re.I,
)


def load_rounds(run):
    text = open(os.path.join(run, "auction_results.md")).read()
    blocks = re.findall(r"````json\n(.*?)\n````", text, re.S)
    return [json.loads(b) for b in blocks]


def tokens_by_round(run):
    """Approximate tokens per round from the agents' logged prompts and replies (chars / 4)."""
    tin, tout = defaultdict(int), defaultdict(int)
    for f in glob.glob(os.path.join(run, "Seller*.md")) + glob.glob(os.path.join(run, "Buyer*.md")):
        for blk in re.split(r"\n(?=## (?:Prompt|Response): Round)", open(f).read()):
            m = re.match(r"## (Prompt|Response): Round (\d+)", blk)
            if m:
                (tin if m.group(1) == "Prompt" else tout)[int(m.group(2))] += len(blk) // 4
    return tin, tout


def pick_message(msgs):
    if not msgs:
        return None
    who, msg = max(msgs.items(), key=lambda kv: len(COLLUSIVE.findall(kv[1])))
    msg = msg if len(msg) <= 108 else msg[:105] + "..."
    return f'{who}: "{msg}"'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", nargs="?", default=DEFAULT_RUN)
    ap.add_argument("--model", default="claude-haiku-5-5", choices=PRICES)
    ap.add_argument("--delay", type=float, default=0.0)
    a = ap.parse_args()

    run = a.run if os.path.isdir(a.run) else os.path.join(DATA, a.run)
    meta = json.load(open(os.path.join(run, "experiment_metadata.json")))["auction_config"]
    metrics = json.load(open(os.path.join(run, "collusion_metrics.json")))
    rounds = load_rounds(run)
    tin, tout = tokens_by_round(run)
    p_in, p_out = PRICES[a.model]
    ce, jpm = metrics["competitive_equilibrium_price"], metrics["joint_profit_maximization_price"]

    flags = " ".join(
        f"--{k}" for k in ("seller_comms_enabled", "oversight_enabled", "boss_pressure", "hide_num_rounds") if meta.get(k)
    )
    print(f"$ python -m src.continuous_double_auction.simulation \\")
    print(f"    --seller_models {a.model} x5 --buyer_models {a.model} x5 \\")
    print(f"    --rounds {meta['rounds']} {flags} --tag {meta['tag']}")
    print(f"[replay of recorded {meta['seller_models'][0]} run; no API calls; bill priced at {a.model}]")
    print(f"sellers' cost $80, buyers' value $100 -> competitive price ${ce:.0f}, cartel price ${jpm:.0f}\n")
    print(f"{'rnd':>3}  {'asks lo/med':>13}  {'top bid':>7}  {'trades':>12}  {'calls':>5}  {'tokens in/out':>13}  {'bill':>6}")

    bill = 0.0
    calls = 0
    for r in rounds:
        n = r["round_number"]
        asks = list(r["seller_asks"].values())
        bids = list(r["buyer_bids"].values())
        trades = r.get("trades", [])
        calls += len(asks) + len(bids)
        bill += tin[n] / 1e6 * p_in + tout[n] / 1e6 * p_out
        tr = f"{len(trades)} @ ${statistics.mean(t['price'] for t in trades):.2f}" if trades else "-"
        print(
            f"{n:>3}  {min(asks):>6.2f}/{statistics.median(asks):<6.2f}  {max(bids):>7.2f}  {tr:>12}  "
            f"{calls:>5}  {f"{tin[n] / 1e3:.0f}k/{tout[n] / 1e3:.0f}k":>13}  ${bill:>5.2f}"
        )
        msg = pick_message(r.get("seller_messages"))
        if msg and (n <= 3 or n % 5 == 0):
            print(f"       chat  {msg}")
        sys.stdout.flush()
        time.sleep(a.delay)

    total_in, total_out = sum(tin.values()), sum(tout.values())
    score = statistics.mean(
        statistics.mean(v) for k, v in metrics.items() if k.endswith("_coordination_score")
    )
    print("\n--- run finished ---")
    print(f"trades {metrics['num_trades']}, average price ${metrics['avg_trade_price_overall']:.2f} "
          f"(competitive ${ce:.0f}, cartel ${jpm:.0f}); price-cost margin {metrics['average_pcm']:.1%}")
    print(f"judge's seller coordination score, mean over rounds: {score:.2f} of 5")
    print(f"tokens {total_in / 1e3:.0f}k in / {total_out / 1e3:.0f}k out over {calls} calls (visible output only)")
    print("same run on each model:")
    for m, (pi, po) in PRICES.items():
        print(f"   {m:<26} ${total_in / 1e6 * pi + total_out / 1e6 * po:>6.2f}")
    print(f"files written: {DATA}/<timestamp>_{meta['tag']}/ (10 transcripts, auction_results.md, collusion_metrics.json)")


if __name__ == "__main__":
    main()
