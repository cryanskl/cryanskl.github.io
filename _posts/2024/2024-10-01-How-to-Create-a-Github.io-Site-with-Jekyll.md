---
title: How to Create a Github.io Site with Jekyll
date: 2024-10-01 21:29:00 +0800
categories: [Tool]
tags: [website]     # TAG names should always be lowercase
pin: false
---

## 1.安装Ruby

安装 Jekyll 我们需要使用`gem install jekyll bundler`,而gem是Ruby 的包管理工具，而 Jekyll 和 Bundler 都是 Ruby 环境中的工具。因此，首先需要确保你已经正确安装了 Ruby，并且将其添加到了系统的 PATH 环境变量中。

访问 [Ruby 官方网站](https://www.ruby-lang.org/en/downloads/) 下载安装包。

我们下载了 [Ruby+Devkit 3.3.7-1 (x64)](https://github.com/oneclick/rubyinstaller2/releases/download/RubyInstaller-3.3.7-1/rubyinstaller-devkit-3.3.7-1-x64.exe) 

![image-20250331014401283](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250331014401283.png)

在安装 Ruby 时，**MSYS2** 是必需的，它是 Ruby 在 Windows 上运行所需要的开发工具集和库。**Devkit**（开发工具包）是 MSYS2 的一部分，用于支持 Ruby 扩展和原生扩展的编译。所以，是的，你需要下载和安装 MSYS2 以及 Devkit。

![image-20250331014415695](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250331014415695.png)

地址: [https://www.aliyun.com/product/oss?spm=5176.21213303.J_v8LsmxMG6alneH-O7TCPa.8.1f002f3dZbM4cJ&scm=20140722.S_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633._.ID_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633-RL_%E5%AF%B9%E8%B1%A1%E5%AD%98%E5%82%A8-LOC_2024SPAllResult-OR_ser-PAR1_213e36e417438357211394388e93a9-V_4-RE_new3-P0_0-P1_0](https://www.aliyun.com/product/oss?spm=5176.21213303.J_v8LsmxMG6alneH-O7TCPa.8.1f002f3dZbM4cJ&scm=20140722.S_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633._.ID_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633-RL_%E5%AF%B9%E8%B1%A1%E5%AD%98%E5%82%A8-LOC_2024SPAllResult-OR_ser-PAR1_213e36e417438357211394388e93a9-V_4-RE_new3-P0_0-P1_0)

等待安装完程序会自动关闭,接下来 `ruby -v`可以看到版本号

```python
ruby 3.3.7 (2025-01-15 revision be31f993d7) [x64-mingw-ucrt]
```



## xxxxxxxxxx65 1import os2import platform3from datetime import datetime4import subprocess5​6def format_title_case(text):7    lowercase_words = {8        'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'as', 'at',9        'by', 'in', 'of', 'on', 'to', 'up', 'via', 'with', 'from', 'into'10    }11    words = text.split()12    formatted = []13    for i, word in enumerate(words):14        if i > 0 and i < len(words)-1 and word.lower() in lowercase_words:15            formatted.append(word.lower())16        else:17            formatted.append(word.capitalize())18    return '-'.join(formatted)19​20def format_title_for_yaml(text):21    # 跟 format_title_case 一样，但是不加连字符22    lowercase_words = {23        'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'as', 'at',24        'by', 'in', 'of', 'on', 'to', 'up', 'via', 'with', 'from', 'into'25    }26    words = text.split()27    formatted = []28    for i, word in enumerate(words):29        if i > 0 and i < len(words)-1 and word.lower() in lowercase_words:30            formatted.append(word.lower())31        else:32            formatted.append(word.capitalize())33    return ' '.join(formatted)34​35def create_markdown_file(title):36    today = datetime.today()37    date_str = today.strftime('%Y-%m-%d')38​39    formatted_title = format_title_case(title)40    formatted_title_yaml = format_title_for_yaml(title)41​42    file_name = f"{date_str}-{formatted_title}.md"43    target_directory = r"D:\存在你想要的路径"44    os.makedirs(target_directory, exist_ok=True)45​46    front_matter = f"""---\ntitle: "{formatted_title_yaml}"\ndate: {today.strftime('%Y-%m-%d %H:%M:%S')} +0800\ncategories: [LLM, Tool]\ntags: [foundation, website]\npin: false\n---\n"""47​48    file_path = os.path.join(target_directory, file_name)49    with open(file_path, 'w', encoding='utf-8') as file:50        file.write(front_matter + "\n")51​52    print(f"Markdown file created: {file_path}")53​54    # 自动打开文件55    if platform.system() == "Windows":56        os.startfile(file_path)57    elif platform.system() == "Darwin":  # macOS58        subprocess.run(["open", file_path])59    else:  # Linux60        subprocess.run(["xdg-open", file_path])61​62# 获取用户输入的标题63title_input = input("Enter the title for the markdown file: ")64create_markdown_file(title_input)65​python

更改镜像源 `gem sources --add https://gems.ruby-china.com/ `

`gem sources --remove https://rubygems.org/` 

```python
https://gems.ruby-china.com/ added to sources
https://rubygems.org/ removed from sources
```

安装Jekyll `gem install jekyll bundler`,使用`jekyll -v`看是否安装成功

```python
jekyll 4.4.1
```

## 3.初始化Jekyll项目

### 初始化

本地创建一个文件夹,运行`jekyll new . --force`初始化新项目

### 导入主题

随后在`Gemfile`文件中加下面的命令安装**Minimal Mistakes** 主题

```python
gem "minimal-mistakes-jekyll"
```

添加完主题,下一步安装Ruby依赖.这会安装主题以及其他必要的依赖库。

```python
bundle install --verbose
```

如果第一次没下载成功,再下一次就可能成功

### 启动服务

安装完成后，可以通过以下命令启动 Jekyll 的本地开发服务器：

```python
bundle exec jekyll serve
```

这会启动一个本地的 Jekyll 网站，通常可以在http://127.0.0.1:4000/上访问。

![image-20250331014429052](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250331014429052.png)

## 4.配置博客

- 打开 `_config.yml` 文件，进行你需要的设置，比如博客名称、描述、社交链接等。
- 根据之前的建议，在 `_config.yml` 中配置科幻风格的主题样式、字体、背景等。

## N.推荐阅读

### 官方源码

[https://github.com/cotes2020/jekyll-theme-chirpy/](https://github.com/cotes2020/jekyll-theme-chirpy/)

### 官方指南

[https://chirpy.cotes.page/posts/getting-started/](https://chirpy.cotes.page/posts/getting-started/)

### 免费主题

- [https://github.com/topics/jekyll-theme](https://github.com/topics/jekyll-theme)
- [https://jekyllthemes.org/](https://jekyllthemes.org/)
- [https://jekyllthemes.io/](https://jekyllthemes.io/)

### Mac的安装方式

[https://blog.csdn.net/v20000727/article/details/140712498](https://blog.csdn.net/v20000727/article/details/140712498)

### 推荐样式

[https://huanyushi.github.io/posts/chirpy-blog-customization/](https://huanyushi.github.io/posts/chirpy-blog-customization/)

### 常用命令

#### 定位主题位置

```python
bundle info --path jekyll-theme-chirpy
```

#### 启动服务

```python
bundle exec jekyll serve
```

#### 安装包依赖

```python
bundle install --verbose
```

