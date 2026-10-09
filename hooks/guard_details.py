"""PreToolUse hook: stop Bash and PowerShell commands from writing into details/.

Edits there must go through Edit or Write, where the `ask` permission rule makes Pedro approve them.
LaTeX builds are left to their own `ask` rules, and copying the kit's template creates details/.
Matching ignores case, as PowerShell and the Windows and macOS file systems do.
"""

import json
import re
import sys

PATH = r"""['"]?(?:\S*[/\\])?details(?![\w.-])(?:[/\\]\S*)?"""
CMDLETS = (
    r"(?:Set|Add|Clear)-Content|Out-File|Tee-Object|(?:Copy|Move|Remove|Rename|New|Set)-Item"
    r"|Expand-Archive|Export-\w+|cpi|mi|ri|rni|ni|si|sc|ac|clc|md|rd|del"
)
DOTNET = (
    r"\[(?:System\.)?IO\.(?:File|Directory)\]::"
    r"(?:Write|Append|Create|Copy|Move|Delete|Replace)\w*\(\s*"
)
WRITES = [
    re.compile(rf">>?\s*{PATH}", re.I),
    re.compile(
        rf"\b(?:tee|cp|mv|rm|rmdir|touch|mkdir|ln|rsync|install|truncate)\b[^|;&]*\s{PATH}", re.I
    ),
    re.compile(rf"\bsed\s+(?:-\w*\s+)*-i\b[^|;&]*\s{PATH}", re.I),
    re.compile(rf"\b(?:{CMDLETS})\b[^|;&]*\s{PATH}", re.I),
    re.compile(rf"{DOTNET}{PATH}", re.I),
]
ALLOWED = re.compile(
    r"^\s*(?:&\s*)?(?:latexmk|lualatex|xelatex|pdflatex)\b|skills[/\\]details[/\\]template", re.I
)
REASON = (
    "details/ is changed only with Edit or Write, after Pedro approves a written change plan "
    "(see /details). Shell writes there are blocked."
)


def main() -> None:
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    if ALLOWED.search(command) or not any(rule.search(command) for rule in WRITES):
        return
    decision = {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": REASON,
    }
    json.dump({"hookSpecificOutput": decision}, sys.stdout)


if __name__ == "__main__":
    main()
