---
title: "Handy Jekyll Scripts"
date: 2024-12-31 03:50:27 +0800
categories: [Tool]
tags: [website, typora]     # TAG names should always be lowercase
pin: false
---

## 1.和Typora兼并的脚本

因为typora用相对路径会有'./'或者'../', 但Jekyll构建html时,图片只能在'/'下

所以我们可以在根目录下建立'assets/img',将图片存在这个地方.

例如, 从typora来看,文件存在

```python
![image-20250331014401283](../assets/img/image-20250331014401283.png)
```

但Jekyll需要图片的路径是`/assets/img/image-20250331014401283.png`, 因此,我们可以做个脚本放在`_plugins`下,命名为`remove_dotdot_assets.rb`

```python
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

```python
import os
import platform
from datetime import datetime
import subprocess

def format_title_case(text):
    lowercase_words = {
        'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'as', 'at',
        'by', 'in', 'of', 'on', 'to', 'up', 'via', 'with', 'from', 'into'
    }
    words = text.split()
    formatted = []
    for i, word in enumerate(words):
        if i > 0 and i < len(words)-1 and word.lower() in lowercase_words:
            formatted.append(word.lower())
        else:
            formatted.append(word.capitalize())
    return '-'.join(formatted)

def format_title_for_yaml(text):
    # 跟 format_title_case 一样，但是不加连字符
    lowercase_words = {
        'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'as', 'at',
        'by', 'in', 'of', 'on', 'to', 'up', 'via', 'with', 'from', 'into'
    }
    words = text.split()
    formatted = []
    for i, word in enumerate(words):
        if i > 0 and i < len(words)-1 and word.lower() in lowercase_words:
            formatted.append(word.lower())
        else:
            formatted.append(word.capitalize())
    return ' '.join(formatted)

def create_markdown_file(title):
    today = datetime.today()
    date_str = today.strftime('%Y-%m-%d')

    formatted_title = format_title_case(title)
    formatted_title_yaml = format_title_for_yaml(title)

    file_name = f"{date_str}-{formatted_title}.md"
    target_directory = r"D:\"
    os.makedirs(target_directory, exist_ok=True)

    front_matter = f"""---\ntitle: "{formatted_title_yaml}"\ndate: {today.strftime('%Y-%m-%d %H:%M:%S')} +0800\ncategories: [LLM, Tool]\ntags: [foundation, website]\npin: false\n---\n"""

    file_path = os.path.join(target_directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(front_matter + "\n")

    print(f"Markdown file created: {file_path}")

    # 自动打开文件
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", file_path])
    else:  # Linux
        subprocess.run(["xdg-open", file_path])

# 获取用户输入的标题
title_input = input("Enter the title for the markdown file: ")
create_markdown_file(title_input)

```

