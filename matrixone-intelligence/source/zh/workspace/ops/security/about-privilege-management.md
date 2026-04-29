# 基于角色的访问控制（RBAC）

## 概述

MatrixOne Intelligence 权限管理帮助你管理租户、用户帐号生命周期，分配给用户相应的角色，控制 MatrixOne Intelligence 中资源的访问权限。当数据库中存在多个用户时，权限管理确保用户只访问已被授权的资源，赋予用户最少权限原则可降低企业信息安全风险。
在 MatrixOne Intelligence 中，每个租户在各自实例中所拥有的数据或资源被安全的隔离，跨实例的用户不可访问其他实例的资源。

## MatrixOne Intelligence 权限管理特性

MatrixOne Intelligence 的权限管理是结合了基于角色的访问控制 (RBAC，Role-based access control) 和自主访问控制 (DAC，Discretionary access control) 两种安全模型设计和实现的，这两种安全模型是中立的访问控制机制，主要围绕角色和权限授权策略。它既保证了数据访问的安全性，又给数据库运维人员提供了灵活且便捷的管理方法。

- **基于角色的访问控制（RBAC）**：将权限分配给角色，再将角色分配给用户。

   ![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/security/basic-concepts-1.png)

- **自主访问控制（DAC）**：每个对象都有一个所有者，所有者可以设置和授予对该对象的访问权限。

   ![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/security/dac.png)

## 关键概念

### 对象

在 MatrixOne Intelligence 中，为了方便管理多种操作权限，于是便把权限封装在一个实体内，这个实体就是**对象**。

#### 对象与对象之间的关系

一个 MatrixOne Intelligence 账号下可以创建多个实例，一个实例即是一个租户（Account），一个租户下可以创建多个用户和角色，一个数据库中可以创建多个表和视图。

在 MatrixOne Intelligence 中，尽管每个对象中的操作权限是相互独立的（例如 Database 对象中的 `SHOW TABLES` 权限和 Table 对象中的 `SELECT` 权限并没有直接关系），但对象之间的创建仍具有一定关联，例如 Database 对象中的 `CREAT TABLE` 权限可以创建 Table 对象，这便形成了对象之间的层级关系，

那么，由于高层级对象可以创建低层级对象，那么较高层级的对象就是**对象的创建者 (Owner)**。

#### 对象的创建者（Owner）

当一个对象被创建后，创建者便是这个对象的 Owner，它具有管理这个对象的最高权限（即 **Ownership 权限**，它是对象内所封装的所有权限），那么 Owner 的操作权限集合了该对象的所有操作权限。

例如 Table 对象有 `Select`，`Insert`，`Update`，`Delete`，`Truncate`，`Ownership` 权限，如果一个角色拥有了某个 Table 的 Ownership 权限，那么该角色等同于拥有了 `Select`，`Insert`，`Update`，`Delete`，`Truncate` 权限。

由于权限、角色和用户之间的传递性，你可以把对象的创建者（以下称为对象 Owner）理解为一个角色。

**如何理解对象的创建者是一个角色呢？**

一个用户可以同时拥有多个角色，比如 User A 拥有 Role 1 和 Role 2，还有 Role 3 这三个角色，每个角色拥有的权限不同，如下图所示，帮助你快速理解这一行为：

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/security/example.png)

假如 User A 当前正在使用的角色为 Role 1，User A 需要创建一个新的用户 New user B，可是当前 Role 1 这个角色没有创建新用户的权限，Role 2 拥有创建新用户的权限，那么 User A 需要切换到 Role 2 这个角色，然后再创建新的用户。那么，New user B 的 Owner 是 Role 2，其他角色 Role 1 和 Role 3 并不能拥有 New user B 的所有权。

**对象的 Owner 要点**

- 对象的 Owner 是一个角色，对象最初的 Owner 是创建它的角色。

- 一个对象的 Owner 在任意时刻有且只有一个。

- 一个角色可以创建多个对象，因此一个角色可以是多个对象的 Owner。

- 角色本身也是一个对象，因此角色也有 Owner。

- 当对象的 Owner 被删除时，该对象的 Owner 会自动变更为被删除角色的 Owner。

- Owner 可以转移给另一个角色。

**Note**: *ACCOUNTADMIN* (租户管理员角色，租户被创建后即自动生成) 虽然不是租户内所用对象的 Owner，但它拥有所有对象的 Ownership 权限。

### 租户

MatrixOne Intelligence 可以创建和管理多个数据和用户权限体系完全隔离的租户，并对这些资源隔离的租户进行管理，这种多租户功能既节省了部署和运维多套数据业务系统的成本，又能利用租户间的硬件资源共享最大限度的节约机器成本。

在 MatrixOne Intelligence 中将租户称为 Account，一个实例对应一个租户。

### 角色

角色也是一个对象，它是 MatrixOne Intelligence 中用来管理和分配权限的对象。

在租户中，用户如果没有被赋予角色，那么用户就不能做任何操作。首先，需要先有一个高权限的账号先做一些初期的资源分配，比如说，由**租户**创建一些角色和用户，将对象权限授予给角色，再将角色赋予给用户，这个时候，用户就可以对对象进行操作了。

