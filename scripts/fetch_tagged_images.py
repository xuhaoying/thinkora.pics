#!/usr/bin/env python3
"""
优化的图片获取脚本 - 专注于获取有标签的高质量图片
仅使用 Unsplash 和 Pixabay API
"""

import os
import json
import requests
import logging
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
import time
import random

# 加载环境变量
load_dotenv('.env') or load_dotenv('unsplash/.env')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/fetch_tagged_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API配置
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')

# 优化的搜索关键词 - 更具体和商业化
SEARCH_QUERIES = [
    # 科技类
    'laptop computer isolated', 'smartphone mockup', 'headphones product',
    'keyboard mouse setup', 'tablet device', 'smartwatch wearable',
    
    # 办公类
    'office supplies', 'desk accessories', 'notebook pen', 
    'calculator business', 'clipboard document', 'coffee cup work',
    
    # 生活类
    'home decor minimal', 'kitchen utensils', 'bathroom accessories',
    'bedroom furniture', 'living room modern', 'plant indoor',
    
    # 美食类
    'food photography overhead', 'restaurant dish', 'coffee beans',
    'fresh vegetables', 'bakery items', 'healthy snacks',
    
    # 时尚类
    'fashion accessories', 'jewelry product', 'sunglasses eyewear',
    'shoes footwear', 'handbag purse', 'watch timepiece',
    
    # 美容健康
    'skincare products', 'makeup cosmetics', 'perfume bottle',
    'wellness spa', 'fitness equipment', 'yoga mat'
]

class TaggedImageFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ThinkOraPics/1.0 (https://thinkora.pics)'
        })
        
        # 创建必要的目录
        os.makedirs('raw/unsplash', exist_ok=True)
        os.makedirs('raw/pixabay', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # 加载已下载记录
        self.downloaded_ids = self.load_downloaded_ids()
    
    def load_downloaded_ids(self) -> Dict[str, set]:
        """加载已下载的图片ID"""
        downloaded_file = 'downloaded_images.json'
        if os.path.exists(downloaded_file):
            with open(downloaded_file, 'r') as f:
                data = json.load(f)
                return {
                    'unsplash': set(data.get('unsplash', [])),
                    'pixabay': set(data.get('pixabay', []))
                }
        return {'unsplash': set(), 'pixabay': set()}
    
    def save_downloaded_ids(self):
        """保存已下载的图片ID"""
        data = {
            'unsplash': list(self.downloaded_ids['unsplash']),
            'pixabay': list(self.downloaded_ids['pixabay'])
        }
        with open('downloaded_images.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def fetch_unsplash_images(self, query: str, per_page: int = 30) -> List[Dict[str, Any]]:
        """从Unsplash获取带标签的图片"""
        if not UNSPLASH_ACCESS_KEY:
            logger.warning("Unsplash API key not found")
            return []
        
        try:
            url = 'https://api.unsplash.com/search/photos'
            params = {
                'query': query,
                'per_page': per_page,
                'order_by': 'relevant',  # 按相关性排序
                'orientation': 'squarish'  # 优先获取方形图片
            }
            headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
            
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for photo in data.get('results', []):
                # 只选择有标签的图片
                tags = [tag['title'] for tag in photo.get('tags', [])]
                if len(tags) >= 3 and photo['id'] not in self.downloaded_ids['unsplash']:
                    image_info = {
                        'id': photo['id'],
                        'platform': 'unsplash',
                        'url': photo['urls']['regular'],
                        'download_url': photo['links']['download'],
                        'download_location': photo['links']['download_location'],
                        'width': photo['width'],
                        'height': photo['height'],
                        'color': photo.get('color', '#ffffff'),
                        'description': photo.get('description') or photo.get('alt_description', ''),
                        'tags': tags[:10],  # 限制标签数量
                        'author': photo['user']['name'],
                        'author_url': photo['user']['links']['html'],
                        'likes': photo.get('likes', 0),
                        'quality_score': photo.get('likes', 0) * 10 + len(tags) * 5
                    }
                    images.append(image_info)
                    logger.info(f"Unsplash {photo['id']}: {len(tags)} tags - {', '.join(tags[:5])}")
            
            # 按质量分数排序
            images.sort(key=lambda x: x['quality_score'], reverse=True)
            return images[:20]  # 返回前20个最佳结果
            
        except Exception as e:
            logger.error(f"Error fetching from Unsplash: {e}")
            return []
    
    def fetch_pixabay_images(self, query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        """从Pixabay获取带标签的图片"""
        if not PIXABAY_API_KEY:
            logger.warning("Pixabay API key not found")
            return []
        
        try:
            url = 'https://pixabay.com/api/'
            params = {
                'key': PIXABAY_API_KEY,
                'q': query,
                'per_page': per_page,
                'image_type': 'photo',
                'min_width': 1000,
                'min_height': 800,
                'safesearch': 'true',
                'order': 'popular'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for photo in data.get('hits', []):
                # 解析标签
                tags = []
                if photo.get('tags'):
                    tags = [tag.strip() for tag in photo['tags'].split(',')]
                
                # 只选择有足够标签的图片
                if len(tags) >= 3 and str(photo['id']) not in self.downloaded_ids['pixabay']:
                    image_info = {
                        'id': str(photo['id']),
                        'platform': 'pixabay',
                        'url': photo['largeImageURL'],
                        'download_url': photo['largeImageURL'],
                        'width': photo['imageWidth'],
                        'height': photo['imageHeight'],
                        'description': f"{', '.join(tags[:3])} - Professional stock photo",
                        'tags': tags[:10],  # 限制标签数量
                        'author': photo['user'],
                        'author_url': f"https://pixabay.com/users/{photo['user']}-{photo['user_id']}/",
                        'views': photo.get('views', 0),
                        'downloads': photo.get('downloads', 0),
                        'likes': photo.get('likes', 0),
                        'quality_score': photo.get('likes', 0) + photo.get('downloads', 0) + len(tags) * 10
                    }
                    images.append(image_info)
                    logger.info(f"Pixabay {photo['id']}: {len(tags)} tags - {', '.join(tags[:5])}")
            
            # 按质量分数排序
            images.sort(key=lambda x: x['quality_score'], reverse=True)
            return images[:30]  # 返回前30个最佳结果
            
        except Exception as e:
            logger.error(f"Error fetching from Pixabay: {e}")
            return []
    
    def download_image(self, image_info: Dict[str, Any]) -> bool:
        """下载单张图片及其元数据"""
        try:
            platform = image_info['platform']
            image_id = image_info['id']
            url = image_info['download_url']
            
            # 构建文件路径
            filename = f"{platform}_{image_id}.jpg"
            filepath = os.path.join('raw', platform, filename)
            
            # 如果文件已存在，跳过
            if os.path.exists(filepath):
                logger.info(f"Image already exists: {filename}")
                return True
            
            # 特殊处理 Unsplash 下载（需要触发下载事件）
            if platform == 'unsplash' and 'download_location' in image_info:
                try:
                    # 触发下载事件
                    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
                    self.session.get(image_info['download_location'], headers=headers)
                except:
                    pass  # 忽略错误，继续下载
            
            # 下载图片
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            # 保存图片
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 保存元数据（包含标签）
            metadata_path = filepath.replace('.jpg', '_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(image_info, f, indent=2, ensure_ascii=False)
            
            # 记录已下载
            self.downloaded_ids[platform].add(image_id)
            logger.info(f"Downloaded: {filename} with {len(image_info.get('tags', []))} tags")
            
            # 延迟以避免频率限制
            time.sleep(random.uniform(1, 2))
            return True
            
        except Exception as e:
            logger.error(f"Error downloading image {image_info['id']}: {e}")
            return False
    
    def fetch_quality_images(self, total_images: int = 50):
        """获取高质量带标签的图片"""
        logger.info(f"Starting to fetch {total_images} quality images with tags")
        
        all_images = []
        images_per_query = max(2, total_images // len(SEARCH_QUERIES))
        
        # 随机选择查询词，避免重复
        selected_queries = random.sample(SEARCH_QUERIES, min(len(SEARCH_QUERIES), total_images // 2))
        
        for query in selected_queries:
            logger.info(f"\n🔍 Searching for: {query}")
            
            # 从 Unsplash 获取
            unsplash_images = self.fetch_unsplash_images(query, 30)
            all_images.extend(unsplash_images)
            logger.info(f"  Unsplash: Found {len(unsplash_images)} images with tags")
            
            # 从 Pixabay 获取
            pixabay_images = self.fetch_pixabay_images(query, 50)
            all_images.extend(pixabay_images)
            logger.info(f"  Pixabay: Found {len(pixabay_images)} images with tags")
            
            # 如果已经有足够的图片，停止
            if len(all_images) >= total_images * 2:
                break
            
            # 避免请求过快
            time.sleep(2)
        
        # 去重（基于ID）
        unique_images = {}
        for img in all_images:
            key = f"{img['platform']}_{img['id']}"
            if key not in unique_images:
                unique_images[key] = img
        
        # 按质量分数排序，选择最好的
        sorted_images = sorted(unique_images.values(), key=lambda x: x['quality_score'], reverse=True)
        selected_images = sorted_images[:total_images]
        
        logger.info(f"\n📊 Summary:")
        logger.info(f"  Total unique images found: {len(unique_images)}")
        logger.info(f"  Selected top {len(selected_images)} images")
        
        # 下载选中的图片
        downloaded_count = 0
        for i, image in enumerate(selected_images, 1):
            logger.info(f"\n[{i}/{len(selected_images)}] Downloading {image['platform']}_{image['id']}")
            logger.info(f"  Tags: {', '.join(image['tags'][:5])}...")
            
            if self.download_image(image):
                downloaded_count += 1
        
        # 保存已下载记录
        self.save_downloaded_ids()
        
        # 生成报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_found': len(unique_images),
            'selected': len(selected_images),
            'downloaded': downloaded_count,
            'platforms': {
                'unsplash': len([img for img in selected_images if img['platform'] == 'unsplash']),
                'pixabay': len([img for img in selected_images if img['platform'] == 'pixabay'])
            },
            'average_tags': sum(len(img['tags']) for img in selected_images) / len(selected_images) if selected_images else 0,
            'queries_used': selected_queries
        }
        
        with open(f'logs/fetch_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\n✅ Fetch completed! Downloaded {downloaded_count} images with tags")
        logger.info(f"📊 Average tags per image: {report['average_tags']:.1f}")
        
        return report


if __name__ == '__main__':
    fetcher = TaggedImageFetcher()
    
    # 获取50张高质量带标签的图片
    fetcher.fetch_quality_images(50)