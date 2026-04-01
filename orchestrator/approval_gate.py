"""安全模式审批门。"""

from __future__ import annotations

from orchestrator.state import WorkflowState, WorkflowStatus


def require_approval(state: WorkflowState) -> WorkflowState:
    state.status = WorkflowStatus.WAITING_APPROVAL
    return state


def approve(state: WorkflowState) -> WorkflowState:
    if state.status != WorkflowStatus.WAITING_APPROVAL:
        raise RuntimeError(
            f"当前状态为 {state.status}，无法确认；仅在 waiting_approval 时可确认。"
        )
    state.status = WorkflowStatus.RUNNING
    state.pending_message = None
    return state


def is_waiting(state: WorkflowState) -> bool:
    return state.status == WorkflowStatus.WAITING_APPROVAL
