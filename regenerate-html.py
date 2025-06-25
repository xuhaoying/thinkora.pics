#!/usr/bin/env python3
"""Regenerate HTML pages from updated metadata"""

import json
import os
from jinja2 import Template

# Read metadata
with open('dist/metadata.json', 'r') as f:
    metadata = json.load(f)

# Read templates
with open('templates/index_template.html', 'r') as f:
    index_template = Template(f.read())

with open('templates/detail_template.html', 'r') as f:
    detail_template = Template(f.read())

# Generate index page
index_html = index_template.render(images=metadata)
with open('dist/index.html', 'w') as f:
    f.write(index_html)
print("✓ Generated index.html")

# Generate showcase page (copy existing)
import shutil
if os.path.exists('dist/showcase.html'):
    print("✓ Showcase page exists")

# Generate detail pages
for i, image in enumerate(metadata):
    # Find previous and next images
    prev_image = metadata[i-1] if i > 0 else None
    next_image = metadata[i+1] if i < len(metadata)-1 else None
    
    # Generate detail page
    detail_html = detail_template.render(
        title=image['title'],
        description=image['description'],
        image_url=image['url'],
        page_url=f"https://thinkora.pics/images/{image['id']}.html",
        author_name=image.get('author', 'Unknown'),
        author_url=image.get('author_url', '#'),
        dimensions=f"{image.get('width', 'N/A')} x {image.get('height', 'N/A')}",
        file_size="N/A",
        category=image.get('category', 'photography'),
        download_url=image['url'],
        prev_image=prev_image,
        next_image=next_image
    )
    
    # Save detail page
    detail_path = f"dist/images/{image['id']}.html"
    with open(detail_path, 'w') as f:
        f.write(detail_html)

print(f"✓ Generated {len(metadata)} detail pages")

# Generate sitemap
sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://thinkora.pics/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://thinkora.pics/showcase.html</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
"""

for image in metadata:
    sitemap_content += f"""    <url>
        <loc>https://thinkora.pics/images/{image['id']}.html</loc>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
"""

sitemap_content += "</urlset>"

with open('dist/sitemap.xml', 'w') as f:
    f.write(sitemap_content)
print("✓ Generated sitemap.xml")

print(f"\nTotal pages generated: {len(metadata) + 2}")