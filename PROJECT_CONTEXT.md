# OpenMontage - Shared Project Context

This is the single source of truth for project architecture and conventions. `CLAUDE.md` points here instead of duplicating this content.

## Identity

OpenMontage is a deterministic, local video production platform.

**The defining constraint:** every tool is reproducible and runs on this
machine. The same project renders the same frames, every time, offline, with
no account. There is no image generation, video generation, avatar synthesis,
music generation, or cloud inference — a single stochastic asset would make an
entire render irreproducible. 51 tools, all local.

## Architecture: Instruction-Driven (Agent-First)

The AI agent IS the intelligence. Python exists only for tools and persistence. Everything else — orchestration, creative decisions, review, stage transitions — lives in instructions (YAML manifests + markdown skills) the agent follows.

```
Agent reads pipeline manifest (YAML) → reads stage director skill (MD)
→ uses tools (Python BaseTool) → self-reviews (meta skill)
→ checkpoints (Python utility) → presents to human for approval
```

**No Python orchestrator, no Python reviewer, no Python handlers.** The agent drives the pipeline.

## Source of Truth

- **Agent guide & contract:** `AGENT_GUIDE.md` (tool inventory, pipeline selection, stage agents, protocols)
- **Skill index:** `skills/INDEX.md`
- **Tool registry:** `tools/tool_registry.py`
- **Pipeline manifests:** `pipeline_defs/`
- **Artifact schemas:** `schemas/artifacts/`
- **Style playbooks:** `styles/*.yaml` (schema: `schemas/styles/playbook.schema.json`)
- **Stage director skills:** `skills/pipelines/<pipeline>/<stage>-director.md`
- **Meta skills:** `skills/meta/*.md` (reviewer, checkpoint-protocol, skill-creator)
- **Architecture deep-dive:** `docs/ARCHITECTURE.md`

## Knowledge Architecture (3 Layers)

```
Layer 1: tools/tool_registry.py     → "What tools exist" (runtime capabilities, status, cost)
Layer 2: skills/                    → "How OpenMontage uses them" (project conventions)
Layer 3: .agents/skills/            → "How the technology works" (generic API rules, skills.sh)
```

Each tool's `agent_skills[]` field bridges Layer 1 → Layer 3. See `skills/INDEX.md` for the full mapping.

## Key Patterns

- **Pipeline state machine:** `idea -> script -> scene_plan -> assets -> edit -> compose -> publish`
- **Instruction-driven stages:** Each stage has a director skill (MD) that teaches the agent HOW
- **Pipeline manifests:** Declarative YAML defining stages, skills, tools, review focus, approval gates
- **Capability-first tool design:** a family with several real backends exposes a
  selector plus concrete tools; a family with one backend does not need a selector
  - Example: `tts_selector` + `piper_tts`
  - Example: `screen_capture_selector` + `screen_recorder` / `cap_recorder`
  - `image_selector` and `video_selector` were removed: with no providers left to
    route to, a selector that always reports "nothing configured" is worse than none
- **Style playbooks:** YAML defining visual language, typography, motion, audio, asset generation constraints
- **Artifacts are canonical:** `brief`, `script`, `scene_plan`, `asset_manifest`, `edit_decisions`, `render_report`, `publish_log`
- **Every tool inherits from `tools/base_tool.py`** (ToolContract)
- **Checkpoint policy** lives in pipeline manifest (`human_approval_default` per stage) + `skills/meta/checkpoint-protocol.md`
- **Reviewer** is a meta skill (`skills/meta/reviewer.md`), advisory, max 2 rounds
- **Cost tracker** (`tools/cost_tracker.py`) records time and units, not spend —
  every tool here is free
- **Canonical artifacts** validated against JSON schemas in `schemas/artifacts/`

## Key Files

