#!/usr/bin/env python3
"""
验证标签系统是否正常工作
"""

import sqlite3
import json
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def verify_tags_in_database():
    """验证数据库中的标签数据"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    logger.info("🔍 验证数据库中的标签系统...\n")
    
    # 1. 获取所有图片的标签信息
    cursor.execute("SELECT id, title, tags FROM images LIMIT 10")
    samples = cursor.fetchall()
    
    logger.info("📸 前10张图片的标签示例:")
    logger.info("-" * 80)
    
    for img_id, title, tags_json in samples:
        try:
            tags = json.loads(tags_json)
            if tags:
                logger.info(f"ID: {img_id}")
                logger.info(f"标题: {title}")
                logger.info(f"标签 ({len(tags)}个): {', '.join(tags[:5])}{'...' if len(tags) > 5 else ''}")
            else:
                logger.info(f"ID: {img_id} - ⚠️ 无标签")
        except:
            logger.info(f"ID: {img_id} - ❌ 标签解析错误")
        logger.info("-" * 80)
    
    # 2. 统计标签使用情况
    cursor.execute("SELECT tags FROM images WHERE tags != '[]'")
    all_tags_data = cursor.fetchall()
    
    all_tags = []
    for (tags_json,) in all_tags_data:
        try:
            tags = json.loads(tags_json)
            all_tags.extend(tags)
        except:
            pass
    
    # 3. 标签统计
    tag_counter = Counter(all_tags)
    total_unique_tags = len(tag_counter)
    total_tag_uses = sum(tag_counter.values())
    
    logger.info(f"\n📊 标签统计:")
    logger.info(f"  - 总标签使用次数: {total_tag_uses}")
    logger.info(f"  - 独特标签数量: {total_unique_tags}")
    logger.info(f"  - 平均每张图片标签数: {total_tag_uses / len(all_tags_data):.1f}")
    
    # 4. 最热门的标签
    logger.info(f"\n🔥 Top 20 热门标签:")
    for i, (tag, count) in enumerate(tag_counter.most_common(20), 1):
        logger.info(f"  {i:2d}. {tag:<20} ({count} 次)")
    
    # 5. 搜索功能测试
    logger.info(f"\n🔍 搜索功能测试:")
    test_queries = ['office', 'computer', 'nature', 'food', 'business']
    
    for query in test_queries:
        cursor.execute("""
            SELECT COUNT(*) FROM images 
            WHERE tags LIKE ? OR title LIKE ? OR description LIKE ?
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        count = cursor.fetchone()[0]
        logger.info(f"  搜索 '{query}': 找到 {count} 张图片")
    
    # 6. 标签分布分析
    cursor.execute("""
        SELECT 
            CASE 
                WHEN json_array_length(tags) = 0 THEN '0个标签'
                WHEN json_array_length(tags) BETWEEN 1 AND 3 THEN '1-3个标签'
                WHEN json_array_length(tags) BETWEEN 4 AND 6 THEN '4-6个标签'
                WHEN json_array_length(tags) BETWEEN 7 AND 10 THEN '7-10个标签'
                ELSE '10+个标签'
            END as tag_range,
            COUNT(*) as count
        FROM images
        GROUP BY tag_range
        ORDER BY 
            CASE tag_range
                WHEN '0个标签' THEN 0
                WHEN '1-3个标签' THEN 1
                WHEN '4-6个标签' THEN 2
                WHEN '7-10个标签' THEN 3
                ELSE 4
            END
    """)
    
    logger.info(f"\n📈 标签数量分布:")
    for tag_range, count in cursor.fetchall():
        bar = '█' * min(50, int(count / 2))
        logger.info(f"  {tag_range:<12} [{count:3d}] {bar}")
    
    # 7. SEO优化建议
    logger.info(f"\n💡 SEO优化建议:")
    
    # 检查是否有足够的标签覆盖
    cursor.execute("SELECT COUNT(*) FROM images WHERE tags != '[]'")
    tagged_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM images")
    total_count = cursor.fetchone()[0]
    
    coverage = (tagged_count / total_count * 100) if total_count > 0 else 0
    
    if coverage >= 90:
        logger.info(f"  ✅ 标签覆盖率: {coverage:.1f}% - 优秀!")
    elif coverage >= 70:
        logger.info(f"  ⚠️ 标签覆盖率: {coverage:.1f}% - 良好，但仍可改进")
    else:
        logger.info(f"  ❌ 标签覆盖率: {coverage:.1f}% - 需要添加更多带标签的图片")
    
    # 检查标签质量
    avg_tags = total_tag_uses / len(all_tags_data) if all_tags_data else 0
    if avg_tags >= 5:
        logger.info(f"  ✅ 平均标签数: {avg_tags:.1f} - 优秀的标签密度")
    elif avg_tags >= 3:
        logger.info(f"  ⚠️ 平均标签数: {avg_tags:.1f} - 可接受，但可以更丰富")
    else:
        logger.info(f"  ❌ 平均标签数: {avg_tags:.1f} - 需要更多标签以提升SEO")
    
    # 检查标签多样性
    if total_unique_tags >= 100:
        logger.info(f"  ✅ 标签多样性: {total_unique_tags} 个独特标签 - 内容丰富多样")
    elif total_unique_tags >= 50:
        logger.info(f"  ⚠️ 标签多样性: {total_unique_tags} 个独特标签 - 中等水平")
    else:
        logger.info(f"  ❌ 标签多样性: {total_unique_tags} 个独特标签 - 需要更多样化的内容")
    
    conn.close()
    
    logger.info("\n✅ 验证完成!")

def generate_tag_cloud_data():
    """生成标签云数据"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT tags FROM images WHERE tags != '[]'")
    all_tags_data = cursor.fetchall()
    
    all_tags = []
    for (tags_json,) in all_tags_data:
        try:
            tags = json.loads(tags_json)
            all_tags.extend(tags)
        except:
            pass
    
    tag_counter = Counter(all_tags)
    
    # 生成标签云数据
    tag_cloud = [
        {
            'tag': tag,
            'count': count,
            'weight': min(count / 10 + 1, 5)  # 权重1-5
        }
        for tag, count in tag_counter.most_common(50)
    ]
    
    # 保存为JSON供前端使用
    with open('tag_cloud_data.json', 'w', encoding='utf-8') as f:
        json.dump(tag_cloud, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n☁️ 已生成标签云数据: tag_cloud_data.json")
    logger.info(f"   包含 {len(tag_cloud)} 个热门标签")
    
    conn.close()

if __name__ == '__main__':
    verify_tags_in_database()
    generate_tag_cloud_data()