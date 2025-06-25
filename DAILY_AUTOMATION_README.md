# Thinkora.pics 每日自动化系统

## 🚀 概述

这是一个完整的自动化系统，用于每天从多个图片平台获取图片、处理背景移除、并上传到Cloudflare R2。

## 📋 功能特性

1. **多平台图片获取**
   - 支持 Unsplash、Pexels、Pixabay
   - 智能去重，避免重复下载
   - 自动轮换搜索关键词

2. **自动背景移除**
   - 使用 AI 模型移除背景
   - 质量评分系统
   - 透明度比例计算
   - 低质量图片自动过滤

3. **R2 自动上传**
   - 批量上传到 Cloudflare R2
   - 自动生成缩略图
   - 更新网站元数据
   - 触发网站重新生成

4. **监控和报告**
   - 每日执行报告
   - 性能图表生成
   - 错误追踪
   - 邮件通知（可选）

## 🛠️ 安装设置

### 1. 环境准备

```bash
# 克隆代码后，进入项目目录
cd thinkora.pics

# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
nano .env
```

### 2. 安装依赖

```bash
# 使用 pip 安装依赖
pip install -r requirements.txt

# 或者使用 pip3
pip3 install -r requirements.txt
```

### 3. 运行设置脚本

```bash
# 给脚本执行权限
chmod +x setup_daily_automation.sh

# 运行设置脚本
./setup_daily_automation.sh
```

## 📝 配置说明

### API 密钥配置

在 `.env` 文件中配置以下内容：

```env
# 图片平台 API
UNSPLASH_ACCESS_KEY=your_key_here
PEXELS_API_KEY=your_key_here
PIXABAY_API_KEY=your_key_here

# Cloudflare R2
R2_ENDPOINT=https://your-account-id.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_key_here
R2_SECRET_ACCESS_KEY=your_secret_here
R2_BUCKET=thinkora-images
R2_PUBLIC_URL=https://your-bucket.r2.dev
```

### 定时任务配置

系统默认在每天凌晨 2:00 执行，可以在 `daily_pipeline.py` 中修改：

```python
# 修改执行时间
schedule.every().day.at("02:00").do(pipeline.run_pipeline)

# 添加多个执行时间
schedule.every().day.at("08:00").do(pipeline.run_pipeline)
schedule.every().day.at("20:00").do(pipeline.run_pipeline)
```

## 🚀 使用方法

### 立即运行一次

```bash
python3 daily_pipeline.py --now
```

### 启动定时任务

```bash
python3 daily_pipeline.py
```

### 查看监控面板

```bash
python3 monitor_dashboard.py
```

### 单独运行各个模块

```bash
# 只获取图片
python3 daily_fetch_images.py

# 只处理图片
python3 daily_process_images.py

# 只上传到 R2
python3 daily_upload_to_r2.py
```

## 📊 监控和日志

### 日志位置

- 每日执行日志：`logs/daily_pipeline_YYYYMMDD.log`
- 获取日志：`logs/daily_fetch_YYYYMMDD.log`
- 处理日志：`logs/daily_process_YYYYMMDD.log`
- 上传日志：`logs/daily_upload_YYYYMMDD.log`

### 报告位置

- 每日报告：`reports/daily_report_YYYYMMDD.json`
- 错误报告：`reports/error_report_YYYYMMDD_HHMMSS.json`
- 监控面板：`reports/dashboard.html`
- 性能图表：`reports/performance_chart.png`

## 🔧 故障排除

### 常见问题

1. **API 限制错误**
   - 检查 API 密钥是否正确
   - 确认 API 配额是否用完
   - 调整每次获取的图片数量

2. **背景移除失败**
   - 确保安装了 rembg 和依赖
   - 检查内存是否充足
   - 降低并发处理数量

3. **R2 上传失败**
   - 验证 R2 凭证是否正确
   - 检查网络连接
   - 确认 bucket 权限设置

4. **定时任务不执行**
   - 检查 cron 服务是否运行
   - 验证 Python 路径是否正确
   - 查看 cron 日志

### 调试命令

```bash
# 查看 cron 任务
crontab -l

# 查看最新日志
tail -f logs/daily_pipeline_$(date +%Y%m%d).log

# 检查环境变量
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('UNSPLASH_ACCESS_KEY'))"
```

## 📈 性能优化

### 调整并发数

在各个脚本中调整 `max_workers` 参数：

```python
# 处理图片时的并发数
processor.run_daily_processing(max_workers=4)

# 上传文件时的并发数
uploader.run_daily_upload(max_workers=4)
```

### 调整获取数量

修改每个平台获取的图片数量：

```python
# 在 daily_pipeline.py 中
fetcher.run_daily_fetch(images_per_platform=10)
```

## 🔒 安全建议

1. **保护 API 密钥**
   - 不要将 `.env` 文件提交到版本控制
   - 定期轮换 API 密钥
   - 使用环境变量而非硬编码

2. **限制访问**
   - 设置 R2 bucket 的适当权限
   - 使用防火墙规则限制访问
   - 监控异常访问模式

3. **备份策略**
   - 定期备份处理后的图片
   - 保存元数据的多个版本
   - 设置 R2 的版本控制

## 📞 支持

如有问题，请查看：
- 项目文档：[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- 日志文件：`logs/` 目录
- 监控面板：运行 `python3 monitor_dashboard.py`

---

Happy Automating! 🎉