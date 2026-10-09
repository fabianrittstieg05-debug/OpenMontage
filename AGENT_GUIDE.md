# OpenMontage — Agent Guide

Start here. This is the complete operating guide and agent contract.

For architecture and conventions see [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md).
For the tool inventory see [`docs/TOOLS.md`](docs/TOOLS.md).

## The rule that defines this project

**Everything here is deterministic. The same project renders the same frames, every time.**

Motion design in OpenMontage is code: an HTML/CSS/GSAP or React composition, a
timing attribute, a seeded procedural world. That makes a video diffable,
reviewable, and re-renderable months later from the artifacts on disk.

There is **no image generation, video generation, avatar synthesis, voice
cloning, music generation, or cloud inference** in this repo. Those were removed
deliberately — a single stochastic asset makes an entire render irreproducible.
All 51 tools run locally, need no account, and cost nothing.

Consequences you must respect:

- **Never suggest adding an API key.** There are none to add. If a user asks for
  AI-generated footage or imagery, say plainly that this toolkit does not do
  that, and offer what it does: code-driven motion graphics, typography, data
  visualisation, procedural 3D, screen capture, character animation.
- **Never fabricate a missing capability.** If a brief needs generated video,
  say so and propose a deterministic treatment instead.
- **Freeze anything fetched from the network.** `pixabay_music` is the one tool
  that reaches the internet. Whatever it returns must be written into
  `projects/<id>/assets/` so the project still renders offline next month.

## First interaction

When the user's first message is vague, exploratory, or asks what you can do
("make me a video", "what can you do?", "start"), run the onboarding skill
**before anything else**:

**Read:** `skills/meta/onboarding.md`

The `/start` command does this for you. It checks the environment, offers the
few local installs that unlock more tools, and presents starter prompts matched
to what actually works.

**Skip onboarding** when the user arrives with a specific, actionable request
("Make a 60-second explainer about black holes"). Go straight to Rule Zero.

## Rule Zero — all production goes through a pipeline

**Every video production request MUST go through the pipeline system.**

1. **Identify the pipeline.** Match the request to one in `pipeline_defs/`. If
   unclear, ask.
2. **Read the manifest.** `pipeline_defs/<pipeline>.yaml` — know the stages,
   tools, and quality gates.
3. **Run preflight.** Discover real tools from the registry (below).
4. **Execute stage by stage.** For EACH stage, read its director skill
   **before** doing any work in that stage.
5. **Read Layer 3 skills before calling a tool** that declares `agent_skills`.

**Do NOT:** write ad-hoc scripts that call tools directly · skip a stage
director skill · bypass preflight, checkpoints, or review.

The intelligence is in the skills, not in improvised code.

## Available pipelines

| Pipeline | Best for | Director skills | Stability |
|---|---|---|---|
| `animated-explainer` | Topic → explainer, code-driven visuals | `skills/pipelines/explainer/` | production |
| `animation` | Motion-graphics and animation-first videos | `skills/pipelines/animation/` | production |
| `character-animation` | SVG rigged characters, reusable acting | `skills/pipelines/character-animation/` | beta |
| `screen-demo` | Screen recordings and walkthroughs | `skills/pipelines/screen-demo/` | production |
| `clip-factory` | Many clips from one long source | `skills/pipelines/clip-factory/` | beta |
| `podcast-repurpose` | Podcast highlights and derivatives | `skills/pipelines/podcast-repurpose/` | beta |
| `talking-head` | Footage-led speaker videos | `skills/pipelines/talking-head/` | beta |
| `hybrid` | Source footage plus support visuals | `skills/pipelines/hybrid/` | production |
| `localization-dub` | Subtitle and translated-narration variants | `skills/pipelines/localization-dub/` | beta |
| `framework-smoke` | Test: minimal 2-stage smoke test | — | test |

Note `animated-explainer` uses the `explainer/` skill directory, not
`animated-explainer/`. The manifest's `skill:` field is authoritative — read it
rather than guessing the path.

> **Beta pipelines** work but have not been fully audited. Say so when a user picks one.

