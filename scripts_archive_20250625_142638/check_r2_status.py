#!/usr/bin/env python3
"""
Check R2 bucket status and list objects
"""

import boto3
import os
from pathlib import Path
import requests

def check_r2_connection():
    """Check if we can connect to R2"""
    print("🔍 Checking R2 connection...")
    
    # R2 credentials
    account_id = os.getenv('R2_ACCOUNT_ID')
    access_key = os.getenv('R2_ACCESS_KEY_ID')
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('R2_BUCKET_NAME', 'thinkora-images')
    
    if not all([account_id, access_key, secret_key]):
        print("❌ Missing R2 credentials in environment variables")
        print("   Required: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY")
        return None
    
    print(f"✅ Found credentials for account: {account_id[:8]}...")
    print(f"📦 Bucket name: {bucket_name}")
    
    # Create S3 client for R2
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='auto'
        )
        print("✅ Successfully connected to R2")
        return s3_client, bucket_name
    except Exception as e:
        print(f"❌ Failed to connect to R2: {e}")
        return None

def list_r2_objects(s3_client, bucket_name, prefix='images/'):
    """List objects in R2 bucket"""
    print(f"\n📋 Listing objects in bucket '{bucket_name}' with prefix '{prefix}'...")
    
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=10  # List first 10 objects
        )
        
        if 'Contents' in response:
            print(f"✅ Found {response['KeyCount']} objects (showing first 10):")
            for obj in response['Contents']:
                print(f"   - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print(f"❌ No objects found with prefix '{prefix}'")
            
        # Try listing without prefix
        print(f"\n📋 Listing all objects in bucket (first 10)...")
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            MaxKeys=10
        )
        
        if 'Contents' in response:
            print(f"✅ Found {response['KeyCount']} objects:")
            for obj in response['Contents']:
                print(f"   - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("❌ No objects found in bucket")
            
    except Exception as e:
        print(f"❌ Error listing objects: {e}")

def test_public_urls():
    """Test if images are accessible via public URLs"""
    print("\n🌐 Testing public URL access...")
    
    test_urls = [
        "https://thinkora.pics/images/0V3uVjouHRc.png",
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/0V3uVjouHRc.png",
        "https://thinkora.pics/0V3uVjouHRc.png",
        "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/0V3uVjouHRc.png"
    ]
    
    for url in test_urls:
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url} - Accessible")
            else:
                print(f"❌ {url} - Status {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Error: {type(e).__name__}")

def check_local_images():
    """Check what images we have locally to upload"""
    print("\n📁 Checking local images...")
    
    # Check processed directory
    processed_dir = Path("static-images")
    if processed_dir.exists():
        png_files = list(processed_dir.rglob("*.png"))
        print(f"✅ Found {len(png_files)} PNG files in {processed_dir}")
        if png_files:
            print("   Sample files:")
            for f in png_files[:5]:
                print(f"   - {f.relative_to(processed_dir)}")
    else:
        print(f"❌ Directory {processed_dir} not found")
    
    # Check dist/static-images
    dist_static = Path("dist/static-images")
    if dist_static.exists():
        png_files = list(dist_static.rglob("*.png"))
        print(f"✅ Found {len(png_files)} PNG files in {dist_static}")
    
    # Check downloads directory
    downloads_dir = Path("downloads")
    if downloads_dir.exists():
        png_files = list(downloads_dir.rglob("*.png"))
        print(f"✅ Found {len(png_files)} PNG files in {downloads_dir}")

def main():
    print("🏥 R2 Bucket Status Check\n")
    
    # Check R2 connection
    result = check_r2_connection()
    if result:
        s3_client, bucket_name = result
        
        # List objects
        list_r2_objects(s3_client, bucket_name)
    
    # Test public URLs
    test_public_urls()
    
    # Check local images
    check_local_images()
    
    print("\n💡 Next steps:")
    print("1. If no images in R2, run: python3 upload_all_images_to_r2.py")
    print("2. Check R2 bucket settings for public access")
    print("3. Verify custom domain configuration in Cloudflare")

if __name__ == "__main__":
    main()