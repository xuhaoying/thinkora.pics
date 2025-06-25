# Cloudflare R2 CORS配置详细指南

## 步骤1：登录Cloudflare控制台

1. 访问 https://dash.cloudflare.com/
2. 登录你的账户
3. 在左侧菜单找到 **R2** 并点击

## 步骤2：进入存储桶设置

1. 点击你的存储桶名称 `thinkora-images`
2. 点击顶部的 **Settings** 标签

## 步骤3：配置CORS（最简单方案）

在CORS Policy部分，使用以下**最简化配置**：

```json
[
  {
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"]
  }
]
```

### 如果上述配置报错，尝试以下几种格式：

#### 方案A：不使用数组包裹
```json
{
  "AllowedOrigins": ["*"],
  "AllowedMethods": ["GET", "HEAD"],
  "AllowedHeaders": ["*"]
}
```

#### 方案B：只配置必需字段
```json
[
  {
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET"]
  }
]
```

#### 方案C：指定具体域名
```json
[
  {
    "AllowedOrigins": [
      "https://thinkora.pics",
      "https://www.thinkora.pics"
    ],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"]
  }
]
```

## 步骤4：如果CORS配置仍然失败

### 选项1：使用Transform Rules（推荐）

1. 返回到主Cloudflare控制台
2. 选择你的域名 `thinkora.pics`
3. 进入 **Rules** → **Transform Rules** → **Modify Response Header**
4. 点击 **Create rule**
5. 配置如下：

**Rule name**: `Add CORS Headers`

**If** (匹配条件):
- Field: `Hostname`
- Operator: `equals`
- Value: `img.thinkora.pics`

**Then** (执行操作):
- Action: `Add`
- Header name: `Access-Control-Allow-Origin`
- Value: `*`

点击 **Deploy** 保存规则。

### 选项2：使用Page Rules

1. 在域名控制台进入 **Rules** → **Page Rules**
2. 创建新规则：
   - URL: `img.thinkora.pics/*`
   - Settings: 
     - Cache Level: `Cache Everything`
     - Edge Cache TTL: `1 month`

### 选项3：创建Cloudflare Worker

如果以上都不行，可以创建一个Worker来处理CORS：

1. 进入 **Workers & Pages**
2. 创建新Worker
3. 使用以下代码：

```javascript
export default {
  async fetch(request, env) {
    // 获取原始响应
    const response = await fetch(request);
    
    // 创建新响应并添加CORS头
    const newHeaders = new Headers(response.headers);
    newHeaders.set('Access-Control-Allow-Origin', '*');
    newHeaders.set('Access-Control-Allow-Methods', 'GET, HEAD');
    newHeaders.set('Access-Control-Allow-Headers', '*');
    
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders
    });
  }
};
```

4. 部署Worker并绑定到 `img.thinkora.pics` 路由

## 验证配置

配置完成后，使用以下命令验证：

```bash
curl -I https://img.thinkora.pics/images/pixabay_business_1051697.png
```

应该看到类似以下的响应头：
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, HEAD
```

## 常见问题

### 1. "Invalid JSON" 错误
- 确保JSON格式正确，没有多余的逗号
- 使用在线JSON验证器检查格式

### 2. "Invalid CORS configuration" 错误
- 尝试只使用最基本的字段
- 不要包含可选字段如 `MaxAgeSeconds`、`ExposeHeaders`

### 3. 保存后仍然无法下载
- 等待5-10分钟让配置在全球CDN生效
- 清除浏览器缓存后重试
- 使用隐私模式测试

## 临时解决方案

如果所有配置都失败，图片下载功能仍然可以通过以下方式工作：
1. 用户可以右键"另存为"保存图片
2. 点击图片会在新标签页打开，然后保存
3. 使用浏览器扩展绕过CORS限制

## 需要帮助？

如果配置仍有问题：
1. 截图错误信息
2. 尝试使用最简单的配置 `{"AllowedOrigins": ["*"], "AllowedMethods": ["GET"]}`
3. 联系Cloudflare支持，说明是R2 CORS配置问题