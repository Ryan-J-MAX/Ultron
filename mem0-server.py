"""Mem0 记忆服务 — 给奥创用的记忆后端

运行方式:
    python3 mem0-server.py

然后通过 MCP 或者直接调用 Memory 实例来操作记忆。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mem0 import Memory
from mem0_config import config  # type: ignore

# 初始化
print("正在初始化 Mem0 记忆服务...")
memory = Memory.from_config(config)
print("✅ Mem0 已就绪")

# 测试连接
try:
    result = memory.search("测试", user_id="ryan", limit=1)
    print(f"✅ 搜索测试通过 (结果数: {len(result.get('results', []))})")
except Exception as e:
    print(f"⚠️ 搜索测试: {e} (可能是首次运行，向量库为空)")

# 便捷函数
def add_memory(text, user_id="ryan"):
    """添加记忆"""
    result = memory.add(text, user_id=user_id)
    return result

def search_memory(query, user_id="ryan", limit=5):
    """搜索记忆"""
    result = memory.search(query, user_id=user_id, limit=limit)
    return result

def get_all_memories(user_id="ryan"):
    """获取所有记忆"""
    result = memory.get_all(user_id=user_id)
    return result

def delete_memory(memory_id):
    """删除记忆"""
    result = memory.delete(memory_id=memory_id)
    return result

if __name__ == "__main__":
    print("\nMem0 记忆服务已就绪。")
    print("可用函数: add_memory(), search_memory(), get_all_memories(), delete_memory()")
    print("\n按 Ctrl+C 退出")
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n已退出")