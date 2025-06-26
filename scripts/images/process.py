#!/usr/bin/env python3
"""
图片处理脚本 - 下载图片并去除背景，生成透明PNG
"""

import os
import sys
import sqlite3
import requests
import argparse
from pathlib import Path
from PIL import Image
import tempfile
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from rembg import remove, new_session
except ImportError:
    print("❌ 请安装rembg: pip install rembg")
    sys.exit(1)

class ImageProcessor:
    def __init__(self):
        self.db_path = "images.db"
        self.output_dir = Path("processed_images")
        self.output_dir.mkdir(exist_ok=True)
        
        # 初始化rembg session
        try:
            self.rembg_session = new_session('u2net')
        except Exception as e:
            print(f"❌ 初始化rembg失败: {e}")
            self.rembg_session = None
    
    def get_unprocessed_images(self, limit=None):
        """获取未处理的图片"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM images WHERE processed = FALSE"
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        images = cursor.fetchall()
        
        # 获取列名
        columns = [description[0] for description in cursor.description]
        
        conn.close()
        
        # 转换为字典列表
        return [dict(zip(columns, row)) for row in images]
    
    def download_image(self, url, timeout=30):
        """下载图片"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=timeout, stream=True)
            response.raise_for_status()
            
            return response.content
        except Exception as e:
            print(f"❌ 下载失败 {url}: {e}")
            return None
    
    def remove_background(self, image_data):
        """去除图片背景"""
        if not self.rembg_session:
            print("❌ rembg未初始化")
            return None
        
        try:
            # 使用临时文件处理
            with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_input:
                temp_input.write(image_data)
                temp_input.flush()
                
                # 打开图片
                input_image = Image.open(temp_input.name)
                
                # 去除背景
                output_image = remove(input_image, session=self.rembg_session)
                
                return output_image
                
        except Exception as e:
            print(f"❌ 背景去除失败: {e}")
            return None
    
    def process_single_image(self, image_data):
        """处理单张图片"""
        image_id = image_data['id']
        url = image_data['url_regular']
        
        print(f"🔄 处理图片: {image_id}")
        
        try:
            # 下载图片
            raw_data = self.download_image(url)
            if not raw_data:
                return False, "下载失败"
            
            # 去除背景
            processed_image = self.remove_background(raw_data)
            if not processed_image:
                return False, "背景去除失败"
            
            # 保存处理后的图片
            output_path = self.output_dir / f"{image_id}.png"
            processed_image.save(output_path, 'PNG', optimize=True)
            
            # 更新数据库状态
            self.mark_as_processed(image_id, str(output_path))
            
            print(f"✅ 处理完成: {image_id}")
            return True, "成功"
            
        except Exception as e:
            error_msg = f"处理异常: {e}"
            print(f"❌ {image_id}: {error_msg}")
            return False, error_msg
    
    def mark_as_processed(self, image_id, output_path):
        """标记图片为已处理"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE images 
            SET processed = TRUE, 
                processed_at = ?,
                processed_path = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), output_path, image_id))
        
        conn.commit()
        conn.close()
    
    def process_images_batch(self, batch_size=50, max_workers=4):
        """批量处理图片"""
        images = self.get_unprocessed_images(batch_size)
        
        if not images:
            print("📋 没有需要处理的图片")
            return 0
        
        print(f"🚀 开始处理 {len(images)} 张图片...")
        
        success_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交任务
            future_to_image = {
                executor.submit(self.process_single_image, image): image 
                for image in images
            }
            
            # 处理结果
            for future in as_completed(future_to_image):
                image = future_to_image[future]
                try:
                    success, message = future.result()
                    if success:
                        success_count += 1
                except Exception as e:
                    print(f"❌ 处理异常 {image['id']}: {e}")
        
        print(f"✅ 批量处理完成: {success_count}/{len(images)} 成功")
        return success_count
    
    def get_processing_stats(self):
        """获取处理统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM images")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM images WHERE processed = TRUE")
        processed = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM images WHERE uploaded = TRUE")
        uploaded = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'processed': processed,
            'uploaded': uploaded,
            'pending': total - processed
        }

def main():
    parser = argparse.ArgumentParser(description="处理图片（去背景）")
    parser.add_argument("--batch-size", type=int, default=50, help="批处理大小")
    parser.add_argument("--workers", type=int, default=4, help="并发工作线程数")
    parser.add_argument("--stats", action="store_true", help="显示处理统计")
    
    args = parser.parse_args()
    
    processor = ImageProcessor()
    
    if args.stats:
        stats = processor.get_processing_stats()
        print("📊 处理统计:")
        print(f"  总图片数: {stats['total']}")
        print(f"  已处理: {stats['processed']}")
        print(f"  已上传: {stats['uploaded']}")
        print(f"  待处理: {stats['pending']}")
    else:
        processor.process_images_batch(args.batch_size, args.workers)

if __name__ == "__main__":
    main()