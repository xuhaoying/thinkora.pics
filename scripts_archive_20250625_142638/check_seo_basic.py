#!/usr/bin/env python3
"""
基础SEO检查器 - 检查网站SEO优化状态
"""

import os
import json
import re

class BasicSEOChecker:
    def __init__(self):
        self.dist_dir = 'dist'
        self.results = {
            'files_checked': 0,
            'sitemaps': [],
            'static_pages': [],
            'category_pages': [],
            'image_pages': 0,
            'missing_files': []
        }
    
    def check_files(self):
        """检查文件存在性"""
        print("🔍 Checking SEO files...")
        
        # 检查关键文件
        key_files = {
            'robots.txt': 'robots.txt',
            'sitemap.xml': 'sitemap.xml',
            'sitemap-images.xml': 'sitemap-images.xml',
            'manifest.json': 'manifest.json',
            'service_worker': 'sw.js',
            '.htaccess': '.htaccess',
            'organization_schema': 'organization-schema.json'
        }
        
        for name, filename in key_files.items():
            filepath = os.path.join(self.dist_dir, filename)
            if os.path.exists(filepath):
                print(f"✅ {name}: Found")
                if 'sitemap' in filename:
                    self.results['sitemaps'].append(filename)
            else:
                print(f"❌ {name}: Missing")
                self.results['missing_files'].append(filename)
        
        # 检查静态页面
        static_pages = ['index.html', 'about.html', 'terms.html', 'privacy.html', '404.html']
        for page in static_pages:
            filepath = os.path.join(self.dist_dir, page)
            if os.path.exists(filepath):
                self.results['static_pages'].append(page)
            else:
                self.results['missing_files'].append(page)
        
        print(f"\n📄 Static pages found: {len(self.results['static_pages'])}/{len(static_pages)}")
        
        # 检查分类页面
        category_dir = os.path.join(self.dist_dir, 'category')
        if os.path.exists(category_dir):
            categories = [f for f in os.listdir(category_dir) if f.endswith('.html')]
            self.results['category_pages'] = categories
            print(f"📁 Category pages found: {len(categories)}")
        else:
            print("❌ Category directory missing")
        
        # 统计图片页面
        images_dir = os.path.join(self.dist_dir, 'images')
        if os.path.exists(images_dir):
            image_pages = [f for f in os.listdir(images_dir) if f.endswith('.html')]
            self.results['image_pages'] = len(image_pages)
            print(f"🖼️  Image pages found: {len(image_pages)}")
        else:
            print("❌ Images directory missing")
    
    def check_metadata(self):
        """检查元数据文件"""
        print("\n📊 Checking metadata...")
        
        metadata_path = os.path.join(self.dist_dir, 'metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            print(f"✅ Metadata found with {len(metadata)} images")
            
            # 检查SEO字段
            sample = metadata[0] if metadata else {}
            seo_fields = ['seoTitle', 'seoDescription', 'seoKeywords', 'structuredData', 'canonicalUrl']
            
            found_fields = [field for field in seo_fields if field in sample]
            print(f"📋 SEO fields found: {', '.join(found_fields)}")
            
            if len(found_fields) < len(seo_fields):
                missing = set(seo_fields) - set(found_fields)
                print(f"⚠️  Missing SEO fields: {', '.join(missing)}")
        else:
            print("❌ Metadata file not found")
    
    def check_performance_assets(self):
        """检查性能优化资源"""
        print("\n⚡ Checking performance assets...")
        
        # 检查CSS文件
        css_files = ['styles.css', 'styles-enhanced.css']
        css_dir = os.path.join(self.dist_dir, 'public', 'css')
        if os.path.exists(css_dir):
            found_css = [f for f in css_files if os.path.exists(os.path.join(css_dir, f))]
            print(f"✅ CSS files: {', '.join(found_css)}")
        
        # 检查JS文件
        js_files = ['main.js', 'main-enhanced.js', 'download-force.js']
        js_dir = os.path.join(self.dist_dir, 'public', 'js')
        if os.path.exists(js_dir):
            found_js = [f for f in js_files if os.path.exists(os.path.join(js_dir, f))]
            print(f"✅ JS files: {', '.join(found_js)}")
    
    def generate_summary(self):
        """生成摘要"""
        print("\n📈 SEO Optimization Summary")
        print("=" * 50)
        
        # 计算完成度
        total_checks = 15  # 总检查项
        completed = total_checks - len(self.results['missing_files'])
        percentage = (completed / total_checks) * 100
        
        print(f"Overall completion: {completed}/{total_checks} ({percentage:.1f}%)")
        print(f"Image pages: {self.results['image_pages']}")
        print(f"Category pages: {len(self.results['category_pages'])}")
        print(f"Static pages: {len(self.results['static_pages'])}")
        print(f"Sitemaps: {len(self.results['sitemaps'])}")
        
        if self.results['missing_files']:
            print(f"\n⚠️  Missing files ({len(self.results['missing_files'])}):")
            for file in self.results['missing_files']:
                print(f"  - {file}")
        
        # 建议
        print("\n💡 Next Steps:")
        if 'og-image.png' in str(self.results['missing_files']):
            print("1. Create and upload Open Graph image (1200x630px)")
        print("2. Submit sitemaps to Google Search Console")
        print("3. Test page loading speed with PageSpeed Insights")
        print("4. Monitor Core Web Vitals")
        print("5. Set up analytics tracking")
        
        # 保存结果
        with open('seo_check_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        print("\n✅ Results saved to seo_check_results.json")

def main():
    checker = BasicSEOChecker()
    checker.check_files()
    checker.check_metadata()
    checker.check_performance_assets()
    checker.generate_summary()

if __name__ == "__main__":
    main()