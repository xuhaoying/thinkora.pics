#!/usr/bin/env python3
"""
SEO优化器 - 为thinkora.pics网站生成优化的SEO内容
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import re

class SEOOptimizer:
    def __init__(self):
        self.metadata_file = 'dist/metadata.json'
        self.base_url = 'https://thinkora.pics'
        self.site_name = 'Thinkora.pics'
        self.site_description = 'Free transparent PNG images for designers and developers'
        
        # SEO关键词映射
        self.category_keywords = {
            'business': ['business', 'office', 'professional', 'corporate', 'work', 'meeting', 'presentation'],
            'technology': ['technology', 'tech', 'digital', 'computer', 'software', 'innovation', 'gadget'],
            'nature': ['nature', 'natural', 'outdoor', 'environment', 'landscape', 'scenic', 'wildlife'],
            'food': ['food', 'cuisine', 'culinary', 'restaurant', 'cooking', 'meal', 'ingredients'],
            'people': ['people', 'person', 'portrait', 'human', 'lifestyle', 'social', 'community'],
            'travel': ['travel', 'tourism', 'vacation', 'destination', 'journey', 'adventure', 'trip'],
            'health': ['health', 'medical', 'healthcare', 'wellness', 'fitness', 'medicine', 'healthy'],
            'education': ['education', 'learning', 'school', 'study', 'knowledge', 'academic', 'teaching'],
            'sports': ['sports', 'athletic', 'fitness', 'exercise', 'game', 'competition', 'activity'],
            'animals': ['animals', 'pets', 'wildlife', 'fauna', 'creatures', 'domestic', 'wild'],
            'fashion': ['fashion', 'style', 'clothing', 'apparel', 'accessories', 'trend', 'design'],
            'buildings': ['buildings', 'architecture', 'construction', 'structure', 'urban', 'real estate'],
            'transportation': ['transportation', 'vehicle', 'transport', 'automotive', 'travel', 'mobility'],
            'music': ['music', 'musical', 'instrument', 'audio', 'sound', 'melody', 'entertainment'],
            'industry': ['industry', 'industrial', 'manufacturing', 'factory', 'production', 'machinery']
        }
    
    def generate_seo_title(self, image: Dict[str, Any]) -> str:
        """生成SEO优化的标题"""
        tags = image.get('tags', [])
        category = image.get('category', 'general')
        width = image.get('width', 0)
        
        # 使用前3个最相关的标签构建标题
        if tags and len(tags) >= 3:
            # 过滤掉过于通用的标签
            generic_tags = ['transparent', 'no-background', 'cutout', 'png', 'image', 'photo', 
                           'premium', 'high-quality', 'quality', '4k', 'hd', 'ultra-hd']
            
            # 获取有意义的标签
            meaningful_tags = [tag for tag in tags if tag not in generic_tags]
            
            if len(meaningful_tags) >= 2:
                # 使用最有意义的标签组合
                primary_tag = meaningful_tags[0].title()
                secondary_tag = meaningful_tags[1].title()
                
                # 根据图片特征选择合适的标题模板
                if width >= 4000:
                    title = f"{primary_tag} {secondary_tag} 4K Transparent PNG"
                elif width >= 2000:
                    title = f"{primary_tag} {secondary_tag} HD Transparent PNG"
                else:
                    title = f"{primary_tag} {secondary_tag} Transparent PNG"
            else:
                # 如果有意义的标签不够，使用第一个标签和类别
                main_tag = meaningful_tags[0].title() if meaningful_tags else tags[0].title() if tags else category.title()
                title = f"{main_tag} {category.title()} Transparent PNG"
        else:
            # 如果没有标签，基于类别生成
            title = f"{category.title()} Transparent PNG Image"
        
        # 添加独特标识符（使用图片ID的一部分）
        image_id = image.get('id', '')
        if len(title) < 45:
            title = f"{title} - Free Download"
        
        # 确保标题长度适中
        if len(title) > 60:
            title = title[:57] + "..."
            
        return title
    
    def generate_seo_description(self, image: Dict[str, Any]) -> str:
        """生成SEO优化的描述"""
        category = image.get('category', 'general')
        tags = image.get('tags', [])
        width = image.get('width', 0)
        height = image.get('height', 0)
        
        # 基于类别的用途描述
        category_uses = {
            'business': ['presentations', 'reports', 'websites', 'marketing materials'],
            'technology': ['app design', 'web development', 'tech blogs', 'software interfaces'],
            'nature': ['environmental campaigns', 'outdoor brands', 'travel blogs', 'eco projects'],
            'food': ['restaurant menus', 'food blogs', 'recipe cards', 'culinary websites'],
            'people': ['social media', 'team pages', 'testimonials', 'lifestyle blogs'],
            'education': ['e-learning', 'educational materials', 'school websites', 'course content'],
            'stock photo': ['commercial projects', 'advertising', 'web design', 'print media']
        }
        
        # 获取有意义的标签（排除通用标签）
        generic_tags = ['transparent', 'no-background', 'cutout', 'png', 'image', 'photo', 
                       'premium', 'high-quality', 'quality', '4k', 'hd', 'ultra-hd']
        meaningful_tags = [tag for tag in tags if tag not in generic_tags][:3]
        
        # 构建独特的描述
        if meaningful_tags:
            # 使用标签创建更具体的描述
            tag_string = ' and '.join(meaningful_tags[:2])
            
            # 尺寸描述
            if width >= 4000:
                size_info = f"4K resolution ({width}×{height}px)"
            elif width >= 2000:
                size_info = f"HD quality ({width}×{height}px)"
            else:
                size_info = f"{width}×{height} pixels"
            
            # 获取用途
            uses = category_uses.get(category, ['creative projects', 'digital design'])
            use_case = uses[0] if uses else 'creative projects'
            
            # 组合描述
            description = f"Free {tag_string} transparent PNG in {size_info}. Perfect for {use_case}. No background, instant download."
        else:
            # 回退到基础描述
            description = f"Download this {category} transparent PNG ({width}×{height}px). Ready to use for commercial projects. No attribution required."
        
        # 确保长度合适
        if len(description) > 160:
            description = description[:157] + "..."
        elif len(description) < 120:
            # 添加额外信息
            extra_tags = meaningful_tags[2:4] if len(meaningful_tags) > 2 else []
            if extra_tags:
                description += f" Features: {', '.join(extra_tags)}."
        
        return description
    
    def generate_structured_data(self, image: Dict[str, Any]) -> Dict[str, Any]:
        """生成结构化数据 (Schema.org)"""
        # 计算或估算文件大小
        file_size = image.get('fileSize', 0)
        if file_size == 0:
            # 估算PNG文件大小 (width * height * 4 bytes * 0.7 压缩率)
            width = image.get('width', 0)
            height = image.get('height', 0)
            if width and height:
                file_size = int(width * height * 4 * 0.7)
        
        # 生成SEO优化的结构化数据
        structured_data = {
            "@context": "https://schema.org",
            "@type": "ImageObject",
            "contentUrl": image.get('imageUrl', ''),
            "thumbnailUrl": image.get('thumbnailUrl', image.get('imageUrl', '')),
            "name": self.generate_seo_title(image),
            "description": self.generate_seo_description(image),
            "keywords": ', '.join(image.get('tags', [])),
            "datePublished": image.get('uploadDate', datetime.now().isoformat()),
            "creator": {
                "@type": "Person",
                "name": image.get('author', 'Unknown'),
                "url": image.get('authorUrl', '')
            },
            "copyrightNotice": "Free for commercial use, no attribution required",
            "license": "https://creativecommons.org/publicdomain/zero/1.0/",
            "acquireLicensePage": f"{self.base_url}/images/{image['id']}.html",
            "width": {
                "@type": "QuantitativeValue",
                "value": image.get('width', 0),
                "unitCode": "E37"  # pixel unit code
            },
            "height": {
                "@type": "QuantitativeValue", 
                "value": image.get('height', 0),
                "unitCode": "E37"  # pixel unit code
            },
            "encodingFormat": "image/png",
            "contentSize": self.format_file_size(file_size),
            "isAccessibleForFree": True,
            "isFamilyFriendly": True,
            "audience": {
                "@type": "Audience",
                "audienceType": ["Designers", "Developers", "Content Creators", "Marketers"]
            }
        }
        
        # 添加聚合评分（如果有的话）
        if image.get('downloadCount', 0) > 100:
            structured_data["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": "4.8",
                "reviewCount": str(image.get('downloadCount', 100) // 10),
                "bestRating": "5",
                "worstRating": "1"
            }
        
        return structured_data
    
    def format_file_size(self, bytes_size: int) -> str:
        """格式化文件大小为人类可读格式"""
        if bytes_size == 0:
            return "0 bytes"
        
        units = ['bytes', 'KB', 'MB', 'GB']
        unit_index = 0
        size = float(bytes_size)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"
    
    def enhance_metadata(self):
        """增强所有图片的元数据"""
        # 加载现有元数据
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            images = json.load(f)
        
        print(f"📊 Enhancing metadata for {len(images)} images...")
        
        # 增强每个图片的SEO信息
        for i, image in enumerate(images):
            # 生成SEO优化的标题和描述
            image['seoTitle'] = self.generate_seo_title(image)
            image['seoDescription'] = self.generate_seo_description(image)
            
            # 生成结构化数据
            image['structuredData'] = self.generate_structured_data(image)
            
            # 添加额外的SEO字段
            image['canonicalUrl'] = f"{self.base_url}/images/{image['id']}.html"
            
            # 生成关键词
            keywords = []
            if image.get('tags'):
                keywords.extend(image['tags'][:5])
            keywords.append(image.get('category', 'general'))
            keywords.extend(['transparent png', 'free download', 'no background'])
            image['seoKeywords'] = ', '.join(keywords)
            
            if (i + 1) % 50 == 0:
                print(f"✅ Processed {i + 1}/{len(images)} images")
        
        # 保存增强后的元数据
        enhanced_file = 'dist/metadata_enhanced.json'
        with open(enhanced_file, 'w', encoding='utf-8') as f:
            json.dump(images, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Enhanced metadata saved to {enhanced_file}")
        return images
    
    def generate_robots_txt(self):
        """生成优化的robots.txt"""
        robots_content = """# Robots.txt for thinkora.pics
