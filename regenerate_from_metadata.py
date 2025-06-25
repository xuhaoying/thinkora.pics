#!/usr/bin/env python3
"""
从metadata.json重新生成所有HTML页面
"""

import json
import os
from jinja2 import Environment, FileSystemLoader

def regenerate_from_metadata():
    """基于metadata.json重新生成所有HTML页面"""
    
    # 读取metadata
    with open('dist/metadata.json', 'r', encoding='utf-8') as f:
        images = json.load(f)
    
    print(f"📊 Found {len(images)} images in metadata.json")
    
    # 设置模板环境
    env = Environment(loader=FileSystemLoader('templates'))
    
    # 生成首页
    index_template = env.get_template('index_template.html')
    index_html = index_template.render(images=images)
    
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("🏠 Generated index.html")
    
    # 生成详情页
    detail_template = env.get_template('detail_template.html')
    
    for i, image in enumerate(images):
        # 计算前一张和后一张图片
        prev_image = images[i-1] if i > 0 else None
        next_image = images[i+1] if i < len(images)-1 else None
        
        # 渲染详情页
        detail_html = detail_template.render(
            title=image['title'],
            description=image['description'],
            image_url=image['imageUrl'],
            download_url=image['downloadUrl'],
            page_url=f"https://thinkora.pics/images/{image['id']}.html",
            author_name=image['author'],
            author_url=image['authorUrl'],
            dimensions=f"{image.get('width', 'N/A')} x {image.get('height', 'N/A')}",
            file_size=image.get('fileSize', 'N/A'),
            category=image['category'],
            prev_image=prev_image,
            next_image=next_image
        )
        
        # 写入文件
        detail_path = f"dist/images/{image['id']}.html"
        with open(detail_path, 'w', encoding='utf-8') as f:
            f.write(detail_html)
    
    print(f"🖼️  Generated {len(images)} detail pages")
    
    # 更新搜索信息
    update_search_info(len(images))
    
    print("✅ All pages regenerated successfully!")
    print(f"📈 Website now has {len(images)} images")

def update_search_info(total_images):
    """更新首页的搜索信息"""
    index_path = 'dist/index.html'
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新搜索信息
    content = content.replace(
        'Search through 106 images',
        f'Search through {total_images} images'
    )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    print("🔄 Regenerating website from metadata.json...")
    regenerate_from_metadata()