---
description: UI verification — verify rendered output in a live browser, never by grepping source. Loads for component, template, and stylesheet files.
paths:
  - "**/*.{jsx,tsx,vue,svelte,astro}"
  - "**/*.{css,scss,sass,less}"
  - "**/*.html"
---

# UI Verification

## Verify against the rendered artifact

- Never verify rendered output with `grep` against source files or CSS selectors. Verify against
  the *rendered* artifact — built HTML, live DOM, computed styles — using Playwright or the
  browser MCP.
- If neither is available, say `UNVERIFIED — no browser` explicitly. Never substitute a
  source-level grep and report it as verification.
- Evidence means measured values — computed styles, element boxes, console/network output. A
  screenshot alone is not evidence; screenshots have come back blank.

## Before committing a UI change

- Verify in a live browser before committing, not before opening the PR. Load the page, exercise
  the change, check both light and dark themes, and re-check at a mobile width.
- Run axe against the real page, not a Storybook iframe — navigate to the page first, then audit.
  Auditing inside the iframe stalls and produces no result.
- Add srcset/responsive checks for any image change.
