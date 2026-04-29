# MOI 对接 DeerFlow 实现 RAG 应用开发指南

## 概述

本指南详细介绍如何将开源 RAG 应用开发引擎 DeerFlow 与 MatrixOne Intelligence (MOI) 的 RAG 服务进行集成，构建强大的深度检索增强生成应用。

## 什么是 DeerFlow？

**DeerFlow** 是字节跳动开源的 RAG 应用开发引擎，旨在简化检索增强生成应用的构建过程。它具有以下核心特性：

- **全流程支持**：提供从文档解析、文本分段、向量嵌入到检索生成的全链路 RAG 能力
- **开箱即用**：预置多种数据源解析器和分段策略，支持快速搭建 RAG 应用
- **灵活扩展**：支持自定义工具和插件，便于业务定制化开发
- **多模态支持**：不仅支持文本，还支持图片、PPT 等多种格式内容处理
- **可视化界面**：提供 Web UI，方便非技术用户使用和管理

DeerFlow 通过标准化 RAG 工作流程，让开发者能够专注于业务逻辑而非底层技术实现，大幅提升 RAG 应用的开发效率。

## 环境准备

### 系统要求

- **Python**: 3.12 或更高版本
- **Node.js**: 22 或更高版本

### DeerFlow 安装部署

详细可参考：<https://github.com/bytedance/deer-flow>

```bash
# 步骤1: 克隆代码仓库
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow

# 步骤2: 安装Python依赖
uv sync

# 步骤3: 初始化配置文件
cp .env.example .env
cp conf.yaml.example conf.yaml

# 步骤4: 安装PPT生成支持(可选)
# macOS使用Homebrew安装
brew install marp-cli

# 步骤5: 安装Web UI依赖(可选)
cd web
pnpm install
```

## MOI RAG 工作流配置

### 创建工作流

具体创建步骤可参考文章[工作流](../workspace/data/processing/workflow.md)

基础 RAG 工作流必须包含解析节点、分段节点和嵌入节点。

### 获取 API 凭证

1. 在 MOI 工作区左下角找到 API 信息
2. 复制 API 密钥 (API Key)
3. 记录 API URL，格式如：`https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn`
4. DeerFlow 接入点为：`{API_URL}`

## DeerFlow 配置对接 MOI

### 配置环境变量

编辑项目根目录下的 `.env` 文件：

```bash
# MOI is a hybrid database that mainly serves enterprise users (https://www.matrixorigin.io/matrixone-intelligence)
RAG_PROVIDER=moi
MOI_API_URL="https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn"
MOI_API_KEY="moi-key-xxxxxxxxxxxx"
MOI_RETRIEVAL_SIZE=10
MOI_LIST_LIMIT=10
```

### 配置基础语言模型

编辑 `conf.yaml` 文件配置 LLM 模型：

```yaml
BASIC_MODEL:
  # 模型服务 API 地址（支持本地部署如 Ollama）
  base_url: http://localhost:11434/v1
  # 模型名称（必须支持工具调用功能）
  model: "qwen2.5:7b"
  # API 密钥（如需要）
  api_key: xxxxxx
```

**重要提示**: 所选基础模型必须支持工具调用 (Tool Calling) 功能，这是 RAG 应用正常工作的关键。

## 启动应用

完成配置后，可以启动 DeerFlow 应用：

```bash
# 在项目根目录执行
uv run main.py
```

如果配置了 Web UI，还需要启动前端服务：

```bash
# 在项目根目录执行
# On macOS/Linux
./bootstrap.sh -d

# On Windows
bootstrap.bat -d
```

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/deerflow_1.png
 width=100% heigth=100%/>
</div>

点击 `Get Started` 进入对话页面，在对话框输入 `@` 符合来获取 MOI 上处理后的文件。目前只返回前十个，可在输入框输入文件名匹配。

:::{note}
目前会调取展示所有处理后文件，需要自行选择包含文本嵌入节点处理后的文件。
:::
<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/release4.1.0_4.png
 width=100% heigth=100%/>
</div>

通过以上步骤，您就可以成功将 DeerFlow 与 MOI RAG 服务集成，构建功能完整的检索增强生成应用。