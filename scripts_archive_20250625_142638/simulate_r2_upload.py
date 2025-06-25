#!/usr/bin/env python3
"""
模拟上传图片到R2并更新数据库URL
"""

import sqlite3
import json
import os
from datetime import datetime
import shutil

def get_images_with_tags():
    """获取所有带标签的图片"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 获取所有带标签的图片
    query = """
    SELECT id, title, description, author_name, author_url, 
           width, height, aspect_ratio, 
           url_thumbnail, url_regular, url_download, 
           tags, category, quality_score, file_size, 
           transparent_ratio, created_at, 
           unsplash_id, unsplash_url, unsplash_download_location
    FROM images 
    WHERE tags IS NOT NULL 
    AND tags != '[]' 
    AND tags != ''
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    images = []
    for row in rows:
        images.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'author_name': row[3],
            'author_url': row[4],
            'width': row[5],
            'height': row[6],
            'aspect_ratio': row[7],
            'url_thumbnail': row[8],
            'url_regular': row[9],
            'url_download': row[10],
            'tags': row[11],
            'category': row[12],
            'quality_score': row[13],
            'file_size': row[14],
            'transparent_ratio': row[15],
            'created_at': row[16],
            'unsplash_id': row[17],
            'unsplash_url': row[18],
            'unsplash_download_location': row[19]
        })
    
    return images

def find_local_image_file(image_id):
    """查找本地图片文件"""
    # 可能的路径
    possible_paths = [
        f'raw/pixabay/pixabay_{image_id}.jpg',
        f'raw/pixabay/{image_id}.jpg',
        f'raw/{image_id}.jpg',
        f'processed_backup/pixabay/pixabay_{image_id}.jpg',
        f'png/pixabay/pixabay_{image_id}.png',
        f'png/{image_id}.png'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def simulate_upload_to_r2(images):
    """模拟上传到R2"""
    print(f"Found {len(images)} images with tags")
    
    # 创建模拟上传记录
    upload_records = []
    r2_base_url = "https://r2.thinkora.pics/images"
    
    for i, image in enumerate(images):
        image_id = image['id']
        
        # 查找本地文件
        local_file = find_local_image_file(image_id)
        
        if local_file:
            print(f"[{i+1}/{len(images)}] Found local file for {image_id}: {local_file}")
            
            # 构建R2 URL
            r2_url = f"{r2_base_url}/{image_id}.jpg"
            
            upload_records.append({
                'id': image_id,
                'local_path': local_file,
                'r2_url': r2_url,
                'r2_thumbnail': r2_url,
                'r2_regular': r2_url,
                'r2_download': r2_url,
                'uploaded': True,
                'timestamp': datetime.now().isoformat()
            })
        else:
            print(f"[{i+1}/{len(images)}] Warning: No local file found for {image_id}")
            upload_records.append({
                'id': image_id,
                'local_path': None,
                'r2_url': f"{r2_base_url}/{image_id}.jpg",
                'r2_thumbnail': f"{r2_base_url}/{image_id}.jpg",
                'r2_regular': f"{r2_base_url}/{image_id}.jpg",
                'r2_download': f"{r2_base_url}/{image_id}.jpg",
                'uploaded': False,
                'timestamp': datetime.now().isoformat()
            })
    
    # 保存上传记录
    with open('simulated_r2_upload.json', 'w') as f:
        json.dump(upload_records, f, indent=2)
    
    print(f"\nUpload simulation complete. Records saved to simulated_r2_upload.json")
    return upload_records

def update_database_urls(upload_records):
    """更新数据库中的URL"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    updated_count = 0
    
    for record in upload_records:
        if record['uploaded']:
            try:
                cursor.execute("""
                UPDATE images 
                SET url_thumbnail = ?,
                    url_regular = ?,
                    url_download = ?
                WHERE id = ?
                """, (
                    record['r2_thumbnail'],
                    record['r2_regular'],
                    record['r2_download'],
                    record['id']
                ))
                updated_count += 1
            except Exception as e:
                print(f"Error updating {record['id']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\nDatabase update complete. Updated {updated_count} records.")
    return updated_count

def generate_metadata_for_frontend():
    """生成前端使用的metadata文件"""
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 获取所有图片信息
    query = """
    SELECT id, title, description, author_name, author_url, 
           width, height, aspect_ratio, 
           url_thumbnail, url_regular, url_download, 
           tags, category, quality_score, file_size, 
           transparent_ratio, created_at
    FROM images 
    WHERE tags IS NOT NULL 
    AND tags != '[]' 
    AND tags != ''
    ORDER BY created_at DESC
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    images = []
    for row in rows:
        # 解析tags
        try:
            tags = json.loads(row[11]) if row[11] else []
        except:
            tags = []
        
        images.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'author': {
                'name': row[3],
                'url': row[4]
            },
            'dimensions': {
                'width': row[5],
                'height': row[6],
                'aspectRatio': row[7]
            },
            'urls': {
                'thumbnail': row[8],
                'regular': row[9],
                'download': row[10]
            },
            'tags': tags,
            'category': row[12],
            'qualityScore': row[13],
            'fileSize': row[14],
            'transparentRatio': row[15],
            'createdAt': row[16]
        })
    
    conn.close()
    
    metadata = {
        'version': '2.0',
        'lastUpdated': datetime.now().isoformat(),
        'totalImages': len(images),
        'images': images
    }
    
    # 保存metadata
    with open('metadata_r2_new.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\nMetadata generated. Total images: {len(images)}")
    print("Saved to metadata_r2_new.json")
    
    return metadata

def main():
    """主函数"""
    print("=== R2 Upload Simulation ===")
    print("This script will:")
    print("1. Find all images with tags in the database")
    print("2. Simulate uploading them to R2")
    print("3. Update database URLs to point to R2")
    print("4. Generate new metadata for frontend")
    print("\n" + "="*50 + "\n")
    
    # 第1步：获取带标签的图片
    print("Step 1: Getting images with tags...")
    images = get_images_with_tags()
    print(f"Found {len(images)} images with tags")
    
    # 第2步：模拟上传到R2
    print("\nStep 2: Simulating upload to R2...")
    upload_records = simulate_upload_to_r2(images)
    
    # 统计信息
    uploaded_count = sum(1 for r in upload_records if r['uploaded'])
    print(f"\nUpload summary:")
    print(f"- Total images: {len(upload_records)}")
    print(f"- Successfully 'uploaded': {uploaded_count}")
    print(f"- Failed/Missing: {len(upload_records) - uploaded_count}")
    
    # 第3步：更新数据库URL
    print("\nStep 3: Updating database URLs...")
    update_count = update_database_urls(upload_records)
    
    # 第4步：生成新的metadata
    print("\nStep 4: Generating new metadata...")
    metadata = generate_metadata_for_frontend()
    
    # 最终总结
    print("\n" + "="*50)
    print("SUMMARY:")
    print(f"- Images with tags: {len(images)}")
    print(f"- Simulated uploads: {uploaded_count}")
    print(f"- Database updates: {update_count}")
    print(f"- Metadata images: {metadata['totalImages']}")
    print("\nFiles created:")
    print("- simulated_r2_upload.json (upload records)")
    print("- metadata_r2_new.json (frontend metadata)")
    print("\nNext steps:")
    print("1. Review simulated_r2_upload.json for any missing files")
    print("2. Replace metadata.json with metadata_r2_new.json")
    print("3. Test the website with R2 URLs")

if __name__ == "__main__":
    main()