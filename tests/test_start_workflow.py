from __future__ import annotations

from pathlib import Path

import pytest

from orchestrator.commander import Commander


def test_start_then_approve_advances_to_pm(tmp_path: Path) -> None:
    root = tmp_path / "hist"
    c = Commander(project_id="t1", storage_root=root)
    st = c.start()
    assert st.last_executed_stage == "OPPORTUNITY"
    assert st.status.value == "waiting_approval"
    assert "opportunity" in st.artifacts

    st2 = c.approve()
    assert st2.last_executed_stage == "PM"
    assert "pm" in st2.artifacts


def test_start_rejected_when_active(tmp_path: Path) -> None:
    root = tmp_path / "hist"
    c = Commander(project_id="t2", storage_root=root)
    c.start()
    with pytest.raises(RuntimeError, match="未完结"):
        c.start()
