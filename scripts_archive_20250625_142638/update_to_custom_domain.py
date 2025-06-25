#!/usr/bin/env python3
"""
Update all image URLs to use custom domain instead of R2 default domain
"""

import json
import os
from pathlib import Path
import re

def update_metadata_to_custom_domain():
    """Update metadata.json to use custom domain"""
    metadata_path = Path("metadata.json")
    
    if not metadata_path.exists():
        print("❌ metadata.json not found")
        return False
    
    # Load metadata
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Update URLs
    old_domain = "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev"
    new_domain = "https://thinkora.pics"
    
    updated_count = 0
    for item in metadata:
        # Update url field
        if 'url' in item and old_domain in item['url']:
            item['url'] = item['url'].replace(old_domain, new_domain)
            updated_count += 1
        
        # Update urls.regular field (if exists)
        if 'urls' in item and 'regular' in item['urls'] and old_domain in item['urls']['regular']:
            item['urls']['regular'] = item['urls']['regular'].replace(old_domain, new_domain)
            updated_count += 1
    
    # Save updated metadata
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Updated {updated_count} URLs in metadata.json")
    return True

def update_html_files_to_custom_domain():
    """Update all HTML files to use custom domain"""
    old_domain = "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev"
    new_domain = "https://thinkora.pics"
    
    # Update index.html
    index_path = Path("dist/index.html")
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content.replace(old_domain, new_domain)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Updated dist/index.html")
    
    # Update all image detail pages
    images_dir = Path("dist/images")
    if images_dir.exists():
        html_files = list(images_dir.glob("*.html"))
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated_content = content.replace(old_domain, new_domain)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        
        print(f"✅ Updated {len(html_files)} HTML files in dist/images/")
    
    return True

def update_sitemap_to_custom_domain():
    """Update sitemap.xml to use custom domain"""
    sitemap_path = Path("dist/sitemap.xml")
    
    if sitemap_path.exists():
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update domain in sitemap
        updated_content = content.replace("https://thinkora.pics", "https://thinkora.pics")  # Already correct
        
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Updated dist/sitemap.xml")
    
    return True

def main():
    print("🔄 Updating all URLs to use custom domain: thinkora.pics")
    
    # Update metadata
    update_metadata_to_custom_domain()
    
    # Update HTML files
    update_html_files_to_custom_domain()
    
    # Update sitemap
    update_sitemap_to_custom_domain()
    
    print("\n✅ All URLs have been updated to use the custom domain!")
    print("📌 Note: Make sure the custom domain is properly configured in Cloudflare R2")

if __name__ == "__main__":
    main()