#!/bin/bash
# 使用AWS CLI上传图片到R2
# 生成时间: 2025-06-24

echo "🚀 使用AWS CLI上传图片到R2..."

# R2配置
BUCKET="thinkora-pics"
ENDPOINT="https://d37e2728a4daeb263e7a08a066e80926.r2.cloudflarestorage.com"
REGION="auto"

# 检查AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI未安装"
    echo "请运行: brew install awscli"
    exit 1
fi

# 设置计数器
COUNT=0
TOTAL=$(ls raw/pixabay/*.jpg 2>/dev/null | wc -l)

echo "📸 找到 $TOTAL 个图片文件"
echo ""

# 上传所有pixabay图片
for file in raw/pixabay/*.jpg; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        COUNT=$((COUNT + 1))
        
        echo -n "[$COUNT/$TOTAL] 上传: $filename ... "
        
        # 上传文件
        aws s3 cp "$file" "s3://$BUCKET/images/$filename" \
            --endpoint-url="$ENDPOINT" \
            --region="$REGION" \
            --acl public-read \
            2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "✅"
        else
            echo "❌"
        fi
    fi
done

echo ""
echo "✅ 上传完成! 共上传 $COUNT 个文件"

# 列出上传的文件
echo ""
echo "📊 验证上传结果:"
aws s3 ls "s3://$BUCKET/images/" \
    --endpoint-url="$ENDPOINT" \
    --region="$REGION" | wc -l