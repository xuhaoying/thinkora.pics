#!/usr/bin/env python3
"""
Copy old PNG images from png/ directory to dist/static-images/unsplash/ with proper naming
"""

import os
import shutil
from pathlib import Path

def copy_old_images():
    """Copy old PNG images to dist/static-images/unsplash with unsplash_ prefix"""
    
    # Ensure dist/static-images/unsplash directory exists
    dist_unsplash_dir = Path("dist/static-images/unsplash")
    dist_unsplash_dir.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    skipped_count = 0
    
    # Copy PNG files from root of png/ directory (these are old images)
    png_dir = Path("png")
    if png_dir.exists():
        for png_file in png_dir.glob("*.png"):
            # Create destination filename with unsplash_ prefix
            dest_filename = f"unsplash_{png_file.name}"
            dest_file = dist_unsplash_dir / dest_filename
            
            if not dest_file.exists():
                shutil.copy2(png_file, dest_file)
                copied_count += 1
                print(f"✅ Copied: {png_file.name} -> {dest_filename}")
            else:
                skipped_count += 1
                print(f"⏭️  Skipped: {png_file.name} (already exists)")
    
    print(f"\n📊 Old images copied: {copied_count}")
    print(f"📊 Images skipped: {skipped_count}")
    
    # Check final count
    total_unsplash_images = len(list(dist_unsplash_dir.glob("*.png")))
    print(f"📁 Total unsplash images now: {total_unsplash_images}")

if __name__ == "__main__":
    copy_old_images()