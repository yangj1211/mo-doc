# **常见问题解答：MatrixOne Intelligence**

## Q：**MatrixOne Intelligence 是什么？**

A：MatrixOne Intelligence 是一个全托管的云原生数据平台，旨在为 HSTAP 数据库 MatrixOne 提供云上服务。这一云上服务显著降低了 MatrixOne 部署和运维的成本。如果您更喜欢纯私有化部署，也可以参考 [MatrixOne 产品介绍](https://docs.matrixorigin.cn/2.0.3/MatrixOne/FAQs/product-faqs/)以获取更多信息。

## Q：**MatrixOne Intelligence 有免费版本吗？**

A：是的，MatrixOne Intelligence 目前为每位用户提供最多 5 个免费数据库实例。每个实例每月将赠送一定数量的计算和存储资源，总价值高达 500 元。这些资源会在每个月自动重置，而时间上没有设定限制。

## Q：**MatrixOne Intelligence 是否兼容 MySQL？**

A：是的，MatrixOne Intelligence 几乎完全兼容 MySQL，因此您可以轻松将 MySQL 数据迁移到 MatrixOne Intelligence 以进行试用或开发。有关更多具体信息，请参考 [MySQL 兼容性](https://docs.matrixorigin.cn/2.0.3/MatrixOne/FAQs/mysql-compatibility/)。

## Q：**MatrixOne Intelligence 上的实例指的是什么？**

A：在 MatrixOne Intelligence 中，您可以创建多个 MatrixOne(MO) 实例。每个 MO 实例相当于一个传统数据库，包括库、表、视图、列等数据库对象。MatrixOne Intelligence 支持创建多种类型的 MO 实例，其中 Serverless 实例和 Standard 实例实际上是 MO 集群的租户。利用多租户能力，您可以快速创建（仅需秒级时间）和扩展或缩减实例，并享有高性价比。

## Q：**有哪些方式可以连接到 MatrixOne Intelligence 上的实例？**

A：MatrixOne(MO) 实例虽然部署在云上，但支持公网和公有云之间的私网两种访问方式。初期的调研和试用阶段，您可以使用公网直接连接 MO 实例。但在测试或进入生产环境时，建议使用私网访问 MO 实例。从工具访问角度来看，MO 支持多种工具和编程语言，包括 MySQL、JDBC、Python、Go 等。此外，MatrixOne Intelligence 还提供了一个直观的数据库管理平台，用于查看数据库的运行状态并执行 SQL 语句。获取更多详情，请参考[连接 MatrixOne 实例](https://docs.matrixorigin.cn/2.0.3/MatrixOne/FAQs/connect-to-mo/)。

## Q：**什么是 Serverless 实例？它有哪些特点？**

A：Serverless 实例是 MatrixOne Intelligence 上的一种简单、经济的 MatrixOne 实例。创建时需要规划计算节点和存储资源的规模，但在业务变化时无需手动调整计算资源。Serverless 实例的计费也相对简单，不再需要为计算节点、I/O、网络出口流量分别付费。用户只需为每条 SQL 的执行计费，计费单位为 Compute Unit（CU）。

## Q：**如何控制 Serverless 实例的消费？**

A：Serverless 实例是后付费的，每个整点后将统计前一个小时的消费费用。尽管 Serverless 实例提供了无限伸缩的性能，但在前一个小时内提供无限资源，可能导致账单不可控。为此，Serverless 实例提供了消费限制功能。您可以设置每日或每月的消费上限，MatrixOne Intelligence 会实时监控消费上限和消费速率，并会提前发出警报。一旦达到消费上限，服务可能会降级或暂停。

## Q：**如何查看 Serverless 实例中每条 SQL 的消费？**

A：在 MatrixOne Intelligence 实例管理平台的实例列表中，单击要查看的实例的连接按钮和连接到平台按钮，即可登录 MatrixOne Intelligence 数据管理平台。然后，点击左侧的 "查询" -> "查询历史" 菜单，您将看到所有历史查询。MatrixOne Intelligence 将统计并显示每一条 SQL 的 CU 消耗数量。默认情况下，CU 列是未显示的，您可以单击列按钮并选中 CU。

## Q：**实例可以删除吗？删除后可以恢复吗？**

A：是的，您可以在实例列表中单击某个实例的 "终止" 按钮来删除实例。MatrixOne Intelligence 会在删除后自动保留实例 3 天。如果误删，您可以在 3 天内将实例恢复。

## Q：**实例的存储如何计费？**

A：MatrixOne 使用对象存储技术，将几乎所有数据存储在公有云的对象存储上。这种存储方式经济高效且高度可用。MatrixOne 的存储费用与公有云官网的价格相同。对于后付费实例（如 Serverless 实例或 Standard 实例），MatrixOne Intelligence 会按小时计算存储的平均使用量。对于预付费实例（如 Standard 包年包月实例），MatrixOne Intelligence 将一次性按照公有云对象存储的价格和折扣扣费。

## Q：**MatrixOne Intelligence 有折扣或优惠吗？**

A：是的，MatrixOne Intelligence 提供与公有云上数据库类似的折扣，包括预付费实例的 1 年 85 折、2 年 7 折和 3 年 5 折的优惠。此外，MatrixOne Intelligence 还提供额外的折扣机制。需要注意的是，这里的折扣仅涉及计算资源，因为数据存储的价格与公有云价格一致，所以不提供存储折扣。MatrixOne Intelligence 还提供代金券，您可以通过各种活动或商务渠道获取。获取更多折扣和优惠信息，请联系我们的销售和市场运营团队。
