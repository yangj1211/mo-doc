# 数据导出 API 文档

## 概述

数据导出 API 提供了一套完整的接口来管理和执行数据导出任务。支持将工作流处理的数据导出到外部系统，如 Dify 知识库等。

## 导出任务管理

### 创建导出任务

```
POST /export/task/create
```

**请求头：**

| 参数     | 是否必填 | 类型   | 含义   |
| -------- | -------- | ------ | ------ |
| moi-key  | 是       | string | API Key |

**输入参数：**

| 参数                                | 是否必填 | 类型    | 含义                         |
| ---------------------------------- | ------- | ------- | ---------------------------- |
| task_name                          | 是      | string  | 任务名称                     |
| creator                            | 是      | string  | 创建者                       |
| connector_id                       | 是      | integer | 连接器 ID                    |
| connector_name                     | 是      | string  | 连接器名称                   |
| type                               | 是      | integer | 任务类型                     |
| config                             | 是      | object  | 导出配置对象                 |
| &nbsp;&nbsp;&nbsp;&nbsp;dify_config| 否      | object  | Dify 配置对象                |
| &nbsp;&nbsp;&nbsp;&nbsp;s3_config  | 否      | object  | OSS 和 S3 的导出配置            |
| &nbsp;&nbsp;&nbsp;&nbsp;mo_config  | 否      | object  | MatrixOne 导出配置对象       |
| &nbsp;&nbsp;&nbsp;&nbsp;merge_title_to_text| 否  | boolean | 是否将标题合并到文本，默认 false |
| files                              | 是      | array   | 文件列表                     |
| &nbsp;&nbsp;&nbsp;&nbsp;file_id    | 是      | string  | 文件 ID                      |
| &nbsp;&nbsp;&nbsp;&nbsp;full_path  | 是      | array   | 文件完整路径数组             |
| &nbsp;&nbsp;&nbsp;&nbsp;is_raw     | 是      | boolean | 是否为原始文件               |

Config 对象详细结构

#### dify_config 对象

| 参数            | 是否必填 | 类型   | 含义      |
| -------------- | ------- | ------ | --------- |
| dataset_id     | 是      | string | 数据集 ID |
| dataset_name   | 是      | string | 数据集名称 |
| embedding_model| 是      | string | 嵌入模型   |

#### s3_config 对象

| 参数            | 是否必填 | 类型    | 含义                |
| -------------- | ------- | ------- | ------------------- |
| path           | 是      | string  | 导出的文件夹地址     |
| need_compress  | 否      | boolean | 是否需要压缩，默认 false |
| compress_method| 否      | string  | 压缩方式            |

#### mo_config 对象

| 参数                | 是否必填 | 类型    | 含义                    |
| ------------------ | ------- | ------- | ----------------------- |
| database_name      | 是      | string  | 数据库名                |
| table_name         | 是      | string  | 表名                    |
| new_table          | 否      | boolean | 是否新建表，默认 false   |
| column             | 是      | object  | 列配置对象              |
| &nbsp;&nbsp;&nbsp;&nbsp;export_column | 是 | array | 字段映射列表 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;source_column | 是 | string | 源字段名 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mapping_column | 是 | string | 目标字段名 |
| &nbsp;&nbsp;&nbsp;&nbsp;combine_column | 是 | array | 需要合并的字段名列表 |
| duplicated_strategy| 是      | integer | 重复数据处理策略（整数） |

**使用说明：**

- 导出到 Dify：提供 `dify_config` 配置

- 导出到 S3/OSS：提供 `s3_config` 配置  

- 导出到 MatrixOne：提供 `mo_config` 配置并设置列映射与重复策略

- 可以同时配置多个导出目标

**示例 (Python)：**

导出到 Dify 示例：

