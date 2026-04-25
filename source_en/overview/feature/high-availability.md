# High Availability

Database HA is a critical enterprise requirement — it guarantees system availability, data safety, and business continuity. MatrixOne is a distributed, highly-available database that meets these needs. This article describes MatrixOne's HA, including fault recovery, data redundancy, and load balancing.

## Business need

Enterprises require HA for:

* **Continuous availability**: critical business databases must run continuously — avoiding long outages and preserving business continuity and user satisfaction.

* **Fault recovery**: quick automatic failure detection and failover minimize downtime — preserving continuity and reliability.

* **Data protection and recovery**: data is a core asset — regular backups and fast restores defend against accidental loss or corruption.

* **Cross-region DR**: critical workloads may require cross-region data centers for disaster recovery.

## Benefits

MatrixOne redundancy uses erasure coding. Transaction-log replication uses the Raft protocol — a transaction commits only after a majority write success, guaranteeing strong consistency. Minority replica failures don't affect availability. MatrixOne HA meets Tier-4 financial standards (RPO=0, RTO<30min).

## Technical architecture

MatrixOne's architecture (diagram below) has HA at every layer.

![high-availability](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/high-availability.png)

### Resource-scheduling layer

MatrixOne is entirely cloud-native — all components run as containers on Kubernetes. Multi-master / multi-worker Kubernetes cluster provides continuous availability. See the [Kubernetes HA topology](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/).

### Storage layer

MatrixOne uses object storage, recommended with MinIO. MinIO — a mature distributed object-store — keeps data services available and files consistent. MinIO cluster architecture is distributed, storing data across nodes for HA and fault tolerance. MinIO uses Erasure Coding for durability — when a node fails, remaining nodes reconstruct lost data.

### Shared log

The LogService is the only component in MatrixOne with distributed transaction state. Three-node Raft architecture keeps it working through a single-node failure. It provides eventual-consistency guarantees for the whole MatrixOne cluster.

### Transaction layer

The Transaction Node handles conflict detection and arbitration — stateless. On failure, Kubernetes relaunches it within seconds — continuous availability. The current version supports a single Transaction Node; multi-TN is on the roadmap for stronger HA.

### Compute layer

The Compute Node parses queries and generates / executes plans — stateless. On failure, Kubernetes relaunches it within seconds — continuous availability.

### Proxy

Proxy (in the resource-scheduling layer) groups CNs for workload isolation and load-balances user connections within groups. Proxy runs as multiple replicas for HA.
