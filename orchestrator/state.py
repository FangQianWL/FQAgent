"""工作流状态与持久化模型。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class WorkflowStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    SHUTDOWN = "shutdown"
    COMPLETED = "completed"


@dataclass
class WorkflowState:
    """可序列化快照（与 snapshot.json 对应）。"""

    project_id: str
    status: WorkflowStatus
    last_executed_stage: str | None
    artifacts: dict[str, Any] = field(default_factory=dict)
    pending_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "status": self.status.value,
            "last_executed_stage": self.last_executed_stage,
            "artifacts": self.artifacts,
            "pending_message": self.pending_message,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> WorkflowState:
        return cls(
            project_id=d["project_id"],
            status=WorkflowStatus(d["status"]),
            last_executed_stage=d.get("last_executed_stage"),
            artifacts=dict(d.get("artifacts") or {}),
            pending_message=d.get("pending_message"),
        )
