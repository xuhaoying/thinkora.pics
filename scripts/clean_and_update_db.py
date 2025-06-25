#!/usr/bin/env python3
"""
清理无标签的图片并更新数据库
"""

import os
import json
import sqlite3
from datetime import datetime
import shutil
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def analyze_current_data():
    """分析当前数据库中的图片数据"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 统计标签情况
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN tags = '[]' THEN 1 ELSE 0 END) as no_tags,
            SUM(CASE WHEN tags != '[]' THEN 1 ELSE 0 END) as with_tags
        FROM images
    """)
    
    total, no_tags, with_tags = cursor.fetchone()
    
    logger.info(f"📊 当前数据库统计:")
    logger.info(f"  总图片数: {total}")
    logger.info(f"  无标签图片: {no_tags}")
    logger.info(f"  有标签图片: {with_tags}")
    
    # 获取无标签图片列表
    cursor.execute("SELECT id, title FROM images WHERE tags = '[]'")
    no_tag_images = cursor.fetchall()
    
    conn.close()
    return no_tag_images, total, no_tags, with_tags

def backup_database():
    """备份数据库"""
    backup_name = f"thinkora_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2('thinkora.db', backup_name)
    logger.info(f"✅ 数据库已备份到: {backup_name}")
    return backup_name

def import_new_images_to_db():
    """将新下载的带标签图片导入数据库"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    imported_count = 0
    platforms = ['unsplash', 'pixabay']
    
    for platform in platforms:
        raw_dir = f'raw/{platform}'
        if not os.path.exists(raw_dir):
            continue
            
        # 查找所有metadata文件
        for filename in os.listdir(raw_dir):
            if filename.endswith('_metadata.json'):
                metadata_path = os.path.join(raw_dir, filename)
                
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 检查是否有标签
                    tags = data.get('tags', [])
                    if len(tags) > 0:
                        # 检查是否已存在
                        image_id = f"{platform}_{data['id']}"
                        cursor.execute("SELECT id FROM images WHERE id = ?", (image_id,))
                        
                        if not cursor.fetchone():
                            # 准备数据
                            cursor.execute("""
                                INSERT INTO images (
                                    id, title, description, author_name, author_url,
                                    width, height, aspect_ratio, url_thumbnail, url_regular,
                                    url_download, tags, category, quality_score, file_size,
                                    transparent_ratio, created_at, unsplash_id, unsplash_url,
                                    unsplash_download_location
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                image_id,
                                f"{', '.join(tags[:3])} - {platform.capitalize()} Image",
                                data.get('description', ''),
                                data.get('author', 'Unknown'),
                                data.get('author_url', '#'),
                                data.get('width', 0),
                                data.get('height', 0),
                                f"{data.get('width', 1)}:{data.get('height', 1)}",
                                data.get('url', ''),
                                data.get('url', ''),
                                data.get('download_url', ''),
                                json.dumps(tags, ensure_ascii=False),
                                'photography',
                                data.get('quality_score', 0),
                                'Unknown',
                                0.0,
                                datetime.now().isoformat(),
                                data.get('id') if platform == 'unsplash' else None,
                                data.get('author_url') if platform == 'unsplash' else None,
                                data.get('download_location') if platform == 'unsplash' else None
                            ))
                            imported_count += 1
                            logger.info(f"✅ 导入: {image_id} - {len(tags)} 个标签")
                        
                except Exception as e:
                    logger.error(f"导入失败 {metadata_path}: {e}")
    
    conn.commit()
    conn.close()
    
    logger.info(f"\n📥 成功导入 {imported_count} 张新图片")
    return imported_count

