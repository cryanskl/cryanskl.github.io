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

PS:其实这里我没细看, 先做后面.这里因为没有配置dns和cdn, 一定会报错

------

### ✅ 步骤 2：开通阿里云 CDN 并绑定域名

1. 打开 [阿里云 CDN 控制台](https://www.aliyun.com/product/cdn)
2. 点击「添加域名」
   - 加速域名填写你的域名，例如 `www.yourdomain.com`
     - ==请注意, 这里会让你在刚才DNS加一个TXT类型, 可以点击帮助文档, 写的很详细==
     - ![https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6330967271/p855492.png](https://zr-picture.oss-cn-shanghai.aliyuncs.com/p855492.png)
   - 加速类型：选择「图片小文件」
   - 源站类型：选择「域名」
   - 源站地址：填写 `yourusername.github.io`
   - 回源协议：端口443
3. 添加成功后，阿里云会提示你将 `CNAME` 指向一个 CDN 域名（例如 `xxx.aliyuncdn.com`）

![image-20250405184716912](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405184716912.png)

![image-20250405185822406](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405185822406.png)

------

### ✅ 步骤 3：修改 DNS，把域名 CNAME 指向阿里云 CDN

去阿里云 DNS 解析控制台：

- 修改或新增一条 `CNAME` 记录：

| 类型    | 主机记录 | 记录值                                              |
| ------- | -------- | --------------------------------------------------- |
| `CNAME` | `www`    | `xxx.aliyuncdn.com` （阿里云提供的 CDN CNAME 地址） |

等待解析生效（通常几分钟）

------

### ✅ 步骤 4：开启 HTTPS

在阿里云 CDN 控制台：

1. 找到你绑定的域名，点击进入配置
2. 选择「证书管理」或「HTTPS 配置」
3. 如果你没有证书，可以选择申请免费的 **阿里云托管证书**
4. 填写域名等信息后，自动生成并配置 HTTPS

![image-20250405203529103](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405203529103.png)

​	5.回到CDN控制台进行配置

![image-20250405203646882](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405203646882.png)

------

## ✅ 完成！

此时你访问 `https://www.yourdomain.com`，就会通过阿里云 CDN 加速访问你的 GitHub Pages 页面，且完全**不再受 github.io 屏蔽的影响**了 🎉

## 2.常见问题

### 2.1.DNS Check需要github.io作为CNAME

如果用了这个为CNAME, 就没有用到CDN, 那么这个配置照样无法顺畅访问



### 2.2.默认页面index.html

当你配置完, 直接访问首页, 发现内容是

![image-20250405204034656](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405204034656.png)

是没有渲染的md文档, 而其他文件可以正常访问.

GPT解答如下:

#### 🎯 问题本质：阿里云 CDN 回源首页时，返回的是源代码，而不是构建后的 `index.html`

也就是：

- 你访问 `https://www.wuzhixiaojiu.com/` 时
  - CDN 去回源 `cryanskl.github.io/`
  - 但可能错误地取到了仓库的 `index.md` 源文件
  - 而不是真正构建生成的 `index.html`

> 所以你看到的就变成了原始 Markdown 文件内容，而非渲染结果。

------

#### ✅ 为什么其他页面可以正常访问？

因为 GitHub Pages 生成后的页面路径是：

- `index.html` ← 首页
- `/about/` → `about/index.html`
- `/posts/foo/` → `posts/foo/index.html`

这些路径在 CDN 中不会冲突到 Markdown 文件名，而首页 `/` 很容易被 CDN 错误映射到 `index.md`（而不是 `index.html`），**尤其是在“回源 Host 头”没设置正确时**。