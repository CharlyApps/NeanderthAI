# NeanderthAI merge analysis

## Sources inspected

The repository was empty and had no Git history. Discovery found these authoritative local sources in the installed Ponytail 4.9.0 bundle:

- `skills/ponytail/SKILL.md` — complete Ponytail runtime skill; no referenced files.
- `benchmarks/arms/caveman-SKILL.md` — Caveman skill vendored verbatim from `JuliusBrussee/caveman`; no referenced files.
- `benchmarks/arms/ponytail.js` and `caveman.js` — adapters that inject each complete skill file as a system prompt; they add no behavior.
- Ponytail benchmark reports and README — supporting evidence that Ponytail changes implementation scope while Caveman changes prose, and that validation/safety must not be reduced.

Reproducible snapshots are retained in `sources/`. Original installed files were not changed.

## Capability matrix

| Capability | Trigger/input | Source behavior and workflow | Overlap/conflict and cost | NeanderthAI disposition |
|---|---|---|---|---|
| Implementation minimalism | Any coding/build/refactor/review task | Ponytail climbs YAGNI → repo reuse → stdlib → native → installed dependency → one line → minimum code | Caveman does not constrain code | **Preserve** in core ladder |
| Inspect before editing | Any implementation; especially bugs | Ponytail reads the real flow and all callers before choosing the smallest root-cause fix | Can conflict with token minimization if interpreted as exhaustive reading | **Merge** with targeted search and scope escalation |
| YAGNI/challenge scope | Speculative or over-engineered requirement | Full/ultra may skip or challenge work; lite builds and mentions alternative | Must not override explicit insistence | **Preserve** with user intent precedence |
| Existing/native mechanisms | Helpers, platform controls, dependencies | Reuse before creating code or packages | None | **Preserve** verbatim in ladder semantics |
| Safety boundaries | Trust boundaries, loss, security, accessibility | Ponytail forbids simplifying these away | Caveman compression can make warnings ambiguous | **Resolve**: correctness/safety force normal grammar |
| Hardware calibration | Physical timing/sensors | Ponytail retains a tuning knob | Specialized token cost | **Preserve** as one core sentence |
| Small runnable check | Non-trivial logic | Ponytail requires one minimal test/self-check; trivial one-liners need none | None | **Preserve**, generalized to proportional validation |
| Deliberate shortcut marker | Known ceiling such as global lock | Ponytail comment records ceiling and upgrade trigger | Prefix was source-specific | **Replace** prefix with `neanderthai:` |
| Concise prose | Caveman/brief/token requests | Caveman removes filler, hedging, articles; keeps technical accuracy | Removing meaningful uncertainty contradicts accuracy | **Merge** into terse output that retains confidence, conditions, units, and negations |
| Prose intensity | `lite`, `full`, `ultra` | Increasing grammatical and abbreviation compression | Names overlap Ponytail build intensity | **Improve**: independent feedback levels `0–3`; legacy aliases retained |
| Classical Chinese modes | `wenyan-lite/full/ultra` | Increasing classical-Chinese compression | Unique to Caveman; uncommon at runtime | **Preserve** behind progressive disclosure |
| Auto-Clarity | Warning, destructive action, ordered steps, repeated question | Caveman temporarily restores full clarity | Supports precedence rules | **Preserve** and strengthen for ambiguity-sensitive work |
| Exact technical artifacts | Code, errors, commits, PRs | Caveman leaves code unchanged and quotes errors exactly | None | **Preserve** |
| Persistence/off switch | Activated mode across session; normal mode | Both persist and stop on their source-specific phrase | Separate switches are redundant in merged skill | **Merge** into NeanderthAI persistence; inherited trigger names remain discoverable |
| Output cap | After implementation | Ponytail: code first and at most three skip lines | Can conflict with requested reports | **Simplify** to result + validation + at most one skip line; explicit reports exempt |
| Failure recovery | Command/test failure | Parents imply validation but lack a compact recovery classifier | New behavior; conditional context | **Improve** in `references/recovery.md` |
| Adaptive investigation | Local vs uncertain vs architectural tasks | Ponytail requires understanding but has one general path | Unnecessary reads on trivial work | **Improve** with Direct/Investigate/Deep routing |

## Conflict resolution

