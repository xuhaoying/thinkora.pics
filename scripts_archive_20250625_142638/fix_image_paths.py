#!/usr/bin/env python3
"""
修复图片路径问题，并将旧图片也复制到dist目录
"""

import os
import json
import shutil
from pathlib import Path

def copy_legacy_images_from_r2():
    """从R2下载并复制旧图片文件（作为备选方案）"""
    # 暂时跳过，因为R2公开访问有问题
    print("⚠️  跳过从R2下载旧图片，因为公开URL无法访问")

def copy_existing_png_files():
    """复制现有的PNG文件到dist静态目录"""
    
    dist_images_dir = Path("dist/static-images")
    dist_images_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建legacy目录存放旧图片
    legacy_dir = dist_images_dir / "legacy"
    legacy_dir.mkdir(exist_ok=True)
    
    copied_count = 0
    
    # 从png目录复制图片
    png_dir = Path("png")
    if png_dir.exists():
        for platform_dir in png_dir.iterdir():
            if platform_dir.is_dir():
                platform_name = platform_dir.name
                
                # 确保平台目录存在
                dist_platform_dir = dist_images_dir / platform_name
                dist_platform_dir.mkdir(exist_ok=True)
                
                # 复制PNG文件
                for png_file in platform_dir.glob("*.png"):
                    dest_file = dist_platform_dir / png_file.name
                    shutil.copy2(png_file, dest_file)
                    copied_count += 1
                    print(f"  ✅ 复制: {png_file.name}")
    
    print(f"📊 已复制 {copied_count} 张新图片")
    return copied_count

def fix_metadata_paths():
    """修复元数据中的图片路径"""
    
    with open("metadata_r2.json", "r") as f:
        metadata = json.load(f)
    
    updated_count = 0
    
    for item in metadata:
        if "imageUrl" in item:
            # 检查是否是新上传的图片（有平台信息）
            if item.get("platform") in ["unsplash", "pexels", "pixabay"]:
                # 新图片：使用实际文件名
                if item.get("platform") == "unsplash":
                    if item["id"].startswith("unsplash_"):
                        filename = f"{item['id']}.png"
                    else:
                        filename = f"unsplash_{item['id']}.png"
                elif item.get("platform") == "pexels":
                    if item["id"].startswith("pexels_"):
                        filename = f"{item['id']}.png"
                    else:
                        filename = f"pexels_{item['id']}.png"
                else:  # pixabay
                    if item["id"].startswith("pixabay_"):
                        filename = f"{item['id']}.png"
                    else:
                        filename = f"pixabay_{item['id']}.png"
                
                # 更新URL
                item["imageUrl"] = f"/static-images/{item['platform']}/{filename}"
                item["thumbnailUrl"] = f"/static-images/{item['platform']}/{filename}"
                item["downloadUrl"] = f"/static-images/{item['platform']}/{filename}"
                
            else:
                # 旧图片：保持原来的R2 URL，因为我们没有这些文件
                # 这些图片需要从R2下载或保持原来的URL
                pass
            
            updated_count += 1
    
    # 保存修复后的元数据
    with open("metadata_local_fixed.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📊 已修复 {updated_count} 条元数据记录")
    return metadata

def regenerate_site_with_fixed_paths():
    """使用修复后的路径重新生成网站"""
    
    print("🌐 使用修复后的路径重新生成网站...")
    
    # 备份原始文件
    shutil.copy("metadata_r2.json", "metadata_r2_original.json")
    
    # 使用修复后的元数据
    shutil.copy("metadata_local_fixed.json", "metadata_r2.json")
    
    try:
        # 重新生成网站
        import subprocess
        result = subprocess.run(["python3", "generate_image_pages.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 网站生成成功")
        else:
            print(f"❌ 网站生成失败: {result.stderr}")
    
    finally:
        # 恢复原始文件
        shutil.copy("metadata_r2_original.json", "metadata_r2.json")

def main():
    """主修复流程"""
    
    print("🔧 修复图片路径问题...")
    print("=" * 50)
    
    # 1. 复制现有图片文件
    copy_existing_png_files()
    
    # 2. 修复元数据路径
    fix_metadata_paths()
    
    # 3. 重新生成网站
    regenerate_site_with_fixed_paths()
    
    print("\n" + "=" * 50)
    print("✅ 图片路径修复完成!")
    print("📁 本地图片: dist/static-images/")
    print("📄 修复元数据: metadata_local_fixed.json")
    print("\n💡 现在新图片应该可以正常显示")
    print("⚠️  旧图片仍然使用R2 URL，需要修复R2公开访问")

if __name__ == "__main__":
    main()