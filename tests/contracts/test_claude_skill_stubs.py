"""`.claude/skills/` must stay a thin pointer layer over `.agents/skills/`.

`.agents/skills/` is the canonical Layer 3 store: `tools/base_tool.py` documents
`agent_skills` against it, `test_agent_skill_pointers.py` resolves pointers
against it, and `npx skills add` writes into it. Claude Code only auto-discovers
skills under `.claude/skills/<name>/SKILL.md`, so that directory has to exist
too -- but it holds one generated stub per skill, not a second copy of the tree.

This used to be a full copy of 428 files, and it had already rotted in exactly
the way a silent copy does:

- `ai-video-gen` lost the Kling official direct API from its description, so the
  text Claude matches on to decide *whether to trigger the skill* no longer
  mentioned a provider the repo supports.
- `elevenlabs` lost the whole "OpenMontage provider routing" section, including
  the shared-installation rule never to tell a user to paste a credential.

Nothing detected either one. These tests are that detector. The frontmatter
check is the load-bearing one: frontmatter is what Claude Code reads to decide
when to invoke a skill, so a stub whose frontmatter has drifted from its
canonical source is a skill that triggers on stale terms.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "sync_claude_skills.py"
CANONICAL_ROOT = REPO_ROOT / ".agents" / "skills"
EXPOSED_ROOT = REPO_ROOT / ".claude" / "skills"


def _load_sync_module():
    """Import the generator so the rule lives in one place, not two."""
    spec = importlib.util.spec_from_file_location("sync_claude_skills", SCRIPT_PATH)
    assert spec and spec.loader, f"cannot load {SCRIPT_PATH}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SYNC = _load_sync_module()
EXPOSED_SKILLS: dict[str, str] = SYNC.EXPOSED_SKILLS
ROSTER = sorted(EXPOSED_SKILLS.items())


def test_roster_is_not_empty() -> None:
    """Guard against the parametrized tests below silently covering nothing."""
    assert EXPOSED_SKILLS


def test_exposed_directories_match_the_roster() -> None:
    """A stray directory is either an undeclared skill or returning duplication."""
    on_disk = {p.name for p in EXPOSED_ROOT.iterdir() if p.is_dir()}
    assert on_disk == set(EXPOSED_SKILLS), (
        "`.claude/skills/` does not match EXPOSED_SKILLS in "
        "scripts/sync_claude_skills.py.\n"
        f"  only on disk: {sorted(on_disk - set(EXPOSED_SKILLS))}\n"
        f"  only in roster: {sorted(set(EXPOSED_SKILLS) - on_disk)}"
    )


@pytest.mark.parametrize(("directory", "canonical"), ROSTER, ids=lambda v: str(v))
def test_canonical_skill_exists(directory: str, canonical: str) -> None:
    assert (CANONICAL_ROOT / canonical / "SKILL.md").exists(), (
        f".claude/skills/{directory} points at .agents/skills/{canonical}, "
        "which does not exist"
    )


@pytest.mark.parametrize(("directory", "canonical"), ROSTER, ids=lambda v: str(v))
def test_stub_frontmatter_matches_canonical(directory: str, canonical: str) -> None:
    """The trigger surface must be byte-identical to the canonical skill.

    This is the check that `ai-video-gen` and `elevenlabs` would have failed.
    """
    stub = EXPOSED_ROOT / directory / "SKILL.md"
    assert stub.exists(), f".claude/skills/{directory}/SKILL.md is missing"

    canonical_frontmatter = SYNC.read_frontmatter(CANONICAL_ROOT / canonical / "SKILL.md")
    stub_frontmatter = SYNC.read_frontmatter(stub)

    assert stub_frontmatter == canonical_frontmatter, (
        f".claude/skills/{directory}/SKILL.md frontmatter has drifted from "
        f".agents/skills/{canonical}/SKILL.md. Claude Code triggers on this text.\n"
        "Run: python scripts/sync_claude_skills.py"
    )


@pytest.mark.parametrize(("directory", "canonical"), ROSTER, ids=lambda v: str(v))
def test_stub_routes_to_the_canonical_skill(directory: str, canonical: str) -> None:
    """An agent that opens the stub has to be sent to the real instructions."""
    body = (EXPOSED_ROOT / directory / "SKILL.md").read_text(encoding="utf-8")
    assert f".agents/skills/{canonical}/SKILL.md" in body, (
        f".claude/skills/{directory}/SKILL.md does not point at its canonical skill"
    )


@pytest.mark.parametrize(("directory", "canonical"), ROSTER, ids=lambda v: str(v))
def test_stub_is_the_only_file_in_its_directory(directory: str, canonical: str) -> None:
    """Re-copying `references/`, `rules/` or `examples/` here is the old bug."""
    extra = sorted(
        p.relative_to(EXPOSED_ROOT / directory).as_posix()
        for p in (EXPOSED_ROOT / directory).rglob("*")
        if p.is_file() and p.name != "SKILL.md"
    )
    assert not extra, (
        f".claude/skills/{directory} has files beyond SKILL.md: {extra}\n"
        f"Bundled resources belong only in .agents/skills/{canonical}/."
    )


def test_generator_reports_in_sync() -> None:
    """Belt and braces: the generator's own --check must pass."""
    problems: list[str] = []
    for directory, canonical in ROSTER:
        expected = SYNC.render_stub(directory, canonical)
        actual = (EXPOSED_ROOT / directory / "SKILL.md").read_text(encoding="utf-8")
        if actual != expected:
            problems.append(directory)
    assert not problems, (
        f"stubs differ from generator output: {problems}\n"
        "Run: python scripts/sync_claude_skills.py"
    )
