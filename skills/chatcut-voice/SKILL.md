---
name: voice
description: |
  Text-to-Speech (TTS), voiceover, narration placement/sync, and custom sound effects (SFX) generator. Use when the user wants generated speech from text, wants to add/replace/align narration or voiceover for an existing video/timeline, wants to keep existing voiceover synced after visual retiming edits, needs voice audition/selection, or explicitly wants a newly generated/custom sound effect that is not available in the Sound Effects library.
user-invocable: true
---

# Voice & Sound Effects Generator

Generate voiceovers (TTS) and sound effects. For TTS, choose a concrete
provider and voice before calling `submit_voice`.

## When to Use

- Generate voiceover/narration from text
- Create text-to-speech audio for videos
- Add, replace, or redo narration/voiceover for an existing video, timeline,
  screen recording, slide animation, product demo, B-roll edit, MG explainer, or
  other visual sequence
- Keep existing narration/voiceover aligned after trimming, speeding up, slowing
  down, moving, reordering, or replacing the visuals it describes
- Offer and audition TTS voice choices when the user has not picked a concrete voice
- Generate custom sound effects from text descriptions only after checking the Sound Effects library first

## TTS (Text-to-Speech)

If the current request has an existing visual target and the user wants
narration, voiceover, dubbing, or replacement speech for that target, read
[references/video-sync.md](references/video-sync.md) before drafting new
narration, using existing narration text to generate TTS, or placing audio. Do
this even when the user did not explicitly say "sync" or "match the visuals";
the existence of a visual target means narration timing and meaning may need to
follow on-screen content. Use the normal standalone TTS path only when there is
no visual target or the user just wants an audio asset from text.

Also read [references/video-sync.md](references/video-sync.md) when the timeline
already has narration/voiceover and the user asks to change the visuals while
keeping that voiceover aligned. This is a sync maintenance task even if no new
TTS is needed.

Use `submit_voice` to create a TTS audio asset. The current MCP tool contract is:

- `provider` is required. Use `doubao` for Chinese-optimized narration and
  `elevenlabs` for English or multilingual narration.
- `voiceId` is required and provider-specific. Do not mix catalogs.
- `submit_voice` creates an audio asset only. Timeline placement, replacement,
  trimming, and alignment happen later with timeline tools.
- For long narration, multiple `submit_voice` calls can be useful: split at
  natural pauses, sentence groups, or script beat boundaries when the workflow
  benefits from separately timed or placed voice clips, such as storyboard beats,
  scene-level ad segments, or a user request for separate assets.
- For Doubao, `speedRatio`, `loudnessRatio`, `pitch`, `emotion`,
  `emotionScale`, `performancePrompt`, and `explicitDialect` are supported
  knobs, but not every Doubao voice supports every expressive control. Check
  [references/voices.md](references/voices.md) before using them.
- For ElevenLabs, `modelId`, `speed`, and `stability` are the supported voice
  knobs. For `eleven_v3`, inline audio tags are available for expressive
  delivery such as emotion, tone, nonverbal cues, accent hints, pauses, or
  local pacing.

### Keep voice providers private

Doubao, ElevenLabs, Fish Audio, their model names, and other provider identity
are internal implementation details. Never expose or attribute them in
user-facing replies, progress updates, voice recommendations, audition cards,
clone instructions, success summaries, or errors. Use ChatCut product language
instead:

- Call curated catalog voices `official voices` / `官方音色`.
- Call saved custom voices `cloned voices` / `克隆音色`, `My Voices` /
  `我的音色`, or use the voice's user-visible saved name.
- Describe status and failures at the ChatCut feature level. If a tool or
  provider error contains a provider name, model name, provider voice id, or
  provider URL, preserve the actionable meaning but remove those details
  before replying.

Provider names and provider-specific ids remain valid only in internal tool
arguments, tool-result interpretation, and these implementation instructions.
Do not copy them from tool output into visible UI metadata or prose.

Doubao control support for current curated voices:

- `vivi`, `xiaohe`, `yunzhou`, `xiaotian`, `naiqimengwa`, `yingtaowanzi`,
  `wenroumama`, `zhixingnv`, `dayi`, `jitangnv`, `liuchang`, `ruyayichen`,
  `morgan`, `qingcang`, `huiben`, `popo`, `yuanboxiaoshu`, `baqiqingshu`, and
  `tangseng` support explicit `emotion` / `emotionScale`,
  `performancePrompt`, and ASMR-style prompt directions.
- `shuanglangshaonian` supports `performancePrompt` and COT/QA-style
  instruction following, but does not support explicit `emotion` /
  `emotionScale` or ASMR-style control.
- `explicitDialect` is only supported by `vivi` and can be `dongbei`,
  `shaanxi`, or `sichuan`.

