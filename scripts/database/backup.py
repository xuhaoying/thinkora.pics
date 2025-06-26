#!/usr/bin/env python3
"""
数据库备份和管理脚本
"""

import os
import shutil
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path
import json

class DatabaseManager:
    def __init__(self):
        self.db_path = Path("images.db")
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self):
        """创建数据库备份"""
        if not self.db_path.exists():
            print("❌ 数据库文件不存在")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"images_backup_{timestamp}.db"
        
        try:
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ 数据库备份成功: {backup_path}")
            
            # 创建备份信息文件
            info_path = backup_path.with_suffix('.json')
            backup_info = {
                "timestamp": timestamp,
                "original_file": str(self.db_path),
                "backup_file": str(backup_path),
                "file_size": backup_path.stat().st_size,
                "created_at": datetime.now().isoformat()
            }
            
            with open(info_path, 'w') as f:
                json.dump(backup_info, f, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False
    
    def list_backups(self):
        """列出所有备份文件"""
        backups = list(self.backup_dir.glob("images_backup_*.db"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not backups:
            print("📋 没有找到备份文件")
            return []
        
        print("📋 备份文件列表:")
        for backup in backups:
            stat = backup.stat()
            size_mb = stat.st_size / (1024 * 1024)
            mtime = datetime.fromtimestamp(stat.st_mtime)
            print(f"  {backup.name} ({size_mb:.1f}MB, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
        
        return backups
    
    def restore_backup(self, backup_file):
        """从备份恢复数据库"""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            print(f"❌ 备份文件不存在: {backup_path}")
            return False
        
        try:
            # 备份当前数据库
            if self.db_path.exists():
                current_backup = f"images_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(self.db_path, self.backup_dir / current_backup)
                print(f"📦 当前数据库已备份为: {current_backup}")
            
            # 恢复数据库
            shutil.copy2(backup_path, self.db_path)
            print(f"✅ 数据库恢复成功: {backup_path} -> {self.db_path}")
            return True
            
        except Exception as e:
            print(f"❌ 恢复失败: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count=10):
        """清理旧的备份文件"""
        backups = list(self.backup_dir.glob("images_backup_*.db"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if len(backups) <= keep_count:
            print(f"📋 当前有 {len(backups)} 个备份，无需清理")
            return 0
        
        to_delete = backups[keep_count:]
        deleted_count = 0
        
        for backup in to_delete:
            try:
                # 删除备份文件和对应的info文件
                backup.unlink()
                info_file = backup.with_suffix('.json')
                if info_file.exists():
                    info_file.unlink()
                deleted_count += 1
                print(f"🗑️ 删除旧备份: {backup.name}")
            except Exception as e:
                print(f"❌ 删除失败 {backup.name}: {e}")
        
        print(f"✅ 清理完成，删除了 {deleted_count} 个旧备份")
        return deleted_count
    
    def get_database_info(self):
        """获取数据库信息"""
        if not self.db_path.exists():
            return {"error": "数据库文件不存在"}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取表信息
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            info = {
                "file_path": str(self.db_path),
                "file_size": self.db_path.stat().st_size,
                "file_size_mb": self.db_path.stat().st_size / (1024 * 1024),
                "modified_time": datetime.fromtimestamp(self.db_path.stat().st_mtime).isoformat(),
                "tables": tables
            }
            
            # 获取images表的详细信息
            if 'images' in tables:
                cursor.execute("SELECT COUNT(*) FROM images")
                total_images = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM images WHERE processed = TRUE")
                processed_images = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM images WHERE uploaded = TRUE")
                uploaded_images = cursor.fetchone()[0]
                
                cursor.execute("SELECT source, COUNT(*) FROM images GROUP BY source")
                source_stats = dict(cursor.fetchall())
                
                info["images"] = {
                    "total": total_images,
                    "processed": processed_images,
                    "uploaded": uploaded_images,
                    "pending": total_images - processed_images,
                    "by_source": source_stats
                }
            
            conn.close()
            return info
            
        except Exception as e:
            return {"error": f"获取数据库信息失败: {e}"}
    
    def optimize_database(self):
        """优化数据库"""
        if not self.db_path.exists():
            print("❌ 数据库文件不存在")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            print("🔄 开始优化数据库...")
            
            # 创建索引
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_images_processed ON images(processed)",
                "CREATE INDEX IF NOT EXISTS idx_images_uploaded ON images(uploaded)",
                "CREATE INDEX IF NOT EXISTS idx_images_source ON images(source)",
                "CREATE INDEX IF NOT EXISTS idx_images_created_at ON images(created_at)"
            ]
            
            for index_sql in indexes:
                conn.execute(index_sql)
            
            # 执行VACUUM来重新组织数据库
            conn.execute("VACUUM")
            
            # 更新统计信息
            conn.execute("ANALYZE")
            
            conn.commit()
            conn.close()
            
            print("✅ 数据库优化完成")
            return True
            
        except Exception as e:
            print(f"❌ 优化失败: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="数据库管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 备份命令
    subparsers.add_parser("backup", help="创建数据库备份")
    
    # 列出备份
    subparsers.add_parser("list", help="列出所有备份")
    
    # 恢复备份
    restore_parser = subparsers.add_parser("restore", help="从备份恢复数据库")
    restore_parser.add_argument("backup_file", help="备份文件路径")
    
    # 清理备份
    cleanup_parser = subparsers.add_parser("cleanup", help="清理旧备份")
    cleanup_parser.add_argument("--keep", type=int, default=10, help="保留备份数量")
    
    # 数据库信息
    subparsers.add_parser("info", help="显示数据库信息")
    
    # 优化数据库
    subparsers.add_parser("optimize", help="优化数据库")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = DatabaseManager()
    
    if args.command == "backup":
        manager.create_backup()
    elif args.command == "list":
        manager.list_backups()
    elif args.command == "restore":
        manager.restore_backup(args.backup_file)
    elif args.command == "cleanup":
        manager.cleanup_old_backups(args.keep)
    elif args.command == "info":
        info = manager.get_database_info()
        if "error" in info:
            print(f"❌ {info['error']}")
        else:
            print("📊 数据库信息:")
            print(f"  文件路径: {info['file_path']}")
            print(f"  文件大小: {info['file_size_mb']:.1f}MB")
            print(f"  修改时间: {info['modified_time']}")
            print(f"  表数量: {len(info['tables'])}")
            
            if "images" in info:
                img_info = info["images"]
                print(f"\n📸 图片统计:")
                print(f"  总数: {img_info['total']}")
                print(f"  已处理: {img_info['processed']}")
                print(f"  已上传: {img_info['uploaded']}")
                print(f"  待处理: {img_info['pending']}")
                print(f"  来源分布: {img_info['by_source']}")
    elif args.command == "optimize":
        manager.optimize_database()

if __name__ == "__main__":
    main()