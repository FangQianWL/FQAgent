"""项目经理：里程碑与风险视图。"""

from __future__ import annotations

from agents.base import AgentContext, AgentResult, AgentRole


def run(ctx: AgentContext) -> AgentResult:
    top = (ctx.artifacts.get("opportunity") or {}).get("selected_top") or {}
    name = top.get("name", "待定项目")
    delta = {
        "pm": {
            "project_name": name,
            "milestones": [
                {"id": "M1", "title": "需求冻结与架构评审", "weeks": 2},
                {"id": "M2", "title": "MVP 开发与内测", "weeks": 4},
                {"id": "M3", "title": "质量门禁与发布准备", "weeks": 2},
            ],
            "risks": [
                {"id": "R1", "description": "竞品功能追赶", "mitigation": "垂直场景差异化"},
                {"id": "R2", "description": "交付周期膨胀", "mitigation": "范围砍半原则"},
            ],
        }
    }
    return AgentResult(
        agent_role=AgentRole.PROJECT_MANAGER,
        summary=f"已立项「{name}」并输出里程碑与风险登记。",
        artifacts_delta=delta,
        next_stage_hint="REQUIREMENTS",
    )