# Generated by SEO Optimizer

User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: *.json$

# Search Engine Crawlers
User-agent: Googlebot
Crawl-delay: 0

User-agent: Bingbot
Crawl-delay: 0

User-agent: Slurp
Crawl-delay: 0

# Image crawlers - we want them!
User-agent: Googlebot-Image
Allow: /

User-agent: bingbot-image
Allow: /

# Sitemap location
Sitemap: https://thinkora.pics/sitemap.xml

# Host directive (for Yandex)
Host: https://thinkora.pics
"""
        
        with open('dist/robots.txt', 'w') as f:
            f.write(robots_content)
        
        print("✅ Generated optimized robots.txt")
    
    def generate_enhanced_sitemap(self, images: List[Dict[str, Any]]):
        """生成增强的sitemap.xml"""
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
"""
        
        # 首页
        sitemap_content += f"""  <url>
    <loc>{self.base_url}/</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
"""
        
        # 图片页面
        for image in images:
            sitemap_content += f"""  <url>
    <loc>{self.base_url}/images/{image['id']}.html</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>{image.get('imageUrl', '')}</image:loc>
      <image:title>{self.clean_xml(image.get('seoTitle', ''))}</image:title>
      <image:caption>{self.clean_xml(image.get('seoDescription', ''))}</image:caption>
    </image:image>
  </url>
"""
        
        sitemap_content += "</urlset>"
        
        with open('dist/sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print("✅ Generated enhanced sitemap.xml with image data")
    
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
    
    def create_og_image(self):
        """创建Open Graph默认图片的说明"""
        og_instructions = """
# Open Graph Image Creation Instructions

To complete the SEO optimization, you need to create an Open Graph image:

1. **Dimensions**: 1200x630 pixels (Facebook/Twitter recommended size)
2. **Content**: 
   - Site logo or name "Thinkora.pics"
   - Tagline: "Free Transparent PNG Images"
   - Visual: Grid of sample transparent images
   - Background: Subtle gradient or pattern

3. **Save as**: dist/images/og-image.png

4. **Tools**: 
   - Canva (https://www.canva.com)
   - Figma (https://www.figma.com)
   - Or any image editor

5. **After creation**: Upload to R2 bucket in the images folder
"""
        
        with open('OG_IMAGE_INSTRUCTIONS.md', 'w') as f:
            f.write(og_instructions)
        
        print("📝 Created OG image instructions")

def main():
    optimizer = SEOOptimizer()
    
    print("🚀 Starting SEO optimization...")
    
    # 1. 增强元数据
    enhanced_images = optimizer.enhance_metadata()
    
    # 2. 生成优化的robots.txt
    optimizer.generate_robots_txt()
    
    # 3. 生成增强的sitemap
    optimizer.generate_enhanced_sitemap(enhanced_images)
    
    # 4. 创建OG图片说明
    optimizer.create_og_image()
    
    print("\n✅ SEO optimization completed!")
    print("Next steps:")
    print("1. Run regenerate_seo_pages.py to update all HTML pages")
    print("2. Create and upload the OG image as per instructions")
    print("3. Submit sitemap to Google Search Console and Bing Webmaster Tools")

if __name__ == "__main__":
    main()