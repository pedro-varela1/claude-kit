"""PreToolUse hook: stop shell commands from writing into details/.

Edits there must go through Edit or Write, where the `ask` permission rule makes Pedro approve them.
LaTeX builds are left to their own `ask` rules, and copying the kit's template creates details/.
"""

import json
import re
import sys

PATH = r"""['"]?(?:\S*/)?details(?![\w.-])(?:/\S*)?"""
WRITES = [
    re.compile(rf">>?\s*{PATH}"),
    re.compile(rf"\b(?:tee|cp|mv|rm|rmdir|touch|mkdir|ln|rsync|install|truncate)\b[^|;&]*\s{PATH}"),
    re.compile(rf"\bsed\s+(?:-\w*\s+)*-i\b[^|;&]*\s{PATH}"),
]
ALLOWED = re.compile(r"^\s*(?:latexmk|lualatex|xelatex|pdflatex)\b|skills/details/template")
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
