"""开发：实现计划与目录骨架说明。"""

from __future__ import annotations

from agents.base import AgentContext, AgentResult, AgentRole


def run(ctx: AgentContext) -> AgentResult:
    delta = {
        "development": {
            "repo_layout": [
                "src/api/",
                "src/core/",
                "src/integration/",
                "tests/",
            ],
            "mvp_endpoints": [
                "POST /v1/tasks",
                "GET /v1/tasks/{id}",
                "POST /v1/webhooks/provider",
            ],
            "notes": "首版以编排与文档为主；业务代码可在后续迭代填充。",
        }
    }
    return AgentResult(
        agent_role=AgentRole.DEVELOPER,
        summary="已输出仓库布局与 MVP 端点草案。",
        artifacts_delta=delta,
        next_stage_hint="UI",
    )
