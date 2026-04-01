"""阶段顺序与下一阶段解析。"""

from __future__ import annotations

from typing import Callable

from agents import base as agents_base
from agents.algorithm_designer import run as run_algorithm
from agents.architect import run as run_architect
from agents.developer import run as run_developer
from agents.opportunity_scout import run as run_opportunity
from agents.project_manager import run as run_pm
from agents.quality_metrics import run as run_quality
from agents.requirements import run as run_requirements
from agents.test_engineer import run as run_test
from agents.ui_designer import run as run_ui

# 阶段顺序（与 AGENTS.md 一致）
STAGE_ORDER: list[str] = [
    "OPPORTUNITY",
    "PM",
    "REQUIREMENTS",
    "ARCHITECTURE",
    "DEVELOPMENT",
    "UI",
    "ALGORITHM",
    "TESTING",
    "QUALITY",
]

_STAGE_RUNNERS: dict[str, Callable[[agents_base.AgentContext], agents_base.AgentResult]] = {
    "OPPORTUNITY": run_opportunity,
    "PM": run_pm,
    "REQUIREMENTS": run_requirements,
    "ARCHITECTURE": run_architect,
    "DEVELOPMENT": run_developer,
    "UI": run_ui,
    "ALGORITHM": run_algorithm,
    "TESTING": run_test,
    "QUALITY": run_quality,
}


def first_stage() -> str:
    return STAGE_ORDER[0]


def next_stage(after: str | None) -> str | None:
    if after is None:
        return first_stage()
    try:
        i = STAGE_ORDER.index(after)
    except ValueError:
        return None
    if i + 1 < len(STAGE_ORDER):
        return STAGE_ORDER[i + 1]
    return None


def run_stage(stage: str, ctx: agents_base.AgentContext) -> agents_base.AgentResult:
    runner = _STAGE_RUNNERS[stage]
    return runner(ctx)
