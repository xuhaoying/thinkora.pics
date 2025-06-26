# Thinkora Pics 脚本系统文档

## 📋 概述

这是一个全新的、模块化的脚本管理系统，用于管理 Thinkora Pics 透明PNG图片网站的所有操作。系统设计遵循单一职责原则，每个脚本都有明确的功能边界。

## 🏗️ 架构设计

```
scripts_new/
├── core/           # 核心管理脚本
├── images/         # 图片相关操作
├── database/       # 数据库管理
├── deployment/     # 部署和云存储
├── utils/          # 工具和检查
└── README.md       # 本文档
```

## 🚀 快速开始

### 1. 环境配置

创建 `.env` 文件：

```env
# API密钥
UNSPLASH_ACCESS_KEY=your_unsplash_access_key
PIXABAY_API_KEY=your_pixabay_api_key

# Cloudflare R2 配置
R2_ACCESS_KEY_ID=your_r2_access_key
R2_SECRET_ACCESS_KEY=your_r2_secret_key
R2_ACCOUNT_ID=your_r2_account_id
R2_BUCKET_NAME=thinkora-pics
R2_PUBLIC_URL=https://img.thinkora.pics
```

### 2. 安装依赖

```bash
pip install requests pillow rembg boto3 python-dotenv
```

### 3. 系统检查

```bash
python3 scripts_new/utils/health_check.py
```

## 📚 脚本详细说明

### Core - 核心管理 (`core/`)

#### `manager.py` - 主控制脚本
统一的入口点，管理所有操作流程。

**功能：**
- 协调各个模块的脚本执行
- 提供完整的图片处理流水线
- 统一的错误处理和日志记录

**使用方法：**
```bash
# 查看帮助
python3 scripts_new/core/manager.py --help

# 获取50张图片
python3 scripts_new/core/manager.py fetch --count 50 --source both

# 处理图片（去背景）
python3 scripts_new/core/manager.py process --batch-size 20

# 上传到R2
python3 scripts_new/core/manager.py upload

# 运行完整流水线
python3 scripts_new/core/manager.py pipeline --count 30

# 系统健康检查
python3 scripts_new/core/manager.py health

# 备份数据库
python3 scripts_new/core/manager.py backup
```

### Images - 图片操作 (`images/`)

#### `fetch.py` - 图片获取脚本
从 Unsplash 和 Pixabay 获取高质量图片。

**特性：**
- 支持多种图片来源
- 智能关键词分类
- 自动去重检查
- 质量评分和筛选

**使用方法：**
```bash
# 从两个平台各获取50张图片
python3 scripts_new/images/fetch.py --count 100 --source both

# 只从Unsplash获取
python3 scripts_new/images/fetch.py --count 50 --source unsplash

# 只从Pixabay获取
python3 scripts_new/images/fetch.py --count 50 --source pixabay
```

#### `process.py` - 图片处理脚本
下载原图并使用AI技术去除背景，生成透明PNG。

**特性：**
- 使用 rembg AI 技术
- 多线程并行处理
- 自动错误恢复
- 处理进度跟踪

**使用方法：**
```bash
# 处理50张图片，使用4个线程
python3 scripts_new/images/process.py --batch-size 50 --workers 4

# 查看处理统计
python3 scripts_new/images/process.py --stats
```

### Database - 数据库管理 (`database/`)

#### `backup.py` - 数据库管理脚本
数据库备份、恢复和优化功能。

**功能：**
- 自动备份数据库
- 备份文件管理
- 数据库恢复
- 性能优化

**使用方法：**
```bash
# 创建备份
python3 scripts_new/database/backup.py backup

# 列出所有备份
python3 scripts_new/database/backup.py list

# 恢复指定备份
python3 scripts_new/database/backup.py restore backups/images_backup_20250625_120000.db

# 清理旧备份，保留最新10个
python3 scripts_new/database/backup.py cleanup --keep 10

# 查看数据库信息
python3 scripts_new/database/backup.py info

# 优化数据库
python3 scripts_new/database/backup.py optimize
```

### Deployment - 部署管理 (`deployment/`)

#### `upload_r2.py` - R2存储上传脚本
将处理后的PNG图片上传到Cloudflare R2存储。

**特性：**
- 并发上传优化
- 断点续传支持
- 自动URL同步
- 上传进度跟踪

**使用方法：**
```bash
# 批量上传待上传的图片
python3 scripts_new/deployment/upload_r2.py

# 强制重新上传所有图片
python3 scripts_new/deployment/upload_r2.py --force

# 使用10个并发线程上传
python3 scripts_new/deployment/upload_r2.py --workers 10

# 查看上传统计
python3 scripts_new/deployment/upload_r2.py --stats

# 同步数据库中的URL
python3 scripts_new/deployment/upload_r2.py --sync-urls
```

### Utils - 工具脚本 (`utils/`)

#### `health_check.py` - 系统健康检查
全面的系统状态检查工具。

**检查项目：**
- 数据库连接和内容
- 环境变量配置
- Python依赖包
- 目录结构
- R2存储连接
- API密钥有效性
- 网站运行状态

**使用方法：**
```bash
python3 scripts_new/utils/health_check.py
```

## 🔄 完整工作流程

### 1. 日常图片更新流程

