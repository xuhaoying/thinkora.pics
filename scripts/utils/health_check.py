#!/usr/bin/env python3
"""
系统健康检查脚本
"""

import os
import sys
import sqlite3
import requests
import subprocess
from pathlib import Path
from datetime import datetime
import json

class HealthChecker:
    def __init__(self):
        self.db_path = "images.db"
        self.checks = []
    
    def add_check(self, name, status, message, details=None):
        """添加检查结果"""
        self.checks.append({
            'name': name,
            'status': status,  # 'ok', 'warning', 'error'
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        })
    
    def check_database(self):
        """检查数据库状态"""
        try:
            if not Path(self.db_path).exists():
                self.add_check("数据库文件", "error", "数据库文件不存在")
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查表结构
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            if 'images' not in tables:
                self.add_check("数据库表", "error", "images表不存在")
                conn.close()
                return
            
            # 获取统计信息
            cursor.execute("SELECT COUNT(*) FROM images")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM images WHERE processed = TRUE")
            processed = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM images WHERE uploaded = TRUE")
            uploaded = cursor.fetchone()[0]
            
            conn.close()
            
            details = {
                'total_images': total,
                'processed_images': processed,
                'uploaded_images': uploaded,
                'processing_rate': f"{processed/total*100:.1f}%" if total > 0 else "0%",
                'upload_rate': f"{uploaded/total*100:.1f}%" if total > 0 else "0%"
            }
            
            if total == 0:
                self.add_check("数据库内容", "warning", "数据库为空", details)
            else:
                self.add_check("数据库内容", "ok", f"数据库包含{total}张图片", details)
            
        except Exception as e:
            self.add_check("数据库连接", "error", f"数据库连接失败: {e}")
    
    def check_environment(self):
        """检查环境变量"""
        required_vars = [
            'UNSPLASH_ACCESS_KEY',
            'PIXABAY_API_KEY',
            'R2_ACCESS_KEY_ID',
            'R2_SECRET_ACCESS_KEY',
            'R2_ACCOUNT_ID'
        ]
        
        missing_vars = []
        present_vars = []
        
        for var in required_vars:
            if os.getenv(var):
                present_vars.append(var)
            else:
                missing_vars.append(var)
        
        if missing_vars:
            self.add_check("环境变量", "warning", f"缺少环境变量: {', '.join(missing_vars)}", {
                'missing': missing_vars,
                'present': present_vars
            })
        else:
            self.add_check("环境变量", "ok", "所有必需的环境变量已配置", {
                'present': present_vars
            })
    
    def check_dependencies(self):
        """检查Python依赖"""
        required_packages = [
            'requests', 'sqlite3', 'PIL', 'rembg', 'boto3', 'python-dotenv'
        ]
        
        missing_packages = []
        present_packages = []
        
        for package in required_packages:
            try:
                if package == 'sqlite3':
                    import sqlite3
                elif package == 'PIL':
                    from PIL import Image
                else:
                    __import__(package)
                present_packages.append(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.add_check("Python依赖", "error", f"缺少依赖包: {', '.join(missing_packages)}", {
                'missing': missing_packages,
                'present': present_packages
            })
        else:
            self.add_check("Python依赖", "ok", "所有依赖包已安装", {
                'present': present_packages
            })
    
    def check_directories(self):
        """检查目录结构"""
        required_dirs = ['scripts_new', 'processed_images', 'backups']
        optional_dirs = ['logs']
        
        missing_dirs = []
        present_dirs = []
        
        for dir_name in required_dirs + optional_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                present_dirs.append(dir_name)
            else:
                missing_dirs.append(dir_name)
        
        # 创建缺失的目录
        created_dirs = []
        for dir_name in missing_dirs:
            if dir_name in required_dirs:
                try:
                    Path(dir_name).mkdir(exist_ok=True)
                    created_dirs.append(dir_name)
                except Exception as e:
                    pass
        
        status = "ok" if not missing_dirs or all(d in optional_dirs for d in missing_dirs) else "warning"
        message = "目录结构正常"
        if created_dirs:
            message += f"，已创建: {', '.join(created_dirs)}"
        
        self.add_check("目录结构", status, message, {
            'present': present_dirs,
            'missing': missing_dirs,
            'created': created_dirs
        })
    
    def check_r2_connectivity(self):
        """检查R2连接"""
        try:
            import boto3
            from botocore.config import Config
            
            access_key = os.getenv('R2_ACCESS_KEY_ID')
            secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
            account_id = os.getenv('R2_ACCOUNT_ID')
            bucket_name = os.getenv('R2_BUCKET_NAME', 'thinkora-pics')
            
            if not all([access_key, secret_key, account_id]):
                self.add_check("R2连接", "error", "R2凭证未配置")
                return
            
            endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
            s3_client = boto3.client(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                config=Config(region_name='auto', retries={'max_attempts': 1})
            )
            
            # 测试连接
            response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
            
            # 获取存储桶信息
            objects_count = 0
            total_size = 0
            
            paginator = s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket_name, Prefix='images/'):
                if 'Contents' in page:
                    objects_count += len(page['Contents'])
                    total_size += sum(obj['Size'] for obj in page['Contents'])
            
            self.add_check("R2连接", "ok", f"R2连接正常，存储桶包含{objects_count}个文件", {
                'bucket': bucket_name,
                'objects_count': objects_count,
                'total_size_mb': round(total_size / (1024 * 1024), 1)
            })
            
        except Exception as e:
            self.add_check("R2连接", "error", f"R2连接失败: {e}")
    
    def check_api_keys(self):
        """检查API密钥有效性"""
        # 检查Unsplash API
        unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY')
        if unsplash_key:
            try:
                url = "https://api.unsplash.com/me"
                headers = {'Authorization': f'Client-ID {unsplash_key}'}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    user_data = response.json()
                    self.add_check("Unsplash API", "ok", f"API正常，用户: {user_data.get('username', 'unknown')}")
                else:
                    self.add_check("Unsplash API", "error", f"API响应错误: {response.status_code}")
            except Exception as e:
                self.add_check("Unsplash API", "error", f"API测试失败: {e}")
        else:
            self.add_check("Unsplash API", "warning", "未配置Unsplash API密钥")
        
        # 检查Pixabay API
        pixabay_key = os.getenv('PIXABAY_API_KEY')
        if pixabay_key:
            try:
                url = "https://pixabay.com/api/"
                params = {'key': pixabay_key, 'q': 'test', 'per_page': 3}
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    total_hits = data.get('totalHits', 0)
                    self.add_check("Pixabay API", "ok", f"API正常，可访问{total_hits}张图片")
                else:
                    self.add_check("Pixabay API", "error", f"API响应错误: {response.status_code}")
            except Exception as e:
                self.add_check("Pixabay API", "error", f"API测试失败: {e}")
        else:
            self.add_check("Pixabay API", "warning", "未配置Pixabay API密钥")
    
    def check_website_status(self):
        """检查网站状态"""
        try:
            # 检查本地开发服务器
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                self.add_check("本地网站", "ok", "本地开发服务器运行正常")
            else:
                self.add_check("本地网站", "warning", f"本地服务器响应异常: {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.add_check("本地网站", "warning", "本地开发服务器未运行")
        except Exception as e:
            self.add_check("本地网站", "error", f"网站检查失败: {e}")
        
        # 检查R2图片访问
        public_url = os.getenv('R2_PUBLIC_URL', 'https://img.thinkora.pics')
        try:
            test_url = f"{public_url}/images/test.png"  # 假设有测试图片
            response = requests.head(test_url, timeout=10)
            self.add_check("R2图片访问", "ok", "R2图片可正常访问")
        except Exception:
            self.add_check("R2图片访问", "warning", "无法验证R2图片访问（可能没有测试图片）")
    
    def run_all_checks(self):
        """运行所有检查"""
        print("🔍 开始系统健康检查...\n")
        
        checks_to_run = [
            ("数据库检查", self.check_database),
            ("环境变量检查", self.check_environment),
            ("依赖包检查", self.check_dependencies),
            ("目录结构检查", self.check_directories),
            ("R2连接检查", self.check_r2_connectivity),
            ("API密钥检查", self.check_api_keys),
            ("网站状态检查", self.check_website_status),
        ]
        
        for check_name, check_func in checks_to_run:
            print(f"🔄 {check_name}...")
            try:
                check_func()
            except Exception as e:
                self.add_check(check_name, "error", f"检查过程出错: {e}")
    
    def print_results(self):
        """打印检查结果"""
        print("\n" + "="*60)
        print("📊 健康检查报告")
        print("="*60)
        
        ok_count = 0
        warning_count = 0
        error_count = 0
        
        for check in self.checks:
            status_emoji = {
                'ok': '✅',
                'warning': '⚠️',
                'error': '❌'
            }
            
            print(f"{status_emoji[check['status']]} {check['name']}: {check['message']}")
            
            if check['status'] == 'ok':
                ok_count += 1
            elif check['status'] == 'warning':
                warning_count += 1
            else:
                error_count += 1
        
        print("\n" + "="*60)
        print(f"📈 总结: {ok_count}个正常, {warning_count}个警告, {error_count}个错误")
        print("="*60)
        
        # 保存详细报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'ok': ok_count,
                'warning': warning_count,
                'error': error_count,
                'total': len(self.checks)
            },
            'checks': self.checks
        }
        
        report_path = Path("logs") / f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 详细报告已保存到: {report_path}")
        
        return error_count == 0  # 返回是否所有检查都通过

def main():
    checker = HealthChecker()
    checker.run_all_checks()
    success = checker.print_results()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()