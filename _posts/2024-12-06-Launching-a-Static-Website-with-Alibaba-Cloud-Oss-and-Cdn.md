---
title: "Launching a Static Website with Alibaba Cloud Oss and Cdn"
date: 2024-12-06 11:51:37 +0800
categories: [Lab]
tags: [website, alicloud]
pin: false
---

## 起因

发现有一个月的github action同步不成功, 定位到了具体文章, 推断是md, jekyll, github pages中间有格式冲突. 遂直接部署静态网页, 不依赖github

## ✅ 你要做的事总览（只做一次的配置 + 日常部署）

### 🧱 一次性配置（只做一次）：

1. **设置 OSS Bucket 开启静态网站托管**
2. **绑定你自己的域名到 OSS**
3. **为域名开启 CDN + HTTPS**

------

## 🚀 每次更新博客时操作：

1. 本地运行 `jekyll build` 生成 `_site/`
2. 执行 `ossutil64 cp -r ./_site/ oss://你的-bucket/` 上传到 OSS

------

## 🛠️ 全流程详细步骤（建议收藏）

### ✅ 第一步：配置 OSS Bucket 为静态网站

1. 登录 OSS 控制台 → 找到你的 Bucket
2. 左侧点击 **“基础设置 > 静态页面”**
3. 开启静态网站托管：
   - 默认主页：`index.html`
   - 错误页面：`404.html`
4. 权限设置：开启 `公共读`

------

### ✅ 第二步：上传本地构建好的站点到 OSS

#### 安装 `ossutil64` 工具（如未安装）

下载：[https://help.aliyun.com/document_detail/120075.html](https://help.aliyun.com/document_detail/120075.html)
 配置：

```
bash


CopyEdit
ossutil64 config
```

输入你的：

- `AccessKeyId`
- `AccessKeySecret`
- `Endpoint`（如 `oss-cn-hangzhou.aliyuncs.com`）

✅ 验证是否连通：

```
bash


CopyEdit
ossutil64 ls oss://你的-bucket/
```

#### 上传命令：

```
bash


CopyEdit
ossutil64 cp -r ./_site/ oss://你的-bucket-name/ --force
```

------

### ✅ 第三步：绑定你的自定义域名到 OSS

1. OSS 控制台 → 域名管理 → 添加绑定域名（如 `blog.example.com`）
2. 到你的 DNS 控制台：
   - 添加 CNAME 记录
   - 指向 OSS 提供的二级域名（如 `your-bucket.oss-cn-hangzhou.aliyuncs.com`）

⚠️ 若你后续用 CDN，则 CNAME 改为指向 CDN 加速域名。

------

### ✅ 第四步：接入 CDN + 启用 HTTPS（可选但推荐）

1. 登录阿里云 CDN 控制台
2. 添加加速域名（如 `blog.example.com`）
   - 源站类型：选择 “OSS”
   - OSS 源站：选择你刚才配置好的 Bucket
3. 配置回源规则和缓存规则（可默认）
4. 启用 HTTPS：
   - 阿里云免费证书申请
   - 开启强制 HTTPS

------

## 📦 Bonus：自动化脚本（可选）

创建一个 `.sh` 脚本：

```
bashCopyEdit#!/bin/bash
bundle exec jekyll build
ossutil64 cp -r ./_site/ oss://你的-bucket-name/ --force
echo "✅ 部署完成"
```

Windows 用户可用 `.bat` 或 PowerShell 脚本。

------

## ✅ 你的站点上线后访问流程：

你访问 `https://blog.example.com`：
 → CDN 加速 → 回源 OSS 静态资源 → 展示构建后的 HTML 页面（即 `_site/` 内容）

------

## 🧠 总结

| 项目                    | 状态     | 操作建议             |
| ----------------------- | -------- | -------------------- |
| Jekyll 本地搭建         | ✅ 已完成 | 保持本地写作         |
| OSS Bucket + CDN + 域名 | ✅ 已配置 | 配置完只需上传       |
| 自动部署                | 🔜 可添加 | 用脚本一键部署更高效 |

