#!/usr/bin/env python3
"""
生成更好的图片标题 - SEO优化且吸引人
"""

import sqlite3
import json
import random
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# 标题模板 - 根据不同类型的标签组合生成标题
TITLE_TEMPLATES = {
    # 办公/工作场景
    'office': [
        "Modern {0} Setup with {1}",
        "Professional {0} and {1} Workspace",
        "Elegant {0} on Office Desk",
        "Minimalist {0} Work Environment",
        "Creative {0} and {1} Station"
    ],
    
    # 科技/电子产品
    'tech': [
        "Latest {0} Technology Showcase",
        "Modern {0} Device Close-up",
        "Premium {0} on Clean Background",
        "Sleek {0} Product Photography",
        "High-Tech {0} Display"
    ],
    
    # 生活方式
    'lifestyle': [
        "Stylish {0} for Modern Living",
        "Beautiful {0} in Natural Light",
        "Cozy {0} Home Decor",
        "Elegant {0} Lifestyle Shot",
        "Trendy {0} and {1} Combination"
    ],
    
    # 自然/植物
    'nature': [
        "Beautiful {0} in Natural Setting",
        "Fresh {0} Nature Photography",
        "Vibrant {0} Plant Collection",
        "Green {0} Indoor Garden",
        "Natural {0} Botanical Display"
    ],
    
    # 健康/美容
    'wellness': [
        "Relaxing {0} Spa Treatment",
        "Luxurious {0} Wellness Experience",
        "Calming {0} Beauty Ritual",
        "Professional {0} Therapy Session",
        "Serene {0} Health & Beauty"
    ],
    
    # 商业/金融
    'business': [
        "Professional {0} Business Tools",
        "Modern {0} Finance Workspace",
        "Corporate {0} Office Essentials",
        "Executive {0} Business Setup",
        "Premium {0} Work Environment"
    ],
    
    # 通用模板
    'general': [
        "Premium {0} Stock Photo",
        "High-Quality {0} Image",
        "Professional {0} Photography",
        "Beautiful {0} Visual Content",
        "Stunning {0} Picture"
    ]
}

# 关键词到类别的映射
CATEGORY_KEYWORDS = {
    'office': ['office', 'desk', 'workspace', 'computer', 'laptop', 'keyboard', 'work', 'business'],
    'tech': ['smartphone', 'phone', 'mobile', 'technology', 'device', 'screen', 'digital', 'electronic'],
    'lifestyle': ['home', 'living', 'lifestyle', 'modern', 'style', 'decor', 'interior', 'design'],
    'nature': ['plant', 'flower', 'nature', 'garden', 'green', 'leaf', 'botanical', 'natural'],
    'wellness': ['spa', 'wellness', 'health', 'beauty', 'massage', 'relax', 'therapy', 'treatment'],
    'business': ['business', 'finance', 'money', 'calculator', 'professional', 'corporate', 'executive']
}

def determine_category(tags):
    """根据标签确定图片类别"""
    tags_lower = [tag.lower() for tag in tags]
    
    # 计算每个类别的匹配分数
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for tag in tags_lower for keyword in keywords if keyword in tag)
        if score > 0:
            category_scores[category] = score
    
    # 返回得分最高的类别
    if category_scores:
        return max(category_scores.items(), key=lambda x: x[1])[0]
    return 'general'

def generate_title(tags, image_id):
    """生成一个吸引人的标题"""
    if not tags:
        return f"Premium Stock Photo {image_id}"
    
    # 确定类别
    category = determine_category(tags)
    
    # 选择合适的模板
    templates = TITLE_TEMPLATES.get(category, TITLE_TEMPLATES['general'])
    template = random.choice(templates)
    
    # 处理标签，使其更适合标题
    processed_tags = []
    for tag in tags[:3]:  # 使用前3个标签
        # 标题化每个单词
        words = tag.split()
        titled_words = [word.capitalize() for word in words]
        processed_tags.append(' '.join(titled_words))
    
    # 生成标题
    try:
        if '{1}' in template and len(processed_tags) >= 2:
            title = template.format(processed_tags[0], processed_tags[1])
        else:
            title = template.format(processed_tags[0])
    except:
        # 如果模板格式化失败，使用备用方案
        title = f"{processed_tags[0]} - Professional Stock Photography"
    
    return title

def generate_description(tags, title):
    """生成更好的描述"""
    if len(tags) >= 5:
        tag_list = ', '.join(tags[:5])
        description = f"{title}. Features {tag_list} and more. Perfect for commercial use, presentations, and creative projects."
    else:
        tag_list = ', '.join(tags)
        description = f"{title}. High-quality image featuring {tag_list}. Ideal for web design, marketing materials, and digital content."
    
    return description

