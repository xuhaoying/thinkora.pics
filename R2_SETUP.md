# Cloudflare R2 设置指南

## 为什么选择静态HTML + R2？

1. **性能最优** - 静态网站 + CDN是最快的组合
2. **成本最低** - R2免费额度很高，静态网站无服务器成本
3. **维护简单** - 无需担心服务器、数据库等复杂问题
4. **扩展性好** - 可以轻松处理大流量

## 设置步骤

### 1. 创建R2 Bucket

1. 登录[Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 R2 Object Storage
3. 创建新的bucket，命名为 `transparent-png-hub`
4. 在bucket设置中启用公开访问

### 2. 获取访问凭证

1. 在R2页面点击"Manage R2 API Tokens"
2. 创建新的API Token
3. 权限选择"Object Read & Write"
4. 记录下：
   - Account ID
   - Access Key ID
   - Secret Access Key
   - Bucket公开URL

### 3. 上传图片到R2

#### 方法1：使用Web界面（推荐新手）
1. 在R2 bucket页面直接上传
2. 创建 `images/` 文件夹
3. 批量上传所有PNG文件

#### 方法2：使用命令行工具
```bash
# 安装rclone
brew install rclone  # macOS
# 或
sudo apt install rclone  # Linux

# 配置rclone
rclone config
# 选择 "s3"
# 输入您的R2凭证

# 批量上传
rclone copy ./png r2:transparent-png-hub/images --progress
```

#### 方法3：使用Python脚本
```bash
pip install boto3
python migrate-to-r2.py
```

### 4. 更新项目配置

1. 编辑 `update-to-r2.js`，设置您的R2公开URL
2. 运行脚本更新metadata.json：
   ```bash
   node update-to-r2.js
   ```

### 5. 部署到Vercel

```bash
git add .
git commit -m "feat: migrate images to Cloudflare R2"
git push
```

## R2 定价优势

- **免费额度**：
  - 10GB存储/月
  - 1000万次请求/月
  - 无出站流量费用！

- **超出免费额度**：
  - 存储：$0.015/GB/月
  - 请求：$0.36/百万次
  - 依然无流量费用

## 性能优化建议

1. **图片优化**
   - 继续使用PNG格式保持透明度
   - 可以考虑生成多种尺寸（缩略图、常规、高清）

2. **缓存策略**
   - R2自动通过Cloudflare CDN分发
   - 设置长期缓存头（已在脚本中配置）

3. **懒加载**
   - 已在index.html中实现
   - 确保良好的用户体验

## 为什么不需要Next.js？

1. **静态内容** - 您的图片和metadata都是静态的
2. **无需SSR** - 搜索和筛选在客户端完成就很快
3. **简单维护** - 纯HTML/JS更容易理解和修改
4. **部署容易** - Vercel对静态网站有最好的支持
5. **性能最优** - 静态网站永远是最快的

## 未来扩展

如果将来需要动态功能，可以考虑：
- **Cloudflare Workers** - 处理API请求
- **Cloudflare D1** - 如果需要数据库
- **保持前端静态** - 只在需要时添加API

这样可以保持网站的高性能和低成本优势！