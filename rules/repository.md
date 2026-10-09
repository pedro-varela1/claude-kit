# Repository contract

Every project has this shape at its root:

```
README.md       how to install and run, nothing else
LICENSE         MIT
config.toml     every tunable constant
details/        paper-style theory snapshot, compiled to details/details.pdf
.claude/        project context (CLAUDE.md), decisions/, research/
<source>        laid out as the language rule says
```

## README.md

A stranger should go from clone to first result in a few minutes. It contains, in this order:

1. Title and two to four sentences on what the project does and what it produces.
2. Requirements: language version, system dependencies (CUDA, TeX, …).
3. Install: the exact commands.
4. Usage: the exact commands, the main outputs and where they land, one line saying that parameters
   live in `config.toml`.
5. A link to `details/details.pdf` for the theory.
6. License: one line pointing to `LICENSE`.

It describes the current state only. No history, no "new", no "now supports", no mention of
decisions, alternatives considered, Claude, or `.claude/`. No badges, no emoji. Under about 60 lines.
Follow `rules/writing.md`.

## LICENSE

MIT, from `~/.claude/kit/templates/LICENSE`, with the current year and "Pedro Varela".

## details/

Exists in every project. Its content is governed by `/details`, and it changes only after I approve a
written change plan.

## .claude/

- `CLAUDE.md`: what the project is, domain notes, commands. Start from
  `~/.claude/kit/templates/CLAUDE.md` and keep it short and current.
- `decisions/`: the decision journal (see `/decide`).
- `research/`: briefs written by `/research`.

## Git

- `.gitignore` covers the language's build artefacts, virtual environments, `.env`, and
  `details/build/`. `details/details.pdf` is committed.
- Commit messages in English, imperative mood, one logical change per commit.
