# claude-kit

Personal Claude Code configuration: one working agreement, one code style and one documentation
style for every project. It defines three workflows (research, build, evolve), a local browser UI for
design decisions, and a LaTeX template for each project's theory document.

## Requirements

- Claude Code
- Python 3.11+
- TeX Live or MiKTeX with LuaLaTeX and `latexmk` (fonts: Source Serif 4, Source Sans 3, STIX Two
  Math; on MiKTeX: `miktex packages install sourceserif sourcesans stix2-otf`)
- macOS, Linux, or Windows with Git for Windows (its Perl runs MiKTeX's `latexmk`)

## Install

```bash
git clone https://github.com/pedro-varela1/claude-kit.git ~/code/claude-kit
python3 ~/code/claude-kit/install.py
```

On Windows, run the same commands in Git Bash with `python` in place of `python3`.

The installer links the kit into `~/.claude` (`kit/`, `rules/kit/`, one link per skill), adds an
import line to `~/.claude/CLAUDE.md`, and merges `settings.json` into `~/.claude/settings.json`
after saving a copy as `settings.before-kit.json`. On Windows the links are directory junctions,
which need no administrator rights. Run it again after pulling changes to `settings.json` or to the
list of skills.

## Usage

Start Claude Code in any project and pick a workflow:

```
/research <idea or problem>
/build <brief or instructions>
/evolve <change>
```

`/decide`, `/details` and `/kit` are used by the workflows and can be called directly. `/kit` changes
this repository and records each change in `CHANGELOG.md`.

## Layout

```
CLAUDE.md            working agreement, loaded in every session
rules/               code style, per-language rules, repository contract, writing, explaining
skills/research      workflow 1: literature, candidates, verdict, brief
skills/build         workflow 2: architecture, milestones, repository contract
skills/evolve        workflow 3: triage, clean insertion, obsolescence sweep
skills/decide        decision protocol and browser UI (decide.py, page.html)
skills/details       details/ protocol and LaTeX template
skills/kit           how the kit changes itself
hooks/               guard against Bash and PowerShell writes into details/
templates/           project CLAUDE.md, LICENSE, .clang-format, biome.json
settings.json        output style, approval rules, hooks
```

## License

MIT, see `LICENSE`. KaTeX in `skills/decide/vendor/katex` is MIT-licensed by its authors.
