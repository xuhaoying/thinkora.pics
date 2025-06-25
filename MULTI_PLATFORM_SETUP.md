# 多平台透明PNG下载器设置指南

## 🚀 功能特性

- **多平台支持**: Unsplash、Pexels、Pixabay
- **自动去背景**: 使用AI技术移除图片背景
- **智能去重**: 避免重复下载相同图片
- **版权安全**: 所有平台都支持免费商用和二次创作
- **批量处理**: 支持批量下载和处理

## 📋 前置要求

1. **Python 3.8+**
2. **虚拟环境** (推荐)
3. **API密钥** (至少一个平台)

## 🔧 安装步骤

### 1. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 2. 安装依赖
```bash
pip install requests python-dotenv rembg pillow onnxruntime
```

### 3. 配置API密钥

#### 获取API密钥

**Unsplash** (推荐)
- 访问: https://unsplash.com/developers
- 注册开发者账户
- 创建应用获取Access Key
- 免费，每小时50个请求

**Pexels**
- 访问: https://www.pexels.com/api/
- 注册账户
- 获取API Key
- 免费，每小时200个请求

**Pixabay**
- 访问: https://pixabay.com/api/docs/
- 注册账户
- 获取API Key
- 免费，每小时5000个请求

#### 创建.env文件
```bash
cp env_example.txt .env
```

编辑`.env`文件，填入你的API密钥：
```env
UNSPLASH_ACCESS_KEY=your_actual_unsplash_key
PEXELS_API_KEY=your_actual_pexels_key
PIXABAY_API_KEY=your_actual_pixabay_key
```

## 🎯 使用方法

### 基本命令

```bash
# 查看帮助
python unsplash/multi_platform_downloader.py --help

# 查看状态
python unsplash/multi_platform_downloader.py --status

# 下载图片
python unsplash/multi_platform_downloader.py --download 20

# 处理图片（去背景）
python unsplash/multi_platform_downloader.py --process

# 指定平台下载
python unsplash/multi_platform_downloader.py --platform pexels --download 10
```

### 高级用法

#### 1. 批量下载
```bash
# 下载50张图片（自动轮换平台）
python unsplash/multi_platform_downloader.py --download 50
```

#### 2. 指定平台
```bash
# 只从Pexels下载
python unsplash/multi_platform_downloader.py --platform pexels --download 20

# 只从Pixabay下载
python unsplash/multi_platform_downloader.py --platform pixabay --download 20
```

#### 3. 处理图片
```bash
# 处理所有未处理的图片
python unsplash/multi_platform_downloader.py --process
```

## 📊 输出文件

### 目录结构
```
project/
├── raw/           # 原始图片 (JPG)
├── png/           # 透明背景图片 (PNG)
├── logs/          # 日志文件
├── metadata.json  # 图片元数据
├── download_state.json  # 下载状态
└── downloaded_ids.json  # 已下载ID列表
```

### 元数据格式
```json
{
  "pexels_12345": {
    "id": "pexels_12345",
    "title": "Beautiful Image",
    "author": "Photographer Name",
    "platform": "pexels",
    "original_url": "https://www.pexels.com/photo/...",
    "width": 1920,
    "height": 1080,
    "tags": ["transparent", "png", "design"],
    "copyright": {
      "platform": "pexels",
      "license": "pexels_license",
      "attribution_required": false,
      "commercial_allowed": true,
      "modification_allowed": true
    }
  }
}
```

## 🔄 工作流程

1. **搜索图片**: 使用关键词搜索各平台
2. **质量检查**: 过滤低质量图片
3. **下载图片**: 保存到raw目录
4. **记录元数据**: 保存版权和使用信息
5. **去背景处理**: 生成透明PNG
6. **状态更新**: 记录下载和处理状态

## ⚠️ 注意事项

### API限制
- **Unsplash**: 每小时50个请求
- **Pexels**: 每小时200个请求  
- **Pixabay**: 每小时5000个请求

### 版权信息
- 所有平台都支持免费商用
- 允许二次创作和修改
- 建议保留原作者信息

### 文件管理
- 原始图片保存在`raw/`目录
- 透明PNG保存在`png/`目录
- 元数据保存在`metadata.json`

## 🛠️ 故障排除

### 常见问题

**1. API密钥错误**
```
❌ 错误：请在.env文件中设置至少一个平台的API密钥
```
**解决方案**: 检查`.env`文件中的API密钥是否正确

**2. 依赖缺失**
```
ModuleNotFoundError: No module named 'requests'
```
**解决方案**: 运行`pip install requests python-dotenv rembg pillow onnxruntime`

**3. API限制**
```
⏰ API限制已达上限，需等待 XX 分钟
```
**解决方案**: 等待一小时后重试，或使用其他平台

**4. 图片处理失败**
```
❌ 处理失败: 图片文件损坏
```
**解决方案**: 删除损坏的图片文件，重新下载

## 📈 性能优化

### 1. 并行处理
```python
# 可以修改代码支持多线程下载
import threading
from concurrent.futures import ThreadPoolExecutor
```

### 2. 缓存优化
```python
# 使用Redis缓存API响应
import redis
```

### 3. 批量处理
```python
# 批量处理图片提高效率
def batch_process_images(image_list, batch_size=10):
    # 实现批量处理逻辑
    pass
```

## 🔮 未来扩展

### 1. 更多平台
- Freepik (付费)
- Flaticon (付费)
- 用户上传

### 2. AI增强
- 自动标签生成
- 智能分类
- 质量评分

### 3. 搜索优化
- 语义搜索
- 视觉搜索
- 标签推荐

## 📞 支持

如果遇到问题，请检查：
1. API密钥是否正确
2. 网络连接是否正常
3. 依赖是否完整安装
4. 文件权限是否正确

## 📄 许可证

本项目遵循MIT许可证。所有下载的图片遵循各自平台的版权政策。 