#!/usr/bin/env python3
"""
修复所有URL使用正确的R2地址
"""

import json
import os

def fix_metadata_to_r2():
    """将元数据中的URL改为R2地址"""
    
    # R2公开URL
    R2_PUBLIC_URL = "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev"
    
    # 加载当前元数据
    with open("metadata_r2.json", "r") as f:
        metadata = json.load(f)
    
    fixed_count = 0
    
    for item in metadata:
        image_id = item.get("id", "")
        
        # 根据不同类型的图片确定R2路径
        if image_id.startswith("unsplash_"):
            # 对于新的unsplash图片，去掉前缀
            clean_id = image_id.replace("unsplash_", "")
            r2_path = f"{R2_PUBLIC_URL}/images/{clean_id}.png"
        elif image_id.startswith("pexels_"):
            # 对于pexels图片
            r2_path = f"{R2_PUBLIC_URL}/images/{image_id}.png"
        elif image_id.startswith("pixabay_"):
            # 对于pixabay图片
            r2_path = f"{R2_PUBLIC_URL}/images/{image_id}.png"
        else:
            # 对于旧图片（没有平台前缀的）
            r2_path = f"{R2_PUBLIC_URL}/images/{image_id}.png"
        
        # 更新所有URL字段
        item["imageUrl"] = r2_path
        item["thumbnailUrl"] = r2_path
        item["downloadUrl"] = r2_path
        
        fixed_count += 1
        print(f"✅ 修复: {image_id}")
    
    # 保存修复后的元数据
    with open("metadata_r2.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n📊 已修复 {fixed_count} 个图片URL")
    print("✅ 元数据已更新为使用R2 URL")
    
    return metadata

def regenerate_site():
    """重新生成网站"""
    import subprocess
    
    print("\n🌐 重新生成网站...")
    
    try:
        # 激活虚拟环境并生成网站
        result = subprocess.run(
            ["bash", "-c", "source venv/bin/activate && python generate_image_pages.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 网站生成成功")
            print(result.stdout)
        else:
            print(f"❌ 网站生成失败")
            print(result.stderr)
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

def verify_r2_urls():
    """验证几个R2 URL"""
    test_urls = [
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/0V3uVjouHRc.png",
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/0o6Lqin4nNE.png",
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/pexels_8516791.png"
    ]
    
    print("\n🔍 测试R2 URL:")
    for url in test_urls:
        print(f"  - {url}")
    
    print("\n💡 请在浏览器中测试这些URL")
    print("   如果无法访问，需要在Cloudflare中检查:")
    print("   1. Public Access 是否已启用")
    print("   2. 文件是否已上传到正确路径")

if __name__ == "__main__":
    print("🚀 修复URL为R2地址...")
    print("=" * 50)
    
    # 1. 修复元数据
    fix_metadata_to_r2()
    
    # 2. 重新生成网站
    regenerate_site()
    
    # 3. 验证URL
    verify_r2_urls()