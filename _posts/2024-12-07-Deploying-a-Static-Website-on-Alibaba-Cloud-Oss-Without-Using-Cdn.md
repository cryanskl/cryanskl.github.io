---
title: "Deploying a Static Website on Alibaba Cloud Oss Without Using Cdn"
date: 2024-12-07 14:53:58 +0800
categories: [Lab]
tags: [website, script, typora, alicloud]
pin: false
---

## 1. 起因

之前遇到一个问题：使用 GitHub Actions 自动部署博客时频繁失败。后来发现，将静态网站直接发布到阿里云 OSS（对象存储服务）是一种更简单、稳定的方式，而且能有效避免格式错乱的问题。

至于取消 CDN 的原因，主要是出于成本考虑。由于博客访问量较小，使用 CDN 每天需要支付两三元，一个月下来大约七八十元，性价比不高，因此选择直接使用 OSS 提供的公网地址访问页面。

现在的构建和部署流程非常简洁高效：

```
CopyEdit
本地使用 Typora 编辑文章 → 运行脚本发布到 OSS → 实时更新完成
```

整个流程不依赖 CDN，也没有同步延迟，体验非常丝滑。

## 2. 注意事项

部署使用的是阿里云提供的命令行工具 `ossutil`，这里有一个重要的坑需要特别注意：**发布时千万不要使用 `--delete` 参数**。我曾经因为这个参数导致之前通过 PicGo 上传的所有图片被误删。

推荐的做法是：在 Typora 中使用相对路径插入图片，并将图片统一保存在 `assets/` 目录下你自定义的子文件夹中。

例如：

```python
![示例图片](../assets/202406/post-image.png)
```

这样在部署时，脚本会将 Markdown 文件及其引用的图片一并同步到 OSS，确保线上内容完整无误。

## 3. 部署及脚本

关于如何将 Jekyll 博客部署到阿里 OSS，前文已有介绍。基本流程如下：

### 步骤一：构建 Jekyll 项目

首先确保你已经搭建并本地调试好 Jekyll 博客。如果尚未安装，可参考以下命令：

```
bashCopyEditgem install jekyll bundler
jekyll new my-blog
cd my-blog
bundle exec jekyll serve
```

确认在本地访问 `http://localhost:4000` 页面无误后，即可进入构建流程。

### 步骤二：构建静态文件

使用以下命令生成静态文件，Jekyll 会将博客内容输出到 `_site/` 目录：

```
bash


CopyEdit
bundle exec jekyll build
```

这个目录就是你最终要上传到 OSS 的文件内容，包括 HTML、CSS、JS、图片等所有静态资源。

### 步骤三：配置阿里云 OSS

1. 登录阿里云控制台，创建一个 OSS Bucket；

2. 设置访问权限为“公共读”，以便用户可以访问你的静态页面；

3. 建议开启静态网站托管功能，设置默认首页（如 `index.html`）和错误页（如 `404.html`）；

4. 下载并配置命令行工具 ossutil：

   ```
   bash
   
   
   CopyEdit
   ./ossutil64 config
   ```

你需要提供 `AccessKeyId`、`AccessKeySecret` 和目标 Bucket 的 Endpoint。

### 步骤四：编写发布脚本

推荐使用一个简单的 Bash 脚本将构建目录上传至 OSS。例如：

```
bashCopyEdit#!/bin/bash

# 构建 Jekyll 站点
bundle exec jekyll build

# 上传到 OSS（替换为你的 Bucket 名称和路径）
./ossutil64 cp -r _site/ oss://your-bucket-name/ --update
```
