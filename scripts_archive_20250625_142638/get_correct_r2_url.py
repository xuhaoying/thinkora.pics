#!/usr/bin/env python3
"""
获取正确的R2公开URL
既然Public Access已启用，需要找到正确的URL格式
"""

import requests
import time

def test_different_r2_formats():
    """测试不同的R2 URL格式"""
    
    # 既然Public Access已启用，尝试不同的可能格式
    account_id = "1045ce59b226648f11cc9e68b2c31a77"
    bucket_name = "thinkora-images"
    test_file = "images/0V3uVjouHRc.png"
    
    # 可能的公开URL格式
    possible_urls = [
        # 标准R2 public URL格式
        f"https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/{test_file}",
        
        # 直接bucket URL格式
        f"https://{bucket_name}.{account_id}.r2.cloudflarestorage.com/{test_file}",
        
        # 另一种格式
        f"https://{bucket_name}.r2.dev/{test_file}",
        
        # 可能的新格式
        f"https://{bucket_name}.pub.r2.dev/{test_file}",
        
        # 账户特定格式
        f"https://pub.{account_id}.r2.dev/{bucket_name}/{test_file}",
        f"https://cdn.{account_id}.r2.dev/{bucket_name}/{test_file}",
        
        # 其他可能格式
        f"https://{account_id}.public.r2.dev/{bucket_name}/{test_file}",
    ]
    
    print("测试各种可能的R2公开URL格式...")
    print("=" * 60)
    
    for i, url in enumerate(possible_urls, 1):
        print(f"\n{i}. 测试: {url}")
        try:
            response = requests.head(url, timeout=8)
            status = response.status_code
            
            if status == 200:
                print(f"   ✅ 成功! 状态码: {status}")
                print(f"   📏 Content-Length: {response.headers.get('Content-Length', 'N/A')}")
                print(f"   🔗 正确的基础URL: {url.replace(test_file, '')}")
                return url.replace(test_file, "").rstrip("/")
            elif status == 404:
                print(f"   ❌ 文件不存在 (404)")
            elif status == 403:
                print(f"   🔒 访问被拒绝 (403) - 可能需要额外配置")
            else:
                print(f"   ⚠️  状态码: {status}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️  超时")
        except requests.exceptions.ConnectionError:
            print(f"   🚫 连接错误")
        except Exception as e:
            print(f"   ❌ 错误: {type(e).__name__}")
        
        # 避免请求过快
        time.sleep(0.5)
    
    return None

def provide_manual_check_instructions():
    """提供手动检查说明"""
    print("\n" + "=" * 60)
    print("🔍 手动检查Cloudflare Dashboard中的公开URL")
    print("=" * 60)
    print("1. 访问: https://dash.cloudflare.com")
    print("2. 进入 R2 Object Storage")
    print("3. 点击 'thinkora-images' bucket")
    print("4. 查看 'Public access' 部分")
    print("5. 应该显示类似这样的URL:")
    print("   https://pub-[随机字符].r2.dev")
    print("6. 复制完整的公开URL")
    print("\n📝 然后更新 .env 文件:")
    print("R2_PUBLIC_URL=https://你看到的正确URL")

if __name__ == "__main__":
    print("🔍 寻找正确的R2公开URL...")
    
    correct_url = test_different_r2_formats()
    
    if correct_url:
        print("\n" + "=" * 60)
        print("🎉 找到正确的公开URL!")
        print("=" * 60)
        print(f"正确的URL: {correct_url}")
        print(f"\n请更新 .env 文件:")
        print(f"R2_PUBLIC_URL={correct_url}")
        print("\n然后运行:")
        print("python3 generate_image_pages.py")
    else:
        provide_manual_check_instructions()
        print("\n💡 如果所有格式都失败，可能需要:")
        print("1. 在Cloudflare Dashboard重新配置公开访问")
        print("2. 等待几分钟让配置生效")
        print("3. 检查是否有自定义域名配置")