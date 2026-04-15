# SCI Writing Review Checklist for Control Papers

This note summarizes a reusable SCI review checklist for control, robotics, and nonlinear systems papers. Use it in reviewer order: global issues first, then section-by-section review, then cross-cutting formatting and writing checks. Keep the review criteria aligned with normal English SCI manuscript standards, but the final review comments can be presented in Chinese. For each part, do not only identify the problem; also state a reasonable revision direction.

When available, deterministic helper scripts can be used before manual review:

- `scripts/check_refs.py` for label/reference checks
- `scripts/check_wording.py` for subjective wording checks
- `scripts/check_tex_structure.py` for template and paragraph-structure checks
- `scripts/check_citations.py` for citation-key consistency checks across `.bib` files and inline `thebibliography` / `\bibitem` entries

## 1. Global Issues

- Is the research problem clear and technically meaningful?
- Do the claimed contributions match what the paper actually delivers?
- Is the manuscript logically closed from problem statement to method, theory, and validation?
- Are there any signs of overclaiming, unsupported novelty, or section-level mismatch?
- If a global issue exists, suggest how to repair the paper structure or claim scope.

## 2. Title, Abstract, and Keywords

- Does the title match the real scope and contribution level?
- Does the abstract cover problem, method, theory, and validation in a compact SCI style?
- Are keywords technically precise and consistent with the paper terminology?
- If weak, suggest whether to tighten the title, rebalance the abstract, or replace vague keywords.

## 3. Introduction

- Does the introduction progress from broad background to core challenge, literature limitations, and then the present solution?
- Are references grouped by problem or method class instead of being listed mechanically?
- Does the literature review identify concrete shortcomings in existing studies?
- Does the manuscript clearly state what gap remains?
- Does the proposed work appear as a targeted response to those gaps?
- Are there unnecessary one-sentence paragraphs or abrupt topic jumps?
- If weak, suggest whether to merge paragraphs, regroup citations, strengthen the gap statement, or rewrite the contribution transition.

## 4. Problem Formulation / Preliminaries / Assumptions

- Are all assumptions explicit and later used in the analysis?
- Are symbols, dimensions, operators, sets, and norms defined before use?
- Is the control or optimization objective mathematically complete?
- Are theorem conditions and feasibility conditions stated at the right level?
- If weak, suggest whether to add definitions, move assumptions, or formalize the objective statement.

## 5. Modeling Section

- Is the model physically and mathematically consistent?
- Are simplifications, coordinate definitions, and parameter meanings sufficiently explained?
- Is the model used for control design consistent with the model used in validation?
- If different model levels coexist, is their relationship clearly explained?
- If weak, suggest whether to justify simplifications, bridge model levels, or clarify variable meanings.

## 6. Method or Controller Design

- Is each design step motivated instead of being introduced as a disconnected formula?
- Does every variable, gain, surface, observer, or transformation have a clear role?
- Are there hidden algebraic jumps or undefined substitutions?
- Are parameter choices or tuning rules explained well enough?
- If weak, suggest whether to add derivation transitions, define variables earlier, or split dense paragraphs.

## 7. Stability, Convergence, or Theoretical Analysis

- Do theorem statements match what is actually proved?
- Does each proof step follow correctly?
- Are required assumptions and bounds already stated?
- Are local, global, asymptotic, finite-time, and practical results distinguished clearly?
- If weak, suggest whether to weaken the claim, add missing lemmas, add missing assumptions, or separate proof stages more clearly.

## 8. Simulation or Experimental Validation

- Does the validation setup actually test the claimed contribution?
- Are comparison baselines appropriate and fairly configured?
- Does the text interpret figures and tables rather than merely repeat numbers?
- Is "experimental" evidence truly experimental rather than only simulation?
- If weak, suggest whether to rename the section, add baseline rationale, add metrics, or rewrite the result discussion.

## 9. Conclusion

- Is the conclusion concise and technically grounded?
- Does it summarize what was achieved without repeating the abstract line by line?
- Are there overclaims, unsupported takeaways, or new technical statements?
- If weak, suggest whether to trim repetition, soften claims, or align the conclusion with the actual evidence.

