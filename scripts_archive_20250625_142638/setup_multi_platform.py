#!/usr/bin/env python3
"""
多平台下载器快速设置脚本
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """创建.env文件"""
    env_content = """# 多平台图片下载器环境变量配置

# Unsplash API密钥
# 获取地址: https://unsplash.com/developers
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here

# Pexels API密钥  
# 获取地址: https://www.pexels.com/api/
PEXELS_API_KEY=your_pexels_api_key_here

# Pixabay API密钥
# 获取地址: https://pixabay.com/api/docs/
PIXABAY_API_KEY=your_pixabay_api_key_here

# 注意：
# 1. 填入你的实际API密钥
# 2. 至少需要配置一个平台的密钥
# 3. 所有平台都支持免费商用和二次创作
"""
    
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️ .env文件已存在，跳过创建")
        return
    
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ 已创建.env文件")
    print("📝 请编辑.env文件，填入你的API密钥")

def check_dependencies():
    """检查依赖"""
    try:
        import requests
        import dotenv
        import rembg
        import PIL
        import onnxruntime
        print("✅ 所有依赖包已安装")
        return True
    except ImportError as e:
        missing_module = str(e).split("'")[1]
        
        package_map = {
            "dotenv": "python-dotenv",
            "PIL": "pillow"
        }
        
        package_name = package_map.get(missing_module, missing_module)
        
        print(f"❌ 缺少依赖包: {package_name}")
        print("💡 请运行以下命令安装:")
        print("   pip install requests python-dotenv rembg pillow onnxruntime")
        return False

def create_directories():
    """创建必要目录"""
    directories = ["raw", "png", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ 已创建必要目录")

def show_api_instructions():
    """显示API密钥获取说明"""
    print("\n🔑 API密钥获取说明:")
    print("=" * 50)
    
    print("\n1. Unsplash (推荐)")
    print("   - 访问: https://unsplash.com/developers")
    print("   - 注册开发者账户")
    print("   - 创建应用获取Access Key")
    print("   - 免费，每小时50个请求")
    
    print("\n2. Pexels")
    print("   - 访问: https://www.pexels.com/api/")
    print("   - 注册账户")
    print("   - 获取API Key")
    print("   - 免费，每小时200个请求")
    
    print("\n3. Pixabay")
    print("   - 访问: https://pixabay.com/api/docs/")
    print("   - 注册账户")
    print("   - 获取API Key")
    print("   - 免费，每小时5000个请求")
    
    print("\n" + "=" * 50)

def show_usage_examples():
    """显示使用示例"""
    print("\n🎯 使用示例:")
    print("=" * 50)
    
    print("\n# 查看状态")
    print("python unsplash/multi_platform_downloader.py --status")
    
    print("\n# 下载20张图片")
    print("python unsplash/multi_platform_downloader.py --download 20")
    
    print("\n# 处理图片（去背景）")
    print("python unsplash/multi_platform_downloader.py --process")
    
    print("\n# 指定平台下载")
    print("python unsplash/multi_platform_downloader.py --platform pexels --download 10")
    
    print("\n# 查看帮助")
    print("python unsplash/multi_platform_downloader.py --help")
    
    print("\n" + "=" * 50)

def main():
    print("🚀 多平台透明PNG下载器设置向导")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 创建目录
    create_directories()
    
    # 创建.env文件
    create_env_file()
    
    # 显示API获取说明
    show_api_instructions()
    
    # 显示使用示例
    show_usage_examples()
    
    print("\n✅ 设置完成！")
    print("📝 下一步：编辑.env文件，填入你的API密钥")
    print("🎯 然后就可以开始下载图片了！")

if __name__ == "__main__":
    main() 