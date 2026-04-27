# 登录实例的数据库管理平台

在 MatrixOne Intelligence 实例管理平台的实例列表中，找到您想连接的实例，依次点击**连接** > **通过云平台连接**进入实例登录页面，然后输入用户名和密码即可成功登录至实例的数据库管理平台。您可以使用 admin 用户或者普通用户登录，有关 admin 用户和普通用户更多的描述请查看 [MatrixOne Intelligence 中的权限管理](../Reference/access-control-type.md)。

## admin 用户

实例的数据库管理平台默认登录用户为 admin，admin 用户密码在创建实例时指定。

## 普通用户

除了可以使用 admin 用户登录到实例的数据库管理平台，还支持普通用户访问，只要授予相应权限即可。

**步骤：**

- 新建用户

通过 admin 用户登录后，创建一个新的用户

```sql
create user u2 identified by '123456';
```

- 新建角色

在租户中，没有被赋予角色的情况下用户是不能做任何操作的，详情可查看[基于角色的访问控制](../Security/about-privilege-management.md)。所以我们需要创建一个新的角色。

```sql
create role if not exists role2;
```

- 授权

将对象权限授予给角色，再将角色赋予给用户，这个时候，用户就可以对对象进行操作了。如果未授权，那么普通用户登录后只能查看查询历史的信息，如需其它操作，则应授予相应权限，详情可查看 [MatrixOne Intelligence 中的权限管理](../Reference/access-control-type.md)。执行以下操作可为角色赋最高权限。

```sql
grant all on account * to role2;
grant all on database * to role2;
grant all on table *.* to role2;
grant role2 to u2;
```

- 登录

若想以普通用户登录到实例的数据库管理平台，用户名处格式应为“用户名：角色名”，例如 "u2:role2", 如果不填写角色名则默认角色为 public。
