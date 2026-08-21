# Humanize ZH（中文 AI 文风检查与改写）

一个面向中文写作习惯的可解释 writing-style linter / humanizer Skill。

它识别空泛开场、意义膨胀、宣传腔、机械排比、连接词流水线、标点与格式滥用、伪共识、抽象动作、整齐段落、强行总结等可观察的写作模式，再按场景进行轻度或深度改写。

> **重要边界**：本项目检查的是写作模式，不判断、证明或估算文本是否由 AI 创作。所谓“AI 味”是通俗的编辑描述，不是可靠的作者身份信号。

## English summary

**Humanize ZH** is an explainable Chinese writing-style linter and rewriting skill. It focuses on patterns that are especially noticeable in contemporary Chinese prose: inflated significance, campaign-like slogans, mechanical parallel structures, vague attribution, abstract action verbs, excessive formatting, uniform paragraphs, and forced conclusions. It supports audit-only, light-edit, and strong-rewrite modes across casual, professional, academic, social, and marketing contexts.

It does **not** detect AI authorship and does not promise to bypass AI detectors. It helps people edit observable style problems while preserving facts, citations, uncertainty, regional language, and author intent.

## 为什么不是一个 prompt

仓库把容易变化的部分拆开维护：

- `SKILL.md`：工作流、模式、输出契约和安全边界；
- `references/`：中文信号库、改写规则、五类场景配置；
- `scripts/audit_text.py`：零第三方依赖的确定性初筛；
- `tests/fixtures/`：跨场景 before/after 行为语料；
- `tests/`：规则覆盖、事实保留和 CLI 契约测试；
- `.github/`：问题反馈、规则提案和贡献流程。

规则的目标不是累计“可疑词黑名单”。每条规则都说明编辑后果、合法使用边界和可执行建议。

## 功能

- `audit`：只诊断，输出问题类型、原句、原因和建议；
- `light`：尽量保留结构和作者措辞，只处理明显套话；
- `strong`：在保留事实与意图的前提下压缩、重排和重写；
- 场景：`casual`、`professional`、`academic`、`social`、`marketing`；
- 简体、繁体及地区用语不被自动当作错误；
- 学术、医学、法律文本的限定条件不会因为“去 AI 味”而被随意删除；
- 本地 CLI 只读取你主动提供的文本，不联网、不上传。

## 安装

### Codex

克隆或下载本仓库后，把整个目录复制到个人 skills 目录。

macOS / Linux：

```bash
cp -R humanize-zh ~/.codex/skills/humanize-zh
```

Windows PowerShell：

```powershell
Copy-Item -Recurse .\humanize-zh "$HOME\.codex\skills\humanize-zh"
```

重新打开 Codex 后，可以显式调用 `$humanize-zh`；其描述也支持在合适的中文编辑任务中自动发现。

如只想临时试用，可让 Codex 直接读取本仓库里的 `SKILL.md`，无需安装 Python 依赖。

### 其他兼容 Agent Skills 的工具

把 `humanize-zh` 文件夹放到该工具约定的 skills 目录。不同产品的发现路径和调用语法可能不同，请以对应产品文档为准。核心 Skill 不依赖 MCP 或外部服务。

## 使用

直接给出文本、模式和场景：

```text
使用 $humanize-zh，以 audit 模式检查下面这段中文。只诊断，不改写：
……
```

```text
使用 $humanize-zh，以 light + professional 改写这封项目邮件。
保留所有日期、负责人和风险说明，只输出修改版：
……
```

```text
使用 $humanize-zh，以 strong + social 重写这段小红书文案。
不要编造个人体验、数字或用户评价，并解释三项主要修改：
……
```

如果未指定模式，Skill 会根据“检查”或“改写”等意图判断；无法判断场景时采用 `professional`。

## 可解释诊断示例

输入：

> 随着人工智能技术的快速发展，AI 正以前所未有的速度重塑工作。这不仅是一场技术革命，更是一场深刻变革。对于普通人而言，拥抱 AI 已经成为不容忽视的重要课题。

诊断节选：

| 类型 | 原句 | 原因 | 建议 |
|---|---|---|---|
| ZH01 空泛开场 | 随着人工智能技术的快速发展 | 没有限定时间或具体变化，主题出现得较晚 | 从已经发生的具体工作变化进入 |
| ZH02 意义膨胀 | 不仅是一场技术革命，更是一场深刻变革 | 用对称升华替代了实际影响 | 说明哪些任务、哪些人、发生了什么变化 |
| ZH03 宣传腔 | 前所未有的速度 | 程度判断没有证据 | 删除或补充可验证的范围与数据 |

`strong + professional` 的一种改法：

> AI 工具已经进入不少日常工作：写邮件、整理资料、查找信息，都可以先交给工具处理初稿。真正需要决定的是哪些任务可以自动化，哪些仍需人工核对和判断。

更多案例见 [examples/before-after.md](examples/before-after.md)。

## 确定性初筛 CLI

CLI 适合长文本预扫和规则回归，不负责生成改写：

```bash
python3 scripts/audit_text.py article.txt
python3 scripts/audit_text.py article.txt --format json
printf '重磅发布，这份内容不容错过。' | python3 scripts/audit_text.py -
```

输出中的“低/中/高”表示建议修改强度，不是 AI 概率。正则候选必须结合语境人工复核。

## 测试

项目只需要 Python 3.10+，无第三方运行依赖：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/public_repo_audit.py
```

每次推送到 `main` 或提交 pull request 时，GitHub Actions 也会运行同一套测试和公开安全审计。测试不会要求生成文本逐字等于标准答案，而会检查场景覆盖、规则稳定性、事实保留项、版本契约和禁止出现的套话。详见 [tests/README.md](tests/README.md)。

## 限制

- 语言风格没有单一标准；正式、排比、口号或整齐结构可能是作者有意选择。
- 确定性脚本以精确率和可解释性优先，无法识别所有上下文，也会有误报。
- Skill 的改写质量取决于输入信息。原文没有事实时，它不应编造细节来填满文本。
- 项目不能证明作者身份、训练数据来源、抄袭与否，也不保证通过任何 AI 检测器。
- 当前规则以现代书面中文为主，方言、古文、诗歌、小说对白和强监管行业模板仍需更多语料验证。
- before/after 示例是可接受改写之一，不是唯一正确答案。

## 路线图

- `v0.1.x`：根据公开 issue 修正规则边界，增加负例和繁体中文样本；
- `v0.2.0`：增加结构化 JSON 诊断 schema 与可选的基准评测脚本；
- `v0.3.0`：建立经过人工标注的地区/场景平衡小型评测集；
- 后续候选：编辑器集成、可配置规则组、社区维护的领域配置。

路线图是方向，不承诺日期。涉及语料发布时会先完成授权、隐私和许可证审查。

## 参与贡献

规则提案需要说明真实编辑问题、适用边界、正例和合法反例，而不是只提交一个“AI 高频词”。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请遵循 [SECURITY.md](SECURITY.md)，社区行为遵循 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 版本与许可证

当前版本：`v0.1.0`。变更见 [CHANGELOG.md](CHANGELOG.md) 和 [v0.1.0 release notes](docs/releases/v0.1.0.md)。

项目采用 [MIT License](LICENSE)。仓库不包含第三方语料、模型权重、品牌素材或用户文本。
