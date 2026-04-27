# MOI 原子能力 API 文档

## 概述

MOI 原子能力 API 是一个用于处理文件的异步管道服务，支持对文件进行解析、分析等多种处理操作。该 API 采用异步处理模式，提交任务后会返回 job_id 用于后续查询处理结果。

### API 列表

本文档包含以下 API：

| API 名称 | 请求方法 | 端点 | 功能说明 |
|---------|---------|------|---------|
| 提交文件处理任务 | POST | `/v1/genai/pipeline` | 提交文件进行处理，支持远程 URL、本地上传或混合使用 |
| 查询任务状态 | GET | `/v1/genai/jobs/{job_id}` | 查询已提交任务的处理状态和文件列表 |
| 获取处理结果 | GET | `/byoa/api/v1/explore/volumes/any/files/{file_id}/raws` | 下载文件处理后的结果数据（ZIP 压缩包） |

---

## 提交文件处理任务

### 基本信息

- **API 地址**: `https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline`
- **请求方法**: `POST`
- **请求格式**:
  - `application/json` 用于远程文件 URL
  - `multipart/form-data` 用于本地文件上传
- **响应格式**: `application/json`

### 调用方式

该 API 支持灵活的文件处理方式：

**方式一：公网文件 URL**

- 使用 `application/json` 格式
- 通过 `file_urls` 参数传递公网文件地址
- 适用于处理已在网络上的文件

**方式二：本地文件上传**

- 使用 `multipart/form-data` 格式
- 通过文件上传方式传递本地文件
- 需要同时传递 `payload` 和 `files` 字段
- 适用于上传本地文件进行处理

**方式三：混合处理**

- **支持同时处理公网文件和本地文件**
- 使用 `multipart/form-data` 格式
- 在 `payload` 中同时指定 `file_urls`（公网文件）和 `file_names`（本地文件）
- 上传本地文件的同时指定公网文件 URL
- API 会一次性处理所有文件（公网 + 本地），返回单一 job_id

### 请求头

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Content-Type | String | 视情况 | 远程 URL 方式：`application/json`<br>本地上传方式：`multipart/form-data` |
| moi-key | String | 是 | API 密钥，用于身份验证 |

**示例：**

远程文件 URL 方式：

```
Content-Type: application/json
moi-key: YOUR-MOI-KEY
```

本地文件上传方式：

```
moi-key: YOUR-MOI-KEY
```

注：使用 `-F` 参数时，curl 会自动设置 `Content-Type: multipart/form-data`

### 请求参数

**方式一：远程文件 URL**

直接发送 JSON 格式的请求体：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file_urls | Array[String] | 是 | 待处理文件的 URL 列表，支持 HTTP/HTTPS 协议的文件地址 |
| file_names | Array[String] | 否 | 保持为空数组 `[]` |
| meta | Array | 否 | 元数据信息，可用于传递额外的处理参数或标识信息 |
| steps | Array[Object] | 是 | 处理步骤配置，定义对文件执行的操作流程 |
| steps[].node | String | 是 | 处理节点名称，如：`ParseNode` |
| steps[].parameters | Object | 是 | 节点处理参数，根据不同节点类型传入不同配置，可为空对象 |

**方式二：本地文件上传**

使用 `multipart/form-data` 格式，包含以下字段：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| payload | String | 是 | JSON 字符串，包含配置信息 |
| payload.file_names | Array[String] | 是 | 上传的文件名列表，需与实际上传的文件对应 |
| payload.meta | Array | 否 | 元数据信息 |
| payload.steps | Array[Object] | 是 | 处理步骤配置 |
| files | File | 是 | 实际上传的文件，支持多文件上传 |

**参数说明：**

- 两种方式选择其一即可
- `steps` 数组定义了文件处理的流程，**按顺序执行**
- 本地上传时，`file_names` 中的文件名应与实际上传的文件名匹配
- 节点之间有依赖关系，必须按照正确的顺序配置

### 处理节点类型

**支持的处理节点：**

| 节点名称 | 功能说明 | 输入 | 输出 |
|---------|---------|------|------|
| ParseNode | 解析节点 | 原始文件 | 结构化数据（文本、表格、图片） |
| ChunkNode | 分块节点 | ParseNode 输出 | 文本块（chunks） |
| EmbedNode | 嵌入节点 | ChunkNode 输出 | 向量嵌入（embeddings） |
| ExtractNode | 提取节点 | 原始文件或其他节点输出 | 特定信息提取 |

**节点组合方式：**

处理节点可以按以下方式组合（必须按顺序）：

