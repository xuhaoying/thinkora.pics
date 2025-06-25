#!/usr/bin/env python3
"""
检查背景去除和上传进度
"""

import os
import sqlite3
from pathlib import Path
import subprocess

def check_progress():
    """检查当前进度"""
    print("🔍 检查背景去除和处理进度\n")
    
    # 1. 检查原始JPG图片
    jpg_dir = Path('public/images')
    if jpg_dir.exists():
        jpg_files = list(jpg_dir.glob('*.jpg'))
        print(f"📁 原始JPG图片: {len(jpg_files)} 张")
    else:
        print("📁 原始JPG图片: 目录不存在")
    
    # 2. 检查PNG图片
    png_dir = Path('public/images_png')
    if png_dir.exists():
        png_files = list(png_dir.glob('*.png'))
        print(f"🖼️  透明PNG图片: {len(png_files)} 张")
        
        # 检查总大小
        try:
            result = subprocess.run(['du', '-sh', str(png_dir)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                size = result.stdout.strip().split('\t')[0]
                print(f"💾 PNG图片总大小: {size}")
        except:
            pass
    else:
        print("🖼️  透明PNG图片: 目录不存在")
    
    # 3. 检查数据库
    if os.path.exists('images.db'):
        conn = sqlite3.connect('images.db')
        cursor = conn.cursor()
        
        # 总图片数
        cursor.execute("SELECT COUNT(*) FROM images")
        total_db = cursor.fetchone()[0]
        print(f"🗄️  数据库记录: {total_db} 条")
        
        # PNG格式的记录数
        cursor.execute("SELECT COUNT(*) FROM images WHERE url_regular LIKE '%.png'")
        png_db = cursor.fetchone()[0]
        print(f"📝 PNG格式记录: {png_db} 条")
        
        # 平均标签数
        cursor.execute("SELECT AVG(json_array_length(tags)) FROM images WHERE tags != '[]'")
        avg_tags = cursor.fetchone()[0]
        print(f"🏷️  平均标签数: {avg_tags:.1f}")
        
        conn.close()
    else:
        print("🗄️  数据库: 不存在")
    
    # 4. 检查后台进程
    try:
        result = subprocess.run(['pgrep', '-f', 'batch_process.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"⚙️  后台处理进程: {len(pids)} 个正在运行")
        else:
            print("⚙️  后台处理进程: 无")
    except:
        print("⚙️  后台处理进程: 检查失败")
    
    # 5. 检查处理日志
    if os.path.exists('batch_process.log'):
        try:
            with open('batch_process.log', 'r') as f:
                lines = f.readlines()
                last_lines = lines[-10:]
                print(f"\n📋 最新处理日志 (最后10行):")
                for line in last_lines:
                    print(f"   {line.strip()}")
        except:
            pass
    
    # 6. 计算进度
    if jpg_dir.exists() and png_dir.exists():
        total_jpg = len(list(jpg_dir.glob('*.jpg')))
        total_png = len(list(png_dir.glob('*.png')))
        
        if total_jpg > 0:
            progress = total_png / total_jpg * 100
            print(f"\n📊 背景去除进度: {total_png}/{total_jpg} ({progress:.1f}%)")
            
            if progress < 100:
                remaining = total_jpg - total_png
                print(f"⏳ 剩余待处理: {remaining} 张")
            else:
                print("✅ 背景去除已完成！")
    
    print("\n" + "="*50)

def show_next_steps():
    """显示下一步操作建议"""
    print("💡 下一步操作建议:")
    
    jpg_count = len(list(Path('public/images').glob('*.jpg'))) if Path('public/images').exists() else 0
    png_count = len(list(Path('public/images_png').glob('*.png'))) if Path('public/images_png').exists() else 0
    
    if png_count == 0:
        print("   1. 启动背景去除: python3 scripts/batch_process.py")
        
    elif png_count < jpg_count:
        print("   1. 等待背景去除完成或重启: python3 scripts/batch_process.py")
        print("   2. 监控日志: tail -f batch_process.log")
        
    else:
        print("   1. 切换图片目录:")
        print("      mv public/images public/images_jpg_backup")
        print("      mv public/images_png public/images")
        print("   2. 配置R2环境变量:")
        print("      export R2_ACCESS_KEY_ID=your_key")
        print("      export R2_SECRET_ACCESS_KEY=your_secret")
        print("      export R2_ACCOUNT_ID=your_account_id")
        print("   3. 测试R2连接: python3 scripts/upload_to_r2.py --test")
        print("   4. 上传到R2: python3 scripts/upload_to_r2.py")
        print("   5. 更新数据库: python3 scripts/upload_to_r2.py --update-db")

if __name__ == '__main__':
    check_progress()
    show_next_steps()