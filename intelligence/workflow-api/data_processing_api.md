# 数据处理相关 API

## 工作流

工作流是一套数据处理流程，由一些数据处理节点组成，每个节点是一个处理单元，这些节点组成一个 DAG 图。文档处理过程就是文档的数据按照这个 DAG 图进行处理和流转的过程。

一个工作流包含两部分重要内容：

* 节点：一个文档处理单元，输入是具体的文档，比如一个 pdf 文件，或者 pdf 文件分段后的结果（如以 800 个字符大小进行分段），输出是经过节点处理后的文档或者分段。
* 节点之间的连线：表示数据处理流向，将所有节点构成一个 DAG 图。如果 A 节点有一条指向 B 节点的连线，表示 A 节点的输出是 B 节点的输入。

### 创建工作流

```
POST /byoa/api/v1/workflow_meta
```

**Body 输入参数：**

| 参数名                      | 是否必填 | 类型                         | 含义                           | 默认值 |
| --------------------------- | -------- | ---------------------------- | ------------------------------ | ------ |
| **name**                      | 是       | string                       | 工作流名称                     |        |
| **source_volume_names**       | 是       | array[string]                | 源数据卷名称列表               |        |
| **source_volume_ids**         | 是       | array[integer]               | 源数据卷 ID 列表                 |        |
| **file_types**                | 是       | array[integer]               | 文件类型列表，支持：<br>NIL = 0<br>TXT = 1<br>PDF = 2<br>IMAGE = 3<br>PPT = 4<br>WORD = 5<br>MARKDOWN = 6<br>CSV = 7<br>PARQUET = 8<br>SQL_FILES = 9<br>DIR = 10<br>DOCX = 11<br>PPTX = 12<br>WAV = 13<br>MP3 = 14<br>AAC = 15<br>FLAC = 16<br>MP4 = 17<br>MOV = 18<br>MKV = 19<br>PNG = 20<br>JPG = 21<br>JPEG = 22<br>BMP = 23                   |        |
| **process_mode**              | 是       | object (**ProcessModeConfig**) | 处理模式配置                   |        |
| **priority**                  | 否       | integer                      | 优先级                         | 300    |
| **target_volume_id**          | 是       | string                       | 目标数据卷 ID                   |        |
| **target_volume_name**        | 否       | string                       | 目标数据卷名称                 | ""     |
| **create_target_volume_name** | 是       | string                       | 创建目标数据卷时使用的名称     |        |
| **workflow**                  | 是       | object (**WorkflowConfig**)    | 工作流配置  |        |
| **branch_name**               | 否       | string                       | 分支名    | "main"     |
| **files**                     | 否       | array[object]                | 预处理文件列表（`SourceFileInfo`） |        |
| **content**                   | 否       | object                        | 工作流额外说明                   |        |

* **ProcessModeConfig 结构：**

  | 参数       | 是否必填 | 类型    | 含义                   |
  | ---------- | -------- | ------- | ---------------------- |
  | **interval** | 是       | integer | 处理模式：0 表示一次性处理，-1 表示关联处理，大于 0 表示周期性处理且值为处理间隔（分钟） |
  | **offset**   | 是       | integer | 处理时间偏移量（分钟），一次性载入时默认为 0 |

* **WorkflowConfig 结构：**

  * **components**: 组件配置列表。每个组件对象包含 **name**, **type**, **component_id**, **intro**, **position**, **input_keys**, **output_keys**, **init_parameters**。
  * **connections**: 连接配置列表。每个连接对象包含 **sender** 和 **receiver**。
  * **edges**: 边配置列表。
  * **extra_components**: 额外组件配置列表。

**示例 (Python)：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta"

headers = {
    "moi-key": "xxxxx"
}

