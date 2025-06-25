#!/usr/bin/env python3
"""
测试API连接
"""

import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_unsplash():
    """测试Unsplash API"""
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    if not access_key:
        return False, "No API key"
    
    try:
        url = 'https://api.unsplash.com/search/photos'
        params = {'query': 'transparent background', 'per_page': 1}
        headers = {'Authorization': f'Client-ID {access_key}'}
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Found {data['total']} images"
        else:
            return False, f"Error: {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_pexels():
    """测试Pexels API"""
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        return False, "No API key"
    
    try:
        url = 'https://api.pexels.com/v1/search'
        params = {'query': 'transparent background', 'per_page': 1}
        headers = {'Authorization': api_key}
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Found {data['total_results']} images"
        else:
            return False, f"Error: {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_pixabay():
    """测试Pixabay API"""
    api_key = os.getenv('PIXABAY_API_KEY')
    if not api_key:
        return False, "No API key"
    
    try:
        url = 'https://pixabay.com/api/'
        params = {'key': api_key, 'q': 'transparent background', 'per_page': 1}
        
        response = requests.get(url, params=params)
        print(f"\nPixabay response: {response.text[:200]}")  # 调试输出
        if response.status_code == 200:
            data = response.json()
            return True, f"Found {data['totalHits']} images"
        else:
            # 获取详细错误信息
            try:
                error_data = response.json()
                return False, f"Error {response.status_code}: {error_data}"
            except:
                return False, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)

def test_r2():
    """测试R2连接"""
    import boto3
    
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('R2_ENDPOINT'),
            aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
            region_name='auto'
        )
        
        # 尝试列出bucket
        buckets = s3_client.list_buckets()
        return True, f"Connected, found {len(buckets['Buckets'])} buckets"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    print("=== Testing API Connections ===\n")
    
    # 测试各个API
    tests = [
        ("Unsplash", test_unsplash),
        ("Pexels", test_pexels),
        ("Pixabay", test_pixabay),
        ("Cloudflare R2", test_r2)
    ]
    
    all_success = True
    for name, test_func in tests:
        print(f"Testing {name}...", end=" ")
        success, message = test_func()
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
            all_success = False
    
    print("\n" + ("="*30))
    if all_success:
        print("✅ All APIs are working!")
    else:
        print("❌ Some APIs failed. Please check your configuration.")