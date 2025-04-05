---
title: How to create a github.io with Jekyll
date: 2024-12-30 21:29:00 +0800
categories: [Tool]
tags: [website]     # TAG names should always be lowercase
pin: false
---

## 1.安装Ruby

安装 Jekyll 我们需要使用`gem install jekyll bundler`,而gem是Ruby 的包管理工具，而 Jekyll 和 Bundler 都是 Ruby 环境中的工具。因此，首先需要确保你已经正确安装了 Ruby，并且将其添加到了系统的 PATH 环境变量中。

访问 [Ruby 官方网站](https://rubyinstaller.org/) 下载安装包。

我们下载了 [Ruby+Devkit 3.3.7-1 (x64)](https://github.com/oneclick/rubyinstaller2/releases/download/RubyInstaller-3.3.7-1/rubyinstaller-devkit-3.3.7-1-x64.exe) 

![image-20250331014401283](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250331014401283.png)

在安装 Ruby 时，**MSYS2** 是必需的，它是 Ruby 在 Windows 上运行所需要的开发工具集和库。**Devkit**（开发工具包）是 MSYS2 的一部分，用于支持 Ruby 扩展和原生扩展的编译。所以，是的，你需要下载和安装 MSYS2 以及 Devkit。

![image-20250331014415695](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250331014415695.png)

按下回车后，安装程序将继续进行安装。可以按 **[1, 3]** 来安装 **MSYS2 基础安装** 和 **MinGW 开发工具链**，这是标准的安装配置，可以确保你能编译 Ruby 的扩展并正常使用相关功能。

等待安装完程序会自动关闭,接下来 `ruby -v`可以看到版本号

```
ruby 3.3.7 (2025-01-15 revision be31f993d7) [x64-mingw-ucrt]
```



## 2.安装Jekyll

更改镜像源 `gem sources --add https://gems.ruby-china.com/ `

`gem sources --remove https://rubygems.org/` 

```
https://gems.ruby-china.com/ added to sources
https://rubygems.org/ removed from sources
```

安装Jekyll `gem install jekyll bundler`,使用`jekyll -v`看是否安装成功

```
jekyll 4.4.1
```

## 3.初始化Jekyll项目

### 初始化

本地创建一个文件夹,运行`jekyll new . --force`初始化新项目

### 导入主题

随后在`Gemfile`文件中加下面的命令安装**Minimal Mistakes** 主题

```
gem "minimal-mistakes-jekyll"
```

添加完主题,下一步安装Ruby依赖.这会安装主题以及其他必要的依赖库。

注意,可以用VSCODE在Gemfile更改source为https://gems.ruby-china.com/

```
bundle install --verbose
```

如果第一次没下载成功,再下一次就可能成功

### 启动服务

安装完成后，可以通过以下命令启动 Jekyll 的本地开发服务器：

```
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

`bundle info --path jekyll-theme-chirpy`

#### 启动服务

`bundle exec jekyll serve`

#### 安装包依赖

`bundle install --verbose`
