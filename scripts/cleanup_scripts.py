#!/usr/bin/env python3
"""
清理无用的脚本文件
"""

import os
import shutil
from datetime import datetime

# 需要保留的核心脚本
KEEP_SCRIPTS = [
    # 数据库相关
    'migrate_to_sqlite.py',
    'clean_and_update_db.py',
    
    # 图片获取
    'fetch_tagged_images.py',
    
    # 标题和标签
    'generate_better_titles.py',
    'verify_tags.py',
    
    # 本地图片设置
    'setup_local_images.py',
    'restore_r2_urls.py',
    
    # 清理脚本本身
    'cleanup_scripts.py'
]

# 分类脚本
SCRIPT_CATEGORIES = {
    'database': ['migrate_to_sqlite.py', 'clean_and_update_db.py'],
    'image_fetch': ['fetch_tagged_images.py', 'daily_fetch_images.py'],
    'tags': ['generate_better_titles.py', 'verify_tags.py', 'generate_image_tags.py'],
    'r2_related': ['upload_to_r2_simple.py', 'rebuild_r2_storage.py', 'restore_r2_urls.py'],
    'local_setup': ['setup_local_images.py'],
    'testing': ['test_pixabay_api.py', 'test_apis.py'],
    'old_download': ['massive_pixabay_downloader.py', 'simple_massive_downloader.py'],
    'utilities': ['quick_start_tags.sh', 'cleanup_scripts.py']
}

def analyze_scripts():
    """分析所有脚本"""
    scripts_dir = 'scripts'
    all_scripts = []
    
    # 获取所有脚本文件
    for file in os.listdir(scripts_dir):
        if file.endswith(('.py', '.sh')):
            all_scripts.append(file)
    
    all_scripts.sort()
    
    print(f"📊 脚本分析报告")
    print(f"=" * 60)
    print(f"总脚本数: {len(all_scripts)}")
    print(f"建议保留: {len(KEEP_SCRIPTS)}")
    print(f"建议删除: {len(all_scripts) - len(KEEP_SCRIPTS)}")
    print()
    
    # 按类别显示
    print("📁 按功能分类:")
    for category, scripts in SCRIPT_CATEGORIES.items():
        existing = [s for s in scripts if s in all_scripts]
        if existing:
            print(f"\n{category}:")
            for script in existing:
                status = "✅ 保留" if script in KEEP_SCRIPTS else "❌ 删除"
                print(f"  {status} {script}")
    
    # 未分类的脚本
    categorized = set()
    for scripts in SCRIPT_CATEGORIES.values():
        categorized.update(scripts)
    
    uncategorized = [s for s in all_scripts if s not in categorized]
    if uncategorized:
        print(f"\n未分类脚本:")
        for script in uncategorized:
            status = "✅ 保留" if script in KEEP_SCRIPTS else "❌ 删除"
            print(f"  {status} {script}")
    
    return all_scripts

def create_archive():
    """创建归档目录"""
    archive_dir = f'scripts_archive_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    os.makedirs(archive_dir, exist_ok=True)
    return archive_dir

def cleanup_scripts(dry_run=True):
    """清理脚本"""
    all_scripts = analyze_scripts()
    
    # 创建归档目录
    archive_dir = create_archive()
    
    to_delete = [s for s in all_scripts if s not in KEEP_SCRIPTS]
    
    print(f"\n🗑️ 准备删除 {len(to_delete)} 个脚本")
    
    if dry_run:
        print("\n⚠️ 试运行模式 - 不会实际删除文件")
        print("\n将删除的脚本:")
        for script in to_delete[:20]:  # 显示前20个
            print(f"  - {script}")
        if len(to_delete) > 20:
            print(f"  ... 还有 {len(to_delete) - 20} 个")
    else:
        print(f"\n📦 归档脚本到: {archive_dir}")
        
        moved_count = 0
        for script in to_delete:
            src = os.path.join('scripts', script)
            dst = os.path.join(archive_dir, script)
            try:
                shutil.move(src, dst)
                moved_count += 1
                print(f"  ✅ 归档: {script}")
            except Exception as e:
                print(f"  ❌ 失败: {script} - {e}")
        
        print(f"\n✅ 成功归档 {moved_count} 个脚本")
        
        # 创建README
        with open(os.path.join(archive_dir, 'README.md'), 'w') as f:
            f.write(f"# 归档的脚本\n\n")
            f.write(f"归档时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"归档数量: {moved_count}\n\n")
            f.write("这些脚本已不再需要，但保留作为参考。\n")
    
    # 显示保留的脚本
    print(f"\n✅ 保留的核心脚本 ({len(KEEP_SCRIPTS)}):")
    for script in KEEP_SCRIPTS:
        if os.path.exists(os.path.join('scripts', script)):
            print(f"  - {script}")

def main():
    import sys
    
    if '--run' in sys.argv:
        print("🧹 开始清理脚本...")
        cleanup_scripts(dry_run=False)
    else:
        print("🔍 分析模式（试运行）")
        cleanup_scripts(dry_run=True)
        print("\n💡 要实际清理，请运行: python3 scripts/cleanup_scripts.py --run")

if __name__ == '__main__':
    main()