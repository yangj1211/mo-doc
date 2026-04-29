# 数据分享

MatrixOne Intelligence 提供集群内跨实例的数据发布与订阅能力，打破实例间的数据边界，显著提升数据流动性与复用效率。用户可通过数据库管理界面完成数据的发布与订阅配置，实现不同实例之间的数据实时共享与同步。同时，平台支持将数据库实例中的业务数据直接发布至 GenAI 工作区，为 NL2SQL 等智能分析与应用场景提供可靠的数据基础，帮助用户更高效地实现数据驱动的智能化决策。

## 应用场景

发布订阅功能具有多种典型的应用场景：

- **数据同步**：当一个数据库需要与另一个数据库保持同步时，发布订阅功能可以用来将数据更改发送到订阅者数据库。例如，当一个网站需要将数据从一个地理位置传输到另一个地理位置时，发布订阅功能可以用来确保两个数据库之间的数据同步。

- **实时数据处理**：发布订阅功能可以用来实现实时数据处理。例如，当一个网站需要对来自不同用户的数据进行处理时，发布订阅功能可以用来将数据传输到处理程序中进行处理，以便实现实时数据分析和决策。

- **数据共享**：当需要与合作伙伴或内部部门共享数据库信息时，可以通过发布订阅安全地共享数据，同时控制数据访问权限。

- **报表和分析**：在需要进行大量数据查询和分析的场景中，在订阅端进行复杂的报表生成和数据分析，避免影响主实例的性能。

## 发布订阅操作

### 发布订阅数据库

1. **发布**: 在 `实例_1` 上创建名为 `mall` 的数据库以及其中的 `customer` 表。现在我们需要发布这个数据库，首先得登录到数据库管理平台。依次点击**数据库** > **发布** > **添加发布**，在发布信息填写页面，创建一个命名为 `pub_mall` 的发布，选择 `mall` 作为要发布的数据库。发布目标设置为本组织内的 `实例_2`：

    ```sql
    -- 实例_1
    create database mall;
    CREATE TABLE mall.customer (
    customer_id INT,
    customer_name VARCHAR(255)
    );
    ```

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-01.png width=80% heigth=80%/>
    </div>

    - **发布名**：发布名，唯一值，长度不大于 64 字符。
    - **发布数据库**：发布对应的数据库名，不支持发布订阅库和系统数据库。
    - **发布权限**：发布库为只读。
    - **发布目标**：发布目标仅限于同一集群内的实例。您至少需要指定一个发布目标，而且可以添加任意数量的目标。通过下拉菜单，可以选择本组织内的实例，或者手动输入其他组织的实例 ID。请注意，不允许将实例设置为发布给它自己。如果是工作区则需要输入工作区的 id。
    - **备注**：对于该发布的备注

    发布创建成功后，您将能够查看发布的详细信息，并可以对其进行编辑或删除。

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-04.png width=100% heigth=100%/>
    </div>

2. **订阅**: `实例_2` 登录到数据库管理平台，依次点击**数据库** > **订阅** > **+**，输入订阅名 sub_mall (订阅自 `实例_1` 的 pub_mall)

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-02.png width=90% heigth=90%/>
    </div>

    订阅成功后，您将能够查看发布的详细信息，并可以对其进行编辑或删除。

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-10.png width=90% heigth=90%/>
    </div>

    查看订阅库，可以发现 `实例_1` 数据库 mall 中的所有数据现在皆可被读取：

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-09.png width=90% heigth=90%/>
    </div>

### 修改发布内容

1. **修改发布**: `实例_1` 创建数据库 mall2 和表 mall2.customer2，修改发布内容：

    ```sql
    -- 实例_1
    create database mall2;
    CREATE TABLE mall2.customer2 (
    customer_id INT,
    customer_name VARCHAR(255)
    );
    ```

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-05.png width=60% heigth=60%/>
    </div>

2. **查看订阅**: `实例_2` 查看订阅，能看到发布数据库修改后的内容：

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-06.png width=100% heigth=100%/>
    </div>

### 删除发布对象

发布者可删除已发布的发布对象，订阅者随即无法连接相关的订阅对象，但是可以删除该订阅。

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-07.png width=90% heigth=90%/>
</div>

### 自动订阅同名发布

发布者删除发布，再创建同名发布，之前的订阅者无需额外操作，即可连接至最新订阅对象。

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/data-sharing/pub-08.png width=90% heigth=90%/>
</div>

:::{note}
如果需要使用 SQL 语句进行发布订阅，请参考章节 [CREATE PUBLICATION](../../../reference/SQL-Reference/Data-Definition-Language/create-publication.md) 和 [CREATE...FROM...PUBLICATION...](../../../reference/SQL-Reference/Data-Definition-Language/create-subscription.md)。
:::
## 限制

- 只有 ACCOUNTADMIN 或 MOADMIN 角色可以创建发布与订阅。
- 订阅端由 ACCOUNTADMIN 或 MOADMIN 角色操作访问订阅数据权限。
- 目前只支持数据库级别的发布订阅
- 一次只能发布一个数据库。
- 目前只开放了订阅库读权限。
- 删除租户前需要删除其所有发布。
- 发布端不能删除已经发布的数据库。
- 若发布端删除了发布，但订阅库中的对应对象仍存在，此时订阅端无法访问订阅对象，但可删除对应订阅。
- 发布名和订阅名需要由数字 0-9，英文字母大小写、_、$组成，长度不能超过 64 个字符。
