<p align="center">
  <img src="assets/work1z-avatar-easywork.png" width="160" height="160" alt="Work1z：轻松完成工作">
</p>

<h1 align="center">Work1z</h1>

<p align="center"><strong>Easy work，轻松把事情做完。</strong></p>

<p align="center">把项目需求写成可确认的 PRD，把实现思路整理成可审查的技术方案。</p>

<p align="center">
  <a href="plugin.json"><img src="https://img.shields.io/badge/Version-0.1.2-blue?style=plastic" alt="Version 0.1.2"></a>
  <a href="skills/"><img src="https://img.shields.io/badge/Skills-2-8A2BE2?style=plastic" alt="2 bundled skills"></a>
  <a href=".agents/plugins/marketplace.json"><img src="https://img.shields.io/badge/Codex-Plugin-111111?style=plastic" alt="Codex plugin"></a>
  <a href=".claude-plugin/plugin.json"><img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=plastic" alt="Claude Code plugin"></a>
  <a href=".qoder-plugin/plugin.json"><img src="https://img.shields.io/badge/Qoder-Plugin-7C3AED?style=plastic" alt="Qoder plugin"></a>
  <a href="skills/work1z/references/文档校验脚本.md"><img src="https://img.shields.io/badge/Validator-Python_3.9%2B-3776AB?style=plastic" alt="Document validator: Python 3.9+"></a>
</p>

<p align="center">
  <strong>简体中文</strong> · <a href="README.en.md">English</a>
</p>

<p align="center">
  <a href="#使用说明">使用说明</a> · <a href="#安装">安装</a> · <a href="#项目文件">项目文件</a>
</p>

![六个字，够开工吗？从一句「支持取消订单」到 PRD 与技术方案](assets/work1z-skill-intro-minimal.png)

Work1z 适合新项目梳理需求，也适合已有项目的功能迭代。PRD 说明本期做什么、怎样验收；技术方案说明怎么实现、为什么这样做，并按版本保留设计与验收依据。

插件标识：`work1z`。仓库名称：`work1z-plugin`。内置 `work1z` 和 `humanizer-zh` 两个 Skill。

## 使用说明

提供 Codex、Claude Code、Qoder 的插件配置和安装说明；其他能读取本地 `SKILL.md` 的 Agent 可按目录加载。两个 Skill 随插件一起提供，无需单独安装 `humanizer-zh`。

<details>
<summary>从一句需求开始</summary>

安装插件后，选择 Work1z，再说明要写哪份文档。也可以直接提供本项目的 `skills/work1z/SKILL.md` 路径。例如：

> 使用 Work1z，为预约系统编写 PRD。先阅读当前项目，再帮我明确本期范围和验收标准。

> 根据现有 PRD 编写订单模块的技术方案，本次只涉及后端。请核对已有接口和数据结构，列出还没确定的业务规则。

> 修订现有 PRD：新增取消预约功能。请检查对权限、状态和验收标准的影响，并同步判断是否需要更新技术方案。

以上是使用示例，不是已交付项目。开始时可以提供项目目录、已有文档、需求材料和本期范围；信息不足时，Agent 会先问影响范围、业务口径和关键设计的问题，每轮最多三个。

</details>

<details>
<summary>什么时候使用</summary>

`work1z` skill 仅在需要编写或修订以下内容时触发：

- 项目需求文档（PRD）或产品需求方案。
- 前端、后端或两端的技术方案。

单独写代码、修复缺陷、运行测试、补验收记录或一般技术问答，不触发本 skill。方案确定后，可以继续安排实现、测试和人工验收，这些工作需要相应授权。

插件还包含 `humanizer-zh` skill，可独立用于中文文本润色，也用于方案交付前的表达检查。

</details>

<details>
<summary>能交付什么</summary>

| 内容 | 交付重点 |
| --- | --- |
| PRD | 本期范围、角色权限、业务规则、异常情况和可观察的验收结果 |
| 技术方案 | 本次涉及的模块、接口与数据设计、关键取舍，以及沿用的既有设计 |
| 图表 | 按问题选图，保持图、正文、数据设计和验收口径一致 |
| 版本归档 | PRD 修改记录、同号技术方案目录，以及能追溯既有设计的项目文档清单 |
| 审查与验收记录 | 实际检查内容、测试结果、人工反馈、遗留问题和证据 |

