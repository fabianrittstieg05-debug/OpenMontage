# Onboarding — Meta Skill

## When to use

On the **first interaction** when the user has not given a concrete production
request — "make me a video", "what can you do?", "start" — or whenever `/start`
is invoked.

**Skip this** when the user arrives with something actionable ("Make a
60-second explainer about black holes"). They already know what they want: go to
Rule Zero in `AGENT_GUIDE.md`.

Most users do not know what is possible. Your job is to show them fast, in plain
language, and leave the machine better set up than you found it.

## Step 1 — Check the environment

Before saying anything about capability:

```bash
python -c "
from tools.tool_registry import registry
import json
registry.discover()
print(json.dumps(registry.provider_menu_summary(), indent=2))
"
```

**Never dump `registry.support_envelope()` into chat.** It is megabytes of JSON
and will bury the user. The summary above is the human-ready rollup and returns
exactly what you need: `composition_runtimes`, `capabilities[]` with
configured/total counts, `setup_offers[]`, and `runtime_warnings[]`.

Detect the GPU rather than asking:

```bash
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
```

If that fails, assume no usable GPU — do not interrogate the user about hardware.

## Step 2 — Lead with determinism

The first thing to establish is *why* this toolkit is different:

> Every video here is built from code, so the same project renders the same
> frames every time — offline, with no account, at no cost. You can diff a
> composition, review it, and re-render it months later and get the identical
> result.

That is the pitch. It is also a constraint, and you must be honest about it:

- **There is no image generation, video generation, avatar synthesis, voice
  cloning, or music generation.** If the user asks for AI-generated footage, say
  so plainly — do not hedge, and do not imply a key or an upgrade would unlock
  it. Nothing will.
- **Never mention API keys.** There are none in this project.
- Offer the real alternative: code-driven motion graphics, kinetic typography,
  data visualisation, Manim, procedural 3D, screen demos, SVG character
  animation, deterministic narration.

## Step 3 — Report what works, in plain language

Translate the summary into capability, not tool names. Keep it to 8–12 lines.
Lead with what works; never apologise for what is absent.

```
WHAT YOU CAN MAKE RIGHT NOW

  Composition:   HyperFrames (HTML/CSS/GSAP), Remotion (React), FFmpeg
  Narration:     Piper — local, free, deterministic
  Captions:      auto-transcribed and burned in
  Graphics:      Mermaid diagrams, code snippets, Manim
  3D:            procedural Three.js worlds, Blender rendering
  Characters:    SVG rigs with a pose library and mocap clips
  Capture:       screen recording, synthetic terminal demos

  Everything runs on your machine. Nothing needs an account.
```

Name **both** Remotion and HyperFrames explicitly when both are available — a
session that never hears "HyperFrames" will not offer it at proposal time. If
only one is present, say which and what the other would add. If neither, say the
options are FFmpeg-only and what is needed to unlock HTML/React composition.

**Do not pick a runtime during onboarding.** That decision belongs at proposal,
once you understand the brief.

## Step 4 — Offer the installs that unlock something

Each is one line. Ask before running anything, and say what it costs.

| Missing | Command | Unlocks |
|---|---|---|
| `transcriber` | `pip install faster-whisper` | captions and subtitles — usually the biggest gap |
| `video_downloader` | `pip install yt-dlp` | the reference-video workflow |
| `math_animate` | `pip install manim` | mathematical animation |
| a Piper voice | `python -m piper.download_voices en_US-lessac-medium` | narration (~60 MB per voice) |
| `music_library` | drop an audio file into `music_library/` | your own background music |
| `upscale`, `face_restore` | `make install-gpu` | GPU enhancement (multi-GB download; only offer at ≥6 GB VRAM) |

Rules:

- **Three questions maximum.** The default path needs no decisions.
- Read `install_instructions` from the registry rather than hardcoding.
- Piper resolves voices from the current directory, so run from the repo root.
  Pick a voice matching the user's language, not just English.
- If the user declines, proceed with the best available path. Do not nag.

## Step 5 — Three starter prompts

Present exactly three, as blockquotes so they are easy to copy. Each should
target a different pipeline and be achievable with what is actually installed.
The first should be the most impressive thing this setup can produce.

> **Try this:** "Make a 30-second animated explainer about why the sky is blue —
> kinetic typography, no stock footage."
>
> Code-driven scenes with real motion design, narrated with Piper and captioned.
> Renders fully offline. *(animated-explainer)*

> **Also try:** "I have a screen recording of a dashboard workflow — turn it
> into a polished product demo with captions." *(screen-demo)*

> **Or:** "Turn this 40-minute podcast into three short vertical clips."
> *(clip-factory)*

Adapt these to what the environment reports. If `transcriber` is missing, do not
lead with a captions-heavy prompt — offer the install first.

Reference-led work is worth mentioning at any tier:

> **Got a video you like?** Paste a link and say "make me something like this" —
> the reference gets analysed locally for pacing, structure and style, then you
> get two or three differentiated concepts. *(needs `video_downloader`)*

## Step 6 — Explain the flow in three sentences

> When you give me a brief, I'll propose concepts and a production plan first and
> wait for your approval. Then I produce it stage by stage — script, scene plan,
> assets, edit, render — pausing at each creative decision. The finished video
> lands in `projects/<name>/renders/`, and everything it was built from stays in
> `projects/<name>/artifacts/` so it can be re-rendered or changed later.

Do not explain the three-layer architecture or pipeline internals here. Point
the curious at `AGENT_GUIDE.md`.

## Common questions

**"What does it cost?"** — Nothing. No API keys, no metered calls, no accounts.
The only cost is render time on your own machine.

**"How long does it take?"** — A short explainer is roughly 5–15 minutes, most of
it composition and rendering. Research and scripting are fast.

**"Can you make [X]?"** — Match it to a pipeline and say which. If it needs
generated footage or a synthetic presenter, say clearly that this toolkit does
not do that, and suggest the closest deterministic treatment.

**"I just want to test it."** — Suggest the shortest zero-dependency prompt:
"Make a 15-second title card animation for a product called Northwind."

## Anti-patterns

- **Don't dump raw JSON.** Translate the summary into plain language.
- **Don't list every tool.** Group by what the user can make.
- **Don't explain the architecture** unless asked. They came to make a video.
- **Don't apologise for missing capability**, and never imply a key would fix it.
- **Don't suggest an API key, cloud provider, or paid upgrade.** None exist.
- **Don't ask about hardware** you can detect yourself.
- **Don't start producing.** Onboarding ends with the user choosing.
- **Don't skip straight past orientation** when the user seems uncertain —
  30 seconds here saves ten minutes of confusion later.
