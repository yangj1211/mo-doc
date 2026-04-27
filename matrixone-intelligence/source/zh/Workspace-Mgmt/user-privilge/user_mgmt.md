
# 用户管理

GenAI 工作区作为多模态数据的集成、处理与应用平台，采用 RBAC（基于角色的访问控制）模型，实现灵活且安全的权限管理。系统通过用户与角色的绑定，以及角色与权限的映射关系，控制用户在平台中的访问范围和操作权限，一个用户可以被授予多个角色，方便权限灵活管理。目前系统除了“管理员”角色，还内置了默认角色“数据开发”，该角色具备除用户权限管理以外的全部操作权限。

如需进行更精细粒度的权限控制，可参考[角色权限](./role_mgmt.md)来创建更多角色，以满足不同类型用户的权限需求。

## 默认用户

- 创建工作区时指定的用户自动成为超级管理员角色
- 超级管理员用户不能被修改角色、禁用和删除

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/workspace/user_mgt_1.png
 width=100% heigth=100%/>
</div>

## 新建用户

创建规则：​

| 字段    | 说明                        |
|---------|-----------------------------------|
| 用户名   | 工作区内唯一     |
| 密码     | 最小长度 8 位，需包含大小写和特殊字符|
| 角色     | 目前只支持**数据开发**这一角色      |
| 备注     | 可选字段，最大 256 字符             |

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/workspace/user_mgt_2.png
 width=90% heigth=90%/>
</div>

## 用户操作

仅超级管理员具有用户管理权限，包括修改密码、调整角色、更新信息、禁用账户及删除账户。被禁用的用户状态变为**禁用**，并将无法登录平台，若该用户已登录，其会被立即强制下线，且无法执行新的操作。已发起且正在执行的操作不受影响。
  
<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/workspace/user_mgt_3.png
 width=100% heigth=100%/>
</div>
