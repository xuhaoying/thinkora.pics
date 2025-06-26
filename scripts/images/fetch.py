#!/usr/bin/env python3
"""
图片获取脚本 - 从Unsplash和Pixabay获取高质量图片
"""

import os
import sys
import requests
import sqlite3
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ImageFetcher:
    def __init__(self):
        self.db_path = "images.db"
        self.unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY')
        self.pixabay_key = os.getenv('PIXABAY_API_KEY')
        
        # 高质量关键词库
        self.keywords = {
            'technology': ['laptop', 'smartphone', 'robot', 'ai', 'digital', 'innovation'],
            'business': ['office', 'meeting', 'professional', 'workspace', 'teamwork'],
            'nature': ['forest', 'mountain', 'ocean', 'tree', 'landscape', 'wildlife'],
            'lifestyle': ['fitness', 'travel', 'food', 'home', 'fashion', 'health'],
            'abstract': ['pattern', 'texture', 'geometric', 'minimalist', 'modern'],
            'design': ['icon', 'symbol', 'graphic', 'illustration', 'vector'],
        }
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                tags TEXT,
                url_thumbnail TEXT,
                url_regular TEXT,
                width INTEGER,
                height INTEGER,
                likes INTEGER DEFAULT 0,
                author TEXT,
                author_url TEXT,
                source TEXT,
                created_at TEXT,
                processed BOOLEAN DEFAULT FALSE,
                uploaded BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def image_exists(self, image_id):
        """检查图片是否已存在"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM images WHERE id = ?", (image_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def fetch_from_unsplash(self, count=50):
        """从Unsplash获取图片"""
        if not self.unsplash_key:
            print("❌ 未配置Unsplash API密钥")
            return []
        
        images = []
        per_page = min(30, count)  # Unsplash限制每页最多30张
        
        for category, keywords in self.keywords.items():
            for keyword in keywords[:2]:  # 每个分类取前2个关键词
                if len(images) >= count:
                    break
                
                try:
                    url = f"https://api.unsplash.com/search/photos"
                    params = {
                        'query': keyword,
                        'per_page': min(per_page, count - len(images)),
                        'orientation': 'all',
                        'order_by': 'popular'
                    }
                    headers = {'Authorization': f'Client-ID {self.unsplash_key}'}
                    
                    response = requests.get(url, headers=headers, params=params)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    for item in data.get('results', []):
                        if len(images) >= count:
                            break
                        
                        image_id = f"unsplash_{item['id']}"
                        
                        if self.image_exists(image_id):
                            continue
                        
                        # 生成标签
                        tags = [keyword, category]
                        if item.get('tags'):
                            tags.extend([tag['title'] for tag in item['tags'][:5]])
                        
                        image_data = {
                            'id': image_id,
                            'title': f"{keyword.title()} Image",
                            'description': item.get('description') or item.get('alt_description', ''),
                            'tags': json.dumps(list(set(tags))),
                            'url_thumbnail': item['urls']['thumb'],
                            'url_regular': item['urls']['regular'],
                            'width': item['width'],
                            'height': item['height'],
                            'likes': item['likes'],
                            'author': item['user']['name'],
                            'author_url': item['user']['links']['html'],
                            'source': 'unsplash',
                            'created_at': datetime.now().isoformat()
                        }
                        
                        images.append(image_data)
                    
                    time.sleep(1)  # API限制
                    
                except Exception as e:
                    print(f"❌ Unsplash获取失败 {keyword}: {e}")
                    continue
        
        return images
    
    def fetch_from_pixabay(self, count=50):
        """从Pixabay获取图片"""
        if not self.pixabay_key:
            print("❌ 未配置Pixabay API密钥")
            return []
        
        images = []
        per_page = min(200, count)  # Pixabay最多200张
        
        for category, keywords in self.keywords.items():
            for keyword in keywords[:2]:
                if len(images) >= count:
                    break
                
                try:
                    url = "https://pixabay.com/api/"
                    params = {
                        'key': self.pixabay_key,
                        'q': keyword,
                        'image_type': 'photo',
                        'orientation': 'all',
                        'min_width': 1920,
                        'min_height': 1080,
                        'per_page': min(per_page, count - len(images)),
                        'safesearch': 'true',
                        'order': 'popular'
                    }
                    
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    for item in data.get('hits', []):
                        if len(images) >= count:
                            break
                        
                        image_id = f"pixabay_{item['id']}"
                        
                        if self.image_exists(image_id):
                            continue
                        
                        # 生成标签
                        tags = [keyword, category]
                        if item.get('tags'):
                            tags.extend(item['tags'].split(', ')[:5])
                        
                        image_data = {
                            'id': image_id,
                            'title': f"{keyword.title()} {category.title()} Image",
                            'description': f"High-quality {keyword} image from Pixabay",
                            'tags': json.dumps(list(set(tags))),
                            'url_thumbnail': item['previewURL'],
                            'url_regular': item['largeImageURL'],
                            'width': item['imageWidth'],
                            'height': item['imageHeight'],
                            'likes': item['likes'],
                            'author': item['user'],
                            'author_url': f"https://pixabay.com/users/{item['user']}-{item['user_id']}/",
                            'source': 'pixabay',
                            'created_at': datetime.now().isoformat()
                        }
                        
                        images.append(image_data)
                    
                    time.sleep(1)  # API限制
                    
                except Exception as e:
                    print(f"❌ Pixabay获取失败 {keyword}: {e}")
                    continue
        
        return images
    
    def save_images(self, images):
        """保存图片数据到数据库"""
        if not images:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for image in images:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO images 
                    (id, title, description, tags, url_thumbnail, url_regular, width, height, 
                     likes, author, author_url, source, created_at, processed, uploaded)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    image['id'], image['title'], image['description'], image['tags'],
                    image['url_thumbnail'], image['url_regular'], image['width'], image['height'],
                    image['likes'], image['author'], image['author_url'], image['source'],
                    image['created_at'], False, False
                ))
                saved_count += 1
            except Exception as e:
                print(f"❌ 保存图片失败 {image['id']}: {e}")
        
        conn.commit()
        conn.close()
        return saved_count
    
    def fetch_images(self, count=100, source="both"):
        """获取图片的主函数"""
        self.init_database()
        
        print(f"🚀 开始获取 {count} 张图片...")
        
        all_images = []
        
        if source in ["unsplash", "both"]:
            print("📸 从Unsplash获取图片...")
            unsplash_count = count if source == "unsplash" else count // 2
            unsplash_images = self.fetch_from_unsplash(unsplash_count)
            all_images.extend(unsplash_images)
            print(f"✅ Unsplash获取了 {len(unsplash_images)} 张图片")
        
        if source in ["pixabay", "both"]:
            print("🎨 从Pixabay获取图片...")
            pixabay_count = count if source == "pixabay" else count // 2
            pixabay_images = self.fetch_from_pixabay(pixabay_count)
            all_images.extend(pixabay_images)
            print(f"✅ Pixabay获取了 {len(pixabay_images)} 张图片")
        
        # 保存到数据库
        saved_count = self.save_images(all_images)
        
        print(f"💾 成功保存 {saved_count} 张新图片到数据库")
        return saved_count

def main():
    parser = argparse.ArgumentParser(description="获取高质量图片")
    parser.add_argument("--count", type=int, default=100, help="获取图片数量")
    parser.add_argument("--source", choices=["unsplash", "pixabay", "both"], 
                       default="both", help="图片来源")
    
    args = parser.parse_args()
    
    fetcher = ImageFetcher()
    fetcher.fetch_images(args.count, args.source)

if __name__ == "__main__":
    main()