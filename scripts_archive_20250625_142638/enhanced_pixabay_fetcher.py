#!/usr/bin/env python3
"""
增强的Pixabay图片获取器
基于Pixabay API官方文档实现的高级功能
支持更多参数、更好的分类和质量控制
"""

import os
import json
import requests
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import time
import random

# 加载环境变量
load_dotenv('.env') or load_dotenv('unsplash/.env')

# 配置日志
logger = logging.getLogger(__name__)

class EnhancedPixabayFetcher:
    def __init__(self):
        self.api_key = os.getenv('PIXABAY_API_KEY')
        self.base_url = "https://pixabay.com/api/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ThinkOraPics/1.0 (https://thinkora.pics)'
        })
        
        # 创建目录
        os.makedirs('raw/pixabay', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # 加载已下载记录
        self.downloaded_ids = self.load_downloaded_ids()
    
    def load_downloaded_ids(self) -> set:
        """加载已下载的Pixabay图片ID"""
        downloaded_file = 'downloaded_images.json'
        if os.path.exists(downloaded_file):
            with open(downloaded_file, 'r') as f:
                data = json.load(f)
                return set(data.get('pixabay', []))
        return set()
    
    def save_downloaded_ids(self):
        """保存已下载的图片ID"""
        downloaded_file = 'downloaded_images.json'
        data = {}
        if os.path.exists(downloaded_file):
            with open(downloaded_file, 'r') as f:
                data = json.load(f)
        
        data['pixabay'] = list(self.downloaded_ids)
        
        with open(downloaded_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def fetch_images_advanced(
        self,
        query: str,
        image_type: str = "photo",  # photo, illustration, vector
        category: Optional[str] = None,  # backgrounds, fashion, nature, science, education, feelings, health, people, religion, places, animals, industry, computer, food, sports, transportation, travel, buildings, business, music
        orientation: str = "all",  # all, horizontal, vertical
        min_width: int = 0,
        min_height: int = 0,
        colors: Optional[str] = None,  # grayscale, transparent, red, orange, yellow, green, turquoise, blue, lilac, pink, white, gray, black, brown
        safesearch: bool = True,
        editors_choice: bool = False,
        order: str = "popular",  # popular, latest
        per_page: int = 20,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        使用Pixabay API的高级参数获取图片
        
        Args:
            query: 搜索关键词 (URL编码，最大100字符)
            image_type: 图片类型 - photo, illustration, vector
            category: 图片分类
            orientation: 图片方向 - all, horizontal, vertical
            min_width: 最小宽度
            min_height: 最小高度
            colors: 颜色过滤
            safesearch: 安全搜索过滤
            editors_choice: 仅编辑精选
            order: 排序方式 - popular, latest
            per_page: 每页结果数 (3-200)
            page: 页码
        """
        if not self.api_key:
            logger.warning("Pixabay API key not found")
            return []
        
        try:
            # 构建参数
            params = {
                'key': self.api_key,
                'q': query,
                'image_type': image_type,
                'orientation': orientation,
                'order': order,
                'per_page': min(per_page, 200),  # API限制最大200
                'page': page,
                'safesearch': 'true' if safesearch else 'false'
            }
            
            # 添加可选参数
            if category:
                params['category'] = category
            if min_width > 0:
                params['min_width'] = min_width
            if min_height > 0:
                params['min_height'] = min_height
            if colors:
                params['colors'] = colors
            if editors_choice:
                params['editors_choice'] = 'true'
            
            logger.info(f"Fetching from Pixabay with query: {query}, type: {image_type}, category: {category}")
            
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            # 解析响应
            total = data.get('total', 0)
            total_hits = data.get('totalHits', 0)
            logger.info(f"Pixabay search results: {total_hits} accessible out of {total} total matches")
            
            for hit in data.get('hits', []):
                image_id = str(hit['id'])
                
                # 跳过已下载的图片
                if image_id not in self.downloaded_ids:
                    # 解析标签
                    tags = []
                    if hit.get('tags'):
                        tags = [tag.strip() for tag in hit['tags'].split(',')]
                    
                    # 构建图片信息
                    image_info = {
                        'id': image_id,
                        'platform': 'pixabay',
                        'url': hit['largeImageURL'],
                        'download_url': hit['largeImageURL'],
                        'preview_url': hit['previewURL'],
                        'web_format_url': hit['webformatURL'],
                        'width': hit['imageWidth'],
                        'height': hit['imageHeight'],
                        'description': f"Pixabay image - {', '.join(tags[:3])}",
                        'tags': tags,
                        'author': hit['user'],
                        'author_url': f"https://pixabay.com/users/{hit['user']}-{hit['user_id']}/",
                        'author_id': hit['user_id'],
                        'views': hit['views'],
                        'downloads': hit['downloads'],
                        'likes': hit['likes'],
                        'comments': hit['comments'],
                        'page_url': hit['pageURL'],
                        'type': hit['type'],
                        'category': category or 'general',
                        'api_metadata': {
                            'image_type': image_type,
                            'orientation': orientation,
                            'colors': colors,
                            'safesearch': safesearch,
                            'editors_choice': editors_choice,
                            'fetch_date': datetime.now().isoformat()
                        }
                    }
                    images.append(image_info)
            
            logger.info(f"Found {len(images)} new images from Pixabay")
            return images
            
        except Exception as e:
            logger.error(f"Error fetching from Pixabay: {e}")
            return []
    
    def fetch_by_categories(
        self,
        query: str,
        categories: List[str],
        images_per_category: int = 5
    ) -> List[Dict[str, Any]]:
        """按分类获取图片"""
        all_images = []
        
        for category in categories:
            logger.info(f"Fetching {images_per_category} images from category: {category}")
            
            # 为透明背景优化的参数
            images = self.fetch_images_advanced(
                query=f"{query} transparent background",
                image_type="photo",
                category=category,
                orientation="all",
                min_width=800,  # 确保质量
                min_height=600,
                safesearch=True,
                editors_choice=False,  # 不限制编辑精选，获得更多结果
                order="popular",
                per_page=images_per_category
            )
            
            all_images.extend(images)
            
            # 遵守API频率限制 (100 requests per 60 seconds)
            time.sleep(1)
        
        return all_images
    
    def fetch_high_quality_transparent(
        self,
        base_queries: List[str],
        per_query: int = 10
    ) -> List[Dict[str, Any]]:
        """获取高质量透明背景图片"""
        all_images = []
        
        # Pixabay分类列表
        categories = [
            'backgrounds', 'business', 'computer', 'education', 
            'fashion', 'food', 'health', 'industry', 'nature',
            'people', 'science', 'sports', 'transportation', 'travel'
        ]
        
        for query in base_queries:
            logger.info(f"Processing query: {query}")
            
            # 尝试不同的图片类型
            for image_type in ['photo', 'illustration']:
                # 随机选择一些分类
                selected_categories = random.sample(categories, min(3, len(categories)))
                
                for category in selected_categories:
                    images = self.fetch_images_advanced(
                        query=f"{query} isolated white background",
                        image_type=image_type,
                        category=category,
                        orientation="all",
                        min_width=1024,  # 高质量要求
                        min_height=768,
                        colors="transparent",  # 优先透明背景
                        safesearch=True,
                        editors_choice=False,
                        order="popular",
                        per_page=max(1, per_query // 6)  # 分配到每个类型和分类
                    )
                    
                    all_images.extend(images)
                    
                    # 控制请求频率
                    time.sleep(0.8)
                    
                    # 如果已经获得足够的图片，提前退出
                    if len(all_images) >= per_query * len(base_queries):
                        break
                
                if len(all_images) >= per_query * len(base_queries):
                    break
            
            if len(all_images) >= per_query * len(base_queries):
                break
        
        # 去重并按质量排序
        unique_images = {}
        for img in all_images:
            if img['id'] not in unique_images:
                unique_images[img['id']] = img
        
        # 按受欢迎程度排序
        sorted_images = sorted(
            unique_images.values(),
            key=lambda x: x['likes'] + x['downloads'],
            reverse=True
        )
        
        return sorted_images
    
    def download_image(self, image_info: Dict[str, Any]) -> bool:
        """下载图片并保存元数据"""
        try:
            image_id = image_info['id']
            url = image_info['download_url']
            
            # 构建文件路径
            filename = f"pixabay_{image_id}.jpg"
            filepath = os.path.join('raw', 'pixabay', filename)
            
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
                json.dump(image_info, f, indent=2, ensure_ascii=False)
            
            # 记录已下载
            self.downloaded_ids.add(image_id)
            logger.info(f"Downloaded: {filename} (likes: {image_info['likes']}, downloads: {image_info['downloads']})")
            
            # 遵守频率限制
            time.sleep(random.uniform(0.5, 1.5))
            return True
            
        except Exception as e:
            logger.error(f"Error downloading image {image_info['id']}: {e}")
            return False
    
    def run_enhanced_fetch(self, total_images: int = 20) -> Dict[str, Any]:
        """运行增强的获取任务"""
        logger.info("Starting enhanced Pixabay fetch")
        
        # 优化的搜索查询
        transparent_queries = [
            "product photography white background",
            "isolated object transparent",
            "studio shot clean background", 
            "cutout png ready",
            "minimal white background",
            "object on white",
            "isolated product",
            "clean cutout"
        ]
        
        # 获取高质量图片
        all_images = self.fetch_high_quality_transparent(
            base_queries=transparent_queries,
            per_query=max(1, total_images // len(transparent_queries))
        )
        
        # 限制图片数量
        if len(all_images) > total_images:
            all_images = all_images[:total_images]
        
        # 下载图片
        downloaded_count = 0
        for image in all_images:
            if self.download_image(image):
                downloaded_count += 1
        
        # 保存下载记录
        self.save_downloaded_ids()
        
        # 生成报告
        report = {
            'date': datetime.now().isoformat(),
            'platform': 'pixabay',
            'total_found': len(all_images),
            'downloaded': downloaded_count,
            'queries_used': transparent_queries,
            'avg_quality_score': sum(img['likes'] + img['downloads'] for img in all_images) / len(all_images) if all_images else 0,
            'categories_fetched': list(set(img.get('category', 'general') for img in all_images)),
            'image_types': list(set(img['api_metadata']['image_type'] for img in all_images))
        }
        
        logger.info(f"Enhanced Pixabay fetch completed. Downloaded {downloaded_count} new images")
        return report


def main():
    """主函数示例"""
    fetcher = EnhancedPixabayFetcher()
    
    # 运行增强获取
    report = fetcher.run_enhanced_fetch(total_images=15)
    
    # 打印报告
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 保存报告
    report_file = f"logs/enhanced_pixabay_report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()