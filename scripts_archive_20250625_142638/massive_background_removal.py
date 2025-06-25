#!/usr/bin/env python3
"""
大批量背景移除处理器
处理从Pixabay下载的大量图片，移除背景并保存为PNG
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict
import glob

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/background_removal_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MassiveBackgroundRemover:
    def __init__(self):
        self.input_dir = 'raw/pixabay_massive'
        self.output_dir = 'png/pixabay_massive'
        self.processed_dir = 'processed_backup/pixabay_massive'
        
        # 创建目录
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # 统计信息
        self.stats = {
            'total_found': 0,
            'processed': 0,
            'succeeded': 0,
            'failed': 0,
            'skipped': 0,
            'category_stats': defaultdict(int),
            'start_time': datetime.now()
        }
        
        # 检查rembg是否可用
        self.check_rembg()
    
    def check_rembg(self):
        """检查rembg是否已安装"""
        try:
            import rembg
            logger.info("✅ rembg library found")
            return True
        except ImportError:
            logger.error("❌ rembg library not found. Installing...")
            self.install_rembg()
    
    def install_rembg(self):
        """安装rembg库"""
        try:
            import subprocess
            import sys
            
            logger.info("📦 Installing rembg...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "rembg"])
            logger.info("✅ rembg installed successfully")
            
            # 重新导入
            import rembg
            
        except Exception as e:
            logger.error(f"❌ Failed to install rembg: {e}")
            raise
    
    def get_image_files(self) -> List[str]:
        """获取所有需要处理的图片文件"""
        pattern = os.path.join(self.input_dir, "*.jpg")
        files = glob.glob(pattern)
        
        logger.info(f"📁 Found {len(files)} images to process")
        self.stats['total_found'] = len(files)
        
        return sorted(files)
    
    def extract_image_info(self, image_path: str) -> Dict[str, Any]:
        """从文件路径和元数据提取图片信息"""
        try:
            # 获取基本文件信息
            filename = os.path.basename(image_path)
            name_without_ext = os.path.splitext(filename)[0]
            
            # 查找对应的元数据文件
            metadata_path = image_path.replace('.jpg', '_metadata.json')
            
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                return {
                    'id': metadata.get('id', name_without_ext),
                    'category': metadata.get('category', 'unknown'),
                    'title': metadata.get('description', name_without_ext),
                    'tags': metadata.get('tags', []),
                    'author': metadata.get('author', 'Unknown'),
                    'author_url': metadata.get('author_url', ''),
                    'quality_score': metadata.get('quality_score', 0),
                    'width': metadata.get('width', 0),
                    'height': metadata.get('height', 0),
                    'query_used': metadata.get('query_used', ''),
                    'platform': 'pixabay'
                }
            else:
                logger.warning(f"No metadata found for {filename}")
                # 从文件名解析基本信息
                parts = name_without_ext.split('_')
                category = parts[1] if len(parts) > 1 else 'unknown'
                image_id = parts[2] if len(parts) > 2 else name_without_ext
                
                return {
                    'id': image_id,
                    'category': category,
                    'title': f"{category.title()} image {image_id}",
                    'tags': [],
                    'author': 'Unknown',
                    'author_url': '',
                    'quality_score': 0,
                    'width': 0,
                    'height': 0,
                    'query_used': '',
                    'platform': 'pixabay'
                }
                
        except Exception as e:
            logger.error(f"Error extracting info from {image_path}: {e}")
            return {
                'id': os.path.splitext(os.path.basename(image_path))[0],
                'category': 'unknown',
                'title': 'Unknown image',
                'tags': [],
                'author': 'Unknown',
                'author_url': '',
                'quality_score': 0,
                'width': 0,
                'height': 0,
                'query_used': '',
                'platform': 'pixabay'
            }
    
    def remove_background(self, input_path: str, output_path: str) -> bool:
        """移除单张图片的背景"""
        try:
            from rembg import remove
            from PIL import Image
            
            # 读取原图
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()
            
            # 移除背景
            output_data = remove(input_data)
            
            # 保存为PNG
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Error removing background from {input_path}: {e}")
            return False
    
    def process_single_image(self, image_path: str) -> bool:
        """处理单张图片"""
        try:
            # 提取图片信息
            image_info = self.extract_image_info(image_path)
            category = image_info['category']
            image_id = image_info['id']
            
            # 构建输出路径
            output_filename = f"pixabay_{category}_{image_id}.png"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # 检查是否已经处理过
            if os.path.exists(output_path):
                logger.debug(f"⏭️ Skipping already processed: {output_filename}")
                self.stats['skipped'] += 1
                return True
            
            # 移除背景
            logger.info(f"🔄 Processing: {os.path.basename(image_path)} -> {output_filename}")
            
            if self.remove_background(image_path, output_path):
                # 复制原图到备份目录
                backup_filename = f"pixabay_{category}_{image_id}.jpg"
                backup_path = os.path.join(self.processed_dir, backup_filename)
                
                import shutil
                shutil.copy2(image_path, backup_path)
                
                # 保存处理后的元数据
                processed_metadata = image_info.copy()
                processed_metadata.update({
                    'processed_date': datetime.now().isoformat(),
                    'output_file': output_filename,
                    'background_removed': True,
                    'file_format': 'PNG',
                    'transparency_added': True
                })
                
                metadata_output_path = output_path.replace('.png', '_metadata.json')
                with open(metadata_output_path, 'w', encoding='utf-8') as f:
                    json.dump(processed_metadata, f, indent=2, ensure_ascii=False)
                
                self.stats['succeeded'] += 1
                self.stats['category_stats'][category] += 1
                
                logger.info(f"✅ Successfully processed: {output_filename}")
                return True
            else:
                self.stats['failed'] += 1
                logger.error(f"❌ Failed to process: {os.path.basename(image_path)}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception processing {image_path}: {e}")
            self.stats['failed'] += 1
            return False
    
    def run_batch_processing(self) -> Dict[str, Any]:
        """执行批量处理"""
        logger.info("🚀 Starting massive background removal processing")
        
        # 获取所有图片文件
        image_files = self.get_image_files()
        
        if not image_files:
            logger.warning("❌ No images found to process")
            return self.generate_report()
        
        logger.info(f"📊 Processing {len(image_files)} images...")
        
        # 处理每张图片
        for i, image_path in enumerate(image_files, 1):
            self.stats['processed'] += 1
            
            logger.info(f"\n🖼️ [{i}/{len(image_files)}] Processing: {os.path.basename(image_path)}")
            
            success = self.process_single_image(image_path)
            
            # 每50张图片输出进度报告
            if i % 50 == 0:
                elapsed = datetime.now() - self.stats['start_time']
                rate = i / elapsed.total_seconds() * 60  # 每分钟处理数
                eta_minutes = (len(image_files) - i) / rate if rate > 0 else 0
                
                logger.info(f"""
