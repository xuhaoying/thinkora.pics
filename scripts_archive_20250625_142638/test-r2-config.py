#!/usr/bin/env python3
"""
R2 配置测试脚本
详细检查权限和配置问题
"""

import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 加载环境变量
load_dotenv()

def test_r2_config():
    """测试R2配置"""
    print("🔍 R2 配置诊断工具")
    print("=" * 50)
    
    # 检查环境变量
    print("\n1. 检查环境变量:")
    required_vars = {
        'R2_ACCOUNT_ID': os.getenv('R2_ACCOUNT_ID'),
        'R2_ACCESS_KEY': os.getenv('R2_ACCESS_KEY'),
        'R2_SECRET_KEY': os.getenv('R2_SECRET_KEY'),
        'R2_BUCKET_NAME': os.getenv('R2_BUCKET_NAME'),
        'R2_PUBLIC_URL': os.getenv('R2_PUBLIC_URL')
    }
    
    for var, value in required_vars.items():
        if value:
            print(f"   ✅ {var}: {value[:8]}..." if len(value) > 8 else f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: 未设置")
    
    # 创建客户端
    print(f"\n2. 创建 R2 客户端...")
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=f'https://{required_vars["R2_ACCOUNT_ID"]}.r2.cloudflarestorage.com',
            aws_access_key_id=required_vars['R2_ACCESS_KEY'],
            aws_secret_access_key=required_vars['R2_SECRET_KEY'],
            config=Config(
                signature_version='s3v4',
                retries={'max_attempts': 3}
            ),
            region_name='auto',
            verify=False
        )
        print("   ✅ 客户端创建成功")
    except Exception as e:
        print(f"   ❌ 客户端创建失败: {e}")
        return False
    
    # 测试列出所有 bucket
    print(f"\n3. 测试列出所有 bucket...")
    try:
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        print(f"   ✅ 成功列出 {len(buckets)} 个 bucket")
        print(f"   📋 Bucket 列表: {buckets}")
        
        if required_vars['R2_BUCKET_NAME'] in buckets:
            print(f"   ✅ 目标 bucket '{required_vars['R2_BUCKET_NAME']}' 存在")
        else:
            print(f"   ❌ 目标 bucket '{required_vars['R2_BUCKET_NAME']}' 不存在")
            print(f"   💡 需要创建 bucket 或检查 bucket 名称")
    except Exception as e:
        print(f"   ❌ 列出 bucket 失败: {e}")
        return False
    
    # 测试 bucket 访问权限
    print(f"\n4. 测试 bucket 访问权限...")
    try:
        response = s3.head_bucket(Bucket=required_vars['R2_BUCKET_NAME'])
        print(f"   ✅ 可以访问 bucket '{required_vars['R2_BUCKET_NAME']}'")
    except Exception as e:
        print(f"   ❌ 无法访问 bucket: {e}")
        return False
    
    # 测试列出 bucket 内容
    print(f"\n5. 测试列出 bucket 内容...")
    try:
        response = s3.list_objects_v2(Bucket=required_vars['R2_BUCKET_NAME'], MaxKeys=5)
        if 'Contents' in response:
            print(f"   ✅ 可以列出 bucket 内容，共有 {len(response['Contents'])} 个文件")
            for obj in response['Contents'][:3]:
                print(f"      - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print(f"   ✅ bucket 为空")
    except Exception as e:
        print(f"   ❌ 列出 bucket 内容失败: {e}")
        return False
    
    # 测试上传权限
    print(f"\n6. 测试上传权限...")
    try:
        # 创建一个测试文件
        test_content = "This is a test file for R2 upload permission"
        test_key = "test-upload-permission.txt"
        
        s3.put_object(
            Bucket=required_vars['R2_BUCKET_NAME'],
            Key=test_key,
            Body=test_content,
            ContentType='text/plain'
        )
        print(f"   ✅ 上传测试文件成功: {test_key}")
        
        # 删除测试文件
        s3.delete_object(
            Bucket=required_vars['R2_BUCKET_NAME'],
            Key=test_key
        )
        print(f"   ✅ 删除测试文件成功")
        
    except Exception as e:
        print(f"   ❌ 上传测试失败: {e}")
        print(f"   💡 这可能是权限问题，请检查 API Token 权限")
        return False
    
    print(f"\n🎉 所有测试通过！R2 配置正确")
    return True

def show_troubleshooting():
    """显示故障排除建议"""
    print(f"\n🔧 故障排除建议:")
    print(f"1. 检查 API Token 权限:")
    print(f"   - 访问: https://dash.cloudflare.com/profile/api-tokens")
    print(f"   - 确保权限包含: Object Read & Write")
    print(f"   - 确保资源选择: Specific bucket → {os.getenv('R2_BUCKET_NAME')}")
    
    print(f"\n2. 检查 bucket 设置:")
    print(f"   - 访问: https://dash.cloudflare.com/r2/overview")
    print(f"   - 确保 bucket '{os.getenv('R2_BUCKET_NAME')}' 存在")
    print(f"   - 检查 bucket 权限设置")
    
    print(f"\n3. 重新创建 API Token:")
    print(f"   - 删除旧的 API Token")
    print(f"   - 创建新的 Custom Token")
    print(f"   - 权限: Object Read & Write")
    print(f"   - 资源: Specific bucket")
    print(f"   - 更新 .env 文件中的密钥")

if __name__ == "__main__":
    if test_r2_config():
        print(f"\n✅ R2 配置正确，可以开始上传图片")
    else:
        print(f"\n❌ R2 配置有问题")
        show_troubleshooting() 