涉及 Java 后端设计与后续实现时，使用项目内的《Java 开发手册（黄山版）》及工程分层规范。

</details>

<details>
<summary>怎样推进</summary>

1. **读现状。** 查看项目文档清单、当前 PRD 和受影响模块的设计，按需核对实现。早期版本中仍适用的设计也要回看。
2. **澄清需求。** 区分已有事实、设计建议和待定问题，不替业务补规则。
3. **交付草稿。** PRD 每轮修改都展示完整草稿，确认后再写入正式文件。技术方案按对应 PRD 编写，迭代时聚焦本次变化。
4. **润色与审查。** 每轮文档交付前调用内置的 `humanizer-zh`，处理空话、重复和模板化表达。技术方案确认后，还要对照需求与规范审查，记录发现及未验证项。
5. **归档并衔接交付。** 维护版本和文件链接；后续实现按模块验证，自动化测试结果和人工验收结论分别记录。

润色保留业务规则、技术约束、事实、确定程度和验证状态。接口能否复用、事务能否回滚等判断，需要说明依据；代码审查结论与实际测试结果分别表述。

</details>

<details>
<summary>版本怎样保存</summary>

PRD 初版为 `v1.0`，每批正式修订递增一个小版本；草稿修改不升版。技术方案沿用 PRD 的版本号，不单独编号。

下面是项目中的文档布局示意，PRD 文件名可按项目实际情况使用：

```text
项目文档目录/
├── PRD.md
├── 项目文档清单.md
├── v1.0/
│   └── 技术方案.md
├── v1.1/
│   └── 技术方案.md
└── facts/
```

只有需要归档技术设计时才创建对应版本目录。确认没有技术变更的版本，在文档清单中注明，不生成空方案。`facts/` 在首次产生记录时创建，按文档版本和模块保存审查、测试及人工验收结果。

</details>

## 安装

先将完整仓库下载或克隆到本地，并让 Agent 打开该目录。下面的命令均从仓库根目录执行；安装提示词可直接复制到目标 Agent。

| 环境 | 安装方式 |
| --- | --- |
| Codex | `plugin.json` + `.agents/plugins/marketplace.json` |
| Claude Code | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` |
| Qoder CLI / IDE | `.qoder-plugin/plugin.json`；从本地目录安装或导入 |
| 其他本地 Agent | 读取完整仓库中的 `skills/work1z/SKILL.md`；自动发现方式取决于宿主 |

<details>
<summary>复制给 Agent：自动识别环境并安装</summary>

```text
请将当前打开的 work1z-plugin 仓库配置到你所在的 Agent 环境中使用。

先读取 README.md 和插件清单，确认仓库绝对路径以及你当前实际运行的宿主。
不要仅凭机器上装了哪些 CLI 来判断宿主；无法确定时先问我。

如果你是 Codex：
1. 检查 codex plugin --help，并检查已有 marketplace 和插件记录。
2. 从仓库根目录运行 codex plugin marketplace add .
3. 运行 codex plugin add work1z@work1z-marketplace。
4. 使用 codex plugin list --json 核对安装和启用状态。

如果你是 Claude Code：
1. 检查 claude plugin --help，并检查已有 marketplace 和插件记录。
2. 从仓库根目录运行 claude plugin validate .，通过后运行 claude plugin marketplace add .
3. 运行 claude plugin install work1z@work1z-marketplace --scope user。
4. 使用 claude plugin list --json 核对安装和启用状态。

