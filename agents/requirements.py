"""需求：用户故事与验收标准。"""

from __future__ import annotations

from agents.base import AgentContext, AgentResult, AgentRole


def run(ctx: AgentContext) -> AgentResult:
    pm = ctx.artifacts.get("pm") or {}
    pname = pm.get("project_name", "项目")
    delta = {
        "requirements": {
            "epics": [
                {
                    "id": "E1",
                    "title": f"{pname} — 核心工作流",
                    "stories": [
                        {
                            "id": "US1",
                            "as": "终端用户",
                            "want": "完成主任务闭环",
                            "criteria": ["主路径可用", "错误可恢复"],
                        },
                        {
                            "id": "US2",
                            "as": "管理员",
                            "want": "配置关键参数",
                            "criteria": ["配置持久化", "变更审计"],
                        },
                    ],
                }
            ],
            "non_functional": ["可用性 99.5%（目标）", "核心 API P95 < 500ms（目标）"],
        }
    }
    return AgentResult(
        agent_role=AgentRole.REQUIREMENTS,
        summary="已输出史诗/故事与初步非功能需求。",
        artifacts_delta=delta,
        next_stage_hint="ARCHITECTURE",
    )
