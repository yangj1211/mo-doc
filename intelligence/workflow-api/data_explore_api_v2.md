# 数据中心 API

本文档介绍 MatrixOne Intelligence 数据中心的资源结构与 API。数据中心由“目录 → 库 → 卷 → 文件”构成，并通过“卷引用”建立跨资源的关联关系。

- 目录：用于组织业务域与资源边界
- 库：承载表与数据对象的逻辑库
- 卷：面向文件与处理结果的资源容器
- 文件：卷内的具体文件条目
- 卷引用：跨卷/跨资源的引用绑定

- 基础地址：`https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn`
- 公共请求头：
  - `moi-key`：string，API Key
- 返回结构：除特殊说明外，统一为：

```json
{
  "code": "OK",
  "msg": "OK",
  "data": { },
  "request_id": "..."
}
```

## 目录

### 创建目录

用途：创建一个新的目录，用于组织库与卷。

```
POST /catalog/create
```

**Body 输入参数：**

| 参数         | 是否必填 | 类型   | 含义     |
| ------------ | -------- | ------ | -------- |
| name         | 是       | string | 目录名称 |
| description  | 否       | string | 描述     |

**示例 (Python)：**

```python
import requests, json
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/create"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "name": "my-catalog",
    "description": "业务域 A 的目录"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": 1
  }
}
```

### 获取目录列表

用途：分页返回当前账号下的目录集合及统计信息。

```
POST /catalog/list
```

**请求：**仅需 `moi-key` 请求头。

**示例 (Python)：**

```python
import requests, json
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/list"
headers = {
    "moi-key": "xxxxx"
}
print(requests.post(url, headers=headers).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "list": [
      {
        "id": 1,
        "name": "my-catalog",
        "description": "业务域 A 的目录",
        "database_count": 2,
        "file_count": 10,
        "table_count": 5,
        "volume_count": 1,
        "reserved": false,
        "created_at": "2025-02-13T10:00:00Z",
        "updated_at": "2025-02-13T10:10:00Z",
        "created_by": "user_a",
        "updated_by": "user_a"
      },
      {
        "id": 2,
        "name": "marketing",
        "description": "市场线目录",
        "database_count": 1,
        "file_count": 3,
        "table_count": 2,
        "volume_count": 1,
        "reserved": false,
        "created_at": "2025-02-12T09:00:00Z",
        "updated_at": "2025-02-12T09:05:00Z",
        "created_by": "user_b",
        "updated_by": "user_b"
      }
    ]
  }
}
```

### 根据 ID 获取目录详情

用途：根据目录 ID 获取目录的基本信息（名称、描述）。

```
POST /catalog/info
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型    | 含义   |
| ---- | -------- | ------- | ------ |
| id   | 是       | integer | 目录 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/info"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": 1
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": 1,
    "name": "my-catalog",
    "description": "业务域 A 的目录"
  }
}
```

### 更新目录

用途：修改目录名称或描述。

```
POST /catalog/update
```

**Body 输入参数：**

| 参数        | 是否必填 | 类型    | 含义     |
| ----------- | -------- | ------- | -------- |
| id          | 是       | integer | 目录 ID   |
| name        | 是       | string  | 目录名称 |
| description | 否       | string  | 描述     |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/update"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": 1,
    "name": "my-catalog-renamed",
    "description": "目录描述更新"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": 1
  }
}
```

### 删除目录

用途：删除指定目录（仅当无强依赖资源时允许删除）。

```
POST /catalog/delete
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型    | 含义   |
| ---- | -------- | ------- | ------ |
| id   | 是       | integer | 目录 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/delete"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": 1
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": 1
  }
}
```

### 获取目录树

用途：以树形结构返回目录下的库与卷层级。

```
POST /catalog/tree
```

**请求：**仅需 `moi-key` 请求头。

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "tree": [
      {
        "id": "catalog-1",
        "name": "my-catalog",
        "type": "catalog",
        "description": "业务域 A 的目录",
        "has_workflow_target_ref": false,
        "node_list": [
          {
            "id": "db-100",
            "name": "db1",
            "type": "database",
            "description": "业务库",
            "node_list": [
              {
                "id": "vol-abc",
                "name": "origin",
                "type": "volume",
                "description": "源数据卷",
                "node_list": []
              }
            ]
          }
        ]
      }
    ]
  }
}
```

