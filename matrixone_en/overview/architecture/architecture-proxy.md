# Proxy Architecture

Proxy is the sole component in MatrixOne that handles load balancing and SQL routing. By grouping CNs with labels and combining with Proxy's SQL dispatch, it implements session-level SQL routing to fit many scenarios.

The SQL dispatch architecture:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/proxy/proxy-arch.png width=70% heigth=70%/>
</div>

- The Kubernetes library layer uses Kubernetes' built-in features to keep Proxy HA and load-balanced.
- SQL Proxy supports long connections, allow-lists, and SQL dispatch — enabling CN load balancing and request forwarding.
- CNs don't have a read-replica concept — they're simply grouped via labels.

## Technical implementation

Given MatrixOne's compute-storage separation + multi-CN architecture and Proxy's responsibilities, HAKeeper and Proxy introduce the concept of CN label groups — a named set of CNs with a fixed replica count.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/proxy/proxy-arch-2.png width=40% heigth=40%/>
</div>

Flow:

1. Create different CN labels via `yaml` configuration (config, replica count, tenant).
2. When the MatrixOne cluster starts, it launches the same number of pods per CN label, and HAKeeper labels them uniformly.
3. MatrixOne Operator (the Kubernetes resource manager) keeps the CN count per label group stable — immediately launching replacements when a CN goes down.
4. Proxy inspects session parameters to route a session to the matching CN group for SQL routing.

    - If a session request doesn't match any CN label, Proxy looks for an unlabeled CN group; if none, the connection fails.
    - On scale-out, Proxy migrates existing sessions onto new CNs based on existing CN session counts — achieving balance.
    - On scale-in, Proxy migrates sessions from CNs going offline onto others — achieving balance.

5. Within a label group, Proxy does intra-group load balancing.

Proxy analyzes session request parameters to decide if they match a CN label. In SQL routing, session parameters are used to look up the matching CN label group. Specifically, Proxy may check certain fields in CN labels — e.g., tenant info, replica count — to route requests to the right CN label group. This way, Proxy matches session requests to CN labels and routes to the correct CN.

## Related

For more on achieving load balancing via Proxy, see [Tenant and workload isolation via Proxy](../../Deploy/mgmt-cn-group-using-proxy.md).
