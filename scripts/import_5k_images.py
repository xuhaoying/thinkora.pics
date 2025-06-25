#!/usr/bin/env python3
"""
导入下载的5000张图片到数据库
生成SEO友好的标题和描述
"""

import os
import json
import sqlite3
import random
from typing import Dict, List, Any
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 标题模板
TITLE_TEMPLATES = {
    'office': [
        "Modern {0} Setup with {1}",
        "Professional {0} and {1} Workspace",
        "Contemporary {0} Office Environment",
        "Sleek {0} Business Setup"
    ],
    'tech': [
        "Latest {0} Technology Showcase",
        "Modern {0} Device Close-up",
        "High-Tech {0} Equipment Display",
        "Innovative {0} Tech Solution"
    ],
    'nature': [
        "Beautiful {0} in Natural Light",
        "Stunning {0} Nature Photography",
        "Serene {0} Landscape View",
        "Breathtaking {0} Natural Scene"
    ],
    'lifestyle': [
        "Relaxing {0} Lifestyle Moment",
        "Modern {0} Living Scene",
        "Comfortable {0} Home Setting",
        "Elegant {0} Lifestyle Photography"
    ],
    'food': [
        "Delicious {0} Food Photography",
        "Fresh {0} Culinary Delight",
        "Appetizing {0} Gourmet Display",
        "Tasty {0} Food Presentation"
    ],
    'business': [
        "Professional {0} Business Concept",
        "Corporate {0} Office Scene",
        "Modern {0} Business Solution",
        "Executive {0} Work Environment"
    ],
    'health': [
        "Healthy {0} Wellness Concept",
        "Medical {0} Healthcare Display",
        "Professional {0} Health Solution",
        "Modern {0} Wellness Photography"
    ],
    'design': [
        "Creative {0} Design Concept",
        "Artistic {0} Visual Display",
        "Modern {0} Design Element",
        "Innovative {0} Creative Solution"
    ]
}

# 类别关键词
CATEGORY_KEYWORDS = {
    'office': ['desk', 'computer', 'laptop', 'office', 'workspace', 'business', 'work'],
    'tech': ['technology', 'digital', 'device', 'smartphone', 'computer', 'gadget', 'electronic'],
    'nature': ['nature', 'flower', 'plant', 'tree', 'landscape', 'outdoor', 'garden'],
    'lifestyle': ['lifestyle', 'home', 'relax', 'comfort', 'living', 'interior', 'cozy'],
    'food': ['food', 'meal', 'cuisine', 'dish', 'drink', 'fruit', 'vegetable'],
    'business': ['business', 'finance', 'meeting', 'corporate', 'professional', 'team'],
    'health': ['health', 'medical', 'wellness', 'fitness', 'therapy', 'care', 'treatment'],
    'design': ['design', 'art', 'creative', 'graphic', 'pattern', 'color', 'style']
}

def categorize_image(tags: List[str]) -> str:
    """根据标签分类图片"""
    tag_text = ' '.join(tags).lower()
    
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in tag_text)
        if score > 0:
            scores[category] = score
    
    if scores:
        return max(scores, key=scores.get)
    return 'general'

def generate_title(tags: List[str], category: str) -> str:
    """生成SEO友好的标题"""
    if not tags:
        return "Professional Stock Photography"
    
    # 获取合适的模板
    templates = TITLE_TEMPLATES.get(category, TITLE_TEMPLATES['office'])
    template = random.choice(templates)
    
    # 选择最重要的标签
    primary_tag = tags[0].title()
    secondary_tag = tags[1].title() if len(tags) > 1 else "Photography"
    
    # 生成标题
    try:
        title = template.format(primary_tag, secondary_tag)
    except:
        title = f"{primary_tag} {secondary_tag} Photography"
    
    return title

def generate_description(tags: List[str], title: str) -> str:
    """生成描述"""
    tag_list = ', '.join(tags[:10])
    return f"{title}. Features {tag_list} and more. Perfect for commercial use, presentations, and creative projects."

