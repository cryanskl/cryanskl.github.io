import os
import re
from datetime import datetime

# 固定要处理的目录
folder_path = r"D:\GitBlog\_posts"

# 正则：匹配文件名中日期前缀，例如 2025-04-09
filename_date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)\.md$')
# 正则：匹配 frontmatter 中的日期字段
date_line_pattern = re.compile(r'^date:\s*(\d{4}-\d{2}-\d{2})')

# --- 第一步：找出所有符合规则的文件，并解析日期 ---
candidates = []
for filename in os.listdir(folder_path):
    if not filename.endswith(".md"):
        continue
    match = filename_date_pattern.match(filename)
    if not match:
        continue
    date_str, _ = match.groups()
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        candidates.append((dt, filename))
    except ValueError:
        continue

# --- 第二步：按日期排序，取最新三篇 ---
candidates.sort(key=lambda x: x[0], reverse=True)
latest_files = [fn for _, fn in candidates[:3]]

print("将处理以下 3 个最新 md：")
for fn in latest_files:
    print(" -", fn)

# --- 第三步：逐个处理 ---
for filename in latest_files:
    file_path = os.path.join(folder_path, filename)
    match = filename_date_pattern.match(filename)
    if not match:
        print(f"跳过文件（文件名不符合规则）: {filename}")
        continue

    old_date, title_part = match.groups()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) < 3:
            print(f"跳过文件（行数不足）: {filename}")
            continue

        date_line = lines[2].strip()
        date_match = date_line_pattern.match(date_line)

        if not date_match:
            print(f"跳过文件（第三行无有效日期）: {filename}")
            continue

        new_date = date_match.group(1)

        if old_date == new_date:
            print(f"文件已是正确日期: {filename}")
            continue

        new_filename = f"{new_date}-{title_part}.md"
        new_path = os.path.join(folder_path, new_filename)

        os.rename(file_path, new_path)
        print(f"已重命名: {filename} -> {new_filename}")

    except Exception as e:
        print(f"处理文件 {filename} 时出错: {e}")
