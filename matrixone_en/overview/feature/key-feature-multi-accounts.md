# Multi-tenancy

MatrixOne uses a single-cluster, multi-tenant design. A tenant (Account) is a logical unit for resource allocation and database management. MatrixOne's multi-tenant mode provides per-tenant database instances with logical isolation — keeping data safe, preventing leaks and tampering.

## Business need

As enterprises grow — with more business units or project teams and more data — they need flexible tenant management that meets independent requirements. MatrixOne's multi-tenancy makes managing tenant data resources simple, enabling analytics, reporting, and other business flows to run smoothly and accurately — and improving efficiency while lowering management cost.

## Benefits

- **Lower operational cost**: many users share one cluster — avoiding the cost of many cluster deployments. Hardware and software spend drops.

- **Resource and workload isolation**: data security and reliability improve — users' data and workloads are isolated from one another; issues or load spikes in one tenant don't affect others.

- **Dynamic resource allocation**: each tenant scales resources independently — maximizing utilization against diverse workloads.

- **Unified management**: tenants are isolated and independent, but admins can manage them centrally through the system tenant — e.g., rapid tenant creation or batch cleanup.

- **Tenant data sharing**: some cross-tenant analytics require data sharing. MatrixOne provides a complete publish / subscribe mechanism for tenant data — supporting more flexible analytical needs.

- **Cross-region deployment**: multi-region tenants can be colocated with their users. MatrixOne lets different tenants in the same cluster sit in different regions, serving business nearby.

## Technical architecture

MatrixOne's multi-tenant system includes two tenant types: the system tenant (`sys`) and regular tenants. `sys` is built into the cluster — it's the default login after cluster startup and its duties include:

- Storing and managing cluster-level system tables.
- Managing cluster features — e.g., create / drop tenants, change system configuration.

Regular tenants are created by `sys` and look like database instances — you must specify a tenant name when connecting. They offer:

- Create their own users.
- Create databases, tables, and all object types.
- Their own `information_schema` and other system databases.
- Their own system variables.
- Other characteristics expected of a database instance.

### Multi-tenant resource isolation

MatrixOne's distributed cluster achieves resource isolation via the Proxy module and CN resource groups.

When a user connects, the connection goes through Proxy. Based on the CN's tenant labels, Proxy routes to a CN in the tenant's CN group — picking the least-loaded CN by load-balancing. In MatrixOne, CNs are containerized, so they're naturally isolated. A tenant's CN group is a set of CNs labeled for that tenant. If resources run short, scale the CN group horizontally — without competing against other groups.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/multi-account-proxy.png width=50% heigth=50%/>
</div>

## Applications

MatrixOne's multi-tenancy shines in the following scenarios.

### Multi-tenant SaaS applications

Multi-tenant design is critical for SaaS serving many enterprise customers.

#### Traditional architectures

Traditional multi-tenant architectures store and manage each tenant's data at the database layer — often with shared-database (each tenant shares a DB but has its own tables / columns) or dedicated-database (each tenant gets its own DB) patterns.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/traditional-arch.png width=60% heigth=60%/>
</div>

Both have drawbacks:

- Shared-DB relies on app-layer SQL and code to distinguish tenants — data and resource isolation are weak; a sudden load spike from one tenant can starve others. But shared-DB uses one cluster, keeping resource cost and operational complexity low; upgrades, scaling, and app changes happen once globally.
- Per-tenant-DB gives strong isolation — at high resource cost and operational complexity. When tenant count passes ~100, routine ops like unified upgrades become extremely time-consuming.

#### MatrixOne architecture

MatrixOne's multi-tenancy changes the equation. Tenants still share a MatrixOne cluster, managed uniformly through the system tenant. Native multi-tenancy provides isolation; each tenant scales resources independently — reducing operational complexity. This meets isolation needs while keeping resource and ops costs low.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/mo-account-arch.png width=30% heigth=30%/>
</div>

| Multi-tenant model | Data isolation | Resource cost | Resource isolation | Ops complexity |
|---|---|---|---|---|
| Shared-DB | Low | Low | Low | Low |
| Per-tenant DB | High | High | High | High |
| MatrixOne | High | Low | High | Low |

### Microservice application architecture

Microservices assemble applications from small services, each in its own process and communicating via lightweight HTTP APIs. Services are typically bounded by business capability, independently developed and deployed, and released via automation.

Microservices face the same shared-vs-dedicated database dilemma. Typically each service has its own database — fitting microservice principles: each service develops, deploys, and scales independently. Schema changes in one service don't affect others. When one service needs extra capacity, scale just that service. And if a service needs specialized database capabilities (Elastic Search, vector search, etc.), this model keeps things flexible.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/microservice-arch.png width=60% heigth=60%/>
</div>

But microservices ultimately serve one business — services need to share data, replaying the SaaS multi-tenancy dilemma.

MatrixOne's multi-tenancy balances both: each microservice maintains data and scaling independence while allowing controlled sharing.

### Group subsidiaries / business units

Conglomerates often split by regional subsidiaries or business units that operate independently — with their own production, sales, tech support, and IT. But headquarters needs a complete business view, so subsidiaries regularly report large volumes of data.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/business.png width=80% heigth=80%/>
</div>

The database design faces the same sharing-vs-isolation tradeoffs. Geography adds another dimension: subsidiaries are typically regional, serving users locally. Manufacturers, for example, are often headquartered in large cities but have factories in second- and third-tier cities. Those factories integrate tightly with ERP / MES and need local deployment — while HQ needs visibility. Traditional architectures deploy separate databases and push data synchronization up into the application layer.

MatrixOne's multi-tenancy cleanly addresses the sharing-vs-isolation dilemma. CNs can sit close to subsidiary regions; as long as the network is connected, they naturally form one cluster with the HQ — enabling local business while meeting HQ reporting and analytics needs efficiently.

## Reference

See more on multi-tenancy:

- [Multi-tenancy use cases](../../Security/role-priviledge-management/app-scenarios.md)
- [Quickstart: create a tenant and verify resource isolation](../../Security/how-tos/quick-start-create-account.md)
