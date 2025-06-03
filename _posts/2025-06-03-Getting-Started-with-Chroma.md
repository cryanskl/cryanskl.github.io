---
title: "Getting Started with Chroma"
date: 2025-06-03 10:39:34 +0800
categories: [LLM, Tool]
tags: [llm, website, script]
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

## 核心流程

### 集合Collection

类似关系数据库的表

### 创建集合

```python
from chromadb.utils import embedding_functions

# 默认情况下，Chroma 使用 DefaultEmbeddingFunction，它是基于 Sentence Transformers 的 MiniLM-L6-v2 模型
default_ef = embedding_functions.DefaultEmbeddingFunction()

# 使用 OpenAI 的嵌入模型，默认使用 text-embedding-ada-002 模型
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key="YOUR_API_KEY",
#     model_name="text-embedding-3-small"
# )

collection = client.create_collection(
    name = "my_collection",
    configuration = {
        # HNSW 索引算法，基于图的近似最近邻搜索算法（Approximate Nearest Neighbor，ANN）
        "hnsw": {
            "space": "cosine", # 指定余弦相似度计算
            "ef_search": 100,
            "ef_construction": 100,
            "max_neighbors": 16,
            "num_threads": 4
        },
        # 指定向量模型
        "embedding_function": default_ef
    }
)
```

### 查询

```python
collection = client.get_collection(name="my_collection")

print(collection.peek())

print(collection.count())

# print(collection.modify(name="new_name"))
```

### 删除

```python
client.delete_collection(name="my_collection")
```

### 添加数据

```python
collection.add(
    documents = ["RAG是一种检索增强生成技术", "向量数据库存储文档的嵌入表示", "在机器学习领域，智能体（Agent）通常指能够感知环境、做出决策并采取行动以实现特定目标的实体"],
    metadatas = [{"source": "RAG"}, {"source": "向量数据库"}, {"source": "Agent"}],
    ids = ["id1", "id2", "id3"]
)

```

### 查询数据

```python
results = collection.query(
    query_texts = ["RAG是什么？"],
    n_results = 4,
    # where = {"source": "RAG"}, # 按元数据过滤
    where_document = {"$contains": "检索增强生成"} # 按文档内容过滤
)

print(results)
```

### 更新数据

```python
collection.update(ids=["id1"], documents=["RAG是一种检索增强生成技术，在智能客服系统中大量使用"])
```

### 删除数据

```python
collection.delete(ids=["id3"])
```

### Client-Server Mode

Server end

```python
chroma run --path /db_path
```

Client end

```python
import chromadb

chroma_client = chromadb.HttpClient(host='localhost', port=8000)
```