如果你是 Qoder：
1. CLI 环境先检查 qoder plugins --help 和 qoder plugins list --json。
2. 从仓库根目录运行 qoder plugins validate .，确认识别到 work1z 和 humanizer-zh 两个 Skill。
3. 校验通过后运行 qoder plugins install . --scope user。
4. 使用 qoder plugins list --json 核对 work1z@local 的安装和启用状态。
5. 提示我在当前交互会话执行 /plugins reload，或新建会话，再通过 /skills 核对两个 Skill。
如果是在 Qoder IDE 中且没有 CLI，使用 Settings → Plugins 的 Import 入口导入完整仓库；
无法操作界面时给出入口和仓库绝对路径，等待我完成导入，不要声称已经安装。

如果你是其他支持本地 Skill 的 Agent：
先查阅该宿主的官方加载说明。保留完整仓库，根据其支持的方式登记或引用
skills/work1z/SKILL.md 和 skills/humanizer-zh/SKILL.md。
不要只复制单个 SKILL.md，也不要拆散两个 Skill 和根目录 assets 的相对位置。
如果只能在对话中按路径读取，就给出可复制的绝对路径调用提示词，说明这不是持久安装。

已有同名来源或插件时，先核对它是否来自当前仓库；一致则复用，不一致则报告差异，
不要覆盖。需要 CLI 但缺失或不支持上述命令时，说明缺少什么，不自动安装或升级宿主。