**1. 仅解析**

```json
"steps": [
    {"node": "ParseNode", "parameters": {}}
]
```

用途：仅解析文件，提取文本、表格、图片

**2. 解析 + 分块**

```json
"steps": [
    {"node": "ParseNode", "parameters": {}},
    {"node": "ChunkNode", "parameters": {}}
]
```

用途：解析文件后将内容分成小块，便于后续处理

**3. 解析 + 分块 + 嵌入**

```json
"steps": [
    {"node": "ParseNode", "parameters": {}},
    {"node": "ChunkNode", "parameters": {}},
    {"node": "EmbedNode", "parameters": {}}
]
```

用途：完整的文档向量化流程，适用于语义搜索

**4. 解析 + 分块 + 嵌入 + 提取**

```json
"steps": [
    {"node": "ParseNode", "parameters": {}},
    {"node": "ChunkNode", "parameters": {}},
    {"node": "EmbedNode", "parameters": {}},
    {"node": "ExtractNode", "parameters": {}}
]
```

用途：解析后提取，包含解析、分块、向量化和信息提取

**5. 仅提取**

```json
"steps": [
    {"node": "ExtractNode", "parameters": {}}
]
```

用途：直接从文件中提取特定信息，不需要解析步骤

**节点参数说明：**

每个节点可以配置 `parameters` 参数来自定义处理行为：

```json
{
    "node": "NodeName",
    "parameters": {
        // 节点特定参数（可选）
        // 如果使用默认配置，可传空对象 {}
    }
}
```

**注意**:

- 如无特殊需求，`parameters` 可以传空对象 `{}`
- 具体参数配置请咨询 API 提供方
- 不同节点支持的参数可能不同

### 请求示例

**示例 1：使用远程文件 URL**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR-MOI-KEY" \
  -d '{
    "file_urls": [
        "http://www.pdf995.com/samples/pdf.pdf",
        "https://example.com/document.pdf"
    ],
    "file_names": [],
    "meta": [],
    "steps": [
        {
            "node": "ParseNode",
            "parameters": {}
        }
    ]
}'
```

**说明：**

- 使用 `-H "Content-Type: application/json"` 指定 JSON 格式
- 使用 `-d` 参数传递 JSON 数据
- `file_urls` 数组可以包含多个 URL
- `file_names` 设置为空数组
- API 会依次处理所有文件，返回单一的 job_id

**成功响应示例：**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "job_id": "b55093a7-ff3c-42ca-a4fe-c4e72074e046"
    },
    "request_id": "969935d0-363e-4451-a5e3-f71f1d20101e"
}
```

**示例 2：上传本地文件**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "moi-key: YOUR-MOI-KEY" \
  -F "files=@/path/to/doc1.pdf" \
  -F "files=@/path/to/doc2.pdf" \
  -F 'payload={"file_names": ["doc1.pdf", "doc2.pdf"], "steps": [{"node": "ParseNode", "parameters": {}}]}'
```

**说明：**

- 使用 `-F` 参数指定 multipart/form-data 格式（不需要 Content-Type 头）
- 多次使用 `-F "files=@文件路径"` 上传多个文件
- `files=@` 后跟文件路径，`@` 符号表示从文件读取内容
- 所有文件字段都使用相同的字段名 `files`
- `payload` 为 JSON 字符串，包含配置信息
- `file_names` 数组中的顺序应与上传的文件对应
- 注意：`files` 字段在前，`payload` 字段在后

**成功响应示例：**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "job_id": "cd072050-ce02-406b-8f28-595f2c86eaaa"
    },
    "request_id": "b6528fde-ebc3-461b-8015-1b7b97ec9c82"
}
```

**示例 3：混合使用**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "moi-key: YOUR-MOI-KEY" \
  -F "files=@2112205248_方佳俊_检测简明报告.pdf" \
  -F 'payload={"file_urls": ["http://www.pdf995.com/samples/pdf.pdf"], "file_names": ["2112205248_方佳俊_检测简明报告.pdf"], "steps": [{"node": "ParseNode", "parameters": {}}]}'
```

**说明：**

- ✅ **支持同时使用本地文件和远程 URL**
- `file_urls` 包含远程文件 URL
- `file_names` 包含上传的本地文件名
- `files` 字段上传本地文件内容
- API 会处理所有文件（本地 + 远程），返回单一 job_id

**成功响应示例：**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "job_id": "322fe48f-698d-4fbb-8851-1a2d9f8031ec"
    },
    "request_id": "ec636405-82ce-4331-902b-6810a83d17f0"
}
```

