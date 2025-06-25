#!/usr/bin/env python3
"""
批量去除图片背景
使用 rembg 库进行背景去除
"""

import os
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_rembg():
    """安装和配置rembg"""
    try:
        import rembg
        return True
    except ImportError:
        logger.error("❌ rembg未安装，请先运行: pip install rembg pillow")
        logger.info("💡 建议使用: pip install rembg[gpu] 以获得更好的性能")
        return False

def remove_background_single(input_path: str, output_path: str) -> bool:
    """去除单张图片的背景"""
    try:
        from rembg import remove
        from PIL import Image
        
        # 读取图片
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
        
        # 去除背景
        output_data = remove(input_data)
        
        # 保存为PNG（支持透明度）
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        # 优化文件大小
        img = Image.open(output_path)
        img.save(output_path, 'PNG', optimize=True)
        
        return True
        
    except Exception as e:
        logger.error(f"处理失败 {input_path}: {e}")
        return False

def process_batch(file_batch: list, input_dir: str, output_dir: str) -> dict:
    """处理一批图片"""
    results = {'success': 0, 'failed': 0}
    
    for filename in file_batch:
        input_path = os.path.join(input_dir, filename)
        # 改为PNG格式
        output_filename = filename.replace('.jpg', '.png').replace('.jpeg', '.png')
        output_path = os.path.join(output_dir, output_filename)
        
        if os.path.exists(output_path):
            logger.debug(f"跳过已存在: {output_filename}")
            results['success'] += 1
            continue
        
        if remove_background_single(input_path, output_path):
            results['success'] += 1
            logger.debug(f"✅ 完成: {filename} -> {output_filename}")
        else:
            results['failed'] += 1
    
    return results

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

def remove_backgrounds_batch(input_dir='public/images', output_dir='public/images_png', max_workers=4):
    """批量去除背景的主函数"""
    
    # 检查rembg
    if not setup_rembg():
        return
    
    logger.info("🚀 开始批量去背景处理")
    logger.info(f"输入目录: {input_dir}")
    logger.info(f"输出目录: {output_dir}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有JPG图片
    all_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    total_files = len(all_files)
    
    if total_files == 0:
        logger.error("❌ 没有找到JPG图片")
        return
    
    logger.info(f"📊 找到 {total_files} 张图片需要处理")
    
    # 分批处理
    batch_size = 50
    processed = 0
    total_success = 0
    total_failed = 0
    
    # 首次运行时导入rembg模型
    logger.info("⏳ 首次运行需要下载AI模型（约150MB），请耐心等待...")
    
    start_time = datetime.now()
    
    for i in range(0, total_files, batch_size):
        batch = all_files[i:i+batch_size]
        results = process_batch(batch, input_dir, output_dir)
        
        total_success += results['success']
        total_failed += results['failed']
        processed += len(batch)
        
        # 显示进度
        progress = processed / total_files * 100
        logger.info(f"进度: {processed}/{total_files} ({progress:.1f}%) - 成功: {total_success}, 失败: {total_failed}")
    
    # 计算耗时
    elapsed = datetime.now() - start_time
    
    # 最终报告
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 去背景处理完成报告:")
    logger.info(f"  总图片数: {total_files}")
    logger.info(f"  成功: {total_success}")
    logger.info(f"  失败: {total_failed}")
    logger.info(f"  耗时: {elapsed}")
    logger.info(f"  输出目录: {output_dir}")
    logger.info(f"{'='*60}")
    
    # 询问是否更新数据库
    if total_success > 0:
        logger.info("\n✅ 背景去除完成！")
        logger.info("\n💡 下一步操作:")
        logger.info("   1. 检查PNG图片质量")
        logger.info("   2. 运行: python3 scripts/remove_backgrounds.py --update-db")
        logger.info("   3. 备份并替换图片目录:")
        logger.info("      mv public/images public/images_jpg_backup")
        logger.info("      mv public/images_png public/images")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='批量去除图片背景')
    parser.add_argument('--input', default='public/images', help='输入目录')
    parser.add_argument('--output', default='public/images_png', help='输出目录')
    parser.add_argument('--workers', type=int, default=4, help='并行处理数')
    parser.add_argument('--test', action='store_true', help='测试模式，只处理前10张')
    parser.add_argument('--update-db', action='store_true', help='只更新数据库URL')
    
    args = parser.parse_args()
    
    if args.update_db:
        # 只更新数据库
        update_database_urls()
        return
    
    if args.test:
        # 测试模式
        logger.info("🧪 测试模式：只处理前10张图片")
        test_dir = 'public/test_images'
        os.makedirs(test_dir, exist_ok=True)
        
        # 复制前10张图片到测试目录
        import shutil
        files = [f for f in os.listdir(args.input) if f.lower().endswith(('.jpg', '.jpeg'))][:10]
        for f in files:
            shutil.copy2(os.path.join(args.input, f), os.path.join(test_dir, f))
        
        remove_backgrounds_batch(test_dir, 'public/test_images_png', args.workers)
    else:
        remove_backgrounds_batch(args.input, args.output, args.workers)

if __name__ == '__main__':
    main()