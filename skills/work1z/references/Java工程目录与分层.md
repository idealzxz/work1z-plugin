# Java 工程目录与分层

## 工程目录

先从根目录定位工程职责，再按项目选定的分包方式展开相关路径。用户明确选择按技术层或按业务分包时遵循该选择；已有项目优先保持现有结构，新项目未指定时结合规模和维护方式给出选择及理由，不将下面的示例当作固定架构。单模块工程沿实际源码路径展示相同职责，不因示例使用多模块就拆分工程。

初版列主要路径，迭代注明变更的位置及用途。正文承诺的 Controller、Service、DAO、模型和转换层都应在目录树中找到位置；`model/entity/`、`model/dto/`、`model/vo/` 分别展开。示例只展示部分业务时明确标注，并说明其余类归属。未建工程标为拟建目录，不把设计路径当作已生成文件。

```text
shop/
├── shop-application/       启动入口 Application.java 和应用配置
├── shop-api/               对外接口及随契约发布的 DTO
├── shop-core/              订单等业务模块，包内结构见下例
├── shop-infrastructure/    缓存、远程客户端等共用技术组件
└── shop-test/              已有独立跨模块测试时列出
```

各模块的单元测试放在本模块的 `src/test/java`。配置、Mapper XML 和迁移脚本按实际归属列出，例如启动模块的 `src/main/resources/application.yml`、持久层所在模块的 `src/main/resources/mapper/`。涉及数据库迁移时标明项目实际使用的迁移路径。

## 分包与共用组件

按业务分包时，技术层位于所属业务包下。以下展开订单业务，其他业务采用相同职责划分：

```text
shop-core/src/main/java/com/example/order/
├── controller/    接收请求、校验格式、映射响应
├── service/       业务用例与流程编排；接口和实现分开时列 impl/
├── manager/       复用的缓存策略、适配逻辑或多个 DAO 的组合
├── dao/           订单数据读写
├── model/
│   ├── entity/    订单持久化对象
│   ├── dto/       订单传输对象
│   └── vo/        订单展示对象
├── converter/     持久化、业务与接口模型间的转换
├── constant/      订单模块常量
└── exception/     订单业务异常
shop-core/src/test/java/com/example/order/service/
                   订单业务规则的单元测试
```

按技术层分包时，各层直接位于应用基础包下，通过类名区分业务。以下只列订单与用户的部分示例类：

```text
shop/src/main/java/com/example/shop/
├── controller/
│   ├── OrderController.java
│   └── UserController.java
├── service/
│   ├── OrderService.java
│   └── UserService.java
├── dao/
│   ├── OrderDao.java
│   └── UserDao.java
├── model/
│   ├── entity/    OrderEntity、UserEntity 等持久化对象
│   ├── dto/       业务传输对象
│   └── vo/        接口展示对象
└── converter/     OrderConverter、UserConverter 等模型转换
shop/src/test/java/com/example/shop/service/
                   OrderServiceTest、UserServiceTest 等测试
```

目录和正文使用同一分包方式，调整选择时同步修改示例路径和测试位置。以上目录按实际职责采用，不为纯适配或执行组件创建没有用途的空层。

查询条件对象（Query）和业务对象（BO）按已有约定归入相应模型包。对外发布的 DTO 由 API 契约所在模块维护。新增包名使用单数，每段为单个小写英文单词。包名和单元测试位置属于手册强制项，职责分层属于推荐项。[《Java 开发手册（黄山版）》](./Java开发手册-黄山版.md)

共用组件按实际职责标位置：配置在 `config/`，通用工具在 `util/`，统一响应和分页类型可归入契约侧的 `common/`。入口侧的全局异常处理负责将业务异常映射为响应。基础设施侧的 `cache/` 封装缓存访问，`rpc/` 适配远程协议与错误；订单缓存键、失效时机等业务策略由订单模块维护。

## 沿业务动作检查分层

| 涉及的变更 | 核对问题 |
| --- | --- |
| 请求入口与业务规则 | 以取消订单为例，入口校验订单号格式，Service 或领域对象判断当前状态能否取消。若后台任务也可取消订单，两处是否调用同一规则？ |
| 数据与接口模型 | 对照请求、持久化对象和响应，关键字段从哪里取得、在哪转换、对谁可见？例如新增内部成本字段后，客户响应仍应符合原契约。 |
| 新增 Manager | 哪些调用方复用同一策略，或哪些外部协议细节需要集中适配？单次读写可由 Service 调用 DAO。 |
| 多次写入与外部调用 | 标明必须一起提交的写入。若订单已提交而通知失败，订单处于什么状态、调用方收到什么结果、通知由谁按什么条件重试？本地事务的回滚范围应与实际参与的资源一致。 |

目录与分层示例参考[《从规范到架构》第 6 节](https://juejin.cn/post/7534114816282542118#heading-62)，具体路径以项目为准。
