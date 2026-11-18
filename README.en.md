<p align="center">
  <img src="assets/work1z-avatar-easywork.png" width="160" height="160" alt="Work1z: make work easy">
</p>

<h1 align="center">Work1z</h1>

<p align="center"><strong>Easy work. Get things done with less effort.</strong></p>

<p align="center">Turn project requirements into PRDs ready for approval and implementation ideas into technical plans ready for review.</p>

<p align="center">
  <a href="plugin.json"><img src="https://img.shields.io/badge/Version-0.1.2-blue?style=plastic" alt="Version 0.1.2"></a>
  <a href="skills/"><img src="https://img.shields.io/badge/Skills-2-8A2BE2?style=plastic" alt="2 bundled skills"></a>
  <a href=".agents/plugins/marketplace.json"><img src="https://img.shields.io/badge/Codex-Plugin-111111?style=plastic" alt="Codex plugin"></a>
  <a href=".claude-plugin/plugin.json"><img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=plastic" alt="Claude Code plugin"></a>
  <a href=".qoder-plugin/plugin.json"><img src="https://img.shields.io/badge/Qoder-Plugin-7C3AED?style=plastic" alt="Qoder plugin"></a>
  <a href="skills/work1z/references/文档校验脚本.md"><img src="https://img.shields.io/badge/Validator-Python_3.9%2B-3776AB?style=plastic" alt="Document validator: Python 3.9+"></a>
</p>

<p align="center">
  <a href="README.md">简体中文</a> · <strong>English</strong>
</p>

<p align="center">
  <a href="#usage">Usage</a> · <a href="#installation">Installation</a> · <a href="#project-files">Project files</a>
</p>

![From a short request to a PRD and technical plan (Chinese illustration)](assets/work1z-skill-intro-minimal.png)

Work1z helps define requirements for new projects and plan feature iterations in existing ones. The PRD explains what to deliver and how to accept it; the technical plan explains how to implement it and why, with versioned design and acceptance records.

Plugin ID: `work1z`. Repository: `work1z-plugin`. Includes two skills: `work1z` and `humanizer-zh`.

This README is available in English; the bundled skill instructions, templates, reference documents, and cover illustration are in Chinese.

## Usage

Plugin configurations and installation instructions are provided for Codex, Claude Code, and Qoder. Other agents that can read local `SKILL.md` files can load the repository by path. Both skills ship together; there is no need to install `humanizer-zh` separately.

<details>
<summary>Start with a requirement</summary>

After installing the plugin, select Work1z and describe the document you need. You can also provide the path to `skills/work1z/SKILL.md`. For example:

> Use Work1z to write a PRD for a booking system. Read the current project first, then help define the scope and acceptance criteria for this release.

> Write a technical plan for the order module based on the existing PRD. This iteration covers only the backend. Check existing APIs and data structures, and list unresolved business rules.

> Revise the existing PRD to support booking cancellation. Check the impact on permissions, states, and acceptance criteria, and determine whether the technical plan needs updating.

These are usage examples, not completed projects. You can provide a project directory, existing documents, requirement materials, and release scope. When information is missing, the agent asks about scope, business rules, and key design decisions, with at most three questions per round.

</details>

<details>
<summary>When to use it</summary>

The `work1z` skill activates only for writing or revising:

- Product requirements documents (PRDs) or product requirement proposals.
- Frontend, backend, or combined technical plans.

Standalone coding, bug fixes, test execution, acceptance record updates, and general technical questions do not activate this skill. Implementation, testing, and manual acceptance can follow an agreed plan with the appropriate authorization.

The plugin also includes `humanizer-zh`, which can independently polish Chinese text and checks wording before document delivery.

</details>

<details>
<summary>What it delivers</summary>

| Deliverable | Focus |
| --- | --- |
| PRD | Release scope, roles and permissions, business rules, exceptions, and observable acceptance outcomes |
| Technical plan | Affected modules, API and data design, key tradeoffs, and existing designs to reuse |
| Diagrams | Choose diagrams for the question at hand; keep diagrams, prose, data design, and acceptance criteria consistent |
| Version archive | PRD revision history, matching technical-plan version directories, and a document index linking existing designs |
| Review and acceptance records | Actual review scope, test results, manual feedback, unresolved issues, and evidence |

Java backend design and subsequent implementation use the bundled Java Development Manual (Huangshan Edition) and engineering layering guidelines.

</details>

<details>
<summary>How the workflow proceeds</summary>

