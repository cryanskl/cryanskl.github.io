---
title: "Jekyll useful scripts"
date: 2024-12-31 03:50:27 +0800
categories: [Tool]
tags: [website, typora]     # TAG names should always be lowercase
pin: false
---

## 1.和Typora兼并的脚本

因为typora用相对路径会有'./'或者'../', 但Jekyll构建html时,图片只能在'/'下

所以我们可以在根目录下建立'assets/img',将图片存在这个地方.

例如, 从typora来看,文件存在

```
![image-20250331014401283](../assets/img/image-20250331014401283.png)
```

但Jekyll需要图片的路径是`/assets/img/image-20250331014401283.png`, 因此,我们可以做个脚本放在`_plugins`下,命名为`remove_dotdot_assets.rb`

```
Jekyll::Hooks.register :site, :post_render do |page|
  # 确保只对 Markdown 文件进行处理
  if page.is_a?(Jekyll::Document) && page.extname == '.md'
    # 读取当前 Markdown 文件的内容
    content = page.content

    # 只在文件中包含图片语法时进行处理
    if content.include?("![") && content.include?("../")
      # 替换路径，将 '../assets' 改为 '/assets'
      updated_content = content.gsub(/\!\[([^\]]*)\]\(\.\.\/assets\//, '![\1](/assets/')

      # 更新页面内容
      page.content = updated_content
    end
  end
end

```

## 2.快速创建md的脚本

Jekyll文件的格式有点麻烦,所以写了一个python脚本命名为md.py. 

执行`python md.py `后, 输入标题就自动打开文章.

代码里只用改目标目录, 分类和标签

```
import os
import platform
from datetime import datetime
import subprocess

def create_markdown_file(title):
    # 获取当前日期
    today = datetime.today()
    date_str = today.strftime('%Y-%m-%d')

    # 生成文件名（格式：YYYY-MM-DD-xx.md）
    file_name = f"{date_str}-{title.lower().replace(' ', '-')}.md"

    # 目标目录
    target_directory = r"D:\xxxxxx"

    # 确保目标目录存在
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # 构建 Front Matter
    front_matter = f"""---
title: "{title}"
date: {today.strftime('%Y-%m-%d %H:%M:%S')} +0800
categories: [LLM]
tags: [foundation]     # TAG names should always be lowercase
---
"""

    # 创建并写入文件
    file_path = os.path.join(target_directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(front_matter)
        file.write("\n")  # 添加空行以分隔 YAML 和内容

    print(f"Markdown file created: {file_path}")

    # 根据操作系统打开文件
    if platform.system() == "Windows":
        os.startfile(file_path)  # Windows 打开文件
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", file_path])
    else:  # Linux
        subprocess.call(["xdg-open", file_path])

# 获取用户输入的标题
title_input = input("Enter the title for the markdown file: ")
create_markdown_file(title_input)

```

