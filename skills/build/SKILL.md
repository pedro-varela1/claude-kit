---
name: build
description: 'Workflow 2: implement a defined idea from scratch, from instructions or a /research brief. Designs the architecture with Pedro, then builds the complete repository in the house style: modules, config.toml, README, LICENSE and details/. Use when the approach is decided and the job is to build it.'
argument-hint: <brief path or instructions>
---

# /build

Goal: a complete, runnable repository that Pedro understands module by module.

## 1. Read and separate

Read the brief (`.claude/research/<slug>.md`) or the instructions. List what is already decided and
what is still open. Read the project's `.claude/CLAUDE.md` and `.claude/decisions/` if they exist.

## 2. Architecture

Draft, in this order:

- the data flow from input to output, as a short diagram;
- the module map: one line per module stating its responsibility and what it depends on;
- the `config.toml` sections and their main keys;
- dependencies, each with a reason;
- how it will be run.

Open direction questions (framework, numerical method, model variant, data format, metrics) go to
Pedro: `/decide` when they chain or need explanation, AskUserQuestion when isolated. Module
boundaries, names and layout are yours; explain the key ones in Insight blocks.

## 3. Plan

Turn the architecture into milestones in the task list. The first milestone is a walking skeleton:
the full path from config to output running end to end with the simplest possible pieces. Each later
milestone replaces one piece with the real thing and leaves everything runnable.

## 4. Implement

- Follow `rules/code-style.md` and the language rule. Write `config.toml` first; it documents the
  model's parameters.
- Run after each milestone. Core logic gets tests.
- A new direction question during implementation goes back to Pedro, not into a silent default.

## 5. Repository contract

Create or update everything in `~/.claude/kit/rules/repository.md`. Before writing the README, read
`~/.claude/kit/rules/writing.md`. Write the project's `.claude/CLAUDE.md` from
`~/.claude/kit/templates/CLAUDE.md`. For `details/`, run `/details`, which asks Pedro before
writing anything.

## 6. Verify and hand over

- Run from a clean state with the README's own commands. They must work exactly as written.
- Sweep for anything unused: functions, config keys, dependencies, files.
- Report in Portuguese:
  - what was built, with the module diagram;
  - the three or four places in the code worth reading to understand the method, with what to look
    for in each;
  - decisions taken (links to `.claude/decisions/`) and remaining limitations.
