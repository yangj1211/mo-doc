# 查询分析

本篇文档将指导用户如何通过 MatrixOne Intelligence 内置的查询分析（Query Profile）进行在线的 SQL 查询分析。也可以理解成，查询分析模块是将数据库中的 Explain，即解释详细执行计划的能力做成了可视化模块，通过可视化的方式向用户展示这条 SQL 的执行计划。
:::{note}
由于执行计划的保存会消耗一些资源，考虑到其主要用于分析和改进慢查询，因此云平台仅保存执行时长大于 1s 的 SQL 的执行计划。
:::
## 什么是执行计划

执行计划（execution plan，也叫查询计划或者解释计划）是数据库执行 SQL 语句的具体步骤，例如通过索引还是全表扫描访问表中的数据，连接查询的实现方式和连接的顺序等；执行计划根据你的表、列、索引和 `WHERE` 子句中的条件的详细信息，可以告诉你这个查询将会被如何执行或者已经被如何执行过，可以在不读取所有行的情况下执行对巨大表的查询；可以在不比较行的每个组合的情况下执行涉及多个表的连接。如果 SQL 语句性能不够理想，首先应该查看它的执行计划。和大多数成熟的数据库产品一样，MatrixOne 数据库也提供了这一分析查询语句性能的功能。

MatrixOne 查询优化器对输入的 SQL 查询语句通过**执行计划**而选择出效率最高的一种执行方案。你也可以通过执行计划看到 SQL 代码中那些效率比较低的地方。

## 使用 `EXPLAIN` 查询执行计划

用户可以使用 `EXPLAIN` 可查看 MatrixOne 执行某条 SQL 语句时的执行计划。

`EXPLAIN` 可以和 `SELECT`、`DELETE`、`INSERT`、`REPLACE`、`UPDATE` 语句结合使用。当 `EXPLAIN` 与可解释的语句一起使用时，MatrixOne 会解释它将如何处理该语句，包括有关表如何连接以及连接顺序的信息。MatrixOne Intelligence 中暂时不支持通过在 SQL 编辑器中使用 `EXPLAIN` 查询执行计划，而是提供了 `查询分析` 的可视化界面向用户展示执行计划，如果用户希望查看 `EXPLAIN` 的原始信息的时候，可以通过 MySQL 客户端连接 MatrixOne Intelligence 的实例进行执行。

:::{note}
使用 MySQL 客户端连接到 MatrixOne 时，为避免输出结果在终端中换行，可先执行 `pager less -S` 命令。执行命令后，新的 `EXPLAIN` 的输出结果不再换行，可按右箭头 **→** 键水平滚动阅读输出结果。
:::
## 在查询历史筛选 Query

在查询历史中找到您想了解的 Query，这里我们以系统自带的 TPCH10G 数据集的 Q1 为例，如下图所示：

![Alt text](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/sqleditor/query_history_0.12_3.png)

## 查看该 Query 的查询分析

点击进入这条 Query 的查询详情界面，我们可以同时看到它的查询分析（Query Profile）界面，如下图所示：

![Alt text](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/sqleditor/history-2.png)

该界面展示了 TPCH Q1 的整个执行过程，总共分为了 4 个计划节点：表扫描 (Table Scan)，聚合 (Aggregate)，排序 (Sort) 及投影 (Project)。

箭头的方向代表了执行的步骤，首先我们会对 `mo_sample_data_tpch_sf10.lineitem` 这张表进行扫描 (Table Scan)，筛选出特定条件的数据，从图中可知道符合条件的数据为 `58,682,142` 行，这些数据作为下一个节点的输入，然后经过聚合 (Aggregate) 运算后输出 `4` 行，再对这 `4` 行数据根据指定字段进行排序 (Sort)，最后从表里选择你所要的列，即进行投影 (Project) 运算。

我们可以看到，在每一个节点块上我们都表明了它的操作对象，执行细节及所消耗的 CPU 和内存资源。如 Table Scan 节点，我们可以看到它的操作对象是 `mo_sample_data_tpch_sf10.lineitem` 这张表，同时这个操作消耗的 CPU 资源是 `1.6 core*s`，内存则消耗了 `4.7GB`, 这些资源消耗即是我们计算 CU 消耗的基础。我们会根据一定的算法加总所有步骤所消耗的 CPU 和内存资源，即得到这条 Query 消耗的 CU 个数。

如果我们再选中点击 Table Scan 节点块，我们将看到 Table Scan 节点执行的更多细节，如下图：

![Alt text](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/sqleditor/history-3.png)

在该案例中我们可以看到 Table Scan 节点执行的过程中选中的是 18 个列中的 7 个 `（l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, l_shipdate）`，另外还包含了一个过滤的条件 `(lineitem.l_shipdate <= 1998-08-11)`。

## 理解 MatrixOne 的执行计划

对于更详细的 MatrixOne 的执行计划的细节和节点类型，请参考 [Explain](../../../../reference/SQL-Reference/Other/Explain/explain.md) 和 [Explain 输出格式](../../../../reference/SQL-Reference/Other/Explain/explain-workflow.md)相关章节说明。
