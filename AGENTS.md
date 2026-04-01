# 芳谦未来智能项目 — AGENTS 组织章程与执行契约

本文档是 **FQAgent（芳谦未来智能项目）** 的最高优先级规范：定义公司角色、子 Agent 映射、指挥链、开工/下班语义、记忆策略与安全审批门。实现代码须与本文档保持一致；冲突时以本文档为准。

---

## 1. 项目定位

- **公司名称**：芳谦未来（虚拟组织，由多角色子 Agent 模拟）。
- **领导者**：真人（你）。你拥有最终决策权与发布权。
- **首版范围**：聚焦 **SaaS / 自动化工具 / API 服务** 类机会的发现、评估与产品化编排。
- **自动化模式**：**安全模式** — 每一 **阶段（Stage）** 完成后进入 **等待审批**，经你确认（`确认` / `approve`）后方可进入下一阶段。

---

## 2. 组织结构与角色映射

| 公司角色 | 子 Agent 模块 | 职责摘要 |
|----------|---------------|----------|
| 机会发现（扩展角色） | `OpportunityScout` | 在 SaaS 赛道内识别/打分候选机会，输出优先级队列 |
| 项目经理 | `ProjectManager` | 立项、里程碑、风险与资源视图；汇总各阶段产物 |
| 需求人员 | `RequirementsAgent` | 用户故事、范围、验收标准、非功能需求 |
| 全栈架构设计师 | `FullstackArchitect` | 技术栈、模块边界、接口与数据流、部署拓扑（文档级） |
| 开发人员 | `DeveloperAgent` | 实现计划、目录结构、核心模块与 API 草案（首版以可执行骨架为准） |
| UI 设计师 | `UIDesignerAgent` | 设计系统要点、关键页面线框、可访问性注意项 |
| 算法设计师 | `AlgorithmDesignerAgent` | 算法/模型选型、数据与评估指标、风险与回滚 |
| 测试工程师 | `TestEngineerAgent` | 测试策略、用例层级、自动化与手工边界 |
| 质量度量人员 | `QualityMetricsAgent` | 质量门禁、指标（缺陷密度、覆盖率目标等）、发布就绪检查清单 |

**指挥链（文档产出顺序）**：

```text
OpportunityScout → ProjectManager → Requirements → Architect → Developer
    → UIDesigner ∥ AlgorithmDesigner（实现上可顺序执行）→ TestEngineer → QualityMetrics
```

并行关系在实现中 **顺序化** 为：Developer 之后先 UI 再 Algorithm（或配置调整），以保证快照与审批门简单可测。

---

## 3. 输入/输出契约（最小字段集）

所有子 Agent 接收 **统一上下文** `AgentContext`（见 `agents/base.py`），返回 **统一结果** `AgentResult`：

- **输入**（最小）：
  - `project_id`：项目标识
  - `stage`：当前阶段名
  - `artifacts`：此前阶段累积的结构化产物（dict）
  - `metadata`：运行元数据（时间、配置路径等）

- **输出**（最小）：
  - `agent_role`：角色枚举值
  - `summary`：人类可读摘要（1～3 句）
  - `artifacts_delta`：本阶段新增/更新的键值（合并进总 `artifacts`）
  - `next_stage_hint`：建议下一阶段（由编排器最终裁定）

**合并规则**：`artifacts` =  deep merge（嵌套 dict 递归合并，叶子覆盖）。

---

## 4. 触发命令语义

在 CLI（`main.py`）或等价入口中：

| 命令 | 语义 |
|------|------|
| `开工` / `start` | 从 **待机（IDLE）** 进入执行：若无存盘状态则从 **机会发现** 开始；若存在未完成工作流则 **拒绝**（需先 `恢复` 或明确 `重置`） |
| `下班` / `shutdown` | 将当前 **工作流状态 + artifacts + 待审批点** 写入快照；进入 **下班（SHUTDOWN）** 态，进程可退出 |
| `恢复` / `resume` | 从最新快照恢复，从 **等待审批** 或 **下一阶段起点** 继续（见 `memory/session_snapshot.py`） |

### 4.1 下班前提交（版本库纪律）

- **约定**：在结束当日工作或执行 CLI **`下班` / `shutdown`** 之前，负责本仓库的真人或受托 Agent 应完成 **至少一次 Git 提交**（`git commit`），将当前已通过自检的 **源码与文档**（含 `AGENTS.md` 等契约）写入版本库。
- **与快照的关系**：§6 中的 `memory/history/<project_id>/` 持久化 **编排运行态与阶段产物**；Git 持久化 **仓库内可协作、可回溯的工程变更**。二者互补，缺一不可。
- **推荐顺序**：`git status` → 处理未跟踪/未暂存项 → `git commit` → 需要远程备份时 `git push` → 再执行 `python main.py 下班`（若当日使用了 FQAgent 工作流）。
| `确认` / `approve` | 在安全模式下，对当前 **WAITING_APPROVAL** 解锁，进入下一阶段 |
| `重置` / `reset` | 清除当前 `project_id` 的运行态与可选快照（慎用；需二次确认由 CLI 标志控制） |

---

## 5. 审批门（安全模式）

- 每个 **Stage** 执行完毕后，编排器将状态置为 `WAITING_APPROVAL`，并 **持久化** 事件与产物。
- 仅当真人输入 `确认`/`approve` 后，才进入下一 Stage。
- **发布**：`QualityMetrics` 阶段结束并经最终审批后，产出「发布就绪包」说明；**实际上线发布仅由真人执行**。

---

## 6. 记忆策略（下班后不遗忘）

1. **短期会话**：当前进程内存中的 `Commander` 状态（与快照一致时等价）。
2. **持久化快照**：`memory/history/<project_id>/snapshot.json`（由 `SessionSnapshot` 读写）。
3. **事件日志**：`memory/history/<project_id>/events.jsonl` — 追加 JSON 行，便于审计与回放。
4. **产物归档**：各阶段 `artifacts` 随快照保存；恢复时完整加载。

**原则**：任何「不可丢」的信息必须落在快照或 `events.jsonl` 中，不得仅依赖模型上下文。与 §4.1 一致：**契约与源码级变更**还须落在 Git 提交中。

---

## 7. 与代码的对应关系

| 概念 | 代码位置 |
|------|----------|
| 编排与状态机 | `orchestrator/commander.py` |
| 阶段定义与转换 | `orchestrator/workflow.py` |
| 审批门 | `orchestrator/approval_gate.py` |
| 记忆存储 | `memory/store.py`, `memory/session_snapshot.py` |
| 机会规则 | `configs/opportunity_rules.yaml` |
| 运行时配置 | `configs/runtime.yaml`（`storage_root` 若为相对路径，则相对于仓库根目录解析） |

---

## 8. 修订流程

修订本文档时：更新版本说明、同步 `docs/architecture/system-overview.md`，并补充/调整测试，避免角色职责漂移。

**版本**：1.1 — 补充「下班前 Git 提交」工程纪律（与 1.0 实现兼容）
