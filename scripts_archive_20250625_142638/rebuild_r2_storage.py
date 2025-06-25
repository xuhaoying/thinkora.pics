#!/usr/bin/env python3
"""
重建R2存储桶 - 只上传当前数据库中的图片
"""

import os
import json
import sqlite3
import requests
import subprocess
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# R2配置
R2_BUCKET_NAME = 'thinkora-pics'
R2_PUBLIC_URL = 'https://r2.thinkora.pics'  # 你的R2公开URL

def get_current_images():
    """获取当前数据库中的所有图片信息"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, tags, width, height, 
               url_thumbnail, url_regular, url_download
        FROM images
        ORDER BY id
    """)
    
    images = []
    for row in cursor.fetchall():
        images.append({
            'id': row[0],
            'title': row[1],
            'tags': json.loads(row[2]),
            'width': row[3],
            'height': row[4],
            'url_thumbnail': row[5],
            'url_regular': row[6],
            'url_download': row[7]
        })
    
    conn.close()
    logger.info(f"📸 从数据库获取 {len(images)} 张图片信息")
    return images

def find_local_image_file(image_id):
    """查找本地图片文件"""
    # 可能的位置
    possible_paths = [
        f'raw/pixabay/{image_id}.jpg',
        f'raw/unsplash/{image_id}.jpg',
        f'raw/pexels/{image_id}.jpg',
        f'png/{image_id}.png',
        f'processed_backup/pixabay/{image_id}.jpg',
        f'processed_backup/unsplash/{image_id}.jpg',
        f'processed_backup/pexels/{image_id}.jpg',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def download_image_if_needed(image):
    """如果本地没有图片，从URL下载"""
    image_id = image['id']
    local_path = find_local_image_file(image_id)
    
    if local_path:
        return local_path
    
    # 需要下载
    logger.info(f"⬇️ 下载图片: {image_id}")
    
    # 确定保存路径
    platform = image_id.split('_')[0]
    save_dir = f'raw/{platform}'
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f'{image_id}.jpg')
    
    # 尝试下载
    url = image.get('url_download') or image.get('url_regular')
    if not url:
        logger.error(f"❌ 没有下载URL: {image_id}")
        return None
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"✅ 下载成功: {save_path}")
        return save_path
        
    except Exception as e:
        logger.error(f"❌ 下载失败 {image_id}: {e}")
        return None

