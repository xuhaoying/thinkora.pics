#!/bin/bash
# 使用rclone批量删除R2文件
# 确保已配置rclone: rclone config

echo "🧹 使用rclone清理R2存储桶..."
echo "将尝试删除 530 个文件路径"

# 批量删除（更高效）
rclone delete r2:thinkora-pics --include-from r2_files_to_delete.txt --dry-run

echo ""
echo "⚠️ 以上是试运行结果"
echo "要实际删除，请去掉 --dry-run 参数："
echo "rclone delete r2:thinkora-pics --include-from r2_files_to_delete.txt"
