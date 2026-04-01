from __future__ import annotations

from pathlib import Path

import pytest

from orchestrator import approval_gate
from orchestrator.commander import Commander
from orchestrator.state import WorkflowState, WorkflowStatus


def test_approve_only_when_waiting() -> None:
    st = WorkflowState(
        project_id="x",
        status=WorkflowStatus.RUNNING,
        last_executed_stage="PM",
        artifacts={},
    )
    with pytest.raises(RuntimeError, match="waiting_approval"):
        approval_gate.approve(st)


def test_full_pipeline_completes(tmp_path: Path) -> None:
    """端到端：开工 + 连续确认直至 COMPLETED。"""
    root = tmp_path / "hist"
    c = Commander(project_id="e2e", storage_root=root)
    c.start()
    for _ in range(9):
        c.approve()
    st = c._load()
    assert st is not None
    assert st.status == WorkflowStatus.COMPLETED
    assert "quality" in st.artifacts