ElevenLabs control support for current curated voices:

- `amelia`, `brittney`, `hope`, `jessica`, `arabella`, `jane`, `maria`,
  `mark`, `frederick`, `peter`, `james`, `jon`, `sully`, `david`, and `alex`
  all support the same request-level controls: `modelId`, `speed`, and
  `stability`.
- These controls are not per-voice guarantees of a specific acting style.
  Use the preset tags/samples to pick a naturally suitable voice, then use the
  controls for moderate delivery changes.
- For ElevenLabs `eleven_v3`, inline audio tags are available when the user
  asks for expressive delivery such as emotion, tone, nonverbal cues, accent
  hints, or local pacing. Official examples fit these useful TTS categories:
  emotion/tone tags such as `[happy]`, `[sad]`, `[angry]`, `[excited]`,
  `[curious]`, `[sarcastic]`, `[crying]`, `[annoyed]`, `[appalled]`,
  `[thoughtful]`, `[surprised]`, and `[mischievously]`; vocal delivery and
  nonverbal cue tags such as `[whispers]`, `[laughs]`, `[sighs]`, `[exhales]`,
  `[inhales deeply]`, `[clears throat]`, `[snorts]`, `[swallows]`,
  `[wheezing]`, and `[coughs]`;
  pacing/pause/local speed tags such as `[slowly]`, `[pause]`,
  `[short pause]`, `[long pause]`, `[rushed]`, and `[drawn out]`; and
  accent/special-performance tags such as
  `[strong X accent]`, for example `[strong French accent]`, plus `[sings]`,
  `[singing]`, `[woo]`, and `[pirate voice]`. Official examples are
  non-exhaustive; similar auditory tags can be tried when the user explicitly
  asks for that delivery and the tag describes how the voice should sound, not
  a visual action. Write tags directly in `text`, close to the short phrase
  they should affect. Treat tags as local guidance, not paragraph-wide controls.
- For pauses and pacing in `eleven_v3`, use punctuation, text structure,
  shorter generated segments, or local audio tags such as `[short pause]` and
  `[slowly]` when needed.

```ts
// English / multilingual via ElevenLabs
mcp__skill__submit_voice({
  provider: "elevenlabs",
  text: "Hello world",
  voiceId: "peter",
});

// Chinese via Doubao
mcp__skill__submit_voice({
  provider: "doubao",
  text: "你好世界",
  voiceId: "liuchang",
});

// With speed adjustment (Doubao only)
mcp__skill__submit_voice({
  provider: "doubao",
  text: "这是一段稍快的中文旁白。",
  voiceId: "liuchang",
  speedRatio: 1.5,
});

// With expressive Doubao controls
mcp__skill__submit_voice({
  provider: "doubao",
  text: "这次事故提醒我们，安全永远不能侥幸。",
  voiceId: "liuchang",
  emotion: "sad",
  emotionScale: 3,
  performancePrompt: "痛心但克制，语速稍慢，像新闻专题旁白",
  pitch: -1,
  speedRatio: 0.92,
});

// With ElevenLabs delivery controls
mcp__skill__submit_voice({
  provider: "elevenlabs",
  text: "The launch changed how teams plan their daily work.",
  voiceId: "peter",
  speed: 0.95,
  stability: 0.4,
});
```

## Cloned Voices in ChatCut Desktop

Before offering voices for a TTS request that does not name a concrete voice,
call `manage_custom_voice` with `action:"list"`. If ready cloned voices exist,
ask whether the user wants one of their voices, an official voice, or a new
clone. It is fine to infer likely official voice qualities from the script, but
still surface the user's ready cloned voices as a first-class option.

When the user chooses to create a new clone, do not collect the recording,
name, preview copy, or authorization in chat. Explain briefly that ChatCut will
open the native flow, then emit exactly one atomic tag on its own line:

```html
<clone-voice />
```

The Desktop dialog owns recording/upload, the 10-second to 3-minute validation,
name, editable preview text, authorization, entitlement checks, cloning,
original-versus-cloned playback, retry, and applying the selected voice back to
the composer. Do not continue to clone through `manage_custom_voice` after
emitting the tag. If the user closes the dialog, wait for their next message.

When a cloned-voice attachment is present in the request, follow its hidden
context exactly and use `manage_custom_voice` with `action:"synthesize"` and
the attached ChatCut `customVoiceId`. Never substitute a Fish provider model
id and never expose the provider id.

For Fish Audio custom-voice synthesis, natural-language cues in square brackets
can guide a local phrase, for example `[whispering softly]`, `[excited]`,
`[calm and reassuring]`, or `[short pause]`. Put a cue immediately before the
text it should affect, keep it audible rather than visual, and use it only when
the user asks for expressive delivery. Treat it as guidance, not a guaranteed
exact performance.