1. **Read the current state.** Review the document index, current PRD, and affected designs; inspect implementation as needed. Earlier designs may still apply.
2. **Clarify requirements.** Separate established facts, design suggestions, and unresolved questions. Do not invent business rules.
3. **Deliver a draft.** Show the complete PRD draft after every revision and obtain approval before writing the official file. Base technical plans on the corresponding PRD and focus iterations on changes.
4. **Polish and review.** Use the bundled `humanizer-zh` before each document delivery to remove vague, repetitive, or formulaic wording. After approval of a technical plan, review it against requirements and applicable standards, recording findings and unverified items.
5. **Archive and continue delivery.** Maintain versions and file links. Verify subsequent implementation by module, recording automated test results separately from manual acceptance.

Editing preserves business rules, technical constraints, facts, certainty, and verification status. Claims about API reuse or transaction rollback need supporting evidence; code review findings and actual test results remain distinct.

</details>

<details>
<summary>How versions are stored</summary>

The initial PRD is `v1.0`. Each batch of official revisions increments the minor version; draft edits do not. Technical plans use the PRD version rather than a separate numbering scheme.

Example document layout (Chinese filenames match the bundled templates; the PRD filename can follow the project convention):

```text
project-docs/
├── PRD.md
├── 项目文档清单.md
├── v1.0/
│   └── 技术方案.md
├── v1.1/
│   └── 技术方案.md
└── facts/
```

Create a version directory only when a technical design needs archiving. When a version has no technical changes, record that in the document index instead of generating an empty plan. Create `facts/` when the first record is produced, and organize review, test, and manual acceptance results by document version and module.

</details>

## Installation

Download or clone the complete repository and open it in your agent. Run the commands below from the repository root. The installation prompt can be copied into the target agent.

| Environment | Installation method |
| --- | --- |
| Codex | `plugin.json` + `.agents/plugins/marketplace.json` |
| Claude Code | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` |
| Qoder CLI / IDE | `.qoder-plugin/plugin.json`; install or import from a local directory |
| Other local agents | Read `skills/work1z/SKILL.md` in the complete repository; automatic discovery depends on the host |

<details>
<summary>Copy to your agent: detect the environment and install</summary>

```text
Configure the currently open work1z-plugin repository for use in your agent environment.

First read README.en.md and the plugin manifests. Identify the absolute repository path
and the host you are actually running in. Do not infer the host solely from installed CLIs;
ask me if you cannot determine it.

If you are Codex:
1. Check codex plugin --help and existing marketplace and plugin records.
2. Run codex plugin marketplace add . from the repository root.
3. Run codex plugin add work1z@work1z-marketplace.
4. Use codex plugin list --json to verify installation and enabled status.

If you are Claude Code:
1. Check claude plugin --help and existing marketplace and plugin records.
2. Run claude plugin validate . from the repository root; if it passes,
   run claude plugin marketplace add .
3. Run claude plugin install work1z@work1z-marketplace --scope user.
4. Use claude plugin list --json to verify installation and enabled status.

If you are Qoder:
1. In the CLI, check qoder plugins --help and qoder plugins list --json.
2. Run qoder plugins validate . from the repository root and verify that it detects
   both work1z and humanizer-zh.
3. If validation passes, run qoder plugins install . --scope user.
4. Use qoder plugins list --json to verify work1z@local and enabled status.
5. Ask me to run /plugins reload in the current interactive session or start a new session,
   then verify both skills with /skills.
In Qoder IDE without the CLI, import the complete repository through Settings → Plugins.
If you cannot operate the UI, provide the entry point and absolute repository path,
and wait for me to import it. Do not claim it is installed.

If you are another agent supporting local skills:
Read that host's official loading instructions first. Keep the complete repository and
register or reference skills/work1z/SKILL.md and skills/humanizer-zh/SKILL.md
using a supported method.
Do not copy only a single SKILL.md or change the relative layout of the two skills
and the root assets directory.
If only reading a path within the conversation is supported, provide a copyable prompt
with absolute paths and explain that this is not a persistent installation.

If a source or plugin with the same name already exists, check whether it points to this
repository. Reuse it if it matches; report differences without overwriting it otherwise.
If a required CLI is missing or does not support these commands, explain what is missing;
do not automatically install or upgrade the host.

