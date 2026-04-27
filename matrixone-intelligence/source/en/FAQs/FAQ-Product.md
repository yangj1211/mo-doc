# Frequently Asked Questions: MatrixOne Intelligence

## Q: What is MatrixOne Intelligence?

A: MatrixOne Intelligence is a fully managed, cloud-native data platform designed to deliver MatrixOne — the HSTAP database — as a cloud service. By moving deployment and operations to the cloud, it dramatically lowers the total cost of running MatrixOne. If you prefer a fully on-premise deployment, please refer to the [MatrixOne product introduction](https://docs.matrixorigin.cn/2.0.3/MatrixOne/FAQs/product-faqs/) instead.

## Q: Is there a free tier?

A: Yes. MatrixOne Intelligence currently offers each user up to 5 free database instances. Each instance receives a monthly grant of compute and storage resources worth up to ¥500. The grant resets automatically every month, with no time limit on how long you can use the free tier.

## Q: Is it MySQL-compatible?

A: Yes. MatrixOne Intelligence is almost fully MySQL-compatible, so you can easily migrate MySQL data into MatrixOne Intelligence for evaluation or development. For details, see [MySQL compatibility](https://docs.matrixorigin.cn/2.0.3/MatrixOne/FAQs/mysql-compatibility/).

## Q: What is an "instance" on MatrixOne Intelligence?

A: On MatrixOne Intelligence you can create multiple MatrixOne (MO) instances. Each MO instance behaves like a traditional database — it owns databases, tables, views, columns, and other database objects. The platform supports multiple types of MO instances; Serverless and Standard instances are tenants of an underlying MO cluster. Thanks to multi-tenancy, instances can be created in seconds and scaled up or down on demand at favorable cost.

## Q: How can I connect to a MatrixOne Intelligence instance?

A: Although MO instances are deployed in the cloud, they can be reached over both the public internet and a private network within the same cloud. For initial evaluation and trials, public-internet access is fine. For testing or production, we strongly recommend private-network access. From a client perspective, MatrixOne supports many tools and languages — MySQL CLI, JDBC, Python, Go, and more. The platform also ships an intuitive database management console for inspecting database health and running SQL. For details, see [Connect to a MatrixOne instance](https://docs.matrixorigin.cn/2.0.3/MatrixOne/FAQs/connect-to-mo/).

## Q: What is a Serverless instance, and what makes it special?

A: A Serverless instance is a simple, cost-effective MatrixOne instance on MatrixOne Intelligence. You plan a compute and storage envelope when creating it, but you do not need to manually adjust compute as workloads change. Billing is also simplified — you no longer pay separately for compute nodes, I/O, or egress traffic. You only pay per SQL execution, denominated in Compute Units (CU).

## Q: How do I cap spend on a Serverless instance?

A: Serverless instances are post-paid. Charges from the previous hour are settled at the top of every hour. While Serverless gives you unbounded performance scaling, an unbounded hour can also produce an unbounded bill. To prevent surprises, Serverless ships a spend-limit feature: set a daily or monthly cap and the platform tracks both the cap and the burn rate in real time, alerting you ahead of the limit. Once a cap is hit, the service may be degraded or paused.

## Q: How do I see CU consumption per SQL on a Serverless instance?

A: From the instance list in the management console, click **Connect** on the target instance, then **Connect to platform** to log into the database management console. Open **Query > Query history** in the left nav to see every historical query. The platform records the CU cost for each SQL. The CU column is hidden by default — click the column toggle and enable **CU**.

## Q: Can I delete an instance? Can I undo it?

A: Yes. Click **Terminate** on the instance in the instance list to delete it. The platform retains the deleted instance for 3 days. If you deleted by mistake, you can recover it within that window.

## Q: How is instance storage billed?

A: MatrixOne stores almost all data on cloud object storage. This is cost-effective and highly available. Storage prices match the underlying public cloud's published prices. For post-paid instances (such as Serverless or Standard pay-as-you-go), the platform calculates an hourly average of storage usage. For pre-paid instances (such as Standard with a yearly or monthly subscription), the storage fee is charged once at the public cloud's object-storage price and discount.

## Q: Are there discounts or promotions?

A: Yes. MatrixOne Intelligence offers discounts comparable to public-cloud databases — for example, 15% off for 1-year commitments, 30% off for 2 years, and 50% off for 3 years on pre-paid instances. Additional discount mechanisms exist on top of that. Note that discounts apply only to compute resources; storage prices follow the public cloud's published rates and are not discounted. The platform also issues vouchers obtainable through campaigns and sales channels. For more discount and promotion details, please contact our sales and marketing team.
