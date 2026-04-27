# 连接 MatrixOne 实例

在 MatrixOne Intelligence 实例创建完成后，您可以使用以下方法来连接到该实例。

## 连接工具方式

根据不同的连接工具，连接方式可分为以下几种：

### MySQL 管理工具

您可以使用支持 MySQL 协议的客户端管理工具来连接 MatrixOne 实例，例如 MySQL Client、Navicat、DBeaver 等。详细步骤请参考[客户端工具连接](../App-Develop/connect-mo/database-client-tools.md)。

### Java

您可以使用 JDBC 连接器或 Java ORMs 来连接到 MatrixOne 实例。详细步骤请参考[使用 Java ORMs 连接](../App-Develop/connect-mo/java-connect-to-matrixone/connect-mo-with-orm.md)。

### Python

您可以使用 Python 驱动程序来连接 MatrixOne 实例。详细步骤请参考[使用 Python 连接](../App-Develop/connect-mo/python-connect-to-matrixone.md)。

### Go

您可以使用 go-mysql-driver 驱动程序以 Go 语言连接 MatrixOne 实例。详细步骤请参考[使用 Golang 连接](../App-Develop/connect-mo/connect-to-matrixone-with-go.md)。

## 网络连接方式

根据不同的网络连接途径，连接方式可分为以下几种：

### 通过公网连接

这是一种最快、最简单的方式连接 MatrixOne 实例，但需要注意数据在公网传输时可能面临安全威胁，性能也不一定稳定。您可以结合 IP 白名单进一步提升安全性。

### 通过私网连接

这是一种较为安全和稳定的连接方式。MatrixOne Intelligence 实例提供 VPC 终端节点服务，允许用户在自己的 VPC 上设置私网访问连接。

### 通过数据库管理平台连接

MO Intelligence 为每个实例提供了界面化的数据库管理平台，用户可以使用浏览器快速、高效地访问和监控数据库。更多详细信息请参考[使用 Web 页面连接](../App-Develop/connect-mo/connect-mo-with-web.md)和[登录实例](../Instance-Mgmt/login-instance.md)。

希望这些连接方式的指南能帮助您成功连接到 MatrixOne 实例。如果您有任何疑问或需要进一步的帮助，请查阅我们的文档或联系支持团队。
