#!/usr/bin/env python3
"""
快速批量去除图片背景 - 使用多进程并行处理
"""

import os
import logging
from pathlib import Path
from multiprocessing import Pool, cpu_count
import sqlite3
from datetime import datetime
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 全局变量，避免重复加载模型
rembg_session = None

def init_worker():
    """初始化工作进程，加载模型"""
    global rembg_session
    from rembg import new_session
    rembg_session = new_session()

def process_single_image(args):
    """处理单张图片（用于多进程）"""
    input_path, output_path = args
    
    try:
        from rembg import remove
        from PIL import Image
        import numpy as np
        
        # 如果输出文件已存在，跳过
        if os.path.exists(output_path):
            return True, "skipped"
        
        # 读取图片
        input_img = Image.open(input_path)
        
        # 去除背景
        output_img = remove(input_img, session=rembg_session)
        
        # 保存为优化的PNG
        output_img.save(output_path, 'PNG', optimize=True)
        
        return True, "success"
        
    except Exception as e:
        return False, str(e)

def remove_backgrounds_parallel(input_dir='public/images', output_dir='public/images_png', num_workers=None):
    """并行批量去除背景"""
    
    # 检查rembg
    try:
        import rembg
        from PIL import Image
    except ImportError:
        logger.error("❌ 请先安装依赖: pip install rembg[gpu] pillow")
        return
    
    logger.info("🚀 开始快速批量去背景处理")
    logger.info(f"输入目录: {input_dir}")
    logger.info(f"输出目录: {output_dir}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有JPG图片
    all_files = []
    for f in os.listdir(input_dir):
        if f.lower().endswith(('.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, f)
            output_filename = f.replace('.jpg', '.png').replace('.jpeg', '.png')
            output_path = os.path.join(output_dir, output_filename)
            all_files.append((input_path, output_path))
    
    total_files = len(all_files)
    
    if total_files == 0:
        logger.error("❌ 没有找到JPG图片")
        return
    
    logger.info(f"📊 找到 {total_files} 张图片需要处理")
    
    # 确定工作进程数
    if num_workers is None:
        num_workers = min(cpu_count(), 8)  # 最多使用8个进程
    
    logger.info(f"⚡ 使用 {num_workers} 个进程并行处理")
    logger.info("⏳ 首次运行需要下载AI模型，请耐心等待...")
    
    start_time = datetime.now()
    
    # 创建进程池并处理
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    with Pool(processes=num_workers, initializer=init_worker) as pool:
        # 简单进度显示
        processed = 0
        for result, status in pool.imap_unordered(process_single_image, all_files):
            if result:
                if status == "skipped":
                    skip_count += 1
                else:
                    success_count += 1
            else:
                fail_count += 1
                logger.error(f"处理失败: {status}")
            
            processed += 1
            if processed % 100 == 0:
                progress = processed / total_files * 100
                logger.info(f"进度: {processed}/{total_files} ({progress:.1f}%) - 成功: {success_count}, 跳过: {skip_count}, 失败: {fail_count}")
    
    # 计算耗时
    elapsed = datetime.now() - start_time
    
    # 最终报告
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 去背景处理完成报告:")
    logger.info(f"  总图片数: {total_files}")
    logger.info(f"  成功处理: {success_count}")
    logger.info(f"  跳过已存在: {skip_count}")
    logger.info(f"  处理失败: {fail_count}")
    logger.info(f"  总耗时: {elapsed}")
    logger.info(f"  平均速度: {total_files / elapsed.total_seconds():.1f} 张/秒")
    logger.info(f"  输出目录: {output_dir}")
    logger.info(f"{'='*60}")
    
    if success_count > 0:
        logger.info("\n✅ 背景去除完成！")
        logger.info("\n💡 下一步操作:")
        logger.info("   1. 检查PNG图片质量: ls -lh public/images_png/ | head")
        logger.info("   2. 更新数据库: python3 scripts/remove_backgrounds_fast.py --update-db")
        logger.info("   3. 切换图片目录:")
        logger.info("      mv public/images public/images_jpg_backup")
        logger.info("      mv public/images_png public/images")

def update_database_urls():
    """更新数据库中的图片URL为PNG格式"""
    logger.info("📝 更新数据库URL...")
    
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    
    # 更新所有URL为PNG格式
    cursor.execute("""
        UPDATE images 
        SET url_thumbnail = REPLACE(url_thumbnail, '.jpg', '.png'),
            url_regular = REPLACE(url_regular, '.jpg', '.png')
        WHERE url_thumbnail LIKE '%.jpg'
    """)
    
    updated = cursor.rowcount
    conn.commit()
    conn.close()
    
    logger.info(f"✅ 更新了 {updated} 条数据库记录")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='快速批量去除图片背景')
    parser.add_argument('--input', default='public/images', help='输入目录')
    parser.add_argument('--output', default='public/images_png', help='输出目录')
    parser.add_argument('--workers', type=int, help='并行进程数（默认自动）')
    parser.add_argument('--update-db', action='store_true', help='只更新数据库URL')
    parser.add_argument('--limit', type=int, help='限制处理数量（用于测试）')
    
    args = parser.parse_args()
    
    if args.update_db:
        update_database_urls()
        return
    
    if args.limit:
        # 限制处理数量
        logger.info(f"⚠️ 限制模式：只处理前 {args.limit} 张图片")
        import shutil
        temp_dir = f'public/temp_images_{args.limit}'
        os.makedirs(temp_dir, exist_ok=True)
        
        files = [f for f in os.listdir(args.input) if f.lower().endswith(('.jpg', '.jpeg'))][:args.limit]
        for f in files:
            shutil.copy2(os.path.join(args.input, f), os.path.join(temp_dir, f))
        
        remove_backgrounds_parallel(temp_dir, f'{args.output}_{args.limit}', args.workers)
    else:
        remove_backgrounds_parallel(args.input, args.output, args.workers)

if __name__ == '__main__':
    main()