"""UI：设计系统与线框要点。"""

from __future__ import annotations

from agents.base import AgentContext, AgentResult, AgentRole


def run(ctx: AgentContext) -> AgentResult:
    delta = {
        "ui": {
            "design_tokens": {
                "primary": "#2563eb",
                "radius": "8px",
                "font_stack": "system-ui, sans-serif",
            },
            "screens": [
                {"id": "dashboard", "elements": ["任务列表", "状态筛选", "空状态引导"]},
                {"id": "task_detail", "elements": ["时间线", "操作区", "错误提示"]},
            ],
            "a11y": ["对比度 AA", "焦点可见", "键盘可操作主路径"],
        }
    }
    return AgentResult(
        agent_role=AgentRole.UI_DESIGNER,
        summary="已输出设计令牌与关键页面线框要点。",
        artifacts_delta=delta,
        next_stage_hint="ALGORITHM",
    )
