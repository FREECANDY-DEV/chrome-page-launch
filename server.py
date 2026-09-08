#!/usr/bin/env python3
"""On each visit, open a visible terminal that launches a new Chrome."""

import os
import subprocess
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8765
HOST = "127.0.0.1"
COUNT_FILE = Path("/tmp/chrome-from-page-count")
LOCK = threading.Lock()
LAST_LAUNCH = 0.0
# Collapse a double-fetch from one load, not a human refresh.
DEBOUNCE_S = 1.0


def next_id():
    with LOCK:
        n = 1
        if COUNT_FILE.exists():
            try:
                n = int(COUNT_FILE.read_text().strip() or "0") + 1
            except ValueError:
                n = 1
        COUNT_FILE.write_text(str(n))
        return n


def launch_from_terminal():
    global LAST_LAUNCH
    now = time.time()
    with LOCK:
        if now - LAST_LAUNCH < DEBOUNCE_S:
            return False
        LAST_LAUNCH = now
    n = next_id()
    env = os.environ.copy()
    env["DISPLAY"] = env.get("DISPLAY") or ":7"
    script = ROOT / "open-chrome.sh"
    subprocess.Popen(
        [
            "xfce4-terminal",
            "--display",
            env["DISPLAY"],
            "--geometry",
            "78x14+16+16",
            "--title",
            f"Chrome launch {n}",
            "--hold",
            "-x",
            "bash",
            str(script),
            str(n),
        ],
        cwd="/tmp",
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return n


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            launched = launch_from_terminal()
            self.log_message("visit %s launched=%s", path, launched)
        return super().do_GET()

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args), flush=True)


def main():
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"serving http://{HOST}:{PORT}/", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
