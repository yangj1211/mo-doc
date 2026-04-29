# MatrixOne Feature List

This document lists the features supported in the latest MatrixOne release — plus common features and roadmap items that are not yet supported.

## Data definition language (DDL)

| DDL | Supported (Y) / Not (N) / Experimental (E) |
| --- | --- |
| CREATE DATABASE | Y |
| DROP DATABASE | Y |
| ALTER DATABASE | N |
| CREATE TABLE | Y |
| ALTER TABLE | E |
| RENAME TABLE | Y |
| DROP TABLE | Y |
| CREATE INDEX | Y |
| DROP INDEX | Y |
| MODIFY COLUMN | Y |
| PRIMARY KEY | Y |
| CREATE VIEW | Y |
| ALTER VIEW | Y |
| DROP VIEW | Y |
| TRUNCATE TABLE | Y |
| AUTO_INCREMENT | Y |
| SEQUENCE | Y |
| TEMPORARY TABLE | Y |
| CREATE DYNAMIC TABLE | E, partial |
| PARTITION BY | E, partial types |
| CHARSET, COLLATION | N, UTF-8 only |

## Data manipulation / query language (DML/DQL)

| Statement | Supported |
| --- | --- |
| SELECT | Y |
| INSERT | Y |
| UPDATE | Y |
| DELETE | Y |
| REPLACE | Y |
| INSERT ON DUPLICATE KEY UPDATE | Y |
| LOAD DATA | Y |
| SELECT INTO | Y |
| INNER / LEFT / RIGHT / OUTER JOIN | Y |
| UNION, UNION ALL | Y |
| EXCEPT, INTERSECT | Y |
| GROUP BY, ORDER BY | Y |
| CLUSTER BY | Y |
| SUBQUERY | Y |
| Common Table Expressions (CTE) | Y |
| BEGIN / START TRANSACTION, COMMIT, ROLLBACK | Y |
| EXPLAIN | Y |
| EXPLAIN ANALYZE | Y |
| LOCK / UNLOCK TABLE | N |
| User-defined variables | Y |

## Advanced SQL

| Feature | Supported |
| --- | --- |
| PREPARE | Y |
| Stored procedure | N |
| Trigger | N |
| Event scheduler | N |
| User-defined function (UDF) | Y |
| Materialized view | N |

## Stream computing

| Feature | Supported |
| --- | --- |
| Dynamic tables | E |
| Kafka connector | E |
| Materialized view | N |
| Incremental materialized view | N |

## Time-series

| Feature | Supported |
| --- | --- |
| Time-series tables | Y |
| Sliding windows | Y |
| Downsampling | Y |
| Interpolation | Y |
| TTL (Time To Live) | N |
| ROLLUP | N |

## Data types

| Category | Type | Supported |
| --- | --- | --- |
| Integer | TINYINT / SMALLINT / INT / BIGINT (UNSIGNED) | Y |
|  | BIT | N |
| Float | FLOAT | Y |
|  | DOUBLE | Y |
| String | CHAR | Y |
|  | VARCHAR | Y |
|  | BINARY | Y |
|  | VARBINARY | Y |
|  | TINYTEXT / TEXT / MEDIUMTEXT / LONGTEXT | Y |
|  | ENUM | Y |
|  | SET | N |
| Binary | TINYBLOB / BLOB / MEDIUMBLOB / LONGBLOB | Y |
| Date / time | DATE | Y |
|  | TIME | Y |
|  | DATETIME | Y |
|  | TIMESTAMP | Y |
|  | YEAR | Y |
| Boolean | BOOL | Y |
| Fixed-point | DECIMAL | Y, up to 38 digits |
| JSON | JSON | Y |
| Vector | VECTOR | Y |
| Array | ARRAY | N (same as MySQL — array operations via JSON) |
| Bitmap | BITMAP | N |
| Spatial | GEOMETRY / POINT / LINESTRING / POLYGON | N |

## Indexes and constraints

| Feature | Supported |
| --- | --- |
| Primary key | Y |
| Composite primary key | Y |
| Unique constraint | Y |
| Secondary index | Y |
| Vector index | Y |
| Foreign-key constraint | Y |
| Check constraint for invalid data | Y |
| ENUM and SET constraints | N |
| NOT NULL | Y |
| AUTO_INCREMENT | Y |

## Transactions

