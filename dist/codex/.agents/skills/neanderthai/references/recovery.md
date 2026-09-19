# Evidence-based recovery

Read only after a command fails, required evidence is unavailable, or observed failures may be unrelated.

1. Keep the command, exit status, and shortest output span that identifies the failure; redact secrets.
2. Classify it:
   - **introduced:** evidence isolates the change as the cause, such as a passing prior version under equivalent conditions;
   - **pre-existing:** the same failure reproduces on the prior version under equivalent conditions;
   - **uncertain:** evidence does not yet distinguish them.
   Touching the failing path alone proves nothing. Compare in an isolated workspace; preserve the user's current changes.
3. Decide whether the signal disproves the current hypothesis. Change strategy if it does.
4. Retry only after changing an input, environment assumption, command, or hypothesis.
5. Expand from target → callers/dependencies → subsystem. Do not jump repo-wide unless the failure crosses boundaries.
6. Fix the requested bug even if it predates your edits, plus regressions you introduced. Report unrelated failures and unresolved uncertainty without expanding scope.

When a required tool is absent, use an already-installed or standard-library equivalent. If none exists, perform static validation and give the exact smoke-test command; never claim it ran.

Ask the user only when proceeding requires a consequential choice, new authority, or unavailable external information. State the evidence already gathered and the smallest decision needed.
