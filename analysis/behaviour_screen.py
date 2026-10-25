"""Behaviour statistics of the order book (undercutting, parked asks), by seller generation: a post hoc check.

Sprint work, Sun Oct 25 2026, after an internal second paper on the same data found that the price score in the report
(a level screen) is not the only price screen. Over rounds 6 to 20 of every market with at least 20 rounds: the share of
seller-rounds in which a seller asks below the previous round's lowest rival ask (undercut), and the share in which a
seller's ask is unchanged from its own previous ask within one cent (parked). AUROC of each, oriented the textbook
cartel way (less undercutting, more parking = more suspicious), for agreement markets (chat flag true) against honest
markets (chat flag false, honest design) of the same generation, with a 2,000-draw bootstrap interval; and the round
from which every seller's ask stays within $0.25 of its round-20 ask (settle round). Reads the recorded markets and
runs/derived/flags.csv; no API calls.

    .venv/bin/python -m analysis.behaviour_screen   -> runs/derived/behaviour-screen.csv, behaviour-screen.md
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.load_runs import load_all, load_live  # noqa: E402

D = ROOT / "runs/derived"
W0, W1 = 6, 20
RNG = np.random.default_rng(20261025)


def auroc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    return (pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean()


def boot(pos, neg, B=2000):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    v = [auroc(RNG.choice(pos, len(pos)), RNG.choice(neg, len(neg))) for _ in range(B)]
    return np.percentile(v, [2.5, 97.5])


def stats(A):
    """A: asks, rounds x sellers. Undercut and parked shares over the window, and the settle round."""
    full = A.loc[W0 - 1:W1]
    under = n_u = parked = n_p = 0
    for t in range(W0, W1 + 1):
        if t not in full.index or t - 1 not in full.index:
            continue
        prev, cur = full.loc[t - 1], full.loc[t]
        for s in full.columns:
            rivals = prev.drop(s).dropna()
            if pd.notna(cur[s]) and len(rivals):
                n_u += 1
                under += cur[s] < rivals.min() - 0.005
            if pd.notna(cur[s]) and pd.notna(prev[s]):
                n_p += 1
                parked += abs(cur[s] - prev[s]) < 0.01
    B = A.loc[1:20]
    ok = (B.sub(B.loc[20]).abs() <= 0.25).all(axis=1)
    settle = next((t for t in range(1, 21) if ok.loc[t:].all()), 21)
    return {"undercut": under / n_u if n_u else np.nan, "parked": parked / n_p if n_p else np.nan, "settle": settle}


def main():
    a, l = load_all(), load_live()
    runs = pd.concat([a["runs"], l["runs"]], ignore_index=True)
    orders = pd.concat([a["orders"], l["orders"]], ignore_index=True)
    asks = orders[orders.side == "ask"]
    f = pd.read_csv(D / "flags.csv").merge(runs[["run_id", "rounds"]], on="run_id", how="left")
    f = f[f.rounds >= W1].copy()
    honest = f.section.str.startswith("Honest")
    shock = f.group.str.contains("seller cost")
    f["cls"] = np.where(f.chat, "agreement", np.where(shock, "stress", np.where(honest, "honest", "silent")))
    rows = []
    for rid in f.run_id:
        A = asks[asks.run_id == rid].pivot_table(index="round", columns="agent", values="price", aggfunc="last")
        rows.append({"run_id": rid} | stats(A))
    S = f.merge(pd.DataFrame(rows), on="run_id")
    S["haiku"] = S.group.str.contains("Haiku")
    S.to_csv(D / "behaviour-screen.csv", index=False)

    L = ["Window rounds 6 to 20; markets with at least 20 rounds. AUROC oriented so that above 0.5 means agreement markets undercut less or park more than honest markets of the same generation; bootstrap 95% intervals, 2,000 draws. Post hoc (not pre-registered); the comparison is the report's own level screen in section 1.\n",
         "| Sellers | agreement n | honest n | undercut AUROC | parked AUROC |", "|---|---|---|---|---|"]
    for name, sel in [("2025 (GPT-4.1, Claude 3.x) against the 10 no-chat markets", S.era == 2025), ("2026, all families", S.era == 2026),
                      ("2026, Haiku 5.5 only", (S.era == 2026) & S.haiku)]:
        p, n = S[sel & (S.cls == "agreement")], S[sel & (S.cls == "honest")]
        cells = []
        for s, sign in (("undercut", -1), ("parked", 1)):
            au = auroc(sign * p[s], sign * n[s])
            lo, hi = boot(sign * p[s], sign * n[s])
            cells.append(f"{au:.2f} ({lo:.2f} to {hi:.2f})")
        L.append(f"| {name} | {len(p)} | {len(n)} | " + " | ".join(cells) + " |")
    L += ["", "Medians by generation and class, and the settle round (first round from which every seller's ask stays within $0.25 of its round-20 ask; 21 = never).", "",
          "| Sellers, class | n | undercut share | parked share | median settle round | settled by round 5 |", "|---|---|---|---|---|---|"]
    for era in (2025, 2026):
        for cls in ("honest", "agreement", "stress"):
            d = S[(S.era == era) & (S.cls == cls)]
            if d.empty:
                continue
            L.append(f"| {era}, {cls} | {len(d)} | {d.undercut.median():.0%} | {d.parked.median():.0%} | {d.settle.median():g} | {(d.settle <= 5).sum()} ({(d.settle <= 5).mean():.0%}) |")
    txt = "\n".join(L) + "\n"
    (D / "behaviour-screen.md").write_text(txt)
    print(txt)


if __name__ == "__main__":
    main()
