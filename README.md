# OpenMontage

**Deterministic video production, driven by an AI agent.**

Motion design here is code. The same project renders the same frames, every
time — offline, with no account, at no cost. You can diff a composition, review
it, and re-render it a year later and get the identical video.

51 tools, all local. No API keys.

## What it does not do

Worth saying up front, because it is the main design decision:

**There is no image generation, video generation, avatar synthesis, voice
cloning, or music generation.** Those were removed deliberately. A single
stochastic asset makes a whole render irreproducible, and reproducibility is the
reason to use this instead of a prompt box.

If you want AI-generated footage, use a different tool. If you want motion
design you can version, review, and rebuild — keep reading.

## What it does do

| | |
|---|---|
| **Composition** | HyperFrames (HTML/CSS/GSAP), Remotion (React), FFmpeg |
| **Kinetic typography** | text as the subject, timed to narration |
| **Data visualisation** | animated charts, KPI grids, stat reveals |
| **Diagrams** | Mermaid flows and architecture, revealed step by step |
| **Mathematical animation** | Manim, 3Blue1Brown style |
| **Narration** | Piper — local, free, and deterministic |
| **Captions** | local transcription, word-level burn-in |
| **Procedural 3D** | Three.js worlds and terrain; Blender for reference-grade |
| **Character animation** | SVG rigs with a pose library and mocap clips |
| **Screen demos** | real capture, or a synthetic terminal |
| **Editing** | cuts, concat, reframe, silence removal, green screen, grading |

## Quick start

**Prerequisites**

- Python 3.10+
- FFmpeg — `brew install ffmpeg` / `sudo apt install ffmpeg`
- Node.js 18+ (22+ for HyperFrames)
- Claude Code

```bash
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
make setup
```

Then open the project in Claude Code and type:

```
/start
```

That checks your environment, offers the few one-line installs that unlock more
tools, and hands you starter prompts that work on your machine. There is no
`.env` to fill in.

Or skip straight to a brief:

```
"Make a 45-second animated explainer about how neural networks learn —
 kinetic typography and diagrams, no stock footage."
```

The agent proposes concepts and a production plan first and waits for your
approval, then produces it stage by stage — script, scene plan, assets, edit,
render — pausing at each creative decision.

> **No `make`?**
> macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt && cd remotion-composer && npm install && cd ..`
> Windows PowerShell: `py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt; cd remotion-composer; npm install; cd ..`

### Optional local installs

Each unlocks more tools. None needs an account.

```bash
pip install faster-whisper                              # captions and subtitles
pip install yt-dlp                                      # reference-video workflow
pip install manim                                       # mathematical animation
python -m piper.download_voices en_US-lessac-medium      # a narration voice
make install-gpu                                        # GPU upscale / face restore
```

Drop royalty-free tracks into `music_library/` for your own background music.

## Pipelines

| Pipeline | Best for |
|---|---|
| `animated-explainer` | a topic → explainer with code-driven visuals |
| `animation` | motion-graphics and animation-first pieces |
| `character-animation` | rigged SVG characters that act |
| `screen-demo` | screen recordings and product walkthroughs |
| `clip-factory` | many short clips from one long source |
| `podcast-repurpose` | highlights and derivatives from an episode |
| `talking-head` | footage-led speaker videos |
| `hybrid` | your footage plus built support visuals |
| `localization-dub` | subtitles and translated narration |

## Watch it happen

The Backlot board shows a production live — stages, script, scene plan, and the
asset filmstrip, straight from disk.

```bash
python -m backlot open <project-id>
```

## Where your work lives

```
projects/<project-id>/
├── artifacts/        # the real source: brief, script, scene_plan, edit_decisions
├── assets/           # canonical media — images, video, audio, music, fonts, brand
├── composition/      # composition source (+ staged asset copies the renderer needs)
├── history/          # superseded checkpoints, archived automatically
└── renders/final.mp4 # the deliverable
```

`projects/` is gitignored on purpose: the artifacts are the source, the render is
build output. Re-render any project from its artifacts.

## How it works

The agent is the intelligence. Python is only tools and persistence.

```
Agent reads a pipeline manifest (YAML) → reads the stage director skill (MD)
→ uses tools (Python) → self-reviews → checkpoints → asks you to approve
```

Three knowledge layers:

| Layer | Location | Answers |
|---|---|---|
| 1 | `tools/` + the registry | what exists, and is it available here |
| 2 | `skills/` | how OpenMontage wants it used |
| 3 | `.agents/skills/` | how the underlying technology works |

Every creative decision is recorded in an append-only `decision_log`, and gated
stages cannot complete without your approval — `lib/checkpoint.py` enforces it.

## Documentation

| | |
|---|---|
| [`AGENT_GUIDE.md`](AGENT_GUIDE.md) | the agent contract — read first |
| [`docs/TOOLS.md`](docs/TOOLS.md) | all 51 tools, generated from the registry |
| [`skills/INDEX.md`](skills/INDEX.md) | which skill to read, and when |
| [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) | architecture and conventions |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | technical deep-dive |

## Testing

```bash
make test             # full suite
make test-contracts   # contract tests only
make lint             # includes the skill-stub drift check
```

No keys needed — there are none.

## Extending it

A new tool must be **deterministic and local**: same inputs, same output, no
account. Inherit `BaseTool`, declare `determinism` and `capability` honestly,
and discovery is automatic. See `skills/meta/capability-extension.md`.

If it calls a cloud API or samples from a model, it does not belong here.

## License

AGPLv3 — see [LICENSE](LICENSE).
