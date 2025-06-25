#!/usr/bin/env python3
"""
验证R2集成是否正常工作
"""

import json
import sqlite3
import os
from collections import Counter

def verify_database_urls():
    """验证数据库中的URL是否已更新到R2"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 检查带标签图片的URL
    cursor.execute("""
    SELECT id, url_thumbnail, url_regular, url_download 
    FROM images 
    WHERE tags IS NOT NULL AND tags != '[]' AND tags != ''
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    r2_count = 0
    non_r2_count = 0
    
    for row in rows:
        image_id, thumbnail, regular, download = row
        
        # 检查是否指向R2
        if 'r2.thinkora.pics' in str(thumbnail):
            r2_count += 1
        else:
            non_r2_count += 1
            print(f"Non-R2 URL found: {image_id} - {thumbnail}")
    
    print(f"\n数据库URL验证结果:")
    print(f"- R2 URLs: {r2_count}")
    print(f"- Non-R2 URLs: {non_r2_count}")
    
    return r2_count, non_r2_count

def verify_metadata_file():
    """验证metadata.json文件"""
    with open('metadata.json', 'r') as f:
        metadata = json.load(f)
    
    total_images = metadata.get('totalImages', 0)
    images = metadata.get('images', [])
    
    r2_images = 0
    non_r2_images = 0
    
    for image in images:
        urls = image.get('urls', {})
        if 'r2.thinkora.pics' in urls.get('thumbnail', ''):
            r2_images += 1
        else:
            non_r2_images += 1
    
    print(f"\nMetadata文件验证结果:")
    print(f"- 总图片数: {total_images}")
    print(f"- 实际图片数: {len(images)}")
    print(f"- R2 URLs: {r2_images}")
    print(f"- Non-R2 URLs: {non_r2_images}")
    
    # 检查tags分布
    all_tags = []
    for image in images:
        all_tags.extend(image.get('tags', []))
    
    tag_counts = Counter(all_tags)
    print(f"\n标签统计 (前10个):")
    for tag, count in tag_counts.most_common(10):
        print(f"  - {tag}: {count}")
    
    return r2_images, non_r2_images

def check_html_pages():
    """检查HTML页面是否存在"""
    image_pages_dir = 'images/images'
    
    if os.path.exists(image_pages_dir):
        html_files = [f for f in os.listdir(image_pages_dir) if f.endswith('.html')]
        print(f"\nHTML页面检查:")
        print(f"- 找到 {len(html_files)} 个HTML文件")
        
        # 检查几个示例文件的内容
        if html_files:
            sample_file = os.path.join(image_pages_dir, html_files[0])
            with open(sample_file, 'r') as f:
                content = f.read()
                if 'r2.thinkora.pics' in content:
                    print("- HTML文件已包含R2 URLs ✓")
                else:
                    print("- HTML文件仍使用旧URLs ✗")
    else:
        print(f"\n警告: 未找到HTML页面目录 {image_pages_dir}")

def check_local_files():
    """检查本地文件是否存在"""
    with open('simulated_r2_upload.json', 'r') as f:
        upload_records = json.load(f)
    
    existing_files = 0
    missing_files = 0
    
    for record in upload_records:
        if record['local_path'] and os.path.exists(record['local_path']):
            existing_files += 1
        else:
            missing_files += 1
    
    print(f"\n本地文件检查:")
    print(f"- 存在的文件: {existing_files}")
    print(f"- 缺失的文件: {missing_files}")

def generate_test_html():
    """生成测试HTML页面"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>R2 Integration Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        .image-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .image-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        .image-info {
            padding: 10px;
        }
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 10px;
        }
        .tag {
            background: #e0e0e0;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        .status {
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>R2 Integration Test Page</h1>
    <div class="status">
        <h2>Status</h2>
        <p>This page tests R2 image loading. If images appear below, R2 integration is working.</p>
    </div>
    <div class="gallery" id="gallery"></div>
    
    <script>
        // Load metadata and display images
        fetch('metadata.json')
            .then(response => response.json())
            .then(data => {
                const gallery = document.getElementById('gallery');
                const images = data.images.slice(0, 12); // Show first 12 images
                
                images.forEach(image => {
                    const card = document.createElement('div');
                    card.className = 'image-card';
                    
                    const img = document.createElement('img');
                    img.src = image.urls.thumbnail;
                    img.alt = image.title;
                    img.onerror = function() {
                        this.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="250" height="200"%3E%3Crect width="250" height="200" fill="%23ccc"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23666"%3EFailed to load%3C/text%3E%3C/svg%3E';
                    };
                    
                    const info = document.createElement('div');
                    info.className = 'image-info';
                    info.innerHTML = `
                        <h4>${image.title}</h4>
                        <p>ID: ${image.id}</p>
                        <div class="tags">
                            ${image.tags.slice(0, 3).map(tag => 
                                `<span class="tag">${tag}</span>`
                            ).join('')}
                        </div>
                    `;
                    
                    card.appendChild(img);
                    card.appendChild(info);
                    gallery.appendChild(card);
                });
                
                console.log('Loaded ' + images.length + ' images');
            })
            .catch(error => {
                console.error('Error loading metadata:', error);
                document.getElementById('gallery').innerHTML = 
                    '<p style="color: red;">Error loading metadata.json</p>';
            });
    </script>
</body>
</html>"""
    
    with open('test_r2_integration.html', 'w') as f:
        f.write(html_content)
    
    print("\n测试HTML页面已生成: test_r2_integration.html")
    print("请在浏览器中打开此文件测试R2图片加载")

def main():
    """主函数"""
    print("=== R2集成验证 ===\n")
    
    # 1. 验证数据库
    db_r2, db_non_r2 = verify_database_urls()
    
    # 2. 验证metadata文件
    meta_r2, meta_non_r2 = verify_metadata_file()
    
    # 3. 检查HTML页面
    check_html_pages()
    
    # 4. 检查本地文件
    check_local_files()
    
    # 5. 生成测试页面
    generate_test_html()
    
    # 总结
    print("\n" + "="*50)
    print("验证总结:")
    
    if db_r2 > 0 and db_non_r2 == 0:
        print("✓ 数据库URL已全部更新到R2")
    else:
        print("✗ 数据库中仍有非R2的URL")
    
    if meta_r2 > 0 and meta_non_r2 == 0:
        print("✓ Metadata文件已全部更新到R2")
    else:
        print("✗ Metadata文件中仍有非R2的URL")
    
    print("\n建议:")
    print("1. 打开 test_r2_integration.html 测试图片加载")
    print("2. 如果图片无法加载，需要:")
    print("   - 检查R2存储桶的公开访问设置")
    print("   - 确认CORS配置正确")
    print("   - 验证域名解析是否正常")
    print("3. 运行 regenerate-html.py 重新生成所有HTML页面")

if __name__ == "__main__":
    main()