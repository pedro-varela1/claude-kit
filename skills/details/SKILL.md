---
name: details
description: 'Create or update details/, the paper-style theory snapshot of a project (LaTeX compiled to details/details.pdf in the house Technical style). Use when a project is created, or when its model, method, theory, results or limitations change. Never edits details/ before Pedro approves a written change plan, in any permission mode.'
---

# /details

`details/details.pdf` explains what the repository computes and why, the way a short paper would. It
is a snapshot: it reads as if the current design had always been the design.

## What belongs

- The problem: inputs, outputs, assumptions, what a good answer is.
- The method at the level of ideas and equations: the physical model, the network architecture, the
  algorithm, with TikZ diagrams.
- Why this approach: for scientific work, how it compares with the literature and why the
  alternatives fit worse, with citations; for pure software, the core idea and why it suits the
  problem, without a literature comparison.
- Results from actual runs: figures, tables, the experimental setup in scientific terms (data size,
  resolution, training budget, hardware class).
- Limitations and open questions.

## What never belongs

- Code: file, module, function or class names, CLI flags, config keys, UI, tooling.
- History: "previously", "now", "new", "we changed", "version 2", any mention of a decision process,
  of `.claude/`, or of Claude.
- Changes that don't alter the science: refactors, performance tweaks without new results, UI.

## When to update

After any change, ask: would a reader of the paper learn something different? Only changes to the
model, method, theory, results or limitations qualify. If none, leave `details/` alone.

## Approval protocol (mandatory, also in auto mode)

1. In the chat, in Portuguese, write the change plan:
   - which sections change, and what is added, rewritten or removed in each, at bullet level;
   - the key equations, figures or tables involved;
   - why the change is relevant to the theory.
2. Ask with AskUserQuestion: apply, adjust, or skip.
3. Only after approval, edit. The permission prompt on `details/` is a second, enforced gate; the
   compile command prompts too.

## Creating details/

The same approval protocol applies to the first version: propose the outline and the content of
each section first. Then create the folder with `cp -r ${CLAUDE_SKILL_DIR}/template details` (the
only shell write into `details/` the guard hook allows), set the title and write the sections.

## Writing

Read `~/.claude/kit/rules/writing.md` first. Paper voice: "we", present tense for the method, past
tense for experiments. Define every symbol at first use. Number only equations that are referenced.
Every figure and table is referenced in the text and has a caption that stands on its own. Use
`\citet`/`\citep` with entries in `references.bib`, only for sources you have read.

## Style elements

From `details.sty`; don't restyle locally. If the style itself should change, that is a `/kit` change.

- Boxes: `keypoint` for the one idea a reader must keep from a section, `limitation` for a limit
  stated where it applies. Use them sparingly.
- Statements: `definition`, `assumption`, `proposition`.
- TikZ styles `block`, `focus` (the component under discussion), `op`, `flow`, `note`; colours
  `ink`, `accent`, `muted`, `tint`, `series1`–`series4`.
- Plots: pgfplots picks up the house cycle list. Figures made in Python use
  `plt.style.use("details/details.mplstyle")`, are saved as PDF in `details/figures/`, and come from a
  project script so they can be regenerated.

## Build and check

```
latexmk -r details/latexmkrc -cd details/details.tex
```

Run it from the project root. `details/latexmkrc` selects LuaLaTeX and sends auxiliary files to
`details/build/` (gitignored); the PDF stays at `details/details.pdf` and is committed. Fonts:
Source Serif 4, Source Sans 3 and STIX Two Math, which TeX Live ships; the style falls back to Latin
Modern if they're missing.

Before reporting: zero errors, no undefined references or citations, no overfull boxes wider than a
couple of points. Render the pages (`pdftoppm -r 80 -png details/details.pdf /tmp/details`) and look
at them. Then tell Pedro what changed in the PDF, section by section.
