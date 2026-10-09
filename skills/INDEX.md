# OpenMontage — Skill Index

The map of every instruction file: what to read, and when.

Read [`AGENT_GUIDE.md`](../AGENT_GUIDE.md) first — it is the agent contract.
This index is the lookup table it refers to.

## Knowledge architecture

Three layers, read in this order:

| Layer | Location | Answers | Count |
|---|---|---|---|
| 1 | `tools/` + the registry | What exists, and is it available here? | 51 tools |
| 2 | `skills/` (this tree) | How does OpenMontage want it used? | 46 skills |
| 3 | `.agents/skills/` | How does the underlying technology work? | 58 skills |

Layer 1 is discovered at runtime (`registry.capability_catalog()`), never
hardcoded. Layer 2 tells you *what* and *when*. Layer 3 tells you *how*.

**Everything here is deterministic.** No image generation, video generation,
avatar synthesis, music generation, or cloud inference — see the rule at the top
of `AGENT_GUIDE.md`. If you are looking for a skill about prompting a diffusion
model, it was deliberately removed.

## Pick a skill by what you are doing

| I need to… | Read |
|---|---|
| Orient a new user / answer "what can you do?" | `meta/onboarding.md` (or run `/start`) |
| Turn a vague idea into a brief | `meta/creative-intake.md` |
| Set art direction for hero work — **Taste Direction** | `meta/taste-direction.md` |
| Hand-author a bespoke composition | `meta/bespoke-composition.md` |
| Choose an animation runtime | `meta/animation-runtime-selector.md` |
| Copy a reference video's feel | `meta/video-reference-analyst.md` |
| Direct a narration performance | `meta/voice-performance-director.md` |
| Self-review a stage | `meta/reviewer.md` |
| Know when to pause for a human | `meta/checkpoint-protocol.md` |
| Add a tool or capability | `meta/capability-extension.md`, `meta/skill-creator.md` |

## Core skills (`core/`)

Technology-level usage inside OpenMontage.

| Skill | Covers |
|---|---|
| `hyperframes.md` | HTML/CSS/GSAP composition; the Remotion-vs-HyperFrames decision matrix |
| `remotion.md` | React composition, scene types, props contract |
| `ffmpeg.md` | Cuts, concat, filters, encoding profiles |
| `subtitle-sync.md` | Caption timing and burn-in |
| `whisperx.md` | Local transcription with `transcriber` |
| `color-grading.md` | Grade profiles via `color_grade` |

## Creative skills (`creative/`)

| Skill | Covers |
|---|---|
| `storytelling.md` | Narrative structure and hooks |
| `typography.md` | Type systems, kinetic type |
| `data-visualization.md` | Charts that read at speed |
| `animation-pipeline.md` | Motion-graphics production flow |
| `short-form.md` / `long-form.md` | Platform-specific pacing |
| `sound-design.md` | Music beds, SFX, mix balance |
| `video-editing.md` / `video-stitching.md` | Cuts, assembly, transitions |
| `screen-recording.md` | Real capture vs synthetic terminal |
| `3d-world-generation.md` | Procedural worlds via `threejs_world` |
| `ink-theater.md` | Hand-drawn ink/doodle engine + Ink Puppet mocap |
| `animated-drawing.md` | Animate a supplied drawing |
| `diagram-gen-usage.md` | Mermaid diagrams via `diagram_gen` |
| `manim-usage.md` | Mathematical animation via `math_animate` |
| `scene-detect-usage.md` | Shot boundaries via `scene_detect` |
| `video-understand-usage.md` | Content analysis of existing footage |
| `enhancement-strategy.md` | When to grade, upscale, or restore |
| `upscale-usage.md` / `face-restore-usage.md` / `bg-remove-usage.md` | Specific enhancement tools |

## Pipeline stage directors (`pipelines/`)

**Read the stage's director skill before doing any work in that stage.** The
manifest's `skill:` field is authoritative for the path — the directory name
does not always match the pipeline name.

| Pipeline | Director directory | Stages |
|---|---|---|
| `animated-explainer` | `pipelines/explainer/` | research, idea, proposal, script, scene, asset, edit, compose, publish |
| `animation` | `pipelines/animation/` | research, idea, proposal, script, scene, asset, edit, compose, publish |
| `character-animation` | `pipelines/character-animation/` | research, proposal, script, character-design, rig-plan, scene, asset, edit, compose, publish |
| `screen-demo` | `pipelines/screen-demo/` | idea, script, scene, asset, edit, compose, publish |
| `clip-factory` | `pipelines/clip-factory/` | idea, script, scene, asset, edit, compose, publish |
| `podcast-repurpose` | `pipelines/podcast-repurpose/` | idea, script, scene, asset, edit, compose, publish |
| `talking-head` | `pipelines/talking-head/` | idea, script, scene, asset, edit, compose, publish |
| `hybrid` | `pipelines/hybrid/` | idea, script, scene, asset, edit, compose, publish |
| `localization-dub` | `pipelines/localization-dub/` | idea, script, scene, asset, edit, compose, publish |

