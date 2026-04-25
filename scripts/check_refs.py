#!/usr/bin/env python3
"""Check label-based references and numbering issues in LaTeX manuscripts."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Finding:
    code: str
    line: int
    message: str


@dataclass
class LabeledObject:
    kind: str
    label: str
    line: int


LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_CMD_RE = re.compile(r"\\(?:eqref|ref|pageref|autoref|nameref|cref|Cref|vref|Vref)\{([^}]+)\}")

HARDCODED_PATTERNS = [
    (
        "hardcoded-figure-ref",
        re.compile(r"\b(?:Fig\.|Figure)\s*~?\s*(\d+|[IVX]+)(?:\([a-z]\))?\b"),
        "Hard-coded figure number; prefer a label-based reference such as Fig.~\\ref{...}.",
    ),
    (
        "hardcoded-table-ref",
        re.compile(r"\b(?:Table)\s*~?\s*(\d+|[IVX]+)(?:\([a-z]\))?\b"),
        "Hard-coded table number; prefer a label-based reference such as Table~\\ref{...}.",
    ),
    (
        "hardcoded-equation-ref",
        re.compile(r"\b(?:Eq\.|Equation)\s*~?\s*\((\d+|[IVX]+)\)"),
        "Hard-coded equation number; prefer \\eqref{...} or (\\ref{...}).",
    ),
    (
        "hardcoded-section-ref",
        re.compile(r"\bSection\s+(?:~?\s*)?(\d+|[IVX]+(?:\.\d+)?)\b"),
        "Hard-coded section number; prefer a label-based section reference.",
    ),
]

ENV_WITH_LABEL = ("figure", "table", "equation")
BEGIN_ENV_RE = re.compile(r"\\begin\{([a-zA-Z*]+)\}")
END_ENV_RE = re.compile(r"\\end\{([a-zA-Z*]+)\}")
CAPTIONOF_RE = re.compile(r"\\captionof\{(figure|table)\}")
LOW_SIGNAL_UNUSED_PREFIXES = (
    "eq:",
    "sec:",
    "subsec:",
    "subsubsec:",
    "rem:",
    "lem:",
    "thm:",
    "prop:",
    "cor:",
)


def strip_comments(line: str) -> str:
    escaped = False
    result = []
    for ch in line:
        if ch == "%" and not escaped:
            break
        result.append(ch)
        escaped = ch == "\\" and not escaped
        if ch != "\\":
            escaped = False
    return "".join(result)


def extract_block(lines: list[str], start: int, env: str) -> tuple[str, int]:
    parts = [lines[start]]
    for idx in range(start + 1, len(lines)):
        parts.append(lines[idx])
        if END_ENV_RE.search(lines[idx]) and END_ENV_RE.search(lines[idx]).group(1) == env:
            return "\n".join(parts), idx
    return "\n".join(parts), len(lines) - 1


def collect_labeled_objects(lines: list[str]) -> list[LabeledObject]:
    objects: list[LabeledObject] = []
    idx = 0

    while idx < len(lines):
        text = strip_comments(lines[idx])
        begin = BEGIN_ENV_RE.search(text)
        if begin:
            env = begin.group(1)
            base_env = env.rstrip("*")
            if base_env in ("figure", "table"):
                block, end_idx = extract_block(lines, idx, env)
                for label in LABEL_RE.findall(block):
                    objects.append(LabeledObject(base_env, label, idx + 1))
                idx = end_idx + 1
                continue

        caption_match = CAPTIONOF_RE.search(text)
        if caption_match:
            kind = caption_match.group(1)
            search_end = min(len(lines), idx + 8)
            nearby = "\n".join(strip_comments(lines[pos]) for pos in range(idx, search_end))
            for label in LABEL_RE.findall(nearby):
                objects.append(LabeledObject(kind, label, idx + 1))

        idx += 1

    deduped: dict[str, LabeledObject] = {}
    for item in objects:
        deduped.setdefault(item.label, item)
    return list(deduped.values())


def check_labels(lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    labels: dict[str, int] = {}
    refs: set[str] = set()
    labeled_objects = {item.label: item for item in collect_labeled_objects(lines)}

    for idx, line in enumerate(lines, start=1):
        text = strip_comments(line)
        for label in LABEL_RE.findall(text):
            if label in labels:
                findings.append(Finding("duplicate-label", idx, f"Duplicate label `{label}`."))
            else:
                labels[label] = idx
        for payload in REF_CMD_RE.findall(text):
            for ref in [part.strip() for part in payload.split(",") if part.strip()]:
                refs.add(ref)

    for ref in sorted(refs):
        if ref not in labels:
            findings.append(Finding("undefined-ref", 0, f"Undefined label reference `{ref}`."))

    for label, line_no in sorted(labels.items(), key=lambda item: item[1]):
        if label in labeled_objects:
            continue
        if label not in refs and not label.startswith(LOW_SIGNAL_UNUSED_PREFIXES):
            findings.append(Finding("unused-label", line_no, f"Label `{label}` is never referenced."))

    return findings


def check_float_references(lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    refs: set[str] = set()

    for raw in lines:
        text = strip_comments(raw)
        for payload in REF_CMD_RE.findall(text):
            for ref in [part.strip() for part in payload.split(",") if part.strip()]:
                refs.add(ref)

    for item in sorted(collect_labeled_objects(lines), key=lambda obj: obj.line):
        if item.label in refs:
            continue
        findings.append(
            Finding(
                f"unreferenced-{item.kind}",
                item.line,
                f"This {item.kind} is displayed but not cited in the main text through its label `{item.label}`.",
            )
        )

    return findings


def check_hardcoded_refs(lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for idx, line in enumerate(lines, start=1):
        text = strip_comments(line)
        for code, pattern, message in HARDCODED_PATTERNS:
            for match in pattern.finditer(text):
                token = match.group(0)
                if "\\ref{" in token or "\\eqref{" in token:
                    continue
                findings.append(Finding(code, idx, message))
    return findings


def check_env_labels(lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    idx = 0
    while idx < len(lines):
        text = strip_comments(lines[idx])
        match = BEGIN_ENV_RE.search(text)
        if not match:
            idx += 1
            continue
        env = match.group(1)
        base_env = env.rstrip("*")
        if base_env not in ENV_WITH_LABEL:
            idx += 1
            continue
        block, end_idx = extract_block(lines, idx, env)
        if "\\nonumber" in block or "\\notag" in block:
            idx = end_idx + 1
            continue
        if not LABEL_RE.search(block):
            findings.append(
                Finding(
                    f"missing-{base_env}-label",
                    idx + 1,
                    f"{base_env.capitalize()} environment appears without a \\label{{...}}.",
                )
            )
        idx = end_idx + 1
    return findings


def render(findings: list[Finding]) -> str:
    if not findings:
        return "No reference or label issues detected."
    parts = []
    for item in sorted(findings, key=lambda f: (f.line == 0, f.line, f.code)):
        location = f"line {item.line}" if item.line else "global"
        parts.append(f"- [{item.code}] {location}: {item.message}")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_file", help="Path to the LaTeX source file to inspect.")
    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.is_file():
        print(f"File not found: {tex_path}", file=sys.stderr)
        return 2

    lines = tex_path.read_text(encoding="utf-8").splitlines()
    findings = []
    findings.extend(check_labels(lines))
    findings.extend(check_float_references(lines))
    findings.extend(check_hardcoded_refs(lines))
    findings.extend(check_env_labels(lines))
    print(render(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
