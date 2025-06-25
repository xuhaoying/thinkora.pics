#!/usr/bin/env python3
"""
生成需要从R2删除的图片列表
"""

import sqlite3
import json
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def get_images_to_keep():
    """获取需要保留的图片ID列表"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 获取当前数据库中的所有图片
    cursor.execute("SELECT id, url_download FROM images")
    keep_images = {}
    
    for image_id, url in cursor.fetchall():
        keep_images[image_id] = url
    
    conn.close()
    logger.info(f"📸 数据库中有 {len(keep_images)} 张需要保留的图片")
    return keep_images

def get_deleted_images():
    """获取已删除的图片ID"""
    deleted_ids = set()
    
    # 从删除记录表获取
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM deleted_images")
        deleted_ids = set(row[0] for row in cursor.fetchall())
        logger.info(f"🗑️ 找到 {len(deleted_ids)} 条删除记录")
    except:
        logger.info("⚠️ 没有删除记录表")
    
    conn.close()
    
    # 也可以从备份数据库获取旧图片ID
    if os.path.exists('thinkora_backup_20250624_205530.db'):
        backup_conn = sqlite3.connect('thinkora_backup_20250624_205530.db')
        backup_cursor = backup_conn.cursor()
        
        backup_cursor.execute("SELECT id FROM images WHERE tags = '[]'")
        old_no_tag_ids = set(row[0] for row in backup_cursor.fetchall())
        deleted_ids.update(old_no_tag_ids)
        
        backup_conn.close()
        logger.info(f"📦 从备份中找到 {len(old_no_tag_ids)} 张无标签图片")
    
    return deleted_ids

def analyze_r2_files():
    """分析R2中可能存在的文件"""
    # 已知的旧图片ID模式
    old_patterns = [
        'unsplash_',  # 旧的Unsplash图片
        'pexels_',    # 旧的Pexels图片（如果没有标签）
    ]
    
    # 读取已知的文件列表（如果有）
    known_files = []
    if os.path.exists('uploaded_to_r2.json'):
        with open('uploaded_to_r2.json', 'r') as f:
            r2_data = json.load(f)
            known_files = [item['r2_key'] for item in r2_data.get('uploaded_files', [])]
            logger.info(f"📄 从上传记录中找到 {len(known_files)} 个文件")
    
    return known_files

def generate_delete_commands(keep_images, deleted_ids):
    """生成删除命令"""
    delete_commands = []
    
    # 生成可能需要删除的文件列表
    potential_deletes = []
    
    # 所有被标记为删除的图片
    for image_id in deleted_ids:
        # 可能的文件路径
        potential_paths = [
            f"images/{image_id}.png",
            f"images/{image_id}.jpg",
            f"png/{image_id}.png",
            f"{image_id}.png",
            f"{image_id}.jpg"
        ]
        potential_deletes.extend(potential_paths)
    
    # 生成删除脚本
    delete_script = f"""#!/bin/bash
# R2图片清理脚本
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 删除 {len(deleted_ids)} 张无标签图片

echo "🧹 开始清理R2存储桶..."
echo "将删除 {len(deleted_ids)} 张无标签图片"
echo ""

# R2配置
R2_BUCKET="thinkora-pics"
R2_ENDPOINT="https://d37e2728a4daeb263e7a08a066e80926.r2.cloudflarestorage.com"

# 统计变量
DELETED=0
FAILED=0

# 删除函数
delete_file() {{
    local file_path=$1
    echo -n "删除: $file_path ... "
    
    # 使用aws cli或rclone删除
    # 选项1: 使用aws cli
    # aws s3 rm "s3://$R2_BUCKET/$file_path" --endpoint-url="$R2_ENDPOINT"
    
    # 选项2: 使用rclone（需要配置）
    # rclone delete "r2:$R2_BUCKET/$file_path"
    
    # 选项3: 使用curl（需要签名，较复杂）
    echo "[需要配置删除命令]"
}}

# 删除旧图片
"""
    
    # 添加每个删除命令
    for image_id in sorted(deleted_ids):
        delete_script += f"""
# 删除 {image_id}
for ext in png jpg jpeg; do
    for prefix in "images/" "png/" ""; do
        delete_file "${{prefix}}{image_id}.${{ext}}"
    done