设立**角色**，是为了节省相同权限授予的操作成本。p1，p2，p3 这三个权限都需要被授予给用户 u1，u2，u3，你只需要先将 p1，p2，p3 授予角色 r1，再将角色 r1 一次性授予用户 u1，u2，u3，相比把每个权限都分别授予每个用户来说，操作上更为简单，并且随着用户和权限数目的增加，这一优势会越发明显。同时，角色的出现进一步抽象了权限集合及其关系，对于后期的权限维护也十分方便。

MatrixOne Intelligence 在集群和租户 (Account) 创建后，会自动创建一些默认角色和用户（详见下面的**初始化访问**章节），这些角色具有最高管理权限，用于在最开始管理集群和租户 (Account)，我们不建议您将这些角色授予日常执行 SQL 的用户，权限过高会引入更多的安全问题，因此，MatrixOne Intelligence 支持创建自定义角色，您可以根据用户的业务需要自定义角色，再将适合的权限赋予这些角色。

**角色要点**

在 MatrixOne Intelligence 中，角色的行为细节如下：

- 一个角色可以被授予多个权限。
- 一个角色可以授予给多个用户。
- 一个角色可以将其权限传递给另一个角色。

  - 将某一角色的全部权限给另一个角色使用，例如将 role1 的所有权限传递给 role2 使用，那么 role2 继承了 role1 的权限。

- 角色和用户仅在各自的租户 (Account) 内生效，包括系统租户 (Sys Account)。

:::{note}
1. 角色的权限继承是动态的，如果被继承角色的权限发生了变化，那么继承角色所继承的权限范围也会动态变化。
2. 角色的继承关系不能成环。例如，role1 继承了 role2，role 2 继承了 role3，role3 继承了 role1。
3. 角色间的权限传递使得权限管理更加便捷，但同时也存在风险，为此，MatrixOne Intelligence 只允许具有 *Manage Grants* 权限的角色才能做这样的操作，该权限被默认赋予给系统默认角色 *MOADMIN* 或 *ACCOUNTADMIN* 中，并且不建议在新建自定义角色时将该权限授予给自定义角色。
:::
#### 角色切换

一个用户被授予多个角色，用于执行不同类型的数据业务。

**主要角色**：用户在某一时刻只能使用其中一个角色，我们称当前所使用的这个角色为**主要角色**。
**次要角色**：除了主要角色之外该用户所拥有的其他角色集合称为**次要角色**。

在默认情况下，如果用户想去执行另一个角色权限的 SQL 时，需要先切换角色（即 `set role <role>`）。此外，为了兼容经典数据库的权限行为，MatrixOne Intelligence 还支持开启*使用次要角色*的功能：使用 `set secondary role all`，执行这条 SQL 后，该用户便可同时拥有他所有角色的权限了，执行 `set secondary role none` 即可关闭此功能。

## 应用场景

### 资源隔离场景介绍

A 公司购买了 MatrixOne Intelligence，并且完成了部署。由于 A 公司规模比较大，业务线多且复杂，数据量也非常庞大，想要针对某个业务线开发一款应用程序，假设命名为 *BusinessApp*，但是需要跟其他业务线的数据进行隔离，那么 MatrxiOne 怎么隔离出这些数据资源、权限资源呢？

完成部署 MatrixOne Intelligence，研发部门的 *Tom* 获取到租户管理员的账号，公司指派他来完成资源隔离这一任务。*Tom* 需要这么做：

1. *Tom* 使用租户管理员的账号登录 MatrixOne Intelligence。
2. *Tom* 需要先创建两个租户，租户账号一个是 *BusinessAccount*，一个是 *ElseAccount*。

    - *BusinessAccount* 内的数据资源主要用于开发应用程序 *BusinessApp*。
    - *ElseAccount* 内的数据资源可以用于其他业务目的。

### 用户创建和授权场景介绍

还是沿用上面的场景示例，*Tom* 把 *BusinessAccount* 这个租户账号给了公司的数据管理员 *Robert*，让 *Robert* 去分配新的用户账号和权限给其他研发同事。

研发同事 *Joe* 是这个 A 公司项目 *BusinessApp* 的应用开发者，*Joe* 有一个开发任务，*Joe* 需要使用数据库内所有的数据。那么 *Robert* 就要帮 *Joe* 开通账号，给 *Joe* 授权：

1. *Robert* 先给 *Joe* 创建了一个用户账号（即，用户），名字叫做 *Joe_G*，*Joe* 就使用 *Joe_G* 这个账号登录到 MatrixOne。
2. *Robert* 又给 *Joe* 创建了一个角色，名字叫做 *Appdeveloper*，并且把 *Appdeveloper* 角色赋予给 *Joe* 的用户账号 *Joe_G* 上。
3. *Robert* 又给角色 *Appdeveloper* 授予了 *ALL ON DATABASE* 的权限。
4. *Joe* 就可以使用 *Joe_G* 这个账号登录到 MatrixOne，并且全权操作数据库进行开发了。

## 初始化访问

初始化账户后，系统会自动生成一些默认用户和默认角色：

| **用户名** | **解释** | **所拥有的角色** | **所拥有的权限** | **描述** |
| --- | --- | --- | --- | --- |
| <自定义> | 租户管理员 | ACCOUNTADMIN | 管理普通租户下的所有资源，包含用户、角色、数据库/表/视图，授权管理 | 租户被创建后自动生成并授予 |
| 所有用户 | 普通用户 | PUBLIC | 连接 MatrixOne Intelligence | 所有用户被创建后，自动被授予 PUBLIC 角色 |
