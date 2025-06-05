import os
import re

# 设置你的 Markdown 文件目录
markdown_dir = r"D:\GitBlog\_posts"

# 正则匹配 Markdown 图片语法中 Windows 本地路径
# 匹配 ![xxx](D:\GitBlog\assets\typoraimg\xxxx.png)
pattern = re.compile(r'!\[(.*?)\]\((?:file:///)?D:\\GitBlog\\assets\\typoraimg\\([^)]+)\)')

# 替换前缀：从本地路径 → 相对路径
replace_prefix = r'../assets/typoraimg/'

# 遍历所有 Markdown 文件
for filename in os.listdir(markdown_dir):
    if filename.endswith(".md"):
        file_path = os.path.join(markdown_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 替换路径
        new_content = pattern.sub(
            lambda m: f"![{m.group(1)}]({replace_prefix}{m.group(2).replace('\\\\', '/')})",
            content
        )

        # 写入文件
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ 已替换: {filename}")
        else:
            print(f"🔍 无变化: {filename}")

print("🎉 完成全部 Markdown 文件处理。")
