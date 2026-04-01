"""质量度量：发布就绪清单。"""

from __future__ import annotations

from agents.base import AgentContext, AgentResult, AgentRole


def run(ctx: AgentContext) -> AgentResult:
    delta = {
        "quality": {
            "release_checklist": [
                "需求可追溯（史诗→故事）",
                "架构与实现路径一致",
                "关键用例自动化覆盖",
                "回滚与监控预案",
            ],
            "targets": {
                "critical_defects": 0,
                "test_coverage_goal_pct": 70,
            },
            "human_release_note": "请真人完成最终部署、域名与合规检查后再对外发布。",
        }
    }
    return AgentResult(
        agent_role=AgentRole.QUALITY_METRICS,
        summary="已生成发布就绪检查清单与质量目标；等待真人发布。",
        artifacts_delta=delta,
        next_stage_hint=None,
    )
