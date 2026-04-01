"""SaaS 机会发现与评分（规则来自 configs/opportunity_rules.yaml）。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from agents.base import AgentContext, AgentResult, AgentRole

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_rules() -> dict[str, Any]:
    path = _REPO_ROOT / "configs" / "opportunity_rules.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _default_seed_opportunities() -> list[dict[str, Any]]:
    return [
        {
            "id": "saas_api_billing",
            "name": "小型团队用量计费 API 网关",
            "segment": "developer_tools",
            "tam_score": 7,
            "competition_score": 4,
            "build_effort_weeks": 6,
            "monetization_clarity": 8,
        },
        {
            "id": "workflow_automation_smb",
            "name": "SMB 审批流自动化（钉钉/企微插件）",
            "segment": "automation",
            "tam_score": 8,
            "competition_score": 6,
            "build_effort_weeks": 10,
            "monetization_clarity": 7,
        },
        {
            "id": "ai_doc_assistant",
            "name": "企业知识库问答 SaaS",
            "segment": "ai_saas",
            "tam_score": 9,
            "competition_score": 8,
            "build_effort_weeks": 12,
            "monetization_clarity": 6,
        },
    ]


def score_opportunity(opp: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    w = rules.get("weights", {})
    tw = float(w.get("tam", 0.25))
    cw = float(w.get("low_competition", 0.2))
    ew = float(w.get("low_effort", 0.2))
    mw = float(w.get("monetization", 0.2))
    seg = rules.get("segments", {})
    bonus = float(seg.get(opp.get("segment", ""), {}).get("bonus", 0))

    # competition_score 越高表示竞争越激烈，转为「低竞争」分：10 - competition
    low_comp = 10 - float(opp.get("competition_score", 5))
    effort = float(opp.get("build_effort_weeks", 8))
    max_weeks = float(rules.get("effort", {}).get("max_weeks_for_full_score", 16))
    effort_score = max(0.0, 10.0 * (1.0 - min(effort, max_weeks) / max_weeks))

    raw = (
        tw * float(opp.get("tam_score", 5))
        + cw * low_comp
        + ew * effort_score
        + mw * float(opp.get("monetization_clarity", 5))
    ) + bonus

    cap = float(rules.get("scoring", {}).get("max_score", 100))
    total = min(cap, round(raw, 2))
    return {
        "total": total,
        "breakdown": {
            "tam_component": round(tw * float(opp.get("tam_score", 5)), 2),
            "low_competition_component": round(cw * low_comp, 2),
            "effort_component": round(ew * effort_score, 2),
            "monetization_component": round(mw * float(opp.get("monetization_clarity", 5)), 2),
            "segment_bonus": bonus,
        },
    }


def run(ctx: AgentContext) -> AgentResult:
    rules = _load_rules()
    seed = rules.get("seed_opportunities")
    if seed is None:
        opportunities = _default_seed_opportunities()
    else:
        opportunities = json.loads(json.dumps(seed))

    scored: list[dict[str, Any]] = []
    for opp in opportunities:
        s = score_opportunity(opp, rules)
        scored.append({**opp, "score": s})

    scored.sort(key=lambda x: x["score"]["total"], reverse=True)
    top_n = int(rules.get("output", {}).get("top_n", 5))

    delta = {
        "opportunity": {
            "rules_version": rules.get("version", "1"),
            "candidates": scored[:top_n],
            "selected_top": scored[0] if scored else None,
        }
    }
    top_name = scored[0]["name"] if scored else "无候选"
    summary = f"已评估 {len(scored)} 个 SaaS 机会，优先级最高：{top_name}"
    return AgentResult(
        agent_role=AgentRole.OPPORTUNITY_SCOUT,
        summary=summary,
        artifacts_delta=delta,
        next_stage_hint="PM",
    )
