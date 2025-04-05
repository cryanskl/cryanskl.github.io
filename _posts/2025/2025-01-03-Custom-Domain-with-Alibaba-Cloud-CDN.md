---
title: "Custom Domain with Alibaba Cloud CDN"
date: 2025-01-03 18:24:37 +0800
categories: [Tool]
tags: [website]
pin: false
---

## 1.绕开限制

基于某些客观原因, 发现连通性很差. 所以用 **阿里云 CDN + GitHub Pages + 自定义域名绑定** 的方式解决

以下是找GPT生成的操作流程, 配上自己的过程图.

### ✅ 步骤 1：设置 GitHub Pages 自定义域名

1. 打开你的 GitHub 项目（例如：`yourusername.github.io`）
2. 进入 `Settings > Pages`
3. 在 **Custom domain** 栏里填上你的域名（如：`www.yourdomain.com`）
4. GitHub 会自动在仓库根目录生成一个 `CNAME` 文件，内容为你的域名
5. ⚠️ 等 GitHub 部署完成（可能需要几分钟）

![image-20250405183139538](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405183139538.png)

------

### ✅ 步骤 2：配置你的域名 DNS（通过阿里云域名控制台）

进入 阿里云域名控制台：

1. 找到你的域名，点击「解析」
2. 添加一条 `CNAME` 记录：

| 类型    | 主机记录                  | 记录值                   |
| ------- | ------------------------- | ------------------------ |
| `CNAME` | `www`（或你希望的子域名） | `yourusername.github.io` |

⚠️ 注意：`记录值` 不加 `https://`，就是纯粹的域名。

![image-20250405183943486](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405183943486.png)

![image-20250405184145641](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405184145641.png)

==这个页面先别离开! 后面CDN还会加一个TXT类型==

------

### ✅ 步骤 3：开通阿里云 CDN 并绑定域名

1. 打开 [阿里云 CDN 控制台](https://www.aliyun.com/product/cdn)
2. 点击「添加域名」
   - 加速域名填写你的域名，例如 `www.yourdomain.com`
     - ==请注意, 这里会让你在刚才DNS加一个TXT类型, 可以点击帮助文档, 写的很详细==
     - ![https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6330967271/p855492.png](https://zr-picture.oss-cn-shanghai.aliyuncs.com/p855492.png)
   - 加速类型：选择「图片小文件」
   - 源站类型：选择「域名」
   - 源站地址：填写 `yourusername.github.io`
   - 回源协议：选择「HTTPS」==没看到这个选项, 选择了端口443==
3. 添加成功后，阿里云会提示你将 `CNAME` 指向一个 CDN 域名（例如 `xxx.aliyuncdn.com`）

![image-20250405184716912](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405184716912.png)

![image-20250405185822406](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405185822406.png)

------

### ✅ 步骤 4：修改 DNS，把域名 CNAME 指向阿里云 CDN

再回到阿里云 DNS 解析控制台：

- 修改或新增一条 `CNAME` 记录：

| 类型    | 主机记录 | 记录值                                              |
| ------- | -------- | --------------------------------------------------- |
| `CNAME` | `www`    | `xxx.aliyuncdn.com` （阿里云提供的 CDN CNAME 地址） |

等待解析生效（通常几分钟）

------

### ✅ 步骤 5：开启 HTTPS（可选但推荐）

在阿里云 CDN 控制台：

1. 找到你绑定的域名，点击进入配置
2. 选择「证书管理」或「HTTPS 配置」
3. 如果你没有证书，可以选择申请免费的 **阿里云托管证书（TrustAsia DV SSL）**
4. 填写域名等信息后，自动生成并配置 HTTPS

------

## ✅ 完成！

此时你访问 `https://www.yourdomain.com`，就会通过阿里云 CDN 加速访问你的 GitHub Pages 页面，且完全**不再受 github.io 屏蔽的影响**了 🎉