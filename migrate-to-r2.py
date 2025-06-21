#!/usr/bin/env python3
"""
将PNG图片迁移到Cloudflare R2存储
"""

import os
import json
import boto3
from botocore.config import Config

# Cloudflare R2配置
R2_ACCOUNT_ID = "your-account-id"
R2_ACCESS_KEY = "your-access-key"
R2_SECRET_KEY = "your-secret-key"
R2_BUCKET_NAME = "transparent-png-hub"
R2_PUBLIC_URL = "https://your-r2-public-url.r2.dev"

# 创建S3客户端（R2兼容S3 API）
def create_r2_client():
    return boto3.client(
        's3',
        endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )

def upload_images_to_r2():
    """上传所有PNG图片到R2"""
    s3 = create_r2_client()
    
    # 创建bucket（如果不存在）
    try:
        s3.create_bucket(Bucket=R2_BUCKET_NAME)
        print(f"✅ Created bucket: {R2_BUCKET_NAME}")
    except:
        print(f"ℹ️ Bucket already exists: {R2_BUCKET_NAME}")
    
    # 上传PNG图片
    png_dir = "png"
    uploaded_count = 0
    
    for filename in os.listdir(png_dir):
        if filename.endswith('.png'):
            local_path = os.path.join(png_dir, filename)
            r2_key = f"images/{filename}"
            
            try:
                # 上传文件
                s3.upload_file(
                    local_path,
                    R2_BUCKET_NAME,
                    r2_key,
                    ExtraArgs={
                        'ContentType': 'image/png',
                        'CacheControl': 'public, max-age=31536000'  # 1年缓存
                    }
                )
                uploaded_count += 1
                print(f"✅ Uploaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to upload {filename}: {e}")
    
    print(f"\n✅ Successfully uploaded {uploaded_count} images to R2")
    return uploaded_count

def update_metadata_urls():
    """更新metadata.json中的图片URL为R2 URL"""
    # 读取现有metadata
    with open('metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # 更新URL
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
    
    # 保存更新后的metadata
    with open('metadata_r2.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print("✅ Created metadata_r2.json with R2 URLs")

def generate_upload_script():
    """生成简单的上传脚本（不依赖boto3）"""
    script = """#!/bin/bash
# 使用rclone上传图片到Cloudflare R2
# 首先需要配置rclone: rclone config

# 上传所有PNG图片
rclone copy ./png r2:transparent-png-hub/images --progress

# 设置公开访问权限
rclone settier r2:transparent-png-hub/images Standard

echo "✅ Upload complete!"
"""
    
    with open('upload-to-r2.sh', 'w') as f:
        f.write(script)
    
    os.chmod('upload-to-r2.sh', 0o755)
    print("✅ Created upload-to-r2.sh script")

if __name__ == "__main__":
    print("🚀 Starting migration to Cloudflare R2...")
    
    # 如果有boto3，使用Python上传
    try:
        import boto3
        upload_images_to_r2()
        update_metadata_urls()
    except ImportError:
        print("⚠️ boto3 not installed. Creating bash upload script instead...")
        generate_upload_script()
        print("\nTo upload images:")
        print("1. Install rclone: brew install rclone")
        print("2. Configure R2: rclone config")
        print("3. Run: ./upload-to-r2.sh")