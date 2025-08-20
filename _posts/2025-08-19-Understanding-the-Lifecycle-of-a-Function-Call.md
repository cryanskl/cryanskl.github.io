---
title: "Understanding the Lifecycle of a Function Call"
date: 2025-02-19 22:21:54 +0800
categories: [LLM]
tags: [agent]
pin: false
---

## 1. Function Calling 的生命周期

Function Calling 是 OpenAI API 中的重要机制，用于让模型在无法直接回答问题时调用外部函数来获取所需信息。其生命周期主要包含以下五个阶段：

### 1. 建立连接

在发起一次对话请求前，客户端需要：

- 指定所使用的模型（如 `gpt-4o-mini`）；
- 提供用户输入的上下文信息（`messages`）；
- 注册可供调用的函数（通过 `tools` 参数）；
- 可选：设置是否支持并行函数调用（`parallel_tool_calls`）。

### 2. 模型决策

模型会基于自身的原生知识与上下文信息，判断该问题：

- 是否可以直接生成回答；
- 是否需要调用某个工具函数来获取额外信息。

这一阶段完全由模型判断，并返回是否调用函数及其参数。

### 3. 函数调用

若模型决定调用函数，将明确返回：

- 所调用函数的名称；
- 需要传递的参数（以 JSON 格式提供）；
- 可包含多个函数调用请求（如果启用并行调用）。

### 4. 执行函数

客户端收到模型的函数调用指令后，应：

- 根据调用指令，从本地注册的函数中执行对应函数；
- 使用模型提供的参数调用；
- 将函数返回结果封装为 `tool` 类型消息，继续添加进对话上下文。

### 5. 回复用户

在函数执行完成后，再次调用模型，将用户原问题、模型中间调用信息、函数结果一并传入：

- 模型会根据完整上下文，生成最终对用户的回复；
- 最终回复可包含解释、格式化结果等内容。

------

## 2. 示例代码

以下为一个典型的 function calling 流程的 Python 实现：

```
from openai import OpenAI
import json

client = OpenAI()
messages = []

while True:
    prompt = input('\n提出一个问题： ')
    if prompt.lower() == "退出":
        break  # 退出交互

    # 添加用户提问到消息历史
    messages.append({'role': 'user', 'content': prompt})

    # 模型判断是否调用函数
    completion = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages,
        tools=tools,
        parallel_tool_calls=False  # 可选：是否启用并行调用
    )

    response = completion.choices[0].message
    tool_calls = response.tool_calls

    if tool_calls:
        # 模型请求调用函数
        function_name = tool_calls[0].function.name
        function_args = json.loads(tool_calls[0].function.arguments)

        # 执行本地函数
        function_response = available_functions[function_name](**function_args)

        # 添加模型请求调用信息
        messages.append(response)

        # 添加函数执行结果，必须带 tool_call_id
        messages.append({
            "role": "tool",
            "name": function_name,
            "content": str(function_response),
            "tool_call_id": tool_calls[0].id,
        })

        # 再次请求模型生成最终回应
        second_response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=messages,
        )

        final_response = second_response.choices[0].message.content
        messages.append({'role': 'assistant', 'content': final_response})
        print(final_response)
    else:
        # 模型无需调用函数，直接回复
        print(response.content)
        messages.append({'role': 'assistant', 'content': response.content})
```

------

## 3. 注意事项

### 1. `tool_call_id` 的必要性

```
messages.append({
    "role": "tool",
    "name": function_name,
    "content": str(function_response),
    "tool_call_id": tool_calls[0].id,
})
```

每一个函数执行结果的消息（`role: tool`）**必须对应**一次 `tool_calls` 中的调用请求，并使用相同的 `tool_call_id`。这是模型识别函数调用链的重要依据。

### 2. `parallel_tool_calls` 控制项

当一次请求可能涉及多个函数调用时：

- 若希望模型**同时发起多个调用请求**，需设置 `parallel_tool_calls=True`（默认值）；
- 若只希望模型每次只调用一个函数，应显式设置 `parallel_tool_calls=False`。

