---
title: "Using-AliCloud-OSS-In-Typora"
date: 2025-01-01 14:32:03 +0800
categories: [Tool]
tags: [website, typora]     # TAG names should always be lowercase
pin: false
---

## 1.Typora相对路径改为CDN

在多次测试部署文章时,有时图片加载并不成功.

虽然上次脚本能完美解决问题, 但是每次都要检索所有的文章. 当以后文章越来越多, 部署时间会增加很多. 

所以考虑换一个加载图片的方式.

## 2.使用阿里云对象存储OSS

直接跟着这篇文章就可以:https://zhuanlan.zhihu.com/p/678419508

### 2.1.访问阿里云OSS

地址: https://www.aliyun.com/product/oss?spm=5176.21213303.J_v8LsmxMG6alneH-O7TCPa.8.1f002f3dZbM4cJ&scm=20140722.S_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633._.ID_product@@%E4%BA%91%E4%BA%A7%E5%93%81@@102633-RL_%E5%AF%B9%E8%B1%A1%E5%AD%98%E5%82%A8-LOC_2024SPAllResult-OR_ser-PAR1_213e36e417438357211394388e93a9-V_4-RE_new3-P0_0-P1_0

需要注意的是, 资源要选对, 不然会贵将近十倍

![image-20250405144717509](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405144717509.png)

### 2.2.PicGo设置

后面的配置跟着来也没问题, 就是看下载的PigGo版本

我下的是2.3.1, 设置的界面会不一样, 输入的内容大同小异

![image-20250405145505128](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405145505128.png)

### 2.3.在PicGo和Typora使用

在PicGo绑定后,会自动上传test图片到OSS, 如果看到图片成功上传到Bucket列表即算成功.

接着跟着作者操作, 在Typora选择

![image-20250405150142852](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405150142852.png)

其实当复制图片进来时, 看到图片有oss标志时就已经算成功了.

![image-20250405145841040](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250405145841040.png)