## 库

### 创建库

用途：在指定目录下创建库。

```
POST /catalog/database/create
```

**Body 输入参数：**

| 参数       | 是否必填 | 类型    | 含义     |
| ---------- | -------- | ------- | -------- |
| catalog_id | 是       | integer | 目录 ID   |
| name       | 是       | string  | 库名 |
| description| 否       | string  | 描述     |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/database/create"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "catalog_id": 1,
    "name": "db1",
    "description": "业务库"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": 100
  }
}
```

### 获取库列表

用途：返回某个目录下的库集合及统计信息。

```
POST /catalog/database/list
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型    | 含义   |
| ---- | -------- | ------- | ------ |
| id   | 是       | integer | 目录 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/database/list"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": 1
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "list": [
      {
        "id": 100,
        "name": "db1",
        "description": "业务库",
        "file_count": 0,
        "table_count": 0,
        "reserved": false,
        "created_at": "2025-02-13T10:00:00Z",
        "updated_at": "2025-02-13T10:05:00Z",
        "created_by": "user_a",
        "updated_by": "user_a"
      }
    ]
  }
}
```

### 根据 ID 获取库详情

用途：根据库 ID 获取详细信息（含创建/更新时间）。

```
POST /catalog/database/info
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型    | 含义   |
| ---- | -------- | ------- | ------ |
| id   | 是       | integer | 库 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/database/info"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": 100
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": 100,
    "name": "db1",
    "description": "业务库",
    "created_at": "2025-02-13T10:00:00Z",
    "updated_at": "2025-02-13T10:05:00Z"
  }
}
```

### 更新库

用途：修改库的描述信息。

```
POST /catalog/database/update
```

**Body 输入参数：**

| 参数        | 是否必填 | 类型    | 含义   |
| ----------- | -------- | ------- | ------ |
| id          | 是       | integer | 库 ID |
| description | 否       | string  | 描述     |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/database/update"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": 100,
    "description": "描述更新"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": 100
  }
}
```

### 删除库

用途：删除指定库（需确保无依赖资源）。

```
POST /catalog/database/delete
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型    | 含义   |
| ---- | -------- | ------- | ------ |
| id   | 是       | integer | 库 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/database/delete"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": 100
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": 100
  }
}
```

### 获取库子列表

用途：查询库下的子资源列表（如卷）。

```
POST /catalog/database/children
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型    | 含义   |
| ---- | -------- | ------- | ------ |
| id   | 是       | integer | 库 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/database/children"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": 100
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "list": [
      {
        "id": "vol-abc",
        "name": "origin",
        "type": "volume",
        "size": 0,
        "children_count": 0,
        "reserved": false,
        "created_at": "2025-02-13T10:10:00Z",
        "updated_at": "2025-02-13T10:10:00Z",
        "created_by": "user_a",
        "updated_by": "user_a"
      }
    ]
  }
}
```

## 卷

### 创建卷

用途：在库下创建卷，用于存放文件与处理结果。

```
POST /catalog/volume/create
```

**Body 输入参数：**

