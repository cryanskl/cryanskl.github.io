# -*- coding: utf-8 -*-
"""
rename_total.py
一次性处理 D:/GitBlog/_posts/ 中按“文件名日期”最新的 3 篇：
1) 校正文件名日期 = 第三行 frontmatter 的 date: YYYY-MM-DD
2) 移动并修正图片链接： (assets/xxx) -> (../assets/typoraimg/xxx)
   源图：D:/GitBlog/_posts/assets/xxx
   目标：D:/GitBlog/assets/typoraimg/xxx
不生成 .bak，直接覆盖保存。
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

# ===== 路径配置 =====
ROOT = Path(r"D:\GitBlog")
POSTS_DIR = ROOT / "_posts"
SRC_IMG_DIR = POSTS_DIR / "assets"                   # 源图片目录：D:\GitBlog\_posts\assets
DEST_IMG_DIR = ROOT / "assets" / "typoraimg"         # 目标图片目录：D:\GitBlog\assets\typoraimg

# ===== 规则 =====
# 文件名：YYYY-MM-DD-Title.md
FILENAME_DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)\.md$')
# 第三行：date: YYYY-MM-DD
FRONT_DATE_RE = re.compile(r'^date:\s*(\d{4}-\d{2}-\d{2})')
# Markdown 图片：![alt](assets/xxx.ext)
IMG_MD_RE = re.compile(r'!\[([^\]]*)\]\((assets/[^)]+)\)')

def parse_filename_date(p: Path):
    m = FILENAME_DATE_RE.match(p.name)
    if not m:
        return None, None
    date_str, title = m.groups()
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt, title
    except ValueError:
        return None, title

def list_latest_three(post_dir: Path):
    cand = []
    for p in post_dir.glob("*.md"):
        dt, _ = parse_filename_date(p)
        if dt:
            cand.append((dt, p))
    cand.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in cand[:3]]

def read_frontmatter_date(md_path: Path):
    """按约定读取第3行 date: YYYY-MM-DD；不满足则返回 None"""
    try:
        with md_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) < 3:
            return None
        m = FRONT_DATE_RE.match(lines[2].strip())
        return m.group(1) if m else None
    except Exception:
        return None

def rename_if_needed(md_path: Path):
    """
    若文件名日期 != 第三行 date: 则重命名。
    返回重命名后的 Path（若无变化，返回原 Path）。
    """
    m = FILENAME_DATE_RE.match(md_path.name)
    if not m:
        print(f"[SKIP] 文件名不符合规则：{md_path.name}")
        return md_path

    old_date, title_part = m.groups()
    fm_date = read_frontmatter_date(md_path)
    if not fm_date:
        print(f"[SKIP] 第三行未找到有效 date: {md_path.name}")
        return md_path

    if fm_date == old_date:
        print(f"[DATE] 已正确：{md_path.name}")
        return md_path

    new_name = f"{fm_date}-{title_part}.md"
    new_path = md_path.with_name(new_name)

    # 如目标已存在且不同文件，避免覆盖
    if new_path.exists() and new_path.resolve() != md_path.resolve():
        print(f"[WARN] 目标已存在，跳过重命名：{new_name}")
        return md_path

    md_path.rename(new_path)
    print(f"[RENAME] {md_path.name} -> {new_name}")
    return new_path

def ensure_dest_dir():
    DEST_IMG_DIR.mkdir(parents=True, exist_ok=True)

def move_image_if_needed(src_rel: str):
    """
    src_rel: 例如 'assets/image-xxx.png'
    仅取 basename，执行从 _posts/assets 移动到 assets/typoraimg。
    返回 (新相对路径, 是否移动或已存在)
    """
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
        print(f"[MOVE] {src_abs} -> {dest_abs}")
        return new_rel, True
    except Exception as e:
        print(f"[ERROR] 移动失败：{src_abs} -> {dest_abs}，原因：{e}")
        return new_rel, False

def rewrite_images(md_path: Path):
    """
    将 md 内形如 (assets/xxx) 的图片链接改为 (../assets/typoraimg/xxx)，并移动图片。
    不改已是 ../assets/typoraimg/ 的链接。
    """
    text = md_path.read_text(encoding="utf-8")

    def repl(m):
        alt = m.group(1)
        old_rel = m.group(2)
        if old_rel.startswith("../assets/typoraimg/"):
            return m.group(0)
        new_rel, _ = move_image_if_needed(old_rel)
        return f"![{alt}]({new_rel})"

    new_text = IMG_MD_RE.sub(repl, text)

    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        print(f"[IMG] 已修正图片链接：{md_path.name}")
    else:
        print(f"[IMG] 无需修改：{md_path.name}")

def main():
    if not POSTS_DIR.exists():
        print(f"[ERROR] 目录不存在：{POSTS_DIR}")
        return

    ensure_dest_dir()

    latest = list_latest_three(POSTS_DIR)
    if not latest:
        print("[INFO] 未找到符合命名规则的 md。")
        return

    print("将处理以下 3 篇（按文件名日期最新）：")
    for p in latest:
        print(" -", p.name)

    for p in latest:
        print("\n[PROC]", p.name)
        # 1) 先按第三行 date 校正文件名（若有重命名，更新路径变量）
        p2 = rename_if_needed(p)

        # 2) 再修正图片链接并移动图片
        rewrite_images(p2)

    print("\n[DONE] 日期校正与图片处理完成。")

if __name__ == "__main__":
    main()