def calculate_file_hash(file_path):
    """计算文件MD5哈希"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def upload_to_r2_rclone(local_path, r2_path):
    """使用rclone上传到R2"""
    try:
        cmd = [
            'rclone', 'copy',
            local_path,
            f'r2:{R2_BUCKET_NAME}/{os.path.dirname(r2_path)}',
            '--s3-acl', 'public-read',
            '--progress'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            logger.error(f"rclone错误: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"上传异常: {e}")
        return False

def process_image(image, use_rclone=True):
    """处理单张图片"""
    image_id = image['id']
    
    # 1. 获取本地文件
    local_path = download_image_if_needed(image)
    if not local_path:
        return {
            'id': image_id,
            'status': 'failed',
            'error': 'No local file'
        }
    
    # 2. 确定R2路径
    ext = os.path.splitext(local_path)[1]
    r2_path = f'images/{image_id}{ext}'
    
    # 3. 上传到R2
    if use_rclone:
        success = upload_to_r2_rclone(local_path, r2_path)
    else:
        # 这里可以添加其他上传方法
        success = False
    
    if success:
        # 计算文件信息
        file_size = os.path.getsize(local_path)
        file_hash = calculate_file_hash(local_path)
        
        return {
            'id': image_id,
            'status': 'success',
            'local_path': local_path,
            'r2_path': r2_path,
            'r2_url': f'{R2_PUBLIC_URL}/{r2_path}',
            'file_size': file_size,
            'file_hash': file_hash,
            'tags': image['tags']
        }
    else:
        return {
            'id': image_id,
            'status': 'failed',
            'error': 'Upload failed'
        }

def update_database_urls(uploaded_images):
    """更新数据库中的图片URL"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    updated_count = 0
    for img in uploaded_images:
        if img['status'] == 'success':
            r2_url = img['r2_url']
            cursor.execute("""
                UPDATE images 
                SET url_thumbnail = ?, url_regular = ?, url_download = ?
                WHERE id = ?
            """, (r2_url, r2_url, r2_url, img['id']))
            updated_count += 1
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ 更新了 {updated_count} 条数据库记录")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='重建R2存储桶')
    parser.add_argument('--check-rclone', action='store_true', help='检查rclone配置')
    parser.add_argument('--dry-run', action='store_true', help='只检查，不实际上传')
    parser.add_argument('--workers', type=int, default=4, help='并发上传数量')
    args = parser.parse_args()
    
    logger.info("🚀 开始重建R2存储桶")
    logger.info("=" * 50)
    
    # 检查rclone
    if args.check_rclone:
        try:
            result = subprocess.run(['rclone', 'version'], capture_output=True)
            logger.info("✅ rclone已安装")
            
            # 检查R2配置
            result = subprocess.run(['rclone', 'ls', f'r2:{R2_BUCKET_NAME}', '--max-depth', '1'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("✅ rclone R2配置正常")
            else:
                logger.error("❌ rclone R2配置错误，请运行: rclone config")
                return
        except:
            logger.error("❌ rclone未安装，请运行: brew install rclone")
            return
    
    # 1. 获取当前数据库中的图片
    images = get_current_images()
    
    if args.dry_run:
        logger.info("\n🔍 试运行模式 - 检查本地文件")
        missing_count = 0
        for img in images:
            local_path = find_local_image_file(img['id'])
            if not local_path:
                logger.warning(f"缺失: {img['id']}")
                missing_count += 1
        
        logger.info(f"\n📊 统计:")
        logger.info(f"  总图片: {len(images)}")
        logger.info(f"  本地存在: {len(images) - missing_count}")
        logger.info(f"  需要下载: {missing_count}")
        return
    
    # 2. 准备上传
    logger.info(f"\n📤 开始上传 {len(images)} 张图片到R2...")
    
    uploaded_images = []
    failed_images = []
    
    # 使用线程池并发上传
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # 提交所有任务
        future_to_image = {
            executor.submit(process_image, img): img 
            for img in images
        }
        
        # 处理完成的任务
        for i, future in enumerate(as_completed(future_to_image), 1):
            result = future.result()
            
            if result['status'] == 'success':
                uploaded_images.append(result)
                logger.info(f"[{i}/{len(images)}] ✅ {result['id']}")
            else:
                failed_images.append(result)
                logger.error(f"[{i}/{len(images)}] ❌ {result['id']}: {result.get('error')}")
    
    # 3. 更新数据库URL
    if uploaded_images:
        logger.info("\n📝 更新数据库URL...")
        update_database_urls(uploaded_images)
    
    # 4. 生成报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_images': len(images),
        'uploaded': len(uploaded_images),
        'failed': len(failed_images),
        'total_size_mb': sum(img['file_size'] for img in uploaded_images) / 1024 / 1024,
        'uploaded_files': uploaded_images,
        'failed_files': failed_images
    }
    
    report_path = f'logs/r2_rebuild_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # 5. 显示摘要
    logger.info("\n✅ 重建完成!")
    logger.info(f"📊 上传统计:")
    logger.info(f"  成功: {len(uploaded_images)} 张")
    logger.info(f"  失败: {len(failed_images)} 张")
    logger.info(f"  总大小: {report['total_size_mb']:.1f} MB")
    logger.info(f"  详细报告: {report_path}")
    
    if failed_images:
        logger.info(f"\n⚠️ 失败的图片ID:")
        for img in failed_images[:10]:
            logger.info(f"  - {img['id']}: {img.get('error')}")

if __name__ == '__main__':
    main()