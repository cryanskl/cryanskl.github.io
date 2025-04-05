---
title: "Getting Started with Hugging Face"
date: 2025-01-05 22:17:42 +0800
categories: [LLM]
tags: [hugggingface, llm]
pin: false
---

## 1.本地在线调用Hugging Face API

官网: https://huggingface.co/

登录后点击头像, 获取列表的 Access Tokens. 建议权限都打开

![image-20250406020136586](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250406020136586.png)

随后可以尝试在本地简单调用

```python
import requests

API_URL = 'https://api-inference.huggingface.co/models/uer/gpt2-chinese-cluecorpussmall'
API_TOKEN = '刚才的token'
headers= {'Authorization': f'Bearer {API_TOKEN}'}
#
response = requests.post(API_URL, headers=headers,json={'inputs':'hello, hugging face'})
print(response.json())
```

可能会有网络波动, 回复的不快或失败.

![image-20250406020702349](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250406020702349.png)

## 2.本地下载模型, 分词器

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = 'uer/gpt2-chinese-cluecorpussmall'
cache_dir = 'model/uer/gpt2-chinese-cluecorpussmall'

AutoModelForCausalLM.from_pretrained(model_name,cache_dir=cache_dir)

AutoTokenizer.from_pretrained(model_name,cache_dir=cache_dir)

print(f'All have downloaded to {cache_dir}')
```

我们可以看到, 模型存在safetensors,也可能.pt. 这里config是设置, tokenizer_config是大概多少长度, vocab是字典大小

![image-20250406032525118](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250406032525118.png)

## 3.调用本地模型生成器

```python
from transformers import AutoModelForCausalLM,AutoTokenizer,pipeline

# 绝对路径
model_dir = r"C:\绝对路径"

model = AutoModelForCausalLM.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

generator = pipeline('text-generation', model=model,tokenizer=tokenizer,device='cpu')

output = generator('hello, i am a', max_length=50,num_return_sequences=1)

print(output)
```

要注意这个绝对路径是包含config.json的地方, 例如

![image-20250406032541065](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250406032541065.png)

结果如下:

![image-20250406021414658](https://zr-picture.oss-cn-shanghai.aliyuncs.com/image-20250406021414658.png)

## 4.数据获取

地址: https://huggingface.co/datasets

一般如果没写缓存, 会默认存在.cache/huggingface/datasets

例如:

```python
from datasets import load_dataset

#在线加载数据
dataset = load_dataset(path='lansinuote/ChnSentiCorp')
print(dataset)

#扩展转为CSV格式
dataset.tocsv(path_or_buf=r'绝对路径.CSV') #Linux不加csv，windows加.csv
```

下载完后能看到huggging face专有的.arrow数据集

```python
from datasets import load_dataset,load_from_disk

#在线加载数据
#dataset = load_dataset(path='lansinuote/ChnSentiCorp')
#print(dataset)

#加载缓存数据
dataseats = load_from_disk(r'绝对路径')
print(datasets) # train, validation, test 训练，验证，测试

train_data = datasets['train']
for data in train_data:
    print(data)
```