body = {
    "name": "wf-from-meta-api",
    "source_volume_names": ["b-vol1"],
    "source_volume_ids": [1889223879880048640],
    "target_volume_id": "eb42f0a1-ab18-4010-b95c-cd1716dd5e95",
    "create_target_volume_name": "new-target-for-wf-from-meta",
    "process_mode": {
        "interval": 0,
        "offset": 0
    },
    "file_types": [2],
    "priority": 300,
    "workflow": {
        "components": [
            {
                "name": "DocumentCleaner",
                "type": "haystack.components.preprocessors.document_cleaner.DocumentCleaner",
                "component_id": "DocumentCleaner_1739377283742",
                "intro": "DocumentCleaner",
                "position": {"x": 0, "y": 0},
                "input_keys": {},
                "output_keys": {},
                "init_parameters": {
                    "ascii_only": False,
                    "keep_id": False,
                    "remove_empty_lines": True,
                    "remove_extra_whitespaces": True,
                    "remove_regex": "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+)|https?://[^\\s]+",
                    "remove_repeated_substrings": False
                }
            }
            
            ,{
                "name":"DocumentWriter",
                "type":"haystack.components.writers.document_writer.DocumentWriter",
                "component_id":"DocumentWriter_1739377283742",
                "intro":"DocumentWriter",
                "position":{"x":0,"y":0},
                "input_keys":{},
                "output_keys":{},
                "init_parameters":{
                    "document_store":{
                        "init_parameters":{
                            "connection_string":{
                                "env_vars":["DATABASE_SYNC_URI"],
                                "strict":True,
                                "type":"env_var"
                            },
                            "embedding_dimension":1024,
                            "keyword_index_name":"haystack_keyword_index",
                            "recreate_table":True,
                            "table_name":"embedding_results",
                            "vector_function":"cosine_similarity"
                        },
                        "type":"byoa.integrations.document_stores.mo_document_store.MOIDocumentStore"
                    },
                    "policy":"NONE"
                }
            }
        ],
        "connections": [],
        "edges": [],
        "extra_components": []
    }
}

response = requests.post(url, json=body, headers=headers)

print(response.status_code)
print(json.dumps(response.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "created_at": "2025-05-30T09:45:58",
        "id": "cf68d259-9cd6-4f44-a0a4-5674c79da083",
        "user_id": "01960e07-60ec-7a3c-b45f-415b7e40e8bf",
        "flow_interval": 0,
        "creator": "admin",
        "file_types": "[1, 2, 4, 5, 6, 7, 11, 12]",
        "target_volume_id": "04614636-b858-4b13-99bf-a036d9351289",
        "files": "[]",
        "updated_at": "2025-05-30T09:45:58",
        "version": "1",
        "priority": 300,
        "name": "test",
        "group_id": "",
        "flow_offset": 0,
        "modifier": "admin",
        "source_volume_ids": "[\"1928383194482323456\"]",
        "source_volume_names": "[\"b_vol3\"]",
        "target_volume_name": "b_vol3"
    }
}
```

### 查看工作流列表

```
GET /byoa/api/v1/workflow_meta
```

**Query 参数：**

| 参数名          | 类型                                  | 是否必填 | 描述                          | 默认值       |
| --------------- | ------------------------------------- | -------- | ----------------------------- | ------------ |
| **name_search**   | string, nullable                      | 否       | 名称搜索 (工作流名)           |              |
| **start_time**    | integer, nullable                     | 否       | 开始时间戳 (毫秒)             |              |
| **end_time**      | integer, nullable                     | 否       | 结束时间戳 (毫秒)             |              |
| **process_modes** | array[integer], nullable              | 否       | 处理模式 (通常指 interval 值) |              |
| **status**        | array[integer], nullable              | 否       | 状态 (例如：1-运行中，2-完成) |              |
| **file_types**    | array[integer], nullable              | 否       | 文件类型                      |              |
| **priority**      | array[integer], nullable              | 否       | 优先级                        |              |
| **creator**       | string, nullable                      | 否       | 创建者                        |              |
| **offset**        | integer, >=0                          | 否       | 当页偏移量                    | 0            |
| **limit**         | integer, >=1                          | 否       | 每页大小                      | 20           |
| **sort_field**    | string, nullable                      | 否       | 排序字段                      | "created_at" |
| **sort_order**    | string, nullable ("ascend"/"descend") | 否       | 排序方式                      | "descend"    |

**示例 (Python)：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta"
headers = {
    "moi-key": "xxxxx"
}
params = {
    "limit": 5,
    "sort_field": "name",
    "sort_order": "ascend"
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(json.dumps(response.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "total": 20,
        "workflows": [
            {
                "id": "YOUR_WORKFLOW_ID_1",
                "name": "Alpha Workflow",
                "created_at": 1739377287000,
                "creator": "YOUR_USERNAME",
                "updated_at": 1739377755000,
                "modifier": "YOUR_USERNAME",
                "source_volume_ids": ["YOUR_SOURCE_VOLUME_ID_1"],
                "source_volume_names": ["b-vol1"],
                "file_types": [2],
                "target_volume_id": "YOUR_TARGET_VOLUME_ID_1",
                "target_volume_name": "a-vol1",
                "process_mode": {"interval": 0, "offset": 0},
                "priority": 300,
                "status": 2,
                "version": "1.0",
                "branch_total": 1,
                "branch_id": "YOUR_BRANCH_ID_1", 
                "branch_name": "main",
                "branch_status": 0,
                "branch_volume_id": "YOUR_BRANCH_TARGET_VOLUME_ID_1"
            }
            
        ]
    }
}
```

