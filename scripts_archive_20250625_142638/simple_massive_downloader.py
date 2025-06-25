#!/usr/bin/env python3
"""
简化的大规模Pixabay图片下载器
使用工作的API密钥下载1000张多样化图片
"""

import os
import json
import requests
import logging
import time
import random
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/simple_download_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleMassiveDownloader:
    def __init__(self):
        # 使用测试验证过的API密钥
        self.api_key = "51008780-20fe13a52bde3f3efd30b126a"
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
        self.total_downloaded = 0
        
    def get_diverse_search_plan(self) -> List[Dict[str, Any]]:
        """获取多样化的搜索计划"""
        return [
            # 商务办公 (150张)
            {'queries': ['office', 'business', 'laptop', 'documents', 'meeting'], 'target': 150, 'category': 'business'},
            
            # 科技电子 (120张)
            {'queries': ['computer', 'smartphone', 'technology', 'gadget', 'digital'], 'target': 120, 'category': 'technology'},
            
            # 食物饮品 (100张)
            {'queries': ['food', 'coffee', 'fruit', 'vegetables', 'cooking'], 'target': 100, 'category': 'food'},
            
            # 健康医疗 (80张)
            {'queries': ['health', 'medical', 'fitness', 'wellness', 'healthcare'], 'target': 80, 'category': 'health'},
            
            # 教育学习 (80张)
            {'queries': ['education', 'books', 'school', 'learning', 'study'], 'target': 80, 'category': 'education'},
            
            # 自然环境 (80张)
            {'queries': ['nature', 'flowers', 'plants', 'trees', 'environment'], 'target': 80, 'category': 'nature'},
            
            # 运动健身 (60张)
            {'queries': ['sports', 'fitness', 'exercise', 'athletic', 'gym'], 'target': 60, 'category': 'sports'},
            
            # 交通工具 (60张)
            {'queries': ['car', 'transport', 'vehicle', 'bicycle', 'automotive'], 'target': 60, 'category': 'transportation'},
            
            # 时尚配饰 (50张)
            {'queries': ['fashion', 'jewelry', 'accessories', 'clothing', 'style'], 'target': 50, 'category': 'fashion'},
            
            # 建筑设施 (50张)
            {'queries': ['building', 'architecture', 'construction', 'house', 'structure'], 'target': 50, 'category': 'buildings'},
            
            # 音乐艺术 (40张)
            {'queries': ['music', 'instrument', 'audio', 'sound', 'entertainment'], 'target': 40, 'category': 'music'},
            
            # 动物宠物 (40张)
            {'queries': ['animals', 'pets', 'dog', 'cat', 'wildlife'], 'target': 40, 'category': 'animals'},
            
            # 旅行度假 (40张)
            {'queries': ['travel', 'vacation', 'tourism', 'luggage', 'holiday'], 'target': 40, 'category': 'travel'},
            
            # 工业制造 (40张)
            {'queries': ['industry', 'manufacturing', 'tools', 'equipment', 'machinery'], 'target': 40, 'category': 'industry'}
        ]
    
    def fetch_images_for_query(self, query: str, category: str, max_images: int = 50) -> List[Dict[str, Any]]:
        """为单个查询获取图片"""
        images = []
        
        try:
            # 简化的参数
            params = {
                'key': self.api_key,
                'q': query,
                'image_type': 'photo',
                'orientation': 'all',
                'min_width': 600,
                'min_height': 400,
                'safesearch': 'true',
                'order': 'popular',
                'per_page': min(50, max_images),
                'page': 1
            }
            
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            for hit in data.get('hits', []):
                if len(images) >= max_images:
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
                        'category': category,
                        'query_used': query,
                        'url': hit['largeImageURL'],
                        'download_url': hit['largeImageURL'],
                        'preview_url': hit['previewURL'],
                        'width': hit['imageWidth'],
                        'height': hit['imageHeight'],
                        'description': f"{category.title()} - {', '.join(tags[:3])}" if tags else f"{category.title()} image from Pixabay",
                        'tags': tags,
                        'author': hit['user'],
                        'author_url': f"https://pixabay.com/users/{hit['user']}-{hit['user_id']}/",
                        'views': hit.get('views', 0),
                        'downloads': hit.get('downloads', 0),
                        'likes': hit.get('likes', 0),
                        'quality_score': hit.get('likes', 0) + hit.get('downloads', 0),
                        'fetch_metadata': {
                            'category_assigned': category,
                            'query_original': query,
                            'fetch_time': datetime.now().isoformat()
                        }
                    }
                    images.append(image_info)
                    self.downloaded_ids.add(image_id)
            
            logger.info(f"Query '{query}' ({category}): found {len(images)} images")
            
        except Exception as e:
            logger.error(f"Error fetching images for query '{query}': {e}")
        
        return images
    
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
            
            self.total_downloaded += 1
            self.category_stats[category] += 1
            
            logger.info(f"✅ Downloaded {self.total_downloaded}: {filename} (quality: {image_info['quality_score']})")
            
            # 控制下载频率
            time.sleep(random.uniform(0.2, 0.5))
            return True
            
        except Exception as e:
            logger.error(f"❌ Error downloading image {image_info['id']}: {e}")
            return False
    
    def run_massive_download(self) -> Dict[str, Any]:
        """执行大规模下载任务"""
        start_time = datetime.now()
        logger.info("🚀 Starting simplified massive Pixabay download - Target: 1000 diverse images")
        
        search_plan = self.get_diverse_search_plan()
        all_images = []
        
        # 第一阶段：收集图片信息
        logger.info("\n📊 Phase 1: Collecting image information...")
        
        for plan in search_plan:
            if len(all_images) >= 1000:
                break
                
            category = plan['category']
            queries = plan['queries']
            target = plan['target']
            
            logger.info(f"\n📁 Category: {category} (target: {target} images)")
            
            category_images = []
            images_per_query = max(1, target // len(queries))
            
            for query in queries:
                if len(category_images) >= target:
                    break
                    
                logger.info(f"  🔍 Searching: {query}")
                query_images = self.fetch_images_for_query(query, category, images_per_query + 10)
                category_images.extend(query_images)
                
                # API频率控制
                time.sleep(0.6)
            
            # 按质量排序并限制数量
            category_images.sort(key=lambda x: x['quality_score'], reverse=True)
            category_images = category_images[:target]
            
            all_images.extend(category_images)
            logger.info(f"✅ Category {category}: collected {len(category_images)} images")
        
        # 限制到1000张
        if len(all_images) > 1000:
            all_images = all_images[:1000]
        
        logger.info(f"\n📊 Collection completed: {len(all_images)} images ready for download")
        
        # 第二阶段：下载图片
        logger.info("\n⬇️ Phase 2: Downloading images...")
        
        success_count = 0
        failed_count = 0
        
        for i, image in enumerate(all_images, 1):
            logger.info(f"\n📥 [{i}/{len(all_images)}] Downloading: {image['category']} - {image['id']}")
            
            if self.download_image(image):
                success_count += 1
            else:
                failed_count += 1
            
            # 每100张图片输出进度报告
            if i % 100 == 0:
                elapsed = datetime.now() - start_time
                rate = i / elapsed.total_seconds() * 60  # 每分钟处理数
                eta_minutes = (len(all_images) - i) / rate if rate > 0 else 0
                
                logger.info(f"""
🔄 Progress Report - {i}/{len(all_images)} processed
✅ Success: {success_count} | ❌ Failed: {failed_count}
⏱️ Speed: {rate:.1f} images/min | ETA: {eta_minutes:.1f} minutes
📊 Categories: {dict(self.category_stats)}
                """)
        
        # 生成最终报告
        end_time = datetime.now()
        total_duration = end_time - start_time
        
        report = {
            'summary': {
                'total_processed': len(all_images),
                'successfully_downloaded': success_count,
                'failed_downloads': failed_count,
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
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'api_key_used': self.api_key[:10] + "...",
                'total_categories': len(search_plan)
            }
        }
        
        # 保存报告
        report_file = f"logs/simple_massive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"""
🎉 MASSIVE DOWNLOAD COMPLETED! 🎉

📊 Final Statistics:
• Total processed: {len(all_images)}
• Successfully downloaded: {success_count}
• Failed downloads: {failed_count}
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
        downloader = SimpleMassiveDownloader()
        report = downloader.run_massive_download()
        
        # 输出JSON格式的报告
        print("\n" + "="*50)
        print("FINAL REPORT JSON:")
        print("="*50)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        
    except KeyboardInterrupt:
        logger.info("⏹️ Download interrupted by user")
    except Exception as e:
        logger.error(f"💥 Critical error: {e}")
        raise


if __name__ == "__main__":
    main()