```python
import requests

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/export/task/create"
headers = {
    "moi-key": "xxxxx"
}

body = {
    "task_name": "导出到 Dify 任务",
    "creator": "admin",
    "connector_id": 1,
    "connector_name": "Dify 连接器",
    "type": 1,
    "config": {
        "dify_config": {
            "dataset_id": "dataset_123",
            "dataset_name": "测试数据集",
            "embedding_model": "text-embedding-ada-002"
        },
        "merge_title_to_text": false
    },
    "files": [
        {
            "file_id": "file_456",
            "full_path": ["data", "documents", "test.pdf"],
            "is_raw": false
        }
    ]
}

response = requests.post(url, json=body, headers=headers)
print(response.json())
```

导出到 S3/OSS 示例：

```python
import requests

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/export/task/create"
headers = {
    "moi-key": "xxxxx"
}

body = {
    "task_name": "导出到 S3 任务",
    "creator": "admin", 
    "connector_id": 2,
    "connector_name": "S3 连接器",
    "type": 2,
    "config": {
        "s3_config": {
            "path": "/export/data/",
            "need_compress": true,
            "compress_method": "zip"
        }
    },
    "files": [
        {
            "file_id": "file_789",
            "full_path": ["data", "processed", "result.json"],
            "is_raw": false
        }
    ]
}

response = requests.post(url, json=body, headers=headers)
print(response.json())
```

导出到 MatrixOne 示例：

```python
import requests

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/export/task/create"
headers = {
    "moi-key": "xxxxx"
}

body = {
    "task_name": "导出到 MatrixOne 任务",
    "creator": "admin",
    "connector_id": 3,
    "connector_name": "MatrixOne 连接器",
    "type": 3,
    "config": {
        "mo_config": {
            "database_name": "test_db",
            "table_name": "documents",
            "new_table": true,
            "column": {
                "export_column": [
                    {
                        "source_column": "content",
                        "mapping_column": "doc_content"
                    },
                    {
                        "source_column": "title", 
                        "mapping_column": "doc_title"
                    }
                ],
                "combine_column": ["content", "title"]
            },
            "duplicated_strategy": 1
        },
        "merge_title_to_text": false
    },
    "files": [
        {
            "file_id": "file_101",
            "full_path": ["data", "documents", "report.pdf"],
            "is_raw": false
        }
    ]
}

response = requests.post(url, json=body, headers=headers)
print(response.json())
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": null
}
```

### 查询导出任务列表

```
POST /export/task/list
```

**请求头：**

| 参数     | 是否必填 | 类型   | 含义    |
| -------- | -------- | ------ | ------- |
| moi-key  | 是       | string | API Key |

**输入参数：**

| 参数            | 数据类型 | 是否必填 | 含义         | 默认值     |
| --------------- | ------- | ------- | ------------ | ---------- |
| offset          | int     | 否      | 分页偏移量    | 0          |
| limit           | int     | 否      | 分页限制     | 10         |
| statuses        | array   | 否      | 任务状态列表  |            |
| creator         | string  | 否      | 任务创建用户  |            |
| connector_name  | string  | 否      | 连接器名称    |            |
| task_id         | string  | 否      | 任务 ID      |            |
| order_by        | string  | 否      | 排序字段     | created_at |
| order_direction | string  | 否      | 排序方向     | desc       |

**输出参数：**

| 参数                                | 含义         |
| ---------------------------------- | ------------ |
| tasks                              | 导出任务列表 |
| &nbsp;&nbsp;&nbsp;&nbsp;id         | 任务 ID      |
| &nbsp;&nbsp;&nbsp;&nbsp;name       | 任务名称     |
| &nbsp;&nbsp;&nbsp;&nbsp;connector_name | 连接器名称 |
| &nbsp;&nbsp;&nbsp;&nbsp;type       | 任务类型     |
| &nbsp;&nbsp;&nbsp;&nbsp;status     | 任务状态     |
| &nbsp;&nbsp;&nbsp;&nbsp;export_source | 导出源     |
| &nbsp;&nbsp;&nbsp;&nbsp;create_time | 创建时间     |
| &nbsp;&nbsp;&nbsp;&nbsp;end_time   | 结束时间     |
| total                              | 总数量       |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/export/task/list"
headers = {
    "moi-key": "xxxxx"
}

