# 修复 Cloudflare R2 公开访问问题

## 🚨 问题诊断

当前图片无法在网站上显示，原因是：
1. R2 bucket 没有配置公开访问
2. 使用的公开 URL 格式可能不正确

## 🔧 解决方案

### 方案 1: 配置 R2 公开访问 (推荐)

1. **登录 Cloudflare Dashboard**
   - 访问 https://dash.cloudflare.com
   - 进入 R2 Object Storage

2. **配置 Bucket 公开访问**
   ```
   1. 选择 "thinkora-images" bucket
   2. 点击 "Settings" 标签
   3. 找到 "Public access" 部分
   4. 点击 "Allow Access" 
   5. 确认启用公开访问
   ```

3. **获取正确的公开 URL**
   - 配置完成后，Cloudflare 会提供公开访问 URL
   - 格式通常是: `https://pub-[random].r2.dev`
   - 记录这个正确的 URL

4. **更新环境变量**
   ```bash
   # 在 .env 文件中更新
   R2_PUBLIC_URL=https://你的正确公开URL
   ```

### 方案 2: 配置自定义域名 (可选)

如果你有自己的域名，可以配置自定义域名：

1. **添加自定义域名**
   ```
   1. 在 R2 bucket 设置中
   2. 点击 "Custom Domains"
   3. 添加如: images.thinkora.pics
   4. 配置 DNS CNAME 记录
   ```

2. **更新 DNS**
   ```
   CNAME images.thinkora.pics -> pub-484484e3162047379f59bcbb36fb442a.r2.dev
   ```

## 🚀 快速测试脚本

运行以下命令测试配置：

```bash
# 测试公开访问
python3 test_r2_urls.py

# 重新生成网站（使用正确URL）
python3 generate_image_pages.py
```

## 📝 临时解决方案

如果需要立即修复，可以：

1. **手动设置正确的公开URL**
2. **重新上传图片到正确路径**
3. **更新元数据文件**

```bash
# 运行修复脚本
python3 fix_public_urls.py
```