| Feature | Supported |
| --- | --- |
| Pessimistic | Y (default) |
| Optimistic | Y |
| Cross-database transactions | Y |
| Distributed transactions | Y |
| Repeatable Read (Snapshot SI) | Y |
| Read Committed (RC) | Y (default) |

## Functions and operators

| Category | Supported |
| --- | --- |
| Aggregate functions | Y |
| Numeric functions | Y |
| Date / time functions | Y |
| String functions | Y |
| Cast | Y |
| Control-flow functions | E |
| Window functions | Y |
| JSON functions | Y |
| Vector functions | Y |
| System functions | Y |
| Other functions | Y |
| Operators | Y |

The complete function list is in [All Functions](../Reference/Functions-and-Operators/matrixone-function-list.md).

## Partitioning

| Type | Supported |
| --- | --- |
| KEY | E |
| HASH | E |
| RANGE | E |
| RANGE COLUMNS | E |
| LIST | E |
| LIST COLUMNS | E |

## Import / export

| Feature | Supported |
| --- | --- |
| INSERT INTO | Y |
| SQL import via SOURCE | Y |
| LOAD DATA INFILE | Y |
| LOAD DATA INLINE (streaming) | Y |
| Import from object storage | Y |
| mo-dump SQL/CSV export | Y |
| SELECT INTO CSV/JSON export | Y |
| mysqldump native tool | N |

## Security and access control

| Feature | Supported |
| --- | --- |
| TLS transport encryption | Y |
| At-rest encryption | Y |
| Object-storage import | Y |
| RBAC (Role-Based Access Control) | Y |
| Multi-tenancy | Y |

## Backup and restore

| Feature | Supported |
| --- | --- |
| Logical backup / restore | Y, mo-dump only |
| Physical backup / restore | Y, mobackup only |
| Snapshot backup / restore | Y, mobackup and SQL |
| PITR | Y, mobackup and SQL |
| CDC sync | Y, MatrixOne → MySQL only (mo_cdc) |
| Primary-standby DR | Y, cold-backup only |

## Management tools

| Tool | Supported |
| --- | --- |
| Standalone mo_ctl | Y |
| Distributed mo_ctl | E, Enterprise only |
| Visual management platform | E, Cloud only |
| System logging | Y |
| System metrics | Y |
| Slow-query log | Y |
| SQL records | Y |
| Kubernetes operator | Y |

## Deployment

| Form | Supported |
| --- | --- |
| Standalone on-premises | Y |
| Distributed on-premises | Y (self-hosted Kubernetes + MinIO) |
| Distributed on Alibaba Cloud | Y (ACK + OSS) |
| Distributed on Tencent Cloud | Y (TKE + COS) |
| Distributed on AWS | Y (EKS + S3) |
| Public-cloud Serverless | Y (MatrixOne Intelligence on AWS and Alibaba Cloud) |

## Application connectors and ORMs

| Connector | Supported |
| --- | --- |
| JDBC | Y |
| ODBC | N |
| pymysql | Y |
| go-sql-driver | Y |
| MyBatis | Y |
| MyBatis-Plus | Y |
| Spring JPA | Y |
| Hibernate | Y |
| GORM | Y |
| SQLAlchemy | Y |

Connectors / ORMs not listed above aren't necessarily unsupported. MatrixOne is highly MySQL 8.0 compatible — anything that works against MySQL will generally work against MatrixOne. Try it directly.

## Ecosystem tools

| Category | Tool | Supported |
| --- | --- | --- |
| DB IDE | Navicat | Y |
|  | MySQL Workbench | Y |
|  | DBeaver | Y |
|  | HeidiSQL | Y |
|  | SQLyog | Y |
| ETL | DataX | Y |
|  | Canal | Y |
|  | Kettle | Y |
|  | Seatunnel | Y |
|  | FlinkCDC | Y |
| Messaging | Kafka | Y |
| Compute | Spark | Y |
|  | Flink | Y |
| BI | Superset | Y |
|  | Tableau | Y |
|  | FineBI | Y |
|  | Yonghong BI | Y |
|  | Datafor | Y |
| Scheduling | DolphinScheduler | Y |
| Monitoring | Grafana | Y |

Tools not listed aren't necessarily unsupported. MatrixOne is highly MySQL 8.0 compatible — anything that works against MySQL generally works against MatrixOne. Try it directly.
