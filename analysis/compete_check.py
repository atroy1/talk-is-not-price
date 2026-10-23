"""G3 price check: may the Haiku compete runs join the honest price reference? (docs/METHODS-NOTES.md section 2)

Sprint work, Fri Oct 23 2026. Rule fixed in notes/log.md before any compete price was read:
the compete runs join the price reference only if (a) their median late-window mean ask is within $1.00 of the
Haiku base runs' median and (b) a two-sided Mann-Whitney test of the two sets of run-level late asks does not
reject at 0.05. Late window = rounds 6 to 30 (the round-6 start of declared deviation 1). Otherwise prices are
calibrated on the base runs alone and the compete runs serve the chat channel only.

    .venv/bin/python -m analysis.compete_check
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scipy.stats import mannwhitneyu  # noqa: E402

from analysis.load_runs import load_live  # noqa: E402
from analysis.scores import START_ROUND  # noqa: E402

GAP = 1.00
ALPHA = 0.05


def late_asks(t, condition):
    o = t["orders"]
    runs = t["runs"]
    ids = runs.loc[runs["condition"] == condition, "run_id"]
    a = o[(o["side"] == "ask") & (o["round"] >= START_ROUND) & o["run_id"].isin(ids)].dropna(subset=["price"])
    return a.groupby("run_id")["price"].mean()


def main():
    t = load_live(["haiku55-base", "haiku55-compete"])
    base, comp = late_asks(t, "haiku55-base"), late_asks(t, "haiku55-compete")
    print(f"Haiku base runs {len(base)}, compete runs {len(comp)} (late window rounds {START_ROUND}-30)")
    if len(base) < 3 or len(comp) < 3:
        sys.exit("too few finished runs to apply the rule yet")
    gap = comp.median() - base.median()
    p = mannwhitneyu(comp, base, alternative="two-sided").pvalue
    join = abs(gap) <= GAP and p >= ALPHA
    print(f"median late ask: base ${base.median():.2f}, compete ${comp.median():.2f}, gap ${gap:+.2f} (rule: within ${GAP:.2f})")
    print(f"Mann-Whitney p = {p:.3f} (rule: not below {ALPHA})")
    print("DECISION: compete runs JOIN the price reference" if join else
          "DECISION: prices calibrated on the base runs alone; compete runs serve the chat channel only")
    if len(comp) < 20:
        print(f"provisional: {len(comp)} of 20 compete runs finished; rerun when all have landed")


if __name__ == "__main__":
    main()
