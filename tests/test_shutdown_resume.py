from __future__ import annotations

from pathlib import Path

import pytest

from orchestrator.commander import Commander
from orchestrator.state import WorkflowStatus


def test_shutdown_then_resume(tmp_path: Path) -> None:
    root = tmp_path / "hist"
    c = Commander(project_id="sd", storage_root=root)
    c.start()
    c.shutdown()
    st = c._load()
    assert st is not None
    assert st.status == WorkflowStatus.SHUTDOWN

    with pytest.raises(RuntimeError, match="下班"):
        c.approve()

    r = c.resume()
    assert r.status == WorkflowStatus.WAITING_APPROVAL

    c.approve()
    st2 = c._load()
    assert st2 is not None
    assert st2.last_executed_stage == "PM"
