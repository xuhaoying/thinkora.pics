#!/usr/bin/env python3
import json
import os
from pathlib import Path

def main():
    # Get the directory paths
    project_dir = Path("/Users/xuhaoying/Desktop/100-Project/AI_Web/A005_AIPics/thinkora.pics")
    png_dir = project_dir / "png"
    metadata_file = project_dir / "metadata.json"
    
    # Get all PNG files in the directory
    png_files = set()
    if png_dir.exists():
        for file in png_dir.iterdir():
            if file.suffix.lower() == '.png':
                # Remove the .png extension to get just the ID
                png_files.add(file.stem)
    
    print(f"Total PNG files found: {len(png_files)}")
    
    # Load metadata.json
    metadata_ids = set()
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            for item in metadata:
                # Extract the ID from the unsplash.id field
                if 'unsplash' in item and 'id' in item['unsplash']:
                    metadata_ids.add(item['unsplash']['id'])
    
    print(f"Total metadata entries found: {len(metadata_ids)}")
    
    # Find PNG files without metadata
    png_without_metadata = png_files - metadata_ids
    print(f"\n{'='*60}")
    print(f"PNG files WITHOUT corresponding metadata entries: {len(png_without_metadata)}")
    print(f"{'='*60}")
    if png_without_metadata:
        for png_id in sorted(png_without_metadata):
            print(f"  - {png_id}.png")
    else:
        print("  (None - all PNG files have metadata)")
    
    # Find metadata without PNG files
    metadata_without_png = metadata_ids - png_files
    print(f"\n{'='*60}")
    print(f"Metadata entries WITHOUT corresponding PNG files: {len(metadata_without_png)}")
    print(f"{'='*60}")
    if metadata_without_png:
        for meta_id in sorted(metadata_without_png):
            print(f"  - {meta_id}")
    else:
        print("  (None - all metadata entries have PNG files)")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total PNG files: {len(png_files)}")
    print(f"Total metadata entries: {len(metadata_ids)}")
    print(f"PNG files without metadata: {len(png_without_metadata)}")
    print(f"Metadata entries without PNG: {len(metadata_without_png)}")
    print(f"Matching entries: {len(png_files & metadata_ids)}")

if __name__ == "__main__":
    main()