# 监控指标

本节将详细介绍 MatrixOne Intelligence 提供的各种监控指标。

## 实例监控指标

实例监控指标是服务于 MatrixOne Intelligence 实例管理平台的运维人员的监控信息，您可以点击右上角的实例名列表来切换您想了解的实例信息，包括：平均连接数，CU 使用量和存储用量。对于 CU 和存储的使用信息您也可以直接点击实例界面您想了解的实例，跳转至实例详情中查看。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/monitor/monitor_0.12_3.png)

- 平均连接数

统计周期内，连接到实例的 Session 平均数。每 15s 统计一次，无连接时为 0，早于实例创建时间的地方为空。

- CU 使用量

在统计周期内，CU 消耗的总量。

- 存储用量

在统计周期内，实例中数据存储的最大使用量。存储的使用量每 15 分钟更新一次，体现的是 15 分钟之前的数据。

## 业务监控指标

业务监控指标是服务于数据应用人员的监控信息，可以在 MatrixOne Intelligence 数据库管理平台中找到，其中包括：

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/monitor/monitor_0.12_1.png)

- 每秒查询次数 (QPS)

平均每秒完成的 SQL 查询数量，代表实例的吞吐能力。

- 每秒查询事务数 (TPS)

平均每秒完成的事务查询数量，反映了数据库在单位时间内处理事务的能力。

- 查询延迟

平均每条 SQL 查询的执行时间，代表实例的运行性能，按 SQL 类型进行统计。

- 事务总数

在统计周期内，执行的事务总数。

- 事务失败数

在统计周期内，执行失败的事务总数。

- SQL 语句总数

在统计周期内，执行的 SQL 语句总数。

- SQL 语句失败数

在统计周期内，执行失败的 SQL 语句总数。

## 统计时长与统计周期

为了帮助用户从宏观和微观角度分析实例的性能和问题，MatrixOne Intelligence 提供了多种统计时长，每种时长对应不同的统计周期，默认显示最近 30 分钟的监控数据，用户可以根据需要自由切换。如下图所示：

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/monitor/monitor_0.12_2.png width=60% heigth=60%/>
</div>

:::{note}
较短的统计周期更能反映业务的最近变化，而较长的统计周期更适合观察长期趋势和历史问题。
:::