**输出参数：**

| 参数        | 类型                                    | 描述                                           |
| ----------- | --------------------------------------- | ---------------------------------------------- |
| **total**     | integer                                 | 符合条件的工作流总数                           |
| **workflows** | array[object] | 工作流列表，每个对象包含工作流及其主要分支信息 |

* **`WorkflowListItem` 对象结构:**
    * id (string): 工作流 ID
    * name (string): 工作流名称
    * created_at (integer): 创建时间戳 (毫秒)
    * creator (string): 创建者
    * updated_at (integer): 更新时间戳 (毫秒)
    * modifier (string, nullable): 更新者
    * source_volume_ids (array[string]): 源数据卷 ID 列表
    * source_volume_names (array[string]): 源数据卷名称列表
    * file_types (array[integer]): 文件类型列表
    * target_volume_id (string): 目标数据卷 ID
    * target_volume_name (string): 目标数据卷名称
    * process_mode (object `ProcessModeConfig`): 处理模式配置
    * priority (integer): 优先级
    * status (integer): 状态
    * version (string, nullable): 版本号
    * branch_total (integer, nullable): 该工作流下的分支总数
    * branch_id (string, nullable): (通常是) 主分支或最新活动分支的 ID
    * branch_name (string, nullable): (通常是) 主分支或最新活动分支的名称
    * branch_status (integer, nullable): (通常是) 主分支或最新活动分支的状态
    * branch_volume_id (string, nullable): (通常是) 主分支或最新活动分支的目标数据卷 ID

### 查看工作流详情

```
GET /byoa/api/v1/workflow_meta/{workflow_id}
```

**路径参数：**

| 参数名        | 类型   | 是否必填 | 描述     |
| ------------- | ------ | -------- | -------- |
| **workflow_id** | string | 是       | 工作流 ID |

**示例 (Python)：**

```python
import requests
import json

workflow_to_get = "YOUR_WORKFLOW_ID"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/{workflow_to_get}"
headers = {
    "moi-key": "xxxxx"
}
response = requests.get(url, headers=headers)

print(response.status_code)
print(json.dumps(response.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "id": "YOUR_WORKFLOW_ID",
        "name": "Detailed Workflow Test",
        "source_volume_ids": ["YOUR_SOURCE_VOLUME_ID_1"],
        "source_volume_names": ["b-vol1"],
        "target_volume_id": "YOUR_TARGET_VOLUME_ID_W", 
        "target_volume_name": "a-vol2",
        "file_types": [2],
        "process_mode": {"interval": 5, "offset": 0},
        "priority": 300,
        "created_at": 1739435482000,
        "creator": "YOUR_USERNAME",
        "updated_at": 1739436347000,
        "modifier": "YOUR_USERNAME",
        "status": 1
        "workflow": {
            "components": [ /* ... */ ],
            "connections": [ /* ... */ ],
            "edges": [],
            "extra_components": []
        },
        "branch_id": "YOUR_MAIN_BRANCH_ID", 
        "branch_name": "main",                    
        "branch_status": 0,                       
        "branch_volume_id": "YOUR_MAIN_BRANCH_TARGET_VOLUME_ID", 
        "version": "1.2",
        "branches": [
            {
                "branch_id": "YOUR_MAIN_BRANCH_ID",
                "created_at": 1739435482000,
                "creator": "YOUR_USERNAME",
                "updated_at": 1739436347000,
                "modifier": "YOUR_USERNAME",
                "status": 1
                "workflow": { /* YOUR_MAIN_BRANCH_ID 分支的特定 Haystack 配置 */ },
                "branch_name": "main",
                "branch_status": 0
                "branch_volume_id": "YOUR_MAIN_BRANCH_TARGET_VOLUME_ID"
            },
            {
                "branch_id": "YOUR_DEV_BRANCH_ID",
                "created_at": 1739500000000,
                "creator": "YOUR_DEVELOPER_USERNAME",
                "updated_at": 1739501000000,
                "modifier": "YOUR_DEVELOPER_USERNAME",
                "status": 1,
                "workflow": { /* YOUR_DEV_BRANCH_ID 分支的特定 Haystack 配置 */ },
                "branch_name": "dev-feature-x",
                "branch_status": 0,
                "branch_volume_id": "YOUR_DEV_BRANCH_TARGET_VOLUME_ID"
            }
        ]
    }
}
```

**输出参数：**
主要包含工作流的基础信息、主工作流的 Haystack 配置 (**workflow**)、主/默认分支的相关信息 (**branch_id**, **branch_name**, **branch_status**, **branch_volume_id**)，以及一个 **branches** 数组，其中每一项是 **WorkflowBranchItem**。

