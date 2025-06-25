# Cloudflare R2 CORS配置指南

为了让图片下载功能正常工作，需要在Cloudflare R2中配置CORS（跨域资源共享）。

## 配置步骤

1. **登录Cloudflare控制台**
   - 访问 https://dash.cloudflare.com/
   - 登录你的账户

2. **进入R2存储**
   - 在左侧菜单中找到"R2"
   - 点击你的存储桶名称（thinkora-images）

3. **配置CORS规则**
   - 进入"Settings"（设置）标签
   - 找到"CORS Policy"（CORS策略）部分
   - 添加以下配置：

```json
[
  {
    "AllowedOrigins": [
      "https://thinkora.pics",
      "https://www.thinkora.pics",
      "http://localhost:*"
    ],
    "AllowedMethods": [
      "GET",
      "HEAD"
    ],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": [
      "Content-Length",
      "Content-Type",
      "Content-Disposition",
      "ETag"
    ],
    "MaxAgeSeconds": 3600
  }
]
```

4. **保存配置**
   - 点击"Save"保存配置
   - 配置会立即生效

## 当前下载解决方案

即使没有配置CORS，网站仍然提供了以下下载方式：

1. **直接下载尝试** - 使用HTML5 download属性
2. **新标签页打开** - 用户可以右键保存图片
3. **Blob下载** - 如果CORS配置正确，会提供更好的下载体验

## 测试下载功能

打开 `test-download.html` 文件来测试不同的下载方法：
```bash
open test-download.html
```

## 注意事项

- CORS配置可能需要几分钟才能在全球CDN节点生效
- 某些浏览器可能会因为安全策略限制跨域下载
- 用户始终可以通过右键"另存为"来保存图片