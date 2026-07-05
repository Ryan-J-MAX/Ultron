---
name: "export-session"
description: "导出OpenClaw session完整对话为markdown。使用trajectory export + Python解析events.jsonl，生成逐字原文对话记录。"
---

# Export Session（导出对话记录）

将 OpenClaw session 的完整对话导出为逐字原文 markdown 文件。

## 触发条件

用户说"导出对话"、"保存对话记录"、"导出session"、"把对话存下来"时启用。

## 流程

### 第1步：确认目标 session

```bash
openclaw sessions list
```

找到要导出的 session key（通常是 `agent:main:main`）。

### 第2步：导出轨迹

```bash
openclaw sessions export-trajectory \
  --session-key "agent:main:main" \
  --workspace . --json
```

输出类似：
```json
{
  "outputDir": "/path/to/.openclaw/trajectory-exports/openclaw-trajectory-xxx",
  "eventCount": 508
}
```

### 第3步：解析 events.jsonl → markdown

在导出目录中运行以下 Python 脚本：

```python
import json, re

with open("events.jsonl", "r") as f:
    events = [json.loads(line) for line in f if line.strip()]

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
        return "\n".join(texts)
    return ""

output = []
for e in events:
    t = e.get("type")
    data = e.get("data", {})
    
    if t == "user.message":
        msg = data.get("message", {})
        text = extract_text(msg.get("content", ""))
        if text.strip():
            output.append(f"\nUser: {text.strip()}\n")
    
    elif t == "assistant.message":
        msg = data.get("message", {})
        text = extract_text(msg.get("content", ""))
        if text.strip():
            output.append(f"\nAssistant: {text.strip()}\n")

result = "\n".join(output)
result = re.sub(r'\n{4,}', '\n\n\n', result)

with open("full-dialog.md", "w") as f:
    f.write(result)

print(f"Done: {len(result.split(chr(10)))} lines, {len(result)} chars")
```

### 第4步：合并到目标文件

如果是要追加到已有的对话记录文件（如 book-notes 的 chat 文件），用 Python 合并：

```python
# Read existing + new, merge with separator
with open("existing-chat.md", "r") as f:
    existing = f.read()
with open("full-dialog.md", "r") as f:
    new = f.read()

merged = existing.rstrip() + "\n\n---\n[新会话]\n\n" + new
with open("merged-chat.md", "w") as f:
    f.write(merged)
```

### 第5步：清理

导出完成后删除临时 trajectory export 目录（`.openclaw/trajectory-exports/`），避免提交到 git。

## 注意事项

- 导出的是当前 session 的完整对话，不含工具输出（书的内容等）
- 如果前半段在飞书等外部平台，需单独导出合并
- trajectory export 目录较大（events.jsonl 约 11MB），不要提交到 git
- 用户名称和助手名称可根据实际情况替换（User → Ryan, Assistant → 奥创）

## 文件结构

```
book-notes/书名/
├── chat-YYYY-MM-DD.md     ← 完整对话记录（最终产出）
├── notes-YYYY-MM-DD.md    ← 结构化笔记
└── .openclaw/             ← 临时导出目录（不提交git）
    └── trajectory-exports/
```
