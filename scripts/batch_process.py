#!/usr/bin/env python3
"""
分批处理剩余图片，避免超时
"""

import os
import logging
import time
from pathlib import Path
import shutil

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_remaining_files():
    """获取还未处理的图片文件"""
    input_dir = 'public/images'
    output_dir = 'public/images_png'
    
    all_jpg_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    
    if not os.path.exists(output_dir):
        return all_jpg_files
    
    processed_png_files = set()
    for f in os.listdir(output_dir):
        if f.lower().endswith('.png'):
            # 转换回JPG文件名
            jpg_name = f.replace('.png', '.jpg')
            processed_png_files.add(jpg_name)
    
    remaining = [f for f in all_jpg_files if f not in processed_png_files]
    return remaining

def process_batch(batch_files, batch_num):
    """处理一批文件"""
    batch_size = len(batch_files)
    logger.info(f"开始处理第 {batch_num} 批，共 {batch_size} 张图片")
    
    # 创建临时目录
    temp_input = f'public/temp_batch_{batch_num}'
    temp_output = f'public/temp_batch_{batch_num}_png'
    
    os.makedirs(temp_input, exist_ok=True)
    os.makedirs(temp_output, exist_ok=True)
    
    # 复制文件到临时目录
    for filename in batch_files:
        src = os.path.join('public/images', filename)
        dst = os.path.join(temp_input, filename)
        shutil.copy2(src, dst)
    
    # 调用处理脚本
    cmd = f'python3 scripts/remove_backgrounds_fast.py --input {temp_input} --output {temp_output} --workers 4'
    result = os.system(cmd)
    
    if result == 0:
        # 移动处理完的文件到主目录
        main_output = 'public/images_png'
        os.makedirs(main_output, exist_ok=True)
        
        moved_count = 0
        for png_file in os.listdir(temp_output):
            if png_file.endswith('.png'):
                src = os.path.join(temp_output, png_file)
                dst = os.path.join(main_output, png_file)
                shutil.move(src, dst)
                moved_count += 1
        
        logger.info(f"✅ 第 {batch_num} 批完成，移动了 {moved_count} 张PNG图片")
        
        # 清理临时目录
        shutil.rmtree(temp_input, ignore_errors=True)
        shutil.rmtree(temp_output, ignore_errors=True)
        
        return moved_count
    else:
        logger.error(f"❌ 第 {batch_num} 批处理失败")
        return 0

def main():
    """主函数"""
    logger.info("🚀 开始分批处理剩余图片")
    
    remaining_files = get_remaining_files()
    total_remaining = len(remaining_files)
    
    logger.info(f"📊 需要处理的图片: {total_remaining} 张")
    
    if total_remaining == 0:
        logger.info("✅ 所有图片都已处理完成！")
        return
    
    # 每批处理200张
    batch_size = 200
    batch_num = 1
    total_processed = 0
    
    for i in range(0, total_remaining, batch_size):
        batch_files = remaining_files[i:i+batch_size]
        processed_count = process_batch(batch_files, batch_num)
        total_processed += processed_count
        
        logger.info(f"📈 总进度: {total_processed}/{total_remaining} ({total_processed/total_remaining*100:.1f}%)")
        
        batch_num += 1
        
        # 短暂休息
        time.sleep(2)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"🎉 分批处理完成！")
    logger.info(f"  总处理: {total_processed} 张")
    logger.info(f"  剩余: {total_remaining - total_processed} 张")
    logger.info(f"{'='*60}")
    
    # 最终统计
    final_count = len([f for f in os.listdir('public/images_png') if f.endswith('.png')])
    logger.info(f"📊 public/images_png 目录中共有 {final_count} 张PNG图片")

if __name__ == '__main__':
    main()