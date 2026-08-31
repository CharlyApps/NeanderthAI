# Evidence-based recovery

Read only after a command fails, required evidence is unavailable, or observed failures may be unrelated.

1. Keep the command, exit status, and shortest output span that identifies the failure.
2. Classify it:
   - **introduced:** the change touches the failing path or the failure disappears when tested against the prior behavior;
   - **pre-existing:** reproducible without the change or documented by the existing baseline;
   - **uncertain:** evidence does not yet distinguish them.
3. Decide whether the signal disproves the current hypothesis. Change strategy if it does.
4. Retry only after changing an input, environment assumption, command, or hypothesis.
5. Expand from target → callers/dependencies → subsystem. Do not jump repo-wide unless the failure crosses boundaries.
6. Fix only introduced, in-scope failures. Report pre-existing or uncertain failures without casually repairing them.

When a required tool is absent, use an already-installed or standard-library equivalent. If none exists, perform static validation and give the exact smoke-test command; never claim it ran.

Ask the user only when proceeding requires a consequential choice, new authority, or unavailable external information. State the evidence already gathered and the smallest decision needed.
