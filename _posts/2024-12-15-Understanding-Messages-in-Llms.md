---
title: "Understanding Messages in LLMs"
date: 2024-12-15 22:15:38 +0800
categories: [LLM]
tags: [llm]
pin: false
---

## 1. Messages 的种类

在与大语言模型（如 OpenAI 的 GPT 系列）交互时，消息（`messages`）通常由以下三种角色组成：

- `user`：代表用户输入的内容；
- `assistant`：代表模型生成的回复；
- `system`：用于设定助手行为的初始指令，对整个对话的语气与角色有重要影响。

这些消息以列表形式按顺序组织，用于构建上下文对话。

## 2. user 消息

用户消息用于向模型提出请求或提问。格式如下：

```
pythonCopyEdit# 创建用户消息
user_message = {
    "role": "user",
    "content": "你好，请介绍下你自己。"
}
```

## 3. assistant 消息

助手消息表示模型的回复，通常紧跟在用户消息之后，用于记录模型历史响应，以保持对话的上下文。

```
pythonCopyEdit# 创建助手消息
assistant_message = {
    "role": "assistant",
    "content": "你好！我是一个由 OpenAI 训练的大语言模型，可以帮助你解答问题、撰写内容等。"
}
```

## 4. system 消息

System 消息用于设定对话的初始行为和语境，例如要求模型扮演某种身份、使用某种语言风格等。它不会显示给用户，但对后续回复有显著影响。

除了设定助手行为，`system` 消息还常用于 Function Calling 场景中提供函数定义信息。

### 多轮对话机器人示例

下面是一个简单的多轮对话实现，演示如何通过 `messages` 列表构建上下文，并与模型持续对话：

```
pythonCopyEditdef multi_round_chat():
    """
    多轮对话机器人示例函数，演示如何持续维护消息上下文并调用语言模型生成回复。
    """
    messages = []

    # 添加系统消息，设定助手角色
    system_message = create_message("system", "You are a helpful assistant.")
    messages.append(system_message)

    while True:
        # 获取用户输入
        user_input = input("User: ")

        if user_input.lower() == 'exit':
            print("对话结束。")
            break

        # 构建用户消息
        user_message = create_message("user", user_input)
        messages.append(user_message)

        # 调用模型生成助手回复（需结合实际 API）
        assistant_reply = chat_with_DeepSeek(client, messages)
        display(Markdown(f"Assistant: {assistant_reply}"))

        # 保存助手消息
        messages.append(create_message("assistant", assistant_reply))
```

> 💡 建议将 `create_message` 和 `chat_with_DeepSeek` 函数封装好，并根据具体 LLM 提供方（如 OpenAI、DeepSeek 等）替换调用方式。
