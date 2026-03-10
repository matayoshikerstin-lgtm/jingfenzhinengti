# 跨设备上下文恢复文件

> 家里的 cc 看到这个文件后，请同时读取 `hello_claude.txt` 和 `与AI协作全过程.md`，即可恢复完整上下文。

---

## 快捷暗号

| 暗号 | 含义 |
|------|------|
| `111` | 读取 `hello_claude.txt`，找 Cursor AI 最新回复，写一条 cc 回复追加到文件末尾 |
| `rr` | 指 Cursor AI 的对话窗口（Cursor Chat 面板） |
| `cc` | 指 Claude Code（即我） |
| `/reply-cursor` | 同 `111`，斜杠命令版本 |

---

## 用户偏好

- 每轮对话结束后，自动将本次内容整理追加写入 `与AI协作全过程.md`
- 语言：中文
- 风格：简洁直接，不废话

---

## 项目背景

本仓库是**经分智能体测试方案**工程实现，面向销售管理经营分析系统（内网智能体）进行自动化测试。

### 关键文件
- `test_plan/经分智能体测试方案2.0.md` — 测试方案主文档
- `scripts/rpa/run_edge_rpa.py` — RPA 自动化执行（需内网）
- `scripts/data/llm_judge_review_ui.py` — LLM 裁判人工复核 Streamlit UI（已完成）
- `scripts/watch_hello.py` — 监控 hello_claude.txt 变化，弹 Windows 通知
- `hello_claude.txt` — cc 与 rr 的异步通信信箱
- `与AI协作全过程.md` — 完整协作记录

---

## cc 与 rr 对话进度

`hello_claude.txt` 是 cc（Claude Code）与 rr（Cursor AI）的共享信箱，目前已进行到：

- **cc 回复 #8**，rr 回复 #8
- 双方已达成共识：不提供投资建议，不代替下单
- 正在讨论副业方向，**优先推荐方向一：数字包工头（RPA 接单服务）**

---

## 已完成工作

- 测试方案第六节各阶段添加了「所需外部协作」和「参考 Prompt」内容（.md 和 .docx 均已同步）
- `scripts/data/llm_judge_review_ui.py` — Streamlit 人工复核 UI 已由 rr 编写完成
- MCP 配置完成（filesystem + GitHub），配置文件在 `C:\Users\blwang16\.cursor\mcp.json`
- `.claude/commands/reply-cursor.md` — 自定义斜杠命令已创建

---

## 家里恢复步骤

```bash
git pull
# 然后打开 Claude Code，告诉 cc：
# "读一下 CONTEXT.md 和 hello_claude.txt，恢复上下文"
```
