# R2存储桶清理指南

## 📊 清理概况
- **需要删除**: 106张无标签的旧图片
- **需要保留**: 89张有标签的新图片
- **删除比例**: 54.4%

## 🗑️ 需要删除的图片ID列表

已生成以下文件：
- `r2_delete_list.json` - 完整的删除清单
- `r2_files_to_delete.txt` - 所有可能的文件路径

主要是以下格式的旧图片：
- `unsplash_*` 开头的图片（无标签）
- 部分 `pexels_*` 图片（如果无标签）

## 🛠️ 删除方法

### 方法1：使用Cloudflare仪表板（推荐）
1. 登录 [Cloudflare仪表板](https://dash.cloudflare.com/)
2. 进入 R2 > thinkora-pics 存储桶
3. 使用搜索/筛选功能找到 `unsplash_` 开头的文件
4. 批量选择并删除

### 方法2：使用rclone（命令行）
```bash
# 1. 安装rclone
brew install rclone

# 2. 配置rclone
rclone config
# 选择 "n" 新建
# 名称: r2
# 类型: 选择 "Amazon S3 Compliant Storage Providers"
# 提供商: 选择 "Cloudflare R2"
# 输入你的 access_key_id 和 secret_access_key
# 区域: auto
# 端点: https://你的账户ID.r2.cloudflarestorage.com

# 3. 测试连接
rclone ls r2:thinkora-pics --max-depth 1

# 4. 删除文件（先用--dry-run测试）
rclone delete r2:thinkora-pics --include-from r2_files_to_delete.txt --dry-run

# 5. 确认后实际删除
rclone delete r2:thinkora-pics --include-from r2_files_to_delete.txt
```

### 方法3：使用AWS CLI
```bash
# 1. 安装AWS CLI
brew install awscli

# 2. 配置
aws configure
# Access Key ID: 你的R2 access key
# Secret Access Key: 你的R2 secret key
# Region: auto
# Output format: json

# 3. 删除单个文件
aws s3 rm s3://thinkora-pics/images/unsplash_xxx.png \
  --endpoint-url https://你的账户ID.r2.cloudflarestorage.com

# 4. 批量删除
while read file; do
  aws s3 rm "s3://thinkora-pics/$file" \
    --endpoint-url https://你的账户ID.r2.cloudflarestorage.com
done < r2_files_to_delete.txt
```

### 方法4：使用Cloudflare API
```bash
# 使用Cloudflare API批量删除
# 需要你的账户ID和API Token

ACCOUNT_ID="你的账户ID"
API_TOKEN="你的API_TOKEN"
BUCKET_NAME="thinkora-pics"

# 删除单个对象
curl -X DELETE \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/r2/buckets/$BUCKET_NAME/objects/images/unsplash_xxx.png" \
  -H "Authorization: Bearer $API_TOKEN"
```

## ⚠️ 注意事项

1. **先备份**: 虽然这些是无标签的旧图片，但建议先确认
2. **分批删除**: 如果文件很多，建议分批删除
3. **验证结果**: 删除后检查网站是否正常显示

## ✅ 删除后验证

删除完成后，运行以下命令验证：
```bash
# 检查数据库状态
sqlite3 thinkora.db "SELECT COUNT(*) as total, 
  SUM(CASE WHEN tags != '[]' THEN 1 ELSE 0 END) as with_tags 
  FROM images"

# 应该显示: 89 | 89
```

## 🎯 保留的图片特征
- 所有 `pixabay_` 开头的新图片（有标签）
- 都有至少3个标签
- 平均每张图片9.9个标签

这样清理后，你的R2存储空间将只保留高质量的带标签图片！