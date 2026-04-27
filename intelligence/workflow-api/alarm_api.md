# 告警相关 API

## 通知对象

### 创建通知对象

用途：新增一个用于接收告警的联系人。

```
POST /alerting/receiver
```

**输入参数：**

| 参数             | 是否必填 | 含义                                                      |
| --------------- | ------- | --------------------------------------------------------- |
| group_id        | 是      | 工作区 ID（workspace_id）                                   |
| name            | 是      | 接收者名称                                                 |
| notify_type     | 是      | 通知类型：0-邮件，1-短信，2-电话语音，3-企业微信                   |
| status          | 是      | 状态：0-禁用，1-启用                                        |
| email           | 否      | 邮箱地址（notify_type 为 0 时必填）                         |
| phone           | 否      | 电话号码（notify_type 为 1 或 2 时必填）                     |
| wecom_key       | 否      | 企业微信机器人密钥（notify_type 为 3 时必填）                 |
| comment         | 否      | 备注                                                      |

**输出参数：**

| 参数       | 含义        |
| ---------- | ----------- |
| id         | 接收者 ID     |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/receiver"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "group_id": "YOUR_WORKSPACE_ID",
    "name": "邮件接收者",
    "notify_type": 0,
    "status": 1,
    "email": "user@example.com",
    "comment": "用于接收告警邮件"
}

response = requests.post(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

返回：

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "id": "receiver_id_12345"
    },
    "request_id": "req_12345"
}
```

### 获取单个通知对象详情

用途：根据接收者 ID 查询详细信息。

```
GET /alerting/receiver?id={receiver_id}
```

**输入参数：**

| 参数 | 是否必填 | 含义     |
| ---- | ------- | -------- |
| id   | 是      | 接收者 ID  |

**输出参数：**

| 参数         | 含义                                                      |
| ------------ | --------------------------------------------------------- |
| id           | 接收者 ID                                                   |
| name         | 接收者名称                                                 |
| notify_type  | 通知类型：0-邮件，1-短信，2-电话语音，3-企业微信                   |
| status       | 状态：0-禁用，1-启用                                        |
| email        | 邮箱地址                                                   |
| phone        | 电话号码                                                   |
| wecom_key    | 企业微信机器人密钥                                         |
| comment      | 备注                                                      |
| org_id       | 组织 ID                                                     |
| workspace_id | 工作区 ID                                                   |
| created_at   | 创建时间（时间戳）                                         |
| updated_at   | 更新时间（时间戳）                                         |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/receiver"
headers = {
    "Accept": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

params = {
    "id": "receiver_id_12345"
}

response = requests.get(url, headers=headers, params=params)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

返回：

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "id": "receiver_id_12345",
        "name": "邮件接收者",
        "notify_type": 0,
        "status": 1,
        "email": "user@example.com",
        "phone": "",
        "wecom_key": "",
        "comment": "用于接收告警邮件",
        "org_id": "org_12345",
        "workspace_id": "workspace_12345",
        "created_at": 1640995200,
        "updated_at": 1640995200
    },
    "request_id": "req_12345"
}
```

### 获取通知对象列表

用途：按条件分页查询接收者。

```
POST /alerting/receiver/list
```

**输入参数：**

| 参数             | 是否必填 | 含义                                                      |
| --------------- | ------- | --------------------------------------------------------- |
| page            | 是      | 页码，从 1 开始                                            |
| page_size       | 是      | 每页大小                                                   |
| receiver_filter | 否      | 过滤条件                                                   |

**receiver_filter 参数：**

| 参数               | 是否必填 | 含义                                                      |
| ----------------- | ------- | --------------------------------------------------------- |
| group_ids         | 否      | 工作区 ID 列表（workspace_id 数组）                           |
| ids               | 否      | 接收者 ID 列表，用于精确查询指定的接收者                      |
| name_keyword      | 否      | 名称关键词，模糊匹配接收者名称                               |
| email_keyword     | 否      | 邮箱关键词，模糊匹配邮箱地址                                |
| phone_keyword     | 否      | 电话关键词，模糊匹配电话号码                                |
| notify_types      | 否      | 通知类型列表：0-邮件，1-短信，2-电话语音，3-企业微信              |
| statuses          | 否      | 状态列表：0-禁用，1-启用                                    |
| search_keyword    | 否      | 搜索关键词，全局搜索接收者信息                               |
| create_time_order | 否      | 创建时间排序：asc（升序）/desc（降序）                      |
| update_time_order | 否      | 更新时间排序：asc（升序）/desc（降序）                      |