🔄 Progress Report - {i}/{len(image_files)} processed
✅ Succeeded: {self.stats['succeeded']} | ❌ Failed: {self.stats['failed']} | ⏭️ Skipped: {self.stats['skipped']}
⏱️ Speed: {rate:.1f} images/min | ETA: {eta_minutes:.1f} minutes
📊 Categories: {dict(self.stats['category_stats'])}
                """)
            
            # 短暂休息避免系统过载
            time.sleep(0.1)
        
        return self.generate_report()
    
    def generate_report(self) -> Dict[str, Any]:
        """生成处理报告"""
        end_time = datetime.now()
        total_duration = end_time - self.stats['start_time']
        
        report = {
            'summary': {
                'total_found': self.stats['total_found'],
                'total_processed': self.stats['processed'],
                'succeeded': self.stats['succeeded'],
                'failed': self.stats['failed'],
                'skipped': self.stats['skipped'],
                'success_rate': f"{self.stats['succeeded'] / max(1, self.stats['processed']) * 100:.1f}%",
                'duration': str(total_duration),
                'processing_speed': f"{self.stats['succeeded'] / total_duration.total_seconds() * 60:.1f} images/min"
            },
            'category_distribution': dict(self.stats['category_stats']),
            'output_locations': {
                'processed_pngs': self.output_dir,
                'backup_jpgs': self.processed_dir,
                'metadata_files': f"{self.output_dir}/*_metadata.json"
            },
            'metadata': {
                'start_time': self.stats['start_time'].isoformat(),
                'end_time': end_time.isoformat(),
                'rembg_used': True,
                'output_format': 'PNG with transparency'
            }
        }
        
        # 保存报告
        report_file = f"logs/background_removal_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"""
🎉 BACKGROUND REMOVAL COMPLETED! 🎉

📊 Final Statistics:
• Total images found: {self.stats['total_found']}
• Successfully processed: {self.stats['succeeded']}
• Failed: {self.stats['failed']}
• Skipped (already done): {self.stats['skipped']}
• Success rate: {self.stats['succeeded'] / max(1, self.stats['processed']) * 100:.1f}%
• Total duration: {total_duration}
• Processing speed: {self.stats['succeeded'] / total_duration.total_seconds() * 60:.1f} images/min

📁 Category distribution:
{chr(10).join(f'• {cat}: {count} images' for cat, count in self.stats['category_stats'].items())}

📄 Output locations:
• PNG files: {self.output_dir}
• Backup JPGs: {self.processed_dir}
• Report: {report_file}
        """)
        
        return report


def main():
    """主函数"""
    try:
        processor = MassiveBackgroundRemover()
        report = processor.run_batch_processing()
        
        # 输出JSON格式的报告
        print("\n" + "="*50)
        print("BACKGROUND REMOVAL REPORT JSON:")
        print("="*50)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        
    except KeyboardInterrupt:
        logger.info("⏹️ Processing interrupted by user")
    except Exception as e:
        logger.error(f"💥 Critical error: {e}")
        raise


if __name__ == "__main__":
    main()