# 快速上手 GenAI 工作区

在本篇文档中，我们将指导您快速创建和使用 GenAI 工作区。

## 第一步：创建 MatrixOne Intelligence 账户

### 1. 注册 MatrixOne Intelligence

- 访问 [MatrixOne Intelligence 注册页面](https://matrixorigin.cn/moi-signup)。
- 填写您的注册信息，并点击**注册**。

**注意：**注册时填写的邮箱将自动注册成为您的 MatrixOne Intelligence 账户。

### 2. 激活 MatrixOne Intelligence 账户

当您点击注册后，我们会发送一封激活邮件到您提供的邮箱地址。请按照邮件中的链接完成激活。

### 3. 登录 MatrixOne Intelligence 账户

激活成功后，系统会跳转至登录界面。首次输入账号密码后，将进入 GenAI 工作区及 MatrixOne 实例选择页面，在此选择 GenAI 工作区后直接进入工作区管理平台。后续登录时，系统会自动记住上一次的选择，如需更换，可直接在 GenAI 工作区管理界面切换 MatrixOne 实例。

## 第二步：进入工作区

首次登录时，系统会自动为您创建一个以账户名称命名的工作区，无需额外设置密码。后续您也可以根据需求新建工作区，详情可参考[工作区管理](../Workspace-Mgmt/workspace.md)

### 1. 数据载入

- 在菜单栏的**数据连接**中点击并进入**数据载入**页面。
- 在数据载入页面右上角点击**载入数据**。
- 在数据载入页面选择**本地上传**，并输入以下配置信息：
    - 载入位置：下拉处创建测试卷
    - 上传 PDF 文件
    - 选择需要载入的文件
- 查看数据载入列表，等待状态变成**完成**

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/workspace_1.png)

如需了解如何创建连接器，从 OSS、S3 等数据源载入数据，请参见[连接器](../Data-Connect/connector.md)

### 2. 创建工作流

平台内置了多种工作流模版，并提供样例数据，帮助您快速构建工作流：

1. 在菜单栏选择**数据处理**，进入**工作流模版**页面。  
2. 点击**图文混合文档 RAG 数据准备**卡片上的**使用模版**按钮，进入创建工作流界面。  
3. 在创建工作流界面，找到**目标位置**，下拉新建用于存储结果的数据卷。  
4. 点击右下角**创建并开始运行**，完成工作流的创建。  
5. 返回工作流列表，等待状态变为**完成**。  

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/workspace_2.png)

### 3. 查看文件解析结果

- 在菜单栏的**数据管理**处中点击并进入**数据中心**页面
- 在处理数据卷中找到上一步创建的目标位置的数据卷
- 点击右侧的预览按钮查看文件解析结果
  
<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/workspace_3.png width=100% heigth=100%/>
</div>

### 4. 下载解析数据

点击右侧下载按钮，即可获得一个包含文字解析信息和图片资源的文件夹，文件夹内包括：

- JSON 文件：记录完整的文字解析内容，包括文件基础信息、分段类型、分段所在页码以及对应图片的原始元数据。
- 图片文件夹：存放文档中解析生成的图片资源，便于后续查看与使用。
- 表格文件夹：存放文档中解析生成的表格资源，便于后续查看与使用。
- full.md 文件：完整 Markdown 内容文件。

恭喜您成功创建 GenAI 工作区并完成文件处理全流程！有关 GenAI 工作区的更多操作详情，可参阅 [GenAI 工作区](../Workspace-Mgmt/overview.md)相关章节。

如需更多支持，请查阅我们的文档或联系支持团队。
