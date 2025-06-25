#!/usr/bin/env python3
"""
使用增强的SEO元数据重新生成所有HTML页面
"""

import json
import os
from jinja2 import Environment, FileSystemLoader
import html

def regenerate_seo_pages():
    """基于增强的metadata重新生成所有HTML页面"""
    
    # 读取增强的metadata
    with open('dist/metadata_enhanced.json', 'r', encoding='utf-8') as f:
        images = json.load(f)
    
    print(f"📊 Found {len(images)} images with enhanced SEO data")
    
    # 设置模板环境
    env = Environment(loader=FileSystemLoader('templates'))
    
    # 创建SEO优化的首页模板
    create_seo_index_template()
    
    # 创建SEO优化的详情页模板
    create_seo_detail_template()
    
    # 重新加载模板
    env = Environment(loader=FileSystemLoader('templates'))
    index_template = env.get_template('index_seo_template.html')
    detail_template = env.get_template('detail_seo_template.html')
    
    # 生成首页
    index_html = index_template.render(
        images=images,
        total_images=len(images),
        site_description="Download free transparent PNG images for your projects. High-quality, no background images for designers, developers, and creators. Commercial use allowed, no attribution required."
    )
    
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("🏠 Generated SEO-optimized index.html")
    
    # 生成详情页
    for i, image in enumerate(images):
        # 计算前一张和后一张图片
        prev_image = images[i-1] if i > 0 else None
        next_image = images[i+1] if i < len(images)-1 else None
        
        # 渲染详情页
        detail_html = detail_template.render(
            title=image.get('seoTitle', image['title']),
            description=image.get('seoDescription', image['description']),
            image_url=image['imageUrl'],
            download_url=image['downloadUrl'],
            canonical_url=image.get('canonicalUrl', f"https://thinkora.pics/images/{image['id']}.html"),
            author_name=image['author'],
            author_url=image['authorUrl'],
            dimensions=f"{image.get('width', 'N/A')} x {image.get('height', 'N/A')}",
            file_size=format_file_size(image.get('fileSize', 0)),
            category=image['category'],
            tags=image.get('tags', []),
            keywords=image.get('seoKeywords', ''),
            structured_data=json.dumps(image.get('structuredData', {})),
            prev_image=prev_image,
            next_image=next_image,
            upload_date=image.get('uploadDate', ''),
            image_id=image['id']
        )
        
        # 写入文件
        detail_path = f"dist/images/{image['id']}.html"
        with open(detail_path, 'w', encoding='utf-8') as f:
            f.write(detail_html)
    
    print(f"🖼️  Generated {len(images)} SEO-optimized detail pages")
    
    # 更新原始metadata文件
    os.rename('dist/metadata.json', 'dist/metadata_old.json')
    os.rename('dist/metadata_enhanced.json', 'dist/metadata.json')
    
    print("✅ All pages regenerated with enhanced SEO!")
    print(f"📈 Website now has {len(images)} SEO-optimized images")

def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "N/A"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"

def create_seo_index_template():
    """创建SEO优化的首页模板"""
    template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Transparent PNG Images - Download High-Quality No Background Images | Thinkora.pics</title>
    <meta name="description" content="{{ site_description }}">
    <meta name="keywords" content="transparent png, free images, no background, png download, transparent images, free stock photos, design resources, commercial use">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://thinkora.pics/">
    
    <!-- Language -->
    <meta name="language" content="English">
    <meta http-equiv="content-language" content="en">
    
    <!-- SEO & Social -->
    <meta property="og:title" content="Thinkora.pics - Free Transparent PNG Images for Designers">
    <meta property="og:description" content="Download {{ total_images }}+ free transparent PNG images. Perfect for web design, presentations, and creative projects. No attribution required.">
    <meta property="og:image" content="https://img.thinkora.pics/images/og-image.png">
    <meta property="og:url" content="https://thinkora.pics">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Thinkora.pics">
    
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Free Transparent PNG Images - Thinkora.pics">
    <meta name="twitter:description" content="Download {{ total_images }}+ free transparent PNG images for your projects.">
    <meta name="twitter:image" content="https://img.thinkora.pics/images/og-image.png">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ImageGallery",
      "name": "Thinkora.pics - Free Transparent PNG Images",
      "description": "{{ site_description }}",
      "url": "https://thinkora.pics",
      "numberOfItems": {{ total_images }},
      "license": "https://creativecommons.org/publicdomain/zero/1.0/",
      "creator": {
        "@type": "Organization",
        "name": "Thinkora.pics",
        "url": "https://thinkora.pics"
      }
    }
    </script>
    
    <link rel="stylesheet" href="/public/css/styles-enhanced.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🖼️</text></svg>">
    
    <!-- Preconnect to CDN -->
    <link rel="preconnect" href="https://img.thinkora.pics">
    <link rel="dns-prefetch" href="https://img.thinkora.pics">
