#!/usr/bin/env python3
"""
综合SEO优化器 - 全面优化thinkora.pics网站的SEO
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any
import urllib.parse

class ComprehensiveSEOOptimizer:
    def __init__(self):
        self.metadata_file = 'dist/metadata.json'
        self.base_url = 'https://thinkora.pics'
        self.site_name = 'Thinkora.pics'
        self.site_description = 'Free transparent PNG images for designers and developers'
        
        # 分类映射和SEO优化
        self.category_info = {
            'business': {
                'title': 'Business & Office',
                'description': 'Professional business and office transparent PNG images',
                'keywords': ['business', 'office', 'professional', 'corporate', 'work', 'meeting'],
                'h1': 'Business & Professional PNG Images'
            },
            'technology': {
                'title': 'Technology & Digital',
                'description': 'Tech and digital innovation transparent PNG images',
                'keywords': ['technology', 'tech', 'digital', 'computer', 'software', 'innovation'],
                'h1': 'Technology & Digital PNG Images'
            },
            'nature': {
                'title': 'Nature & Environment',
                'description': 'Natural landscapes and environmental transparent PNG images',
                'keywords': ['nature', 'natural', 'outdoor', 'environment', 'landscape', 'scenic'],
                'h1': 'Nature & Environmental PNG Images'
            },
            'food': {
                'title': 'Food & Culinary',
                'description': 'Delicious food and culinary transparent PNG images',
                'keywords': ['food', 'cuisine', 'culinary', 'restaurant', 'cooking', 'meal'],
                'h1': 'Food & Culinary PNG Images'
            },
            'people': {
                'title': 'People & Lifestyle',
                'description': 'People portraits and lifestyle transparent PNG images',
                'keywords': ['people', 'person', 'portrait', 'human', 'lifestyle', 'social'],
                'h1': 'People & Lifestyle PNG Images'
            },
            'travel': {
                'title': 'Travel & Tourism',
                'description': 'Travel destinations and tourism transparent PNG images',
                'keywords': ['travel', 'tourism', 'vacation', 'destination', 'journey', 'adventure'],
                'h1': 'Travel & Tourism PNG Images'
            },
            'health': {
                'title': 'Health & Medical',
                'description': 'Healthcare and medical transparent PNG images',
                'keywords': ['health', 'medical', 'healthcare', 'wellness', 'fitness', 'medicine'],
                'h1': 'Health & Medical PNG Images'
            },
            'education': {
                'title': 'Education & Learning',
                'description': 'Educational and learning transparent PNG images',
                'keywords': ['education', 'learning', 'school', 'study', 'knowledge', 'academic'],
                'h1': 'Education & Learning PNG Images'
            },
            'sports': {
                'title': 'Sports & Fitness',
                'description': 'Sports and athletic transparent PNG images',
                'keywords': ['sports', 'athletic', 'fitness', 'exercise', 'game', 'competition'],
                'h1': 'Sports & Fitness PNG Images'
            },
            'animals': {
                'title': 'Animals & Wildlife',
                'description': 'Cute animals and wildlife transparent PNG images',
                'keywords': ['animals', 'pets', 'wildlife', 'fauna', 'creatures', 'domestic'],
                'h1': 'Animals & Wildlife PNG Images'
            }
        }
    
    def generate_seo_friendly_url(self, image: Dict[str, Any]) -> str:
        """生成SEO友好的URL"""
        tags = image.get('tags', [])
        category = image.get('category', 'general')
        
        # 选择最佳关键词
        if tags:
            main_keyword = max(tags, key=len)[:30]  # 最长的tag，限制30字符
        else:
            main_keyword = category
        
        # 清理和格式化URL
        url_slug = main_keyword.lower()
        url_slug = re.sub(r'[^a-z0-9]+', '-', url_slug)
        url_slug = url_slug.strip('-')
        
        # 添加图片ID确保唯一性
        image_id = image.get('id', '')
        if image_id.startswith('unsplash_'):
            url_slug = f"{url_slug}-{image_id.replace('unsplash_', 'us')}"
        elif image_id.startswith('pixabay_'):
            url_slug = f"{url_slug}-{image_id.replace('pixabay_', 'px')}"
        else:
            url_slug = f"{url_slug}-{image_id[:8]}"
        
        return url_slug
    
    def create_category_pages(self, images: List[Dict[str, Any]]):
        """创建分类页面"""
        categories = {}
        for image in images:
            cat = image.get('category', 'general')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(image)
        
        os.makedirs('dist/category', exist_ok=True)
        
        for category, cat_images in categories.items():
            cat_info = self.category_info.get(category, {
                'title': f"{category.title()} Images",
                'description': f"Free {category} transparent PNG images",
                'h1': f"{category.title()} PNG Images"
            })
            
            html_content = self.generate_category_page(category, cat_images, cat_info)
            
            with open(f'dist/category/{category}.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        print(f"✅ Created {len(categories)} category pages")
    
    def generate_category_page(self, category: str, images: List[Dict[str, Any]], cat_info: Dict[str, Any]) -> str:
        """生成分类页面HTML"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_info.get('title', category.title())} - Free Transparent PNG Download | Thinkora.pics</title>
    <meta name="description" content="{cat_info.get('description', f'Download {len(images)} free {category} transparent PNG images. High-quality, no background images for commercial use.')}">
    <meta name="keywords" content="{', '.join(cat_info.get('keywords', [category]))}">
    
    <link rel="canonical" href="{self.base_url}/category/{category}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{cat_info.get('title', category.title())} - Thinkora.pics">
    <meta property="og:description" content="{cat_info.get('description')}">
    <meta property="og:url" content="{self.base_url}/category/{category}">
    <meta property="og:type" content="website">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "{cat_info.get('title')}",
        "description": "{cat_info.get('description')}",
        "url": "{self.base_url}/category/{category}",
        "mainEntity": {{
            "@type": "ImageGallery",
            "name": "{cat_info.get('h1')}",
            "numberOfItems": {len(images)}
        }},
        "breadcrumb": {{
            "@type": "BreadcrumbList",
            "itemListElement": [
                {{
                    "@type": "ListItem",
                    "position": 1,
                    "item": {{
                        "@id": "{self.base_url}",
                        "name": "Home"
                    }}
                }},
                {{
                    "@type": "ListItem",
                    "position": 2,
                    "item": {{
                        "@id": "{self.base_url}/category/{category}",
                        "name": "{cat_info.get('title')}"
                    }}
                }}
            ]
        }}
    }}
    </script>
    
    <link rel="stylesheet" href="/public/css/styles-enhanced.css">
