#!/usr/bin/env python3
"""
多平台透明PNG下载器 - 支持Unsplash、Pexels、Pixabay
"""

import os
import json
import requests
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import argparse
import sys
from abc import ABC, abstractmethod

# macOS 特定配置
if sys.platform == "darwin":
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

class PlatformDownloader(ABC):
    """抽象基类，定义下载器接口"""
    
    @abstractmethod
    def search_photos(self, query: str, page: int = 1, per_page: int = 30):
        """搜索图片"""
        pass
    
    @abstractmethod
    def download_photo(self, photo_data: dict):
        """下载单张图片"""
        pass
    
    @abstractmethod
    def get_photo_url(self, photo_data: dict):
        """获取图片下载URL"""
        pass

class UnsplashDownloader(PlatformDownloader):
    """Unsplash下载器"""
    
    def __init__(self, access_key: str):
        self.access_key = access_key
        self.base_url = "https://api.unsplash.com"
    
    def search_photos(self, query: str, page: int = 1, per_page: int = 30):
        """搜索Unsplash图片"""
        response = requests.get(
            f"{self.base_url}/search/photos",
            params={
                "query": query,
                "per_page": per_page,
                "page": page,
                "order_by": "relevant"
            },
            headers={"Authorization": f"Client-ID {self.access_key}"},
            timeout=10
        )
        
        if response.status_code != 200:
            raise Exception(f"Unsplash API错误: {response.status_code}")
        
        data = response.json()
        return data.get("results", [])
    
    def get_photo_url(self, photo_data: dict):
        """获取Unsplash图片URL"""
        return photo_data["urls"]["regular"]
    
    def download_photo(self, photo_data: dict):
        """下载Unsplash图片"""
        photo_id = photo_data["id"]
        download_url = self.get_photo_url(photo_data)
        
        # 下载图片
        img_response = requests.get(download_url, timeout=15)
        if img_response.status_code != 200:
            raise Exception(f"图片下载失败: HTTP {img_response.status_code}")
        
        # 保存文件
        filename = f"raw/{photo_id}.jpg"
        with open(filename, "wb") as f:
            f.write(img_response.content)
        
        # 发送下载统计
        try:
            requests.get(
                photo_data["links"]["download_location"],
                headers={"Authorization": f"Client-ID {self.access_key}"},
                timeout=5
            )
        except:
            pass  # 忽略统计发送失败
        
        return {
            "id": photo_id,
            "filename": filename,
            "size": len(img_response.content),
            "platform": "unsplash"
        }

class PexelsDownloader(PlatformDownloader):
    """Pexels下载器"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"
    
    def search_photos(self, query: str, page: int = 1, per_page: int = 30):
        """搜索Pexels图片"""
        response = requests.get(
            f"{self.base_url}/search",
            params={
                "query": query,
                "page": page,
                "per_page": per_page
            },
            headers={"Authorization": self.api_key},
            timeout=10
        )
        
        if response.status_code != 200:
            raise Exception(f"Pexels API错误: {response.status_code}")
        
        data = response.json()
        return data.get("photos", [])
    
    def get_photo_url(self, photo_data: dict):
        """获取Pexels图片URL"""
        # 选择中等大小的图片
        return photo_data["src"]["medium"]
    
    def download_photo(self, photo_data: dict):
        """下载Pexels图片"""
        photo_id = photo_data["id"]
        download_url = self.get_photo_url(photo_data)
        
        # 下载图片
        img_response = requests.get(download_url, timeout=15)
        if img_response.status_code != 200:
            raise Exception(f"图片下载失败: HTTP {img_response.status_code}")
        
        # 保存文件
        filename = f"raw/pexels_{photo_id}.jpg"
        with open(filename, "wb") as f:
            f.write(img_response.content)
        
        return {
            "id": f"pexels_{photo_id}",
            "filename": filename,
            "size": len(img_response.content),
            "platform": "pexels"
        }

class PixabayDownloader(PlatformDownloader):
    """Pixabay下载器"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://pixabay.com/api"
    
    def search_photos(self, query: str, page: int = 1, per_page: int = 30):
        """搜索Pixabay图片"""
        response = requests.get(
            self.base_url,
            params={
                "key": self.api_key,
                "q": query,
                "page": page,
                "per_page": per_page,
                "image_type": "photo",
                "safesearch": "true"
            },
            timeout=10
        )
        
        if response.status_code != 200:
            raise Exception(f"Pixabay API错误: {response.status_code}")
        
        data = response.json()
        return data.get("hits", [])
    
    def get_photo_url(self, photo_data: dict):
        """获取Pixabay图片URL"""
        # 选择中等大小的图片
        return photo_data["webformatURL"]
    
    def download_photo(self, photo_data: dict):
        """下载Pixabay图片"""
        photo_id = photo_data["id"]
        download_url = self.get_photo_url(photo_data)
        
        # 下载图片
        img_response = requests.get(download_url, timeout=15)
        if img_response.status_code != 200:
            raise Exception(f"图片下载失败: HTTP {img_response.status_code}")
        
        # 保存文件
        filename = f"raw/pixabay_{photo_id}.jpg"
        with open(filename, "wb") as f:
            f.write(img_response.content)
        
        return {
            "id": f"pixabay_{photo_id}",
            "filename": filename,
            "size": len(img_response.content),
            "platform": "pixabay"
        }

