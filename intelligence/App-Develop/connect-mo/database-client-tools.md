# 客户端工具连接

MatrixOne 现在支持通过以下几种数据库客户端工具的方式连接 MatrixOne 服务：

- MySQL Client
- Navicat
- DBeaver

## 前期准备

- 已完成[创建实例](../../Instance-Mgmt/create-instance/create-serverless-instance.md)。
- 已经[获取 MatrixOne Intelligence 实例的连接命令](../../Instance-Mgmt/create-instance.md#_10)。
- 默认为公网连接，若想使用私网连接请参考章节[私网连接]( ../../Security/private-link.md)完成配置。

## 通过 MySQL Client 连接 MatrixOne Intelligence 服务

1. 下载安装 [MySQL Client](https://dev.mysql.com/downloads/mysql/)。

2. 下载完成后，你可以使用 MySQL 命令行客户端来连接 MatrixOne Intelligence 服务，只需要复制你获取的 MatrixOne Intelligence 实例的连接命令，并根据提示输入密码。

    ```
    mysql -h freetier-01.cn-hangzhou.cluster.matrixonecloud.cn -P 6001 -u 585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx:admin:accountadmin  -p
    Enter password:
    ```

:::{note}
如果需要使用 LOAD DATA LOCAL 语句读取本地文件，需要在连接时添加参数 `--local-infile`。
:::
3. 连接成功提示如下：

    ```
    Welcome to the MySQL monitor. Commands end with ; or \g. Your MySQL connection id is 1031
    Server version: 8.0.30-MatrixOne-v2.0.3 MatrixOne
    Copyright (c) 2000, 2022, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its affiliates. Other names may be trademarks of their respective owners.
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    ```

:::{note}
MatrixOne Intelligence 与客户端默认是非加密传输，如果需要开启加密传输请参见[数据传输加密](../../Security/TLS-introduction.md)。
:::
## 通过 Navicat 连接 MatrixOne Intelligence 服务

1. 下载安装 [Navicat](https://www.navicat.com/en/products)。

2. 安装 Navicat 完成后，打开 Navicat，点击左上角 **Connection > MySQL**，在弹窗中填入如下参数：

    - **连接名**: moc
    - **主机**: freetier-01.cn-hangzhou.cluster.matrixonecloud.cn
    - **端口**: 6001
    - **用户名**: 585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx:admin:accountadmin
    - **密码**: your_password
    - **保存密码**：勾选

3. 点击**保存**保存设置。

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/navicat-1.png width=60% heigth=60%/>
    </div>

4. 双击左侧数据库目录中的 **moc**，图标点亮，连接成功。

5. 连接到 MatrixOne Intelligence 后，在左侧数据库目录栏，你将看到 5 个默认系统数据库：

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/navicat-2.png width=50% heigth=50%/>
    </div>

    右侧窗口可查看有关此连接的基本信息：

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/navicat-3.png width=30% heigth=30%/>
    </div>

## 通过 DBeaver 连接 MatrixOne Intelligence 服务

1. 下载安装 [DBeaver](https://dbeaver.io/download/)。

2. 安装 DBeaver 完成后，打开 DBeaver，点击左上角**连接**图标，在弹窗中选择 **MySQL**，点击**下一步**。

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/dbeaver-6.png width=60% heigth=60%/>
    </div>

    在 **Connect to a database** 窗口的 **Main** 区中填写如下参数：

    - **服务器地址**: freetier-01.cn-hangzhou.cluster.matrixonecloud.cn
    - **端口**: 6001
    - **数据库**: system
    - **用户名**: 585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx:admin:accountadmin
    - **密码**: your_password
    - **保存密码**: 勾选
    :::{note}
    初次连接可以将 Database 选项填写系统库 `system` 方便连接，后续可根据需求自行修改。  
    :::
    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/dbeaver-1.png width=60% heigth=60%/>
    </div>

    并点击**连接详情**修改连接名称为 **moc**。

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/dbeaver-2.png width=60% heigth=60%/>
    </div>

3. 双击左侧目录中的 **moc**，连接 MatrixOne Intelligence 服务。你可以在左侧目录树中看到默认的三个系统数据库：

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/dbeaver-3.png width=60% heigth=60%/>
    </div>

4. 默认情况下，DBeaver 中不展示视图。如需显示完整的系统数据库，你可以右键单击 **moc**，选择**连接视图**并打开**显示系统对象**：

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/dbeaver-4.png width=60% heigth=60%/>
    </div>

    设置完成后，你将看到五个系统数据库。

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/connect/dbeaver-5.png width=60% heigth=60%/>
    </div>
