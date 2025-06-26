#!/usr/bin/env python3
"""
Thinkora Pics 快速管理脚本
简化的命令入口
"""

import sys
import subprocess
from pathlib import Path

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("🎯 Thinkora Pics 管理工具")
        print("\n📋 可用命令:")
        print("  health      - 系统健康检查")
        print("  fetch [N]   - 获取N张图片（默认50张）")
        print("  process     - 处理图片（去背景）")
        print("  upload      - 上传到R2存储")
        print("  pipeline [N]- 运行完整流水线")
        print("  backup      - 备份数据库")
        print("  stats       - 查看统计信息")
        print("\n📖 详细文档: scripts/README.md")
        return
    
    command = sys.argv[1]
    manager_script = Path("scripts/core/manager.py")
    
    if command == "health":
        subprocess.run([sys.executable, "scripts/utils/health_check.py"])
    elif command == "fetch":
        count = sys.argv[2] if len(sys.argv) > 2 else "50"
        subprocess.run([sys.executable, str(manager_script), "fetch", "--count", count])
    elif command == "process":
        subprocess.run([sys.executable, str(manager_script), "process"])
    elif command == "upload":
        subprocess.run([sys.executable, str(manager_script), "upload"])
    elif command == "pipeline":
        count = sys.argv[2] if len(sys.argv) > 2 else "50"
        subprocess.run([sys.executable, str(manager_script), "pipeline", "--count", count])
    elif command == "backup":
        subprocess.run([sys.executable, str(manager_script), "backup"])
    elif command == "stats":
        print("📊 系统统计:")
        subprocess.run([sys.executable, "scripts/images/process.py", "--stats"])
        subprocess.run([sys.executable, "scripts/deployment/upload_r2.py", "--stats"])
        subprocess.run([sys.executable, "scripts/database/backup.py", "info"])
    else:
        print(f"❌ 未知命令: {command}")
        print("运行 'python3 manage.py' 查看可用命令")

if __name__ == "__main__":
    main()