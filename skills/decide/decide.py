"""Serve one decision round in the browser and record Pedro's answers.

Usage: python3 decide.py <round.json> [--no-browser]

Prints `open <url>` when the page is ready and `answered <record.md>` after submission, then exits.
The answers are written into the round file and rendered as a Markdown record next to it.
"""

import json
import sys
import threading
import webbrowser
import zlib
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PAGE = Path(__file__).with_name("page.html")
VENDOR = Path(__file__).with_name("vendor")
PLACEHOLDER = "/*ROUND*/"
CONTENT_TYPES = {".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2"}
PORT_RANGE = (49152, 16384)


def fail(message: str) -> None:
    sys.exit(f"decide: {message}")


def load_round(path: Path) -> dict:
    if not path.is_file():
        fail(f"round file not found: {path}")
    round_ = json.loads(path.read_text(encoding="utf-8"))
    if "answers" in round_:
        fail(f"{path.name} is already answered; start a new round")
    for key in ("id", "title", "questions"):
        if key not in round_:
            fail(f"round is missing '{key}'")
    question_ids = [q["id"] for q in round_["questions"]]
    if len(set(question_ids)) != len(question_ids):
        fail("question ids must be unique")
    for q in round_["questions"]:
        if not q.get("options"):
            fail(f"question '{q['id']}' has no options")
        if sum(bool(o.get("recommended")) for o in q["options"]) > 1:
            fail(f"question '{q['id']}' recommends more than one option")
    return round_


def validate_answers(round_: dict, answers: dict) -> None:
    for q in round_["questions"]:
        given = answers["questions"].get(q["id"], {})
        valid = {o["id"] for o in q["options"]}
        selected = given.get("selected", [])
        if not set(selected) <= valid:
            raise ValueError(f"unknown option in '{q['id']}'")
        if not selected and not given.get("notes", "").strip():
            raise ValueError(f"question '{q['id']}' needs an option or a note")


def render_record(round_: dict) -> str:
    answers = round_["answers"]
    lines = [f"# {round_['id']} · {round_['title']}", "", f"_{answers['submitted_at']}_", ""]
    if round_.get("context"):
        lines += [round_["context"], ""]
    for q in round_["questions"]:
        given = answers["questions"][q["id"]]
        chosen = set(given.get("selected", []))
        lines += [f"## {q['title']}", ""]
        if q.get("explanation"):
            lines += [q["explanation"], ""]
        for o in q["options"]:
            marks = ""
            if o.get("recommended"):
                marks += " (recommended)"
            if o["id"] in chosen:
                marks += " **← chosen**"
            lines.append(f"- **{o['label']}**{marks}: {o.get('summary', '')}")
            if o.get("details"):
                lines += ["", *[f"  {line}" for line in o["details"].splitlines()], ""]
        if lines[-1]:
            lines.append("")
        if given.get("notes", "").strip():
            lines += [f"**Notes:** {given['notes'].strip()}", ""]
    if answers.get("comments", "").strip():
        lines += ["## Comments", "", answers["comments"].strip(), ""]
    return "\n".join(lines)


def bind(path: Path, handler: type[BaseHTTPRequestHandler]) -> ThreadingHTTPServer:
    # A port derived from the round keeps the page origin, and so the saved draft, across restarts.
    start, size = PORT_RANGE
    try:
        return ThreadingHTTPServer(
            ("127.0.0.1", start + zlib.crc32(str(path).encode()) % size), handler
        )
    except OSError:
        return ThreadingHTTPServer(("127.0.0.1", 0), handler)


def serve(path: Path, open_browser: bool) -> None:
    round_ = load_round(path)
    payload = json.dumps(round_, ensure_ascii=False).replace("</", "<\\/")
    page = PAGE.read_text(encoding="utf-8").replace(PLACEHOLDER, payload).encode()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if not self.path.startswith("/vendor/"):
                self.reply(200, page, "text/html; charset=utf-8")
                return
            asset = (VENDOR / self.path.removeprefix("/vendor/")).resolve()
            if asset.is_relative_to(VENDOR) and asset.is_file():
                self.reply(
                    200,
                    asset.read_bytes(),
                    CONTENT_TYPES.get(asset.suffix, "application/octet-stream"),
                )
            else:
                self.reply(404, b"", "text/plain")

        def do_POST(self) -> None:
            try:
                body = self.rfile.read(int(self.headers["Content-Length"]))
                answers = json.loads(body)
                validate_answers(round_, answers)
            except (ValueError, KeyError, TypeError) as error:
                self.reply(400, json.dumps({"error": str(error)}).encode(), "application/json")
                return
            answers["submitted_at"] = datetime.now().astimezone().isoformat(timespec="minutes")
            round_["answers"] = answers
            path.write_text(
                json.dumps(round_, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            record = path.with_suffix(".md")
            record.write_text(render_record(round_), encoding="utf-8")
            self.reply(200, b'{"ok": true}', "application/json")
            print(f"answered {record}", flush=True)
            threading.Thread(target=server.shutdown, daemon=True).start()

        def reply(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_) -> None:
            pass

    server = bind(path, Handler)
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"open {url}", flush=True)
    if open_browser:
        webbrowser.open(url)
    server.serve_forever()


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        fail("usage: decide.py <round.json> [--no-browser]")
    try:
        serve(Path(args[0]).resolve(), open_browser="--no-browser" not in sys.argv)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