完成后核对安装副本或已登记目录中两个 Skill 均存在，work1z 对 humanizer-zh、
模板、校验脚本及图片的相对引用有效。不要另外安装 humanizer-zh。
最后报告实际安装位置、启用状态、验证结果，以及是否需要新建会话。
区分“配置检查通过”和“新会话已实际加载”，未验证的不要写成已验证。
```

</details>

<details>
<summary>Codex：手动安装与核对</summary>

使用 [Agent Plugins 插件结构](https://developers.openai.com/plugins/build/plugins)。根目录的 `plugin.json` 声明插件，`.agents/plugins/marketplace.json` 提供本地安装入口。

在仓库根目录运行：

```bash
codex plugin marketplace add .
codex plugin add work1z@work1z-marketplace
codex plugin list --json
```

安装后新建对话，选择 Work1z 或要求使用它编写方案。支持本地 marketplace 的桌面客户端也可在插件目录中选择 Work1z 来源并安装。CLI 没有 `plugin` 子命令时，需要先使用支持插件管理的版本。

</details>

<details>
<summary>Claude Code：手动安装、调用与临时试用</summary>

使用 [Claude Code 插件清单](https://code.claude.com/docs/en/plugins-reference)和 [marketplace](https://code.claude.com/docs/en/plugin-marketplaces)。各平台共享同一份 `skills/`，不需要另外复制 Skill。

在仓库根目录运行，默认安装到当前用户：

```bash
claude plugin validate .
claude plugin marketplace add .
claude plugin install work1z@work1z-marketplace --scope user
claude plugin list --json
```

安装后新建 Claude Code 会话，用 `/work1z:work1z` 编写方案，或用 `/work1z:humanizer-zh` 润色已有中文文本。PRD 和技术方案交付前也会按工作流读取内置润色规则。

仅试用、不登记 marketplace 时，从仓库根目录运行：

```bash
claude --plugin-dir .
```

这只为本次启动加载插件，不等于持久安装。命令与作用域见 [Claude Code 命令参考](https://code.claude.com/docs/en/plugins/cli-reference)。

</details>

<details>
<summary>Qoder：CLI 安装与 IDE 导入</summary>

使用 [Qoder 插件清单](https://docs.qoder.com/cli/plugins-reference)，元信息位于 `.qoder-plugin/plugin.json`。Qoder 从根目录 `skills/` 发现两个 Skill，模板、脚本和内置润色规则随插件一起安装。

Qoder CLI 支持从本地目录直接安装，无需登记 marketplace。在仓库根目录运行：

```bash
qoder plugins validate .
qoder plugins install . --scope user
qoder plugins list --json
```

校验输出应列出 `work1z` 和 `humanizer-zh` 两个 Skill；安装列表中核对 `work1z@local` 及启用状态。安装后新建 CLI 会话，或在当前交互会话执行 `/plugins reload`，再用 `/skills` 检查技能是否已加载。命令与作用域见 [Qoder CLI 插件指南](https://docs.qoder.com/cli/plugins)。

Qoder IDE 可在 Settings → Plugins 的 Custom 区域点击 Import，选择本仓库根目录；也可从插件市场的 Create Plugin 入口选择导入本地文件夹。导入时选择用户级或项目级作用域，完成后在新对话输入 `/` 检查可用能力。入口见 [Qoder IDE 插件说明](https://docs.qoder.com/extensions/plugins)。

导入的是包含 `.qoder-plugin/`、`skills/` 和 `assets/` 的完整目录，不是单个 `SKILL.md`。当前仓库已提供配置，Qoder CLI 校验、实际安装及新会话加载仍需在装有 Qoder 的环境中验证。

</details>

<details>
<summary>其他 Agent：按完整目录加载</summary>

宿主需要能读取本地 Markdown 文件；执行文档校验还需要命令执行能力及 Python 3.9 以上版本。不同宿主的 Skill 自动发现位置并不通用，不能直接照搬 Codex 或 Claude Code 的安装命令。

保留完整仓库，将下面的“仓库绝对路径”替换为实际位置后，复制给 Agent：

```text
请读取 /仓库绝对路径/skills/work1z/SKILL.md，并按照其中的规则执行接下来的方案任务。
模板和脚本相对于该 Skill 目录解析；中文润色规则在同级的
../humanizer-zh/SKILL.md，介绍图资源位于仓库根目录 assets/。
不要另外安装 humanizer-zh。现在先告诉我你已读到的两个 Skill 名称，等待我的具体需求。
```

这是按路径加载方式。若要让后续会话自动发现，应按该宿主的官方说明登记这两个入口，并保留目录关系。

</details>

<details>
<summary>依赖、路径与文档校验</summary>

插件无 MCP 服务或账号认证。marketplace 使用相对路径，克隆仓库后无需修改配置中的路径；已经登记的本地来源在目录移动后需要重新添加。

插件已内置 [humanizer-zh](skills/humanizer-zh/SKILL.md)，无需单独安装。Work1z 通过插件内的相对路径读取润色规则，不依赖全局同名 skill。打包版本保留源文件中的修订标记 `2026-09-23`、来源说明及 [MIT 许可证](skills/humanizer-zh/LICENSE)。该许可证适用于内置的 humanizer-zh，当前仓库尚未声明整个项目的许可证。

文档校验脚本使用 Python 3.9 及以上版本，无第三方依赖。草稿交付前检查结构、版本及链接，归档后核对清单和目录；参数和使用方法见[文档校验脚本说明](skills/work1z/references/文档校验脚本.md)。从仓库根目录查看参数：

```bash
python3 skills/work1z/scripts/validate_docs.py --help
```

</details>


## 自动更新与发布

正式版本发布在 [GitHub Releases](https://github.com/idealzxz/work1z-plugin/releases)。安装时优先下载附件 `work1z-plugin-vX.Y.Z.zip` 并完整解压，再按上面的宿主步骤安装；发布包包含文件校验清单。GitHub 自动提供的 Source code 压缩包不包含该清单。

两个 Skill 在每次新任务开始时调用公共更新脚本，同一次任务只检查一次。有更高的正式版本时，校验下载包和本地文件后更新当前插件副本，再重新读取新版规则。没有 Release 或网络不可用时继续使用当前版本，并说明实际检查结果。

- 更新需要 Python 3.9+、命令执行权限、网络和插件目录写权限，无第三方 Python 依赖。
- 只跟随正式 Release，不跟随 main，不安装预发布版本或降级。
- 本地发布文件有修改、缺失或路径冲突时不覆盖；不在发布清单中的文件会保留。
- Git 开发检出目录只检查版本。宿主从 Git 复制的缓存若没有清单，会从当前版本的正式发布包取得基线；无法取得基线时跳过更新。
- 更新只作用于当前加载的插件目录。宿主的注册记录及其他安装副本不会被改写；必要时执行宿主重载或新建会话，管理界面的版本显示可能要刷新后才同步。
- 首次使用本机制需要安装 `0.1.1` 或后续正式发布包。旧版本没有检查入口，无法自行启动更新。

从插件根目录手动检查或更新：

```bash
python3 scripts/release.py update --check-only
python3 scripts/release.py update
```

具体结果处理及异常恢复见[自动更新规则](skills/work1z/references/自动更新.md)。

<details>
<summary>维护者：自动打包与发布</summary>

[Release 工作流](https://github.com/idealzxz/work1z-plugin/blob/main/.github/workflows/release.yml) 在推送 `vX.Y.Z` 标签时运行：

1. 运行打包和更新测试。
2. 校验根目录、Claude Code 和 Qoder 三个 `plugin.json` 的版本与标签一致。
3. 打包两个 Skill、模板、脚本、图片、插件配置及中英文 README，生成逐文件清单与 ZIP 的 SHA-256；排除 `.DS_Store`、Python 缓存、Git 元数据及开发测试。
4. 创建草稿 Release，上传 ZIP 和校验文件后再公开。失败的草稿可重跑补齐；已经公开的版本不覆盖，修订需发新版本。

版本号使用 `主版本.次版本.修订号`，例如 `0.1.2`；Git 标签为 `v0.1.2`。发布前同步三个清单和 README 版本徽章，将待发布改动提交到标签对应的提交后，再创建并推送标签。工作流只在远程收到标签后执行，需要仓库启用 GitHub Actions，并允许工作流通过 `GITHUB_TOKEN` 写入 Releases。

本地验证与打包（输出目录放在仓库之外）：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/release.py pack --tag v0.1.2 --output /tmp/work1z-dist
```

