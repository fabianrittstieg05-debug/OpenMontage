---
description: Set up OpenMontage and show what it can make. Run this first in a fresh clone — it checks the environment, offers the few local installs that unlock more tools, and hands you starter prompts that work on your machine.
argument-hint: (no arguments)
---

Onboard this user. Read `skills/meta/onboarding.md` and follow it — it owns the
protocol. This command exists so onboarding has a reliable trigger instead of
depending on you guessing that a first message was "vague enough".

Hold to these, which the skill expands on:

1. **Check the environment before saying anything about capability.**

   ```bash
   python -c "
   from tools.tool_registry import registry
   import json
   registry.discover()
   print(json.dumps(registry.provider_menu_summary(), indent=2))
   "
   ```

   Never paste `support_envelope()` into chat — it is megabytes of JSON.

2. **Lead with determinism.** The first thing a new user should understand is
   that every render here is reproducible: the same project produces the same
   frames, offline, at no cost. That is the reason to use this over a prompt box.

3. **Never mention API keys.** There are none. If they ask for AI-generated
   footage, say plainly that this toolkit does not generate video or images, then
   show what it does instead — code-driven motion graphics, kinetic typography,
   data visualisation, Manim, procedural 3D, screen demos, character animation.

4. **At most three questions.** The default path needs no decisions at all.
   Detect the GPU rather than asking:

   ```bash
   nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
   ```

   Only offer GPU extras (`make install-gpu` → `upscale`, `face_restore`) when
   that reports ≥6 GB. Ask only if the command fails.

5. **Offer the local installs that actually unlock something**, with consent
   before running anything. Each is one line:

   | Missing | Command | Unlocks |
   |---|---|---|
   | `transcriber` | `pip install faster-whisper` | captions and subtitles |
   | `video_downloader` | `pip install yt-dlp` | reference-video workflow |
   | `math_animate` | `pip install manim` | mathematical animation |
   | a Piper voice | `python -m piper.download_voices en_US-lessac-medium` | narration |
   | `music_library` | drop an audio file into `music_library/` | your own music |

   Say what each costs in time and disk. Do not nag if declined — proceed with
   the best available path.

6. **Finish with three starter prompts** that work on *this* machine, each
   targeting a different pipeline, formatted as blockquotes so they are easy to
   copy. Then stop and let the user choose. Do not start producing.

End by pointing at `AGENT_GUIDE.md` for anyone who wants the full contract, and
`docs/TOOLS.md` for the tool inventory.