## Preflight — mandatory before creative work

Use `provider_menu_summary()`. It is the human-ready rollup.

```bash
python -c "
from tools.tool_registry import registry
import json
registry.discover()
print(json.dumps(registry.provider_menu_summary(), indent=2))
"
```

**Never dump `support_envelope()` into chat.** It is megabytes of JSON and will
bury the user. Use it only when debugging a specific tool contract.

The summary returns:

- `composition_runtimes` — booleans for `ffmpeg`, `remotion`, `hyperframes`.
- `capabilities[]` — one entry per capability family with configured/total counts.
- `setup_offers[]` — tools one local install away from working.
- `runtime_warnings[]` — surface these to the user verbatim.

Then read the pipeline manifest, check its `required_tools` against the
registry, and report `passed`, `degraded`, or `blocked`.

### What "unavailable" means now

A tool is never unavailable for want of a credential. It is unavailable because
a **local dependency** is missing — and that is usually one command:

| Tool | Needs | Unlocks |
|---|---|---|
| `transcriber` | `pip install faster-whisper` | captions and subtitles |
| `video_downloader` | `pip install yt-dlp` | reference-video workflow |
| `math_animate` | `pip install manim` | mathematical animation |
| `music_library` | one audio file in `music_library/` | your own background music |
| `upscale`, `face_restore` | `make install-gpu` | GPU enhancement |
| `blender_world` | Blender on PATH or `BLENDER_PATH` | 3D world rendering |

Offer these as concrete one-line fixes. If the user declines, proceed with the
best available path and do not nag.

## Tools — 51, all local

**Do not maintain hardcoded tool lists.** Query the registry:

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

Capability families:

| Family | Tools |
|---|---|
`video_post` (9) | `video_compose`, `hyperframes_compose`, `video_stitch`, `video_trimmer`, `silence_cutter`, `auto_reframe`, `green_screen_composite`, `green_screen_processor`, `showcase_card` |
`analysis` (11) | `transcriber`, `transcript_fetcher`, `scene_detect`, `frame_sampler`, `audio_probe`, `audio_energy`, `video_analyzer`, `video_understand`, `visual_qa`, `composition_validator`, `face_tracker` |
`character_animation` (6) | `svg_rig_builder`, `character_spec_generator`, `pose_library_builder`, `action_timeline_compiler`, `character_rig_renderer`, `character_animation_reviewer` |
`enhancement` (6) | `color_grade`, `face_enhance`, `eye_enhance`, `bg_remove`, `upscale`, `face_restore` |
`graphics` (3) | `diagram_gen` (Mermaid), `code_snippet`, `math_animate` (Manim) |
`screen_capture` (3) | `screen_recorder`, `cap_recorder`, `screen_capture_selector` |
`tts` (2) | `piper_tts`, `tts_selector` |
`subtitle` (2) | `subtitle_gen`, `remotion_caption_burn` |
`audio_processing` (2) | `audio_mixer`, `audio_enhance` |
3D (3) | `threejs_world`, `threejs_asset_catalog`, `blender_world` |
Music (2) | `music_library`, `pixabay_music` |
Other (2) | `video_downloader`, `export_bundle` |

### Narration is deterministic

`piper_tts` is the only TTS tool. It runs locally, costs nothing, and declares
`determinism=deterministic`: the same text and voice produce the same audio.

Voices are downloaded per language and live in the repo root:

```bash
python -m piper.download_voices de_DE-thorsten-medium   # or en_US-lessac-medium
```

`piper` resolves voices from the current directory, so run tools from the repo
root. Route through `tts_selector`, which discovers providers from the registry.

### Tool conventions

All tool classes use **PascalCase without a `Tool` suffix** (`VideoCompose`,
`PiperTTS`, `AudioMixer`). Check with `grep "^class " tools/<path>.py`.

All tools are called via `.execute(params_dict)` and return a `ToolResult` with
`.success`, `.data`, `.error` — **not** `.run()`.

## Composition runtimes

`video_compose` has three render engines. The choice is made at proposal and
locked in `edit_decisions.render_runtime`.

