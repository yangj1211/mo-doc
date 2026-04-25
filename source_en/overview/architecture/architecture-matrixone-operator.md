# MatrixOne-Operator Design and Implementation

MatrixOne is a cloud-native distributed database — naturally adapted to cloud infrastructure and optimized for cloud cost models. Unlike typical SaaS, for performance and data-safety reasons, databases often need to follow the applications — running on the same infrastructure. To serve as many users as possible, MatrixOne must adapt to all kinds of public, private, and hybrid clouds. The greatest common divisor is Kubernetes (K8s). So MatrixOne uses K8s as its default runtime for distributed deployments — unifying adaptation across clouds.
MatrixOne-Operator is MatrixOne's automated deployment / operations software on K8s — it extends K8s, offering a declarative, K8s-style API for managing MatrixOne clusters.

This article walks through MatrixOne-Operator's design and implementation, and shares our experience.

## Design

K8s natively provides the StatefulSet API for orchestrating stateful apps — but because application-layer state is hard to abstract uniformly across stateful apps, K8s doesn't natively manage application state. The Operator pattern addresses this. A typical K8s Operator has two parts — API and Controller:

- **API**

Usually declared via K8s CustomResourceDefinition (CRD). After submitting a CRD to the K8s api-server, api-server registers a corresponding RESTful API. K8s clients can `GET`, `LIST`, `POST`, `DELETE` against the new API the same way they would against built-in resources. By convention, `.spec` is user-managed — declaring the desired state; `.status` is controller-managed — exposing the actual state.

- **Controller**

