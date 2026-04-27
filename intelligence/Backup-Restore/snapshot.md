# 快照备份恢复

快照是数据库在特定时间点的完整镜像，包含所有数据、配置和元数据，能够快速捕捉数据库的当前状态。与全量备份不同，快照备份的速度较快，因为它只是记录数据的变化或在特定时间点的状态，而不需要复制所有数据。在发生故障或误操作时，用户可以通过恢复快照将数据库迅速恢复至备份时的状态。MatrixOne Intelligence 提供了高效的快照备份与恢复功能，确保数据的可靠性和可恢复性。

:::{note}
目前，快照备份与恢复功能仅对付费实例开放，且处于 Beta 阶段，主要用于体验和测试目的。在使用过程中，请避免对重要数据进行恢复操作，以防止数据丢失或其他潜在风险。
:::
## 快照备份

MatrixOne Intelligence 提供了秒级快照备份功能，备份过程高效且无需消耗计算资源（CU），仅占用极少的存储空间。例如，当您的数据量为 100GB，但实际变化量只有 1GB 时，仅会备份新增或修改的部分数据，从而节省了冗余存储空间。用户可以通过登录实例管理平台，选择需要操作的实例，进入后即可访问**备份与恢复**功能栏，进行相关操作。

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/backup/snapshot-1.png
 width=100% heigth=100%/>
</div>

:::{note}
备份数据总存储的统计有 3-4h 的延迟。
:::
目前 MatrixOne Intelligence 支持手动和自动两种快照备份方式：

- 自动备份：默认启用，备份时间设定为每天的 01:00 UTC+8。暂无法修改备份周期，但可以调整备份时间或关闭自动备份功能。
- 手动备份：点击后，将立即对该实例执行一次备份操作。

连接实例，创建测试数据：

```sql
create table t1(n1 int);
insert into t1 values(1),(2),(3);

mysql> select * from t1;
+------+
| n1   |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.03 sec)
```

点击**手动备份**以启动实例备份操作，确认后可在下方的备份列表中查看此次备份的详细信息。

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/backup/snapshot-2.png
 width=100% heigth=100%/>
</div>

## 快照恢复

MatrixOne Intelligence 提供了高效的快照恢复功能。

连接实例并清除先前创建的 t1 数据。

```sql
truncate table t1;

mysql> select * from t1;
Empty set (0.03 sec)
```

在快照列表中点击刚才创建的快照右方的恢复按钮，将数据恢复到清除 t1 前。

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/backup/snapshot-3.png
 width=100% heigth=100%/>
</div>

请注意：

- 数据恢复期间，实例服务将会中断；  
- 数据恢复时间与实例总存储量相关，时间可能会较长，请做好充分的时间规划；
- 暂不支持取消数据恢复功能，建议您在数据恢复前手动备份一次，避免误操作导致的数据丢失；
- 关于数据恢复的计费方式：Serverless 实例会统计到“CU（数据恢复）”，标准实例使用其购买的计算节点恢复数据，故不收取费用。

连接实例并查看数据恢复状态，确认数据已成功恢复。您可以前往事件列表查看相关的恢复记录。

```sql
mysql> select * from t1;
+------+
| n1   |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.19 sec)
```

## 快照清除

如果不再需要某些快照，除了点击快照列表右方的删除按钮外，还可以通过点击上方的**备份清除**按钮来设置自定义清除周期。清除周期的设置范围为 7 到 365 天之间的任意整数。

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/backup/snapshot-4.png
 width=100% heigth=100%/>
</div>
