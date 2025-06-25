#!/usr/bin/env python3
"""
Copy all PNG images to dist/static-images for local serving
"""

import os
import shutil
from pathlib import Path

def copy_all_png_images():
    """Copy all PNG images to dist/static-images directory"""
    
    # Create dist/static-images directory structure
    dist_static_dir = Path("dist/static-images")
    dist_static_dir.mkdir(parents=True, exist_ok=True)
    
    # Create platform subdirectories
    for platform in ["unsplash", "pexels", "pixabay"]:
        platform_dir = dist_static_dir / platform
        platform_dir.mkdir(exist_ok=True)
    
    copied_count = 0
    
    # Copy from png directory
    png_dir = Path("png")
    if png_dir.exists():
        for platform_dir in png_dir.iterdir():
            if platform_dir.is_dir():
                platform_name = platform_dir.name
                dist_platform_dir = dist_static_dir / platform_name
                
                for png_file in platform_dir.glob("*.png"):
                    dest_file = dist_platform_dir / png_file.name
                    if not dest_file.exists():
                        shutil.copy2(png_file, dest_file)
                        copied_count += 1
                        print(f"✅ Copied: {png_file.name}")
                    else:
                        print(f"⏭️  Skipped: {png_file.name} (already exists)")
    
    # Also try to copy from old images directory if it exists
    old_images_dir = Path("images")
    if old_images_dir.exists():
        for png_file in old_images_dir.glob("*.png"):
            # For old images without platform prefix, put them in unsplash folder
            dest_file = dist_static_dir / "unsplash" / png_file.name
            if not dest_file.exists():
                shutil.copy2(png_file, dest_file)
                copied_count += 1
                print(f"✅ Copied old image: {png_file.name}")
    
    print(f"\n📊 Total images copied: {copied_count}")
    
    # List what we have now
    total_images = 0
    for platform_dir in dist_static_dir.iterdir():
        if platform_dir.is_dir():
            platform_count = len(list(platform_dir.glob("*.png")))
            total_images += platform_count
            print(f"📁 {platform_dir.name}: {platform_count} images")
    
    print(f"📊 Total images available: {total_images}")

if __name__ == "__main__":
    copy_all_png_images()