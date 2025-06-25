#!/usr/bin/env python3
"""
为现有的HTML文件添加图片点击下载功能
"""

import os
import re
import json

def add_image_download_to_html():
    """为dist/images/目录下的所有HTML文件添加图片点击下载功能"""
    
    # 读取metadata.json获取正确的图片URL
    with open('dist/metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # 创建ID到URL的映射
    url_map = {}
    for item in metadata:
        url_map[item['id']] = item['url']
    
    html_dir = 'dist/images'
    
    for filename in os.listdir(html_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(html_dir, filename)
            image_id = filename.replace('.html', '')
            
            # 获取对应的图片URL
            image_url = url_map.get(image_id, '')
            
            if not image_url:
                print(f"Warning: No URL found for {image_id}")
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找现有的图片标签
            img_pattern = r'<img src="([^"]*)" alt="([^"]*)" loading="eager">'
            match = re.search(img_pattern, content)
            
            if match:
                current_src = match.group(1)
                alt_text = match.group(2)
                
                # 如果图片已经被包在下载链接中，跳过
                if '<a href=' in content and 'download=' in content and current_src == image_url:
                    print(f"✓ {filename} already has download link")
                    continue
                
                # 构建新的HTML结构：包含下载链接的图片
                new_img_html = f'''<a href="{image_url}" download="{alt_text}.png" title="Click to download {alt_text}">
                    <img src="{image_url}" alt="{alt_text}" loading="eager">
                </a>'''
                
                # 替换原来的图片标签
                old_img_html = f'<img src="{current_src}" alt="{alt_text}" loading="eager">'
                content = content.replace(old_img_html, new_img_html)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✓ Updated {filename} with downloadable image")
            else:
                print(f"✗ Could not find image tag in {filename}")

if __name__ == "__main__":
    print("🔧 Adding image download functionality to HTML files...")
    add_image_download_to_html()
    print("✅ Done!")