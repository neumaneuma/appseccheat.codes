from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


class AdminHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/reset_admin_password":
            self.send_error(404, message="Path not found")
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            response = "Admin password reset to admin\n".encode("utf8")
            self.wfile.write(response)


server_address = ("127.0.0.1", 8484)
httpd = ThreadingHTTPServer(server_address, AdminHandler)
httpd.serve_forever()