**输出参数：**

| 参数       | 含义                                                      |
| ---------- | --------------------------------------------------------- |
| receivers  | 接收者列表，每个元素包含接收者的详细信息                      |
| total      | 符合条件的接收者总数                                        |

**receivers 数组元素结构：**

| 参数         | 含义                                                      |
| ------------ | --------------------------------------------------------- |
| id           | 接收者 ID                                                   |
| name         | 接收者名称                                                 |
| notify_type  | 通知类型：0-邮件，1-短信，2-电话语音，3-企业微信                   |
| status       | 状态：0-禁用，1-启用                                        |
| email        | 邮箱地址                                                   |
| phone        | 电话号码                                                   |
| wecom_key    | 企业微信机器人密钥                                         |
| comment      | 备注                                                      |
| org_id       | 组织 ID                                                     |
| workspace_id | 工作区 ID                                                   |
| created_at   | 创建时间（时间戳）                                         |
| updated_at   | 更新时间（时间戳）                                         |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/receiver/list"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "page": 1,
    "page_size": 10,
    "receiver_filter": {
        "group_ids": ["YOUR_WORKSPACE_ID"],
        "statuses": [1]
    }
}

response = requests.post(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

返回：

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "receivers": [
            {
                "id": "receiver_id_12345",
                "name": "邮件接收者",
                "notify_type": 0,
                "status": 1,
                "email": "user1@example.com",
                "phone": "",
                "wecom_key": "",
                "comment": "用于接收告警邮件",
                "org_id": "org_12345",
                "workspace_id": "workspace_12345",
                "created_at": 1640995200,
                "updated_at": 1640995200
            },
            {
                "id": "receiver_id_67890",
                "name": "企业微信接收者",
                "notify_type": 3,
                "status": 1,
                "email": "",
                "phone": "",
                "wecom_key": "wecom_bot_key_12345",
                "comment": "企业微信群告警通知",
                "org_id": "org_12345",
                "workspace_id": "workspace_12345",
                "created_at": 1640995260,
                "updated_at": 1640995260
            }
        ],
        "total": 15
    },
    "request_id": "req_12345"
}
```

**错误响应：**

400 参数错误：

```json
{
    "code": "INVALID_ARGUMENT",
    "msg": "参数错误：page 必须大于 0",
    "request_id": "req_12345"
}
```

500 服务器内部错误：

```json
{
    "code": "INTERNAL_ERROR",
    "msg": "服务器内部错误",
    "request_id": "req_12345"
}
```

### 更新通知对象

用途：更新指定 ID 的接收者信息。

```
PUT /alerting/receiver
```

**输入参数：**

| 参数         | 是否必填 | 含义                                                      |
| ------------ | ------- | --------------------------------------------------------- |
| id           | 是      | 接收者 ID                                                   |
| name         | 否      | 接收者名称                                                 |
| notify_type  | 否      | 通知类型：0-邮件，1-短信，2-电话语音，3-企业微信                   |
| status       | 否      | 状态：0-禁用，1-启用                                        |
| email        | 否      | 邮箱地址                                                   |
| phone        | 否      | 电话号码                                                   |
| wecom_key    | 否      | 企业微信机器人密钥                                         |
| comment      | 否      | 备注                                                      |

**输出参数：**

| 参数 | 含义     |
| ---- | -------- |
| id   | 接收者 ID |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/receiver"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "id": "receiver_id_12345",
    "name": "更新后的接收者名称",
    "status": 1,
    "comment": "更新后的备注"
}

response = requests.put(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

### 删除通知对象

用途：删除指定 ID 的接收者，并同步更新相关告警规则。

```
DELETE /alerting/receiver
```

**输入参数：**

| 参数 | 是否必填 | 含义     |
| ---- | ------- | -------- |
| id   | 是      | 接收者 ID |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/receiver"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "id": "receiver_id_12345"
}

response = requests.delete(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

## 告警规则

### 创建告警规则

```
POST /alerting/workspace/alert/rule/create
```

**Header 参数：**

| 参数名         | 类型   | 是否必填 | 描述                        |
| -------------- | ------ | -------- | --------------------------- |
| `moi-key`      | string | 是       | MOI API 密钥                |

**输入参数：**

| 参数             | 是否必填 | 含义                                                      |
| --------------- | ------- | --------------------------------------------------------- |
| workspace_id    | 是      | 工作区 ID（工作区模式下必填）                                 |
| expression_id   | 是      | 表达式 ID                                                   |
| category        | 是      | 类别：0-metric（数据处理），1-event（数据加载）                       |
| level           | 是      | 告警级别                                                   |
| args            | 否      | 参数列表                                                   |
| receivers       | 否      | 接收者 ID 列表                                               |
| repeat_interval | 否      | 重复间隔                                                   |
| silence_rule    | 否      | 静默规则                                                   |

**输出参数：**

| 参数     | 含义     |
| -------- | -------- |
| alert_id | 告警 ID   |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/workspace/alert/rule/create"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "workspace_id": "YOUR_WORKSPACE_ID",
    "expression_id": "expr_12345",
    "category": 1,  # 1-event（事件），0-metric（指标）
    "level": "critical",
    "args": [
        {
            "key": "threshold",
            "value": "80"
        }
    ],
    "receivers": ["receiver_id_12345"],
    "repeat_interval": 300,
    "silence_rule": {
        "enabled": false
    }
}

response = requests.post(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

### 获取告警规则列表

```
POST /alerting/workspace/alert/rule/list
```

**Header 参数：**

| 参数名         | 类型   | 是否必填 | 描述                        |
| -------------- | ------ | -------- | --------------------------- |
| `moi-key`      | string | 是       | MOI API 密钥                |

**输入参数：**

| 参数     | 是否必填 | 含义                                                      |
| -------- | ------- | --------------------------------------------------------- |
| filters  | 否      | 过滤条件，用于筛选告警规则                                 |
| limit    | 否      | 限制返回的告警数量                                         |
| offset   | 否      | 偏移量，用于分页查询                                       |
| sorter   | 否      | 排序条件，指定结果排序方式                                 |

**filters 参数：**

| 参数         | 是否必填 | 含义                                                      |
| ------------ | ------- | --------------------------------------------------------- |
| workspace_id | 否      | 工作区 ID，用于筛选指定工作区的告警规则                      |
| org_id       | 否      | 组织 ID，用于筛选指定组织的告警规则                          |
| org_id_list  | 否      | 组织 ID 列表，用于批量筛选多个组织的告警规则                  |
| rule_id      | 否      | 规则 ID，用于精确查询指定的告警规则                          |
| alert_types  | 否      | 告警类型列表，用于筛选指定类型的告警                         |
| levels       | 否      | 告警级别列表，用于筛选指定级别的告警                         |
| states       | 否      | 告警状态列表，用于筛选指定状态的告警                         |
| enable       | 否      | 启用状态列表，用于筛选启用/禁用的告警规则                    |
| contact_id   | 否      | 联系人 ID，用于筛选指定联系人的告警规则                      |
| expression   | 否      | 表达式关键词，用于模糊匹配告警表达式                         |
| notify_types | 否      | 通知类型列表，用于筛选指定通知方式的告警                     |
| intervals    | 否      | 时间间隔列表，用于筛选指定间隔的告警                         |

**sorter 参数：**

| 参数     | 是否必填 | 含义                                                      |
| -------- | ------- | --------------------------------------------------------- |
| sort_by  | 否      | 排序字段，如 "created_at"、"updated_at" 等                 |
| is_desc  | 否      | 是否降序排列，true-降序，false-升序                        |

**输出参数：**

| 参数   | 含义                                                      |
| ------ | --------------------------------------------------------- |
| alerts | 告警规则列表，每个元素包含告警规则的详细信息                 |
| total  | 符合条件的告警规则总数                                     |

**alerts 数组元素结构：**

| 参数              | 含义                                                      |
| ----------------- | --------------------------------------------------------- |
| alert_id          | 告警 ID                                                     |
| alert_config      | 告警配置信息                                               |
| complete_expr     | 完整表达式（英文）                                         |
| complete_expr_cn  | 完整表达式（中文）                                         |
| state             | 告警状态                                                   |
| has_new           | 是否有新告警                                               |
| silence_rule      | 静默规则配置                                               |
| org_id            | 组织 ID（工作区模式下为空）                                 |
| workspace_id      | 工作区 ID（组织模式下为空）                                 |
| created_at        | 创建时间                                                   |
| updated_at        | 更新时间                                                   |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/workspace/alert/rule/list"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "filters": {
        "workspace_id": "YOUR_WORKSPACE_ID",
        "levels": ["critical", "warning"],
        "states": ["active"]
    },
    "limit": 10,
    "offset": 0,
    "sorter": {
        "sort_by": "created_at",
        "is_desc": true
    }
}

response = requests.post(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

返回：

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "alerts": [
            {
                "alert_id": "alert_12345",
                "alert_config": {
                    "id": "config_12345",
                    "alert_type": "cpu_usage",
                    "category": 0,
                    "level": "critical",
                    "content": "CPU usage is high",
                    "content_cn": "CPU 使用率过高",
                    "expression": "cpu_usage > 80",
                    "expression_cn": "CPU 使用率 > 80%",
                    "is_default_enable": true
                },
                "complete_expr": "cpu_usage > 80 for 5 minutes",
                "complete_expr_cn": "CPU 使用率 > 80% 持续 5 分钟",
                "state": "active",
                "has_new": true,
                "silence_rule": {
                    "enabled": false,
                    "resume_at": ""
                },
                "org_id": "",
                "workspace_id": "workspace_12345",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            },
            {
                "alert_id": "alert_67890",
                "alert_config": {
                    "id": "config_67890",
                    "alert_type": "memory_usage",
                    "category": 0,
                    "level": "warning",
                    "content": "Memory usage is high",
                    "content_cn": "内存使用率过高",
                    "expression": "memory_usage > 70",
                    "expression_cn": "内存使用率 > 70%",
                    "is_default_enable": true
                },
                "complete_expr": "memory_usage > 70 for 3 minutes",
                "complete_expr_cn": "内存使用率 > 70% 持续 3 分钟",
                "state": "active",
                "has_new": false,
                "silence_rule": {
                    "enabled": false,
                    "resume_at": ""
                },
                "org_id": "",
                "workspace_id": "workspace_12345",
                "created_at": "2024-01-01T11:00:00Z",
                "updated_at": "2024-01-01T11:00:00Z"
            }
        ],
        "total": 25
    },
    "request_id": "req_12345"
}
```

