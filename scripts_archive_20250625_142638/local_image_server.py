#!/usr/bin/env python3
"""
本地图片服务器 - 模拟R2服务
在实际上传到R2之前，可以使用这个服务器测试项目
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
import json
from urllib.parse import urlparse

class ImageServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # 设置根目录为项目目录
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        # 解析请求路径
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 如果请求的是 /images/ 路径下的图片
        if path.startswith('/images/'):
            # 提取图片文件名
            filename = os.path.basename(path)
            image_id = os.path.splitext(filename)[0]
            
            # 查找本地图片文件
            local_paths = [
                f'raw/pixabay/{filename}',
                f'raw/unsplash/{filename}',
                f'raw/pexels/{filename}',
                f'png/{image_id}.png'
            ]
            
            for local_path in local_paths:
                if os.path.exists(local_path):
                    # 设置正确的响应头
                    self.send_response(200)
                    if local_path.endswith('.png'):
                        self.send_header('Content-Type', 'image/png')
                    else:
                        self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Cache-Control', 'public, max-age=31536000')
                    self.end_headers()
                    
                    # 发送图片内容
                    with open(local_path, 'rb') as f:
                        self.wfile.write(f.read())
                    return
            
            # 如果没找到图片
            self.send_error(404, f"Image not found: {filename}")
        else:
            # 处理其他请求
            super().do_GET()

def update_local_urls():
    """临时更新URL到本地服务器"""
    import sqlite3
    
    print("📝 更新数据库URL到本地服务器...")
    
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 更新到本地服务器URL
    cursor.execute("""
        UPDATE images 
        SET url_thumbnail = 'http://localhost:8080/images/' || id || '.jpg',
            url_regular = 'http://localhost:8080/images/' || id || '.jpg',
            url_download = 'http://localhost:8080/images/' || id || '.jpg'
        WHERE tags != '[]'
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ 数据库URL已更新为本地服务器")
    
    # 更新metadata.json
    with open('metadata.json', 'r') as f:
        metadata = json.load(f)
    
    for image in metadata['images']:
        image_id = image['id']
        local_url = f'http://localhost:8080/images/{image_id}.jpg'
        image['urls'] = {
            'thumbnail': local_url,
            'regular': local_url,
            'download': local_url
        }
    
    with open('metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ metadata.json已更新为本地服务器")

def restore_r2_urls():
    """恢复R2的URL"""
    import sqlite3
    
    print("📝 恢复数据库URL到R2...")
    
    conn = sqlite3.connect('thinkora.db')
    cursor = conn.cursor()
    
    # 恢复到R2 URL
    cursor.execute("""
        UPDATE images 
        SET url_thumbnail = 'https://r2.thinkora.pics/images/' || id || '.jpg',
            url_regular = 'https://r2.thinkora.pics/images/' || id || '.jpg',
            url_download = 'https://r2.thinkora.pics/images/' || id || '.jpg'
        WHERE tags != '[]'
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ 数据库URL已恢复为R2")
    
    # 恢复metadata.json
    with open('metadata.json', 'r') as f:
        metadata = json.load(f)
    
    for image in metadata['images']:
        image_id = image['id']
        r2_url = f'https://r2.thinkora.pics/images/{image_id}.jpg'
        image['urls'] = {
            'thumbnail': r2_url,
            'regular': r2_url,
            'download': r2_url
        }
    
    with open('metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ metadata.json已恢复为R2")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--restore-r2':
            restore_r2_urls()
            return
        elif sys.argv[1] == '--help':
            print("使用方法:")
            print("  python3 local_image_server.py          # 启动本地服务器")
            print("  python3 local_image_server.py --restore-r2  # 恢复R2 URL")
            return
    
    # 更新URL到本地服务器
    update_local_urls()
    
    # 启动服务器
    port = 8080
    server_address = ('', port)
    httpd = HTTPServer(server_address, ImageServerHandler)
    
    print(f"\n🚀 本地图片服务器已启动!")
    print(f"📡 服务地址: http://localhost:{port}")
    print(f"🌐 图片URL格式: http://localhost:{port}/images/[图片ID].jpg")
    print(f"\n💡 使用说明:")
    print(f"   1. 在另一个终端运行: npm run dev")
    print(f"   2. 访问 http://localhost:3000 查看网站")
    print(f"   3. 按 Ctrl+C 停止服务器")
    print(f"\n⚠️ 停止服务器后，运行以下命令恢复R2 URL:")
    print(f"   python3 scripts/local_image_server.py --restore-r2")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")
        print("💡 记得运行: python3 scripts/local_image_server.py --restore-r2")

if __name__ == '__main__':
    main()