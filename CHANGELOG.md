# Changelog

## 2026-10-11

- `/details` template: `latexmkrc` puts the project folder on `BIBINPUTS`, so BibTeX running in
  `build/` no longer picks another `references.bib` from the TeX path.

## 2026-10-09

- Windows support: the installer links with directory junctions, writes imports and settings paths
  in the forms Claude Code expects on Windows, runs the hook with `python`, and adds an `ask` rule
  for the kit's real location.
- The `details/` guard and the LaTeX `ask` rules also cover the PowerShell tool, Windows paths and
  case-insensitive names.
- README and `/details` accept MiKTeX (with its font packages and Git Bash's Perl for `latexmk`);
  `/decide` and `/details` quote `${CLAUDE_SKILL_DIR}`; `decide.py` prints UTF-8.
- Initial kit: working agreement, code style with Python, C/C++/CUDA and TypeScript rules,
  repository contract, writing and explaining rules.
- Workflows `/research`, `/build`, `/evolve`; `/decide` with the browser UI; `/details` with the
  Technical LaTeX style; `/kit` for changing the kit.
- Settings: Explanatory output style, approval rules for `details/`, LaTeX builds and kit edits, and a
  hook that blocks shell writes into `details/`.
