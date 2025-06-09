# 🚀 AI故事工厂 - 安全部署指南

## ⚠️ 重要安全提醒

**绝对不要将真实的API密钥提交到代码仓库！**

## 📋 环境变量配置

### 本地开发环境

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，添加你的真实API密钥：
```bash
# AI故事工厂环境变量配置

# Replicate API配置 (必需)
VITE_REPLICATE_API_TOKEN=你的真实API密钥

# 可选配置
VITE_DEMO_MODE=false
VITE_APP_URL=http://localhost:5174
```

## 🌐 部署选项

### 选项1：Vercel (推荐)

1. **连接GitHub仓库**
   ```bash
   # 确保敏感信息已被清理
   git add .gitignore
   git commit -m "docs: 更新安全配置"
   git push origin main
   ```

2. **在Vercel配置环境变量**
   - 访问 [vercel.com](https://vercel.com)
   - 导入你的GitHub仓库
   - 在 Settings > Environment Variables 中添加：
     ```
     VITE_REPLICATE_API_TOKEN = 你的Replicate API密钥
     VITE_DEMO_MODE = false
     ```

3. **部署**
   - Vercel会自动构建和部署
   - 每次推送到main分支都会自动重新部署

### 选项2：Netlify

1. **配置环境变量**
   - 在Netlify Dashboard > Site Settings > Environment Variables
   - 添加所有必要的环境变量

2. **构建设置**
   - Build command: `npm run build`
   - Publish directory: `dist`

### 选项3：自托管 (Docker)

创建 `docker-compose.yml`：
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - VITE_REPLICATE_API_TOKEN=${VITE_REPLICATE_API_TOKEN}
      - VITE_DEMO_MODE=${VITE_DEMO_MODE}
    env_file:
      - .env.production
```

## 🔒 安全最佳实践

### API密钥管理

1. **获取Replicate API密钥**
   ```bash
   # 访问 https://replicate.com/account/api-tokens
   # 创建新的API token
   # 复制密钥（格式：r8_xxxxxx）
   ```

2. **密钥权限设置**
   - 只授予必要的权限
   - 定期轮换API密钥
   - 监控API使用情况

3. **成本控制**
   ```bash
   # 在Replicate设置使用限制
   # 监控每月API调用次数
   # 设置预算警报
   ```

### Git安全

1. **检查提交历史**
   ```bash
   # 检查是否意外提交了敏感信息
   git log --oneline -p | grep -i "api\|key\|secret\|password"
   ```

2. **如果已经提交敏感信息**
   ```bash
   # 立即使用 git filter-branch 清理历史
   git filter-branch --env-filter '
   if [ "$GIT_COMMIT" = "commit_hash_with_secrets" ]
   then
       export GIT_AUTHOR_EMAIL="your-email@example.com"
       export GIT_COMMITTER_EMAIL="your-email@example.com"
   fi' -- --all
   
   # 强制推送（慎用！）
   git push --force-with-lease origin main
   ```

3. **预提交检查**
   ```bash
   # 安装预提交钩子防止意外提交敏感信息
   npm install --save-dev @commitlint/cli @commitlint/config-conventional
   ```

## 🚨 紧急响应

### 如果API密钥泄露

1. **立即撤销密钥**
   - 登录Replicate控制台
   - 删除泄露的API密钥
   - 生成新的API密钥

2. **更新部署环境**
   - 在Vercel/Netlify中更新环境变量
   - 重新部署应用

3. **监控异常使用**
   - 检查API使用日志
   - 监控意外的费用

## 📱 域名和SSL

### 自定义域名 (Vercel)
```bash
# 在Vercel Dashboard添加自定义域名
# 配置DNS记录：
# A记录: @ -> 76.76.19.61
# CNAME记录: www -> cname.vercel-dns.com
```

### SSL证书
- Vercel/Netlify自动提供免费SSL证书
- 确保所有流量都通过HTTPS

## 🔍 监控和分析

### 性能监控
```javascript
// 在生产环境中添加错误监控
if (import.meta.env.PROD) {
  // 集成 Sentry 或其他监控工具
}
```

### API使用监控
- 设置Replicate使用警报
- 监控响应时间和错误率
- 跟踪用户使用模式

## 💡 开发提示

1. **本地测试**
   ```bash
   # 使用演示模式测试
   npm run dev
   
   # 添加真实API密钥测试AI功能
   echo "VITE_REPLICATE_API_TOKEN=你的密钥" >> .env
   ```

2. **构建检查**
   ```bash
   npm run build
   npm run preview
   ```

3. **类型检查**
   ```bash
   npx tsc --noEmit
   ```

记住：**安全第一，永远不要在代码中硬编码敏感信息！**