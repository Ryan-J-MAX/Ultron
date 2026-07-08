#!/usr/bin/env python3
"""Mem0 CLI — 给奥创用的命令行记忆工具

用法:
    python3 mem0_cli.py add "Ryan 喜欢喝咖啡" [--user ryan]
    python3 mem0_cli.py search "Ryan 喜欢什么" [--user ryan] [--limit 5]
    python3 mem0_cli.py list [--user ryan] [--limit 20]
    python3 mem0_cli.py delete <memory_id>
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mem0 import Memory
from mem0_config import config

# 抑制日志
import logging
logging.disable(logging.CRITICAL)

# 抑制 PostHog
os.environ["POSTHOG_DISABLED"] = "1"

_memory = None

def get_memory():
    global _memory
    if _memory is None:
        _memory = Memory.from_config(config)
    return _memory

def cmd_add(args):
    text = args[0]
    user_id = "ryan"
    for i, a in enumerate(args):
        if a == "--user" and i + 1 < len(args):
            user_id = args[i + 1]
    m = get_memory()
    result = m.add(text, user_id=user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def cmd_search(args):
    query = ""
    user_id = "ryan"
    limit = 5
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--user" and i + 1 < len(args):
            i += 1
            user_id = args[i]
        elif a == "--limit" and i + 1 < len(args):
            i += 1
            limit = int(args[i])
        else:
            query += a + " "
        i += 1
    query = query.strip()
    m = get_memory()
    result = m.search(query, filters={"user_id": user_id}, limit=limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def cmd_list(args):
    user_id = "ryan"
    limit = 20
    for i, a in enumerate(args):
        if a == "--user" and i + 1 < len(args):
            user_id = args[i + 1]
        elif a == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
    m = get_memory()
    result = m.get_all(filters={"user_id": user_id}, limit=limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def cmd_delete(args):
    memory_id = args[0]
    m = get_memory()
    result = m.delete(memory_id=memory_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

COMMANDS = {
    "add": cmd_add,
    "search": cmd_search,
    "list": cmd_list,
    "delete": cmd_delete,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: mem0_cli.py <add|search|list|delete> [...]", file=sys.stderr)
        print("  add '文本' [--user ryan]", file=sys.stderr)
        print("  search '查询' [--user ryan] [--limit 5]", file=sys.stderr)
        print("  list [--user ryan] [--limit 20]", file=sys.stderr)
        print("  delete <memory_id>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)

    COMMANDS[cmd](sys.argv[2:])