| Engine | Used for | Requires |
|---|---|---|
| **FFmpeg** | cuts, concat, trim, subtitle burn | `ffmpeg` (always present) |
| **Remotion** | React composition: text/stat cards, charts, callouts, spring transitions, word-level captions | Node + `remotion-composer/node_modules` |
| **HyperFrames** | HTML/CSS/GSAP: kinetic typography, promos, launch reels, registry blocks, SVG rigs | Node ≥ 22 + ffmpeg + `npx` |

Check availability via `provider_menu_summary()["composition_runtimes"]`.

### Present Both Composition Runtimes (HARD RULE)

When both Remotion and HyperFrames are available, you **MUST present both to the
user** before locking `render_runtime`. You may recommend one with reasoning, but
**silently picking a default is forbidden** — even when a manifest or director
skill suggests one.

For each runtime, give:

1. one sentence on what it is best at for **this specific brief**;
2. one sentence of honest tradeoff (why it might be wrong here);
3. your recommendation and why, tied to the brief's delivery promise.

Then wait for explicit approval. Record the full shortlist — both runtimes plus
any `ffmpeg` option that applies — as `options_considered` in the
`render_runtime_selection` entry in `decision_log`. A decision log with only one
runtime considered when both were available is a CRITICAL reviewer finding.

