#!/usr/bin/env python3
"""
大批量R2上传器
将处理后的透明背景PNG图片上传到Cloudflare R2
"""

import os
import json
import boto3
import logging
import time
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict
import glob
from botocore.client import Config
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('.env') or load_dotenv('unsplash/.env')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/r2_upload_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MassiveR2Uploader:
    def __init__(self):
        self.input_dir = 'png/pixabay_massive'
        
        # R2配置从环境变量获取
        self.r2_endpoint = os.getenv('R2_ENDPOINT')
        self.r2_access_key = os.getenv('R2_ACCESS_KEY_ID')
        self.r2_secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.r2_bucket = os.getenv('R2_BUCKET')
        self.r2_public_url = os.getenv('R2_PUBLIC_URL', 'https://img.thinkora.pics')
        
        # 验证配置
        if not all([self.r2_endpoint, self.r2_access_key, self.r2_secret_key, self.r2_bucket]):
            raise ValueError("Missing R2 configuration. Check environment variables.")
        
        # 初始化R2客户端
        self.r2_client = boto3.client(
            's3',
            endpoint_url=self.r2_endpoint,
            aws_access_key_id=self.r2_access_key,
            aws_secret_access_key=self.r2_secret_key,
            config=Config(signature_version='s3v4')
        )
        
        # 创建目录
        os.makedirs('logs', exist_ok=True)
        
        # 统计信息
        self.stats = {
            'total_found': 0,
            'uploaded': 0,
            'failed': 0,
            'skipped': 0,
            'category_stats': defaultdict(int),
            'start_time': datetime.now()
        }
        
        logger.info(f"✅ R2 uploader initialized")
        logger.info(f"🔗 Endpoint: {self.r2_endpoint}")
        logger.info(f"🪣 Bucket: {self.r2_bucket}")
        logger.info(f"🌐 Public URL: {self.r2_public_url}")
    
    def get_png_files(self) -> List[str]:
        """获取所有需要上传的PNG文件"""
        pattern = os.path.join(self.input_dir, "*.png")
        files = glob.glob(pattern)
        
        logger.info(f"📁 Found {len(files)} PNG files to upload")
        self.stats['total_found'] = len(files)
        
        return sorted(files)
    
    def load_image_metadata(self, png_path: str) -> Dict[str, Any]:
        """加载图片元数据"""
        try:
            metadata_path = png_path.replace('.png', '_metadata.json')
            
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"No metadata found for {os.path.basename(png_path)}")
                
                # 从文件名解析基本信息
                filename = os.path.basename(png_path)
                name_without_ext = os.path.splitext(filename)[0]
                parts = name_without_ext.split('_')
                
                return {
                    'id': parts[2] if len(parts) > 2 else name_without_ext,
                    'category': parts[1] if len(parts) > 1 else 'unknown',
                    'title': f"Image {parts[2] if len(parts) > 2 else name_without_ext}",
                    'platform': 'pixabay',
                    'background_removed': True,
                    'file_format': 'PNG'
                }
                
        except Exception as e:
            logger.error(f"Error loading metadata for {png_path}: {e}")
            return {
                'id': os.path.splitext(os.path.basename(png_path))[0],
                'category': 'unknown',
                'title': 'Unknown image',
                'platform': 'pixabay',
                'background_removed': True,
                'file_format': 'PNG'
            }
    
    def check_if_exists(self, s3_key: str) -> bool:
        """检查文件是否已在R2中存在"""
        try:
            self.r2_client.head_object(Bucket=self.r2_bucket, Key=s3_key)
            return True
        except:
            return False
    
    def upload_single_file(self, local_path: str, metadata: Dict[str, Any]) -> bool:
        """上传单个文件到R2"""
        try:
            filename = os.path.basename(local_path)
            s3_key = f"images/{filename}"
            
            # 检查是否已存在
            if self.check_if_exists(s3_key):
                logger.debug(f"⏭️ File already exists in R2: {filename}")
                self.stats['skipped'] += 1
                return True
            
            # 准备上传元数据
            upload_metadata = {
                'Content-Type': 'image/png',
                'Cache-Control': 'public, max-age=31536000',  # 1年缓存
                'Metadata': {
                    'original-id': str(metadata.get('id', '')),
                    'category': str(metadata.get('category', '')),
                    'platform': str(metadata.get('platform', 'pixabay')),
                    'processed': 'true',
                    'background-removed': 'true',
                    'upload-date': datetime.now().isoformat()
                }
            }
            
            # 上传文件
            logger.info(f"📤 Uploading: {filename} -> {s3_key}")
            
            with open(local_path, 'rb') as f:
                self.r2_client.upload_fileobj(
                    f,
                    self.r2_bucket,
                    s3_key,
                    ExtraArgs=upload_metadata
                )
            
            self.stats['uploaded'] += 1
            self.stats['category_stats'][metadata.get('category', 'unknown')] += 1
            
            logger.info(f"✅ Successfully uploaded: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to upload {local_path}: {e}")
            self.stats['failed'] += 1
            return False
    
    def create_unified_metadata(self, processed_files: List[str]) -> List[Dict[str, Any]]:
        """创建统一的元数据文件"""
        unified_metadata = []
        
        for png_path in processed_files:
            try:
                # 加载元数据
                metadata = self.load_image_metadata(png_path)
                
                # 构建统一格式
                filename = os.path.basename(png_path)
                image_id = metadata.get('id', os.path.splitext(filename)[0])
                
                unified_entry = {
                    'id': f"pixabay_{image_id}",
                    'title': metadata.get('title', f"Image {image_id}"),
                    'description': metadata.get('description', metadata.get('title', f"High-quality transparent background image from Pixabay")),
                    'tags': metadata.get('tags', []),
                    'category': metadata.get('category', 'general'),
                    'imageUrl': f"{self.r2_public_url}/images/{filename}",
                    'thumbnailUrl': f"{self.r2_public_url}/images/{filename}",
                    'downloadUrl': f"{self.r2_public_url}/images/{filename}",
                    'width': metadata.get('width', 0),
                    'height': metadata.get('height', 0),
                    'transparencyRatio': 1.0,  # 处理后的图片都有透明背景
                    'qualityScore': metadata.get('quality_score', 95),
                    'platform': 'pixabay',
                    'author': metadata.get('author', 'Pixabay Contributor'),
                    'authorUrl': metadata.get('author_url', 'https://pixabay.com/'),
                    'uploadDate': datetime.now().isoformat(),
                    'fileSize': os.path.getsize(png_path) if os.path.exists(png_path) else 0,
                    'processingInfo': {
                        'background_removed': True,
                        'file_format': 'PNG',
                        'transparency_added': True,
                        'processed_date': metadata.get('processed_date', datetime.now().isoformat()),
                        'original_query': metadata.get('query_used', ''),
                        'fetch_metadata': metadata.get('fetch_metadata', {})
                    }
                }
                
                unified_metadata.append(unified_entry)
                
            except Exception as e:
                logger.error(f"Error processing metadata for {png_path}: {e}")
        
        return unified_metadata
    
    def run_massive_upload(self) -> Dict[str, Any]:
        """执行大批量上传任务"""
        logger.info("🚀 Starting massive R2 upload")
        
        # 获取所有PNG文件
        png_files = self.get_png_files()
        
        if not png_files:
            logger.warning("❌ No PNG files found to upload")
            return self.generate_report([])
        
        logger.info(f"📊 Uploading {len(png_files)} PNG files to R2...")
        
        # 上传每个文件
        uploaded_files = []
        
        for i, png_path in enumerate(png_files, 1):
            logger.info(f"\n📤 [{i}/{len(png_files)}] Processing: {os.path.basename(png_path)}")
            
            # 加载元数据
            metadata = self.load_image_metadata(png_path)
            
            # 上传文件
            if self.upload_single_file(png_path, metadata):
                uploaded_files.append(png_path)
            
            # 每50个文件输出进度报告
            if i % 50 == 0:
                elapsed = datetime.now() - self.stats['start_time']
                rate = i / elapsed.total_seconds() * 60  # 每分钟上传数
                eta_minutes = (len(png_files) - i) / rate if rate > 0 else 0
                
                logger.info(f"""
🔄 Progress Report - {i}/{len(png_files)} processed
✅ Uploaded: {self.stats['uploaded']} | ❌ Failed: {self.stats['failed']} | ⏭️ Skipped: {self.stats['skipped']}
⏱️ Speed: {rate:.1f} files/min | ETA: {eta_minutes:.1f} minutes
📊 Categories: {dict(self.stats['category_stats'])}
                """)
            
            # 短暂休息避免过载
            time.sleep(0.1)
        
        return self.generate_report(uploaded_files)
    
    def generate_report(self, uploaded_files: List[str]) -> Dict[str, Any]:\n        \"\"\"生成上传报告\"\"\"\n        end_time = datetime.now()\n        total_duration = end_time - self.stats['start_time']\n        \n        # 创建统一元数据\n        logger.info(\"📝 Creating unified metadata...\")\n        unified_metadata = self.create_unified_metadata(uploaded_files)\n        \n        # 保存新的元数据到现有文件\n        metadata_file = 'dist/metadata.json'\n        existing_metadata = []\n        \n        # 加载现有元数据\n        if os.path.exists(metadata_file):\n            try:\n                with open(metadata_file, 'r', encoding='utf-8') as f:\n                    existing_metadata = json.load(f)\n                logger.info(f\"📚 Loaded {len(existing_metadata)} existing images\")\n            except Exception as e:\n                logger.error(f\"Error loading existing metadata: {e}\")\n                existing_metadata = []\n        \n        # 合并元数据（避免重复）\n        existing_ids = {img.get('id') for img in existing_metadata}\n        new_images = [img for img in unified_metadata if img['id'] not in existing_ids]\n        \n        # 更新元数据文件\n        all_metadata = existing_metadata + new_images\n        \n        with open(metadata_file, 'w', encoding='utf-8') as f:\n            json.dump(all_metadata, f, indent=2, ensure_ascii=False)\n        \n        # 生成报告\n        report = {\n            'summary': {\n                'total_found': self.stats['total_found'],\n                'uploaded': self.stats['uploaded'],\n                'failed': self.stats['failed'],\n                'skipped': self.stats['skipped'],\n                'new_images_added': len(new_images),\n                'total_images_now': len(all_metadata),\n                'success_rate': f\"{self.stats['uploaded'] / max(1, self.stats['total_found']) * 100:.1f}%\",\n                'duration': str(total_duration),\n                'upload_speed': f\"{self.stats['uploaded'] / total_duration.total_seconds() * 60:.1f} files/min\"\n            },\n            'category_distribution': dict(self.stats['category_stats']),\n            'r2_info': {\n                'endpoint': self.r2_endpoint,\n                'bucket': self.r2_bucket,\n                'public_url': self.r2_public_url,\n                'total_files_uploaded': self.stats['uploaded']\n            },\n            'metadata': {\n                'start_time': self.stats['start_time'].isoformat(),\n                'end_time': end_time.isoformat(),\n                'metadata_file': metadata_file,\n                'existing_images': len(existing_metadata),\n                'new_images': len(new_images)\n            }\n        }\n        \n        # 保存报告\n        report_file = f\"logs/r2_upload_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json\"\n        with open(report_file, 'w') as f:\n            json.dump(report, f, indent=2, ensure_ascii=False)\n        \n        logger.info(f\"\"\"\n🎉 MASSIVE R2 UPLOAD COMPLETED! 🎉\n\n📊 Final Statistics:\n• Total files found: {self.stats['total_found']}\n• Successfully uploaded: {self.stats['uploaded']}\n• Failed uploads: {self.stats['failed']}\n• Skipped (already exists): {self.stats['skipped']}\n• Success rate: {self.stats['uploaded'] / max(1, self.stats['total_found']) * 100:.1f}%\n• Total duration: {total_duration}\n• Upload speed: {self.stats['uploaded'] / total_duration.total_seconds() * 60:.1f} files/min\n\n📁 Category distribution:\n{chr(10).join(f'• {cat}: {count} images' for cat, count in self.stats['category_stats'].items())}\n\n🌐 R2 Info:\n• Bucket: {self.r2_bucket}\n• Public URL: {self.r2_public_url}\n• Total images now: {len(all_metadata)}\n\n📄 Files:\n• Metadata: {metadata_file}\n• Report: {report_file}\n        \"\"\")\n        \n        return report\n\n\ndef main():\n    \"\"\"主函数\"\"\"\n    try:\n        uploader = MassiveR2Uploader()\n        report = uploader.run_massive_upload()\n        \n        # 输出JSON格式的报告\n        print(\"\\n\" + \"=\"*50)\n        print(\"R2 UPLOAD REPORT JSON:\")\n        print(\"=\"*50)\n        print(json.dumps(report, indent=2, ensure_ascii=False))\n        \n    except KeyboardInterrupt:\n        logger.info(\"⏹️ Upload interrupted by user\")\n    except Exception as e:\n        logger.error(f\"💥 Critical error: {e}\")\n        raise\n\n\nif __name__ == \"__main__\":\n    main()"