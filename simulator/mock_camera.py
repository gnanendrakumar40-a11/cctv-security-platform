import http.server
import socketserver
import socket
import threading
import time
import urllib.parse

HTTP_PORT = 8081
RTSP_PORT = 554
DAHUA_PORT = 37777

# Default mock credentials
VALID_USER = "admin"
VALID_PASS = "admin123"

class MockCameraHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Responds with realistic CCTV web management headers and handles authentication."""
    
    def _send_page(self, title: str, body_html: str):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Server", "Embedded-Web-Server/3.1 (Hikvision-IPCam)")
        self.end_headers()
        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>{title}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f8; }}
                    .card {{ background: white; padding: 24px; border-radius: 8px; max-width: 450px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                    h2 {{ color: #1f2937; margin-top: 0; }}
                    input[type="text"], input[type="password"] {{ width: 90%; padding: 8px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; }}
                    input[type="submit"] {{ background: #2563eb; color: white; border: none; padding: 10px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; }}
                    input[type="submit"]:hover {{ background: #1d4ed8; }}
                    .badge {{ background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; font-size: 0.85rem; font-weight: bold; }}
                    .error {{ color: #dc2626; font-size: 0.9rem; margin-bottom: 12px; }}
                </style>
            </head>
            <body>
                <div class="card">
                    {body_html}
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        body = f"""
            <h2>Hikvision IP Camera System</h2>
            <p>Status: <span class="badge">Active</span> | Firmware: v5.5.0 build 240829</p>
            <form method="POST">
                <label><strong>Username:</strong></label><br/>
                <input type="text" name="user" placeholder="admin" required/><br/>
                <label><strong>Password:</strong></label><br/>
                <input type="password" name="pass" placeholder="admin123" required/><br/><br/>
                <input type="submit" value="Login to Device"/>
            </form>
        """
        self._send_page("Hikvision Web Management Portal", body)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed = urllib.parse.parse_qs(post_data)
        
        user = parsed.get('user', [''])[0]
        password = parsed.get('pass', [''])[0]

        if user == VALID_USER and password == VALID_PASS:
            body = f"""
                <h2>Camera Console: Authenticated</h2>
                <p>Welcome, <strong>{user}</strong>!</p>
                <hr/>
                <p><strong>Device Model:</strong> DS-2CD2042WD-I</p>
                <p><strong>RTSP Video Stream:</strong> <code>rtsp://127.0.0.1:554/live/ch0</code></p>
                <p><strong>Resolution:</strong> 1920x1080 @ 30fps</p>
                <br/>
                <a href="/">Log out</a>
            """
            self._send_page("Hikvision Console - Logged In", body)
        else:
            body = f"""
                <h2>Hikvision IP Camera System</h2>
                <p class="error">Authentication Failed: Invalid credentials.</p>
                <form method="POST">
                    <label><strong>Username:</strong></label><br/>
                    <input type="text" name="user" value="{user}" required/><br/>
                    <label><strong>Password:</strong></label><br/>
                    <input type="password" name="pass" required/><br/><br/>
                    <input type="submit" value="Login to Device"/>
                </form>
            """
            self._send_page("Hikvision Web Management Portal", body)

    def log_message(self, format, *args):
        pass

def run_http_service():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", HTTP_PORT), MockCameraHTTPHandler) as httpd:
        print(f"[*] Mock HTTP Service running on port {HTTP_PORT} (Web Management)")
        httpd.serve_forever()

def run_raw_port_listener(port: int, service_name: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("0.0.0.0", port))
        sock.listen(5)
        print(f"[*] Mock {service_name} Listener active on port {port}")
        while True:
            conn, _ = sock.accept()
            conn.close()
    except Exception as e:
        print(f"[-] Could not bind port {port} ({service_name}): {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("    STARTING MOCK CCTV / DVR SIMULATION APPLIANCE")
    print("=" * 60)

    http_thread = threading.Thread(target=run_http_service, daemon=True)
    http_thread.start()

    rtsp_thread = threading.Thread(target=run_raw_port_listener, args=(RTSP_PORT, "RTSP Streaming"), daemon=True)
    rtsp_thread.start()

    dahua_thread = threading.Thread(target=run_raw_port_listener, args=(DAHUA_PORT, "Dahua Management"), daemon=True)
    dahua_thread.start()

    print("\n[+] Mock Surveillance Device online! Press Ctrl+C to terminate.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Shutting down mock device...")