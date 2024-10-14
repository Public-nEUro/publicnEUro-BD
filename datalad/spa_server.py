import os
from http.server import HTTPServer, SimpleHTTPRequestHandler


class SPARequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        first_part = self.path.split("/")[1]

        if not os.path.exists(first_part):
            self.path = "/index.html"

        return super().do_GET()


os.chdir("/root/repo")
PORT = 3000

with HTTPServer(("", PORT), SPARequestHandler) as httpd:
    print(f"Serving files from /root/repo on port {PORT}")
    httpd.serve_forever()
