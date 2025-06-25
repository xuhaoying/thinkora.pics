# Cloudflare R2 图片存储设置指南

## 为什么选择 Cloudflare R2？

### 成本对比
| 服务 | 存储费用 | 流量费用 | 请求费用 | 免费额度 |
|------|----------|----------|----------|----------|
| **Cloudflare R2** | $0.015/GB/月 | **免费** | $0.36/百万次 | 10GB + 1000万次 |
| AWS S3 | $0.023/GB/月 | $0.09/GB | $0.005/1000次 | 5GB + 20000次 |
| Google Cloud Storage | $0.020/GB/月 | $0.12/GB | $0.004/10000次 | 5GB + 50000次 |
| Azure Blob | $0.018/GB/月 | $0.087/GB | $0.004/10000次 | 5GB + 20000次 |

### 性能优势
- 全球CDN分发，访问速度快
- 无流量费用，适合图片密集型应用
- 自动缓存优化

## 设置步骤

### 1. 创建 Cloudflare 账户
1. 访问 [Cloudflare.com](https://cloudflare.com)
2. 注册账户并验证邮箱
3. 添加您的域名（可选，用于自定义域名）

### 2. 创建 R2 Bucket
1. 登录 Cloudflare Dashboard
2. 进入 "R2 Object Storage"
3. 点击 "Create bucket"
4. 输入 bucket 名称：`thinkora-images`
5. 选择区域（建议选择离用户最近的区域）

### 3. 配置公开访问
1. 在 bucket 设置中启用 "Public bucket"
2. 记录下公开访问URL（格式：`https://xxx.r2.dev`）

### 4. 创建 API Token
1. 在 R2 页面点击 "Manage R2 API Tokens"
2. 点击 "Create API token"
3. 选择 "Custom token"
4. 权限设置：
   - Object Read & Write
   - 选择刚创建的 bucket
5. 记录下：
   - Account ID
   - Access Key ID
   - Secret Access Key

### 5. 上传图片

#### 方法1：使用提供的Python脚本
```bash
# 安装依赖
pip install boto3

# 编辑配置
vim migrate-to-r2.py
# 更新以下配置：
# R2_ACCOUNT_ID = "your-account-id"
# R2_ACCESS_KEY = "your-access-key"
# R2_SECRET_KEY = "your-secret-key"
# R2_BUCKET_NAME = "thinkora-images"
# R2_PUBLIC_URL = "https://your-bucket.r2.dev"

# 运行迁移
python migrate-to-r2.py
```

#### 方法2：使用 rclone（推荐）
```bash
# 安装 rclone
brew install rclone  # macOS
# 或
sudo apt install rclone  # Linux

# 配置 rclone
rclone config
# 选择 "s3"
# 输入您的R2凭证

# 上传图片
rclone copy ./png r2:thinkora-images/images --progress
```

### 6. 更新项目配置
```bash
# 更新 metadata.json 中的图片URL
node update-to-r2.js
```

## 最佳实践

### 1. 图片优化
- 保持PNG格式以支持透明背景
- 考虑生成多种尺寸：
  - 缩略图：200x200px
  - 常规：800x800px
  - 高清：1200x1200px

### 2. 缓存策略
```javascript
// 设置长期缓存
const cacheHeaders = {
  'Cache-Control': 'public, max-age=31536000', // 1年
  'Content-Type': 'image/png'
};
```

### 3. 懒加载
```html
<img src="placeholder.png" 
     data-src="https://your-bucket.r2.dev/images/image.png"
     loading="lazy"
     alt="Coloring page">
```

### 4. 错误处理
```javascript
// 图片加载失败时的处理
function handleImageError(img) {
  img.src = '/fallback-image.png';
  img.alt = 'Image not available';
}
```

## 监控和维护

### 1. 使用量监控
- 在 Cloudflare Dashboard 查看 R2 使用量
- 设置使用量告警

### 2. 成本控制
- 定期清理未使用的图片
- 监控请求次数，避免超出免费额度

### 3. 备份策略
- 定期备份 metadata.json
- 考虑跨区域备份重要图片

## 扩展建议

### 1. 自定义域名
```bash
# 在 Cloudflare 中设置自定义域名
# 例如：images.thinkora.pics
# 需要先添加域名到 Cloudflare
```

### 2. 图片处理
```javascript
// 使用 Cloudflare Images 进行实时处理
const imageUrl = `https://imagedelivery.net/account/image-id/width=800,height=800`;
```

### 3. 防盗链设置
```javascript
// 在 R2 中设置 Referer 白名单
const refererPolicy = {
  'Referer': 'https://thinkora.pics/*'
};
```

## 故障排除

### 常见问题
1. **上传失败**：检查 API Token 权限
2. **访问慢**：检查 CDN 缓存设置
3. **费用过高**：检查是否有异常请求

### 联系支持
- Cloudflare 支持：https://support.cloudflare.com
- R2 文档：https://developers.cloudflare.com/r2/

## 总结

Cloudflare R2 是目前最适合您项目的图片存储解决方案：
- ✅ 成本最低（无流量费用）
- ✅ 性能最优（全球CDN）
- ✅ 设置简单（兼容S3 API）
- ✅ 扩展性好（支持自定义域名）

建议立即开始迁移，以降低存储成本并提升用户体验！ 