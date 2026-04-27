# 私网连接（PrivateLink）

## 介绍

阿里云的私网连接（PrivateLink）是一项私有网络连接服务，允许应用程序通过私有 IP 地址与云服务进行安全、私密的通信。通过 PrivateLink，您可以将应用程序连接到位于阿里云同一地区（region）的 MatrixOne Intelligence 实例，这不仅节省了公网流量，还提升了连接带宽，从而实现更加高效、稳定的网络访问。

:::{note}
为了获得更高的网络稳定性和最低延迟，推荐您将应用部署在与 MatrixOne Intelligence 实例相同的可用区。
:::
MatrixOne Intelligence 的架构如下：

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/priveteLink-connectInstance-arch.jpg)

有关阿里云私网连接（PrivateLink）概念的更多详细信息，请参阅以下文档：

- [什么是私网连接](https://help.aliyun.com/document_detail/161974.html)
- [阿里云私网连接概述](https://help.aliyun.com/document_detail/2539840.html)

## 如何使用私网链接

### 步骤一：在 MatrixOne Intelligence 实例管理平台获取私网连接相关信息

在 MatrixOne Intelligence 实例管理平台的实例列表中，找到需要访问的 MatrixOne 实例，依次点击**连接 > 通过第三方工具连接>私网连接**，这时可以获取服务名称，可用区 ID，地区 ID。

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/priveteLink-connect.png width=80% heigth=80%/>
</div>

### 步骤二：在阿里云控制台配置终端节点

使用阿里云管理控制台创建终端节点，请按照以下步骤操作：

1. 登录阿里云控制台[阿里云控制台](https://home.console.aliyun.com/home)，打开阿里云 VPC 控制台[专有网络](https://vpc.console.aliyun.com/)。

2. 从区域下拉列表中选择您的 VPC 所在的地域。在左侧导航栏中单击**终端节点**，在右侧页面单击左上角的**创建终端节点**，进入**创建终端节点**页面。

    ![创建终端节点](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/priveteLink-createNode.png)

3. 选择**接口终端节点**。

4. 搜索框中搜索步骤一中的**服务名称**，这里就可以看到可用服务，选中可用服务。

5. 选择业务服务所在的 vpc，添加完专有网络，会出现下面两个选择项。

    ![设置安全组&amp;网络交换机](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/priveteLink-setSafeGroup.png)

6. 选择已有安全组或者创建一个。

7. 可用区交换机如果存在要选择在端点服务所在可用区，不存在请创建一个；这里默认要填两个，这些交换机会用于不同的可用区，以实现高可用性和容错能力。

8. 单击创建端点。等待创建成功，在终端节点详情页面您即可得到**终端节点服务域名**。
    <div align="center">
        <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/privatelink-1.png width=80% heigth=80%/>
    </div>

### 步骤三：在您的 ECS 主机连接 MatrixOne Intelligence 服务

1. 确保您的 ECS 主机已经安装 Mysql Client 客户端。
2. 使用 MySQL 客户端连接 MatrixOne Intelligence 服务时，需将 **host** 设置为**终端节点服务的域名**。

```mysql
mysql -h <privatelink_endpoint_domain> -P 6001 -u xxx:admin:accountadmin  -p
```

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/privatelink-4.png)