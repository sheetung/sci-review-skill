---
name: sci-review
description: Use when reviewing or revising SCI manuscripts section by section, with reviewer-style comments and concrete revision guidance for each part, including equations, notation, logic, experiments, and references.
---

# SCI Review

Use this skill when the user wants a reviewer-style pass on an SCI manuscript and expects usable revision guidance rather than only a high-level verdict. Review the manuscript in SCI writing order, and for each part give both the identified issues and a reasonable way to revise them. Keep the review criteria aligned with standard English SCI manuscript expectations, but present the output comments in Chinese unless the user explicitly asks for English.

## Workflow

1. Identify the manuscript source.
- Prefer the main `.tex` file.
- If there are multiple versions, inspect the one the user explicitly names.

2. Start with global issues.
- Check whether the research problem is clear.
- Check whether the claimed contribution matches the actual content.
- Check whether the manuscript is logically closed from problem statement to method, theory, and validation.
- Flag major technical or structural risks before local wording issues.

3. Then review in SCI writing order.
- Title, abstract, and keywords
- Introduction
- Problem formulation / preliminaries / assumptions
- Modeling section
- Method or controller design
- Stability / convergence / theoretical analysis
- Simulation or experimental validation
- Conclusion
- References

4. After the section review, run cross-cutting checks.
- Equations and formula presentation
- Notation consistency
- Figures and tables
- Language, tense, and paragraph structure

5. For each section, always provide both diagnosis and revision direction.
- Do not stop at "this part is weak."
- Say what is wrong, why it matters, and how it should be revised.
- Prefer practical revision guidance such as reordering, merging, clarifying, defining, tightening claims, or rewriting specific sentence types.
- If the issue is local, give a local fix.
- If the issue is structural, give a structural fix.

## Section Checks

### Title, Abstract, and Keywords

- Check whether the title matches the actual technical contribution and scope.
- Check whether the abstract follows a compact SCI structure: problem, method, theory, validation.
- Check whether keywords are precise and aligned with the main terminology.
- When commenting, suggest whether to tighten the title, rebalance the abstract, or replace vague keywords.

### Introduction

- Check whether the introduction progresses from background to challenge, literature limitations, and then the present solution.
- Check whether the literature is synthesized around problems rather than listed mechanically.
- Check whether concrete gaps are identified.
- Check whether the paper clearly explains why the proposed work addresses those gaps.
- Flag disconnected references, abrupt topic jumps, weak contribution statements, and unnecessary one-sentence paragraphs.
- When commenting, suggest whether to merge paragraphs, regroup citations, sharpen the gap statement, or rewrite the contribution transition.

### Problem Formulation / Preliminaries / Assumptions

- Check whether assumptions are explicit, necessary, and later used.
- Check whether symbols, dimensions, sets, and operators are defined before use.
- Check whether the mathematical objective is complete and consistent.
- When commenting, suggest whether to add definitions, move assumptions forward, or restate the control objective more formally.

### Modeling Section

- Check whether the model is physically and mathematically consistent.
- Check whether simplifications and coordinate definitions are justified.
- Check whether the model used for analysis matches the model used later for control and validation.
- When commenting, suggest whether to clarify modeling assumptions, explain simplifications, or explicitly bridge different model levels.

### Method or Controller Design

- Check whether each design step is motivated rather than dropped in as an isolated formula.
- Check whether each gain, surface, virtual input, or auxiliary variable has a clear role.
- Check whether there are hidden jumps or undefined substitutions.
- When commenting, suggest whether to add derivation transitions, explain parameter choices, or split overloaded paragraphs.

### Stability / Convergence / Theoretical Analysis

- Check whether theorem statements match what is actually proved.
- Check whether each proof step follows correctly from the previous one.
- Check whether assumptions and bounds used in the proof have already been stated.
- When commenting, suggest whether to weaken claims, strengthen intermediate lemmas, add missing conditions, or separate local from global results.

### Simulation or Experimental Validation

- Check whether the validation setup matches the claimed contribution.
- Check whether comparisons are fair and sufficiently informative.
- Check whether the discussion interprets the results instead of repeating numbers.
- Check whether "experiment" is truly experiment rather than simulation.
- When commenting, suggest whether to rename sections, add baseline rationale, add missing metrics, or rewrite result discussion around evidence.

### Conclusion

