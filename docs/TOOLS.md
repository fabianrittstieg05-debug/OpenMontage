# Tools

51 tools. Every one runs on your machine, needs no account, and
is reproducible: the same inputs render the same output.

There is no image generation, video generation, avatar synthesis or cloud
inference here. Those were removed deliberately — a single stochastic asset
makes an entire render irreproducible, which is the one property this project
exists to protect. See `AGENT_GUIDE.md` for the rule.

Generated from the registry by `docs/TOOLS.md` regeneration; to see live
status on your machine run:

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu_summary(), indent=2))"
```

`status` below is from a clean checkout — tools marked *needs install* work
once their local dependency is present; none of them need a key.

## Composition & editing

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `auto_reframe` | experimental | available |  |
| `green_screen_composite` | experimental | available |  |
| `green_screen_processor` | experimental | available |  |
| `hyperframes_compose` | beta | available | HTML/CSS/GSAP composition: kinetic typography, product promos, |
| `showcase_card` | experimental | available |  |
| `silence_cutter` | experimental | available |  |
| `video_compose` | experimental | available | Final render for explainer and animation pipelines |
| `video_stitch` | experimental | available |  |
| `video_trimmer` | experimental | available |  |

## Narration

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `piper_tts` | experimental | available | offline narration fallback |
| `tts_selector` | beta | available | preflight tool selection |

## Captions

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `remotion_caption_burn` | experimental | available |  |
| `subtitle_gen` | experimental | available |  |

## Music — your own files

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `music_library` | production | needs install | user-provided, intentional background music |

## Music — search

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `pixabay_music` | experimental | available | quick background music with zero setup (no API key) |

## Code-driven graphics

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `code_snippet` | experimental | available |  |
| `diagram_gen` | experimental | available |  |
| `math_animate` | experimental | needs install |  |

## 3D — procedural worlds

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `threejs_world` | beta | available | Editable cinematic 3D worlds and terrain fly-throughs |

## 3D — rendering

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `blender_world` | beta | needs install | Production-quality world assembly from many generated and lice |

## 3D — asset libraries

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `threejs_asset_catalog` | beta | available | Installing rights-safe GLTF/GLB libraries for detailed Three.j |

## Character animation

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `action_timeline_compiler` | beta | available |  |
| `character_animation_reviewer` | beta | available |  |
| `character_rig_renderer` | beta | available |  |
| `character_spec_generator` | beta | available | Converting approved concepts into structured character_design  |
| `pose_library_builder` | beta | available |  |
| `svg_rig_builder` | beta | available |  |

## Analysis & measurement

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `audio_energy` | production | available | finding where ambient music gets interesting (skip quiet intro |
| `audio_probe` | production | available | getting audio/video duration before composition |
| `composition_validator` | production | available | catching audio-video duration mismatches before render |
| `face_tracker` | experimental | needs install |  |
| `frame_sampler` | experimental | available |  |
| `scene_detect` | experimental | available |  |
| `transcriber` | experimental | needs install |  |
| `transcript_fetcher` | production | needs install | fast YouTube transcript extraction |
| `video_analyzer` | beta | available | comprehensive video analysis |
| `video_understand` | experimental | needs install |  |
| `visual_qa` | experimental | available |  |

## Enhancement

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `bg_remove` | experimental | needs install |  |
| `color_grade` | experimental | available |  |
| `eye_enhance` | experimental | needs install |  |
| `face_enhance` | experimental | available |  |
| `face_restore` | experimental | needs install |  |
| `upscale` | experimental | needs install |  |

## Audio processing

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `audio_enhance` | experimental | available |  |
| `audio_mixer` | experimental | available |  |

## Screen capture

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `cap_recorder` | beta | available | Professional screen recordings with webcam overlay |
| `screen_capture_selector` | beta | available | Choosing between quick FFmpeg recording and polished Cap recor |
| `screen_recorder` | beta | available | Quick screen recording without additional software |

## Source ingest

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `video_downloader` | production | needs install | downloading reference video from URL |

## Publish

| Tool | Stability | Status | Notes |
|---|---|---|---|
| `export_bundle` | beta | available | packaging a finished render for hand-off to any platform |