### 更新告警规则

```
POST /alerting/workspace/alert/rule/update
```

**Header 参数：**

| 参数名         | 类型   | 是否必填 | 描述                        |
| -------------- | ------ | -------- | --------------------------- |
| `moi-key`      | string | 是       | MOI API 密钥                |

**输入参数：**

| 参数             | 是否必填 | 含义                                                      |
| --------------- | ------- | --------------------------------------------------------- |
| alert_id        | 是      | 告警 ID                                                     |
| level           | 否      | 告警级别                                                   |
| args            | 否      | 参数列表                                                   |
| receivers       | 否      | 接收者 ID 列表                                               |
| repeat_interval | 否      | 重复间隔                                                   |
| silence_rule    | 否      | 静默规则                                                   |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/workspace/alert/rule/update"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "alert_id": "alert_12345",
    "level": "warning",
    "args": [
        {
            "key": "threshold",
            "value": "90"
        }
    ],
    "receivers": ["receiver_id_12345", "receiver_id_67890"],
    "repeat_interval": 600
}

response = requests.post(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

### 删除告警规则

```
POST /alerting/workspace/alert/rule/delete
```

**Header 参数：**

| 参数名         | 类型   | 是否必填 | 描述                        |
| -------------- | ------ | -------- | --------------------------- |
| `moi-key`      | string | 是       | MOI API 密钥                |

**输入参数：**

| 参数     | 是否必填 | 含义   |
| -------- | ------- | ------ |
| alert_id | 是      | 告警 ID |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/workspace/alert/rule/delete"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "alert_id": "alert_12345"
}

