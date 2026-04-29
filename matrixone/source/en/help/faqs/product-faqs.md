# Product FAQ

## About the product

**What is MatrixOne?**

MatrixOne is a forward-looking, hyper-converged, heterogeneous, cloud-native database. A hyper-converged data engine supports mixed transactional / analytical / stream workloads; a heterogeneous cloud-native architecture supports cross-datacenter, multi-region, and cloud-edge collaboration. MatrixOne aims to simplify data-system development and operations, reduce data fragmentation across complex systems, and break the barriers to data unification.
To learn more, see [MatrixOne Introduction](../../concepts/matrixone-introduction.md).

**Is MatrixOne based on MySQL or another existing database?**

MatrixOne is a brand-new database built from scratch. MatrixOne is compatible with a subset of MySQL syntax and semantics, and will diverge further from MySQL over time as we evolve into a more powerful hyper-converged database.
See [MySQL compatibility](../../concepts/feature/mysql-compatibility.md) for details.

**Which programming language is MatrixOne developed in?**

MatrixOne is primarily written in **Go**.

**Which programming languages are supported for connecting to MatrixOne?**

MatrixOne supports Java, Python, and Go connectors and ORMs. Other languages can connect via MySQL-compatible drivers.

**What compression algorithm does MatrixOne's columnar storage use?**

LZ4. Configuration is not changeable.

**Can older versions be upgraded directly to the latest version?**

From v0.8.0 onward, you can upgrade straight to the latest via `mo_ctl upgrade latest` — see the [mo_ctl tool](../Maintain/mo_ctl.md). If you need to upgrade from a version earlier than v0.8.0, we recommend backing up your data, reinstalling, and reimporting.

**Is MatrixOne in a stable release? Which version is recommended?**

MatrixOne has released v25.2.2.2, which includes extensive stability work and is production-ready. Feedback from the community is welcome.

**Is there a MatrixOne cloud version for quick testing?**

Yes — MatrixOne Intelligence is currently in public beta. See the [MatrixOne Intelligence docs](https://docs.matrixorigin.cn/zh/matrixonecloud/MatrixOne-Cloud/Get-Started/quickstart/).

## Architecture

**Does MatrixOne use RBAC for permissions? Can I grant permissions directly to users?**

MatrixOne's permission model combines Role-Based Access Control (RBAC) and Discretionary Access Control (DAC). You cannot grant permissions directly to users — roles are the unit of authorization.

**How do I use the HA architecture?**

The MatrixOne standalone version does not yet have HA. The primary-standby HA design is in progress. The distributed version is inherently HA — Kubernetes and S3 are both HA architectures. CN and TN are stateless and can be re-launched at any time; log service is stateful, with 3 nodes forming a Raft group — one node failure is fine, the system continues; two node failures make the system unavailable.

**Can TN nodes be scaled out in a Kubernetes cluster?**

TN scale-out is not supported yet.

**What do the various components do? What's the minimum deployment? Will zero-downtime scale-out be supported later?**

MatrixOne's core components: proxy, CN, TN, log service. CN is a stateless compute node; TN is the transaction node; log service is the transaction log (effectively WAL). Proxy handles load balancing and resource-group management. A mixed deployment fits into three physical / virtual machines. Scale-out is seamless — with compute/storage separation, storage scaling is just scaling S3. Compute scaling is scaling CNs — based on Kubernetes, CNs are stateless containers and scale quickly.

**How is resource isolation between tenants implemented?**

The core is that `ACCOUNT` can be mapped to a CN Set (resource group). Tenant isolation is essentially CN-container isolation. Beyond the per-tenant level, you can further split CN resource groups by workload type inside a single tenant for finer-grained control. For the full story, see [Workload & tenant isolation](../Deploy/mgmt-cn-group-using-proxy.md).

**Can MySQL table engines be migrated directly? Is InnoDB compatible?**

MatrixOne does not support MySQL engines like InnoDB or MyISAM — but it accepts MySQL statements and silently ignores the engine clause. MatrixOne has a single storage engine, TAE, which is independently developed and works well across workloads. No `ENGINE=XXX` switching is needed.

## Features

**Which applications is MatrixOne a good fit for?**

MatrixOne provides best-in-class HTAP, suited for enterprise data platforms, big-data analytics, and similar scenarios.

**Which database is MatrixOne compatible with?**

MatrixOne is highly compatible with MySQL 8.0 — SQL syntax, wire protocol, operators, and functions. For the full compatibility gap list, see [MySQL compatibility](../../concepts/feature/mysql-compatibility.md).

**How well does MatrixOne work with BI tools as a MySQL replacement?**

Very well — MatrixOne is highly MySQL-compatible across protocol, SQL, client tools, and development patterns. Management tools and ecosystem tools built for MySQL can largely be reused. BI tools can use MatrixOne as if it were MySQL. See: [FineBI with MatrixOne](../Develop/Ecological-Tools/BI-Connection/FineBI-connection.md), [Yonghong BI with MatrixOne](../Develop/Ecological-Tools/BI-Connection/yonghong-connection.md), [Superset with MatrixOne](../Develop/Ecological-Tools/BI-Connection/Superset-connection.md).

## Database comparisons

**Standalone MatrixOne vs. MySQL — performance?**

Standalone MatrixOne is slightly behind MySQL on TP, but significantly ahead on `LOAD`, streaming writes, and analytical queries.

**How is MatrixOne different from TiDB (HTAP)?**

The architectures are different. MatrixOne uses compute-storage separation with a cloud-native shared-storage architecture — one copy of the data served by one engine for HTAP. TiDB is share-nothing with data sharded across TiKV for TP and TiFlash for AP, using two engines plus ETL to deliver HTAP — data is stored twice.

## Other

* **Can I contribute to MatrixOne?**

MatrixOne is an open-source project fully developed on GitHub — contributions from all developers are welcome. See the [Contribution Guide](../Contribution-Guide/make-your-first-contribution.md).

* **Any other channels to learn about MatrixOne besides the official docs?**

The [MatrixOne docs](https://docs.matrixorigin.cn) are the most complete and up-to-date source. We also have technical chats on Slack and WeChat. For anything else, reach out to [opensource@matrixorigin.io](mailto:opensource@matrixorigin.io).
