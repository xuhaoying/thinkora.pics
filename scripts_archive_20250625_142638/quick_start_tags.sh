#!/bin/bash

# 快速启动脚本 - 获取带标签的图片并更新数据库

echo "🚀 ThinkOra.pics 标签系统快速启动"
echo "=================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. 检查环境
echo -e "\n${YELLOW}1. 检查环境...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

if [ ! -f ".env" ] && [ ! -f "unsplash/.env" ]; then
    echo -e "${RED}❌ 未找到 .env 文件${NC}"
    echo "请创建 .env 文件并添加以下内容："
    echo "UNSPLASH_ACCESS_KEY=你的Unsplash密钥"
    echo "PIXABAY_API_KEY=你的Pixabay密钥"
    exit 1
fi

echo -e "${GREEN}✅ 环境检查通过${NC}"

# 2. 创建必要目录
echo -e "\n${YELLOW}2. 创建必要目录...${NC}"
mkdir -p logs raw/unsplash raw/pixabay
echo -e "${GREEN}✅ 目录创建完成${NC}"

# 3. 获取带标签的图片
echo -e "\n${YELLOW}3. 开始获取带标签的高质量图片...${NC}"
echo "这可能需要几分钟时间..."

python3 scripts/fetch_tagged_images.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 图片获取失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 图片获取完成${NC}"

# 4. 更新数据库
echo -e "\n${YELLOW}4. 更新数据库...${NC}"
echo "将导入新图片并清理无标签数据..."

python3 scripts/clean_and_update_db.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 数据库更新失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 数据库更新完成${NC}"

# 5. 验证结果
echo -e "\n${YELLOW}5. 验证标签系统...${NC}"

python3 scripts/verify_tags.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 验证失败${NC}"
    exit 1
fi

# 6. 显示摘要
echo -e "\n${GREEN}🎉 恭喜！标签系统更新完成！${NC}"
echo "=================================="
echo "📊 更新摘要："

# 显示数据库统计
sqlite3 thinkora.db "SELECT 
    '  - 总图片数: ' || COUNT(*) || ' 张' as stat FROM images
UNION ALL
SELECT 
    '  - 有标签图片: ' || COUNT(*) || ' 张' FROM images WHERE tags != '[]'
UNION ALL
SELECT 
    '  - 平均标签数: ' || ROUND(AVG(json_array_length(tags)), 1) || ' 个' 
    FROM images WHERE tags != '[]';"

echo -e "\n${YELLOW}下一步建议:${NC}"
echo "1. 运行 'npm run dev' 查看网站效果"
echo "2. 查看 logs/ 目录下的详细报告"
echo "3. 使用搜索功能测试标签系统"
echo ""
echo "💡 提示: 可以定期运行此脚本来获取更多带标签的图片"