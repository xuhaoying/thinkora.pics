#!/usr/bin/env python3
"""
Thinkora Pics 核心管理脚本
统一管理所有操作的入口点
"""

import sys
import os
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

class ThinkoraManager:
    def __init__(self):
        self.scripts_dir = Path(__file__).parent.parent
        self.project_root = self.scripts_dir.parent
        
    def run_script(self, script_path, *args):
        """运行指定脚本"""
        cmd = [sys.executable, str(script_path)] + list(args)
        print(f"🚀 执行: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True, 
                                  capture_output=True, text=True)
            print(f"✅ 成功完成: {script_path.name}")
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 执行失败: {script_path.name}")
            print(f"错误: {e.stderr}")
            return False
    
    def fetch_images(self, count=100, source="both"):
        """获取新图片"""
        script = self.scripts_dir / "images" / "fetch.py"
        return self.run_script(script, "--count", str(count), "--source", source)
    
    def process_images(self, batch_size=50):
        """处理图片（去背景）"""
        script = self.scripts_dir / "images" / "process.py"
        return self.run_script(script, "--batch-size", str(batch_size))
    
    def upload_to_r2(self, force=False):
        """上传到R2存储"""
        script = self.scripts_dir / "deployment" / "upload_r2.py"
        args = ["--force"] if force else []
        return self.run_script(script, *args)
    
    def backup_database(self):
        """备份数据库"""
        script = self.scripts_dir / "database" / "backup.py"
        return self.run_script(script)
    
    def check_health(self):
        """健康检查"""
        script = self.scripts_dir / "utils" / "health_check.py"
        return self.run_script(script)
    
    def run_full_pipeline(self, count=50):
        """运行完整的图片处理流水线"""
        print("🔄 开始完整的图片处理流水线...")
        
        steps = [
            ("获取图片", lambda: self.fetch_images(count)),
            ("处理图片", lambda: self.process_images()),
            ("上传到R2", lambda: self.upload_to_r2()),
            ("备份数据库", lambda: self.backup_database()),
            ("健康检查", lambda: self.check_health()),
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 步骤: {step_name}")
            if not step_func():
                print(f"❌ 流水线在 '{step_name}' 步骤失败")
                return False
        
        print("\n✅ 完整流水线执行成功!")
        return True

def main():
    parser = argparse.ArgumentParser(description="Thinkora Pics 管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 获取图片
    fetch_parser = subparsers.add_parser("fetch", help="获取新图片")
    fetch_parser.add_argument("--count", type=int, default=100, help="获取图片数量")
    fetch_parser.add_argument("--source", choices=["unsplash", "pixabay", "both"], 
                             default="both", help="图片来源")
    
    # 处理图片
    process_parser = subparsers.add_parser("process", help="处理图片")
    process_parser.add_argument("--batch-size", type=int, default=50, help="批处理大小")
    
    # 上传到R2
    upload_parser = subparsers.add_parser("upload", help="上传到R2")
    upload_parser.add_argument("--force", action="store_true", help="强制重新上传")
    
    # 备份
    subparsers.add_parser("backup", help="备份数据库")
    
    # 健康检查
    subparsers.add_parser("health", help="系统健康检查")
    
    # 完整流水线
    pipeline_parser = subparsers.add_parser("pipeline", help="运行完整流水线")
    pipeline_parser.add_argument("--count", type=int, default=50, help="处理图片数量")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = ThinkoraManager()
    
    if args.command == "fetch":
        manager.fetch_images(args.count, args.source)
    elif args.command == "process":
        manager.process_images(args.batch_size)
    elif args.command == "upload":
        manager.upload_to_r2(args.force)
    elif args.command == "backup":
        manager.backup_database()
    elif args.command == "health":
        manager.check_health()
    elif args.command == "pipeline":
        manager.run_full_pipeline(args.count)

if __name__ == "__main__":
    main()