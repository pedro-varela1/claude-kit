---
paths:
  - "**/*.{ts,tsx,mts,js,jsx,mjs,cjs}"
  - "**/package.json"
  - "**/tsconfig*.json"
---

# TypeScript and JavaScript

- TypeScript in strict mode for anything beyond a single script. ES modules only.
- `npm` with a committed lockfile, so anyone can reproduce with `npm ci`.
- Format and lint with Biome using the kit's `templates/biome.json`.
- Small modules of pure functions; side effects at the edges. Named exports only, no default exports.
- No `any`. Explicit return types on exported functions. Model data with `type` and discriminated
  unions; validate external data at the boundary.
- Config: read `config.toml` with `smol-toml` on the server or at build time; the browser receives
  only the values it needs.
- UIs: plain HTML, CSS and TypeScript with Vite by default. Bring in a framework only when the state
  complexity justifies it, and treat that as a direction decision.
- Tests with Vitest.
