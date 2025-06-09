#!/bin/bash

# Pre-commit安全检查脚本
echo "🔍 运行安全检查..."

# 检查是否意外提交了敏感文件
if git diff --cached --name-only | grep -E "\.env$|\.env\..*|.*\.key$|.*\.pem$"; then
    echo "❌ 错误: 发现敏感文件即将被提交!"
    echo "请检查以下文件:"
    git diff --cached --name-only | grep -E "\.env$|\.env\..*|.*\.key$|.*\.pem$"
    exit 1
fi

# 检查提交内容中的敏感信息
if git diff --cached | grep -i -E "(api_key|secret|password|token|private.*key)" | grep -v -E "(your_.*_here|example|placeholder|template)"; then
    echo "❌ 错误: 发现敏感信息即将被提交!"
    echo "请检查以下内容:"
    git diff --cached | grep -i -E "(api_key|secret|password|token|private.*key)" | grep -v -E "(your_.*_here|example|placeholder|template)"
    exit 1
fi

# 检查.gitignore是否包含必要的排除项
if ! grep -q "\.env" .gitignore; then
    echo "❌ 错误: .gitignore缺少.env配置!"
    exit 1
fi

# 检查是否存在.env文件但未被忽略
if [ -f ".env" ] && ! git check-ignore .env > /dev/null 2>&1; then
    echo "❌ 错误: .env文件存在但未被Git忽略!"
    exit 1
fi

echo "✅ 安全检查通过!"
exit 0