#!/usr/bin/env python3
"""
恢复R2 URL - 当图片上传到R2后使用此脚本
"""

import sqlite3
import json
import os
from datetime import datetime

def restore_r2_urls(r2_base_url="https://r2.thinkora.pics"):
    """恢复数据库和metadata.json中的R2 URL"""
    
    print("🔄 恢复R2 URL...")
    
    # 1. 更新数据库
    print("📝 更新数据库...")
    # 检查是否存在thinkora.db，如果不存在，使用images.db
    db_file = 'thinkora.db' if os.path.exists('thinkora.db') else 'images.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE images 
        SET url_thumbnail = ? || '/images/' || id || '.png',
            url_regular = ? || '/images/' || id || '.png',
            url_download = ? || '/images/' || id || '.png'
        WHERE tags != '[]'
    """, (r2_base_url, r2_base_url, r2_base_url))
    
    updated_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"✅ 更新了 {updated_count} 条数据库记录")
    
    # 2. 更新metadata.json（如果存在）
    if os.path.exists('metadata.json'):
        print("\n📝 更新metadata.json...")
        with open('metadata.json', 'r') as f:
            metadata = json.load(f)
        
        # 检查metadata的结构
        if isinstance(metadata, dict) and 'images' in metadata:
            metadata['lastUpdated'] = datetime.now().isoformat()
            for image in metadata['images']:
                image_id = image['id']
                r2_url = f'{r2_base_url}/images/{image_id}.png'
                image['urls'] = {
                    'thumbnail': r2_url,
                    'regular': r2_url,
                    'download': r2_url
                }
            
            with open('metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print("✅ metadata.json已更新")
        else:
            print("⚠️ metadata.json格式不正确，跳过更新")
    
    # 3. 创建确认文件
    with open('r2_restore_log.txt', 'w') as f:
        f.write(f"R2 URL恢复日志\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"基础URL: {r2_base_url}\n")
        f.write(f"更新记录数: {updated_count}\n")
    
    print("\n✅ R2 URL恢复完成！")
    print(f"   基础URL: {r2_base_url}")
    print(f"   示例: {r2_base_url}/images/pixabay_1478822.jpg")
    print("\n⚠️ 注意：")
    print("   1. 确保图片已上传到R2的images/目录")
    print("   2. 确保R2存储桶已设置为公开访问")
    print("   3. 如果使用自定义域名，请相应修改基础URL")

def main():
    import sys
    
    if len(sys.argv) > 1:
        # 支持自定义R2 URL
        r2_base_url = sys.argv[1]
        print(f"使用自定义R2 URL: {r2_base_url}")
        restore_r2_urls(r2_base_url)
    else:
        # 使用默认URL
        restore_r2_urls()

if __name__ == '__main__':
    main()