</head>
<body>
    <header class="site-header">
        <div class="site-title"><a href="/">Thinkora.pics</a></div>
        <nav class="breadcrumb">
            <a href="/">Home</a> › 
            <span>{cat_info.get('title')}</span>
        </nav>
    </header>
    
    <main class="container">
        <h1>{cat_info.get('h1')}</h1>
        <p class="category-description">{cat_info.get('description')} Browse our collection of {len(images)} high-quality transparent PNG images perfect for your creative projects.</p>
        
        <div class="image-grid">
            {"".join([self.generate_image_card(img) for img in images[:50]])}
        </div>
        
        {self.generate_pagination(len(images), 50, f'/category/{category}', 1) if len(images) > 50 else ''}
    </main>
    
    <footer class="site-footer">
        <p>&copy; 2024 Thinkora.pics. All images free for commercial use.</p>
        <nav>
            <a href="/">Home</a> |
            <a href="/about">About</a> |
            <a href="/terms">Terms</a> |
            <a href="/privacy">Privacy</a> |
            <a href="/sitemap.xml">Sitemap</a>
        </nav>
    </footer>
</body>
</html>"""
    
    def generate_image_card(self, image: Dict[str, Any]) -> str:
        """生成图片卡片HTML"""
        return f"""
            <article class="image-card">
                <a href="/images/{image['id']}.html" title="{image.get('seoTitle', image['title'])}">
                    <div class="image-card__image-wrapper">
                        <img src="{image['imageUrl']}" 
                             alt="{image.get('seoTitle', image['title'])}" 
                             loading="lazy" 
                             width="{image.get('width', '')}" 
                             height="{image.get('height', '')}">
                    </div>
                    <div class="image-card__content">
                        <h2 class="image-card__title">{image.get('seoTitle', image['title'])}</h2>
                        <div class="image-card__footer">
                            <span class="image-card__size">{image.get('width', 0)}×{image.get('height', 0)}</span>
                        </div>
                    </div>
                </a>
            </article>"""
    
    def generate_pagination(self, total: int, per_page: int, base_url: str, current_page: int) -> str:
        """生成分页HTML"""
        total_pages = (total + per_page - 1) // per_page
        if total_pages <= 1:
            return ""
        
        pagination_html = '<nav class="pagination" aria-label="Pagination">'
        
        # Previous button
        if current_page > 1:
            pagination_html += f'<a href="{base_url}/page/{current_page-1}" rel="prev">← Previous</a>'
        
        # Page numbers
        for page in range(1, min(total_pages + 1, 6)):
            if page == current_page:
                pagination_html += f'<span class="current">{page}</span>'
            else:
                pagination_html += f'<a href="{base_url}/page/{page}">{page}</a>'
        
        # Next button
        if current_page < total_pages:
            pagination_html += f'<a href="{base_url}/page/{current_page+1}" rel="next">Next →</a>'
        
        pagination_html += '</nav>'
        return pagination_html
    
    def create_static_pages(self):
        """创建静态页面（About, Terms, Privacy, 404）"""
        pages = {
            'about': self.generate_about_page(),
            'terms': self.generate_terms_page(),
            'privacy': self.generate_privacy_page(),
            '404': self.generate_404_page()
        }
        
        for filename, content in pages.items():
            with open(f'dist/{filename}.html', 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"✅ Created {len(pages)} static pages")
    
    def generate_about_page(self) -> str:
        """生成关于页面"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Thinkora.pics - Free Transparent PNG Images</title>
    <meta name="description" content="Learn about Thinkora.pics, your source for high-quality transparent PNG images free for commercial use.">
    <link rel="canonical" href="https://thinkora.pics/about">
    <link rel="stylesheet" href="/public/css/styles-enhanced.css">
