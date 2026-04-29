# MatrixOne vs. Common OLTP Databases

## What characterizes an OLTP database

OLTP stands for Online Transaction Processing — a database system geared toward business transactions. OLTP databases process many short transactions — day-to-day operations like order processing, inventory, banking. They provide high concurrency and real-time processing to meet demands for instant data access.

Main characteristics:

- **ACID**: OLTP systems must correctly record entire transactions. A transaction typically involves multiple steps or operations and completes only when all parties confirm, products/services are delivered, or certain tables receive the right updates. The transaction counts as correctly recorded only when every step is executed and logged. If any step errors, the whole transaction must abort and all effects must be removed — ensuring data accuracy.
- **High concurrency**: large user bases often access the same data at once. The system must ensure every user can read/write concurrently. Concurrency control prevents two users modifying the same data simultaneously, or forces one to wait until the other is done.
- **High availability**: OLTP systems must always be available to accept transactions. Failures risk revenue loss or legal consequences. Transactions run worldwide, at any time — so the system must be 24/7.
- **Fine-grained data access**: OLTP databases typically work with records — supporting efficient insert / update / delete plus fast commit and rollback.
- **High reliability**: OLTP systems must recover from any hardware or software failure.

## OLTP categories today

OLTP databases further split by architecture and tech path into centralized, distributed, and cloud-native:

* Most well-known OLTP databases are traditional centralized — Oracle, Microsoft SQL Server, MySQL, PostgreSQL, DB2 — most born between 1980–2000.
* Distributed OLTP is typified by Google's 2012 Spanner — share-nothing at the core — scaling via sharded storage and compute across nodes, with consensus for distributed consistency. Many call this architecture "NewSQL" — e.g., CockroachDB, SAP HANA, TiDB, OceanBase.
* Cloud-native OLTP — e.g., Aurora, PolarDB, NeonDB — distinctly adopts shared storage — fully decoupling compute and storage — scaling via the cloud's elastic storage service. MatrixOne takes this cloud-native path.

Note these three categories don't have strict boundaries — in practice each database gradually absorbs capabilities from others. Oracle's RAC architecture is classic shared-storage with some scalability. CockroachDB and TiDB are evolving toward cloud-native / shared storage. OLTP serves the broadest use case, and all three paths have large user bases.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/mo-other-database/oltp_category.png width=80% heigth=80%/>
</div>

## MatrixOne's OLTP characteristics

MatrixOne meets the OLTP basics:

* **Data operations + ACID**: row-level CRUD plus ACID transactions — see [Transactions in MatrixOne](../../Develop/Transactions/matrixone-transaction-overview/overview.md).
* **High concurrency**: for OLTP, the industry-standard TPC-C benchmark at 100 warehouses reaches tens of thousands of tpmC; capacity scales with nodes.
* **High availability**: MatrixOne runs on Kubernetes + shared storage — both have mature HA patterns in cloud environments. MatrixOne's own design also considers HA and fault recovery for each component. See [HA in MatrixOne](../../Overview/feature/high-availability.md).

Per the diagram above, on architecture MatrixOne sits in the cloud-native camp — closer to Aurora. Compared to share-nothing, its biggest advantage is separated compute/storage — both are used on demand.

Two differences vs. Aurora:

* Aurora exposes the write node at the user layer — users can only write through one node. MatrixOne hides write processing in TN + LogService — from the user, every CN accepts reads and writes.
* Aurora's shared storage still heavily uses block storage as primary, with object storage as backup. MatrixOne uses object storage as the full-data primary directly.

MatrixOne isn't limited to OLTP — its workload coverage goes beyond Aurora's positioning.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/mo-other-database/mo_vs_aurora.png)

## MatrixOne vs. MySQL

