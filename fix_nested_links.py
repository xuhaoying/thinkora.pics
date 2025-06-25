#!/usr/bin/env python3
"""
修复嵌套的下载链接问题
"""

import os
import re

def fix_nested_links():
    """修复HTML文件中嵌套的<a>标签问题"""
    
    html_dir = 'dist/images'
    
    for filename in os.listdir(html_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(html_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找嵌套的链接模式
            # <a href="None" download="...">
            #     <a href="https://..." download="...">
            #     <img src="..." alt="..." loading="eager">
            # </a>
            # </a>
            
            # 匹配嵌套的a标签
            nested_pattern = r'<a href="None"[^>]*>\s*<a href="([^"]*)"([^>]*)>\s*<img([^>]*)>\s*</a>\s*</a>'
            
            def replace_nested(match):
                correct_href = match.group(1)
                download_attrs = match.group(2)
                img_attrs = match.group(3)
                
                return f'<a href="{correct_href}"{download_attrs}>\n                    <img{img_attrs}>\n                </a>'
            
            new_content = re.sub(nested_pattern, replace_nested, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ Fixed nested links in {filename}")
            else:
                print(f"- No nested links found in {filename}")

if __name__ == "__main__":
    print("🔧 Fixing nested download links...")
    fix_nested_links()
    print("✅ Done!")