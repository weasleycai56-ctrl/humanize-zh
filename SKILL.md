---
name: humanize-zh
description: Audit and rewrite Chinese text that feels formulaic, inflated, or overly promotional. Use for explainable Chinese writing-style linting and humanization; do not use it to determine whether a person or AI authored text.
---

# Humanize ZH

Improve Chinese prose by identifying observable writing patterns and revising them without inventing facts. Treat every finding as an editorial signal, never as proof of AI authorship.

## Choose the task

Infer omitted settings conservatively:

- `audit`: diagnose only. Do not rewrite unless the user also asks for a revision.
- `light`: preserve structure, voice, claims, and most wording; fix the clearest style problems.
- `strong`: freely restructure and compress while preserving supported meaning, facts, names, figures, citations, uncertainty, and required calls to action.

Supported profiles are `casual`, `professional`, `academic`, `social`, and `marketing`. Infer the profile from context; when genuinely ambiguous, use `professional`. Keep the user's language variety and script unless asked to convert them.

Read resources progressively:

- Read [references/chinese-ai-tells.md](references/chinese-ai-tells.md) when auditing or explaining findings.
- Read [references/rewrite-rules.md](references/rewrite-rules.md) before any rewrite.
- Read only the relevant section of [references/style-profiles.md](references/style-profiles.md) for the selected profile.
- Consult [examples/before-after.md](examples/before-after.md) only when a boundary or transformation is unclear.

For a deterministic first pass on longer text, optionally run `python3 scripts/audit_text.py <file> --format json`. Its output is a candidate list to review in context, not a verdict.

## Work from evidence

1. Identify the text's purpose, audience, facts that must survive, voice, and formatting constraints.
2. Flag only observable patterns supported by the rule library. Quote the smallest useful excerpt.
3. Distinguish harmful habits from legitimate rhetoric. Parallelism, colons, bold text, and formal phrases are not errors by themselves.
4. Rank findings by effect on clarity, credibility, specificity, or natural rhythm. Do not inflate the issue count.
5. For rewrites, remove unsupported evaluation before changing tone. Prefer concrete subjects, actions, evidence, and varied sentence rhythm.
6. Compare the result with the source and restore any lost facts, qualifiers, citations, or intent.

## Output contract

For `audit`, return:

```markdown
文风信号：低 / 中 / 高

| 类型 | 原句 | 原因 | 建议 |
|---|---|---|---|
| ... | ... | ... | ... |

总体建议：...
```

The signal level summarizes editing intensity. Never label it an “AI probability,” detection score, or authorship judgment.

For `light` or `strong`, return:

```markdown
修改版
...

主要调整
- 问题类型：具体改动与理由
```

If the user asks for clean copy only, provide only the revised text. If a source passage contains unverifiable claims, preserve or qualify them rather than silently strengthening them. Never fabricate examples, data, quotations, citations, personal experiences, or first-person feelings to sound “human.”

## Boundaries

- Do not promise to bypass AI detectors or plagiarism checks.
- Do not erase domain terminology, legal wording, academic caution, accessibility, or a deliberate brand voice merely to create variation.
- Do not convert all formal Chinese into casual speech. Naturalness depends on audience and purpose.
- Do not treat regional usage in Mainland China, Hong Kong, Taiwan, Singapore, or diaspora communities as inherently unnatural.
- When the input is already clear, specific, and appropriate, say so and make few or no changes.
