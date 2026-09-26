"""Local board. Scanning happens in-process, so the page spends no Bobcoins."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from aftershock.report import build_report, repo_root


def _page() -> bytes:
    return _static_page().read_bytes()


def _static_page():
    return repo_root() / "aftershock" / "static" / "index.html"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/report":
            payload = json.dumps(build_report().to_dict()).encode("utf-8")
            self._send(200, "application/json; charset=utf-8", payload)
            return
        if path in ("/", "/index.html"):
            self._send(200, "text/html; charset=utf-8", _page())
            return
        self._send(404, "text/plain; charset=utf-8", b"not found\n")

    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        return


class BoardServer(ThreadingHTTPServer):
    allow_reuse_address = True


def make_server(host: str, port: int) -> BoardServer:
    return BoardServer((host, port), Handler)


def serve(host: str, port: int) -> None:
    server = make_server(host, port)
    print(f"Aftershock board at http://{host}:{port}")
    print("Scan stays on this machine. Bobcoins spent by the board: 0")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()
