#!/usr/bin/env python3
"""
Comprehensive website health check
"""

import json
import os
from pathlib import Path
from urllib.parse import urlparse
from collections import Counter
from bs4 import BeautifulSoup

def check_metadata():
    """Check metadata.json for completeness and correctness"""
    print("🔍 Checking metadata.json...")
    
    metadata_path = Path("metadata.json")
    if not metadata_path.exists():
        print("❌ metadata.json not found!")
        return False
    
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print(f"📊 Total images in metadata: {len(metadata)}")
    
    # Check each image entry
    issues = []
    missing_fields = Counter()
    url_domains = Counter()
    categories = Counter()
    
    for i, item in enumerate(metadata):
        # Check required fields
        required_fields = ['id', 'category']
        for field in required_fields:
            if field not in item:
                missing_fields[field] += 1
                issues.append(f"Image {i}: Missing field '{field}'")
        
        # Check URL field
        if 'url' in item:
            url = item['url']
            domain = urlparse(url).netloc
            url_domains[domain] += 1
            
            # Check if URL uses custom domain
            if 'thinkora.pics' not in url:
                issues.append(f"Image {item.get('id', i)}: URL not using custom domain - {url}")
        elif 'urls' in item and 'regular' in item['urls']:
            url = item['urls']['regular']
            domain = urlparse(url).netloc
            url_domains[domain] += 1
            
            if 'thinkora.pics' not in url:
                issues.append(f"Image {item.get('id', i)}: URL not using custom domain - {url}")
        else:
            issues.append(f"Image {i}: No URL found")
        
        # Count categories
        if 'category' in item:
            categories[item['category']] += 1
        
        # Check author and description
        if 'author' not in item or item.get('author') == 'Unknown':
            missing_fields['author'] += 1
        
        if 'description' not in item or not item.get('description'):
            missing_fields['description'] += 1
    
    # Report findings
    print(f"\n📈 URL Domains:")
    for domain, count in url_domains.items():
        print(f"  - {domain}: {count} images")
    
    print(f"\n📂 Categories:")
    for category, count in categories.items():
        print(f"  - {category}: {count} images")
    
    print(f"\n⚠️  Missing Fields:")
    for field, count in missing_fields.items():
        print(f"  - {field}: {count} images missing")
    
    if issues:
        print(f"\n❌ Found {len(issues)} issues:")
        for issue in issues[:10]:  # Show first 10 issues
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
        return False
    else:
        print("✅ All metadata entries are complete and using custom domain!")
        return True

def check_html_structure():
    """Check HTML files for proper structure"""
    print("\n🔍 Checking HTML structure...")
    
    # Check index.html
    index_path = Path("dist/index.html")
    if not index_path.exists():
        print("❌ dist/index.html not found!")
        return False
    
    with open(index_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Check for required elements
    image_cards = soup.find_all('div', class_='image-card')
    print(f"📊 Found {len(image_cards)} image cards in index.html")
    
    # Check image detail pages
    detail_pages = list(Path("dist/images").glob("*.html"))
    print(f"📊 Found {len(detail_pages)} detail pages")
    
    # Sample check a few detail pages
    issues = []
    for i, page_path in enumerate(detail_pages[:5]):  # Check first 5
        with open(page_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Check for required elements
        if not soup.find('img'):
            issues.append(f"{page_path.name}: No image tag found")
        
        img_tag = soup.find('img')
        if img_tag and 'thinkora.pics' not in img_tag.get('src', ''):
            issues.append(f"{page_path.name}: Image not using custom domain")
        
        if not soup.find('h1'):
            issues.append(f"{page_path.name}: No h1 title found")
        
        if not soup.find('a', class_='download-button'):
            issues.append(f"{page_path.name}: No download button found")
    
    if issues:
        print(f"❌ Found issues in detail pages:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ HTML structure looks good!")
        return True

def check_search_functionality():
    """Check if search functionality files exist"""
    print("\n🔍 Checking search functionality...")
    
    # Check for main.js
    js_path = Path("dist/public/js/main.js")
    if not js_path.exists():
        print("❌ main.js not found!")
        return False
    
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check for search-related code
    search_indicators = ['search', 'filter', 'query', 'filterImages']
    found_search = any(indicator in js_content.lower() for indicator in search_indicators)
    
    if found_search:
        print("✅ Search functionality code found in main.js")
        
        # Check if metadata is embedded or loaded
        if 'metadata' in js_content or 'fetch' in js_content:
            print("✅ Metadata loading mechanism found")
        else:
            print("⚠️  No metadata loading mechanism found")
    else:
        print("❌ No search functionality found in main.js")
        return False
    
    return True

def check_navigation():
    """Check navigation between pages"""
    print("\n🔍 Checking navigation...")
    
    # Check a few detail pages for navigation links
    detail_pages = sorted(Path("dist/images").glob("*.html"))
    
    if len(detail_pages) < 3:
        print("❌ Not enough detail pages to check navigation")
        return False
    
    # Check middle page (should have both prev and next)
    middle_page = detail_pages[len(detail_pages) // 2]
    
    with open(middle_page, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    nav_links = soup.find_all('a', text=lambda x: x and ('Previous' in x or 'Next' in x))
    
    if len(nav_links) >= 2:
        print(f"✅ Navigation links found in {middle_page.name}")
        return True
    else:
        print(f"❌ Navigation links missing in {middle_page.name}")
        return False

def check_image_consistency():
    """Check consistency between metadata and HTML files"""
    print("\n🔍 Checking image consistency...")
    
    # Load metadata
    with open("metadata.json", 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Get all image IDs from metadata
    metadata_ids = {item['id'] for item in metadata}
    
    # Get all HTML files
    html_files = {p.stem for p in Path("dist/images").glob("*.html")}
    
    # Check for mismatches
    only_in_metadata = metadata_ids - html_files
    only_in_html = html_files - metadata_ids
    
    if only_in_metadata:
        print(f"❌ Images in metadata but no HTML: {len(only_in_metadata)}")
        for img_id in list(only_in_metadata)[:5]:
            print(f"  - {img_id}")
    
    if only_in_html:
        print(f"❌ HTML files without metadata: {len(only_in_html)}")
        for img_id in list(only_in_html)[:5]:
            print(f"  - {img_id}")
    
    if not only_in_metadata and not only_in_html:
        print(f"✅ Perfect match: {len(metadata_ids)} images in both metadata and HTML")
        return True
    
    return False

def main():
    print("🏥 Running comprehensive website health check...\n")
    
    results = {
        "Metadata": check_metadata(),
        "HTML Structure": check_html_structure(),
        "Search Functionality": check_search_functionality(),
        "Navigation": check_navigation(),
        "Image Consistency": check_image_consistency()
    }
    
    print("\n📋 Summary:")
    all_good = True
    for check, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}: {'PASSED' if result else 'FAILED'}")
        if not result:
            all_good = False
    
    if all_good:
        print("\n🎉 All checks passed! Website is healthy!")
    else:
        print("\n⚠️  Some issues found. Please review the output above.")
    
    return all_good

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)