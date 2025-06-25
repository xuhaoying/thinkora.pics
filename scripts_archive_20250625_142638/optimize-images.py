#!/usr/bin/env python3
"""
图片优化脚本
生成多种尺寸的图片以优化加载性能
"""

import os
import json
from pathlib import Path
from PIL import Image, ImageOps
import argparse

class ImageOptimizer:
    def __init__(self):
        self.sizes = {
            'thumbnail': (200, 200),
            'small': (400, 400),
            'medium': (800, 800),
            'large': (1200, 1200)
        }
        
    def optimize_image(self, input_path, output_dir, filename):
        """优化单张图片"""
        try:
            with Image.open(input_path) as img:
                # 确保图片有透明背景
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # 创建输出目录
                os.makedirs(output_dir, exist_ok=True)
                
                results = {}
                
                for size_name, (width, height) in self.sizes.items():
                    # 计算缩放比例，保持宽高比
                    img_ratio = img.width / img.height
                    target_ratio = width / height
                    
                    if img_ratio > target_ratio:
                        # 图片更宽，以高度为准
                        new_height = height
                        new_width = int(height * img_ratio)
                    else:
                        # 图片更高，以宽度为准
                        new_width = width
                        new_height = int(width / img_ratio)
                    
                    # 缩放图片
                    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # 居中裁剪到目标尺寸
                    left = (new_width - width) // 2
                    top = (new_height - height) // 2
                    right = left + width
                    bottom = top + height
                    
                    cropped = resized.crop((left, top, right, bottom))
                    
                    # 保存图片
                    output_path = os.path.join(output_dir, f"{size_name}_{filename}")
                    cropped.save(output_path, 'PNG', optimize=True)
                    
                    results[size_name] = {
                        'path': output_path,
                        'size': os.path.getsize(output_path),
                        'dimensions': (width, height)
                    }
                    
                    print(f"  ✅ {size_name}: {width}x{height} ({results[size_name]['size']} bytes)")
                
                return results
                
        except Exception as e:
            print(f"  ❌ 处理失败: {e}")
            return None
    
    def optimize_all_images(self, input_dir="png", output_dir="optimized"):
        """优化所有图片"""
        print("🎨 开始优化图片...")
        
        input_path = Path(input_dir)
        if not input_path.exists():
            print(f"❌ 输入目录不存在: {input_dir}")
            return
        
        # 创建输出目录结构
        for size_name in self.sizes.keys():
            os.makedirs(os.path.join(output_dir, size_name), exist_ok=True)
        
        total_files = 0
        successful_files = 0
        optimization_stats = {
            'total_original_size': 0,
            'total_optimized_size': 0,
            'sizes': {size: {'count': 0, 'total_size': 0} for size in self.sizes.keys()}
        }
        
        # 处理所有PNG文件
        for png_file in input_path.glob('*.png'):
            total_files += 1
            print(f"\n📸 处理: {png_file.name}")
            
            # 获取原始文件大小
            original_size = png_file.stat().st_size
            optimization_stats['total_original_size'] += original_size
            
            # 优化图片
            results = self.optimize_image(png_file, output_dir, png_file.name)
            
            if results:
                successful_files += 1
                
                # 统计优化结果
                for size_name, result in results.items():
                    optimization_stats['sizes'][size_name]['count'] += 1
                    optimization_stats['sizes'][size_name]['total_size'] += result['size']
                    optimization_stats['total_optimized_size'] += result['size']
        
        # 输出统计信息
        self.print_optimization_stats(optimization_stats, total_files, successful_files)
        
        # 生成优化后的metadata
        self.generate_optimized_metadata(output_dir)
    
    def print_optimization_stats(self, stats, total_files, successful_files):
        """打印优化统计信息"""
        print(f"\n📊 优化统计:")
        print(f"   总文件数: {total_files}")
        print(f"   成功处理: {successful_files}")
        print(f"   原始大小: {stats['total_original_size'] / (1024**2):.2f} MB")
        print(f"   优化后大小: {stats['total_optimized_size'] / (1024**2):.2f} MB")
        
        savings = stats['total_original_size'] - stats['total_optimized_size']
        savings_percent = (savings / stats['total_original_size']) * 100
        
        print(f"   节省空间: {savings / (1024**2):.2f} MB ({savings_percent:.1f}%)")
        
        print(f"\n📏 各尺寸统计:")
        for size_name, size_stats in stats['sizes'].items():
            if size_stats['count'] > 0:
                avg_size = size_stats['total_size'] / size_stats['count']
                print(f"   {size_name}: {size_stats['count']} 张, 平均 {avg_size/1024:.1f} KB")
    
    def generate_optimized_metadata(self, output_dir):
        """生成优化后的metadata"""
        print(f"\n📝 生成优化后的metadata...")
        
        # 读取原始metadata
        if not os.path.exists('metadata.json'):
            print("❌ 未找到 metadata.json")
            return
        
        with open('metadata.json', 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # 更新每个图片的URL
        for item in metadata:
            image_id = item['id'].replace('unsplash_', '')
            
            # 为不同尺寸生成URL
            item['urls'] = {
                'thumbnail': f"https://your-bucket.r2.dev/optimized/thumbnail/{image_id}.png",
                'small': f"https://your-bucket.r2.dev/optimized/small/{image_id}.png",
                'medium': f"https://your-bucket.r2.dev/optimized/medium/{image_id}.png",
                'large': f"https://your-bucket.r2.dev/optimized/large/{image_id}.png"
            }
        
        # 保存优化后的metadata
        with open('metadata_optimized.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print("✅ 已生成 metadata_optimized.json")
    
    def create_upload_script(self, output_dir="optimized"):
        """创建上传脚本"""
        script_content = f"""#!/bin/bash
# 上传优化后的图片到 Cloudflare R2

echo "🚀 上传优化后的图片到 Cloudflare R2..."

# 上传不同尺寸的图片
for size in thumbnail small medium large; do
    echo "📤 上传 {size} 尺寸图片..."
    rclone copy ./{output_dir}/{size} r2:thinkora-images/optimized/{size} --progress
done

echo "✅ 上传完成!"
echo "🌐 图片访问地址:"
echo "   缩略图: https://your-bucket.r2.dev/optimized/thumbnail/"
echo "   小图: https://your-bucket.r2.dev/optimized/small/"
echo "   中图: https://your-bucket.r2.dev/optimized/medium/"
echo "   大图: https://your-bucket.r2.dev/optimized/large/"
"""
        
        with open('upload-optimized.sh', 'w') as f:
            f.write(script_content)
        
        os.chmod('upload-optimized.sh', 0o755)
        print("✅ 已创建 upload-optimized.sh 脚本")

def main():
    parser = argparse.ArgumentParser(description='优化图片并生成多种尺寸')
    parser.add_argument('--input', default='png', help='输入目录 (默认: png)')
    parser.add_argument('--output', default='optimized', help='输出目录 (默认: optimized)')
    parser.add_argument('--upload-script', action='store_true', help='生成上传脚本')
    
    args = parser.parse_args()
    
    optimizer = ImageOptimizer()
    
    # 检查依赖
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow 未安装")
        print("请运行: pip install Pillow")
        return
    
    # 优化图片
    optimizer.optimize_all_images(args.input, args.output)
    
    # 生成上传脚本
    if args.upload_script:
        optimizer.create_upload_script(args.output)
    
    print(f"\n🎉 优化完成!")
    print(f"📁 优化后的图片保存在: {args.output}/")
    print(f"📄 优化后的metadata: metadata_optimized.json")

if __name__ == "__main__":
    main() 