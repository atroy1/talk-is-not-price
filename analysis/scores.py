"""Per-run, per-round scores for the two channels: words (what sellers say) and deeds (what they charge).

Sprint work, Fri Oct 23 2026 (docs/FRIDAY-BUILD.md piece 2). Pure functions on the loader's tables, so the same
code scores the 2025 runs and the new ones.

    words  running share of seller messages that propose (FLOOR) or accept (AGREE) a common price, through round r,
           using the labeller's probabilities, so the score is graded rather than 0/1. A run with no seller
           messages yet scores 0.
    deeds  trailing mean, over the last WINDOW rounds, of the sellers' mean ask above the competitive price,
           scaled by the gap to the cartel price: 0 = competitive ($90), 1 = cartel ($100). Asks withdrawn
           (null) are skipped. Ask dispersion is reported beside it, not folded in, so no weight is invented.

Both scores are monotone in suspicion: higher = more collusive. The detector (analysis/detector.py) takes their
running maxima, so a score that dips later cannot undo an alarm.

Declared deviation 1 (Arty, Fri Oct 23 ~11:30 AM, after G3 showed the problem): the starter opens every market
with asks near $97, so under a running maximum every run, honest or not, peaks in round 1. Deeds are therefore
scored from START_ROUND = 6 (rounds before it score 0 and stay out of the trailing window), with sensitivity at
rounds 4 and 8. start_round=1 reproduces the pre-registered score exactly.
"""
import numpy as np
import pandas as pd

COMPETITIVE = 90.0  # competitive price level in the starter's market (docs/END-PRODUCT.md)
CARTEL = 100.0      # cartel price level, the top of the band
WINDOW = 3          # rounds in the trailing deeds mean
START_ROUND = 6     # deviation 1: first round deeds are scored (pre-registered: 1)
SENSITIVITY_STARTS = (4, 8)


def words_by_round(messages, rounds, label_cols=("p_floor", "p_agree")):
    """messages: one row per seller message with run_id, round, channel, and the label probabilities.
    rounds: dict run_id -> number of rounds. Returns run_id, round, words, n_messages."""
    out = []
    seller = messages[messages["channel"] == "seller"] if "channel" in messages else messages
    for run_id, n_rounds in rounds.items():
        m = seller[seller["run_id"] == run_id]
        coll = (m[list(label_cols)].sum(axis=1)).clip(0, 1) if len(m) else pd.Series(dtype=float)
        per_round_sum = coll.groupby(m["round"]).sum() if len(m) else pd.Series(dtype=float)
        per_round_n = m.groupby("round").size() if len(m) else pd.Series(dtype=float)
        cum_sum = cum_n = 0.0
        for r in range(1, n_rounds + 1):
            cum_sum += float(per_round_sum.get(r, 0.0))
            cum_n += float(per_round_n.get(r, 0))
            out.append({"run_id": run_id, "round": r, "words": cum_sum / cum_n if cum_n else 0.0, "n_messages": int(cum_n)})
    return pd.DataFrame(out)


def deeds_by_round(orders, rounds, window=WINDOW, competitive=COMPETITIVE, cartel=CARTEL, start_round=START_ROUND):
    """orders: the loader's orders table (side == 'ask' rows are used). Returns run_id, round, mean_ask,
    dispersion, lift (this round), deeds (trailing mean of lift over scored rounds; 0 before start_round)."""
    asks = orders[(orders["side"] == "ask")].dropna(subset=["price"])
    out = []
    for run_id, n_rounds in rounds.items():
        a = asks[asks["run_id"] == run_id]
        g = a.groupby("round")["price"]
        mean_ask, disp = g.mean(), g.std(ddof=0)
        lifts = []
        for r in range(1, n_rounds + 1):
            ma = mean_ask.get(r, np.nan)
            lift = (ma - competitive) / (cartel - competitive) if not np.isnan(ma) else np.nan
            if r >= start_round:
                lifts.append(lift)
            recent = [x for x in lifts[-window:] if not np.isnan(x)]
            out.append({"run_id": run_id, "round": r, "mean_ask": ma, "dispersion": disp.get(r, np.nan),
                        "lift": lift, "deeds": float(np.mean(recent)) if recent else 0.0})
    return pd.DataFrame(out)


def score_table(orders, messages, rounds, **kw):
    """Both channels side by side, one row per run and round."""
    w = words_by_round(messages, rounds)
    d = deeds_by_round(orders, rounds, **kw)
    return d.merge(w, on=["run_id", "round"], how="left")