</head>
<body>

    <header class="site-header">
        <h1 class="site-title">Thinkora.pics</h1>
        <p class="site-tagline">Free Transparent PNG Images for Your Projects</p>
    </header>

    <main class="container">
        <!-- Search Section -->
        <div class="search-container">
            <div class="search-wrapper">
                <input type="text" id="search-input" class="search-input" placeholder="Search {{ total_images }}+ transparent images..." aria-label="Search images">
                <button id="clear-search" class="clear-search-btn" style="display: none;" aria-label="Clear search">×</button>
            </div>
            <div id="search-info" class="search-info">{{ total_images }} free transparent PNG images available</div>
        </div>

        <div class="image-grid" id="image-grid">
            {% for image in images %}
            <article class="image-card">
                <a href="/images/{{ image.id }}.html" title="{{ image.seoTitle }}">
                    <div class="image-card__image-wrapper">
                        <img src="{{ image.imageUrl }}" 
                             alt="{{ image.seoTitle }}" 
                             loading="lazy" 
                             width="{{ image.width }}" 
                             height="{{ image.height }}">
                    </div>
                    <div class="image-card__content">
                        <h2 class="image-card__title">{{ image.seoTitle }}</h2>
                        {% if image.tags %}
                        <div class="image-card__tags">
                            {% for tag in image.tags[:3] %}
                                <span class="image-card__tag">{{ tag }}</span>
                            {% endfor %}
                        </div>
                        {% endif %}
                        <div class="image-card__footer">
                            <span class="image-card__size">{{ image.width }}×{{ image.height }}</span>
                            <span class="image-card__author">by {{ image.author }}</span>
                        </div>
                    </div>
                </a>
            </article>
            {% endfor %}
        </div>
    </main>

    <footer class="site-footer">
        <p>&copy; 2024 Thinkora.pics. All images are free for commercial use. No attribution required.</p>
        <p><a href="/sitemap.xml">Sitemap</a> | <a href="/about">About</a> | <a href="/terms">Terms</a></p>
    </footer>

    <script src="/public/js/main-enhanced.js"></script>
