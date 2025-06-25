#!/usr/bin/env python3
"""
上传PNG图片到Cloudflare R2存储
"""

import os
import logging
import boto3
import sqlite3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from botocore.config import Config
import time
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class R2Uploader:
    def __init__(self):
        """初始化R2客户端"""
        # 从环境变量获取认证信息
        self.access_key = os.getenv('R2_ACCESS_KEY_ID') or os.getenv('R2_ACCESS_KEY')
        self.secret_key = os.getenv('R2_SECRET_ACCESS_KEY') or os.getenv('R2_SECRET_KEY')
        self.account_id = os.getenv('R2_ACCOUNT_ID')
        self.bucket_name = os.getenv('R2_BUCKET') or os.getenv('R2_BUCKET_NAME') or "thinkora-pics"
        self.endpoint_url = os.getenv('R2_ENDPOINT')
        self.public_url = os.getenv('R2_PUBLIC_URL')
        
        # 如果没有endpoint，使用account_id构建
        if not self.endpoint_url and self.account_id:
            self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
        
        if not all([self.access_key, self.secret_key, self.endpoint_url]):
            logger.error("❌ 请设置R2环境变量:")
            logger.error("   R2_ACCESS_KEY_ID 或 R2_ACCESS_KEY")
            logger.error("   R2_SECRET_ACCESS_KEY 或 R2_SECRET_KEY")
            logger.error("   R2_ENDPOINT 或 R2_ACCOUNT_ID")
            logger.error(f"\n当前环境变量:")
            logger.error(f"   Access Key: {'已设置' if self.access_key else '未设置'}")
            logger.error(f"   Secret Key: {'已设置' if self.secret_key else '未设置'}")
            logger.error(f"   Endpoint: {self.endpoint_url or '未设置'}")
            logger.error(f"   Bucket: {self.bucket_name}")
            raise ValueError("Missing R2 credentials")
        
        # 创建S3客户端（R2兼容S3 API）
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(
                region_name='auto',
                retries={'max_attempts': 3}
            )
        )
        
        logger.info(f"✅ R2客户端初始化成功")
        logger.info(f"   Endpoint: {self.endpoint_url}")
        logger.info(f"   Bucket: {self.bucket_name}")
    
    def test_connection(self):
        """测试R2连接"""
        try:
            # 尝试列出bucket
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                MaxKeys=1
            )
            logger.info("✅ R2连接测试成功")
            return True
        except Exception as e:
            logger.error(f"❌ R2连接测试失败: {e}")
            return False
    
    def upload_file(self, local_path: str, r2_key: str) -> bool:
        """上传单个文件到R2"""
        try:
            # 设置PNG的正确Content-Type
            extra_args = {
                'ContentType': 'image/png',
                'CacheControl': 'public, max-age=31536000'  # 1年缓存
            }
            
            self.s3_client.upload_file(
                local_path,
                self.bucket_name,
                r2_key,
                ExtraArgs=extra_args
            )
            
            return True
            
        except Exception as e:
            logger.error(f"上传失败 {r2_key}: {e}")
            return False
    
    def get_uploaded_files(self):
        """获取已上传的文件列表"""
        try:
            uploaded = set()
            paginator = self.s3_client.get_paginator('list_objects_v2')
            
            for page in paginator.paginate(Bucket=self.bucket_name, Prefix='images/'):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        uploaded.add(obj['Key'])
            
            return uploaded
            
        except Exception as e:
            logger.error(f"获取已上传文件列表失败: {e}")
            return set()
    
    def upload_images_batch(self, images_dir='public/images_png', max_workers=5):
        """批量上传图片"""
        logger.info("🚀 开始批量上传PNG图片到R2")
        
        # 检查连接
        if not self.test_connection():
            return
        
        # 获取所有PNG文件
        png_files = list(Path(images_dir).glob('*.png'))
        total_files = len(png_files)
        
        if total_files == 0:
            logger.error(f"❌ 在 {images_dir} 中没有找到PNG文件")
            return
        
        logger.info(f"📊 找到 {total_files} 张PNG图片需要上传")
        
        # 获取已上传的文件
        logger.info("📋 检查已上传的文件...")
        uploaded_files = self.get_uploaded_files()
        logger.info(f"已上传文件数: {len(uploaded_files)}")
        
        # 准备上传任务
        upload_tasks = []
        for png_file in png_files:
            r2_key = f"images/{png_file.name}"
            if r2_key not in uploaded_files:
                upload_tasks.append((str(png_file), r2_key))
        
        logger.info(f"需要上传: {len(upload_tasks)} 张图片")
        
        if len(upload_tasks) == 0:
            logger.info("✅ 所有图片都已上传！")
            return
        
        # 开始上传
        start_time = datetime.now()
        success_count = 0
        fail_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交任务
            future_to_task = {
                executor.submit(self.upload_file, local_path, r2_key): (local_path, r2_key)
                for local_path, r2_key in upload_tasks
            }
            
            # 处理结果
            for i, future in enumerate(as_completed(future_to_task), 1):
                local_path, r2_key = future_to_task[future]
                
                try:
                    result = future.result()
                    if result:
                        success_count += 1
                        logger.debug(f"✅ 上传成功: {r2_key}")
                    else:
                        fail_count += 1
                except Exception as e:
                    fail_count += 1
                    logger.error(f"❌ 上传异常 {r2_key}: {e}")
                
                # 每100个文件显示一次进度
                if i % 100 == 0:
                    progress = i / len(upload_tasks) * 100
                    logger.info(f"进度: {i}/{len(upload_tasks)} ({progress:.1f}%) - 成功: {success_count}, 失败: {fail_count}")
        
        # 上传完成报告
        elapsed = datetime.now() - start_time
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 R2上传完成报告:")
        logger.info(f"  总文件数: {len(upload_tasks)}")
        logger.info(f"  成功上传: {success_count}")
        logger.info(f"  上传失败: {fail_count}")
        logger.info(f"  总耗时: {elapsed}")
        logger.info(f"  平均速度: {success_count / elapsed.total_seconds():.2f} 文件/秒")
        logger.info(f"{'='*60}")
        
        if success_count > 0:
            logger.info("\n✅ 上传完成！")
            logger.info(f"🌐 图片可通过以下URL访问:")
            logger.info(f"   https://r2.thinkora.pics/images/filename.png")
            logger.info(f"\n💡 下一步:")
            logger.info(f"   1. 配置R2存储桶的公开访问")
            logger.info(f"   2. 设置自定义域名（可选）")
            logger.info(f"   3. 运行: python3 scripts/restore_r2_urls.py")

