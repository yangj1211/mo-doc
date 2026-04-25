# Hybrid Workloads (HTAP)

MatrixOne is a database that supports HTAP (Hybrid Transaction Analytical Processing) workloads — aiming to meet both TP and AP needs within a single database. With storage/compute/transactions decoupled, MatrixOne supports online transactions and real-time statistical analysis in the same data engine, with efficient resource isolation. This design preserves data freshness and removes the need to build a real-time data warehouse in many scenarios — helping customers realize business value faster.

## Business need

As data scales, traditional online databases must be split. But the sharded architecture can't serve scenarios requiring cross-shard aggregation and real-time analytics. Real-time data warehouses fill this gap, but they're complex and expensive — not every team can build them. MatrixOne's HTAP mode delivers online throughput and real-time analytics at scale in one engine — driving efficiency and continuous innovation.

## Benefits

- **One-stop experience**: TP + AP in a single database.
- **Simpler integration**: minimal integration work to cover all TP and AP scenarios — significantly reducing the complex ETL from TP to AP databases.
- **Cost efficiency**: a single storage engine for HTAP means one cluster and one copy of the data — much cheaper hardware than multi-engine approaches.

## Technical architecture

MatrixOne delivers HTAP via modular storage / compute / transaction architecture, a multi-tier storage system, and workload-path isolation.

### Modular separation of storage, compute, and transactions

MatrixOne uses complete compute-storage separation. Modular design splits compute, storage, and transactions into independent tiers, each independently scalable. MatrixOne has three tiers:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/htap/mo-htap-arch.png width=80% heigth=80%/>
</div>

- **Compute tier**: Compute Nodes (CN) — serverless compute and transaction processing with their own cache; restartable / scalable on demand; multiple CNs compute in parallel for faster queries.
- **Transaction tier**: Transaction Node (TN) + Log Service — full log service and metadata, with built-in Logtail preserving recently written data.
- **Storage tier**: all data stored in S3-class object storage — low-cost, effectively infinite; File Service abstracts backend differences uniformly across nodes.

### Multi-tier storage

The storage system comprises full-data shared storage, a small shared log, and stateless caches on compute nodes.

- Full data lives in object storage — the database's primary store and sole durable location. Object storage is cheap and scales effectively without limit.
- LogService provides the shared log — it captures writes / updates / transactional state for the whole cluster. It's the only stateful component. LogService uses distributed Raft with 3 nodes for HA. It retains only a recent window of transactions — the Logtail. TNs periodically compact older log data into S3, keeping Logtail compact (typically a few GB).
- Each CN has a cache. On first query, related data is fetched from object storage into cache as hot data. On repeat queries, hitting cache returns results fast. See [Cold/hot data tiering architecture](../architecture/architecture-cold-hot-data-separation.md). CNs also subscribe to Logtail from LogService — LogService pushes updates in real time.

### Workload-path isolation

#### Custom workload isolation

User requests enter MatrixOne through the Proxy module. Proxy groups compute nodes and isolates workloads — splitting CNs into groups with labels for tenants or workloads, so different business needs route to different CN groups.

See [Managing CN groups with Proxy](../../Deploy/mgmt-cn-group-using-proxy.md).

#### TP/AP path isolation

MatrixOne routes requests to different processing paths at execution time, isolating OLTP and OLAP. We describe read and write paths below.

##### Writes

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/htap/write.png width=40% heigth=40%/>
</div>

Processing writes (INSERT/UPDATE/DELETE):

1. CN starts a transaction and checks the write for PK conflicts or other transaction issues — returning an error to the user if any.

2. CN decides the path based on write size. If the volume is below a threshold (typically 10MB), CN forwards the data to TN. TN runs write-write conflict checks and transaction arbitration, then writes to LogService as log entries forming the Logtail.

3. Updated Logtail is pushed in real time to subscribing CNs for query. If the write exceeds the threshold, CN writes directly to object storage and sends a commit to TN. TN runs conflict checks and arbitration, then commits.

