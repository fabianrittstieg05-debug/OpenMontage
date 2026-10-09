"""Torch device selection for the local GPU tools.

Extracted from the former `tools/video/_shared.py`, which was 795 lines of
provider plumbing for cloud and diffusion video generators. Those tools are
gone; `get_torch_device()` was the only piece the surviving GPU tools
(`upscale`, `face_restore`) still needed, so it lives here on its own rather
than keeping the module — and its HeyGen/fal/Modal credentials — alive for it.
"""

from __future__ import annotations


def get_torch_device() -> str:
    """Return best available torch device: cuda > mps (Apple Silicon Metal) > cpu.

    Priority order:
      1. cuda  — NVIDIA GPU (fastest for most models)
      2. mps   — Apple Silicon Metal (M1/M2/M3/M4/M5, macOS >= 12.3)
      3. cpu   — fallback, always available but slow

    MPS detection is guarded for torch builds that lack ``torch.backends.mps``
    (e.g. older pip wheels or Linux builds).  We check both build-time support
    (``is_built()``) and runtime availability (``is_available()``).
    """
    try:
        import torch as _torch  # noqa: PLC0415
    except ImportError:
        return "cpu"
    if _torch.cuda.is_available():
        return "cuda"
    # Guard: torch.backends.mps may not exist on older/non-macOS builds
    try:
        mps_backend = getattr(_torch, "backends", None)
        mps_backend = getattr(mps_backend, "mps", None) if mps_backend else None
        if mps_backend is not None:
            # Check build-time support first, then runtime availability
            is_built = getattr(mps_backend, "is_built", lambda: True)()
            is_available = getattr(mps_backend, "is_available", lambda: False)()
            if is_built and is_available:
                return "mps"
    except Exception:
        pass
    return "cpu"