def import_images():
    """导入图片到数据库"""
    # 连接数据库
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    
    # 获取已存在的图片ID
    cursor.execute("SELECT id FROM images")
    existing_ids = set(row[0] for row in cursor.fetchall())
    logger.info(f"数据库中已有 {len(existing_ids)} 张图片")
    
    # 统计
    stats = {
        'imported': 0,
        'skipped': 0,
        'errors': 0
    }
    
    # 处理所有平台的图片
    for platform in ['unsplash', 'pixabay']:
        platform_dir = f'raw/{platform}'
        if not os.path.exists(platform_dir):
            continue
            
        # 获取所有元数据文件
        metadata_files = [f for f in os.listdir(platform_dir) if f.endswith('_metadata.json')]
        logger.info(f"处理 {platform} 平台的 {len(metadata_files)} 张图片")
        
        for metadata_file in metadata_files:
            try:
                # 读取元数据
                with open(os.path.join(platform_dir, metadata_file), 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # 构建图片ID
                image_id = f"{platform}_{metadata['id']}"
                
                # 检查是否已存在
                if image_id in existing_ids:
                    stats['skipped'] += 1
                    continue
                
                # 准备数据
                tags = metadata.get('tags', [])
                if not tags or len(tags) < 3:
                    stats['skipped'] += 1
                    continue
                
                # 生成标题和描述
                category = categorize_image(tags)
                title = generate_title(tags, category)
                description = generate_description(tags, title)
                
                # 构建URL（使用本地路径）
                url = f"/images/{image_id}.jpg"
                
                # 插入数据库
                cursor.execute("""
                    INSERT INTO images (
                        id, title, description, tags, url_thumbnail, url_regular,
                        width, height, likes, author, author_url, source, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    image_id,
                    title,
                    description,
                    json.dumps(tags[:15]),  # 限制标签数量
                    url,
                    url,
                    metadata.get('width', 1920),
                    metadata.get('height', 1080),
                    metadata.get('likes', 0) or metadata.get('views', 0),
                    metadata.get('author', 'Unknown'),
                    metadata.get('author_url', ''),
                    platform.title(),
                    datetime.now().isoformat()
                ))
                
                stats['imported'] += 1
                
                if stats['imported'] % 100 == 0:
                    conn.commit()
                    logger.info(f"已导入 {stats['imported']} 张图片")
                
            except Exception as e:
                logger.error(f"处理 {metadata_file} 时出错: {e}")
                stats['errors'] += 1
    
    # 最终提交
    conn.commit()
    
    # 获取最终统计
    cursor.execute("SELECT COUNT(*) FROM images")
    total_images = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*), AVG(json_array_length(tags)) 
        FROM images 
        WHERE json_array_length(tags) > 0
    """)
    tagged_count, avg_tags = cursor.fetchone()
    
    conn.close()
    
    # 报告
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 导入完成报告:")
    logger.info(f"  成功导入: {stats['imported']} 张")
    logger.info(f"  跳过: {stats['skipped']} 张")
    logger.info(f"  错误: {stats['errors']} 张")
    logger.info(f"  数据库总图片数: {total_images} 张")
    logger.info(f"  有标签的图片: {tagged_count} 张")
    logger.info(f"  平均标签数: {avg_tags:.1f}")
    logger.info(f"{'='*60}")
    
    # 复制图片到public目录
    if stats['imported'] > 0:
        logger.info("\n准备复制图片到 public/images 目录...")
        copy_images_to_public()

def copy_images_to_public():
    """复制图片到public目录"""
    public_dir = 'public/images'
    os.makedirs(public_dir, exist_ok=True)
    
    copied = 0
    for platform in ['unsplash', 'pixabay']:
        platform_dir = f'raw/{platform}'
        if not os.path.exists(platform_dir):
            continue
            
        for img_file in os.listdir(platform_dir):
            if img_file.endswith('.jpg'):
                src = os.path.join(platform_dir, img_file)
                dst = os.path.join(public_dir, img_file)
                
                if not os.path.exists(dst):
                    import shutil
                    shutil.copy2(src, dst)
                    copied += 1
                    
                    if copied % 100 == 0:
                        logger.info(f"已复制 {copied} 张图片")
    
    logger.info(f"✅ 复制完成，共复制 {copied} 张图片到 public/images")

def main():
    """主函数"""
    logger.info("🚀 开始导入5000张图片到数据库")
    import_images()
    
if __name__ == '__main__':
    main()