* **`WorkflowBranchItem` 结构:**
    * branch_id (string): 分支 ID
    * created_at (integer): 创建时间戳
    * creator (string): 创建者
    * updated_at (integer): 更新时间戳
    * modifier (string): 更新者
    * status (integer): 此分支应用的工作流部分的状态
    * workflow (object `WorkflowConfig`): 此分支特定的 Haystack 配置
    * branch_name (string): 分支名
    * branch_status (integer): 分支自身的状态
    * branch_volume_id (string): 分支的目标数据卷 ID

### 修改工作流基础信息

```
PUT /byoa/api/v1/workflow_meta/{workflow_id}/base_info
```

**描述：**更新指定工作流的配置。这通常会更新工作流的 "main" 或默认分支。

**路径参数：**

| 参数名        | 类型   | 是否必填 | 描述     |
| ------------- | ------ | -------- | -------- |
| **workflow_id** | string | 是       | 工作流 ID |

**Body 输入参数：**
与 "创建工作流" 的 Body 结构相同。所有字段都可以更新。

**示例 (Python)：**

```python
import requests
import json

workflow_to_update = "YOUR_WORKFLOW_ID"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/{workflow_to_update}/base_info"
headers = {
    "moi-key": "xxxxx"
}

body = { # WorkflowRequest 结构
    "name": "wf-3-updated-name",
    "source_volume_names": ["b-vol1-updated"],
    "source_volume_ids": ["YOUR_SOURCE_VOLUME_ID_1"], 
    "target_volume_id": "YOUR_TARGET_VOLUME_ID_W", 
    "create_target_volume_name": "", 
        "process_mode": {
        "interval": 10, // 更新处理间隔为10分钟
            "offset": 0
        },
    "file_types": [2, 6],
    "priority": 350,      // 更新优先级
        "workflow": {
        // 更新后的 Haystack 配置
            "components": [
                {
                    "name": "DocumentCleaner",
                    "type": "haystack.components.preprocessors.document_cleaner.DocumentCleaner",
                "component_id": "YOUR_COMPONENT_ID_UPDATED",
                "intro": "Updated DocumentCleaner",
                "position": {"x": 0, "y": 0},
                "input_keys": {}, "output_keys": {},
                    "init_parameters": {
                    "remove_empty_lines": False,
                    "remove_extra_whitespaces": True
                }
            }
            // ... 其他组件和连接
        ],
        "connections": [ /* ... */ ],
        "edges": [],
        "extra_components": []
    }
}

response = requests.put(url, json=body, headers=headers)
print(response.status_code)
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

### 删除工作流

```
DELETE /byoa/api/v1/workflow_meta/{workflow_id}
```

**描述：**删除指定的工作流及其所有分支和关联的作业元数据。

**路径参数：**

| 参数名        | 类型   | 是否必填 | 描述     |
| ------------- | ------ | -------- | -------- |
| **workflow_id** | string | 是       | 工作流 ID |

**Query 参数：**

| 参数名        | 类型    | 是否必填 | 描述                           | 默认值 |
| ------------- | ------- | -------- | ------------------------------ | ------ |
| **delete_data** | boolean | 否       | 是否删除该工作流产生的所有数据 | false  |

**示例 (Python)：**

```python
import requests
import json

workflow_to_delete = "YOUR_WORKFLOW_ID_TO_DELETE" # 替换为实际的 workflow_id
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/{workflow_to_delete}"

headers = {
    "moi-key": "xxxxx"
}
params = {
    "delete_data": True
}

response = requests.delete(url, headers=headers, params=params)

print(response.status_code)
if response.content: 
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Response text:", response.text)
else:
    print("Request successful, no content returned.")

```

**返回：**
成功时通常返回此结构，或 HTTP 204 No Content。

```json
{
    "code": "ok",
    "msg": "ok",
    "data": null
}
```

### 停止工作流

```
PUT /byoa/api/v1/workflow_meta/{workflow_id}/stop
```

**描述：**停止指定工作流的运行。这通常会将工作流的状态更改为 "已停止" 或类似状态，并可能停止所有关联的正在进行的作业。

**路径参数：**

| 参数名        | 类型   | 是否必填 | 描述     |
| ------------- | ------ | -------- | -------- |
| **workflow_id** | string | 是       | 工作流 ID |

**示例 (Python)：**

```python
import requests
import json

workflow_to_stop = "your_workflow_id_to_stop"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/{workflow_to_stop}/stop"

headers = {
    "moi-key": "xxxxx"
}

