#!/usr/bin/env python3
"""
测试Pixabay API连接和参数
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('.env') or load_dotenv('unsplash/.env')

def test_pixabay_api():
    # Test both API keys in the .env file
    api_keys = [
        "51008780-20fe13a52bde3f3efd30b126a",  # From line 23
        "5bkPrVrE2icbvZDSGBD11fYklA95hOCVO0QcwVV_i2M"  # From line 54
    ]
    
    env_key = os.getenv('PIXABAY_API_KEY')
    if env_key and env_key not in api_keys:
        api_keys.append(env_key)
    
    print(f"🔍 Testing {len(api_keys)} API keys...")
    
    for i, api_key in enumerate(api_keys, 1):
        print(f"\n🔑 Testing API Key {i}: {api_key[:10]}...")
        
        try:
            url = "https://pixabay.com/api/"
            params = {
                'key': api_key,
                'q': 'business',
                'per_page': 5
            }
            
            response = requests.get(url, params=params)
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Key {i} working! Found {data.get('totalHits', 0)} total images")
                print(f"📊 Sample results: {len(data.get('hits', []))} images returned")
                
                # Test different parameter combinations
                test_params = [
                    {'q': 'office'},
                    {'q': 'computer', 'image_type': 'photo'},
                    {'q': 'food', 'min_width': 800},
                    {'q': 'nature', 'safesearch': 'true'}
                ]
                
                success_count = 0
                for test_param in test_params:
                    test_param['key'] = api_key
                    test_param['per_page'] = 3
                    
                    test_response = requests.get(url, params=test_param)
                    if test_response.status_code == 200:
                        test_data = test_response.json()
                        print(f"  ✅ Query '{test_param['q']}': {test_data.get('totalHits', 0)} results")
                        success_count += 1
                    else:
                        print(f"  ❌ Query '{test_param['q']}': {test_response.status_code}")
                
                print(f"🎯 API Key {i} success rate: {success_count}/{len(test_params)} tests passed")
                
                if success_count > 0:
                    print(f"✅ Using API Key {i} for downloads: {api_key}")
                    return api_key
                
            else:
                print(f"❌ API Key {i} error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ API Key {i} exception: {e}")
    
    print("❌ No working API keys found")
    return None

if __name__ == "__main__":
    test_pixabay_api()