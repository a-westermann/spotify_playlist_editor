from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class SpotifyRedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # inherited method
        query_components = parse_qs(urlparse(self.path).query)
        self.server.auth_code = query_components['code'][0]
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>You can close this window now yo</h1></body></html>")
        # self.server.shutdown()


def start_local_server():
    server = HTTPServer(('localhost', 8000), SpotifyRedirectHandler)
    server.auth_code = None
    server.error_message = None
    server.handle_request()  # just handle a single request then quit
    return server.auth_code, server.error_message