def update_database_r2_urls(base_url="https://r2.thinkora.pics"):
    """更新数据库中的图片URL为R2地址"""
    logger.info("📝 更新数据库中的图片URL为R2地址...")
    
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    
    # 更新所有URL为R2地址
    cursor.execute("""
        UPDATE images 
        SET url_thumbnail = ? || '/images/' || id || '.png',
            url_regular = ? || '/images/' || id || '.png'
        WHERE url_thumbnail LIKE '%/images/%'
    """, (base_url, base_url))
    
    updated = cursor.rowcount
    conn.commit()
    conn.close()
    
    logger.info(f"✅ 更新了 {updated} 条数据库记录")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='上传PNG图片到Cloudflare R2')
    parser.add_argument('--images-dir', default='public/images_png', help='PNG图片目录')
    parser.add_argument('--workers', type=int, default=5, help='并发上传数')
    parser.add_argument('--test', action='store_true', help='只测试连接')
    parser.add_argument('--update-db', action='store_true', help='更新数据库URL为R2地址')
    
    args = parser.parse_args()
    
    if args.update_db:
        update_database_r2_urls()
        return
    
    try:
        uploader = R2Uploader()
        
        if args.test:
            uploader.test_connection()
        else:
            uploader.upload_images_batch(args.images_dir, args.workers)
            
    except Exception as e:
        logger.error(f"❌ 程序执行失败: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())