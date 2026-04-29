# 开发指南

```{toctree}
:maxdepth: 2
:caption: 概述

develop-overview
```

```{toctree}
:maxdepth: 2
:caption: 连接到 MatrixOne

connect-mo/database-client-tools
connect-mo/java-connect-to-matrixone/connect-mo-with-jdbc
connect-mo/java-connect-to-matrixone/connect-mo-with-orm
connect-mo/connect-to-matrixone-with-c#
connect-mo/python-connect-to-matrixone
connect-mo/connect-to-matrixone-with-go
connect-mo/connect-to-matrixone-with-typescript
```

```{toctree}
:maxdepth: 2
:caption: 数据库模式设计

schema-design/overview
schema-design/create-database
schema-design/create-table
schema-design/create-table-as-select
schema-design/create-view
schema-design/create-temporary-table
schema-design/create-secondary-index
schema-design/data-integrity/overview-of-integrity-constraint-types
schema-design/data-integrity/not-null-constraints
schema-design/data-integrity/unique-key-constraints
schema-design/data-integrity/primary-key-constraints
schema-design/data-integrity/foreign-key-constraints
schema-design/data-integrity/auto-increment-integrity
```

```{toctree}
:maxdepth: 2
:caption: 数据写入

import-data/insert-data
import-data/stream-load
import-data/bulk-load/bulk-load-overview
import-data/bulk-load/load-csv
import-data/bulk-load/load-jsonline
import-data/bulk-load/load-s3
import-data/bulk-load/using-source
import-data/update-data
import-data/delete-data
import-data/prepared
```

```{toctree}
:maxdepth: 2
:caption: 数据写出

export-data/select-into-outfile
export-data/modump
```

```{toctree}
:maxdepth: 2
:caption: 数据读取

read-data/query-data-single-table
read-data/multitable-join-query
read-data/subquery
read-data/views
read-data/cte
read-data/window-function/window-function
read-data/window-function/time-window
```

```{toctree}
:maxdepth: 2
:caption: 数据去重

distinct-data/count-distinct
distinct-data/bitmap
```

```{toctree}
:maxdepth: 2
:caption: 数据集成

data-integration/stage-datalink
```

```{toctree}
:maxdepth: 2
:caption: 租户设计

publish-subscribe/multi-account-overview
publish-subscribe/pub-sub-overview
```

```{toctree}
:maxdepth: 2
:caption: 事务

transactions/common-transaction-overview
transactions/matrixone-transaction-overview/overview
transactions/matrixone-transaction-overview/explicit-transaction
transactions/matrixone-transaction-overview/implicit-transaction
transactions/matrixone-transaction-overview/pessimistic-transaction
transactions/matrixone-transaction-overview/optimistic-transaction
transactions/matrixone-transaction-overview/isolation-level
transactions/matrixone-transaction-overview/mvcc
transactions/matrixone-transaction-overview/how-to-use
transactions/matrixone-transaction-overview/scenario
```

```{toctree}
:maxdepth: 2
:caption: 用户定义函数

udf/udf-python
udf/udf-python-advanced
```

```{toctree}
:maxdepth: 2
:caption: 向量

vector/vector_type
vector/vector_search
vector/vector_index
vector/cluster_centers
```

```{toctree}
:maxdepth: 2
:caption: 应用开发示例

tutorials/develop-java-crud-demo
tutorials/develop-python-crud-demo
tutorials/springboot-hibernate-crud-demo
tutorials/springboot-mybatis-crud-demo
tutorials/sqlalchemy-python-crud-demo
tutorials/django-python-crud-demo
tutorials/develop-golang-crud-demo
tutorials/gorm-golang-crud-demo
tutorials/c-net-crud-demo
tutorials/typescript-crud-demo
tutorials/htap-demo
tutorials/rag-demo
tutorials/search-picture-demo
tutorials/python-sdk-demo
tutorials/dify-mo-demo
```

```{toctree}
:maxdepth: 2
:caption: 生态工具

ecological-tools/message-queue/Kafka
ecological-tools/bi-connection/FineBI-connection
ecological-tools/bi-connection/yonghong-connection
ecological-tools/bi-connection/Superset-connection
ecological-tools/etl/seatunnel/seatunnel-overview
ecological-tools/etl/seatunnel/seatunnel-mysql-matrixone
ecological-tools/etl/seatunnel/seatunnel-oracle-matrixone
ecological-tools/etl/datax/datax-overview
ecological-tools/etl/datax/datax-mysql-matrixone
ecological-tools/etl/datax/datax-oracle-matrixone
ecological-tools/etl/datax/datax-postgresql-matrixone
ecological-tools/etl/datax/datax-sqlserver-matrixone
ecological-tools/etl/datax/datax-mongodb-matrixone
ecological-tools/etl/datax/datax-tidb-matrixone
ecological-tools/etl/datax/datax-clickhouse-matrixone
ecological-tools/etl/datax/datax-doris-matrixone
ecological-tools/etl/datax/datax-influxdb-matrixone
ecological-tools/etl/datax/datax-elasticsearch-matrixone
ecological-tools/computing-engine/spark/spark-overview
ecological-tools/computing-engine/spark/spark-mysql-matrixone
ecological-tools/computing-engine/spark/spark-hive-matrixone
ecological-tools/computing-engine/spark/spark-doris-matrixone
ecological-tools/computing-engine/flink/flink-overview
ecological-tools/computing-engine/flink/flink-mysql-matrixone
ecological-tools/computing-engine/flink/flink-oracle-matrixone
ecological-tools/computing-engine/flink/flink-sqlserver-matrixone
ecological-tools/computing-engine/flink/flink-postgresql-matrixone
ecological-tools/computing-engine/flink/flink-mongo-matrixone
ecological-tools/computing-engine/flink/flink-tidb-matrixone
ecological-tools/computing-engine/flink/flink-kafka-matrixone
ecological-tools/scheduling-tools/dolphinScheduler
```