def remove_no_tag_images(no_tag_images):
    """从数据库中删除无标签图片"""
    if not no_tag_images:
        logger.info("没有需要删除的无标签图片")
        return 0
    
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 创建一个表来记录被删除的图片
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deleted_images (
            id TEXT PRIMARY KEY,
            title TEXT,
            deleted_at TEXT
        )
    """)
    
    deleted_count = 0
    for image_id, title in no_tag_images:
        try:
            # 记录到删除表
            cursor.execute("""
                INSERT INTO deleted_images (id, title, deleted_at)
                VALUES (?, ?, ?)
            """, (image_id, title, datetime.now().isoformat()))
            
            # 从主表删除
            cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
            deleted_count += 1
            
        except Exception as e:
            logger.error(f"删除失败 {image_id}: {e}")
    
    conn.commit()
    conn.close()
    
    logger.info(f"🗑️ 已删除 {deleted_count} 张无标签图片")
    return deleted_count

def generate_summary_report():
    """生成更新报告"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 获取更新后的统计
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN tags = '[]' THEN 1 ELSE 0 END) as no_tags,
            SUM(CASE WHEN tags != '[]' THEN 1 ELSE 0 END) as with_tags,
            AVG(CASE 
                WHEN tags != '[]' 
                THEN json_array_length(tags) 
                ELSE 0 
            END) as avg_tags
        FROM images
    """)
    
    total, no_tags, with_tags, avg_tags = cursor.fetchone()
    
    # 获取标签分布
    cursor.execute("""
        SELECT tags FROM images WHERE tags != '[]' LIMIT 100
    """)
    
    all_tags = []
    for row in cursor.fetchall():
        tags = json.loads(row[0])
        all_tags.extend(tags)
    
    # 统计最常见的标签
    tag_count = {}
    for tag in all_tags:
        tag_count[tag] = tag_count.get(tag, 0) + 1
    
    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:20]
    
    conn.close()
    
    # 生成报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'statistics': {
            'total_images': total,
            'images_with_tags': with_tags,
            'images_without_tags': no_tags,
            'average_tags_per_image': round(avg_tags or 0, 2)
        },
        'top_20_tags': [{'tag': tag, 'count': count} for tag, count in top_tags],
        'tag_coverage': f"{(with_tags/total*100):.1f}%" if total > 0 else "0%"
    }
    
    # 保存报告
    report_path = f'logs/db_update_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 打印摘要
    logger.info("\n📊 更新后的数据库摘要:")
    logger.info(f"  总图片数: {total}")
    logger.info(f"  有标签图片: {with_tags} ({report['tag_coverage']})")
    logger.info(f"  平均标签数: {report['statistics']['average_tags_per_image']}")
    logger.info(f"\n🏷️ Top 10 标签:")
    for tag, count in top_tags[:10]:
        logger.info(f"  - {tag}: {count}")
    
    return report

def main(auto_delete=False):
    """主函数"""
    logger.info("🚀 开始清理和更新数据库")
    
    # 1. 分析当前数据
    no_tag_images, total, no_tags, with_tags = analyze_current_data()
    
    if no_tags == 0:
        logger.info("✅ 数据库中没有无标签的图片，无需清理")
        return
    
    # 2. 备份数据库
    backup_database()
    
    # 3. 导入新的带标签图片
    logger.info("\n📥 导入新的带标签图片...")
    imported = import_new_images_to_db()
    
    # 4. 询问是否删除无标签图片
    if no_tags > 0:
        logger.info(f"\n⚠️ 发现 {no_tags} 张无标签图片")
        
        if auto_delete:
            logger.info("自动模式：删除无标签图片")
            remove_no_tag_images(no_tag_images)
        else:
            try:
                response = input("是否删除这些无标签图片? (y/n): ")
                if response.lower() == 'y':
                    remove_no_tag_images(no_tag_images)
                else:
                    logger.info("跳过删除步骤")
            except EOFError:
                logger.info("非交互模式：跳过删除步骤")
    
    # 5. 生成报告
    logger.info("\n📊 生成更新报告...")
    generate_summary_report()
    
    logger.info("\n✅ 数据库更新完成!")

if __name__ == '__main__':
    import sys
    # 如果传入 --auto 参数，自动删除无标签图片
    auto_delete = '--auto' in sys.argv
    main(auto_delete)