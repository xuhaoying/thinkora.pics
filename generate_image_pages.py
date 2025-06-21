#!/usr/bin/env python3
"""
为每个图片生成独立的HTML页面，用于SEO优化
"""

import json
import os
from datetime import datetime

def create_image_page_template():
    """创建图片详情页模板"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title} - Free Transparent PNG">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_url}">
    <title>{title} - Transparent PNG Download | Free High Quality</title>
    <link rel="canonical" href="https://thinkora.pics/images/{slug}.html">
    <style>
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --background: #0f172a;
            --surface: #1e293b;
            --surface-light: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border: #334155;
            --radius: 12px;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--background);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .header {{
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
            padding: 1.5rem 0;
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            text-decoration: none;
        }}
        
        .nav-links {{
            display: flex;
            gap: 2rem;
        }}
        
        .nav-link {{
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        .nav-link:hover {{
            color: var(--text-primary);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}
        
        .breadcrumb {{
            margin-bottom: 2rem;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}
        
        .breadcrumb a {{
            color: var(--primary);
            text-decoration: none;
        }}
        
        .image-detail {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            margin-bottom: 4rem;
        }}
        
        .image-preview {{
            background: repeating-conic-gradient(#1e293b 0% 25%, #334155 0% 50%) 50% / 20px 20px;
            border-radius: var(--radius);
            padding: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .image-preview img {{
            max-width: 100%;
            max-height: 500px;
            object-fit: contain;
        }}
        
        .image-info {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        .image-info h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1.2;
        }}
        
        .author-info {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
        }}
        
        .author-info a {{
            color: var(--primary);
            text-decoration: none;
        }}
        
        .image-meta {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            padding: 1.5rem;
            background: var(--surface);
            border-radius: var(--radius);
        }}
        
        .meta-item {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}
        
        .meta-label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}
        
        .meta-value {{
            font-size: 1.125rem;
            font-weight: 600;
        }}
        
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        .tag {{
            padding: 0.375rem 1rem;
            background: var(--surface-light);
            border-radius: 999px;
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        .tag:hover {{
            background: var(--primary);
            color: white;
        }}
        
        .download-section {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .download-button {{
            padding: 1rem 2rem;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: var(--radius);
            font-size: 1.125rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            text-decoration: none;
            display: inline-block;
        }}
        
        .download-button:hover {{
            background: var(--primary-dark);
            transform: translateY(-2px);
        }}
        
        .license-note {{
            padding: 1rem;
            background: var(--surface);
            border-radius: var(--radius);
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}
        
        .related-images {{
            margin-top: 4rem;
        }}
        
        .related-images h2 {{
            font-size: 1.75rem;
            margin-bottom: 2rem;
        }}
        
        .related-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
        }}
        
        .related-card {{
            background: var(--surface);
            border-radius: var(--radius);
            overflow: hidden;
            transition: all 0.3s;
            text-decoration: none;
        }}
        
        .related-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}
        
        .related-card img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            background: repeating-conic-gradient(#1e293b 0% 25%, #334155 0% 50%) 50% / 20px 20px;
        }}
        
        .related-card-info {{
            padding: 1rem;
        }}
        
        .related-card-title {{
            color: var(--text-primary);
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}
        
        .related-card-meta {{
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}
        
        @media (max-width: 768px) {{
            .image-detail {{
                grid-template-columns: 1fr;
                gap: 2rem;
            }}
            
            .image-info h1 {{
                font-size: 1.75rem;
            }}
            
            .nav-links {{
                gap: 1rem;
            }}
            
            .related-grid {{
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 1rem;
            }}
        }}
    </style>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "ImageObject",
        "name": "{title}",
        "description": "{description}",
        "contentUrl": "{image_url}",
        "thumbnailUrl": "{image_url}",
        "uploadDate": "{created_at}",
        "author": {{
            "@type": "Person",
            "name": "{author_name}",
            "url": "{author_url}"
        }},
        "keywords": "{keywords}",
        "encodingFormat": "image/png",
        "width": {{
            "@type": "QuantitativeValue",
            "value": {width}
        }},
        "height": {{
            "@type": "QuantitativeValue",
            "value": {height}
        }}
    }}
    </script>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="/" class="logo">
                <span>🖼️</span>
                <span>Transparent PNG Hub</span>
            </a>
            <nav class="nav-links">
                <a href="/" class="nav-link">Browse</a>
                <a href="/#about" class="nav-link">About</a>
                <a href="/#license" class="nav-link">License</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <nav class="breadcrumb">
            <a href="/">Home</a> / <a href="/?category={category}">{category_display}</a> / {title}
        </nav>

        <div class="image-detail">
            <div class="image-preview">
                <img src="{image_url}" alt="{title}" loading="eager">
            </div>
            
            <div class="image-info">
                <h1>{title}</h1>
                
                <div class="author-info">
                    <span>Photo by</span>
                    <a href="{author_url}" target="_blank" rel="noopener">{author_name}</a>
                    <span>on</span>
                    <a href="https://unsplash.com" target="_blank" rel="noopener">Unsplash</a>
                </div>
                
                <p>{description}</p>
                
                <div class="image-meta">
                    <div class="meta-item">
                        <span class="meta-label">Dimensions</span>
                        <span class="meta-value">{width} × {height}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">File Size</span>
                        <span class="meta-value">{file_size}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Aspect Ratio</span>
                        <span class="meta-value">{ratio}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Quality Score</span>
                        <span class="meta-value">{quality_score}%</span>
                    </div>
                </div>
                
                <div class="tags">
                    {tags_html}
                </div>
                
                <div class="download-section">
                    <a href="{download_url}" class="download-button" download="{filename}">
                        Download PNG ({file_size})
                    </a>
                    <div class="license-note">
                        ⚖️ Free to use under the Unsplash License. Please provide attribution to <a href="{author_url}" target="_blank">{author_name}</a>.
                    </div>
                </div>
            </div>
        </div>

        <section class="related-images">
            <h2>Related Transparent PNGs</h2>
            <div class="related-grid">
                {related_html}
            </div>
        </section>
    </main>

    <script>
        // Download tracking
        document.querySelector('.download-button').addEventListener('click', function() {{
            console.log('Download:', '{title}');
        }});
    </script>
</body>
</html>'''

def generate_sitemap(pages):
    """生成sitemap.xml"""
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://thinkora.pics/</loc>
        <lastmod>{}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
'''.format(datetime.now().strftime('%Y-%m-%d'))
    
    for page in pages:
        sitemap += '''    <url>
        <loc>https://thinkora.pics/images/{}.html</loc>
        <lastmod>{}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
'''.format(page['slug'], datetime.now().strftime('%Y-%m-%d'))
    
    sitemap += '</urlset>'
    return sitemap

def create_image_pages():
    """为每个图片创建独立页面"""
    # 读取元数据
    with open('metadata.json', 'r', encoding='utf-8') as f:
        images = json.load(f)
    
    # 创建images目录
    os.makedirs('images', exist_ok=True)
    
    # 获取模板
    template = create_image_page_template()
    
    pages = []
    
    for idx, img in enumerate(images):
        # 生成slug（URL友好的ID）
        slug = img['id'].replace('unsplash_', '')
        
        # 生成标签HTML
        tags_html = ' '.join([
            f'<a href="/?tag={tag}" class="tag">{tag}</a>'
            for tag in img['tags']
        ])
        
        # 获取相关图片（同类别的其他图片）
        related_images = [
            other for other in images 
            if other['category'] == img['category'] 
            and other['id'] != img['id']
        ][:4]  # 最多4个相关图片
        
        # 生成相关图片HTML
        related_html = ''
        for related in related_images:
            related_slug = related['id'].replace('unsplash_', '')
            related_html += f'''
                <a href="/images/{related_slug}.html" class="related-card">
                    <img src="{related['urls']['thumbnail']}" alt="{related['title']}" loading="lazy">
                    <div class="related-card-info">
                        <div class="related-card-title">{related['title']}</div>
                        <div class="related-card-meta">{related['dimensions']['width']} × {related['dimensions']['height']}</div>
                    </div>
                </a>
            '''
        
        # 填充模板
        page_html = template.format(
            title=img['title'],
            description=img['description'],
            image_url=img['urls']['regular'],
            download_url=img['urls']['download'],
            filename=f"{slug}.png",
            slug=slug,
            author_name=img['author']['name'],
            author_url=img['author']['url'],
            width=img['dimensions']['width'],
            height=img['dimensions']['height'],
            ratio=img['dimensions']['ratio'],
            file_size=img['file_size'],
            quality_score=img['quality_score'],
            category=img['category'],
            category_display=img['category'].title(),
            tags_html=tags_html,
            keywords=', '.join(img['tags']),
            created_at=img['created_at'],
            related_html=related_html
        )
        
        # 写入文件
        with open(f'images/{slug}.html', 'w', encoding='utf-8') as f:
            f.write(page_html)
        
        pages.append({'slug': slug, 'title': img['title']})
        print(f"Created page: images/{slug}.html")
    
    # 生成sitemap
    sitemap_content = generate_sitemap(pages)
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"\n✅ Created {len(pages)} image pages")
    print("✅ Generated sitemap.xml")
    
    # 生成页面列表（可选，用于主页链接）
    with open('image_pages.json', 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    create_image_pages()