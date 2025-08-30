---
title: "Automated Script for Static Website Submission"
date: 2024-12-04 16:57:35 +0800
categories: [Lab]
tags: [website, script]
pin: false
---

## deploy.bat

写了一个deploy.bat, 本地构建好Jekyll后增量上传到阿里OSS, 并且刷新阿里云缓存

### 🧩 所需工具与环境配置

在开始之前，请先安装并配置以下工具：

| 工具                          | 作用                                   | 安装地址或命令                                   |
| ----------------------------- | -------------------------------------- | ------------------------------------------------ |
| Ruby + Jekyll                 | 用于构建博客                           | Jekyll 安装教程                                  |
| Bundler                       | Ruby 依赖管理器                        | `gem install bundler`                            |
| 阿里云 OSS 工具（ossutil）    | 上传文件到阿里云对象存储               | 官方文档                                         |
| 阿里云 CLI 工具（aliyun-cli） | 调用 CDN 接口                          | 官方文档                                         |
| Python（可选）                | 用于处理文件名与 Front Matter 日期对齐 | [Python 官网](https://www.python.org/downloads/) |

安装完成后：

- 配置 ossutil（运行一次 `ossutil64 config`）
- 配置 aliyun CLI（运行一次 `aliyun configure`）

------

### 📝 脚本结构说明

#### ✅ 1. Python 预处理部分（fix_post_filename.py）

作用：确保 `_posts/` 中的 Markdown 文件名日期与 Front Matter 中一致，防止 Jekyll 报错或文章无法渲染。

关键逻辑：

```
pythonCopyEdit# 读取文件名和第三行 frontmatter 中的日期是否一致
# 若不一致，则自动重命名文件
```

#### ✅ 2. Jekyll 构建

```
bat


CopyEdit
call bundle exec jekyll build
```

在当前目录下构建生成 `_site/` 文件夹，即网站静态内容。

#### ✅ 3. 增量上传至 OSS

```
bat


CopyEdit
ossutil64 sync D:\GitBlog\_site oss://osspath -u --delete
```

- `-u`：仅上传变更过的文件（**增量上传**）
- `--delete`：自动删除 OSS 上已被本地删除的文件

#### ✅ 4. 刷新 CDN 缓存

```
bat


CopyEdit
aliyun cdn RefreshObjectCaches --ObjectPath "https://yourosspath.aliyuncs.com/*" --ObjectType File
```

防止用户访问的是缓存页面，而不是刚刚上传的新版本。

------

### 🎯 使用方法

1. 将 `.bat` 脚本文件放到桌面
2. 将 `fix_post_filename.py` 放入博客根目录（如 `D:\GitBlog`）
3. 双击 `.bat` 脚本，即可完成全流程部署

建议文件结构：

```
makefileCopyEditD:\GitBlog\
│
├── _posts\
├── _site\
├── fix_post_filename.py
└── blog_sync.bat
```

------

### 💡 常见问题

#### 📌 为什么上传时有很多文件变化？

请确认 Jekyll 没有生成 `.DS_Store`、`.sass-cache`、或 `.jekyll-cache` 等文件。如果这些文件在 `_site` 目录中存在，可以在 `.gitignore` 和 Jekyll 配置中排除它们。

#### 📌 aliyun 命令无法识别？

请确保 `aliyun.exe` 所在目录已添加到系统环境变量 `Path`。你也可以在 `.bat` 中写死路径，如：

```
bat


CopyEdit
"D:\Tools\aliyun-clipath" ...
```

------

### 🧭 拓展建议

- 添加 **自动备份**，如 zip 打包 `_posts` 和 `_config.yml`
- 使用 GitHub Actions 或 Azure DevOps 做远程自动部署
- 加入 `jekyll serve` 自动预览功能

------

### ✅ 总结

通过这个脚本，我们实现了从 Markdown 编写到网页上线的「一键式部署」。对博主而言，这意味着更高效的内容迭代、更少的操作出错，以及更快的发布速度。

## 补充

完整脚本如下

```bat
@echo off
chcp 65001 > nul
title 🚀 自动部署 Jekyll 博客至 OSS
echo ===============================
echo 🛠️ 正在构建 Jekyll 网站...
echo ===============================
cd /d %~dp0

call bundle exec jekyll build

echo.
echo ===============================
echo ☁️ 正在增量上传至阿里云 OSS...
echo ===============================

ossutil64 sync "%~dp0_site" oss://youross -u --delete

echo.
echo ===============================
echo ⚡ 正在刷新阿里云 CDN 缓存...
echo ===============================

aliyun cdn RefreshObjectCaches --ObjectPath "https://youross*" --ObjectType File

echo.
echo ✅ 所有任务已完成！
pause

```