## Voice Audition Before Generation

When the user needs TTS and has not already chosen a concrete preset, treat
broad words like "middle-aged male", "warm female", or "professional" as
requirements for filtering candidate voices.

Before recommending, rendering, or submitting any TTS voice option, read
[references/voices.md](references/voices.md). Use that file as the preset
source for preset ids / `voiceId`, provider choice, display labels, tags, and
sample URLs. Do not create voice options from memory, translated names, or
broad user descriptions.

First determine two separate languages:

- User conversation language: the language the user used to talk to you. Use
  this for the surrounding reply, `form-visual label`, `visual-option name`,
  and `summary`.
- Target narration language: the language of the text being synthesized. Use
  this only to choose provider and voice catalog.

For the voice audition widget, set `submit_label` to a short submit action in
the user conversation language, not the target narration language. For example:
English users see `submit_label="Submit"`, Chinese users see
`submit_label="提交"`, and Spanish users see `submit_label="Enviar"`.

"help me generate ... voice over in Chinese" is an English conversation asking
for Chinese narration, so the audition widget copy stays in English while the
voice candidates come from Doubao.

Instead:

1. Filter `references/voices.md` by target narration language / provider and
   the user's explicit requirements such as gender, age range, tone, and use
   case.
2. If no preset matches all explicit requirements, say there is no exact match
   and offer the closest supported presets with a clear caveat.
3. Pick 2-4 matching curated presets.
4. Load `widget-forms`. In Codex, call `ask_followup_questions` with voice
   options and audio samples. In Claude Code, render the recipe's combined
   voice cards and resolve each `voice/<voiceId>` through
   `${CLAUDE_PLUGIN_ROOT}/assets/widget-media/manifest.json`; use a label-only
   card when the key is absent and never use or process the original sample URL.
5. Wait for the user to choose.
6. Call `submit_voice` with the selected preset id as `voiceId`.

For Codex audition options, keep `value`, display label, `media`, and `summary`
tied to the same preset row from `references/voices.md`. Use sample URLs from
`references/voices.md` (`/voice-samples/<provider>-<preset>.mp3`). They are
editor assets, not paths that need an external origin. Pass each documented
`/voice-samples/...` path verbatim as `media`: never prepend an inferred S3,
CDN, editor, localhost, or production base URL, and never reconstruct an
absolute URL from the filename pattern. Keep `value` as the preset id and
`media` as the matching editor asset path. For every host, write names and
summaries in the user's conversation language. The target narration language
only decides the provider/voice catalog. For example, if the user asks in
English for a Chinese voiceover, keep the widget copy in English and use
English-friendly voice names/tags. If the user's message itself is Chinese, use
Chinese widget copy and Doubao's official Chinese display names. For known
`/voice-samples/...` presets, Codex can fill display text only when
`name`/`summary` are omitted; authored widget text is the normal path for
arbitrary languages. After the user submits, map the submitted display name
back to the preset id from the same candidate list.

In Claude Code specifically, use the provider-neutral localized display name as
the Elicitation `data-value` and keep the provider voice id only in the
label-to-id map held in context. Use an ephemeral DOM audio key for playback,
not the provider id. After the user presses Enter and the host-generated answer
line appears, map the visible name back to the preset id and continue without
another confirmation.

English request for Chinese narration:

```html
<widget submit_label="Submit">
  <form-visual
    id="voiceId"
    label="For Chinese voiceover, I recommend a few voices to try:"
    required="true"
  >
    <visual-option
      value="vivi"
      name="Vivi"
      media="/voice-samples/doubao-vivi.mp3"
      aspect-ratio="16:5"
      summary="Female / young / friendly, general"
    />
    <visual-option
      value="xiaohe"
      name="Xiaohe"
      media="/voice-samples/doubao-xiaohe.mp3"
      aspect-ratio="16:5"
      summary="Female / young / soft, clear"
    />
    <visual-option
      value="yunzhou"
      name="Yunzhou"
      media="/voice-samples/doubao-yunzhou.mp3"
      aspect-ratio="16:5"
      summary="Male / young / neutral, business"
    />
  </form-visual>
</widget>
```

Chinese request for Chinese narration:

