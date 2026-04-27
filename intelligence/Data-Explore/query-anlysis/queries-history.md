# **SQL 查询历史**

本篇文章将介绍查询历史模块，以帮助你轻松查看历史 SQL 查询记录，识别潜在风险的 SQL 语句和异常情况等审计内容。

## SQL 查询记录

1. 登录到 MatrixOne Intelligence 实例管理平台。选择目标实例，然后点击**通过云平台连接**以访问 MatrixOne Intelligence 数据库管理平台。

2. 在 MatrixOne Intelligence 数据库管理平台中，找到左侧菜单栏中的**查询历史**模块。点击以进入 SQL 查询历史页面。

在此页面，默认显示最近两小时内的查询历史，您可以设置特定筛选条件，如 SQL 类型、时间以及更多的筛选条件，如 SQL 文本、时长、数据库等，以缩小查询范围，快速定位到特定条件下的 SQL 查询记录。点击**搜索**按钮，以筛选出符合特定条件的查询记录列表。
:::{note}
当开启 SQL 文本作为筛选条件时，请注意区分大小写。
:::
   ![查询历史页面](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/sqleditor/query_history_0.12_1.png)

在 **SQL 文本**列您可以看到部分 SQL 前面会有 "/ *x queries*/" 的标志，这是因为记录查询历史的表信息量较大。为了提高查询速度，我们将超轻量级的 tp sqls 按以下规则聚合记录：

- 聚合周期为 5s  
- 聚合 SQL 的条件  
    - 时间小于 200 ms 的 Insert、Update、Delete、Execute、Select 语句  
    - response_at（响应时间）在聚合周期内的 sql  
    - sql_source_type：internal_sql (系统内部 SQL 请求)、cloud_nonuser_sql (云平台非用户语句)、external_sql (外部语句)  

其中，字段**时长**为 SQL 语句聚合后总的响应时间，"/ *x queries*/" 中的 "x" 指的是聚合的条数

作为 MatrixOne 的云上数据库管理平台，MatrixOne Intelligence 为用户提供了数据库信息的界面化展示，在实例平台上的任何操作获得的信息都是从数据库中获取的，也就是说在平台的所有操作都会产生 SQL 从而消耗 CU。但是由于考虑到用户可能更关心业务方面的 SQL，为了给用户更好的观测体验，平台上非用户操作的 SQL（除了 SQL Editor 执行的 SQL）在查询历史中默认是不显示的。对于生产实例来说，平台上非用户操作产生的 CU 也是收费的，可在筛选项中开启**非用户执行**选项来查看这部分 SQL 的详细信息。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/sqleditor/query_history_0.12_2.png)

## SQL 查询详情

在列表中，点击 SQL 文本内容，即可进入 SQL 查询详情页。在此页面，您可以详细查看特定 SQL 查询的执行时间、起止时间、事务 ID、会话 ID、CU 消耗、SQL 查询语句内容等详细信息，同时，您也可以查看特定 SQL 查询的查询结果，点击**下载**按钮以导出完整的查询结果。

   ![查询详情页面](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/sqleditor/src_history_3.png)

需要注意的是，对于非在平台 **SQL 编辑器**执行的 SELECT 语句，只保存以 `/* cloud_user */` 和 `/* save_result */` 固定开头的 SELECT 语句的查询结果，当不带上述 hint 时，Query 将不会显示详细的查询结果，如下图所示：

  ![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/sqleditor/src_history_4.png)

若想了解更多 MatrixOne 对于保存查询结果的支持，请查看[保存查询结果支持](https://docs.matrixorigin.cn/v25.2.1.0/MatrixOne/Reference/Variable/system-variables/save_query_result/#_2)。

现在，您已经了解如何访问 SQL 查询历史，筛选查询记录，并查看详细的查询信息。这将有助于您监测和审计 SQL 查询，以确保数据库的正常运行和安全性。
