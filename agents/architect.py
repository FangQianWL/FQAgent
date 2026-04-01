"""全栈架构：模块与接口草案。"""

from __future__ import annotations

from agents.base import AgentContext, AgentResult, AgentRole


def run(ctx: AgentContext) -> AgentResult:
    delta = {
        "architecture": {
            "stack": {
                "backend": "Python / FastAPI（建议）",
                "frontend": "React 或轻量 SSR（按团队定）",
                "db": "PostgreSQL",
                "queue": "Redis / Celery（按需）",
            },
            "modules": [
                {"name": "api", "responsibility": "REST/JSON API 与鉴权"},
                {"name": "core", "responsibility": "领域逻辑与工作流"},
                {"name": "integration", "responsibility": "第三方 Webhook/开放平台"},
            ],
            "deployment": "容器化 + 单区域多实例；后续再考虑多区域",
        }
    }
    return AgentResult(
        agent_role=AgentRole.ARCHITECT,
        summary="已给出技术栈、模块边界与部署基线。",
        artifacts_delta=delta,
        next_stage_hint="DEVELOPMENT",
    )
