# Shot Vocabulary

A shared vocabulary for describing a shot: framing, camera movement, height,
angle, point of view, lighting, optics, transitions, and style.

Used by the scene directors, `skills/creative/storytelling.md` and
`skills/meta/video-reference-analyst.md` so that a beat, a scene plan, and a
reference analysis all name the same things the same way.

**This is for describing shots you build**, not for prompting a generative
model — there is no video or image generation in this project. Use these terms
to specify a HyperFrames or Remotion camera move, a `threejs_world` fly-through,
a Blender camera path, or the framing of supplied footage. The five aspects
(subject, scene, camera, lighting, motion) come from the CMU/Harvard CHAI study
on precise video language and remain the canonical breakdown.

## Camera Shot Types

| Shot | When to Use |
|------|-------------|
| **Wide / establishing shot** | Open a scene, show location context |
| **Full / long shot** | Subject head-to-toe with environment |
| **Medium shot** | Waist up, balances detail with context |
| **Medium close-up** | Chest up, conversational intimacy |
| **Close-up** | Face or key object, emphasize emotion |
| **Extreme close-up** | Isolated detail (eye, drop, texture) |
| **Over-the-shoulder** | Conversation framing, connection |
| **Point-of-view (POV)** | Viewer becomes the character |
| **Bird's-eye / top-down** | Map-like overview, omniscient feel |
| **Worm's-eye view** | Looking straight up, emphasize height |
| **Dutch / canted angle** | Tilted horizon, unease or tension |
| **Low-angle** | Subject appears powerful, dominant |
| **High-angle** | Subject appears small, vulnerable |


## Camera Movements

The paper shows current models confuse translation, rotation, and lens-only changes — group your prompts so the model can't conflate them:

| Group | Primitives | Rule |
|---|---|---|
| **Translation** (camera physically moves) | dolly in/out, truck left/right, pedestal up/down | "dolly forward toward subject" |
| **Rotation** (camera pivots in place) | pan left/right, tilt up/down, roll CW/CCW | "pan right across the room" |
| **Lens-only** (no camera move) | zoom in/out, rack focus, pull focus, focus tracking | "zoom in" ≠ "dolly in" |
| **Hybrid / signature** | dolly zoom (vertigo), arc/orbit, crane, whip pan, tracking/follow, handheld | "vertigo" only at moments of revelation |
| **Stillness states** | static (NO movement at all — strict), micro-shake, locked-off | "static" requires zero movement, focus change, or zoom |

> **dolly ≠ zoom.** dolly is camera translation; zoom is focal-length change. Models follow whichever token dominates. **pan ≠ truck.** pan rotates, truck translates laterally.

> **Static shot is strict.** A static shot has zero movement, zero focus change, zero zoom. If any of those occur, do NOT write "static camera" — pick the right movement primitive.


## Camera Height (relative to ground)

| Primitive | Example |
|---|---|
| Aerial-level | "drone-altitude wide of the city" |
| Overhead-level | "rooftop height looking across the street" |
| Eye-level | "framed at eye level" |
| Hip-level | "hip-height tracking shot" |
| Ground-level | "low to the ground, ankle height" |
| Water-level | "skimming the water surface" |
| Underwater | "submerged below the surface" |


## Camera Angle (relative to subject)

| Primitive | Definition |
|---|---|
| **Bird's-eye** | strict top-down. Not the same as aerial. |
| High angle | looking down on subject |
| Level angle | camera and subject at same height |
| Low angle | looking up at subject |
| Worm's-eye | looking straight up |
| **Dutch angle (fixed)** | tilted horizon held steady |
| **Dutch angle (rolling)** | horizon tilt changes during shot |

> **bird's-eye = strict top-down. aerial = altitude.** A drone shot at 45° looking down is a high angle from aerial height, NOT bird's-eye.


## Point of View (POV)

| POV | Example |
|---|---|
| First-person | "the camera follows the character's viewpoint as they walk" |
| Drone | "aerial drone footage of city skyline" |
| Over-the-shoulder | "OTS framing of the laptop screen" |
| Top-down oblique | "top-down view of the chess board, tilted slightly" |
| Dashcam | "vehicle dashcam framing of the road" |
| Objective / Neutral | (default — use when no specific POV) |


## Lighting Vocabulary

