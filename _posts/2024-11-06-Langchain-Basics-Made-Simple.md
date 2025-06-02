---
title: "Langchain Basics Made Simple"
date: 2024-11-06 17:29:30 +0800
categories: [LLM]
tags: [llm,rag,langchain,project]
pin: false
---

## 1. 实现效果

借助 LangChain 快速搭建本地化知识库，实现用户查询驱动的智能问答系统，支持文本溯源与多模型对接（如 OpenAI、通义千问）。

## 2. 搭建流程

1. 加载文档，并按照设定规则切分为小块文本
2. 使用嵌入模型将文本块向量化并存入向量数据库
3. 封装语义检索接口
4. 构建调用链路：`Query -> 检索 -> Prompt -> LLM -> 回复`

## 3. 安装依赖

```python
pip install pypdf2 dashscope langchain langchain-openai langchain-community faiss-cpu
```

## 4. 实现流程详解

### **1. PDF 文本提取与处理**

- 使用 `PyPDF2` 的 `PdfReader` 提取文本，并记录每行对应的页码，方便后续信息溯源。
- 使用 `RecursiveCharacterTextSplitter` 对长文本进行分割，便于向量化处理。

### **2. 构建向量数据库**

- 使用 `OpenAIEmbeddings` 或 `DashScopeEmbeddings` 将文本块转换为向量。
- 使用 `FAISS` 构建本地向量数据库，并保存每个文本块对应的页码信息，支持高效的相似度检索与溯源。

```python
import os
import logging
import pickle
from typing import List, Tuple

from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.callbacks.manager import get_openai_callback
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


def extract_text_with_page_numbers(pdf: PdfReader) -> Tuple[str, List[int]]:
    """
    提取 PDF 全文内容，并记录每行文本对应的页码。

    参数:
        pdf: 已初始化的 PdfReader 对象

    返回:
        text: 合并后的完整文本
        page_numbers: 每行文本对应的页码列表（用于溯源）
    """
    lines = []
    page_numbers = []

    for page_number, page in enumerate(pdf.pages, start=1):
        extracted_text = page.extract_text()
        if extracted_text:
            page_lines = extracted_text.splitlines()
            lines.extend(page_lines)
            page_numbers.extend([page_number] * len(page_lines))
        else:
            logging.warning(f"第 {page_number} 页未提取到文本内容。")

    return "\n".join(lines), page_numbers


def process_text_with_splitter(text: str, page_numbers: List[int], save_path: str = None) -> FAISS:
    """
    将长文本分割、向量化，并存入 FAISS 向量数据库。

    参数:
        text: 合并后的原始文本
        page_numbers: 每行文本对应的页码列表
        save_path: 可选，若指定则保存向量数据库及页码信息

    返回:
        knowledge_base: FAISS 向量检索对象，附带 page_info 属性
    """
    # 分割文本为小块
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " ", ""],
        chunk_size=512,
        chunk_overlap=128,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    print(f"文本已分割为 {len(chunks)} 个片段。")

    # 初始化嵌入模型
    embeddings = DashScopeEmbeddings(model="text-embedding-v2")

    # 构建向量数据库
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    print("向量数据库构建完成。")

    # 映射页码（防越界）
    page_info = {}
    for i, chunk in enumerate(chunks):
        line_idx = min(i, len(page_numbers) - 1)
        page_info[chunk] = page_numbers[line_idx]
    knowledge_base.page_info = page_info

    # 保存至本地
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        knowledge_base.save_local(save_path)
        with open(os.path.join(save_path, "page_info.pkl"), "wb") as f:
            pickle.dump(page_info, f)
        print(f"向量数据库及页码信息已保存至：{save_path}")

    return knowledge_base


def load_knowledge_base(load_path: str, embeddings=None) -> FAISS:
    """
    从本地加载 FAISS 向量数据库及页码映射信息。

    参数:
        load_path: 数据库存储目录
        embeddings: 可选，若为空则默认使用 DashScopeEmbeddings

    返回:
        knowledge_base: 加载后的向量数据库对象
    """
    if embeddings is None:
        embeddings = DashScopeEmbeddings(model="text-embedding-v2")

    knowledge_base = FAISS.load_local(
        load_path, embeddings, allow_dangerous_deserialization=True
    )
    print(f"成功加载向量数据库：{load_path}")

    # 加载页码信息
    page_info_path = os.path.join(load_path, "page_info.pkl")
    if os.path.exists(page_info_path):
        with open(page_info_path, "rb") as f:
            knowledge_base.page_info = pickle.load(f)
        print("页码信息加载成功。")
    else:
        print("警告：未找到 page_info.pkl，将无法显示来源页码。")

    return knowledge_base


# 示例调用：加载 PDF 并提取文本与页码
pdf_reader = PdfReader('./your_file.pdf')  # 修改为实际路径
text, page_numbers = extract_text_with_page_numbers(pdf_reader)
print(f"提取文本总长度：{len(text)} 字符")

```

更改pdf_reader位置即可

```python
# 设置向量数据库保存目录
save_dir = "./vector_db"

# 处理文本并创建知识库，同时保存至本地
print(f"开始处理文本（总长度: {len(text)} 个字符）并构建知识库...")
knowledge_base = process_text_with_splitter(text, page_numbers, save_path=save_dir)

# 可选：确认知识库加载成功
print(f"知识库构建完成，包含 {len(knowledge_base.index_to_docstore_id)} 个向量片段。")

```

### **3. 语义检索与问答链**

- 使用 `similarity_search` 对用户查询进行向量匹配，检索相关文本。
- 结合 `load_qa_chain` 与语言模型，构建问答链生成最终回答。

### **4. 成本跟踪与结果展示**

- 使用 `get_openai_callback` 跟踪调用成本，提升可控性。
- 展示回答结果与相关页码，增强可验证性。

OpenAI:

```python
query = "你想查询的问题？"
if query:
    docs = knowledgeBase.similarity_search(query)
    chatLLM = ChatOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="deepseek-v3"
    )
    chain = load_qa_chain(chatLLM, chain_type="stuff")
    input_data = {"input_documents": docs, "question": query}
    with get_openai_callback() as cost:
        response = chain.invoke(input=input_data)
        print(f"查询处理完毕，成本: {cost}")
        print(response["output_text"])
        print("来源页码：")
        unique_pages = {
            knowledgeBase.page_info.get(doc.page_content.strip(), "未知")
            for doc in docs
        }
        for page in unique_pages:
            print(f"- 第 {page} 页")

```

示例：使用通义千问 (Tongyi) 模型

```python
from langchain_community.llms import Tongyi

query = "你的问题？"
if query:
    embeddings = DashScopeEmbeddings(model="text-embedding-v2")
    loaded_knowledgeBase = load_knowledge_base("./vector_db", embeddings)
    docs = loaded_knowledgeBase.similarity_search(query)
    llm = Tongyi(model_name="deepseek-v3", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"))
    chain = load_qa_chain(llm, chain_type="stuff")
    input_data = {"input_documents": docs, "question": query}
    with get_openai_callback() as cost:
        response = chain.invoke(input=input_data)
        print(f"查询处理完毕，成本: {cost}")
        print(response["output_text"])
        print("来源页码：")
        unique_pages = {
            knowledgeBase.page_info.get(doc.page_content.strip(), "未知")
            for doc in docs
        }
        for page in unique_pages:
            print(f"- 第 {page} 页")

```



## References

阿里大模型平台百炼：[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)
