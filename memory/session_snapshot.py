"""下班快照与恢复。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orchestrator.state import WorkflowState, WorkflowStatus

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _snapshot_path(project_id: str, storage_root: str | Path | None) -> Path:
    from memory.store import ensure_history

    d = ensure_history(project_id, storage_root)
    return d / "snapshot.json"


def save(
    state: WorkflowState,
    storage_root: str | Path | None = None,
) -> Path:
    path = _snapshot_path(state.project_id, storage_root)
    path.write_text(
        json.dumps(state.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def load(
    project_id: str,
    storage_root: str | Path | None = None,
) -> WorkflowState | None:
    path = _snapshot_path(project_id, storage_root)
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return WorkflowState.from_dict(data)


def has_active_workflow(
    project_id: str,
    storage_root: str | Path | None = None,
) -> bool:
    st = load(project_id, storage_root)
    if st is None:
        return False
    return st.status in (
        WorkflowStatus.WAITING_APPROVAL,
        WorkflowStatus.SHUTDOWN,
        WorkflowStatus.RUNNING,
    )


def clear_snapshot(project_id: str, storage_root: str | Path | None = None) -> bool:
    path = _snapshot_path(project_id, storage_root)
    if path.is_file():
        path.unlink()
        return True
    return False
