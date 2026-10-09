---
name: research
description: 'Workflow 1: turn a new idea or open problem into a justified approach. Surveys the literature and the state of the art, compares candidate approaches, explains why the losers lose, judges feasibility and limitations, and hands the direction decisions to Pedro. Use for "I have an idea…", "what is the best way to…", or any new project that starts from a question.'
argument-hint: <idea or problem>
---

# /research

Goal: Pedro ends with a direction he understands and could defend, backed by sources, and a brief
that `/build` can implement. You propose; he decides.

## 1. Frame the problem

Restate the problem in one paragraph: inputs, outputs, constraints (data, compute, time, hardware),
and how success will be measured. If an ambiguity would change the direction, ask before searching
(AskUserQuestion is enough here).

## 2. Survey

- Search primary sources: arXiv, Semantic Scholar, Google Scholar, venue proceedings, official
  documentation and benchmark leaderboards. Cover the foundational work and the last three years.
- For each relevant source note: authors, year, venue (or "preprint"), link, the claim, the evidence
  behind it (dataset, metric, numbers), and why it matters here.
- Read the paper or its abstract and results before citing it. Never cite from memory alone, never
  invent a reference. If you can't verify something, say so.
- Look for negative results and known failure modes, not only successes.

## 3. Candidates

Pick three to five approaches, always including the simplest credible baseline. For each:

- core idea in two sentences, and the assumption it rests on;
- evidence that it works on problems like this one;
- cost: data, compute, implementation effort, maintenance;
- how it fails.

## 4. Verdict

- Recommend one approach and say why it fits this problem specifically.
- For every other candidate, give the concrete reason it loses here: a violated assumption, cost,
  weaker evidence, or a failure mode we would hit. "Less popular" is not a reason.
- Feasibility: can it work within the constraints? What is the smallest experiment that would show
  early that it doesn't?
- Limitations that remain even if it works.

## 5. Decide with Pedro

Use `/decide`; research almost always needs the UI. Typical rounds:

1. the approach (with the comparison above as explanation);
2. the choices that depend on it: data, metrics, scope of the first version;
3. anything still open.

## 6. Write the brief

Save `.claude/research/<slug>.md` (create the folder if needed):

```markdown
# <Problem>
## Problem          inputs, outputs, constraints, success metric
## Literature       one entry per source: citation, link, claim, evidence, relevance
## Candidates       the comparison table and the reasons each loses
## Decision         the chosen approach, linking to the decision records
## Limitations      what remains hard or unknown, and the early-failure experiment
## Build brief      what /build must implement: components, data flow, experiments, outputs
## References       BibTeX entries, ready to move into details/references.bib
```

Finish by summarising the decision in Portuguese and offering `/build` with this brief.
