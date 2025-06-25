#!/usr/bin/env python3
"""
获取5000张高质量带标签的图片
支持Unsplash和Pixabay，分批获取，避免API限制
"""

import os
import json
import requests
import time
import random
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# 加载环境变量
load_dotenv('.env') or load_dotenv('unsplash/.env')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/fetch_5k_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API配置
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')

# 扩展的搜索关键词库
SEARCH_KEYWORDS = {
    'technology': [
        'laptop computer', 'smartphone device', 'tablet screen', 'headphones audio',
        'keyboard typing', 'mouse click', 'monitor display', 'camera photography',
        'smartwatch wearable', 'drone flying', 'virtual reality', 'gaming console',
        'usb cable', 'wireless charger', 'bluetooth speaker', 'microphone podcast'
    ],
    'business': [
        'office desk', 'meeting room', 'business card', 'handshake deal',
        'presentation slides', 'financial chart', 'calculator accounting', 'contract document',
        'team collaboration', 'corporate building', 'startup workspace', 'entrepreneur laptop',
        'invoice payment', 'business strategy', 'marketing plan', 'sales report'
    ],
    'lifestyle': [
        'coffee morning', 'healthy breakfast', 'yoga mat', 'fitness workout',
        'reading book', 'travel suitcase', 'home interior', 'cozy bedroom',
        'kitchen cooking', 'fashion style', 'beauty skincare', 'wellness spa',
        'outdoor adventure', 'hobby craft', 'pet companion', 'family time'
    ],
    'nature': [
        'plant indoor', 'flower bouquet', 'succulent pot', 'tree forest',
        'mountain landscape', 'ocean beach', 'sunset sky', 'garden outdoor',
        'leaf autumn', 'rain weather', 'snow winter', 'spring bloom',
        'cactus desert', 'bamboo zen', 'herb garden', 'botanical tropical'
    ],
    'food': [
        'fresh fruit', 'vegetable organic', 'coffee cup', 'tea ceremony',
        'bakery bread', 'dessert sweet', 'salad healthy', 'pasta italian',
        'sushi japanese', 'pizza slice', 'smoothie drink', 'chocolate treat',
        'wine glass', 'cocktail bar', 'breakfast meal', 'dinner plate'
    ],
    'education': [
        'book study', 'notebook writing', 'pencil drawing', 'classroom teaching',
        'student learning', 'graduation cap', 'library books', 'online course',
        'homework assignment', 'science lab', 'math equation', 'art supplies',
        'music instrument', 'language learning', 'exam test', 'school supplies'
    ],
    'health': [
        'medical stethoscope', 'pills medicine', 'doctor consultation', 'hospital care',
        'fitness equipment', 'yoga pose', 'meditation calm', 'nutrition food',
        'mental health', 'first aid', 'thermometer fever', 'mask protection',
        'vaccine injection', 'dental care', 'eye glasses', 'wellness therapy'
    ],
    'design': [
        'color palette', 'sketch drawing', 'graphic design', 'typography font',
        'logo brand', 'mockup template', 'wireframe ui', 'prototype ux',
        'illustration art', 'pattern texture', 'icon set', 'poster creative',
        'business card', 'brochure layout', 'web design', 'mobile app'
    ]
}

class MassiveImageFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ThinkOraPics/2.0 (https://thinkora.pics)'
        })
        
        # 创建目录
        os.makedirs('raw/unsplash', exist_ok=True)
        os.makedirs('raw/pixabay', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # 加载已下载记录
        self.downloaded_ids = self.load_downloaded_ids()
        self.stats = {
            'unsplash': {'fetched': 0, 'downloaded': 0},
            'pixabay': {'fetched': 0, 'downloaded': 0},
            'total_with_tags': 0
        }
    
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
    
    def fetch_unsplash_batch(self, query: str, page: int = 1, per_page: int = 30) -> List[Dict]:
        """从Unsplash获取一批图片"""
        if not UNSPLASH_ACCESS_KEY:
            return []
        
        try:
            url = 'https://api.unsplash.com/search/photos'
            params = {
                'query': query,
                'page': page,
                'per_page': per_page,
                'order_by': 'relevant'
            }
            headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
            
            response = self.session.get(url, params=params, headers=headers)
            
            # 检查rate limit
            remaining = int(response.headers.get('X-Ratelimit-Remaining', 0))
            if remaining < 10:
                logger.warning(f"Unsplash rate limit low: {remaining}")
                time.sleep(60)  # 等待1分钟
            
            response.raise_for_status()
            data = response.json()
            
            images = []
            for photo in data.get('results', []):
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
                        'description': photo.get('description') or photo.get('alt_description', ''),
                        'tags': tags[:15],  # 限制标签数量
                        'author': photo['user']['name'],
                        'author_url': photo['user']['links']['html'],
                        'likes': photo.get('likes', 0)
                    }
                    images.append(image_info)
                    self.stats['unsplash']['fetched'] += 1
            
            return images
            
        except Exception as e:
            logger.error(f"Unsplash error: {e}")
            return []
    
    def fetch_pixabay_batch(self, query: str, page: int = 1, per_page: int = 100) -> List[Dict]:
        """从Pixabay获取一批图片"""
        if not PIXABAY_API_KEY:
            return []
        
        try:
            url = 'https://pixabay.com/api/'
            params = {
                'key': PIXABAY_API_KEY,
                'q': query,
                'page': page,
                'per_page': min(per_page, 200),  # Pixabay最大200
                'image_type': 'photo',
                'min_width': 800,
                'min_height': 600,
                'safesearch': 'true',
                'order': 'popular'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for photo in data.get('hits', []):
                tags = []
                if photo.get('tags'):
                    tags = [tag.strip() for tag in photo['tags'].split(',')]
                
                if len(tags) >= 3 and str(photo['id']) not in self.downloaded_ids['pixabay']:
                    image_info = {
                        'id': str(photo['id']),
                        'platform': 'pixabay',
                        'url': photo['largeImageURL'],
                        'download_url': photo['largeImageURL'],
                        'width': photo['imageWidth'],
                        'height': photo['imageHeight'],
                        'description': f"{', '.join(tags[:3])} stock photo",
                        'tags': tags[:15],
                        'author': photo['user'],
                        'author_url': f"https://pixabay.com/users/{photo['user']}-{photo['user_id']}/",
                        'views': photo.get('views', 0),
                        'downloads': photo.get('downloads', 0),
                        'likes': photo.get('likes', 0)
                    }
                    images.append(image_info)
                    self.stats['pixabay']['fetched'] += 1
            
            return images
            
        except Exception as e:
            logger.error(f"Pixabay error: {e}")
            return []
    
    def download_image(self, image_info: Dict) -> bool:
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
                return True
            
            # Unsplash需要触发下载事件
            if platform == 'unsplash' and 'download_location' in image_info:
                try:
                    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
                    self.session.get(image_info['download_location'], headers=headers)
                except:
                    pass
            
            # 下载图片
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 保存图片
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 保存元数据
            metadata_path = filepath.replace('.jpg', '_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(image_info, f, indent=2, ensure_ascii=False)
            
            # 记录已下载
            self.downloaded_ids[platform].add(image_id)
            self.stats[platform]['downloaded'] += 1
            self.stats['total_with_tags'] += 1
            
            return True
            
        except Exception as e:
            logger.error(f"Download error {image_info['id']}: {e}")
            return False
    
    def fetch_5k_images(self, target_count: int = 5000):
        """获取5000张图片的主函数"""
        logger.info(f"🚀 开始获取 {target_count} 张带标签的图片")
        logger.info(f"📊 已有图片: Unsplash {len(self.downloaded_ids['unsplash'])}, Pixabay {len(self.downloaded_ids['pixabay'])}")
        
        all_images = []
        
        # 生成所有搜索组合
        search_queries = []
        for category, keywords in SEARCH_KEYWORDS.items():
            for keyword in keywords:
                search_queries.append(f"{keyword} {category}")
        
        # 随机打乱搜索顺序
        random.shuffle(search_queries)
        
        # 分批获取图片
        batch_size = 100
        current_count = len(self.downloaded_ids['unsplash']) + len(self.downloaded_ids['pixabay'])
        
        for query_idx, query in enumerate(search_queries):
            if current_count >= target_count:
                break
            
            logger.info(f"\n🔍 [{query_idx+1}/{len(search_queries)}] 搜索: {query}")
            
            # 从Pixabay获取（更多免费额度）
            for page in range(1, 6):  # 获取前5页
                pixabay_images = self.fetch_pixabay_batch(query, page, 200)
                if not pixabay_images:
                    break
                all_images.extend(pixabay_images)
                logger.info(f"  Pixabay第{page}页: 获得 {len(pixabay_images)} 张图片")
                time.sleep(1)  # 避免请求过快
            
            # 从Unsplash获取（质量更高但额度有限）
            for page in range(1, 4):  # 获取前3页
                unsplash_images = self.fetch_unsplash_batch(query, page, 30)
                if not unsplash_images:
                    break
                all_images.extend(unsplash_images)
                logger.info(f"  Unsplash第{page}页: 获得 {len(unsplash_images)} 张图片")
                time.sleep(2)  # Unsplash限制更严格
            
            # 定期保存进度
            if len(all_images) >= batch_size:
                logger.info(f"\n📥 下载批次 {len(all_images)} 张图片...")
                self.download_batch(all_images[:batch_size])
                all_images = all_images[batch_size:]
                current_count = self.stats['total_with_tags']
                logger.info(f"✅ 当前进度: {current_count}/{target_count}")
                
                # 保存进度
                self.save_downloaded_ids()
                self.save_progress_report()
        
        # 下载剩余图片
        if all_images:
            logger.info(f"\n📥 下载最后 {len(all_images)} 张图片...")
            self.download_batch(all_images)
        
        # 最终报告
        self.save_final_report(target_count)
        
    def download_batch(self, images: List[Dict]):
        """批量下载图片"""
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self.download_image, img): img for img in images}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    img = futures[future]
                    logger.debug(f"✅ 下载成功: {img['platform']}_{img['id']}")
    
    def save_progress_report(self):
        """保存进度报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'total_downloaded': len(self.downloaded_ids['unsplash']) + len(self.downloaded_ids['pixabay'])
        }
        
        with open('logs/fetch_5k_progress.json', 'w') as f:
            json.dump(report, f, indent=2)
    
    def save_final_report(self, target_count: int):
        """保存最终报告"""
        total = self.stats['total_with_tags']
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'target': target_count,
            'achieved': total,
            'completion_rate': f"{(total/target_count*100):.1f}%",
            'platforms': {
                'unsplash': {
                    'fetched': self.stats['unsplash']['fetched'],
                    'downloaded': self.stats['unsplash']['downloaded'],
                    'total': len(self.downloaded_ids['unsplash'])
                },
                'pixabay': {
                    'fetched': self.stats['pixabay']['fetched'],
                    'downloaded': self.stats['pixabay']['downloaded'],
                    'total': len(self.downloaded_ids['pixabay'])
                }
            }
        }
        
        report_path = f'logs/fetch_5k_final_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 最终报告:")
        logger.info(f"  目标: {target_count} 张")
        logger.info(f"  完成: {total} 张 ({report['completion_rate']})")
        logger.info(f"  Unsplash: {report['platforms']['unsplash']['total']} 张")
        logger.info(f"  Pixabay: {report['platforms']['pixabay']['total']} 张")
        logger.info(f"  报告已保存: {report_path}")
        logger.info(f"{'='*60}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='获取5000张带标签的图片')
    parser.add_argument('--count', type=int, default=5000, help='目标图片数量')
    parser.add_argument('--resume', action='store_true', help='继续上次的下载')
    args = parser.parse_args()
    
    fetcher = MassiveImageFetcher()
    
    if args.resume:
        current = len(fetcher.downloaded_ids['unsplash']) + len(fetcher.downloaded_ids['pixabay'])
        logger.info(f"📂 继续下载，当前已有 {current} 张图片")
    
    fetcher.fetch_5k_images(args.count)

if __name__ == '__main__':
    main()