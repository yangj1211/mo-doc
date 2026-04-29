# Pricing: Standard instances

For Standard Instances, MO Intelligence charges based on the resources you consume: compute nodes, storage, data requests, and public network egress. The rest of this page walks through each line item.

## Compute node unit price

Compute nodes (CNs) in MatrixOne handle SQL execution. Provision the right number and size of CNs for your workload.

Standard Instance CNs offer two billing models: **subscription (annual / monthly)** and **pay-as-you-go**. With pay-as-you-go, you create and stop instances on demand and we bill hourly for actual usage. The unit price is higher, so this model is best for evaluation. For production we recommend subscription billing — the cost for the chosen term is collected up-front when you create the instance, and the longer the term, the deeper the discount.

Unit prices by node spec and billing model:

| Billing model      | 8c32g           | 16c64g         |
| ------------------ | --------------- | -------------- |
| Pay-as-you-go      | ¥4.8/hour       | ¥9.6/hour      |
| Monthly            | ¥2304/month     | ¥4608/month    |
| Annual             | ¥1958.4/month   | ¥3916.8/month  |

:::{note}
The table shows list prices. Your actual price at purchase is the discounted price applicable at that time.
:::

## Storage unit price

Storage is the size of the data you store in a MatrixOne Intelligence instance. Thanks to MatrixOne's architecture, almost all your data lives on cost-effective object storage; we pass the Alibaba Cloud retail price through to you.

MatrixOne Intelligence storage today is pay-as-you-go only, priced at **¥0.15/GB-month**.

## Data request unit price

The data-request fee is the per-call cost between your SQL execution and object storage. Alibaba Cloud Object Storage (OSS) charges per request; MO Intelligence passes the retail rate through.

Because request count depends on actual usage, this fee isn't collected at instance creation — it's settled and deducted hourly. The unit price is **¥0.01 per 10,000 requests**.

## Public network egress unit price

You can reach a MO Intelligence instance on Alibaba Cloud over either the public network or a private network. Private access (e.g. VPC Peering, Private Link) carries no egress charges; public access does, and MO Intelligence passes the Alibaba Cloud public egress rate through.

Because public egress depends on actual usage, this fee isn't collected at instance creation — it's settled and deducted hourly. The unit price is **¥0.8/GB**.
