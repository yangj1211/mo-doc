# MatrixOne Architecture Design

## Overview

MatrixOne is a hyper-converged, heterogeneous, cloud-native database.

**Hyper-converged** means combining capabilities across different workload types. MatrixOne supports OLTP, OLAP, and streaming within a single database — we call this combined capability HSTAP (Hybrid Streaming & Transaction/Analytical Processing). HSTAP redefines HTAP by emphasizing the built-in stream-processing capability connecting TP and AP tables — giving users a database experience as flexible as a big-data platform. Many users are already familiar with this pattern thanks to the big-data ecosystem. With MatrixOne, minimal integration yields a one-stop TP + AP experience — without the bloat and constraints of traditional big-data stacks.

**Heterogeneous cloud-native** means MatrixOne is fully redesigned for cloud-native infrastructure (Kubernetes + object storage) — satisfying public cloud, private cloud, edge cloud single-cloud and cross-cloud deployments — while fully leveraging cloud-native capabilities for compute-storage separation and linear scalability. In Kubernetes-dominated environments, databases have typically been left out of the unified orchestration because they're stateful — deployed and operated on VMs or bare metal. The root cause is that traditional standalone / distributed databases weren't redesigned for cloud-native. MatrixOne is built from scratch — fully in-house storage + compute — designed for cloud-native environments to maximize container-based software-defined resources and flexible allocation. This unifies MatrixOne with the application layer in the same cloud-native environment. Kubernetes' cross-cloud capabilities let MatrixOne work seamlessly across heterogeneous cloud / IaaS environments.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture.png)

## Architectural tiers

As shown below, MatrixOne runs on Kubernetes — all components are containers, built and managed as such. MatrixOne splits into three tiers: compute, transaction, and storage. Storage, compute, and transactions are fully decoupled — each has its own object units and roles, and each scales independently.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/architecture-1.png)

- **Storage tier**: designed for cloud-native environments where object storage is the de facto storage standard — reliable, low-cost, effectively infinite. MatrixOne uses S3-compatible object storage as primary storage; all data is eventually persisted here. Major cloud providers (public and private) support the S3 API, and MatrixOne works seamlessly across them. For on-prem environments without object storage, you can self-host [MinIO](https://min.io/).

- **Compute tier**: built around Compute Nodes (CN). In Kubernetes, each CN is a stateless container pod — resource size and count are software-defined, and Kubernetes provides them on demand. Each CN has two tiers of cache (memory + local disk) to accelerate queries; the cache uses LRU. Because CNs are stateless, they can be restarted, scaled vertically and horizontally at will — and as pods, scaling is seconds-level, with fast restart or failover on failure.

- **Transaction tier**: on top of containers + object storage, MatrixOne's design works well for OLAP (low-concurrency IO, large blocks). But high-concurrency TP can't be served purely from object storage — S3 supports only hundreds of concurrent IO and is unfriendly to small files. MatrixOne adds a dedicated transaction tier — Transaction Node (TN) + Log Service (LS) — handling data-write flows.
    * **TN**: CNs are uniform — any CN can accept writes. TN ensures transactional integrity, arbitrates writes from different CNs (detecting conflicts and ordering locks), and accepts the final commit request for ACID. TN also buffers new small writes in memory, asynchronously persisting to object storage once big enough. Above a threshold, TN (after arbitration) lets CN write directly to object storage; the commit carries the S3 location. TN is stateless — start/stop and vertically scale at will.
    * **LS**: the small chunk of new data held in TN's memory — Logtail — isn't fully durable by itself, so LS records the corresponding write log. LS is a Raft group of three nodes — three replicas plus leader election keep service available through one-node failure.

## System components

![MatrixOne Component](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/mo-component.png)

Several components combine to deliver MatrixOne's distributed + multi-engine fusion:

### File Service

File Service handles all storage media reads and writes. Media include memory, disk, and object storage. Features:

- Uniform API across media types — the same interface works for everything.
- Designed around data immutability — once a file is written it's never updated; updates produce a new file.
- This simplifies caching, migration, and verification — and raises concurrency.
- On top of the uniform API, File Service provides tiered caching with flexible policies — balancing speed and capacity.

### Log Service

Log Service handles transaction logs. Features:

- Raft for consistency; multiple replicas for availability.
- Stores and processes all MatrixOne transaction logs; before commit, ensures Log Service writes are healthy; on restart, replays the logs.
- After transaction commit + flush, truncates Log Service content to keep size bounded. Remaining content is the Logtail.
- If multiple replicas fail at once, MatrixOne goes down.

### Transaction Node

TN hosts MatrixOne's distributed storage engine TAE. Features:

- Manages MatrixOne metadata and Log Service transaction logs.
- Accepts distributed-transaction requests from CNs, arbitrates read/write, pushes arbitration results back to CN, and pushes content to Log Service — ensuring ACID.
- Generates snapshots at checkpoints for Snapshot Isolation, releasing snapshot info post-commit.

### Compute Node

CN accepts user requests and processes SQL. Modules:

- **Frontend**: handles MySQL wire protocol, parses SQL, dispatches, and returns results.
- **Plan**: parses the frontend's output and produces a logical plan — dispatched to Pipeline.
- **Pipeline**: transforms the logical plan into an executable plan and runs it.
- **Disttae**: executes reads and writes — subscribing to Logtail from TN, reading from S3, and pushing writes to TN.

### Stream Engine

Built-in Stream Engine supports real-time data querying, processing, and augmentation — particularly for incoming data streams (point series). Using Stream Engine you define stream pipelines via SQL and serve real-time data backends, and you can join streaming data with non-streaming datasets via SQL — simplifying the overall data stack.

### Proxy

Proxy is a powerful tool for load balancing and SQL routing:

- SQL routing achieves tenant resource isolation — CNs from different tenants don't interfere.
- Inside a tenant's resource group, SQL routing allows a second split — raising resource utilization.
- Within the second split, Proxy load-balances across CNs — making the system more stable and efficient.

## Related

Other info:

* [Install standalone MatrixOne](../../Get-Started/install-standalone-matrixone.md)
* [What's new](../whats-new.md)
