#!/usr/bin/env python3
"""
修复R2公开访问问题
"""

import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()

def check_bucket_policy():
    """检查bucket公开访问策略"""
    s3_client = boto3.client(
        's3',
        endpoint_url=os.getenv('R2_ENDPOINT'),
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        region_name='auto'
    )
    
    bucket_name = os.getenv('R2_BUCKET')
    
    try:
        # 检查当前策略
        response = s3_client.get_bucket_policy(Bucket=bucket_name)
        print("当前bucket策略:")
        print(response['Policy'])
    except Exception as e:
        print(f"获取bucket策略失败: {e}")
        
        # 设置公开读取策略
        public_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        
        try:
            s3_client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(public_policy)
            )
            print("✅ 已设置公开读取策略")
        except Exception as e:
            print(f"❌ 设置公开策略失败: {e}")

def test_file_access():
    """测试文件访问"""
    import requests
    
    # 测试一些已知文件
    test_urls = [
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/0V3uVjouHRc.png",
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/unsplash/unsplash_GZUwekngRYM.png"
    ]
    
    for url in test_urls:
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - 可访问")
            else:
                print(f"❌ {url} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - 错误: {e}")

def list_recent_files():
    """列出最近上传的文件"""
    s3_client = boto3.client(
        's3',
        endpoint_url=os.getenv('R2_ENDPOINT'),
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        region_name='auto'
    )
    
    bucket_name = os.getenv('R2_BUCKET')
    
    print("\n最近上传的文件:")
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix='images/',
        MaxKeys=10
    )
    
    for obj in response.get('Contents', []):
        print(f"  {obj['Key']} ({obj['Size']} bytes)")

if __name__ == "__main__":
    print("=== R2访问检查和修复 ===\n")
    
    print("1. 检查bucket策略...")
    check_bucket_policy()
    
    print("\n2. 列出最近文件...")
    list_recent_files()
    
    print("\n3. 测试文件访问...")
    test_file_access()