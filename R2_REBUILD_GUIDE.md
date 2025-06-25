# R2存储桶重建指南

## 🎯 目标
清空R2存储桶，只上传当前数据库中的89张带标签图片

## 📋 步骤1：清空R2存储桶

### 方法A：使用Cloudflare仪表板（最简单）
1. 登录 [Cloudflare仪表板](https://dash.cloudflare.com/)
2. 进入 R2 > thinkora-pics
3. 选择所有文件
4. 点击删除

### 方法B：使用rclone命令
```bash
# 删除整个存储桶内容（谨慎！）
rclone delete r2:thinkora-pics --rmdirs

# 或者只删除images目录
rclone delete r2:thinkora-pics/images --rmdirs
```

## 📋 步骤2：重新上传图片

### 准备工作
```bash
# 1. 确保rclone已配置
rclone ls r2:thinkora-pics --max-depth 1

# 2. 检查本地文件
python3 scripts/rebuild_r2_storage.py --dry-run
```

### 执行上传
```bash
# 方法1：使用重建脚本
python3 scripts/rebuild_r2_storage.py

# 方法2：直接使用rclone批量上传
rclone copy raw/pixabay r2:thinkora-pics/images --include "*.jpg"
```

## 📋 步骤3：更新数据库URL

更新所有图片URL指向新的R2地址：

```sql
-- 备份数据库
cp thinkora.db thinkora_backup_$(date +%Y%m%d).db

-- 更新URL（在SQLite中执行）
UPDATE images 
SET url_thumbnail = 'https://r2.thinkora.pics/images/' || id || '.jpg',
    url_regular = 'https://r2.thinkora.pics/images/' || id || '.jpg',
    url_download = 'https://r2.thinkora.pics/images/' || id || '.jpg';
```

## 🚀 快速命令序列

```bash
# 1. 清空R2（谨慎！）
rclone delete r2:thinkora-pics --rmdirs

# 2. 创建images目录
rclone mkdir r2:thinkora-pics/images

# 3. 上传所有pixabay图片
rclone copy raw/pixabay r2:thinkora-pics/images \
  --include "*.jpg" \
  --s3-acl public-read \
  --progress

# 4. 验证上传
rclone ls r2:thinkora-pics/images | wc -l
# 应该显示89个文件
```

## ✅ 验证清单

1. **检查R2文件数量**
   ```bash
   rclone size r2:thinkora-pics
   ```

2. **检查数据库**
   ```sql
   SELECT COUNT(*) FROM images;  -- 应该是89
   SELECT COUNT(*) FROM images WHERE tags != '[]';  -- 应该是89
   ```

3. **测试图片访问**
   ```bash
   # 随机测试几个图片URL
   curl -I https://r2.thinkora.pics/images/pixabay_1478822.jpg
   ```

## 🎨 上传后的结果

- **图片数量**: 89张
- **平均标签**: 9.9个/张
- **存储结构**: 
  ```
  thinkora-pics/
  └── images/
      ├── pixabay_1478822.jpg
      ├── pixabay_335965.jpg
      └── ... (共89个文件)
  ```

## 💡 提示

1. **并发上传**：使用 `--transfers 8` 提高上传速度
2. **进度显示**：使用 `--progress` 查看上传进度
3. **日志记录**：使用 `--log-file upload.log` 记录上传日志

这样重建后，你的R2存储将只包含高质量的带标签图片，干净整洁！