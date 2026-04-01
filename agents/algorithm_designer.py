"""算法：选型与评估指标。"""

from __future__ import annotations

from agents.base import AgentContext, AgentResult, AgentRole


def run(ctx: AgentContext) -> AgentResult:
    delta = {
        "algorithm": {
            "use_cases": ["规则引擎优先", "必要时引入小规模 ML 排序/推荐"],
            "metrics": ["precision@k", "人工复核率", "延迟 P95"],
            "risks": ["数据漂移", "反馈闭环不足"],
            "rollback": "特征开关 + 回退到规则基线",
        }
    }
    return AgentResult(
        agent_role=AgentRole.ALGORITHM_DESIGNER,
        summary="已给出算法路径、指标与回滚策略。",
        artifacts_delta=delta,
        next_stage_hint="TESTING",
    )