</head>
<body>
    <header class="site-header">
        <div class="site-title"><a href="/">Thinkora.pics</a></div>
        <nav class="breadcrumb">
            <a href="/">Home</a> › About
        </nav>
    </header>
    
    <main class="container content-page">
        <h1>About Thinkora.pics</h1>
        
        <p>Welcome to Thinkora.pics, your premier destination for high-quality transparent PNG images that are completely free for commercial use.</p>
        
        <h2>Our Mission</h2>
        <p>We believe that great design resources should be accessible to everyone. Our mission is to provide designers, developers, and creators with a vast collection of transparent PNG images that can be used in any project without attribution requirements.</p>
        
        <h2>What We Offer</h2>
        <ul>
            <li>Over 400+ carefully curated transparent PNG images</li>
            <li>High-resolution images suitable for professional use</li>
            <li>No background - ready to use in your designs</li>
            <li>100% free for commercial and personal use</li>
            <li>No attribution required (though appreciated)</li>
            <li>Regular updates with new images</li>
        </ul>
        
        <h2>Image Categories</h2>
        <p>Our collection spans various categories including:</p>
        <ul>
            <li>Business & Professional</li>
            <li>Technology & Digital</li>
            <li>Nature & Environment</li>
            <li>Food & Culinary</li>
            <li>People & Lifestyle</li>
            <li>Travel & Tourism</li>
            <li>Health & Medical</li>
            <li>Education & Learning</li>
            <li>Sports & Fitness</li>
            <li>Animals & Wildlife</li>
        </ul>
        
        <h2>How to Use</h2>
        <ol>
            <li>Browse or search for the perfect image</li>
            <li>Click on any image to view details</li>
            <li>Download the PNG file instantly</li>
            <li>Use it in your project - no strings attached!</li>
        </ol>
        
        <h2>Contact Us</h2>
        <p>Have questions or suggestions? We'd love to hear from you! While we don't have a direct contact form, you can find us through our social media channels or community forums.</p>
    </main>
    
    <footer class="site-footer">
        <p>&copy; 2024 Thinkora.pics. All images free for commercial use.</p>
        <nav>
            <a href="/">Home</a> |
            <a href="/about">About</a> |
            <a href="/terms">Terms</a> |
            <a href="/privacy">Privacy</a> |
            <a href="/sitemap.xml">Sitemap</a>
        </nav>
    </footer>
