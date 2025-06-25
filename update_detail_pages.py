#!/usr/bin/env python3
"""
Update all detail pages to use enhanced CSS and JS
"""

from pathlib import Path
import re

def update_detail_pages():
    """Update all HTML files in dist/images to use enhanced assets"""
    
    images_dir = Path("dist/images")
    if not images_dir.exists():
        print("❌ dist/images directory not found")
        return
    
    html_files = list(images_dir.glob("*.html"))
    print(f"📊 Found {len(html_files)} detail pages to update")
    
    updated_count = 0
    
    for html_file in html_files:
        try:
            # Read the file
            content = html_file.read_text(encoding='utf-8')
            
            # Update CSS reference
            content = content.replace(
                'href="/public/css/styles.css"',
                'href="/public/css/styles-enhanced.css"'
            )
            
            # Update JS reference
            content = content.replace(
                'src="/public/js/main.js"',
                'src="/public/js/main-enhanced.js"'
            )
            
            # Write back
            html_file.write_text(content, encoding='utf-8')
            
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error updating {html_file.name}: {e}")
    
    print(f"✅ Updated {updated_count} detail pages")

def main():
    print("🔄 Updating detail pages to use enhanced assets...")
    update_detail_pages()
    print("✨ All pages now use enhanced CSS and JavaScript!")

if __name__ == "__main__":
    main()