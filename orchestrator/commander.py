"""主调度器：开工 / 确认 / 下班 / 恢复。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agents.base import AgentContext, deep_merge
from config_loader import load_runtime

_REPO_ROOT = Path(__file__).resolve().parent.parent
from memory import session_snapshot
from memory.store import append_event
from orchestrator import approval_gate, workflow
from orchestrator.state import WorkflowState, WorkflowStatus


class Commander:
    def __init__(
        self,
        project_id: str | None = None,
        storage_root: str | Path | None = None,
        runtime_config_path: Path | None = None,
    ) -> None:
        cfg = load_runtime(runtime_config_path)
        self.project_id = project_id or cfg.get("default_project_id", "fq-default")
        root = storage_root or cfg.get("storage_root")
        if root:
            p = Path(root)
            self.storage_root = p if p.is_absolute() else (_REPO_ROOT / p).resolve()
        else:
            self.storage_root = None

    def _save(self, state: WorkflowState) -> None:
        session_snapshot.save(state, self.storage_root)

    def _load(self) -> WorkflowState | None:
        return session_snapshot.load(self.project_id, self.storage_root)

    def start(self) -> WorkflowState:
        if session_snapshot.has_active_workflow(self.project_id, self.storage_root):
            raise RuntimeError(
                "存在未完结工作流（等待审批/已下班暂停）。请先执行「恢复」再继续，"
                "或使用「重置」清空后重新开工。"
            )
        existing = self._load()
        if existing and existing.status == WorkflowStatus.COMPLETED:
            raise RuntimeError(
                "当前项目已完成。请使用「重置」后重新开工，或更换 project_id。"
            )

        state = WorkflowState(
            project_id=self.project_id,
            status=WorkflowStatus.RUNNING,
            last_executed_stage=None,
            artifacts={},
        )
        first = workflow.first_stage()
        state = self._run_one_stage(state, first)
        state.last_executed_stage = first
        state = approval_gate.require_approval(state)
        state.pending_message = (
            f"阶段「{first}」已完成，请审阅产物后执行「确认」进入下一阶段。"
        )
        self._save(state)
        append_event(
            self.project_id,
            "stage_completed",
            {"stage": first, "status": state.status.value},
            self.storage_root,
        )
        return state

    def approve(self) -> WorkflowState:
        state = self._load()
        if state is None:
            raise RuntimeError("无快照；请先「开工」。")
        if state.status == WorkflowStatus.SHUTDOWN:
            raise RuntimeError("当前为下班状态；请先「恢复」再「确认」。")

        if (
            state.status == WorkflowStatus.WAITING_APPROVAL
            and state.last_executed_stage == "QUALITY"
        ):
            state.status = WorkflowStatus.COMPLETED
            state.pending_message = "全部阶段已完成。请真人执行发布与上线。"
            self._save(state)
            append_event(
                self.project_id,
                "workflow_completed",
                {},
                self.storage_root,
            )
            return state

        state = approval_gate.approve(state)
        nxt = workflow.next_stage(state.last_executed_stage)
        if nxt is None:
            state.status = WorkflowStatus.COMPLETED
            self._save(state)
            return state

        state = self._run_one_stage(state, nxt)
        state.last_executed_stage = nxt
        state = approval_gate.require_approval(state)
        state.pending_message = (
            f"阶段「{nxt}」已完成，请审阅产物后执行「确认」进入下一阶段。"
        )
        self._save(state)
        append_event(
            self.project_id,
            "stage_completed",
            {"stage": nxt, "status": state.status.value},
            self.storage_root,
        )
        return state

    def shutdown(self) -> WorkflowState:
        state = self._load()
        if state is None:
            raise RuntimeError("无快照；请先「开工」。")
        if state.status == WorkflowStatus.COMPLETED:
            raise RuntimeError("工作流已完成，无需下班。")
        state.status = WorkflowStatus.SHUTDOWN
        state.pending_message = "已下班：快照已保存。下次请「恢复」后继续。"
        self._save(state)
        append_event(
            self.project_id,
            "shutdown",
            {"last_stage": state.last_executed_stage},
            self.storage_root,
        )
        return state

    def resume(self) -> WorkflowState:
        state = self._load()
        if state is None:
            raise RuntimeError("无快照；请先「开工」。")
        if state.status != WorkflowStatus.SHUTDOWN:
            raise RuntimeError("仅在下班（shutdown）状态下需要恢复。")
        state.status = WorkflowStatus.WAITING_APPROVAL
        state.pending_message = (
            f"已恢复。当前停在阶段「{state.last_executed_stage}」之后，等待审批。"
        )
        self._save(state)
        append_event(
            self.project_id,
            "resume",
            {"last_stage": state.last_executed_stage},
            self.storage_root,
        )
        return state

    def reset(self) -> None:
        session_snapshot.clear_snapshot(self.project_id, self.storage_root)
        # 可选：清理 events — 首版保留 events 作为审计
        append_event(self.project_id, "reset", {}, self.storage_root)

    def _run_one_stage(self, state: WorkflowState, stage: str) -> WorkflowState:
        ctx = AgentContext(
            project_id=state.project_id,
            stage=stage,
            artifacts=state.artifacts,
            metadata={"storage_root": str(self.storage_root or "")},
        )
        result = workflow.run_stage(stage, ctx)
        state.artifacts = deep_merge(state.artifacts, result.artifacts_delta)
        append_event(
            self.project_id,
            "stage_run",
            {
                "stage": stage,
                "agent": result.agent_role.value,
                "summary": result.summary,
            },
            self.storage_root,
        )
        return state

    def status(self) -> dict[str, Any]:
        st = self._load()
        if st is None:
            return {"project_id": self.project_id, "snapshot": None}
        return {
            "project_id": st.project_id,
            "status": st.status.value,
            "last_executed_stage": st.last_executed_stage,
            "pending_message": st.pending_message,
        }
