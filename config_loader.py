"""加载 YAML 配置。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_ROOT = Path(__file__).resolve().parent


def load_runtime(config_path: Path | None = None) -> dict[str, Any]:
    path = config_path or _ROOT / "configs" / "runtime.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
