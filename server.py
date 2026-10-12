#!/usr/bin/env python3
"""Static dev server for RC Crawler + a tiny endpoint used once to save terrain preview thumbnails."""
import http.server, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PREVIEWS = os.path.join(ROOT, 'assets', 'previews')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_POST(self):
        m = re.match(r'^/save-preview\?id=([a-z0-9_-]{1,32})$', self.path)
        if not m or self.client_address[0] not in ('127.0.0.1', '::1'):
            self.send_error(404); return
        n = int(self.headers.get('Content-Length', 0))
        if n <= 0 or n > 3_000_000:
            self.send_error(413); return
        data = self.rfile.read(n)
        if not data.startswith(b'\xff\xd8'):
            self.send_error(400); return
        os.makedirs(PREVIEWS, exist_ok=True)
        with open(os.path.join(PREVIEWS, m.group(1) + '.jpg'), 'wb') as f:
            f.write(data)
        self.send_response(204); self.end_headers()

    def log_message(self, *a):
        pass

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5190
    http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
