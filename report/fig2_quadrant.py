"""Figure 2 DRAFT: the words-and-deeds quadrant on real runs (2025 data now; new runs added as they land).

Sprint work, Fri Oct 23 2026. Same size, fonts and palette as the layout proof (report/fig_proof.py).
    .venv/bin/python report/fig2_quadrant.py   -> report/draft/fig2_quadrant_draft.png

x = price lift late in the game: mean ask over rounds 6-30 (declared deviation 1), minus the $90 competitive price,
    in dollars. y = share of seller messages proposing or agreeing to a common price, over the whole game.
One dot per run. Exploratory figure (pre-registration: the quadrant is descriptive, not a test).
"""
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
OUT = HERE / "draft"
OUT.mkdir(exist_ok=True)

GROUPS = {  # condition -> (legend label, colour); semantic, never cycled
    "base": ("no chat (honest)", "#777777"),
    "headline": ("chat, collusion possible", "#0072B2"),
    "panel2": ("chat + oversight or CEO pressure", "#D55E00"),
}
HEADLINE = ["base-seller_comms", "claude_buyers-claude_sellers-seller_comms", "claude_buyers-gpt_sellers-seller_comms",
            "claude_buyers-mixed_sellers-seller_comms", "gpt_buyers-claude_sellers-seller_comms",
            "gpt_buyers-mixed_sellers-seller_comms"]


def main():
    s = pd.read_csv(ROOT / "runs/derived/scores-2025.csv")
    late = s[s["round"] >= 6].groupby("run_id").agg(cond=("condition", "first"), ask=("mean_ask", "mean"))
    words = s.sort_values("round").groupby("run_id")["words"].last()
    d = late.join(words)
    d["x"] = d["ask"] - 90.0
    d["group"] = d["cond"].map(lambda c: "base" if c == "base" else ("headline" if c in HEADLINE else "panel2"))

    fig, ax = plt.subplots(figsize=(3.15, 3.0))
    ax.axvline(0, color="#bbbbbb", linewidth=0.6)
    ax.axhline(0.5, color="#bbbbbb", linewidth=0.6)
    for g, (lab, c) in GROUPS.items():
        q = d[d["group"] == g]
        ax.scatter(q["x"], q["words"], s=14, color=c, edgecolor="white", linewidth=0.5, label=f"{lab} ({len(q)})", zorder=3)
    tacit = d[(d["group"] == "base")].sort_values("x").iloc[-1]
    ax.annotate("no chat, all five\nsellers at $95.33", (tacit["x"], tacit["words"]), xytext=(-4, 22),
                textcoords="offset points", fontsize=6.5, color="#555555", ha="right",
                arrowprops=dict(arrowstyle="-", color="#999999", linewidth=0.5))
    for (x, y, txt, va) in [(-5.8, 0.53, "collusion on paper", "bottom"), (0.3, 0.53, "explicit cartel", "bottom"),
                            (-5.8, 0.47, "competitive", "top"), (0.3, 0.47, "tacit collusion", "top")]:
        ax.text(x, y, txt, fontsize=7, color="#333333", va=va, style="italic")
    ax.set_xlim(-6, 8); ax.set_ylim(0, 1)
    ax.set_xlabel("late-game ask above the $90 competitive price")
    ax.set_ylabel("share of seller messages\nproposing or agreeing a floor")
    ax.set_xticks([-5, 0, 5]); ax.set_xticklabels(["-$5", "$0", "+$5"])
    ax.legend(loc="upper left", bbox_to_anchor=(-0.02, -0.2), ncol=1, handletextpad=0.3, fontsize=7)
    ax.grid(False)
    ax.text(1.0, 1.02, "DRAFT: 2025 runs only", transform=ax.transAxes, ha="right", va="bottom", fontsize=7, color="#b00020")
    fig.savefig(OUT / "fig2_quadrant_draft.png", bbox_inches="tight")
    counts = d.assign(hi_w=d["words"] >= 0.5, hi_p=d["x"] > 0).groupby(["group", "hi_w", "hi_p"]).size()
    print("runs per quadrant (words >= 0.5, ask above $90):")
    print(counts.to_string())
    print("wrote", (OUT / "fig2_quadrant_draft.png").relative_to(ROOT))


if __name__ == "__main__":
    main()