response = requests.put(url, headers=headers)

print(response.status_code)
if response.content:
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Response text:", response.text)
```

**返回：**
成功时通常返回此结构，表示操作已接受。

```json
{
    "code": "ok",
    "msg": "ok",
    "data": null
}
```

### 工作流分支

#### 创建工作流分支

```
POST /byoa/api/v1/workflow_meta/{workflow_id}/branch
```

**描述：**为指定的工作流创建一个新的分支。

**路径参数：**

| 参数名        | 类型   | 是否必填 | 描述     |
| ------------- | ------ | -------- | -------- |
| **workflow_id** | string | 是       | 工作流 ID |

**Body 输入参数：**

| 参数名        | 是否必填 | 类型                      | 含义       | 默认值 |
| ------------- | -------- | ------------------------- | ---------- | ------ |
| **branch_name** | 否       | string, nullable          | 新的分支名     | ""     |
| **workflow**    | 是       | object | 新的工作流配置 |        |

**示例 (Python)：**

```python
import requests
import json

workflow_id_for_branch = "your_workflow_id"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/{workflow_id_for_branch}/branch"

headers = {
    "moi-key": "xxxxx"
}

body = {
    "branch_name": "feature-branch-alpha",
    "workflow": {
        // ... (与主工作流类似的 Haystack Pipeline 配置, 但可能针对分支有所调整)
        "components": [],
        "connections": [],
        "edges": [],
        "extra_components": []
    }
}

response = requests.post(url, json=body, headers=headers)
print(response.status_code)
if response.content:
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(response.text)
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": null
}
```

#### 查看工作流分支列表

```
GET /byoa/api/v1/workflow_meta/{workflow_id}/branch
```

**描述：**获取指定工作流下的所有分支列表。

**路径参数：**

| 参数名        | 类型   | 是否必填 | 描述     |
| ------------- | ------ | -------- | -------- |
| **workflow_id** | string | 是       | 工作流 ID |

**Query 参数：**

| 参数名          | 类型                     | 是否必填 | 描述                                    |
| --------------- | ------------------------ | -------- | --------------------------------------- |
| **status_in**     | array[integer], nullable | 否       | 工作流状态 (分支应用的工作流部分的状态) |

**示例 (Python)：**

```python
import requests
import json

workflow_id_for_branches = "your_workflow_id"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/{workflow_id_for_branches}/branch"

headers = {
    "moi-key": "xxxxx"
}
params = {}

response = requests.get(url, headers=headers, params=params)
print(response.status_code)
if response.content:
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(response.text)
```

**返回：**
返回结构与 "查看工作流列表" (**GET /byoa/api/v1/workflow_meta**) 类似，其中 **data.workflows** 数组的每一项是 **WorkflowListItem**，但此处代表的是该工作流下的各个分支的信息。请参考 **WorkflowListItem** 结构。

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "total": 2
        "workflows": [
            {
                "id": "workflow_id_for_branch_1",
                "name": "Parent Workflow Name - Branch Alpha"
                "branch_id": "branch_uuid_alpha",
                "branch_name": "alpha-feature",
                "branch_status": 0
                "branch_volume_id": "target_vol_for_alpha_branch"

            },
            {
                "id": "workflow_id_for_branch_1",
                "name": "Parent Workflow Name - Branch Beta",
                "branch_id": "branch_uuid_beta",
                "branch_name": "beta-experiment",
                "branch_status": 1,
                "branch_volume_id": "target_vol_for_beta_branch"
            }
        ]
    }
}
```

**输出参数：**
(具体字段参考 `GET /byoa/api/v1/workflow_meta` 的 `WorkflowListItem` 定义，此处 id 是父工作流 ID, `branch_id`, `branch_name`, `branch_status` 等描述分支特有属性)

#### 获取工作流分支详情

```
GET /byoa/api/v1/workflow_meta/branch/{branch_id}
```

**描述：**获取特定工作流分支的详细信息。

**路径参数：**

| 参数名      | 类型   | 是否必填 | 描述         |
| ----------- | ------ | -------- | ------------ |
| **branch_id** | string | 是       | 工作流分支 ID |

**示例 (Python)：**

```python
import requests
import json

branch_to_get = "your_branch_id"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/branch/{branch_to_get}"
headers = {
    "moi-key": "xxxxx"
}
response = requests.get(url, headers=headers)
print(response.status_code)
if response.content:
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(response.text)
```

