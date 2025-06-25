#!/usr/bin/env python3
"""
清理R2存储桶中的无标签旧图片
"""

import os
import json
import sqlite3
import boto3
from botocore.config import Config
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# R2配置
R2_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL', 'https://d37e2728a4daeb263e7a08a066e80926.r2.cloudflarestorage.com')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID', '')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY', '')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME', 'thinkora-pics')

def get_current_db_images():
    """获取当前数据库中的所有图片ID"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM images")
    db_images = set(row[0] for row in cursor.fetchall())
    
    conn.close()
    logger.info(f"数据库中有 {len(db_images)} 张图片")
    return db_images

def get_deleted_images():
    """获取已删除的图片记录"""
    deleted_images = set()
    
    # 检查是否有删除记录表
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM deleted_images")
        deleted_images = set(row[0] for row in cursor.fetchall())
        logger.info(f"找到 {len(deleted_images)} 条删除记录")
    except sqlite3.OperationalError:
        logger.info("没有找到删除记录表")
    
    conn.close()
    return deleted_images

def list_r2_images():
    """列出R2存储桶中的所有图片"""
    if not all([R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY]):
        logger.error("缺少R2认证信息，请设置环境变量")
        return []
    
    # 创建S3客户端
    s3_client = boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    
    r2_images = []
    
    try:
        # 列出所有对象
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=R2_BUCKET_NAME)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    # 只处理图片文件
                    if key.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        # 提取图片ID（例如：images/unsplash_xxx.png -> unsplash_xxx）
                        filename = os.path.basename(key)
                        image_id = os.path.splitext(filename)[0]
                        
                        r2_images.append({
                            'key': key,
                            'id': image_id,
                            'size': obj['Size'],
                            'last_modified': obj['LastModified']
                        })
        
        logger.info(f"R2存储桶中有 {len(r2_images)} 张图片")
        return r2_images
        
    except Exception as e:
        logger.error(f"列出R2图片失败: {e}")
        return []

def identify_images_to_delete(r2_images, db_images, deleted_images):
    """识别需要删除的图片"""
    to_delete = []
    
    for r2_image in r2_images:
        image_id = r2_image['id']
        
        # 如果图片不在当前数据库中，或者在删除记录中
        if image_id not in db_images or image_id in deleted_images:
            to_delete.append(r2_image)
    
    logger.info(f"识别出 {len(to_delete)} 张需要删除的图片")
    return to_delete

def delete_r2_images(images_to_delete, dry_run=True):
    """删除R2中的图片"""
    if not images_to_delete:
        logger.info("没有需要删除的图片")
        return
    
    if dry_run:
        logger.info("🔍 试运行模式 - 以下图片将被删除:")
        for img in images_to_delete[:10]:  # 显示前10个
            logger.info(f"  - {img['key']} (ID: {img['id']}, 大小: {img['size']/1024:.1f}KB)")
        if len(images_to_delete) > 10:
            logger.info(f"  ... 还有 {len(images_to_delete)-10} 张图片")
        
        total_size = sum(img['size'] for img in images_to_delete)
        logger.info(f"\n总计: {len(images_to_delete)} 张图片, {total_size/1024/1024:.1f}MB")
        return
    
    # 实际删除
    s3_client = boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    
    deleted_count = 0
    failed_deletions = []
    
    logger.info(f"开始删除 {len(images_to_delete)} 张图片...")
    
    # 批量删除（R2支持一次删除最多1000个对象）
    batch_size = 1000
    for i in range(0, len(images_to_delete), batch_size):
        batch = images_to_delete[i:i+batch_size]
        
        delete_objects = {
            'Objects': [{'Key': img['key']} for img in batch]
        }
        
        try:
            response = s3_client.delete_objects(
                Bucket=R2_BUCKET_NAME,
                Delete=delete_objects
            )
            
            # 检查是否有删除失败的
            if 'Errors' in response:
                for error in response['Errors']:
                    failed_deletions.append(error['Key'])
                    logger.error(f"删除失败: {error['Key']} - {error['Message']}")
            
            deleted_count += len(batch) - len(response.get('Errors', []))
            logger.info(f"已删除 {deleted_count}/{len(images_to_delete)} 张图片")
            
        except Exception as e:
            logger.error(f"批量删除失败: {e}")
            failed_deletions.extend([img['key'] for img in batch])
    
    # 生成删除报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_to_delete': len(images_to_delete),
        'successfully_deleted': deleted_count,
        'failed_deletions': failed_deletions,
        'space_freed_mb': sum(img['size'] for img in images_to_delete if img['key'] not in failed_deletions) / 1024 / 1024
    }
    
    report_path = f'logs/r2_cleanup_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"\n✅ 删除完成!")
    logger.info(f"  成功删除: {deleted_count} 张图片")
    logger.info(f"  释放空间: {report['space_freed_mb']:.1f}MB")
    if failed_deletions:
        logger.info(f"  删除失败: {len(failed_deletions)} 张图片")
    logger.info(f"  详细报告: {report_path}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='清理R2存储桶中的无标签旧图片')
    parser.add_argument('--delete', action='store_true', help='实际执行删除（默认为试运行）')
    parser.add_argument('--check-env', action='store_true', help='检查环境变量设置')
    args = parser.parse_args()
    
    logger.info("🧹 R2存储桶清理工具")
    logger.info("=" * 50)
    
    # 检查环境变量
    if args.check_env or not all([R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY]):
        logger.info("\n📋 环境变量检查:")
        logger.info(f"  R2_ENDPOINT_URL: {'✅' if R2_ENDPOINT_URL else '❌'} {R2_ENDPOINT_URL[:50]}...")
        logger.info(f"  R2_ACCESS_KEY_ID: {'✅' if R2_ACCESS_KEY_ID else '❌'} {R2_ACCESS_KEY_ID[:10] if R2_ACCESS_KEY_ID else 'Not set'}...")
        logger.info(f"  R2_SECRET_ACCESS_KEY: {'✅' if R2_SECRET_ACCESS_KEY else '❌'} {'*' * 10 if R2_SECRET_ACCESS_KEY else 'Not set'}")
        logger.info(f"  R2_BUCKET_NAME: {'✅' if R2_BUCKET_NAME else '❌'} {R2_BUCKET_NAME}")
        
        if not all([R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY]):
            logger.error("\n❌ 请设置R2认证环境变量后再运行")
            logger.info("\n可以通过以下方式设置:")
            logger.info("export R2_ACCESS_KEY_ID='your-access-key'")
            logger.info("export R2_SECRET_ACCESS_KEY='your-secret-key'")
            return
    
    # 1. 获取当前数据库中的图片
    logger.info("\n1️⃣ 获取数据库图片信息...")
    db_images = get_current_db_images()
    deleted_images = get_deleted_images()
    
    # 2. 列出R2中的所有图片
    logger.info("\n2️⃣ 连接R2存储桶...")
    r2_images = list_r2_images()
    
    if not r2_images:
        logger.error("无法获取R2图片列表")
        return
    
    # 3. 识别需要删除的图片
    logger.info("\n3️⃣ 分析需要删除的图片...")
    images_to_delete = identify_images_to_delete(r2_images, db_images, deleted_images)
    
    # 4. 执行删除
    if images_to_delete:
        logger.info(f"\n4️⃣ {'执行删除' if args.delete else '试运行'}...")
        delete_r2_images(images_to_delete, dry_run=not args.delete)
        
        if not args.delete:
            logger.info("\n💡 提示: 这是试运行模式，没有实际删除任何文件")
            logger.info("   要实际删除文件，请使用: python3 scripts/clean_r2_old_images.py --delete")
    else:
        logger.info("\n✨ R2存储桶已经是最新的，没有需要删除的图片")

if __name__ == '__main__':
    main()