body = {
    "offset": 0,
    "limit": 10,
    "statuses": [1, 2],
    "creator": "admin",
    "order_by": "created_at",
    "order_direction": "desc"
}

response = requests.post(url, json=body, headers=headers)

print("Response Body:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "tasks": [
            {
                "id": "string",
                "name": "string",
                "connector_name": "string",
                "type": 1,
                "status": 2,
                "export_source": [["string"]],
                "create_time": "2024-01-01T00:00:00Z",
                "end_time": "2024-01-01T01:00:00Z"
            }
        ],
        "total": 1
    }
}
```

### 获取导出任务详情

```
POST /export/task/info
```

**请求头：**

| 参数     | 是否必填 | 类型   | 含义    |
| -------- | -------- | ------ | ------- |
| moi-key  | 是       | string | API Key |

**输入参数：**

| 参数 | 是否必填 | 类型   | 含义    |
| ---- | ------- | ------ | ------- |
| id   | 是      | string | 任务 ID |

**输出参数：**

| 参数                                | 含义                     |
| ---------------------------------- | ------------------------ |
| id                                 | 任务 ID                  |
| name                               | 任务名称                 |
| creator                            | 创建者                   |
| connector_name                     | 连接器名称               |
| type                               | 任务类型                 |
| status                             | 任务状态                 |
| config                             | 导出配置                 |
| &nbsp;&nbsp;&nbsp;&nbsp;dify_config| Dify 配置对象            |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dataset_id | 数据集 ID |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dataset_name | 数据集名称 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;embedding_model | 嵌入模型 |
| &nbsp;&nbsp;&nbsp;&nbsp;merge_title_to_text| 是否合并标题 |
| create_time                        | 创建时间                 |
| end_time                           | 结束时间                 |
| file_stats                         | 文件导出状态             |
| &nbsp;&nbsp;&nbsp;&nbsp;total      | 总数                     |
| &nbsp;&nbsp;&nbsp;&nbsp;pending    | 等待中                   |
| &nbsp;&nbsp;&nbsp;&nbsp;running    | 运行中                   |
| &nbsp;&nbsp;&nbsp;&nbsp;failed     | 失败                     |
| &nbsp;&nbsp;&nbsp;&nbsp;completed  | 完成                     |
| fileSuccess| 成功总数                 |
| fileFail   | 失败总数                 |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/export/task/info"
headers = {
    "moi-key": "xxxxx"
}

body = {
    "id": "task_123"
}

response = requests.post(url, json=body, headers=headers)

print("Response Body:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "id": "task_123",
        "name": "导出到 Dify 任务",
        "creator": "admin",
        "connector_name": "Dify 连接器",
        "type": 1,
        "status": 2,
        "config": {
            "dify_config": {
                "dataset_id": "dataset_123",
                "dataset_name": "测试数据集",
                "embedding_model": "text-embedding-ada-002"
            },
            "merge_title_to_text": false
        },
        "create_time": "2024-01-01T00:00:00Z",
        "end_time": "2024-01-01T01:00:00Z",
        "file_stats": {
            "total": 100,
            "pending": 10,
            "running": 20,
            "failed": 5,
            "completed": 65,
            "fileSuccess": 65,
            "fileFail": 5
        }
    }
}
```

### 查询导出任务文件列表

```
POST /export/task/files
```

**请求头：**

| 参数     | 是否必填 | 类型   | 含义    |
| -------- | -------- | ------ | ------- |
| moi-key  | 是       | string | API Key |

**输入参数：**

| 参数            | 数据类型 | 是否必填 | 含义         | 默认值     |
| --------------- | ------- | ------- | ------------ | ---------- |
| offset          | int     | 否      | 分页偏移量    | 0          |
| limit           | int     | 否      | 分页限制     | 10         |
| task_id         | string  | 是      | 任务 ID      |            |
| statuses        | array   | 否      | 文件状态列表  |            |
| order_by        | string  | 否      | 排序字段     | created_at |
| order_direction | string  | 否      | 排序方向     | desc       |