done
"""
    
    delete_script += """
echo ""
echo "✅ 清理完成!"
echo "   成功删除: $DELETED 个文件"
echo "   删除失败: $FAILED 个文件"
"""
    
    # 保存删除脚本
    script_path = 'scripts/r2_delete_commands.sh'
    with open(script_path, 'w') as f:
        f.write(delete_script)
    os.chmod(script_path, 0o755)
    
    # 生成删除清单
    delete_list = {
        'generated_at': datetime.now().isoformat(),
        'total_to_keep': len(keep_images),
        'total_to_delete': len(deleted_ids),
        'delete_ids': list(deleted_ids),
        'potential_paths': potential_deletes[:100]  # 显示前100个
    }
    
    list_path = 'r2_delete_list.json'
    with open(list_path, 'w') as f:
        json.dump(delete_list, f, indent=2)
    
    logger.info(f"\n✅ 已生成删除清单: {list_path}")
    logger.info(f"✅ 已生成删除脚本: {script_path}")
    
    return delete_list

def generate_rclone_commands(deleted_ids):
    """生成rclone批量删除命令"""
    logger.info("\n📝 生成rclone删除命令...")
    
    # 创建要删除的文件列表
    delete_files = []
    for image_id in deleted_ids:
        # 添加所有可能的路径
        delete_files.extend([
            f"images/{image_id}.png",
            f"images/{image_id}.jpg",
            f"png/{image_id}.png",
            f"{image_id}.png",
            f"{image_id}.jpg"
        ])
    
    # 保存到文件
    with open('r2_files_to_delete.txt', 'w') as f:
        for file_path in delete_files:
            f.write(f"{file_path}\n")
    
    # 生成rclone命令
    rclone_script = f"""#!/bin/bash
# 使用rclone批量删除R2文件
# 确保已配置rclone: rclone config

echo "🧹 使用rclone清理R2存储桶..."
echo "将尝试删除 {len(delete_files)} 个文件路径"

# 批量删除（更高效）
rclone delete r2:thinkora-pics --include-from r2_files_to_delete.txt --dry-run

echo ""
echo "⚠️ 以上是试运行结果"
echo "要实际删除，请去掉 --dry-run 参数："
echo "rclone delete r2:thinkora-pics --include-from r2_files_to_delete.txt"
"""
    
    with open('scripts/r2_rclone_delete.sh', 'w') as f:
        f.write(rclone_script)
    os.chmod('scripts/r2_rclone_delete.sh', 0o755)
    
    logger.info(f"✅ 已生成rclone删除脚本: scripts/r2_rclone_delete.sh")
    logger.info(f"✅ 已生成文件列表: r2_files_to_delete.txt")

def main():
    """主函数"""
    logger.info("🔍 分析R2存储桶清理需求...")
    logger.info("=" * 50)
    
    # 1. 获取需要保留的图片
    keep_images = get_images_to_keep()
    
    # 2. 获取已删除的图片
    deleted_ids = get_deleted_images()
    
    # 3. 分析R2文件
    r2_files = analyze_r2_files()
    
    # 4. 生成删除命令
    delete_list = generate_delete_commands(keep_images, deleted_ids)
    
    # 5. 生成rclone命令
    generate_rclone_commands(deleted_ids)
    
    # 显示摘要
    logger.info("\n📊 清理摘要:")
    logger.info(f"  保留图片: {len(keep_images)} 张")
    logger.info(f"  删除图片: {len(deleted_ids)} 张")
    logger.info(f"  删除比例: {len(deleted_ids)/(len(keep_images)+len(deleted_ids))*100:.1f}%")
    
    logger.info("\n🚀 下一步操作:")
    logger.info("1. 安装并配置rclone:")
    logger.info("   brew install rclone")
    logger.info("   rclone config  # 添加R2配置")
    logger.info("\n2. 运行删除脚本:")
    logger.info("   ./scripts/r2_rclone_delete.sh")
    logger.info("\n3. 或者使用AWS CLI:")
    logger.info("   brew install awscli")
    logger.info("   aws configure  # 配置R2凭证")

if __name__ == '__main__':
    main()