#!/usr/bin/env python3
"""
Mac 本地透明PNG下载器
适配 macOS 环境，包含完整的错误处理和进度显示
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

# macOS 特定配置
if sys.platform == "darwin":
    # 禁用 OpenMP 警告（macOS 常见问题）
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

class MacDownloader:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        self.access_key = os.getenv("ACCESS_KEY")
        if not self.access_key:
            print("❌ 错误：请在 .env 文件中设置 ACCESS_KEY")
            print("💡 获取方式：https://unsplash.com/developers")
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
            "headphones audio tech"
        ]
        
        print(f"🍎 Mac 下载器初始化完成")
        print(f"📂 工作目录: {os.getcwd()}")
        print(f"🔑 API密钥: {self.access_key[:10]}...")
    
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
                "current_query_index": 0
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
        
        return self.state["requests_this_hour"] < 45  # 留5个请求的余量
    
    def download_batch(self, batch_size=15):
        """下载一批图片"""
        if not self.check_api_limit():
            remaining_time = 3600 - (datetime.now() - datetime.fromisoformat(self.state["hour_start"])).total_seconds()
            print(f"⏰ API限制已达上限，需等待 {remaining_time/60:.1f} 分钟")
            return 0
        
        # 选择查询
        query = self.queries[self.state["current_query_index"]]
        self.state["current_query_index"] = (self.state["current_query_index"] + 1) % len(self.queries)
        
        print(f"\n🔍 开始下载: '{query}' (目标: {batch_size} 张)")
        
        downloaded = 0
        page = 1
        
        while downloaded < batch_size and self.check_api_limit():
            try:
                # API请求
                print(f"📡 搜索第 {page} 页...")
                response = requests.get(
                    "https://api.unsplash.com/search/photos",
                    params={
                        "query": query,
                        "per_page": 30,
                        "page": page,
                        "order_by": "relevant"
                    },
                    headers={"Authorization": f"Client-ID {self.access_key}"},
                    timeout=10
                )
                
                if response.status_code != 200:
                    print(f"❌ API请求失败: {response.status_code}")
                    break
                
                self.state["requests_this_hour"] += 1
                results = response.json().get("results", [])
                
                if not results:
                    print("📄 没有更多结果")
                    break
                
                print(f"✅ 找到 {len(results)} 张图片")
                
                for photo in results:
                    if downloaded >= batch_size:
                        break
                    
                    # 检查重复
                    if photo["id"] in self.downloaded_ids:
                        continue
                    
                    # 质量检查
                    if photo["width"] < 1000 or photo["height"] < 1000:
                        continue
                    
                    # 下载图片
                    if self.download_single_image(photo):
                        downloaded += 1
                        self.downloaded_ids.add(photo["id"])
                        print(f"✅ 已下载: {photo['id']} ({downloaded}/{batch_size})")
                    
                    if not self.check_api_limit():
                        print("⚠️ 达到API限制")
                        break
                
                page += 1
                
            except Exception as e:
                print(f"❌ 错误: {e}")
                break
        
        self.state["total_downloaded"] += downloaded
        self.save_state()
        self.save_downloaded_ids()
        
        print(f"\n🎉 本批次完成: {downloaded} 张")
        print(f"📊 总计下载: {self.state['total_downloaded']} 张")
        print(f"🔄 API使用: {self.state['requests_this_hour']}/45")
        
        return downloaded
    
    def download_single_image(self, photo):
        """下载单张图片"""
        try:
            # 下载图片
            img_response = requests.get(photo["urls"]["regular"], timeout=15)
            if img_response.status_code != 200:
                return False
            
            # 保存文件
            filename = f"raw/{photo['id']}.jpg"
            with open(filename, "wb") as f:
                f.write(img_response.content)
            
            # 发送下载统计（必需）
            if self.check_api_limit():
                requests.get(
                    photo["links"]["download_location"],
                    headers={"Authorization": f"Client-ID {self.access_key}"},
                    timeout=5
                )
                self.state["requests_this_hour"] += 1
            
            # 保存元数据
            self.save_image_metadata(photo)
            
            return True
            
        except Exception as e:
            print(f"⚠️ 下载失败 {photo['id']}: {e}")
            return False
    
    def save_image_metadata(self, photo):
        """保存图片元数据"""
        # 加载现有元数据
        metadata = {}
        if Path(self.metadata_file).exists():
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
        
        # 添加新数据
        metadata[photo["id"]] = {
            "id": photo["id"],
            "title": photo.get("description") or photo.get("alt_description") or f"Image {photo['id']}",
            "author": photo["user"]["name"],
            "author_url": photo["user"]["links"]["html"],
            "description": photo.get("description", ""),
            "width": photo["width"],
            "height": photo["height"],
            "unsplash_url": photo["links"]["html"],
            "downloaded_at": datetime.now().isoformat(),
            "raw_path": f"raw/{photo['id']}.jpg"
        }
        
        # 保存元数据
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
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
    parser = argparse.ArgumentParser(description="Mac 本地图片下载器")
    parser.add_argument("--download", type=int, default=0, help="下载图片数量")
    parser.add_argument("--process", action="store_true", help="处理图片（去背景）")
    parser.add_argument("--status", action="store_true", help="显示状态")
    args = parser.parse_args()
    
    downloader = MacDownloader()
    
    if args.status:
        print(f"\n📊 当前状态:")
        print(f"已下载: {downloader.state['total_downloaded']} 张")
        print(f"本小时请求: {downloader.state['requests_this_hour']}/45")
        print(f"原图文件: {len(list(Path('raw').glob('*.jpg')))}")
        print(f"PNG文件: {len(list(Path('png').glob('*.png')))}")
    
    elif args.download > 0:
        downloader.download_batch(args.download)
    
    elif args.process:
        downloader.process_images()
    
    else:
        print("\n🍎 Mac 透明PNG下载器")
        print("使用方法:")
        print("  python mac_downloader.py --download 20    # 下载20张图片")
        print("  python mac_downloader.py --process        # 处理图片去背景")
        print("  python mac_downloader.py --status         # 查看状态")

if __name__ == "__main__":
    main()