---
name: evolve
description: 'Workflow 3: change or extend an existing implementation: a new feature, a new structure, or a change of idea. Triages simple versus complex, validates complex changes against the literature, inserts the change cleanly and removes whatever became obsolete. Use for any modification of a project that already exists.'
argument-hint: <change to make>
---

# /evolve

Goal: the code looks as if the change had been part of the design from the start.

## 1. Understand the current state

Read the modules the change touches, `config.toml`, `details/` (the theory the code implements) and
`.claude/decisions/`. If the request contradicts an earlier decision, say so and ask whether the
earlier one still holds.

## 2. Triage

- **Simple**: local, no new concept, no effect on results or theory. Implement it.
- **Complex**: a new method or model, a change to results or theory, or a change that cuts across
  modules. First find the best way to do it: run steps 2–4 of `/research` in compact form (sources,
  two or three candidates, verdict), then decide with Pedro (`/decide` or AskUserQuestion).

If you're unsure which it is, treat it as complex and say why in one line.

## 3. Design the insertion

- Find where the change belongs: an existing seam, or a new module with one responsibility.
- No special cases bolted on: no flags that switch between old and new behaviour, no duplicated
  paths. If the current structure can't hold the change cleanly, refactor first (structure is your
  call; direction is Pedro's).
- New parameters go to `config.toml` with a comment and unit.

## 4. Implement and sweep

- Implement, run, test.
- Sweep for obsolescence: functions, parameters, config keys, files, dependencies, tests and README
  lines that are now unused or wrong. Search for references, delete, run again.

## 5. Documentation

- README: update only if install or usage changed. It describes the current state, never the change.
- `details/`: if the change alters the model, method, theory, results or limitations, run
  `/details`. It shows Pedro exactly what would change in the PDF and waits for approval. Refactors,
  UI and tooling changes never touch `details/`.

## 6. Report

In Portuguese: what changed and why it sits where it does, what was removed, decisions taken, and
anything Pedro should read to understand the new part.
