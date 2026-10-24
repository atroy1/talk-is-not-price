"""A chat monitor with no language model: four regex patterns in place of the labeller, same threshold rule.

Sprint work, Sat Oct 24 2026 (in-session Friday night; a script for `make reproduce`). A message counts as
coordination talk if it matches the floor, no-undercut, joint-move or agreement pattern of analysis/message_taxonomy.py.
The score is the running share of such messages; the threshold is the detector's rule on the 20 honest Haiku markets
told the conduct is illegal, leave-one-out for reference runs. Sensitivity row for the report: is the catch the
labeller's doing, or the sellers' plain words?

    .venv/bin/python -m analysis.keyword_rule   -> runs/derived/keyword-rule.csv
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.controls import HEADLINE, PANEL2  # noqa: E402
from analysis.detector import threshold  # noqa: E402
from analysis.load_runs import load_all, load_live  # noqa: E402
from analysis.message_taxonomy import TAGS  # noqa: E402

PATTERN = re.compile("|".join(f"(?:{TAGS[k]})" for k in ("floor", "no_undercut", "joint_move", "agreement")), re.I)
GROUPS = [("2025 headline", lambda c: c in HEADLINE, False), ("2025 panel 2", lambda c: c in PANEL2, False),
          ("Haiku chat", lambda c: c == "haiku55-seller_comms", False), ("Haiku, set your ask independently", lambda c: c == "haiku55-compete", False),
          ("DeepSeek chat", lambda c: c == "dsflash-seller_comms", False), ("Luna chat", lambda c: c == "luna-seller_comms", False),
          ("Qwen chat", lambda c: c.startswith(("qwen35b-stock-chat", "qwen35b-abl-chat")), False),
          ("honest: Haiku told it is illegal (reference, LOO)", lambda c: c == "haiku55-explicit", True),
          ("honest: +$6 shock", lambda c: c == "haiku55-costshock-explicit", True), ("honest: +$12 shock", lambda c: c == "haiku55-costshock12-explicit", True),
          ("honest: Sonnet and Opus illegal or no price talk (20 r)", lambda c: c.startswith("xm20") and ("notalk" in c or "explicit" in c), True),
          ("Haiku, do not discuss prices", lambda c: c == "haiku55-pilot-notalk", True), ("Qwen told it is illegal", lambda c: c.startswith("qwen35b-stock-explicit"), True)]


def main():
    old, new = load_all(), load_live()
    runs = pd.concat([old["runs"], new["runs"]], ignore_index=True).set_index("run_id")["condition"]
    m = pd.concat([old["messages"], new["messages"]], ignore_index=True)
    m = m[(m.channel == "seller") & m.text.notna() & (m.text.astype(str).str.strip() != "")].copy()
    m["kw"] = m.text.astype(str).str.contains(PATTERN)

    def run_max(d):
        d = d.sort_values("round")
        return (d.kw.cumsum() / np.arange(1, len(d) + 1)).max()

    mx = m.groupby("run_id").apply(run_max, include_groups=False)
    cond = runs.reindex(mx.index)
    ref = mx[cond == "haiku55-explicit"]
    rows = []
    for name, test, honest in GROUPS:
        ids = cond[cond.map(lambda c: bool(test(str(c))))].index
        if not len(ids):
            continue
        caught = sum(mx[r] > threshold(ref.drop(r, errors="ignore").tolist())[0] for r in ids)
        rows.append({"group": name, "honest_by_design": honest, "n": len(ids), "flagged": int(caught), "median_max_share": round(float(mx[ids].median()), 3)})
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "runs/derived/keyword-rule.csv", index=False)
    thr, rate, k = threshold(ref.tolist())
    print(f"keyword rule, threshold {thr:.3f} on {len(ref)} honest markets (k = {k}, certified {rate:.1%})")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
