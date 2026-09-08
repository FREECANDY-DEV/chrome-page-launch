#!/usr/bin/env python3
"""Serve the notes page. Visiting it asks this computer to open the terminal."""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8765
HOST = "127.0.0.1"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self.log_message("visit %s from %s", path, self.client_address[0])
            return self.serve_notes()
        return super().do_GET()

    def serve_notes(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        tag = '<script src="/visitor-gui.js" defer></script>\n'
        if "</body>" in html:
            html = html.replace("</body>", tag + "</body>", 1)
        else:
            html += tag
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args), flush=True)


def main():
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"serving http://{HOST}:{PORT}/", flush=True)
    print("Register once on this computer: ./register-handler.sh", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
