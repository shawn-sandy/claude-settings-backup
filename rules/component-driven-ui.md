---
description: Component-driven UI — build interfaces bottom-up from modular components. Loads for JS-framework component files (React/Astro/Vue/Svelte); does not apply to plain HTML.
paths:
  - "**/*.jsx"
  - "**/*.tsx"
  - "**/*.astro"
  - "**/*.vue"
  - "**/*.svelte"
---

# Component-Driven UI

All projects build user interfaces with modular components, bottom-up: start with the smallest primitives, then compose them progressively into larger components, then screens. Reference: https://www.componentdriven.org/

## How to apply

- **Bottom-up, not top-down.** Build and verify the atoms (button, input, badge) before the molecules (form field, card) before the organisms (form, list, header) before pages/screens. Never author a screen as one monolithic block — decompose it into reusable parts.
- **One component, one responsibility.** A component does one thing. If it branches on many boolean props to look like several different things, split it.
- **Compose, don't duplicate.** Assemble larger UI from existing smaller components. Reach for an existing primitive before writing a new one.
- **Isolation first.** Every component must be buildable and viewable in isolation (Storybook, a preview route, or a test harness) — independent of the screen that uses it.
- **Props are the contract.** Keep props explicit and typed; pass data down, emit events up. No hidden coupling to global state a component doesn't own.

## Why

Bottom-up composition makes UI reusable, independently testable, and cheaper to change — a fix to a primitive propagates everywhere it's used, and screens become thin compositions rather than tangled one-offs.
