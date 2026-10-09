---
name: kit
description: 'Change the kit itself (the global CLAUDE.md, rules, skills, decision UI, LaTeX style, templates or settings) when Pedro states a new preference or a better way of working. Finds every file the change touches so the kit stays coherent, shows the complete change before applying it, and records it in the CHANGELOG.'
argument-hint: <preference or change>
---

# /kit

The kit is a git repository linked at `~/.claude/kit`. Find its real location with
`readlink -f ~/.claude/kit` and work there.

## 1. Find everything the change touches

Read the files directly involved, then search the whole kit for related terms, because one idea often
lives in several places. Examples:

- the accent colour is in `skills/details/template/details.sty`, `details.mplstyle` and
  `skills/decide/page.html`;
- a workflow step can be referenced from `CLAUDE.md` and other skills;
- a rule about README content appears in `rules/repository.md` and in `/build`.

Look for contradictions the change would create, and for text it makes obsolete.

## 2. Show the change

Before editing, in Portuguese:

1. a table: file · what changes · why;
2. the exact diff for every file (unified diff, or the full content of a new file);
3. effects outside the kit: projects that would need a refresh (for example a new LaTeX style), or a
   settings change that needs `python3 install.py` again.

Ask with AskUserQuestion: apply, adjust, or cancel. Edits under `~/.claude/kit` also trigger a
permission prompt, so Pedro sees each file being written.

## 3. Apply and record

- Apply exactly what was approved. Keep files short: instructions that only matter for one task belong
  in a skill, not in `CLAUDE.md` or an unconditional rule.
- Add an entry at the top of `CHANGELOG.md`: date, one line per change.
- Commit in the kit repository: `git -C <kit> add -A && git -C <kit> commit -m "<summary>"`.
- If `settings.json` changed, run `python3 <kit>/install.py` (`python` on Windows).
- Mention that new or edited skills and rules load in new sessions.

## Rules for kit content

- Instructions in English, general, never about one specific project.
- Say each thing once and reference it elsewhere.
- What must be guaranteed goes into `settings.json` (permissions, hooks); `.md` files are guidance.
