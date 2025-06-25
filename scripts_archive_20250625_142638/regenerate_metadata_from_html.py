#!/usr/bin/env python3
"""
Regenerate metadata.json from the existing HTML files
"""

import json
import re
from pathlib import Path

def extract_info_from_html(html_path):
    """Extract image information from HTML file"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract image ID from filename
    image_id = html_path.stem
    
    # Extract title
    title_match = re.search(r'<h1>([^<]+)</h1>', content)
    title = title_match.group(1) if title_match else f"Image {image_id}"
    
    # Extract description
    desc_match = re.search(r'<p>([^<]+)</p>', content)
    description = desc_match.group(1) if desc_match else title
    
    # Extract author
    author_match = re.search(r'<strong>Author:</strong>\s*<a[^>]+>([^<]+)</a>', content)
    author = author_match.group(1) if author_match else "Unknown"
    
    # Extract author URL
    author_url_match = re.search(r'<strong>Author:</strong>\s*<a href="([^"]+)"', content)
    author_url = author_url_match.group(1) if author_url_match else "https://unsplash.com/"
    
    # Extract dimensions
    dims_match = re.search(r'<strong>Dimensions:</strong>\s*(\d+)\s*x\s*(\d+)', content)
    width = int(dims_match.group(1)) if dims_match else 1920
    height = int(dims_match.group(2)) if dims_match else 1080
    
    # Extract image URL
    img_match = re.search(r'<img src="([^"]+)"', content)
    image_url = img_match.group(1) if img_match else f"https://thinkora.pics/images/{image_id}.png"
    
    # Determine platform based on ID format
    if image_id.isdigit():
        platform = "pexels"
    else:
        platform = "unsplash"
    
    return {
        "id": image_id,
        "url": image_url,
        "title": title,
        "description": description,
        "author": author,
        "author_url": author_url,
        "category": "photography",
        "width": width,
        "height": height,
        "platform": platform
    }

def main():
    print("🔄 Regenerating metadata.json from HTML files...")
    
    # Get all HTML files in dist/images
    html_files = sorted(Path("dist/images").glob("*.html"))
    print(f"📊 Found {len(html_files)} HTML files")
    
    # Extract metadata from each file
    metadata = []
    for html_file in html_files:
        try:
            info = extract_info_from_html(html_file)
            metadata.append(info)
            print(f"✅ Processed {html_file.name}")
        except Exception as e:
            print(f"❌ Error processing {html_file.name}: {e}")
    
    # Save metadata
    with open("metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Successfully regenerated metadata.json with {len(metadata)} images")
    
    # Show sample entries
    print("\n📋 Sample entries:")
    for item in metadata[:3]:
        print(f"  - {item['id']}: {item['title'][:50]}... by {item['author']}")

if __name__ == "__main__":
    main()