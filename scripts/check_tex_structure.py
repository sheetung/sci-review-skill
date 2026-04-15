#!/usr/bin/env python3
"""Check LaTeX structure issues that are easy to detect heuristically."""

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


TEMPLATE_RULES = [
    ("template-article-type", re.compile(r"\\articletype\{Article Type\}"), "Template placeholder `Article Type` is still present."),
    ("template-old-date", re.compile(r"\\received\{26 April 2016\}|\\revised\{6 June 2016\}|\\accepted\{6 June 2016\}"), "Template example dates are still present."),
    ("template-biography", re.compile(r"Author Name\. This is sample author biography text"), "Template biography text is still present."),
]

HARDCODED_SECTION_RE = re.compile(r"\bSection\s+(?:III|IV|V|VI|VII|VIII|IX|X|\d+(?:\.\d+)?)\b")
BEGIN_ENV_RE = re.compile(r"\\begin\{([a-zA-Z*]+)\}")
END_ENV_RE = re.compile(r"\\end\{([a-zA-Z*]+)\}")
COMMAND_ONLY_RE = re.compile(r"^\s*\\")


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


def count_sentences(text: str) -> int:
    matches = re.findall(r"[.!?](?:\s|$)", text)
    return len(matches)


def check_template_findings(lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for idx, raw in enumerate(lines, start=1):
        text = strip_comments(raw)
        for code, pattern, message in TEMPLATE_RULES:
            if pattern.search(text):
                findings.append(Finding(code, idx, message))
        if HARDCODED_SECTION_RE.search(text) and "\\ref{" not in text:
            findings.append(Finding("hardcoded-section-ref", idx, "Hard-coded section reference; prefer `Section~\\ref{...}`."))
    return findings


def check_single_sentence_paragraphs(lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    env_stack: list[str] = []
    current: list[tuple[int, str]] = []

    def flush_paragraph() -> None:
        nonlocal current
        if not current:
            return
        joined = " ".join(part for _, part in current).strip()
        if joined and count_sentences(joined) == 1 and len(joined) > 80:
            findings.append(
                Finding(
                    "single-sentence-paragraph",
                    current[0][0],
                    "Possible single-sentence paragraph; review whether it should be merged or expanded.",
                )
            )
        current = []

    for idx, raw in enumerate(lines, start=1):
        text = strip_comments(raw).strip()
        begin = BEGIN_ENV_RE.search(text)
        end = END_ENV_RE.search(text)
        if begin:
            env_stack.append(begin.group(1))
            flush_paragraph()
        if end and env_stack:
            env_stack.pop()
            flush_paragraph()
            continue
        if env_stack:
            continue
        if not text:
            flush_paragraph()
            continue
        if COMMAND_ONLY_RE.match(text):
            flush_paragraph()
            continue
        current.append((idx, text))

    flush_paragraph()
    return findings


def render(findings: list[Finding]) -> str:
    if not findings:
        return "No structural issues detected by the configured heuristics."
    return "\n".join(f"- [{item.code}] line {item.line}: {item.message}" for item in findings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_file", help="Path to the LaTeX source file to inspect.")
    args = parser.parse_args()

    path = Path(args.tex_file)
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    lines = path.read_text(encoding="utf-8").splitlines()
    findings = []
    findings.extend(check_template_findings(lines))
    findings.extend(check_single_sentence_paragraphs(lines))
    print(render(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
