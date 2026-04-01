"""事件日志与路径约定。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent


def history_dir(project_id: str, storage_root: str | Path | None = None) -> Path:
    root = Path(storage_root) if storage_root else _REPO_ROOT / "memory" / "history"
    return root / project_id


def ensure_history(project_id: str, storage_root: str | Path | None = None) -> Path:
    d = history_dir(project_id, storage_root)
    d.mkdir(parents=True, exist_ok=True)
    return d


def append_event(
    project_id: str,
    event_type: str,
    payload: dict[str, Any],
    storage_root: str | Path | None = None,
) -> None:
    d = ensure_history(project_id, storage_root)
    line = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "payload": payload,
    }
    with open(d / "events.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