</body>
</html>"""
    
    def generate_terms_page(self) -> str:
        """生成服务条款页面"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - Thinkora.pics</title>
    <meta name="description" content="Terms of service for using Thinkora.pics free transparent PNG images.">
    <link rel="canonical" href="https://thinkora.pics/terms">
    <link rel="stylesheet" href="/public/css/styles-enhanced.css">
</head>
<body>
    <header class="site-header">
        <div class="site-title"><a href="/">Thinkora.pics</a></div>
        <nav class="breadcrumb">
            <a href="/">Home</a> › Terms of Service
        </nav>
    </header>
    
    <main class="container content-page">
        <h1>Terms of Service</h1>
        <p class="last-updated">Last updated: December 2024</p>
        
        <h2>1. Acceptance of Terms</h2>
        <p>By accessing and using Thinkora.pics, you agree to be bound by these Terms of Service.</p>
        
        <h2>2. Use License</h2>
        <p>All images on Thinkora.pics are provided under the Creative Commons Zero (CC0) license, which means:</p>
        <ul>
            <li>You can use images for commercial and non-commercial purposes</li>
            <li>No attribution is required (though appreciated)</li>
            <li>You can modify, distribute, and use the images</li>
            <li>No permission is needed from the image author or Thinkora.pics</li>
        </ul>
        
        <h2>3. Prohibited Uses</h2>
        <p>While our images are free to use, you may NOT:</p>
        <ul>
            <li>Sell unmodified images as stock photos</li>
            <li>Use images in a way that depicts identifiable persons in a bad light</li>
            <li>Use images to mislead or deceive</li>
            <li>Imply endorsement of your product by people in the images</li>
        </ul>
        
        <h2>4. No Warranty</h2>
        <p>Images are provided "as is" without warranty of any kind. We do not guarantee that images will meet your specific requirements.</p>
        
        <h2>5. Limitation of Liability</h2>
        <p>Thinkora.pics shall not be liable for any damages arising from the use or inability to use images from our website.</p>
        
        <h2>6. Third-Party Content</h2>
        <p>Some images may be sourced from third-party providers. We ensure all images are properly licensed for free use.</p>
        
        <h2>7. Changes to Terms</h2>
        <p>We reserve the right to modify these terms at any time. Continued use of the site constitutes acceptance of modified terms.</p>
        
        <h2>8. Contact</h2>
        <p>For questions about these terms, please refer to our About page for contact information.</p>
    </main>
    
    <footer class="site-footer">
        <p>&copy; 2024 Thinkora.pics. All images free for commercial use.</p>
        <nav>
            <a href="/">Home</a> |
            <a href="/about">About</a> |
            <a href="/terms">Terms</a> |
            <a href="/privacy">Privacy</a> |
            <a href="/sitemap.xml">Sitemap</a>
        </nav>
    </footer>
</body>
</html>"""
    
    def generate_privacy_page(self) -> str:
        """生成隐私政策页面"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Thinkora.pics</title>
    <meta name="description" content="Privacy policy for Thinkora.pics - how we handle your data and protect your privacy.">
    <link rel="canonical" href="https://thinkora.pics/privacy">
    <link rel="stylesheet" href="/public/css/styles-enhanced.css">
