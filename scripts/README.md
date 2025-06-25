# 核心脚本说明

本目录包含维护 thinkora.pics 项目所需的核心脚本。

## 📁 保留的脚本 (8个)

### 1. 数据库管理
- **`migrate_to_sqlite.py`** - 将JSON数据迁移到SQLite数据库
- **`clean_and_update_db.py`** - 清理无标签图片，导入新的带标签图片

### 2. 图片获取
- **`fetch_tagged_images.py`** - 从Unsplash和Pixabay获取带标签的高质量图片
  ```bash
  python3 scripts/fetch_tagged_images.py
  ```

### 3. 内容优化
- **`generate_better_titles.py`** - 为图片生成SEO友好的标题和描述
  ```bash
  python3 scripts/generate_better_titles.py
  ```
  
- **`verify_tags.py`** - 验证标签系统，生成标签统计报告
  ```bash
  python3 scripts/verify_tags.py
  ```

### 4. 部署相关
- **`setup_local_images.py`** - 设置本地图片服务（开发环境）
  ```bash
  python3 scripts/setup_local_images.py
  ```
  
- **`restore_r2_urls.py`** - 恢复R2云存储URL（生产环境）
  ```bash
  python3 scripts/restore_r2_urls.py
  # 或指定自定义域名
  python3 scripts/restore_r2_urls.py https://cdn.example.com
  ```

### 5. 维护工具
- **`cleanup_scripts.py`** - 清理不需要的脚本文件
  ```bash
  # 分析模式
  python3 scripts/cleanup_scripts.py
  # 执行清理
  python3 scripts/cleanup_scripts.py --run
  ```

## 🚀 常用工作流程

### 添加新图片
1. 获取带标签的图片: `python3 scripts/fetch_tagged_images.py`
2. 更新数据库: `python3 scripts/clean_and_update_db.py`
3. 生成标题: `python3 scripts/generate_better_titles.py`
4. 验证结果: `python3 scripts/verify_tags.py`

### 本地开发
```bash
python3 scripts/setup_local_images.py
npm run dev
```

### 部署到生产
```bash
# 上传图片到R2后
python3 scripts/restore_r2_urls.py
```

## 📝 注意事项
- 所有已删除的脚本都归档在 `scripts_archive_*` 目录中
- 如需要某个旧脚本，可以从归档目录恢复
- 建议定期运行 `verify_tags.py` 检查数据质量