Finally, verify that both skills exist in the installed copy or registered directory and
that Work1z's relative references to humanizer-zh, templates, validation scripts, and
images resolve. Do not install humanizer-zh separately.
Report the actual installation location, enabled status, verification results, and whether
a new session is needed. Distinguish configuration checks from actual loading in a new
session; do not mark unverified behavior as verified.
```

</details>

<details>
<summary>Codex: manual installation and verification</summary>

Uses the [Agent Plugins structure](https://developers.openai.com/plugins/build/plugins). The root `plugin.json` declares the plugin; `.agents/plugins/marketplace.json` provides the local installation entry point.

Run from the repository root:

```bash
codex plugin marketplace add .
codex plugin add work1z@work1z-marketplace
codex plugin list --json
```

Start a new conversation after installation, then select Work1z or ask to use it for a plan. Desktop clients supporting local marketplaces can also install Work1z from its source in the plugin catalog. A CLI without the `plugin` subcommand needs a version supporting plugin management.

</details>

<details>
<summary>Claude Code: manual installation, invocation, and temporary use</summary>

Uses the [Claude Code plugin manifest](https://code.claude.com/docs/en/plugins-reference) and [marketplace](https://code.claude.com/docs/en/plugin-marketplaces). All platforms share the same `skills/` directory; no additional skill copies are needed.

Run from the repository root to install for the current user:

```bash
claude plugin validate .
claude plugin marketplace add .
claude plugin install work1z@work1z-marketplace --scope user
claude plugin list --json
```

Start a new Claude Code session and use `/work1z:work1z` to write plans or `/work1z:humanizer-zh` to polish existing Chinese text. The workflow also reads the bundled editing rules before delivering PRDs and technical plans.

For a temporary trial without registering a marketplace, run from the repository root:

```bash
claude --plugin-dir .
```

This loads the plugin only for that launch; it is not a persistent installation. See the [Claude Code command reference](https://code.claude.com/docs/en/plugins/cli-reference) for commands and scopes.

</details>

<details>
<summary>Qoder: CLI installation and IDE import</summary>

Uses the [Qoder plugin manifest](https://docs.qoder.com/cli/plugins-reference), stored in `.qoder-plugin/plugin.json`. Qoder discovers both skills in the root `skills/` directory; templates, scripts, and bundled editing rules ship with the plugin.

Qoder CLI supports direct installation from a local directory without registering a marketplace. Run from the repository root:

```bash
qoder plugins validate .
qoder plugins install . --scope user
qoder plugins list --json
```

Validation should list both `work1z` and `humanizer-zh`. Verify `work1z@local` and its enabled status in the plugin list. Start a new CLI session or run `/plugins reload` in the current interactive session, then check loaded skills with `/skills`. See the [Qoder CLI plugin guide](https://docs.qoder.com/cli/plugins).

In Qoder IDE, click Import under the Custom section in Settings → Plugins and select the repository root. Alternatively, use Create Plugin in the plugin marketplace to import a local folder. Select user or project scope, then enter `/` in a new conversation to check available capabilities. See [Qoder IDE plugin instructions](https://docs.qoder.com/extensions/plugins).

Import the complete directory containing `.qoder-plugin/`, `skills/`, and `assets/`, not a single `SKILL.md`. This repository provides the configuration; Qoder CLI validation, actual installation, and loading in a new session still need verification in an environment with Qoder installed.

</details>

<details>
<summary>Other agents: load the complete directory</summary>

The host must be able to read local Markdown files. Document validation also requires command execution and Python 3.9 or later. Skill discovery locations vary by host; Codex or Claude Code installation commands are not interchangeable with those of other agents.

Keep the complete repository. Replace the absolute path below with its actual location and copy this prompt to your agent:

```text
Read /absolute/path/to/repository/skills/work1z/SKILL.md and follow its rules for
the upcoming planning task.
Resolve templates and scripts relative to that skill directory. Chinese editing rules
are in ../humanizer-zh/SKILL.md, and introduction images are in the root assets/ directory.
Do not install humanizer-zh separately. First tell me the names of the two skills
you have read, then wait for my specific requirements.
```

This loads skills by path. To enable discovery in future sessions, register both entry points according to the host's official instructions while preserving their relative directory layout.

</details>

<details>
<summary>Dependencies, paths, and document validation</summary>

The plugin has no MCP service or account authentication. Marketplaces use relative paths, so cloning requires no configuration path changes. Re-register a local source if its directory moves.

[humanizer-zh](skills/humanizer-zh/SKILL.md) is bundled and requires no separate installation. Work1z reads it through a relative path within the plugin, independently of any globally installed skill with the same name. The bundled copy preserves the source revision marker `2026-09-23`, attribution, and [MIT license](skills/humanizer-zh/LICENSE). This license belongs to the bundled humanizer-zh skill; the repository does not currently declare a project-wide license.

The document validator requires Python 3.9 or later and has no third-party dependencies. Before draft delivery it checks structure, versions, and links; after archiving it checks the index and directories. See the [document validator guide](skills/work1z/references/文档校验脚本.md) for usage and arguments. To view arguments from the repository root:

```bash
python3 skills/work1z/scripts/validate_docs.py --help
```

</details>


## Automatic updates and releases

Stable versions are published on [GitHub Releases](https://github.com/idealzxz/work1z-plugin/releases). Prefer the attached `work1z-plugin-vX.Y.Z.zip`: extract the complete package, then follow the host installation steps above. This package includes a file checksum inventory; GitHub's automatic Source code archives do not.

Both skills invoke the shared updater at the start of each new task, checking only once within that task. When a newer stable release exists, it verifies the download and local files, updates the current plugin copy, and asks the agent to reread the new instructions. With no release or network access, it keeps the current version and reports the actual check result.

- Requires Python 3.9+, command execution, network access, and a writable plugin directory. No third-party Python dependencies.
- Follows stable Releases only, never main, prereleases, or downgrades.
- Preserves locally modified files and stops on missing release files or path conflicts. Files outside the release inventory are retained.
- Git development checkouts are checked but not rewritten. Host caches copied from Git without an inventory obtain a baseline from their current version's official release package; updates are skipped if that baseline is unavailable.
- Only the currently loaded plugin directory is updated. Host registration records and other installed copies are not modified. Reload the host or start a new session when required; the management UI may need refreshing to display the new version.
- Install the official `0.1.1` package or a later release to enable this mechanism. Older versions have no update entry point and cannot bootstrap it themselves.

To check or update manually from the plugin root:

```bash
python3 scripts/release.py update --check-only
python3 scripts/release.py update
```

See the [update rules](skills/work1z/references/自动更新.md) for status handling and recovery.

<details>
<summary>Maintainers: automatic packaging and publishing</summary>

The [Release workflow](https://github.com/idealzxz/work1z-plugin/blob/main/.github/workflows/release.yml) runs when a `vX.Y.Z` tag is pushed:

1. Run packaging and update tests.
2. Check that the root, Claude Code, and Qoder `plugin.json` versions match the tag.
3. Package both skills, templates, scripts, images, plugin configurations, and both READMEs. Generate a file inventory and ZIP SHA-256 checksum, excluding `.DS_Store`, Python caches, Git metadata, and development tests.
4. Create a draft Release, upload the ZIP and checksum, then publish it. Failed drafts can be retried; public releases are not overwritten, so corrections need a new version.

Use `MAJOR.MINOR.PATCH` versions such as `0.1.2` and matching `v0.1.2` Git tags. Before publishing, update all three manifests and README version badges, commit the release changes, then create and push the corresponding tag. The workflow runs only after the remote receives the tag. GitHub Actions must be enabled, with `GITHUB_TOKEN` allowed to write Releases.

Local validation and packaging (write outside the repository):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/release.py pack --tag v0.1.2 --output /tmp/work1z-dist
```

