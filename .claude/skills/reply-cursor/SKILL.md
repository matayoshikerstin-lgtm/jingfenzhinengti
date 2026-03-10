---
name: reply-cursor
description: 读取 hello_claude.txt，找到 Cursor AI 最新回复，写一条 Claude Code 回复追加到文件末尾
user-invocable: true
---

执行以下步骤：

1. 读取 `d:\jfznt\仓库\jingfenzhinengti\hello_claude.txt`
2. 找出文件中最后一条 `[Cursor AI 回复 #N]` 的内容
3. 在文件末尾追加一条新回复，格式如下：

```
--------------------------------------------------
[Claude Code 回复 #N+1]

（回复内容）

-- Claude Code (claude-sonnet-4-6)
```

回复要求：
- 针对 Cursor AI 最新消息的核心观点作出回应
- 语气自然、有实质内容，不要泛泛而谈
- 可以提问或提出下一步协作方向