def update_titles_and_descriptions():
    """更新所有图片的标题和描述"""
    logger.info("🚀 开始生成更好的标题和描述...")
    
    # 连接数据库
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 获取所有图片
    cursor.execute("SELECT id, tags FROM images WHERE tags != '[]'")
    images = cursor.fetchall()
    
    logger.info(f"📸 处理 {len(images)} 张图片...")
    
    # 更新每张图片
    updated_count = 0
    examples = []
    
    for image_id, tags_json in images:
        tags = json.loads(tags_json)
        
        # 生成新标题和描述
        new_title = generate_title(tags, image_id)
        new_description = generate_description(tags, new_title)
        
        # 更新数据库
        cursor.execute("""
            UPDATE images 
            SET title = ?, description = ?
            WHERE id = ?
        """, (new_title, new_description, image_id))
        
        updated_count += 1
        
        # 保存一些例子
        if len(examples) < 10:
            examples.append({
                'id': image_id,
                'old_title': f"{', '.join(tags[:3])} - Pixabay Image",
                'new_title': new_title,
                'tags': tags[:5]
            })
        
        if updated_count % 10 == 0:
            logger.info(f"  已更新 {updated_count} 个标题...")
    
    # 提交更改
    conn.commit()
    conn.close()
    
    logger.info(f"\n✅ 成功更新 {updated_count} 个标题和描述！")
    
    # 显示一些例子
    logger.info("\n📝 标题更新示例:")
    logger.info("-" * 80)
    for example in examples[:5]:
        logger.info(f"ID: {example['id']}")
        logger.info(f"旧标题: {example['old_title']}")
        logger.info(f"新标题: {example['new_title']}")
        logger.info(f"标签: {', '.join(example['tags'])}")
        logger.info("-" * 80)
    
    # 更新metadata.json
    update_metadata_json()
    
    return updated_count

def update_metadata_json():
    """同步更新metadata.json"""
    logger.info("\n📝 更新metadata.json...")
    
    # 读取更新后的数据库数据
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, description, tags 
        FROM images 
        WHERE tags != '[]'
        ORDER BY id
    """)
    
    db_images = {}
    for row in cursor.fetchall():
        db_images[row[0]] = {
            'title': row[1],
            'description': row[2],
            'tags': json.loads(row[3])
        }
    
    conn.close()
    
    # 更新metadata.json
    with open('metadata.json', 'r') as f:
        metadata = json.load(f)
    
    updated = 0
    for image in metadata['images']:
        if image['id'] in db_images:
            image['title'] = db_images[image['id']]['title']
            image['description'] = db_images[image['id']]['description']
            updated += 1
    
    metadata['lastUpdated'] = datetime.now().isoformat()
    
    with open('metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ 更新了 {updated} 个图片的元数据")

def show_title_statistics():
    """显示标题统计信息"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 统计不同类型的标题
    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN title LIKE '%Modern%' THEN 1 END) as modern,
            COUNT(CASE WHEN title LIKE '%Professional%' THEN 1 END) as professional,
            COUNT(CASE WHEN title LIKE '%Beautiful%' THEN 1 END) as beautiful,
            COUNT(CASE WHEN title LIKE '%Premium%' THEN 1 END) as premium,
            COUNT(CASE WHEN title LIKE '%Elegant%' THEN 1 END) as elegant
        FROM images
    """)
    
    stats = cursor.fetchone()
    
    logger.info("\n📊 标题关键词统计:")
    logger.info(f"  Modern: {stats[0]}")
    logger.info(f"  Professional: {stats[1]}")
    logger.info(f"  Beautiful: {stats[2]}")
    logger.info(f"  Premium: {stats[3]}")
    logger.info(f"  Elegant: {stats[4]}")
    
    conn.close()

def main():
    """主函数"""
    # 备份数据库
    import shutil
    backup_name = f"thinkora_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2('thinkora.db', backup_name)
    logger.info(f"✅ 数据库已备份到: {backup_name}")
    
    # 更新标题和描述
    update_titles_and_descriptions()
    
    # 显示统计
    show_title_statistics()
    
    logger.info("\n🎉 标题优化完成！")
    logger.info("   - 所有图片现在都有独特且吸引人的标题")
    logger.info("   - 描述也更加详细和SEO友好")
    logger.info("   - 记得重新生成HTML页面以应用新标题")

if __name__ == '__main__':
    main()