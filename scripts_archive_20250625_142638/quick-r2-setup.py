#!/usr/bin/env python3
"""
快速设置 Cloudflare R2 图片存储
交互式配置和自动上传
"""

import os
import json
import sys
from pathlib import Path

def get_user_input():
    """获取用户输入的R2配置"""
    print("🚀 Cloudflare R2 快速设置")
    print("=" * 50)
    
    config = {}
    
    print("\n1. 请从 Cloudflare Dashboard 获取以下信息：")
    print("   - 访问 https://dash.cloudflare.com/")
    print("   - 进入 R2 Object Storage")
    print("   - 创建新的 bucket")
    print("   - 创建 API Token")
    
    config['account_id'] = input("\n请输入 Account ID: ").strip()
    config['access_key'] = input("请输入 Access Key ID: ").strip()
    config['secret_key'] = input("请输入 Secret Access Key: ").strip()
    config['bucket_name'] = input("请输入 Bucket 名称 (默认: thinkora-images): ").strip() or "thinkora-images"
    config['public_url'] = input("请输入 Bucket 公开URL (格式: https://xxx.r2.dev): ").strip()
    
    return config

def create_env_file(config):
    """创建环境变量文件"""
    env_content = f"""# Cloudflare R2 配置
R2_ACCOUNT_ID={config['account_id']}
R2_ACCESS_KEY={config['access_key']}
R2_SECRET_KEY={config['secret_key']}
R2_BUCKET_NAME={config['bucket_name']}
R2_PUBLIC_URL={config['public_url']}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ 已创建 .env 文件")

def update_migrate_script(config):
    """更新迁移脚本配置"""
    script_path = 'migrate-to-r2.py'
    
    if not os.path.exists(script_path):
        print("❌ 未找到 migrate-to-r2.py 文件")
        return
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # 更新配置
    content = content.replace('R2_ACCOUNT_ID = "your-account-id"', f'R2_ACCOUNT_ID = "{config["account_id"]}"')
    content = content.replace('R2_ACCESS_KEY = "your-access-key"', f'R2_ACCESS_KEY = "{config["access_key"]}"')
    content = content.replace('R2_SECRET_KEY = "your-secret-key"', f'R2_SECRET_KEY = "{config["secret_key"]}"')
    content = content.replace('R2_BUCKET_NAME = "transparent-png-hub"', f'R2_BUCKET_NAME = "{config["bucket_name"]}"')
    content = content.replace('R2_PUBLIC_URL = "https://your-r2-public-url.r2.dev"', f'R2_PUBLIC_URL = "{config["public_url"]}"')
    
    with open(script_path, 'w') as f:
        f.write(content)
    
    print("✅ 已更新 migrate-to-r2.py 配置")

def check_dependencies():
    """检查依赖"""
    try:
        import boto3
        print("✅ boto3 已安装")
        return True
    except ImportError:
        print("❌ boto3 未安装")
        print("请运行: pip install boto3")
        return False

def estimate_costs():
    """估算成本"""
    png_dir = Path('png')
    if not png_dir.exists():
        print("❌ 未找到 png 目录")
        return
    
    total_size = 0
    file_count = 0
    
    for png_file in png_dir.glob('*.png'):
        total_size += png_file.stat().st_size
        file_count += 1
    
    size_gb = total_size / (1024**3)
    
    print(f"\n📊 存储估算:")
    print(f"   图片数量: {file_count}")
    print(f"   总大小: {size_gb:.2f} GB")
    print(f"   月存储费用: ${size_gb * 0.015:.4f}")
    print(f"   免费额度: 10GB (足够使用!)")
    
    if size_gb > 10:
        print(f"   ⚠️  超出免费额度: {size_gb - 10:.2f} GB")
        print(f"   额外费用: ${(size_gb - 10) * 0.015:.4f}/月")

def create_upload_script():
    """创建上传脚本"""
    script_content = """#!/bin/bash
# 自动上传图片到 Cloudflare R2

echo "🚀 开始上传图片到 Cloudflare R2..."

# 检查 rclone 是否安装
if ! command -v rclone &> /dev/null; then
    echo "❌ rclone 未安装"
    echo "请先安装: brew install rclone (macOS) 或 sudo apt install rclone (Linux)"
    exit 1
fi

# 检查配置
if [ ! -f ~/.config/rclone/rclone.conf ]; then
    echo "❌ rclone 未配置"
    echo "请先运行: rclone config"
    exit 1
fi

# 上传图片
echo "📤 上传图片..."
rclone copy ./png r2:thinkora-images/images --progress

# 设置缓存
echo "⚙️  设置缓存策略..."
rclone settier r2:thinkora-images/images Standard

echo "✅ 上传完成!"
echo "🌐 图片访问地址: https://your-bucket.r2.dev/images/"
"""
    
    with open('upload-images.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('upload-images.sh', 0o755)
    print("✅ 已创建 upload-images.sh 脚本")

def main():
    """主函数"""
    print("🎨 Thinkora.pics 图片存储设置")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 估算成本
    estimate_costs()
    
    # 获取用户配置
    config = get_user_input()
    
    # 创建配置文件
    create_env_file(config)
    update_migrate_script(config)
    create_upload_script()
    
    print("\n🎉 设置完成!")
    print("\n下一步:")
    print("1. 运行: python migrate-to-r2.py")
    print("2. 或者运行: ./upload-images.sh")
    print("3. 更新网站中的图片URL")
    
    print("\n💡 提示:")
    print("- 所有图片将通过 Cloudflare CDN 分发")
    print("- 无流量费用，访问速度快")
    print("- 支持全球访问")

if __name__ == "__main__":
    main() 