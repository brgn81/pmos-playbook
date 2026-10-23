"""Layout checks of the Playbook that `pmos playbook validate` does not make.

Skills, agents and commands carry a name and a description, a skill's name is its folder, and every
reference between files resolves: skill and rule paths, relative links, agent names, slash commands.

Run with `uv run scripts/check_layout.py [root]`. Exit 0 clean, 1 findings.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Commands PMOS generates in the workspace; they have no file in this repository.
GENERATED_COMMANDS = {"pull", "push", "status"}
FENCE = re.compile(r"```.*?```", re.DOTALL)


def frontmatter(text: str) -> Optional[Dict[str, str]]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    return {key: value.strip().strip("\"'") for key, value in re.findall(r"^(\w+):\s*(.*)$", match.group(1), re.MULTILINE)}


def check(root: Path) -> List[str]:
    findings: List[str] = []
    skills: Dict[str, Path] = {}
    agents: Dict[str, Path] = {}
    commands = {path.stem for path in root.glob("commands/*.md")} | GENERATED_COMMANDS

    def need(path: Path, fields: Tuple[str, ...]) -> Optional[Dict[str, str]]:
        data = frontmatter(path.read_text(encoding="utf-8"))
        if data is None:
            findings.append(f"{path.relative_to(root)}: no frontmatter")
            return None
        for field in fields:
            if not data.get(field):
                findings.append(f"{path.relative_to(root)}: frontmatter has no {field}")
        return data

    for path in sorted(root.glob("skills/*/*/SKILL.md")):
        data = need(path, ("name", "description"))
        if data and data.get("name"):
            if data["name"] != path.parent.name:
                findings.append(f"{path.relative_to(root)}: name '{data['name']}' is not the folder '{path.parent.name}'")
            if data["name"] in skills:
                findings.append(f"{path.relative_to(root)}: duplicate skill name, also {skills[data['name']].relative_to(root)}")
            skills[data["name"]] = path
    for path in sorted(root.glob("agents/*.md")):
        data = need(path, ("name", "description"))
        if data and data.get("name") and data["name"] != path.stem:
            findings.append(f"{path.relative_to(root)}: name '{data['name']}' is not the file name")
        agents[path.stem] = path
    for path in sorted(root.glob("commands/*.md")):
        need(path, ("description",))

    files = [root / "playbook.md"] + sorted(root.glob("agents/*.md")) + sorted(root.glob("commands/*.md"))
    files += sorted(root.glob("rules/*.md")) + sorted(root.glob("skills/**/*.md"))
    for path in files:
        if not path.is_file():
            continue
        name = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        prose = FENCE.sub("", text)
        for pack, skill in re.findall(r"\.claude/skills/([\w-]+)/([\w-]+)/SKILL\.md", text):
            if not (root / "skills" / pack / skill / "SKILL.md").is_file():
                findings.append(f"{name}: no skill {pack}/{skill}")
        for rule in re.findall(r"\.claude/rules/([\w-]+\.md)", text):
            if not (root / "rules" / rule).is_file():
                findings.append(f"{name}: no rule {rule}")
        for target in re.findall(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)", prose):
            target = target.split("#")[0]
            if target and not (path.parent / target).resolve().exists():
                findings.append(f"{name}: broken link {target}")
        if path.parent.name == "agents":
            for agent in re.findall(r"`([a-z]+(?:-[a-z]+)*-helper|product-explainer|pm-agent)`", text):
                if agent not in agents:
                    findings.append(f"{name}: no agent {agent}")
        for command in re.findall(r"(?<![\w/.:<`-])/([a-z][a-z-]+)(?![\w/.-])", prose):
            if command not in commands:
                findings.append(f"{name}: no command /{command}")
    return findings


def main(argv: List[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    findings = check(root)
    for finding in findings:
        print(finding)
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
