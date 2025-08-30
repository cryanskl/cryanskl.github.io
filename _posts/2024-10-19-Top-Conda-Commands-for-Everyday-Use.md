---
title: "Top Conda Commands for Everyday Use"
date: 2024-10-19 13:54:31 +0800
categories: [Lab]
tags: [script, conda]
pin: false
---

## 基础命令

### conda env list

列出有什么环境

### conda create -n testname python=3.10

创建名为 testname 的环境

### conda activate testname

激活环境

### pip list

看有什么包

### conda remove -n testname --all

删除

### conda create --name oldtest --clone newtest

克隆

## 装包导包

### pip install numpy

安装包

### pip install -r requirements.txt

### pip uninstall numpy

### pip install numpy==2.2.1

### pip freeze > requirements.txt

导文件, 提供包

### pip uninstall -r requirements.txt

## 补充

如果在pycharm里新建项目

要自定义环境选择对应的环境

这样在conda安装新的包后, 例如openai, 就可以在pycharm中直接看到对应的包
