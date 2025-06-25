#!/bin/bash
# 设置每日自动化任务脚本

echo "=== Thinkora.pics Daily Automation Setup ==="
echo

# 检查Python环境
echo "Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# 安装依赖
echo "Installing required dependencies..."
pip3 install -r requirements.txt

# 创建必要的目录
echo "Creating necessary directories..."
mkdir -p raw/{unsplash,pexels,pixabay}
mkdir -p png/{unsplash,pexels,pixabay}
mkdir -p logs
mkdir -p reports
mkdir -p processed_backup/{unsplash,pexels,pixabay}

# 检查环境变量
echo "Checking environment variables..."
if [ ! -f ".env" ]; then
    echo "Error: .env file not found. Please create it from .env.example"
    echo "cp unsplash/.env.example .env"
    echo "Then edit .env and add your API keys"
    exit 1
fi

# 创建cron任务（Linux/Mac）
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Setting up cron job..."
    
    # 获取当前目录
    CURRENT_DIR=$(pwd)
    
    # 创建cron任务
    CRON_CMD="0 2 * * * cd $CURRENT_DIR && /usr/bin/python3 daily_pipeline.py >> logs/cron.log 2>&1"
    
    # 检查是否已存在
    if crontab -l 2>/dev/null | grep -q "daily_pipeline.py"; then
        echo "Cron job already exists"
    else
        # 添加到crontab
        (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
        echo "Cron job added successfully"
        echo "Pipeline will run daily at 2:00 AM"
    fi
    
    echo
    echo "To view current cron jobs: crontab -l"
    echo "To edit cron jobs: crontab -e"
    echo "To remove cron job: crontab -l | grep -v daily_pipeline.py | crontab -"
    
# Windows系统使用任务计划程序
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "For Windows, please use Task Scheduler:"
    echo "1. Open Task Scheduler"
    echo "2. Create Basic Task"
    echo "3. Set trigger: Daily at 2:00 AM"
    echo "4. Set action: Start a program"
    echo "5. Program: python"
    echo "6. Arguments: $CURRENT_DIR/daily_pipeline.py"
    echo "7. Start in: $CURRENT_DIR"
fi

echo
echo "=== Setup Complete ==="
echo
echo "To test the pipeline immediately, run:"
echo "python3 daily_pipeline.py --now"
echo
echo "To monitor the system, run:"
echo "python3 monitor_dashboard.py"
echo
echo "Logs are stored in: logs/"
echo "Reports are stored in: reports/"