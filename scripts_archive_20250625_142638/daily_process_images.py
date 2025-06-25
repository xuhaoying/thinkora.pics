#!/usr/bin/env python3
"""
每日自动处理图片脚本
自动移除背景并生成透明PNG
"""

import os
import json
import logging
from datetime import datetime
from PIL import Image
import numpy as np
from rembg import remove, new_session
import shutil
from typing import List, Dict, Any
import concurrent.futures
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/daily_process_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        # 创建必要的目录
        os.makedirs('png', exist_ok=True)
        os.makedirs('png/unsplash', exist_ok=True)
        os.makedirs('png/pexels', exist_ok=True)
        os.makedirs('png/pixabay', exist_ok=True)
        os.makedirs('processed_backup', exist_ok=True)
        
        # 初始化rembg会话
        self.rembg_session = new_session('u2net')
        
        # 加载处理记录
        self.processed_images = self.load_processed_records()
    
    def load_processed_records(self) -> set:
        """加载已处理的图片记录"""
        processed_file = 'processed_images.json'
        if os.path.exists(processed_file):
            with open(processed_file, 'r') as f:
                data = json.load(f)
                return set(data.get('processed', []))
        return set()
    
    def save_processed_records(self):
        """保存已处理的图片记录"""
        with open('processed_images.json', 'w') as f:
            json.dump({'processed': list(self.processed_images)}, f, indent=2)
    
    def calculate_transparency_ratio(self, image: Image.Image) -> float:
        """计算透明像素比例"""
        if image.mode != 'RGBA':
            return 0.0
        
        arr = np.array(image)
        transparent_pixels = np.sum(arr[:, :, 3] == 0)
        total_pixels = arr.shape[0] * arr.shape[1]
        
        return transparent_pixels / total_pixels if total_pixels > 0 else 0
    
    def evaluate_image_quality(self, image: Image.Image, transparency_ratio: float) -> Dict[str, Any]:
        """评估图片质量"""
        quality_score = 0
        reasons = []
        
        # 透明度评分
        if transparency_ratio > 0.3:
            quality_score += 40
            reasons.append("Good transparency ratio")
        elif transparency_ratio > 0.1:
            quality_score += 20
            reasons.append("Moderate transparency ratio")
        
        # 尺寸评分
        width, height = image.size
        if width >= 1000 and height >= 1000:
            quality_score += 30
            reasons.append("High resolution")
        elif width >= 600 and height >= 600:
            quality_score += 15
            reasons.append("Medium resolution")
        
        # 宽高比评分
        aspect_ratio = width / height
        if 0.8 <= aspect_ratio <= 1.2:
            quality_score += 20
            reasons.append("Good aspect ratio")
        elif 0.5 <= aspect_ratio <= 2.0:
            quality_score += 10
            reasons.append("Acceptable aspect ratio")
        
        # 主体检测（简单版本）
        arr = np.array(image)
        if image.mode == 'RGBA':
            # 检查主体是否居中
            alpha = arr[:, :, 3]
            rows = np.any(alpha > 0, axis=1)
            cols = np.any(alpha > 0, axis=0)
            rmin, rmax = np.where(rows)[0][[0, -1]]
            cmin, cmax = np.where(cols)[0][[0, -1]]
            
            center_y = (rmin + rmax) / 2
            center_x = (cmin + cmax) / 2
            img_center_y = height / 2
            img_center_x = width / 2
            
            offset_y = abs(center_y - img_center_y) / height
            offset_x = abs(center_x - img_center_x) / width
            
            if offset_y < 0.1 and offset_x < 0.1:
                quality_score += 10
                reasons.append("Well-centered subject")
        
        return {
            'score': quality_score,
            'reasons': reasons,
            'transparency_ratio': transparency_ratio,
            'dimensions': f"{width}x{height}",
            'aspect_ratio': round(aspect_ratio, 2)
        }
    
    def process_single_image(self, input_path: str, output_path: str, metadata_path: str) -> Dict[str, Any]:
        """处理单张图片"""
        try:
            # 读取原始图片
            input_image = Image.open(input_path)
            
            # 移除背景
            logger.info(f"Removing background from {os.path.basename(input_path)}")
            output_image = remove(input_image, session=self.rembg_session)
            
            # 计算透明度比例
            transparency_ratio = self.calculate_transparency_ratio(output_image)
            
            # 评估质量
            quality_info = self.evaluate_image_quality(output_image, transparency_ratio)
            
            # 只保存质量分数超过阈值的图片
            if quality_info['score'] >= 50:
                # 保存PNG
                output_image.save(output_path, 'PNG', optimize=True)
                
                # 读取原始元数据
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        original_metadata = json.load(f)
                else:
                    original_metadata = {}
                
                # 更新元数据
                processed_metadata = {
                    **original_metadata,
                    'processed': True,
                    'processed_date': datetime.now().isoformat(),
                    'transparency_ratio': transparency_ratio,
                    'quality_score': quality_info['score'],
                    'quality_reasons': quality_info['reasons'],
                    'dimensions': quality_info['dimensions'],
                    'aspect_ratio': quality_info['aspect_ratio'],
                    'file_size': os.path.getsize(output_path)
                }
                
                # 保存处理后的元数据
                output_metadata_path = output_path.replace('.png', '_metadata.json')
                with open(output_metadata_path, 'w') as f:
                    json.dump(processed_metadata, f, indent=2)
                
                # 备份原始文件
                backup_path = input_path.replace('raw/', 'processed_backup/')
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.move(input_path, backup_path)
                
                logger.info(f"Processed successfully: {os.path.basename(output_path)} (Score: {quality_info['score']})")
                return {
                    'status': 'success',
                    'quality_score': quality_info['score'],
                    'transparency_ratio': transparency_ratio
                }
            else:
                logger.warning(f"Image quality too low: {os.path.basename(input_path)} (Score: {quality_info['score']})")
                return {
                    'status': 'low_quality',
                    'quality_score': quality_info['score'],
                    'transparency_ratio': transparency_ratio
                }
                
        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_unprocessed_images(self) -> List[Dict[str, str]]:
        """获取未处理的图片列表"""
        unprocessed = []
        
        for platform in ['unsplash', 'pexels', 'pixabay']:
            raw_dir = os.path.join('raw', platform)
            if not os.path.exists(raw_dir):
                continue
            
            for filename in os.listdir(raw_dir):
                if filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    image_id = filename.replace('.jpg', '').replace('.jpeg', '')
                    
                    if image_id not in self.processed_images:
                        input_path = os.path.join(raw_dir, filename)
                        output_filename = filename.replace('.jpg', '.png').replace('.jpeg', '.png')
                        output_path = os.path.join('png', platform, output_filename)
                        metadata_path = input_path.replace('.jpg', '_metadata.json').replace('.jpeg', '_metadata.json')
                        
                        unprocessed.append({
                            'id': image_id,
                            'platform': platform,
                            'input_path': input_path,
                            'output_path': output_path,
                            'metadata_path': metadata_path
                        })
        
        return unprocessed
    
    def run_daily_processing(self, max_workers: int = 4):
        """执行每日处理任务"""
        logger.info("Starting daily image processing")
        
        # 获取未处理的图片
        unprocessed_images = self.get_unprocessed_images()
        logger.info(f"Found {len(unprocessed_images)} unprocessed images")
        
        if not unprocessed_images:
            logger.info("No new images to process")
            return
        
        # 处理统计
        results = {
            'total': len(unprocessed_images),
            'success': 0,
            'low_quality': 0,
            'error': 0,
            'processed_images': []
        }
        
        # 使用线程池并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_image = {
                executor.submit(
                    self.process_single_image,
                    img['input_path'],
                    img['output_path'],
                    img['metadata_path']
                ): img for img in unprocessed_images
            }
            
            for future in concurrent.futures.as_completed(future_to_image):
                image_info = future_to_image[future]
                try:
                    result = future.result()
                    
                    if result['status'] == 'success':
                        results['success'] += 1
                        self.processed_images.add(image_info['id'])
                        results['processed_images'].append({
                            'id': image_info['id'],
                            'platform': image_info['platform'],
                            'quality_score': result['quality_score'],
                            'transparency_ratio': result['transparency_ratio']
                        })
                    elif result['status'] == 'low_quality':
                        results['low_quality'] += 1
                        self.processed_images.add(image_info['id'])  # 也标记为已处理
                    else:
                        results['error'] += 1
                        
                except Exception as e:
                    logger.error(f"Error in thread: {e}")
                    results['error'] += 1
        
        # 保存处理记录
        self.save_processed_records()
        
        # 生成处理报告
        report = {
            'date': datetime.now().isoformat(),
            'total_processed': results['total'],
            'successful': results['success'],
            'low_quality': results['low_quality'],
            'errors': results['error'],
            'success_rate': round(results['success'] / results['total'] * 100, 2) if results['total'] > 0 else 0,
            'processed_images': results['processed_images']
        }
        
        # 保存报告
        report_file = f"logs/process_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Daily processing completed. Success: {results['success']}, Low quality: {results['low_quality']}, Errors: {results['error']}")
        return report


if __name__ == "__main__":
    processor = ImageProcessor()
    report = processor.run_daily_processing(max_workers=4)
    print(json.dumps(report, indent=2))