## 10. References

- Are entries complete, retrievable, and consistently formatted?
- Are key recent papers included where necessary?
- Do cited references genuinely support nearby claims?
- Are citation keys consistent with the actual bibliography source, whether it is an external `.bib` file or inline `thebibliography` entries in the `.tex` source?
- If author number is greater than 3, use `et al.` where required by style.
- If weak, suggest whether to add recent literature, complete missing fields, or replace weak citations.

## 11. Equations and Formula Presentation

- Check that displayed equations have correct numbering and that numbering is sequential and cross-referenced consistently.
- If a displayed equation ends a sentence or an independent clause, add the required punctuation mark after the equation.
- If a displayed equation is followed immediately by `where`, `with`, `subject to`, or a similar connector that continues the sentence, do not add punctuation after the equation.
- Make sure the sentence remains grammatically complete across the text before and after the equation.
- Check whether displayed equations are introduced and interpreted smoothly rather than dropped into the text without transition.
- Check whether equation references in the main text use label-based references such as `\eqref{...}` or `(\ref{...})` instead of hard-coded numbers.
- If weak, say whether the fix is to renumber, add or remove punctuation, replace hard-coded equation numbers with label references, define symbols, rewrite the lead-in sentence, or repair the derivation.

## 12. Notation and Definitions

- Use one primary term for the main system, method, or object throughout the paper.
- Avoid switching among near-synonyms for the same concept.
- Check whether the same symbol is reused for different meanings.
- Be consistent with time-varying notation such as `(t)`.
- If a symbol table exists, avoid repeating a full symbol-by-symbol explanation immediately afterward.
- If weak, suggest whether to unify symbols, add a notation table, or remove redundant explanations.

## 13. Mathematical Writing

- Avoid colloquial transitions such as `we can get`, `it is easy to see`, `obviously`, and `in order to make`.
- Prefer formal phrasing such as `yields`, `it follows that`, `it can be deduced that`, `to ensure`, and `to facilitate`.
- Prefer `Taking the time derivative of ... yields` over overly abrupt transitions when readability matters.
- Check that derivation text explains purpose, not only algebra.
- If weak, suggest whether to rewrite transitions, explain motivation, or shorten overloaded derivation sentences.

## 14. Figures and Tables

- Are figure and table numbers, captions, and in-text references complete and consistent?
- Are captions concise and descriptive?
- Do figures and tables summarize evidence instead of duplicating nearby text?
- Are table metric names short, accurate, and statistically correct?
- Check whether figure and table references in the main text use labels such as `Fig.~\ref{...}` and `Table~\ref{...}` instead of hard-coded numbers.
- If weak, suggest whether to tighten captions, rename metrics, replace hard-coded numbers with label references, or rewrite the discussion around the visuals.

## 15. Language and Structure

- Is the tense mainly simple present in the main body?
- Are section headings grammatically parallel?
- Are paragraphs generally multi-sentence and well developed?
- Are there abrupt one-sentence paragraphs that should be merged or expanded?
- Is the wording neutral, scientific, and free of avoidable colloquial phrasing?
- Are subjective or weakly justified words such as `favorable`, `arbitrary`, and similar expressions avoided unless they are precisely defined or technically supported?
- If weak, suggest whether to merge paragraphs, standardize tense, or replace colloquial wording.

## 16. Final Submission Sanity Check

- No references in the conclusion unless the journal explicitly allows it.
- Remove metadata placeholders before submission.
- Recheck figure, table, theorem, and equation numbering after float adjustments.
- Recheck labels, cross-references, and citation commands after major edits.
- Recheck that all cited keys exist in the active bibliography source, including inline `\bibitem` entries if no `.bib` file is used.

## 17. Minimal Self-Review Questions

Before submission, ask:

- Is the main contribution clear and honestly stated?
- Is the logic closed from problem statement to validation?
- Does each section do the job expected in an SCI paper?
- Are equation numbering and punctuation correct?
- Are figure, table, and equation references label-based rather than hard-coded?
- Are notation, figures, tables, and references consistent?
- Does each major comment have a corresponding revision path?
