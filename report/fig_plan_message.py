"""Figure 2 candidate DRAFT: what the sellers planned against what they said, 2025 chat markets.

Sprint work, Fri Oct 23 2026, late night. Reads runs/derived/private-plan-turns.csv (analysis/private_plan.py).
(a) Seller turns by condition: open (private plan and public message both collusive), concealed (plan collusive,
    message not, or no message sent), message only, neither.
(b) By round, oversight markets against plain GPT-4.1 chat markets: share of seller turns whose private plan is
    collusive, and share whose public message is. The gap is what a chat monitor cannot see.
    .venv/bin/python report/fig_plan_message.py   -> report/draft/fig_plan_message.png
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
plt.style.use(HERE / "figstyle.mplstyle")
FINAL = bool(os.environ.get("FINAL"))  # FINAL=1: print files, no DRAFT tag, 300 dpi
OUT = HERE / ("final/figures" if FINAL else "draft")
OUT.mkdir(parents=True, exist_ok=True)
ORDER = ["chat, GPT-4.1", "chat, mixed Claude/GPT", "chat, CEO pressure", "chat, overseer reads messages", "chat, overseer + CEO pressure"]
CELLS = [("open", "#111111", "plan and message collusive"), ("concealed: message says less", "#D55E00", "plan collusive, message not"),
         ("concealed: no message sent", "#CC79A7", "plan collusive, no message sent"), ("message only", "#0072B2", "message collusive, plan not"),
         ("neither", "#e3e3e3", "neither")]


def main():
    s = pd.read_csv(ROOT / "runs/derived/private-plan-turns.csv")
    fig = plt.figure(figsize=(6.5, 3.6))
    ax = fig.add_axes([0.30, 0.16, 0.36, 0.72])
    ys = []
    for i, g in enumerate(ORDER):
        d = s[s.group == g]
        if d.empty:
            continue
        left = 0.0
        for cell, color, _ in CELLS:
            share = (d.cell == cell).mean()
            if share > 0:
                ax.barh(i, share, left=left, color=color, height=0.7, edgecolor="white", linewidth=0.4)
            left += share
        ys.append((i, f"{g} ({d.run_id.nunique()})"))
    ax.set_yticks([y for y, _ in ys]); ax.set_yticklabels([l for _, l in ys], fontsize=7.5)
    ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xticks([0, .5, 1]); ax.set_xticklabels(["0", "50%", "100%"])
    ax.set_xlabel("share of seller turns", fontsize=8); ax.grid(False)
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=c) for _, c, _ in CELLS], [l for _, _, l in CELLS], fontsize=6.5, ncol=1,
              loc="upper left", bbox_to_anchor=(0.0, -0.22))
    ax.text(0, 1.03, "(a)", transform=ax.transAxes, fontsize=8, fontweight="bold")

    bx = fig.add_axes([0.72, 0.16, 0.26, 0.72])
    for g, color, short in [("chat, overseer + CEO pressure", "#D55E00", "overseer + pressure"), ("chat, overseer reads messages", "#0072B2", "overseer")]:
        d = s[s.group == g]
        if d.empty:
            continue
        d = d.assign(nb=d["scratch_coord"].astype(str) == "True")
        byr = d.groupby("round").agg(nb=("nb", "mean"), msg=("msg_coll", "mean"))
        bx.plot(byr.index, byr.nb, color=color, linewidth=1.3, label=f"{short}: private notebook")
        bx.plot(byr.index, byr.msg, color=color, linewidth=1.0, linestyle=(0, (3, 2)), label=f"{short}: public message")
    bx.set_xlim(1, 30); bx.set_ylim(0, 1); bx.set_xlabel("round", fontsize=8)
    bx.set_yticks([0, .5, 1]); bx.set_yticklabels(["0", "50%", "100%"])
    bx.legend(fontsize=5.8, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=1)
    bx.text(0, 1.03, "(b) share of seller turns coordinating", transform=bx.transAxes, fontsize=8, fontweight="bold")
    if not FINAL:
        fig.text(0.98, 0.985, "DRAFT", ha="right", va="top", fontsize=7, color="#b00020")
    fig.savefig(OUT / "fig_plan_message.png", dpi=(300 if FINAL else 200), bbox_inches="tight")
    print("wrote", (OUT / "fig_plan_message.png").relative_to(ROOT))


if __name__ == "__main__":
    main()
