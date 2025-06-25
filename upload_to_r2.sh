#!/bin/bash
# R2批量上传脚本
# 生成时间: 2025-06-24 21:10:03
# 上传 89 个文件

echo '🚀 开始上传图片到R2...'

# 方法1: 批量上传整个目录（推荐）
rclone copy raw/pixabay r2:thinkora-pics/images \
  --include '*.jpg' \
  --include '*.jpeg' \
  --include '*.png' \
  --s3-acl public-read \
  --transfers 8 \
  --progress

# 方法2: 单个文件上传（可选）
# COUNT=0
# TOTAL=89
# rclone copy raw/pixabay/pixabay_1052023.jpg r2:thinkora-pics/images/ --s3-acl public-read
# rclone copy raw/pixabay/pixabay_1229893.jpg r2:thinkora-pics/images/ --s3-acl public-read
# rclone copy raw/pixabay/pixabay_1238598.jpg r2:thinkora-pics/images/ --s3-acl public-read
# rclone copy raw/pixabay/pixabay_1282241.jpg r2:thinkora-pics/images/ --s3-acl public-read
# rclone copy raw/pixabay/pixabay_1284248.jpg r2:thinkora-pics/images/ --s3-acl public-read
# ...

echo '✅ 上传完成!'
echo '📊 验证上传结果:'
rclone size r2:thinkora-pics
