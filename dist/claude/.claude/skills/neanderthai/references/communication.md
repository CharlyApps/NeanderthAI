# Feedback compactness

Read only to apply or change feedback level or language style.

Feedback level changes wording, never reasoning depth or implementation quality. Technical substance, identifiers, code, commands, errors, commit messages, and PR text remain exact at every level.

| Level | Alias | Output rule |
|---:|---|---|
| `0` | clear | Concise full sentences; no caveman grammar. |
| `1` | compact / lite | Remove filler and repetition; retain full sentences and meaningful uncertainty. |
| `2` | caveman / full | Prefer fragments and short synonyms; articles may drop when meaning stays obvious. |
| `3` | grunt / ultra | Use common technical abbreviations and `X → Y`; one word when sufficient. |

Default pattern: `[result] [reason]. [next action if any].`

Use `wenyan-lite|full|ultra` for classical-Chinese style at levels `1|2|3`. This changes feedback only and preserves the current build mode.

Keep the selected language when changing numeric levels. A request such as “feedback 0 for this answer” temporarily overrides compactness; “feedback 0 from now on” persists. Preserve causal qualifications, negations, units, and confidence at every level.

Do not compress security warnings, destructive confirmations, ordered procedures, or text the user found unclear. State those in complete plain sentences, then resume the selected mode.

Examples:

- Level 1: `A new object reference can defeat a memoized child's shallow prop comparison. Profile before optimizing.`
- Level 2: `New object ref can defeat shallow prop comparison. Profile first.`
- Level 3: `New ref may defeat shallow compare. Profile first.`
- Wenyan full: `新參照或破淺比之效。先測後改。`

If the user asks for clarification or repeats the question, answer once in normal full sentences. Resume compression afterward.
