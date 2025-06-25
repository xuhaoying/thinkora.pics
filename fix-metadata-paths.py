#!/usr/bin/env python3
"""Fix metadata paths to match actual R2 structure"""

import json

# Read metadata
with open('dist/metadata.json', 'r') as f:
    metadata = json.load(f)

# Map of incorrect IDs to correct paths
path_fixes = {
    'GZUwekngRYM': 'unsplash/unsplash_GZUwekngRYM',
    'mQ9vzpnjYnA': 'unsplash/unsplash_mQ9vzpnjYnA', 
    'uh_W-27b8Lw': 'unsplash/unsplash_uh_W-27b8Lw',
    '10727328': 'pexels/pexels_10727328',
    '8516791': 'pexels/pexels_8516791',
    '8532777': 'pexels/pexels_8532777'
}

# Update metadata
updated_count = 0
for item in metadata:
    if item['id'] in path_fixes:
        new_path = path_fixes[item['id']]
        item['url'] = f"https://thinkora.pics/images/{new_path}.png"
        print(f"Updated {item['id']} -> {new_path}")
        updated_count += 1

# Save updated metadata
with open('dist/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"\nTotal images updated: {updated_count}")

# Also update metadata_r2.json if it exists
try:
    with open('metadata_r2.json', 'r') as f:
        metadata_r2 = json.load(f)
    
    for item in metadata_r2:
        if item['id'] in path_fixes:
            new_path = path_fixes[item['id']]
            item['url'] = f"https://thinkora.pics/images/{new_path}.png"
    
    with open('metadata_r2.json', 'w') as f:
        json.dump(metadata_r2, f, indent=2)
    print("Also updated metadata_r2.json")
except:
    print("metadata_r2.json not found or couldn't be updated")