class MultiPlatformDownloader:
    """多平台下载器主类"""
    
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # 初始化各平台下载器
        self.downloaders = {}
        
        # Unsplash
        unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")
        if unsplash_key:
            self.downloaders["unsplash"] = UnsplashDownloader(unsplash_key)
            print("✅ Unsplash下载器已初始化")
        
        # Pexels
        pexels_key = os.getenv("PEXELS_API_KEY")
        if pexels_key:
            self.downloaders["pexels"] = PexelsDownloader(pexels_key)
            print("✅ Pexels下载器已初始化")
        
        # Pixabay
        pixabay_key = os.getenv("PIXABAY_API_KEY")
        if pixabay_key:
            self.downloaders["pixabay"] = PixabayDownloader(pixabay_key)
            print("✅ Pixabay下载器已初始化")
        
        if not self.downloaders:
            print("❌ 错误：请在.env文件中设置至少一个平台的API密钥")
            print("💡 支持的平台：UNSPLASH_ACCESS_KEY, PEXELS_API_KEY, PIXABAY_API_KEY")
            sys.exit(1)
        
        # 文件路径
        self.state_file = "download_state.json"
        self.downloaded_ids_file = "downloaded_ids.json"
        self.metadata_file = "metadata.json"
        
        # 创建必要目录
        Path("raw").mkdir(exist_ok=True)
        Path("png").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        
        # 初始化状态
        self.load_state()
        self.load_downloaded_ids()
        
        # 查询配置
        self.queries = [
            "laptop computer minimal",
            "smartphone mobile device", 
            "coffee cup workspace",
            "office supplies desk",
            "plant succulent office",
            "book notebook reading",
            "camera photography",
            "headphones audio tech",
            "modern furniture",
            "kitchen appliances",
            "fashion accessories",
            "sports equipment",
            "musical instruments",
            "art supplies",
            "garden tools"
        ]
        
        print(f"🚀 多平台下载器初始化完成")
        print(f"📂 工作目录: {os.getcwd()}")
        print(f"🔑 已配置平台: {list(self.downloaders.keys())}")
    
    def load_state(self):
        """加载下载状态"""
        if Path(self.state_file).exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                "last_run": None,
                "total_downloaded": 0,
                "requests_this_hour": 0,
                "hour_start": None,
                "current_query_index": 0,
                "current_platform_index": 0
            }
    
    def save_state(self):
        """保存状态"""
        self.state["last_run"] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def load_downloaded_ids(self):
        """加载已下载ID"""
        if Path(self.downloaded_ids_file).exists():
            with open(self.downloaded_ids_file, 'r') as f:
                self.downloaded_ids = set(json.load(f))
        else:
            self.downloaded_ids = set()
        
        print(f"📋 已记录 {len(self.downloaded_ids)} 个已下载图片")
    
    def save_downloaded_ids(self):
        """保存已下载ID"""
        with open(self.downloaded_ids_file, 'w') as f:
            json.dump(list(self.downloaded_ids), f)
    
    def check_api_limit(self):
        """检查API限制"""
        now = datetime.now()
        
        if self.state["hour_start"]:
            hour_start = datetime.fromisoformat(self.state["hour_start"])
            if now - hour_start >= timedelta(hours=1):
                # 重置计数器
                self.state["requests_this_hour"] = 0
                self.state["hour_start"] = now.isoformat()
        else:
            self.state["hour_start"] = now.isoformat()
        
        # 每小时限制100个请求（保守估计）
        return self.state["requests_this_hour"] < 90
    
    def download_batch(self, batch_size=15):
        """下载一批图片"""
        if not self.check_api_limit():
            remaining_time = 3600 - (datetime.now() - datetime.fromisoformat(self.state["hour_start"])).total_seconds()
            print(f"⏰ API限制已达上限，需等待 {remaining_time/60:.1f} 分钟")
            return 0
        
        # 选择平台和查询
        platforms = list(self.downloaders.keys())
        platform = platforms[self.state["current_platform_index"]]
        self.state["current_platform_index"] = (self.state["current_platform_index"] + 1) % len(platforms)
        
        query = self.queries[self.state["current_query_index"]]
        self.state["current_query_index"] = (self.state["current_query_index"] + 1) % len(self.queries)
        
        print(f"\n🔍 开始下载: {platform.upper()} - '{query}' (目标: {batch_size} 张)")
        
        downloaded = 0
        page = 1
        
        while downloaded < batch_size and self.check_api_limit():
            try:
                # 搜索图片
                print(f"📡 搜索第 {page} 页...")
                photos = self.downloaders[platform].search_photos(query, page, 30)
                self.state["requests_this_hour"] += 1
                
                if not photos:
                    print("📄 没有更多结果")
                    break
                
                print(f"✅ 找到 {len(photos)} 张图片")
                
                for i, photo in enumerate(photos):
                    if downloaded >= batch_size:
                        break
                    
                    try:
                        # 检查重复
                        photo_id = photo.get("id", f"{platform}_{i}")
                        if platform != "unsplash":
                            photo_id = f"{platform}_{photo_id}"
                        
                        if photo_id in self.downloaded_ids:
                            print(f"⏭️ 跳过重复图片: {photo_id}")
                            continue
                        
                        # 质量检查
                        if platform == "unsplash":
                            if photo["width"] < 1000 or photo["height"] < 1000:
                                print(f"⚠️ 跳过低质量图片: {photo_id}")
                                continue
                        
                        # 下载图片
                        result = self.downloaders[platform].download_photo(photo)
                        downloaded += 1
                        self.downloaded_ids.add(result["id"])
                        
                        # 保存元数据
                        self.save_image_metadata(photo, platform, result)
                        
                        print(f"✅ 已下载: {result['id']} ({downloaded}/{batch_size})")
                        
                        if not self.check_api_limit():
                            print("⚠️ 达到API限制")
                            break
                            
                    except Exception as e:
                        print(f"❌ 处理图片时出错: {e}")
                        continue
                
                page += 1
                
            except Exception as e:
                print(f"❌ 批次下载出错: {e}")
                break
        
        self.state["total_downloaded"] += downloaded
        self.save_state()
        self.save_downloaded_ids()
        
        print(f"\n🎉 本批次完成: {downloaded} 张")
        print(f"📊 总计下载: {self.state['total_downloaded']} 张")
        print(f"🔄 API使用: {self.state['requests_this_hour']}/90")
        
        return downloaded
    
    def save_image_metadata(self, photo: dict, platform: str, result: dict):
        """保存图片元数据"""
        try:
            # 加载现有元数据
            metadata = {}
            if Path(self.metadata_file).exists():
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
                if isinstance(metadata, list):
                    print("⚠️ metadata.json is a list, converting to dict.")
                    metadata = {}
            
            # 根据平台提取信息
            if platform == "unsplash":
                title = photo.get("description") or photo.get("alt_description") or f"Unsplash Image {photo['id']}"
                author = photo["user"]["name"]
                author_url = photo["user"]["links"]["html"]
                width = photo["width"]
                height = photo["height"]
                original_url = photo["links"]["html"]
            elif platform == "pexels":
                title = photo.get("alt", f"Pexels Image {photo['id']}")
                author = photo["photographer"]
                author_url = photo["photographer_url"]
                width = photo["width"]
                height = photo["height"]
                original_url = photo["url"]
            elif platform == "pixabay":
                title = photo.get("tags", f"Pixabay Image {photo['id']}")
                author = photo["user"]
                author_url = f"https://pixabay.com/users/{photo['user_id']}/"
                width = photo["imageWidth"]
                height = photo["imageHeight"]
                original_url = photo["pageURL"]
            
            # 添加新数据
            metadata[result["id"]] = {
                "id": result["id"],
                "title": title,
                "author": author,
                "author_url": author_url,
                "description": f"High-quality transparent background PNG image from {platform.title()}",
                "width": width,
                "height": height,
                "platform": platform,
                "original_url": original_url,
                "downloaded_at": datetime.now().isoformat(),
                "raw_path": result["filename"],
                "file_size": f"{result['size'] / 1024 / 1024:.1f}MB",
                "tags": [
                    "transparent",
                    "png",
                    "design",
                    "isolated",
                    "cutout",
                    platform
                ],
                "category": "general",
                "quality_score": 95,
                "transparent_ratio": 0.3,  # 默认值，后续处理时更新
                "copyright": {
                    "platform": platform,
                    "license": f"{platform}_license",
                    "attribution_required": False,
                    "commercial_allowed": True,
                    "modification_allowed": True
                }
            }
            
            # 保存元数据
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ 保存元数据失败: {e}")
    
    def process_images(self):
        """处理图片（去背景）"""
        try:
            from rembg import remove, new_session
            from PIL import Image
        except ImportError:
            print("❌ 缺少依赖，请运行：pip install rembg pillow")
            return
        
        print("\n🎨 开始去背景处理...")
        
        # 获取需要处理的图片
        raw_images = list(Path("raw").glob("*.jpg"))
        processed_images = set(p.stem for p in Path("png").glob("*.png"))
        
        to_process = [img for img in raw_images if img.stem not in processed_images]
        
        if not to_process:
            print("✅ 所有图片已处理完成")
            return
        
        print(f"📸 需要处理 {len(to_process)} 张图片")
        
        # 创建去背景会话
        session = new_session("u2net")
        
        for i, img_path in enumerate(to_process):
            try:
                print(f"🖼️ 处理中: {img_path.name} ({i+1}/{len(to_process)})")
                
                with Image.open(img_path) as img:
                    # 如果图片太大，先缩放
                    if max(img.size) > 2048:
                        ratio = 2048 / max(img.size)
                        new_size = tuple(int(dim * ratio) for dim in img.size)
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # 去背景
                    output = remove(img, session=session)
                    
                    # 保存PNG
                    png_path = f"png/{img_path.stem}.png"
                    output.save(png_path, "PNG", optimize=True)
                    
                    print(f"✅ 完成: {png_path}")
                
            except Exception as e:
                print(f"❌ 处理失败 {img_path.name}: {e}")
        
        print("🎉 图片处理完成！")

