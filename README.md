# sci-review skill

`sci-review` is a reusable skill for reviewer-style SCI manuscript review.
It follows standard English SCI review expectations while outputting comments in Chinese by default.

## What it does

- reviews manuscripts section by section instead of only giving a global verdict
- checks equations, notation, figures, tables, references, and writing rigor
- flags hard-coded figure, table, equation, and section numbers
- prefers label-based LaTeX references such as `\ref{...}` and `\eqref{...}`
- detects weak academic wording such as subjective or loosely justified expressions
- supports both external `.bib` files and inline `thebibliography` / `\bibitem` references

## Repository layout

```text
.
|-- CHANGELOG.md
|-- LICENSE
|-- README.md
|-- SKILL.md
|-- agents
|   `-- openai.yaml
|-- references
|   `-- checklist.md
`-- scripts
    |-- check_citations.py
    |-- check_refs.py
    |-- check_tex_structure.py
    `-- check_wording.py
```

## Use in Codex

Codex discovers skills from `~/.codex/skills/<name>/SKILL.md`.

### Option 1: clone directly into your skills directory

```powershell
git clone https://github.com/sheetung/sci-review-skill.git $HOME\.codex\skills\sci-review
```

### Option 2: clone elsewhere and copy the skill folder

```powershell
git clone https://github.com/sheetung/sci-review-skill.git $HOME\sci-review-skill
Copy-Item -Recurse $HOME\sci-review-skill $HOME\.codex\skills\sci-review
```

Then restart Codex if needed and invoke it in a prompt such as:

```text
$sci-review review this SCI manuscript
```

## Use in OpenCode

OpenCode can discover skills from locations such as:

- project local: `.opencode/skills/<name>/SKILL.md`
- global: `~/.config/opencode/skills/<name>/SKILL.md`
- compatible paths: `.claude/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md`

### Option 1: project-local install

```powershell
git clone https://github.com/sheetung/sci-review-skill.git $HOME\sci-review-skill
New-Item -ItemType Directory -Force .opencode\skills | Out-Null
Copy-Item -Recurse $HOME\sci-review-skill .opencode\skills\sci-review
```

### Option 2: global install

```powershell
git clone https://github.com/sheetung/sci-review-skill.git $HOME\sci-review-skill
New-Item -ItemType Directory -Force $HOME\.config\opencode\skills | Out-Null
Copy-Item -Recurse $HOME\sci-review-skill $HOME\.config\opencode\skills\sci-review
```

Then restart OpenCode if needed and ask the agent to use `sci-review`.

## Script-assisted checks

When Python is available, the skill can use bundled helper scripts before manual review:

- `scripts/check_refs.py`
- `scripts/check_wording.py`
- `scripts/check_tex_structure.py`
- `scripts/check_citations.py`

These scripts are meant to improve precision for deterministic issues such as:

- missing or duplicate labels
- hard-coded references
- weak wording
- template leftovers
- citation-key mismatches
- unused bibliography entries

## Maintenance files

- `CHANGELOG.md`: update history for the skill repository
- `LICENSE`: MIT open-source license

## License

This repository is released under the MIT License.