**输出参数：**

| 参数                                | 含义             |
| ---------------------------------- | ---------------- |
| files                              | 文件列表         |
| &nbsp;&nbsp;&nbsp;&nbsp;id         | 文件 ID          |
| &nbsp;&nbsp;&nbsp;&nbsp;status     | 文件状态         |
| &nbsp;&nbsp;&nbsp;&nbsp;full_path  | 文件完整路径     |
| &nbsp;&nbsp;&nbsp;&nbsp;details    | 详细信息         |
| &nbsp;&nbsp;&nbsp;&nbsp;create_time| 创建时间         |
| &nbsp;&nbsp;&nbsp;&nbsp;start_time | 开始时间         |
| &nbsp;&nbsp;&nbsp;&nbsp;end_time   | 结束时间         |
| &nbsp;&nbsp;&nbsp;&nbsp;file_name  | 文件名           |
| &nbsp;&nbsp;&nbsp;&nbsp;file_type  | 文件类型         |
| total                              | 总数量           |
| total_failure                      | 导出失败的文件数  |
| total_files                        | 导出总文件数     |
| total_success                      | 导出成功文件数   |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/export/task/files"
headers = {
    "moi-key": "xxxxx"
}

body = {
    "offset": 0,
    "limit": 10,
    "task_id": "task_123",
    "statuses": [1, 2],
    "order_by": "created_at",
    "order_direction": "desc"
}

response = requests.post(url, json=body, headers=headers)

print("Response Body:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "files": [
            {
                "id": "file_123",
                "status": 2,
                "full_path": ["data", "documents", "test.pdf"],
                "details": "导出成功",
                "create_time": "2024-01-01T00:00:00Z",
                "start_time": "2024-01-01T00:00:00Z",
                "end_time": "2024-01-01T01:00:00Z",
                "file_name": "test.pdf",
                "file_type": 1
            },
            {
                "id": "file_124",
                "status": 3,
                "full_path": ["data", "documents", "report.docx"],
                "details": "导出失败：文件格式不支持",
                "create_time": "2024-01-01T00:05:00Z",
                "start_time": "2024-01-01T00:05:00Z",
                "end_time": "2024-01-01T00:06:00Z",
                "file_name": "report.docx",
                "file_type": 2
            }
        ],
        "total": 50,
        "total_failure": 5,
        "total_files": 50,
        "total_success": 45
    }
}
```

### 导出失败重试

```
POST /export/task/{task_id}/rerun
```

**请求头：**

| 参数     | 是否必填 | 类型   | 含义    |
| -------- | -------- | ------ | ------- |
| moi-key  | 是       | string | API Key |

**路径参数：**

| 参数    | 是否必填 | 类型   | 含义        |
| ------- | ------- | ------ | ----------- |
| task_id | 是      | string | 导出任务 ID |

**示例：**

```python
import requests

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/export/task/task_123/rerun"
headers = {
    "moi-key": "xxxxx"
}

response = requests.post(url, headers=headers)

if response.status_code == 200:
    print(response.json()) 
else:
    print(f"请求失败，状态码：{response.status_code}, 错误信息：{response.text}")
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": null
}
```

### 删除导出任务

```
POST /export/task/delete
```

**请求头：**

| 参数     | 是否必填 | 类型   | 含义    |
| -------- | -------- | ------ | ------- |
| moi-key  | 是       | string | API Key |

**输入参数：**

| 参数 | 是否必填 | 类型   | 含义    |
| ---- | ------- | ------ | ------- |
| id   | 是      | string | 任务 ID |

**示例：**

```python
import requests

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/export/task/delete"
headers = {
    "moi-key": "xxxxx"
}

body = {
    "id": "task_123"
}

response = requests.post(url, json=body, headers=headers)

if response.status_code == 200:
    print(response.json()) 
else:
    print(f"请求失败，状态码：{response.status_code}, 错误信息：{response.text}")
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": null
}
```