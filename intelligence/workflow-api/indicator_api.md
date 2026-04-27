# 指标相关 API

```
POST /metric/observice
```

**数据载入：**

|  指标名称     | 指标名参数                     | 含义               |
| ------------ | ---------------------------- |------------------- |
| 文件完成数量   | PipelineLoadFileCount        |一段时间内成功载入的文件数 |
| 文件载入大小   | PipelineLoadFileSize         |一段时间内成功载入的文件总大小|
| 任务完成数    | PipelineLoadTaskCount         |一段时间内成功完成的任务数|
| 文件载入延迟   | PipelineLoadFileLatency      |一段时间内每个文件从开始载入到载入成功的平均时间 |
| 文件载入吞吐量 | PipelineLoadFileThroughput   |单位时间内成功载入的数据量（字节/s） |
| 每秒载入文件数 | PipelineLoadFilePerSecond    |单位时间内成功处理的文件数（文件数/s）|
| 任务平均延迟 | PipelineLoadTaskLatency        |一段时间内每个任务平均完成时间|
| 文件成功率    | PipelineLoadFileSuccessRate   |一段时间内文件载入的成功率|
| 任务超时率    | PipelineLoadTaskTimeoutRate   |一段时间内载入任务的超时率|

**数据处理：**

|  指标名称     | 指标名参数                             | 含义               |
| ------------ | -----------------------------------  |------------------- |
| 作业完成数量   | PipelineProcessFinishJobCount        |一段时间内执行处理作业数量|
| 作业处理延迟   | PipelineProcessFinishJobLatency      |一段时间内执行处理作业平均耗时 |
| 工作流成功率   | PipelineProcessWorkflowSuccessRate   |一段时间内工作流执行处理作业的成功率 |
| 工作流超时率   |PipelineProcessWorkflowTimeoutRate    |一段时间内工作流执行处理作业的超时率|

**输入参数：**
  
|  参数             | 是否必填 |含义|
|  --------------- | ------- |----  |
| acconut          | 是      | 工作区 id |
| metrics          | 是      | 指标名，可以填写多个 |
| start             | 是      | 统计开始时间 |
| end               | 是      | 统计结束时间 |
| interval          | 是      | 时间间隔，秒 |

**示例：**

```bash
import requests
import json

url = "https://freetier-01.cn-hangzhou.cluster.matrixonecloud.cn/metric/observice"
headers = {
    "moi-key": "xxxxx"
}

body={
  "account": "YOUR_ACCOUNT_ID",
  "start": "2025-02-10T09:40:24+08:00",
  "end": "2025-02-10T10:00:24+08:00",
  "interval": 60,
  "metrics": [
    {
      "name": "PipelineProcessFinishJobCount"
    }
  ]
}

response = requests.post(url, headers=headers,json=body)
print("Response Body:", json.dumps(response.json(), indent=4, ensure_ascii=False))
```

返回：

```
Response Body: {
    "code": "OK",
    "msg": "OK",
    "data": {
        "start": "2025-02-10T01:41:24Z",
        "end": "2025-02-10T02:00:24Z",
        "metrics": [
            {
                "name": "PipelineProcessFinishJobCount",
                "agg": "",
                "labels": [
                    {
                        "labelKey": "user_id",
                        "labelValue": "YOUR_USER_ID"
                    }
                ],
                "values": [
                    {
                        "timestamp": "2025-02-10T01:41:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:42:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:43:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:44:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:45:00Z",
                        "value": 2
                    },
                    {
                        "timestamp": "2025-02-10T01:46:00Z",
                        "value": 2
                    },
                    {
                        "timestamp": "2025-02-10T01:47:00Z",
                        "value": 2
                    },
                    {
                        "timestamp": "2025-02-10T01:48:00Z",
                        "value": 2
                    },
                    {
                        "timestamp": "2025-02-10T01:49:00Z",
                        "value": 2
                    },
                    {
                        "timestamp": "2025-02-10T01:50:00Z",
                        "value": 2
                    },
                    {
                        "timestamp": "2025-02-10T01:51:00Z",
                        "value": 2
                    },
                    {
                        "timestamp": "2025-02-10T01:52:00Z",
                        "value": 2
                    },
                    {
                        "timestamp": "2025-02-10T01:53:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:54:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:55:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:56:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:57:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:58:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T01:59:00Z",
                        "value": null
                    },
                    {
                        "timestamp": "2025-02-10T02:00:00Z",
                        "value": null
                    }
                ]
            }
        ]
    }
}
```