Small OLTP-style writes flow CN → TN → LogService. Large writes (e.g., `LOAD`) flow CN → S3, with minimal CN → TN traffic.

##### Reads

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/htap/read.png width=40% heigth=40%/>
</div>

On reads, CN first checks subscribed Logtail — hits return immediately from the newest writes. On Logtail miss, CN checks its own and other visible CN caches — a hit returns immediately. On cache miss, CN analyzes the plan to decide if large reads are required; above a threshold (e.g., 200 blocks) multiple CNs read from object storage in parallel, otherwise a single CN reads.

Whether OLTP or OLAP, reads go via CN → S3. Proxy-based CN isolation adds workload separation.

## Applications

HTAP has broad applications across finance, telecom, manufacturing, internet, tech, and more.

In finance, HTAP databases handle high-throughput trading and real-time risk management — meeting high-throughput, low-latency requirements while enabling real-time analytics for decisions and monitoring.

In telecom, HTAP databases support real-time billing and network optimization — processing massive streams of usage data and network activity, and backing intelligent real-time decisions to improve service quality and user experience.

In IoT, HTAP databases support device management and real-time monitoring — processing huge volumes of sensor and device-state data and providing real-time monitoring and management — important for real-time decisions, remote diagnostics, and predictive maintenance.

### Financial real-time risk control

A city-commercial bank runs a real-time risk control system for credit-card business — monitoring transactions, detecting risk, and taking prompt action.

| Core requirement | Workload type | MatrixOne HTAP |
| --- | --- | --- |
| Real-time acquisition of transaction data | Fast, low-latency writes at high scale | MatrixOne writes massive data concurrently; scale CNs + object storage to raise performance further. |
| Offline computation of data metrics, user-behavior and risk analysis | Complex analytical queries on TB-scale data | MatrixOne handles massive star/snowflake analytics; multi-CN parallelism scales linearly. |
| Real-time analysis and risk computation | Typical AP work with strict SLAs | Multi-CN parallel compute meets large-report SLAs with fast reads. |
| Frequent, sharp workload swings | Flexible scale-in/out | Compute-storage separation gives MatrixOne strong elasticity — scale fast to match workload. |

### Telecom business management

A province-level telecom operator serves tens of millions of users, mostly voice — needing to support massive concurrent usage and statistical analytics.

| Core scenario | Workload type | MatrixOne HTAP |
| --- | --- | --- |
| Query balance and real-time suspension | High-concurrency short transactions, low latency | OLTP capability; multi-CN distributed architecture keeps performance stable under concurrency; load balancing. |
| Real-time balance updates after top-ups | High-concurrency short transactions, low latency | Meets high-concurrency low-latency TP; multi-CN distributed architecture for load balancing. |
| Bulk plan adjustments effective next month | Very large transactions, high throughput | Direct S3 writes avoid LogService contention, enabling fast bulk ingestion. |
| Daily / weekly / monthly / quarterly / yearly stats | Typical AP within SLAs | Multi-CN parallelism meets large-report SLAs with fast reads. |

### Manufacturing execution (MES)

An electronics manufacturer runs tens of production lines. The MES system manages people, machines, materials, and processes — and periodically analyzes efficiency and energy use.

| Core scenario | Workload type | MatrixOne HTAP |
| --- | --- | --- |
| Manage production, warehousing, quality | High-concurrency short transactions, low latency | OLTP capability; distributed multi-CN keeps performance stable under concurrency; load balancing. |
| Real-time ingestion of machine data | High-concurrency, multi-type writes | Massive concurrent writes; scale CNs + object storage further. |
| Root-cause analysis across history | Multi-dimensional analytics on large offline data | MatrixOne handles star/snowflake analytics at scale with linear multi-CN scaling. |
| Real-time efficiency, energy, and machine state queries | Extremely fast ad-hoc analytics | Complex SQL via multi-CN parallel compute yields real-time analytics. |
