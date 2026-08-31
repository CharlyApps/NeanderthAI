#!/usr/bin/env python3
"""Build, install, audit, and statically validate NeanderthAI."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skill-src" / "neanderthai"
DIST = ROOT / "dist"
TARGETS = {
    "codex": Path("codex/.agents/skills/neanderthai"),
    "claude": Path("claude/.claude/skills/neanderthai"),
    "copilot": Path("copilot/.github/skills/neanderthai"),
}
PROJECT_PATHS = {
    "codex": Path(".agents/skills/neanderthai"),
    "claude": Path(".claude/skills/neanderthai"),
    "copilot": Path(".github/skills/neanderthai"),
}
USER_PATHS = {
    "codex": Path(".agents/skills/neanderthai"),
    "claude": Path(".claude/skills/neanderthai"),
    "copilot": Path(".copilot/skills/neanderthai"),
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"{path}: missing YAML frontmatter")
    block = text.split("\n---\n", 1)[0][4:]
    values: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        match = re.match(r"^([a-z][a-z0-9-]*):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            values[key] = value.strip(' "')
        elif key and line.startswith((" ", "\t")):
            values[key] = f"{values[key]} {line.strip()}".strip()
    return values


def files(path: Path) -> list[Path]:
    return sorted(p for p in path.rglob("*") if p.is_file())


def digest(path: Path) -> str:
    hashed = hashlib.sha256()
    for item in files(path):
        hashed.update(item.relative_to(path).as_posix().encode())
        hashed.update(item.read_bytes())
    return hashed.hexdigest()


def copy_exact(source: Path, target: Path) -> None:
    target = target.resolve()
    if DIST.resolve() not in target.parents:
        raise ValueError(f"refusing to replace non-dist path: {target}")
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)


def build() -> None:
    for relative in TARGETS.values():
        copy_exact(SOURCE, DIST / relative)
    print(f"built {len(TARGETS)} distributions from {SOURCE.relative_to(ROOT)}")


def validate_tree(path: Path) -> list[str]:
    errors: list[str] = []
    skill = path / "SKILL.md"
    if not skill.is_file():
        return [f"{path}: missing SKILL.md"]
    try:
        meta = frontmatter(skill)
    except ValueError as error:
        return [str(error)]
    if meta.get("name") != "neanderthai":
        errors.append(f"{skill}: name must be neanderthai")
    if not meta.get("description") or meta.get("description") in {">", "|"}:
        errors.append(f"{skill}: description is required")
    if len(meta.get("description", "")) > 1024:
        errors.append(f"{skill}: description exceeds 1024 characters")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", meta.get("name", "")):
        errors.append(f"{skill}: invalid portable skill name")
    text = skill.read_text(encoding="utf-8")
    for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if "://" not in link and not (path / link.split("#", 1)[0]).is_file():
            errors.append(f"{skill}: broken relative link {link}")
    for item in files(path):
        content = item.read_text(encoding="utf-8")
        if re.search(r"(?:/Users/|[A-Za-z]:\\\\Users\\\\)", content):
            errors.append(f"{item}: contains a user-specific absolute path")
        if "TODO" in content or "REPLACE_ME" in content:
            errors.append(f"{item}: contains unfinished placeholder")
    return errors


def validate() -> None:
    errors = validate_tree(SOURCE)
    source_hash = digest(SOURCE)
    for name, relative in TARGETS.items():
        target = DIST / relative
        errors.extend(validate_tree(target))
        if target.is_dir() and digest(target) != source_hash:
            errors.append(f"{name}: distribution differs from canonical source")
    if errors:
        raise SystemExit("validation failed:\n- " + "\n- ".join(errors))
    print(f"validated canonical source and {len(TARGETS)} identical distributions")


def approximate_tokens(path: Path) -> int:
    return math.ceil(len(path.read_text(encoding="utf-8")) / 4)


def audit(write: bool = False) -> str:
    ponytail = ROOT / "sources" / "ponytail-SKILL.md"
    caveman = ROOT / "sources" / "caveman-SKILL.md"
    core = SOURCE / "SKILL.md"
    refs = files(SOURCE / "references")
    source_counts = {p.stem.removesuffix("-SKILL"): approximate_tokens(p) for p in (ponytail, caveman)}
    core_count = approximate_tokens(core)
    ref_counts = {p.name: approximate_tokens(p) for p in refs}
    naive = sum(source_counts.values())
    typical = core_count + min(ref_counts.values(), default=0)
    worst = core_count + sum(ref_counts.values())
    reduction = (1 - core_count / naive) * 100
    report = f"""# Token audit

