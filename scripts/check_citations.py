#!/usr/bin/env python3
"""Check citation keys in a LaTeX manuscript against BibTeX databases."""

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


CITE_CMD_RE = re.compile(
    r"\\(?:cite|autocite|citenum|citep|citet|citealp|citeauthor|citeyear|citeyearpar)\*?\{([^}]+)\}"
)
BIB_RE = re.compile(r"\\bibliography\{([^}]+)\}")
ADD_BIB_RE = re.compile(r"\\addbibresource(?:\[[^\]]*\])?\{([^}]+)\}")
BIB_ENTRY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")
BEGIN_THEBIB_RE = re.compile(r"\\begin\{thebibliography\}")
END_THEBIB_RE = re.compile(r"\\end\{thebibliography\}")
BibITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")


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


def resolve_bib_path(base_dir: Path, token: str) -> Path:
    token = token.strip()
    candidate = base_dir / token
    if candidate.suffix.lower() != ".bib":
        candidate = candidate.with_suffix(".bib")
    return candidate


def parse_tex(tex_path: Path) -> tuple[list[Finding], dict[str, int], list[Path], dict[str, int]]:
    findings: list[Finding] = []
    citation_lines: dict[str, int] = {}
    bib_paths: list[Path] = []
    inline_bibitems: dict[str, int] = {}
    in_thebibliography = False

    lines = tex_path.read_text(encoding="utf-8").splitlines()
    for idx, raw in enumerate(lines, start=1):
        text = strip_comments(raw)

        if BEGIN_THEBIB_RE.search(text):
            in_thebibliography = True
        if in_thebibliography:
            for match in BibITEM_RE.finditer(text):
                key = match.group(1).strip()
                if key in inline_bibitems:
                    findings.append(Finding("duplicate-bibitem-key", idx, f"Duplicate \\bibitem key `{key}` in the TeX source."))
                else:
                    inline_bibitems[key] = idx
        if END_THEBIB_RE.search(text):
            in_thebibliography = False

        for match in CITE_CMD_RE.finditer(text):
            payload = match.group(1)
            for key in [part.strip() for part in payload.split(",") if part.strip()]:
                if re.fullmatch(r"#\d+", key):
                    continue
                citation_lines.setdefault(key, idx)

        for match in BIB_RE.finditer(text):
            for item in [part.strip() for part in match.group(1).split(",") if part.strip()]:
                bib_paths.append(resolve_bib_path(tex_path.parent, item))

        for match in ADD_BIB_RE.finditer(text):
            bib_paths.append(resolve_bib_path(tex_path.parent, match.group(1).strip()))

    if not bib_paths and not inline_bibitems:
        findings.append(Finding("missing-bibliography-command", 0, "No bibliography command or `thebibliography` environment was found in the TeX source."))

    unique_paths: list[Path] = []
    seen: set[Path] = set()
    for path in bib_paths:
        if path not in seen:
            seen.add(path)
            unique_paths.append(path)

    return findings, citation_lines, unique_paths, inline_bibitems


def parse_bib_files(paths: list[Path]) -> tuple[list[Finding], dict[str, int]]:
    findings: list[Finding] = []
    entries: dict[str, int] = {}

    for path in paths:
        if not path.is_file():
            findings.append(Finding("missing-bib-file", 0, f"Bibliography file not found: `{path}`."))
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for idx, raw in enumerate(lines, start=1):
            text = strip_comments(raw)
            match = BIB_ENTRY_RE.search(text)
            if not match:
                continue
            key = match.group(1).strip()
            if key in entries:
                findings.append(Finding("duplicate-bib-key", idx, f"Duplicate BibTeX key `{key}` found in `{path.name}`."))
            else:
                entries[key] = idx
    return findings, entries


def compare_citations(citations: dict[str, int], entries: dict[str, int]) -> list[Finding]:
    findings: list[Finding] = []

    for key, line in sorted(citations.items(), key=lambda item: item[1]):
        if key not in entries:
            findings.append(Finding("undefined-citation-key", line, f"Citation key `{key}` is cited but not found in the loaded `.bib` files."))

    for key in sorted(entries):
        if key not in citations:
            findings.append(Finding("unused-bib-entry", 0, f"BibTeX entry `{key}` is not cited in the TeX source."))

    return findings


def render(findings: list[Finding]) -> str:
    if not findings:
        return "No citation or bibliography issues detected."
    ordered = sorted(findings, key=lambda item: (item.line == 0, item.line, item.code, item.message))
    lines = []
    for item in ordered:
        location = f"line {item.line}" if item.line else "global"
        lines.append(f"- [{item.code}] {location}: {item.message}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_file", help="Path to the LaTeX source file to inspect.")
    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.is_file():
        print(f"File not found: {tex_path}", file=sys.stderr)
        return 2

    findings, citations, bib_paths, inline_bibitems = parse_tex(tex_path)
    bib_findings, bib_entries = parse_bib_files(bib_paths)
    findings.extend(bib_findings)
    merged_entries = dict(bib_entries)
    for key, line in inline_bibitems.items():
        if key in merged_entries:
            findings.append(Finding("duplicate-citation-source", line, f"Citation key `{key}` exists both in inline bibliography and in a loaded `.bib` source."))
        else:
            merged_entries[key] = line
    findings.extend(compare_citations(citations, merged_entries))
    print(render(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
