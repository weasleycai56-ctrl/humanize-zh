# Tests

The fixtures are behavioral examples for maintainers and agents. Each case records the source, intended profile and mode, rules that should be noticed, facts or terms that must survive, phrases that should not survive, and one acceptable revision.

The `expected_after` field is not a golden string. Good rewrites can differ. Tests enforce stable rule coverage and preservation invariants rather than exact prose.

Some examples deliberately show the danger of adding specificity that was not present in the source. Their `notes` explain that those details must be verified before use. This makes the fixtures useful for reviewing an agent's judgment, not for copying answers blindly.

Run:

```bash
python3 -m unittest discover -s tests -v
```

When adding a rule, include at least one positive fixture and consider adding a legitimate-use counterexample. Do not add a phrase solely because it appeared in one AI-generated sample; document the editorial harm and boundary first.
