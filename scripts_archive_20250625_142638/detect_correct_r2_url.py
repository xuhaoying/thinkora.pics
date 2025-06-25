#!/usr/bin/env python3
"""
检测正确的R2公开URL并更新配置
"""

import boto3
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def detect_working_url():
    """检测有效的R2公开URL"""
    
    # 首先列出一个已知存在的文件
    s3_client = boto3.client(
        's3',
        endpoint_url=os.getenv('R2_ENDPOINT'),
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        region_name='auto'
    )
    
    bucket_name = os.getenv('R2_BUCKET')
    
    # 获取一个测试文件
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix='images/',
        MaxKeys=1
    )
    
    if not response.get('Contents'):
        print("❌ 没有找到测试文件")
        return None
    
    test_file = response['Contents'][0]['Key']
    print(f"使用测试文件: {test_file}")
    
    # 尝试不同的URL格式
    account_id = "1045ce59b226648f11cc9e68b2c31a77"
    
    url_patterns = [
        f"https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/{test_file}",
        f"https://{bucket_name}.{account_id}.r2.cloudflarestorage.com/{test_file}",
        f"https://{bucket_name}.r2.dev/{test_file}",
        f"https://r2.thinkora.pics/{test_file}",  # 如果配置了自定义域名
    ]
    
    print("\n检测可用的URL格式:")
    for url in url_patterns:
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ 有效: {url}")
                base_url = url.replace(f"/{test_file}", "")
                return base_url
            elif response.status_code == 403:
                print(f"🔒 需要配置公开访问: {url}")
            else:
                print(f"❌ 状态码 {response.status_code}: {url}")
        except requests.exceptions.Timeout:
            print(f"⏱️  超时: {url}")
        except Exception as e:
            print(f"❌ 错误: {url} - {type(e).__name__}")
    
    return None

def check_r2_dashboard_instructions():
    """提供R2 Dashboard配置说明"""
    print("\n" + "="*50)
    print("🔧 R2公开访问配置说明")
    print("="*50)
    print("1. 访问 Cloudflare Dashboard:")
    print("   https://dash.cloudflare.com")
    print("\n2. 导航到 R2 Object Storage")
    print("\n3. 选择 'thinkora-images' bucket")
    print("\n4. 点击 'Settings' 标签")
    print("\n5. 在 'Public access' 部分:")
    print("   - 点击 'Allow Access'")
    print("   - 确认启用公开访问")
    print("\n6. 记录提供的公开URL")
    print("\n7. 更新 .env 文件中的 R2_PUBLIC_URL")
    print("="*50)

def generate_fixed_urls_if_pattern_found():
    """如果找到模式，生成修复脚本"""
    
    # 检查是否需要更新URL格式
    print("\n正在生成URL修复脚本...")
    
    # 基于已知的R2存储结构创建修复脚本
    fix_script = """#!/usr/bin/env python3
# 自动生成的URL修复脚本

import json

def fix_metadata_urls():
    # 读取现有元数据
    with open('metadata_r2.json', 'r') as f:
        metadata = json.load(f)
    
    # 当有效的公开URL确定后，更新这里
    # NEW_BASE_URL = "https://正确的公开URL"
    
    print("请先在Cloudflare Dashboard配置R2公开访问")
    print("然后更新NEW_BASE_URL变量")
    
    # 示例修复代码：
    # for item in metadata:
    #     if 'imageUrl' in item:
    #         # 更新URL
    #         pass
    
if __name__ == "__main__":
    fix_metadata_urls()
"""
    
    with open('fix_urls_after_r2_config.py', 'w') as f:
        f.write(fix_script)
    
    print("✅ 已生成 fix_urls_after_r2_config.py")

if __name__ == "__main__":
    print("=== R2公开URL检测 ===\n")
    
    working_url = detect_working_url()
    
    if working_url:
        print(f"\n✅ 找到有效URL: {working_url}")
        print(f"\n请更新 .env 文件:")
        print(f"R2_PUBLIC_URL={working_url}")
    else:
        print(f"\n❌ 没有找到有效的公开URL")
        check_r2_dashboard_instructions()
        generate_fixed_urls_if_pattern_found()
        
        print(f"\n⚠️  建议操作:")
        print(f"1. 按照上述说明配置R2公开访问")
        print(f"2. 运行: python3 fix_urls_after_r2_config.py")
        print(f"3. 重新生成网站: python3 generate_image_pages.py")