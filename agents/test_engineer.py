"""测试：策略与用例分层。"""

from __future__ import annotations

from agents.base import AgentContext, AgentResult, AgentRole


def run(ctx: AgentContext) -> AgentResult:
    delta = {
        "testing": {
            "strategy": "测试金字塔：单测为主，合约为辅，少量 E2E",
            "layers": [
                {"name": "unit", "scope": "core 规则与校验"},
                {"name": "contract", "scope": "API schema 与错误码"},
                {"name": "e2e", "scope": "主路径冒烟"},
            ],
            "ci_gate": ["pytest 通过", "lint（可选）"],
        }
    }
    return AgentResult(
        agent_role=AgentRole.TEST_ENGINEER,
        summary="已输出测试分层与 CI 门禁建议。",
        artifacts_delta=delta,
        next_stage_hint="QUALITY",
    )
