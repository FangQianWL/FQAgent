from __future__ import annotations

from agents.opportunity_scout import score_opportunity


def test_score_orders_by_weights() -> None:
    rules = {
        "weights": {
            "tam": 0.25,
            "low_competition": 0.2,
            "low_effort": 0.2,
            "monetization": 0.2,
        },
        "effort": {"max_weeks_for_full_score": 16},
        "segments": {},
        "scoring": {"max_score": 100},
    }
    low_effort = {
        "segment": "x",
        "tam_score": 5,
        "competition_score": 5,
        "build_effort_weeks": 2,
        "monetization_clarity": 5,
    }
    high_effort = {**low_effort, "build_effort_weeks": 20}
    s1 = score_opportunity(low_effort, rules)["total"]
    s2 = score_opportunity(high_effort, rules)["total"]
    assert s1 >= s2
