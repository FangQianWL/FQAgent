"""统一 Agent 上下文与结果契约（与 AGENTS.md 一致）。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentRole(str, Enum):
    OPPORTUNITY_SCOUT = "opportunity_scout"
    PROJECT_MANAGER = "project_manager"
    REQUIREMENTS = "requirements"
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    UI_DESIGNER = "ui_designer"
    ALGORITHM_DESIGNER = "algorithm_designer"
    TEST_ENGINEER = "test_engineer"
    QUALITY_METRICS = "quality_metrics"


@dataclass
class AgentContext:
    project_id: str
    stage: str
    artifacts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    agent_role: AgentRole
    summary: str
    artifacts_delta: dict[str, Any] = field(default_factory=dict)
    next_stage_hint: str | None = None


def deep_merge(base: dict[str, Any], delta: dict[str, Any]) -> dict[str, Any]:
    """递归合并 dict；delta 覆盖叶子。"""
    out = dict(base)
    for k, v in delta.items():
        if (
            k in out
            and isinstance(out[k], dict)
            and isinstance(v, dict)
        ):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out
