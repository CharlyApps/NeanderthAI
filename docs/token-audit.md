# Token audit

Counts use one documented approximation for every file: `ceil(UTF-8 text characters / 4)`. This is reproducible and tokenizer-independent, but not a billing-token claim.

| Runtime material | Approx. tokens |
|---|---:|
| Ponytail source | 1654 |
| Caveman source | 880 |
| Naive combined baseline | 2534 |
| NeanderthAI core | 1129 |
| Typical invocation (core + one smallest relevant reference) | 1457 |
| Worst relevant invocation (core + all references) | 1847 |

Core reduction versus naive concatenation: **55.4%**.

Progressive disclosure moves explicit communication variants (390 tokens) and failure recovery (328 tokens) out of the default path. Most direct tasks need only the core.