| 参数        | 是否必填 | 类型    | 含义     |
| ----------- | -------- | ------- | -------- |
| database_id | 是       | integer | 库 ID |
| name        | 是       | string  | 卷名称   |
| description | 否       | string  | 描述     |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/volume/create"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "database_id": 100,
    "name": "origin",
    "description": "源数据卷"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": "vol-abc"
  }
}
```

### 获取卷详情

用途：根据卷 ID 获取卷的基础信息。

```
POST /catalog/volume/info
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型   | 含义 |
| ---- | -------- | ------ | ---- |
| id   | 是       | string | 卷 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/volume/info"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": "vol-abc"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": "vol-abc",
    "name": "origin",
    "description": "源数据卷",
    "created_at": "2025-02-13T10:10:00Z",
    "updated_at": "2025-02-13T10:10:00Z"
  }
}
```

### 更新卷

用途：修改卷的名称与描述。

```
POST /catalog/volume/update
```

**Body 输入参数：**

| 参数        | 是否必填 | 类型   | 含义   |
| ----------- | -------- | ------ | ------ |
| id          | 是       | string | 卷 ID   |
| name        | 是       | string | 卷名称 |
| description | 是       | string | 描述   |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/volume/update"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": "vol-abc",
    "name": "origin-updated",
    "description": "源数据卷描述更新"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": "vol-abc"
  }
}
```

### 删除卷

用途：删除指定卷（需确保未被引用）。

```
POST /catalog/volume/delete
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型   | 含义 |
| ---- | -------- | ------ | ---- |
| id   | 是       | string | 卷 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/volume/delete"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": "vol-abc"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": "vol-abc"
  }
}
```

## 文件

### 获取文件信息

用途：根据文件 ID 获取文件详情（类型、大小、归属卷等）。

```
POST /catalog/file/info
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型   | 含义   |
| ---- | -------- | ------ | ------ |
| id   | 是       | string | 文件 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/file/info"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": "file-xyz"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": "file-xyz",
    "name": "demo.md",
    "file_type": "text",
    "file_ext": ".md",
    "origin_file_ext": ".md",
    "parent_id": "",
    "ref_file_id": "",
    "show_type": "markdown",
    "size": 1234,
    "created_at": "2025-02-13T11:00:00Z",
    "updated_at": "2025-02-13T11:10:00Z",
    "volume_id": "vol-abc"
  }
}
```

### 获取文件列表

用途：分页查询卷内或账号范围内的文件列表，支持排序过滤。

```
POST /catalog/file/list
```

**Body 输入参数（可选）：**

| 参数       | 类型              | 含义                 |
| ---------- | ----------------- | -------------------- |
| filters    | array[Filter]     | 过滤条件             |
| order      | string            | asc/desc             |
| order_by   | string            | 排序字段             |
| page       | integer           | 页码（默认 1）        |
| page_size  | integer           | 每页数量（默认 10）   |

- `Filter` 对象结构：
  - `name`: string - 过滤字段名称（如："volume_id" 表示按卷名过滤）
  - `values`: string [] - 过滤值数组（如：["vol-abc", "vol-def"] 表示卷 ID 列表）
  - `fuzzy`: boolean - 是否模糊匹配

**示例 (Python)：**

基础查询示例：

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/file/list"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "order": "desc",
    "order_by": "created_at",
    "page": 1,
    "page_size": 10
}
print(requests.post(url, headers=headers, json=body).json())
```

按卷过滤查询示例：

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/file/list"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "filters": [
        {
            "name": "volume_name",
            "values": ["vol-abc", "vol-def"],
            "fuzzy": false
        }
    ],
    "order": "desc",
    "order_by": "created_at",
    "page": 1,
    "page_size": 10
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "list": [
      {
        "id": "file-xyz",
        "name": "demo.md",
        "file_type": "text",
        "file_ext": ".md",
        "origin_file_ext": ".md",
        "parent_id": "",
        "ref_file_id": "",
        "ref_workflow_id": "",
        "save_path": "/user_a/origin/file-xyz/demo.md",
        "show_path": "/origin/demo.md",
        "show_type": "markdown",
        "size": 1234,
        "created_at": "2025-02-13T11:00:00Z",
        "updated_at": "2025-02-13T11:10:00Z",
        "created_by": "user_a",
        "volume_id": "vol-abc",
        "volume_name": "origin",
        "volume_reserved": false
      }
    ],
    "total": 1
  }
}
```

### 更新文件

用途：修改文件名称等元数据。

```
POST /catalog/file/update
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型   | 含义   |
| ---- | -------- | ------ | ------ |
| id   | 是       | string | 文件 ID |
| name | 是       | string | 新名称 |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/file/update"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": "file-xyz",
    "name": "demo-renamed.md"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": "file-xyz"
  }
}
```

