---
name: decide
description: 'Ask Pedro for direction decisions and record them. Chooses between AskUserQuestion and the local decision UI, writes rounds of questions with explanations and a recommendation, runs the UI and waits for the answers, and logs every round to .claude/decisions/. Use whenever an approach, method, architecture, library, data format or scope has to be chosen.'
---

# /decide

## AskUserQuestion or the UI

Use **AskUserQuestion** when all of these hold:

- at most four questions, independent of each other;
- each question and its options are clear in a couple of lines;
- no comparison table, equation or code is needed to choose well.

Use **the UI** when any of these holds:

- a choice needs a paragraph or more of explanation, a table, an equation or a snippet;
- the decisions form a chain, so answers to this round shape the next one;
- it is a `/research` verdict or a `/build` architecture.

## Rounds

- One round holds every question that doesn't depend on another unanswered question. Questions
  that do depend on one wait for the next round, written in light of the answers.
- Prefer fewer, fuller rounds; never split independent questions across rounds.
- Before the next round, read every note. If Pedro didn't understand something, explain it again from
  a different angle (`rules/explaining.md`), in the next round's context or in the chat.

## Writing a round

Number rounds per project: list `.claude/decisions/` and take the next `NNN`. Write
`.claude/decisions/NNN-<slug>.json` following `${CLAUDE_SKILL_DIR}/example.json`:

- `id`, `title`, `context`: where we are, what earlier rounds decided, why this round exists.
- `questions[]`: `id`, `title`, `explanation`, optional `multiple: true`, and `options[]` with `id`,
  `label`, `summary` (one line), `details` (pros, cons, evidence, sources) and `recommended: true` on
  exactly one option.
- Markdown works in `context`, `explanation`, `summary` and `details`: paragraphs, lists, tables,
  `code`, links, and math as `$…$` or `$$…$$`.
- Figures: save PNG or SVG in `.claude/decisions/NNN-<slug>/` and reference them as
  `![caption](NNN-<slug>/figure.png)`; the page and the Markdown record both resolve that path.
- Content in Portuguese, technical terms in English. Say why the recommended option wins and why each
  alternative loses for this problem. Don't hide a weak point of the recommendation.

## Running the UI

Run it with the **Monitor** tool, deadline 30 minutes:

```
python3 "${CLAUDE_SKILL_DIR}/decide.py" .claude/decisions/NNN-<slug>.json
```

On Windows the interpreter is `python`.

- First line `open <url>`: the browser opened. Tell Pedro in one line that the round is open, with
  the link in case the browser didn't open, then stop and wait.
- Line `answered <record.md>`: read the round JSON (`answers` key) and continue.
- Ignore any other line.
- If the deadline passes without an answer, start the same command again. The page keeps Pedro's
  draft.
- Without Monitor, run it with Bash and the maximum timeout. If the command moves to the background,
  tell Pedro to submit and reply "ok", then read the JSON.
- On a remote machine without a browser add `--no-browser` and send Pedro the URL.

The script refuses a file that already has answers; a new decision is a new round.

## Records

The UI writes `NNN-<slug>.md` next to the JSON: context, questions, options, the choice and Pedro's
notes. For decisions taken through AskUserQuestion, write the same `.md` by hand:

```markdown
# NNN · <title>
_<date>_

## <question>
- **<option>** (recommended): <summary>
- **<option>** **← chosen**: <summary>

**Notes:** <Pedro's text, if any>
```

These records are Pedro's learning journal and the project's memory. Read them before revisiting a
topic. They are never mentioned in the README or in `details/`.
