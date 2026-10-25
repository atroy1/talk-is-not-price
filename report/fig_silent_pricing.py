"""Illustration DRAFT: the silent-pricing run a chat monitor cannot see (one run; an illustration, not a rate).

Sprint work, Fri Oct 23 2026 (Arty: report the single silent-pricing run as an illustration). Opus 5.5 sellers with the
neutral sentence, 20 rounds, Haiku buyers: no seller messages, asks held together high. Compared with honest Haiku
markets over the same rounds.
    .venv/bin/python report/fig_silent_pricing.py   -> report/draft/fig_silent_pricing.png
"""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
plt.style.use(HERE / "figstyle.mplstyle")
FINAL = bool(os.environ.get("FINAL"))  # FINAL=1: print files, no DRAFT tag, 300 dpi
OUT = HERE / ("final/figures" if FINAL else "draft")
OUT.mkdir(parents=True, exist_ok=True)
from analysis.load_runs import load_live  # noqa: E402

RUN = "xm20-opus55-neutral-1"


def main():
    t = load_live(["xm20-opus55-neutral", "haiku55-explicit", "haiku55-base"])
    runs = t["runs"].set_index("run_id")["condition"]
    a = t["orders"]
    a = a[(a.side == "ask") & (a["round"] <= 20)].copy()
    a["cond"] = a.run_id.map(runs)
    fig, ax = plt.subplots(figsize=(3.15, 2.3))
    for cond, color, lab in [("haiku55-explicit", "#5b9bd5", "honest Haiku, told it is illegal ({n} runs)"),
                             ("haiku55-base", "#b0b0b0", "honest Haiku, no chat ({n} runs)")]:
        per = a[a.cond == cond].groupby(["run_id", "round"]).price.mean().unstack(0)
        ax.fill_between(per.index, per.min(axis=1), per.max(axis=1), color=color, alpha=0.6, linewidth=0, label=lab.format(n=per.shape[1]))
    thr = pd.read_csv(ROOT / "runs/derived/detect-results-explicit.csv")
    bar = 90 + 10 * float(thr[(thr["set"] == "Haiku chat") & (thr.detector == "deeds")].threshold.iloc[0])
    ax.axhline(bar, color="#555555", linewidth=0.6, linestyle=(0, (1, 2)))
    ax.text(20.2, bar, f"price screen bar ${bar:.2f}", fontsize=5.5, color="#555555", va="center")
    r = a[a.run_id == RUN].groupby("round").price
    ax.fill_between(r.mean().index, r.min(), r.max(), color="#D55E00", alpha=0.25, linewidth=0)
    ax.plot(r.mean().index, r.mean(), color="#D55E00", linewidth=1.5, label="Opus 5.5, neutral sentence (1 run)")
    tr = t["trades"]
    n_tr, p_tr = int((tr.run_id == RUN).sum()), tr[tr.run_id == RUN].price.mean()
    ax.text(10.5, 97.6, f"0 messages sent; {n_tr} trades\nat ${p_tr:.2f} on average", fontsize=6.5, color="#9a3b00", ha="center")
    ax.axhline(90, color="#999999", linewidth=0.6, linestyle=(0, (3, 2)))
    ax.text(20.2, 90, "$90", fontsize=6.5, color="#777777", va="center")
    ax.set_xlim(1, 20); ax.set_ylim(84, 99)
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.set_xlabel("round", fontsize=7); ax.set_ylabel("sellers' asks ($)", fontsize=7)
    ax.tick_params(labelsize=6.5)
    ax.legend(fontsize=5.8, frameon=False, loc="lower left")
    if not FINAL:
        ax.text(1.0, 1.02, "DRAFT: one run, an illustration", transform=ax.transAxes, ha="right", va="bottom", fontsize=6, color="#b00020")
    fig.savefig(OUT / "fig_silent_pricing.png", dpi=(300 if FINAL else 200), bbox_inches="tight")
    print("wrote", (OUT / "fig_silent_pricing.png").relative_to(ROOT))


if __name__ == "__main__":
    main()
