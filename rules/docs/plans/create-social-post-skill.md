---
status: todo
type: feature
created: 2026-05-26
repo-name: claude
---

# Plan: Create social-post skill

## Context

During a session on 2026-05-26 the user wrote a LinkedIn post about changes to `plan-mode.md` and generated a dark-mode GitHub-style diff card to accompany it. The workflow — draft copy, build styled HTML, start a local HTTP server, Playwright screenshot, deliver image — was done manually. The user wants this captured as a reusable `/social-post` skill so the same pipeline can be triggered on demand for any post.

## Objective

Create `~/.claude/skills/social-post/` with a `SKILL.md` that drives the full workflow (clarify → draft platform-aware copy → populate a card template → screenshot via Playwright → deliver copy + image), three dark-mode HTML card templates, and a helper script for port selection.

## Steps

1. **Create the directory skeleton.** Run `mkdir -p ~/.claude/skills/social-post/{templates,scripts}` to establish the required layout before writing any files.
   - *Why:* Write tools require the parent path to exist; creating it first prevents silent failures on nested paths.
   - *Verify:* `ls ~/.claude/skills/social-post/` shows `templates/` and `scripts/` directories.

2. **Write `SKILL.md`.** Create the main skill file with YAML frontmatter (`name: social-post`, `description`, `version: 0.1.0`) and a workflow section covering: (a) Clarify — `AskUserQuestion` for platform, card type, and tone when not supplied; (b) Draft — platform-aware copy rules (LinkedIn ≤1 500 chars narrative; Twitter/X ≤280 chars punchy; Bluesky same as Twitter); (c) Pick template — heuristic: diff/rule/code change → `diff-card`, release/feature → `feature-card`, insight/quote → `quote-card`; (d) Populate — substitute `{{VARIABLES}}` in the chosen template; (e) Screenshot pipeline — write HTML to `~/.claude/tmp/social-post-card.html`, run `python3 scripts/find_free_port.py` to get a free port, start `python3 -m http.server <port>` in background, Playwright navigate + full-page screenshot to `~/.claude/tmp/social-post-card.png`, kill the server; (f) Deliver — present copy in a fenced block followed by the image.
   - *Why:* SKILL.md is the sole runtime artefact Claude loads; all workflow logic must live here in imperative, step-by-step form — reference files are for reference material, not core instructions.
   - *Verify:* `head -6 ~/.claude/skills/social-post/SKILL.md` shows valid YAML frontmatter with `name`, `description`, and `version`; reading the file confirms all six workflow phases are present.

3. **Create `templates/diff-card.html`.** Parameterise the dark-mode diff card built in this session. Replace hard-coded content with template variables: `{{FILENAME}}`, `{{BADGE}}`, `{{HUNK_1_HEADER}}`, `{{HUNK_1_ROWS}}`, `{{HUNK_2_HEADER}}`, `{{HUNK_2_ROWS}}`, `{{STAT_ADD}}`, `{{STAT_DEL}}`, `{{WORKFLOW_SUMMARY}}`. Retain the full CSS (colour tokens, `.add`/`.del`/`.ctx` row styles, `.hl-add`/`.hl-del` inline highlights, section-label badges, footer stat bar).
   - *Why:* The diff card produced in this session is already visually validated; parameterising it rather than regenerating from scratch guarantees fidelity to the approved design.
   - *Verify:* Open the file; confirm nine `{{...}}` placeholders are present and no hard-coded content from today's session remains.

4. **Create `templates/feature-card.html`.** Build a dark-mode card suited to feature/release announcements. Layout: title area with `{{TITLE}}` and `{{SUBTITLE}}`; a bullet list region `{{BULLETS}}` (each bullet rendered as a `<li>` with a coloured left-border accent); a footer bar showing `{{BADGE}}` and `{{FOOTER_NOTE}}`. Reuse the same CSS colour tokens and `box-shadow` as the diff card for visual consistency.
   - *Why:* Release posts have a different content shape than diffs — a headline + bullets is the standard LinkedIn/Twitter format — but should look like they came from the same design system.
   - *Verify:* Open the file; confirm `{{TITLE}}`, `{{SUBTITLE}}`, `{{BULLETS}}`, `{{BADGE}}`, `{{FOOTER_NOTE}}` are present; open in a browser and confirm the layout is legible and matches the dark-mode colour scheme.

