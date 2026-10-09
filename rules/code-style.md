# Code style

One house style for every language: minimal, direct, modular. Code should read like a short, careful
explanation of the method.

## Shape

- A module owns one responsibility; a function does one thing. If a name needs "and", split it.
- Keep the call graph shallow and the data flow visible: inputs in, outputs out, no hidden state.
- Return early instead of nesting. Prefer plain functions and small immutable data types over class
  hierarchies; reach for a class when there is state with invariants to protect.
- No speculative abstraction: no interface with one implementation, no option nobody uses. Leave a
  clean seam where change is likely and stop there.
- Separate the science from the plumbing: numerical core free of I/O, CLI and plotting at the edges.

## Names

- Names say what a thing is, in the vocabulary of the domain. Use the paper's symbols when the code
  implements an equation (`kappa`, `dt`, `k_max`) and full words everywhere else.
- Units go in the name when ambiguity is possible: `length_m`, `timeout_s`.

## Comments

Write a comment only when the code cannot say it:

- why a non-obvious choice was made, an invariant, a unit, a numerical subtlety;
- the source of a formula: `# Eq. (4), Li et al. (2021)`.

Never narrate what the next line does, never leave commented-out code, never write history
("changed from…", "new:", "fixed"). Public functions get a one-line docstring only when the name and
types leave something out.

## Configuration

- Every tunable constant lives in `config.toml` at the repository root: hyperparameters, physical
  parameters, sizes, tolerances, seeds, paths. TOML because it has comments, types and sections, and
  every language here reads it.
- Group keys by section (`[model]`, `[training]`, `[physics]`, `[paths]`) and comment each key with
  its meaning and unit.
- Load it once at the entry point into a typed, immutable object and pass what each part needs.
  Library code never reads the file itself.
- Mathematical constants come from the language (`math.pi`). Literals like `0`, `1`, `2` in obvious
  roles stay inline. Everything else is a named config value.
- Secrets never go in `config.toml`: use environment variables, with `.env` gitignored.

## Robustness

- Fail fast with a message that names the bad value and what was expected. No bare or silent catches.
- Validate at the boundaries (config, files, user input); trust values inside.
- Seed every source of randomness from config.

## Dependencies and tooling

- Few, standard, well-maintained dependencies, pinned in the language's manifest.
- Format and lint with the language's standard tool (see the language rule) and keep it clean.

## Changing code

- Fit the change into the existing structure; if the structure no longer fits, refactor first.
- In the same change, delete whatever became unused: functions, parameters, config keys, files,
  dependencies, README lines. Search for references before deleting.
- Verify by running it. Core logic (numerics, parsing, transforms) gets tests.