- Check whether the conclusion is compact and supported by the paper.
- Check whether it overclaims or introduces new content.
- When commenting, suggest whether to trim repeated material, soften unsupported claims, or align the conclusion with the actual findings.

### References

- Check whether references are complete, current, and consistently formatted.
- Check whether key claims are supported by the cited literature.
- When commenting, suggest whether to add recent references, complete missing bibliographic fields, or replace weak citations.

## Cross-Cutting Checks

### Equations and Formula Presentation

- Check whether displayed equations have correct and consistent numbering.
- Check whether displayed equations use sentence-level punctuation when they end a sentence or clause.
- If an equation is immediately followed by `where`, `with`, `subject to`, or a similar connector, do not require punctuation after the equation.
- Check whether equations are grammatically integrated into the surrounding sentence.
- Check whether equation references in the main text are made through labels such as `\eqref{...}` or `(\ref{...})` rather than hard-coded equation numbers.
- When commenting, explicitly classify the issue as numbering, punctuation, sentence integration, notation, or analytical validity.
- When suggesting revisions, say whether the fix is to renumber, add or remove punctuation, replace hard-coded numbers with label references, rewrite the lead-in sentence, define symbols, or repair the derivation.

### Notation Consistency

- Check whether the same symbol is reused with multiple meanings.
- Check whether time arguments such as `(t)` are used consistently.
- Check whether notation is aligned across text, equations, tables, and figures.
- When commenting, suggest whether to unify a symbol, add a symbol table, or remove redundant repeated definitions.

### Figures and Tables

- Check whether numbering, captions, and in-text references are consistent.
- Check whether captions are concise and descriptive.
- Check whether figures and tables support the argument rather than duplicate the text.
- Check whether figure and table references in the main text use labels such as `Fig.~\ref{...}` and `Table~\ref{...}` rather than hard-coded numbers.
- When commenting, suggest whether to tighten captions, rename metrics, replace hard-coded numbers with label references, or rewrite the surrounding discussion.

### Language and Structure

- Check terminology consistency, tense consistency, and section-heading parallelism.
- Flag abrupt paragraphing, especially unnecessary one-sentence paragraphs.
- Prefer neutral scientific wording over colloquial transitions.
- Flag subjective or weakly justified wording such as `favorable`, `arbitrary`, and similar terms when they are used without precise technical support.
- Prefer rigorous scientific wording over evaluative or casual wording.
- When commenting, suggest whether to merge paragraphs, replace colloquial phrases, or standardize tense and terminology.

## Review Style

- Use a reviewer mindset: identify logical gaps, weak assumptions, formatting inconsistencies, unsupported claims, and writing problems.
- Start with the largest technical or structural risks before local language polish.
- Treat equations, theorem-level claims, references, and figure/table captions as high-sensitivity areas.
- Prefer section-aware comments that follow SCI writing order.
- If the user asks to update the manuscript, make the smallest change that resolves the issue cleanly.

## When to Load References

Read `references/checklist.md` when:
- performing a full-manuscript SCI writing review
- building a reusable review checklist for another paper
- checking whether an issue is a general SCI writing problem or only a project-specific preference

## Output Expectations

- Do not respond with only a global summary.
- Review section by section.
- Keep the review logic and standards aligned with normal English SCI review expectations.
- Output the review comments in Chinese by default.
- Use Markdown for the review output.
- Prefer short section headers, short paragraphs, and flat bullet lists.
- Avoid producing one long wall of text.
- Group comments into visually clear sections so the user can scan them quickly.
- For each reviewed part, provide:
  - what is good enough, if relevant
  - what is wrong or weak
  - why it is a problem
  - how to revise it reasonably
- Prefer a Markdown structure with short Chinese section headings for:
  - overall issues
  - title / abstract / keywords
  - introduction
  - problem formulation / assumptions
  - modeling
  - method design
  - stability analysis
  - validation
  - conclusion
  - equations and notation
  - references
- Within each section, prefer short Chinese bullet labels meaning:
  - current assessment
  - problems found
  - why it matters
  - suggested revision
- For small wording questions, provide the corrected sentence directly.
- For equation-related comments, explicitly state whether the issue is numbering, punctuation, sentence integration, notation, or analytical validity.
- For figure, table, and equation references, explicitly flag hard-coded numbering in the main text and recommend label-based referencing.
- Keep the final overall summary brief; the main value should be in the section-level comments and revision directions.