MatrixOne targets MySQL compatibility, and MySQL is the [most popular open-source database](https://db-engines.com/en/ranking). Many MatrixOne users migrate from MySQL. So here's a detailed comparison.

| | MySQL | MatrixOne |
| --- | --- | --- |
| Version | 8.0.37 | latest |
| License | GPL | Apache 2.0 |
| Architecture | Centralized | Distributed cloud-native |
| Workload types | OLTP; analytics depends on Enterprise Heatwave | HTAP, time-series |
| Storage format | Row | Column |
| Storage engine | InnoDB / MyISAM | TAE |
| Interface | SQL | SQL |
| Deployment | Standalone / primary-standby | Standalone / primary-standby / distributed / Kubernetes |
| Horizontal scale | Depends on sharding middleware | Native |
| Transactions | Pessimistic / optimistic; ANSI 4 isolation levels (InnoDB) | Pessimistic / optimistic; RC / SI |
| Data types | Basics, date/time, string, JSON, spatial | Basics, date/time, string, JSON, vector |
| Indexes & constraints | PK, secondary, unique, foreign | PK, secondary, unique, foreign |
| Access control | RBAC | RBAC |
| Window functions | Basic | Basic + sliding time windows |
| Advanced SQL | Triggers, stored procedures | Not supported |
| Stream computing | Not supported | Streaming writes / Kafka connector / Dynamic Tables |
| UDF | SQL and C UDFs | SQL and Python UDFs |
| Multi-tenancy | Not supported | Supported |
| Data sharing | Not supported | Cross-tenant data sharing |
| Languages | Most languages | Java, Python, Go connectors & ORMs broadly supported |
| Visual admin tools | Navicat, DBeaver, MySQL Workbench, DataGrip, HeidiSQL… | Same as MySQL |
| Backup tools | Logical, physical | Logical, physical, snapshot |
| CDC | Yes | Not supported |
| OLTP performance | Excellent standalone, not scalable | Good standalone, scalable |
| OLAP performance | Weak | Excellent, scalable |
| Bulk-write performance | Weak | Excellent, scalable |
| Storage capacity | Bound by disk | Infinite |

More detail in the [MatrixOne MySQL compatibility guide](../../Overview/feature/mysql-compatibility.md).

Overall, MatrixOne is a highly MySQL-compatible cloud-native HTAP database — most MySQL-based apps port seamlessly. It also has strong scalability and support for other workload types. Compute-storage separation + multi-tenancy let users offload workload-isolation problems — previously solved at the app, middleware, or separate-database layer — to MatrixOne end-to-end.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/mo-other-database/mo_mysql_use_case.png width=60% heigth=60%/>
</div>

For MySQL users facing any of the following, MatrixOne is a better fit:

* Single tables exceed millions of rows and queries slow down — need to shard.
* Total data exceeds TB — MySQL requires very expensive hardware.
* Multi-table join analytics or large single-table aggregate queries.
* Large-scale real-time writes — millions of rows per second.
* Multi-tenant application design — SaaS scenarios.
* Frequent vertical scaling due to workload changes.
* Frequent data-movement and collaboration needs.
* Integrating with app frameworks in K8s — reducing ops complexity.
* Stream processing — real-time ingest and transformation.
* Storing and searching vector data.

We also have tech-blog posts comparing MatrixOne and MySQL and describing migration:

[MatrixOne vs MySQL — Deployment](https://mp.weixin.qq.com/s?__biz=Mzg2NjU2ODUwMA==&mid=2247491148&idx=2&sn=a83e592da9504d6b4ab356abd6cc2369&chksm=cf9274a6b133599752c811ea241d1c0b25fc44dcc255bf907de131b9a9bb6972d5ebd076d1b6&scene=0&xtrack=1#rd)

[MatrixOne vs MySQL — Multi-tenancy](https://mp.weixin.qq.com/s?__biz=Mzg2NjU2ODUwMA==&mid=2247491293&idx=1&sn=e1967b12371a7f8b57b336d1f8ada986&chksm=cf974c93821360fb559c865b5eba71adb155c410a99e3bc4d0f7aac675a80eab6d95a24853f6&scene=0&xtrack=1#rd)

[MatrixOne vs MySQL — Migration](https://mp.weixin.qq.com/s?__biz=Mzg2NjU2ODUwMA==&mid=2247491369&idx=2&sn=a0bab26c2709edd7bc278a1bcbb07d64&chksm=cf3ea15bec8aef761e476a5281b9723638c90f059af813b0c0cc799a3256a92fc96d483e0670&scene=0&xtrack=1#rd)
