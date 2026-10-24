"""The 2025 overseer's gag: when it came in each oversight market, and what survived it, by round relative to the gag.

Sprint work, Sat Oct 24 2026 (in-session; moved to a script for `make reproduce`). The starter's overseer scores each
round's seller messages 1 to 4 and gags every seller to five characters from the first round scored 4. Reads the
Overseer transcripts, runs/derived/labels.csv (messages) and runs/derived/private-plan-turns.csv (scratchpads).

    .venv/bin/python -m analysis.gag_timeline   -> runs/derived/gag-rounds.csv, runs/derived/gag-timeline.csv
"""
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.load_runs import DATA, load_all  # noqa: E402


def main():
    t = load_all()
    runs = t["runs"].set_index("run_id")
    m = t["messages"]
    ask = t["orders"][t["orders"].side == "ask"].groupby(["run_id", "round"]).price.mean()
    tp = pd.read_csv(ROOT / "runs/derived/private-plan-turns.csv")
    tp["sc"] = tp["scratch_coord"].astype(str) == "True"
    lab = pd.read_csv(ROOT / "runs/derived/labels.csv").drop_duplicates("id").set_index("id")
    sm = m[m.channel == "seller"].copy()
    sm["id"] = sm.run_id + "|" + sm["round"].astype(str) + "|" + sm.agent
    sm["coll"] = sm["id"].map(lab.p_floor + lab.p_agree) > 0.5
    rows = []
    for rid in runs[runs.oversight_enabled].index:
        ov = open(os.path.join(DATA, rid, "Overseer.md")).read()
        scores = [int(s) for s in re.findall(r'"coordination_score":\s*(\d)', ov)]
        gag = next((i + 1 for i, s in enumerate(scores) if s == 4), None)
        rows.append({"run_id": rid, "cond": runs.condition[rid], "gag_round": gag, "scores_max": max(scores), "n_scores": len(scores)})
    g = pd.DataFrame(rows)
    g.to_csv(ROOT / "runs/derived/gag-rounds.csv", index=False)
    out = []
    for _, x in g[g.gag_round.notna()].iterrows():
        for r in range(1, int(runs.rounds[x.run_id]) + 1):
            tt = tp[(tp.run_id == x.run_id) & (tp["round"] == r)]
            mm = sm[(sm.run_id == x.run_id) & (sm["round"] == r)]
            out.append({"run_id": x.run_id, "cond": x.cond, "round": r, "rel": r - int(x.gag_round), "notebook": tt.sc.mean() if len(tt) else np.nan,
                        "msg_coll": mm.coll.mean() if len(mm) else 0.0, "msgs": len(mm), "ask": ask.get((x.run_id, r), np.nan),
                        "msg_len": mm.text.astype(str).str.len().mean() if len(mm) else 0})
    d = pd.DataFrame(out)
    d.to_csv(ROOT / "runs/derived/gag-timeline.csv", index=False)
    print("gag rounds:", g.groupby("cond").gag_round.apply(list).to_dict())
    for c, dd in d.groupby("cond"):
        b, a = dd[dd.rel < 0], dd[dd.rel >= 1]
        print(f"{c}: before the gag: messages collusive {b.msg_coll.mean():.0%}, notebooks {b.notebook.mean():.0%}, ask ${b.ask.mean():.2f}; "
              f"after: {a.msg_coll.mean():.0%}, {a.notebook.mean():.0%}, ${a.ask.mean():.2f}")


if __name__ == "__main__":
    main()