**示例 4：解析 + 分块**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{
    "file_urls": ["http://example.com/document.pdf"],
    "file_names": [],
    "steps": [
        {"node": "ParseNode", "parameters": {}},
        {"node": "ChunkNode", "parameters": {}}
    ]
  }'
```

**说明：**

- 先解析文件
- 再将解析后的内容分块
- 适用于需要对文档进行分段处理的场景

**示例 5：完整向量化流程**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{
    "file_urls": ["http://example.com/document.pdf"],
    "file_names": [],
    "steps": [
        {"node": "ParseNode", "parameters": {}},
        {"node": "ChunkNode", "parameters": {}},
        {"node": "EmbedNode", "parameters": {}}
    ]
  }'
```

**说明：**

- 解析 → 分块 → 向量嵌入
- 适用于构建语义搜索索引、RAG 系统等
- 生成的向量可用于相似度搜索

**示例 6：完整流程**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{
    "file_urls": ["http://example.com/document.pdf"],
    "file_names": [],
    "steps": [
        {"node": "ParseNode", "parameters": {}},
        {"node": "ChunkNode", "parameters": {}},
        {"node": "EmbedNode", "parameters": {}},
        {"node": "ExtractNode", "parameters": {}}
    ]
  }'
```

**说明：**

- 解析 → 分块 → 向量嵌入 → 信息提取
- 完整的文档处理流程
- 适用于需要全面分析文档的场景

**示例 7：仅信息提取**

```bash
curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{
    "file_urls": ["http://example.com/document.pdf"],
    "file_names": [],
    "steps": [
        {"node": "ExtractNode", "parameters": {}}
    ]
  }'
```

**说明：**

- 直接提取文件中的特定信息
- 无需经过解析步骤
- 适用于快速提取结构化数据

### 响应参数

**成功响应：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | String | 状态码，成功时为 `OK` |
| msg | String | 响应消息，成功时为 `OK` |
| data | Object | 响应数据对象 |
| data.job_id | String | 任务 ID，用于查询任务处理状态和结果 |
| request_id | String | 请求唯一标识，可用于问题追踪 |

**成功响应示例：**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "job_id": "c66f4354-6833-4c75-8d34-d630024e5254"
    },
    "request_id": "d16e0fc2-50dd-4928-9eac-d55f88e0160c"
}
```

**错误响应：**

```json
{
    "code": "ERROR_CODE",
    "msg": "错误描述信息",
    "data": null,
    "request_id": "请求 ID"
}
```

---

## 查询任务状态

### 基本信息

- **API 地址**: `https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/jobs/{job_id}`
- **请求方法**: `GET`
- **请求格式**: URL 路径参数
- **响应格式**: `application/json`

### 请求头

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| moi-key | String | 是 | API 密钥，用于身份验证 |

### 路径参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| job_id | String | 是 | 提交任务时返回的任务 ID |

### 响应参数

**成功响应：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | String | 状态码，成功时为 `OK` |
| msg | String | 响应消息，成功时为 `OK` |
| data | Object | 响应数据对象 |
| data.status | String | 任务整体状态：`pending`、`processing`、`completed`、`failed` |
| data.files | Array[Object] | 文件列表，包含每个文件的处理详情 |
| data.files[].file_id | String | 文件唯一标识 ID |
| data.files[].file_name | String | 文件名称 |
| data.files[].file_type | Integer | 文件类型编号 |
| data.files[].file_status | String | 文件处理状态：`pending`、`processing`、`completed`、`failed` |
| data.files[].error_message | String | 错误信息，成功时为空字符串 |
| data.files[].start_time | String | 文件处理开始时间 |
| data.files[].end_time | String | 文件处理结束时间 |
| request_id | String | 请求唯一标识 |

### 请求示例

**示例：查询任务状态**

```bash
curl -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/jobs/322fe48f-698d-4fbb-8851-1a2d9f8031ec" \
  -H "moi-key: YOUR-MOI-KEY"
```

**说明：**

- 使用 GET 方法
- job_id 作为 URL 路径的一部分
- 只需要 `moi-key` 认证头

### 响应示例