### 删除文件

用途：删除指定文件记录（若存在引用关系需先解除）。

```
POST /catalog/file/delete
```

**Body 输入参数：**

| 参数 | 是否必填 | 类型   | 含义   |
| ---- | -------- | ------ | ------ |
| id   | 是       | string | 文件 ID |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/file/delete"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "id": "file-xyz"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "id": "file-xyz"
  }
}
```

### 下载文件链接

用途：获取文件的直链下载地址（带签名，短时有效）。

```
POST /catalog/file/download
```

**Body 输入参数：**

| 参数      | 是否必填 | 类型   | 含义   |
| --------- | -------- | ------ | ------ |
| file_id   | 是       | string | 文件 ID |
| volume_id | 否       | string | 卷 ID   |

**示例 (Python)：**

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/catalog/file/download"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "file_id": "file-xyz",
    "volume_id": "vol-abc"
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "OK",
  "msg": "OK",
  "data": {
    "link": "https://oss.example.com/bucket/user_a/origin/file-xyz/demo.md?signature=..."
  }
}
```

## 文件分块

### 获取文件分块

用途：获取文件的块数据，支持数据增强结果和普通嵌入块数据两种模式。

```
POST /byoa/api/v1/explore/volumes/{vid}/files/{fid}/blocks
```

**路径参数：**

| 参数 | 是否必填 | 类型   | 含义   |
| ---- | -------- | ------ | ------ |
| vid  | 是       | string | 卷 ID  |
| fid  | 是       | string | 文件 ID |

**请求头：**

| 参数     | 是否必填 | 类型   | 含义    |
| -------- | -------- | ------ | ------- |
| moi-key  | 是       | string | API Key |

**Body 输入参数（可选）：**

| 参数    | 类型    | 含义                     |
| ------- | ------- | ------------------------ |
| filters | object  | 过滤条件                 |
| offset  | integer | 偏移量（默认 0）         |
| limit   | integer | 限制数量（默认 30）      |

**Filters 对象结构：**

| 参数           | 类型     | 含义                     |
| -------------- | -------- | ------------------------ |
| types          | string[] | 块类型筛选               |
| levels         | string[] | 层级筛选                 |
| search_content | string   | 搜索内容                 |
| block_ids      | string[] | 指定块 ID 列表           |
| list_embedding | boolean  | 是否列出嵌入信息         |

**示例 (Python)：**

基础查询示例：

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/vol-abc/files/file-xyz/blocks"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "offset": 0,
    "limit": 30
}
print(requests.post(url, headers=headers, json=body).json())
```

带过滤条件查询示例：

```python
import requests
url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/explore/volumes/vol-abc/files/file-xyz/blocks"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "filters": {
        "types": ["text", "table"],
        "search_content": "关键词",
        "list_embedding": true
    },
    "offset": 0,
    "limit": 30
}
print(requests.post(url, headers=headers, json=body).json())
```

**返回：**

```json
{
  "code": "ok",
  "msg": "ok",
  "data": {
    "total": 25,
    "type": 0,
    "items": [
      {
        "id": "block-123",
        "content": "这是文档的一个文本块内容...",
        "type": "text",
        "content_type": "text",
        "file_id": "file-xyz",
        "description": "段落内容",
        "created_at": "2025-02-13T12:00:00Z",
        "updated_at": "2025-02-13T12:00:00Z",
        "text_and_image_id": null,
        "image_process_type": null,
        "level": "paragraph"
      },
      {
        "id": "block-124", 
        "content": "这是另一个文本块内容...",
        "type": "text",
        "content_type": "text",
        "file_id": "file-xyz",
        "description": "段落内容",
        "created_at": "2025-02-13T12:01:00Z",
        "updated_at": "2025-02-13T12:01:00Z",
        "text_and_image_id": null,
        "image_process_type": null,
        "level": "paragraph"
      }
    ]
  }
}
```
