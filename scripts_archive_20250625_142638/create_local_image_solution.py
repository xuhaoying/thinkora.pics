#!/usr/bin/env python3
"""
创建本地图片解决方案
将图片直接复制到dist目录，作为临时解决方案
"""

import os
import shutil
import json
from pathlib import Path

def copy_images_to_dist():
    """将处理后的图片复制到dist目录"""
    
    print("🖼️  复制图片到dist目录...")
    
    # 确保dist/images目录存在
    dist_images_dir = Path("dist/static-images")
    dist_images_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制png目录下的所有图片
    png_dir = Path("png")
    copied_count = 0
    
    if png_dir.exists():
        for platform_dir in png_dir.iterdir():
            if platform_dir.is_dir():
                platform_name = platform_dir.name
                
                # 在dist中创建平台目录
                dist_platform_dir = dist_images_dir / platform_name
                dist_platform_dir.mkdir(exist_ok=True)
                
                # 复制PNG文件
                for png_file in platform_dir.glob("*.png"):
                    dest_file = dist_platform_dir / png_file.name
                    shutil.copy2(png_file, dest_file)
                    copied_count += 1
                    print(f"  ✅ {png_file.name}")
    
    print(f"📊 已复制 {copied_count} 张图片到 dist/static-images/")
    return copied_count

def update_metadata_for_local_images():
    """更新元数据使用本地图片路径"""
    
    print("📝 更新元数据使用本地路径...")
    
    # 读取现有元数据
    with open("metadata_r2.json", "r") as f:
        metadata = json.load(f)
    
    # 更新URL指向本地静态文件
    updated_count = 0
    for item in metadata:
        if "imageUrl" in item:
            # 提取文件名
            if item.get("platform") == "unsplash":
                filename = f"unsplash_{item['id']}.png"
                item["imageUrl"] = f"/static-images/unsplash/{filename}"
                item["thumbnailUrl"] = f"/static-images/unsplash/{filename}"
                item["downloadUrl"] = f"/static-images/unsplash/{filename}"
            elif item.get("platform") == "pexels":
                filename = f"pexels_{item['id']}.png"
                item["imageUrl"] = f"/static-images/pexels/{filename}"
                item["thumbnailUrl"] = f"/static-images/pexels/{filename}"
                item["downloadUrl"] = f"/static-images/pexels/{filename}"
            else:
                # 旧格式图片，使用ID作为文件名
                image_id = item["id"].replace("unsplash_", "")
                item["imageUrl"] = f"/static-images/legacy/{image_id}.png"
                item["thumbnailUrl"] = f"/static-images/legacy/{image_id}.png"
                item["downloadUrl"] = f"/static-images/legacy/{image_id}.png"
            
            updated_count += 1
    
    # 保存更新的元数据
    with open("metadata_local.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📊 已更新 {updated_count} 条元数据记录")
    return updated_count

def generate_website_with_local_images():
    """使用本地图片生成网站"""
    
    print("🌐 生成使用本地图片的网站...")
    
    # 修改generate_image_pages.py使用本地元数据
    import subprocess
    
    # 临时修改元数据文件
    if os.path.exists("metadata_local.json"):
        # 备份原文件
        shutil.copy("metadata_r2.json", "metadata_r2_backup.json")
        
        # 使用本地元数据
        shutil.copy("metadata_local.json", "metadata_r2.json")
        
        # 生成网站
        result = subprocess.run(["python3", "generate_image_pages.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 网站生成成功")
        else:
            print(f"❌ 网站生成失败: {result.stderr}")
        
        # 恢复原文件
        shutil.copy("metadata_r2_backup.json", "metadata_r2.json")
    
def create_local_solution():
    """创建完整的本地解决方案"""
    
    print("🚀 创建本地图片解决方案...")
    print("=" * 50)
    
    # 1. 复制图片
    copied_images = copy_images_to_dist()
    
    # 2. 更新元数据
    updated_metadata = update_metadata_for_local_images()
    
    # 3. 生成网站
    generate_website_with_local_images()
    
    print("\n" + "=" * 50)
    print("✅ 本地解决方案创建完成!")
    print("📁 图片位置: dist/static-images/")
    print("📄 本地元数据: metadata_local.json")
    print("\n💡 这是临时解决方案，建议仍然修复R2配置")

if __name__ == "__main__":
    create_local_solution()