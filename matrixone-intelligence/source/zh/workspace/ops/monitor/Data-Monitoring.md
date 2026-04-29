# 监控数据

本篇文档将详细介绍 MatrixOne Intelligence 提供的数据查看功能。

## 概述

在 MatrixOne Intelligence 数据库管理平台中，我们提供了数据库功能，可以实时查看实例中的数据统计信息和进行数据采样。这有助于 SQL 管理员实时了解数据状态，同时为 SQL 使用人员提供了有用的信息参考。该功能分别从实例、数据库和数据表等层次提供了详细的数据信息统计。

## 实例数据总览

你可以轻松查看实例中的所有数据库基本信息，其中包括数据库的数量、每个数据库的创建时间以及包含的数据表数量。这使你能够快速了解数据的总体规模，并能够执行数据库的删除操作。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/monitor/monitor-3.png)

## 数据库信息

在界面左侧的数据库对象树区域，点击你感兴趣的数据库名称，右侧区域将显示数据库的基本信息，包括该数据库包含的表数、每张表的行数、存储大小、创建时间等等。通过这些信息，你可以详细了解数据库的容量分布情况，并可以选择性删除特定表。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/monitor/monitor-4.png)

## 数据表信息

通过查看上层数据库的信息，你可以在对象树中点击感兴趣的表名，以进一步查看表的详细信息。这包括表的创建语句、列数、列的数据类型、默认值、键类型、以及最大值和最小值等信息。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/monitor/monitor-5.png)
