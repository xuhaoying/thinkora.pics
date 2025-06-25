#!/usr/bin/env python3
"""
每日自动获取多平台图片脚本
支持 Unsplash, Pexels, Pixabay
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
        logging.FileHandler(f'logs/daily_fetch_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API配置
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')

# 搜索关键词 - 针对透明背景优化
SEARCH_QUERIES = [
    'product photography', 'isolated object', 'white background',
    'cutout', 'studio shot', 'minimal design', 'clean background', 
    'single object', 'transparent', 'png ready', 'commercial use',
    'high quality', 'professional', 'isolated item'
]

# Pixabay官方支持的类别
PIXABAY_CATEGORIES = [
    'backgrounds', 'fashion', 'nature', 'science', 'education', 
    'feelings', 'health', 'people', 'religion', 'places', 'animals', 
    'industry', 'computer', 'food', 'sports', 'transportation', 
    'travel', 'buildings', 'business', 'music'
]

# 通用类别关键词
CATEGORIES = [
    'electronics', 'office', 'home decor', 'lifestyle', 'fashion',
    'food', 'nature', 'technology', 'business', 'education',
    'health', 'sports', 'travel', 'animals', 'music'
]

# 优化的搜索组合
OPTIMIZED_QUERIES = [
    "product white background",
    "object isolated transparent", 
    "commercial photography clean",
    "studio lighting minimal",
    "professional cutout png",
    "high resolution isolated",
    "marketing material clean",
    "presentation ready object"
]

class MultiPlatformImageFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ThinkOraPics/1.0 (https://thinkora.pics)'
        })
        
        # 创建必要的目录
        os.makedirs('raw/unsplash', exist_ok=True)
        os.makedirs('raw/pexels', exist_ok=True)
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
                    'pexels': set(data.get('pexels', [])),
                    'pixabay': set(data.get('pixabay', []))
                }
        return {'unsplash': set(), 'pexels': set(), 'pixabay': set()}
    
    def save_downloaded_ids(self):
        """保存已下载的图片ID"""
        data = {
            'unsplash': list(self.downloaded_ids['unsplash']),
            'pexels': list(self.downloaded_ids['pexels']),
            'pixabay': list(self.downloaded_ids['pixabay'])
        }
        with open('downloaded_images.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def fetch_unsplash_images(self, query: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """从Unsplash获取图片"""
        if not UNSPLASH_ACCESS_KEY:
            logger.warning("Unsplash API key not found")
            return []
        
        try:
            url = 'https://api.unsplash.com/search/photos'
            params = {
                'query': query,
                'per_page': per_page,
                'order_by': 'latest'
            }
            headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
            
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for photo in data.get('results', []):
                if photo['id'] not in self.downloaded_ids['unsplash']:
                    image_info = {
                        'id': photo['id'],
                        'platform': 'unsplash',
                        'url': photo['urls']['regular'],
                        'download_url': photo['links']['download'],
                        'width': photo['width'],
                        'height': photo['height'],
                        'description': photo.get('description', ''),
                        'tags': [tag['title'] for tag in photo.get('tags', [])],
                        'author': photo['user']['name'],
                        'author_url': photo['user']['links']['html']
                    }
                    images.append(image_info)
            
            return images
            
        except Exception as e:
            logger.error(f"Error fetching from Unsplash: {e}")
            return []
    
    def fetch_pexels_images(self, query: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """从Pexels获取图片"""
        if not PEXELS_API_KEY:
            logger.warning("Pexels API key not found")
            return []
        
        try:
            url = 'https://api.pexels.com/v1/search'
            params = {
                'query': query,
                'per_page': per_page
            }
            headers = {'Authorization': PEXELS_API_KEY}
            
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for photo in data.get('photos', []):
                if str(photo['id']) not in self.downloaded_ids['pexels']:
                    image_info = {
                        'id': str(photo['id']),
                        'platform': 'pexels',
                        'url': photo['src']['large2x'],
                        'download_url': photo['src']['original'],
                        'width': photo['width'],
                        'height': photo['height'],
                        'description': photo.get('alt', ''),
                        'tags': [],  # Pexels不提供标签
                        'author': photo['photographer'],
                        'author_url': photo['photographer_url']
                    }
                    images.append(image_info)
            
            return images
            
        except Exception as e:
            logger.error(f"Error fetching from Pexels: {e}")
            return []
    
    def fetch_pixabay_images(self, query: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """从Pixabay获取图片 - 增强版本"""
        if not PIXABAY_API_KEY:
            logger.warning("Pixabay API key not found")
            return []
        
        try:
            url = 'https://pixabay.com/api/'
            
            # 优化的参数设置
            params = {
                'key': PIXABAY_API_KEY,
                'q': f"{query} isolated white background",  # 优化搜索词
                'per_page': min(per_page, 200),  # API限制
                'image_type': 'photo',
                'orientation': 'all',
                'min_width': 800,  # 确保质量
                'min_height': 600,
                'safesearch': 'true',
                'order': 'popular',  # 优先获取受欢迎的图片
                'category': random.choice(['business', 'computer', 'education', 'nature', 'science', 'food', 'health'])  # 随机分类
            }
            
            # 随机添加颜色过滤以获得更好的透明背景效果
            if random.random() < 0.3:  # 30%概率添加透明色彩过滤
                params['colors'] = 'transparent'
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            # 记录API响应信息
            total = data.get('total', 0)
            total_hits = data.get('totalHits', 0)
            logger.info(f"Pixabay search '{query}': {total_hits} accessible out of {total} total matches")
            
            for photo in data.get('hits', []):
                if str(photo['id']) not in self.downloaded_ids['pixabay']:
                    # 解析标签
                    tags = []
                    if photo.get('tags'):
                        tags = [tag.strip() for tag in photo['tags'].split(',')]
                    
                    image_info = {
                        'id': str(photo['id']),
                        'platform': 'pixabay',
                        'url': photo['largeImageURL'],
                        'download_url': photo['largeImageURL'],
                        'preview_url': photo.get('previewURL', ''),
                        'web_format_url': photo.get('webformatURL', ''),
                        'width': photo['imageWidth'],
                        'height': photo['imageHeight'],
                        'description': f"High-quality image: {', '.join(tags[:3])}" if tags else f"Pixabay image {photo['id']}",
                        'tags': tags,
                        'author': photo['user'],
                        'author_url': f"https://pixabay.com/users/{photo['user']}-{photo['user_id']}/",
                        'author_id': photo.get('user_id', ''),
                        'views': photo.get('views', 0),
                        'downloads': photo.get('downloads', 0),
                        'likes': photo.get('likes', 0),
                        'comments': photo.get('comments', 0),
                        'page_url': photo.get('pageURL', ''),
                        'type': photo.get('type', 'photo'),
                        'category': params.get('category', 'general'),
                        'quality_score': photo.get('likes', 0) + photo.get('downloads', 0),  # 质量评分
                        'api_metadata': {
                            'orientation': params.get('orientation'),
                            'min_resolution': f"{params.get('min_width')}x{params.get('min_height')}",
                            'safesearch': params.get('safesearch'),
                            'fetch_date': datetime.now().isoformat(),
                            'enhanced_query': params['q']
                        }
                    }
                    images.append(image_info)
            
            # 按质量排序
            images.sort(key=lambda x: x['quality_score'], reverse=True)
            
            return images
            
        except Exception as e:
            logger.error(f"Error fetching from Pixabay: {e}")
            return []
    
    def download_image(self, image_info: Dict[str, Any]) -> bool:
        """下载单张图片"""
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
            
            # 下载图片
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            # 保存图片
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 保存元数据
            metadata_path = filepath.replace('.jpg', '_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(image_info, f, indent=2)
            
            # 记录已下载
            self.downloaded_ids[platform].add(image_id)
            logger.info(f"Downloaded: {filename}")
            
            # 延迟以避免频率限制
            time.sleep(random.uniform(1, 3))
            return True
            
        except Exception as e:
            logger.error(f"Error downloading image {image_info['id']}: {e}")
            return False
    
    def run_daily_fetch(self, images_per_platform: int = 10):
        """执行每日获取任务 - 增强版本"""
        logger.info("Starting enhanced daily image fetch")
        
        all_images = []
        
        # 智能选择查询策略
        use_optimized = random.random() < 0.7  # 70%概率使用优化查询
        
        if use_optimized:
            # 使用优化的搜索组合
            base_query = random.choice(OPTIMIZED_QUERIES)
            category = random.choice(CATEGORIES)
            full_query = f"{base_query} {category}"
        else:
            # 使用传统组合
            query = random.choice(SEARCH_QUERIES)
            category = random.choice(CATEGORIES)
            full_query = f"{query} {category}"
        
        logger.info(f"Today's search strategy: {'Optimized' if use_optimized else 'Traditional'}")
        logger.info(f"Today's search query: {full_query}")
        
        # 从各平台获取图片
        platform_results = {}
        
        if UNSPLASH_ACCESS_KEY:
            unsplash_images = self.fetch_unsplash_images(full_query, images_per_platform)
            all_images.extend(unsplash_images)
            platform_results['unsplash'] = {
                'found': len(unsplash_images),
                'avg_quality': sum(getattr(img, 'quality_score', 0) for img in unsplash_images) / len(unsplash_images) if unsplash_images else 0
            }
            logger.info(f"Found {len(unsplash_images)} new images from Unsplash")
        
        if PEXELS_API_KEY:
            pexels_images = self.fetch_pexels_images(full_query, images_per_platform)
            all_images.extend(pexels_images)
            platform_results['pexels'] = {
                'found': len(pexels_images),
                'avg_quality': sum(getattr(img, 'quality_score', 0) for img in pexels_images) / len(pexels_images) if pexels_images else 0
            }
            logger.info(f"Found {len(pexels_images)} new images from Pexels")
        
        if PIXABAY_API_KEY:
            pixabay_images = self.fetch_pixabay_images(full_query, images_per_platform)
            all_images.extend(pixabay_images)
            platform_results['pixabay'] = {
                'found': len(pixabay_images),
                'avg_quality': sum(img.get('quality_score', 0) for img in pixabay_images) / len(pixabay_images) if pixabay_images else 0,
                'categories_used': list(set(img.get('category', 'general') for img in pixabay_images))
            }
            logger.info(f"Found {len(pixabay_images)} new images from Pixabay")
        
        # 按质量排序所有图片
        all_images.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        
        # 下载所有新图片
        downloaded_count = 0
        failed_downloads = []
        
        for image in all_images:
            if self.download_image(image):
                downloaded_count += 1
            else:
                failed_downloads.append(image['id'])
        
        # 保存已下载记录
        self.save_downloaded_ids()
        
        # 生成增强的每日报告
        report = {
            'date': datetime.now().isoformat(),
            'search_strategy': 'optimized' if use_optimized else 'traditional',
            'query': full_query,
            'total_found': len(all_images),
            'downloaded': downloaded_count,
            'failed_downloads': len(failed_downloads),
            'success_rate': f"{(downloaded_count / len(all_images) * 100):.1f}%" if all_images else "0%",
            'platform_results': platform_results,
            'quality_distribution': {
                'high_quality': len([img for img in all_images if img.get('quality_score', 0) > 100]),
                'medium_quality': len([img for img in all_images if 10 <= img.get('quality_score', 0) <= 100]),
                'low_quality': len([img for img in all_images if img.get('quality_score', 0) < 10])
            },
            'image_dimensions': {
                'high_res': len([img for img in all_images if img.get('width', 0) >= 1920]),
                'medium_res': len([img for img in all_images if 800 <= img.get('width', 0) < 1920]),
                'low_res': len([img for img in all_images if img.get('width', 0) < 800])
            }
        }
        
        # 保存报告
        report_file = f"logs/daily_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Enhanced daily fetch completed. Downloaded {downloaded_count}/{len(all_images)} images")
        logger.info(f"Success rate: {report['success_rate']}")
        
        return report


if __name__ == "__main__":
    fetcher = MultiPlatformImageFetcher()
    report = fetcher.run_daily_fetch(images_per_platform=10)
    print(json.dumps(report, indent=2))