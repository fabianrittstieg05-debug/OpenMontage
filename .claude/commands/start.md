---
description: Set up OpenMontage and show what it can make. Run this first in a fresh clone — it installs what's missing, then hands you starter prompts that work on your machine.
argument-hint: (no arguments)
---

Get this user from a fresh clone to making something. Two phases: **bootstrap**,
then **orient**. `skills/meta/onboarding.md` owns the orientation protocol —
read it before phase 2.

This command exists so neither phase depends on guessing. Onboarding used to
fire on a heuristic ("if the first message seems vague"), which silently did not
happen.

## Phase 1 — Bootstrap

Do this before saying anything about capability. **A fresh clone cannot even
list its own tools**: `tools/cost_tracker.py` imports `lib/config_model.py`,
which needs `pydantic`, so `registry.discover()` raises `ModuleNotFoundError`
until dependencies are installed.

**Step 1.** Check the OS-level prerequisites, which the repo cannot install for
the user:

```bash
python3 --version; ffmpeg -version 2>/dev/null | head -1; node --version
```

If any is missing, give the one command for their platform and stop — there is
nothing useful to do until these exist:

| Missing | macOS | Debian/Ubuntu |
|---|---|---|
| FFmpeg | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| Node.js | `brew install node` | `sudo apt install nodejs npm` |
| Python 3.10+ | `brew install python` | `sudo apt install python3 python3-venv` |

**Step 2.** Check whether the project itself is installed:

```bash
.venv/bin/python -c "from tools.tool_registry import registry; registry.discover(); print('ready')" 2>&1 | tail -2
```

If that prints `ready`, skip to Phase 2.

If it fails, say so in one sentence, explain what you are about to install, and
**ask before running it**:

> This clone isn't installed yet. `make setup` creates a virtualenv, installs
> the Python dependencies, and installs the Remotion renderer (~390 MB of
> `node_modules`). Takes a few minutes. Shall I run it?

```bash
make setup
```

Then re-run the Step 2 check and confirm it reports `ready`.

**Why this isn't shipped pre-installed**, if they ask: every dependency that
matters is compiled per platform — `pydantic_core`, `numpy`, `Pillow` and even
`yaml` ship `.so` files built for one OS, one architecture and one Python
version, and Remotion's compositor is a native binary per platform. Committing
them would mean gigabytes of platform-specific binaries in git history that
still break on any combination not anticipated. `.gitignore` records the same
rule for the portable Blender runtime.

**If they only want the HTML/CSS/GSAP path**, the 390 MB Remotion install is
skippable: HyperFrames needs only `npx` and `ffmpeg` and fetches itself on first
use (~20 MB cached). `make install` does the Python side alone. Offer this when
install size matters to them.

## Phase 2 — Orient

Read `skills/meta/onboarding.md` and follow it. The essentials it expands on:

1. **Check what works** — never paste `support_envelope()` into chat; it is
   megabytes of JSON:

   ```bash
   .venv/bin/python -c "
   from tools.tool_registry import registry
   import json
   registry.discover()
   print(json.dumps(registry.provider_menu_summary(), indent=2))
   "
   ```

2. **Lead with determinism.** The first thing a new user should understand is
   that every render is reproducible: the same project produces the same frames,
   offline, at no cost. That is the reason to use this over a prompt box.

3. **Never mention API keys.** There are none. If they ask for AI-generated
   footage, say plainly that this toolkit does not generate video or images, then
   show what it does — code-driven motion graphics, kinetic typography, data
   visualisation, Manim, procedural 3D, screen demos, character animation.

4. **At most three questions.** Detect the GPU rather than asking:

   ```bash
   nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
   ```

   Only offer GPU extras (`make install-gpu` → `upscale`, `face_restore`) at
   ≥6 GB. Ask only if that command fails.

5. **Offer the remaining one-liners**, with consent, and say what each costs.
   `make setup` deliberately cannot pick these:

   | Missing | Command | Unlocks |
   |---|---|---|
   | a Piper voice | `python -m piper.download_voices en_US-lessac-medium` | narration (~60 MB, one per language) |
   | `transcriber` | `pip install faster-whisper` | captions and subtitles |
   | `video_downloader` | `pip install yt-dlp` | reference-video workflow |
   | `math_animate` | `pip install manim` | mathematical animation |
   | `music_library` | drop an audio file into `music_library/` | your own music |

   Pick the voice language from what the user writes in, not automatically
   English. Do not nag if declined — proceed with the best available path.

6. **Finish with three starter prompts** that work on *this* machine, each
   targeting a different pipeline, as blockquotes so they are easy to copy. Then
   stop and let the user choose. Do not start producing.

End by pointing at `AGENT_GUIDE.md` for the full contract and `docs/TOOLS.md`
for the tool inventory.
