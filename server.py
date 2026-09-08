#!/usr/bin/env python3
"""On each visit, open a terminal that runs a GUI ASCII-art message. Windows and Linux."""

import os
import subprocess
import sys
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
# Pause after the page is on screen, then open the terminal.
# Set this to 0 for full power: the visit launches immediately.
LAUNCH_DELAY_S = 1.0


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
    """Open a terminal and run the GUI art script. Linux and Windows."""
    global LAST_LAUNCH
    now = time.time()
    with LOCK:
        if now - LAST_LAUNCH < DEBOUNCE_S:
            return False
        LAST_LAUNCH = now
    n = next_id()
    # Serve the page first. The delay lives on a side thread so the
    # notes page is on screen before the terminal opens.
    threading.Thread(target=_open_terminal, args=(n,), daemon=True).start()
    return n


def _open_terminal(n):
    """Wait LAUNCH_DELAY_S, then open the terminal. Set delay to 0 for full power."""
    if LAUNCH_DELAY_S > 0:
        time.sleep(LAUNCH_DELAY_S)
    script = ROOT / "show-vuln-art.py"
    env = os.environ.copy()
    if sys.platform == "win32":
        # A visible cmd window that stays open and runs the same script.
        bat = ROOT / "show-vuln-art.bat"
        subprocess.Popen(
            ["cmd", "/c", "start", f"vuln part {n}", "cmd", "/k", str(bat)],
            cwd=str(ROOT),
            env=env,
            creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
        )
        return n
    env["DISPLAY"] = env.get("DISPLAY") or ":7"
    subprocess.Popen(
        [
            "xfce4-terminal",
            "--display",
            env["DISPLAY"],
            "--geometry",
            "72x10+16+16",
            "--title",
            f"vuln part {n}",
            "--hold",
            "-x",
            sys.executable,
            str(script),
        ],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return n


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

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