The parents are complementary: Ponytail controls implementation; Caveman controls communication. NeanderthAI exposes those as independent build and feedback controls so a user can request strict minimalism with fully grammatical feedback, or compact feedback without changing implementation decisions. The main conflict occurs when compressed prose threatens safety or comprehension. NeanderthAI uses this order: correctness, repository/user constraints, safety/reversibility, verifiability, task evidence, context cost, execution complexity. Therefore terse prose yields to precise grammar for warnings, irreversible actions, ordered procedures, and clarification.

The second tension is between Ponytail's “trace the whole flow” and minimal context. NeanderthAI interprets “whole” as the smallest complete dependency surface, found by search and expanded only on evidence. This keeps root-cause quality without automatic repo-wide ingestion.

## Progressive disclosure

`SKILL.md` contains only the default router, ladder, validation boundary, and output contract. Explicit prose variants live in `references/communication.md`; failure classification lives in `references/recovery.md`. There is no index layer and no reference-to-reference chain.

## Platform findings

- Codex uses the Agent Skills format and discovers project skills under `.agents/skills`; it supports optional `agents/openai.yaml` metadata.
- Claude Code uses `.claude/skills`, follows the Agent Skills standard, and supports additional vendor-only frontmatter that this portable skill intentionally avoids.
- GitHub Copilot accepts `.github/skills`, `.claude/skills`, or `.agents/skills` for project skills and the same required `name`/`description` frontmatter.

One canonical source is copied deterministically into isolated platform package roots under `dist/`, avoiding divergent prompts and avoiding duplicate registration in the repository root.

## Enhancement review: 2026-09-18

The review found these specific issues and addressed them without adding runtime dependencies:

| Observed issue | Change |
|---|---|
| Removing “hedging” could turn an unconfirmed cause into a fact. | Preserve uncertainty, conditions, units, negations, and actual test status at every feedback level. |
| The implementation loop also triggered for review and explanation requests. | Route by requested action before changing files; prose-only work requires no repo exploration. |
| “Start at Direct” conflicted with already-known security or architectural risk. | Select the appropriate investigation level immediately from available evidence. |
| Reloading/defaults, temporary overrides, and numeric language changes were ambiguous. | Preserve explicit conversation settings, expire one-answer overrides, and keep language/build independent. |
| Recovery labeled a failure introduced merely because the edited file was on its path. | Require causal evidence; compare equivalent baselines without discarding working changes. |
| “Fix only introduced failures” excluded the existing bug the user requested. | Permit the requested bug fix and new regressions; retain scope boundaries for unrelated failures. |
| A one-test rule could duplicate existing tests or cap security validation. | Reuse the repository's test convention and validate relevant edge cases. |
| Reference links outside `SKILL.md` went unchecked; binary assets could crash text checks; the Windows-path regex was overescaped. | Validate inline links in every Markdown file, require local targets within the bundle, skip binary assets in text checks, and correct the regex. |
| Eval “invariants” were merely required words; even empty case fields could pass. | Validate nonempty typed fields, unique IDs, and required categories, explicitly reporting that no model behavior was tested. |
| The “typical invocation” estimate arbitrarily added the smallest reference. | Show separate core-only, communication, recovery, and all-reference scenarios plus discovery metadata. |

Four standard-library regression tests exercise the tooling changes. Five focused live prompt checks use Claude Code 2.1.267 with the canonical core and both references appended, all tools disabled, user/project settings excluded, hooks disabled, and no session persistence. Only case inputs are supplied, not expected outputs or scoring criteria. These checks assess responses against the rubric; they do not test skill discovery, real multi-turn persistence, autonomous tool choices, or behavior on every supported host.

| Live case | Observed response | Rubric result |
|---|---|---|
| `compressed-uncertainty` | Retained “unconfirmed”, TTL `30s`, and “Regression test not run.” | Pass |
| `repair-requested-existing-bug` | Proposed `>= 18` and assertions for ages 18 and 17; explicitly said it did not run them. | Pass |
| `temporary-feedback-override` | Identified build `ultra` and restored feedback `3` after the temporary override. | Pass for the supplied conversation scenario |
| `review-without-edits` | Identified default-allow access, suggested an allowlist, and said no changes were made. | Pass for response content; mutation prevention enforced by disabled tools |
| `failure-attribution-needs-evidence` | Called attribution uncertain and proposed an equivalent isolated baseline comparison. | Pass |

No before/after model benchmark was run, so these results support the revised instructions without establishing a measured improvement in model accuracy or task token consumption.
