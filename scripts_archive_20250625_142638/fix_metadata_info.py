#!/usr/bin/env python3
"""
修复图片元数据，使用真实的图片信息
"""

import json
import os
from pathlib import Path

def load_raw_metadata():
    """加载原始元数据"""
    raw_metadata = {}
    
    # 加载旧图片的原始元数据
    if os.path.exists("metadata_raw.json"):
        with open("metadata_raw.json", "r") as f:
            raw_metadata.update(json.load(f))
    
    # 加载新图片的元数据文件
    png_dir = Path("png")
    for platform_dir in ["unsplash", "pexels", "pixabay"]:
        platform_path = png_dir / platform_dir
        if platform_path.exists():
            for metadata_file in platform_path.glob("*_metadata.json"):
                try:
                    with open(metadata_file, "r") as f:
                        metadata = json.load(f)
                        image_id = metadata.get("id")
                        if image_id:
                            raw_metadata[image_id] = metadata
                except Exception as e:
                    print(f"⚠️  Error loading {metadata_file}: {e}")
    
    return raw_metadata

def fix_metadata():
    """修复元数据信息"""
    
    # 加载当前元数据
    with open("metadata_r2.json", "r") as f:
        current_metadata = json.load(f)
    
    # 加载原始详细元数据
    raw_metadata = load_raw_metadata()
    
    fixed_count = 0
    
    for item in current_metadata:
        # 提取图片ID（去掉平台前缀）
        item_id = item.get("id", "").replace("unsplash_", "").replace("pexels_", "").replace("pixabay_", "")
        
        if item_id in raw_metadata:
            raw_info = raw_metadata[item_id]
            
            # 更新真实信息
            if raw_info.get("author"):
                item["author"] = raw_info["author"]
            
            if raw_info.get("author_url"):
                item["authorUrl"] = raw_info["author_url"]
            
            if raw_info.get("description"):
                item["description"] = raw_info["description"]
                item["title"] = raw_info["description"][:50] + "..." if len(raw_info["description"]) > 50 else raw_info["description"]
            
            # 更新尺寸信息
            if raw_info.get("width"):
                item["width"] = raw_info["width"]
            if raw_info.get("height"):
                item["height"] = raw_info["height"]
            
            # 更新文件大小
            if raw_info.get("file_size"):
                item["fileSize"] = raw_info["file_size"]
            
            # 更新标签
            if raw_info.get("tags"):
                item["tags"] = raw_info["tags"]
            
            # 根据平台设置类别
            if raw_info.get("platform"):
                if raw_info["platform"] == "unsplash":
                    item["category"] = "photography"
                elif raw_info["platform"] == "pexels":
                    item["category"] = "stock photo"
                elif raw_info["platform"] == "pixabay":
                    item["category"] = "digital art"
            
            fixed_count += 1
            print(f"✅ 修复: {item['id']} - {item.get('author', 'Unknown')}")
        else:
            print(f"⚠️  未找到元数据: {item['id']}")
    
    # 保存修复后的元数据
    with open("metadata_fixed.json", "w") as f:
        json.dump(current_metadata, f, indent=2)
    
    print(f"\n📊 修复了 {fixed_count} 张图片的元数据")
    print(f"📄 保存到: metadata_fixed.json")
    
    return current_metadata

if __name__ == "__main__":
    fix_metadata()