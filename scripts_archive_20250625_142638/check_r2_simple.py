#!/usr/bin/env python3
"""
Simple R2 status check using curl
"""

import subprocess
import os
from pathlib import Path
import json

def test_public_urls():
    """Test if images are accessible via public URLs"""
    print("🌐 Testing public URL access...\n")
    
    # Test different URL patterns
    test_cases = [
        {
            "name": "Custom domain with /images/ path",
            "url": "https://thinkora.pics/images/0V3uVjouHRc.png"
        },
        {
            "name": "Custom domain without /images/ path", 
            "url": "https://thinkora.pics/0V3uVjouHRc.png"
        },
        {
            "name": "R2 domain with /images/ path",
            "url": "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/images/0V3uVjouHRc.png"
        },
        {
            "name": "R2 domain without /images/ path",
            "url": "https://pub-484484e3162047379f59bcbb36fb442a.r2.dev/0V3uVjouHRc.png"
        }
    ]
    
    working_urls = []
    
    for test in test_cases:
        print(f"Testing: {test['name']}")
        print(f"URL: {test['url']}")
        
        try:
            # Use curl to test the URL
            result = subprocess.run(
                ['curl', '-I', '-s', test['url']],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Check if we got a 200 OK
            if 'HTTP/2 200' in result.stdout or 'HTTP/1.1 200' in result.stdout:
                print("✅ Success - Image is accessible")
                working_urls.append(test['url'])
            elif 'HTTP/2 404' in result.stdout or 'HTTP/1.1 404' in result.stdout:
                print("❌ 404 Not Found - Image doesn't exist at this path")
            elif 'HTTP/2 403' in result.stdout or 'HTTP/1.1 403' in result.stdout:
                print("❌ 403 Forbidden - Access denied (check bucket permissions)")
            else:
                print(f"❌ Failed - Response:\n{result.stdout[:200]}")
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout - Request took too long")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50 + "\n")
    
    return working_urls

def check_local_images():
    """Check what images we have locally"""
    print("\n📁 Checking local image files...\n")
    
    locations = [
        "static-images",
        "processed", 
        "downloads",
        "dist/static-images"
    ]
    
    all_images = []
    
    for location in locations:
        path = Path(location)
        if path.exists():
            # Find all PNG files
            png_files = list(path.rglob("*.png"))
            if png_files:
                print(f"✅ {location}: Found {len(png_files)} PNG files")
                # Show a few examples
                for f in png_files[:3]:
                    rel_path = f.relative_to(path)
                    print(f"   - {rel_path}")
                if len(png_files) > 3:
                    print(f"   ... and {len(png_files) - 3} more")
                
                all_images.extend(png_files)
            else:
                print(f"⚠️  {location}: No PNG files found")
        else:
            print(f"❌ {location}: Directory not found")
    
    print(f"\n📊 Total unique images found locally: {len(set(f.name for f in all_images))}")
    
    return all_images

def suggest_upload_script(local_images, working_urls):
    """Create an upload script based on findings"""
    print("\n🔧 Creating upload script...\n")
    
    if not local_images:
        print("❌ No local images found to upload")
        return
    
    # Determine the correct path structure based on working URLs
    use_images_prefix = any('/images/' in url for url in working_urls)
    
    script_content = '''#!/usr/bin/env python3
"""
Upload all images to R2
"""

import os
import subprocess
from pathlib import Path

def upload_to_r2():
    account_id = os.getenv('R2_ACCOUNT_ID')
    access_key = os.getenv('R2_ACCESS_KEY_ID') 
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    bucket_name = 'thinkora-images'
    
    if not all([account_id, access_key, secret_key]):
        print("❌ Missing R2 credentials")
        return
    
    # Find all PNG files
    images = []
'''
    
    # Add paths to find images
    for location in ['static-images', 'processed', 'downloads']:
        script_content += f'''
    if Path('{location}').exists():
        images.extend(Path('{location}').rglob('*.png'))
'''
    
    script_content += f'''
    
    print(f"Found {{len(images)}} images to upload")
    
    # Upload each image
    for img_path in images:
        # Determine R2 key
        filename = img_path.name
        r2_key = {'f"images/{filename}"' if use_images_prefix else 'filename'}
        
        # Use AWS CLI to upload
        cmd = [
            'aws', 's3', 'cp',
            str(img_path),
            f's3://{{bucket_name}}/{{r2_key}}',
            '--endpoint-url', f'https://{{account_id}}.r2.cloudflarestorage.com',
            '--no-verify-ssl'
        ]
        
        print(f"Uploading {{filename}} to {{r2_key}}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Uploaded {{filename}}")
        else:
            print(f"❌ Failed to upload {{filename}}: {{result.stderr}}")

if __name__ == "__main__":
    upload_to_r2()
'''
    
    with open('upload_all_to_r2.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created upload_all_to_r2.py")
    print("\nTo use it:")
    print("1. Install AWS CLI: brew install awscli")
    print("2. Configure AWS credentials for R2:")
    print("   aws configure set aws_access_key_id $R2_ACCESS_KEY_ID")
    print("   aws configure set aws_secret_access_key $R2_SECRET_ACCESS_KEY")
    print("3. Run: python3 upload_all_to_r2.py")

def main():
    print("🏥 R2 Configuration Diagnostic\n")
    
    # Test URLs
    working_urls = test_public_urls()
    
    # Check local images
    local_images = check_local_images()
    
    # Analysis
    print("\n📊 Analysis:\n")
    
    if working_urls:
        print(f"✅ Found {len(working_urls)} working URL pattern(s)")
        print("Working pattern:", working_urls[0])
    else:
        print("❌ No working URLs found - images need to be uploaded to R2")
        
    # Check if we need to upload
    if not working_urls and local_images:
        print("\n💡 Solution: Upload local images to R2")
        suggest_upload_script(local_images, working_urls)
    elif not local_images:
        print("\n❌ No local images found to upload!")
        print("💡 Try running the image fetch/download scripts first")
    
    # R2 configuration tips
    print("\n📌 R2 Configuration Checklist:")
    print("1. ✓ Public Access must be enabled in R2 bucket settings")
    print("2. ✓ Custom domain must be configured in Cloudflare")
    print("3. ✓ Images must be uploaded to the correct path")
    print("4. ✓ Check if you need 'images/' prefix in the path")

if __name__ == "__main__":
    main()