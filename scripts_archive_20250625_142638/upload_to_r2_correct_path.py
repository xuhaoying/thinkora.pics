#!/usr/bin/env python3
"""
正确上传图片到R2，确保路径匹配
"""

import os
import boto3
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('.env')

# R2配置
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME', 'thinkora')

def get_r2_client():
    """创建R2客户端"""
    return boto3.client(
        service_name='s3',
        endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        region_name='auto'
    )

def upload_images_with_correct_paths():
    """上传图片到R2，使用正确的路径"""
    
    s3_client = get_r2_client()
    uploaded_count = 0
    
    # 1. 上传旧图片（100张）
    png_dir = Path("png")
    if png_dir.exists():
        for png_file in png_dir.glob("*.png"):
            # R2路径：images/filename.png
            r2_key = f"images/{png_file.name}"
            
            try:
                print(f"📤 上传: {png_file.name} -> {r2_key}")
                s3_client.upload_file(
                    str(png_file),
                    R2_BUCKET_NAME,
                    r2_key,
                    ExtraArgs={
                        'ContentType': 'image/png',
                        'CacheControl': 'public, max-age=31536000'
                    }
                )
                uploaded_count += 1
            except Exception as e:
                print(f"❌ 上传失败 {png_file.name}: {str(e)}")
    
    # 2. 上传新图片（6张）
    for platform in ["unsplash", "pexels", "pixabay"]:
        platform_dir = png_dir / platform
        if platform_dir.exists():
            for png_file in platform_dir.glob("*.png"):
                # 提取图片ID（去掉平台前缀）
                image_id = png_file.stem.replace(f"{platform}_", "")
                # R2路径：images/id.png
                r2_key = f"images/{image_id}.png"
                
                try:
                    print(f"📤 上传: {png_file.name} -> {r2_key}")
                    s3_client.upload_file(
                        str(png_file),
                        R2_BUCKET_NAME,
                        r2_key,
                        ExtraArgs={
                            'ContentType': 'image/png',
                            'CacheControl': 'public, max-age=31536000'
                        }
                    )
                    uploaded_count += 1
                except Exception as e:
                    print(f"❌ 上传失败 {png_file.name}: {str(e)}")
    
    print(f"\n✅ 成功上传 {uploaded_count} 张图片到R2")
    
    # 3. 验证上传
    verify_uploads(s3_client)

def verify_uploads(s3_client):
    """验证图片是否正确上传"""
    
    print("\n🔍 验证上传的图片...")
    
    try:
        response = s3_client.list_objects_v2(
            Bucket=R2_BUCKET_NAME,
            Prefix='images/',
            MaxKeys=10
        )
        
        if 'Contents' in response:
            print(f"📊 找到 {len(response['Contents'])} 个文件:")
            for obj in response['Contents']:
                print(f"  ✅ {obj['Key']} - {obj['Size']} bytes")
        else:
            print("❌ 未找到任何文件")
    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")

def list_r2_structure():
    """列出R2中的完整结构"""
    
    s3_client = get_r2_client()
    
    print("\n📂 R2 Bucket 结构:")
    print("=" * 50)
    
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=R2_BUCKET_NAME)
        
        file_count = 0
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    print(f"  {obj['Key']} ({obj['Size']} bytes)")
                    file_count += 1
        
        print(f"\n📊 总文件数: {file_count}")
    except Exception as e:
        print(f"❌ 列出文件失败: {str(e)}")

if __name__ == "__main__":
    print("🚀 开始上传图片到R2...")
    print("=" * 50)
    
    if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY, R2_SECRET_KEY]):
        print("❌ 请先配置R2环境变量")
        print("需要设置: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY")
        exit(1)
    
    # 1. 上传图片
    upload_images_with_correct_paths()
    
    # 2. 列出完整结构
    list_r2_structure()
    
    print("\n💡 下一步:")
    print("1. 在Cloudflare Dashboard中确认Public Access已启用")
    print("2. 测试公开URL: https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/0V3uVjouHRc.png")
    print("3. 如果可以访问，运行: python fix_r2_urls.py 来更新所有URL")