If only one is available, proceed but say so explicitly ("HyperFrames isn't
installed here; I'm proceeding with Remotion"), and record the unavailable option
as `rejected_because: "runtime not available on this machine"`.

If the locked runtime later becomes unavailable, surface a structured blocker —
never swap silently.

See `skills/core/hyperframes.md` for the Remotion-vs-HyperFrames decision matrix.

### Authoring mode — templated vs atelier

Orthogonal to runtime. Log it as `composition_mode` in `decision_log`.

- **Templated** — assemble stock scene types (`text_card`, `stat_card`,
  `bar_chart`, …) into the `Explainer`/`CinematicRenderer` compositions. Fast,
  reliable, and the reason most videos look alike. Right for batch output,
  localization variants, and quick drafts.
- **Atelier** — hand-author the composition: bespoke scenes, a one-off theme,
  motion written for this piece. **Default to atelier for hero work.** The stock
  scene catalog and registry blocks are off-limits in this mode; read them only
  as a mechanics codex. Route through `skills/meta/taste-direction.md` then
  `skills/meta/bespoke-composition.md`.

Remotion scene types live in `remotion-composer/SCENE_TYPES.md` — that file is
authoritative for `cut.type` values.

## Project structure — where everything goes

Every run creates a workspace under `projects/`. **`projects/` is gitignored**:
artifacts are the source, renders are build output.

```
projects/<project-id>/
├── project.json              # marker the Backlot board reads
├── artifacts/                # the real source of the video
│   ├── research_brief.json   script.json        scene_plan.json
│   ├── asset_manifest.json   edit_decisions.json
│   └── render_report.json    final_review.json
├── checkpoint_<stage>.json   # per-stage state
├── history/                  # superseded checkpoints, archived automatically
├── decision_log.json         # append-only record of every choice
├── events.jsonl              # append-only audit trail
├── assets/                   # CANONICAL media — write originals here
│   ├── images/   video/   audio/   music/
│   └── fonts/    brand/
├── composition/              # composition source + staged asset copies
└── renders/final.mp4         # the deliverable
```

**Naming:** kebab-case from the title (`hidden-math-of-nature`).

At pipeline init, before any stage:

1. `python -c "from lib.checkpoint import init_project; init_project('<id>', title='<Title>', pipeline_type='<pipeline>')"`
2. `python -m backlot open <id>` — opens the live board. If it fails, continue;
   the board observes, it never blocks. This is your only board duty.

### The two asset tiers — read this before writing any file

There are two locations, and the distinction matters:

- **`projects/<id>/assets/` is canonical.** Every tool writes originals here.
  Always pass an explicit `output_path` under this tree. `asset_manifest`
  records these paths. Assets written to the repo root, cwd, or a temp dir are
  invisible to the board and violate the workspace contract.
- **`projects/<id>/composition/assets/` is a staged copy, created for you.**
  HyperFrames resolves `src=` relative to the composition HTML, so every asset
  must physically sit inside the workspace tree.
  `HyperFramesCompose._resolve_and_stage_assets` copies files in automatically
  and records each copy. **Do not hand-place assets here, and do not treat the
  duplicate as a bug** — it is how the renderer resolves paths.

`assets/fonts/` and `assets/brand/` are first-class: real productions need
locked typefaces and brand marks, and freezing them is what makes a project
re-renderable.

This applies to atelier and hand-authored HyperFrames runs too: they still write
the canonical artifacts they have plus checkpoints into `projects/<id>/`. The
board is runtime-agnostic; only runs that skip artifacts get a degraded board.

### Music library

Users drop royalty-free tracks in `music_library/` (gitignored). `music_library`
reports unavailable until the folder holds at least one audio file — `.mp3 .wav
.m4a .aac .flac .ogg .opus .aiff`, subfolders fine. Override the location with
`MUSIC_LIBRARY_DIR`. Check it before `pixabay_music`.

## Orchestrator

You orchestrate the production state machine yourself:

`research -> proposal -> script -> scene_plan -> assets -> edit -> compose`

1. Read the pipeline manifest (`pipeline_defs/*.yaml`) to know the process.
2. Call `checkpoint.get_next_stage()` to find where to resume.
3. Read that stage's director skill to know HOW.
4. Use tools from `tools/` for concrete capabilities.
5. Self-review with `skills/meta/reviewer.md`.
6. Checkpoint per `skills/meta/checkpoint-protocol.md`.
7. Present to the human when `human_approval_default: true`.

Infrastructure: `lib/checkpoint.py` (read/write checkpoints, stage validation),
`lib/pipeline_loader.py` (manifest loading), `tools/cost_tracker.py` (budget —
every tool here is free, so this records time and units, not spend).

**Python is tools plus persistence.** No orchestration logic, creative
decisions, review logic, or checkpoint policy belongs in Python. You make those
decisions, guided by the instructions.

## Music plan

Music matters to a finished video, so surface it at proposal time rather than
discovering a gap at the asset stage. Check in this order:

```bash
python -c "from tools.tool_registry import registry; registry.discover(); print([t.name for t in registry.get_by_capability(\"music_library\")])"
python -c "from tools.tool_registry import registry; registry.discover(); print([t.name for t in registry.get_by_capability(\"music_search\")])"
```

1. **The user's library** — `get_by_capability("music_library")` plus a look in
   `music_library/`. If tracks exist, list them with durations and let the user pick.
2. **Keyless search** — `get_by_capability("music_search")` reaches
   `pixabay_music`. Report the licence, and freeze whatever you fetch into
   `projects/<id>/assets/music/` so the project still renders offline later.
3. **Bring your own** — the user can drop a file into `music_library/`.
4. **No music** — a legitimate choice, especially for short brand pieces.

There is no music generation in this repo. Do not offer it. Record the music
decision in the proposal artifact so the asset director knows what to do.

## Stage Agents

Each stage produces one canonical artifact that is the contract for the next.

| Stage | Canonical output | Quality bar |
|---|---|---|
| `idea` / `proposal` | `brief` / `proposal_packet` | clear hook, platform, duration, tone |
| `script` | `script` | structured sections, valid timing, coherent narration |
| `scene_plan` | `scene_plan` | ordered scenes, timings, asset requirements |
| `assets` | `asset_manifest` | provenance, paths, tool metadata, scene linkage |
| `edit` | `edit_decisions` | concrete cuts, overlays, subtitle/music decisions |
| `compose` | `render_report` | output paths, encoding profile, verification notes |

Rules:

- A `completed` or `awaiting_human` checkpoint must include its canonical artifact.
- Artifacts must validate against `schemas/artifacts/`.
- Media files belong in stage-specific directories, not in artifacts.
- Record seeds and tool versions for reproducibility.

## Human Checkpoint Protocol

Read `skills/meta/checkpoint-protocol.md`.

- `human_approval_default` in the manifest is **binding** — never re-judge it.
  `lib/checkpoint.py` enforces it: a gated stage cannot be written `completed`
  without `human_approved=True`.
- Typically gated: `idea`/`proposal`, `script`, `scene_plan`, **`assets`**
  (review the board's filmstrip before compose locks them in), and `publish`.
  The manifest you loaded is the only authority.
- When approval is required: write the checkpoint `awaiting_human`, present the
  artifact summary, review findings and cost snapshot — then **END YOUR TURN**.
  Doing further pipeline work in the same response is a gate violation.
- **Approval is per-gate.** An early "go ahead" never covers later gates.
  Blanket pre-authorization must be recorded as a `decision_log` entry
  (`category: "approval_policy"`) to count.
- Write `in_progress` on entering each stage; during `assets`/`compose` refresh
  `metadata.partial_progress` after each unit so the board shows live progress.
- Superseded checkpoints archive to `projects/<id>/history/` automatically — a
  stage re-run never destroys history.

## Decision communication

Announce meaningful production decisions before acting. The user should never
have to infer which runtime or treatment was chosen after the fact.

Before a consequential step, state the tool, the runtime or model variant, the
reason, and whether it is a sample or a batch.

**Ask before changing** any major choice: switching runtime, switching from
video-led to still-led treatment, dropping narration or music, or moving from
sample to batch.

**Re-log changed decisions.** `decision_log` is append-only history, not a
scratchpad. When a logged choice changes mid-run, **append a new entry reusing
the same `category` AND `subject`**, moving the superseded option into
`options_considered` with `rejected_because`. The board keys on the
(category, subject) pair and renders the latest as current. Editing a
downstream artifact while leaving the old decision in place is a defect.

**Escalate blockers explicitly:** what was attempted, what failed, whether it is
a tool bug or a design problem, what options exist, which you recommend. Do not
execute a substitute path without approval.

## Reviewer Protocol

`skills/meta/reviewer.md` — advisory, never blocks progression.

Self-review after each stage before checkpointing. Load the stage's
`review_focus` from the manifest. Two rounds maximum, then pass with warnings.
Critical findings → fix and re-review. Suggestions → note and proceed. Playbook
`quality_rules` are constraints, not suggestions.

## Style playbooks

`styles/*.yaml`, validated by `schemas/styles/playbook.schema.json`.

| Playbook | Best for |
|---|---|
| `clean-professional` | corporate, educational, SaaS |
| `premium-minimalist` | investor updates, expert explainers |
| `flat-motion-graphics` | social, TikTok, startups |
| `minimalist-diagram` | technical deep-dives, architecture |
| `anime-ghibli` | illustrative, hand-painted warmth |

Load with `styles/playbook_loader.py` → `load_playbook("clean-professional")`.

For custom, brand, launch, or hero work read `skills/meta/taste-direction.md`
first and carry its `taste_profile` into the proposal.

**Hand-drawn ink/doodle look** → Ink Theater + Ink Puppet
(`skills/creative/ink-theater.md`, `ink-theater/README.md`). A style and
reusable engine, not a pipeline: illustration pieces run on `animation`, a mocap
character runs on `character-animation`. Entry points `/ink-art` (create a
vector doodle) and `/animated-drawing` (animate a supplied drawing). Never
hand-tune character motion — choose named mocap clips.

## Layer map

Three instruction layers, read in this order:

1. **`tools/`** — what exists, availability, runtime, fallbacks. Discover via
   the registry, never by guessing.
2. **`skills/`** — how OpenMontage wants those tools used. Layer 2 tells you
   *what* and *when*.
3. **`.agents/skills/`** — raw technology knowledge (58 skills). Layer 3 tells
   you *how*.

**Prefer skills over source code** for tool usage. Skills exist so you don't
need implementation details in the common case.

**Exception: debugging and audits.** When a skill and a tool disagree, read the
tool source — that is often the only way to catch a stale doc. If you do,
consider updating the skill afterward.

Layer 3 is not optional: before calling a tool that declares `agent_skills`,
read the referenced skill. A tool with `agent_skills = []` has no Layer 3
knowledge to read — that is intentional, not an omission.

### Layer 3 by category

| Category | Skills |
|---|---|
| **Composition** | `remotion`, `remotion-best-practices`, `synthetic-screen-recording`, `website-to-video`, `remotion-to-hyperframes`, `hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-cli`, `hyperframes-creative`, `hyperframes-media`, `hyperframes-registry` |
| **Animation** | `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-utils`, `gsap-react`, `gsap-performance`, `gsap-scrolltrigger`, `gsap-frameworks`, `framer-motion` (Disney's 12 principles), `lottie-bodymovin`, `motion-graphics` |
| **Character animation** | `character-rigging`, `svg-character-animation`, `pose-library-design`, `canvas-procedural-animation`, `character-animation-qa` |
| **3D** | `threejs-fundamentals`, `-geometry`, `-materials`, `-textures`, `-lighting`, `-loaders`, `-animation`, `-shaders`, `-postprocessing`, `-interaction`, `threejs-world-generation` |
| **Visualisation** | `beautiful-mermaid`, `d3-viz`, `manim-composer`, `manimce-best-practices`, `manimgl-best-practices` |
| **Media & capture** | `ffmpeg`, `video-edit`, `video-download`, `video-understand`, `video-toolkit`, `playwright-recording`, `media-use`, `visual-style`, `music-to-video` |
| **Design** | `tailwind-design-system`, `web-design-guidelines`, `vercel-react-best-practices`, `vercel-composition-patterns` |

**Routing files when unsure:** `skills/meta/animation-runtime-selector.md` picks
between Remotion primitives, GSAP plugins, framer-motion, Lottie, Manim and D3.
For screen-recording mode (real capture vs synthetic terminal) read
`pipeline_defs/screen-demo.yaml` plus its idea-director.

## Communication Protocol

Agents coordinate through canonical JSON artifacts, checkpoints, manifests, and
the registry.

- Artifact schemas: `schemas/artifacts/`
- Checkpoint schema: `schemas/checkpoints/checkpoint.schema.json`
- Manifest schema: `schemas/pipelines/pipeline_manifest.schema.json`
- Pipeline manifests: `pipeline_defs/`
- Style playbooks: `styles/*.yaml`
- Tool contract: `tools/base_tool.py`
- Tool registry: `tools/tool_registry.py`
- Stage directors: `skills/pipelines/<dir>/<stage>-director.md`
- Meta skills: `skills/meta/*.md`

Adding a pipeline requires a manifest plus stage director skills. Every
production tool must inherit `BaseTool` and be discovered through the registry,
not ad-hoc imports.

## Quick lookup

| Question | Where |
|---|---|
| What tools exist? | `registry.capability_catalog()` and [`docs/TOOLS.md`](docs/TOOLS.md) |
| Is a tool available here? | `registry.provider_menu_summary()` |
| How does a tool work? | its `usage_location` from the registry |
| How should this stage behave? | `skills/pipelines/<dir>/<stage>-director.md` |
| Checkpoint/review policy? | `skills/meta/` |
| Where do assets go? | "Project structure" above — `projects/<id>/assets/` |

## What not to do

- **Do not suggest API keys, cloud providers, or AI generation.** None exist here.
- **Do not bypass the pipeline.** No ad-hoc scripts calling tools directly.
- **Do not skip a stage director skill** before executing that stage.
- **Do not dump `support_envelope()`** into chat.
- **Do not hand-place files in `composition/assets/`** — staging is automatic.
- **Do not write assets outside `projects/<id>/`.**
- Do not use deleted legacy names such as `tts_cloud`, `tts_engine`, `video_gen`,
  `image_selector`, or `video_selector`.
- Do not begin asset generation before user approval on the production plan.
- Do not hide degraded paths. Record substitutions and blocked options explicitly.
- Do not change runtime or render path without telling the user and getting
  approval when the change is material.
