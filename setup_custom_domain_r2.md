# R2自定义域名设置指南

如果默认的R2公开URL有问题，可以设置自定义域名作为替代方案。

## 🌐 方案：设置自定义域名

### 1. 在Cloudflare中添加自定义域名

1. **进入R2 bucket设置**
   - Cloudflare Dashboard → R2 → thinkora-images
   - 点击 "Settings" 标签

2. **添加自定义域名**
   - 找到 "Custom Domains" 部分
   - 点击 "Connect Domain"
   - 输入域名，如: `images.thinkora.pics`

3. **配置DNS**
   - 如果域名在Cloudflare托管，会自动添加CNAME记录
   - 如果不是，需要手动添加CNAME记录：
     ```
     CNAME images.thinkora.pics -> [Cloudflare提供的目标]
     ```

### 2. 更新项目配置

```bash
# 更新 .env 文件
R2_PUBLIC_URL=https://images.thinkora.pics

# 重新生成网站
python3 generate_image_pages.py
```

## 🚀 快速替代方案

如果需要立即修复，也可以：

1. **使用免费的图床服务**暂时托管图片
2. **设置Vercel的静态文件服务**
3. **使用GitHub Pages托管图片**

## 📞 联系Cloudflare支持

如果R2公开URL仍然无法工作，建议：
1. 联系Cloudflare支持
2. 检查账户是否有R2的完整权限
3. 确认没有防火墙规则阻止访问