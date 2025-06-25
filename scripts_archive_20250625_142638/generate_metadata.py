#!/usr/bin/env python3
"""
生成符合PRD规范的元数据文件
包含维度、文件大小、质量分数、中文标签等信息
"""

import json
import os
from datetime import datetime
from PIL import Image
import hashlib

# 中英文标签映射
TAG_MAPPING = {
    'laptop': '笔记本电脑',
    'computer': '电脑',
    'technology': '科技',
    'tech': '科技',
    'work': '工作',
    'office': '办公',
    'minimal': '简约',
    'business': '商务',
    'workspace': '工作空间',
    'desk': '桌面',
    'keyboard': '键盘',
    'screen': '屏幕',
    'display': '显示器',
    'device': '设备',
    'gadget': '配件',
    'electronics': '电子产品',
    'digital': '数字',
    'modern': '现代',
    'design': '设计',
    'product': '产品',
    'professional': '专业',
    'productivity': '生产力',
    'mobile': '移动设备',
    'phone': '手机',
    'smartphone': '智能手机',
    'tablet': '平板',
    'camera': '相机',
    'headphones': '耳机',
    'speaker': '音响',
    'mouse': '鼠标',
    'accessories': '配件',
    'white': '白色',
    'black': '黑色',
    'silver': '银色',
    'gray': '灰色',
    'clean': '干净',
    'simple': '简单',
    'elegant': '优雅',
    'premium': '高端',
    'wireless': '无线',
    'portable': '便携',
    'home': '家居',
    'studio': '工作室',
    'creative': '创意',
    'innovation': '创新',
    'smart': '智能',
    'connected': '互联',
    'lifestyle': '生活方式',
    'communication': '通讯',
    'entertainment': '娱乐',
    'gaming': '游戏',
    'audio': '音频',
    'video': '视频',
    'photography': '摄影',
    'coding': '编程',
    'development': '开发',
    'software': '软件',
    'hardware': '硬件',
    'apple': '苹果',
    'mac': 'Mac',
    'windows': 'Windows',
    'android': '安卓',
    'ios': 'iOS'
}

# 类别映射
CATEGORY_KEYWORDS = {
    'electronics': ['laptop', 'computer', 'phone', 'tablet', 'camera', 'headphones', 'speaker', 'mouse', 'keyboard', 'monitor', 'device', 'gadget', 'tech', 'digital', 'hardware'],
    'office': ['desk', 'workspace', 'office', 'professional', 'business', 'productivity', 'work'],
    'lifestyle': ['home', 'lifestyle', 'living', 'interior', 'decor', 'modern', 'minimal'],
    'accessories': ['accessories', 'cable', 'charger', 'adapter', 'case', 'cover', 'stand'],
    'audio': ['headphones', 'speaker', 'audio', 'music', 'sound'],
    'photography': ['camera', 'photography', 'photo', 'lens'],
    'mobile': ['phone', 'smartphone', 'mobile', 'tablet', 'cellular']
}

def calculate_quality_score(image_path, png_path):
    """计算图片质量分数"""
    try:
        with Image.open(png_path) as img:
            width, height = img.size
            
            # 基础分数
            score = 70
            
            # 分辨率加分
            if width >= 1920 or height >= 1920:
                score += 15
            elif width >= 1280 or height >= 1280:
                score += 10
            elif width >= 800 or height >= 800:
                score += 5
            
            # 长宽比加分（接近常见比例）
            ratio = width / height
            common_ratios = [16/9, 4/3, 1/1, 3/2, 2/3]
            if any(abs(ratio - r) < 0.1 for r in common_ratios):
                score += 10
            
            # 透明度检测
            if img.mode == 'RGBA':
                alpha = img.getchannel('A')
                alpha_data = list(alpha.getdata())
                transparent_pixels = sum(1 for p in alpha_data if p < 255)
                transparent_ratio = transparent_pixels / len(alpha_data)
                
                # 合理的透明区域加分
                if 0.2 <= transparent_ratio <= 0.8:
                    score += 5
            
            return min(score, 95)  # 最高95分
    except:
        return 75  # 默认分数

def get_file_size_mb(file_path):
    """获取文件大小（MB）"""
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return f"{size_mb:.1f}MB"
    except:
        return "Unknown"