**示例 1：任务已完成**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "status": "completed",
        "files": [
            {
                "file_id": "019ad8c4-cf7e-75ca-afa1-5bd971ff9ed9",
                "file_name": "2112205248_方佳俊_检测简明报告.pdf",
                "file_type": 2,
                "file_status": "completed",
                "error_message": "",
                "start_time": "2025-12-01T07:16:11.000000+0000",
                "end_time": "2025-12-01T07:16:38.000000+0000"
            }
        ]
    },
    "request_id": "2934576f-246e-46cf-93d1-79a95fd52251"
}
```

**示例 2：多文件任务已完成**

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "status": "completed",
        "files": [
            {
                "file_id": "019ad8cb-3861-795c-99a6-03bdc37215ee",
                "file_name": "2112205248_方佳俊_检测简明报告.pdf",
                "file_type": 2,
                "file_status": "completed",
                "error_message": "",
                "start_time": "2025-12-01T07:23:38.000000+0000",
                "end_time": "2025-12-01T07:24:40.000000+0000"
            },
            {
                "file_id": "019ad8cb-3861-7963-8fa5-e2e6b66a265c",
                "file_name": "pdf.pdf",
                "file_type": 2,
                "file_status": "completed",
                "error_message": "",
                "start_time": "2025-12-01T07:23:39.000000+0000",
                "end_time": "2025-12-01T07:25:38.000000+0000"
            }
        ]
    },
    "request_id": "74983c96-98db-4e13-9d51-aee91dfcd163"
}
```

**说明：**

- 混合上传的任务包含两个文件：本地上传的文件和远程 URL 文件
- 每个文件都有独立的 `file_id`、处理状态和时间信息
- 本例中两个文件都已成功完成处理

### 任务状态说明

**整体任务状态：**

| 状态 | 说明 |
|------|------|
| pending | 任务已提交，等待处理 |
| processing | 任务正在处理中 |
| completed | 所有文件处理完成 |
| failed | 任务处理失败 |

**单个文件状态：**

| 状态 | 说明 |
|------|------|
| pending | 文件等待处理 |
| processing | 文件处理中 |
| completed | 文件处理成功 |
| failed | 文件处理失败，查看 `error_message` 了解原因 |

### 注意事项

1. **轮询间隔**：建议每 3-5 秒查询一次任务状态，避免频繁请求
2. **处理时间**：
   - 小文件（<1MB）通常需要几秒到几十秒
   - 大文件可能需要数分钟
   - 具体时间取决于文件大小和复杂度
3. **错误处理**：如果 `file_status` 为 `failed`，查看 `error_message` 字段了解失败原因
4. **时间格式**：所有时间均为 UTC 时间，格式为 `YYYY-MM-DDTHH:MM:SS.ffffff+0000`
5. **文件顺序**：`files` 数组中的顺序与提交时的顺序一致

### 使用流程示例

```bash
# 步骤1: 提交任务
JOB_ID=$(curl -X POST "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/pipeline" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -d '{"file_urls": ["http://example.com/file.pdf"], "file_names": [], "steps": [{"node": "ParseNode", "parameters": {}}]}' \
  | jq -r '.data.job_id')

echo "Job ID: $JOB_ID"

# 步骤2: 等待几秒
sleep 5

# 步骤3: 查询任务状态
curl -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/v1/genai/jobs/$JOB_ID" \
  -H "moi-key: YOUR_API_KEY" \
  | jq '.'

# 步骤4: 根据 status 决定是否继续轮询
# 如果 status 为 "completed"，任务完成
# 如果 status 为 "processing"，继续等待并查询
```

---

## 获取处理结果

### 基本信息

- **API 地址**: `https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/any/files/{file_id}/raws`
- **请求方法**: `GET`
- **请求格式**: URL 路径参数
- **响应格式**: `application/zip`

### 请求头

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Content-Type | String | 建议 | `application/json` |
| moi-key | String | 是 | API 密钥，用于身份验证 |

### 路径参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file_id | String | 是 | 文件 ID，从查询任务状态 API 返回的 `data.files[].file_id` 获取 |

### 响应说明

**成功响应：**

返回一个 **ZIP 压缩包**，包含文件处理后的所有结果数据。

**ZIP 包内容结构：**

```
{file_name}-{file_id}/
├── {file_name}_parse.json         # 解析结果的JSON数据
├── {file_name}.md                 # 提取的Markdown格式文本
├── tables/                        # 提取的表格（HTML格式）
│   ├── {table_id_1}.html
│   ├── {table_id_2}.html
│   └── ...
└── images/                        # 提取的图片
    ├── {image_hash_1}.jpg
    ├── {image_hash_2}.jpg
    └── ...
```

**文件说明：**

