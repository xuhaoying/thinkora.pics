#!/usr/bin/env python3
"""
监控仪表板 - 查看系统状态和统计信息
"""

import os
import json
import glob
from datetime import datetime, timedelta
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

class MonitorDashboard:
    def __init__(self):
        self.reports_dir = 'reports'
        self.logs_dir = 'logs'
        
    def load_recent_reports(self, days: int = 7) -> List[Dict[str, Any]]:
        """加载最近几天的报告"""
        reports = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 查找所有日报文件
        report_files = glob.glob(os.path.join(self.reports_dir, 'daily_report_*.json'))
        
        for report_file in report_files:
            try:
                with open(report_file, 'r') as f:
                    report = json.load(f)
                    
                report_date = datetime.fromisoformat(report['date'])
                if report_date >= cutoff_date:
                    reports.append(report)
            except Exception as e:
                print(f"Error loading {report_file}: {e}")
        
        # 按日期排序
        reports.sort(key=lambda x: x['date'])
        return reports
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        stats = {
            'total_images': 0,
            'by_platform': defaultdict(int),
            'by_category': defaultdict(int),
            'storage_usage': 0,
            'average_quality_score': 0,
            'average_transparency_ratio': 0
        }
        
        # 加载元数据
        if os.path.exists('metadata_r2.json'):
            with open('metadata_r2.json', 'r') as f:
                metadata = json.load(f)
                
            stats['total_images'] = len(metadata)
            
            quality_scores = []
            transparency_ratios = []
            
            for item in metadata:
                stats['by_platform'][item.get('platform', 'unknown')] += 1
                stats['by_category'][item.get('category', 'other')] += 1
                stats['storage_usage'] += item.get('fileSize', 0)
                
                if 'qualityScore' in item:
                    quality_scores.append(item['qualityScore'])
                if 'transparencyRatio' in item:
                    transparency_ratios.append(item['transparencyRatio'])
            
            if quality_scores:
                stats['average_quality_score'] = sum(quality_scores) / len(quality_scores)
            if transparency_ratios:
                stats['average_transparency_ratio'] = sum(transparency_ratios) / len(transparency_ratios)
        
        # 转换存储大小为MB
        stats['storage_usage_mb'] = round(stats['storage_usage'] / (1024 * 1024), 2)
        
        return dict(stats)
    
    def generate_performance_chart(self, reports: List[Dict[str, Any]]):
        """生成性能图表"""
        if not reports:
            return
        
        dates = []
        fetched = []
        processed = []
        uploaded = []
        
        for report in reports:
            date = datetime.fromisoformat(report['date']).strftime('%m-%d')
            dates.append(date)
            
            fetch_report = report.get('fetch_report', {})
            process_report = report.get('process_report', {})
            upload_report = report.get('upload_report', {})
            
            fetched.append(fetch_report.get('downloaded', 0))
            processed.append(process_report.get('successful', 0))
            uploaded.append(upload_report.get('new_images', 0))
        
        # 创建图表
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(dates, fetched, 'o-', label='Fetched', linewidth=2, markersize=8)
        plt.plot(dates, processed, 's-', label='Processed', linewidth=2, markersize=8)
        plt.plot(dates, uploaded, '^-', label='Uploaded', linewidth=2, markersize=8)
        plt.xlabel('Date')
        plt.ylabel('Number of Images')
        plt.title('Daily Image Pipeline Performance')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # 成功率图表
        plt.subplot(1, 2, 2)
        success_rates = []
        for report in reports:
            process_report = report.get('process_report', {})
            rate = process_report.get('success_rate', 0)
            success_rates.append(rate)
        
        plt.bar(dates, success_rates, color='green', alpha=0.7)
        plt.xlabel('Date')
        plt.ylabel('Success Rate (%)')
        plt.title('Processing Success Rate')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('reports/performance_chart.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def print_dashboard(self):
        """打印监控仪表板"""
        print("\n" + "="*60)
        print("THINKORA.PICS MONITORING DASHBOARD")
        print("="*60)
        print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # 系统统计
        stats = self.get_system_stats()
        print("\n📊 SYSTEM STATISTICS")
        print(f"Total Images: {stats['total_images']}")
        print(f"Storage Usage: {stats['storage_usage_mb']} MB")
        print(f"Average Quality Score: {stats['average_quality_score']:.1f}")
        print(f"Average Transparency Ratio: {stats['average_transparency_ratio']:.2%}")
        
        print("\n📱 BY PLATFORM:")
        for platform, count in stats['by_platform'].items():
            print(f"  - {platform.capitalize()}: {count}")
        
        print("\n📁 BY CATEGORY:")
        for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {category.capitalize()}: {count}")
        
        # 最近7天的报告
        reports = self.load_recent_reports(7)
        if reports:
            print("\n📈 LAST 7 DAYS PERFORMANCE:")
            print(f"{'Date':<12} {'Fetched':<10} {'Processed':<12} {'Uploaded':<10} {'Success Rate':<12}")
            print("-" * 60)
            
            for report in reports[-7:]:
                date = datetime.fromisoformat(report['date']).strftime('%Y-%m-%d')
                fetch = report.get('fetch_report', {}).get('downloaded', 0)
                process = report.get('process_report', {}).get('successful', 0)
                upload = report.get('upload_report', {}).get('new_images', 0)
                rate = report.get('process_report', {}).get('success_rate', 0)
                
                print(f"{date:<12} {fetch:<10} {process:<12} {upload:<10} {rate:<12.1f}%")
            
            # 生成图表
            self.generate_performance_chart(reports)
            print("\n✅ Performance chart saved to: reports/performance_chart.png")
        
        # 检查错误
        error_files = glob.glob(os.path.join(self.reports_dir, 'error_report_*.json'))
        if error_files:
            print(f"\n⚠️  RECENT ERRORS: {len(error_files)} error reports found")
            
            # 显示最近的错误
            latest_error = max(error_files, key=os.path.getctime)
            with open(latest_error, 'r') as f:
                error_data = json.load(f)
            print(f"  Latest error: {error_data.get('error', 'Unknown')} at {error_data.get('date', 'Unknown')}")
        
        print("\n" + "="*60)
    
    def generate_html_report(self):
        """生成HTML格式的报告"""
        stats = self.get_system_stats()
        reports = self.load_recent_reports(7)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Thinkora.pics Monitor Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; text-align: center; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
                .stat-card {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
                .stat-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
                .stat-label {{ color: #666; margin-top: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                .chart-container {{ text-align: center; margin: 20px 0; }}
                .timestamp {{ text-align: center; color: #666; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Thinkora.pics Monitoring Dashboard</h1>
                <p class="timestamp">Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h2>System Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{stats['total_images']}</div>
                        <div class="stat-label">Total Images</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['storage_usage_mb']} MB</div>
                        <div class="stat-label">Storage Usage</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['average_quality_score']:.1f}</div>
                        <div class="stat-label">Avg Quality Score</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['average_transparency_ratio']:.1%}</div>
                        <div class="stat-label">Avg Transparency</div>
                    </div>
                </div>
                
                <h2>Recent Performance</h2>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Fetched</th>
                        <th>Processed</th>
                        <th>Uploaded</th>
                        <th>Success Rate</th>
                    </tr>
        """
        
        for report in reports[-7:]:
            date = datetime.fromisoformat(report['date']).strftime('%Y-%m-%d')
            fetch = report.get('fetch_report', {}).get('downloaded', 0)
            process = report.get('process_report', {}).get('successful', 0)
            upload = report.get('upload_report', {}).get('new_images', 0)
            rate = report.get('process_report', {}).get('success_rate', 0)
            
            html_content += f"""
                    <tr>
                        <td>{date}</td>
                        <td>{fetch}</td>
                        <td>{process}</td>
                        <td>{upload}</td>
                        <td>{rate:.1f}%</td>
                    </tr>
            """
        
        html_content += """
                </table>
                
                <div class="chart-container">
                    <h2>Performance Chart</h2>
                    <img src="performance_chart.png" alt="Performance Chart" style="max-width: 100%; height: auto;">
                </div>
            </div>
        </body>
        </html>
        """
        
        with open('reports/dashboard.html', 'w') as f:
            f.write(html_content)
        
        print("\n✅ HTML dashboard saved to: reports/dashboard.html")


if __name__ == "__main__":
    dashboard = MonitorDashboard()
    dashboard.print_dashboard()
    dashboard.generate_html_report()