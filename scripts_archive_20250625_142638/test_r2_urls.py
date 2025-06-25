#!/usr/bin/env python3
"""
测试不同的R2 URL格式
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_different_url_formats():
    """测试不同的URL格式"""
    
    account_id = "1045ce59b226648f11cc9e68b2c31a77"  # 从endpoint提取
    bucket_name = "thinkora-images"
    test_file = "images/0V3uVjouHRc.png"
    
    # 不同可能的URL格式
    url_formats = [
        f"https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/{test_file}",
        f"https://{bucket_name}.{account_id}.r2.cloudflarestorage.com/{test_file}",
        f"https://{account_id}.r2.cloudflarestorage.com/{bucket_name}/{test_file}",
        f"https://{bucket_name}.r2.dev/{test_file}",
    ]
    
    print("测试不同的R2 URL格式:")
    for url in url_formats:
        try:
            response = requests.head(url, timeout=5)
            print(f"✅ {url} - 状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                print(f"   Content-Length: {response.headers.get('Content-Length', 'N/A')}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {url} - 错误: {type(e).__name__}")
        except Exception as e:
            print(f"❌ {url} - 错误: {e}")

if __name__ == "__main__":
    test_different_url_formats()