**返回：**
返回结构与 "查看工作流详情" (**GET /byoa/api/v1/workflow_meta/{workflow_id}**) 类似，但 **data** 部分描述的是该分支的详情。

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
                  "id": "parent_workflow_uuid"
                  "name": "Parent Workflow Name (Branch: feature-x)",
                  "workflow": {},
        "branch_id": "your_branch_id",       // 当前分支 ID
        "branch_name": "feature-x",          // 当前分支名称
        "branch_status": 0,                  // 当前分支状态
        "branch_volume_id": "target_vol_for_feature_x_branch", // 当前分支目标卷
                  "branches": null
    }
}
```

**输出参数：**
(参考 `GET /byoa/api/v1/workflow_meta/{workflow_id}` 的 `WorkflowDetailResponse` 定义，其中 id 为父工作流 ID，`workflow` 为此分支的配置，`branch_id`, `branch_name` 等为当前分支信息)

#### 更新工作流分支

```
PUT /byoa/api/v1/workflow_meta/branch/{branch_id}
```

**描述：**更新指定工作流分支的配置。

**路径参数：**

| 参数名      | 类型   | 是否必填 | 描述         |
| ----------- | ------ | -------- | ------------ |
| **branch_id** | string | 是       | 工作流分支 ID |

**Body 输入参数：**

| 参数名        | 是否必填 | 类型                      | 含义           | 默认值 |
| ------------- | -------- | ------------------------- | -------------- | ------ |
| **branch_name** | 否       | string, nullable          | 新的分支名     | ""     |
| **workflow**    | 是       | object | 新的工作流配置 |        |

**示例 (Python)：**

```python
import requests
import json

branch_to_update = "your_branch_id_to_update"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/branch/{branch_to_update}"
headers = {
    "moi-key": "xxxxx"
}
body = {
    "branch_name": "feature-branch-alpha-v2",
    "workflow": {
        // ... (更新后的 Haystack Pipeline 配置)
        "components": [],
        "connections": []
    }
}
response = requests.put(url, json=body, headers=headers)
print(response.status_code)
if response.content:
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(response.text)
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": null
}
```

#### 删除工作流分支

```
DELETE /byoa/api/v1/workflow_meta/branch/{branch_id}
```

**描述：**删除指定的工作流分支。

**路径参数：**

| 参数名      | 类型   | 是否必填 | 描述         |
| ----------- | ------ | -------- | ------------ |
| **branch_id** | string | 是       | 工作流分支 ID |

**Query 参数：**

| 参数名        | 类型    | 是否必填 | 描述                         | 默认值 |
| ------------- | ------- | -------- | ---------------------------- | ------ |
| **delete_data** | boolean | 否       | 是否删除该分支产生的所有数据 | false  |

**示例 (Python)：**

```python
import requests
import json

branch_to_delete = "your_branch_id_to_delete"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/branch/{branch_to_delete}"
headers = {
    "moi-key": "xxxxx"
}
params = {
    "delete_data": False # 或 True
}
response = requests.delete(url, headers=headers, params=params)
print(response.status_code)
if response.content and response.text.strip():
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(f"Response Text: {response.text}")
else:
    print("Request successful, no content returned or empty response.")
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": null
}
```

## 作业

### 查看作业列表

```
GET /byoa/api/v1/workflow_job
```

**描述：**获取符合条件的工作流作业列表。

**Query 参数：**

| 参数名          | 类型                                  | 是否必填 | 描述                          | 默认值 |
| --------------- | ------------------------------------- | -------- | ----------------------------- | ------ |
| **workflow_id**   | string, nullable                      | 否       | 工作流 ID                     |        |
| **name_search**   | string, nullable                      | 否       | 名称搜索 (工作流名称)             |        |
| **file_types**    | array[integer], nullable              | 否       | 文件类型                      |        |
| **priority**      | array[integer], nullable              | 否       | 优先级                        |        |
| **page_num**      | integer, >=1                          | 否       | 页码                          | 1      |
| **page_size**     | integer, >=1                          | 否       | 每页大小                      | 10     |
| **count_le**      | integer, nullable                     | 否       | 小于等于的文件数量            |        |
| **count_ge**      | integer, nullable                     | 否       | 大于等于的文件数量            |        |
| **sort_field**    | string, nullable                      | 否       | 排序字段（未设置时按创建时间降序） |        |
| **sort_order**    | string, nullable                      | 否       | 排序方式（asc/desc）          | asc    |

**示例 (Python)：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_job"
headers = {"moi-key": "xxxxx"}
params = {"page_num": 1, "page_size": 10, "sort_order": "asc"}
resp = requests.get(url, headers=headers, params=params)
print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "total": 20,
        "jobs": [
            {
                "id": "job_uuid_1",
                "name": "Alpha Job",
                "created_at": 1739377287000,
                "creator": "admin_user",
                "updated_at": 1739377755000,
                "modifier": "admin_user",
                "status": 2,
                "version": "1.0",
                "workflow_meta_id": "ff5d119a-4e94-4968-ac0c-6ef64fcabb6c",
                "workflow_branch_id": "main"
            }
        ]
    }
}
```