输出为 `work1z-plugin-v0.1.2.zip` 和 `work1z-plugin-v0.1.2.zip.sha256`。打包本身不会创建标签或发布 Release。更换版本后，将示例标签替换为对应版本。

</details>

## 项目文件

<details>
<summary>插件结构</summary>

```text
work1z-plugin/
├── README.md
├── README.en.md
├── plugin.json
├── scripts/release.py
├── .github/workflows/release.yml
├── tests/test_release.py
├── .agents/plugins/marketplace.json
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .qoder-plugin/plugin.json
├── assets/
└── skills/
    ├── work1z/
    │   ├── SKILL.md
    │   ├── references/
    │   └── scripts/
    └── humanizer-zh/
        ├── SKILL.md
        └── LICENSE
```

</details>

<details>
<summary>文件导航</summary>

| 文件 | 用途 |
| --- | --- |
| [plugin.json](plugin.json) | 插件标识、版本及展示信息 |
| [Codex marketplace](.agents/plugins/marketplace.json) | Codex 本地插件安装入口 |
| [Claude Code 插件清单](.claude-plugin/plugin.json) | Claude Code 插件标识、版本及展示信息 |
| [Claude Code marketplace](.claude-plugin/marketplace.json) | Claude Code 本地插件安装入口 |
| [Qoder 插件清单](.qoder-plugin/plugin.json) | Qoder 本地插件安装与导入元信息 |
| [SKILL.md](skills/work1z/SKILL.md) | 触发范围、执行规则及交付检查 |
| [humanizer-zh](skills/humanizer-zh/SKILL.md) | 中文润色规则，随插件一起安装 |
| [PRD 模板](skills/work1z/references/PRD模板.md) | 需求文档结构与修订格式 |
| [技术方案模板](skills/work1z/references/技术方案模板.md) | 技术设计的组织方式 |
| [项目文档清单模板](skills/work1z/references/项目文档清单模板.md) | 版本、模块和设计文件索引 |
| [需求分析图表规范](skills/work1z/references/需求分析图表规范.md) | 图种选择与表达规范 |
| [Java 开发手册（黄山版）](skills/work1z/references/Java开发手册-黄山版.md) | Java 编码与检查依据 |
| [Java 工程目录与分层](skills/work1z/references/Java工程目录与分层.md) | 包结构、职责和依赖方向 |
| [文档写作正反例](skills/work1z/references/文档写作正反例.md) | 正文表达、技术判断与修订记录示例 |

</details>

