#!/usr/bin/env python3
"""
使用环境变量的 Cloudflare R2 迁移脚本
自动读取 .env 文件中的配置
"""

import os
import json
import boto3
from botocore.config import Config
from pathlib import Path
from dotenv import load_dotenv
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 加载环境变量
load_dotenv()

# 从环境变量读取 R2 配置
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY')
R2_SECRET_KEY = os.getenv('R2_SECRET_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME', 'thinkora-images')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

def check_config():
    """检查配置是否完整"""
    required_vars = ['R2_ACCOUNT_ID', 'R2_ACCESS_KEY', 'R2_SECRET_KEY', 'R2_PUBLIC_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        print("请检查 .env 文件中的配置")
        return False
    
    print("✅ 环境变量配置完整")
    print(f"   Account ID: {R2_ACCOUNT_ID[:8]}...")
    print(f"   Access Key: {R2_ACCESS_KEY[:8]}...")
    print(f"   Bucket: {R2_BUCKET_NAME}")
    print(f"   Public URL: {R2_PUBLIC_URL}")
    return True

def create_r2_client():
    """创建 R2 客户端"""
    return boto3.client(
        's3',
        endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(
            signature_version='s3v4',
            retries={'max_attempts': 3}
        ),
        region_name='auto',
        verify=False  # 禁用SSL验证
    )

def upload_images_to_r2():
    """上传所有PNG图片到R2"""
    print(f"\n🚀 开始上传图片到 Cloudflare R2...")
    
    s3 = create_r2_client()
    
    # 检查 bucket 是否存在
    try:
        s3.head_bucket(Bucket=R2_BUCKET_NAME)
        print(f"✅ Bucket 已存在: {R2_BUCKET_NAME}")
    except Exception as e:
        print(f"ℹ️  Bucket 不存在，尝试创建...")
        try:
            s3.create_bucket(Bucket=R2_BUCKET_NAME)
            print(f"✅ 创建 bucket: {R2_BUCKET_NAME}")
        except Exception as e:
            print(f"❌ 创建 bucket 失败: {e}")
            return False
    
    # 上传PNG图片
    png_dir = Path("png")
    if not png_dir.exists():
        print(f"❌ PNG 目录不存在: {png_dir}")
        return False
    
    png_files = list(png_dir.glob('*.png'))
    if not png_files:
        print(f"❌ PNG 目录中没有找到图片文件")
        return False
    
    uploaded_count = 0
    failed_count = 0
    
    print(f"📁 找到 {len(png_files)} 张PNG图片")
    
    for png_file in png_files:
        r2_key = f"images/{png_file.name}"
        
        try:
            # 上传文件
            s3.upload_file(
                str(png_file),
                R2_BUCKET_NAME,
                r2_key,
                ExtraArgs={
                    'ContentType': 'image/png',
                    'CacheControl': 'public, max-age=31536000'  # 1年缓存
                }
            )
            uploaded_count += 1
            print(f"✅ 已上传: {png_file.name}")
        except Exception as e:
            failed_count += 1
            print(f"❌ 上传失败 {png_file.name}: {e}")
    
    print(f"\n📊 上传统计:")
    print(f"   成功: {uploaded_count} 张")
    print(f"   失败: {failed_count} 张")
    
    return uploaded_count > 0

def update_metadata_urls():
    """更新metadata.json中的图片URL为R2 URL"""
    print(f"\n📝 更新 metadata.json...")
    
    # 读取现有metadata
    if not os.path.exists('metadata.json'):
        print("❌ 未找到 metadata.json")
        return False
    
    with open('metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # 更新URL
    updated_count = 0
    for item in metadata:
        image_id = item['id'].replace('unsplash_', '')
        filename = f"{image_id}.png"
        
        # 更新为R2 URL
        r2_url = f"{R2_PUBLIC_URL}/images/{filename}"
        item['urls'] = {
            'thumbnail': r2_url,
            'regular': r2_url,
            'download': r2_url
        }
        updated_count += 1
    
    # 保存更新后的metadata
    with open('metadata_r2.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新 {updated_count} 张图片的URL")
    print(f"📄 新文件: metadata_r2.json")
    return True

def test_r2_access():
    """测试R2访问"""
    print(f"\n🧪 测试 R2 访问...")
    
    try:
        s3 = create_r2_client()
        
        # 测试列出 bucket
        response = s3.list_objects_v2(Bucket=R2_BUCKET_NAME, MaxKeys=1)
        print("✅ R2 连接成功")
        
        # 显示已上传的图片数量
        if 'Contents' in response:
            count = len(response['Contents'])
            print(f"📊 Bucket 中已有 {count} 个文件")
        else:
            print(f"📊 Bucket 为空")
        
        return True
    except Exception as e:
        print(f"❌ R2 连接失败: {e}")
        print(f"💡 这可能是因为 bucket 还不存在，我们将尝试创建它")
        return True  # 继续执行，尝试创建 bucket

def main():
    """主函数"""
    print("🎨 Thinkora.pics R2 迁移工具")
    print("=" * 50)
    
    # 检查配置
    if not check_config():
        return
    
    # 测试连接
    test_r2_access()
    
    # 询问用户是否继续
    png_count = len(list(Path('png').glob('*.png')))
    print(f"\n⚠️  即将上传 {png_count} 张图片到 R2")
    response = input("是否继续? (y/N): ").strip().lower()
    
    if response != 'y':
        print("❌ 已取消")
        return
    
    # 上传图片
    if upload_images_to_r2():
        # 更新metadata
        update_metadata_urls()
        
        print(f"\n🎉 迁移完成!")
        print(f"🌐 图片访问地址: {R2_PUBLIC_URL}/images/")
        print(f"📄 更新后的metadata: metadata_r2.json")
        
        print(f"\n💡 下一步:")
        print(f"1. 检查图片是否正常访问")
        print(f"2. 更新网站中的图片URL")
        print(f"3. 部署到生产环境")
    else:
        print("❌ 迁移失败")

if __name__ == "__main__":
    main() 