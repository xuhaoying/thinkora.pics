#!/usr/bin/env python3
"""
快速更新metadata.json文件，添加已上传的Pixabay图片
"""

import os
import json
import glob
from datetime import datetime

def update_metadata_from_uploaded():
    """从已上传的图片更新metadata"""
    
    # 从日志中获取已上传的文件列表
    uploaded_files = []
    log_file = 'logs/r2_upload_20250624.log'
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f:
                if 'Successfully uploaded:' in line:
                    # 提取文件名
                    filename = line.split('Successfully uploaded: ')[1].strip()
                    if filename.endswith('.png'):
                        uploaded_files.append(filename)
    
    print(f"📊 Found {len(uploaded_files)} uploaded files in log")
    
    # 加载现有metadata
    metadata_file = 'dist/metadata.json'
    existing_metadata = []
    
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            existing_metadata = json.load(f)
    
    print(f"📚 Existing metadata entries: {len(existing_metadata)}")
    
    # 创建新的metadata条目
    new_entries = []
    r2_public_url = "https://img.thinkora.pics"
    
    for filename in uploaded_files:
        # 解析文件名
        parts = filename.replace('.png', '').split('_')
        if len(parts) >= 3:
            platform = parts[0]  # pixabay
            category = parts[1]
            image_id = parts[2]
            
            # 查找对应的metadata文件
            png_path = f"png/pixabay_massive/{filename}"
            metadata_path = png_path.replace('.png', '_metadata.json')
            
            image_info = {
                'id': image_id,
                'category': category,
                'title': f'{category.title()} Image',
                'platform': platform,
                'width': 0,
                'height': 0,
                'quality_score': 95
            }
            
            # 如果有metadata文件，读取详细信息
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    image_info.update(metadata)
                except:
                    pass
            
            # 构建统一格式的metadata条目
            entry = {
                'id': f"pixabay_{image_id}",
                'title': image_info.get('title', f"{category.title()} Image {image_id}"),
                'description': image_info.get('description', f"High-quality transparent background image from Pixabay - {category}"),
                'tags': image_info.get('tags', []),
                'category': category,
                'imageUrl': f"{r2_public_url}/images/{filename}",
                'thumbnailUrl': f"{r2_public_url}/images/{filename}",
                'downloadUrl': f"{r2_public_url}/images/{filename}",
                'width': image_info.get('width', 0),
                'height': image_info.get('height', 0),
                'transparencyRatio': 1.0,
                'qualityScore': image_info.get('quality_score', 95),
                'platform': 'pixabay',
                'author': image_info.get('author', 'Pixabay Contributor'),
                'authorUrl': image_info.get('author_url', 'https://pixabay.com/'),
                'uploadDate': datetime.now().isoformat(),
                'fileSize': os.path.getsize(png_path) if os.path.exists(png_path) else 0,
                'processingInfo': {
                    'background_removed': True,
                    'file_format': 'PNG',
                    'transparency_added': True,
                    'processed_date': datetime.now().isoformat(),
                    'original_query': image_info.get('query_used', ''),
                    'fetch_metadata': image_info.get('fetch_metadata', {})
                }
            }
            
            new_entries.append(entry)
    
    # 合并metadata（避免重复）
    existing_ids = {img.get('id') for img in existing_metadata}
    filtered_new_entries = [img for img in new_entries if img['id'] not in existing_ids]
    
    # 更新metadata文件
    all_metadata = existing_metadata + filtered_new_entries
    
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(all_metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated metadata.json:")
    print(f"   - Previous images: {len(existing_metadata)}")
    print(f"   - New Pixabay images: {len(filtered_new_entries)}")
    print(f"   - Total images: {len(all_metadata)}")
    
    return len(all_metadata)

if __name__ == "__main__":
    total_images = update_metadata_from_uploaded()
    print(f"\n🎉 Metadata update completed! Website now has {total_images} images.")