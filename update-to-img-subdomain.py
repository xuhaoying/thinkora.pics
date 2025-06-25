#!/usr/bin/env python3
"""Update all image URLs to use img.thinkora.pics subdomain"""

import json
import os
import re

def update_metadata():
    """Update metadata.json to use img.thinkora.pics"""
    with open('dist/metadata.json', 'r') as f:
        metadata = json.load(f)
    
    updated_count = 0
    for item in metadata:
        old_url = item['url']
        # Replace thinkora.pics with img.thinkora.pics in the URL
        new_url = old_url.replace('https://thinkora.pics/', 'https://img.thinkora.pics/')
        if old_url != new_url:
            item['url'] = new_url
            updated_count += 1
            print(f"Updated: {old_url} -> {new_url}")
    
    # Save updated metadata
    with open('dist/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✓ Updated {updated_count} URLs in metadata.json")
    
    # Also update metadata_r2.json if it exists
    try:
        with open('metadata_r2.json', 'r') as f:
            metadata_r2 = json.load(f)
        
        for item in metadata_r2:
            if 'url' in item:
                old_url = item['url']
                item['url'] = old_url.replace('https://thinkora.pics/', 'https://img.thinkora.pics/')
        
        with open('metadata_r2.json', 'w') as f:
            json.dump(metadata_r2, f, indent=2)
        print("✓ Also updated metadata_r2.json")
    except FileNotFoundError:
        print("metadata_r2.json not found, skipping")
    except Exception as e:
        print(f"Error updating metadata_r2.json: {e}")

def update_html_files():
    """Update all HTML files to use img.thinkora.pics"""
    # Pattern to match image URLs
    pattern = re.compile(r'https://thinkora\.pics/images/')
    replacement = 'https://img.thinkora.pics/images/'
    
    files_updated = 0
    
    # Update index.html
    index_path = 'dist/index.html'
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            content = f.read()
        
        new_content = pattern.sub(replacement, content)
        if content != new_content:
            with open(index_path, 'w') as f:
                f.write(new_content)
            files_updated += 1
            print(f"✓ Updated {index_path}")
    
    # Update all image detail pages
    images_dir = 'dist/images'
    if os.path.exists(images_dir):
        for filename in os.listdir(images_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(images_dir, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                new_content = pattern.sub(replacement, content)
                if content != new_content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    files_updated += 1
        
        print(f"✓ Updated {files_updated - 1} detail pages")
    
    # Update sitemap.xml
    sitemap_path = 'dist/sitemap.xml'
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r') as f:
            content = f.read()
        
        # Note: sitemap should keep main domain for page URLs, only update if there are image URLs
        # For now, we'll leave sitemap as is since it contains page URLs, not image URLs
        print("✓ Sitemap.xml checked (no image URLs to update)")
    
    print(f"\n✓ Total HTML files updated: {files_updated}")

def update_env_file():
    """Update .env file with new R2 public URL"""
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('R2_PUBLIC_URL='):
                # Check if it's already updated
                if 'img.thinkora.pics' not in line:
                    lines[i] = 'R2_PUBLIC_URL=https://img.thinkora.pics\n'
                    updated = True
                    print("✓ Updated R2_PUBLIC_URL in .env")
                break
        
        if updated:
            with open(env_path, 'w') as f:
                f.writelines(lines)

def update_vercel_json():
    """Update vercel.json to handle img subdomain"""
    vercel_path = 'vercel.json'
    if os.path.exists(vercel_path):
        with open(vercel_path, 'r') as f:
            config = json.load(f)
        
        # Update rewrites if they exist
        if 'rewrites' in config:
            for rewrite in config['rewrites']:
                if 'destination' in rewrite and 'thinkora.pics/images/' in rewrite['destination']:
                    rewrite['destination'] = rewrite['destination'].replace(
                        'https://thinkora.pics/images/', 
                        'https://img.thinkora.pics/images/'
                    )
                    print(f"✓ Updated rewrite rule: {rewrite['destination']}")
        
        with open(vercel_path, 'w') as f:
            json.dump(config, f, indent=2)
        print("✓ Updated vercel.json")

def main():
    print("Updating all configurations to use img.thinkora.pics...\n")
    
    # Update metadata
    update_metadata()
    
    # Update HTML files
    print("\nUpdating HTML files...")
    update_html_files()
    
    # Update environment variables
    print("\nUpdating environment variables...")
    update_env_file()
    
    # Update Vercel configuration
    print("\nUpdating Vercel configuration...")
    update_vercel_json()
    
    print("\n✅ All updates completed!")
    print("\nNext steps:")
    print("1. Make sure img.thinkora.pics is configured as a custom domain for your R2 bucket")
    print("2. Run: python regenerate-html.py (if needed)")
    print("3. Commit and push changes")
    print("4. Verify images load correctly from img.thinkora.pics")

if __name__ == "__main__":
    main()