def main():
    parser = argparse.ArgumentParser(description="多平台透明PNG下载器")
    parser.add_argument("--download", type=int, default=0, help="下载图片数量")
    parser.add_argument("--process", action="store_true", help="处理图片（去背景）")
    parser.add_argument("--status", action="store_true", help="显示状态")
    parser.add_argument("--platform", choices=["unsplash", "pexels", "pixabay", "all"], default="all", help="指定平台")
    args = parser.parse_args()
    
    downloader = MultiPlatformDownloader()
    
    if args.status:
        print(f"\n📊 当前状态:")
        print(f"已下载: {downloader.state['total_downloaded']} 张")
        print(f"本小时请求: {downloader.state['requests_this_hour']}/90")
        print(f"原图文件: {len(list(Path('raw').glob('*.jpg')))}")
        print(f"PNG文件: {len(list(Path('png').glob('*.png')))}")
        print(f"可用平台: {list(downloader.downloaders.keys())}")
    
    elif args.download > 0:
        downloader.download_batch(args.download)
    
    elif args.process:
        downloader.process_images()
    
    else:
        print("\n🚀 多平台透明PNG下载器")
        print("使用方法:")
        print("  python multi_platform_downloader.py --download 20    # 下载20张图片")
        print("  python multi_platform_downloader.py --process        # 处理图片去背景")
        print("  python multi_platform_downloader.py --status         # 查看状态")
        print("  python multi_platform_downloader.py --platform pexels --download 10  # 指定平台")

if __name__ == "__main__":
    main() 