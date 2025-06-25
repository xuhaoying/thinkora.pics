#!/usr/bin/env python3
"""
更新metadata_r2.json的格式，统一新旧数据格式
"""

import json
import os

def convert_metadata_format():
    """转换元数据格式"""
    
    # 读取现有元数据
    with open('metadata_r2.json', 'r') as f:
        metadata = json.load(f)
    
    # 统一转换为新格式
    unified_metadata = []
    
    for item in metadata:
        # 如果已经是新格式，直接使用
        if 'imageUrl' in item:
            unified_metadata.append(item)
        else:
            # 转换旧格式到新格式
            new_item = {
                'id': item.get('id', ''),
                'title': item.get('title', ''),
                'description': item.get('description', ''),
                'tags': item.get('tags', []),
                'category': item.get('category', 'other'),
                'imageUrl': item.get('urls', {}).get('regular', ''),
                'thumbnailUrl': item.get('urls', {}).get('thumbnail', ''),
                'downloadUrl': item.get('urls', {}).get('download', ''),
                'width': item.get('dimensions', {}).get('width', 0),
                'height': item.get('dimensions', {}).get('height', 0),
                'transparencyRatio': item.get('transparent_ratio', 0),
                'qualityScore': item.get('quality_score', 0),
                'platform': 'unsplash' if 'unsplash' in item.get('id', '') else 'unknown',
                'author': item.get('author', {}).get('name', '') if isinstance(item.get('author'), dict) else item.get('author', ''),
                'authorUrl': item.get('author', {}).get('url', '') if isinstance(item.get('author'), dict) else '',
                'uploadDate': item.get('created_at', ''),
                'fileSize': 0  # 旧格式没有文件大小
            }
            unified_metadata.append(new_item)
    
    # 备份原文件
    if os.path.exists('metadata_r2.json'):
        import shutil
        shutil.copy('metadata_r2.json', 'metadata_r2_backup.json')
    
    # 保存统一格式的元数据
    with open('metadata_r2.json', 'w') as f:
        json.dump(unified_metadata, f, indent=2)
    
    print(f"Updated {len(unified_metadata)} metadata entries")
    
    # 同时更新模板匹配的数据结构
    return unified_metadata

if __name__ == "__main__":
    convert_metadata_format()