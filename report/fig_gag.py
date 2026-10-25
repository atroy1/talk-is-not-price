"""Appendix figure DRAFT: the 2025 overseer's gag, and what survived it (rounds relative to the gag).

Sprint work, Sat Oct 24 2026. Reads runs/derived/gag-timeline.csv (written in-session from the Overseer transcripts,
labels and scratchpad labels). The starter's overseer gags every seller to five characters from the first round it
scores coordination 4 of 4; all 20 oversight markets were gagged between rounds 1 and 7.
    .venv/bin/python report/fig_gag.py   -> report/draft/fig_gag.png
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
CONDS = [("oversight", "#0072B2", "overseer only (10 markets)"), ("boss_pressure-oversight", "#D55E00", "overseer + CEO pressure (10 markets)")]


def main():
    d = pd.read_csv(ROOT / "runs/derived/gag-timeline.csv")
    d = d[(d.rel >= -4) & (d.rel <= 20)]
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.0))
    for ax, (col, lab, fmt) in zip(axes, [("msg_coll", "messages labelled collusive", "{:.0%}"), ("notebook", "private notebooks that coordinate", "{:.0%}"),
                                           ("ask", "mean ask, dollars", "${:.0f}")]):
        for cond, color, name in CONDS:
            g = d[d.cond == cond].groupby("rel")[col].mean()
            ax.plot(g.index, g.values, color=color, linewidth=1.3, label=name)
        ax.axvline(0, color="#999999", linewidth=0.7, linestyle=(0, (3, 2)))
        ax.set_title(lab, fontsize=7.5, loc="left")
        ax.set_xlabel("rounds after the gag", fontsize=7); ax.tick_params(labelsize=6.5); ax.grid(False)
        if col != "ask":
            ax.set_ylim(0, 1); ax.set_yticks([0, .5, 1]); ax.set_yticklabels(["0", "50%", "100%"])
        else:
            ax.set_ylim(86, 98); ax.axhline(90, color="#bbbbbb", linewidth=0.5)
    axes[0].text(0.3, 0.9, "gag", fontsize=6.5, color="#666666", transform=axes[0].get_xaxis_transform(), ha="left")
    axes[0].legend(fontsize=6, loc="center right")
    if not FINAL:
        fig.text(0.99, 0.99, "DRAFT", ha="right", va="top", fontsize=7, color="#b00020")
    fig.tight_layout()
    fig.savefig(OUT / "fig_gag.png", dpi=(300 if FINAL else 200), bbox_inches="tight")
    print("wrote", (OUT / "fig_gag.png").relative_to(ROOT))


if __name__ == "__main__":
    main()
