# Token audit

Counts use one documented approximation for every file: `ceil(UTF-8 text characters / 4)`. This is reproducible and tokenizer-independent, but not a billing-token claim.

| Runtime material | Approx. tokens |
|---|---:|
| Ponytail source | 1654 |
| Caveman source | 880 |
| Naive combined baseline | 2534 |
| Discovery metadata (name + description only) | 75 |
| NeanderthAI core | 1325 |
| Default invocation (core; no optional reference) | 1325 |
| Language variant or clarification (core + communication) | 1774 |
| Failure recovery (core + recovery) | 1702 |
| Worst relevant invocation (core + all references) | 2151 |

Core reduction versus naive concatenation: **47.7%**.

Core counts include frontmatter; discovery metadata is listed separately, not added again. Host wrappers, paths, tool output, and generated responses are excluded. These are static instruction estimates, not measured task savings.

Progressive disclosure moves language variants and clarification (449 tokens) and failure recovery (377 tokens) out of the default path. Numeric feedback levels need only the core.
