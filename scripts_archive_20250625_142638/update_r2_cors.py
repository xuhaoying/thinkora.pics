#!/usr/bin/env python3
"""
更新R2存储桶的CORS配置以支持跨域下载
"""

import boto3
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('.env') or load_dotenv('unsplash/.env')

def update_cors_configuration():
    """更新R2的CORS配置"""
    
    # R2配置
    r2_endpoint = os.getenv('R2_ENDPOINT')
    r2_access_key = os.getenv('R2_ACCESS_KEY_ID')
    r2_secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    r2_bucket = os.getenv('R2_BUCKET')
    
    # 创建S3客户端
    s3_client = boto3.client(
        's3',
        endpoint_url=r2_endpoint,
        aws_access_key_id=r2_access_key,
        aws_secret_access_key=r2_secret_key
    )
    
    # CORS配置
    cors_configuration = {
        'CORSRules': [
            {
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'HEAD'],
                'AllowedOrigins': [
                    'https://thinkora.pics',
                    'https://www.thinkora.pics',
                    'http://localhost:*',
                    'http://127.0.0.1:*',
                    'file://*'  # 用于本地测试
                ],
                'ExposeHeaders': [
                    'Content-Length',
                    'Content-Type',
                    'Content-Disposition',
                    'ETag'
                ],
                'MaxAgeSeconds': 3600
            }
        ]
    }
    
    try:
        # 获取当前CORS配置
        print("📋 Checking current CORS configuration...")
        try:
            current_cors = s3_client.get_bucket_cors(Bucket=r2_bucket)
            print("Current CORS configuration:")
            print(json.dumps(current_cors['CORSRules'], indent=2))
        except s3_client.exceptions.NoSuchCORSConfiguration:
            print("No CORS configuration found.")
        except Exception as e:
            print(f"Error getting CORS: {e}")
        
        # 更新CORS配置
        print("\n🔄 Updating CORS configuration...")
        s3_client.put_bucket_cors(
            Bucket=r2_bucket,
            CORSConfiguration=cors_configuration
        )
        
        print("✅ CORS configuration updated successfully!")
        print("\nNew CORS configuration:")
        print(json.dumps(cors_configuration['CORSRules'], indent=2))
        
    except Exception as e:
        print(f"❌ Error updating CORS: {e}")
        print("\nNote: Cloudflare R2 might not support CORS configuration via S3 API.")
        print("You may need to configure CORS in the Cloudflare dashboard:")
        print("1. Go to Cloudflare Dashboard > R2")
        print("2. Select your bucket")
        print("3. Go to Settings > CORS")
        print("4. Add the following allowed origins:")
        print("   - https://thinkora.pics")
        print("   - https://www.thinkora.pics")

if __name__ == "__main__":
    update_cors_configuration()