</head>
<body>
    <header class="site-header">
        <div class="site-title"><a href="/">Thinkora.pics</a></div>
        <nav class="breadcrumb">
            <a href="/">Home</a> › Privacy Policy
        </nav>
    </header>
    
    <main class="container content-page">
        <h1>Privacy Policy</h1>
        <p class="last-updated">Last updated: December 2024</p>
        
        <h2>1. Information We Collect</h2>
        <p>Thinkora.pics is committed to protecting your privacy. We collect minimal information:</p>
        <ul>
            <li><strong>Analytics Data:</strong> We use privacy-focused analytics to understand site usage</li>
            <li><strong>Server Logs:</strong> Basic access logs for security and performance</li>
            <li><strong>No Personal Data:</strong> We do not require registration or collect personal information</li>
        </ul>
        
        <h2>2. How We Use Information</h2>
        <p>The limited information we collect is used to:</p>
        <ul>
            <li>Improve website performance and user experience</li>
            <li>Understand which images are most popular</li>
            <li>Protect against abuse and maintain security</li>
        </ul>
        
        <h2>3. Cookies</h2>
        <p>We use minimal cookies:</p>
        <ul>
            <li>Session cookies for basic functionality</li>
            <li>Analytics cookies (can be disabled)</li>
            <li>No tracking or advertising cookies</li>
        </ul>
        
        <h2>4. Third-Party Services</h2>
        <p>We use the following third-party services:</p>
        <ul>
            <li><strong>CDN (Content Delivery Network):</strong> For faster image delivery</li>
            <li><strong>Analytics:</strong> Privacy-focused analytics service</li>
        </ul>
        
        <h2>5. Data Security</h2>
        <p>We implement appropriate security measures to protect against unauthorized access or data breaches.</p>
        
        <h2>6. Your Rights</h2>
        <p>You have the right to:</p>
        <ul>
            <li>Access the site without providing personal information</li>
            <li>Use browser settings to control cookies</li>
            <li>Download images without registration</li>
        </ul>
        
        <h2>7. Children's Privacy</h2>
        <p>Our service is not directed at children under 13, and we do not knowingly collect information from children.</p>
        
        <h2>8. Changes to Privacy Policy</h2>
        <p>We may update this policy periodically. Check this page for the latest version.</p>
        
        <h2>9. Contact</h2>
        <p>For privacy-related questions, please refer to our About page for contact information.</p>
    </main>
    
    <footer class="site-footer">
        <p>&copy; 2024 Thinkora.pics. All images free for commercial use.</p>
        <nav>
            <a href="/">Home</a> |
            <a href="/about">About</a> |
            <a href="/terms">Terms</a> |
            <a href="/privacy">Privacy</a> |
            <a href="/sitemap.xml">Sitemap</a>
        </nav>
    </footer>
</body>
</html>"""
    
    def generate_404_page(self) -> str:
        """生成404错误页面"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found | Thinkora.pics</title>
    <meta name="description" content="The page you're looking for doesn't exist. Browse our collection of free transparent PNG images.">
    <meta name="robots" content="noindex, follow">
    <link rel="stylesheet" href="/public/css/styles-enhanced.css">
</head>
<body>
    <header class="site-header">
        <div class="site-title"><a href="/">Thinkora.pics</a></div>
    </header>
    
    <main class="container error-page">
        <div class="error-content">
            <h1>404</h1>
            <h2>Oops! Page Not Found</h2>
            <p>The page you're looking for doesn't exist or has been moved.</p>
            
            <div class="error-actions">
                <a href="/" class="button">Go to Homepage</a>
                <a href="/category/popular" class="button-outline">Browse Popular Images</a>
            </div>
            
            <div class="error-suggestions">
                <h3>You might be interested in:</h3>
                <ul>
                    <li><a href="/category/business">Business Images</a></li>
                    <li><a href="/category/technology">Technology Images</a></li>
                    <li><a href="/category/nature">Nature Images</a></li>
                    <li><a href="/category/people">People Images</a></li>
                </ul>
            </div>
        </div>
    </main>
    
    <footer class="site-footer">
        <p>&copy; 2024 Thinkora.pics. All images free for commercial use.</p>
        <nav>
            <a href="/">Home</a> |
            <a href="/about">About</a> |
            <a href="/terms">Terms</a> |
            <a href="/privacy">Privacy</a>
        </nav>
    </footer>
</body>
</html>"""
    
    def enhance_robots_txt(self):
        """增强robots.txt文件"""
        robots_content = """# Robots.txt for thinkora.pics
# Generated by Comprehensive SEO Optimizer

# Default access
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: *.json$
Disallow: /search?
Crawl-delay: 1

# Search Engine Specific Rules
User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: Bingbot
Allow: /
Crawl-delay: 0

User-agent: Slurp
Allow: /
Crawl-delay: 1

User-agent: DuckDuckBot
Allow: /
Crawl-delay: 1

# Image crawlers - we want them!
User-agent: Googlebot-Image
Allow: /
Disallow: /api/

User-agent: Bingbot-Image
Allow: /
Disallow: /api/

User-agent: Slurp-Image
Allow: /

# Social Media Crawlers
User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: LinkedInBot
Allow: /

