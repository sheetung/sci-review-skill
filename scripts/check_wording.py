#!/usr/bin/env python3
"""Scan LaTeX manuscripts for subjective or weakly justified wording."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Rule:
    name: str
    pattern: re.Pattern[str]
    note: str


RULES = [
    Rule(
        "subjective-favorable",
        re.compile(r"\bfavorable\b", re.IGNORECASE),
        "Subjective wording; prefer a measurable claim or a neutral technical description.",
    ),
    Rule(
        "subjective-arbitrary",
        re.compile(r"\barbitrary\b", re.IGNORECASE),
        "Potentially loose wording; use a mathematically precise description unless arbitrariness is essential.",
    ),
    Rule(
        "subjective-obviously",
        re.compile(r"\bobviously\b", re.IGNORECASE),
        "Avoid assuming the reader sees a step as obvious; explain or justify it instead.",
    ),
    Rule(
        "subjective-clearly",
        re.compile(r"\bclearly\b", re.IGNORECASE),
        "Prefer evidence-based wording over `clearly` unless the statement is directly shown.",
    ),
    Rule(
        "subjective-easy-to-see",
        re.compile(r"\bit is easy to see\b", re.IGNORECASE),
        "This phrase is often too informal for rigorous SCI writing; replace it with a justification.",
    ),
    Rule(
        "subjective-good-bad",
        re.compile(r"\b(?:good|bad|excellent)\b", re.IGNORECASE),
        "Use precise technical evaluation instead of informal qualitative wording.",
    ),
]


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


def render_matches(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[str] = []
    for idx, raw in enumerate(lines, start=1):
        text = strip_comments(raw)
        for rule in RULES:
            if rule.pattern.search(text):
                findings.append(f"- [{rule.name}] line {idx}: {rule.note}")
    if not findings:
        return "No wording issues detected by the configured scan list."
    return "\n".join(findings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_file", help="Path to the LaTeX source file to inspect.")
    args = parser.parse_args()

    path = Path(args.tex_file)
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    print(render_matches(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