Counts use one documented approximation for every file: `ceil(UTF-8 text characters / 4)`. This is reproducible and tokenizer-independent, but not a billing-token claim.

| Runtime material | Approx. tokens |
|---|---:|
| Ponytail source | {source_counts['ponytail']} |
| Caveman source | {source_counts['caveman']} |
| Naive combined baseline | {naive} |
| NeanderthAI core | {core_count} |
| Typical invocation (core + one smallest relevant reference) | {typical} |
| Worst relevant invocation (core + all references) | {worst} |

Core reduction versus naive concatenation: **{reduction:.1f}%**.

Progressive disclosure moves explicit communication variants ({ref_counts.get('communication.md', 0)} tokens) and failure recovery ({ref_counts.get('recovery.md', 0)} tokens) out of the default path. Most direct tasks need only the core.
"""
    if write:
        target = ROOT / "docs" / "token-audit.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(report, encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")
    return report


def run_evals() -> None:
    cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
    required = {
        "ponytail-unique", "caveman-unique", "overlap", "conflict", "trivial",
        "deep", "context-heavy", "recovery", "ambiguous", "stop",
    }
    categories = {case.get("category") for case in cases}
    missing = required - categories
    fields = {"id", "category", "input", "expected_behavior", "source_behavior", "prohibited_regressions", "validation_criteria"}
    malformed = [case.get("id", "<unnamed>") for case in cases if fields - case.keys()]
    core = (SOURCE / "SKILL.md").read_text(encoding="utf-8").lower()
    invariants = [
        "search before reading", "root cause", "standard library", "native platform",
        "direct", "investigate", "deep", "stop when", "security", "accessibility",
        "stop ponytail", "stop caveman", "wenyan", "feedback 0", "neanderthal",
        "quote errors exactly",
    ]
    absent = [item for item in invariants if item not in core]
    if missing or malformed or absent:
        raise SystemExit(f"eval validation failed: missing={sorted(missing)} malformed={malformed} absent={absent}")
    print(f"validated {len(cases)} behavioral eval specifications and {len(invariants)} core invariants")


def install(agent: str, scope: str, target: Optional[Path]) -> None:
    base = target.resolve() if target else (Path.cwd() if scope == "project" else Path.home())
    relative = PROJECT_PATHS[agent] if scope == "project" else USER_PATHS[agent]
    destination = base / relative
    if destination.exists():
        raise SystemExit(f"refusing to overwrite existing skill: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, destination)
    print(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("build")
    commands.add_parser("validate")
    audit_parser = commands.add_parser("audit")
    audit_parser.add_argument("--write", action="store_true")
    commands.add_parser("eval")
    commands.add_parser("all")
    install_parser = commands.add_parser("install")
    install_parser.add_argument("agent", choices=TARGETS)
    install_parser.add_argument("--scope", choices=("project", "user"), default="project")
    install_parser.add_argument("--target", type=Path, help="base directory; defaults to cwd or home")
    args = parser.parse_args()
    if args.command == "build":
        build()
    elif args.command == "validate":
        validate()
    elif args.command == "audit":
        print(audit(args.write))
    elif args.command == "eval":
        run_evals()
    elif args.command == "install":
        install(args.agent, args.scope, args.target)
    else:
        build()
        validate()
        run_evals()
        print(audit(write=True))


if __name__ == "__main__":
    main()