A controller is a long-running piece of code watching a set of K8s objects, including our new API. Based on desired state and actual state it observes (actual state is collected from reality and then written to `.status`, not read directly from it), the controller automates operations to drive actual state toward desired state. This process loops forever — called the "control loop" (or "reconciliation loop," echoing K8s' "orchestration" metaphor).

The following is a simplified MatrixOneCluster API example:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/mo-op-1.png width=70% heigth=70%/>
</div>

MatrixOne-Operator provides workload-style APIs (MatrixOneCluster), task-style APIs (backup/restore), and resource-style APIs (object-storage bucket). Each API and controller has its own design concerns, but all follow this pattern. We'll cover the key tradeoffs.

## Cluster API design

A distributed MO cluster consists of Log Service, Transaction Node, Compute Node, Proxy, and more. CNs need heterogeneous placement for workload-specific hardware, cross-cloud, and cloud-edge. Managing the whole cluster via one API object with one controller is convenient, but a maintenance nightmare. So MatrixOne-Operator committed early to the principle of **loosely-coupled, fine-grained APIs** — designing LogSet, CNSet, ProxySet, BucketClaim, etc. with clear responsibilities and independent controllers. To keep usability, a `MatrixOneCluster` API was introduced. The MatrixOneCluster controller doesn't repeat the other controllers' work — when a cluster needs a LogSet for the log service, the MatrixOneCluster controller just creates a LogSet object and delegates the rest.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/mo-op-2.png width=60% heigth=60%/>
</div>

Under this design, there are many APIs but users only need to care about MatrixOneCluster; MatrixOne-Operator developers face a narrow scope per fine-grained API and controller.

Inevitably, API objects have dependencies — e.g., Transaction Nodes and Compute Nodes depend on HAKeeper running in Log Service for service discovery. So we must start the log service first and bootstrap HAKeeper before starting TN and CN. We could push that logic into the MatrixOneCluster controller — but that leaks knowledge from other controllers and recouples them. Instead, in mo-operator, all inter-component dependency logic lives on the depending side. The depended-on side simply exposes state via conventional `.status`. For example, when reconciling a CNSet, the controller actively waits until the LogSet the CNSet points to is ready — neither the LogSet controller nor the higher-level MatrixOneCluster controller needs to know.

Loose, fine-grained APIs also suit heterogeneous CN orchestration. Beyond declaring multiple CN groups in MatrixOneCluster for convenience, you can create a standalone CNSet that joins an existing cluster — which can live in another K8s cluster. With network connectivity, cross-cloud or cloud-edge MO orchestration becomes feasible.

During iteration, MatrixOne-Operator tends to add features through new API objects. For example, when managing object storage, MatrixOne-Operator must ensure no overlap between clusters and cleanup after cluster destroy. The answer: a new BucketClaim API — mirroring K8s PersistentVolumeClaim's control logic — implementing object-storage path lifecycle in an independent controller to avoid complex race-condition handling and code coupling.

## Controller implementation

K8s provides the controller-runtime package for building controllers, but for generality the API is low-level:

```
Reconcile(ctx context.Context, req Request)(Result, error)
```

A controller implements `Reconcile`, registers with controller-runtime declaring which objects to watch and filter rules. controller-runtime calls the controller's `Reconcile` on each relevant object change or retry, passing an identifier. This method contains significant boilerplate. Pseudocode:

```
func reconcile(namespace+name of object A) {
  fetch A.spec
  if A is being deleted {
    perform cleanup
    update cleanup progress to A.status
    remove finalizer on A
  } else {
    add finalizer to A
    run reconciliation
    update progress to A.status
  }
}
```

Similar boilerplate appears across community controllers; developers are forced to think about non-business concerns: proper finalizer handling (avoid resource leaks), timely progress / error updates in `status` for visibility, logger context passing, and kube-client caching.

Since we don't need general-purpose coverage, MatrixOne-Operator introduces a more specialized abstraction — the Actor interface:

```
type Actor[T client.Object] interface {  
    Observe(*Context[T]) (Action[T], error)  
    Finalize(*Context[T]) (done bool, err error)  
}

type Action[T client.Object] func(*Context[T]) error
```

The generic controller-framework logic behind handles all the boilerplate and prepares a `Context[T]` with the target object and a properly-contextualized Logger, EventRecorder, and KubeClient. Then:

- For an undeleted object, call `Actor.Observe` — real business reconciliation logic runs.

- For an object being deleted, call `Actor.Finalize` — run business cleanup; retry until it returns done; finalizer is removed last.

Object state machine:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/mo-op-3.png width=70% heigth=70%/>
</div>

Under this model, create and destroy lifecycle management is straightforward — call K8s APIs to provision storage, deploy workloads, configure service discovery based on MO ops knowledge, and reverse the process on delete. Update reconciliation is also standard diff logic. For `cnSets` in MatrixOneCluster:

```
func sync(c MatrixOneCluster) {
  existingCNSets := gather all CNSets of this cluster
  for _, desired := range c.spec.CNSets {
    cnSet := buildCNSet(desired)
    if _, ok := existingCNSets[cnSet.Name]; ok {
      // 1. CNSet exists — update
      ....
      // 2. Mark this cnSet as needed by desired state
      delete(existingCNSets, cnSet.Name)
    } else {
      // CNSet doesn't exist — create
      ....
    }
  }
  for _, orphan := range existingCNSets {
    // Clean up CNSets present in reality but not in desired state
  }
}
```

One tricky area: ConfigMap / Secret updates. MO — like many apps — needs config files and must restart to reload. Config is typically stored in native K8s ConfigMaps. A common pitfall: ConfigMap contents are mutable, while most apps read it only at startup. Viewing the ConfigMap referenced by a pod doesn't tell you the current running config — it may have changed since startup. Further, to roll pods on ConfigMap changes, a common trick is hashing ConfigMap content into the pod template's annotation — changing the annotation on ConfigMap change forces a rolling update. But in-place ConfigMap edits still cause surprises:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/mo-op-4.png width=70% heigth=70%/>
</div>

Suppose the ConfigMap hash annotation changes from 123 to 321. If 321 fails to become Ready due to bad config, the rolling update correctly stalls and contains the blast radius. However, pods not yet updated still read the new ConfigMap — one container restart or pod recreation and they break. This differs from updating the image or other fields: under normal updates, green pods belong to the old ReplicaSet/ControllerRevision — restart or recreate uses the old config, and blast radius stays bounded.

Root cause: ConfigMap content isn't in the pod spec — modifying ConfigMap in place violates the **immutable infrastructure** principle.

So MatrixOne-Operator makes every object referenced from pods immutable. For ConfigMap: every config change via CRD produces a new ConfigMap and rolls the component's replicas onto the new ConfigMap:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/mo-op-5.png width=70% heigth=70%/>
</div>

Under this principle, at any moment the pod spec uniquely determines all pod info. Rolling updates behave correctly.

## Application state management

Besides lifecycle, MatrixOne-Operator has another important job — managing application state. But distributed systems usually manage their own state via heartbeats — why replicate that in the Operator?

The Operator encodes automation knowledge — e.g., it knows which Pod is about to be recreated/restarted next during a rolling update. It can pre-adjust application state — e.g., migrate workload off a pod — to minimize the impact of rolling updates. Two common implementations:

- Use pod lifecycle hooks (InitContainer, PostStart, PreStop) to adjust application state there.

- Call the app's API from inside the Operator's reconciliation loop.

Option 1 is simpler; option 2 is more flexible and handles complex cases better. For example, scaling in a CNSet requires migrating sessions off the shrinking CN pod before terminating it. If this were in PreStop, it's irreversible. In reality, a group of CNs may scale in and then scale back out before shrinking completes (especially with autoscaling) — the Operator's loop can notice this and reuse the CN still going offline — via MO's internal management API, restore it to serving state, stop session migration, and have the Proxy route new sessions to it — avoiding launching a new CN.

## Conclusion

As a mainstream approach to extending K8s orchestration, the Operator pattern has mature libraries and tooling — and plenty of open-source references. Writing an Operator for K8s isn't novel. But real complexity lives in business details — addressing them requires mastery of both K8s and your domain. MatrixOne, as a cloud-native distributed database, shares many design ideas and domain knowledge with other cloud-native systems. We hope this short article illustrates mo-operator's design choices and gives you useful perspective when designing your own Operator.

## Related

For MatrixOne-Operator deployment and operations, see [Operator management](../../Deploy/MatrixOne-Operator-mgmt.md).
