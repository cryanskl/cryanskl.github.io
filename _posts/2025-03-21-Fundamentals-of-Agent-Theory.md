---
title: "Fundamentals of Agent Theory"
date: 2025-03-21 22:57:43 +0800
categories: [LLM]
tags: [agent]
pin: false
---

## 1. **ReAct Agent 基本理论**

ReAct 框架由 *Reason*（推理）与 *Act*（行动）结合而成，其核心是一个 **思想—行动—观察（Thought–Action–Observation）循环**。
 在这一循环中，代理（Agent）会基于已有的观察结果进行推理（Reasoning），从而决定下一步要采取的行动（Acting）；而行动的结果又会作为新的观察（Observation）反馈到循环中，直到任务完成。这种设计使得 ReAct 既能进行逻辑推理，又能灵活调用外部工具来解决问题。

在 ReAct 中，几个关键要素如下：

- **Question**：用户提出的任务或问题。
- **Thought**：大模型的内部思考过程，用于规划如何解决问题以及决定下一步的行动。
- **Action**：执行具体操作，例如调用工具或 API。
- **Action Input**：行动的输入参数，例如查询关键词、计算公式等。
- **Observation**：执行行动后的反馈结果。
- **Answer**：最终给用户的回答，通常在若干次循环后得出。

> 举个例子：如果用户问「法国的首都是哪里？」
>
> - Thought：模型会思考“我应该查一下法国的相关信息”。
> - Action：调用 `wikipedia: France`。
> - Observation：Wikipedia 返回“法国的首都是巴黎”。
> - Answer：模型总结得出“法国的首都是巴黎”。

这种模式的优势在于，它既能利用大模型的推理能力，也能借助外部工具进行事实检索或计算，从而提高回答的可靠性和准确性。

------

## 2. **ReAct Prompt 示例**

下面给出一个简化版的 ReAct Prompt，用于指导模型按照 **Thought–Action–Observation–Answer** 的模式来运行：

```
prompt = """
You run in a loop of Thought, Action, Observation, Answer.
At the end of the loop you output an Answer.

Use Thought to describe your reasoning about the question.
Use Action to run one of the available tools.
Observation will be the result of the Action.
Answer will be your final conclusion.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a Python calculation and returns the result. 
Be careful to use floating point when necessary.

wikipedia:
e.g. wikipedia: Django
Looks up a topic on Wikipedia and returns a summary.

Always check Wikipedia if it may provide useful information.

Example session:

Question: What is the capital of France?

Thought: I should look up France on Wikipedia.
Action: wikipedia: France
Observation: [Wikipedia summary about France, including capital]
Answer: The capital of France is Paris.
"""
```

------

## 3. **实现 ReAct Agent 的三个关键步骤**

要通过代码实现一个可运行的 ReAct Agent，可以从以下三个方面着手：

1. **设计提示词（Prompt Engineering）**
    在大模型的 `system` 提示中设置完整的规则，明确规定代理的推理方式、可用工具以及响应格式。这相当于为代理写“操作手册”。
2. **动态注入用户输入**
    将用户的问题（`Question`）作为变量注入到提示词中，使模型能够根据实时需求生成 Thought、Action 和 Answer。
3. **集成工具调用**
    构建并对接外部工具（如搜索引擎、数据库、API 等），并将它们的调用格式嵌入到提示词中。这样，模型在推理过程中就能通过 Action 调用这些工具，并将结果纳入循环。

------

## References

1. [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/pdf/2210.03629)
2. [ReAct 官方项目主页](https://react-lm.github.io/)
