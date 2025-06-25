#!/usr/bin/env python3
"""
每日自动化管道主脚本
协调图片获取、处理、上传的完整流程
"""

import os
import json
import logging
import time
from datetime import datetime
import schedule
import sys
from typing import Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# 导入各个模块
from daily_fetch_images import MultiPlatformImageFetcher
from daily_process_images import ImageProcessor
from daily_upload_to_r2 import R2Uploader

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/daily_pipeline_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 邮件配置（可选）
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT', 587)
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')

class DailyPipeline:
    def __init__(self):
        self.fetcher = MultiPlatformImageFetcher()
        self.processor = ImageProcessor()
        self.uploader = R2Uploader()
        
        # 创建日志目录
        os.makedirs('logs', exist_ok=True)
        os.makedirs('reports', exist_ok=True)
    
    def send_notification(self, subject: str, content: str):
        """发送邮件通知（可选）"""
        if not all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, NOTIFICATION_EMAIL]):
            logger.info("Email notification not configured, skipping")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = SMTP_USERNAME
            msg['To'] = NOTIFICATION_EMAIL
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'html'))
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Notification sent: {subject}")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
    
    def generate_daily_report(self, fetch_report: Dict, process_report: Dict, upload_report: Dict) -> str:
        """生成每日报告"""
        report_date = datetime.now().strftime("%Y-%m-%d")
        
        html_content = f"""
        <html>
        <body>
        <h2>Thinkora.pics Daily Report - {report_date}</h2>
        
        <h3>1. Image Fetching</h3>
        <ul>
            <li>Search Query: {fetch_report.get('query', 'N/A')}</li>
            <li>Total Found: {fetch_report.get('total_found', 0)}</li>
            <li>Downloaded: {fetch_report.get('downloaded', 0)}</li>
            <li>Platforms:
                <ul>
                    <li>Unsplash: {fetch_report.get('platforms', {}).get('unsplash', 0)}</li>
                    <li>Pexels: {fetch_report.get('platforms', {}).get('pexels', 0)}</li>
                    <li>Pixabay: {fetch_report.get('platforms', {}).get('pixabay', 0)}</li>
                </ul>
            </li>
        </ul>
        
        <h3>2. Image Processing</h3>
        <ul>
            <li>Total Processed: {process_report.get('total_processed', 0)}</li>
            <li>Successful: {process_report.get('successful', 0)}</li>
            <li>Low Quality: {process_report.get('low_quality', 0)}</li>
            <li>Errors: {process_report.get('errors', 0)}</li>
            <li>Success Rate: {process_report.get('success_rate', 0)}%</li>
        </ul>
        
        <h3>3. R2 Upload</h3>
        <ul>
            <li>New Images Uploaded: {upload_report.get('new_images', 0)}</li>
            <li>Total Files Uploaded: {upload_report.get('total_files', 0)}</li>
            <li>Failed Uploads: {upload_report.get('failed_uploads', 0)}</li>
            <li>Total Images in R2: {upload_report.get('total_images_in_r2', 0)}</li>
        </ul>
        
        <h3>Summary</h3>
        <p>Pipeline completed successfully. Added {upload_report.get('new_images', 0)} new transparent images to the platform.</p>
        
        </body>
        </html>
        """
        
        return html_content
    
    def run_pipeline(self):
        """运行完整的每日管道"""
        logger.info("=== Starting Daily Pipeline ===")
        start_time = time.time()
        
        try:
            # 步骤1：获取图片
            logger.info("Step 1: Fetching images from platforms")
            fetch_report = self.fetcher.run_daily_fetch(images_per_platform=3)  # 测试时只获取3张
            
            # 步骤2：处理图片
            logger.info("Step 2: Processing images (removing backgrounds)")
            process_report = self.processor.run_daily_processing(max_workers=4)
            
            # 步骤3：上传到R2
            logger.info("Step 3: Uploading to Cloudflare R2")
            upload_report = self.uploader.run_daily_upload(max_workers=4)
            
            # 生成综合报告
            daily_report = {
                'date': datetime.now().isoformat(),
                'pipeline_status': 'success',
                'execution_time': round(time.time() - start_time, 2),
                'fetch_report': fetch_report,
                'process_report': process_report,
                'upload_report': upload_report
            }
            
            # 保存报告
            report_file = f"reports/daily_report_{datetime.now().strftime('%Y%m%d')}.json"
            with open(report_file, 'w') as f:
                json.dump(daily_report, f, indent=2)
            
            # 发送通知
            html_report = self.generate_daily_report(fetch_report, process_report, upload_report)
            self.send_notification(
                f"Thinkora.pics Daily Report - {datetime.now().strftime('%Y-%m-%d')}",
                html_report
            )
            
            logger.info(f"=== Pipeline Completed Successfully in {daily_report['execution_time']}s ===")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            
            # 错误报告
            error_report = {
                'date': datetime.now().isoformat(),
                'pipeline_status': 'failed',
                'error': str(e),
                'execution_time': round(time.time() - start_time, 2)
            }
            
            report_file = f"reports/error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(error_report, f, indent=2)
            
            # 发送错误通知
            self.send_notification(
                f"Thinkora.pics Pipeline Error - {datetime.now().strftime('%Y-%m-%d')}",
                f"<h2>Pipeline Error</h2><p>Error: {str(e)}</p><p>Please check the logs for details.</p>"
            )
            
            raise

def main():
    """主函数"""
    pipeline = DailyPipeline()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--now':
        # 立即运行一次
        logger.info("Running pipeline immediately")
        pipeline.run_pipeline()
    else:
        # 设置定时任务
        logger.info("Setting up scheduled tasks")
        
        # 每天凌晨2点运行
        schedule.every().day.at("02:00").do(pipeline.run_pipeline)
        
        # 也可以设置多个时间点
        # schedule.every().day.at("08:00").do(pipeline.run_pipeline)
        # schedule.every().day.at("20:00").do(pipeline.run_pipeline)
        
        logger.info("Daily pipeline scheduler started. Waiting for scheduled time...")
        logger.info("Next run scheduled at: 02:00")
        
        # 保持运行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    main()