**输出参数：**

| 参数    | 类型                               | 描述                                       |
| ------- | ---------------------------------- | ------------------------------------------ |
| **total** | integer                            | 符合条件的工作流作业总数                   |
| **jobs**  | array[object] | 作业列表，每个对象包含作业及其主要分支信息 |

* **`JobListItem` 对象结构:**
    * id (string): 作业 ID
    * name (string): 作业名称
    * created_at (integer): 创建时间戳 (毫秒)
    * creator (string): 创建者
    * updated_at (integer): 更新时间戳 (毫秒)
    * modifier (string, nullable): 更新者
    * status (integer): 状态
    * version (string, nullable): 版本号
    * workflow_meta_id (string): 工作流元数据 ID
    * workflow_branch_id (string): 工作流分支 ID

### 查看作业详情

```
GET /byoa/api/v1/workflow_job/{job_id}
```

**描述：**获取指定作业的详细信息。

**路径参数：**

| 参数名   | 类型   | 是否必填 | 描述   |
| -------- | ------ | -------- | ------ |
| **job_id** | string | 是       | 作业 ID |

**示例 (Python)：**

```python
import requests
import json

job_to_get = "YOUR_JOB_ID"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_job/{job_to_get}"
headers = {
    "moi-key": "xxxxx"
}
response = requests.get(url, headers=headers)

print(response.status_code)
print(json.dumps(response.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "created_at": "2025-05-30T09:45:58",
        "id": "cf68d259-9cd6-4f44-a0a4-5674c79da083",
        "user_id": "01960e07-60ec-7a3c-b45f-415b7e40e8bf",
        "flow_interval": 0,
        "creator": "admin",
        "file_types": "[1, 2, 4, 5, 6, 7, 11, 12]",
        "target_volume_id": "04614636-b858-4b13-99bf-a036d9351289",
        "files": "[]",
        "updated_at": "2025-05-30T09:45:58",
        "version": "1",
        "priority": 300,
        "name": "test",
        "group_id": "",
        "flow_offset": 0,
        "modifier": "admin",
        "source_volume_ids": "[\"1928383194482323456\"]",
        "source_volume_names": "[\"b_vol3\"]",
        "target_volume_name": "b_vol3"
    }
}
```