Each directory also holds an `executive-producer.md` — the end-to-end view of
that pipeline, useful for understanding how the stages fit together.

The `cinematic`, `avatar-spokesperson` and `documentary-montage` pipelines were
removed along with the generative tools they depended on.

## Capability families

Discover at runtime; never hardcode a tool list.

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

| Family | Count | Notes |
|---|---|---|
| `video_post` | 9 | composition and editing; `video_compose` routes to ffmpeg / Remotion / HyperFrames |
| `analysis` | 11 | transcription, scene detection, probes, QA |
| `character_animation` | 6 | SVG rigs, pose libraries, action timelines |
| `enhancement` | 6 | grade, face/eye enhance, bg removal, upscale, restore |
| `graphics` | 3 | Mermaid, code snippets, Manim |
| `screen_capture` | 3 | ffmpeg capture, Cap, selector |
| `tts` | 2 | `piper_tts` (local, deterministic) + selector |
| `subtitle` | 2 | SRT generation, caption burn |
| `audio_processing` | 2 | mixing, enhancement |
| 3D | 3 | `threejs_world`, `threejs_asset_catalog`, `blender_world` |
| music | 2 | `music_library` (your files), `pixabay_music` (keyless, freeze on fetch) |

### Selector pattern

`tts_selector` and `screen_capture_selector` auto-discover providers via
`registry.get_by_capability(...)`, so adding a provider tool makes it available
through the selector with no selector change.

`image_selector` and `video_selector` were removed: with no providers to route
to, a selector that always reports "nothing configured" is worse than none.

### Adding a tool

Inherit `BaseTool`, declare `capability`, `provider`, `determinism`, `runtime`,
`best_for`, `install_instructions`, and `agent_skills`. Discovery is automatic —
the registry walks the `tools` package. Then read `meta/capability-extension.md`.

A new tool must be **deterministic and local**. If it calls a cloud API or
samples from a model, it does not belong here.

## Style playbooks

`styles/*.yaml`, validated against `schemas/styles/playbook.schema.json`.
Load via `styles/playbook_loader.py` → `load_playbook("clean-professional")`.

| Playbook | Mood | Best for |
|---|---|---|
| `clean-professional` | polished, trustworthy | corporate, educational, SaaS |
| `premium-minimalist` | calm, editorial | investor updates, expert explainers |
| `flat-motion-graphics` | energetic, bold | social, TikTok, startups |
| `minimalist-diagram` | focused, technical | technical deep-dives, architecture |
| `anime-ghibli` | illustrative, warm | hand-painted, story-led pieces |

## Layer 3 skills (`.agents/skills/`)

58 skills, managed with `npx skills add`. That directory is the single source of
truth — `agent_skills` pointers, the registry, and
`tests/contracts/test_agent_skill_pointers.py` all resolve against it.

Claude Code only auto-discovers skills under `.claude/skills/<name>/SKILL.md`, so
30 of them are also exposed there as **generated pointer stubs**: canonical
frontmatter verbatim (so triggering is identical) plus a body routing to
`.agents/skills/<name>/`. They are not symlinks — the desktop app skips
symlinked skill directories, and a Windows checkout without `core.symlinks`
turns them into text files containing a path.

Edit the skill in `.agents/skills/`, never the stub, then:

```bash
python scripts/sync_claude_skills.py          # regenerate
python scripts/sync_claude_skills.py --check  # CI guard; also a contract test
```

To expose another skill, add it to `EXPOSED_SKILLS` in that script and regenerate.

| Category | Skills |
|---|---|
| **Composition** | `remotion`, `remotion-best-practices`, `remotion-to-hyperframes`, `hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-cli`, `hyperframes-creative`, `hyperframes-media`, `hyperframes-registry`, `website-to-video`, `synthetic-screen-recording` |
| **Animation** | `gsap`, `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-utils`, `gsap-react`, `gsap-performance`, `gsap-scrolltrigger`, `gsap-frameworks`, `framer-motion`, `lottie-bodymovin`, `motion-graphics` |
| **Character animation** | `character-rigging`, `svg-character-animation`, `pose-library-design`, `canvas-procedural-animation`, `character-animation-qa` |
| **3D** | `threejs-fundamentals`, `-geometry`, `-materials`, `-textures`, `-lighting`, `-loaders`, `-animation`, `-shaders`, `-postprocessing`, `-interaction`, `threejs-world-generation` |
| **Visualisation** | `beautiful-mermaid`, `d3-viz`, `manim-composer`, `manimce-best-practices`, `manimgl-best-practices` |
| **Media & capture** | `ffmpeg`, `video-edit`, `video-download`, `video-understand`, `video-toolkit`, `playwright-recording`, `media-use`, `visual-style`, `music-to-video` |
| **Design** | `tailwind-design-system`, `web-design-guidelines`, `vercel-react-best-practices`, `vercel-composition-patterns` |

The provider skills that used to sit here (Kling, HeyGen, Seedance, FLUX,
ElevenLabs, Azure, ComfyUI and the rest) were removed with their tools.
