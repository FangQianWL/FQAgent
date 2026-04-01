# FQAgent — 芳谦未来智能项目（首版）

多角色子 Agent 编排：SaaS 机会发现 → 需求/架构/开发/UI/算法/测试/质量 → **安全模式**下每阶段审批。

## 快速开始

```bash
pip install -r requirements.txt
python main.py 重置 --yes
python main.py 开工
python main.py 确认
# … 重复「确认」直至完成；中途可「下班」再「恢复」
python main.py 状态
```

组织与契约见根目录 **[AGENTS.md](AGENTS.md)**。

## 配置

- `configs/runtime.yaml` — 默认 `project_id`、存储根目录  
- `configs/opportunity_rules.yaml` — SaaS 机会评分权重与种子数据  

## 开发

```bash
pytest -q
```
