import json, subprocess, time
from pathlib import Path

config = json.load(open("batch_config.json"))
total_downloaded = 0

for query in config["queries"]:
    print(f"\n🔍 处理查询: {query['term']} (目标: {query['count']} 张)")
    
    # 为每个查询创建子目录
    query_dir = f"raw_{query['term'].replace(' ', '_')}"
    Path(query_dir).mkdir(exist_ok=True)
    
    # 调用下载脚本
    cmd = f"python fetch.py --query '{query['term']}' --n {query['count']}"
    subprocess.run(cmd, shell=True)
    
    total_downloaded += query['count']
    print(f"✅ {query['term']} 完成，累计: {total_downloaded} 张")
    
    # 避免 API 限流
    time.sleep(2)

print(f"\n🎉 批量下载完成！总计目标: {total_downloaded} 张")