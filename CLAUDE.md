# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目背景

本仓库是**经分智能体测试方案**的工程实现，面向销售管理经营分析系统（内网智能体）进行自动化测试。

核心数据来自三张业务表（`test_data/` 目录）：
- **商机表** (`fact_opportunity_*.csv`)：字段含 `opp_id`, `opp_name`, `opp_amount`, `win_rate`, `est_gross_profit`, `est_deal_date`, `sales_process`, `life_status`, `exclude_reason`, `owner_id`, `customer_name`, `business_unit_name`, `legion_product_line`
- **合同表** (`fact_contract_*.csv`)：字段含 `contract_approval_code`, `contract_name`, `sales_amount_total`, `gross_margin_rate`, `net_profit`, `archive_time`, `final_user_name`, `opp_code`（与商机表 `opp_id` 关联）
- **项目表** (`fact_project_*.csv`)

测试方案文档：[`test_plan/经分智能体测试方案2.0.md`](test_plan/经分智能体测试方案2.0.md)

## 工作规则

- **每轮对话结束后**，将本次对话内容整理追加写入 `与AI协作全过程.md`

## 环境依赖

```bash
pip install -r requirements.txt       # mammoth, markdownify
pip install pandas openpyxl playwright
playwright install msedge
```

所有脚本需从**项目根目录**运行，路径均为相对路径（如 `test_data/`、`test_result/`）。

## 目录结构与用途

```
scripts/
  rpa/          # RPA 自动化执行引擎
  data/         # Ground Truth 计算脚本（基于真实脱敏数据）
  docx/         # Word 文档操作脚本（python-docx + lxml）
  debug/        # docx 结构调试脚本
test_data/      # 原始数据文件（CSV/xlsx）及测试题库（测试数据.xlsx）
test_result/    # RPA 抓取结果（result.xlsx）
test_plan/      # 测试方案文档（.md 和 .docx 保持同步）
```

## 关键脚本说明

### RPA 自动化执行
```bash
python scripts/rpa/run_edge_rpa.py
```
使用 Playwright 驱动 Edge 浏览器，读取 `test_result/result.xlsx` 中的"问题"列，逐题向内网智能体（`http://172.30.32.19:30016/home`）提问并写回"智能体回复"列。支持断点续传（已有回复的题目自动跳过）。需在能访问内网的机器上运行，启动后有 15 秒手动登录窗口。

### Ground Truth 计算
```bash
python scripts/data/calc_answers.py        # 计算 Q1-Q40 基准答案
python scripts/data/calc_q21_q33.py        # Q21-Q33 专项计算
python scripts/data/calc_risk_concentration.py  # 风险集中度相关题目
python scripts/data/solve_open_final.py    # 开放题参考答案
python scripts/data/solve_q40.py           # Q40 跨表关联查询
```
从 `test_data/` 读取 CSV，计算非开放题基准答案。商机表与合同表通过 `opp_df.opp_id` ↔ `con_df.opp_code` 关联。

### docx 文档操作
`scripts/docx/` 下各脚本直接操作 `test_plan/经分智能体测试方案2.0.docx`，使用 `lxml` 的 `addprevious()`/`addnext()` 在指定位置插入段落。操作完成后 .md 文件需同步更新。

### 检查 docx 结构
```bash
python scripts/docx/inspect_docx.py
```

### docx 转 md
```bash
python scripts/docx/docx_to_md.py
```
使用 mammoth + markdownify 将 .docx 转换为 .md，转换后需人工校对格式。

## 文档同步原则

`.md` 和 `.docx` 是同一份文档的两种格式，修改任一方后需同步另一方。`.md` 用于 git 版本管理和预览，`.docx` 用于正式交付。
