#!/usr/bin/env python3
import json
import os
from pathlib import Path

def main():
    # Get the directory paths
    project_dir = Path("/Users/xuhaoying/Desktop/100-Project/AI_Web/A005_AIPics/thinkora.pics")
    png_dir = project_dir / "png"
    raw_dir = project_dir / "raw"
    metadata_file = project_dir / "metadata.json"
    
    # Get all PNG files in the directory
    png_files = set()
    if png_dir.exists():
        for file in png_dir.iterdir():
            if file.suffix.lower() == '.png':
                png_files.add(file.stem)
    
    # Get all RAW files in the directory
    raw_files = set()
    if raw_dir.exists():
        for file in raw_dir.iterdir():
            if file.suffix.lower() in ['.jpg', '.jpeg']:
                raw_files.add(file.stem)
    
    # Load metadata.json
    metadata_ids = set()
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            for item in metadata:
                if 'unsplash' in item and 'id' in item['unsplash']:
                    metadata_ids.add(item['unsplash']['id'])
    
    # Find PNG files without metadata
    png_without_metadata = png_files - metadata_ids
    
    print(f"{'='*80}")
    print("DETAILED ANALYSIS OF PNG FILES WITHOUT METADATA")
    print(f"{'='*80}")
    print(f"\nTotal PNG files without metadata: {len(png_without_metadata)}\n")
    
    # Check if these PNG files have corresponding raw files
    png_with_raw = []
    png_without_raw = []
    
    for png_id in sorted(png_without_metadata):
        if png_id in raw_files:
            png_with_raw.append(png_id)
        else:
            png_without_raw.append(png_id)
    
    print(f"PNG files without metadata BUT WITH corresponding RAW files: {len(png_with_raw)}")
    if png_with_raw:
        for png_id in png_with_raw:
            print(f"  - {png_id}.png (has {png_id}.jpg)")
    
    print(f"\nPNG files without metadata AND WITHOUT corresponding RAW files: {len(png_without_raw)}")
    if png_without_raw:
        for png_id in png_without_raw:
            print(f"  - {png_id}.png (no raw file)")
    
    # Additional analysis - check raw files
    print(f"\n{'='*80}")
    print("RAW FILES ANALYSIS")
    print(f"{'='*80}")
    
    raw_without_png = raw_files - png_files
    raw_without_metadata = raw_files - metadata_ids
    
    print(f"\nTotal RAW files: {len(raw_files)}")
    print(f"RAW files without PNG: {len(raw_without_png)}")
    print(f"RAW files without metadata: {len(raw_without_metadata)}")
    
    if raw_without_metadata:
        print(f"\nRAW files without metadata entries:")
        for raw_id in sorted(raw_without_metadata):
            has_png = " (has PNG)" if raw_id in png_files else " (no PNG)"
            print(f"  - {raw_id}.jpg{has_png}")

if __name__ == "__main__":
    main()