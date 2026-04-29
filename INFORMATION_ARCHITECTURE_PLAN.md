# 信息架构梳理(IA Plan)

> 范围:`matrixone/source/zh/` 全部 markdown 文件,共 628 篇。
> 本文不做任何代码/内容/CSS 改动,仅为 IA 决策提供依据。

## 1. 当前架构问题

| 维度 | 实际情况 | 期望 |
|---|---|---|
| 顶部一级导航 | 6 项(快速开始 / 产品概述 / 开发指南 / SQL 参考 / 常见问题 / 版本发布) | 与左树顶级分类一一对应 |
| 左侧侧边栏顶级分类 | **16 个**(包含 deploy / maintain / migrate / test / performance-tuning / security / troubleshooting / tutorial / contribution-guide / glossary,这 10 个不在顶部 nav) | 顶部点哪个,左树只显示对应内容 |
| 失配导致 | 顶部"6 选 1"无法精确切到左树。当前 CSS `.toctree-l1:not(.current)` 隐藏方案在 deploy/maintain 等 stranded 分类页面下,顶部不会高亮任一项 | 一一对应 |

**散落在顶部 nav 之外的文件**:约 98 篇(15.6%),分布在 deploy(15)、tutorial(15)、maintain(14)、performance-tuning(12)、security(12)、contribution-guide(12)、migrate(6)、test(6)、troubleshooting(5)、根 glossary(1)。

---

## 2. 完整盘点

每个分类下列出所有文档的:文件路径、H1 标题、首段一句摘要(从源文件第一段散文提取,空白 = 无散文)。
SQL Reference 子树达 364 篇,按 sub-section 分组展示(避免 700+ 行 SQL 命令罗列);其它分类完整列出。

### 主页 / 根级文件  `(_root/, 2 篇)`

- `glossary.md` — 术语表 — 阅读以下对相关词汇的概念解释或许有助于你理解我们的整体架构。
- `index.md` — 一个持续运行、自我优化的数据飞轮 — MatrixOne 是面向 AI 时代的一体化数据库，在一套引擎中同时提供 OLTP、OLAP、流处理与向量检索能力。本站帮助你从 5 分钟上手到深入掌握核心概念与 SQL 语法。

### 关于 MatrixOne(产品概述)  `(overview/, 25 篇)`
> 产品定位、功能清单、架构详解、与其它库对比

- `overview/architecture/architecture-cold-hot-data-separation.md` — 数据缓存及冷热数据分离架构详解 — 数据缓存及冷热数据分离是 MatrixOne 的一项关键特性，该特性将数据分为热数据和冷数据，以使用频率为区分标准，并将它们以不同的存储方式进行管理。这一设计使得 MatrixOn
- `overview/architecture/architecture-logservice.md` — Logservice 架构详解 — Logservice 在 MatrixOne 中扮演着非常重要的角色，它是一个独立的服务，通过 RPC 的方式供外部组件使用，用于日志管理。
- `overview/architecture/architecture-logtail.md` — Logtail 协议详解 — Logtail 是 CN（Computation Node，计算节点）与 TN（Transaction Node，事务节点）之间的一种日志同步协议，它作为 CN 和 TN 协同工作
- `overview/architecture/architecture-matrixone-operator.md` — Matrixone-Operator 设计与实现详解 — MatrixOne 是一款云原生分布式数据库，天然适应云基础设施并面向云的成本模型进行优化。而与一般的 SaaS 服务不同，出于对性能和数据安全的需求，在严肃场景下数据库往往需要跟
- `overview/architecture/architecture-proxy.md` — Proxy 架构详解 — Proxy 作为 MatrixOne 中承担负载均衡与 SQL 请求分发的唯一组件，通过将 CN 分组标签的方式，搭配 Proxy 的 SQL 分发，实现会话级别的 SQL 路由功
- `overview/architecture/architecture-tae.md` — 存储引擎架构详解 — MatrixOne 的存储引擎称为事务分析引擎（Transactional Analytical Engine，TAE）。
- `overview/architecture/architecture-transaction-lock.md` — 事务与锁机制实现详解 — 本文将向你介绍 MatrixOne 的事务与锁机制的实现细节。
- `overview/architecture/architecture-wal.md` — WAL 技术详解 — WAL（Write Ahead Log）是一项与数据库原子性和持久性相关的技术，在事务提交时把随机写转换成顺序读写。事务的更改随机地发生在各页上，这些页很分散，随机写的开销大于顺序
- `overview/architecture/matrixone-architecture-design.md` — MatrixOne 架构设计 — MatrixOne 是一款超融合异构云原生数据库。
- `overview/architecture/streaming.md` — 流引擎架构详解 — MatrixOne 内置流引擎，用于实时查询、处理和/或丰富传入的一系列数据点（即数据流）的数据存储。开发人员现在可以使用 SQL 来定义和创建流处理管道，并作为实时数据后端提供服
- `overview/feature/cost-effective.md` — 高性价比 — MatrixOne 是一款全新设计的数据库，其架构设计理念强调高性价比。MatrixOne 的高性价比主要体现在以下几个方面：
- `overview/feature/high-availability.md` — 高可用性 — 数据库的高可用性是企业关键需求，它保证了系统的持续可用性、数据的安全性，以及业务的连续性。MatrixOne 作为一款高可用性的分布式数据库，能满足企业的需求。本文档旨在介绍 Ma
- `overview/feature/key-feature-htap.md` — 混合负载 HTAP — MatrixOne 是一款能够支持 HTAP（Hybrid Transaction Analytical Processing）混合负载处理的数据库，旨在提供满足单一数据库内事务处
- `overview/feature/key-feature-multi-accounts.md` — 多租户 — MatrixOne 的设计采用了单一集群多租户的方式。在这个设计中，租户（Account）是一个逻辑概念，作为资源分配和数据库管理的单位。MatrixOne 的多租户模式能够为不同
- `overview/feature/mysql-compatibility.md` — MySQL 兼容性 — 本篇文章主要对比并介绍 MatrixOne 数据库的 MySQL 模式以及原生 MySQL 数据库的兼容性信息。
- `overview/feature/scalability.md` — 极致扩展性 — MatrixOne 是一款超级整合异构云原生数据库，其整体基于存储、计算和事务分离的架构，拥有极致的弹性扩展能力，能够迅速应对用户负载的变动。随着数据量和业务的扩大，企业对数据库扩
- `overview/feature/stream.md` — 流 — 随着实时数据分析的兴起，流式数据在多个领域中变得越来越重要。这些数据源主要包括但不限于社交媒体实时动态、在线零售交易、实时市场分析、网络安全监控、即时通讯记录，以及智能城市基础设施
- `overview/feature/time-series.md` — 时序能力 — 随着物联网的发展，时序数据库的需求越来越多，比如智能汽车产生的数据，工厂的设备监控、金融行业的交易行情指标数据等。常见的业务场景包括：
- `overview/feature/udf.md` — 用户定义函数 UDF — 您可以编写用户定义函数 (UDF) 来扩展系统，以执行 MatrixOne 提供的内置系统定义函数无法执行的操作，创建 UDF 后，您可以多次重复使用它。
- `overview/index.md` — 关于 MatrixOne
- `overview/matrixone-feature-list.md` — MatrixOne 功能清单 — 本文档列出了 MatrixOne 最新版本所支持的功能清单，针对常见以及在 MatrixOne 的路线图中的功能但是目前不支持的功能也将列出。
- `overview/matrixone-introduction.md` — MatrixOne 简介 — MatrixOne 是一款超融合异构分布式数据库，通过云原生化和存储、计算、事务分离的架构构建 HSTAP 超融合数据引擎，实现单一数据库系统支持 OLTP、OLAP、流计算等多种
- `overview/matrixone-vs-other_databases/matrixone-positioning.md` — MatrixOne 的定位 — 在庞大而复杂的数据技术栈和各类数据库产品中，MatrixOne 的定位是一款主打一站式融合能力和灵活扩展性的 SQL 关系型数据库。MatrixOne 的设计目标是提供一个使用体验
- `overview/matrixone-vs-other_databases/matrixone-vs-oltp.md` — MatrixOne 与常见 OLTP 数据库的对比 — OLTP 是指一种面向业务交易的数据库管理系统。OLTP 数据库用于处理大量的短期交易，这些交易通常是一些日常业务操作，例如订单处理、库存管理、银行交易等。它可以提供高并发性能和实
- `overview/whats-new.md` — 最新发布 — MatrixOne 的最新版本为 v25.2.2.2，发布于 2025 年 07 月 17 日，详情请见：

### 快速开始  `(getting-started/, 9 篇)`
> 安装(Linux / macOS / Docker)+ 基本 SQL