| 文件/目录 | 说明 |
|----------|------|
| `{file_name}_parse.json` | 结构化的解析结果，包含文档的完整解析数据 |
| `{file_name}.md` | 提取的文本内容，Markdown 格式，便于阅读 |
| `tables/*.html` | 文档中的表格，每个表格一个 HTML 文件 |
| `images/*.jpg` | 文档中的图片，以内容哈希命名 |

### 请求示例

**示例 1：下载处理结果**

```bash
curl -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/any/files/019ad8c4-cf7e-75ca-afa1-5bd971ff9ed9/raws" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR-MOI-KEY" \
  -o result.zip
```

**说明：**

- 使用 `-o result.zip` 将响应保存为 ZIP 文件
- `file_id` 来自查询任务状态 API 的响应
- 下载完成后可以解压查看结果

**示例 2：下载并解压**

```bash
# 1. 下载结果
curl -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/any/files/019ad8c4-cf7e-75ca-afa1-5bd971ff9ed9/raws" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -o result.zip

# 2. 解压文件
unzip result.zip

# 3. 查看解压内容
ls -R
```

**示例 3：查看 ZIP 包内容**

```bash
curl -s -X GET "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/any/files/019ad8c4-cf7e-75ca-afa1-5bd971ff9ed9/raws" \
  -H "Content-Type: application/json" \
  -H "moi-key: YOUR_API_KEY" \
  -o result.zip && unzip -l result.zip
```

### 响应示例

**ZIP 包内容列表示例：**

```
Archive:  result.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     4463  12-01-2025 07:37   2112205248_方佳俊_检测简明报告.pdf-019ad8cb-.../2112205248_方佳俊_检测简明报告.pdf_parse.json
      940  12-01-2025 07:37   2112205248_方佳俊_检测简明报告.pdf-019ad8cb-.../tables/60d46443-0cec-4556-bf7d-bbff5812f9f5.html
      784  12-01-2025 07:37   2112205248_方佳俊_检测简明报告.pdf-019ad8cb-.../tables/3fef6f19-af8c-4791-b18f-a2747af88fa0.html
     3222  12-01-2025 07:37   2112205248_方佳俊_检测简明报告.pdf-019ad8cb-.../2112205248_方佳俊_检测简明报告.pdf.md
    33287  12-01-2025 07:37   2112205248_方佳俊_检测简明报告.pdf-019ad8cb-.../images/21ec307c62a48eecbc5f24cedd92eee95706024ab5f041cd17a463e78c377b2f.jpg
    38704  12-01-2025 07:37   2112205248_方佳俊_检测简明报告.pdf-019ad8cb-.../images/d0be52c9d88f4fe0f7a092863de5679e624a4529552fb863f0d1cdd5ff4fd7cc.jpg
    44015  12-01-2025 07:37   2112205248_方佳俊_检测简明报告.pdf-019ad8cb-.../images/de217bbf2728e9979cf88d0fc7a81ae5adb5695a329a9ad1863eb079dfd22c22.jpg
---------                     -------
   125415                     7 files
```

**解压后的文件结构示例：**

```
2112205248_方佳俊_检测简明报告.pdf-019ad8cb-3861-795c-99a6-03bdc37215ee/
├── 2112205248_方佳俊_检测简明报告.pdf_parse.json  (4.4 KB)
├── 2112205248_方佳俊_检测简明报告.pdf.md          (3.2 KB)
├── tables/
│   ├── 60d46443-0cec-4556-bf7d-bbff5812f9f5.html  (940 B)
│   └── 3fef6f19-af8c-4791-b18f-a2747af88fa0.html  (784 B)
└── images/
    ├── 21ec307c62a48eecbc5f24cedd92eee95706024ab5f041cd17a463e78c377b2f.jpg  (33 KB)
    ├── d0be52c9d88f4fe0f7a092863de5679e624a4529552fb863f0d1cdd5ff4fd7cc.jpg  (38 KB)
    └── de217bbf2728e9979cf88d0fc7a81ae5adb5695a329a9ad1863eb079dfd22c22.jpg  (44 KB)
```

### 注意事项

1. **file_id 来源**: 必须先调用查询任务状态 API 获取 `file_id`
2. **任务状态**: 建议在任务状态为 `completed` 后再获取结果
3. **文件大小**: ZIP 包大小取决于原文件内容，可能包含大量图片
4. **内容完整性**: ZIP 包包含 ParseNode 处理的所有输出结果
5. **文件命名**: 图片使用内容哈希命名，确保唯一性
6. **保存位置**: 使用 `-o` 参数指定保存的文件名和路径
7. **多文件任务**: 如果一个任务包含多个文件，需要分别用各自的 `file_id` 获取结果
