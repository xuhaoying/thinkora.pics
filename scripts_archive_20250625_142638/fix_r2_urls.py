#!/usr/bin/env python3
"""
修复所有图片URL使用R2公开访问地址
"""

import json
import os

def fix_to_r2_urls():
    """将所有图片URL改回使用R2"""
    
    # R2公开访问URL
    R2_PUBLIC_URL = "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev"
    
    # 加载当前元数据
    with open("metadata_r2.json", "r") as f:
        metadata = json.load(f)
    
    fixed_count = 0
    
    for item in metadata:
        # 获取图片ID
        image_id = item.get("id", "")
        
        # 确定图片在R2中的路径
        if image_id.startswith("unsplash_"):
            # 新图片格式
            r2_path = f"/images/{image_id.replace('unsplash_', '')}.png"
        elif image_id.startswith("pexels_"):
            r2_path = f"/images/{image_id.replace('pexels_', '')}.png"
        elif image_id.startswith("pixabay_"):
            r2_path = f"/images/{image_id.replace('pixabay_', '')}.png"
        else:
            # 旧图片格式
            r2_path = f"/images/{image_id}.png"
        
        # 更新URL为R2地址
        r2_url = f"{R2_PUBLIC_URL}{r2_path}"
        
        item["imageUrl"] = r2_url
        item["thumbnailUrl"] = r2_url
        item["downloadUrl"] = r2_url
        
        fixed_count += 1
        print(f"✅ 修复: {image_id} -> {r2_url}")
    
    # 保存修复后的元数据
    with open("metadata_r2_fixed.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n📊 已修复 {fixed_count} 个图片URL")
    print(f"📄 保存到: metadata_r2_fixed.json")
    
    return metadata

def check_r2_public_access():
    """检查R2公开访问是否正常"""
    import requests
    
    # 测试URL
    test_urls = [
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/0V3uVjouHRc.png",
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/0o6Lqin4nNE.png",
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/5EgJ-mUklbg.png"
    ]
    
    print("\n🔍 检查R2公开访问...")
    print("=" * 50)
    
    for url in test_urls:
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url.split('/')[-1]} - 可访问")
            else:
                print(f"❌ {url.split('/')[-1]} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ {url.split('/')[-1]} - 错误: {str(e)}")
    
    print("\n💡 如果无法访问，请检查：")
    print("1. 在Cloudflare R2控制台中，确认bucket设置为'Public'")
    print("2. 检查R2 bucket的CORS设置是否允许您的域名")
    print("3. 确认图片文件已经上传到R2")

def generate_r2_cors_config():
    """生成R2 CORS配置"""
    cors_config = {
        "CORSRules": [
            {
                "AllowedOrigins": [
                    "https://thinkora.pics",
                    "http://localhost:*",
                    "https://*.vercel.app"
                ],
                "AllowedMethods": ["GET", "HEAD"],
                "AllowedHeaders": ["*"],
                "MaxAgeSeconds": 3600
            }
        ]
    }
    
    with open("r2_cors_config.json", "w") as f:
        json.dump(cors_config, f, indent=2)
    
    print("\n📄 已生成R2 CORS配置: r2_cors_config.json")
    print("请在Cloudflare R2控制台中应用此配置")

if __name__ == "__main__":
    # 1. 修复URL为R2地址
    fix_to_r2_urls()
    
    # 2. 检查R2访问
    try:
        check_r2_public_access()
    except:
        print("\n⚠️  无法检查R2访问（可能缺少requests库）")
    
    # 3. 生成CORS配置
    generate_r2_cors_config()