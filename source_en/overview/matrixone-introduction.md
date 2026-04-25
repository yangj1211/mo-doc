# MatrixOne Introduction

MatrixOne is a hyper-converged, heterogeneous, distributed database. Its cloud-native, compute/storage/transaction-separated architecture builds an HSTAP hyper-converged data engine — a single database system that serves OLTP, OLAP, and stream-computing workloads, deployable across public cloud, private cloud, and edge, with compatibility across heterogeneous infrastructure.

MatrixOne brings real-time HTAP, multi-tenancy, stream computing, extreme elasticity, cost efficiency, enterprise-grade high availability, and high MySQL compatibility in a single hyper-converged data solution — consolidating work previously split across multiple databases into one, simplifying development and operations, eliminating data fragmentation, and improving agility.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture.png)

MatrixOne is a good fit for scenarios that require real-time writes, substantial data volumes, bursty workloads, multi-modal data management, and both transactional and analytical workloads — e.g., generative-AI applications, mobile / internet apps, IoT data processing, real-time data warehouses, and SaaS platforms.

## Core features

### Hyper-converged engine

* **Hyper-converged engine**

    An HTAP data engine — one database serves TP, AP, time-series, and ML workloads.

* **Built-in stream engine**

    Built-in stream-computing engine — real-time ingest, real-time transformation, and real-time queries.

### Heterogeneous cloud-native

* **Compute/storage separation**

    Storage, compute, and transactions are fully decoupled, all containerized for extreme elasticity.

* **Multi-infrastructure compatibility**

    Cross-datacenter / multi-region / cloud-edge collaboration — seamless scale in/out and efficient, unified data management.

### Extreme performance

* **High-performance execution engine**

    Flexible coordination of Compute Nodes and Transaction Nodes handles both point queries and batch workloads — extreme performance on OLTP and OLAP.

* **Enterprise-grade high availability**

    A state-of-the-art Multi-Raft replication state machine backs a strongly-consistent shared log — ensuring cluster HA without data duplication.

### Simple to use

* **Built-in multi-tenancy**

    Native multi-tenancy — tenants are isolated and scale independently, with unified management — simplifying multi-tenant design at the application layer.

* **MySQL compatibility**

    High MySQL 8.0 compatibility — wire protocol, SQL syntax, and ecosystem tools — lowering the cost of adoption and migration.

### Cost efficiency

* **Efficient storage design**

    Low-cost object storage as the primary store; erasure coding delivers high availability with only ~150% data redundancy. Paired with high-speed caching and hot/cold tiered storage, MatrixOne balances cost and performance.

* **Flexible resource allocation**

    Allocate resources between OLTP and OLAP as business dictates — maximizing utilization.

### Enterprise-grade security and compliance

* Role-Based Access Control (RBAC), TLS connections, and data encryption build a multi-layer security posture — meeting enterprise data-security and compliance needs.

## User value

* **Simplified data development and operations**

    As business grows, teams accumulate more data engines and middleware. Each engine typically depends on 5+ base components, stores 3+ data copies, and needs its own install / monitoring / patching / upgrading. Selection, dev, and ops costs soar. With MatrixOne's unified architecture, one database serves many workloads — the component and tech-stack footprint shrinks by 80%, significantly reducing management burden.

* **Eliminated data fragmentation and inconsistency**

    In complex existing architectures, multiple pipelines produce redundant data copies. Complex dependencies make data updates painful and upstream/downstream inconsistencies common — hand-verification is hard. MatrixOne's high-cohesion architecture and incremental materialized views let downstream systems respond to upstream updates in real time — trimming ETL and enabling end-to-end real-time data processing.

* **No infrastructure lock-in**

    Fragmented infrastructure means an enterprise's private and public-cloud data clusters often diverge — migration is expensive. Once cloud-database selection happens, subsequent scaling and component purchases are tied to the chosen vendor. MatrixOne provides a unified cloud-edge infrastructure and unified data management — enterprise data architecture is no longer tied to infrastructure, enabling a single data cluster to scale seamlessly across clouds with better economics.

* **Blazing-fast analytics**

    Slow complex queries and layers of intermediate tables hurt data-warehouse agility; huge wide tables hurt iteration speed. MatrixOne's factorized compute and vectorized execution engine deliver blazing performance on complex queries — fast on single-table, star, and snowflake schemas alike.

* **TP-grade reliability for AP**

    Traditional warehouses make data updates expensive — "update is immediately visible" is hard. For marketing-risk control, autonomous driving, smart factories, and similar scenarios with fast-moving upstream data, current analytics systems require full reloads and can't do incremental updates. MatrixOne's cross-engine high-performance global distributed transactions support row-level real-time incremental updates — delivering blazing analytics while supporting updates, deletes, and real-time point queries.

* **Zero-downtime auto-scaling**

    Traditional warehouses trade off performance vs. flexibility and fall short on price-performance. MatrixOne's compute-storage separation scales storage and compute nodes independently, responding efficiently to workload shifts.

## Target scenarios

* **Traditional business systems needing scalability and analytical reporting**

OA / ERP / CRM and similar systems grow past single-node limits as data scales. Many teams add a dedicated analytical database for month-end / quarter-end reporting. With MatrixOne, one database serves both business and analytics — and grows seamlessly with the business.

* **Real-time dashboards / BI**

OLAP workloads like dashboards and BI reports often analyze huge datasets and hit performance walls at scale. MatrixOne's strong analytical performance and elasticity accelerate complex large SQL queries to near-real-time — improving decision-making agility.

* **Data platforms ingesting heterogeneous real-time streams**

Sensors and networks produce massive data from IoT devices — production lines, EVs, surveillance cameras — easily hundreds of TB to PB. Digital-transformation demands increasingly require storing and using this data. Traditional databases can't handle this ingest + processing load. MatrixOne handles streaming writes and transformation with strong elasticity — fitting any workload and data scale.

* **Enterprise data-platform scenarios**

Mid/large enterprises typically run many business systems. To unify analysis and connect data sources, many build a data platform bridging systems for a complete enterprise view. Traditional Hadoop-based stacks are complex and expensive. MatrixOne's HTAP architecture lets you use a data platform with MySQL-like ergonomics — run SQL on massive data directly for reporting, greatly reducing cost.

* **Volatile internet workloads**

Gaming, e-commerce, entertainment, social, news — large user counts and volatile workloads. Hot events need big compute bursts. MatrixOne's cloud-native architecture auto-scales with workload changes — dramatically reducing ops burden.

* **Enterprise SaaS**

Enterprise SaaS must balance multi-tenancy. Shared vs. dedicated instances trade off cost vs. isolation. MatrixOne's native multi-tenancy — naturally isolated per-tenant, independently scalable, unified management — is the best of both worlds.

## Related

* [MatrixOne architecture design](architecture/matrixone-architecture-design.md)
* [MatrixOne quickstart](../Get-Started/install-standalone-matrixone.md)
