# Codex for Open Source 申请准备清单

这份清单用于准备材料，不代表满足条件或保证获批。项目状态、计划规则和申请入口可能变化，正式申请前应以 OpenAI 官方最新页面为准。

当前状态（2026-08-21）：仓库已经维护者确认并设为 **Public**；`v0.1.0` 正式标签和 GitHub Release 正在准备中。

## 1. 公开前仓库质量

- [x] 维护者已逐文件审核，无私人路径、密钥、联系方式或内部资料。
- [x] 所有文本和测试语料均为原创、获授权或许可证兼容，并记录来源。
- [x] `LICENSE`、`README.md`、`CONTRIBUTING.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md` 齐全。
- [x] `python3 -m unittest discover -s tests -v` 通过（9 项，2026-08-21）。
- [x] `python3 scripts/public_repo_audit.py` 通过（2026-08-21）。
- [x] Codex skill validator 通过（2026-08-21）。
- [x] `VERSION`、Changelog 和 release notes 一致；正式 Git tag 将在最终 CI 通过后创建。
- [x] README 中的安装方式已在干净目录实测。
- [x] GitHub 链接已指向 `weasleycai56-ctrl/humanize-zh`。
- [ ] 已启用 Private Vulnerability Reporting 或提供明确的私密安全渠道。

## 2. 建立可验证的 OSS 记录

- [x] 维护者已完成最终审核，并确认将仓库设为 Public（2026-08-21）。
- [ ] 发布 `v0.1.0`，附真实测试结果和已知限制。
- [ ] 建立清楚的 issue 标签，例如 `bug`、`rule-proposal`、`false-positive`、`good-first-issue`。
- [ ] 对用户反馈和 PR 保持可见、礼貌、可复现的维护记录。
- [ ] 用真实 issue/PR 展示规则如何因反例而改进。
- [ ] 在有证据后再记录 stars、forks、downloads、外部贡献者或真实使用案例。
- [ ] 不购买、交换或虚构任何热度数据。

## 3. 申请材料

准备以下可核查信息：

- 仓库 URL、许可证、维护者角色和主要贡献；
- 项目解决的问题，以及为什么需要中文优先的规则体系；
- 可运行的安装命令和 1–2 个简短演示；
- 测试、安全、隐私、版权和治理措施；
- 真实维护活动：release、issue、PR、讨论和路线图；
- Codex 如何用于开发、测试或维护本项目的具体说明；
- 任何使用量或社区影响都附公开来源和统计日期。

## 4. Copy-ready 项目定位

> Humanize ZH is an MIT-licensed, Chinese-first writing-style linter and rewriting skill for Codex and compatible Agent Skills tools. It provides explainable diagnostics and context-aware light or strong revisions across casual, professional, academic, social, and marketing writing. The project deliberately does not claim to detect AI authorship; it focuses on observable editorial patterns, factual preservation, and maintainable regression fixtures.

## 5. Copy-ready “why this matters”

> Most generic humanizer prompts are built around English word lists. Humanize ZH documents patterns that are especially salient in modern Chinese writing—such as campaign-style significance claims, stacked four-character abstractions, mechanical parallelism, vague consensus, and forced elevation—while recording legitimate-use boundaries. The repository turns those decisions into a maintainable Skill, a deterministic local audit, and cross-context behavioral fixtures.

## 6. 诚实填写的占位项

提交前用公开证据替换方括号；没有数据就写“not yet measured”，不要估算。

- Stars: `[public count as of YYYY-MM-DD / not yet measured]`
- Downloads or installs: `[source and date / not yet measured]`
- External contributors: `[public count / none yet]`
- User examples: `[linked public examples / none published yet]`
- Latest release: `[tag and URL]`
- Test status: `[workflow or local command and commit]`

## 7. 申请前最后核对

- [ ] 查阅 OpenAI 官方最新资格、条款和申请页面。
- [ ] 所有陈述能由仓库、release 或公开链接验证。
- [ ] 没有把本地完成、计划功能或个人试用写成社区采用。
- [ ] 没有暗示 OpenAI 认可、赞助或保证资格。
- [ ] 保存申请内容和统计日期，便于后续更新。