Outputs: `work1z-plugin-v0.1.2.zip` and `work1z-plugin-v0.1.2.zip.sha256`. Packaging alone does not create a tag or publish a Release. Replace the example tag when changing versions.

</details>

## Project files

<details>
<summary>Plugin structure</summary>

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
<summary>File navigation</summary>

| File | Purpose |
| --- | --- |
| [plugin.json](plugin.json) | Plugin ID, version, and display information |
| [Codex marketplace](.agents/plugins/marketplace.json) | Local Codex plugin installation |
| [Claude Code manifest](.claude-plugin/plugin.json) | Claude Code plugin ID, version, and display information |
| [Claude Code marketplace](.claude-plugin/marketplace.json) | Local Claude Code plugin installation |
| [Qoder manifest](.qoder-plugin/plugin.json) | Metadata for local Qoder installation and import |
| [SKILL.md](skills/work1z/SKILL.md) | Activation scope, execution rules, and delivery checks |
| [humanizer-zh](skills/humanizer-zh/SKILL.md) | Bundled Chinese editing rules |
| [PRD template](skills/work1z/references/PRD模板.md) | Requirements document structure and revision format |
| [Technical plan template](skills/work1z/references/技术方案模板.md) | Technical design structure |
| [Document index template](skills/work1z/references/项目文档清单模板.md) | Index of versions, modules, and design files |
| [Requirements diagram guidelines](skills/work1z/references/需求分析图表规范.md) | Diagram selection and notation |
| [Java Development Manual (Huangshan Edition)](skills/work1z/references/Java开发手册-黄山版.md) | Java coding and review guidelines |
| [Java directory structure and layering](skills/work1z/references/Java工程目录与分层.md) | Package structure, responsibilities, and dependency direction |
| [Document writing examples](skills/work1z/references/文档写作正反例.md) | Examples of prose, technical judgments, and revision records |

</details>
