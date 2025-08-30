# -*- coding: utf-8 -*-
"""
renameimg.py  (no .bak version)
在 D:\GitBlog\_posts\ 中选择按“文件名中的日期”排序最新的 3 篇 md，
将其中形如 !(...)(assets/xxx.ext) 的图片从 _posts/assets/ 移动到 /assets/typoraimg/，
并把 md 内路径从 (assets/xxx.ext) 改为 (../assets/typoraimg/xxx.ext)。
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

# 目录配置
POSTS_DIR = Path(r"D:\GitBlog\_posts")
SRC_IMG_DIR = POSTS_DIR / "assets"                   # D:\GitBlog\_posts\assets
DEST_IMG_DIR = Path(r"D:\GitBlog\assets\typoraimg")  # D:\GitBlog\assets\typoraimg

# 匹配形如：![alt](assets/xxx.ext)
IMG_MD_PATTERN = re.compile(r'!\[([^\]]*)\]\((assets/[^)]+)\)')

def parse_date_from_name(p: Path):
    try:
        return datetime.strptime(p.name[:10], "%Y-%m-%d")
    except Exception:
        return None

def pick_latest_three(posts_dir: Path):
    candidates = []
    for p in posts_dir.glob("*.md"):
        dt = parse_date_from_name(p)
        if dt:
            candidates.append((dt, p))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in candidates[:3]]

def ensure_dest_dir():
    DEST_IMG_DIR.mkdir(parents=True, exist_ok=True)

def move_image_if_needed(src_rel: str):
    basename = Path(src_rel).name
    src_abs = SRC_IMG_DIR / basename
    dest_abs = DEST_IMG_DIR / basename
    new_rel = f"../assets/typoraimg/{basename}"

    if not src_abs.exists():
        print(f"[WARN] 源图不存在：{src_abs}")
        return new_rel, False

    if dest_abs.exists():
        print(f"[INFO] 目标已存在，跳过移动：{dest_abs}")
        return new_rel, True

    try:
        shutil.move(str(src_abs), str(dest_abs))
        print(f"[MOVE] {src_abs}  ->  {dest_abs}")
        return new_rel, True
    except Exception as e:
        print(f"[ERROR] 移动失败：{src_abs} -> {dest_abs}，原因：{e}")
        return new_rel, False

def process_md_file(md_path: Path):
    text = md_path.read_text(encoding="utf-8")

    def repl(m: re.Match):
        alt_text = m.group(1)
        old_rel = m.group(2)
        if old_rel.startswith("../assets/typoraimg/"):
            return m.group(0)
        new_rel, _ = move_image_if_needed(old_rel)
        return f"![{alt_text}]({new_rel})"

    new_text = IMG_MD_PATTERN.sub(repl, text)

    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        print(f"[OK] 已写入：{md_path.name}")
    else:
        print(f"[SKIP] 未发现需要替换的链接：{md_path.name}")

def main():
    if not POSTS_DIR.exists():
        print(f"[ERROR] 目录不存在：{POSTS_DIR}")
        return
    ensure_dest_dir()

    latest_posts = pick_latest_three(POSTS_DIR)
    if not latest_posts:
        print("[INFO] 未找到符合命名规范的 md 文件。")
        return

    print("将处理以下 3 个最新 md：")
    for p in latest_posts:
        print(" -", p.name)

    for p in latest_posts:
        print("\n[PROC]", p.name)
        process_md_file(p)

    print("\n[DONE] 图片移动与路径修正完成（无 .bak 备份）。")

if __name__ == "__main__":
    main()
