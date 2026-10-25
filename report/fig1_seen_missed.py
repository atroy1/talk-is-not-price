"""Figure 1 DRAFT: what a chat monitor sees and misses (a), with lead time as the supporting panel (b).

Sprint work, Fri Oct 23 2026, for the post-results headline. Reads runs/derived/flags.csv (analysis/flag_matrix.py) and
runs/derived/leads-explicit.csv (analysis/detect.py). Palette as in the layout proof (report/fig_proof.py).
    .venv/bin/python report/fig1_seen_missed.py   -> report/draft/fig1_seen_missed.png
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
CELLS = [("chat only", "#0072B2"), ("both", "#111111"), ("prices only", "#D55E00"), ("neither", "#e3e3e3")]
WORDS, DEEDS, FUSED, JUDGE = "#0072B2", "#D55E00", "#111111", "#999999"


def main():
    flags = pd.read_csv(ROOT / "runs/derived/flags.csv")
    flags["cell"] = "neither"
    flags.loc[flags.chat & flags.prices, "cell"] = "both"
    flags.loc[flags.chat & ~flags.prices, "cell"] = "chat only"
    flags.loc[~flags.chat & flags.prices, "cell"] = "prices only"
    order = list(dict.fromkeys(zip(flags.section, flags.group)))
    fig = plt.figure(figsize=(6.5, 4.6))
    ax = fig.add_axes([0.42, 0.36, 0.55, 0.6])
    y, ys, labels, last = 0, [], [], None
    for section, group in order:
        if section != last and last is not None:
            y += 0.6
        if section != last:
            ax.text(-0.02, y - 0.75, section, transform=ax.get_yaxis_transform(), ha="right", va="center",
                    fontsize=7.5, fontweight="bold", color="#333333")
            y += 0.55
        last = section
        g = flags[(flags.section == section) & (flags.group == group)]
        left = 0.0
        for cell, color in CELLS:
            share = (g.cell == cell).mean()
            if share > 0:
                ax.barh(y, share, left=left, color=color, height=0.72, edgecolor="white", linewidth=0.4)
            left += share
        ys.append(y)
        labels.append(f"{group.strip()} ({len(g)})")
        y += 1
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xticks([0, .5, 1]); ax.set_xticklabels(["0", "50%", "100%"], fontsize=7)
    ax.set_xlabel("share of runs flagged", fontsize=7.5)
    ax.grid(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, c in CELLS]
    ax.legend(handles, ["chat only", "chat and prices", "prices only", "neither"], ncol=4, fontsize=7, frameon=False,
              loc="lower left", bbox_to_anchor=(-0.02, 1.0))
    ax.text(0, -0.13, "(a)", transform=ax.transAxes, fontsize=8, fontweight="bold")

    leads = pd.read_csv(ROOT / "runs/derived/leads-explicit.csv")
    head = leads[leads["set"] == "2025 headline"]
    bx = fig.add_axes([0.42, 0.07, 0.55, 0.17])
    for det, color, lab, style in [("fused_hard", FUSED, "chat + prices", "-"), ("words_hard", WORDS, "chat", "-"),
                                   ("deeds", DEEDS, "prices", "-"), ("judge_score", JUDGE, "2025 LLM judge", "--")]:
        d = head[head["detector"] == det]
        if d.empty:
            continue
        n = d["run_id"].nunique()
        bx.step(range(1, 31), [(d["first_alarm"] <= r).sum() / n for r in range(1, 31)], where="post",
                color=color, linestyle=style, linewidth=1.4 if det == "fused_hard" else 1.0, label=lab)
    bx.axvline(6, color="#bbbbbb", linewidth=0.6, linestyle=(0, (3, 2)))
    bx.set_xlim(1, 30); bx.set_ylim(0, 1.05)
    bx.set_yticks([0, 1]); bx.set_yticklabels(["0", "100%"], fontsize=7)
    bx.tick_params(axis="x", labelsize=7)
    bx.set_xlabel("round (2025 collusive-design runs; prices scored from round 6)", fontsize=7)
    bx.legend(fontsize=6.5, frameon=False, ncol=4, loc="lower right")
    bx.text(-0.02, 0.5, "(b) flagged by round", transform=bx.transAxes, ha="right", va="center", fontsize=7.5)
    if not FINAL:
        fig.text(0.97, 0.985, "DRAFT", ha="right", va="top", fontsize=7, color="#b00020")
    fig.savefig(OUT / "fig1_seen_missed.png", dpi=(300 if FINAL else 200))
    print("wrote", (OUT / "fig1_seen_missed.png").relative_to(ROOT))


if __name__ == "__main__":
    main()
