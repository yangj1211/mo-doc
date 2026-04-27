# Cost Efficiency

MatrixOne is a fresh-designed database with cost efficiency as a core principle. Cost efficiency manifests in several dimensions:

## Hybrid workloads (HTAP) in a single cluster

As big-data applications expand, traditional processing models struggle to keep up with real-time analytics on massive data. Modern data workloads increasingly require high-concurrency OLTP plus large-scale OLAP together.

MatrixOne is purpose-built for hybrid workloads. It supports OLTP and OLAP in one cluster — true HTAP (Hybrid Transactional and Analytical Processing). Users no longer need separate OLTP and OLAP systems — one database handles both. This avoids the cost of building and running two systems and removes the ETL step between them. You run business and analytics in the same cluster easily.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/high-cost-performance/HTAP.png width=80% heigth=80%/>
</div>

## HTAP with a single storage engine

HTAP in the industry typically wraps an OLTP engine and an OLAP engine behind one product. Data is moved between the two engines transparently, but two copies of data live in two engines — hardware and storage costs don't actually drop.

MatrixOne is different — one storage engine for HTAP. By grouping CNs and differentiating execution paths per workload type, MatrixOne delivers single-engine HTAP. When a request enters the cluster, Proxy dispatches OLAP-like requests to CN groups dedicated to OLAP. These typically scan or bulk-write data — CNs talk directly to object storage. Small OLTP writes (`INSERT`, `UPDATE`, `DELETE`) are handled by a CN group dedicated to OLTP — TN handles transaction metadata and writes to LogService. TN periodically compacts LogService data and flushes to object storage.

Overall, your data lives once and is served by a single storage engine — significantly lowering storage and compute costs.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/high-cost-performance/HTAP-single-engine.png width=50% heigth=50%/>
</div>

## Flexible resource allocation boosts machine utilization

Most of the time, a database serves CRUD-style transactional workloads. At certain moments — end of day, month, or year — you need OLAP analytics. With one database, you either cut business load temporarily or run AP at off-hours. Analysis often runs long; you can't stress the business. Deploying a separate AP system often leads to low utilization — wasting resources.

As described above, MatrixOne groups stateless compute nodes, and routes OLTP and OLAP workloads differently at the lower tier — delivering HTAP. Resources can be reallocated dynamically to match business — raising utilization and true cost efficiency.
When CRUD demand is high, assign more CNs to OLTP. When analytics demand rises, assign more CNs to OLAP. Adjustments are fully dynamic.

For example: originally you needed 3 nodes for OLTP and 3 for OLAP, strictly partitioned — OLTP nodes couldn't serve OLAP and vice versa. Users typically over-provision. Peak full-use is brief. With MatrixOne, you can use just 4 nodes — typically 3 OLTP + 1 OLAP; at month-end 1 OLTP + 3 OLAP; then revert. Utilization improves by ~40%.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/high-cost-performance/usage-optimize.png width=80% heigth=80%/>
</div>

## Efficient, low-cost object storage

Storage is primarily object storage. With erasure coding, just ~33% redundancy protects data against loss. Compared to multi-replica schemes common in the industry, erasure coding achieves the same reliability with better space efficiency.

For MatrixOne's smallest recommended on-prem MinIO deployment (4 nodes × 4 disks), MatrixOne supports a 4-disk erasure + 12-disk data layout — redundancy of 1.33.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/high-cost-performance/erasure-code.png width=80% heigth=80%/>
</div>

Object storage also supports HDDs and other low-cost media. For clusters where compute isn't dominant and storage is the priority, this further lowers cost.

## High compression from columnar storage

Structured data has a consistent structure per column. MatrixOne stores data columnar-wise — a layout that compresses well:

1. Free choice of compression algorithms: each column is stored independently and can pick the compression that best fits its type. Leveraging repetition, ordering, and type-specific techniques produces stronger compression. Row stores typically use generic algorithms that can't take advantage.
2. High intra-column redundancy: similar values cluster together, letting algorithms identify and compress them more effectively — pushing up compression ratios.

MatrixOne's compression ratio can be as low as 1% — the exact ratio depends on data structure, redundancy, and other factors.

In short, MatrixOne's columnar storage dramatically compresses your actual usage — cutting storage cost significantly.

## MySQL compatibility

MatrixOne maintains MySQL compatibility across syntax, protocol, and ecosystem tools — minimizing the cost of migrating from or learning after MySQL.

For details, see [MySQL compatibility](mysql-compatibility.md).
