#!/usr/bin/env python3
"""
设置本地图片 - 将图片复制到public目录，使项目可以立即运行
"""

import os
import shutil
import sqlite3
import json
from datetime import datetime

def setup_local_images():
    """将图片复制到public/images目录"""
    print("🚀 设置本地图片...")
    
    # 创建public/images目录
    public_images_dir = 'public/images'
    os.makedirs(public_images_dir, exist_ok=True)
    
    # 获取所有需要的图片
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM images WHERE tags != '[]'")
    image_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    print(f"📸 需要处理 {len(image_ids)} 张图片")
    
    copied_count = 0
    for image_id in image_ids:
        # 查找源文件
        source_paths = [
            f'raw/pixabay/{image_id}.jpg',
            f'raw/pixabay/{image_id}.jpeg',
            f'raw/unsplash/{image_id}.jpg',
            f'raw/pexels/{image_id}.jpg',
        ]
        
        source_file = None
        for path in source_paths:
            if os.path.exists(path):
                source_file = path
                break
        
        if source_file:
            # 复制到public/images
            dest_file = os.path.join(public_images_dir, f'{image_id}.jpg')
            shutil.copy2(source_file, dest_file)
            copied_count += 1
            print(f"✅ 复制: {image_id}.jpg")
        else:
            print(f"⚠️ 未找到: {image_id}")
    
    print(f"\n✅ 成功复制 {copied_count} 张图片到 {public_images_dir}")
    
    # 更新数据库URL为相对路径
    print("\n📝 更新数据库URL...")
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE images 
        SET url_thumbnail = '/images/' || id || '.jpg',
            url_regular = '/images/' || id || '.jpg',
            url_download = '/images/' || id || '.jpg'
        WHERE tags != '[]'
    """)
    
    conn.commit()
    conn.close()
    print("✅ 数据库URL已更新")
    
    # 更新metadata.json
    print("\n📝 更新metadata.json...")
    with open('metadata.json', 'r') as f:
        metadata = json.load(f)
    
    metadata['lastUpdated'] = datetime.now().isoformat()
    for image in metadata['images']:
        image_id = image['id']
        local_url = f'/images/{image_id}.jpg'
        image['urls'] = {
            'thumbnail': local_url,
            'regular': local_url,
            'download': local_url
        }
    
    with open('metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print("✅ metadata.json已更新")
    
    # 创建一个说明文件
    with open('public/images/README.md', 'w') as f:
        f.write(f"""# 图片目录

此目录包含 {copied_count} 张图片，用于本地开发。

## 注意事项
- 这些图片是从 raw/pixabay 复制过来的
- 在生产环境中，这些图片应该从R2加载
- 运行 `python3 scripts/restore_r2_urls.py` 可以恢复R2的URL
""")
    
    print("\n🎉 设置完成！")
    print("   现在可以运行 npm run dev 查看网站")
    print("   所有图片都会从 /public/images 加载")

def main():
    setup_local_images()

if __name__ == '__main__':
    main()