#!/usr/bin/env python3
"""
简单的R2上传脚本 - 上传所有带标签的图片
"""

import os
import json
import sqlite3
import requests
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cloudflare R2配置 - 需要你填写
ACCOUNT_ID = "d37e2728a4daeb263e7a08a066e80926"  # 从你的R2 URL中提取
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID', '')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY', '')
R2_BUCKET_NAME = "thinkora-pics"

# 如果你有自定义域名
R2_PUBLIC_URL = "https://r2.thinkora.pics"  # 或 "https://pub-xxx.r2.dev"

def get_images_from_db():
    """从数据库获取所有图片信息"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, tags 
        FROM images 
        WHERE tags != '[]'
        ORDER BY id
    """)
    
    images = []
    for row in cursor.fetchall():
        images.append({
            'id': row[0],
            'title': row[1],
            'tags': json.loads(row[2])
        })
    
    conn.close()
    logger.info(f"📸 数据库中有 {len(images)} 张带标签的图片")
    return images

def find_local_file(image_id):
    """查找本地图片文件"""
    # 提取平台前缀
    platform = image_id.split('_')[0]
    
    # 可能的路径
    possible_paths = [
        f'raw/{platform}/{image_id}.jpg',
        f'raw/{platform}/{image_id}.jpeg',
        f'raw/{platform}/{image_id}.png',
        f'png/{image_id}.png',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def upload_using_requests(file_path, r2_key):
    """使用requests上传文件到R2（需要配置签名）"""
    # 这个方法需要AWS签名，比较复杂
    # 建议使用rclone或AWS CLI
    logger.warning("使用requests上传需要AWS签名，请使用rclone方法")
    return False

def create_upload_commands():
    """生成上传命令"""
    images = get_images_from_db()
    
    # 检查本地文件
    upload_list = []
    missing_files = []
    
    for img in images:
        local_path = find_local_file(img['id'])
        if local_path:
            upload_list.append({
                'id': img['id'],
                'local_path': local_path,
                'r2_path': f"images/{img['id']}.jpg",
                'tags': img['tags']
            })
        else:
            missing_files.append(img['id'])
    
    logger.info(f"✅ 找到 {len(upload_list)} 个本地文件")
    if missing_files:
        logger.warning(f"⚠️ 缺失 {len(missing_files)} 个文件: {missing_files[:5]}...")
    
    # 生成rclone批量上传脚本
    with open('upload_to_r2.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# R2批量上传脚本\n")
        f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 上传 {len(upload_list)} 个文件\n\n")
        
        f.write("echo '🚀 开始上传图片到R2...'\n\n")
        
        # 使用rclone copy批量上传
        f.write("# 方法1: 批量上传整个目录（推荐）\n")
        f.write("rclone copy raw/pixabay r2:thinkora-pics/images \\\n")
        f.write("  --include '*.jpg' \\\n")
        f.write("  --include '*.jpeg' \\\n")
        f.write("  --include '*.png' \\\n")
        f.write("  --s3-acl public-read \\\n")
        f.write("  --transfers 8 \\\n")
        f.write("  --progress\n\n")
        
        f.write("# 方法2: 单个文件上传（可选）\n")
        f.write("# COUNT=0\n")
        f.write("# TOTAL=" + str(len(upload_list)) + "\n")
        for item in upload_list[:5]:  # 只显示前5个作为示例
            f.write(f"# rclone copy {item['local_path']} r2:thinkora-pics/images/ --s3-acl public-read\n")
        f.write("# ...\n\n")
        
        f.write("echo '✅ 上传完成!'\n")
        f.write("echo '📊 验证上传结果:'\n")
        f.write("rclone size r2:thinkora-pics\n")
    
    os.chmod('upload_to_r2.sh', 0o755)
    logger.info("✅ 已生成上传脚本: upload_to_r2.sh")
    
    # 生成文件列表供其他工具使用
    with open('files_to_upload.txt', 'w') as f:
        for item in upload_list:
            f.write(f"{item['local_path']}\n")
    
    # 生成上传映射
    upload_mapping = {
        'generated_at': datetime.now().isoformat(),
        'total_files': len(upload_list),
        'missing_files': len(missing_files),
        'upload_list': upload_list
    }
    
    with open('upload_mapping.json', 'w') as f:
        json.dump(upload_mapping, f, indent=2)
    
    return upload_list

def update_database_urls(base_url="https://r2.thinkora.pics"):
    """更新数据库中的图片URL"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 更新所有图片的URL
    cursor.execute("""
        UPDATE images 
        SET url_thumbnail = ? || '/images/' || id || '.jpg',
            url_regular = ? || '/images/' || id || '.jpg',
            url_download = ? || '/images/' || id || '.jpg'
        WHERE tags != '[]'
    """, (base_url, base_url, base_url))
    
    updated = cursor.rowcount
    conn.commit()
    conn.close()
    
    logger.info(f"✅ 更新了 {updated} 条数据库记录的URL")

def main():
    """主函数"""
    logger.info("🚀 R2图片上传工具")
    logger.info("=" * 50)
    
    # 1. 创建上传命令
    upload_list = create_upload_commands()
    
    # 2. 显示使用说明
    logger.info("\n📋 接下来的步骤:")
    logger.info("\n1️⃣ 确保已安装并配置rclone:")
    logger.info("   brew install rclone")
    logger.info("   rclone config")
    logger.info("   (添加R2配置，类型选择Amazon S3，提供商选择Cloudflare R2)")
    
    logger.info("\n2️⃣ 执行上传:")
    logger.info("   ./upload_to_r2.sh")
    
    logger.info("\n3️⃣ 上传完成后，更新数据库URL:")
    logger.info("   python3 scripts/upload_to_r2_simple.py --update-urls")
    
    # 处理命令行参数
    import sys
    if '--update-urls' in sys.argv:
        logger.info("\n📝 更新数据库URL...")
        update_database_urls()
    
    logger.info("\n✅ 准备完成!")

if __name__ == '__main__':
    main()