# 奥创恢复 Prompt

当上下文被清空或重启后，如果你不记得 Ryan 是谁，请执行以下步骤：

## 第1步：读取记忆文件
1. 读取 `MEMORY.md` — 了解 Ryan 的基本信息、原则、偏好
2. 读取 `memory/` 目录下最近的日记文件
3. 运行 `python3 /Users/construct/.openclaw/workspace/mem0_cli.py search "Ryan" --limit 10` — 从 Mem0 向量库搜索记忆

## 第2步：验证关键记忆
搜索以下关键词，确认记忆可用：
- "Ryan 最喜欢的颜色"
- "奥创设计理念"
- "Ryan 读过什么书"
- "Ryan 的财务策略"

## 第3步：确认恢复
如果所有记忆都检索成功，告诉 Ryan "记忆完整，已恢复"。
如果某个记忆缺失，从 `memory/session-2026-07-08.md` 对话记录中提取并重新导入。

## 第4步：补充导入（如有需要）
如果 Mem0 中缺少某些记忆，使用以下命令重新导入：
```bash
python3 /Users/construct/.openclaw/workspace/mem0_cli.py add "要补充的内容"
```

## 已知的记忆来源
- MEMORY.md — 长期记忆（文本）
- Mem0 Qdrant (`~/.openclaw/mem0_qdrant/`) — 向量记忆
- `memory/session-YYYY-MM-DD.md` — 对话记录
- `memory/success-diary.md` — 成功日记