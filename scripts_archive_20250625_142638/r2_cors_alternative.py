#!/usr/bin/env python3
"""
R2 CORS配置的替代方案
如果Cloudflare控制台无法设置CORS，可以尝试这些方法
"""

import os
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('.env') or load_dotenv('unsplash/.env')

def generate_cors_json():
    """生成CORS配置JSON文件"""
    
    # 标准CORS配置
    cors_config = {
        "CORSRules": [
            {
                "ID": "allow-thinkora-pics",
                "AllowedOrigins": [
                    "https://thinkora.pics",
                    "https://www.thinkora.pics",
                    "http://localhost:3000",
                    "http://localhost:8080",
                    "http://127.0.0.1:3000",
                    "http://127.0.0.1:8080"
                ],
                "AllowedMethods": ["GET", "HEAD"],
                "AllowedHeaders": ["*"],
                "ExposeHeaders": [
                    "ETag",
                    "Content-Type",
                    "Content-Length",
                    "Date"
                ],
                "MaxAgeSeconds": 3600
            }
        ]
    }
    
    # 保存配置文件
    with open('r2_cors_config.json', 'w') as f:
        json.dump(cors_config, f, indent=2)
    
    print("✅ CORS配置文件已生成: r2_cors_config.json")
    print("\n请尝试以下方法：")
    print("\n方法1: 简化CORS配置")
    print("在Cloudflare控制台中只添加最基本的配置：")
    print("- Allowed Origins: *")
    print("- Allowed Methods: GET")
    print("- Allowed Headers: *")
    print("\n方法2: 使用Cloudflare Workers")
    print("创建一个Worker来处理CORS头：")
    
    worker_code = '''
// Cloudflare Worker代码
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // 获取原始响应
  const response = await fetch(request)
  
  // 创建新的响应，添加CORS头
  const newResponse = new Response(response.body, response)
  
  // 添加CORS头
  newResponse.headers.set('Access-Control-Allow-Origin', '*')
  newResponse.headers.set('Access-Control-Allow-Methods', 'GET, HEAD')
  newResponse.headers.set('Access-Control-Allow-Headers', '*')
  newResponse.headers.set('Access-Control-Max-Age', '3600')
  
  return newResponse
}
'''
    
    with open('cors_worker.js', 'w') as f:
        f.write(worker_code)
    
    print("\n✅ Worker代码已生成: cors_worker.js")
    
    print("\n方法3: 使用Transform Rules")
    print("在Cloudflare控制台 > Rules > Transform Rules > Response Headers中添加：")
    print("- When: Hostname equals 'img.thinkora.pics'")
    print("- Then: Add Header")
    print("  - Header name: Access-Control-Allow-Origin")
    print("  - Value: *")
    
    # 生成简化版CORS配置
    simple_cors = [
        {
            "AllowedOrigins": ["*"],
            "AllowedMethods": ["GET"],
            "AllowedHeaders": ["*"]
        }
    ]
    
    with open('simple_cors.json', 'w') as f:
        json.dump(simple_cors, f, indent=2)
    
    print("\n✅ 简化CORS配置已生成: simple_cors.json")
    print("\n如果以上方法都不行，可以考虑：")
    print("1. 使用Cloudflare Pages Functions")
    print("2. 设置自定义域名的Page Rules")
    print("3. 联系Cloudflare支持")

def check_r2_public_access():
    """检查R2的公共访问设置"""
    print("\n🔍 R2公共访问检查清单：")
    print("1. 确保R2存储桶已启用公共访问")
    print("2. 检查是否有自定义域名设置")
    print("3. 确认公共URL格式正确")
    
    r2_public_url = os.getenv('R2_PUBLIC_URL', 'https://img.thinkora.pics')
    print(f"\n当前配置的公共URL: {r2_public_url}")
    
    print("\n测试URL:")
    test_image = f"{r2_public_url}/images/pixabay_business_1051697.png"
    print(f"curl -I {test_image}")
    
    print("\n如果返回403错误，需要：")
    print("1. 在R2设置中启用'Public Access'")
    print("2. 确保域名已正确绑定到R2存储桶")

if __name__ == "__main__":
    print("🛠️ R2 CORS配置替代方案")
    print("="*50)
    
    generate_cors_json()
    check_r2_public_access()
    
    print("\n💡 最简单的解决方案：")
    print("如果CORS配置持续失败，可以暂时使用以下方法：")
    print("1. 在CORS配置中，只填写一个星号 * 作为Allowed Origins")
    print("2. 这将允许所有域名访问，虽然不够安全但能快速解决问题")
    print("3. 等功能正常后再逐步收紧CORS策略")