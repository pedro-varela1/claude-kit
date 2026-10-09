"""Link this kit into ~/.claude so every Claude Code session uses it.

Run it once after cloning, and again whenever settings.json or the list of skills changes.
Edits to existing files need no reinstall: everything is linked, not copied.
"""

import json
import os
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
DEFAULT_HOME = Path.home() / ".claude"
HOME = Path(os.environ.get("CLAUDE_CONFIG_DIR", DEFAULT_HOME)).expanduser().resolve()


def link(target: Path, link_path: Path) -> None:
    if link_path.is_symlink():
        link_path.unlink()
    elif link_path.exists():
        sys.exit(f"install: {link_path} exists and is not a link; move it away and run again")
    link_path.parent.mkdir(parents=True, exist_ok=True)
    link_path.symlink_to(target, target_is_directory=target.is_dir())


def link_skills() -> None:
    skills = HOME / "skills"
    for entry in skills.glob("*"):
        if entry.is_symlink() and not entry.exists() and KIT in Path(os.readlink(entry)).parents:
            entry.unlink()
    for skill in sorted((KIT / "skills").iterdir()):
        if (skill / "SKILL.md").is_file():
            link(skill, skills / skill.name)


def import_instructions() -> None:
    memory = HOME / "CLAUDE.md"
    line = f"@{HOME / 'kit' / 'CLAUDE.md'}"
    text = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if line not in text.splitlines():
        separator = "\n" if text and not text.endswith("\n") else ""
        memory.write_text(f"{text}{separator}{line}\n", encoding="utf-8")


def merge(base, extra):
    if isinstance(base, dict) and isinstance(extra, dict):
        merged = dict(base)
        for key, value in extra.items():
            merged[key] = merge(base[key], value) if key in base else value
        return merged
    if isinstance(base, list) and isinstance(extra, list):
        return base + [item for item in extra if item not in base]
    return extra


def kit_settings() -> dict:
    text = (KIT / "settings.json").read_text(encoding="utf-8")
    if HOME != DEFAULT_HOME:
        text = text.replace("$HOME/.claude", str(HOME)).replace("~/.claude", f"/{HOME}")
    return json.loads(text)


def merge_settings() -> None:
    path = HOME / "settings.json"
    current = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    backup = path.with_name("settings.before-kit.json")
    if path.exists() and not backup.exists():
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.write_text(json.dumps(merge(current, kit_settings()), indent=2) + "\n", encoding="utf-8")


def main() -> None:
    link(KIT, HOME / "kit")
    link(KIT / "rules", HOME / "rules" / "kit")
    link_skills()
    import_instructions()
    merge_settings()
    print(f"Kit at {KIT} is linked into {HOME}. Start a new Claude Code session to load it.")


if __name__ == "__main__":
    main()