| File | Purpose |
|------|---------|
| `config.yaml` | Global configuration |
| `lib/config_model.py` | Runtime config loader (Pydantic) |
| `lib/checkpoint.py` | Checkpoint writer/reader |
| `lib/pipeline_loader.py` | Pipeline manifest loader + helpers |
| `lib/media_profiles.py` | Platform-specific render profiles |
| `styles/playbook_loader.py` | Style playbook loader + validator + design intelligence (color/type/a11y) |
| `tools/base_tool.py` | ToolContract base class |
| `tools/tool_registry.py` | Tool discovery and reporting |
| `tools/cost_tracker.py` | Budget governance |
| `tools/torch_device.py` | Torch device selection (cuda/mps/cpu) for the local GPU tools |
| `tools/video/video_stitch.py` | Multi-clip assembly (stitch, spatial, validate, preview) |
| `tools/video/video_compose.py` | Runtime-aware composition orchestrator — routes to Remotion / HyperFrames / FFmpeg based on `edit_decisions.render_runtime` |
| `tools/video/hyperframes_compose.py` | HyperFrames runtime — templated workspace materialization plus authored-workspace unified `check`/`render`, FFmpeg floor check |
| `tools/graphics/threejs_world.py` | Local semantic 3D-world authoring with explicit blockout/production fidelity tiers, region-aware terrain, diagnostics, and HyperFrames atelier workspaces |
| `tools/graphics/threejs_asset_catalog.py` | CC0 GLTF/GLB catalog acquisition, inventory, and provenance for production-fidelity world builds |
| `tools/graphics/blender_world.py` | Blender 4.5 LTS production world assembly, terrain, lighting, camera, and Eevee Next rendering |
| `tools/character/character_animation.py` | Local character-animation tools — character specs, SVG rig plans, pose libraries, action timelines, HyperFrames packages, and QA reports |
| `lib/hyperframes_style_bridge.py` | Playbook → CSS custom properties + `DESIGN.md` bridge for HyperFrames workspaces |
| `remotion-composer/src/components/` | 8 Remotion components (TextCard, StatCard, ProgressBar, CalloutBox, ComparisonCard + charts/) |
| `.agents/skills/hyperframes*/` | Vendored HyperFrames Layer 3 skills (authoring contract, CLI, registry, website-to-video) |
| `.agents/skills/threejs-world-generation/` | Layer 3 coarse-to-fine semantic world construction and render-guided refinement workflow |
| `skills/core/hyperframes.md` | Layer 2 — when OpenMontage should pick HyperFrames vs Remotion, artifact → workspace mapping |
| `schemas/styles/playbook.schema.json` | Playbook schema v2 with design tokens (chart_palette, scale_system, weight_matrix, color_rules) |
| `tests/qa/` | Quality validation test scripts for tool-by-tool output inspection |

## Available Pipelines

| Pipeline | Manifest | Director skills | Type |
|---|---|---|---|
| `animated-explainer` | `pipeline_defs/animated-explainer.yaml` | `skills/pipelines/explainer/` | Code-driven explainer |
| `animation` | `pipeline_defs/animation.yaml` | `skills/pipelines/animation/` | Animation-first |
| `character-animation` | `pipeline_defs/character-animation.yaml` | `skills/pipelines/character-animation/` | Local rigged character animation |
| `screen-demo` | `pipeline_defs/screen-demo.yaml` | `skills/pipelines/screen-demo/` | Screen recording |
| `clip-factory` | `pipeline_defs/clip-factory.yaml` | `skills/pipelines/clip-factory/` | Short-form batch extraction |
| `podcast-repurpose` | `pipeline_defs/podcast-repurpose.yaml` | `skills/pipelines/podcast-repurpose/` | Podcast repurposing |
| `talking-head` | `pipeline_defs/talking-head.yaml` | `skills/pipelines/talking-head/` | Footage-led |
| `hybrid` | `pipeline_defs/hybrid.yaml` | `skills/pipelines/hybrid/` | Source plus support |
| `localization-dub` | `pipeline_defs/localization-dub.yaml` | `skills/pipelines/localization-dub/` | Subtitles and translated narration |
| `framework-smoke` | `pipeline_defs/framework-smoke.yaml` | — | Test harness |

Note `animated-explainer` uses the `explainer/` skill directory. The manifest's
`skill:` field is authoritative for the path.

`cinematic`, `avatar-spokesperson` and `documentary-montage` were removed along
with the generative tools they depended on.

## Where Assets Go

Two tiers, and the distinction matters:

- **`projects/<id>/assets/`** is canonical. Tools write originals here
  (`images/ video/ audio/ music/ fonts/ brand/`), and `asset_manifest` records
  these paths. Always pass an explicit `output_path` under this tree.
- **`projects/<id>/composition/assets/`** is a staged copy created automatically.
  HyperFrames resolves `src=` relative to the composition HTML, so assets must
  physically sit inside the workspace;
  `HyperFramesCompose._resolve_and_stage_assets` copies them in. Do not
  hand-place files there, and do not treat the duplicate as a bug.

`projects/` is gitignored: artifacts are the source, renders are build output.

## When Building New Pipelines

1. Create a YAML manifest in `pipeline_defs/` (validated by `pipeline_manifest.schema.json`)
2. Create stage director skills in `skills/pipelines/<dir>/` (idea through publish)
3. Reference meta skills (reviewer, checkpoint-protocol) in the manifest
4. Add compatible playbooks to the manifest
5. Add contract tests in `tests/contracts/`

## When Building New Tools

1. Inherit from `tools/base_tool.py` `BaseTool`
2. Put the tool in the correct capability package (`tools/audio/`, `tools/video/`,
   `tools/enhancement/`, `tools/analysis/`, `tools/graphics/`, `tools/character/`,
   `tools/subtitle/`, `tools/capture/`, `tools/publishers/`)
   - **The tool must be deterministic and local.** Declare `determinism`
     accurately; if it calls a cloud API or samples from a model, it does not
     belong in this repo
3. Prefer the selector-plus-provider pattern:
   - one capability router tool for agent convenience
   - one concrete tool per real provider/runtime path
4. Set all contract fields (name, version, tier, capability, provider, supports, fallback_tools, agent_skills, etc.)
5. Implement `execute()` returning a `ToolResult`
6. Let discovery happen through `tools/tool_registry.py`; do not depend on ad hoc imports
7. Add a JSON schema in `schemas/tools/` if the tool has complex I/O
8. Add tests only after the runtime path is correct
