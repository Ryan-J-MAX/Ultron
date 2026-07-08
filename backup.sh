#!/bin/bash
# 奥创记忆备份脚本 — 每天自动同步到 Ryan-J-MAX/Ultron
# 备份内容: workspace 文件 + memory/ + mem0_qdrant/ + 配置(脱敏)

set -e

REPO_DIR="/Users/construct/.openclaw/workspace/Ultron"
REPO_URL="https://github.com/Ryan-J-MAX/Ultron.git"
WORKSPACE="/Users/construct/.openclaw/workspace"
MEM0_DATA="/Users/construct/.openclaw/mem0_qdrant"
OPENCLAW_CONFIG="/Users/construct/.openclaw/openclaw.json"

# 首次运行时 clone
if [ ! -d "$REPO_DIR/.git" ]; then
    mkdir -p "$REPO_DIR"
    git clone "$REPO_URL" "$REPO_DIR"
fi

# 拉取最新
cd "$REPO_DIR"
git pull -q origin main 2>/dev/null || true

# 同步 workspace 文件
cp "$WORKSPACE/MEMORY.md" "$REPO_DIR/MEMORY.md"
cp "$WORKSPACE/SOUL.md" "$REPO_DIR/SOUL.md" 2>/dev/null || true
cp "$WORKSPACE/IDENTITY.md" "$REPO_DIR/IDENTITY.md" 2>/dev/null || true
cp "$WORKSPACE/AGENTS.md" "$REPO_DIR/AGENTS.md" 2>/dev/null || true
cp "$WORKSPACE/USER.md" "$REPO_DIR/USER.md" 2>/dev/null || true
cp "$WORKSPACE/TOOLS.md" "$REPO_DIR/TOOLS.md" 2>/dev/null || true
cp "$WORKSPACE/HEARTBEAT.md" "$REPO_DIR/HEARTBEAT.md" 2>/dev/null || true

# 同步 memory 目录
rm -rf "$REPO_DIR/memory"
cp -r "$WORKSPACE/memory" "$REPO_DIR/memory"

# 同步 Mem0 向量数据
rm -rf "$REPO_DIR/mem0_qdrant"
cp -r "$MEM0_DATA" "$REPO_DIR/mem0_qdrant" 2>/dev/null || true

# 同步工具脚本
cp "$WORKSPACE/mem0_cli.py" "$REPO_DIR/mem0_cli.py" 2>/dev/null || true
cp "$WORKSPACE/mem0_config.py" "$REPO_DIR/mem0_config.py" 2>/dev/null || true
cp "$WORKSPACE/mem0-server.py" "$REPO_DIR/mem0-server.py" 2>/dev/null || true
cp "$WORKSPACE/backup.sh" "$REPO_DIR/backup.sh" 2>/dev/null || true

# 脱敏处理 mem0_config.py 和 openclaw.json
if [ -f "$REPO_DIR/mem0_config.py" ]; then
    sed -i '' 's/ARK_API_KEY = "[^"]*"/ARK_API_KEY = "***REMOVED***"/' "$REPO_DIR/mem0_config.py"
fi
if [ -f "$OPENCLAW_CONFIG" ]; then
    sed -E 's/"apiKey": *"[^"]+"/"apiKey": "***REMOVED***"/g; s/"appSecret": *"[^"]+"/"appSecret": "***REMOVED***"/g; s/"token": *"[^"]+"/"token": "***REMOVED***"/g' "$OPENCLAW_CONFIG" > "$REPO_DIR/openclaw.json"
fi

# 添加 .gitignore
cat > "$REPO_DIR/.gitignore" << 'EOF'
# 不要在 GitHub 上暴露密钥
*secret*
*api_key*
*.key
EOF

# Git 提交
git add -A

if git diff --cached --quiet; then
    echo "[$(date '+%Y-%m-%d %H:%M')] 无变化，跳过"
    exit 0
fi

DATE=$(date '+%Y-%m-%d %H:%M')
git commit -m "备份 $DATE" -q
git push -q origin main

echo "[$(date '+%Y-%m-%d %H:%M')] 备份完成 ✅"