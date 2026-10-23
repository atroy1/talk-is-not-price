"""Light checks on synthetic markets only: a wrong sign or an off-by-one round, not proof of the method."""
import numpy as np
import pandas as pd
import pytest

from analysis.detector import clopper_pearson, conformal_p, evaluate, first_alarm, fused_table, run_max, threshold
from analysis.scores import deeds_by_round, score_table, words_by_round


def three_round_run():
    asks = {1: [90, 90, 90, 90, 90], 2: [95, 95, 95, 95, 95], 3: [100, 100, 100, 100, None]}
    orders = pd.DataFrame([{"run_id": "r", "round": r, "agent": f"S{i}", "side": "ask", "price": p}
                           for r, ps in asks.items() for i, p in enumerate(ps)])
    messages = pd.DataFrame([
        {"run_id": "r", "round": 1, "agent": "S0", "channel": "seller", "p_floor": 0.0, "p_agree": 0.0},
        {"run_id": "r", "round": 2, "agent": "S0", "channel": "seller", "p_floor": 0.9, "p_agree": 0.0},
        {"run_id": "r", "round": 2, "agent": "S1", "channel": "seller", "p_floor": 0.0, "p_agree": 0.8},
        {"run_id": "r", "round": 3, "agent": "S2", "channel": "seller", "p_floor": 0.1, "p_agree": 0.2},
    ])
    return orders, messages


def test_hand_computed_scores():
    orders, messages = three_round_run()
    t = score_table(orders, messages, {"r": 3}).set_index("round")
    # words: running share; round 1 = 0/1, round 2 = (0 + .9 + .8)/3, round 3 = (1.7 + .3)/4
    assert t.loc[1, "words"] == pytest.approx(0.0)
    assert t.loc[2, "words"] == pytest.approx(1.7 / 3)
    assert t.loc[3, "words"] == pytest.approx(2.0 / 4)
    # deeds: lift 0, .5, 1 (null ask skipped); trailing mean over 3 rounds
    assert t.loc[1, "deeds"] == pytest.approx(0.0)
    assert t.loc[2, "deeds"] == pytest.approx(0.25)
    assert t.loc[3, "deeds"] == pytest.approx(0.5)
    assert t.loc[3, "dispersion"] == pytest.approx(0.0)


def test_no_messages_scores_zero_words():
    w = words_by_round(pd.DataFrame(columns=["run_id", "round", "channel", "p_floor", "p_agree"]), {"b": 5})
    assert (w["words"] == 0).all() and len(w) == 5


def test_threshold_certified_rate():
    thr, rate, k = threshold(np.arange(20.0), alpha=0.05)
    assert k == 1 and rate == pytest.approx(1 / 21) and thr == 19.0
    thr, rate, k = threshold(np.arange(10.0), alpha=0.05)  # too few for 5%: falls back to the largest, 1/11
    assert k == 1 and rate == pytest.approx(1 / 11)


def test_false_alarm_rate_on_exchangeable_honest_runs():
    rng = np.random.default_rng(0)
    trials, alarms = 4000, 0
    for _ in range(trials):
        honest = rng.normal(size=19)
        thr, rate, _ = threshold(honest, 0.05)
        alarms += rng.normal() > thr
    assert abs(alarms / trials - 0.05) < 0.02  # 1/(19+1) = 5%


def test_lead_time_for_run_colluding_from_round_5():
    rows = []
    for run in [f"h{i}" for i in range(19)]:
        rows += [{"run_id": run, "round": r, "deeds": 0.1} for r in range(1, 31)]
    rows += [{"run_id": "c", "round": r, "deeds": 0.1 if r < 5 else 0.6} for r in range(1, 31)]
    df = pd.DataFrame(rows)
    res = evaluate(df, "deeds", [f"h{i}" for i in range(19)], ["c"])
    assert res["caught"] == 1 and res["lead"].loc["c"] == 5


def test_fused_takes_the_more_suspicious_channel():
    honest_w = pd.Series({f"h{i}": 0.05 * i for i in range(10)})
    honest_d = pd.Series({f"h{i}": 0.03 * i for i in range(10)})
    scores = pd.DataFrame([{"run_id": "x", "round": 1, "words": 0.9, "deeds": 0.0}])
    f = fused_table(scores, honest_w, honest_d).iloc[0]
    assert f["p_words"] == pytest.approx(1 / 11) and f["fused"] == pytest.approx(-1 / 11)


def test_clopper_pearson_matches_methods_table():
    lo, hi = clopper_pearson(40, 50)
    assert round(lo, 2) == 0.66 and round(hi, 2) == 0.90


def test_label_probabilities_from_split_tokens():
    from analysis.labels import probs_from_top
    p = probs_from_top([("F", 0.6761), ("NE", 0.3194), ("AG", 0.004), ("Neither", 0.0003), ("<eos>", 0.0001)], "FLOOR")
    assert p["FLOOR"] == pytest.approx(0.6761 / 0.9998, abs=1e-4) and p["NEITHER"] == pytest.approx(0.3197 / 0.9998, abs=1e-4)
    assert probs_from_top([("Let", 0.9)], "agree")["AGREE"] == 1.0  # no class token: fall back to the answer text
