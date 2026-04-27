# 终止和恢复实例

本篇文档将介绍如何终止和恢复实例，以及相关产品行为。

:::{note}
MO Intelligence 不会永久保存已终止实例的状态，请谨慎操作。如果不慎删除，及时恢复实例以防数据丢失。
:::
## 终止实例

1. 点击菜单栏中的**实例**按钮，进入实例列表。
2. 在**可用实例**页签中选择要终止的实例，在实例卡片上点击**终止**。
3. 在弹窗中确认要终止实例的名称，实例将进入终止中状态。数秒后，实例将完全终止，并显示在**终止实例**页签中。

:::{note}
 1. 实例终止后，将立即终止数据库的所有访问连接。
 2. 我们会为终止状态的实例保留 7 天的数据，7 天后，MO Intelligence 将自动永久删除该实例的数据信息。
:::
## 恢复实例

在**终止实例**页签内的实例可以恢复到**可用实例**，请按照以下步骤操作：

1. 选择要恢复的实例，然后点击**恢复**按钮。
2. 在弹窗中确认，实例将在数秒后完全恢复正常状态。

## 实例状态

在云平台中，不同的情况下实例会有不同的状态，而实例状态图标也会有所变化。以下是对不同实例状态下的描述和可进行的操作的说明：

**实例状态：创建中**

  - 描述：创建实例中
  - 实例操作：无
  - 其他操作：无

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/instance-mgmt/create.png width=50% heigth=50%/>
</div>

**实例状态：可用**

  - 描述：正常运行中，可以提供服务
  - 实例操作：终止
  - 其他操作：连接、监控、实例详情、编辑消费限制

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/instance-mgmt/active.png width=50% heigth=50%/>
</div>

**实例状态：限制**

  - 描述：在以下情况实例会呈现限制状态：
      - 免费实例的 cu 或存储已用完，服务不可用，下月可用，推荐转生产实例。
      - 生产实例消费已达限额且未开启服务保持，服务不可用。
      - 生产实例消费已达限额且开启服务保持，服务保持低速运行。
      - 账户余额不足，生产实例产生欠费情况，服务不可用。
  - 实例操作：终止
  - 其他操作：连接（仅在生产实例消费已达限额且开启服务保持时可操作），监控、实例详情、编辑限制

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/instance-mgmt/limit.png width=50% heigth=50%/>
</div>

**实例状态：无效**

  - 描述：实例状态异常，无法提供完整服务
  - 实例操作：终止
  - 其他操作：监控、实例详情、编辑限制

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/instance-mgmt/inactive.png width=50% heigth=50%/>
</div>

**实例状态：终止中**

  - 描述：实例终止中
  - 实例操作：无
  - 其他操作：监控

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/instance-mgmt/terminating.png width=50% heigth=50%/>
</div>

**实例状态：已终止**

  - 描述：实例终止
  - 实例操作：恢复
  - 其他操作：无

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/instance-mgmt/termination.png width=50% heigth=50%/>
</div>

**实例状态：恢复中**

  - 描述：实例恢复中
  - 实例操作：无
  - 其他操作：无

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/instance-mgmt/recoving.png width=50% heigth=50%/>
</div>

希望这些操作指南能够帮助您更好地管理和恢复 MatrixOne 实例。如有任何疑问或需要进一步的帮助，请继续查看我们的文档或联系支持团队。
