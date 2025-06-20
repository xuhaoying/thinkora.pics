from rembg import remove, new_session
from PIL import Image
import pathlib, argparse, time
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--in", dest="inp", default="raw")
parser.add_argument("--out", dest="out", default="png")
parser.add_argument("--model", default="u2net", help="u2net, silueta, isnet-general-use")
args = parser.parse_args()

pathlib.Path(args.out).mkdir(exist_ok=True)

# 使用指定模型创建会话
session = new_session(args.model)

success_count = 0
error_count = 0

print(f"🎨 开始去背景处理，使用模型: {args.model}")

for p in tqdm(list(pathlib.Path(args.inp).glob("*.jpg"))):
    try:
        start_time = time.time()
        
        with Image.open(p) as im:
            # 如果图片太大，先缩放以提高处理速度
            if max(im.size) > 2048:
                ratio = 2048 / max(im.size)
                new_size = tuple(int(dim * ratio) for dim in im.size)
                im = im.resize(new_size, Image.Resampling.LANCZOS)
            
            # 去背景
            output = remove(im, session=session)
            
            # 保存为 PNG
            output_path = f"{args.out}/{p.stem}.png"
            output.save(output_path, "PNG", optimize=True)
            
            process_time = time.time() - start_time
            success_count += 1
            
            # 记录处理时间（用于性能分析）
            if success_count % 10 == 0:
                print(f"📊 已处理 {success_count} 张，平均 {process_time:.2f}s/张")
                
    except Exception as e:
        error_count += 1
        print(f"❌ 处理 {p.name} 失败: {e}")

print(f"✅ 去背景完成！成功: {success_count}, 失败: {error_count}")