```bash
# 1. 系统检查
python3 scripts_new/utils/health_check.py

# 2. 运行完整流水线（获取100张图片）
python3 scripts_new/core/manager.py pipeline --count 100

# 3. 检查结果
python3 scripts_new/images/process.py --stats
python3 scripts_new/deployment/upload_r2.py --stats
```

### 2. 维护和备份流程

```bash
# 1. 备份数据库
python3 scripts_new/database/backup.py backup

# 2. 清理旧备份
python3 scripts_new/database/backup.py cleanup --keep 10

# 3. 优化数据库
python3 scripts_new/database/backup.py optimize

# 4. 健康检查
python3 scripts_new/utils/health_check.py
```

### 3. 紧急恢复流程

```bash
# 1. 列出可用备份
python3 scripts_new/database/backup.py list

# 2. 恢复最新备份
python3 scripts_new/database/backup.py restore backups/images_backup_YYYYMMDD_HHMMSS.db

# 3. 同步R2 URL
python3 scripts_new/deployment/upload_r2.py --sync-urls

# 4. 验证系统状态
python3 scripts_new/utils/health_check.py
```

## 📊 数据库结构

```sql
CREATE TABLE images (
    id TEXT PRIMARY KEY,              -- 图片唯一标识
    title TEXT NOT NULL,              -- 图片标题
    description TEXT,                 -- 图片描述
    tags TEXT,                        -- 标签（JSON格式）
    url_thumbnail TEXT,               -- 缩略图URL
    url_regular TEXT,                 -- 常规尺寸URL
    width INTEGER,                    -- 图片宽度
    height INTEGER,                   -- 图片高度
    likes INTEGER DEFAULT 0,          -- 点赞数
    author TEXT,                      -- 作者
    author_url TEXT,                  -- 作者链接
    source TEXT,                      -- 来源（unsplash/pixabay）
    created_at TEXT,                  -- 创建时间
    processed BOOLEAN DEFAULT FALSE,  -- 是否已处理
    uploaded BOOLEAN DEFAULT FALSE,   -- 是否已上传
    processed_at TEXT,                -- 处理时间
    uploaded_at TEXT,                 -- 上传时间
    processed_path TEXT               -- 处理后文件路径
);
```

## 🛠️ 配置说明

### 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `UNSPLASH_ACCESS_KEY` | 是 | Unsplash API访问密钥 |
| `PIXABAY_API_KEY` | 是 | Pixabay API密钥 |
| `R2_ACCESS_KEY_ID` | 是 | Cloudflare R2访问密钥ID |
| `R2_SECRET_ACCESS_KEY` | 是 | Cloudflare R2私钥 |
| `R2_ACCOUNT_ID` | 是 | Cloudflare账户ID |
| `R2_BUCKET_NAME` | 否 | R2存储桶名称（默认：thinkora-pics） |
| `R2_PUBLIC_URL` | 否 | R2公开访问URL（默认：https://img.thinkora.pics） |

### 目录结构

```
项目根目录/
├── scripts_new/           # 新脚本系统
├── processed_images/      # 处理后的PNG图片
├── backups/              # 数据库备份
├── logs/                 # 日志文件
├── images.db             # 主数据库
└── .env                  # 环境变量配置
```

## 🔧 故障排除

### 常见问题

1. **"❌ 请安装rembg"**
   ```bash
   pip install rembg
   ```

2. **"❌ R2连接测试失败"**
   - 检查 `.env` 文件中的R2配置
   - 确认网络连接正常

3. **"❌ API响应错误"**
   - 检查API密钥是否有效
   - 确认API配额未超限

4. **数据库锁定错误**
   ```bash
   # 停止所有相关进程，然后重试
   pkill -f "python.*scripts_new"
   ```

### 性能优化建议

1. **并发设置**
   - 图片处理：建议4-8个线程
   - R2上传：建议5-10个线程

2. **批处理大小**
   - 小内存环境：20-50张图片/批
   - 充足内存：50-100张图片/批

3. **网络优化**
   - 使用稳定的网络连接
   - 避免在网络高峰期运行大批量任务

## 📈 监控和日志

### 日志文件位置
- 健康检查报告：`logs/health_check_*.json`
- 处理日志：各脚本的标准输出
- 数据库备份信息：`backups/*.json`

### 监控指标
- 图片获取成功率
- 处理成功率
- 上传成功率
- 数据库大小变化
- R2存储使用量

## 🔄 版本更新

### 从旧脚本迁移

1. **备份现有数据**
   ```bash
   python3 scripts_new/database/backup.py backup
   ```

2. **移除旧脚本目录**
   ```bash
   rm -rf scripts/  # 旧的scripts目录
   ```

3. **使用新脚本系统**
   ```bash
   python3 scripts_new/core/manager.py health
   ```

### 脚本更新

脚本系统支持平滑更新，更新时：
1. 先运行健康检查
2. 备份数据库
3. 更新脚本文件
4. 再次运行健康检查确认

## 📞 支持

如果遇到问题：

1. 首先运行健康检查：`python3 scripts_new/utils/health_check.py`
2. 查看相关日志文件
3. 检查环境变量配置
4. 确认网络连接和API配额

---

**注意：** 这是全新的脚本系统，相比旧版本有以下优势：
- ✅ 模块化设计，易于维护
- ✅ 统一的错误处理
- ✅ 完整的健康检查
- ✅ 自动化备份和恢复
- ✅ 详细的文档和示例