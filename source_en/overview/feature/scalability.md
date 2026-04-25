# Extreme Scalability

MatrixOne is a hyper-converged, heterogeneous, cloud-native database. Its storage/compute/transaction-separation architecture brings extreme elasticity — responding quickly to workload changes. As data and workload scale, the need for scalability intensifies.

From 0 to 100TB-scale data, from hundreds to tens of thousands of concurrent users — MatrixOne scales to meet performance demands.

## Business need

Enterprises need scalability for these pain points:

- **Growing data volume**: as business grows, data keeps accumulating. Weak scalability means slow queries and degraded operations.
- **Rising concurrency**: more users means more concurrent requests. Weak scalability means long response times and poor UX.
- **Evolving business requirements**: business changes over time. Weak scalability forces extra investment in DB tuning and restructuring.
- **System availability**: weak scalability complicates handling hardware or network failures, risking continuity.

A scalable database helps enterprises absorb data growth, handle rising concurrency, and preserve availability.

## Technical architecture

MatrixOne is entirely cloud-native — all components are containers managed by Kubernetes, which brings strong orchestration and management. Manual scaling often means just editing Kubernetes configuration.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/scalability.png width=50% heigth=50%/>
</div>

## Benefits

From the architecture diagram, extreme scalability manifests as:

* **Flexible scaling under a distributed architecture**: storage/compute separation with independent storage, transaction, and compute tiers lets MatrixOne scale elastically at the bottleneck. Storage is primarily object storage, with partial caching at CN. Transactions live at stateless TN. Compute lives at stateless CN. Multi-node architecture allocates resources better, preventing hotspots and contention.

* **Effectively infinite S3 storage**: core storage is S3. S3 is inherently HA and effectively unlimited — so MatrixOne's storage scalability is excellent. On-premises deployments use MinIO for S3; on public cloud, MatrixOne leverages the cloud-provider object store.

* **Stateless compute and transaction nodes**: CNs and TNs are stateless — both are safe to scale horizontally at any time, with no persisted data on them. This makes MatrixOne highly flexible under large concurrent requests. (In v0.8 TN isn't yet scalable, but since TN mostly handles commit metadata, a single TN serves large clusters well. TN scalability is being added in later versions.)

* **Independent scaling per workload / tenant**: via Proxy, CNs can be grouped into CN Sets labeled for independent scaling. You can bind a tenant to a CN Set, isolating tenants and scaling independently; you can also bind different workloads (reads vs writes, or TP vs AP) to distinct CN Sets for independent isolation and scaling.
