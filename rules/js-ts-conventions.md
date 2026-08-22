---
description: React and TypeScript conventions — component style, field naming, quote style. Loads for JS/TS source files.
paths:
  - "**/*.{ts,tsx,js,jsx}"
---

# JavaScript / TypeScript Conventions

- React components: arrow functions, function components. No class components.
- TypeScript: `_underscore` prefix for private fields, `camelCase` for public fields.
- Prefer double quotes — matches the `quoteStyle` settings in the VS Code config.
- When a file's local style differs from these conventions, match the file. Mention the mismatch;
  do not restyle it.
