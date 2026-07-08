"""Mem0 配置 — 使用火山引擎 DeepSeek V4 + Doubao Embedding"""
import os

# 火山引擎 API 配置
ARK_API_KEY = "***REMOVED***"
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "deepseek-v4-pro",
            "openai_base_url": ARK_BASE_URL,
            "api_key": ARK_API_KEY,
            "temperature": 0.1,
            "max_tokens": 2000,
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "doubao-embedding-vision",
            "openai_base_url": ARK_BASE_URL,
            "api_key": ARK_API_KEY,
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": os.path.expanduser("~/.openclaw/mem0_qdrant"),
            "on_disk": True,
            "embedding_model_dims": 2048,
        }
    },
    "history_db_path": os.path.expanduser("~/.openclaw/mem0_history.db"),
}