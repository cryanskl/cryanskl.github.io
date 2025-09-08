---
title: "Getting Started with Knowledge Graphs"
date: 2025-05-07 11:02:19 +0800
categories: [LLM]
tags: [rag, graphrag, graph]
pin: false
---

## 1. 知识图谱基础

  知识图谱（Knowledge Graph）建立在**图论**基础之上，是用于建模实体及其之间关系的一种数据结构。在图结构中，主要由两个核心要素组成：**节点（Node）\**和\**边/关系（Edge/Relationship）**。

- **节点（Node）**：表示具体的实体，例如一个人、一家公司或一个地点。它们类似于关系型数据库中的记录（Row）。
- **关系（Relationship）**：表示两个实体之间的语义关联，例如“属于”“合作”“位于”等。

  此外，为了提升查询与建模效率，节点和关系通常都具有**标签（Label）\**与\**属性（Property）**：

- 节点通过标签进行分类，例如 `Person`、`Product` 等；
- 每个节点和关系都可以包含多个以键值对形式存储的属性，例如 `name: "Alice"`、`age: 30`。

## 2. 节点

  节点是知识图谱中最基本的组成单元，常见的实体类型包括：

- `Person`（人）
- `Organization`（组织/公司）
- `Product`（产品）
- `Location`（地点）

  每个节点可以拥有多个属性，这些属性以键值对形式存储。例如，`Person` 类型的节点可能包含 `name`、`age`、`gender`、`city` 等字段。

以下是使用 Neo4j（图数据库）创建节点的示例代码：

```
with driver.session() as session:
    # 添加用户节点
    session.run("""
        CREATE (u1:User {user_id: 'U001', name: 'Alice', city: 'Beijing'}),
               (u2:User {user_id: 'U002', name: 'Bob', city: 'Shanghai'})
    """)
    
    # 添加商品节点
    session.run("""
        CREATE (p1:Product {product_id: 'P001', name: 'Laptop', price: 5999}),
               (p2:Product {product_id: 'P002', name: 'Headphones', price: 399})
    """)
    
    # 添加商家节点
    session.run("""
        CREATE (s1:Seller {seller_id: 'S001', name: 'TechStore'}),
               (s2:Seller {seller_id: 'S002', name: 'AudioMart'})
    """)
    
    # 添加分类节点
    session.run("""
        CREATE (c1:Category {name: 'Electronics'}),
               (c2:Category {name: 'Accessories'})
    """)

```

## 3. 关系

  关系用于连接两个节点，表达它们之间的语义联系。一个关系通常包含以下要素：

- **关系类型（Type）**：例如 `FRIEND`（朋友）、`WORKS_FOR`（就职于）、`LOCATED_IN`（位于）等；
- **关系方向（Direction）**：关系是有方向的，表示“从哪个节点指向哪个节点”。

  在 Neo4j 中创建关系的基本语法如下：

```
CREATE (node_name)-[:RELATION_TYPE]->(related_node_name)
```

示例说明：

```
with driver.session() as session:
    session.run("""
        MATCH (u:User {user_id: 'U001'}), (p:Product {product_id: 'P001'})
        CREATE (u)-[:PURCHASED {date: '2023-08-01'}]->(p)
    """)
    
    session.run("""
        MATCH (p:Product {product_id: 'P001'}), (s:Seller {seller_id: 'S001'})
        CREATE (p)-[:SOLD_BY]->(s)
    """)
    
    session.run("""
        MATCH (p:Product {product_id: 'P001'}), (c:Category {name: 'Electronics'})
        CREATE (p)-[:BELONGS_TO]->(c)
    """)

```

表示名为 “muyu” 的 `Person` 节点与名为 “Fufan” 的 `Company` 节点之间存在一条 `WORKS_FOR` 类型的有向关系。
