#!/usr/bin/env python3
"""List all files in R2 bucket"""

import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# R2 configuration
ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID') or os.getenv('R2_ACCESS_KEY')
SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY') or os.getenv('R2_SECRET_KEY')
BUCKET_NAME = os.getenv('R2_BUCKET_NAME', 'thinkora-images')

# Create S3 client
s3_client = boto3.client(
    's3',
    endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name='auto'
)

try:
    # List all objects in the bucket
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' in response:
        print(f"Total files in R2: {len(response['Contents'])}")
        print("\nImage files in R2:")
        
        image_files = []
        for obj in response['Contents']:
            if obj['Key'].endswith('.png'):
                image_files.append(obj['Key'])
                print(f"  - {obj['Key']} (Size: {obj['Size']:,} bytes)")
        
        print(f"\nTotal PNG images: {len(image_files)}")
        
        # Check if all metadata images exist
        import json
        with open('dist/metadata.json', 'r') as f:
            metadata = json.load(f)
        
        print(f"\nMetadata has {len(metadata)} images")
        
        # Find missing images
        r2_image_ids = set(key.replace('images/', '').replace('.png', '') for key in image_files)
        metadata_ids = set(item['id'] for item in metadata)
        
        missing_in_r2 = metadata_ids - r2_image_ids
        extra_in_r2 = r2_image_ids - metadata_ids
        
        if missing_in_r2:
            print(f"\nImages in metadata but MISSING in R2 ({len(missing_in_r2)}):")
            for img_id in sorted(missing_in_r2):
                print(f"  - {img_id}")
        
        if extra_in_r2:
            print(f"\nImages in R2 but NOT in metadata ({len(extra_in_r2)}):")
            for img_id in sorted(extra_in_r2):
                print(f"  - {img_id}")
                
    else:
        print("No files found in R2 bucket")
        
except Exception as e:
    print(f"Error listing R2 files: {e}")
    print(f"Account ID: {ACCOUNT_ID}")
    print(f"Access Key ID: {ACCESS_KEY_ID[:10]}..." if ACCESS_KEY_ID else "None")
    print(f"Bucket Name: {BUCKET_NAME}")