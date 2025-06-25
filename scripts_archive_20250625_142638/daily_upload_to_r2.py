#!/usr/bin/env python3
"""
每日自动上传图片到Cloudflare R2
包括元数据更新和网站重新生成
"""

import os
import json
import boto3
import logging
from datetime import datetime
from typing import List, Dict, Any
from botocore.exceptions import NoCredentialsError
import hashlib
from dotenv import load_dotenv
import concurrent.futures

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/daily_upload_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# R2配置
R2_ENDPOINT = os.getenv('R2_ENDPOINT')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET = os.getenv('R2_BUCKET', 'thinkora-images')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

class R2Uploader:
    def __init__(self):
        # 初始化S3客户端（R2兼容S3 API）
        self.s3_client = boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name='auto'
        )
        
        # 加载已上传记录
        self.uploaded_files = self.load_uploaded_records()
        
        # 加载现有元数据
        self.metadata = self.load_metadata()
    
    def load_uploaded_records(self) -> set:
        """加载已上传的文件记录"""
        uploaded_file = 'uploaded_to_r2.json'
        if os.path.exists(uploaded_file):
            with open(uploaded_file, 'r') as f:
                data = json.load(f)
                return set(data.get('uploaded', []))
        return set()
    
    def save_uploaded_records(self):
        """保存已上传的文件记录"""
        with open('uploaded_to_r2.json', 'w') as f:
            json.dump({'uploaded': list(self.uploaded_files)}, f, indent=2)
    
    def load_metadata(self) -> List[Dict[str, Any]]:
        """加载现有元数据"""
        if os.path.exists('metadata_r2.json'):
            with open('metadata_r2.json', 'r') as f:
                return json.load(f)
        return []
    
    def save_metadata(self):
        """保存更新后的元数据"""
        with open('metadata_r2.json', 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def calculate_file_hash(self, filepath: str) -> str:
        """计算文件哈希值"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def upload_single_file(self, local_path: str, r2_key: str) -> bool:
        """上传单个文件到R2"""
        try:
            # 确定内容类型
            content_type = 'image/png' if local_path.endswith('.png') else 'application/json'
            
            # 设置缓存头
            extra_args = {
                'ContentType': content_type,
                'CacheControl': 'public, max-age=31536000, immutable' if content_type == 'image/png' else 'public, max-age=3600'
            }
            
            # 上传文件
            with open(local_path, 'rb') as f:
                self.s3_client.put_object(
                    Bucket=R2_BUCKET,
                    Key=r2_key,
                    Body=f,
                    **extra_args
                )
            
            logger.info(f"Uploaded: {r2_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading {local_path}: {e}")
            return False
    
    def get_new_images(self) -> List[Dict[str, Any]]:
        """获取需要上传的新图片"""
        new_images = []
        
        for platform in ['unsplash', 'pexels', 'pixabay']:
            png_dir = os.path.join('png', platform)
            if not os.path.exists(png_dir):
                continue
            
            for filename in os.listdir(png_dir):
                if filename.endswith('.png'):
                    file_hash = self.calculate_file_hash(os.path.join(png_dir, filename))
                    
                    if file_hash not in self.uploaded_files:
                        # 加载图片元数据
                        metadata_path = os.path.join(png_dir, filename.replace('.png', '_metadata.json'))
                        if os.path.exists(metadata_path):
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                            
                            new_images.append({
                                'filename': filename,
                                'platform': platform,
                                'local_path': os.path.join(png_dir, filename),
                                'metadata_path': metadata_path,
                                'hash': file_hash,
                                'metadata': metadata
                            })
        
        return new_images
    
    def update_metadata_entry(self, image_info: Dict[str, Any]) -> Dict[str, Any]:
        """创建或更新元数据条目"""
        metadata = image_info['metadata']
        filename = image_info['filename']
        
        # 构建R2 URL
        r2_url = f"{R2_PUBLIC_URL}/images/{image_info['platform']}/{filename}"
        thumbnail_url = f"{R2_PUBLIC_URL}/thumbnails/{image_info['platform']}/{filename}"
        
        # 创建元数据条目
        entry = {
            'id': metadata.get('id', filename.replace('.png', '')),
            'title': metadata.get('description', '').split('.')[0] if metadata.get('description') else f"Image {filename}",
            'description': metadata.get('description', ''),
            'tags': metadata.get('tags', []),
            'category': self.determine_category(metadata.get('tags', [])),
            'imageUrl': r2_url,
            'thumbnailUrl': thumbnail_url,
            'downloadUrl': r2_url,
            'width': metadata.get('width', 0),
            'height': metadata.get('height', 0),
            'transparencyRatio': metadata.get('transparency_ratio', 0),
            'qualityScore': metadata.get('quality_score', 0),
            'platform': image_info['platform'],
            'author': metadata.get('author', ''),
            'authorUrl': metadata.get('author_url', ''),
            'uploadDate': datetime.now().isoformat(),
            'fileSize': metadata.get('file_size', 0)
        }
        
        return entry
    
    def determine_category(self, tags: List[str]) -> str:
        """根据标签确定类别"""
        tag_str = ' '.join(tags).lower()
        
        categories = {
            'electronics': ['electronic', 'computer', 'phone', 'tech', 'gadget', 'device'],
            'office': ['office', 'desk', 'work', 'business', 'stationery'],
            'lifestyle': ['lifestyle', 'home', 'living', 'daily', 'personal'],
            'fashion': ['fashion', 'clothing', 'style', 'wear', 'accessory'],
            'food': ['food', 'eat', 'drink', 'cuisine', 'meal'],
            'nature': ['nature', 'plant', 'flower', 'outdoor', 'garden'],
            'education': ['education', 'learn', 'study', 'book', 'school'],
            'health': ['health', 'medical', 'fitness', 'wellness', 'care'],
            'art': ['art', 'creative', 'design', 'craft', 'artistic'],
            'photography': ['photo', 'camera', 'lens', 'photography']
        }
        
        for category, keywords in categories.items():
            if any(keyword in tag_str for keyword in keywords):
                return category
        
        return 'other'
    
    def generate_thumbnails(self, image_path: str, thumbnail_path: str):
        """生成缩略图（简化版，实际应该使用PIL）"""
        # 这里应该使用PIL生成实际的缩略图
        # 暂时只是复制文件作为演示
        import shutil
        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
        shutil.copy2(image_path, thumbnail_path)
    
    def run_daily_upload(self, max_workers: int = 4):
        """执行每日上传任务"""
        logger.info("Starting daily R2 upload")
        
        # 获取新图片
        new_images = self.get_new_images()
        logger.info(f"Found {len(new_images)} new images to upload")
        
        if not new_images:
            logger.info("No new images to upload")
            return
        
        # 上传统计
        results = {
            'total': len(new_images),
            'uploaded': 0,
            'failed': 0,
            'new_metadata_entries': []
        }
        
        # 使用线程池并行上传
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for image in new_images:
                # 上传原图
                r2_key = f"images/{image['platform']}/{image['filename']}"
                futures.append(executor.submit(self.upload_single_file, image['local_path'], r2_key))
                
                # 生成并上传缩略图
                thumbnail_path = f"temp_thumbnails/{image['platform']}/{image['filename']}"
                self.generate_thumbnails(image['local_path'], thumbnail_path)
                thumbnail_r2_key = f"thumbnails/{image['platform']}/{image['filename']}"
                futures.append(executor.submit(self.upload_single_file, thumbnail_path, thumbnail_r2_key))
                
                # 上传元数据
                metadata_r2_key = f"metadata/{image['platform']}/{image['filename'].replace('.png', '_metadata.json')}"
                futures.append(executor.submit(self.upload_single_file, image['metadata_path'], metadata_r2_key))
            
            # 等待所有上传完成
            for future in concurrent.futures.as_completed(futures):
                try:
                    if future.result():
                        results['uploaded'] += 1
                    else:
                        results['failed'] += 1
                except Exception as e:
                    logger.error(f"Upload error: {e}")
                    results['failed'] += 1
        
        # 更新元数据
        for image in new_images:
            metadata_entry = self.update_metadata_entry(image)
            self.metadata.append(metadata_entry)
            results['new_metadata_entries'].append(metadata_entry)
            self.uploaded_files.add(image['hash'])
        
        # 保存更新的记录
        self.save_uploaded_records()
        self.save_metadata()
        
        # 清理临时缩略图
        import shutil
        if os.path.exists('temp_thumbnails'):
            shutil.rmtree('temp_thumbnails')
        
        # 生成上传报告
        report = {
            'date': datetime.now().isoformat(),
            'total_files': results['total'] * 3,  # 原图、缩略图、元数据
            'successful_uploads': results['uploaded'],
            'failed_uploads': results['failed'],
            'new_images': len(new_images),
            'total_images_in_r2': len(self.metadata),
            'new_entries': [
                {
                    'id': entry['id'],
                    'title': entry['title'],
                    'category': entry['category'],
                    'platform': entry['platform']
                } for entry in results['new_metadata_entries']
            ]
        }
        
        # 保存报告
        report_file = f"logs/upload_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Daily upload completed. Uploaded {len(new_images)} new images")
        
        # 触发网站重新生成
        self.regenerate_website()
        
        return report
    
    def regenerate_website(self):
        """重新生成网站静态文件"""
        logger.info("Regenerating website with new images")
        
        try:
            # 调用生成脚本
            import subprocess
            result = subprocess.run(
                ['python', 'generate_image_pages.py'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("Website regenerated successfully")
            else:
                logger.error(f"Website regeneration failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error regenerating website: {e}")


if __name__ == "__main__":
    # 检查必要的环境变量
    if not all([R2_ENDPOINT, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_PUBLIC_URL]):
        logger.error("Missing R2 configuration. Please set environment variables.")
        exit(1)
    
    uploader = R2Uploader()
    report = uploader.run_daily_upload()
    print(json.dumps(report, indent=2))