```html
<widget submit_label="提交">
  <form-visual
    id="voiceId"
    label="我推荐这几个中文旁白音色，先试听一下："
    required="true"
  >
    <visual-option
      value="morgan"
      name="Morgan"
      media="/voice-samples/doubao-morgan.mp3"
      aspect-ratio="16:5"
      summary="男 / 中年 / 低沉知识解说"
    />
    <visual-option
      value="zhixingnv"
      name="知性女声"
      media="/voice-samples/doubao-zhixingnv.mp3"
      aspect-ratio="16:5"
      summary="女 / 中年 / 冷静知识讲解"
    />
    <visual-option
      value="vivi"
      name="Vivi"
      media="/voice-samples/doubao-vivi.mp3"
      aspect-ratio="16:5"
      summary="女 / 年轻 / 亲切通用口播"
    />
  </form-visual>
</widget>
```

## Sound Effects

For ordinary editing sound effects (SFX), do **not** generate first. Use the
built-in Sound Effects library before spending credits:

1. Call `browse_library` with `category:"sound-effects"` and a query such as
   `"whoosh"`, `"camera shutter"`, `"notification"`, `"censor beep"`, or
   `"record scratch"`.
2. Inspect the returned `library:sound:<id>`.
3. Place it with `edit_item`, using `fromFrame` as the sound's
   anchor/editorial moment frame:

```ts
mcp__core__browse_library({
  category: "sound-effects",
  query: "short whoosh transition",
});

mcp__core__edit_item({
  adds: [
    {
      type: "audio",
      assetId: "library:sound:whoosh-short",
      fromFrame: 120,
      trackId: "A1",
    },
  ],
});
```

Only generate sound effects from text descriptions with `submit_sound` when:

- The user explicitly asks for a generated/original/custom sound.
- The requested sound is too specific for the existing Sound Effects library.
- `browse_library({ category:"sound-effects", query })` returns no suitable
  match.

```ts
// Custom/generated sound effect after the library has no suitable match
mcp__skill__submit_sound({ prompt: "A dog barking in the distance" });

// With custom duration (0.5-22 seconds)
mcp__skill__submit_sound({
  prompt: "Thunder and heavy rain",
  durationSeconds: 15,
});

// High prompt adherence
mcp__skill__submit_sound({
  prompt: "Sci-fi laser gun firing",
  promptInfluence: 0.8,
});
```

**Tips for better results:**

- Be specific: "A dog barking loudly" vs just "dog"
- Include context: "Footsteps on wooden floor in an empty room"
- Specify style: "Cinematic whoosh" or "8-bit game sound"

## Parameters

### TTS

| Field        | Description                            | Notes           |
| ------------ | -------------------------------------- | --------------- |
| `provider`   | TTS provider: `doubao` or `elevenlabs` | Required        |
| `text`       | Text to synthesize                     | Required        |
| `voiceId`    | Curated preset id or provider voice id | Required        |
| `speedRatio` | Speech speed                           | Doubao only     |
| `modelId`    | ElevenLabs model id                    | ElevenLabs only |
| `stability`  | ElevenLabs stability                   | ElevenLabs only |
| `speed`      | ElevenLabs speech speed                | ElevenLabs only |
| `name`       | Asset name                             | Optional        |

### Sound Effects

| Field             | Description       | Notes          |
| ----------------- | ----------------- | -------------- |
| `prompt`          | Sound description | Required       |
| `durationSeconds` | Duration          | 0.5-22 seconds |
| `promptInfluence` | Prompt adherence  | 0-1            |
| `name`            | Asset name        | Optional       |

## Voices

Use [references/voices.md](references/voices.md) for the current curated
preset list, display labels, tags, and sample URLs.

### Voice presets are provider-specific — do NOT mix them

ElevenLabs and Doubao have separate voice catalogs. `vivi` / `dayi` are only
Doubao; `mark` / `amelia` / `james` are only ElevenLabs. Passing a Doubao name
to ElevenLabs (e.g. `voiceId: "vivi"` with `provider: "elevenlabs"`) will fail.

If you need a specific voice and a particular language:

- For Chinese narration -> use `provider: "doubao"` and either a curated Doubao
  preset (`vivi`, `dayi`, `xiaohe`, `yunzhou`, `liuchang`, etc.) or a raw
  `speaker_id` from the configured Doubao catalog.
- For English / multilingual -> use `provider: "elevenlabs"` and an ElevenLabs
  preset.

## Hard rules — what you must NOT do

1. Never use a voice preset name from a different provider.
2. Never submit TTS when the voice is only described broadly and the user has
   not confirmed a concrete preset.
3. Never recommend or render a TTS voice option before checking
   [references/voices.md](references/voices.md).
4. Never claim stable age, regional accent, pronunciation dictionary, or exact
   duration controls; the current tool does not expose those as reliable fields.
5. Never replace original recorded speech with TTS unless the user asks.
6. Never expose Doubao, ElevenLabs, Fish Audio, provider model names,
   provider-specific ids, or provider URLs to the user. Use `official voice`
   and `cloned voice` product terminology, and sanitize provider details from
   visible errors and status messages.
