#!/bin/bash

echo "🔍 检查R2公开访问..."
echo "================================"

# R2 公开URL
R2_PUBLIC_URL="https://pub-484484e3162047379f59bcbb36fb442a.r2.dev"

# 测试图片列表
test_images=(
    "0V3uVjouHRc.png"
    "0o6Lqin4nNE.png"
    "5EgJ-mUklbg.png"
    "-lkFmMG1BP0.png"
)

echo "测试URL: $R2_PUBLIC_URL"
echo ""

for img in "${test_images[@]}"; do
    url="$R2_PUBLIC_URL/images/$img"
    echo -n "检查 $img ... "
    
    # 使用curl检查
    status=$(curl -s -o /dev/null -w "%{http_code}" -I "$url" --max-time 5)
    
    if [ "$status" = "200" ]; then
        echo "✅ 可访问 (HTTP $status)"
    elif [ "$status" = "000" ]; then
        echo "❌ 连接失败"
    else
        echo "❌ HTTP $status"
    fi
done

echo ""
echo "💡 诊断建议："
echo "1. 如果所有都显示'连接失败'，可能是R2公开访问未正确配置"
echo "2. 如果显示403，需要在Cloudflare中启用Public Access"
echo "3. 如果显示404，说明文件不存在或路径不正确"
echo ""
echo "📋 在Cloudflare Dashboard中检查："
echo "   - R2 > 你的bucket > Settings > Public Access"
echo "   - 确保'Enable Public Access'已开启"
echo "   - 确认Public bucket URL是: $R2_PUBLIC_URL"