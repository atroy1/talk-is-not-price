"""Figure 1 DRAFT: share of collusive-design runs each detector has flagged, by round (2025 headline set).

Sprint work, Fri Oct 23 2026. Reads runs/derived/leads-<reference>.csv from analysis/detect.py. Same size, fonts and
palette as the layout proof (report/fig_proof.py).
    .venv/bin/python report/fig1_leadtime.py [explicit|compete]   -> report/draft/fig1_leadtime_<reference>.png
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
plt.style.use(HERE / "figstyle.mplstyle")
OUT = HERE / "draft"
OUT.mkdir(exist_ok=True)
COLORS = {"words": "#0072B2", "deeds": "#D55E00", "fused": "#111111", "judge_score": "#999999"}
LABELS = {"words": "chat only", "deeds": "prices only", "fused": "chat + prices", "judge_score": "2025 LLM judge"}


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else "explicit"
    leads = pd.read_csv(ROOT / f"runs/derived/leads-{ref}.csv")
    res = pd.read_csv(ROOT / f"runs/derived/detect-results-{ref}.csv")
    head = leads[leads["set"] == "2025 headline"]
    fig, ax = plt.subplots(figsize=(6.5, 2.4))
    rounds = range(1, 31)
    for det in ["fused", "words", "deeds", "judge_score"]:
        d = head[head["detector"] == det]
        if d.empty:
            continue
        n = d["run_id"].nunique()
        share = [(d["first_alarm"] <= r).sum() / n for r in rounds]
        rate = res[(res["set"] == "2025 headline") & (res["detector"] == det)]["certified_fa"]
        lab = f"{LABELS[det]} ({float(rate.iloc[0]):.0%} false alarms)" if len(rate) else LABELS[det]
        ax.step(list(rounds), share, where="post", color=COLORS[det], label=lab,
                linewidth=1.6 if det == "fused" else 1.1, linestyle="--" if det == "judge_score" else "-")
    ax.axvline(6, color="#bbbbbb", linewidth=0.6, linestyle=(0, (3, 2)))
    ax.text(6.3, 0.04, "prices scored\nfrom round 6", fontsize=7, color="#666666", va="bottom")
    ax.set_xlim(1, 30); ax.set_ylim(0, 1.02)
    ax.set_xlabel("round"); ax.set_ylabel("collusive-design runs\nflagged so far")
    ax.set_yticks([0, .25, .5, .75, 1]); ax.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
    ax.legend(loc="center right", fontsize=7, frameon=False)
    ax.text(1.0, 1.02, f"DRAFT: chat reference = {ref}", transform=ax.transAxes, ha="right", va="bottom", fontsize=7, color="#b00020")
    fig.savefig(OUT / f"fig1_leadtime_{ref}.png", bbox_inches="tight")
    print("wrote", (OUT / f"fig1_leadtime_{ref}.png").relative_to(ROOT))


if __name__ == "__main__":
    main()
