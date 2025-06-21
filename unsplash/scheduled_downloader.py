import os
import json
import requests
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Set
import argparse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class DownloadConfig:
    """下载配置"""
    max_requests_per_hour: int = 45
    batch_size: int = 15  # 每次下载的图片数
    min_resolution: int = 1000  # 最小分辨率
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    quality_threshold: float = 0.7  # 质量阈值

class ImageDownloader:
    def __init__(self, config: DownloadConfig):
        self.config = config
        self.access_key = os.getenv("ACCESS_KEY")
        self.state_file = "download_state.json"
        self.metadata_file = "metadata.json"
        self.downloaded_ids_file = "downloaded_ids.json"
        
        # 初始化状态
        self.load_state()
        self.load_downloaded_ids()
        
        # 查询队列（轮换使用）
        self.query_queue = [
            {"query": "laptop computer minimal", "priority": 10},
            {"query": "smartphone mobile device", "priority": 9},
            {"query": "coffee cup workspace", "priority": 8},
            {"query": "office supplies desk", "priority": 7},
            {"query": "plant succulent decoration", "priority": 6},
            {"query": "book notebook reading", "priority": 5},
            {"query": "camera photography equipment", "priority": 4},
            {"query": "headphones audio technology", "priority": 3},
            {"query": "watch clock time", "priority": 2},
            {"query": "keyboard mouse tech", "priority": 1},
        ]
        
    def load_state(self):
        """加载下载状态"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                "last_run": None,
                "current_query_index": 0,
                "total_downloaded": 0,
                "last_hour_requests": 0,
                "last_hour_start": None,
                "failed_downloads": [],
                "query_stats": {}
            }
    
    def save_state(self):
        """保存下载状态"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def load_downloaded_ids(self):
        """加载已下载图片ID列表"""
        if os.path.exists(self.downloaded_ids_file):
            with open(self.downloaded_ids_file, 'r') as f:
                self.downloaded_ids = set(json.load(f))
        else:
            self.downloaded_ids = set()
        
        logging.info(f"已加载 {len(self.downloaded_ids)} 个已下载图片ID")
    
    def save_downloaded_ids(self):
        """保存已下载图片ID列表"""
        with open(self.downloaded_ids_file, 'w') as f:
            json.dump(list(self.downloaded_ids), f)
    
    def load_metadata(self):
        """加载现有元数据"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_metadata(self, metadata):
        """保存元数据"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def can_make_requests(self) -> bool:
        """检查是否可以继续发送请求"""
        now = datetime.now()
        
        # 检查是否是新的一小时
        if self.state["last_hour_start"]:
            last_hour = datetime.fromisoformat(self.state["last_hour_start"])
            if now - last_hour >= timedelta(hours=1):
                # 重置计数器
                self.state["last_hour_requests"] = 0
                self.state["last_hour_start"] = now.isoformat()
        else:
            self.state["last_hour_start"] = now.isoformat()
        
        return self.state["last_hour_requests"] < self.config.max_requests_per_hour
    
    def calculate_image_hash(self, img_data: bytes) -> str:
        """计算图片哈希值用于去重"""
        return hashlib.md5(img_data).hexdigest()
    
    def is_high_quality_image(self, photo: dict) -> bool:
        """判断图片是否符合质量要求"""
        # 检查分辨率
        if photo["width"] < self.config.min_resolution or photo["height"] < self.config.min_resolution:
            return False
        
        # 检查宽高比（避免过于极端的比例）
        ratio = max(photo["width"], photo["height"]) / min(photo["width"], photo["height"])
        if ratio > 5:  # 宽高比超过5:1
            return False
        
        # 检查描述质量（有描述的通常质量更好）
        has_description = bool(photo.get("description") or photo.get("alt_description"))
        
        # 检查作者活跃度（下载量高的作者通常质量更好）
        author_downloads = photo["user"].get("total_photos", 0)
        
        # 综合评分
        quality_score = 0.5  # 基础分
        if has_description:
            quality_score += 0.2
        if author_downloads > 100:
            quality_score += 0.2
        if photo["likes"] > 50:
            quality_score += 0.1
        
        return quality_score >= self.config.quality_threshold
    
    def get_next_query(self) -> dict:
        """获取下一个查询"""
        query_info = self.query_queue[self.state["current_query_index"]]
        
        # 更新索引（循环）
        self.state["current_query_index"] = (self.state["current_query_index"] + 1) % len(self.query_queue)
        
        return query_info
    
    def download_batch(self) -> int:
        """下载一批图片"""
        if not self.can_make_requests():
            logging.warning("已达到API请求限制，跳过本次下载")
            return 0
        
        query_info = self.get_next_query()
        query = query_info["query"]
        
        logging.info(f"开始下载批次: '{query}'")
        
        # 创建目录
        Path("raw").mkdir(exist_ok=True)
        
        # 加载现有元数据
        metadata = self.load_metadata()
        
        downloaded_count = 0
        page = 1
        
        while downloaded_count < self.config.batch_size and self.can_make_requests():
            try:
                # 搜索请求
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
                response.raise_for_status()
                self.state["last_hour_requests"] += 1
                
                results = response.json()["results"]
                if not results:
                    logging.info(f"查询 '{query}' 第 {page} 页无更多结果")
                    break
                
                for photo in results:
                    if downloaded_count >= self.config.batch_size:
                        break
                    
                    # 多层去重检查
                    if self.is_duplicate(photo):
                        continue
                    
                    # 质量检查
                    if not self.is_high_quality_image(photo):
                        logging.debug(f"跳过低质量图片: {photo['id']}")
                        continue
                    
                    # 下载图片
                    success = self.download_single_image(photo, metadata)
                    if success:
                        downloaded_count += 1
                        self.downloaded_ids.add(photo["id"])
                        logging.info(f"成功下载: {photo['id']} ({downloaded_count}/{self.config.batch_size})")
                    
                    if not self.can_make_requests():
                        logging.warning("API请求达到限制，停止下载")
                        break
                
                page += 1
                
            except Exception as e:
                logging.error(f"搜索请求失败: {e}")
                break
        
        # 更新统计
        if query not in self.state["query_stats"]:
            self.state["query_stats"][query] = {"downloaded": 0, "last_run": None}
        
        self.state["query_stats"][query]["downloaded"] += downloaded_count
        self.state["query_stats"][query]["last_run"] = datetime.now().isoformat()
        self.state["total_downloaded"] += downloaded_count
        
        # 保存状态和数据
        self.save_state()
        self.save_downloaded_ids()
        self.save_metadata(metadata)
        
        logging.info(f"批次完成: 下载了 {downloaded_count} 张图片")
        return downloaded_count
    
    def is_duplicate(self, photo: dict) -> bool:
        """检查是否为重复图片"""
        # 1. ID去重
        if photo["id"] in self.downloaded_ids:
            return True
        
        # 2. URL去重（检查原始URL）
        # 这里可以添加更复杂的重复检测逻辑
        
        return False
    
    def download_single_image(self, photo: dict, metadata: dict) -> bool:
        """下载单张图片"""
        try:
            # 下载图片
            img_response = requests.get(photo["urls"]["regular"], timeout=15)
            img_response.raise_for_status()
            
            # 检查文件大小
            if len(img_response.content) > self.config.max_file_size:
                logging.warning(f"图片 {photo['id']} 过大，跳过")
                return False
            
            # 保存文件
            raw_path = f"raw/{photo['id']}.jpg"
            with open(raw_path, "wb") as f:
                f.write(img_response.content)
            
            # 发送下载统计请求（必需）
            if self.can_make_requests():
                requests.get(
                    photo["links"]["download_location"],
                    headers={"Authorization": f"Client-ID {self.access_key}"},
                    timeout=5
                )
                self.state["last_hour_requests"] += 1
            
            # 生成元数据
            metadata[photo["id"]] = {
                "id": photo["id"],
                "title": photo.get("description") or photo.get("alt_description") or f"Image {photo['id']}",
                "author": photo["user"]["name"],
                "author_url": photo["user"]["links"]["html"],
                "description": photo.get("description", ""),
                "width": photo["width"],
                "height": photo["height"],
                "likes": photo.get("likes", 0),
                "unsplash_url": photo["links"]["html"],
                "download_url": photo["urls"]["regular"],
                "raw_path": raw_path,
                "downloaded_at": datetime.now().isoformat(),
                "file_size": len(img_response.content),
                "file_hash": self.calculate_image_hash(img_response.content)
            }
            
            return True
            
        except Exception as e:
            logging.error(f"下载图片 {photo['id']} 失败: {e}")
            self.state["failed_downloads"].append({
                "id": photo["id"],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def run_continuous(self, hours: int = 24):
        """连续运行指定小时数"""
        end_time = datetime.now() + timedelta(hours=hours)
        
        logging.info(f"开始连续运行 {hours} 小时")
        
        while datetime.now() < end_time:
            try:
                if self.can_make_requests():
                    downloaded = self.download_batch()
                    if downloaded > 0:
                        logging.info(f"本次下载 {downloaded} 张，总计 {self.state['total_downloaded']} 张")
                else:
                    # 等待到下一小时
                    if self.state["last_hour_start"]:
                        last_hour = datetime.fromisoformat(self.state["last_hour_start"])
                        wait_time = 3600 - (datetime.now() - last_hour).total_seconds()
                        if wait_time > 0:
                            logging.info(f"等待 {wait_time/60:.1f} 分钟到下一小时")
                            time.sleep(min(wait_time + 60, 300))  # 最多等5分钟
                
                # 每次间隔5-10分钟
                time.sleep(300 + (hash(str(datetime.now())) % 300))
                
            except KeyboardInterrupt:
                logging.info("收到中断信号，正在停止...")
                break
            except Exception as e:
                logging.error(f"运行出错: {e}")
                time.sleep(60)  # 出错后等待1分钟
        
        logging.info("连续运行结束")
    
    def print_stats(self):
        """打印统计信息"""
        print("\n📊 下载统计:")
        print(f"总下载数: {self.state['total_downloaded']}")
        print(f"本小时请求数: {self.state['last_hour_requests']}/{self.config.max_requests_per_hour}")
        print(f"失败下载数: {len(self.state['failed_downloads'])}")
        
        print("\n📈 查询统计:")
        for query, stats in self.state["query_stats"].items():
            print(f"  {query}: {stats['downloaded']} 张")

def main():
    parser = argparse.ArgumentParser(description="定时图片下载器")
    parser.add_argument("--mode", choices=["single", "continuous"], default="single",
                       help="运行模式：single=单次，continuous=连续")
    parser.add_argument("--hours", type=int, default=24,
                       help="连续模式运行小时数")
    parser.add_argument("--batch-size", type=int, default=15,
                       help="每批下载图片数")
    args = parser.parse_args()
    
    # 检查API密钥
    if not os.getenv("ACCESS_KEY"):
        print("❌ 请设置 ACCESS_KEY 环境变量")
        return
    
    # 创建配置
    config = DownloadConfig(batch_size=args.batch_size)
    downloader = ImageDownloader(config)
    
    # 运行
    if args.mode == "single":
        downloaded = downloader.download_batch()
        print(f"✅ 单次运行完成，下载了 {downloaded} 张图片")
    else:
        downloader.run_continuous(args.hours)
    
    # 显示统计
    downloader.print_stats()

if __name__ == "__main__":
    main()