User-agent: WhatsApp
Allow: /

# Block bad bots
User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Disallow: /

User-agent: MJ12bot
Disallow: /

User-agent: DotBot
Disallow: /

# Sitemap location
Sitemap: https://thinkora.pics/sitemap.xml
Sitemap: https://thinkora.pics/sitemap-images.xml

# Host directive
Host: https://thinkora.pics
"""
        
        with open('dist/robots.txt', 'w') as f:
            f.write(robots_content)
        
        print("✅ Enhanced robots.txt created")
    
    def generate_comprehensive_sitemap(self, images: List[Dict[str, Any]]):
        """生成综合的sitemap文件"""
        # 主sitemap
        main_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Homepage -->
  <url>
    <loc>https://thinkora.pics/</loc>
    <lastmod>{}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  
  <!-- Static Pages -->
  <url>
    <loc>https://thinkora.pics/about</loc>
    <lastmod>{}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://thinkora.pics/terms</loc>
    <lastmod>{}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
  
  <url>
    <loc>https://thinkora.pics/privacy</loc>
    <lastmod>{}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
""".format(
    datetime.now().strftime('%Y-%m-%d'),
    datetime.now().strftime('%Y-%m-%d'),
    datetime.now().strftime('%Y-%m-%d'),
    datetime.now().strftime('%Y-%m-%d')
)
        
        # 添加分类页面
        categories = set(img.get('category', 'general') for img in images)
        for category in categories:
            main_sitemap += f"""  <url>
    <loc>https://thinkora.pics/category/{category}</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        
        main_sitemap += "</urlset>"
        
        with open('dist/sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(main_sitemap)
        
        # 图片sitemap
        image_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
"""
        
        for image in images:
            image_sitemap += f"""  <url>
    <loc>https://thinkora.pics/images/{image['id']}.html</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <image:image>
      <image:loc>{image.get('imageUrl', '')}</image:loc>
      <image:title>{self.clean_xml(image.get('seoTitle', image.get('title', '')))}</image:title>
      <image:caption>{self.clean_xml(image.get('seoDescription', ''))}</image:caption>
      <image:license>https://creativecommons.org/publicdomain/zero/1.0/</image:license>
    </image:image>
  </url>
"""
        
        image_sitemap += "</urlset>"
        
        with open('dist/sitemap-images.xml', 'w', encoding='utf-8') as f:
            f.write(image_sitemap)
        
        print("✅ Generated comprehensive sitemaps")
    
    def clean_xml(self, text: str) -> str:
        """清理XML特殊字符"""
        if not text:
            return ""
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text
    
    def create_organization_schema(self):
        """创建组织架构数据"""
        org_schema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Thinkora.pics",
            "url": "https://thinkora.pics",
            "logo": "https://thinkora.pics/logo.png",
            "description": "Free transparent PNG images for designers and developers",
            "sameAs": [
                # 添加社交媒体链接
            ],
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "availableLanguage": ["English"]
            }
        }
        
        with open('dist/organization-schema.json', 'w', encoding='utf-8') as f:
            json.dump(org_schema, f, indent=2)
        
        print("✅ Created organization schema")

def main():
    optimizer = ComprehensiveSEOOptimizer()
    
    print("🚀 Starting comprehensive SEO optimization...")
    
    # 读取元数据
    with open('dist/metadata.json', 'r', encoding='utf-8') as f:
        images = json.load(f)
    
    print(f"📊 Processing {len(images)} images...")
    
    # 1. 创建分类页面
    optimizer.create_category_pages(images)
    
    # 2. 创建静态页面
    optimizer.create_static_pages()
    
    # 3. 增强robots.txt
    optimizer.enhance_robots_txt()
    
    # 4. 生成综合sitemap
    optimizer.generate_comprehensive_sitemap(images)
    
    # 5. 创建组织架构数据
    optimizer.create_organization_schema()
    
    print("\n✅ Comprehensive SEO optimization completed!")
    print("\nNext steps:")
    print("1. Run the main SEO optimizer to enhance metadata")
    print("2. Regenerate all pages with new templates")
    print("3. Create and upload OG image")
    print("4. Submit sitemaps to search engines")
    print("5. Set up 404 page in server configuration")

if __name__ == "__main__":
    main()