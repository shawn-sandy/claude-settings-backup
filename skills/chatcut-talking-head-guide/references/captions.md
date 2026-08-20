## Captions

### Goal

Improve accessibility and engagement with on-screen text.

Captions start from the source transcript. When the user asks for translation or bilingual captions, use `edit_captions` action `translate`; its `languageCode` is the translation target. Languages are ordinary caption sources, so use `source_set` for custom language presentation.

### Presets

Prefer built-in caption presets because they provide more stable, tested results. Use only real built-in `edit_captions` preset names; there is no `youtube` or `vox` preset.

- For a general style request, first list the language-aware presets with `edit_captions` action `template`, then choose one or offer relevant returned presets for the user to choose from.
- Use custom `style` / `layout` only when the user clearly requests a custom look or a specific adjustment.
- For adjustments, start from the closest preset and change only the requested properties.

### Optional emphasis follow-up

After captions are first created and verified, if the user has not already requested emphasis, ask once whether they want it. Base the question on the actual caption content: mention only relevant categories—such as data, concepts or conclusions, people, organizations or product names, steps or actions, and contrasts or risks—and include an option to let the Agent decide. Treat a chosen category as guidance, not a requirement to emphasize every match. Do not interrupt an explicitly requested end-to-end workflow; offer this only after the requested work is complete.

Emphasis is opt-in. Once requested, read the complete caption sequence with `read_captions`. First choose Cards whose content adds distinct value for understanding, recall, action, decision, state tracking, or an expressive payoff. Suppress setup, filler, and repeated payloads; allow adjacent selections when each adds something independent, and let the content determine how many spans to emphasize.

Within each eligible Card, choose the smallest contiguous verbatim span that remains truthful. Preserve negation or modality, conditions, scope or uncertainty, required units or referents, indispensable action objects, and both sides of a contrast when needed. If the same text occurs more than once, use `occurrence`; use `languageCode` to target one bilingual projection.

Apply the requested spans with `set_card_span_style`, then read the captions again and verify the resulting `inlineStyles`. Do not change caption wording, timing, Card boundaries, line breaks, position, pacing, or overall style.
