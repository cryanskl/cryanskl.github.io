---
title: "Using Alibaba Cloud OSS in Typora"
date: 2024-10-04 14:32:03 +0800
categories: [Dev]
tags: [website,typora, alicloud]     # TAG names should always be lowercase
pin: false
---

## 1.Typora相对路径改为CDN

在多次测试部署文章时,有时图片加载并不成功.

虽然上次脚本能完美解决问题, 但是每次都要检索所有的文章. 当以后文章越来越多, 部署时间会增加很多. 

所以考虑换一个加载图片的方式.

## 2.使用阿里云对象存储OSS

直接跟着这篇文章就可以:[https://zhuanlan.zhihu.com/p/678419508](https://zhuanlan.zhihu.com/p/678419508)

### 2.1.访问阿里云OSS

地址: [https://www.aliyun.com/product/oss?spm=5176.21213303.J_v8LsmxMG6alneH-O7TCPa.8.1f002f3dZbM4cJ&scm=20140722.S_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633._.ID_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633-RL_%E5%AF%B9%E8%B1%A1%E5%AD%98%E5%82%A8-LOC_2024SPAllResult-OR_ser-PAR1_213e36e417438357211394388e93a9-V_4-RE_new3-P0_0-P1_0](https://www.aliyun.com/product/oss?spm=5176.21213303.J_v8LsmxMG6alneH-O7TCPa.8.1f002f3dZbM4cJ&scm=20140722.S_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633._.ID_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633-RL_%E5%AF%B9%E8%B1%A1%E5%AD%98%E5%82%A8-LOC_2024SPAllResult-OR_ser-PAR1_213e36e417438357211394388e93a9-V_4-RE_new3-P0_0-P1_0)

需要注意的是, 资源要选对, 不然会贵将近十倍

### 2.2.PicGo设置

### 2.3.在PicGo和Typora使用

xxxxxxxxxx65 1import os2import platform3from datetime import datetime4import subprocess5​6def format_title_case(text):7    lowercase_words = {8        'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'as', 'at',9        'by', 'in', 'of', 'on', 'to', 'up', 'via', 'with', 'from', 'into'10    }11    words = text.split()12    formatted = []13    for i, word in enumerate(words):14        if i > 0 and i < len(words)-1 and word.lower() in lowercase_words:15            formatted.append(word.lower())16        else:17            formatted.append(word.capitalize())18    return '-'.join(formatted)19​20def format_title_for_yaml(text):21    # 跟 format_title_case 一样，但是不加连字符22    lowercase_words = {23        'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'as', 'at',24        'by', 'in', 'of', 'on', 'to', 'up', 'via', 'with', 'from', 'into'25    }26    words = text.split()27    formatted = []28    for i, word in enumerate(words):29        if i > 0 and i < len(words)-1 and word.lower() in lowercase_words:30            formatted.append(word.lower())31        else:32            formatted.append(word.capitalize())33    return ' '.join(formatted)34​35def create_markdown_file(title):36    today = datetime.today()37    date_str = today.strftime('%Y-%m-%d')38​39    formatted_title = format_title_case(title)40    formatted_title_yaml = format_title_for_yaml(title)41​42    file_name = f"{date_str}-{formatted_title}.md"43    target_directory = r"D:\存在你想要的路径"44    os.makedirs(target_directory, exist_ok=True)45​46    front_matter = f"""---\ntitle: "{formatted_title_yaml}"\ndate: {today.strftime('%Y-%m-%d %H:%M:%S')} +0800\ncategories: [LLM, Tool]\ntags: [foundation, website]\npin: false\n---\n"""47​48    file_path = os.path.join(target_directory, file_name)49    with open(file_path, 'w', encoding='utf-8') as file:50        file.write(front_matter + "\n")51​52    print(f"Markdown file created: {file_path}")53​54    # 自动打开文件55    if platform.system() == "Windows":56        os.startfile(file_path)57    elif platform.system() == "Darwin":  # macOS58        subprocess.run(["open", file_path])59    else:  # Linux60        subprocess.run(["xdg-open", file_path])61​62# 获取用户输入的标题63title_input = input("Enter the title for the markdown file: ")64create_markdown_file(title_input)65​python

其实当复制图片进来时, 看到图片有oss标志时就已经算成功了.

## Reference

[https://zhuanlan.zhihu.com/p/678419508](https://zhuanlan.zhihu.com/p/678419508)