def determine_category(tags, title, description):
    """根据标签确定类别"""
    text = f"{' '.join(tags)} {title} {description}".lower()
    
    # 计算每个类别的匹配分数
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score > 0:
            category_scores[category] = score
    
    # 返回得分最高的类别
    if category_scores:
        return max(category_scores, key=category_scores.get)
    return 'others'

def enhance_tags(original_tags):
    """增强标签，添加中文翻译"""
    enhanced_tags = []
    seen = set()
    
    for tag in original_tags:
        # 处理原始标签
        if isinstance(tag, dict):
            tag_text = tag.get('tag', '').lower()
        else:
            tag_text = str(tag).lower()
        
        if tag_text and tag_text not in seen:
            seen.add(tag_text)
            # 添加英文标签
            enhanced_tags.append(tag_text)
            
            # 添加中文翻译
            if tag_text in TAG_MAPPING:
                chinese_tag = TAG_MAPPING[tag_text]
                if chinese_tag not in seen:
                    seen.add(chinese_tag)
                    enhanced_tags.append(chinese_tag)
    
    return enhanced_tags[:10]  # 限制最多10个标签

def generate_enhanced_metadata():
    """生成增强的元数据"""
    # 读取原始元数据
    with open('metadata_raw.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    enhanced_data = []
    
    for filename, img_data in raw_data.items():
        # 基础ID
        image_id = filename.replace('.jpg', '')
        png_filename = f"{image_id}.png"
        png_path = os.path.join('png', png_filename)
        
        # 获取图片尺寸
        dimensions = {"width": 1920, "height": 1280, "ratio": "3:2"}  # 默认值
        transparent_ratio = 0.35  # 默认值
        
        if os.path.exists(png_path):
            try:
                with Image.open(png_path) as img:
                    width, height = img.size
                    ratio = f"{width//100}:{height//100}" if width > height else f"{height//100}:{width//100}"
                    dimensions = {
                        "width": width,
                        "height": height,
                        "ratio": ratio
                    }
                    
                    # 计算透明度比例
                    if img.mode == 'RGBA':
                        alpha = img.getchannel('A')
                        alpha_data = list(alpha.getdata())
                        transparent_pixels = sum(1 for p in alpha_data if p < 255)
                        transparent_ratio = round(transparent_pixels / len(alpha_data), 2)
            except:
                pass
        
        # 增强标签
        original_tags = img_data.get('tags', [])
        enhanced_tags = enhance_tags(original_tags)
        
        # 确定类别
        title = img_data.get('description', '').split('.')[0]  # 第一句作为标题
        description = img_data.get('description', '')
        category = determine_category(enhanced_tags, title, description)
        
        # 计算质量分数
        quality_score = calculate_quality_score(filename, png_path)
        
        # 获取文件大小
        file_size = get_file_size_mb(png_path) if os.path.exists(png_path) else "Unknown"
        
        # 构建增强的元数据
        enhanced_item = {
            "id": f"unsplash_{image_id}",
            "title": title or f"透明背景图片 {image_id[:8]}",
            "description": description or "高质量透明背景PNG图片，适合设计和创意项目使用",
            "author": {
                "name": img_data.get('author', 'Unknown'),
                "url": f"https://unsplash.com/@{img_data.get('author', 'unknown').lower().replace(' ', '')}"
            },
            "dimensions": dimensions,
            "urls": {
                "thumbnail": f"./png/{png_filename}",  # 暂时使用同一个文件
                "regular": f"./png/{png_filename}",
                "download": f"./png/{png_filename}"
            },
            "tags": enhanced_tags,
            "category": category,
            "quality_score": quality_score,
            "file_size": file_size,
            "transparent_ratio": transparent_ratio,
            "created_at": datetime.now().isoformat() + "Z",
            "unsplash": {
                "id": image_id,
                "url": f"https://unsplash.com/photos/{image_id}",
                "download_location": img_data.get('download_location', f"https://unsplash.com/photos/{image_id}/download")
            }
        }
        
        enhanced_data.append(enhanced_item)
    
    # 按质量分数排序
    enhanced_data.sort(key=lambda x: x['quality_score'], reverse=True)
    
    # 保存增强的元数据
    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成增强元数据，共 {len(enhanced_data)} 张图片")
    print(f"📊 类别分布：")
    category_count = {}
    for item in enhanced_data:
        cat = item['category']
        category_count[cat] = category_count.get(cat, 0) + 1
    for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {cat}: {count} 张")

if __name__ == "__main__":
    generate_enhanced_metadata()