**输出参数：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "created_at": "2025-05-30T09:45:58",
        "id": "cf68d259-9cd6-4f44-a0a4-5674c79da083",
        "user_id": "01960e07-60ec-7a3c-b45f-415b7e40e8bf",
        "flow_interval": 0,
        "creator": "admin",
        "file_types": "[1, 2, 4, 5, 6, 7, 11, 12]",
        "target_volume_id": "04614636-b858-4b13-99bf-a036d9351289",
        "files": "[]",
        "updated_at": "2025-05-30T09:45:58",
        "version": "1",
        "priority": 300,
        "name": "test",
        "group_id": "",
        "flow_offset": 0,
        "modifier": "admin",
        "source_volume_ids": "[\"1928383194482323456\"]",
        "source_volume_names": "[\"b_vol3\"]",
        "target_volume_name": "b_vol3"
    }
}
```

### 查看作业文件列表

```
GET /byoa/api/v1/workflow_job/{job_id}/files
```

**描述：**获取作业关联的文件列表

**路径参数：**

| 参数名   | 类型   | 是否必填 | 描述   |
| -------- | ------ | -------- | ------ |
| **job_id** | string | 是       | 作业 ID |

**Query 参数：**

| 参数名       | 类型                     | 是否必填 | 描述       | 默认值 |
| ------------ | ------------------------ | -------- | ---------- | ------ |
| **page_num**   | integer, >=1             | 否       | 页码       | 1      |
| **page_size**  | integer, >=1             | 否       | 每页大小   | 10     |
| **statuses**   | array[integer], nullable | 否       | 文件状态筛选 | []     |

**示例 (Python)：**

```python
import requests, json
job_id_for_files = "your_job_id"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_job/{job_id_for_files}/files"
headers = {"moi-key": "xxxxx"}
params = {"page_num": 1, "page_size": 10, "statuses": [2,3]}
resp = requests.get(url, headers=headers, params=params)
print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "files": [
            {
                "id": "file_uuid_1",
                "file_name": "document_part_1.pdf",
                "file_type": 2,
                "file_status": 3,
                "error_message": null,
                "start_time": "2025-01-15T10:30:00",
                "end_time": "2025-01-15T10:35:00",
                "source_id": "source_file_123",
                "ref_file_id": "ref_123",
                "target_volume_id": "target_volume_uuid"
            }
        ],
        "file_total": 5,
        "total": 10,
        "completed": 5,
        "failed": 1,
        "processing": 2,
        "pending": 2,
        "stopped": 0
    }
}
```

**输出参数：**

| 参数          | 类型                  | 描述                   |
| ------------- | --------------------- | ---------------------- |
| **files**     | array[object]         | 文件列表               |
| **file_total** | integer               | 总文件数 (过滤后的)     |
| **total**     | integer               | 总数                   |
| **completed** | integer               | 已完成                 |
| **failed**    | integer               | 失败                   |
| **processing** | integer               | 处理中                 |
| **pending**   | integer               | 待处理                 |
| **stopped**   | integer               | 已停止                 |

* **`FileInfo` 对象结构:**
    * id (string): 文件 ID
    * file_name (string): 文件名
    * file_type (integer): 文件类型
    * file_status (integer): 文件状态
    * error_message (string, nullable): 错误信息
    * start_time (string): 开始处理时间
    * end_time (string): 结束处理时间
    * source_id (string, nullable): 源文件 ID
    * ref_file_id (string, nullable): 原生的 file_id
    * target_volume_id (string, nullable): 目标卷 ID，可用于 raw 下载接口

### 重试处理作业文件

```
POST /byoa/api/v1/workflow_job/{job_id}/files
```

**描述：**重试处理指定作业下的文件列表。

**路径参数：**

| 参数名   | 类型   | 是否必填 | 描述   |
| -------- | ------ | -------- | ------ |
| **job_id** | string | 是       | 作业 ID |

**Body 输入参数：**

| 参数名    | 是否必填 | 类型            | 描述                         |
| --------- | -------- | --------------- | ---------------------------- |
| **files** | 是       | array[string]   | 需要重试的文件 ID 列表（`JobFileItem.id`） |

**示例 (Python)：**

```python
import requests, json
job_id_for_retry = "your_job_id"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_job/{job_id_for_retry}/files"
headers = {"moi-key": "xxxxx"}
body = {"files": ["file_item_uuid_1", "file_item_uuid_2"]}
resp = requests.post(url, headers=headers, json=body)
print(resp.status_code)
if resp.content and resp.text.strip():
    print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
  "data": null
}
```

### 获取作业状态

```
GET /byoa/api/v1/workflow_job/{job_id}/status
```

**描述：**获取指定作业的当前状态。

**路径参数：**

| 参数名   | 类型   | 是否必填 | 描述   |
| -------- | ------ | -------- | ------ |
| **job_id** | string | 是       | 作业 ID |

**示例 (Python)：**

```python
import requests
import json

job_id_for_status = "your_job_id"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_job/{job_id_for_status}/status"

headers = {
    "moi-key": "xxxxx"
}

response = requests.get(url, headers=headers)

print(response.status_code)
if response.content:
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(response.text)
```

**返回：**

```json
{
    "code": "ok",
    "msg": "ok",
    "data": {
        "job_id": "your_job_id",
        "status": 2,
        "message": "Job completed successfully.",
        "progress": 100,
        "start_time": 1739377287000,
        "end_time": 1739377755000
    }
}
```

**输出参数：**

| 参数         | 类型              | 描述                                                         |
| ------------ | ----------------- | ------------------------------------------------------------ |
| **job_id**     | string            | 作业 ID                                                       |
| **status**     | integer           | 作业的当前状态 |
| **message**    | string, nullable  | 状态相关的附加信息                                           |
| **progress**   | integer, nullable | 作业进度 (0-100)                                             |
| **start_time** | integer, nullable | 作业开始时间戳 (毫秒)                                        |
| **end_time**   | integer, nullable | 作业结束时间戳 (毫秒)                                        |

### 重新运行工作流

```
PUT /byoa/api/v1/workflow_meta/{workflow_id}/rerun
```

**描述：**重新运行指定工作流。

**路径参数：**

| 参数名        | 类型   | 是否必填 | 描述     |
| ------------- | ------ | -------- | -------- |
| **workflow_id** | string | 是       | 工作流 ID |

**示例 (Python)：**

```python
import requests
workflow_to_rerun = "YOUR_WORKFLOW_ID"
url = f"https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/byoa/api/v1/workflow_meta/{workflow_to_rerun}/rerun"
headers = {"moi-key": "xxxxx"}
resp = requests.put(url, headers=headers)
print(resp.status_code)
print(resp.json() if resp.content else "OK")
```
