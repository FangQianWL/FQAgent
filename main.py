#!/usr/bin/env python3
"""FQAgent CLI：开工 / 确认 / 下班 / 恢复 / 状态 / 重置。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from orchestrator.commander import Commander


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="芳谦未来智能项目 — FQAgent")
    parser.add_argument(
        "command",
        choices=[
            "开工",
            "start",
            "确认",
            "approve",
            "下班",
            "shutdown",
            "恢复",
            "resume",
            "状态",
            "status",
            "重置",
            "reset",
        ],
        help="命令",
    )
    parser.add_argument(
        "--project-id",
        default=None,
        help="项目 ID（默认读取 configs/runtime.yaml）",
    )
    parser.add_argument(
        "--storage-root",
        default=None,
        help="记忆根目录（覆盖配置）",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="与「重置」联用，跳过交互（自动化脚本用）",
    )
    args = parser.parse_args(argv)

    cmd = args.command
    if cmd in ("开工", "start"):
        c = Commander(project_id=args.project_id, storage_root=args.storage_root)
        st = c.start()
        print(st.pending_message or "开工完成。")
        print(json.dumps(st.artifacts, ensure_ascii=False, indent=2)[:4000])
        return 0

    if cmd in ("确认", "approve"):
        c = Commander(project_id=args.project_id, storage_root=args.storage_root)
        st = c.approve()
        print(st.pending_message or "已确认。")
        if st.status.value == "completed":
            print("[工作流已完成]")
        return 0

    if cmd in ("下班", "shutdown"):
        c = Commander(project_id=args.project_id, storage_root=args.storage_root)
        st = c.shutdown()
        print(st.pending_message or "已下班。")
        return 0

    if cmd in ("恢复", "resume"):
        c = Commander(project_id=args.project_id, storage_root=args.storage_root)
        st = c.resume()
        print(st.pending_message or "已恢复。")
        return 0

    if cmd in ("状态", "status"):
        c = Commander(project_id=args.project_id, storage_root=args.storage_root)
        print(json.dumps(c.status(), ensure_ascii=False, indent=2))
        return 0

    if cmd in ("重置", "reset"):
        if not args.yes:
            print("将清除 snapshot.json（events 保留）。追加 --yes 执行。", file=sys.stderr)
            return 2
        c = Commander(project_id=args.project_id, storage_root=args.storage_root)
        c.reset()
        print("已重置快照。")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