- `getting-started/basic-sql.md` — MatrixOne 的 SQL 基本操作 — MatrixOne 兼容 MySQL，你可以使用 MySQL 客户端或其他方式连接 MatrixOne。参加 [MySQL 兼容性](../Overview/feature/mys
- `getting-started/index.md` — 快速开始
- `getting-started/install-on-linux/install-on-linux-method1.md` — Linux 使用源代码部署 — 本篇文档将指导你使用源代码在 Linux 环境中部署单机版 MatrixOne。我们将采用 [mo_ctl](https://github.com/matrixorigin/mo_
- `getting-started/install-on-linux/install-on-linux-method2.md` — Linux 使用二进制包部署 — 本篇文档将指导你使用二进制包在 Linux 环境中部署单机版 MatrixOne，这种安装方案无需安装前置依赖和编译源码包，可以直接通过 [mo_ctl](https://gith
- `getting-started/install-on-linux/install-on-linux-method3.md` — 使用 Docker 部署 — 本篇文档将指导你使用 Docker 部署单机版 MatrixOne。
- `getting-started/install-on-macos/install-on-macos-method1.md` — macOS 使用源代码部署 — 本篇文档将指导你使用源代码在 macOS 环境中部署单机版 MatrixOne。我们将采用 [mo_ctl](https://github.com/matrixorigin/mo_
- `getting-started/install-on-macos/install-on-macos-method2.md` — macOS 使用二进制包部署 — 本篇文档将指导你使用二进制包在 macOS 环境中部署单机版 MatrixOne，这种安装方案无需安装前置依赖和编译源码包，可以直接通过 [mo_ctl](https://gith
- `getting-started/install-on-macos/install-on-macos-method3.md` — 使用 Docker 部署 — 本篇文档将指导你使用 Docker 部署单机版 MatrixOne。
- `getting-started/install-standalone-matrixone.md` — 单机部署 MatrixOne — 单机版 MatrixOne 适用场景即是使用单台开发机器部署 MatrixOne，体验 MatrixOne 的基本功能，与单机版使用一个 MySQL 基本相同。

### 开发指南  `(develop/, 93 篇)`
> 驱动连接 / Schema / 读写 / 事务 / 向量 / 生态工具

- `develop/connect-mo/connect-to-matrixone-with-c#.md` — C# 连接 — MatrixOne 支持 C# 连接，并且支持 MySQL Connector/NET 驱动。
- `develop/connect-mo/connect-to-matrixone-with-go.md` — Golang 连接 — MatrixOne 支持 Golang 连接，并且支持 [`Go-MySQL-Driver`](https://github.com/go-sql-driver/mysql)。
- `develop/connect-mo/connect-to-matrixone-with-typescript.md` — TypeScript 连接 — MatrixOne 支持 TypeScript 连接。
- `develop/connect-mo/database-client-tools.md` — 客户端工具连接 — MatrixOne 现在支持通过以下几种数据库客户端工具的方式连接 MatrixOne 服务：
- `develop/connect-mo/java-connect-to-matrixone/connect-mo-with-jdbc.md` — 使用 JDBC 连接 — 在 Java 中，我们可以通过 Java 代码使用 JDBC 连接器（Java Database Connectivity）连接到 MatrixOne。JDBC 是用于数据库连接的
- `develop/connect-mo/java-connect-to-matrixone/connect-mo-with-orm.md` — 使用 Java ORMs 连接 — 除了使用 JDBC 连接 MatrixOne 之外，我们还可以使用对象关系映射 (ORM) 框架连接到 MatrixOne 数据库。在本篇文档中，介绍了如何使用 Spring Da
- `develop/connect-mo/python-connect-to-matrixone.md` — Python 连接 — MatrixOne 支持 Python 连接，支持 `pymysql` 和 `sqlalchemy` 两种驱动程序。
- `develop/data-integration/stage-datalink.md` — Stage — 在 MatrixOne，Stage 用于连接外部存储位置（如 AWS S3、MINIO 或文件系统），从而支持数据文件的批量导入、导出以及管理。DATALINK 则是一种数据类型，
- `develop/develop-overview.md` — 概述 — 本篇文章及其后续章节主要旨在介绍如何利用 MatrixOne 进行应用开发。我们将展示如何连接到 MatrixOne，如何创建数据库和表，以及如何构建基于常见编程语言（如 Java
- `develop/distinct-data/bitmap.md` — 使用 BITMAP 对数据去重 — Matrixone 支持使用 [`BITMAP`](../../Reference/Functions-and-Operators/Aggregate-Functions/bitm
- `develop/distinct-data/count-distinct.md` — 使用 COUNT(DISTINCT) 对数据去重 — 本篇文章将介绍如何使用 `COUNT(DISTINCT)` 对少量数据去重。
- `develop/ecological-tools/bi-connection/FineBI-connection.md` — 通过 FineBI 实现 MatrixOne 的可视化报表 — FineBI 是新一代大数据分析工具，它有助于企业的业务人员深入了解和充分利用他们的数据。在 FineBI 中，用户可以轻松地制作多样化的数据可视化信息，自由分析和探索数据。Fin
- `develop/ecological-tools/bi-connection/Superset-connection.md` — 通过 Superset 实现 MatrixOne 的可视化监控 — Superset 是一个开源的、现代的、轻量级 BI 分析工具，能够连接多种数据源、提供丰富的可视化图表，支持自定义仪表盘，帮助用户轻松探索和呈现数据。
- `develop/ecological-tools/bi-connection/yonghong-connection.md` — 通过永洪 BI 实现 MatrixOne 的可视化报表 — 永洪 BI 是一款全面的大数据平台，它整合了自服务数据准备、探索性自助分析、深度分析、企业级管理和高性能计算功能，提供了一站式的大数据解决方案。永洪 BI 的目标是为各种规模的企业
- `develop/ecological-tools/computing-engine/flink/flink-kafka-matrixone.md` — 使用 Flink 将 Kafka 数据写入 MatrixOne — 本章节将介绍如何使用 Flink 将 Kafka 数据写入到 MatrixOne。
- `develop/ecological-tools/computing-engine/flink/flink-mongo-matrixone.md` — 使用 Flink 将 MongoDB 数据写入 MatrixOne — 本章节将介绍如何使用 Flink 将 MongoDB 数据写入到 MatrixOne。
- `develop/ecological-tools/computing-engine/flink/flink-mysql-matrixone.md` — 使用 Flink 将 MySQL 数据写入 MatrixOne — 本章节将介绍如何使用 Flink 将 MySQL 数据写入到 MatrixOne。
- `develop/ecological-tools/computing-engine/flink/flink-oracle-matrixone.md` — 使用 Flink 将 Oracle 数据写入 MatrixOne — 本章节将介绍如何使用 Flink 将 Oracle 数据写入到 MatrixOne。
- `develop/ecological-tools/computing-engine/flink/flink-overview.md` — 概述 — Apache Flink 是一个强大的框架和分布式处理引擎，专注于进行有状态计算，适用于处理无边界和有边界的数据流。Flink 能够在各种常见集群环境中高效运行，并以内存速度执行计
- `develop/ecological-tools/computing-engine/flink/flink-postgresql-matrixone.md` — 使用 Flink 将 PostgreSQL 数据写入 MatrixOne — 本章节将介绍如何使用 Flink 将 PostgreSQL 数据写入到 MatrixOne。
- `develop/ecological-tools/computing-engine/flink/flink-sqlserver-matrixone.md` — 使用 Flink 将 SQL Server 数据写入 MatrixOne — 本章节将介绍如何使用 Flink 将 SQL Server 数据写入到 MatrixOne。
- `develop/ecological-tools/computing-engine/flink/flink-tidb-matrixone.md` — 使用 Flink 将 TiDB 数据写入 MatrixOne — 本章节将介绍如何使用 Flink 将 TiDB 数据写入到 MatrixOne。
- `develop/ecological-tools/computing-engine/spark/spark-doris-matrixone.md` — 使用 Spark 从 Doris 迁移数据至 MatrixOne — 在本章节，我们将介绍使用 Spark 计算引擎实现 Doris 批量数据写入 MatrixOne。
- `develop/ecological-tools/computing-engine/spark/spark-hive-matrixone.md` — 使用 Spark 将 Hive 数据导入到 MatrixOne — 在本章节，我们将介绍使用 Spark 计算引擎实现 Hive 批量数据写入 MatrixOne。
- `develop/ecological-tools/computing-engine/spark/spark-mysql-matrixone.md` — 使用 Spark 从 MySQL 迁移数据至 MatrixOne — 在本章节，我们将介绍使用 Spark 计算引擎实现 MySQL 批量数据写入 MatrixOne。
- `develop/ecological-tools/computing-engine/spark/spark-overview.md` — 概述 — Apache Spark 是一个为高效处理大规模数据而设计的分布式计算引擎。它采用分布式并行计算的方式，将数据拆分、计算、合并的任务分散到多台计算机上，从而实现了高效的数据处理和分
- `develop/ecological-tools/etl/datax/datax-clickhouse-matrixone.md` — 使用 DataX 将 ClickHouse 数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 ClickHouse 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-doris-matrixone.md` — 使用 DataX 将 Doris 数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 Doris 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-elasticsearch-matrixone.md` — 使用 DataX 将 ElasticSearch 数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 ElasticSearch 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-influxdb-matrixone.md` — 使用 DataX 将 InfluxDB 数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 InfluxDB 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-mongodb-matrixone.md` — 使用 DataX 将 MongoDB 数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 MongoDB 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-mysql-matrixone.md` — 使用 DataX 将 MySQL 数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 MySQL 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-oracle-matrixone.md` — 使用 DataX 将数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 Oracle 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-overview.md` — 使用 DataX 将数据写入 MatrixOne — DataX 是一款由阿里开源的异构数据源离线同步工具，提供了稳定和高效的数据同步功能，旨在实现各种异构数据源之间的高效数据同步。
- `develop/ecological-tools/etl/datax/datax-postgresql-matrixone.md` — 使用 DataX 将数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 PostgreSQL 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-sqlserver-matrixone.md` — 使用 DataX 将数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 SQL Server 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/datax/datax-tidb-matrixone.md` — 使用 DataX 将数据写入 MatrixOne — 本文介绍如何使用 DataX 工具将 TiDB 数据离线写入 MatrixOne 数据库。
- `develop/ecological-tools/etl/seatunnel/seatunnel-mysql-matrixone.md` — 使用 SeaTunnel 将 MySQL 数据写入 MatrixOne — 本章节将介绍如何使用 SeaTunnel 将 MySQL 数据写入到 MatrixOne。
- `develop/ecological-tools/etl/seatunnel/seatunnel-oracle-matrixone.md` — 使用 SeaTunnel 将数据写入 MatrixOne — 本文档将介绍如何使用 SeaTunnel 将 Oracle 数据写入 MatrixOne。
- `develop/ecological-tools/etl/seatunnel/seatunnel-overview.md` — 概述 — [SeaTunnel](https://seatunnel.apache.org/) 是一个分布式、高性能、易扩展的数据集成平台，专注于海量数据（包括离线和实时数据）同步和转化。M
- `develop/ecological-tools/message-queue/Kafka.md` — 使用 Kafka 连接 MatrixOne — Apache Kafka 是一个开源的分布式事件流平台，被数千家公司用于高性能数据管道、流分析、数据集成和关键任务应用。
- `develop/ecological-tools/scheduling-tools/dolphinScheduler.md` — 使用 DolphinScheduler 连接 MatrixOne — Apache DolphinScheduler 是一个分布式、易扩展的可视化 DAG 工作流任务调度开源系统。它提供了一种解决方案，可以通过可视化操作任务、工作流和全生命周期的数据
- `develop/export-data/modump.md` — mo-dump 工具写出 — MatrixOne 支持以下两种方式导出数据：
- `develop/export-data/select-into-outfile.md` — SELECT INTO 写出 — MatrixOne 支持以下两种方式导出数据：
- `develop/import-data/bulk-load/bulk-load-overview.md` — 批量导入概述 — MatrixOne 支持使用 `LOAD DATA` 命令将大量行插入至 MatrixOne 数据表，也支持使用 `SOURCE` 命令将表结构和数据导入整个数据库。
- `develop/import-data/bulk-load/load-csv.md` — 插入 csv 文件 — 本篇文档将指导你在 MySQL 客户端连接 MatrixOne 时如何完成 csv 格式数据导入。
- `develop/import-data/bulk-load/load-jsonline.md` — 插入 jsonlines 文件 — 本篇文档将指导你如何将 JSONLines 格式数据（即 jl 或 jsonl 文件）导入 MatrixOne。
- `develop/import-data/bulk-load/load-s3.md` — 从对象存储导入文件 — S3（Simple Storage Service）对象存储是指亚马逊的简单存储服务。你还可以使用与 S3 兼容的对象存储来存储几乎任何类型和大小的数据，包括数据湖、云原生应用程序
- `develop/import-data/bulk-load/using-source.md` — Source 插入 — 本篇文档将指导你使用 `source` 命令批量导入数据至 MatrixOne。
- `develop/import-data/delete-data.md` — 删除数据 — 本文档介绍如何使用 SQL 语句在 MatrixOne 中删除数据。
- `develop/import-data/insert-data.md` — INSERT 插入 — 本文档介绍如何使用 SQL 语句在 MatrixOne 中插入数据。
- `develop/import-data/prepared.md` — 预处理 — MatrixOne 提供对服务器端预处理语句的支持。利用客户端或服务器二进制协议的高效性，对参数值使用带有占位符的语句进行预处理，执行过程中的优点如下：
- `develop/import-data/stream-load.md` — 流式导入 — 本文档介绍如何使用 SQL 语句在 MatrixOne 中进行流式导入数据。具体来说，MatrixOne 支持使用 `LOAD DATA INLINE` 语法对以 csv 格式组织
- `develop/import-data/update-data.md` — 更新数据 — 本文档介绍如何使用 SQL 语句在 MatrixOne 中更新数据。
- `develop/index.md` — 开发指南
- `develop/publish-subscribe/multi-account-overview.md` — 多租户概述 — 与 MySQL 不同，MatrixOne 是一个具备多租户能力的数据库。在一个 MatrixOne 集群中，可以通过使用 `CREATE ACCOUNT` 命令创建租户。这些租户在
- `develop/publish-subscribe/pub-sub-overview.md` — 发布订阅 — 数据库的发布订阅（Publish-Subscribe，简称 Pub/Sub）是一种消息传递模式，其中发布者将消息发送给一个或多个订阅者，而订阅者则接收并处理该消息。在这种模式下，发
- `develop/read-data/cte.md` — 公共表表达式 (CTE) — 公用表表达式（CTE,Common table expression) 是一个命名的临时结果集，仅在单个 SQL 语句 (例如 `SELECT`，`INSERT`，`UPDATE`
- `develop/read-data/multitable-join-query.md` — 多表连接查询 — 一些使用数据库的场景中，需要一个查询当中使用到多张表的数据，你可以通过 `JOIN` 语句将两张或多张表的数据组合在一起。
- `develop/read-data/query-data-single-table.md` — 单表查询 — 本篇文章介绍如何使用 SQL 来对数据库中的数据进行查询。
- `develop/read-data/subquery.md` — 子查询 — 本篇文档向你介绍 MatrixOne 的子查询功能。
- `develop/read-data/views.md` — 视图 — 本篇文档向你介绍 MatrixOne 的视图功能。
- `develop/read-data/window-function/time-window.md` — 时间窗口 — 在时序场景中，数据通常是流式的，流数据通常是无穷无尽的，我们无法知道什么时候数据源会继续/停止发送数据，所以在流上处理聚合事件（count、sum 等）的处理方式与批处理中的处理方
- `develop/read-data/window-function/window-function.md` — 窗口函数 — 窗口函数（Window Function）是一种特殊的函数，它能够在查询结果集的某个窗口（Window）上执行计算操作。窗口函数可以用于对结果集进行分组、排序和聚合操作，同时还能够
- `develop/schema-design/create-database.md` — 创建数据库 — 本篇文档中介绍如何使用 SQL 来创建数据库，及创建数据库时应遵守的规则。
- `develop/schema-design/create-secondary-index.md` — 创建次级索引 — 在非主键上标识的索引，次级索引也称为非聚集索引（non-clustered index），用于提高查询性能和加速数据检索。次级索引并不直接存储表数据，而是对数据的一部分（如某个列）
- `develop/schema-design/create-table-as-select.md` — 使用 CTAS 复制表 — CTAS([Create Table As Select](../../Reference/SQL-Reference/Data-Definition-Language/creat
- `develop/schema-design/create-table.md` — 创建表 — 本篇文档中介绍如何使用 SQL 来创建表。上一篇文档中介绍了创建一个名为 modatabase 的数据库，本篇文档我们介绍在这个数据库中创建一个表。
- `develop/schema-design/create-temporary-table.md` — 创建临时表 — 临时表（temporary table）是一种特殊的表，它在创建后只在当前会话可见。在当前会话结束时，数据库自动删除临时表并释放所有空间，你也可以使用 `DROP TABLE` 删
- `develop/schema-design/create-view.md` — 创建视图 — 视图（View）是一个基于 SQL 语句的结果集的可视化、只读的虚拟表，其内容由查询定义。与普通表（存储数据的表）不同，视图不包含数据，仅仅是基于基表（被查询的表）的查询结果的格式
- `develop/schema-design/data-integrity/auto-increment-integrity.md` — AUTO INCREMENT 自增约束 — 自增约束（Auto-Increment Constraint）是 MatrixOne 一种用于自动为表中的列生成唯一标识值的特性。它允许你在插入新行时，自动为指定的自增列生成一个递
- `develop/schema-design/data-integrity/foreign-key-constraints.md` — FOREIGN KEY 外键约束 — FOREIGN KEY 外键约束允许表内或跨表交叉引用相关数据，有助于保持相关数据的一致性。
- `develop/schema-design/data-integrity/not-null-constraints.md` — NOT NULL 非空约束 — NOT NULL 约束可用于限制一个列中不能包含 NULL 值。
- `develop/schema-design/data-integrity/overview-of-integrity-constraint-types.md` — 约束概述 — 在 MatrixOne 数据库中，为了确保数据的正确性、完整性、有效性，在建表语句中，会对某些列加入限制条件，确保数据库内存储的信息遵从一定的业务规则，这些限制条件被称为约束。例如
- `develop/schema-design/data-integrity/primary-key-constraints.md` — PRIMARY KEY 主键约束 — PRIMARY KEY 约束可用于确保表内的每一数据行都可以由某一个键值唯一地确定。
- `develop/schema-design/data-integrity/unique-key-constraints.md` — UNIQUE KEY 唯一约束 — UNIQUE KEY 约束可用于确保将要被插入或更新的数据行的列或列组的值是唯一的，表的任意两行的某列或某个列集的值不重复，并且唯一键约束也必须非空。
- `develop/schema-design/overview.md` — 数据库模式设计概述 — 本篇文章简要概述了 MatrixOne 的数据库模式。本篇概述主要介绍 MatrixOne 数据库相关术语和后续的数据读写示例。
- `develop/transactions/common-transaction-overview.md` — 事务通用概念 — 在许多大型、关键的应用程序中，计算机每秒钟都在执行大量的任务。更为经常的不是这些任务本身，而是将这些任务结合在一起完成一个业务要求，称为事务。如果能成功地执行一个任务，而在第二个或
- `develop/transactions/matrixone-transaction-overview/explicit-transaction.md` — 显式事务 — 在 MatrixOne 的事务类别中，显式事务还遵循以下规则：
- `develop/transactions/matrixone-transaction-overview/how-to-use.md` — 事务使用指南 — 本章节向你介绍如何简单的开启、提交、回滚一个事务，以及如何自动提交事务。
- `develop/transactions/matrixone-transaction-overview/implicit-transaction.md` — 隐式事务 — 在 MatrixOne 的事务类别中，隐式事务还遵循以下规则：
- `develop/transactions/matrixone-transaction-overview/isolation-level.md` — 隔离级别 — MatrixOne 默认读已提交（Read Committed）隔离级别，它的特点如下：
- `develop/transactions/matrixone-transaction-overview/mvcc.md` — MVCC — MVCC（Multiversion Concurrency Control，多版本并发控制）应用于 MatrixOne，以保证事务快照隔离，实现事务的隔离性。
- `develop/transactions/matrixone-transaction-overview/optimistic-transaction.md` — 乐观事务 — 乐观事务开始时，不会做冲突检测或锁操作，会将当前相关数据缓存至对应内存区域，并对该数据进行增删改。
- `develop/transactions/matrixone-transaction-overview/overview.md` — MatrixOne 的事务概述 — MatrixOne 事务遵循数据库事务的标准定义与基本特征 (ACID)。它旨在帮助用户在分布式数据库环境下，确保每一次数据库数据操作行为，都能够令结果保证数据的一致性和完整性，在
- `develop/transactions/matrixone-transaction-overview/pessimistic-transaction.md` — 悲观事务 — 悲观事务开始时，一定会做冲突检测或锁操作，在未检测到冲突或锁的时候，会将待写数据中的某一列当做主键列，并对该列上锁并创建时间戳。对于此时间戳之后对相关行进行的写入均判定为写冲突。
- `develop/transactions/matrixone-transaction-overview/scenario.md` — 应用场景 — 在一个财务系统中，不同用户之间的转账是非常常见的场景，而转账在数据库中的实际操作，通常是两个步骤，首先是对一个用户的账面金额抵扣之后，然后是对另一个用户的账面金额进行增加。只有利用
- `develop/udf/udf-python-advanced.md` — UDF-Python-进阶 — 本篇文档将指导你如何使用 UDF 进阶功能，包括以 phython 文件、whl 包构建 UDF。
- `develop/udf/udf-python.md` — UDF-Python — 您可以使用 Python 编写用户自定义函数 (UDF) 的处理程序。本篇文档将指导你如何创建一个简单 Python UDF，包括使用环境要求、UDF 创建、查看、使用和删除。
- `develop/vector/cluster_centers.md` — 聚类中心 — 在使用聚类算法，特别是 K-means 算法时，聚类数量 K 代表了你想要将数据集分成的簇（cluster）的数量。每个簇由其聚类中心（centroid）代表，聚类中心是簇内所有数
- `develop/vector/vector_index.md` — 向量索引 — 向量索引是一种用于在高维向量空间中快速查找和检索数据的技术，通常用于处理大规模的向量数据集。向量索引的核心目的是在大量向量中高效地找到与查询向量相似的向量，常用于应用场景如图像检索
- `develop/vector/vector_search.md` — 向量检索 — 向量检索就是在一个给定向量数据集中，按照某种度量方式，检索出与查询向量相近的 K 个向量（K-Nearest Neighbor，KNN）。这是一种在大规模高维向量数据中寻找与给定查
- `develop/vector/vector_type.md` — 向量类型 — 在数据库中，向量通常是一组数字，它们以特定的方式排列，以表示某种数据或特征。这些向量可以是一维数组、多维数组或具有更高维度的数据结构。在机器学习和数据分析领域中，向量用于表示数据点

### 部署指南  `(deploy/, 15 篇)`
> 集群部署 / 单机部署 / 部署拓扑 / Operator

- `deploy/MatrixOne-Operator-mgmt.md` — Operator 管理 — [MatrixOne Operator](https://github.com/matrixorigin/matrixone-operator) 用来定义和管理 MatrixOne
- `deploy/MatrixOne-cluster-Scale.md` — 集群扩缩容 — 本篇文档将介绍 MatrixOne 集群如何进行扩缩容，并包括 Kubernetes 集群本身的扩缩容与 MatrixOne 的各个服务的扩缩容。
- `deploy/MatrixOne-start-stop.md` — 启动与停服下线 — 本篇文档将介绍如何启停分布式 MatrixOne 集群。
- `deploy/deploy-matrixone-cluster/deploy-MatrixOne-cluster-with-k8.md` — 集群部署指南 — 本篇文档将主要讲述如何在已存在 Kubernetes 和 S3 环境的基础上部署一个 MatrixOne 集群。
- `deploy/deploy-matrixone-cluster/deploy-MatrixOne-cluster-without-k8.md` — 集群部署指南 — 本篇文档将主要讲述如何从 0 开始部署一个基于私有化 Kubernetes 集群的云原生存算分离的分布式数据库 MatrixOne。
- `deploy/deploy-matrixone-single-with-s3.md` — 基于 S3 部署一个单机的 MatrixOne — 本文提供一个示例，旨在说明如何基于 S3 部署一个单机的 MatrixOne。区别于一般的单机部署方式，这种方式使用 S3 作为 MatrixOne 的存储介质，而不是直接采用宿主
- `deploy/deployment-topology/experience-deployment-topology.md` — 体验环境 — 本篇文档介绍的 MatrixOne 体验环境部署规划可以用于体验 MatrixOne 的分布式基础能力，你可以简单体验数据库的基础开发、运维等功能，但是不适用于部署生产环境，进行性
- `deploy/deployment-topology/minimal-deployment-topology.md` — 最小生产环境 — 本篇文章介绍的 MatrixOne 分布式集群的最小生产配置可以用于生产环境，可以支撑千万级数据数百并发的 OLTP 业务，或者数十 GB 数据量的 OLAP 业务，同时有一定的高
- `deploy/deployment-topology/recommended-prd-deployment-topology.md` — 推荐生产环境 — 本篇文档介绍的 MatrixOne 分布式集群的推荐配置适用于生产环境，并具备强大的性能和可靠性。这种配置可以支持亿级数据的数千并发 OLTP 业务，或者处理数十 TB 数据量的 
- `deploy/deployment-topology/topology-overview.md` — MatrixOne 集群拓扑概述 — MatrixOne 数据库集群是一种在多个物理或虚拟服务器上分布式部署数据库系统的架构，旨在提供高可用性、高可伸缩性。通过将数据库分散到多台服务器上，集群可以实现数据的冗余备份、负
- `deploy/health-check-resource-monitoring.md` — 健康检查与资源监控 — 在 MatrixOne 分布式集群中，包含了多个组件和对象，为了确保其正常运行并排除故障，我们需要进行一系列的健康检查和资源监控。
- `deploy/import-data-from-minio-to-mo.md` — 本地对象存储导入导入数据 — 在 MatrixOne 分布式集群中，除了本地导入数据和从公有云对象存储 S3 导入数据到 MatrixOne，还可以通过本地 Minio 组件导入数据。
- `deploy/index.md` — 部署指南
- `deploy/mgmt-cn-group-using-proxy.md` — 负载与租户隔离 — Proxy 是 MatrixOne 在 0.8 版本中引进的新系统组件，它可以通过流量代理和转发的方式实现租户、负载隔离等功能。关于 Proxy 的技术设计，可以参考 [Proxy
- `deploy/update-MatrixOne-cluster.md` — 版本升级 — 本篇文档将介绍如何滚动升级或者重装升级 MatrixOne 集群。

### 运维  `(maintain/, 14 篇)`
> 启停 / 备份 / 健康检查 / 故障切换 / 缩扩容

- `maintain/backup-restore/active-standby.md` — MatrixOne 主备容灾功能 — MatrixOne 支持基于日志复制的主备集群冷备功能，通过实时同步主数据库的事务日志到备库，保障主备数据的一致性和高可用性。在主库出现故障时，备库可以快速接管业务，确保不中断；故
- `maintain/backup-restore/backup-restore-overview.md` — MatrixOne 备份与恢复概述 — 数据库备份与恢复是任何数据库管理系统的核心操作之一，也是数据安全与可用性的重要保障。MatrixOne 也提供了灵活且强大的数据库备份与恢复功能，以确保用户数据的完整性和持续性。本
- `maintain/backup-restore/key-concepts.md` — 备份与恢复相关概念 — 物理备份是将数据库文件直接复制到备份介质（如磁带、硬盘等）上的过程。此方式将数据库的所有物理数据块复制到备份介质，包括数据文件、控制文件和重做日志文件等。备份的数据是实际存储在磁盘
- `maintain/backup-restore/mobr-backup-restore/mobr-physical-backup-restore.md` — 原理概述 — 数据库常规物理备份是直接复制数据库的物理存储文件，包括数据文件、日志文件和控制文件等，以创建数据库的一个独立副本。这一过程通常在文件系统级别进行，可以通过操作系统的命令实现，生成的
- `maintain/backup-restore/mobr-backup-restore/mobr-pitr-backup-restore.md` — mo_br 工具进行 PITR 备份恢复 — PITR（时间点恢复）备份恢复的实现基于完整备份和增量日志，通过记录数据库的事务操作并应用这些增量日志，系统可以将数据库恢复到指定的时间点。恢复过程首先从完整备份开始，将数据库还原
- `maintain/backup-restore/mobr-backup-restore/mobr-snapshot-backup-restore.md` — mo_br 工具进行快照备份恢复 — 数据库快照备份恢复通过创建数据库在特定时间点的只读静态视图，这个视图被称为快照。快照利用存储系统的写时复制（COW）技术，仅在原始数据页被修改前复制并存储该页，从而生成数据库在快照
- `maintain/backup-restore/mobr-backup-restore/mobr.md` — mo_br 备份与恢复 — 数据库物理备份和快照备份是两种重要的数据保护策略，它们在很多场景下都发挥着重要的作用。物理备份通过复制数据库的物理文件，如数据文件和日志文件，能够实现快速和完整的数据库恢复，特别适
- `maintain/backup-restore/modump-backup-restore.md` — mo-dump 备份与恢复 — 对于企业而言，每天都会产生大量数据，那么对于数据库的备份就非常重要。在系统崩溃或者硬件故障，又或者用户误操作的情况下，你可以恢复数据并重启系统，不会造成数据丢失。
- `maintain/cdc/mo-mo.md` — MatrixOne 到 MatrixOne CDC 功能 — 一家社交平台企业使用 MatrixOne 作为生产数据库存储用户活动日志（如登录、点赞、评论等）。为了支持实时分析（如活跃用户统计、行为趋势等），需要将用户活动数据从生产 Matr
- `maintain/cdc/mo-mysql.md` — MatrixOne 到 MySQL CDC 功能 — 一家在线零售企业使用 MatrixOne 作为订单管理系统的生产数据库，用于存储订单数据。为了支持业务的实时分析需求（如订单数量、销售趋势、客户行为等），需要将订单数据从 Matr
- `maintain/cdc/mocdc.md` — mo_cdc 数据同步 — CDC（Change Data Capture）是一种实时捕获数据库中数据变更的技术，能够记录插入、更新和删除操作。它通过监控数据库的变更，实现数据的实时同步和增量处理，确保不同系
- `maintain/index.md` — 运维
- `maintain/mo-directory-structure.md` — MatrixOne 目录结构 — 完成 MatrixOne 搭建和连接后，首次执行时，MatrixOne 会自动生成以下目录，用于存放各类数据文件或元数据信息。
- `maintain/mount-data-by-docker.md` — 挂载目录到 Docker 容器 — 本篇文档将指导你在使用 Docker 启动 MatrixOne 的情况下，如何挂载数据目录或自定义配置文件到 Docker 容器。

### 数据迁移  `(migrate/, 6 篇)`
> 从其它库迁入 MatrixOne

- `migrate/index.md` — 数据迁移
- `migrate/migrate-from-mysql-to-matrixone.md` — 将数据从 MySQL 迁移至 MatrixOne — 本篇文档将指导你如何将数据从 MySQL 迁移至 MatrixOne。
- `migrate/migrate-from-oracle-to-matrixone.md` — 将数据从 Oracle 迁移至 MatrixOne — 本篇文档将指导你如何将数据从 Oracle 迁移至 MatrixOne。
- `migrate/migrate-from-postgresql-to-matrixone.md` — 将数据从 PostgreSQL 迁移至 MatrixOne — 本篇文档将指导你如何将数据从 PostgreSQL 迁移至 MatrixOne。
- `migrate/migrate-from-sqlserver-to-matrixone.md` — 将数据从 SQL Server 迁移至 MatrixOne — 本篇文档将指导你如何将数据从 SQL Server 迁移至 MatrixOne。
- `migrate/migrate-overview.md` — 将数据迁移至 MatrixOne 概述 — 在使用 MatrixOne 时，有时需要将数据从其他数据库迁移至 MatrixOne。由于不同数据库之间存在差异，数据迁移需要一些额外的工作。为了方便用户快速导入外部数据，Matr

### 测试  `(test/, 6 篇)`
> TPC-H / SSB benchmark + mo-tester

- `test/index.md` — 测试
- `test/performance-testing/SSB-test-with-matrixone.md` — 完成 SSB 测试 — SSB 星型模式基准测试是 OLAP 数据库性能测试的常用场景，通过本篇教程，您可以了解到如何在 MatrixOne 中实现 SSB 测试。
- `test/performance-testing/TPCC-test-with-matrixone.md` — 完成 TPC-C 测试 — 通过阅读本教程，你将学习如何使用 MatrixOne 完成 TPC-C 测试。
- `test/performance-testing/TPCH-test-with-matrixone.md` — 完成 TPCH 测试 — TPC Benchmark™H（TPC-H）是决策支持基准。它由一套面向业务的即时查询（ad-hoc）和并发数据修改组成。选择查询和填充数据库的数据具有广泛的行业相关性。该基准测试
- `test/testing-tool/mo-tester-reference.md` — MO-Tester 规范要求 — 有时，为了达到特定的目的，如暂停或创建新连接，您可以向脚本文件添加特殊的标记。Mo tester 提供以下标签供使用：
- `test/testing-tool/mo-tester.md` — MO-Tester 简介 — 从 0.5.0 版本开始，MatrixOne 引入了一个自动测试框架 [MO-Tester](https://github.com/matrixorigin/mo-tester)。

### 性能调优  `(performance-tuning/, 12 篇)`
> 执行计划 / 分区 / 索引 / 配置参数

- `performance-tuning/explain/explain-aggregation.md` — 用 EXPLAIN 查看聚合查询执行计划 — SQL 查询中可能会使用聚合计算，可以通过 EXPLAIN 语句来查看聚合查询的执行计划。
- `performance-tuning/explain/explain-joins.md` — 用 EXPLAIN 查看 JOIN 查询的执行计划 — SQL 查询中可能会使用 JOIN 进行表连接，可以通过 EXPLAIN 语句来查看 JOIN 查询的执行计划。
- `performance-tuning/explain/explain-overview.md` — MatrixOne 执行计划概述 — 执行计划（execution plan，也叫查询计划或者解释计划）是数据库执行 SQL 语句的具体步骤，例如通过索引还是全表扫描访问表中的数据，连接查询的实现方式和连接的顺序等；执
- `performance-tuning/explain/explain-subqueries.md` — 用 EXPLAIN 查看子查询的执行计划 — MatrixOne 会执行多种子查询相关的优化，以提升子查询的执行性能。本文档介绍一些常见子查询的优化方式，以及如何解读 EXPLAIN 语句返回的执行计划信息。
- `performance-tuning/explain/explain-views.md` — 用 EXPLAIN 查看带视图的 SQL 执行计划 — 我们这里准备一个简单的示例，帮助你理解使用 EXPLAIN 解读 VIEW 的执行计划。
- `performance-tuning/explain/explain-walkthrough.md` — 使用 EXPLAIN 解读执行计划 — SQL 是一种声明性语言，因此无法通过 SQL 语句直接判断一条查询的执行是否有效率，但是可以使用 `EXPLAIN` 语句查看当前的执行计划。
- `performance-tuning/index.md` — 性能调优
- `performance-tuning/optimization-concepts/through-CN-extensions.md` — 通过扩展 CN 提升性能 — MatrixOne 是一种分布式数据库，最显著的特点是可以通过节点扩展来提升系统整体性能。在 MatrixOne 的存算分离架构中，CN 是无状态的计算节点，快速扩展 CN 节点是
- `performance-tuning/optimization-concepts/through-cluster-by.md` — 使用 Cluster by 语句调优 — 以下是使用 `Cluster by` 的一些注意事项：
- `performance-tuning/optimization-concepts/through-partition/through-partition-by.md` — 使用分区表调优 — 分区表是数据库中的一种数据组织方法，即是一种表分割方法，它将表数据分散到多个分区中，每个分区相当于一个独立的小表。
- `performance-tuning/optimization-concepts/through-partition/through-partition-pruning.md` — 分区裁剪 — 分区裁剪（Partition Pruning）是数据库查询优化的一个过程，它能够识别并排除那些不必要的分区，从而减少查询需要扫描的数据量。当执行一个查询时，如果查询条件与表的分区键
- `performance-tuning/performance-tuning-overview.md` — SQL 性能调优方法概述 — SQL 性能调优是一种优化数据库查询和操作的过程，旨在提高数据库的性能和响应时间。常见的几种性能调优方式如下：

### 安全与权限  `(security/, 12 篇)`
> 账号管理 / RBAC / 审计 / 加密

- `security/Authentication.md` — 身份鉴别与认证 — 用户在访问 MatrixOne 数据库时需要进行身份鉴别与认证，目前 MatrixOne 仅支持用户名密码验证方式登录。数据库会对访问数据的用户进行身份验证，确认该用户是否能够与某
- `security/Security-Permission-Overview.md` — 安全与权限概述 — 数据库安全和权限是确保数据库系统及其中存储的数据受到保护和管理的关键方面。它涉及一系列策略、措施和权限控制，以确保只有经过授权的用户能够访问、修改和操作数据库。本章节将为您介绍 M
- `security/TLS-introduction.md` — 数据传输加密 — 本篇文档将介绍 MatrixOne 对数据传输加密的支持情况以及如何开始加密传输。
- `security/audit.md` — 安全审计 — 本文档对 MatrixOne 安全审计基本功能进行阐述，并指引如何开启和使用。
- `security/how-tos/quick-start-create-account.md` — 创建租户，验证资源隔离 — 初始化接入 MatrixOne 集群，系统会自动生成一个默认账号，即集群管理员。集群管理员被自动默认赋予管理租户账号的权限，但不能管理租户下的资源。
- `security/how-tos/quick-start-create-user.md` — 创建新租户，并由新租户创建用户、创建角色和授权 — 初始化接入 MatrixOne 集群，系统会自动生成一个默认账号，即集群管理员。集群管理员默认用户名为 root，root 既是集群管理员，同时也是系统租户管理员，root 可以创
- `security/how-tos/user-guide.md` — 权限管理操作概述 — 有关 root 账号对应的角色和权限如下表所示：
- `security/index.md` — 安全与权限
- `security/password-mgmt.md` — 密码管理 — 为了保护用户密码的安全，MatrixOne 支持密码管理能力：
- `security/role-priviledge-management/about-privilege-management.md` — 权限管理概述 — MatrixOne 权限管理帮助你管理租户、用户帐号生命周期，分配给用户相应的角色，控制 MatrixOne 中资源的访问权限。当数据库或集群单位中存在多个用户时，权限管理确保用户
- `security/role-priviledge-management/app-scenarios.md` — 权限管理应用场景 — 在实际应用场景中，需要设立一个数据管理员的岗位，他负责管理整个数据库中资源分配的情况，比如说，公司其他成员需要被分配一个用户账号和密码，被分配角色，并被授予最低的使用权限。
- `security/role-priviledge-management/best-practice.md` — 最佳实践 — 以下是 MatrixOne 中的典型角色以及建议的最低权限，供你进行参考。

### 参考手册(SQL Reference)  `(sql-reference/, 364 篇)`
> DDL / DML / DCL / DQL / 函数 / 数据类型 / 系统变量

#### functions-and-operators/  (150 篇)
  - `sql-reference/functions-and-operators/aggregate-functions/any-value.md` — ANY_VALUE — 返回类型和输入类型相同。
  - `sql-reference/functions-and-operators/aggregate-functions/avg.md` — AVG — 以 `Double` 类型返回该列的算术平均值。
  - `sql-reference/functions-and-operators/aggregate-functions/bit_and.md` — BIT_AND — BIT_AND() 是一个聚合函数，计算了列中所有位的按位与。
  - `sql-reference/functions-and-operators/aggregate-functions/bit_or.md` — BIT_OR — BIT_OR() 是一个聚合函数，计算了列中所有位的按位或。
  - `sql-reference/functions-and-operators/aggregate-functions/bit_xor.md` — BIT_XOR — BIT_XOR() 是一个聚合函数，计算了列中所有位的按位异或。
  - `sql-reference/functions-and-operators/aggregate-functions/bitmap.md` — BITMAP 函数 — 我们可以只使用一个 bit 位标识一个元素的存在与否，存在为 1，不存在则为 0，用 bitmap 的第 n 个 bit 来记录这个元素是否存在。
  - … 及其余 144 篇(同一类 SQL 命令的参考页)

#### sql-reference/  (119 篇)
  - `sql-reference/sql-reference/SQL-Type.md` — SQL 语句的分类 — 在 MatrixOne 中，SQL 语句包含多种分类，每一种分类的定义与包含内容按照如下描述的每个部分所展示：
  - `sql-reference/sql-reference/data-control-language/alter-account.md` — ALTER ACCOUNT — 修改租户信息。
  - `sql-reference/sql-reference/data-control-language/alter-user.md` — ALTER USER — 修改数据库用户的属性和密码。
  - `sql-reference/sql-reference/data-control-language/create-account.md` — CREATE ACCOUNT — 为其中一个集群成员创建一个新的租户。
  - `sql-reference/sql-reference/data-control-language/create-role.md` — CREATE ROLE — 在系统中创建一个新角色。
  - `sql-reference/sql-reference/data-control-language/create-user.md` — CREATE USER — 在系统中创建一个新的用户。
  - … 及其余 113 篇(同一类 SQL 命令的参考页)

#### operators/  (58 篇)
  - `sql-reference/operators/interval.md` — INTERVAL — 你可以在 `expr` 中使用任何标点分隔符。上表所示为建议的分隔符。
  - `sql-reference/operators/operators/arithmetic-operators/addition.md` — +
  - `sql-reference/operators/operators/arithmetic-operators/arithmetic-operators-overview.md` — 算数运算符概述 — — 对于 `-`、`+` 和 ``，如果两个运算数值都是整数，计算结果将以 BIGINT (64 位) 精度计算。
  - `sql-reference/operators/operators/arithmetic-operators/div.md` — DIV — 如果两个运算数值都是非整数类型，则会将运算数值转换为 `DECIMAL`，并在将结果转换为 `BIGINT` 之前使用 `DECIMAL` 算法进行除法。如果结果超出 `BIGIN
  - `sql-reference/operators/operators/arithmetic-operators/division.md` — / — 除法运算不可以除以 O。
  - `sql-reference/operators/operators/arithmetic-operators/minus.md` — -
  - … 及其余 52 篇(同一类 SQL 命令的参考页)

#### data-types/  (11 篇)
  - `sql-reference/data-types/blob-text-type.md` — BLOB 和 TEXT 数据类型 — BLOB
  - `sql-reference/data-types/data-type-conversion.md` — 数据类型转换 — MatrixOne 支持不同数据类型之间的转换，下表列出了数据类型转换支持情况：
  - `sql-reference/data-types/data-types.md` — 数据类型 — MatrixOne 的数据类型与 MySQL 数据类型的定义一致，可参考：
  - `sql-reference/data-types/datalink-type.md` — DATALINK 类型 — 使用 `DATALINK` 数据类型可以：
  - `sql-reference/data-types/date-time-data-types/timestamp-initialization.md` — TIMESTAMP 和 DATETIME 的自动初始化和更新 — 对于表中的任何 `TIMESTAMP` 或 `DATETIME` 列，你可以将当前时间戳指定为默认值、自动更新值或两者均可：
  - `sql-reference/data-types/date-time-data-types/year-type.md` — YEAR 类型 — YEAR 类型是用于表示年份值的 1 字节类型。可以声明为 YEAR，其隐式显示宽度为 4 个字符，或等效地声明为 `YEAR(4)`，显式指定显示宽度为 4。
  - … 及其余 5 篇(同一类 SQL 命令的参考页)

#### variable/  (11 篇)
  - `sql-reference/variable/custom-variable.md` — 自定义变量 — 在 MatrixOne 中，自定义变量是一种用于存储和操作值的机制。自定义变量可以通过 `SET` 语句设置，并且可以在整个会话期间保持值不变。你可以通过 `SET` 命令进行变量
  - `sql-reference/variable/system-variables/foreign_key_checks.md` — 外键约束检查 — 在 MatrixOne 中，`foreign_key_checks` 是一个系统变量，用于控制外键约束的检查。这个变量可以是全局的，也可以是会话级别的。当设置为 1（默认值）时，M
  - `sql-reference/variable/system-variables/illegal_login_restrictions.md` — 非法登录限制 — 在数据安全日益重要的今天，合理的连接控制和密码管理策略是数据库防护的关键。MatrixOne 提供了一系列全局参数，旨在加强连接安全和密码管理，防止恶意攻击和未授权访问。
  - `sql-reference/variable/system-variables/keep_user_target_list_in_result.md` — keep_user_target_list_in_result 保持查询结果集列名与用户指定大小写一致 — 在 MatrixOne 查询中，保持结果集列名与用户指定的名称大小一致，除了可以通过使用别名（alias）来实现，还可以通过设置参数来实现。
  - `sql-reference/variable/system-variables/lower_case_tables_name.md` — lower_case_table_names 大小写敏感支持 — 与 mysql 不同的是，MatrixOne 暂时只支持 0 和 1 两种模式，且在 linux 和 mac 系统下默认值都为 1。
  - `sql-reference/variable/system-variables/password_complex.md` — 密码复杂度校验 — MatrixOne 提供一系列系统变量用于配置密码复杂度校验，以确保密码安全性。这些变量支持动态修改，其中核心变量为 validate_password，其余设置仅在 valida
  - … 及其余 5 篇(同一类 SQL 命令的参考页)

#### mo-tools/  (6 篇)
  - `sql-reference/mo-tools/mo_ctl.md` — mo_ctl 分布式版工具指南 — mo_ctl 分布式版是一款专为企业级用户设计的高效数据库集群管理工具。如需获取该工具的下载路径，请与您的 MatrixOne 客户经理取得联系。
  - `sql-reference/mo-tools/mo_ctl_standalone.md` — mo_ctl 单机版工具指南 — 根据您是否有互联网访问权限，可以选择在线或离线安装 `mo_ctl` 工具，你需要注意始终以 root 或具有 sudo 权限执行命令（并在每个命令前添加 sudo）。同时，`in
  - `sql-reference/mo-tools/mo_datax_writer.md` — mo_datax_writer 工具指南 — 在 datax/job 目录下添加 datax 配置文件 mysql2mo.json，内容如下：
  - `sql-reference/mo-tools/mo_ssb_open.md` — mo_ssb_open 工具指南 — -s：表示产生大约 1GB 的数据集，不指定参数，默认生成 100G 数据，
  - `sql-reference/mo-tools/mo_tpch_open.md` — mo_tpch_open 工具指南 — 使用以下命令生成数据集：
  - `sql-reference/mo-tools/mo_ts_perf_test.md` — mo_ts_perf_test 工具指南 — 根据实际情况修改 matrixone/conf 目录下的 db.conf 配置文件

#### system-parameters/  (3 篇)
  - `sql-reference/system-parameters/distributed-configuration-settings.md` — 分布式版通用参数配置 — 在 matrixone/etc/launch-with-proxy/ 目录下，有四个配置文件：cn.toml、tn.toml、proxy.toml 和 log.toml。这些配置文
  - `sql-reference/system-parameters/standalone-configuration-settings.md` — 单机版通用参数配置 — 在 matrixone/etc/launch/ 目录下有四个配置文件：cn.toml、tn.toml、proxy.toml 和 log.toml，用于配置通用参数。
  - `sql-reference/system-parameters/system-parameter.md` — 系统参数概述 — 在 MatrixOne 中，涉及多种数据库系统参数，其中一部分以配置文件的方式进行设置，仅在启动时生效，这类参数被称为静态参数。

#### language-structure/  (2 篇)
  - `sql-reference/language-structure/comment.md` — 注释 — 本文档介绍 MatrixOne 支持的注释语法。
  - `sql-reference/language-structure/keywords.md` — 关键字 — 本章介绍 MatrixOne 的关键字，在 MatrixOne 中对保留关键字和非保留关键字进行了分类，你在使用 SQL 语句时，可以查阅保留关键字和非保留关键字。

#### System-tables.md/  (1 篇)
  - `sql-reference/System-tables.md` — MatrixOne 系统数据库和表 — MatrixOne 系统数据库和表是 MatrixOne 存储系统信息的地方，你可以通过它们访问系统信息。MatrixOne 在初始化时创建了 6 个系统数据库：`mo_catal

#### access-control-type.md/  (1 篇)
  - `sql-reference/access-control-type.md` — MatrixOne 权限分类 — 本篇文章主要介绍 MatrixOne 中的权限分类。

#### index.md/  (1 篇)
  - `sql-reference/index.md` — 参考手册

#### limitations/  (1 篇)
  - `sql-reference/limitations/mo-jdbc-feature-list.md` — MatrixOne 的 JDBC 功能支持列表 — 使用 JDBC 开发应用，MatrixOne 支持以下类和对象：

### 故障诊断  `(troubleshooting/, 5 篇)`
> 错误码 / 慢查询 / 表统计

- `troubleshooting/common-statistics-query.md` — 常用统计数据查询 — 统计数据是数据库在运维使用的过程中周期性进行的常用查询，可以帮助数据库用户较为直观准确地掌握当前数据库的状态以及健康程度。
- `troubleshooting/error-code.md` — 错误码 — 在 MatrixOne 中，错误信息是根据错误编码进行分类，某一类的错误编码会统一至一个确定的错误编码中，以便于用户进行排查。MatrixOne 数据库服务所发出的所有消息都分配有
- `troubleshooting/index.md` — 故障诊断
- `troubleshooting/query-table-statistics.md` — MatrixOne 数据库统计信息 — MatrixOne 数据库统计信息是指数据库通过采样、统计出来的表、列的相关信息，例如，表的个数、表的列数、表所占的存储空间等。MatrixOne 数据库在生成执行计划时，需要根据
- `troubleshooting/slow-queries.md` — 慢查询 — 慢查询，即在日志中记录运行比较慢的 SQL 语句。慢查询记录在慢查询日志中，通过慢查询日志，可以查找出哪些查询语句的执行效率低，以便进行优化。

### 常见问题  `(faqs/, 4 篇)`
> 部署 / 产品 / SQL 三大主题

- `faqs/deployment-faqs.md` — 部署常见问题 — 部署 MatrixOne 所需的操作系统版本是什么？
- `faqs/index.md` — 常见问题解答
- `faqs/product-faqs.md` — 产品常见问题 — 什么是 MatrixOne？
- `faqs/sql-faqs.md` — SQL 常见问题 — MatrixOne 对标识符大小写敏感吗？

### 版本发布  `(release-notes/, 34 篇)`
> 每个 release 的特性 / 优化 / 修复

- `release-notes/index.md` — 版本发布纪要
- `release-notes/release-timeline.md` — MatrixOne 版本发布历史记录 — 本文列出了所有已发布的 MatrixOne 版本，按发布时间倒序排列呈现。
- `release-notes/v21.0.1.0.md` — MatrixOne v21.0.1.0 Release Notes — 热烈祝贺 MatrixOne 的 v21.0.1.0 版本于 2021 年 10 月 24 日正式发布！
- `release-notes/v22.0.2.0.md` — MatrixOne v22.0.2.0 发布报告 — 热烈祝贺 MatrixOne 的 v22.0.2.0 版本于 2022 年 1 月 6 日正式发布！以下我们将对版本最新的更新内容进行陈列。
- `release-notes/v22.0.3.0.md` — MatrixOne v22.0.3.0 发布报告 — 热烈祝贺 MatrixOne 的 v22.0.3.0 版本于 2022 年 3 月 10 日正式发布！以下我们将对版本最新的更新内容进行陈列。
- `release-notes/v22.0.4.0.md` — MatrixOne v22.0.4.0 发布报告 — 热烈祝贺 MatrixOne 的 v22.0.4.0 版本于 2022 年 5 月 5 日正式发布！以下我们对版本最新的更新内容进行简要说明。
- `release-notes/v22.0.5.0.md` — MatrixOne v22.0.5.0 发布报告 — 热烈祝贺 MatrixOne 的 v22.0.5.0 版本于 2022 年 7 月 18 日正式发布！在这个版本中，MatrixOne 拥有一个独立的列式存储引擎，可以支持 HTA
- `release-notes/v22.0.5.1.md` — MatrixOne v22.0.5.1 发布报告 — 热烈祝贺 MatrixOne 的 v22.0.5.1 版本于 2022 年 8 月 19 日正式发布！在这个版本中，MatrixOne 解决了一些日志回放和存储垃圾收集（GC，Ga
- `release-notes/v22.0.6.0.md` — MatrixOne v22.0.6.0 发布报告 — 热烈祝贺 MatrixOne 的 v22.0.6.0 版本于 2022 年 11 月 29 日正式发布！在这个版本中，MatrixOne 已升级为存算分离、读写分离、冷热分离、事务
- `release-notes/v23.0.7.0.md` — MatrixOne v23.0.7.0 发布报告 — 热烈祝贺 MatrixOne 的 v23.0.7.0 版本于 2023 年 2 月 23 日正式发布！在这个版本中，MatrixOne 在云原生架构和完整数据库功能形态下，版本 0
- `release-notes/v23.0.8.0.md` — MatrixOne v23.0.8.0 发布报告 — 热烈祝贺 MatrixOne 的 v23.0.8.0 版本于 2023 年 6 月 30 日正式发布！
- `release-notes/v23.1.0.0-rc1.md` — MatrixOne v23.1.0.0-RC1 发布报告 — 我们非常高兴地宣布 MatrixOne 内核 v23.1.0.0-RC1 版本于 2023 年 8 月 24 日正式发布！
- `release-notes/v23.1.0.0-rc2.md` — MatrixOne v23.1.0.0-RC2 发布报告 — 与之前的 v23.1.0.0-RC1 相比，v23.1.0.0-RC2 没有引入任何新功能，而是专注于一些改进和错误修复。
- `release-notes/v23.1.0.0.md` — MatrixOne v23.1.0.0 发布报告 — 发布日期：2023 年 11 月 13 日
- `release-notes/v23.1.0.1.md` — MatrixOne v23.1.0.1 发布报告 — 发布日期：2023 年 12 月 16 日
- `release-notes/v23.1.0.2.md` — MatrixOne v23.1.0.2 发布报告 — 发布日期：2023 年 12 月 23 日
- `release-notes/v23.1.1.0.md` — MatrixOne v23.1.1.0 发布报告 — 我们非常高兴地宣布 MatrixOne 内核 v23.1.1.0 版本于 2023 年 12 月 29 日正式发布！
- `release-notes/v24.1.1.1.md` — MatrixOne v24.1.1.1 发布报告 — 发布日期：2024 年 02 月 04 日
- `release-notes/v24.1.1.2.md` — MatrixOne v24.1.1.2 发布报告 — 发布日期：2024 年 04 月 02 日
- `release-notes/v24.1.1.3.md` — MatrixOne v24.1.1.3 发布报告 — 发布日期：2024 年 04 月 16 日
- `release-notes/v24.1.2.0.md` — MatrixOne v24.1.2.0 发布报告 — 我们非常高兴地宣布 MatrixOne 内核 v24.1.2.0 版本于 2024 年 05 月 20 日正式发布！
- `release-notes/v24.1.2.1.md` — MatrixOne v24.1.2.1 发布报告 — 发布日期：2024 年 06 月 30 日
- `release-notes/v24.1.2.2.md` — MatrixOne v24.1.2.2 发布报告 — 发布日期：2024 年 07 月 12 日
- `release-notes/v24.1.2.3.md` — MatrixOne v24.1.2.3 发布报告 — 发布日期：2024 年 09 月 11 日
- `release-notes/v24.1.2.4.md` — MatrixOne v24.1.2.4 发布报告 — 发布日期：2024 年 09 月 23 日
- `release-notes/v24.2.0.0.md` — MatrixOne v24.2.0.0 发布报告 — 我们非常高兴地宣布 MatrixOne 内核 v24.2.0.0 版本于 2024 年 11 月 01 日正式发布！
- `release-notes/v24.2.0.1.md` — MatrixOne v24.2.0.1 发布报告 — 发布日期：2024 年 12 月 10 日
- `release-notes/v25.2.0.2.md` — MatrixOne v24.2.0.2 发布报告 — 发布日期：2025 年 01 月 25 日
- `release-notes/v25.2.0.3.md` — MatrixOne v25.2.0.3 发布报告 — 发布日期：2025 年 03 月 12 日
- `release-notes/v25.2.1.0.md` — MatrixOne v25.2.1.0 Release Note — 我们非常高兴地宣布 MatrixOne 内核 v25.2.1.0 版本于 2025 年 04 月 06 日正式发布！
- `release-notes/v25.2.1.1.md` — MatrixOne v25.2.1.1 发布报告 — 发布日期：2025 年 05 月 08 日
- `release-notes/v25.2.2.0.md` — MatrixOne v25.2.2.0 发布报告 — 发布日期：2025 年 06 月 18 日
- `release-notes/v25.2.2.1.md` — MatrixOne v25.2.2.1 发布报告 — 发布日期：2025 年 07 月 13 日
- `release-notes/v25.2.2.2.md` — MatrixOne v25.2.2.2 发布报告 — 发布日期：2025 年 7 月 17 日

### 教程  `(tutorial/, 15 篇)`
> CRUD demo / HTAP demo / dify demo

- `tutorial/c-net-crud-demo.md` — C# 基础示例 — 本篇文档将指导你如何使用 C# 构建一个简单的应用程序，并实现 CRUD（创建、读取、更新、删除）功能。
- `tutorial/develop-golang-crud-demo.md` — Golang 基础示例
- `tutorial/develop-java-crud-demo.md` — Java 基础示例 — 本篇文档所介绍的演示程序的源代码下载地址为：[Java CRUD 示例](https://github.com/matrixorigin/matrixone_java_crud_e
- `tutorial/develop-python-crud-demo.md` — Python 基础示例 — 本篇文档将指导你如何使用 Python 构建一个简单的应用程序，并实现 CRUD（创建、读取、更新、删除）功能。
- `tutorial/dify-mo-demo.md` — Dify 平台接入 MatrixOne 指南 — 本文档介绍如何将 Dify 平台与 MatrixOne 数据库集成，使用 MatrixOne 作为 Dify 的向量存储后端。
- `tutorial/django-python-crud-demo.md` — Django 基础示例 — 本篇文档将指导你如何使用 Django 构建一个简单的应用程序，并实现 CRUD（创建、读取、更新、删除）功能。
- `tutorial/gorm-golang-crud-demo.md` — gorm 基础示例 — 本篇文档将指导你如何使用 golang 和 gorm 构建一个简单的应用程序，并实现 CRUD（创建、读取、更新、删除）功能。
- `tutorial/htap-demo.md` — HTAP — 随着企业规模的增长和数据量的爆炸性增加，传统的交易型数据库在应对数据分析等高级应用时开始显得捉襟见肘，无法满足企业对数据分析的多维需求。业务系统的激增和业务逻辑的日益复杂化，迫使许
- `tutorial/python-sdk-demo.md` — MatrixOne Python SDK 适配示例 — MatrixOne Python SDK 提供了一种高效、便捷的方式，帮助开发者快速实现基于向量的语义搜索、全文搜索及混合检索等场景。通过 SDK，用户可以轻松地将文本数据转化为向
- `tutorial/rag-demo.md` — RAG 应用基础示例 — RAG，全称为 Retrieval-Augmented Generation（检索增强生成），是一种结合了信息检索和文本生成的技术，用于提高大型语言模型（LLM）生成文本的准确性和
- `tutorial/search-picture-demo.md` — 以图（文）搜图应用基础示例 — 当下，以图搜图和以文搜图的相关应用涵盖了广泛的领域，在电子商务中，用户可以通过上传图片或文本描述来搜索商品；在社交媒体平台，通过图像或文本快速找到相关内容，增强用户的体验；而在版权
- `tutorial/springboot-hibernate-crud-demo.md` — SpringBoot 和 JPA 基础示例 — 本篇文档将指导你如何使用 SpringBoot、Spring Data JPA 和 Intellij IDEA 构建一个简单的应用程序，并实现 CRUD（创建、读取、更新、删除）功
- `tutorial/springboot-mybatis-crud-demo.md` — SpringBoot 和 MyBatis 基础示例 — 本篇文档将指导你如何使用 SpringBoot、Mybatis 和 Intellij IDEA 构建一个简单的应用程序，并实现 CRUD（创建、读取、更新、删除）功能。
- `tutorial/sqlalchemy-python-crud-demo.md` — SQLAlchemy 基础示例 — 本篇文档将指导你如何使用 Python 和 SQLAlchemy 构建一个简单的应用程序，并实现 CRUD（创建、读取、更新、删除）功能。
- `tutorial/typescript-crud-demo.md` — TypeScript 基础示例 — 本篇文档将指导你如何使用 TypeScript 构建一个简单的应用程序，并实现 CRUD（创建、读取、更新、删除）功能。

### 社区贡献指南  `(contribution-guide/, 12 篇)`
> 代码风格 / 提 PR 流程 / 文档贡献

- `contribution-guide/code-style/code-comment-style.md` — 代码注释规范 — 本文描述了 MatrixOne 所使用的代码注释的规范和样式。当你提交代码时，请务必遵循已有的代码注释规范。
- `contribution-guide/code-style/code-of-conduct.md` — MatrixOne 行为守则 — 我们作为项目与社区的贡献者和维护者，承诺在参与项目以及社区的过程中，致力于彼此帮助、共同成长，维护开源开放、和谐友善的氛围，无论年龄、体型、种族、性别、性取向、表达、经验、教育、社
- `contribution-guide/code-style/commit-pr-style.md` — 提交信息&PR 规范 — 本文档描述了应用于 MatrixOrigin 的所有存储库的提交消息 (commit mesage) 和 PR(pull request) 的样式规范。当你提交代码时，务必遵循这种
- `contribution-guide/how-to-contribute/contribute-code.md` — 代码贡献 — MatrixOne 是一个由项目管理者、社区开发者共同维护、改进和扩展的开源项目。
- `contribution-guide/how-to-contribute/contribute-documentation.md` — 文档贡献指南 — 欢迎对 MatrixOne 文档的提出贡献。MatrixOne 社区一直在努力简化整个贡献流程，为此，我们创建本节来一步步地指导您完成文档贡献的过程。
- `contribution-guide/how-to-contribute/make-a-design.md` — 提交设计方案 — 前面章节提到了很多种类的修改，比如 Bug 修复、文档完善，这些都可以通过 GitHub 的 PR 工作流程来实现；但与此不同的是，如果您想要在 MatrixOne 中实现新的功能
- `contribution-guide/how-to-contribute/preparation.md` — 准备工作 — 非常欢迎您参与到 MatrixOne（以下简称 MO）项目的建设中来！无论你是初识 MatrixOne，还是已经迫切地想参与到开发工作中来，亦或是在阅读文档、使用产品的过程中发现了
- `contribution-guide/how-to-contribute/report-an-issue.md` — 提出问题 — 您在使用或开发 MatrixOne 过程中遇见的任何问题都能以 [Issues](https://github.com/matrixorigin/matrixone/issues/
- `contribution-guide/how-to-contribute/review-a-pull-request.md` — 审阅与评论 — 对 MatrixOne 来说，对 PR 的审阅和评论是至关重要的：您可以对他人的 PR 进行分类，以便有专家更快的来解决这些问题；您也可以对代码的内容进行审阅，对代码编写的风格、规
- `contribution-guide/how-to-contribute/types-of-contributions.md` — 贡献类型 — 对 MatrixOne 的贡献绝不仅限于代码。以下为您展示了参与 MatrixOne 项目并参与我们的开源社区的各种方式：
- `contribution-guide/index.md` — 社区贡献指南
- `contribution-guide/make-your-first-contribution.md` — 快速贡献 — MatrixOne 社区欢迎所有开发者的加入和贡献！本章节旨在帮助您快速完成首次贡献。


---

## 3. 新 IA 提案

参考 Snowflake / Databricks 的"Get Started → Concepts → Guides → Reference → Help → Release Notes"模板,结合 MatrixOne 实际内容(SQL 参考 364 篇是绝对主体,运维相关 80+ 篇散在 6 个 dir 里)。

### 主推方案:**7 个一级分类**

```
顶部导航                         覆盖现有目录                                 篇数
─────────────────────────       ──────────────────────────────────────────  ─────
1. 快速开始 Get Started          getting-started/                              9

2. 核心概念 Concepts             overview/(整体,25)
                                  + glossary.md(从根目录提到这里,1)        26
                                 (纯定义/架构/对比/术语,不混入 demo)

3. 开发 Develop                  develop/(主体,93)
                                  + tutorial/(全部 15 篇,作为
                                    develop/tutorials/ 子目录)              108
                                 (所有"动手做一遍"性质的内容都收在这里,
                                  不论是 CRUD demo、HTAP demo 还是 RAG demo)

4. 运维 Operate                  deploy/             (15)
                                  + maintain/         (14)
                                  + migrate/          (6)
                                  + performance-tuning/(12)
                                  + security/         (12)
                                  + test/             (6)                    65

5. SQL 参考 Reference            sql-reference/(原样保留)                   364

6. 帮助 Help                     troubleshooting/    (5)
                                  + faqs/            (4)                      9

7. 版本发布 Release Notes        release-notes/(原样)                        34
```

**关键原则**:每个一级分类对应一个**动作语义**,不混搭。
- Concepts = "这是什么 / 为什么这么设计"(读)
- Develop = "我要照着做"(写代码 + 跑 demo)
- 因此 demo 一律归 Develop,Concepts 只放架构/定义/对比/术语。

**社区贡献指南**(`contribution-guide/`,12 篇):**移出顶部 nav**,放页脚或独立"Community"小入口。它面向贡献者不是用户。

### 备选方案 A:**6 个一级**(把 Help 合并到 Release Notes 同栏的"Resources")

```
1. Get Started
2. Concepts
3. Develop
4. Operate
5. Reference
6. Resources(合并 Help / Release Notes / Glossary / Contribution)
```

更接近 Snowflake 顶栏风格,但 Help/Release Notes 用户访问频率高,塞进 Resources 二级查找成本上升。**不推荐。**

### 备选方案 B:**5 个一级**(Operate 拆回 Reference 的 "Admin" 子树)

把 deploy/maintain/migrate/security 视为"管理员参考"塞进 SQL Reference 的伞下。MatrixOne 的运维内容偏 SQL 命令(grant / role / show 之类),理论可行。**不推荐**,运维内容里部署拓扑/性能调优是非 SQL 操作内容,塞进 Reference 体验差。

---

## 4. 旧 → 新 映射表(目录级)

按主推方案(7 个一级):

| 旧路径 | 新路径 | 备注 |
|---|---|---|
| `index.md` | `index.md` | 不变,仍是 4 卡片入口 |
| `glossary.md` | `concepts/glossary.md` | 从根级提到 Concepts |
| `overview/**` | `concepts/**`(直接重命名 dir) | 25 篇,1:1 映射 |
| `getting-started/**` | `get-started/**` | 9 篇,改 dir 名(去 hyphen 也行,看口味) |
| `develop/**` | `develop/**` | 93 篇,主体保留 |
| `tutorial/**` | `develop/tutorials/**` | 15 篇全部移入,作为 develop 下的"实战教程"子目录 |
| `tutorial/index.md` | `develop/tutorials/index.md` | 重写一份 toctree,列 15 篇 demo |
| `deploy/**` | `operate/deploy/**` | 二级落入 operate |
| `maintain/**` | `operate/maintain/**` | |
| `migrate/**` | `operate/migrate/**` | |
| `performance-tuning/**` | `operate/performance/**` | 简短化 |
| `security/**` | `operate/security/**` | |
| `test/**` | `operate/test/**` | benchmark 归运维 |
| `sql-reference/**` | `reference/**` | 364 篇,改 dir 名 |
| `troubleshooting/**` | `help/troubleshooting/**` | 5 篇 |
| `faqs/**` | `help/faqs/**` | 4 篇 |
| `release-notes/**` | `release-notes/**` | 不变,34 篇 |
| `contribution-guide/**` | `contribution/**` 或留原位但从主 nav 摘掉 | 不进顶栏 |

**目录数变化**:16 → **7**(顶级),侧边栏顶层从 13 → 7,顶部 nav 从 6 → 7,**完全对齐**。

### URL 变化示例(供后续 301 重定向参考)

```
旧                                                       新
─────────────────────────────────────────────────────  ───────────────────────────────────────────────
/zh/overview/matrixone-introduction.html              → /zh/concepts/matrixone-introduction.html
/zh/overview/architecture/architecture-tae.html       → /zh/concepts/architecture/architecture-tae.html
/zh/getting-started/install-on-macos/...              → /zh/get-started/install-on-macos/...
/zh/deploy/deploy-matrixone-cluster/...               → /zh/operate/deploy/deploy-matrixone-cluster/...
/zh/maintain/backup/...                               → /zh/operate/maintain/backup/...
/zh/performance-tuning/optimization-concepts/...      → /zh/operate/performance/optimization-concepts/...
/zh/sql-reference/sql-reference/data-definition-language/create-table.html
                                                      → /zh/reference/sql-reference/data-definition-language/create-table.html
/zh/troubleshooting/error-code.html                   → /zh/help/troubleshooting/error-code.html
/zh/faqs/sql-faqs.html                                → /zh/help/faqs/sql-faqs.html
/zh/tutorial/develop-java-crud-demo.html              → /zh/develop/tutorials/develop-java-crud-demo.html
/zh/tutorial/htap-demo.html                           → /zh/develop/tutorials/htap-demo.html
/zh/glossary.html                                     → /zh/concepts/glossary.html
```

---

## 5. 执行计划

### 5.1 准备阶段(本提案审完先做)

1. **冻结期**:期间不要新增/重组内容,避免合并冲突。
2. **建分支**:`git checkout -b ia-restructure`
3. **跑 4 个 build 留下基线**:`make clean && make html`,把 `build/html/` 整目录复制成 `_baseline_html/`,后面对照"链接是否断"。

### 5.2 内容物理移动(脚本化,不要手 mv)

写一个 `scripts/migrate_ia.py`,做以下事:

1. **目录改名**(`git mv` 保 history)
   - `overview/` → `concepts/`
   - `getting-started/` → `get-started/`
   - `sql-reference/` → `reference/`
   - 新建 `operate/`,把 `deploy/ maintain/ migrate/ performance-tuning/ security/ test/` 全部 `git mv` 进去(改名 performance-tuning → performance)
   - 新建 `help/`,把 `troubleshooting/ faqs/` 移进去
   - 新建 `develop/tutorials/`,把 `tutorial/` 下全部 15 篇(含 htap-demo / dify-mo-demo / rag-demo / search-picture-demo / *-crud-demo / python-sdk-demo 等)整体迁入
   - 把根 `glossary.md` 移到 `concepts/glossary.md`
   - 删空的 `tutorial/` 目录

2. **改写 toctree 与跨分类内链**
   - 每个被移动的 .md 内,如果有相对链接指向"旧路径",批量替换:
     - `(../overview/...)` → `(../concepts/...)`
     - `(../tutorial/htap-demo.md)` → `(../develop/tutorials/htap-demo.md)`
     - 跨分类的 `[xx](getting-started/quickstart.md)` → `(get-started/quickstart.md)`
   - 工具:`grep -rEln '\[.*\]\((overview|tutorial|getting-started|deploy|maintain|migrate|performance-tuning|security|test|troubleshooting|faqs|sql-reference)/' matrixone/source/zh` 找出所有需要改的内链,Python 脚本批量正则替换。

3. **重写各 section 的 index.md**
   - `concepts/index.md`:overview/index.md 内容 + 加入 glossary(纯定义/架构,**不挂 demo**)
   - `operate/index.md`:**新建**,toctree 引 deploy/maintain/migrate/performance/security/test 各自的 index
   - `help/index.md`:**新建**,toctree 引 troubleshooting/faqs
   - `develop/index.md`:加 tutorials/ 子目录入口
   - `develop/tutorials/index.md`:**新建**,toctree 列全部 15 篇 demo(原 tutorial/index.md 内容 + 补全)
   - 其它 section index 路径不变,toctree 列表跟着改

4. **重写顶层 `index.md` 的隐藏 toctree**
   - 把现在 13+ 项的列表压缩成 7 项,每项指向 `<section>/index`

### 5.3 顶部导航 + 侧边栏代码改

1. **`_shared_theme/_static/js/topbar.js`**
   - I18N.zh.tabs 与 en.tabs 改成 7 项,`match` 字段改新 dir 名(`get-started, concepts, develop, operate, reference, help, release-notes`)
2. **`_shared_theme/_static/css/custom.css`**
   - 当前的 `.sidebar-tree > ul.current > li.toctree-l1:not(.current) { display: none }` 规则保持,但效果会"刚好正确"——左树顶级 7 项与顶部 7 项 1:1 对应

### 5.4 同步 EN

`matrixone/source/en/` 当前有 78 篇,结构应已与 zh 对应(用于覆盖度切换)。同样的 mv 脚本对 en 跑一遍。

### 5.5 验收 + 死链扫描

1. `make clean && make html`,期望 0 warning(目前有 6 处 release-notes `***` transition warning,与 IA 无关)
2. 跑死链扫描:`uv run sphinx-build -b linkcheck matrixone build/linkcheck/matrixone-zh`
3. 对照 baseline,curl 取每个 url 看 200/404
4. 抽样 20 个深层页面眼看左树是否只显示当前分类

### 5.6 重定向(后续,非本次)

旧 URL → 新 URL 的 301 redirect 不在本次 demo 实现。如果生产部署需要,有两条路:
- **Nginx / Cloudflare 层**:写一份 301 表(每条记录可机器生成),挂在反向代理
- **Sphinx `sphinx-reredirects` 扩展**:在 conf.py 加 `redirects = {...}`,生成 client-side meta refresh,缺点是不返 301 状态码

---

## 6. 风险 / 未决问题

| # | 项 | 风险 | 缓解 |
|---|---|---|---|
| 1 | 跨分类相对链接数量 | 文档 .md 之间的 `[xx](../foo/bar.md)` 链接,跨分类的需要全部更新 | 移动前先 `grep` 出全列表,Python 正则批量替换,移动后 `make html` 看 myst.xref_missing warning 兜底 |
| 2 | `sql-reference/sql-reference/` 二层重名 | 子目录套了同名子目录,新结构想不想拍平? | 主推方案保留(改成 `reference/sql-reference/`),拍平另议 |
| 3 | release-notes 6 处 `***` transition error | 与 IA 无关,但本次重构若不顺手修,新结构 build 仍会有 warning | 顺手把 `***` 删掉或改成空行 |
| 4 | EN 站当前内容只有 78 篇(zh 是 628) | EN 的 IA 重组可能涉及"找不到对应文件"问题 | EN 按"有就 mv,没有就跳过"处理;新结构下 EN 站缺哪一节,顶部 tab 仍点得进去(进 section index 显示空内容 toctree) |
| 5 | `lang-switcher.js` 的 `PARTIAL_EN` 白名单是按旧路径写的 | 路径变了白名单全部失效 | 同步更新白名单到新路径 |
| 6 | 站内 hardcoded 链接 | 主页 4 卡 `:link:` 用的是 `getting-started/index` 之类的 docname,改了 dir 必须同步改主页 | 主页 + 顶栏 + footer 的硬编码链接在 IA 重组同一 PR 一起改 |
| 7 | Tutorial 现在的 index.md 内容偏旧 | 移到 `develop/tutorials/` 后需要新写一份 toctree 把 15 篇全列上,顺带把"概念演示"和"代码 demo"在页内做个分组小标题 | 重构脚本里新建 develop/tutorials/index.md,toctree 列出 `:caption: 概念演示` 与 `:caption: 代码 CRUD demo` 两个分组 |

---

## 7. 决策点(等你拍板)

1. **方案选 7 还是 6**?(我推 7,Help 与 Release Notes 分立查找成本低)
2. **dir 命名**:
   - `getting-started` 还是 `get-started`?(Snowflake 用 `getting-started`,我倾向保留)
   - `performance-tuning` 还是 `performance`?(短一点更好用,但破坏现有 URL)
   - `sql-reference` 二层套 vs 拍平?
3. **contribution-guide** 是从主 nav 摘掉还是保留?(我推摘掉,放页脚或 footer 一个小入口)
4. **是否同期顺手修 release-notes 的 `***` transition warning**?
5. **是否同期把 matrixone-intelligence 也按同一套 IA 重组**?(intelligence 当前 16 个顶级目录,问题相同;但内容是 mkdocs 迁过来的,有自己的语义,可能不照搬这套分类)
6. **本次只动 zh,还是 zh+en 同步动**?(en 站只 78 篇,跟动成本不高,推荐同步)

---

**审完此文请回复:**
- 选哪个方案(7 / 6 / 改进)
- 决策点 1-6 的回答
- 是否进入 5.2 的脚本化执行

