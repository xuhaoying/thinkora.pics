import os, requests, json, argparse, pathlib, time
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--query", default="minimal desk")
parser.add_argument("--n", type=int, default=100)
args = parser.parse_args()

KEY = os.getenv("ACCESS_KEY")
if not KEY:
    print("❌ 请在 .env 文件中设置 ACCESS_KEY")
    exit(1)

pathlib.Path("raw").mkdir(exist_ok=True)

# Load existing metadata if it exists
if os.path.exists("metadata_raw.json"):
    with open("metadata_raw.json", "r", encoding="utf-8") as f:
        try:
            metadata = json.load(f)
        except json.JSONDecodeError:
            metadata = {} # Start fresh if JSON is invalid
else:
    metadata = {}

downloaded = 0
target = min(args.n, 1000)  # Unsplash 限制

print(f"🔍 搜索 '{args.query}'，目标下载 {target} 张...")

for page in range(1, target//30 + 2):
    if downloaded >= target:
        break
        
    try:
        r = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": args.query, "per_page": 30, "page": page, "order_by": "relevant"},
            headers={"Authorization": f"Client-ID {KEY}"}
        )
        r.raise_for_status()
        results = r.json()["results"]
        
        for ph in tqdm(results, desc=f"Page {page}"):
            if downloaded >= target:
                break
                
            try:
                # 下载图片
                img_resp = requests.get(ph["urls"]["full"], timeout=10)
                img_resp.raise_for_status()
                
                filename = f"raw/{ph['id']}.jpg"
                with open(filename, "wb") as f:
                    f.write(img_resp.content)
                
                # 保存元数据
                metadata[ph['id']] = {
                    "id": ph['id'],
                    "author": ph['user']['name'],
                    "author_url": ph['user']['links']['html'],
                    "unsplash_url": ph['links']['html'],
                    "description": ph.get('description') or ph.get('alt_description', ''),
                    "width": ph['width'],
                    "height": ph['height'],
                    "created_at": ph['created_at']
                }
                
                # 必需的下载统计请求
                requests.get(ph["links"]["download_location"],
                           headers={"Authorization": f"Client-ID {KEY}"})
                
                downloaded += 1
                time.sleep(0.1)  # 避免触发限流
                
            except Exception as e:
                print(f"⚠️ 下载 {ph['id']} 失败: {e}")
                continue
                
    except Exception as e:
        print(f"❌ 第 {page} 页请求失败: {e}")
        break

# 保存元数据
with open("metadata_raw.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✅ 完成！已下载 {downloaded} 张图片到 ./raw/ 目录")