#!/usr/bin/env python3
"""
智能图片标签生成器 - 为没有标签的图片生成相关标签
"""

import json
import os
import re
from typing import List, Dict, Any
from collections import defaultdict

class ImageTagGenerator:
    def __init__(self):
        self.metadata_file = 'dist/metadata.json'
        
        # 基于类别的通用标签
        self.category_tags = {
            'business': ['business', 'professional', 'office', 'corporate', 'work', 'finance', 'meeting', 'team', 'career', 'success'],
            'photography': ['photography', 'photo', 'camera', 'image', 'picture', 'artistic', 'creative', 'visual', 'composition', 'art'],
            'stock photo': ['stock', 'commercial', 'marketing', 'advertising', 'media', 'content', 'digital', 'creative', 'design', 'visual'],
            'education': ['education', 'learning', 'school', 'study', 'knowledge', 'academic', 'teaching', 'student', 'classroom', 'books'],
            'food': ['food', 'culinary', 'cuisine', 'meal', 'cooking', 'recipe', 'delicious', 'nutrition', 'dining', 'restaurant'],
            'other': ['miscellaneous', 'various', 'general', 'mixed', 'diverse', 'collection', 'assorted', 'different', 'unique', 'special']
        }
        
        # 基于文件名模式的标签
        self.filename_patterns = {
            # 常见对象
            r'coffee|cafe': ['coffee', 'cafe', 'beverage', 'drink', 'morning', 'cup', 'hot drink'],
            r'laptop|computer|pc': ['laptop', 'computer', 'technology', 'device', 'work', 'digital', 'tech'],
            r'phone|mobile|smartphone': ['phone', 'mobile', 'smartphone', 'device', 'communication', 'technology'],
            r'book|reading': ['book', 'reading', 'literature', 'education', 'knowledge', 'study', 'library'],
            r'desk|office|workspace': ['desk', 'office', 'workspace', 'professional', 'work', 'business'],
            r'team|people|group': ['team', 'people', 'group', 'collaboration', 'teamwork', 'meeting'],
            r'nature|outdoor|landscape': ['nature', 'outdoor', 'landscape', 'environment', 'natural', 'scenery'],
            r'plant|flower|botanical': ['plant', 'flower', 'botanical', 'nature', 'green', 'garden'],
            r'food|meal|dish': ['food', 'meal', 'dish', 'cuisine', 'culinary', 'dining'],
            r'hand|hands': ['hand', 'gesture', 'human', 'touch', 'interaction', 'communication'],
            
            # 动作/概念
            r'work|working': ['work', 'working', 'professional', 'productivity', 'busy', 'career'],
            r'study|studying': ['study', 'studying', 'learning', 'education', 'student', 'academic'],
            r'meeting|conference': ['meeting', 'conference', 'business', 'discussion', 'collaboration'],
            r'travel|journey': ['travel', 'journey', 'adventure', 'tourism', 'vacation', 'trip'],
            r'success|achievement': ['success', 'achievement', 'goal', 'victory', 'accomplishment'],
            
            # 技术相关
            r'data|analytics': ['data', 'analytics', 'information', 'statistics', 'analysis', 'insights'],
            r'code|coding|programming': ['code', 'coding', 'programming', 'developer', 'software', 'tech'],
            r'design|creative': ['design', 'creative', 'artistic', 'visual', 'graphics', 'art'],
            r'social|media': ['social', 'media', 'network', 'communication', 'digital', 'online'],
            
            # 颜色
            r'white|light': ['white', 'light', 'bright', 'clean', 'minimal', 'simple'],
            r'black|dark': ['black', 'dark', 'shadow', 'contrast', 'dramatic', 'bold'],
            r'blue': ['blue', 'color', 'cool', 'calm', 'peaceful', 'serene'],
            r'green': ['green', 'color', 'nature', 'fresh', 'eco', 'environmental'],
            r'red': ['red', 'color', 'warm', 'passion', 'energy', 'vibrant']
        }
        
        # 基于尺寸的标签
        self.size_tags = {
            'small': ['icon', 'small', 'compact', 'mini', 'thumbnail'],
            'medium': ['medium', 'standard', 'regular', 'normal'],
            'large': ['large', 'big', 'high-resolution', 'detailed'],
            'hd': ['hd', 'high-definition', 'quality', 'sharp', 'clear'],
            '4k': ['4k', 'ultra-hd', 'high-resolution', 'premium', 'professional']
        }
        
        # 基于透明度的标签
        self.transparency_tags = {
            'full': ['transparent', 'no-background', 'cutout', 'isolated', 'png'],
            'partial': ['semi-transparent', 'translucent', 'opacity', 'overlay'],
            'none': ['solid', 'background', 'filled', 'complete']
        }
    
    def generate_tags_from_title(self, title: str) -> List[str]:
        """从标题生成标签"""
        tags = []
        title_lower = title.lower()
        
        # 提取标题中的关键词
        # 移除常见的无用词
        stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'image', 
                      'transparent', 'background', 'png', 'free', 'download']
        
        # 分词并过滤
        words = re.findall(r'\b[a-z]+\b', title_lower)
        for word in words:
            if len(word) > 2 and word not in stop_words:
                tags.append(word)
        
        return tags[:5]  # 限制从标题提取的标签数量
    
    def generate_tags_from_filename(self, filename: str) -> List[str]:
        """从文件名生成标签"""
        tags = []
        filename_lower = filename.lower()
        
        # 检查文件名模式
        for pattern, pattern_tags in self.filename_patterns.items():
            if re.search(pattern, filename_lower):
                tags.extend(pattern_tags[:3])  # 每个模式最多3个标签
        
        return list(dict.fromkeys(tags))  # 去重
    
    def generate_tags_from_size(self, width: int, height: int) -> List[str]:
        """基于图片尺寸生成标签"""
        tags = []
        
        # 计算尺寸
        total_pixels = width * height
        
        if width >= 3840 or height >= 2160:
            tags.extend(self.size_tags['4k'][:2])
        elif width >= 1920 or height >= 1080:
            tags.extend(self.size_tags['hd'][:2])
        elif total_pixels < 500000:
            tags.extend(self.size_tags['small'][:2])
        elif total_pixels > 2000000:
            tags.extend(self.size_tags['large'][:2])
        else:
            tags.extend(self.size_tags['medium'][:1])
        
        # 添加方向标签
        aspect_ratio = width / height if height > 0 else 1
        if aspect_ratio > 1.5:
            tags.append('landscape')
            tags.append('horizontal')
        elif aspect_ratio < 0.7:
            tags.append('portrait')
            tags.append('vertical')
        else:
            tags.append('square')
        
        return tags
    
    def generate_tags_from_transparency(self, transparency_ratio: float) -> List[str]:
        """基于透明度生成标签"""
        if transparency_ratio > 0.9:
            return self.transparency_tags['full'][:3]
        elif transparency_ratio > 0.5:
            return self.transparency_tags['partial'][:2]
        else:
            return self.transparency_tags['none'][:1]
    
    def generate_smart_tags(self, image: Dict[str, Any]) -> List[str]:
        """为图片生成智能标签"""
        all_tags = []
        
        # 1. 如果已有标签，保留并增强
        existing_tags = image.get('tags', [])
        if existing_tags:
            all_tags.extend(existing_tags)
        
        # 2. 从类别生成标签
        category = image.get('category', 'other')
        if category in self.category_tags:
            all_tags.extend(self.category_tags[category][:3])
        
        # 3. 从标题生成标签
        title = image.get('title', '')
        if title:
            all_tags.extend(self.generate_tags_from_title(title))
        
        # 4. 从文件名生成标签
        filename = image.get('id', '')
        all_tags.extend(self.generate_tags_from_filename(filename))
        
        # 5. 从尺寸生成标签
        width = image.get('width', 0)
        height = image.get('height', 0)
        if width and height:
            all_tags.extend(self.generate_tags_from_size(width, height))
        
        # 6. 从透明度生成标签
        transparency = image.get('transparencyRatio', 1.0)
        all_tags.extend(self.generate_tags_from_transparency(transparency))
        
        # 7. 添加平台标签
        platform = image.get('platform', '')
        if platform:
            all_tags.append(platform)
        
        # 8. 添加质量标签
        quality_score = image.get('qualityScore', 0)
        if quality_score >= 95:
            all_tags.extend(['premium', 'high-quality'])
        elif quality_score >= 90:
            all_tags.append('quality')
        
        # 去重并限制数量
        unique_tags = []
        seen = set()
        for tag in all_tags:
            tag_lower = tag.lower().strip()
            if tag_lower and tag_lower not in seen and len(tag_lower) > 1:
                seen.add(tag_lower)
                unique_tags.append(tag_lower)
        
        # 返回前20个最相关的标签
        return unique_tags[:20]
    
    def enhance_metadata(self):
        """增强所有图片的元数据"""
        # 加载现有元数据
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            images = json.load(f)
        
        print(f"📊 Processing {len(images)} images...")
        
        # 统计
        stats = {
            'images_without_tags': 0,
            'tags_added': 0,
            'total_tags': 0
        }
        
        # 处理每个图片
        for i, image in enumerate(images):
            existing_tags = image.get('tags', [])
            
            # 生成智能标签
            smart_tags = self.generate_smart_tags(image)
            
            # 如果没有标签，统计
            if not existing_tags:
                stats['images_without_tags'] += 1
            
            # 更新标签
            image['tags'] = smart_tags
            stats['tags_added'] += len(smart_tags) - len(existing_tags)
            stats['total_tags'] += len(smart_tags)
            
            # 更新SEO相关字段
            if smart_tags:
                # 重新生成SEO标题（包含主要标签）
                main_tag = smart_tags[0] if smart_tags else image.get('category', 'general')
                category = image.get('category', 'general')
                width = image.get('width', 0)
                
                # 生成更具描述性的标题
                if width >= 4000:
                    resolution = "4K"
                elif width >= 2000:
                    resolution = "HD"
                else:
                    resolution = ""
                
                title_parts = [main_tag.title()]
                if main_tag != category:
                    title_parts.append(category.title())
                title_parts.append("Transparent PNG")
                if resolution:
                    title_parts.append(resolution)
                
                image['seoTitle'] = ' '.join(title_parts) + " - Free Download"
                
                # 更新SEO关键词
                image['seoKeywords'] = ', '.join(smart_tags[:10])
            
            if (i + 1) % 50 == 0:
                print(f"✅ Processed {i + 1}/{len(images)} images")
        
        # 保存更新后的元数据
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(images, f, indent=2, ensure_ascii=False)
        
        # 打印统计
        print(f"\n📈 Tag Generation Statistics:")
        print(f"Images without tags: {stats['images_without_tags']}")
        print(f"Total tags added: {stats['tags_added']}")
        print(f"Average tags per image: {stats['total_tags'] / len(images):.1f}")
        
        return images
    
    def analyze_tag_distribution(self, images: List[Dict[str, Any]]):
        """分析标签分布"""
        tag_counts = defaultdict(int)
        
        for image in images:
            for tag in image.get('tags', []):
                tag_counts[tag] += 1
        
        # 排序并显示前20个最常见的标签
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\n🏷️  Top 20 Most Common Tags:")
        for tag, count in sorted_tags[:20]:
            print(f"  {tag}: {count} images")

def main():
    generator = ImageTagGenerator()
    
    print("🚀 Starting intelligent tag generation...")
    
    # 生成标签
    enhanced_images = generator.enhance_metadata()
    
    # 分析标签分布
    generator.analyze_tag_distribution(enhanced_images)
    
    print("\n✅ Tag generation completed!")
    print("Next step: Run regenerate_seo_pages.py to update all HTML pages with new tags")

if __name__ == "__main__":
    main()