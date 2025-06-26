#!/usr/bin/env python3
"""
R2存储上传脚本 - 将处理后的PNG图片上传到Cloudflare R2
"""

import os
import sys
import sqlite3
import boto3
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from botocore.config import Config
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class R2Uploader:
    def __init__(self):
        self.db_path = "images.db"
        self.processed_dir = Path("processed_images")
        
        # R2配置
        self.access_key = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.account_id = os.getenv('R2_ACCOUNT_ID')
        self.bucket_name = os.getenv('R2_BUCKET_NAME', 'thinkora-pics')
        self.public_url = os.getenv('R2_PUBLIC_URL', 'https://img.thinkora.pics')
        
        if not all([self.access_key, self.secret_key, self.account_id]):
            print("❌ 请配置R2环境变量 (R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID)")
            sys.exit(1)
        
        # 初始化S3客户端
        self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
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
    
    def test_connection(self):
        """测试R2连接"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                MaxKeys=1
            )
            print("✅ R2连接测试成功")
            return True
        except Exception as e:
            print(f"❌ R2连接测试失败: {e}")
            return False
    
    def get_pending_uploads(self):
        """获取待上传的图片"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM images 
            WHERE processed = TRUE AND uploaded = FALSE
        """)
        
        images = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        
        return [dict(zip(columns, row)) for row in images]
    
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
            print(f"❌ 获取已上传文件列表失败: {e}")
            return set()
    
    def upload_single_file(self, image_data, force=False):
        """上传单个文件"""
        image_id = image_data['id']
        local_path = self.processed_dir / f"{image_id}.png"
        r2_key = f"images/{image_id}.png"
        
        if not local_path.exists():
            return False, f"本地文件不存在: {local_path}"
        
        # 检查是否已上传
        if not force:
            try:
                self.s3_client.head_object(Bucket=self.bucket_name, Key=r2_key)
                return True, "文件已存在"
            except:
                pass  # 文件不存在，继续上传
        
        try:
            # 上传文件
            extra_args = {
                'ContentType': 'image/png',
                'CacheControl': 'public, max-age=31536000'  # 1年缓存
            }
            
            self.s3_client.upload_file(
                str(local_path),
                self.bucket_name,
                r2_key,
                ExtraArgs=extra_args
            )
            
            # 更新数据库
            self.mark_as_uploaded(image_id, f"{self.public_url}/{r2_key}")
            
            return True, "上传成功"
            
        except Exception as e:
            return False, f"上传失败: {e}"
    
    def mark_as_uploaded(self, image_id, public_url):
        """标记为已上传"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE images 
            SET uploaded = TRUE,
                uploaded_at = ?,
                url_regular = ?,
                url_download = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), public_url, public_url, image_id))
        
        conn.commit()
        conn.close()
    
    def upload_batch(self, force=False, max_workers=5):
        """批量上传"""
        if not self.test_connection():
            return 0
        
        images = self.get_pending_uploads()
        
        if not images:
            print("📋 没有待上传的图片")
            return 0
        
        print(f"🚀 开始上传 {len(images)} 张图片到R2...")
        
        success_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交任务
            future_to_image = {
                executor.submit(self.upload_single_file, image, force): image 
                for image in images
            }
            
            # 处理结果
            for i, future in enumerate(as_completed(future_to_image), 1):
                image = future_to_image[future]
                try:
                    success, message = future.result()
                    if success:
                        success_count += 1
                        print(f"✅ ({i}/{len(images)}) {image['id']}")
                    else:
                        print(f"❌ ({i}/{len(images)}) {image['id']}: {message}")
                except Exception as e:
                    print(f"❌ ({i}/{len(images)}) {image['id']}: 处理异常 {e}")
        
        print(f"✅ 批量上传完成: {success_count}/{len(images)} 成功")
        return success_count
    
    def sync_database_urls(self):
        """同步数据库中的URL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE images 
            SET url_regular = ? || '/images/' || id || '.png',
                url_download = ? || '/images/' || id || '.png'
            WHERE uploaded = TRUE
        """, (self.public_url, self.public_url))
        
        updated_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"✅ 同步了 {updated_count} 条数据库记录的URL")
        return updated_count
    
    def get_upload_stats(self):
        """获取上传统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM images WHERE processed = TRUE")
        processed = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM images WHERE uploaded = TRUE")
        uploaded = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'processed': processed,
            'uploaded': uploaded,
            'pending': processed - uploaded
        }

def main():
    parser = argparse.ArgumentParser(description="上传图片到R2存储")
    parser.add_argument("--force", action="store_true", help="强制重新上传")
    parser.add_argument("--workers", type=int, default=5, help="并发上传数")
    parser.add_argument("--stats", action="store_true", help="显示上传统计")
    parser.add_argument("--sync-urls", action="store_true", help="同步数据库URL")
    
    args = parser.parse_args()
    
    uploader = R2Uploader()
    
    if args.stats:
        stats = uploader.get_upload_stats()
        print("📊 上传统计:")
        print(f"  已处理: {stats['processed']}")
        print(f"  已上传: {stats['uploaded']}")
        print(f"  待上传: {stats['pending']}")
    elif args.sync_urls:
        uploader.sync_database_urls()
    else:
        uploader.upload_batch(args.force, args.workers)

if __name__ == "__main__":
    main()