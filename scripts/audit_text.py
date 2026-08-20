#!/usr/bin/env python3
"""Deterministic first-pass linter for common Chinese writing-style patterns.

This tool reports editorial signals. It does not detect AI authorship.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean, pstdev


@dataclass(frozen=True)
class Rule:
    rule_id: str
    label: str
    pattern: str
    reason: str
    suggestion: str


@dataclass(frozen=True)
class Issue:
    rule_id: str
    label: str
    excerpt: str
    reason: str
    suggestion: str


RULES = (
    Rule(
        "ZH01",
        "空泛开场",
        r"(?:随着.{0,18}(?:不断发展|快速发展|日益普及)|在当今.{0,14}(?:背景下|时代)|近年来.{0,16}越来越受到关注)",
        "背景句缺少可核查的时间、范围或变化，主题出现得较晚。",
        "从具体事件、问题、数据或结论开始；必要背景随后补充。",
    ),
    Rule(
        "ZH02",
        "意义膨胀",
        r"(?:不仅(?:仅)?是.{0,28}(?:更是|而且是)|意义深远|具有(?:重要|重大|里程碑式)意义|注入(?:了)?新动能|迈出(?:了)?.{0,16}(?:坚实|关键)(?:的)?一步|开启.{0,12}新篇章|彰显(?:了)?)",
        "评价强度可能超过文本给出的事实或证据。",
        "说明具体改变、受益对象和结果；没有依据的升华可以删除。",
    ),
    Rule(
        "ZH03",
        "宣传腔或绝对化",
        r"(?:重磅|震撼发布|颠覆(?:性)?|史诗级|不容错过|必看|必收藏|前所未有|彻底改变|重新定义|引领未来|全网最全|终极指南|一次讲透)",
        "高强度措辞可能制造了超出证据的承诺。",
        "改写为具体功能、收益、适用对象或可验证差异。",
    ),
    Rule(
        "ZH04",
        "机械对举或堆叠排比",
        r"(?:不仅.{0,30}(?:而且|更)|既.{0,20}又.{0,20}|全方位[、，]多维度[、，]深层次|新高度[、，]新格局[、，]新篇章)",
        "形式整齐，但项目之间的逻辑关系可能不清或含义重叠。",
        "合并同义项，并写清并列、因果、递进或取舍关系。",
    ),
    Rule(
        "ZH07",
        "空泛归因或伪共识",
        r"(?:众所周知|不难发现|显而易见|有研究表明|业内普遍认为|专家指出|毋庸置疑|不可否认|值得注意的是)",
        "判断的来源、范围或证据不明确。",
        "补充可核查来源和适用范围；否则改成有边界的判断。",
    ),
    Rule(
        "ZH08",
        "抽象动作",
        r"(?:进行.{0,10}(?:优化|提升|推进)|实现.{0,10}(?:提升|突破|转变)|赋能.{0,12}|打造.{0,12}(?:体系|生态|平台)|构建.{0,12}(?:格局|体系)|推动.{0,12}落地)",
        "抽象动词隐藏了行动主体、具体动作或结果。",
        "写明谁做了什么，以及可观察的结果。",
    ),
    Rule(
        "ZH10",
        "强行总结",
        r"(?:综上所述|总而言之|由此可见|让我们携手|共同期待.{0,12}(?:未来|明天))",
        "结尾可能只是在复述主题或追加空泛号召。",
        "以具体结论、限制、下一步或问题收束。",
    ),
    Rule(
        "ZH11",
        "伪口语或替读者表态",
        r"(?:你是不是也|相信大家(?:都)?|让我们一起|想必大家|还不赶快|你一定会)",
        "文本替读者预设情绪或用生硬互动制造亲近感。",
        "直接说明读者能获得什么，保留真实而克制的互动。",
    ),
    Rule(
        "ZH12",
        "空泛金句",
        r"(?:真正的.{0,16}从来不是.{0,20}而是|我们缺少的不是.{0,20}而是|选择比努力更重要|每一次.{0,18}都是一次)",
        "对称句式可能把复杂问题压缩成无法验证的二分判断。",
        "改成有条件、有对象、能由上下文支持的具体结论。",
    ),
    Rule(
        "ZH14",
        "多重限定",
        r"(?:可能.{0,8}(?:在一定程度上|或许).{0,10}(?:有助于|能够)|在一定程度上.{0,8}可能.{0,8}(?:有助于|能够))",
        "多个同义缓和词叠加，必要的不确定性变得含混。",
        "保留一个准确限定，并说明不确定性的来源或范围。",
    ),
)

RULE_MAP = {rule.rule_id: rule for rule in RULES}
SENTENCE_BOUNDARY = re.compile(r"(?<=[。！？!?；;])")


def sentence_for(text: str, start: int, end: int, limit: int = 100) -> str:
    left_candidates = [text.rfind(mark, 0, start) for mark in "。！？!?；;\n"]
    left = max(left_candidates) + 1
    right_candidates = [pos for mark in "。！？!?；;\n" if (pos := text.find(mark, end)) >= 0]
    right = min(right_candidates) + 1 if right_candidates else len(text)
    excerpt = re.sub(r"\s+", " ", text[left:right]).strip()
    if len(excerpt) > limit:
        excerpt = excerpt[: limit - 1].rstrip() + "…"
    return excerpt


def regex_issues(text: str) -> list[Issue]:
    issues: list[Issue] = []
    for rule in RULES:
        match = re.search(rule.pattern, text)
        if match:
            issues.append(
                Issue(
                    rule.rule_id,
                    rule.label,
                    sentence_for(text, match.start(), match.end()),
                    rule.reason,
                    rule.suggestion,
                )
            )
    return issues


def structural_issues(text: str) -> list[Issue]:
    issues: list[Issue] = []

    connectors = re.findall(r"(?:首先|其次|再次|此外|另外|最后|综上)", text)
    if len(connectors) >= 3:
        issues.append(
            Issue(
                "ZH05",
                "连接词流水线",
                "、".join(connectors[:6]),
                "多个结构词连续替内容导航，文章可能呈现答题模板感。",
                "只保留有导航价值的层级，其余用内容之间的真实关系衔接。",
            )
        )

    visible_marks = len(re.findall(r"(?:——|：|!|！|\*\*[^*]+\*\*)", text))
    if len(text) >= 80 and visible_marks / len(text) >= 0.035:
        issues.append(
            Issue(
                "ZH06",
                "标点与格式表演",
                f"{len(text)} 字中检测到 {visible_marks} 处冒号、破折号、感叹号或加粗",
                "视觉强调较密，可能打断句子和段落的自然节奏。",
                "让每处强调只承担一个功能，并把不必要的标签写回自然句。",
            )
        )

    paragraphs = [re.sub(r"\s+", "", p) for p in re.split(r"\n\s*\n", text) if len(re.sub(r"\s+", "", p)) >= 20]
    if len(paragraphs) >= 3:
        lengths = [len(p) for p in paragraphs]
        avg = mean(lengths)
        variation = pstdev(lengths) / avg if avg else 1
        if variation <= 0.12:
            issues.append(
                Issue(
                    "ZH09",
                    "段落过度均匀",
                    f"{len(lengths)} 个主要段落长度为 {', '.join(map(str, lengths[:6]))} 字",
                    "连续段落长度高度接近，信息可能被同一模板切分。",
                    "按观点转折和信息量重新分段，不必刻意等长。",
                )
            )
    return issues


def audit(text: str) -> dict[str, object]:
    issues = regex_issues(text) + structural_issues(text)
    issues.sort(key=lambda item: item.rule_id)
    unique_rules = len({issue.rule_id for issue in issues})
    affected_ratio = min(1.0, sum(len(issue.excerpt) for issue in issues) / max(len(text), 1))
    if unique_rules >= 5 or (unique_rules >= 4 and affected_ratio >= 0.7):
        signal = "高"
    elif unique_rules >= 2:
        signal = "中"
    else:
        signal = "低"
    return {
        "disclaimer": "这是写作模式诊断，不是 AI 作者身份检测。",
        "signal": signal,
        "issue_count": len(issues),
        "issues": [asdict(issue) for issue in issues],
    }


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        f"文风信号：{report['signal']}",
        "",
        str(report["disclaimer"]),
        "",
        "| 类型 | 原句或证据 | 原因 | 建议 |",
        "|---|---|---|---|",
    ]
    issues = report["issues"]
    if not issues:
        lines.append("| 未发现明显模式 | — | 当前规则未发现需要优先修改的问题 | 结合语境人工复核即可 |")
    else:
        for issue in issues:
            values = [
                f"{issue['rule_id']} {issue['label']}",
                issue["excerpt"],
                issue["reason"],
                issue["suggestion"],
            ]
            escaped = [str(value).replace("|", "\\|").replace("\n", " ") for value in values]
            lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("path", nargs="?", type=Path, help="UTF-8 text file, or - for stdin")
    source.add_argument("--text", help="Text to audit directly")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.text is not None:
        text = args.text
    elif str(args.path) == "-":
        text = sys.stdin.read()
    else:
        text = args.path.read_text(encoding="utf-8")
    report = audit(text)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
