---
title: "Getting Started with Chroma"
date: 2024-11-02 19:42:01 +0800
categories: [LLM]
tags: [llm, chroma, rag]
pin: false
---

## Chroma

### 安装

```python
pip install chromadb
```

### 使用

有内存模式和持久化模式,

内存模式重启会没

```python
import chromadb

client = chromadb.Client()
```

持久化模式

```python
# 数据保存至本地目录
client = chromadb.PersistentClient(path="xxx")
```