</body>
</html>'''
    
    with open('templates/index_seo_template.html', 'w', encoding='utf-8') as f:
        f.write(template_content)

def create_seo_detail_template():
    """创建SEO优化的详情页模板"""
    template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Free Download | Thinkora.pics</title>
    <meta name="description" content="{{ description }}">
    <meta name="keywords" content="{{ keywords }}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{{ canonical_url }}">
    
    <!-- Language -->
    <meta name="language" content="English">
    <meta http-equiv="content-language" content="en">
    
    <!-- SEO & Social -->
    <meta property="og:title" content="{{ title }} - Thinkora.pics">
    <meta property="og:description" content="{{ description }}">
    <meta property="og:image" content="{{ image_url }}">
    <meta property="og:url" content="{{ canonical_url }}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Thinkora.pics">
    <meta property="article:published_time" content="{{ upload_date }}">
    <meta property="article:author" content="{{ author_name }}">
    <meta property="article:tag" content="{{ category }}">
    
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{ title }}">
    <meta name="twitter:description" content="{{ description }}">
    <meta name="twitter:image" content="{{ image_url }}">
    
    <!-- Image specific meta -->
    <meta property="og:image:width" content="{{ dimensions.split(' x ')[0] }}">
    <meta property="og:image:height" content="{{ dimensions.split(' x ')[1] }}">
    <meta property="og:image:type" content="image/png">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{ structured_data }}
    </script>
    
    <!-- Breadcrumb Structured Data -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "item": {
            "@id": "https://thinkora.pics",
            "name": "Home"
          }
        },
        {
          "@type": "ListItem",
          "position": 2,
          "item": {
            "@id": "https://thinkora.pics/category/{{ category }}",
            "name": "{{ category|title }}"
          }
        },
        {
          "@type": "ListItem",
          "position": 3,
          "item": {
            "@id": "{{ canonical_url }}",
            "name": "{{ title }}"
          }
        }
      ]
    }
    </script>
    
    <link rel="stylesheet" href="/public/css/styles-enhanced.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🖼️</text></svg>">
    
    <!-- Preload image -->
    <link rel="preload" as="image" href="{{ image_url }}">
</head>
<body>

    <header class="site-header">
        <div class="site-title"><a href="/">Thinkora.pics</a></div>
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="/">Home</a> › 
            <a href="/category/{{ category }}">{{ category|title }}</a> › 
            <span aria-current="page">{{ title }}</span>
        </nav>
    </header>

    <main class="container">
        <article class="detail-container">
            <div class="detail-image-wrapper">
                <a href="{{ download_url }}" download="{{ title }}.png" title="Click to download {{ title }}">
                    <img src="{{ image_url }}" 
                         alt="{{ title }} - {{ description }}" 
                         loading="eager"
                         width="{{ dimensions.split(' x ')[0] }}"
                         height="{{ dimensions.split(' x ')[1] }}">
                </a>
            </div>
            <div class="detail-info">
                <h1>{{ title }}</h1>
                <p class="description">{{ description }}</p>
                
                <dl class="detail-meta">
                    <dt>Author:</dt>
                    <dd><a href="{{ author_url }}" target="_blank" rel="noopener noreferrer">{{ author_name }}</a></dd>
                    
                    <dt>Dimensions:</dt>
                    <dd>{{ dimensions }} pixels</dd>
                    
                    <dt>File Size:</dt>
                    <dd>{{ file_size }}</dd>
                    
                    <dt>Category:</dt>
                    <dd><a href="/category/{{ category }}">{{ category|title }}</a></dd>
                    
                    <dt>Format:</dt>
                    <dd>PNG (Transparent Background)</dd>
                    
                    <dt>License:</dt>
                    <dd>Free for commercial use, no attribution required</dd>
                </dl>
                
                {% if tags %}
                <div class="tags-section">
                    <h2>Related Tags</h2>
                    <div class="tags">
                        {% for tag in tags %}
                        <a href="/tag/{{ tag|lower|replace(' ', '-') }}" class="tag">{{ tag }}</a>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
                
                <div class="download-section">
                    <a href="{{ download_url }}" class="download-button" download>
                        Download Free PNG
                    </a>
                    <p class="download-info">Right-click and "Save as" if download doesn't start</p>
                </div>
                
                <nav class="detail-nav" aria-label="Image navigation">
                    {% if prev_image %}
                        <a href="/images/{{ prev_image.id }}.html" 
                           rel="prev" 
                           title="{{ prev_image.seoTitle }}">&laquo; Previous</a>
                    {% endif %}
                    {% if next_image %}
                        <a href="/images/{{ next_image.id }}.html" 
                           rel="next" 
                           title="{{ next_image.seoTitle }}">Next &raquo;</a>
                    {% endif %}
                </nav>
            </div>
        </article>
    </main>

    <footer class="site-footer">
        <p>&copy; 2024 Thinkora.pics. Free transparent PNG images for commercial use.</p>
        <p><a href="/sitemap.xml">Sitemap</a> | <a href="/">Browse All Images</a></p>
    </footer>

    <script src="/public/js/download-force.js"></script>
</body>
</html>'''
    
    with open('templates/detail_seo_template.html', 'w', encoding='utf-8') as f:
        f.write(template_content)

if __name__ == "__main__":
    print("🔄 Regenerating website with enhanced SEO...")
    regenerate_seo_pages()