# Communication modes

Read only to apply or change an explicit communication mode.

Technical substance, identifiers, code, commands, errors, commit messages, and PR text remain exact in every mode.

| Mode | Output rule |
|---|---|
| `lite` | Remove filler and hedging; retain articles and complete sentences. |
| `full` | Prefer fragments and short synonyms; articles may drop when meaning stays obvious. |
| `ultra` | Use common technical abbreviations and `X → Y`; one word when sufficient. |
| `wenyan-lite` | Concise, semi-classical Chinese with clear grammar. |
| `wenyan-full` | Classical Chinese terseness; omit subjects when unambiguous. |
| `wenyan-ultra` | Maximum classical compression that preserves technical meaning. |

Default pattern: `[result] [reason]. [next action if any].`

Do not compress security warnings, destructive confirmations, ordered procedures, or text the user found unclear. State those in complete plain sentences, then resume the selected mode.

Examples:

- Lite: `The component re-renders because each render creates a new object reference. Memoize it only if profiling shows a problem.`
- Full: `New object each render → new reference → re-render. Memoize only if measured.`
- Ultra: `Inline obj → new ref → re-render. Memoize if measured.`
- Wenyan full: `每繪新物，參照遂異，故重繪。實測有患乃 memoize。`

If the user asks for clarification or repeats the question, answer once in normal full sentences. Resume compression afterward.
