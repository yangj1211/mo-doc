利用 MatrixOne 自带的向量化能力，我们推出了 AI 智能文档问答小助手 **MOne**。用户在云平台通过以文字的方式对小助手提问，可快速获取用户想了解的关于 MatrixOne 的信息，免去搜查资料的过程，这为用户提供了更加智能化、个性化的服务，使用户的体验感得到极大的提升。

## 实现

AI 框架我们采用的是 LangChain，Embedding 使用了 OpenAI Embedding 模型，OpenAI LLM 大模型使用的是 GPT-3.5-Turbo。MatrixOne Intelligence 调用 OpenAI embedding 接口为每段文本生成向量表示，基于 MatrixOne 的向量化能力完成向量存储和相似度搜索，收集相似度最高的文本，调用 GPT 3.5 模型提炼优化文本，最终得到最为贴近的答案。

实现的过程包括两部分：  

- 加载文件 -> 读取文本 -> 文本分割 -> 文本向量化 -> 存储向量在 Matrixone 中  
- 用户提问 -> 问题向量化 -> 在文本向量中匹配出与问题向量相似度最高的 -> 匹配出的文本作为上下文和问题一起添加到 prompt 中 -> 提交给 LLM 生成回答

整体流程如下图所示：

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/overview/mone-1.png width=70% heigth=70%/>
</div>

## 如何使用 MOne

登录实例管理平台或数据库管理平台之后，您可在右下角点击 MOne 图标唤醒它。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/overview/mone-2.png)

进入提问页面后，您可以点击具体某个推荐问题直接进入应用对话交互，也可提问其它您想了解的与 MatrixOne 有关的问题。我们还提供了答案一键复制的功能，当您获取到您想要的信息，只需点击答案右下角的复制图标即可进行一键复制。如果您对 MOne 助手提供的答案感到满意，也可以给我们点一个赞哦。
:::{note}
MOne 助手是基于 LLM 模型开发的，由于 LLM 模型可能存在的一些缺陷，在某些场景下，MOne 助手可能会出现回答不佳的情况。此外，MOne 助手只能回答与 MatrixOne 相关的产品问题，且问题字数不能超过 200。
:::