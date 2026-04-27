# 图文混合文档 RAG 数据准备

本模版帮助你快速构建适用于图文混合文档的智能解析与知识抽取流程，生成高质量的多模态知识数据，支持构建基于图文内容的 RAG（检索增强生成）应用。通过自动识别文档中的文字与图片段落，实现结构化分段与知识组织，广泛适用于图文知识库管理、文档检索与摘要生成等场景。

## 模版详情

在模版列表点击**查看详情**进入模版详情页面。在模版详情页面，可以看到处理的效果示例图和工作流拓扑结构。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/wf_template/template_RAG/template_rag_1.png)

## 使用模版

- 在模版列表选择**图文混合文档 RAG 数据准备**模版，在模版列表或详情页点击**使用模版**，即可创建数据处理任务并快速生成对应工作流。
- 系统内置示例数据，便于快速上手和测试。
- 需要自行创建目标位置
- 支持根据实际需求，自定义调整解析、分段等工作流节点配置。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/wf_template/template_RAG/template_rag_2.png)

点击**创建并开始运行**，等待工作流运行完毕。

## 查看处理结果

导航至**数据中心**，找到刚才工作流中选择的目标位置，点击文件右侧的预览按钮，查看处理结果

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/wf_template/template_RAG/template_rag_8.png)

## 导出到 dify

1. 导航至数据连接->连接器，创建 dify 连接器，具体配置操作可参考[连接器](../../Data-Connect/connector.md)；
2. 然后在**数据导出**中选择**导出至知识库 → Dify**；
3. 配置导出信息，选择刚才处理后的 json 文件，启动导出任务，系统自动同步图文分段数据至目标知识库。

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/wf_template/template_RAG/template_rag_3.png
 width=60% heigth=60%/>
</div>

等待任务状态变成**已完成**，前往 Dify 验证。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/template/template_RAG/template_rag_4.png)

## 构建 RAG 应用

1. 在设置页面配置模型供应商和 API Key
2. 选择合适的 AI 模型

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/wf_template/template_RAG/template_rag_5.png
     width=60% heigth=60%/>
    </div>

3. 在 Dify Studio 中创建新应用并关联已导入的知识库

    ![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/wf_template/template_RAG/template_rag_6.png)

4. 点击**预览**测试图文混合问答效果

    ![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/wf_template/template_RAG/template_rag_7.png)
