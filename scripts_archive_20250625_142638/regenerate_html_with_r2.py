#!/usr/bin/env python3
"""
使用新的R2 URL重新生成所有HTML页面
"""

import json
import os
import shutil
from datetime import datetime

def load_metadata():
    """加载metadata文件"""
    with open('metadata.json', 'r') as f:
        return json.load(f)

def generate_index_page(metadata):
    """生成主页"""
    images = metadata['images']
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Free HD Images & Stock Photos - ThinkOra.pics">
    <title>Free HD Images & Stock Photos - ThinkOra.pics</title>
    <link rel="stylesheet" href="/css/styles-enhanced.css">
    <style>
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        .image-card {
            position: relative;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .image-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
        .image-card img {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }
        .image-info {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
            color: white;
            padding: 20px 15px 15px;
        }
        .image-title {
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 5px;
        }
        .image-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .tag {
            background: rgba(255,255,255,0.2);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Free HD Images & Stock Photos</h1>
        <p>Discover high-quality images for your projects</p>
    </header>
    
    <main>
        <div class="image-grid">
"""
    
    for image in images[:48]:  # Show first 48 images on homepage
        tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in image['tags'][:3]])
        
        html_content += f"""
            <div class="image-card">
                <a href="/images/images/{image['id']}.html">
                    <img src="{image['urls']['thumbnail']}" alt="{image['title']}" loading="lazy">
                    <div class="image-info">
                        <div class="image-title">{image['title']}</div>
                        <div class="image-tags">{tags_html}</div>
                    </div>
                </a>
            </div>
"""
    
    html_content += """
        </div>
    </main>
    
    <footer>
        <p>&copy; 2025 ThinkOra.pics - Free Images for Everyone</p>
    </footer>
</body>
</html>"""
    
    # 保存主页
    os.makedirs('images', exist_ok=True)
    with open('images/index.html', 'w') as f:
        f.write(html_content)
    
    # 也保存到根目录
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print("✓ Generated index.html")

def generate_detail_pages(metadata):
    """生成详情页面"""
    images = metadata['images']
    os.makedirs('images/images', exist_ok=True)
    
    for i, image in enumerate(images):
        # 找到前后图片
        prev_image = images[i-1] if i > 0 else None
        next_image = images[i+1] if i < len(images)-1 else None
        
        # 生成标签HTML
        tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in image['tags']])
        
        # 生成相关图片
        related_images = []
        for other in images:
            if other['id'] != image['id'] and len(related_images) < 6:
                # 检查是否有共同标签
                if any(tag in other['tags'] for tag in image['tags']):
                    related_images.append(other)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{image['description']}">
    <meta property="og:title" content="{image['title']}">
    <meta property="og:description" content="{image['description']}">
    <meta property="og:image" content="{image['urls']['regular']}">
    <meta property="og:url" content="https://thinkora.pics/images/images/{image['id']}.html">
    <title>{image['title']} - ThinkOra.pics</title>
    <link rel="stylesheet" href="/css/styles-enhanced.css">
    <style>
        .detail-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .image-main {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .image-main img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .image-meta {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }}
        .tag {{
            background: #e0e0e0;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
        }}
        .download-btn {{
            background: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
        }}
        .download-btn:hover {{
            background: #45a049;
        }}
        .navigation {{
            display: flex;
            justify-content: space-between;
            margin: 30px 0;
        }}
        .nav-btn {{
            padding: 10px 20px;
            background: #f0f0f0;
            border-radius: 5px;
            text-decoration: none;
            color: #333;
        }}
        .related-images {{
            margin-top: 50px;
        }}
        .related-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .related-item {{
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .related-item img {{
            width: 100%;
            height: 150px;
            object-fit: cover;
        }}
    </style>
</head>
<body>
    <header>
        <h1><a href="/">ThinkOra.pics</a></h1>
    </header>
    
    <main class="detail-container">
        <div class="navigation">
            {f'<a href="{prev_image["id"]}.html" class="nav-btn">← Previous</a>' if prev_image else '<span></span>'}
            <a href="/" class="nav-btn">Home</a>
            {f'<a href="{next_image["id"]}.html" class="nav-btn">Next →</a>' if next_image else '<span></span>'}
        </div>
        
        <div class="image-main">
            <img src="{image['urls']['regular']}" alt="{image['title']}">
        </div>
        
        <div class="image-meta">
            <h2>{image['title']}</h2>
            <p>{image['description']}</p>
            
            <div class="tags">
                {tags_html}
            </div>
            
            <p><strong>Dimensions:</strong> {image['dimensions']['width']} × {image['dimensions']['height']} px</p>
            <p><strong>Author:</strong> <a href="{image['author']['url']}" target="_blank">{image['author']['name']}</a></p>
            <p><strong>Category:</strong> {image['category']}</p>
            
            <a href="{image['urls']['download']}" class="download-btn" download>Download Free Image</a>
        </div>
        
        <div class="related-images">
            <h3>Related Images</h3>
            <div class="related-grid">
"""
        
        for related in related_images:
            html_content += f"""
                <a href="{related['id']}.html" class="related-item">
                    <img src="{related['urls']['thumbnail']}" alt="{related['title']}" loading="lazy">
                </a>
"""
        
        html_content += """
            </div>
        </div>
    </main>
    
    <footer>
        <p>&copy; 2025 ThinkOra.pics - Free Images for Everyone</p>
    </footer>
    
    <script src="/js/download-handler.js"></script>
</body>
</html>"""
        
        # 保存详情页
        with open(f'images/images/{image["id"]}.html', 'w') as f:
            f.write(html_content)
    
    print(f"✓ Generated {len(images)} detail pages")

def generate_sitemap(metadata):
    """生成sitemap.xml"""
    images = metadata['images']
    
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://thinkora.pics/</loc>
        <lastmod>{}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
""".format(datetime.now().strftime('%Y-%m-%d'))
    
    for image in images:
        sitemap_content += f"""    <url>
        <loc>https://thinkora.pics/images/images/{image['id']}.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
"""
    
    sitemap_content += "</urlset>"
    
    with open('images/sitemap.xml', 'w') as f:
        f.write(sitemap_content)
    
    # 也保存到根目录
    with open('sitemap.xml', 'w') as f:
        f.write(sitemap_content)
    
    print("✓ Generated sitemap.xml")

def generate_robots_txt():
    """生成robots.txt"""
    robots_content = """User-agent: *
Allow: /

Sitemap: https://thinkora.pics/sitemap.xml
"""
    
    with open('images/robots.txt', 'w') as f:
        f.write(robots_content)
    
    # 也保存到根目录
    with open('robots.txt', 'w') as f:
        f.write(robots_content)
    
    print("✓ Generated robots.txt")

def copy_static_files():
    """复制静态文件"""
    # 复制CSS和JS文件
    if os.path.exists('public'):
        if os.path.exists('public/css'):
            os.makedirs('images/public/css', exist_ok=True)
            for file in os.listdir('public/css'):
                shutil.copy2(f'public/css/{file}', f'images/public/css/{file}')
        
        if os.path.exists('public/js'):
            os.makedirs('images/public/js', exist_ok=True)
            for file in os.listdir('public/js'):
                shutil.copy2(f'public/js/{file}', f'images/public/js/{file}')
    
    print("✓ Copied static files")

def main():
    """主函数"""
    print("=== Regenerating HTML with R2 URLs ===\n")
    
    # 加载metadata
    metadata = load_metadata()
    print(f"Loaded {metadata['totalImages']} images from metadata")
    
    # 生成页面
    generate_index_page(metadata)
    generate_detail_pages(metadata)
    generate_sitemap(metadata)
    generate_robots_txt()
    copy_static_files()
    
    print("\n✓ All pages regenerated with R2 URLs")
    print("\nNext steps:")
    print("1. Deploy the 'images' directory to your web server")
    print("2. Ensure R2 bucket is publicly accessible")
    print("3. Configure CORS on R2 if needed")
    print("4. Test image loading in browser")

if __name__ == "__main__":
    main()