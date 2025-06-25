#!/usr/bin/env python3
import json
import os
import shutil
import sqlite3
from jinja2 import Environment, FileSystemLoader

# --- Configuration ---
# METADATA_FILE = 'metadata.json'  # No longer needed
DB_FILE = 'thinkora.db'
TABLE_NAME = 'images'
TEMPLATES_DIR = 'templates'
OUTPUT_DIR = 'images'
INDEX_OUTPUT_PATH = 'index.html'
STATIC_DIR = 'public'  # Directory for CSS, JS, etc.
BASE_URL = "https://thinkora.pics" # Replace with your actual domain if different

def fetch_images_from_db():
    """
    Fetches all image records from the SQLite database.
    Returns a list of dictionaries, where each dictionary represents an image.
    """
    print(f"Connecting to database '{DB_FILE}'...")
    conn = sqlite3.connect(DB_FILE)
    # Return rows as dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"Fetching all records from table '{TABLE_NAME}'...")
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    images = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    print(f"Found {len(images)} records. Connection closed.")

    # Post-process data for template compatibility
    for image in images:
        # The 'tags' field is stored as a JSON string, so we need to parse it back
        if image.get('tags'):
            image['tags'] = json.loads(image['tags'])
        else:
            image['tags'] = []
            
        # Recreate the nested structures for compatibility with templates
        image['author'] = {'name': image.get('author_name'), 'url': image.get('author_url')}
        image['dimensions'] = {'width': image.get('width'), 'height': image.get('height'), 'ratio': image.get('aspect_ratio')}
        image['urls'] = {'thumbnail': image.get('url_thumbnail'), 'regular': image.get('url_regular'), 'download': image.get('url_download')}

    return images

def main():
    """
    Main function to generate the static site.
    """
    print("🚀 Starting static site generation...")

    # 1. Setup Environment & Load Data
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    # if not os.path.exists(METADATA_FILE):
    #     print(f"❌ Error: Metadata file not found at '{METADATA_FILE}'")
    #     return
        
    images = fetch_images_from_db()

    # Clean and prepare output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(os.path.join(OUTPUT_DIR, 'images'), exist_ok=True)
    
    # 2. Generate Homepage
    print("🏠 Generating homepage (index.html)...")
    generate_homepage(env, images)

    # 3. Generate Detail Pages
    print("🖼️  Generating detail pages...")
    generate_detail_pages(env, images)
    
    # 4. Generate SEO files
    print("📜 Generating sitemap.xml and robots.txt...")
    generate_sitemap(images)
    generate_robots_txt()

    # 5. Copy Static Assets
    print("🎨 Copying static assets (CSS, JS)...")
    shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, STATIC_DIR))

    print(f"\n✅ Success! Static site generated in '{OUTPUT_DIR}' directory.")
    print(f"   - {len(images)} detail pages created.")
    print("   - To deploy, upload the contents of the 'dist' folder to your web host.")

def generate_homepage(env, images):
    template = env.get_template('index_template.html')
    html_content = template.render(images=images)
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_detail_pages(env, images):
    template = env.get_template('detail_template.html')
    total_images = len(images)
    
    for i, image in enumerate(images):
        image_id = image['id'].replace('unsplash_', '')
        
        prev_image = images[i - 1] if i > 0 else None
        next_image = images[i + 1] if i < total_images - 1 else None

        context = {
            'title': image.get('title', 'Untitled Image'),
            'description': image.get('description', 'A high-quality transparent PNG image.'),
            'image_url': image.get('imageUrl', image.get('urls', {}).get('regular', '')),
            'page_url': f"{BASE_URL}/images/{image_id}.html",
            'author_name': image.get('author', 'Unknown') if isinstance(image.get('author'), str) else image.get('author', {}).get('name', 'Unknown'),
            'author_url': image.get('authorUrl', image.get('author', {}).get('url', '#') if isinstance(image.get('author'), dict) else '#'),
            'dimensions': f"{image.get('width', 0)} x {image.get('height', 0)}" if 'width' in image else f"{image.get('dimensions', {}).get('width', 0)} x {image.get('dimensions', {}).get('height', 0)}",
            'file_size': f"{image.get('fileSize', 0) / (1024*1024):.1f}MB" if image.get('fileSize') else image.get('file_size', 'N/A'),
            'category': image.get('category', 'General'),
            'download_url': image.get('downloadUrl', image.get('urls', {}).get('download', '')),
            'tags': image.get('tags', []),
            'prev_image': prev_image,
            'next_image': next_image
        }
        
        html_content = template.render(context)
        
        output_path = os.path.join(OUTPUT_DIR, 'images', f"{image_id}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    print(f"   - Processed {total_images} images.")

def generate_sitemap(images):
    urls = [BASE_URL + '/']
    for image in images:
        image_id = image['id'].replace('unsplash_', '')
        urls.append(f"{BASE_URL}/images/{image_id}.html")

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap_content += f'  <url>\n    <loc>{url}</loc>\n  </url>\n'
    sitemap_content += '</urlset>'

    with open(os.path.join(OUTPUT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_content)

def generate_robots_txt():
    content = f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml"
    with open(os.path.join(OUTPUT_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()