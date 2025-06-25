#!/usr/bin/env python3
"""
SEO性能检查器 - 检查网站SEO优化状态
"""

import os
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict

class SEOPerformanceChecker:
    def __init__(self):
        self.dist_dir = 'dist'
        self.issues = defaultdict(list)
        self.stats = {
            'total_pages': 0,
            'pages_with_meta': 0,
            'pages_with_og': 0,
            'pages_with_schema': 0,
            'pages_with_h1': 0,
            'pages_with_alt': 0,
            'unique_titles': set(),
            'unique_descriptions': set()
        }
    
    def check_html_file(self, filepath):
        """检查单个HTML文件的SEO状态"""
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        self.stats['total_pages'] += 1
        filename = os.path.basename(filepath)
        
        # 检查title标签
        title = soup.find('title')
        if title and title.text:
            title_text = title.text.strip()
            self.stats['unique_titles'].add(title_text)
            
            # 检查标题长度
            if len(title_text) < 30:
                self.issues['title_too_short'].append(f"{filename}: {title_text}")
            elif len(title_text) > 60:
                self.issues['title_too_long'].append(f"{filename}: {title_text[:60]}...")
        else:
            self.issues['missing_title'].append(filename)
        
        # 检查meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_text = meta_desc['content'].strip()
            self.stats['pages_with_meta'] += 1
            self.stats['unique_descriptions'].add(desc_text)
            
            # 检查描述长度
            if len(desc_text) < 120:
                self.issues['description_too_short'].append(f"{filename}: {desc_text}")
            elif len(desc_text) > 160:
                self.issues['description_too_long'].append(f"{filename}: {desc_text[:60]}...")
        else:
            self.issues['missing_description'].append(filename)
        
        # 检查Open Graph标签
        og_tags = soup.find_all('meta', property=re.compile('^og:'))
        if len(og_tags) >= 4:  # 至少需要title, description, image, url
            self.stats['pages_with_og'] += 1
        else:
            self.issues['incomplete_og'].append(filename)
        
        # 检查结构化数据
        schema_scripts = soup.find_all('script', type='application/ld+json')
        if schema_scripts:
            self.stats['pages_with_schema'] += 1
            # 验证JSON格式
            for script in schema_scripts:
                try:
                    json.loads(script.string)
                except:
                    self.issues['invalid_schema'].append(filename)
        else:
            self.issues['missing_schema'].append(filename)
        
        # 检查H1标签
        h1_tags = soup.find_all('h1')
        if h1_tags:
            self.stats['pages_with_h1'] += 1
            if len(h1_tags) > 1:
                self.issues['multiple_h1'].append(f"{filename}: {len(h1_tags)} H1 tags")
        else:
            self.issues['missing_h1'].append(filename)
        
        # 检查图片alt属性
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        if images_without_alt:
            self.issues['missing_alt'].append(f"{filename}: {len(images_without_alt)} images without alt")
        elif images:
            self.stats['pages_with_alt'] += 1
        
        # 检查内部链接
        internal_links = soup.find_all('a', href=re.compile('^/'))
        broken_links = []
        for link in internal_links:
            href = link['href']
            if href.endswith('.html'):
                link_path = os.path.join(self.dist_dir, href.lstrip('/'))
                if not os.path.exists(link_path):
                    broken_links.append(href)
        
        if broken_links:
            self.issues['broken_links'].append(f"{filename}: {broken_links}")
    
    def check_all_pages(self):
        """检查所有HTML页面"""
        print("🔍 Checking SEO performance...")
        
        # 检查主页
        index_path = os.path.join(self.dist_dir, 'index.html')
        if os.path.exists(index_path):
            self.check_html_file(index_path)
        
        # 检查所有图片详情页
        images_dir = os.path.join(self.dist_dir, 'images')
        if os.path.exists(images_dir):
            for filename in os.listdir(images_dir):
                if filename.endswith('.html'):
                    filepath = os.path.join(images_dir, filename)
                    self.check_html_file(filepath)
        
        # 检查分类页面
        category_dir = os.path.join(self.dist_dir, 'category')
        if os.path.exists(category_dir):
            for filename in os.listdir(category_dir):
                if filename.endswith('.html'):
                    filepath = os.path.join(category_dir, filename)
                    self.check_html_file(filepath)
        
        # 检查静态页面
        static_pages = ['about.html', 'terms.html', 'privacy.html', '404.html']
        for page in static_pages:
            filepath = os.path.join(self.dist_dir, page)
            if os.path.exists(filepath):
                self.check_html_file(filepath)
    
    def check_technical_seo(self):
        """检查技术SEO要素"""
        print("\n🔧 Checking technical SEO...")
        
        # 检查robots.txt
        robots_path = os.path.join(self.dist_dir, 'robots.txt')
        if os.path.exists(robots_path):
            with open(robots_path, 'r') as f:
                robots_content = f.read()
                if 'Sitemap:' in robots_content:
                    print("✅ Sitemap reference found in robots.txt")
                else:
                    self.issues['technical'].append("No sitemap reference in robots.txt")
        else:
            self.issues['technical'].append("Missing robots.txt")
        
        # 检查sitemap.xml
        sitemap_path = os.path.join(self.dist_dir, 'sitemap.xml')
        if os.path.exists(sitemap_path):
            print("✅ Sitemap.xml exists")
            # 可以进一步验证sitemap格式
        else:
            self.issues['technical'].append("Missing sitemap.xml")
        
        # 检查.htaccess (如果存在)
        htaccess_path = os.path.join(self.dist_dir, '.htaccess')
        if os.path.exists(htaccess_path):
            print("✅ .htaccess file exists")
        
        # 检查manifest.json
        manifest_path = os.path.join(self.dist_dir, 'manifest.json')
        if os.path.exists(manifest_path):
            print("✅ Web app manifest exists")
        else:
            self.issues['technical'].append("Missing manifest.json for PWA")
        
        # 检查service worker
        sw_path = os.path.join(self.dist_dir, 'sw.js')
        if os.path.exists(sw_path):
            print("✅ Service worker exists")
        else:
            self.issues['technical'].append("Missing service worker for PWA")
    
    def generate_report(self):
        """生成SEO性能报告"""
        print("\n📊 SEO Performance Report")
        print("=" * 50)
        
        # 统计数据
        print(f"\n📈 Statistics:")
        print(f"Total pages analyzed: {self.stats['total_pages']}")
        print(f"Pages with meta descriptions: {self.stats['pages_with_meta']} ({self.stats['pages_with_meta']/self.stats['total_pages']*100:.1f}%)")
        print(f"Pages with Open Graph tags: {self.stats['pages_with_og']} ({self.stats['pages_with_og']/self.stats['total_pages']*100:.1f}%)")
        print(f"Pages with structured data: {self.stats['pages_with_schema']} ({self.stats['pages_with_schema']/self.stats['total_pages']*100:.1f}%)")
        print(f"Pages with H1 tags: {self.stats['pages_with_h1']} ({self.stats['pages_with_h1']/self.stats['total_pages']*100:.1f}%)")
        print(f"Pages with proper alt tags: {self.stats['pages_with_alt']} ({self.stats['pages_with_alt']/self.stats['total_pages']*100:.1f}%)")
        print(f"Unique titles: {len(self.stats['unique_titles'])}")
        print(f"Unique descriptions: {len(self.stats['unique_descriptions'])}")
        
        # 问题汇总
        if self.issues:
            print(f"\n⚠️  Issues Found:")
            for issue_type, pages in self.issues.items():
                if pages:
                    print(f"\n{issue_type.replace('_', ' ').title()} ({len(pages)} pages):")
                    for i, page in enumerate(pages[:5]):  # 只显示前5个
                        print(f"  - {page}")
                    if len(pages) > 5:
                        print(f"  ... and {len(pages) - 5} more")
        else:
            print("\n✅ No major SEO issues found!")
        
        # 建议
        print("\n💡 Recommendations:")
        if self.issues['title_too_short']:
            print("- Expand short titles to 50-60 characters for better SEO")
        if self.issues['description_too_short']:
            print("- Expand short descriptions to 150-160 characters")
        if self.issues['missing_alt']:
            print("- Add descriptive alt text to all images")
        if self.issues['broken_links']:
            print("- Fix broken internal links")
        if len(self.stats['unique_titles']) < self.stats['total_pages'] * 0.9:
            print("- Ensure more unique titles across pages")
        
        # 计算SEO得分
        score = 100
        score -= len(self.issues['missing_title']) * 5
        score -= len(self.issues['missing_description']) * 3
        score -= len(self.issues['missing_h1']) * 2
        score -= len(self.issues['missing_alt']) * 1
        score -= len(self.issues['broken_links']) * 2
        score = max(0, score)
        
        print(f"\n🎯 Overall SEO Score: {score}/100")
        
        # 保存报告
        report = {
            'stats': dict(self.stats),
            'issues': dict(self.issues),
            'score': score,
            'unique_titles_count': len(self.stats['unique_titles']),
            'unique_descriptions_count': len(self.stats['unique_descriptions'])
        }
        
        with open('seo_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print("\n📄 Detailed report saved to seo_report.json")

def main():
    checker = SEOPerformanceChecker()
    checker.check_all_pages()
    checker.check_technical_seo()
    checker.generate_report()

if __name__ == "__main__":
    main()