response = requests.post(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

## 告警记录

### 查看告警记录列表

用途：分页查询告警记录历史。

```
POST /alerting/history/list
```

**输入参数：**

| 参数   | 是否必填 | 含义                                                      |
| ------ | ------- | --------------------------------------------------------- |
| page   | 否      | 页数                                                       |
| size   | 否      | 每页显示条数                                               |
| filter | 否      | 过滤条件                                                   |

**filter 参数：**

| 参数             | 是否必填 | 含义                                                      |
| --------------- | ------- | --------------------------------------------------------- |
| group_id        | 否      | 工作区 ID                                                    |
| start           | 否      | 开始时间                                                   |
| end             | 否      | 结束时间                                                   |
| create_at_order | 否      | 告警时间排序                                               |
| search_keyword  | 否      | 查询关键字                                                 |
| severity        | 否      | 告警严重性                                                 |

**输出参数：**

| 参数      | 含义                                                      |
| --------- | --------------------------------------------------------- |
| total     | 告警总数                                                   |
| histories | 告警记录列表，每个元素包含告警记录的详细信息                 |

**histories 数组元素结构：**

| 参数                 | 含义                                                      |
| ------------------- | --------------------------------------------------------- |
| id                  | 告警记录 ID                                                 |
| rule_id             | 告警规则 ID                                                 |
| group_id            | 工作区 ID                                                    |
| rule_template_id    | 表达式 ID                                                   |
| rule_expression     | 告警表达式（英文）                                         |
| rule_expression_cn  | 告警表达式（中文）                                         |
| alert_type          | 告警类别                                                   |
| alert_severity      | 告警严重性                                                 |
| receivers           | 通知对象列表                                               |
| create_at           | 创建时间                                                   |
| is_read             | 是否已读                                                   |

**receivers 数组元素结构：**

| 参数        | 含义                                                      |
| ----------- | --------------------------------------------------------- |
| id          | 通知对象 ID                                                 |
| name        | 通知对象名称                                               |
| notify_type | 通知类型：0-邮件，1-短信，2-电话语音，3-企业微信              |
| email       | 通知对象邮箱                                               |
| phone       | 通知对象电话                                               |
| wecom_key   | 企业微信机器人密钥                                         |

**示例：**

```python
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/alerting/history/list"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "moi-key": "YOUR_MOI_KEY"
}

body = {
    "page": 1,
    "size": 10,
    "filter": {
        "group_id": "YOUR_WORKSPACE_ID",
        "start": "2024-01-01T00:00:00Z",
        "end": "2024-01-31T23:59:59Z",
        "severity": "critical",
        "create_at_order": "desc"
    }
}

response = requests.post(url, headers=headers, json=body)
print("Response:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

返回：

```json
{
    "code": "OK",
    "msg": "OK",
    "data": {
        "total": 25,
        "histories": [
            {
                "id": "history_12345",
                "rule_id": "rule_12345",
                "group_id": "workspace_12345",
                "rule_template_id": "template_12345",
                "rule_expression": "cpu_usage > 80",
                "rule_expression_cn": "CPU 使用率 > 80%",
                "alert_type": "cpu_usage",
                "alert_severity": "critical",
                "receivers": [
                    {
                        "id": "receiver_12345",
                        "name": "运维团队",
                        "notify_type": 0,
                        "email": "ops@example.com",
                        "phone": "",
                        "wecom_key": ""
                    },
                    {
                        "id": "receiver_67890",
                        "name": "企业微信群",
                        "notify_type": 3,
                        "email": "",
                        "phone": "",
                        "wecom_key": "wecom_bot_key_12345"
                    }
                ],
                "create_at": "2024-01-15T10:30:00Z",
                "is_read": false
            },
            {
                "id": "history_67890",
                "rule_id": "rule_67890",
                "group_id": "workspace_12345",
                "rule_template_id": "template_67890",
                "rule_expression": "memory_usage > 90",
                "rule_expression_cn": "内存使用率 > 90%",
                "alert_type": "memory_usage",
                "alert_severity": "warning",
                "receivers": [
                    {
                        "id": "receiver_12345",
                        "name": "运维团队",
                        "notify_type": 0,
                        "email": "ops@example.com",
                        "phone": "",
                        "wecom_key": ""
                    }
                ],
                "create_at": "2024-01-15T09:15:00Z",
                "is_read": true
            }
        ]
    },
    "request_id": "req_12345"
}
```