5. **Create `templates/quote-card.html`.** Build a minimal dark-mode quote card. Layout: large pull-quote `{{QUOTE}}` centred with generous padding; `{{ATTRIBUTION}}` in smaller muted text below; optional `{{CONTEXT}}` tag line at the top. Typography-forward — no table rows, no diff chrome.
   - *Why:* Insight/opinion posts need a visually distinct treatment from code-change posts; a quote card signals "thought leadership" rather than "technical diff".
   - *Verify:* Open the file; confirm `{{QUOTE}}`, `{{ATTRIBUTION}}`, `{{CONTEXT}}` are present; render in a browser and confirm legibility.

6. **Create `scripts/find_free_port.py`.** Write a short Python 3 script that binds a `socket` to port 0 (OS assigns a free port), prints the port number to stdout, and exits. The skill calls it with `python3 ~/.claude/skills/social-post/scripts/find_free_port.py` to avoid collisions with other running servers.
   - *Why:* Hard-coding port 9341 (used in this session) will conflict if another process is already bound there; letting the OS assign a free port makes the pipeline reliably re-entrant.
   - *Verify:* Run `python3 ~/.claude/skills/social-post/scripts/find_free_port.py` twice and confirm both calls print a valid integer and that the two integers differ (or are both free at call time).

## Acceptance Criteria

- [ ] `~/.claude/skills/social-post/SKILL.md` exists with valid frontmatter (`name`, `description`, `version`).
- [ ] Invoking `/social-post` without arguments triggers an `AskUserQuestion` for at minimum platform and topic.
- [ ] Invoking `/social-post linkedin diff` (or equivalent explicit args) skips the clarify step and proceeds directly to drafting.
- [ ] The skill selects the correct template based on context (diff context → `diff-card.html`, feature context → `feature-card.html`).
- [ ] The screenshot pipeline produces a PNG at `~/.claude/tmp/social-post-card.png` without leaving a dangling HTTP server process.
- [ ] Copy output respects platform length/tone rules (LinkedIn ≤1 500 chars; Twitter ≤280 chars).
- [ ] The final response presents post copy in a fenced block and attaches the PNG in the same turn.

## Verification

Invoke `/social-post` using the exact context from this session — the LinkedIn post about `plan-mode.md` Clarify/Align additions. The skill should:
1. Skip the clarify step (platform and topic are supplied).
2. Select `diff-card.html`.
3. Produce copy within 1 500 characters matching a LinkedIn professional tone.
4. Deliver a PNG that visually matches (or improves on) the diff card generated manually in this session.

Separately invoke `/social-post` with a made-up feature announcement and confirm `feature-card.html` is chosen and the copy is appropriately shorter/punchier for Twitter when that platform is specified.

## Next Steps *(optional)*

- Add a `quote-card` invocation test:
  ```text
  Invoke /social-post with a short insight or opinion (no code context) and confirm the skill selects quote-card.html and produces a typography-forward card rather than a diff or feature card.
  ```

- Add a `--output` flag so images save to a user-specified directory instead of `~/.claude/tmp/`:
  ```text
  Update ~/.claude/skills/social-post/SKILL.md to accept an optional --output <path> argument. When provided, save the PNG to <path> instead of ~/.claude/tmp/. Document the flag in a README.md alongside the skill.
  ```

- Package the skill for distribution:
  ```text
  Run /skill-packager on ~/.claude/skills/social-post/ at version 0.1.0 and generate a distributable ZIP + Download.md. Save the output to ~/.claude/downloads/social-post/.
  ```
