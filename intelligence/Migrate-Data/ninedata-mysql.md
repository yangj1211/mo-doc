# 使用 NineData 将 MySQL 数据写入 MatrixOne Intelligence

本章节将以从阿里云 MySQL RDS 向 MatrixOne Intelligence 转移数据为例来介绍如何使用 Ninedata 将 MySQL 数据写入到 MatrixOne Intelligence。

## 开始前准备

- 完成 [MatrixOne Intelligence 实例创建](../Get-Started/quickstart.md)。
  
- 完成 [NineData 在线平台的注册](https://console.ninedata.cloud/user/register)。

## 操作步骤

### 创建测试数据

本章节使用的是 TPC-H 标准测试数据，具体测试数据生成及注入请参考[完成 TPCH 测试](https://docs.matrixorigin.cn/v25.2.1.0/MatrixOne/Test/performance-testing/TPCH-test-with-matrixone/)

1. 创建名为 `tpch` 的 MySQL 数据库，并在其中按照 TPCH benchmark 要求生成 lineitem, partsupp, part, supplier, nation, region, orders, customers 这八张表。

    ```sql
    mysql> \. 路径/dss.ddl
    ```

2. 添加主键以及外键

    ```shell
    mysql> \. 路径/dss.ri
    ```

3. 使用 `dbgen` 生成 100MB 数据

    ```sql
    ./dbgen -s 0.1
    ```

4. 将生成的八个 tbl 表的数据全部导入到测试的 MySQL 测试数据库中

  ```sql
  USE tpch;
  SET FOREIGN_KEY_CHECKS=0;
  LOAD DATA LOCAL INFILE '/root/TPC-H V3.0.1/dbgen/customer.tbl' INTO TABLE CUSTOMER
  FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';
  LOAD DATA LOCAL INFILE '/root/TPC-H V3.0.1/dbgen/lineitem.tbl' INTO TABLE LINEITEM
  FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';
  LOAD DATA LOCAL INFILE '/root/TPC-H V3.0.1/dbgen/nation.tbl' INTO TABLE NATION
  FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';
  LOAD DATA LOCAL INFILE '/root/TPC-H V3.0.1/dbgen/orders.tbl' INTO TABLE ORDERS
  FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';
  LOAD DATA LOCAL INFILE '/root/TPC-H V3.0.1/dbgen/partsupp.tbl' INTO TABLE PARTSUPP
  FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';
  LOAD DATA LOCAL INFILE '/root/TPC-H V3.0.1/dbgen/part.tbl' INTO TABLE PART
  FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';
  LOAD DATA LOCAL INFILE '/root/TPC-H V3.0.1/dbgen/region.tbl' INTO TABLE REGION
  FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';
  LOAD DATA LOCAL INFILE '/root/TPC-H V3.0.1/dbgen/supplier.tbl' INTO TABLE SUPPLIER
  FIELDS TERMINATED BY '|' LINES TERMINATED BY '|\n';
  SET FOREIGN_KEY_CHECKS=1;
  ```

### 设置 NineData 数据源

1. 在 [NineData 工作台](https://console.ninedata.cloud/home/main)界面选择数据源

2. 点击创建数据源，并选择在 `自建数据库` 的 `关系型数据库` 一栏中选择 MySQL

3. 依次设置好阿里云 MySQL RDS 的数据源信息和 MatrixOne Intelligence 的数据源信息，设置如图所示：

   ![dataSourceSetup](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/ninedata/dataSourceSetup.png)

4. 新建数据迁移任务

      点击左侧边栏 `数据复制` 大类，选择 `数据复制` 进入数据复制页面，点击 `创建复制`。

      填入任务名称、源数据源（本例中采用阿里云 RDS 数据源），目标数据源（本例中采用 MOC 数据源），选择复制方式、复制类型、复制规格以及目标库存在同名对象的处理方式，点击下一步。

      设置如图：
      ![sourceTarget](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/ninedata/sourceTarget.png)

5. 设置需要复制的对象

      在源对象中选择需要数据迁移的表，点击中间的转移箭头，点击下一步，如图所示

      ![replican](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/ninedata/replican.png)

6. 检查配置映射

      确定映射的源数据库和目标数据库各自的表名一一对应，点击保存并预检查

      ![configuration](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/ninedata/configuration.png)

7. 预检查成功后点击启动任务即可

      ![sourceTarget](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/ninedata/sourceTarget.png)

8. 100MB 的数据大概会耗时 4 分钟进行迁移，在迁移完成后可以选择数据对比选项来比较迁移前后是否数据一致。