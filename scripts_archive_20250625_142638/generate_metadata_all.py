#!/usr/bin/env python3
"""
生成所有PNG文件的元数据
扫描png目录下的所有文件，生成完整的metadata.json
"""

import json
import os
from datetime import datetime
from PIL import Image
import re

# 类别关键词映射
CATEGORY_KEYWORDS = {
    'electronics': ['laptop', 'computer', 'phone', 'smartphone', 'tablet', 'keyboard', 'mouse', 'screen', 'monitor', 'device', 'gadget', 'camera', 'headphones', 'speaker', 'tech', 'technology', 'digital', 'macbook', 'iphone', 'ipad'],
    'office': ['office', 'desk', 'workspace', 'workplace', 'business', 'work', 'professional', 'productivity', 'meeting', 'conference'],
    'lifestyle': ['coffee', 'tea', 'drink', 'beverage', 'food', 'meal', 'breakfast', 'lunch', 'dinner', 'cup', 'mug'],
    'photography': ['photo', 'camera', 'photography', 'picture', 'image', 'lens', 'shoot', 'capture'],
    'fashion': ['fashion', 'style', 'clothing', 'wear', 'outfit', 'accessories', 'jewelry', 'watch'],
    'nature': ['nature', 'plant', 'flower', 'tree', 'leaf', 'garden', 'outdoor', 'landscape'],
    'art': ['art', 'design', 'creative', 'artistic', 'illustration', 'drawing', 'painting', 'sketch'],
    'home': ['home', 'house', 'furniture', 'interior', 'decor', 'room', 'living', 'bedroom', 'kitchen']
}

def get_file_size_mb(file_path):
    """获取文件大小（MB）"""
    size = os.path.getsize(file_path) / (1024 * 1024)
    return f"{size:.1f}MB"

def extract_info_from_filename(filename):
    """从文件名提取信息"""
    # 移除扩展名
    name = filename.replace('.png', '')
    
    # 尝试从文件名生成标题
    # 将连字符、下划线替换为空格
    title = name.replace('-', ' ').replace('_', ' ')
    
    # 如果是ID格式（如 QLqNalPe0RA），保持原样
    if re.match(r'^[a-zA-Z0-9_-]+$', name) and len(name) < 20:
        title = f"Transparent Background Image {name[:8]}"
    
    return name, title

def determine_category(filename, title=""):
    """根据文件名和标题确定类别"""
    text = (filename + " " + title).lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category
    
    return 'others'

def generate_metadata_for_all_pngs():
    """为所有PNG文件生成元数据"""
    png_dir = 'png'
    metadata = []
    
    # 获取所有PNG文件
    png_files = [f for f in os.listdir(png_dir) if f.endswith('.png')]
    png_files.sort()
    
    print(f"📁 找到 {len(png_files)} 个PNG文件")
    
    for i, filename in enumerate(png_files):
        png_path = os.path.join(png_dir, filename)
        
        # 提取基本信息
        image_id, title = extract_info_from_filename(filename)
        
        # 获取图片尺寸和透明度
        dimensions = {"width": 1920, "height": 1080, "ratio": "16:9"}
        transparent_ratio = 1.0
        
        try:
            with Image.open(png_path) as img:
                width, height = img.size
                gcd = lambda a, b: b if a == 0 else gcd(b % a, a)
                g = gcd(width, height)
                ratio = f"{width//g}:{height//g}"
                
                dimensions = {
                    "width": width,
                    "height": height,
                    "ratio": ratio
                }
                
                # 计算透明度比例
                if img.mode == 'RGBA':
                    alpha = img.getchannel('A')
                    alpha_data = list(alpha.getdata())
                    transparent_pixels = sum(1 for p in alpha_data if p < 255)
                    transparent_ratio = round(transparent_pixels / len(alpha_data), 2)
        except Exception as e:
            print(f"⚠️ 无法读取图片 {filename}: {e}")
        
        # 确定类别
        category = determine_category(filename, title)
        
        # 获取文件大小
        file_size = get_file_size_mb(png_path)
        
        # 构建元数据
        item = {
            "id": f"unsplash_{image_id}",
            "title": title,
            "description": f"High-quality transparent background PNG image",
            "author": {
                "name": "Unknown",
                "url": "https://unsplash.com/"
            },
            "dimensions": dimensions,
            "urls": {
                "thumbnail": f"./png/{filename}",
                "regular": f"./png/{filename}",
                "download": f"./png/{filename}"
            },
            "tags": [],
            "category": category,
            "quality_score": 95,
            "file_size": file_size,
            "transparent_ratio": transparent_ratio,
            "created_at": datetime.now().isoformat() + "Z",
            "unsplash": {
                "id": image_id,
                "url": f"https://unsplash.com/photos/{image_id}",
                "download_location": f"https://unsplash.com/photos/{image_id}/download"
            }
        }
        
        metadata.append(item)
        
        if (i + 1) % 10 == 0:
            print(f"✅ 已处理 {i + 1}/{len(png_files)} 个文件")
    
    # 保存元数据
    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功生成元数据，共 {len(metadata)} 张图片")
    
    # 统计类别
    category_count = {}
    for item in metadata:
        cat = item['category']
        category_count[cat] = category_count.get(cat, 0) + 1
    
    print(f"📊 类别分布：")
    for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {cat}: {count} 张")

if __name__ == "__main__":
    generate_metadata_for_all_pngs()