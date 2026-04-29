# FAQ

## Does MatrixOne support the MySQL protocol?

Yes. MatrixOne is compatible with the **MySQL 8.0 protocol** — most MySQL clients and drivers connect out of the box, no adaptation needed.

Command line:

```bash
mysql -h 127.0.0.1 -P 6001 -u dump -p111
```

JDBC connection string:

```text
jdbc:mysql://127.0.0.1:6001/your_db?useSSL=false&serverTimezone=Asia/Shanghai
```

A few features are not supported: some stored-procedure syntax, GIS spatial indexes, and MySQL's native full-text search (MatrixOne uses its own vector search instead).

## How much data can a single node handle?

In single-node deployments, MatrixOne has been validated at **10 TB scale** in production. Distributed deployments can theoretically scale to PB.

A demo usually needs only hundreds of MB to a few GB — a single node is plenty. Deployment guidance:

- **Dev / demo** — single-node Docker, 4 cores / 8 GB
- **Small-to-mid production** — single-node bare metal, 16 cores / 32 GB or more
- **Large scale** — distributed, 3+ nodes

## How is it different from TiDB or Doris?

MatrixOne is positioned as an **HTAP + AI-Ready** all-in-one database. Key differentiators:

- **One dataset serves both OLTP and OLAP** — no ETL to another system
- **Built-in vector search and AI functions** — a solid backing store for RAG applications
- **Data branches / snapshots** — Git-like data versioning
- **Serverless architecture** — separated compute and storage, pay-per-use (cloud edition)

Guidance: for pure OLTP, TiDB is still recommended; for pure OLAP, Doris or ClickHouse. **When you need both plus AI capabilities**, consider MatrixOne.

## How do I check the current version?

Two ways:

```sql
SELECT version();
```

Or query the system table for more detailed build info:

```sql
SELECT * FROM mo_catalog.mo_version;
```

## Which language clients are supported?

Official or community clients, all built on the MySQL protocol:

- **Go** — `github.com/go-sql-driver/mysql`
- **Python** — `pymysql`, `mysql-connector-python`, `sqlalchemy`
- **Java** — `mysql-connector-java`
- **Node.js** — `mysql2`
- **Rust** — `sqlx` (with the MySQL feature enabled)
- **.NET** — `MySqlConnector`

Any MySQL-protocol-compatible ORM or connection pool (HikariCP, Druid, etc.) also works directly.

## How do I back up data?

Two recommended approaches, pick by scenario:

1. **Snapshot + restore** — use `CREATE SNAPSHOT` for a point-in-time snapshot. Zero cost, completes in seconds. See [CREATE SNAPSHOT](../../reference/snapshot.md).
2. **mo-dump** — a CLI tool for logical backups, well suited for cross-environment migration:

   ```bash
   mo-dump -u dump -p111 -h 127.0.0.1 -P 6001 \
     -db demo > demo.sql
   ```

Daily: use snapshots for point-in-time protection (fast, same-instance only). Cross-environment: use `mo-dump` (slower but portable). The two can be combined.
