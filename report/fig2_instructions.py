"""Figure 2 DRAFT: what two instruction sentences do to talk and price, by model (small multiples).

Sprint work, Sat Oct 24 2026. Columns: seller model. Rows of each panel: the instruction (none, "set your ask
independently", "... coordinating prices is illegal", "do not discuss prices"). Bar = share of seller messages labelled
collusive (P above 0.5); dot = mean ask from round 6 on, in dollars (right axis); "silent" where no seller sent a
message. Claude models from the 20-round sample (2 markets a cell) plus the 30-round Haiku sets where they exist;
Qwen3.5 35B from the 30-round arm (ZIP buyers, so its prices are not comparable and are drawn hollow).
    .venv/bin/python report/fig2_instructions.py   -> report/draft/fig2_instructions.png
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
from analysis.load_runs import load_live  # noqa: E402

MODELS = [("Claude Haiku 5.5", {"none": ["haiku55-seller_comms"], "independent": ["haiku55-compete", "xm20-haiku55-neutral"],
                                "illegal": ["haiku55-explicit", "xm20-haiku55-explicit"], "no price talk": ["haiku55-pilot-notalk", "xm20-haiku55-notalk"]}),
          ("Claude Sonnet 5.5", {"independent": ["xm20-sonnet55-neutral"], "illegal": ["xm20-sonnet55-explicit"], "no price talk": ["xm20-sonnet55-notalk"]}),
          ("Claude Opus 5.5", {"independent": ["xm20-opus55-neutral"], "illegal": ["xm20-opus55-explicit"], "no price talk": ["xm20-opus55-notalk"]}),
          ("Qwen3.5 35B (ZIP buyers)", {"none": ["qwen35b-stock-chat"], "independent": ["qwen35b-stock-compete"], "illegal": ["qwen35b-stock-explicit"]})]
ROWS = ["none", "independent", "illegal", "no price talk"]
ROWLAB = {"none": "no instruction", "independent": "\"set your ask\nindependently\"", "illegal": "+ \"coordinating prices\nis illegal\"", "no price talk": "\"do not discuss\nprices\""}


def main():
    t = load_live()
    runs = t["runs"].set_index("run_id")["condition"]
    m = t["messages"]; m = m[(m.channel == "seller") & m.text.notna() & (m.text.astype(str).str.strip() != "")].copy()
    lab = pd.read_csv(ROOT / "runs/derived/labels.csv").drop_duplicates("id").set_index("id")
    m["id"] = m.run_id + "|" + m["round"].astype(str) + "|" + m.agent
    m["coll"] = (m.id.map(lab.p_floor + lab.p_agree) > 0.5)
    a = t["orders"]; a = a[(a.side == "ask") & (a["round"] >= 6)]
    fig, axes = plt.subplots(1, len(MODELS), figsize=(6.5, 2.6), sharey=True)
    for ax, (name, cells) in zip(axes, MODELS):
        ax2 = ax.twiny()  # a second x axis (dollars) on the same rows
        for i, row in enumerate(ROWS):
            conds = cells.get(row)
            if not conds:
                ax.text(0.5, i, "not run", ha="center", va="center", fontsize=6.5, color="#aaaaaa")
                continue
            ids = runs[runs.map(lambda c: any(str(c) == x or str(c).startswith(x + "-") for x in conds))].index  # Qwen tags keep their -sN seed
            mm = m[m.run_id.isin(ids)]
            share = mm.coll.mean() if len(mm) else 0.0
            ask = a[a.run_id.isin(ids)].price.mean()
            if len(mm) == 0:
                ax.text(0.02, i, "silent", ha="left", va="center", fontsize=6.5, color="#555555", style="italic")
            elif share == 0:
                ax.text(0.02, i, "talks, 0%", ha="left", va="center", fontsize=6.5, color="#0072B2", style="italic")
            else:
                ax.barh(i, share, color="#0072B2", height=0.6)
            hollow = "Qwen" in name
            ax2.plot([ask], [i], marker="o", markersize=5, color="#D55E00", markerfacecolor="none" if hollow else "#D55E00", linewidth=0)
            ax.text(1.02, i, f"{len(ids)}", ha="left", va="center", fontsize=6, color="#777777", transform=ax.get_yaxis_transform())
        ax.set_xlim(0, 1); ax.set_xticks([0, .5, 1]); ax.set_xticklabels(["0", "50%", "100%"], fontsize=6.5)
        ax.set_yticks(range(len(ROWS))); ax.set_yticklabels([ROWLAB[r] for r in ROWS], fontsize=6.5)
        ax.invert_yaxis(); ax.set_title(name, fontsize=7.5, loc="center"); ax.grid(False)
        ax2.set_xlim(78, 98); ax2.axvline(90, color="#D55E00", linewidth=0.5, linestyle=(0, (3, 2)), alpha=0.6)
        ax2.tick_params(axis="x", labelsize=6.5, colors="#D55E00"); ax2.set_xticks([80, 90, 97]); ax2.grid(False)
        ax2.spines["top"].set_visible(True); ax2.spines["top"].set_color("#D55E00"); ax2.spines["right"].set_visible(False)
    axes[0].set_xlabel("share of messages collusive (bars)", fontsize=6.5)
    fig.text(0.5, 1.02, "mean ask from round 6, dollars (dots, top axis); n markets at right", ha="center", fontsize=6.5, color="#D55E00")
    fig.text(0.99, -0.02, "DRAFT: Claude cells are 20-round samples plus 30-round sets where they exist; Qwen prices face ZIP buyers (hollow)",
             ha="right", fontsize=6, color="#b00020")
    fig.savefig(OUT / "fig2_instructions.png", dpi=200, bbox_inches="tight")
    print("wrote", (OUT / "fig2_instructions.png").relative_to(ROOT))


if __name__ == "__main__":
    main()