| Term | Effect |
|------|--------|
| **Natural light** | Soft, realistic (morning sun, overcast, moonlight) |
| **Golden hour** | Warm sunlight, long shadows, romantic |
| **High-key** | Bright, even, cheerful — comedy, lifestyle |
| **Low-key** | Dark, high contrast — thriller, drama |
| **Rembrandt** | Triangle of light on cheek, classic portrait |
| **Film noir** | Deep shadows, stark highlights |
| **Volumetric** | Visible light rays through atmosphere (fog, dust) |
| **Backlighting** | Light behind subject, silhouette effect |
| **Side lighting** | Strong directional, dramatic shadows |
| **Practical lights** | In-frame sources (lamps, candles, neon signs) |
| **Rim / edge light** | Highlights subject outline, separates from background |

**Lighting direction modifiers**: key light, fill light, bounce, rim, spill, negative fill.

**Color temperature**: warm (tungsten, amber), cool (daylight, blue), mixed.


## Lens & Optical Effects

| Effect | Result |
|--------|--------|
| **Wide-angle lens** (24-35mm) | Broader view, exaggerated perspective |
| **Telephoto** (85mm+) | Compressed perspective, subject isolation |
| **Anamorphic** | Stretched aspect, signature lens flares |
| **Lens flare** | Streaks from bright light hitting lens |

### Lens Distortion

The paper distinguishes two primitives that models honor as separate effects — they are NOT interchangeable:

| Primitive | Effect |
|---|---|
| **Fisheye** | extreme curvature, edges bent strongly outward |
| **Barrel** | mild distortion, straight lines bow slightly outward |

### Focus / Depth of Field

| Primitive | Definition |
|---|---|
| Deep focus | everything sharp, FG to BG |
| Shallow DoF | subject sharp, background bokeh |
| Extremely shallow DoF | razor-thin focal plane |
| Rack focus | shifts focus between two subjects mid-shot |
| Pull focus | gradual focus shift (slower than rack) |
| Focus tracking | focus follows a moving subject |

When DoF changes during a shot, label start AND end focal plane (FG/MG/BG/out-of-focus).


## Subject Transitions

When subjects enter, leave, or hand off focus, name the transition explicitly:

| Primitive | When |
|---|---|
| **Subject revealing** | a new subject enters frame (by subject movement OR camera movement) |
| **Subject disappearing** | a subject exits frame |
| **Subject switching** | focus shifts from one subject to another (often via rack focus or camera move) |
| **Complex alternating** | subjects alternate focus multiple times |

Always name the cause: "by subject movement" or "by camera movement". This unlocks reveal-style camerawork in multi-shot prompts.


## Style & Aesthetic References

### Cinematic Styles
- Film noir, period drama, thriller, modern romance
- Documentary, arthouse, experimental film
- Epic space opera, fantasy, horror
- 1970s romantic drama, 90s documentary-style

### Animation Styles
- Studio Ghibli / Japanese anime
- Classic Disney, Pixar-like 3D
- Stop-motion, claymation
- Hand-painted 2D/3D hybrid
- Cel-shaded, low-poly 3D

### Art Movements
- Impressionistic, surrealist, Art Deco, Bauhaus
- Watercolor, charcoal sketch, ink wash
- Graphic novel, blueprint schematic

### Film Stock / Grade
- Kodak warm grade, Fuji cool tones
- 16mm black-and-white, 35mm photochemical contrast
- Vintage grain overlay, halation on speculars
- Teal-and-orange color grade


## Temporal Effects

### Playback Speed

The paper defines six explicit playback-speed primitives. Use the right one — they're not synonymous:

| Primitive | Definition |
|---|---|
| Time-lapse | events significantly faster than real time (clouds racing) |
| Fast-motion | slightly faster than real (1x–3x) |
| Slow-motion | slower than real |
| Stop-motion | frame-by-frame discrete movements |
| Speed-ramp | mix of fast and slow within the same shot |
| Time-reversed | plays in reverse |

### Other Temporal Devices

| Effect | Use |
|--------|-----|
| **Freeze-frame** | Dramatic pause |
| **Rapid cuts** | Energy, urgency |
| **Continuous / long take** | Immersion, tension |
| **Fade in / fade out** | Scene transitions |
| **Match cut** | Visual continuity between scenes |

