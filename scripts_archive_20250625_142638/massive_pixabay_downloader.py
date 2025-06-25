#!/usr/bin/env python3
"""
大规模Pixabay图片下载器
下载1000张多样化的高质量图片
确保类别分布均匀，避免过度集中
"""

import os
import json
import requests
import logging
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Set
from dotenv import load_dotenv
from collections import defaultdict

# 加载环境变量
load_dotenv('.env') or load_dotenv('unsplash/.env')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/massive_download_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MassivePixabayDownloader:
    def __init__(self):
        self.api_key = os.getenv('PIXABAY_API_KEY')
        self.base_url = "https://pixabay.com/api/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ThinkOraPics/1.0 (https://thinkora.pics)'
        })
        
        # 创建目录
        os.makedirs('raw/pixabay_massive', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # 下载统计
        self.downloaded_ids = set()
        self.category_stats = defaultdict(int)
        self.download_progress = {
            'total_target': 1000,
            'downloaded': 0,
            'failed': 0,
            'start_time': datetime.now()
        }
        
        if not self.api_key:
            raise ValueError("PIXABAY_API_KEY not found in environment variables")
    
    def get_diverse_categories(self) -> List[Dict[str, Any]]:
        """获取多样化的分类配置"""
        return [
            # 商务办公类 (100张)
            {
                'name': 'business',
                'queries': ['office supplies', 'business meeting', 'laptop computer', 'documents', 'presentation'],
                'target_count': 100,
                'keywords': ['professional', 'corporate', 'workspace']
            },
            # 科技电子类 (100张)
            {
                'name': 'technology',
                'queries': ['smartphone', 'tablet', 'camera', 'headphones', 'smart watch'],
                'target_count': 100,
                'keywords': ['digital', 'electronic', 'gadget']
            },
            # 食物饮品类 (100张)
            {
                'name': 'food',
                'queries': ['fresh fruit', 'vegetables', 'coffee cup', 'dessert', 'healthy meal'],
                'target_count': 100,
                'keywords': ['organic', 'fresh', 'delicious']
            },
            # 时尚配饰类 (80张)
            {
                'name': 'fashion',
                'queries': ['jewelry', 'handbag', 'shoes', 'sunglasses', 'watch'],
                'target_count': 80,
                'keywords': ['stylish', 'elegant', 'luxury']
            },
            # 健康医疗类 (80张)
            {
                'name': 'health',
                'queries': ['medical equipment', 'vitamins', 'fitness equipment', 'healthcare', 'wellness'],
                'target_count': 80,
                'keywords': ['medical', 'health', 'wellness']
            },
            # 教育学习类 (80张)
            {
                'name': 'education',
                'queries': ['books', 'school supplies', 'study materials', 'laboratory', 'learning tools'],
                'target_count': 80,
                'keywords': ['educational', 'academic', 'knowledge']
            },
            # 运动健身类 (70张)
            {
                'name': 'sports',
                'queries': ['sports equipment', 'fitness gear', 'athletic wear', 'outdoor gear', 'exercise'],
                'target_count': 70,
                'keywords': ['athletic', 'fitness', 'active']
            },
            # 家居装饰类 (70张)
            {
                'name': 'home',
                'queries': ['home decor', 'furniture', 'kitchen utensils', 'plants', 'interior design'],
                'target_count': 70,
                'keywords': ['home', 'decorative', 'interior']
            },
            # 交通工具类 (60张)
            {
                'name': 'transportation',
                'queries': ['car', 'bicycle', 'motorcycle', 'vehicle', 'transport'],
                'target_count': 60,
                'keywords': ['vehicle', 'transport', 'automotive']
            },
            # 建筑设施类 (60张)
            {
                'name': 'buildings',
                'queries': ['architecture', 'building', 'construction', 'urban', 'structure'],
                'target_count': 60,
                'keywords': ['architectural', 'construction', 'urban']
            },
            # 自然环境类 (60张)
            {
                'name': 'nature',
                'queries': ['flowers', 'trees', 'landscape', 'natural elements', 'environment'],
                'target_count': 60,
                'keywords': ['natural', 'organic', 'environmental']
            },
            # 动物类 (50张)
            {
                'name': 'animals',
                'queries': ['pets', 'wildlife', 'domestic animals', 'cute animals', 'animal portraits'],
                'target_count': 50,
                'keywords': ['animal', 'wildlife', 'pet']
            },
            # 音乐艺术类 (50张)
            {
                'name': 'music',
                'queries': ['musical instruments', 'audio equipment', 'music tools', 'sound gear', 'entertainment'],
                'target_count': 50,
                'keywords': ['musical', 'audio', 'entertainment']
            },
            # 旅行度假类 (40张)
            {
                'name': 'travel',
                'queries': ['luggage', 'travel accessories', 'vacation items', 'tourism', 'journey'],
                'target_count': 40,
                'keywords': ['travel', 'vacation', 'tourism']
            }
        ]
    
    def fetch_category_images(
        self,
        category: Dict[str, Any],
        max_pages: int = 5
    ) -> List[Dict[str, Any]]:
        """获取特定分类的图片"""
        logger.info(f"Fetching images for category: {category['name']} (target: {category['target_count']})")
        
        all_images = []
        queries = category['queries']
        keywords = category['keywords']
        
        for query_base in queries:
            if len(all_images) >= category['target_count']:
                break
                
            # 为每个查询添加不同的关键词组合
            for keyword in keywords:
                if len(all_images) >= category['target_count']:
                    break
                
                enhanced_query = f"{query_base} {keyword} isolated white background"
                
                for page in range(1, max_pages + 1):
                    if len(all_images) >= category['target_count']:
                        break
                    
                    try:
                        params = {
                            'key': self.api_key,
                            'q': enhanced_query,
                            'image_type': 'photo',
                            'category': category['name'] if category['name'] in [
                                'backgrounds', 'fashion', 'nature', 'science', 'education', 
                                'health', 'animals', 'industry', 'computer', 'food', 
                                'sports', 'transportation', 'travel', 'buildings', 'business', 'music'
                            ] else None,
                            'orientation': 'all',
                            'min_width': 800,
                            'min_height': 600,
                            'safesearch': 'true',
                            'order': 'popular',
                            'per_page': 50,
                            'page': page
                        }
                        
                        # 移除None值
                        params = {k: v for k, v in params.items() if v is not None}
                        
                        response = self.session.get(self.base_url, params=params)
                        response.raise_for_status()
                        
                        data = response.json()
                        
                        for hit in data.get('hits', []):
                            if len(all_images) >= category['target_count']:
                                break
                                
                            image_id = str(hit['id'])
                            if image_id not in self.downloaded_ids:
                                # 解析标签
                                tags = []
                                if hit.get('tags'):
                                    tags = [tag.strip() for tag in hit['tags'].split(',')]
                                
                                image_info = {
                                    'id': image_id,
                                    'platform': 'pixabay',
                                    'category': category['name'],
                                    'query_used': enhanced_query,
                                    'url': hit['largeImageURL'],
                                    'download_url': hit['largeImageURL'],
                                    'preview_url': hit['previewURL'],
                                    'width': hit['imageWidth'],
                                    'height': hit['imageHeight'],
                                    'description': f"{category['name'].title()} - {', '.join(tags[:3])}" if tags else f"{category['name'].title()} image",
                                    'tags': tags,
                                    'author': hit['user'],
                                    'author_url': f"https://pixabay.com/users/{hit['user']}-{hit['user_id']}/",
                                    'views': hit.get('views', 0),
                                    'downloads': hit.get('downloads', 0),
                                    'likes': hit.get('likes', 0),
                                    'quality_score': hit.get('likes', 0) + hit.get('downloads', 0),
                                    'fetch_metadata': {
                                        'category_target': category['name'],
                                        'query_base': query_base,
                                        'keyword_used': keyword,
                                        'page': page,
                                        'fetch_time': datetime.now().isoformat()
                                    }
                                }
                                all_images.append(image_info)
                                self.downloaded_ids.add(image_id)
                        
                        # API频率限制
                        time.sleep(0.8)
                        
                    except Exception as e:
                        logger.error(f"Error fetching page {page} for query '{enhanced_query}': {e}")
                        time.sleep(2)  # 错误后等待更长时间
        
        # 按质量排序
        all_images.sort(key=lambda x: x['quality_score'], reverse=True)
        
        # 限制数量
        result = all_images[:category['target_count']]
        logger.info(f"Category {category['name']}: found {len(result)} images")
        
        return result
    
    def download_image(self, image_info: Dict[str, Any]) -> bool:
        """下载单张图片"""
        try:
            image_id = image_info['id']
            category = image_info['category']
            url = image_info['download_url']
            
            # 构建文件路径
            filename = f"pixabay_{category}_{image_id}.jpg"
            filepath = os.path.join('raw', 'pixabay_massive', filename)
            
            # 如果文件已存在，跳过
            if os.path.exists(filepath):
                logger.debug(f"Image already exists: {filename}")
                return True
            
            # 下载图片
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 保存图片
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 保存元数据
            metadata_path = filepath.replace('.jpg', '_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(image_info, f, indent=2, ensure_ascii=False)
            
            self.download_progress['downloaded'] += 1
            self.category_stats[category] += 1
            
            logger.info(f"Downloaded {self.download_progress['downloaded']}/1000: {filename} (quality: {image_info['quality_score']})")
            
            # 控制下载频率
            time.sleep(random.uniform(0.3, 0.8))
            return True
            
        except Exception as e:
            logger.error(f"Error downloading image {image_info['id']}: {e}")
            self.download_progress['failed'] += 1
            return False
    
    def run_massive_download(self) -> Dict[str, Any]:
        """执行大规模下载任务"""
        logger.info("🚀 Starting massive Pixabay download - Target: 1000 diverse images")
        
        categories = self.get_diverse_categories()
        all_images = []
        
        # 按分类获取图片
        for category in categories:
            logger.info(f"\n📁 Processing category: {category['name']} (target: {category['target_count']} images)")
            
            category_images = self.fetch_category_images(category)
            all_images.extend(category_images)
            
            logger.info(f"✅ Category {category['name']} completed: {len(category_images)} images collected")
            
            # 检查是否已达到目标
            if len(all_images) >= 1000:
                logger.info("🎯 Reached target of 1000 images!")
                break
        
        # 限制到1000张
        if len(all_images) > 1000:
            all_images = all_images[:1000]
        
        logger.info(f"\n📊 Collection phase completed: {len(all_images)} images ready for download")
        
        # 下载所有图片
        logger.info("\n⬇️ Starting download phase...")
        
        success_count = 0
        for i, image in enumerate(all_images, 1):
            logger.info(f"\n📥 Downloading {i}/{len(all_images)}: {image['category']} - {image['id']}")
            
            if self.download_image(image):
                success_count += 1
            
            # 每100张图片输出进度报告
            if i % 100 == 0:
                elapsed = datetime.now() - self.download_progress['start_time']
                rate = i / elapsed.total_seconds() * 60  # 每分钟下载数
                eta_minutes = (len(all_images) - i) / rate if rate > 0 else 0
                
                logger.info(f"""
🔄 Progress Report - {i}/{len(all_images)} images processed
✅ Success: {success_count} | ❌ Failed: {i - success_count}
⏱️ Speed: {rate:.1f} images/min | ETA: {eta_minutes:.1f} minutes
📊 Category distribution: {dict(self.category_stats)}
                """)
        
        # 生成最终报告
        end_time = datetime.now()
        total_duration = end_time - self.download_progress['start_time']
        
        report = {
            'summary': {
                'total_collected': len(all_images),
                'successfully_downloaded': success_count,
                'failed_downloads': len(all_images) - success_count,
                'success_rate': f"{success_count / len(all_images) * 100:.1f}%",
                'duration': str(total_duration),
                'download_speed': f"{success_count / total_duration.total_seconds() * 60:.1f} images/min"
            },
            'category_distribution': dict(self.category_stats),
            'quality_stats': {
                'high_quality': len([img for img in all_images if img['quality_score'] > 100]),
                'medium_quality': len([img for img in all_images if 20 <= img['quality_score'] <= 100]),
                'basic_quality': len([img for img in all_images if img['quality_score'] < 20])
            },
            'resolution_stats': {
                'high_res': len([img for img in all_images if img['width'] >= 1920]),
                'medium_res': len([img for img in all_images if 1200 <= img['width'] < 1920]),
                'standard_res': len([img for img in all_images if img['width'] < 1200])
            },
            'metadata': {
                'start_time': self.download_progress['start_time'].isoformat(),
                'end_time': end_time.isoformat(),
                'total_categories': len(categories),
                'api_calls_estimated': len(all_images) // 50 + len(categories) * 5
            }
        }
        
        # 保存报告
        report_file = f"logs/massive_download_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"""
🎉 MASSIVE DOWNLOAD COMPLETED! 🎉

📊 Final Statistics:
• Total images collected: {len(all_images)}
• Successfully downloaded: {success_count}
• Success rate: {success_count / len(all_images) * 100:.1f}%
• Total duration: {total_duration}
• Download speed: {success_count / total_duration.total_seconds() * 60:.1f} images/min

📁 Category distribution:
{chr(10).join(f'• {cat}: {count} images' for cat, count in self.category_stats.items())}

📄 Report saved to: {report_file}
        """)
        
        return report


def main():
    """主函数"""
    try:
        downloader = MassivePixabayDownloader()
        report = downloader.run_massive_download()
        
        # 输出JSON格式的报告供脚本调用
        print(json.dumps(report, indent=2, ensure_ascii=False))
        
    except Exception as e:
        logger.error(f"Critical error in massive download: {e}")
        raise


if __name__ == "__main__":
    main()