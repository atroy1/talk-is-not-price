"""Gate G3 on the 2025 runs: score every run, then the price-side controls and the LLM judge baseline.

Sprint work, Fri Oct 23 2026, after the pre-registration lock (commit 824c801).

    .venv/bin/python -m analysis.controls

Writes runs/derived/scores-2025.csv (one row per run and round, both channels and the judge) and prints the
control numbers. The chat side cannot be calibrated until the compete runs land (the 10 base runs have no chat),
so here words are described by condition only.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.detector import evaluate, run_max, threshold  # noqa: E402
from analysis.load_runs import load_all  # noqa: E402
from analysis.scores import score_table  # noqa: E402

HEADLINE = ["base-seller_comms", "claude_buyers-claude_sellers-seller_comms", "claude_buyers-gpt_sellers-seller_comms",
            "claude_buyers-mixed_sellers-seller_comms", "gpt_buyers-claude_sellers-seller_comms",
            "gpt_buyers-mixed_sellers-seller_comms"]
PANEL2 = ["oversight", "boss_pressure", "boss_pressure-oversight"]


def build_scores():
    t = load_all()
    runs = t["runs"].set_index("run_id")
    rounds = runs["rounds"].to_dict()
    msgs = t["messages"]
    msgs = msgs[msgs["channel"] == "seller"].copy()
    msgs["id"] = msgs["run_id"] + "|" + msgs["round"].astype(str) + "|" + msgs["agent"]
    lab = pd.read_csv(ROOT / "runs/derived/labels.csv")[["id", "p_floor", "p_agree"]]
    msgs = msgs.merge(lab, on="id", how="left")
    missing = msgs["p_floor"].isna().sum()
    msgs[["p_floor", "p_agree"]] = msgs[["p_floor", "p_agree"]].fillna(0.0)  # empty messages carry no claim
    s = score_table(t["orders"], msgs, rounds)
    j = t["judge"]
    jr = j.assign(yes=(j["coordination"] == "yes").astype(float)).groupby(["run_id", "round"]).agg(
        judge_score=("score", "mean"), judge_yes=("yes", "mean")).reset_index()
    s = s.merge(jr, on=["run_id", "round"], how="left")
    s["condition"] = s["run_id"].map(runs["condition"])
    return s, int(missing)


def seller_shuffle_null(orders, base_ids, n=200, seed=23):
    """Pseudo-honest runs: five sellers' ask series, each from a different base run. Deeds computed as usual."""
    rng = np.random.default_rng(seed)
    asks = orders[(orders["side"] == "ask") & orders["run_id"].isin(base_ids)]
    by_seller = {(r, a): g for (r, a), g in asks.groupby(["run_id", "agent"])}
    keys_by_run = {}
    for (r, a) in by_seller:
        keys_by_run.setdefault(r, []).append((r, a))
    rows = []
    for i in range(n):
        picked_runs = rng.choice(list(keys_by_run), size=5, replace=False)
        for r in picked_runs:
            k = keys_by_run[r][rng.integers(len(keys_by_run[r]))]
            g = by_seller[k]
            rows.append(g.assign(run_id=f"null{i}", agent=f"{k[0]}|{k[1]}"))
    return pd.concat(rows, ignore_index=True)


def main():
    s, missing = build_scores()  # deeds at the deviation's START_ROUND
    t = load_all()
    rounds = t["runs"].set_index("run_id")["rounds"].to_dict()
    from analysis.scores import START_ROUND, SENSITIVITY_STARTS, deeds_by_round
    variants = {f"deeds_from_r{r}": r for r in sorted({1, START_ROUND, *SENSITIVITY_STARTS})}
    for col, r in variants.items():
        s = s.merge(deeds_by_round(t["orders"], rounds, start_round=r)[["run_id", "round", "deeds"]]
                    .rename(columns={"deeds": col}), on=["run_id", "round"])
    out = ROOT / "runs/derived/scores-2025.csv"
    s.to_csv(out, index=False)
    cond = s.groupby("run_id")["condition"].first()
    base = cond[cond == "base"].index.tolist()
    head = cond[cond.isin(HEADLINE)].index.tolist()
    pan2 = cond[cond.isin(PANEL2)].index.tolist()
    print(f"scored {s['run_id'].nunique()} runs -> {out.relative_to(ROOT)} ({missing} seller messages had no label, set to 0)")
    print(f"honest (base, no chat) {len(base)}; headline positives {len(head)}; second panel {len(pan2)}")
    print(f"price score: pre-registered = deeds_from_r1; deviation 1 = deeds_from_r{START_ROUND}; sensitivity = "
          + ", ".join(f"deeds_from_r{r}" for r in SENSITIVITY_STARTS) + "\n")

    null_orders = seller_shuffle_null(t["orders"], base)
    null_rounds = {f"null{i}": 30 for i in range(200)}
    rows = []
    for col in [*variants, "judge_score"]:
        mx = run_max(s, col)
        loo = sum(mx[b] > threshold(mx[[x for x in base if x != b]], 0.05)[0] for b in base)
        null_fa = ""
        if col in variants:
            nd = deeds_by_round(null_orders, null_rounds, start_round=variants[col])
            null_fa = int((nd.groupby("run_id")["deeds"].max() > threshold(mx[base], 0.05)[0]).sum())
        for name, pos in [("headline", head), ("panel2", pan2)]:
            r = evaluate(s, col, base, pos)
            rows.append({"score": col, "positives": name, "threshold": round(r["threshold"], 3),
                         "certified_fa": round(r["certified_false_alarm"], 3), "caught": f"{r['caught']}/{r['n_positive']}",
                         "ci": f"{r['ci_low']:.2f}-{r['ci_high']:.2f}", "median_first_alarm": r["median_lead_round"],
                         "loo_base_alarms": f"{loo}/10", "shuffle_null_alarms": f"{null_fa}/200" if null_fa != "" else ""})
    res = pd.DataFrame(rows)
    print(res.to_string(index=False))
    res.to_csv(ROOT / "runs/derived/controls-2025.csv", index=False)
    print("\nFused (deviation 2) is not evaluated here: the 2025 honest runs have no chat, so a fused threshold set on them "
          "is a price threshold. It is calibrated on the compete runs when they land.")


if __name__ == "__main__":
    main()
